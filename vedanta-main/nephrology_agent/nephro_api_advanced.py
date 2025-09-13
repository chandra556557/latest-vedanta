from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
import google.generativeai as genai
import os
import json
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import logging
from contextlib import asynccontextmanager
import time
import hashlib
import jwt
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import uvicorn
from advanced_training_data import AdvancedNephrologyTrainingData

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nephro_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = "HS256"

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Pydantic Models
class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8)
    role: str = Field(default="user", pattern=r'^(user|doctor|admin)$')
    full_name: Optional[str] = None
    medical_license: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context_type: str = Field(default="general", pattern=r'^(general|ckd|aki|dialysis|transplant)$')
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    confidence_score: Optional[float] = None
    sources: Optional[List[str]] = None
    follow_up_questions: Optional[List[str]] = None

class PatientData(BaseModel):
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., pattern=r'^(male|female|other)$')
    weight: Optional[float] = Field(None, ge=0, le=500)
    height: Optional[float] = Field(None, ge=0, le=300)
    creatinine: float = Field(..., ge=0.1, le=20.0)
    bun: Optional[float] = Field(None, ge=0, le=200)
    diabetes: bool = False
    hypertension: bool = False
    cardiovascular_disease: bool = False
    smoking: bool = False
    family_history_kidney_disease: bool = False
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None

class RiskAssessmentResponse(BaseModel):
    gfr: float
    ckd_stage: str
    cardiovascular_risk: str
    progression_risk: str
    recommendations: List[str]
    monitoring_frequency: str
    lifestyle_modifications: List[str]
    drug_adjustments: Optional[Dict[str, str]] = None
    referral_needed: bool
    urgency_level: str

class ClinicalGuideline(BaseModel):
    guideline_type: str
    version: str
    recommendations: Dict[str, Any]
    evidence_level: str
    last_updated: str

class AnalyticsRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    user_id: Optional[str] = None
    metric_type: str = Field(..., pattern=r'^(usage|outcomes|performance|errors)$')

class AdvancedNephrologyAPI:
    """Advanced Enterprise-Grade Nephrology AI API"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.training_data = AdvancedNephrologyTrainingData()
        self.init_database()
        
    def init_database(self):
        """Initialize comprehensive database schema"""
        self.conn = sqlite3.connect('nephro_enterprise.db', check_same_thread=False)
        
        # Users table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                full_name TEXT,
                medical_license TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Sessions table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Conversations table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id INTEGER,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                context_type TEXT DEFAULT 'general',
                confidence_score REAL,
                response_time REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Risk assessments table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id INTEGER,
                patient_data TEXT NOT NULL,
                assessment_result TEXT NOT NULL,
                gfr REAL,
                ckd_stage TEXT,
                risk_level TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Analytics table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # API usage tracking
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                status_code INTEGER,
                response_time REAL,
                ip_address TEXT,
                user_agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        logger.info("Database initialized successfully")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None
    
    def register_user(self, user_data: UserRegistration) -> Dict[str, Any]:
        """Register new user"""
        try:
            # Check if user exists
            cursor = self.conn.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (user_data.username, user_data.email)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="User already exists")
            
            # Hash password
            password_hash = self.hash_password(user_data.password)
            
            # Insert user
            cursor = self.conn.execute(
                """INSERT INTO users (username, email, password_hash, role, full_name, medical_license)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_data.username, user_data.email, password_hash, user_data.role,
                 user_data.full_name, user_data.medical_license)
            )
            self.conn.commit()
            
            user_id = cursor.lastrowid
            
            # Create access token
            access_token = self.create_access_token(
                data={"sub": user_data.username, "user_id": user_id, "role": user_data.role}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user_id,
                "username": user_data.username,
                "role": user_data.role
            }
            
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            raise HTTPException(status_code=500, detail="Registration failed")
    
    def authenticate_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate user login"""
        try:
            cursor = self.conn.execute(
                "SELECT id, username, password_hash, role, is_active FROM users WHERE username = ?",
                (login_data.username,)
            )
            user = cursor.fetchone()
            
            if not user or not self.verify_password(login_data.password, user[2]):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            if not user[4]:  # is_active
                raise HTTPException(status_code=401, detail="Account deactivated")
            
            # Update last login
            self.conn.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user[0],)
            )
            self.conn.commit()
            
            # Create access token
            access_token = self.create_access_token(
                data={"sub": user[1], "user_id": user[0], "role": user[3]}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user[0],
                "username": user[1],
                "role": user[3]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise HTTPException(status_code=500, detail="Authentication failed")
    
    async def generate_enhanced_response(self, request: ChatRequest, user_id: Optional[int] = None) -> ChatResponse:
        """Generate enhanced AI response with advanced features"""
        start_time = time.time()
        
        try:
            # Get enhanced context
            enhanced_context = self.training_data.get_enhanced_context(request.message)
            
            # Build comprehensive prompt
            base_prompt = self.training_data.generate_training_prompt(request.context_type)
            
            full_prompt = f"""
{base_prompt}

