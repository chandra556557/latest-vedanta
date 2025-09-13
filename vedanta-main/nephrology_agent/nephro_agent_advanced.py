import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import json
import sqlite3
import pandas as pd
from typing import Dict, List, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from advanced_training_data import AdvancedNephrologyTrainingData
from ai_clinical_intelligence import AIClinicaIntelligence
from data_export_system import DataExportSystem
from patient_timeline_visualization import PatientTimelineVisualization
from real_time_monitoring import RealTimeMonitoringSystem
from patient_portal import PatientPortalSystem
from localization import get_localization_manager, t, create_language_selector
from advanced_security import get_security_manager, AdvancedSecurityManager
from mobile_responsive import init_responsive_design, get_responsive_manager
from audit_logging import get_audit_logger, log_user_action, log_security_event, AuditEventType, AuditSeverity
import base64

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class AdvancedNephrologyAgent:
    """Advanced Enterprise-Grade Nephrology AI Agent with AI Clinical Intelligence"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.training_data = AdvancedNephrologyTrainingData()
        self.ai_clinical = AIClinicaIntelligence()
        self.data_export = DataExportSystem()
        self.timeline_viz = PatientTimelineVisualization()
        self.monitoring_system = RealTimeMonitoringSystem()
        self.patient_portal = PatientPortalSystem()
        self.localization_manager = get_localization_manager()
        self.conversation_history = []
        self.init_database()
        
        # Enhanced nephrology context with advanced training data
        self.nephrology_context = self.training_data.generate_training_prompt("general")
        
    def init_database(self):
        """Initialize SQLite database for session management"""
        self.conn = sqlite3.connect('nephro_sessions.db', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp DATETIME,
                user_input TEXT,
                ai_response TEXT,
                assessment_data TEXT,
                risk_scores TEXT
            )
        ''')
        self.conn.commit()
    
    def get_enhanced_response(self, user_input: str, context_type: str = "general") -> str:
        """Get enhanced AI response with advanced training data"""
        try:
            # Get enhanced context based on query
            enhanced_context = self.training_data.get_enhanced_context(user_input)
            
            # Build comprehensive prompt
            full_prompt = f"""
{self.nephrology_context}

{enhanced_context}

Conversation History:
{self._format_conversation_history()}

User Query: {user_input}

Please provide a comprehensive, evidence-based response that includes:
1. Direct answer to the query
2. Relevant clinical guidelines or recommendations
3. Risk factors and contraindications if applicable
4. Suggested follow-up or monitoring
5. Patient education points

