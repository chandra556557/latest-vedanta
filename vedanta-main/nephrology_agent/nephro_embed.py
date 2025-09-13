import os
import streamlit as st
import google.generativeai as genai
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page for iframe embedding
st.set_page_config(
    page_title="Dr. Nephro - Kidney Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide Streamlit elements for clean embedding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}
.stToolbar {display:none;}
#stDecoration {display:none;}
.css-1rs6os {display:none;}
.css-17ziqus {display:none;}
.css-1v0mbdj {display:none;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
.stChatMessage {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 10px;
    margin: 5px 0;
}
.stChatInput {
    border-radius: 20px;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
if GEMINI_API_KEY and GEMINI_API_KEY != "your-api-key-here":
    genai.configure(api_key=GEMINI_API_KEY)

class NephrologyAgent:
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
        Keep responses concise but comprehensive for chat interface.
        """
    
    def get_response(self, user_input: str) -> str:
        try:
            prompt = f"{self.nephrology_context}\n\nPatient/User Question: {user_input}\n\nProvide a helpful, concise response:"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}. Please ensure your API key is configured correctly."

# Initialize the agent
if 'nephro_agent' not in st.session_state:
    st.session_state.nephro_agent = NephrologyAgent()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    welcome_msg = "👋 Hello! I'm Dr. Nephro, your AI kidney health assistant. I'm here to help with questions about kidney health, chronic kidney disease, dialysis, and more. How can I assist you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Compact header
st.markdown("""
<div style='text-align: center; padding: 10px; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0;'>🩺 Dr. Nephro</h2>
    <p style='color: #e8f4fd; margin: 5px 0 0 0; font-size: 14px;'>AI Kidney Health Assistant</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about kidney health..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Dr. Nephro is thinking..."):
                response = st.session_state.nephro_agent.get_response(prompt)
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

# Emergency notice at bottom
st.markdown("""
<div style='background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 10px; margin-top: 20px; font-size: 12px;'>
    <strong>⚠️ Important:</strong> This is for educational purposes only. For medical emergencies, call emergency services immediately. Always consult your healthcare provider for medical advice.
</div>
""", unsafe_allow_html=True)