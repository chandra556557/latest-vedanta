import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
if GEMINI_API_KEY and GEMINI_API_KEY != "your-api-key-here":
    genai.configure(api_key=GEMINI_API_KEY)

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

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

# FastAPI app
app = FastAPI(
    title="Nephrology AI Agent API",
    description="Specialized AI assistant for nephrology and kidney health",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NephrologyAIAgent:
    def __init__(self):
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
    
    def generate_response(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        try:
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
            except:
                # Fallback structure
                result = {
                    "content": response.text,
                    "related_topics": ["Kidney Function", "CKD Management", "Dialysis", "Kidney Transplant", "Preventive Care"]
                }
            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating education content: {str(e)}")

# Initialize the AI agent
nephro_agent = NephrologyAIAgent()

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

@app.post("/chat", response_model=ChatResponse)
async def chat_with_nephro_agent(request: ChatRequest):
    """Chat with the nephrology AI agent"""
    try:
        response_text = nephro_agent.generate_response(
            request.message, 
            request.conversation_history
        )
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    uvicorn.run(app, host="0.0.0.0", port=8002)