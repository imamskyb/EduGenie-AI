import os
import logging
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from dotenv import load_dotenv

load_dotenv()

# Logger setup
logger = logging.getLogger("EduGenie.Explanation")

# Model variables for local explanation
explain_tokenizer = None
explain_model = None
_model_load_attempted = False


def _init_local_model():
    """Lazily load MBZUAI/LaMini-Flan-T5-783M if transformers and torch are installed."""
    global explain_tokenizer, explain_model, _model_load_attempted
    if _model_load_attempted:
        return
    _model_load_attempted = True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch

        logger.info("Loading MBZUAI/LaMini-Flan-T5-783M model...")
        explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        logger.info("MBZUAI/LaMini-Flan-T5-783M loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load local model MBZUAI/LaMini-Flan-T5-783M: {e}. Falling back to Gemini.")


def explain_topic(topic: str) -> str:
    """
    Explains a concept in a simple and clear way for a school student.
    Uses MBZUAI/LaMini-Flan-T5-783M locally when available, or Gemini as reliable fallback.
    """
    _init_local_model()

    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."

    if explain_tokenizer is not None and explain_model is not None:
        try:
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True,
            )
            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            logger.error(f"Local model generation failed: {e}")

    # Fallback to Gemini if local model is unavailable or failed
    try:
        import google.generativeai as genai
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ Error in Explanation: GEMINI_API_KEY not configured. Please add GEMINI_API_KEY in .env file."
        genai.configure(api_key=api_key)
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(input_text)
            return response.text.strip()
        except Exception:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            response = model.generate_content(input_text)
            return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Explanation: {e}"
