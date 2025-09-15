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
import aiohttp
from llama_service import LlamaService

# Simple in-memory cache
cache_store = {}

# Load environment variables
load_dotenv()

# AI Model Configuration
AI_MODEL_TYPE = os.getenv('AI_MODEL_TYPE', 'llama').lower()
LLAMA_API_URL = os.getenv('LLAMA_API_URL', 'http://localhost:8000')
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')

# Initialize Gemini (fallback)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai = None
if GOOGLE_API_KEY or GEMINI_API_KEY:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY or GEMINI_API_KEY)

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

# Load environment variables
load_dotenv()

# Configure AI Model based on environment
print(f"AI Model Type: {AI_MODEL_TYPE}")
if AI_MODEL_TYPE == 'llama':
    print(f"Llama API URL: {LLAMA_API_URL}")
else:
    print("Using Gemini API as fallback")

# Pydantic models
class ModelConfig(BaseModel):
    model_type: str = AI_MODEL_TYPE
    temperature: float = 0.7
    max_tokens: Optional[int] = 1000

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    ai_model_config: Optional[ModelConfig] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    conversation_id: Optional[str] = None

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

# Simple in-memory storage for development

# FastAPI app with optimized settings
# Models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

# Duplicate ModelConfig removed - using the one defined earlier

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []
    ai_model_config: Optional[ModelConfig] = None

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

# Add request timeout middleware
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "Request timeout"}
        )

class NephrologyAIAgent:
    def __init__(self):
        self.ai_model_type = AI_MODEL_TYPE
        if genai:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.nephrology_context = """
        You are Dr. Nephro, a specialized AI assistant for nephrology and kidney health.
        You have extensive knowledge about:
        - Chronic Kidney Disease (CKD) stages and management
        - Acute Kidney Injury (AKI) diagnosis and treatment
        - Dialysis (hemodialysis and peritoneal dialysis)
        - Kidney transplantation
        - Hypertension and kidney disease
        - Diabetes and diabetic nephropathy
        - Glomerular diseases
        - Kidney stones and urological conditions
        - Electrolyte disorders
        - Fluid balance management
        - Nephrotoxic medications
        - Pediatric nephrology
        
        Always provide evidence-based medical information while emphasizing that:
        1. This is for educational purposes only
        2. Patients should always consult with their healthcare provider
        3. Emergency symptoms require immediate medical attention
        
        Be empathetic, clear, and use appropriate medical terminology with explanations.
        Provide structured, helpful responses that are easy to understand.
        """
    
    async def generate_response(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        try:
            if self.ai_model_type == 'llama':
                # Use Llama service
                conversation_msgs = []
                if conversation_history:
                    for msg in conversation_history[-5:]:  # Last 5 messages for context
                        conversation_msgs.append({
                            "role": msg.role,
                            "content": msg.content
                        })
                
                # Use the global llama_service instance with async method
                response = await llama_service.generate_response_async(
                    prompt=message,
                    conversation_history=conversation_msgs
                )
                return response
            else:
                # Use Gemini as fallback
                if not hasattr(self, 'model') or not self.model:
                    raise HTTPException(status_code=500, detail="Gemini model not initialized")
                
                # Build conversation context
                context = self.nephrology_context + "\n\n"
                
                if conversation_history:
                    context += "Previous conversation:\n"
                    for msg in conversation_history[-5:]:  # Last 5 messages for context
                        context += f"{msg.role}: {msg.content}\n"
                
                context += f"\nCurrent question: {message}\n\nProvide a comprehensive, helpful response:"
                
                response = self.model.generate_content(context)
                return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
    
    def assess_symptoms(self, symptoms: List[str], medical_history: Dict[str, bool], age: int = None, gender: str = None) -> Dict:
        try:
            assessment_prompt = f"""
            {self.nephrology_context}
            
            Provide a kidney health assessment based on:
            Symptoms: {', '.join(symptoms)}
            Medical History: {json.dumps(medical_history)}
            Age: {age if age else 'Not specified'}
            Gender: {gender if gender else 'Not specified'}
            
            Provide a JSON response with:
            1. "assessment": Detailed analysis of symptoms in relation to kidney health
            2. "risk_level": "low", "moderate", "high", or "urgent"
            3. "recommendations": Array of specific recommendations
            4. "urgent_care_needed": boolean indicating if immediate medical attention is needed
            
            Focus on kidney-related conditions and provide educational information.
            Always emphasize this is not a diagnosis and professional consultation is needed.
            """
            
            response = self.model.generate_content(assessment_prompt)
            
            # Try to parse JSON response, fallback to structured text if needed
            try:
                result = json.loads(response.text)
            except:
                # Fallback if AI doesn't return proper JSON
                result = {
                    "assessment": response.text,
                    "risk_level": "moderate",
                    "recommendations": ["Consult with a healthcare provider", "Monitor symptoms closely"],
                    "urgent_care_needed": any(urgent_symptom in ' '.join(symptoms).lower() 
                                           for urgent_symptom in ['severe pain', 'no urination', 'blood', 'chest pain'])
                }
            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in symptom assessment: {str(e)}")
    
    def get_education_content(self, topic: str) -> Dict:
        try:
            education_prompt = f"""
            {self.nephrology_context}
            
            Provide comprehensive educational content about: {topic}
            
            Structure your response as JSON with:
            1. "content": Detailed educational information about the topic
            2. "related_topics": Array of 3-5 related nephrology topics
            
            Make the content accessible to patients while maintaining medical accuracy.
            Include practical information, lifestyle tips, and when to seek medical care.
            """
            
            response = self.model.generate_content(education_prompt)
            
            try:
                result = json.loads(response.text)
                # Cache the response
                cache_store[topic] = {
                    'response': response.text,
                    'timestamp': time.time()
                }
            except:
                # Fallback structure
                result = {
                    "content": response.text,
                    "related_topics": ["Kidney Function", "CKD Management", "Dialysis", "Kidney Transplant", "Preventive Care"]
                }
            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating education content: {str(e)}")

# Initialize the AI agents
nephro_agent = NephrologyAIAgent()
llama_service = LlamaService()

# ModelConfig already defined earlier in the file

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Nephrology AI Agent API",
        "version": "1.0.0",
        "description": "Specialized AI assistant for nephrology and kidney health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": GEMINI_API_KEY != "your-api-key-here"
    }

