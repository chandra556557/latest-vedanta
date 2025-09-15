from typing import Optional, Dict, Any, List, Union
import aiohttp
import asyncio
import os
import json
import logging
from functools import lru_cache
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=300)  # 300 seconds timeout for Phi-3:3.8b
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds

class LlamaService:
    _instance = None
    _session = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LlamaService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize Llama service with connection pooling and caching
        
        Args:
            base_url: Base URL of your Llama 3.2 API server
            api_key: API key if required by your Llama server
        """
        if self._initialized:
            return
            
        self.base_url = base_url or os.getenv("LLAMA_API_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("LLAMA_API_KEY")
        self._initialized = True
        
        # Connection pool for HTTP requests
        connector = aiohttp.TCPConnector(
            limit=100,  # Max number of simultaneous connections
            ttl_dns_cache=300  # Cache DNS for 5 minutes
        )
        
        self._session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                "User-Agent": "Vedanta-AI-Backend/1.0"
            },
            connector=connector,
            timeout=DEFAULT_TIMEOUT,
            json_serialize=json.dumps
        )
        
        logger.info(f"LlamaService initialized with base URL: {self.base_url}")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("Closed LlamaService HTTP session")
    
    @lru_cache(maxsize=1000)
    def _get_cache_key(self, prompt: str, conversation_hash: int, **kwargs) -> str:
        """Generate a cache key for the request"""
        return f"llama_resp:{hash(prompt)}:{conversation_hash}:{hash(frozenset(kwargs.items()))}"
    
    async def generate_response_async(
        self, 
        prompt: str, 
        conversation_history: List[Dict[str, str]] = None,
        session: aiohttp.ClientSession = None,
        **kwargs
    ) -> str:
        """
        Generate a response using Llama 3.2 asynchronously with retry logic and caching
        
        Args:
            prompt: User's input message
            conversation_history: List of previous messages in the conversation
            session: Optional aiohttp session for connection pooling
            **kwargs: Additional parameters for the model
            
        Returns:
            Generated response text
            
        Raises:
            HTTPException: If the request fails after retries
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        conversation_history = conversation_history or []
        
        # Create a stable hash of the conversation for caching
        conversation_hash = hash(tuple((m.get('role', ''), m.get('content', '')) 
                                    for m in conversation_history))
        
        # Check cache first
        cache_key = self._get_cache_key(prompt, conversation_hash, **kwargs)
        if hasattr(self, '_cache') and cache_key in self._cache:
            logger.debug(f"Cache hit for key: {cache_key}")
            return self._cache[cache_key]
        
        # Format messages for the API
        messages = [{"role": "system", "content": "You are a helpful AI assistant specialized in nephrology and kidney health."}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        # Prepare the request payload for Ollama API
        payload = {
            "model": "phi3:3.8b",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": min(float(kwargs.get('temperature', 0.7)), 1.0),
                "num_predict": min(int(kwargs.get('max_tokens', 1000)), 4000),
                "top_p": float(kwargs.get('top_p', 0.9))
            }
        }
        
        # Use provided session or ensure we have a valid session
        if session:
            use_session = session
            close_session = False
        elif self._session and not self._session.closed:
            use_session = self._session
            close_session = False
        else:
            # Create a new session if needed
            connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
            use_session = aiohttp.ClientSession(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "User-Agent": "Vedanta-AI-Backend/1.0"
                },
                connector=connector,
                timeout=DEFAULT_TIMEOUT
            )
            close_session = True
        
        last_exception = None
        
        for attempt in range(MAX_RETRIES):
            try:
                # Make the API request with timeout to Ollama
                async with use_session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=DEFAULT_TIMEOUT
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Llama API error ({response.status}): {error_text}")
                        
                        if response.status == 429:  # Rate limit
                            retry_after = int(response.headers.get('Retry-After', '1'))
                            await asyncio.sleep(retry_after)
                            continue
                            
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Llama API error: {error_text}"
                        )
                    
                    result = await response.json()
                    # Ollama returns response in 'message' -> 'content' format
                    response_text = result.get('message', {}).get('content', '')
                    
                    # Cache the successful response
                    if not hasattr(self, '_cache'):
                        self._cache = {}
                    self._cache[cache_key] = response_text
                    
                    return response_text
                    
            except asyncio.TimeoutError:
                last_exception = HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="Request to Llama API timed out"
                )
                logger.warning(f"Llama API timeout (attempt {attempt + 1}/{MAX_RETRIES})")
                
            except aiohttp.ClientError as e:
                last_exception = HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Error connecting to Llama API: {str(e)}"
                )
                logger.error(f"Llama API connection error: {str(e)}")
                
            except Exception as e:
                last_exception = HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(e)}"
                )
                logger.exception("Unexpected error in generate_response_async")
            
            # Exponential backoff before retry
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                await asyncio.sleep(wait_time)
        
        # Close session if we created it
        if close_session and use_session and not use_session.closed:
            await use_session.close()
        
        # If we get here, all retries failed
        logger.error(f"All {MAX_RETRIES} attempts to call Llama API failed")
        raise last_exception or HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response after multiple attempts"
        )

    def get_embeddings(self, text: str) -> list[float]:
        """
        Get embeddings for the input text
        
        Args:
            text: Input text to get embeddings for
            
        Returns:
            List of embedding values
        """
        try:
            response = self._session.post(
                "/v1/embeddings",
                json={"input": text, "model": "llama-3.2"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except aiohttp.ClientError as e:
            print(f"Error getting embeddings: {str(e)}")
            raise

    # Synchronous wrapper for backward compatibility
    def generate_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None, **kwargs) -> str:
        """
        Synchronous wrapper around generate_response_async
        Note: Not recommended for production use with async frameworks
        """
        import asyncio
        
        # Create a new event loop for the synchronous call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(
                self.generate_response_async(prompt, conversation_history, **kwargs)
            )
        finally:
            loop.close()


# Example usage
if __name__ == "__main__":
    import asyncio
    import time
    
    async def main():
        # Initialize the service with context manager
        async with LlamaService() as llama:
            # Example conversation
            conversation = [
                {"role": "user", "content": "What is chronic kidney disease?"},
                {"role": "assistant", "content": "Chronic kidney disease (CKD) is a long-term condition..."}
            ]
            
            try:
                # Generate a response asynchronously
                response = await llama.generate_response_async(
                    "What are the symptoms?",
                    conversation_history=conversation,
                    temperature=0.7,
                    max_tokens=500
                )
                print("Response:", response)
                
                # Test caching
                print("\nTesting caching (should be instant):")
                start_time = time.time()
                cached_response = await llama.generate_response_async(
                    "What are the symptoms?",
                    conversation_history=conversation,
                    temperature=0.7,
                    max_tokens=500
                )
                print(f"Cached response (took {time.time() - start_time:.4f}s):", cached_response[:100] + "...")
                
            except Exception as e:
                print(f"Error: {str(e)}")
    
    # Run the async main function
    asyncio.run(main())