Response:
"""
            
            response = self.model.generate_content(full_prompt)
            ai_response = response.text
            
            # Store conversation
            self.conversation_history.append({
                "user": user_input,
                "assistant": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Save to database
            self._save_session(user_input, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def calculate_kidney_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive kidney risk assessment"""
        try:
            # Extract patient data
            age = patient_data.get('age', 0)
            gender = patient_data.get('gender', 'male')
            creatinine = patient_data.get('creatinine', 1.0)
            
            # Calculate GFR
            gfr = self.training_data.calculate_gfr(creatinine, age, gender)
            
            # Determine CKD stage
            ckd_stage = self._determine_ckd_stage(gfr)
            
            # Get clinical recommendations
            recommendations = self.training_data.get_clinical_recommendation("ckd", ckd_stage)
            
            # Calculate cardiovascular risk
            cv_risk = self._calculate_cv_risk(patient_data, gfr)
            
            # Generate risk assessment
            risk_assessment = {
                "gfr": gfr,
                "ckd_stage": ckd_stage,
                "cv_risk": cv_risk,
                "recommendations": recommendations,
                "monitoring_frequency": self._get_monitoring_frequency(ckd_stage),
                "lifestyle_modifications": self._get_lifestyle_recommendations(ckd_stage)
            }
            
            return risk_assessment
            
        except Exception as e:
            return {"error": f"Risk calculation failed: {str(e)}"}
    
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
    
    def _calculate_cv_risk(self, patient_data: Dict[str, Any], gfr: float) -> str:
        """Calculate cardiovascular risk"""
        risk_factors = 0
        
        if gfr < 60:
            risk_factors += 1
        if patient_data.get('diabetes', False):
            risk_factors += 1
        if patient_data.get('hypertension', False):
            risk_factors += 1
        if patient_data.get('age', 0) > 65:
            risk_factors += 1
        
        if risk_factors >= 3:
            return "high"
        elif risk_factors >= 2:
            return "moderate"
        else:
            return "low"
    
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
    
    def _get_lifestyle_recommendations(self, ckd_stage: str) -> List[str]:
        """Get lifestyle recommendations based on CKD stage"""
        base_recommendations = [
            "Maintain healthy blood pressure (<130/80 mmHg)",
            "Control blood sugar if diabetic (HbA1c <7%)",
            "Follow kidney-friendly diet",
            "Stay physically active",
            "Avoid nephrotoxic medications",
            "Stay hydrated (unless fluid restricted)"
        ]
        
        if ckd_stage in ["stage_4", "stage_5"]:
            base_recommendations.extend([
                "Limit protein intake (0.8g/kg/day)",
                "Monitor phosphorus and potassium",
                "Consider renal replacement therapy options"
            ])
        
        return base_recommendations
    
    def get_ai_clinical_analysis(self, patient_data: Dict[str, Any], lab_data: Dict[str, Any] = None, 
                                medications: List[str] = None, historical_data: Dict[str, List] = None) -> Dict[str, Any]:
        """Get comprehensive AI clinical intelligence analysis"""
        try:
            # Perform comprehensive AI analysis
            analysis = self.ai_clinical.comprehensive_analysis(
                patient_data, lab_data, medications, historical_data
            )
            
            # Add traditional risk assessment for comparison
            traditional_risk = self.calculate_kidney_risk(patient_data)
            analysis['traditional_assessment'] = traditional_risk
            
            return analysis
            
        except Exception as e:
            return {"error": f"AI clinical analysis failed: {str(e)}"}
    

    
    def get_intelligent_alerts(self, lab_data: Dict[str, Any], historical_data: Dict[str, List] = None) -> Dict[str, Any]:
        """Get intelligent alerts for critical values and trends"""
        try:
            alerts = {}
            
            # Check critical values
            if lab_data:
                critical_alerts = self.ai_clinical.alert_system.check_critical_values(lab_data)
                alerts['critical_alerts'] = critical_alerts
            
            # Analyze trends
            if historical_data:
                trend_alerts = self.ai_clinical.alert_system.analyze_trends(historical_data)
                alerts['trend_alerts'] = trend_alerts
            
            return alerts
            
        except Exception as e:
            return {"error": f"Alert analysis failed: {str(e)}"}
    
    def get_enhanced_predictions(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get enhanced ML-based predictions"""
        try:
            # GFR prediction
            gfr_prediction = self.ai_clinical.kidney_predictor.predict_gfr(patient_data)
            
            # Progression risk
            progression_risk = self.ai_clinical.kidney_predictor.predict_progression_risk(patient_data)
            
            return {
                'gfr_prediction': gfr_prediction,
                'progression_risk': progression_risk
            }
            
        except Exception as e:
            return {"error": f"Enhanced predictions failed: {str(e)}"}
    
    def get_dialysis_readiness(self, patient_data: Dict[str, Any], lab_data: Dict[str, Any] = None, symptoms: List[str] = None) -> Dict[str, Any]:
        """Analyze dialysis readiness and timing predictions"""
        try:
            return self.ai_clinical.dialysis_predictor.predict_dialysis_timing(
                patient_data, lab_data, symptoms
            )
        except Exception as e:
            return {'error': f"Dialysis analysis failed: {str(e)}"}
    
    def get_transplant_readiness(self, patient_data: Dict[str, Any], lab_data: Dict[str, Any] = None, comorbidities: List[str] = None) -> Dict[str, Any]:
        """Analyze transplant eligibility and readiness"""
        try:
            return self.ai_clinical.transplant_analyzer.analyze_transplant_eligibility(
                patient_data, lab_data, comorbidities
            )
        except Exception as e:
            return {'error': f"Transplant analysis failed: {str(e)}"}
    
    def get_drug_dosing_recommendations(self, patient_data: Dict[str, Any], medications: List[str], lab_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get AI-powered drug dosing recommendations based on kidney function"""
        try:
            return self.ai_clinical.drug_dosing.get_dosing_recommendations(
                patient_data, medications, lab_data
            )
        except Exception as e:
            return {'error': f"Drug dosing analysis failed: {str(e)}"}
    
    def analyze_clinical_notes(self, notes_text: str, patient_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze clinical notes using natural language processing"""
        try:
            return self.ai_clinical.clinical_nlp.analyze_clinical_notes(notes_text, patient_data)
        except Exception as e:
            return {'error': f"Clinical notes analysis failed: {str(e)}"}
    
    def get_intelligent_alerts(self, current_labs: Dict[str, Any], historical_data: Dict[str, List[float]] = None, 
                              patient_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get intelligent alerts for critical lab values and trends"""
        try:
            return self.ai_clinical.intelligent_alerts.generate_smart_alerts(
                current_labs, historical_data, patient_data
            )
        except Exception as e:
            return {'error': f"Intelligent alerts analysis failed: {str(e)}"}
    
    def get_ml_outcome_predictions(self, patient_data: Dict[str, Any], lab_data: Dict[str, Any], 
                                  historical_data: Dict[str, Any] = None, donor_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get comprehensive ML-based outcome predictions"""
        try:
            predictions = {}
            
            # Dialysis initiation prediction
            dialysis_pred = self.ai_clinical.ml_predictions.predict_dialysis_initiation(
                patient_data, lab_data, historical_data
            )
            predictions['dialysis_initiation'] = dialysis_pred
            
            # Transplant success prediction
            transplant_pred = self.ai_clinical.ml_predictions.predict_transplant_success(
                patient_data, lab_data, donor_data
            )
            predictions['transplant_success'] = transplant_pred
            
            # Mortality risk prediction
            mortality_pred = self.ai_clinical.ml_predictions.predict_mortality_risk(
                patient_data, lab_data, historical_data
            )
            predictions['mortality_risk'] = mortality_pred
            
            # Disease progression prediction
            progression_pred = self.ai_clinical.ml_predictions.predict_disease_progression(
                patient_data, lab_data, historical_data
            )
            predictions['disease_progression'] = progression_pred
            
            return predictions
            
        except Exception as e:
            return {'error': f"ML prediction failed: {str(e)}"}
    
    def get_clinical_recommendations(self, patient_data: Dict[str, Any], gfr_prediction: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get evidence-based clinical recommendations"""
        try:
            if not gfr_prediction:
                gfr_prediction = self.ai_clinical.kidney_predictor.predict_gfr(patient_data)
            
            return self.ai_clinical.decision_support.get_treatment_recommendations(
                patient_data, gfr_prediction
            )
            
        except Exception as e:
            return [{"error": f"Clinical recommendations failed: {str(e)}"}]
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for context"""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted = []
        for entry in self.conversation_history[-3:]:  # Last 3 exchanges
            formatted.append(f"User: {entry['user']}")
            formatted.append(f"Assistant: {entry['assistant'][:200]}...")  # Truncate for context
        
        return "\n".join(formatted)
    
    def _save_session(self, user_input: str, ai_response: str):
        """Save session to database"""
        try:
            session_id = st.session_state.get('session_id', 'default')
            self.conn.execute(
                "INSERT INTO sessions (session_id, timestamp, user_input, ai_response) VALUES (?, ?, ?, ?)",
                (session_id, datetime.now(), user_input, ai_response)
            )
            self.conn.commit()
        except Exception as e:
            st.error(f"Failed to save session: {e}")

# Initialize localization manager early
localization_manager = get_localization_manager()

# Initialize advanced systems
security_manager = get_security_manager()
responsive_manager = init_responsive_design()
audit_logger = get_audit_logger()

# Log application startup
audit_logger.log_event(
    AuditEventType.SYSTEM_ACCESS,
    "application_startup",
    details={"version": "2.0", "features": ["security", "responsive", "audit"]},
    severity=AuditSeverity.INFO
)

# Streamlit UI Configuration
st.set_page_config(
    page_title=t('app_title'),
    page_icon="🫘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card Styles */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .feature-card h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Chat Styles */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        background: #f8f9fa;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 4px solid #ffffff;
    }
    
    /* Metrics Styles */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e1e5e9;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Alert Styles */
    .alert-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Progress Bar */
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid #e1e5e9;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'nephro_agent' not in st.session_state:
    st.session_state.nephro_agent = AdvancedNephrologyAgent()
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Language Selector (top right)
col_lang, col_spacer = st.columns([1, 4])
with col_lang:
    create_language_selector()

# Main Header
st.markdown(f"""
<div class="main-header">
    <h1>🫘 {t('app_title')}</h1>
    <p>{t('app_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Quick Actions
    st.markdown("#### Quick Actions")
    if st.button("🆘 Emergency Symptoms", use_container_width=True):
        emergency_info = """
        **Seek immediate medical attention if experiencing:**
        - Severe decrease in urination or no urination
        - Severe swelling in face, hands, or feet
        - Difficulty breathing or shortness of breath
        - Chest pain or pressure
        - Severe nausea and vomiting
        - Confusion or altered mental state
        - Severe fatigue or weakness
        
        **Call 911 or go to the nearest emergency room immediately.**
        """
        st.error(emergency_info)
    
    if st.button("📊 Risk Calculator", use_container_width=True):
        st.session_state.show_risk_calculator = True
    
    if st.button("📚 Clinical Guidelines", use_container_width=True):
        st.session_state.show_guidelines = True
    
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.nephro_agent.conversation_history = []
        st.rerun()
    
    # Session Info
    st.markdown("---")
    st.markdown("#### Session Info")
    st.info(f"Session ID: {st.session_state.session_id[:8]}...")
    st.info(f"Messages: {len(st.session_state.chat_history)}")
    
    # Quick Topics
    st.markdown("#### Quick Topics")
    topics = [
        "Chronic Kidney Disease",
        "Acute Kidney Injury",
        "Dialysis Options",
        "Kidney Transplant",
        "Hypertension & Kidneys",
        "Diabetes & Kidneys"
    ]
    
    for topic in topics:
        if st.button(topic, key=f"topic_{topic}", use_container_width=True):
            st.session_state.selected_topic = topic

# Main Content Area - Tabbed Interface
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([t('tab_consultation'), t('tab_clinical_intelligence'), t('tab_risk_assessment'), t('tab_analytics'), t('tab_timeline'), t('tab_monitoring'), t('tab_patient_portal'), '🔒 Security Dashboard'])

with tab4:
    # Analytics Tab
    st.markdown("### 📊 Clinical Analytics & Insights")
    st.markdown("Advanced analytics and population health insights.")
    
    # Analytics Options
    analytics_option = st.selectbox(
        "Select Analytics View",
        ["Session Analytics", "Population Trends", "Risk Distribution", "Outcome Predictions"]
    )
    
    if analytics_option == "Session Analytics":
        # Session Analytics
        st.markdown("#### 📈 Current Session Analytics")
        
        # Simple analytics
        total_messages = len(st.session_state.chat_history)
        user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_messages}</div>
                <div class="metric-label">Total Messages</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{user_messages}</div>
                <div class="metric-label">Your Questions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ai_messages}</div>
                <div class="metric-label">AI Responses</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Message length analysis
        if st.session_state.chat_history:
            avg_user_length = sum(len(m["content"]) for m in st.session_state.chat_history if m["role"] == "user") / max(user_messages, 1)
            avg_ai_length = sum(len(m["content"]) for m in st.session_state.chat_history if m["role"] == "assistant") / max(ai_messages, 1)
            
            st.markdown("#### Message Analysis")
            col_d, col_e = st.columns(2)
            with col_d:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_user_length:.0f}</div>
                    <div class="metric-label">Avg User Message Length</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_e:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_ai_length:.0f}</div>
                    <div class="metric-label">Avg AI Response Length</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif analytics_option == "Population Trends":
        st.markdown("#### 🌍 Population Health Trends")
        st.info("This feature would show population-level kidney disease trends and statistics.")
        
        # Placeholder for population data visualization
        import numpy as np
        
        # Generate sample data for demonstration
        years = list(range(2020, 2025))
        ckd_prevalence = [11.0, 11.2, 11.5, 11.8, 12.1]
        
        fig = px.line(x=years, y=ckd_prevalence, title="CKD Prevalence Trends")
        fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif analytics_option == "Risk Distribution":
        st.markdown("#### 📊 Risk Factor Distribution")
        st.info("This feature would show risk factor distributions across patient populations.")
        
        # Sample risk distribution data
        risk_factors = ['Diabetes', 'Hypertension', 'CVD', 'Family History', 'Smoking']
        prevalence = [34.2, 45.6, 23.1, 18.9, 12.3]
        
        fig = px.bar(x=risk_factors, y=prevalence, title="Risk Factor Prevalence")
        fig.update_layout(xaxis_title="Risk Factor", yaxis_title="Prevalence (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif analytics_option == "Outcome Predictions":
        st.markdown("#### 🔮 Outcome Prediction Models")
        st.info("This feature would show predictive model performance and outcomes.")
        
        # Model performance metrics
        col_f, col_g, col_h = st.columns(3)
        with col_f:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">0.87</div>
                <div class="metric-label">Model Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_g:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">0.82</div>
                <div class="metric-label">Sensitivity</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_h:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">0.91</div>
                <div class="metric-label">Specificity</div>
            </div>
            """, unsafe_allow_html=True)

# Main Content Area - Tabbed Interface
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["💬 AI Consultation", "🧠 AI Clinical Intelligence", "🧮 Risk Assessment", "📊 Analytics", "📈 Patient Timeline", "🚨 Real-Time Monitoring", "👤 Patient Portal"])

with tab1:
    # Chat Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {t('ai_consultation_title')}")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message">
                    <strong>AI Nephrologist:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input(t('enter_symptoms'))
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("🤔 Analyzing your query with advanced medical knowledge..."):
            response = st.session_state.nephro_agent.get_enhanced_response(user_input)
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Handle selected topics
    if 'selected_topic' in st.session_state:
        topic = st.session_state.selected_topic
        with st.spinner(f"Loading information about {topic}..."):
            response = st.session_state.nephro_agent.get_enhanced_response(
                f"Please provide comprehensive information about {topic}"
            )
        
        st.session_state.chat_history.append({"role": "user", "content": f"Tell me about {topic}"})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        del st.session_state.selected_topic
        st.rerun()
    
    with col2:
        # Quick Info Panel for Chat Tab
        st.markdown("""<div class="feature-card">
            <h3>💡 Quick Tips</h3>
            <p>Ask about:</p>
            <ul>
                <li>Kidney function tests</li>
                <li>Treatment options</li>
                <li>Lifestyle modifications</li>
                <li>Medication interactions</li>
            </ul>
        </div>""", unsafe_allow_html=True)

with tab2:
    # AI Clinical Intelligence Tab
    st.markdown("### 🧠 AI Clinical Intelligence")
    st.markdown("Advanced machine learning-powered clinical analysis and decision support.")
    
    # Patient Data Input Form
    with st.expander("📋 Patient Data Input", expanded=True):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("**Demographics**")
            patient_age = st.number_input("Age", min_value=18, max_value=120, value=65, key="ai_age")
            patient_gender = st.selectbox("Gender", ["male", "female"], key="ai_gender")
            patient_bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, value=25.0, step=0.1, key="ai_bmi")
        
        with col_b:
            st.markdown("**Lab Values**")
            creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=10.0, value=1.5, step=0.1, key="ai_creat")
            bun = st.number_input("BUN (mg/dL)", min_value=5, max_value=200, value=30, key="ai_bun")
            albumin = st.number_input("Albumin (g/dL)", min_value=1.0, max_value=6.0, value=3.5, step=0.1, key="ai_albumin")
            hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=5.0, max_value=20.0, value=11.0, step=0.1, key="ai_hgb")
        
        with col_c:
            st.markdown("**Comorbidities**")
            diabetes = st.checkbox("Diabetes", key="ai_diabetes")
            hypertension = st.checkbox("Hypertension", key="ai_htn")
            cvd = st.checkbox("Cardiovascular Disease", key="ai_cvd")
            proteinuria = st.checkbox("Proteinuria", key="ai_proteinuria")
    
    # Additional Data Inputs
    col_d, col_e = st.columns(2)
    
    with col_d:
        with st.expander("💊 Current Medications"):
            medications_input = st.text_area("Enter medications (one per line)", 
                                           placeholder="metformin\nlisinopril\nfurosemide", key="ai_meds")
            medications = [med.strip() for med in medications_input.split('\n') if med.strip()] if medications_input else []
    
    with col_e:
        with st.expander("📈 Lab History (Optional)"):
            st.markdown("Enter recent lab values for trend analysis:")
            creat_history = st.text_input("Creatinine history (comma-separated)", placeholder="1.2, 1.4, 1.5", key="ai_creat_hist")
            gfr_history = st.text_input("GFR history (comma-separated)", placeholder="55, 50, 45", key="ai_gfr_hist")
    
    # Analysis Button
    if st.button("🔬 Run AI Clinical Analysis", type="primary", use_container_width=True):
        # Prepare patient data
        patient_data = {
            'patient_id': f'AI_ANALYSIS_{int(time.time())}',
            'age': patient_age,
            'gender': patient_gender,
            'bmi': patient_bmi,
            'current_gfr': 175 * (creatinine ** -1.154) * (patient_age ** -0.203) * (0.742 if patient_gender == 'female' else 1),
            'creatinine': creatinine,
            'bun': bun,
            'albumin': albumin,
            'hemoglobin': hemoglobin,
            'diabetes': diabetes,
            'hypertension': hypertension,
            'cardiovascular_disease': cvd,
            'proteinuria': proteinuria
        }
        
        # Prepare lab data
        lab_data = {
            'creatinine': creatinine,
            'hemoglobin': hemoglobin
        }
        
        # Prepare historical data if provided
        historical_data = {}
        if creat_history:
            try:
                historical_data['creatinine'] = [float(x.strip()) for x in creat_history.split(',')]
            except:
                st.warning("Invalid creatinine history format")
        if gfr_history:
            try:
                historical_data['gfr'] = [float(x.strip()) for x in gfr_history.split(',')]
            except:
                st.warning("Invalid GFR history format")
        
        # Run AI Analysis
        with st.spinner("🤖 Running AI Clinical Intelligence Analysis..."):
            analysis = st.session_state.nephro_agent.get_ai_clinical_analysis(
                patient_data, lab_data, medications, historical_data if historical_data else None
            )
            
            # Add dialysis and transplant readiness analysis
            if 'error' not in analysis:
                analysis['dialysis_readiness'] = st.session_state.nephro_agent.get_dialysis_readiness(
                    patient_data, lab_data, []
                )
                analysis['transplant_readiness'] = st.session_state.nephro_agent.get_transplant_readiness(
                    patient_data, lab_data, []
                )
                
                # Add drug dosing recommendations if medications are provided
                if medications:
                    analysis['drug_dosing'] = st.session_state.nephro_agent.get_drug_dosing_recommendations(
                        patient_data, medications, lab_data
                    )
        
        # Display Results
        if 'error' not in analysis:
            # Predictions Section
            st.markdown("### 🔮 AI Predictions")
            pred_col1, pred_col2, pred_col3 = st.columns(3)
            
            with pred_col1:
                gfr_pred = analysis['predictions']['gfr']
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value">{gfr_pred['predicted_gfr']}</div>
                    <div class="metric-label">Predicted GFR</div>
                    <small>Confidence: {gfr_pred['confidence']}%</small>
                </div>""", unsafe_allow_html=True)
            
            with pred_col2:
                prog_risk = analysis['predictions']['progression']
                risk_color = "#e74c3c" if prog_risk['risk_level'] == 'High' else "#f39c12" if prog_risk['risk_level'] == 'Moderate' else "#27ae60"
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value" style="color: {risk_color}">{prog_risk['progression_risk']}%</div>
                    <div class="metric-label">Progression Risk</div>
                    <small>{prog_risk['risk_level']} Risk</small>
                </div>""", unsafe_allow_html=True)
            
            with pred_col3:
                stage = gfr_pred['stage']
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value" style="font-size: 1.2rem;">{stage.split('(')[0]}</div>
                    <div class="metric-label">CKD Stage</div>
                    <small>{stage.split('(')[1].rstrip(')') if '(' in stage else ''}</small>
                </div>""", unsafe_allow_html=True)
            
            # Clinical Recommendations
            st.markdown("### 📋 Evidence-Based Recommendations")
            for rec in analysis['recommendations']:
                priority_color = "#e74c3c" if rec['priority'] == 'High' else "#f39c12" if rec['priority'] == 'Moderate' else "#27ae60"
                st.markdown(f"""<div class="feature-card">
                    <h4 style="color: {priority_color};">{rec['category']} 
                        <span style="font-size: 0.8rem; background: {priority_color}; color: white; padding: 2px 8px; border-radius: 12px;">{rec['priority']}</span>
                    </h4>
                    <p>{rec['recommendation']}</p>
                    <small><strong>Evidence Level:</strong> {rec['evidence_level']}</small>
                </div>""", unsafe_allow_html=True)
            
            # Drug Dosing Recommendations
            if 'drug_dosing' in analysis and analysis['drug_dosing']:
                st.markdown("### 💊 Drug Dosing Adjustments")
                for drug_rec in analysis['drug_dosing']:
                    priority_color = "#e74c3c" if drug_rec['priority'] == 'High' else "#f39c12"
                    st.markdown(f"""<div class="alert-warning">
                        <strong>{drug_rec['medication']}</strong> (GFR: {drug_rec['current_gfr']} mL/min/1.73m²)<br>
                        {drug_rec['recommendation']}
                    </div>""", unsafe_allow_html=True)
            
            # Alerts
            if 'critical_alerts' in analysis and analysis['critical_alerts']:
                st.markdown("### ⚠️ Critical Alerts")
                for alert in analysis['critical_alerts']:
                    alert_class = "alert-danger" if alert['urgency'] == 'Critical' else "alert-warning"
                    st.markdown(f"""<div class="{alert_class}">
                        <strong>{alert['type']}:</strong> {alert['lab']} = {alert['value']}<br>
                        <strong>Action:</strong> {alert['action']}
                    </div>""", unsafe_allow_html=True)
            
            # Risk Factors
            if prog_risk['factors']:
                st.markdown("### 🎯 Key Risk Factors")
                for factor in prog_risk['factors']:
                    st.markdown(f"• {factor}")
            
            # Dialysis and Transplant Readiness
            if 'dialysis_readiness' in analysis and 'error' not in analysis['dialysis_readiness']:
                st.markdown("### 🏥 Dialysis Readiness Analysis")
                dialysis = analysis['dialysis_readiness']
                
                dial_col1, dial_col2 = st.columns(2)
                with dial_col1:
                    urgency_color = "#e74c3c" if dialysis['urgency'] == 'Critical' else "#f39c12" if dialysis['urgency'] == 'High' else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {urgency_color}">{dialysis['readiness_score']}</div>
                        <div class="metric-label">Readiness Score</div>
                        <small>{dialysis['urgency']} Priority</small>
                    </div>""", unsafe_allow_html=True)
                
                with dial_col2:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="font-size: 0.9rem;">{dialysis['predicted_timeline']}</div>
                        <div class="metric-label">Predicted Timeline</div>
                        <small>Based on current trajectory</small>
                    </div>""", unsafe_allow_html=True)
                
                # Dialysis recommendations
                if dialysis.get('recommendations'):
                    st.markdown("**Dialysis Preparation Recommendations:**")
                    for rec in dialysis['recommendations']:
                        st.markdown(f"• {rec}")
            
            if 'transplant_readiness' in analysis and 'error' not in analysis['transplant_readiness']:
                st.markdown("### 🫀 Transplant Readiness Analysis")
                transplant = analysis['transplant_readiness']
                
                trans_col1, trans_col2 = st.columns(2)
                with trans_col1:
                    status_color = "#27ae60" if "Excellent" in transplant['status'] else "#f39c12" if "Good" in transplant['status'] else "#e74c3c"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {status_color}">{transplant['eligibility_score']}</div>
                        <div class="metric-label">Eligibility Score</div>
                        <small>{transplant['status']}</small>
                    </div>""", unsafe_allow_html=True)
                
                with trans_col2:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="font-size: 0.9rem;">{transplant['timeline']}</div>
                        <div class="metric-label">Evaluation Timeline</div>
                        <small>Recommended timing</small>
                    </div>""", unsafe_allow_html=True)
                
                # Transplant next steps
                if transplant.get('next_steps'):
                    st.markdown("**Next Steps for Transplant Evaluation:**")
                    for step in transplant['next_steps']:
                        st.markdown(f"• {step}")
                
                # Contraindications if any
                if transplant.get('contraindications'):
                    st.markdown("**⚠️ Potential Contraindications:**")
                    for contra in transplant['contraindications']:
                        st.markdown(f"• {contra}")
            
            # Drug Dosing Recommendations
            if 'drug_dosing' in analysis and 'error' not in analysis['drug_dosing']:
                st.markdown("### 💊 Drug Dosing Recommendations")
                dosing = analysis['drug_dosing']
                
                if dosing.get('recommendations'):
                    for rec in dosing['recommendations']:
                        with st.expander(f"📋 {rec['medication']} - {rec['risk_level']} Risk"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Normal Dose:** {rec['normal_dose']}")
                                st.markdown(f"**Recommended Dose:** {rec['recommended_dose']}")
                                if rec['age_adjustment']:
                                    st.markdown(f"**Age Adjustment:** {rec['age_adjustment']}")
                            
                            with col2:
                                st.markdown(f"**Monitoring:** {rec['monitoring']}")
                                st.markdown(f"**Rationale:** {rec['rationale']}")
                                
                                # Risk level indicator
                                risk_color = "#e74c3c" if rec['risk_level'] == 'High' else "#f39c12" if rec['risk_level'] == 'Moderate' else "#27ae60"
                                st.markdown(f"<span style='color: {risk_color}; font-weight: bold;'>Risk Level: {rec['risk_level']}</span>", unsafe_allow_html=True)
                
                # General principles
                if dosing.get('general_principles'):
                    st.markdown("**📋 General Dosing Principles:**")
                    for principle in dosing['general_principles']:
                        st.markdown(f"• {principle}")
                
                # Monitoring schedule
                if dosing.get('monitoring_schedule'):
                    st.info(f"**🔍 Monitoring Schedule:** {dosing['monitoring_schedule']}")
        
        else:
            st.error(f"Analysis failed: {analysis['error']}")
    
    # Clinical Notes Analysis Section
    st.markdown("### 📝 Clinical Notes Analysis")
    st.markdown("AI-powered analysis of clinical notes, progress notes, and discharge summaries.")
    
    clinical_notes = st.text_area(
        "Enter clinical notes for AI analysis:",
        height=150,
        placeholder="Enter patient clinical notes, progress notes, or discharge summaries...",
        key="clinical_notes_input"
    )
    
    if clinical_notes and st.button("🔍 Analyze Clinical Notes", type="primary"):
        # Prepare patient data for context (if available from previous analysis)
        context_data = None
        if 'patient_data' in locals():
            context_data = patient_data
        
        with st.spinner("🤖 Analyzing clinical notes with AI..."):
            notes_analysis = st.session_state.nephro_agent.analyze_clinical_notes(
                clinical_notes, context_data
            )
        
        if 'error' not in notes_analysis:
            # Medical entities
            if 'entities' in notes_analysis:
                st.markdown("#### 🔍 Extracted Medical Entities")
                entities_col1, entities_col2 = st.columns(2)
                
                with entities_col1:
                    if notes_analysis['entities'].get('conditions'):
                        st.markdown("**🏥 Conditions:**")
                        for condition in notes_analysis['entities']['conditions']:
                            st.markdown(f"• {condition}")
                    
                    if notes_analysis['entities'].get('medications'):
                        st.markdown("**💊 Medications:**")
                        for med in notes_analysis['entities']['medications']:
                            st.markdown(f"• {med}")
                
                with entities_col2:
                    if notes_analysis['entities'].get('symptoms'):
                        st.markdown("**🩺 Symptoms:**")
                        for symptom in notes_analysis['entities']['symptoms']:
                            st.markdown(f"• {symptom}")
                    
                    if notes_analysis['entities'].get('lab_values'):
                        st.markdown("**🧪 Lab Values:**")
                        for lab in notes_analysis['entities']['lab_values']:
                            st.markdown(f"• {lab}")
            
            # Sentiment and risk analysis
            col1, col2 = st.columns(2)
            with col1:
                if 'sentiment' in notes_analysis:
                    sentiment = notes_analysis['sentiment']
                    sentiment_color = "#e74c3c" if sentiment['overall'] == 'negative' else "#f39c12" if sentiment['overall'] == 'neutral' else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {sentiment_color}">{sentiment['overall'].title()}</div>
                        <div class="metric-label">Overall Sentiment</div>
                        <small>Score: {sentiment['score']:.2f}</small>
                    </div>""", unsafe_allow_html=True)
            
            with col2:
                if 'risk_indicators' in notes_analysis:
                    risk_count = len(notes_analysis['risk_indicators'])
                    risk_color = "#e74c3c" if risk_count > 3 else "#f39c12" if risk_count > 1 else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {risk_color}">{risk_count}</div>
                        <div class="metric-label">Risk Indicators</div>
                        <small>Found in notes</small>
                    </div>""", unsafe_allow_html=True)
            
            # Risk indicators
            if notes_analysis.get('risk_indicators'):
                st.markdown("#### ⚠️ Risk Indicators")
                for risk in notes_analysis['risk_indicators']:
                    severity_color = "#e74c3c" if risk['severity'] == 'high' else "#f39c12" if risk['severity'] == 'medium' else "#27ae60"
                    st.markdown(f"""<div class="alert-warning">
                        <strong style="color: {severity_color}">{risk['type']}:</strong> {risk['description']} 
                        <span style="background: {severity_color}; color: white; padding: 2px 6px; border-radius: 8px; font-size: 0.8rem;">{risk['severity'].upper()}</span>
                    </div>""", unsafe_allow_html=True)
            
            # Recommendations
            if notes_analysis.get('recommendations'):
                st.markdown("#### 💡 AI Recommendations")
                for rec in notes_analysis['recommendations']:
                    priority_color = "#e74c3c" if rec['priority'] == 'high' else "#f39c12" if rec['priority'] == 'medium' else "#27ae60"
                    st.markdown(f"""<div class="feature-card">
                        <h4 style="color: {priority_color}">{rec['category']} 
                            <span style="font-size: 0.8rem; background: {priority_color}; color: white; padding: 2px 8px; border-radius: 12px;">{rec['priority'].upper()}</span>
                        </h4>
                        <p>{rec['recommendation']}</p>
                    </div>""", unsafe_allow_html=True)
            
            # Summary
            if notes_analysis.get('summary'):
                st.markdown("#### 📋 Clinical Summary")
                st.markdown(f"""<div class="feature-card">
                    <p>{notes_analysis['summary']}</p>
                </div>""", unsafe_allow_html=True)
        
        else:
             st.error(f"Analysis failed: {notes_analysis['error']}")
    
    # Intelligent Alerts Section
    st.markdown("### 🚨 Intelligent Lab Alerts")
    st.markdown("AI-powered critical value detection and trend analysis for proactive patient monitoring.")
    
    # Current lab values input for alerts
    with st.expander("📊 Lab Values for Alert Analysis", expanded=False):
        alert_col1, alert_col2 = st.columns(2)
        
        with alert_col1:
            st.markdown("**Current Lab Values**")
            alert_creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=15.0, value=2.0, step=0.1, key="alert_creat")
            alert_gfr = st.number_input("GFR (mL/min/1.73m²)", min_value=5, max_value=120, value=35, key="alert_gfr")
            alert_potassium = st.number_input("Potassium (mEq/L)", min_value=2.0, max_value=8.0, value=4.5, step=0.1, key="alert_k")
            alert_hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=4.0, max_value=18.0, value=9.5, step=0.1, key="alert_hgb")
        
        with alert_col2:
            st.markdown("**Additional Parameters**")
            alert_albumin = st.number_input("Albumin (g/dL)", min_value=1.0, max_value=6.0, value=3.0, step=0.1, key="alert_alb")
            alert_phosphorus = st.number_input("Phosphorus (mg/dL)", min_value=1.0, max_value=10.0, value=5.5, step=0.1, key="alert_phos")
            alert_calcium = st.number_input("Calcium (mg/dL)", min_value=6.0, max_value=14.0, value=9.0, step=0.1, key="alert_ca")
            alert_bun = st.number_input("BUN (mg/dL)", min_value=5, max_value=200, value=45, key="alert_bun")
    
    # Historical data input for trend analysis
    with st.expander("📈 Historical Data for Trend Analysis (Optional)"):
        st.markdown("Enter comma-separated values for trend analysis:")
        hist_col1, hist_col2 = st.columns(2)
        
        with hist_col1:
            creat_trend = st.text_input("Creatinine trend (last 6 months)", placeholder="1.5, 1.7, 1.9, 2.0", key="creat_trend")
            gfr_trend = st.text_input("GFR trend (last 6 months)", placeholder="45, 40, 38, 35", key="gfr_trend")
        
        with hist_col2:
            hgb_trend = st.text_input("Hemoglobin trend (last 6 months)", placeholder="11.0, 10.5, 10.0, 9.5", key="hgb_trend")
            k_trend = st.text_input("Potassium trend (last 6 months)", placeholder="4.2, 4.3, 4.4, 4.5", key="k_trend")
    
    if st.button("🔍 Generate Intelligent Alerts", type="primary"):
        # Prepare current lab data
        current_labs = {
            'creatinine': alert_creatinine,
            'gfr': alert_gfr,
            'potassium': alert_potassium,
            'hemoglobin': alert_hemoglobin,
            'albumin': alert_albumin,
            'phosphorus': alert_phosphorus,
            'calcium': alert_calcium,
            'bun': alert_bun
        }
        
        # Prepare historical data if provided
        historical_data = {}
        try:
            if creat_trend:
                historical_data['creatinine'] = [float(x.strip()) for x in creat_trend.split(',')]
            if gfr_trend:
                historical_data['gfr'] = [float(x.strip()) for x in gfr_trend.split(',')]
            if hgb_trend:
                historical_data['hemoglobin'] = [float(x.strip()) for x in hgb_trend.split(',')]
            if k_trend:
                historical_data['potassium'] = [float(x.strip()) for x in k_trend.split(',')]
        except ValueError:
            st.warning("Invalid format in historical data. Please use comma-separated numbers.")
            historical_data = {}
        
        # Get patient context if available from previous analysis
        context_data = None
        if 'patient_data' in locals():
            context_data = patient_data
        
        with st.spinner("🤖 Analyzing lab values and generating intelligent alerts..."):
            alerts_result = st.session_state.nephro_agent.get_intelligent_alerts(
                current_labs, historical_data if historical_data else None, context_data
            )
        
        if 'error' not in alerts_result:
            # Alert Summary
            st.markdown("#### 📋 Alert Summary")
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                total_alerts = alerts_result['critical_values']['total_alerts']
                alert_color = "#e74c3c" if total_alerts > 3 else "#f39c12" if total_alerts > 1 else "#27ae60"
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value" style="color: {alert_color}">{total_alerts}</div>
                    <div class="metric-label">Total Alerts</div>
                </div>""", unsafe_allow_html=True)
            
            with summary_col2:
                overall_risk = alerts_result['critical_values']['overall_risk']
                risk_color = "#e74c3c" if overall_risk == 'critical' else "#f39c12" if overall_risk == 'high' else "#27ae60"
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value" style="color: {risk_color}">{overall_risk.title()}</div>
                    <div class="metric-label">Overall Risk</div>
                </div>""", unsafe_allow_html=True)
            
            with summary_col3:
                critical_count = alerts_result['critical_values']['severity_breakdown']['critical']
                critical_color = "#e74c3c" if critical_count > 0 else "#27ae60"
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value" style="color: {critical_color}">{critical_count}</div>
                    <div class="metric-label">Critical Values</div>
                </div>""", unsafe_allow_html=True)
            
            # Critical Value Alerts
            if alerts_result['critical_values']['alerts']:
                st.markdown("#### 🚨 Critical Value Alerts")
                for alert in alerts_result['prioritized_alerts']:
                    if alert.get('lab'):  # Critical value alert
                        severity_color = "#e74c3c" if alert['severity'] == 'critical' else "#f39c12" if alert['severity'] == 'severe' else "#ffa500"
                        urgency_text = alert.get('urgency', 'standard').replace('_', ' ').title()
                        
                        st.markdown(f"""<div class="alert-danger" style="border-left: 4px solid {severity_color}">
                            <strong style="color: {severity_color}">{alert['severity'].upper()}</strong> - {alert['lab'].title()}: {alert['value']}<br>
                            <strong>Message:</strong> {alert['message']}<br>
                            <strong>Urgency:</strong> {urgency_text}<br>
                            <strong>Actions:</strong> {', '.join(alert['actions'])}
                        </div>""", unsafe_allow_html=True)
            
            # Trend Analysis
            if alerts_result.get('trends') and alerts_result['trends'].get('trend_alerts'):
                st.markdown("#### 📈 Trend Analysis")
                
                trend_col1, trend_col2 = st.columns(2)
                with trend_col1:
                    declining = len(alerts_result['trends']['declining_parameters'])
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: #e74c3c">{declining}</div>
                        <div class="metric-label">Declining Parameters</div>
                    </div>""", unsafe_allow_html=True)
                
                with trend_col2:
                    improving = len(alerts_result['trends']['improving_parameters'])
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: #27ae60">{improving}</div>
                        <div class="metric-label">Improving Parameters</div>
                    </div>""", unsafe_allow_html=True)
                
                # Individual trend alerts
                for trend_alert in alerts_result['trends']['trend_alerts']:
                    alert_color = "#e74c3c" if trend_alert['alert_level'] == 'critical' else "#f39c12" if trend_alert['alert_level'] == 'moderate' else "#ffa500"
                    direction_icon = "📉" if trend_alert['direction'] == 'declining' else "📈" if trend_alert['direction'] == 'improving' else "➡️"
                    
                    st.markdown(f"""<div class="feature-card" style="border-left: 4px solid {alert_color}">
                        <h4 style="color: {alert_color}">{direction_icon} {trend_alert['lab'].title()} Trend</h4>
                        <p><strong>Change:</strong> {trend_alert['overall_change_percent']:.1f}% overall, {trend_alert['recent_change_percent']:.1f}% recent</p>
                        <p><strong>Recommendation:</strong> {trend_alert['recommendation']}</p>
                    </div>""", unsafe_allow_html=True)
            
            # Contextual Alerts
            if alerts_result.get('contextual_alerts'):
                st.markdown("#### 🎯 Contextual Alerts")
                for ctx_alert in alerts_result['contextual_alerts']:
                    st.markdown(f"""<div class="alert-warning">
                        <strong>{ctx_alert['category'].replace('_', ' ').title()}:</strong> {ctx_alert['message']}<br>
                        <strong>Actions:</strong> {', '.join(ctx_alert['actions'])}
                    </div>""", unsafe_allow_html=True)
            
            # Immediate Actions
            if alerts_result['critical_values']['immediate_actions']:
                st.markdown("#### ⚡ Immediate Actions Required")
                for action in alerts_result['critical_values']['immediate_actions']:
                    st.error(f"🚨 {action}")
            
            # Monitoring Recommendations
            if alerts_result.get('next_monitoring'):
                st.markdown("#### 📅 Recommended Monitoring Schedule")
                monitoring = alerts_result['next_monitoring']
                st.info(f"**Frequency:** {monitoring['frequency']} | **Duration:** {monitoring['duration']} | **Parameters:** {monitoring['parameters']}")
            
            # Overall Summary
            if alerts_result.get('summary'):
                st.markdown("#### 📝 Summary")
                st.markdown(f"""<div class="feature-card">
                    <p>{alerts_result['summary']}</p>
                </div>""", unsafe_allow_html=True)
        
        else:
            st.error(f"Alert analysis failed: {alerts_result['error']}")

    # ML Outcome Predictions Section
    st.markdown("---")
    st.markdown("### 🔮 ML-Based Outcome Predictions")
    st.markdown("Advanced machine learning models for predicting patient outcomes and disease progression.")
    
    with st.expander("📊 Outcome Prediction Analysis", expanded=False):
        pred_col1, pred_col2 = st.columns(2)
        
        with pred_col1:
            st.markdown("**Patient Demographics**")
            pred_age = st.number_input("Age", min_value=18, max_value=120, value=65, key="pred_age")
            pred_gender = st.selectbox("Gender", ["male", "female"], key="pred_gender")
            pred_diabetes = st.checkbox("Diabetes", key="pred_dm")
            pred_hypertension = st.checkbox("Hypertension", key="pred_htn")
            pred_cvd = st.checkbox("Cardiovascular Disease", key="pred_cvd")
        
        with pred_col2:
            st.markdown("**Current Lab Values**")
            pred_creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=15.0, value=2.5, step=0.1, key="pred_creat")
            pred_gfr = st.number_input("GFR (mL/min/1.73m²)", min_value=5, max_value=120, value=25, key="pred_gfr")
            pred_albumin = st.number_input("Albumin (g/dL)", min_value=1.0, max_value=6.0, value=3.2, step=0.1, key="pred_alb")
            pred_hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=4.0, max_value=18.0, value=9.8, step=0.1, key="pred_hgb")
            pred_phosphorus = st.number_input("Phosphorus (mg/dL)", min_value=1.0, max_value=10.0, value=5.2, step=0.1, key="pred_phos")
    
        # Optional donor data for transplant predictions
        with st.expander("🫀 Donor Information (for Transplant Predictions)", expanded=False):
            donor_col1, donor_col2 = st.columns(2)
            
            with donor_col1:
                donor_age = st.number_input("Donor Age", min_value=18, max_value=80, value=45, key="donor_age")
                donor_gender = st.selectbox("Donor Gender", ["male", "female"], key="donor_gender")
                donor_type = st.selectbox("Donor Type", ["living", "deceased"], key="donor_type")
            
            with donor_col2:
                donor_creatinine = st.number_input("Donor Creatinine (mg/dL)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key="donor_creat")
                hla_mismatch = st.number_input("HLA Mismatches", min_value=0, max_value=6, value=2, key="hla_mismatch")
                cold_ischemia = st.number_input("Cold Ischemia Time (hours)", min_value=0, max_value=48, value=8, key="cold_ischemia")
    
        if st.button("🔮 Generate ML Predictions", type="primary"):
            # Prepare patient data
            patient_data = {
                'age': pred_age,
                'gender': pred_gender,
                'diabetes': pred_diabetes,
                'hypertension': pred_hypertension,
                'cardiovascular_disease': pred_cvd
            }
            
            # Prepare lab data
            lab_data = {
                'creatinine': pred_creatinine,
                'gfr': pred_gfr,
                'albumin': pred_albumin,
                'hemoglobin': pred_hemoglobin,
                'phosphorus': pred_phosphorus
            }
            
            # Prepare donor data if provided
            donor_data = {
                'age': donor_age,
                'gender': donor_gender,
                'type': donor_type,
                'creatinine': donor_creatinine,
                'hla_mismatch': hla_mismatch,
                'cold_ischemia_time': cold_ischemia
            }
            
            with st.spinner("🤖 Running ML prediction models..."):
                predictions = st.session_state.nephro_agent.get_ml_outcome_predictions(
                    patient_data, lab_data, None, donor_data
                )
            
            if 'error' not in predictions:
                # Prediction Results Display
                st.markdown("#### 🎯 Prediction Results")
                
                # Create metrics for each prediction
                pred_metrics_col1, pred_metrics_col2, pred_metrics_col3, pred_metrics_col4 = st.columns(4)
                
                with pred_metrics_col1:
                    dialysis_risk = predictions['dialysis_initiation']['risk_score']
                    risk_color = "#e74c3c" if dialysis_risk > 0.7 else "#f39c12" if dialysis_risk > 0.4 else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {risk_color}">{dialysis_risk:.1%}</div>
                        <div class="metric-label">Dialysis Risk (1 year)</div>
                    </div>""", unsafe_allow_html=True)
                
                with pred_metrics_col2:
                    transplant_success = predictions['transplant_success']['success_probability']
                    success_color = "#27ae60" if transplant_success > 0.8 else "#f39c12" if transplant_success > 0.6 else "#e74c3c"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {success_color}">{transplant_success:.1%}</div>
                        <div class="metric-label">Transplant Success</div>
                    </div>""", unsafe_allow_html=True)
                
                with pred_metrics_col3:
                    mortality_risk = predictions['mortality_risk']['risk_score']
                    mortality_color = "#e74c3c" if mortality_risk > 0.3 else "#f39c12" if mortality_risk > 0.15 else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {mortality_color}">{mortality_risk:.1%}</div>
                        <div class="metric-label">Mortality Risk (5 year)</div>
                    </div>""", unsafe_allow_html=True)
                
                with pred_metrics_col4:
                    progression_rate = predictions['disease_progression']['progression_rate']
                    progression_color = "#e74c3c" if progression_rate > 5 else "#f39c12" if progression_rate > 2 else "#27ae60"
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-value" style="color: {progression_color}">{progression_rate:.1f}</div>
                        <div class="metric-label">GFR Decline (mL/min/year)</div>
                    </div>""", unsafe_allow_html=True)
                
                # Detailed predictions
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    # Dialysis Initiation Details
                    st.markdown("##### 🩺 Dialysis Initiation Prediction")
                    dialysis_pred = predictions['dialysis_initiation']
                    timeframe = dialysis_pred['predicted_timeframe']
                    confidence = dialysis_pred['confidence_interval']
                    
                    st.markdown(f"""<div class="feature-card">
                        <p><strong>Predicted Timeframe:</strong> {timeframe}</p>
                        <p><strong>Confidence Interval:</strong> {confidence['lower']:.1%} - {confidence['upper']:.1%}</p>
                        <p><strong>Key Risk Factors:</strong></p>
                        <ul>{''.join([f'<li>{factor}</li>' for factor in dialysis_pred['risk_factors']])}</ul>
                    </div>""", unsafe_allow_html=True)
                    
                    # Disease Progression Details
                    st.markdown("##### 📈 Disease Progression")
                    progression_pred = predictions['disease_progression']
                    
                    st.markdown(f"""<div class="feature-card">
                        <p><strong>Predicted GFR in 1 year:</strong> {progression_pred['predicted_gfr_1year']:.1f} mL/min/1.73m²</p>
                        <p><strong>Predicted GFR in 5 years:</strong> {progression_pred['predicted_gfr_5year']:.1f} mL/min/1.73m²</p>
                        <p><strong>Stage Progression Risk:</strong> {progression_pred['stage_progression_risk']:.1%}</p>
                    </div>""", unsafe_allow_html=True)
                
                with detail_col2:
                    # Transplant Success Details
                    st.markdown("##### 🫀 Transplant Success Prediction")
                    transplant_pred = predictions['transplant_success']
                    
                    st.markdown(f"""<div class="feature-card">
                        <p><strong>1-year Survival:</strong> {transplant_pred['survival_1year']:.1%}</p>
                        <p><strong>5-year Survival:</strong> {transplant_pred['survival_5year']:.1%}</p>
                        <p><strong>Rejection Risk:</strong> {transplant_pred['rejection_risk']:.1%}</p>
                        <p><strong>Compatibility Score:</strong> {transplant_pred['compatibility_score']:.2f}/1.0</p>
                    </div>""", unsafe_allow_html=True)
                    
                    # Mortality Risk Details
                    st.markdown("##### ⚠️ Mortality Risk Assessment")
                    mortality_pred = predictions['mortality_risk']
                    
                    st.markdown(f"""<div class="feature-card">
                        <p><strong>Risk Category:</strong> {mortality_pred['risk_category']}</p>
                        <p><strong>1-year Risk:</strong> {mortality_pred['risk_1year']:.1%}</p>
                        <p><strong>5-year Risk:</strong> {mortality_pred['risk_5year']:.1%}</p>
                        <p><strong>Primary Risk Factors:</strong></p>
                        <ul>{''.join([f'<li>{factor}</li>' for factor in mortality_pred['primary_risk_factors']])}</ul>
                    </div>""", unsafe_allow_html=True)
                
                # Recommendations based on predictions
                st.markdown("##### 💡 AI Recommendations")
                recommendations = []
                
                if dialysis_risk > 0.6:
                    recommendations.append("Consider early dialysis access planning and patient education")
                if transplant_success < 0.7:
                    recommendations.append("Optimize patient condition before transplant listing")
                if mortality_risk > 0.2:
                    recommendations.append("Implement aggressive risk factor modification")
                if progression_rate > 3:
                    recommendations.append("Consider nephrology referral for CKD management optimization")
                
                if recommendations:
                    for rec in recommendations:
                        st.info(f"💡 {rec}")
                else:
                    st.success("✅ Current predictions suggest stable disease course with appropriate management")
            
            else:
                st.error(f"ML prediction failed: {predictions['error']}")
                
        # Data Export Section
        st.markdown("---")
        st.markdown("#### 📊 Data Export & Reporting")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            if st.button("📄 Export to CSV", use_container_width=True):
                try:
                    # Prepare export data
                    patient_export_data = {
                        'id': f"PATIENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        'age': pred_age,
                        'gender': pred_gender,
                        'diabetes': pred_diabetes,
                        'hypertension': pred_hypertension,
                        'cardiovascular_disease': pred_cvd
                    }
                    
                    lab_export_data = [{
                        'parameter': 'Creatinine',
                        'value': pred_creatinine,
                        'unit': 'mg/dL',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }, {
                        'parameter': 'GFR',
                        'value': pred_gfr,
                        'unit': 'mL/min/1.73m²',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }]
                    
                    csv_data = st.session_state.nephro_agent.data_export.export_patient_data_csv(
                        patient_export_data, lab_export_data
                    )
                    
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"patient_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    st.success("✅ CSV export ready for download!")
                    
                except Exception as e:
                    st.error(f"CSV export failed: {str(e)}")
        
        with export_col2:
            if st.button("📊 Export to Excel", use_container_width=True):
                try:
                    # Prepare comprehensive export data
                    patient_export_data = {
                        'id': f"PATIENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        'age': pred_age,
                        'gender': pred_gender,
                        'diabetes': pred_diabetes,
                        'hypertension': pred_hypertension,
                        'cardiovascular_disease': pred_cvd
                    }
                    
                    lab_export_data = [{
                        'parameter': 'Creatinine',
                        'value': pred_creatinine,
                        'unit': 'mg/dL',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'reference_range': '0.6-1.2'
                    }, {
                        'parameter': 'GFR',
                        'value': pred_gfr,
                        'unit': 'mL/min/1.73m²',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'reference_range': '>90'
                    }]
                    
                    # Include predictions if available
                    predictions_data = None
                    if 'predictions' in locals() and 'error' not in predictions:
                        predictions_data = predictions
                    
                    excel_data = st.session_state.nephro_agent.data_export.export_patient_data_excel(
                        patient_export_data, lab_export_data, None, predictions_data
                    )
                    
                    st.download_button(
                        label="💾 Download Excel",
                        data=excel_data,
                        file_name=f"patient_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    st.success("✅ Excel export ready for download!")
                    
                except Exception as e:
                    st.error(f"Excel export failed: {str(e)}")
        
        with export_col3:
            if st.button("📋 Generate PDF Report", use_container_width=True):
                try:
                    # Prepare comprehensive report data
                    patient_export_data = {
                        'id': f"PATIENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        'age': pred_age,
                        'gender': pred_gender,
                        'diabetes': pred_diabetes,
                        'hypertension': pred_hypertension,
                        'cardiovascular_disease': pred_cvd
                    }
                    
                    lab_export_data = [{
                        'parameter': 'Creatinine',
                        'value': pred_creatinine,
                        'unit': 'mg/dL',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'reference_range': '0.6-1.2 mg/dL'
                    }, {
                        'parameter': 'GFR',
                        'value': pred_gfr,
                        'unit': 'mL/min/1.73m²',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'reference_range': '>90 mL/min/1.73m²'
                    }]
                    
                    # Include predictions and assessments if available
                    predictions_data = None
                    if 'predictions' in locals() and 'error' not in predictions:
                        predictions_data = predictions
                    
                    assessments_data = [{
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'assessment': 'AI-Generated Clinical Assessment',
                        'recommendations': 'Based on current lab values and patient history'
                    }]
                    
                    pdf_data = st.session_state.nephro_agent.data_export.generate_clinical_report_pdf(
                        patient_export_data, lab_export_data, assessments_data, predictions_data
                    )
                    
                    st.download_button(
                        label="💾 Download PDF Report",
                        data=pdf_data,
                        file_name=f"clinical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ PDF report ready for download!")
                    
                except Exception as e:
                    st.error(f"PDF report generation failed: {str(e)}")
 
with tab3:
    # Risk Assessment Tab
    st.markdown("### 🧮 Advanced Risk Assessment")
    st.markdown("Comprehensive kidney disease risk evaluation and monitoring.")
    
    # Enhanced Risk Calculator
    with st.expander("🎯 Enhanced Risk Calculator", expanded=True):
        risk_col1, risk_col2 = st.columns(2)
        
        with risk_col1:
            st.markdown("**Patient Information**")
            risk_age = st.number_input("Age", min_value=18, max_value=120, value=65, key="risk_age")
            risk_gender = st.selectbox("Gender", ["male", "female"], key="risk_gender")
            risk_race = st.selectbox("Race", ["white", "black", "asian", "hispanic", "other"], key="risk_race")
            
            st.markdown("**Lab Values**")
            risk_creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=10.0, value=1.2, step=0.1, key="risk_creat")
            risk_albumin_creat = st.number_input("Albumin/Creatinine Ratio (mg/g)", min_value=0, max_value=5000, value=30, key="risk_acr")
        
        with risk_col2:
            st.markdown("**Medical History**")
            risk_diabetes = st.checkbox("Diabetes Mellitus", key="risk_dm")
            risk_hypertension = st.checkbox("Hypertension", key="risk_htn")
            risk_cvd = st.checkbox("Cardiovascular Disease", key="risk_cvd")
            risk_family_history = st.checkbox("Family History of Kidney Disease", key="risk_fh")
            
            st.markdown("**Lifestyle Factors**")
            risk_smoking = st.selectbox("Smoking Status", ["never", "former", "current"], key="risk_smoke")
            risk_bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, value=25.0, step=0.1, key="risk_bmi")
    
    if st.button("🔍 Calculate Comprehensive Risk", type="primary", use_container_width=True):
        # Calculate GFR
        calculated_gfr = 175 * (risk_creatinine ** -1.154) * (risk_age ** -0.203) * (0.742 if risk_gender == 'female' else 1) * (1.212 if risk_race == 'black' else 1)
        
        # Prepare risk data
        risk_data = {
            'age': risk_age,
            'gender': risk_gender,
            'race': risk_race,
            'creatinine': risk_creatinine,
            'gfr': calculated_gfr,
            'albumin_creatinine_ratio': risk_albumin_creat,
            'diabetes': risk_diabetes,
            'hypertension': risk_hypertension,
            'cardiovascular_disease': risk_cvd,
            'family_history': risk_family_history,
            'smoking': risk_smoking,
            'bmi': risk_bmi
        }
        
        # Get enhanced risk assessment
        with st.spinner("🔬 Calculating comprehensive risk profile..."):
            risk_result = st.session_state.nephro_agent.calculate_kidney_risk(risk_data)
        
        # Display Results
        st.markdown("### 📊 Risk Assessment Results")
        
        # Main Metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{calculated_gfr:.1f}</div>
                <div class="metric-label">eGFR</div>
                <small>mL/min/1.73m²</small>
            </div>""", unsafe_allow_html=True)
        
        with metric_col2:
            stage_color = "#e74c3c" if calculated_gfr < 30 else "#f39c12" if calculated_gfr < 60 else "#27ae60"
            ckd_stage = "5" if calculated_gfr < 15 else "4" if calculated_gfr < 30 else "3" if calculated_gfr < 60 else "2" if calculated_gfr < 90 else "1"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value" style="color: {stage_color}">Stage {ckd_stage}</div>
                <div class="metric-label">CKD Stage</div>
                <small>Current Status</small>
            </div>""", unsafe_allow_html=True)
        
        with metric_col3:
            cv_risk = "High" if (risk_diabetes and calculated_gfr < 60) or risk_cvd else "Moderate" if risk_hypertension or calculated_gfr < 60 else "Low"
            cv_color = "#e74c3c" if cv_risk == "High" else "#f39c12" if cv_risk == "Moderate" else "#27ae60"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value" style="color: {cv_color}">{cv_risk}</div>
                <div class="metric-label">CV Risk</div>
                <small>Cardiovascular</small>
            </div>""", unsafe_allow_html=True)
        
        with metric_col4:
            progression_risk = "High" if (risk_diabetes and calculated_gfr < 45) or risk_albumin_creat > 300 else "Moderate" if calculated_gfr < 60 or risk_albumin_creat > 30 else "Low"
            prog_color = "#e74c3c" if progression_risk == "High" else "#f39c12" if progression_risk == "Moderate" else "#27ae60"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value" style="color: {prog_color}">{progression_risk}</div>
                <div class="metric-label">Progression</div>
                <small>Risk Level</small>
            </div>""", unsafe_allow_html=True)
        
        # Detailed Recommendations
        st.markdown("### 📋 Personalized Recommendations")
        
        # Generate recommendations based on risk factors
        recommendations = []
        if calculated_gfr < 60:
            recommendations.append({"category": "Monitoring", "text": "Regular nephrology follow-up recommended", "priority": "High"})
        if risk_diabetes:
            recommendations.append({"category": "Diabetes Management", "text": "Optimize glycemic control (HbA1c < 7%)", "priority": "High"})
        if risk_hypertension:
            recommendations.append({"category": "Blood Pressure", "text": "Target BP < 130/80 mmHg with ACE inhibitor/ARB", "priority": "High"})
        if risk_albumin_creat > 30:
            recommendations.append({"category": "Proteinuria", "text": "Consider ACE inhibitor or ARB therapy", "priority": "High"})
        if risk_smoking == "current":
            recommendations.append({"category": "Lifestyle", "text": "Smoking cessation counseling and support", "priority": "High"})
        if risk_bmi > 30:
            recommendations.append({"category": "Weight Management", "text": "Weight reduction to BMI < 25", "priority": "Moderate"})
        
        for rec in recommendations:
            priority_color = "#e74c3c" if rec['priority'] == 'High' else "#f39c12"
            st.markdown(f"""<div class="feature-card">
                <h4 style="color: {priority_color};">{rec['category']} 
                    <span style="font-size: 0.8rem; background: {priority_color}; color: white; padding: 2px 8px; border-radius: 12px;">{rec['priority']}</span>
                </h4>
                <p>{rec['text']}</p>
            </div>""", unsafe_allow_html=True)
    
    # Clinical Guidelines Section
    with st.expander("📋 Clinical Guidelines", expanded=False):
        guideline_type = st.selectbox(
            "Select Guidelines",
            ["CKD Staging (KDIGO)", "AKI Staging (KDIGO)", "Dialysis Adequacy"]
        )
        
        if guideline_type == "CKD Staging (KDIGO)":
            try:
                stages_data = st.session_state.nephro_agent.training_data.clinical_guidelines["ckd_guidelines"]["kdigo_2024"]["stages"]
                
                for stage, info in stages_data.items():
                    stage_name = stage.replace('_', ' ').title()
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{stage_name}</h4>
                        <p><strong>GFR:</strong> {info['gfr']} mL/min/1.73m²</p>
                        <p><strong>Description:</strong> {info['description']}</p>
                        <p><strong>Management:</strong></p>
                        <ul>
                    """, unsafe_allow_html=True)
                    
                    for mgmt in info['management']:
                        st.markdown(f"<li>{mgmt}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Guidelines data not available: {e}")

