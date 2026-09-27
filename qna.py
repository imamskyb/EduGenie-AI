import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def answer_question_with_gemini(question: str) -> str:
    """Answers general knowledge and academic questions using Google Gemini."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Error in QnA: GEMINI_API_KEY not configured. Please add GEMINI_API_KEY in .env file."
    genai.configure(api_key=api_key)
    
    for model_name in ["gemini-flash-latest", "gemini-pro-latest", "models/gemini-1.5-pro", "models/gemini-1.5-flash"]:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(question)
            return response.text.strip()
        except Exception:
            continue
    return "⚠️ Error in QnA: Failed to generate response with available Gemini models."
