import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Optional
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Load env from nearest .env (searches parent dirs too)
load_dotenv(find_dotenv())

# Configure Gemini via env var
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ----- Pydantic models matching the frontend -----
class Message(BaseModel):
    role: Literal['user', 'assistant', 'system']
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str
    is_question: bool
    symptom: Optional[str] = None
    options: Optional[List[str]] = None

# Fitness assistant shares the same request/response models

class HealthCheckResponse(BaseModel):
    status: Literal['healthy', 'unhealthy']
    model_loaded: bool

# ----- FastAPI app -----
app = FastAPI(title="Healtho API", version="0.2.0")

# CORS: allow local dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model status flag
MODEL_LOADED = bool(GEMINI_API_KEY)

@app.get("/api/health", response_model=HealthCheckResponse)
def health() -> HealthCheckResponse:
    return HealthCheckResponse(status="healthy", model_loaded=MODEL_LOADED)

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    # Prefer Gemini if configured; otherwise fall back to simple rules
    last_user = next((m for m in reversed(req.messages) if m.role == 'user'), None)
    user_text = (last_user.content if last_user else '').strip()

    if GEMINI_API_KEY:
        # Build a concise system prompt to keep answers aligned
        system_prompt = (
            "You are Healtho, a helpful health assistant."
            " Keep responses concise, friendly, and not diagnostic."
            " Prefer asking one yes/no follow-up when appropriate."
            " If user asks for a health tip, provide 1 practical tip."
        )
        # Create the model and generate
        model = genai.GenerativeModel(GEMINI_MODEL)
        messages_text = "\n".join([f"{m.role.upper()}: {m.content}" for m in req.messages])
        prompt = f"{system_prompt}\n\nConversation so far:\n{messages_text}\n\nAssistant:"
        try:
            result = model.generate_content(prompt)
            text = (result.text or "I'm here to help.").strip()
            # Very light heuristic to attach quick replies
            options: Optional[List[str]] = None
            is_question = text.endswith("?")
            if is_question:
                options = ["Yes", "No"]
            elif any(k in user_text.lower() for k in ["tip", "advice", "suggestion", "healthy"]):
                options = ["Get another tip", "Learn more"]
            return ChatResponse(response=text, is_question=is_question, options=options)
        except Exception:
            # Fall back to rule-based on failure
            pass

    # Fallback simple rules
    text_lower = user_text.lower()
    if any(k in text_lower for k in ["health tip", "advice", "suggestion", "healthy"]):
        return ChatResponse(
            response=(
                "💡 Stay Hydrated: Drink at least 8 glasses of water daily.\n\n"
                "Proper hydration supports digestion, temperature regulation, and joint health."
            ),
            is_question=False,
            options=["Get another tip", "Learn more about hydration"],
        )
    if any(k in text_lower for k in ["symptom", "feel", "pain", "fever", "cough", "nausea"]):
        return ChatResponse(
            response="Do you currently have a fever?",
            is_question=True,
            symptom="fever",
            options=["Yes", "No"],
        )
    if text_lower in ("yes", "no"):
        if text_lower == "yes":
            return ChatResponse(
                response="Thanks. Do you also have a persistent cough?",
                is_question=True,
                symptom="cough",
                options=["Yes", "No"],
            )
        else:
            return ChatResponse(
                response="Understood. Are you experiencing fatigue?",
                is_question=True,
                symptom="fatigue",
                options=["Yes", "No"],
            )
    return ChatResponse(
        response=(
            "I'm Healtho. I can help with basic symptom triage. "
            "You can tell me your symptoms or ask for a health tip."
        ),
        is_question=False,
        options=["Check symptoms", "Get a health tip"],
    )

@app.post("/api/fitness/chat", response_model=ChatResponse)
def fitness_chat(req: ChatRequest) -> ChatResponse:
    """Fitness-focused assistant: diet/workout guidance only."""
    last_user = next((m for m in reversed(req.messages) if m.role == 'user'), None)
    user_text = (last_user.content if last_user else '').strip()

    if GEMINI_API_KEY:
        system_prompt = (
            "You are Vedanta Fitness Assistant. Provide concise, actionable "
            "guidance about fitness and diet only. Avoid medical diagnoses. "
            "Prefer clear bullet points and include a brief follow-up question when helpful."
        )
        model = genai.GenerativeModel(GEMINI_MODEL)
        messages_text = "\n".join([f"{m.role.upper()}: {m.content}" for m in req.messages])
        prompt = f"{system_prompt}\n\nConversation so far:\n{messages_text}\n\nAssistant:"
        try:
            result = model.generate_content(prompt)
            text = (result.text or "How can I help with your fitness today?").strip()
            options: Optional[List[str]] = None
            is_question = text.endswith("?")
            if is_question:
                options = ["Yes", "No"]
            elif any(k in user_text.lower() for k in ["plan", "diet", "workout", "routine", "meal", "exercise"]):
                options = ["Suggest a workout", "Suggest a diet plan"]
            return ChatResponse(response=text, is_question=is_question, options=options)
        except Exception:
            pass

    # Simple fallback rules
    tl = user_text.lower()
    if any(k in tl for k in ["diet", "meal", "nutrition", "protein", "calorie"]):
        return ChatResponse(
            response=(
                "Diet tip: Prioritize protein (1.2–1.6 g/kg), include vegetables in each meal, "
                "and keep a modest calorie deficit (300–500 kcal) for fat loss."
            ),
            is_question=False,
            options=["Suggest a diet plan", "Protein sources"],
        )
    if any(k in tl for k in ["workout", "exercise", "gym", "training", "cardio", "strength"]):
        return ChatResponse(
            response=(
                "Workout tip: 3x/week full-body strength (squat, hinge, push, pull) + 2x/week cardio. "
                "Start light and progress gradually."
            ),
            is_question=False,
            options=["Suggest a workout", "Beginner routine"],
        )
    return ChatResponse(
        response=(
            "I'm your fitness assistant. Ask me about workouts, routines, or diet planning."
        ),
        is_question=False,
        options=["Suggest a workout", "Suggest a diet plan"],
    )

# To run locally:
#   uvicorn app:app --host 0.0.0.0 --port 3001 --reload