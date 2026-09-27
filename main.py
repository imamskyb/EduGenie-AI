import os
import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(
    title="EduGenie: Google Gemini Powered Learning Assistant",
    description="A lightweight AI-powered educational assistant for students of all academic levels.",
    version="1.0.0",
)

# Mount static directory for CSS styling
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template setup
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main EduGenie educational assistant web interface."""
    return templates.TemplateResponse(request=request, name="index.html")


# Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    """Handles questions and returns smart, concise answers."""
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    """Handles complex concepts and returns simplified explanations."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)
    
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    """Handles large educational passages and returns concise summaries."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)

    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    """Generates 3 MCQs with 4 options each from a passage or topic."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)

    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    print("Generated quiz:", quiz)  # DEBUG
    return JSONResponse(content={"quiz": quiz})


# Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    """Generates a structured, adaptive learning path with beginner to advanced concepts and resources."""
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
