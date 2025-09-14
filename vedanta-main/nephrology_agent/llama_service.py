from typing import Optional, Dict, Any
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LlamaService:
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize Llama service
        
        Args:
            base_url: Base URL of your Llama 3.2 API server
            api_key: API key if required by your Llama server
        """
        self.base_url = base_url or os.getenv("LLAMA_API_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("LLAMA_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
    
    def generate_response(self, prompt: str, conversation_history: list = None, **kwargs) -> str:
        """
        Generate a response using Llama 3.2
        
        Args:
            prompt: User's input message
            conversation_history: List of previous messages in the conversation
            **kwargs: Additional parameters for the model (temperature, max_tokens, etc.)
            
        Returns:
            Generated response text
        """
        if conversation_history is None:
            conversation_history = []
            
        # Format messages for the API
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        # Prepare the request payload
        payload = {
            "model": "llama-3.2",
            "messages": messages,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error calling Llama API: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise

    def get_embeddings(self, text: str) -> list[float]:
        """
        Get embeddings for the input text
        
        Args:
            text: Input text to get embeddings for
            
        Returns:
            List of embedding values
        """
        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                headers=self.headers,
                json={"input": text, "model": "llama-3.2"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except requests.exceptions.RequestException as e:
            print(f"Error getting embeddings: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Initialize the service
    llama = LlamaService()
    
    # Example chat
    response = llama.generate_response(
        "What is the capital of France?",
        temperature=0.7,
        max_tokens=100
    )
    print("Llama response:", response)
