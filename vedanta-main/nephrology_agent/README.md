# Nephrology AI Agent

A specialized AI-powered assistant for nephrology and kidney health, built with Google Gemini LLM integration.

## Features

- **Specialized Nephrology Knowledge**: Expert-level information on kidney diseases, treatments, and management
- **Interactive Chatbot**: Natural language conversations about kidney health
- **Symptom Assessment**: AI-powered evaluation of kidney-related symptoms
- **Educational Content**: Comprehensive information on nephrology topics
- **Multiple Interfaces**: Both Streamlit web app and FastAPI backend
- **Google Gemini Integration**: Powered by advanced AI language model

## Quick Start

### 1. Install Dependencies

```bash
cd nephrology_agent
pip install -r requirements.txt
```

### 2. Configure API Key

1. Copy the environment file:
   ```bash
   copy .env.example .env
   ```

2. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Edit `.env` file and replace `your-google-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```

### 3. Run the Application

#### Option A: Streamlit Web App (Recommended for end users)
```bash
streamlit run nephro_agent.py
```
Access at: http://localhost:8501

#### Option B: FastAPI Backend (For developers/API integration)
```bash
python nephro_api.py
```
Access at: http://localhost:8002
API Documentation: http://localhost:8002/docs

## Application Features

### 🩺 Chat with Dr. Nephro
- Interactive conversations about kidney health
- Personalized responses based on medical context
- Educational guidance and recommendations

### 📊 Health Assessment
- Symptom evaluation for kidney-related conditions
- Risk level assessment (low, moderate, high, urgent)
- Personalized recommendations
- Emergency symptom detection

### 📚 Kidney Health Education
- Comprehensive information on nephrology topics
- Easy-to-understand explanations
- Related topic suggestions
- Evidence-based medical content

## Supported Topics

- Chronic Kidney Disease (CKD)
- Acute Kidney Injury (AKI)
- Dialysis (Hemodialysis & Peritoneal)
- Kidney Transplantation
- Diabetic Nephropathy
- Hypertensive Nephropathy
- Glomerulonephritis
- Kidney Stones
- Polycystic Kidney Disease
- Electrolyte Disorders
- Fluid Balance Management
- Nephrotoxic Medications
- Pediatric Nephrology
- Kidney Diet and Nutrition

## API Endpoints

### FastAPI Backend Endpoints:

- `GET /` - API information
- `GET /health` - Health check
- `POST /chat` - Chat with the AI agent
- `POST /assess-symptoms` - Symptom assessment
- `POST /education` - Get educational content
- `GET /topics` - Available nephrology topics
- `GET /emergency-symptoms` - Emergency symptoms list

### Example API Usage:

```python
import requests

# Chat with the agent
response = requests.post("http://localhost:8002/chat", json={
    "message": "What are the early signs of kidney disease?",
    "conversation_history": []
})

# Assess symptoms
response = requests.post("http://localhost:8002/assess-symptoms", json={
    "symptoms": ["frequent urination", "fatigue", "swelling"],
    "medical_history": {"diabetes": True, "hypertension": False},
    "age": 45,
    "gender": "male"
})
```

## Important Medical Disclaimer

⚠️ **This application is for educational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.**

### Emergency Situations
Seek immediate medical attention if experiencing:
- Complete absence of urination
- Severe kidney pain
- Blood in urine with severe symptoms
- Difficulty breathing with swelling
- Chest pain with kidney symptoms

## Technical Details

### Architecture
- **Frontend**: Streamlit web application
- **Backend**: FastAPI with RESTful endpoints
- **AI Model**: Google Gemini 1.5 Flash
- **Language**: Python 3.8+

### Dependencies
- `fastapi` - Web framework for API
- `uvicorn` - ASGI server
- `streamlit` - Web app framework
- `google-generativeai` - Google Gemini integration
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management

## Development

### Project Structure
```
nephrology_agent/
├── nephro_agent.py      # Streamlit web application
├── nephro_api.py        # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your API keys (create this)
└── README.md          # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues:

1. **API Key Error**: Ensure your `.env` file contains a valid Google Gemini API key
2. **Import Errors**: Run `pip install -r requirements.txt` to install dependencies
3. **Port Conflicts**: Change ports in the code if 8501 or 8002 are in use

### Getting Help:
- Check the API documentation at `/docs` endpoint
- Review error messages in the terminal
- Ensure all dependencies are installed

## License

This project is for educational and research purposes. Please ensure compliance with Google's API terms of service and applicable medical regulations in your jurisdiction.