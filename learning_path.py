import os
import traceback
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def get_learning_recommendations(topic: str) -> str:
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ Error: GEMINI_API_KEY not configured in .env file."
    genai.configure(api_key=api_key)

    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, websites, videos).
Include beginner, intermediate, and advanced levels if needed.
"""
    try:
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(prompt)
        except Exception:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            response = model.generate_content(prompt)

        print("Gemini raw response:", response)

        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "❌ Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()  # This gives full error trace
        return f"❌ Error occurred: {str(e)}"