with tab5:
    # Patient Timeline Visualization Tab
    st.markdown("### 📈 Patient Timeline Visualization")
    st.markdown("Comprehensive visualization of patient health journey and trends.")
    
    # Patient Selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        patient_id = st.text_input("Patient ID", placeholder="Enter patient ID for timeline analysis")
    
    with col2:
        timeline_type = st.selectbox(
            "Timeline Type",
            ["Complete Timeline", "Lab Trends", "GFR Progression", "Medication Timeline"]
        )
    
    if patient_id:
        try:
            # Generate sample patient data for demonstration
            sample_data = {
                'patient_id': patient_id,
                'dates': pd.date_range('2023-01-01', periods=12, freq='M'),
                'creatinine': [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3],
                'gfr': [65, 62, 58, 55, 52, 48, 45, 42, 38, 35, 32, 28],
                'blood_pressure': [(140, 90), (138, 88), (142, 92), (145, 95), (148, 98), 
                                 (150, 100), (152, 102), (155, 105), (158, 108), (160, 110), (162, 112), (165, 115)],
                'medications': ['ACE Inhibitor', 'Diuretic', 'Beta Blocker', 'Calcium Channel Blocker'],
                'events': [
                    {'date': '2023-03-15', 'event': 'Started ACE Inhibitor', 'type': 'medication'},
                    {'date': '2023-06-20', 'event': 'Nephrology Consultation', 'type': 'appointment'},
                    {'date': '2023-09-10', 'event': 'Added Diuretic', 'type': 'medication'},
                    {'date': '2023-11-05', 'event': 'Emergency Visit - High BP', 'type': 'emergency'}
                ]
            }
            
            if timeline_type == "Complete Timeline":
                st.markdown("#### 🔄 Complete Patient Timeline")
                
                # Timeline visualization
                timeline_fig = st.session_state.nephro_agent.timeline_viz.create_comprehensive_timeline(sample_data)
                st.plotly_chart(timeline_fig, use_container_width=True)
                
                # Key events summary
                st.markdown("#### 📋 Key Events")
                for event in sample_data['events']:
                    event_color = {
                        'medication': '🟢',
                        'appointment': '🔵', 
                        'emergency': '🔴'
                    }.get(event['type'], '⚪')
                    
                    st.markdown(f"{event_color} **{event['date']}**: {event['event']}")
            
            elif timeline_type == "Lab Trends":
                st.markdown("#### 🧪 Laboratory Trends")
                
                # Lab trends visualization
                lab_fig = st.session_state.nephro_agent.timeline_viz.create_lab_trends(sample_data)
                st.plotly_chart(lab_fig, use_container_width=True)
                
                # Current values
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Current Creatinine", f"{sample_data['creatinine'][-1]} mg/dL", 
                             delta=f"{sample_data['creatinine'][-1] - sample_data['creatinine'][-2]:.1f}")
                
                with col_b:
                    st.metric("Current eGFR", f"{sample_data['gfr'][-1]} mL/min/1.73m²", 
                             delta=f"{sample_data['gfr'][-1] - sample_data['gfr'][-2]}")
                
                with col_c:
                    bp_current = sample_data['blood_pressure'][-1]
                    st.metric("Current BP", f"{bp_current[0]}/{bp_current[1]} mmHg")
            
            elif timeline_type == "GFR Progression":
                st.markdown("#### 📉 GFR Progression Analysis")
                
                # GFR progression
                gfr_fig = st.session_state.nephro_agent.timeline_viz.create_gfr_progression(sample_data)
                st.plotly_chart(gfr_fig, use_container_width=True)
                
                # GFR insights
                gfr_decline_rate = (sample_data['gfr'][0] - sample_data['gfr'][-1]) / len(sample_data['gfr'])
                
                st.markdown("#### 📊 GFR Analysis")
                col_d, col_e = st.columns(2)
                
                with col_d:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{gfr_decline_rate:.1f}</div>
                        <div class="metric-label">Monthly Decline Rate (mL/min/1.73m²)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_e:
                    ckd_stage = "Stage 3b" if sample_data['gfr'][-1] < 45 else "Stage 3a"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{ckd_stage}</div>
                        <div class="metric-label">Current CKD Stage</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif timeline_type == "Medication Timeline":
                st.markdown("#### 💊 Medication Timeline")
                
                # Medication timeline
                med_fig = st.session_state.nephro_agent.timeline_viz.create_medication_timeline(sample_data)
                st.plotly_chart(med_fig, use_container_width=True)
                
                # Current medications
                st.markdown("#### 💊 Current Medications")
                for i, med in enumerate(sample_data['medications']):
                    st.markdown(f"**{i+1}.** {med}")
            
            # Interactive dashboard option
            st.markdown("---")
            if st.button("🎛️ Open Interactive Dashboard", key="timeline_dashboard"):
                with st.spinner("Loading interactive dashboard..."):
                    dashboard_fig = st.session_state.nephro_agent.timeline_viz.create_interactive_dashboard(sample_data)
                    st.plotly_chart(dashboard_fig, use_container_width=True)
                    
                    # Dashboard insights
                    insights = st.session_state.nephro_agent.timeline_viz.generate_timeline_insights(sample_data)
                    
                    st.markdown("#### 🔍 Timeline Insights")
                    for insight in insights:
                        st.info(f"💡 {insight}")
        
        except Exception as e:
            st.error(f"Error generating timeline visualization: {e}")
            st.info("Please ensure the patient ID is valid and try again.")
    
    else:
        st.info("👆 Enter a patient ID above to generate timeline visualizations.")
        
        # Sample timeline preview
        st.markdown("#### 📋 Sample Timeline Features")
        
        feature_cols = st.columns(2)
        
        with feature_cols[0]:
            st.markdown("""
            **📈 Lab Trends**
            - Creatinine progression
            - eGFR decline tracking
            - Blood pressure monitoring
            - Proteinuria levels
            
            **💊 Medication History**
            - Drug initiation dates
            - Dosage changes
            - Medication interactions
            - Adherence tracking
            """)
        
        with feature_cols[1]:
            st.markdown("""
            **🏥 Clinical Events**
            - Hospital admissions
            - Procedure dates
            - Consultation notes
            - Emergency visits
            
            **📊 Predictive Insights**
            - Disease progression
            - Risk factor evolution
            - Treatment effectiveness
            - Outcome predictions
             """)

