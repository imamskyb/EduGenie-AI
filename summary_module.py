import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def summarize_text(text: str) -> str:
    """Summarizes text into concise, simple language using Gemini."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Error in Summary: GEMINI_API_KEY not configured in .env file."
    genai.configure(api_key=api_key)

    prompt = f"Summarize the following text in simple language:\n\n{text}"
    try:
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(prompt)
        except Exception:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"
