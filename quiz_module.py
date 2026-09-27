import os
import re
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def clean_json_block(text: str) -> str:
    """Removes Markdown ```json code fences and strips extra whitespace."""
    cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)```", r"\1", text, flags=re.DOTALL).strip()
    return cleaned


def generate_quiz(text: str) -> list:
    """
    Generates 3 multiple-choice questions from given passage/topic with 4 options each
    and the correct answer matching one of the options.
    Returns a Python list of dictionaries.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return [{"error": "GEMINI_API_KEY not configured in .env file."}]
    genai.configure(api_key=api_key)

    prompt = f"""
You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
    try:
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(prompt)
        except Exception:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            response = model.generate_content(prompt)

        quiz_text = response.text.strip()
        cleaned_text = clean_json_block(quiz_text)
        
        # In case the model returns any text before/after the JSON array
        start_idx = cleaned_text.find('[')
        end_idx = cleaned_text.rfind(']')
        if start_idx != -1 and end_idx != -1:
            cleaned_text = cleaned_text[start_idx:end_idx + 1]

        parsed = json.loads(cleaned_text)
        return parsed
    except Exception as e:
        return [{"error": f"Error generating quiz: {e}"}]