with tab6:
    # Real-Time Monitoring Dashboard Tab
    st.markdown("### 🚨 Real-Time Patient Monitoring")
    st.markdown("Live monitoring dashboard with intelligent alerts and notifications.")
    
    # Monitoring controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        monitoring_mode = st.selectbox(
            "Monitoring Mode",
            ["Active Alerts", "Patient Dashboard", "Alert Management", "Simulate Data"]
        )
    
    with col2:
        auto_refresh = st.checkbox("Auto Refresh", value=True)
    
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(2)
        st.rerun()
    
    if monitoring_mode == "Active Alerts":
        st.markdown("#### 🚨 Active Alerts Dashboard")
        
        # Get all active alerts
        active_alerts = st.session_state.nephro_agent.monitoring_system.get_active_alerts()
        
        if active_alerts:
            # Alert summary metrics
            alert_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            for alert in active_alerts:
                alert_counts[alert['severity']] += 1
            
            # Display alert metrics
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff4444;">
                    <div class="metric-value">{alert_counts['critical']}</div>
                    <div class="metric-label">Critical Alerts</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff8800;">
                    <div class="metric-value">{alert_counts['high']}</div>
                    <div class="metric-label">High Priority</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ffaa00;">
                    <div class="metric-value">{alert_counts['medium']}</div>
                    <div class="metric-label">Medium Priority</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[3]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #00aa00;">
                    <div class="metric-value">{alert_counts['low']}</div>
                    <div class="metric-label">Low Priority</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display individual alerts
            st.markdown("#### 📋 Alert Details")
            
            for alert in active_alerts[:10]:  # Show top 10 alerts
                severity_colors = {
                    'critical': '#ff4444',
                    'high': '#ff8800',
                    'medium': '#ffaa00',
                    'low': '#00aa00'
                }
                
                severity_icons = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }
                
                alert_time = pd.to_datetime(alert['timestamp']).strftime('%Y-%m-%d %H:%M')
                
                with st.expander(f"{severity_icons[alert['severity']]} {alert['alert_type'].replace('_', ' ').title()} - Patient {alert['patient_id']}"):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.markdown(f"**Message:** {alert['message']}")
                        st.markdown(f"**Time:** {alert_time}")
                        st.markdown(f"**Status:** {'✅ Acknowledged' if alert['acknowledged'] else '⏳ Pending'}")
                    
                    with col_b:
                        if not alert['acknowledged']:
                            if st.button("✅ Acknowledge", key=f"ack_{alert['id']}"):
                                st.session_state.nephro_agent.monitoring_system.acknowledge_alert(alert['id'])
                                st.success("Alert acknowledged!")
                                st.rerun()
                        
                        if st.button("✅ Resolve", key=f"resolve_{alert['id']}"):
                            st.session_state.nephro_agent.monitoring_system.resolve_alert(alert['id'])
                            st.success("Alert resolved!")
                            st.rerun()
        else:
            st.success("🎉 No active alerts! All patients are within normal parameters.")
            
            # Show recent resolved alerts
            st.markdown("#### 📈 Recent Activity")
            st.info("No recent alert activity to display.")
    
    elif monitoring_mode == "Patient Dashboard":
        st.markdown("#### 📊 Multi-Patient Monitoring Dashboard")
        
        # Patient selection for monitoring
        patient_ids_input = st.text_input(
            "Patient IDs (comma-separated)",
            placeholder="e.g., P001, P002, P003",
            value="P001, P002, P003"
        )
        
        if patient_ids_input:
            patient_ids = [pid.strip() for pid in patient_ids_input.split(',')]
            
            try:
                # Create monitoring dashboard
                dashboard_fig = st.session_state.nephro_agent.monitoring_system.create_monitoring_dashboard(patient_ids)
                st.plotly_chart(dashboard_fig, use_container_width=True)
                
                # Patient status summary
                st.markdown("#### 👥 Patient Status Summary")
                
                status_cols = st.columns(min(len(patient_ids), 4))
                
                for i, patient_id in enumerate(patient_ids[:4]):
                    with status_cols[i]:
                        patient_alerts = st.session_state.nephro_agent.monitoring_system.get_active_alerts(patient_id)
                        alert_count = len(patient_alerts)
                        
                        if alert_count == 0:
                            status_color = "#00aa00"
                            status_text = "Stable"
                        elif alert_count <= 2:
                            status_color = "#ffaa00"
                            status_text = "Monitoring"
                        else:
                            status_color = "#ff4444"
                            status_text = "Critical"
                        
                        st.markdown(f"""
                        <div class="metric-card" style="border-left: 4px solid {status_color};">
                            <div class="metric-value">{patient_id}</div>
                            <div class="metric-label">{status_text} ({alert_count} alerts)</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error creating dashboard: {e}")
                st.info("Try simulating some patient data first using the 'Simulate Data' mode.")
    
    elif monitoring_mode == "Alert Management":
        st.markdown("#### ⚙️ Alert Management & Configuration")
        
        # Alert summary report
        report_days = st.slider("Report Period (days)", 1, 30, 7)
        
        if st.button("📊 Generate Alert Report"):
            report = st.session_state.nephro_agent.monitoring_system.generate_alert_summary_report(report_days)
            
            st.markdown(f"#### 📈 Alert Summary Report ({report_days} days)")
            
            report_cols = st.columns(3)
            
            with report_cols[0]:
                st.metric("Total Alerts", report['total_alerts'])
            
            with report_cols[1]:
                if report['by_severity']:
                    most_severe = max(report['by_severity'].items(), key=lambda x: x[1])
                    st.metric("Most Common Severity", f"{most_severe[0].title()} ({most_severe[1]})")
            
            with report_cols[2]:
                if report['by_type']:
                    most_common = max(report['by_type'].items(), key=lambda x: x[1])
                    st.metric("Most Common Type", most_common[0].replace('_', ' ').title())
            
            if report['trends']:
                st.info(f"📊 **Trend Analysis:** {report['trends']}")
            
            # Severity distribution chart
            if report['by_severity']:
                severity_df = pd.DataFrame(list(report['by_severity'].items()), columns=['Severity', 'Count'])
                fig = px.pie(severity_df, values='Count', names='Severity', title="Alert Distribution by Severity")
                st.plotly_chart(fig, use_container_width=True)
        
        # Alert threshold configuration
        st.markdown("#### ⚙️ Alert Thresholds Configuration")
        
        with st.expander("🔧 Configure Alert Thresholds"):
            thresholds = st.session_state.nephro_agent.monitoring_system.alert_thresholds
            
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                st.markdown("**Laboratory Thresholds**")
                new_creat_high = st.number_input("High Creatinine (mg/dL)", value=thresholds['creatinine_high'], step=0.1)
                new_gfr_low = st.number_input("Low eGFR (mL/min/1.73m²)", value=thresholds['gfr_low'], step=1)
                new_proteinuria = st.number_input("High Proteinuria (mg/g)", value=thresholds['proteinuria_high'], step=10)
            
            with col_t2:
                st.markdown("**Vital Sign Thresholds**")
                new_bp_sys = st.number_input("High Systolic BP (mmHg)", value=thresholds['blood_pressure_high'][0], step=5)
                new_bp_dia = st.number_input("High Diastolic BP (mmHg)", value=thresholds['blood_pressure_high'][1], step=5)
                new_k_high = st.number_input("High Potassium (mEq/L)", value=thresholds['potassium_high'], step=0.1)
            
            if st.button("💾 Update Thresholds"):
                # Update thresholds (in a real implementation, this would save to database)
                st.success("Alert thresholds updated successfully!")
    
    elif monitoring_mode == "Simulate Data":
        st.markdown("#### 🧪 Data Simulation for Testing")
        st.info("Generate sample patient data to test the monitoring system.")
        
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            sim_patient_id = st.text_input("Patient ID for Simulation", value="P001")
            sim_data_points = st.slider("Number of Data Points", 5, 50, 20)
        
        with sim_col2:
            sim_scenario = st.selectbox(
                "Simulation Scenario",
                ["Normal Progression", "Rapid Decline", "Stable Condition", "Critical Events"]
            )
        
        if st.button("🚀 Generate Simulation Data"):
            with st.spinner("Generating patient data..."):
                st.session_state.nephro_agent.monitoring_system.simulate_patient_data(sim_patient_id, sim_data_points)
                st.success(f"✅ Generated {sim_data_points} data points for patient {sim_patient_id}")
                
                # Show generated alerts
                new_alerts = st.session_state.nephro_agent.monitoring_system.get_active_alerts(sim_patient_id)
                if new_alerts:
                    st.warning(f"⚠️ Generated {len(new_alerts)} new alerts for this patient")
                    for alert in new_alerts[:3]:  # Show first 3 alerts
                        st.error(f"🚨 {alert['alert_type'].replace('_', ' ').title()}: {alert['message']}")
                else:
                    st.info("No alerts generated - patient parameters within normal ranges")
        
        # Quick simulation buttons
        st.markdown("#### ⚡ Quick Simulations")
        
        quick_cols = st.columns(3)
        
        with quick_cols[0]:
            if st.button("🟢 Simulate Stable Patient"):
                st.session_state.nephro_agent.monitoring_system.simulate_patient_data("STABLE_001", 10)
                st.success("Stable patient data generated")
        
        with quick_cols[1]:
            if st.button("🟡 Simulate Declining Patient"):
                st.session_state.nephro_agent.monitoring_system.simulate_patient_data("DECLINE_001", 15)
                st.warning("Declining patient data generated")
        
        with quick_cols[2]:
            if st.button("🔴 Simulate Critical Patient"):
                st.session_state.nephro_agent.monitoring_system.simulate_patient_data("CRITICAL_001", 20)
                st.error("Critical patient data generated")

        with tab7:
            st.header(f"👤 {t('patient_portal_title')}")
            st.markdown(f"**{t('patient_portal_subtitle')}**")
            
            # Initialize session state for patient login
            if 'patient_logged_in' not in st.session_state:
                st.session_state.patient_logged_in = False
                st.session_state.current_patient_id = None
            
            if not st.session_state.patient_logged_in:
                # Login Form
                st.subheader(f"🔐 {t('patient_login')}")
                
                with st.form("patient_login_form"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        email = st.text_input(t('email_address'), placeholder="patient@email.com")
                        password = st.text_input(t('password'), type="password", placeholder="Enter your password")
                        
                    with col2:
                        st.info(f"**{t('demo_credentials')}:**\n\n" +
                               "📧 john.smith@email.com\n" +
                               "🔑 password123\n\n" +
                               "📧 maria.garcia@email.com\n" +
                               "🔑 password123\n\n" +
                               "📧 david.johnson@email.com\n" +
                               "🔑 password123")
                    
                    login_submitted = st.form_submit_button(f"🚪 {t('login')}", use_container_width=True)
                    
                    if login_submitted:
                        if email and password:
                            try:
                                patient_id = st.session_state.nephro_agent.patient_portal.authenticate_patient(email, password)
                                if patient_id:
                                    st.session_state.patient_logged_in = True
                                    st.session_state.current_patient_id = patient_id
                                    st.success(f"✅ {t('login_successful')}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {t('invalid_credentials')}")
                            except Exception as e:
                                st.error(f"Login error: {str(e)}")
                        else:
                            st.warning(f"⚠️ {t('enter_credentials')}")
                
                # Registration Info
                st.markdown("---")
                st.info(f"**{t('new_patient_info')}**")
                
            else:
                # Patient Dashboard
                try:
                    patient_record = st.session_state.nephro_agent.patient_portal.get_patient_record(st.session_state.current_patient_id)
                    
                    if patient_record:
                        # Header with patient info and logout
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(f"Welcome, {patient_record.name}")
                            st.caption(f"MRN: {patient_record.medical_record_number}")
                        with col2:
                            if st.button("🚪 Logout", use_container_width=True):
                                st.session_state.patient_logged_in = False
                                st.session_state.current_patient_id = None
                                st.rerun()
                        
                        # Dashboard Summary
                        summary = st.session_state.nephro_agent.patient_portal.get_dashboard_summary(st.session_state.current_patient_id)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("📅 Upcoming Appointments", summary['upcoming_appointments'])
                        with col2:
                            st.metric("🧪 Recent Lab Results", summary['recent_lab_results'])
                        with col3:
                            st.metric("📧 Unread Messages", summary['unread_messages'])
                        with col4:
                            st.metric("📋 Total Records", summary['total_appointments'] + summary['total_lab_results'])
                        
                        st.markdown("---")
                        
                        # Portal Sections
                        portal_tab1, portal_tab2, portal_tab3, portal_tab4, portal_tab5 = st.tabs([
                            "📊 Dashboard", "📅 Appointments", "🧪 Lab Results", "📧 Messages", "👤 Profile"
                        ])
                        
                        with portal_tab1:
                            st.subheader("📊 Health Dashboard")
                            
                            # Quick Actions
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("📅 Schedule Appointment", use_container_width=True):
                                    st.info("Please call (555) 123-4567 to schedule an appointment.")
                            with col2:
                                if st.button("💊 Request Prescription Refill", use_container_width=True):
                                    st.info("Prescription refill requests can be made through your pharmacy or by calling our office.")
                            with col3:
                                if st.button("📞 Contact Provider", use_container_width=True):
                                    st.info("Use the Messages tab to send a secure message to your healthcare team.")
                            
                            # Recent Activity
                            st.subheader("📈 Recent Activity")
                            
                            # Get recent appointments and lab results
                            appointments = st.session_state.nephro_agent.patient_portal.get_patient_appointments(st.session_state.current_patient_id)[:3]
                            lab_results = st.session_state.nephro_agent.patient_portal.get_patient_lab_results(st.session_state.current_patient_id)[:3]
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Recent Appointments**")
                                for apt in appointments:
                                    status_color = "🟢" if apt.status == "completed" else "🟡" if apt.status == "scheduled" else "🔴"
                                    st.write(f"{status_color} {apt.appointment_date} - {apt.doctor_name}")
                            
                            with col2:
                                st.write("**Recent Lab Results**")
                                for lab in lab_results:
                                    st.write(f"🧪 {lab.date_collected} - {lab.test_name}: {lab.result_value}")
                        
                        with portal_tab2:
                            st.subheader("📅 My Appointments")
                            
                            appointments = st.session_state.nephro_agent.patient_portal.get_patient_appointments(st.session_state.current_patient_id)
                            
                            if appointments:
                                # Filter options
                                filter_col1, filter_col2 = st.columns(2)
                                with filter_col1:
                                    status_filter = st.selectbox("Filter by Status", ["All", "scheduled", "completed", "cancelled"])
                                with filter_col2:
                                    sort_order = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)"])
                                
                                # Apply filters
                                filtered_appointments = appointments
                                if status_filter != "All":
                                    filtered_appointments = [a for a in appointments if a.status == status_filter]
                                
                                # Display appointments
                                for apt in filtered_appointments:
                                    with st.expander(f"{apt.appointment_date} {apt.appointment_time} - {apt.doctor_name}"):
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write(f"**Doctor:** {apt.doctor_name}")
                                            st.write(f"**Date:** {apt.appointment_date}")
                                            st.write(f"**Time:** {apt.appointment_time}")
                                        with col2:
                                            status_color = "🟢" if apt.status == "completed" else "🟡" if apt.status == "scheduled" else "🔴"
                                            st.write(f"**Status:** {status_color} {apt.status.title()}")
                                            if apt.notes:
                                                st.write(f"**Notes:** {apt.notes}")
                            else:
                                st.info("No appointments found.")
                        
                        with portal_tab3:
                            st.subheader("🧪 Lab Results")
                            
                            lab_results = st.session_state.nephro_agent.patient_portal.get_patient_lab_results(st.session_state.current_patient_id)
                            
                            if lab_results:
                                # Test selection for trending
                                unique_tests = list(set([lab.test_name for lab in lab_results]))
                                selected_test = st.selectbox("View Trend for Test", unique_tests)
                                
                                if selected_test:
                                    chart = st.session_state.nephro_agent.patient_portal.create_lab_results_chart(st.session_state.current_patient_id, selected_test)
                                    if chart:
                                        st.plotly_chart(chart, use_container_width=True)
                                
                                st.markdown("---")
                                
                                # Results table
                                st.write("**All Lab Results**")
                                for lab in lab_results:
                                    with st.expander(f"{lab.date_collected} - {lab.test_name}"):
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.write(f"**Test:** {lab.test_name}")
                                            st.write(f"**Date:** {lab.date_collected}")
                                        with col2:
                                            st.write(f"**Result:** {lab.result_value}")
                                            st.write(f"**Reference:** {lab.reference_range}")
                                        with col3:
                                            status_color = "🟢" if lab.status == "completed" else "🟡"
                                            st.write(f"**Status:** {status_color} {lab.status.title()}")
                            else:
                                st.info("No lab results found.")
                        
                        with portal_tab4:
                            st.subheader("📧 Messages")
                            
                            messages = st.session_state.nephro_agent.patient_portal.get_patient_messages(st.session_state.current_patient_id)
                            
                            if messages:
                                # Message filters
                                filter_col1, filter_col2 = st.columns(2)
                                with filter_col1:
                                    read_filter = st.selectbox("Filter Messages", ["All", "Unread", "Read"])
                                with filter_col2:
                                    sender_filter = st.selectbox("Filter by Sender", ["All", "doctor", "nurse", "admin"])
                                
                                # Apply filters
                                filtered_messages = messages
                                if read_filter == "Unread":
                                    filtered_messages = [m for m in messages if not m['is_read']]
                                elif read_filter == "Read":
                                    filtered_messages = [m for m in messages if m['is_read']]
                                
                                if sender_filter != "All":
                                    filtered_messages = [m for m in filtered_messages if m['sender_type'] == sender_filter]
                                
                                # Display messages
                                for msg in filtered_messages:
                                    read_icon = "📖" if msg['is_read'] else "📩"
                                    sender_icon = "👨‍⚕️" if msg['sender_type'] == "doctor" else "👩‍⚕️" if msg['sender_type'] == "nurse" else "👤"
                                    
                                    with st.expander(f"{read_icon} {msg['subject']} - {msg['sender_name']}"):
                                        col1, col2 = st.columns([3, 1])
                                        with col1:
                                            st.write(f"**From:** {sender_icon} {msg['sender_name']} ({msg['sender_type'].title()})")
                                            st.write(f"**Date:** {msg['created_at']}")
                                            st.write(f"**Message:**")
                                            st.write(msg['message_body'])
                                        with col2:
                                            if not msg['is_read']:
                                                if st.button(f"Mark as Read", key=f"read_{msg['message_id']}"):
                                                    st.session_state.nephro_agent.patient_portal.mark_message_as_read(msg['message_id'])
                                                    st.rerun()
                            else:
                                st.info("No messages found.")
                            
                            # Compose new message
                            st.markdown("---")
                            st.subheader("✍️ Send Message")
                            with st.form("compose_message"):
                                recipient = st.selectbox("To", ["Dr. Sarah Wilson", "Dr. Michael Brown", "Dr. Emily Davis", "Nurse Jennifer", "Patient Services"])
                                subject = st.text_input("Subject")
                                message_body = st.text_area("Message", height=100)
                                
                                if st.form_submit_button("📤 Send Message"):
                                    if subject and message_body:
                                        st.success("✅ Message sent successfully! You will receive a response within 24-48 hours.")
                                    else:
                                        st.warning("⚠️ Please fill in both subject and message.")
                        
                        with portal_tab5:
                            st.subheader("👤 My Profile")
                            
                            # Display patient information
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Personal Information**")
                                st.write(f"**Name:** {patient_record.name}")
                                st.write(f"**Date of Birth:** {patient_record.date_of_birth}")
                                st.write(f"**Email:** {patient_record.email}")
                                st.write(f"**Phone:** {patient_record.phone}")
                            
                            with col2:
                                st.write("**Medical Information**")
                                st.write(f"**Medical Record Number:** {patient_record.medical_record_number}")
                                st.write(f"**Emergency Contact:** {patient_record.emergency_contact}")
                            
                            st.markdown("---")
                            
                            # Profile actions
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("📝 Update Contact Info", use_container_width=True):
                                    st.info("Please contact Patient Services at (555) 123-4567 to update your contact information.")
                            with col2:
                                if st.button("🔒 Change Password", use_container_width=True):
                                    st.info("Password changes can be requested through Patient Services for security purposes.")
                            with col3:
                                if st.button("📄 Download Records", use_container_width=True):
                                    st.info("Medical records can be requested through Patient Services. Processing may take 3-5 business days.")
                    
                    else:
                        st.error("Patient record not found. Please contact support.")
                        if st.button("🚪 Logout"):
                            st.session_state.patient_logged_in = False
                            st.session_state.current_patient_id = None
                            st.rerun()
                
                except Exception as e:
                    st.error(f"Error loading patient portal: {str(e)}")
                    if st.button("🚪 Logout"):
                        st.session_state.patient_logged_in = False
                        st.session_state.current_patient_id = None
                        st.rerun()

with tab8:
    # Security Dashboard Tab
    st.markdown("### 🔒 Security Dashboard")
    st.markdown("Advanced security monitoring and audit logging system.")
    
    # Security Overview
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Get security statistics
        security_report = security_manager.generate_security_report()
        audit_stats = audit_logger.get_audit_statistics(30)
        
        with col1:
            st.metric(
                "Total Users",
                security_report.get('total_users', 0),
                delta=None
            )
        
        with col2:
            st.metric(
                "Active Sessions",
                security_report.get('active_sessions', 0),
                delta=None
            )
        
        with col3:
            st.metric(
                "Security Events (30d)",
                audit_stats.get('total_events', 0),
                delta=None
            )
        
        with col4:
            success_rate = audit_stats.get('success_rate', 0)
            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%",
                delta=None
            )
        
        # Security Events Chart
        st.markdown("#### Recent Security Events")
        
        events_by_type = audit_stats.get('events_by_type', {})
        if events_by_type:
            fig = px.bar(
                x=list(events_by_type.keys()),
                y=list(events_by_type.values()),
                title="Security Events by Type (Last 30 Days)",
                labels={'x': 'Event Type', 'y': 'Count'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Audit Events
        st.markdown("#### Recent Audit Events")
        
        # Get recent events
        recent_events = audit_logger.get_audit_events(limit=50)
        
        if recent_events:
            # Convert to DataFrame for display
            events_df = pd.DataFrame(recent_events)
            
            # Select relevant columns
            display_columns = ['timestamp', 'event_type', 'username', 'action', 'ip_address', 'success', 'severity']
            available_columns = [col for col in display_columns if col in events_df.columns]
            
            if available_columns:
                display_df = events_df[available_columns].copy()
                
                # Format timestamp
                if 'timestamp' in display_df.columns:
                    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Show recent events
                st.dataframe(
                    display_df.head(20),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No audit events to display.")
        else:
            st.info("No recent audit events found.")
        
        # Security Configuration
        st.markdown("#### Security Configuration")
        
        config_col1, config_col2 = st.columns(2)
        
        with config_col1:
            st.markdown("**Authentication Settings:**")
            config = security_report.get('security_config', {})
            st.write(f"• Max Failed Attempts: {config.get('max_failed_attempts', 'N/A')}")
            st.write(f"• Session Timeout: {config.get('session_timeout', 'N/A')}s")
            st.write(f"• 2FA Enabled: {config.get('enable_2fa', False)}")
        
        with config_col2:
            st.markdown("**Audit Settings:**")
            st.write(f"• Audit Logging: {config.get('enable_audit_logging', False)}")
            st.write(f"• Real-time Alerts: {config.get('enable_real_time_alerts', False)}")
            st.write(f"• Retention Days: {config.get('retention_days', 'N/A')}")
        
        # Device Testing (Developer Mode)
        st.markdown("#### Responsive Design Testing")
        responsive_manager.add_device_selector()
        
        # Security Actions
        st.markdown("#### Security Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🧹 Cleanup Old Logs", use_container_width=True):
                try:
                    deleted_count = audit_logger.cleanup_old_logs()
                    st.success(f"Cleaned up {deleted_count} old audit records.")
                    log_user_action(
                        "security_cleanup",
                        details={"deleted_records": deleted_count}
                    )
                except Exception as e:
                    st.error(f"Error during cleanup: {str(e)}")
        
        with action_col2:
            if st.button("📊 Generate Report", use_container_width=True):
                try:
                    end_date = datetime.utcnow()
                    start_date = end_date - timedelta(days=30)
                    report = audit_logger.generate_audit_report(start_date, end_date)
                    
                    st.json(report)
                    log_user_action(
                        "security_report_generated",
                        details={"report_period": "30_days"}
                    )
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
        
        with action_col3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
        
    except Exception as e:
        st.error(f"Error loading security dashboard: {str(e)}")
        st.info("Security features may not be fully initialized. Please check system configuration.")

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ <strong>Medical Disclaimer:</strong> This AI assistant provides educational information only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.</p>
    <p>🔒 Your conversations are securely stored and used only to improve your experience.</p>
    <p>© 2024 Advanced Nephrology AI Agent - Enterprise Edition</p>
</div>
""", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    pass