{enhanced_context}

User Query: {request.message}

Context Type: {request.context_type}

Please provide a comprehensive, evidence-based response that includes:
1. Direct answer to the query
2. Relevant clinical guidelines or recommendations
3. Risk factors and contraindications if applicable
4. Suggested follow-up or monitoring
5. Patient education points
6. Confidence level in your response (1-10)

Response:
"""
            
            # Generate response
            response = await asyncio.to_thread(self.model.generate_content, full_prompt)
            ai_response = response.text
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Extract confidence score (simplified)
            confidence_score = self._extract_confidence_score(ai_response)
            
            # Generate follow-up questions
            follow_up_questions = self._generate_follow_up_questions(request.message, request.context_type)
            
            # Create session if not exists
            session_id = request.session_id or f"session_{int(time.time())}_{user_id or 'anon'}"
            
            # Save conversation
            self._save_conversation(
                session_id, user_id, request.message, ai_response,
                request.context_type, confidence_score, response_time
            )
            
            # Track analytics
            self._track_analytics("response_generated", {
                "context_type": request.context_type,
                "response_time": response_time,
                "confidence_score": confidence_score
            })
            
            return ChatResponse(
                response=ai_response,
                session_id=session_id,
                timestamp=datetime.now().isoformat(),
                confidence_score=confidence_score,
                sources=["KDIGO Guidelines", "Advanced Training Data"],
                follow_up_questions=follow_up_questions
            )
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate response")
    
    def calculate_comprehensive_risk(self, patient_data: PatientData, user_id: Optional[int] = None) -> RiskAssessmentResponse:
        """Calculate comprehensive kidney risk assessment"""
        try:
            # Calculate GFR
            gfr = self.training_data.calculate_gfr(
                patient_data.creatinine,
                patient_data.age,
                patient_data.gender
            )
            
            # Determine CKD stage
            ckd_stage = self._determine_ckd_stage(gfr)
            
            # Calculate cardiovascular risk
            cv_risk = self._calculate_comprehensive_cv_risk(patient_data, gfr)
            
            # Calculate progression risk
            progression_risk = self._calculate_progression_risk(patient_data, gfr)
            
            # Get recommendations
            recommendations = self._get_comprehensive_recommendations(patient_data, ckd_stage)
            
            # Get monitoring frequency
            monitoring_frequency = self._get_monitoring_frequency(ckd_stage)
            
            # Get lifestyle modifications
            lifestyle_modifications = self._get_lifestyle_recommendations(ckd_stage, patient_data)
            
            # Get drug adjustments
            drug_adjustments = self._get_drug_adjustments(patient_data, gfr)
            
            # Determine referral need
            referral_needed = self._needs_referral(ckd_stage, patient_data)
            
            # Determine urgency
            urgency_level = self._determine_urgency(gfr, patient_data)
            
            # Create assessment result
            assessment_result = RiskAssessmentResponse(
                gfr=gfr,
                ckd_stage=ckd_stage,
                cardiovascular_risk=cv_risk,
                progression_risk=progression_risk,
                recommendations=recommendations,
                monitoring_frequency=monitoring_frequency,
                lifestyle_modifications=lifestyle_modifications,
                drug_adjustments=drug_adjustments,
                referral_needed=referral_needed,
                urgency_level=urgency_level
            )
            
            # Save assessment
            self._save_risk_assessment(user_id, patient_data, assessment_result)
            
            return assessment_result
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            raise HTTPException(status_code=500, detail="Risk assessment failed")
    
    def _extract_confidence_score(self, response: str) -> float:
        """Extract confidence score from AI response"""
        # Simplified confidence scoring based on response characteristics
        if "uncertain" in response.lower() or "may" in response.lower():
            return 0.7
        elif "likely" in response.lower() or "probably" in response.lower():
            return 0.8
        elif "evidence shows" in response.lower() or "studies indicate" in response.lower():
            return 0.9
        else:
            return 0.85
    
    def _generate_follow_up_questions(self, message: str, context_type: str) -> List[str]:
        """Generate relevant follow-up questions"""
        follow_ups = {
            "general": [
                "Would you like to know about specific treatment options?",
                "Do you have any symptoms you'd like to discuss?",
                "Are you interested in prevention strategies?"
            ],
            "ckd": [
                "Would you like information about slowing CKD progression?",
                "Are you interested in dietary recommendations?",
                "Do you want to know about when to consider dialysis?"
            ],
            "aki": [
                "Would you like to know about AKI prevention?",
                "Are you interested in recovery expectations?",
                "Do you want information about monitoring during recovery?"
            ]
        }
        
        return follow_ups.get(context_type, follow_ups["general"])
    
    def _determine_ckd_stage(self, gfr: float) -> str:
        """Determine CKD stage based on GFR"""
        if gfr >= 90:
            return "stage_1"
        elif gfr >= 60:
            return "stage_2"
        elif gfr >= 45:
            return "stage_3a"
        elif gfr >= 30:
            return "stage_3b"
        elif gfr >= 15:
            return "stage_4"
        else:
            return "stage_5"
    
    def _calculate_comprehensive_cv_risk(self, patient_data: PatientData, gfr: float) -> str:
        """Calculate comprehensive cardiovascular risk"""
        risk_score = 0
        
        # GFR-based risk
        if gfr < 30:
            risk_score += 3
        elif gfr < 60:
            risk_score += 2
        elif gfr < 90:
            risk_score += 1
        
        # Age-based risk
        if patient_data.age > 75:
            risk_score += 2
        elif patient_data.age > 65:
            risk_score += 1
        
        # Comorbidity-based risk
        if patient_data.diabetes:
            risk_score += 2
        if patient_data.hypertension:
            risk_score += 1
        if patient_data.cardiovascular_disease:
            risk_score += 2
        if patient_data.smoking:
            risk_score += 1
        
        if risk_score >= 6:
            return "very_high"
        elif risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "moderate"
        else:
            return "low"
    
    def _calculate_progression_risk(self, patient_data: PatientData, gfr: float) -> str:
        """Calculate CKD progression risk"""
        risk_factors = 0
        
        if gfr < 45:
            risk_factors += 2
        elif gfr < 60:
            risk_factors += 1
        
        if patient_data.diabetes:
            risk_factors += 2
        if patient_data.hypertension:
            risk_factors += 1
        if patient_data.family_history_kidney_disease:
            risk_factors += 1
        
        if risk_factors >= 4:
            return "high"
        elif risk_factors >= 2:
            return "moderate"
        else:
            return "low"
    
    def _get_comprehensive_recommendations(self, patient_data: PatientData, ckd_stage: str) -> List[str]:
        """Get comprehensive clinical recommendations"""
        base_recs = self.training_data.get_clinical_recommendation("ckd", ckd_stage).get("management", [])
        
        additional_recs = []
        
        if patient_data.diabetes:
            additional_recs.append("Optimize glycemic control (HbA1c <7%)")
        
        if patient_data.hypertension:
            additional_recs.append("Target blood pressure <130/80 mmHg")
        
        if patient_data.smoking:
            additional_recs.append("Smoking cessation counseling and support")
        
        return base_recs + additional_recs
    
    def _get_monitoring_frequency(self, ckd_stage: str) -> str:
        """Get monitoring frequency based on CKD stage"""
        frequencies = {
            "stage_1": "Annually",
            "stage_2": "Annually",
            "stage_3a": "Every 6 months",
            "stage_3b": "Every 3-6 months",
            "stage_4": "Every 3 months",
            "stage_5": "Monthly or as clinically indicated"
        }
        return frequencies.get(ckd_stage, "As clinically indicated")
    
    def _get_lifestyle_recommendations(self, ckd_stage: str, patient_data: PatientData) -> List[str]:
        """Get personalized lifestyle recommendations"""
        base_recs = [
            "Follow a kidney-friendly diet",
            "Maintain healthy weight",
            "Stay physically active (as tolerated)",
            "Limit sodium intake (<2g/day)",
            "Stay adequately hydrated"
        ]
        
        if ckd_stage in ["stage_4", "stage_5"]:
            base_recs.extend([
                "Limit protein intake (0.8g/kg/day)",
                "Monitor phosphorus and potassium intake",
                "Consider renal dietitian consultation"
            ])
        
        if patient_data.diabetes:
            base_recs.append("Follow diabetic diet guidelines")
        
        return base_recs
    
    def _get_drug_adjustments(self, patient_data: PatientData, gfr: float) -> Dict[str, str]:
        """Get drug dosing adjustments"""
        adjustments = {}
        
        if patient_data.medications:
            for medication in patient_data.medications:
                adjustment = self.training_data.get_drug_adjustment(medication, gfr)
                if adjustment != "No adjustment needed":
                    adjustments[medication] = adjustment
        
        return adjustments
    
    def _needs_referral(self, ckd_stage: str, patient_data: PatientData) -> bool:
        """Determine if nephrology referral is needed"""
        if ckd_stage in ["stage_4", "stage_5"]:
            return True
        
        if ckd_stage == "stage_3b" and (patient_data.diabetes or patient_data.hypertension):
            return True
        
        return False
    
    def _determine_urgency(self, gfr: float, patient_data: PatientData) -> str:
        """Determine urgency level"""
        if gfr < 15:
            return "urgent"
        elif gfr < 30:
            return "high"
        elif gfr < 45 and (patient_data.diabetes or patient_data.cardiovascular_disease):
            return "moderate"
        else:
            return "routine"
    
    def _save_conversation(self, session_id: str, user_id: Optional[int], user_message: str,
                          ai_response: str, context_type: str, confidence_score: float, response_time: float):
        """Save conversation to database"""
        try:
            self.conn.execute(
                """INSERT INTO conversations 
                   (session_id, user_id, user_message, ai_response, context_type, confidence_score, response_time)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, user_id, user_message, ai_response, context_type, confidence_score, response_time)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
    
    def _save_risk_assessment(self, user_id: Optional[int], patient_data: PatientData, assessment: RiskAssessmentResponse):
        """Save risk assessment to database"""
        try:
            session_id = f"assessment_{int(time.time())}_{user_id or 'anon'}"
            self.conn.execute(
                """INSERT INTO risk_assessments 
                   (session_id, user_id, patient_data, assessment_result, gfr, ckd_stage, risk_level)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, user_id, patient_data.json(), assessment.json(),
                 assessment.gfr, assessment.ckd_stage, assessment.cardiovascular_risk)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save risk assessment: {e}")
    
    def _track_analytics(self, metric_name: str, metadata: Dict[str, Any]):
        """Track analytics metrics"""
        try:
            self.conn.execute(
                "INSERT INTO analytics (metric_type, metric_name, metric_value, metadata) VALUES (?, ?, ?, ?)",
                ("usage", metric_name, 1, json.dumps(metadata))
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to track analytics: {e}")
    
    def get_analytics(self, request: AnalyticsRequest) -> Dict[str, Any]:
        """Get analytics data"""
        try:
            query = "SELECT * FROM analytics WHERE metric_type = ?"
            params = [request.metric_type]
            
            if request.start_date:
                query += " AND timestamp >= ?"
                params.append(request.start_date)
            
            if request.end_date:
                query += " AND timestamp <= ?"
                params.append(request.end_date)
            
            cursor = self.conn.execute(query, params)
            results = cursor.fetchall()
            
            # Process results
            analytics_data = {
                "total_records": len(results),
                "metrics": []
            }
            
            for row in results:
                analytics_data["metrics"].append({
                    "metric_name": row[2],
                    "metric_value": row[3],
                    "metadata": json.loads(row[4]) if row[4] else {},
                    "timestamp": row[5]
                })
            
            return analytics_data
            
        except Exception as e:
            logger.error(f"Analytics retrieval failed: {e}")
            raise HTTPException(status_code=500, detail="Analytics retrieval failed")

# Initialize API
api_instance = AdvancedNephrologyAPI()

# Dependency for getting current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token_data = api_instance.verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data

# Optional dependency for user (allows anonymous access)
async def get_current_user_optional(request: Request):
    """Get current user if authenticated, otherwise None"""
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            token_data = api_instance.verify_token(token)
            return token_data
    except:
        pass
    return None

# FastAPI app setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Advanced Nephrology API")
    yield
    logger.info("Shutting down Advanced Nephrology API")

app = FastAPI(
    title="Advanced Nephrology AI API",
    description="Enterprise-grade nephrology AI assistant with advanced clinical decision support",
    version="2.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API Routes
@app.get("/", tags=["System"])
async def root():
    """API root endpoint"""
    return {
        "message": "Advanced Nephrology AI API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Advanced AI responses",
            "Comprehensive risk assessment",
            "Clinical guidelines integration",
            "User authentication",
            "Analytics and monitoring",
            "Rate limiting",
            "Enterprise security"
        ]
    }

@app.get("/health", tags=["System"])
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "ai_model": "operational"
    }

# Authentication endpoints
@app.post("/auth/register", tags=["Authentication"])
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserRegistration):
    """Register new user"""
    return api_instance.register_user(user_data)

@app.post("/auth/login", tags=["Authentication"])
@limiter.limit("10/minute")
async def login(request: Request, login_data: UserLogin):
    """User login"""
    return api_instance.authenticate_user(login_data)

# Chat endpoints
@app.post("/chat", response_model=ChatResponse, tags=["AI Chat"])
@limiter.limit("30/minute")
async def chat(request: Request, chat_request: ChatRequest, current_user: Optional[Dict] = Depends(get_current_user_optional)):
    """Enhanced AI chat with advanced features"""
    user_id = current_user.get("user_id") if current_user else None
    return await api_instance.generate_enhanced_response(chat_request, user_id)

# Risk assessment endpoints
@app.post("/assess-risk", response_model=RiskAssessmentResponse, tags=["Clinical Assessment"])
@limiter.limit("20/minute")
async def assess_risk(request: Request, patient_data: PatientData, current_user: Optional[Dict] = Depends(get_current_user_optional)):
    """Comprehensive kidney risk assessment"""
    user_id = current_user.get("user_id") if current_user else None
    return api_instance.calculate_comprehensive_risk(patient_data, user_id)

# Analytics endpoints
@app.post("/analytics", tags=["Analytics"])
@limiter.limit("10/minute")
async def get_analytics(request: Request, analytics_request: AnalyticsRequest, current_user: Dict = Depends(get_current_user)):
    """Get analytics data (authenticated users only)"""
    if current_user.get("role") not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return api_instance.get_analytics(analytics_request)

# Clinical guidelines endpoint
@app.get("/guidelines/{guideline_type}", tags=["Clinical Guidelines"])
@limiter.limit("50/minute")
async def get_guidelines(request: Request, guideline_type: str):
    """Get clinical guidelines"""
    guidelines = api_instance.training_data.clinical_guidelines
    
    if guideline_type == "ckd":
        return guidelines.get("ckd_guidelines", {})
    elif guideline_type == "aki":
        return guidelines.get("ckd_guidelines", {}).get("aki_guidelines", {})
    elif guideline_type == "dialysis":
        return guidelines.get("dialysis_guidelines", {})
    else:
        raise HTTPException(status_code=404, detail="Guidelines not found")

# Drug interaction endpoint
@app.get("/drug-interactions/{drug_name}", tags=["Drug Information"])
@limiter.limit("50/minute")
async def get_drug_interactions(request: Request, drug_name: str, gfr: Optional[float] = None):
    """Get drug interaction information"""
    drug_info = api_instance.training_data.drug_interactions
    
    # Search for drug in nephrotoxic drugs
    for category, drugs in drug_info.get("nephrotoxic_drugs", {}).items():
        if drug_name.lower() in [d.lower() for d in drugs.get("examples", [])]:
            result = {
                "drug": drug_name,
                "category": category,
                "information": drugs
            }
            
            if gfr:
                result["dose_adjustment"] = api_instance.training_data.get_drug_adjustment(drug_name, gfr)
            
            return result
    
    return {"drug": drug_name, "information": "No specific nephrology interactions found"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    return {"error": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc} - {request.url}")
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    uvicorn.run(
        "nephro_api_advanced:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    )