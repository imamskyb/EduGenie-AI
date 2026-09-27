# EduGenie: Google Gemini Powered Learning Assistant 🎓✨

EduGenie is a lightweight AI-powered educational assistant designed to simplify learning through generative AI. Designed for students of all academic levels, EduGenie integrates cloud-based intelligence (Google Gemini) with an intuitive web interface built on FastAPI.

---

## 🌟 Key Features

1. **Ask EduGenie a Question (Q&A Module - `/qa`)**
   - General knowledge and academic question answering powered by Google Gemini.
   - Scenario: *"Which is the largest ocean?"* ➔ Instant, accurate answer.

2. **Need an Explanation? (Concept Explanation Module - `/explain`)**
   - Breaks down complex topics into clear, intuitive explanations suitable for school students.
   - Built to run local models (`MBZUAI/LaMini-Flan-T5-783M`) or Gemini with intelligent fallback.
   - Scenario: Explains *"Photosynthesis"* or *"Quantum computing"* simply.

3. **Summarize a Paragraph (Summarization Module - `/summarize`)**
   - Condenses lengthy educational passages, articles, and textbook chapters into concise, key-point summaries for rapid revision.
   - Scenario: Summarizes *"The Industrial Revolution"* into core takeaways.

4. **Generate a Quiz (Quiz Generation Module - `/quiz`)**
   - Generates 3 multiple-choice questions (MCQs) with 4 options each from any passage or topic.
   - Includes real-time interactive answer verification (`Correct!` / `Incorrect. Correct answer: ...`).
   - Scenario: Generates a quiz on *"Pythagoras Theorem"* or *"Solar System"*.

5. **Get Learning Recommendations (Learning Path Module - `/learn/recommendations`)**
   - Creates a personalized, structured learning roadmap from beginner to advanced levels with study topics, timelines, and recommended resources (books, websites, videos).
   - Scenario: Step-by-step roadmap for *"SQL"* or *"Linear Regression"*.

---

## 📁 Project Architecture

```text
EDUGenie/
├── main.py                     # FastAPI application & route controllers
├── qna.py                      # Question answering module (Gemini)
├── explanation_module.py       # Concept explanation logic (LaMini-Flan-T5 / Gemini)
├── quiz_module.py              # Quiz generation module (Gemini)
├── summary_module.py           # Summarization module (Gemini)
├── learning_path.py            # Learning recommendation module (Gemini)
├── templates/
│   └── index.html              # HTML frontend template (Jinja2)
├── static/
│   └── style.css               # Modern, responsive CSS styling
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment configuration
├── .env                        # Local environment file (API keys)
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Google Gemini API Key ([Get one free from Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment
Clone or navigate to the project directory:
```bash
cd EDUGenie
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Open `.env` (or copy `.env.example` to `.env`) and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Run the Application
Start the Uvicorn ASGI server with hot reloading:
```bash
uvicorn main:app --reload
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 📡 REST API Endpoints

| Endpoint | Method | Params / Body | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | None | Renders the HTML frontend UI |
| `/qa` | `GET` | `?question=<str>` | Returns answer for a question |
| `/explain` | `POST` | `{"topic": "<str>"}` | Returns simple explanation for a concept |
| `/summarize` | `POST` | `{"text": "<str>"}` | Returns concise summary of text |
| `/quiz` | `POST` | `{"text": "<str>"}` | Generates 3 MCQs in JSON format |
| `/learn/recommendations` | `GET` | `?topic=<str>` | Returns structured learning roadmap |

---

## 🛠️ Technology Stack
- **Backend**: FastAPI, Uvicorn, Pydantic, Python 3.11
- **Templating**: Jinja2
- **AI Models**: Google Gemini 1.5 Pro / Flash (via `google-generativeai`), LaMini-Flan-T5
- **Frontend**: HTML5, Modern CSS3 (Responsive Grid/Flexbox), Vanilla JavaScript (Fetch API)

---

## 👥 Credits
- **Project**: EduGenie - SmartBridge / SmartInternz
- **Author**: Tella Divya Sree
- **Mentor**: Siri
