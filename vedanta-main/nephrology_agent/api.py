import os
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Literal
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple in-memory cache
cache_store = {}

# Initialize FastAPI
app = FastAPI(
    title="Nephrology AI Agent API",
    description="Specialized AI assistant for nephrology and kidney health",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini if API key is available
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)

# Pydantic Models
class ModelConfig(BaseModel):
    model_type: str = "gemini"
    temperature: float = 0.7
    max_tokens: Optional[int] = 1000

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []
    model_settings: Optional[ModelConfig] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model_used: str

class SymptomAssessmentRequest(BaseModel):
    symptoms: List[str]
    medical_history: Dict[str, bool]
    age: Optional[int] = None
    gender: Optional[str] = None

class AssessmentResponse(BaseModel):
    assessment: str
    risk_level: str
    recommendations: List[str]
    urgent_care_needed: bool

class KidneyEducationRequest(BaseModel):
    topic: str

class EducationResponse(BaseModel):
    content: str
    related_topics: List[str]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "gemini": bool(GOOGLE_API_KEY)
        }
    }

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai_agent(chat_request: ChatRequest):
    """Chat with the AI agent using Gemini"""
    try:
        if not GOOGLE_API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="Google API key not configured. Please set GOOGLE_API_KEY in your environment variables."
            )
            
        config = chat_request.model_settings or ModelConfig()
        prompt = chat_request.message
        cache_key = f"chat_{hash(prompt)}"
        
        # Simple cache check (5 minute cache)
        if cache_key in cache_store:
            cached = cache_store[cache_key]
            if (datetime.utcnow() - cached['timestamp']).total_seconds() < 300:
                return cached['response']
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Build conversation context
        context = """You are Dr. Nephro, a specialized AI assistant for nephrology and kidney health.
        You have extensive knowledge about kidney diseases, treatments, and general nephrology.
        Be professional, empathetic, and provide accurate medical information.
        Always recommend consulting with a healthcare professional for medical advice.
        """
        
        # Format conversation history
        messages = [{"role": "user", "parts": [context]}]
        for msg in chat_request.conversation_history:
            messages.append({"role": msg.role, "parts": [msg.content]})
        messages.append({"role": "user", "parts": [prompt]})
        
        # Generate response
        response = model.generate_content(
            messages,
            generation_config={
                'temperature': config.temperature,
                'max_output_tokens': config.max_tokens or 1000,
            }
        )
        
        response_text = response.text
        
        # Cache the response
        cache_store[cache_key] = {
            'response': ChatResponse(
                response=response_text,
                timestamp=datetime.utcnow().isoformat(),
                model_used="gemini"
            ),
            'timestamp': datetime.utcnow()
        }
        
        return cache_store[cache_key]['response']
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )

# Additional endpoints for other features
@app.post("/api/assess-symptoms", response_model=AssessmentResponse)
async def assess_symptoms(request: SymptomAssessmentRequest):
    """Assess kidney-related symptoms"""
    try:
        # This is a simplified version - in a real app, you'd want more sophisticated logic
        return AssessmentResponse(
            assessment="Please consult with a healthcare professional for accurate symptom assessment.",
            risk_level="moderate",
            recommendations=[
                "Drink plenty of water", 
                "Monitor your symptoms", 
                "Contact a healthcare provider"
            ],
            urgent_care_needed=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/education/{topic}", response_model=EducationResponse)
async def get_education(topic: str):
    """Get educational content about kidney health topics"""
    try:
        # This is a simplified version - in a real app, you'd want to fetch from a knowledge base
        return EducationResponse(
            content=f"Educational content about {topic} would appear here. This is a placeholder response.",
            related_topics=["Kidney Function", "CKD Management", "Dialysis"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