# Cache key builder for chat responses
def chat_cache_key(
    request: Request,
    body: bytes,
    *,
    prefix: str = "fastapi-cache"
) -> str:
    from hashlib import md5
    from fastapi import Request
    
    # Create a unique key based on request data
    body_hash = md5(body).hexdigest()
    return f"{prefix}:{request.url.path}:{body_hash}"

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai_agent(chat_request: ChatRequest):
    """Chat with the AI agent using configured model (Llama 3.2 or Gemini)"""
    try:
        # Check if required API keys are configured based on model type
        if AI_MODEL_TYPE == 'llama':
            if not LLAMA_API_KEY:
                raise HTTPException(status_code=500, detail="Llama API key not configured")
        else:
            if not (GOOGLE_API_KEY or GEMINI_API_KEY):
                raise HTTPException(status_code=500, detail="Google/Gemini API key not configured")
            
        config = chat_request.ai_model_config or ModelConfig()
        prompt = chat_request.message
        cache_key = f"chat_{hash(prompt)}_{AI_MODEL_TYPE}"
        
        # Simple cache check (5 minute cache)
        if cache_key in cache_store:
            cached = cache_store[cache_key]
            if (datetime.utcnow() - cached['timestamp']).total_seconds() < 300:
                return cached['response']
        
        # Use the nephro_agent to generate response
        response_text = await nephro_agent.generate_response(
            message=prompt,
            conversation_history=chat_request.conversation_history
        )
        
        # Create response object
        response = ChatResponse(
            response=response_text,
            timestamp=datetime.utcnow().isoformat(),
            model_used=f"llama-3.2" if AI_MODEL_TYPE == 'llama' else "gemini-pro"
        )
        
        # Cache the response
        cache_store[cache_key] = {
            'response': response,
            'timestamp': datetime.utcnow()
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@app.post("/assess-symptoms", response_model=AssessmentResponse)
async def assess_kidney_symptoms(request: SymptomAssessmentRequest):
    """Assess kidney-related symptoms and provide recommendations"""
    try:
        assessment_result = nephro_agent.assess_symptoms(
            request.symptoms,
            request.medical_history,
            request.age,
            request.gender
        )
        
        return AssessmentResponse(**assessment_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/education", response_model=EducationResponse)
async def get_kidney_education(request: KidneyEducationRequest):
    """Get educational content about kidney health topics"""
    try:
        education_result = nephro_agent.get_education_content(request.topic)
        
        return EducationResponse(**education_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topics")
async def get_available_topics():
    """Get list of available nephrology topics"""
    topics = [
        "Chronic Kidney Disease (CKD)",
        "Acute Kidney Injury (AKI)",
        "Dialysis - Hemodialysis",
        "Dialysis - Peritoneal Dialysis",
        "Kidney Transplantation",
        "Diabetic Nephropathy",
        "Hypertensive Nephropathy",
        "Glomerulonephritis",
        "Kidney Stones",
        "Polycystic Kidney Disease",
        "Electrolyte Disorders",
        "Fluid Balance",
        "Nephrotoxic Medications",
        "Kidney Diet and Nutrition",
        "Pediatric Nephrology",
        "Kidney Function Tests",
        "Blood Pressure and Kidneys",
        "Pregnancy and Kidney Disease"
    ]
    
    return {"topics": topics}

@app.get("/emergency-symptoms")
async def get_emergency_symptoms():
    """Get list of kidney-related emergency symptoms"""
    emergency_symptoms = [
        "Complete absence of urination (anuria)",
        "Severe decrease in urination (oliguria)",
        "Blood in urine with severe pain",
        "Severe flank or back pain",
        "Difficulty breathing with swelling",
        "Chest pain with kidney symptoms",
        "Severe nausea and vomiting with kidney symptoms",
        "Confusion or altered mental state",
        "Severe swelling in face, legs, or abdomen",
        "Signs of severe dehydration"
    ]
    
    return {
        "emergency_symptoms": emergency_symptoms,
        "message": "If experiencing any of these symptoms, seek immediate medical attention"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Nephrology AI Backend Service...")
    print(f"Server will be available at: http://localhost:8002")
    print(f"API Documentation: http://localhost:8002/docs")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")