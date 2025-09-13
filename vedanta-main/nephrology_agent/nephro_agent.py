import os
import streamlit as st
import google.generativeai as genai
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
if GEMINI_API_KEY and GEMINI_API_KEY != "your-api-key-here":
    genai.configure(api_key=GEMINI_API_KEY)

class NephrologyAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversation_history = []
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
        """
    
    def get_response(self, user_input: str) -> str:
        try:
            # Add nephrology context to the conversation
            prompt = f"{self.nephrology_context}\n\nPatient/User Question: {user_input}\n\nProvide a comprehensive, helpful response:"
            
            response = self.model.generate_content(prompt)
            
            # Store conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "ai_response": response.text
            })
            
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}. Please ensure your API key is configured correctly."
    
    def get_kidney_health_assessment(self, symptoms: List[str], medical_history: Dict) -> str:
        assessment_prompt = f"""
        {self.nephrology_context}
        
        Please provide a kidney health assessment based on:
        Symptoms: {', '.join(symptoms)}
        Medical History: {medical_history}
        
        Provide:
        1. Possible kidney-related conditions to consider
        2. Recommended tests or evaluations
        3. Lifestyle recommendations
        4. When to seek immediate medical care
        
        Remember to emphasize this is educational and not a diagnosis.
        """
        
        try:
            response = self.model.generate_content(assessment_prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate assessment. Error: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Nephrology AI Agent - Dr. Nephro",
        page_icon="🫘",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1f77b4;
        color: white;
    }
    .kidney-info {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the agent
    if 'nephro_agent' not in st.session_state:
        st.session_state.nephro_agent = NephrologyAgent()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Header
    st.title("🫘 Dr. Nephro - Nephrology AI Assistant")
    st.markdown("### Your specialized AI companion for kidney health and nephrology questions")
    
    # Sidebar
    with st.sidebar:
        st.header("🏥 Quick Actions")
        
        if st.button("🆘 Emergency Symptoms"):
            st.error("""
            **Seek immediate medical attention if you experience:**
            - Severe decrease in urination or no urination
            - Severe swelling in legs, ankles, or face
            - Difficulty breathing
            - Chest pain
            - Severe nausea and vomiting
            - Confusion or altered mental state
            - Blood in urine (hematuria)
            - Severe flank pain
            """)
        
        st.markdown("---")
        st.header("📋 Common Topics")
        
        topics = [
            "Chronic Kidney Disease (CKD)",
            "Dialysis Information",
            "Kidney Stones",
            "High Blood Pressure & Kidneys",
            "Diabetes & Kidney Health",
            "Kidney Transplant",
            "Diet for Kidney Health",
            "Medications & Kidneys"
        ]
        
        for topic in topics:
            if st.button(topic):
                st.session_state.selected_topic = topic
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with Dr. Nephro")
        
        # Display chat history
        if st.session_state.chat_history:
            for i, chat in enumerate(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**You:** {chat['user']}")
                    st.markdown(f"**Dr. Nephro:** {chat['assistant']}")
                    st.markdown("---")
        
        # Chat input
        user_input = st.text_area(
            "Ask Dr. Nephro about kidney health, symptoms, treatments, or any nephrology-related questions:",
            height=100,
            placeholder="e.g., What are the early signs of kidney disease? How can I protect my kidneys if I have diabetes?"
        )
        
        if st.button("Send Message", type="primary"):
            if user_input:
                with st.spinner("Dr. Nephro is thinking..."):
                    response = st.session_state.nephro_agent.get_response(user_input)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'user': user_input,
                        'assistant': response
                    })
                    
                    st.rerun()
    
    with col2:
        st.header("🔍 Kidney Health Assessment")
        
        with st.expander("Quick Health Check", expanded=True):
            st.markdown("**Select any symptoms you're experiencing:**")
            
            symptoms = []
            if st.checkbox("Swelling in legs/ankles/face"):
                symptoms.append("Swelling in legs/ankles/face")
            if st.checkbox("Changes in urination"):
                symptoms.append("Changes in urination")
            if st.checkbox("Fatigue or weakness"):
                symptoms.append("Fatigue or weakness")
            if st.checkbox("Shortness of breath"):
                symptoms.append("Shortness of breath")
            if st.checkbox("Nausea or vomiting"):
                symptoms.append("Nausea or vomiting")
            if st.checkbox("Back or flank pain"):
                symptoms.append("Back or flank pain")
            if st.checkbox("High blood pressure"):
                symptoms.append("High blood pressure")
            
            st.markdown("**Medical History:**")
            diabetes = st.checkbox("Diabetes")
            hypertension = st.checkbox("High Blood Pressure")
            family_history = st.checkbox("Family history of kidney disease")
            
            medical_history = {
                "diabetes": diabetes,
                "hypertension": hypertension,
                "family_history": family_history
            }
            
            if st.button("Get Assessment") and symptoms:
                with st.spinner("Analyzing..."):
                    assessment = st.session_state.nephro_agent.get_kidney_health_assessment(symptoms, medical_history)
                    st.markdown("### Assessment Results:")
                    st.markdown(assessment)
        
        # Educational content
        st.markdown("---")
        st.header("📚 Educational Resources")
        
        with st.expander("Kidney Function Basics"):
            st.markdown("""
            **Your kidneys:**
            - Filter waste and excess water from blood
            - Regulate blood pressure
            - Produce red blood cells
            - Balance electrolytes
            - Maintain acid-base balance
            """)
        
        with st.expander("CKD Stages"):
            st.markdown("""
            **Stage 1:** Normal/high function (GFR ≥90)
            **Stage 2:** Mild decrease (GFR 60-89)
            **Stage 3a:** Moderate decrease (GFR 45-59)
            **Stage 3b:** Moderate decrease (GFR 30-44)
            **Stage 4:** Severe decrease (GFR 15-29)
            **Stage 5:** Kidney failure (GFR <15)
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
    <strong>⚠️ Important Disclaimer:</strong> This AI assistant provides educational information only. 
    Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment. 
    In case of emergency, contact your local emergency services immediately.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()