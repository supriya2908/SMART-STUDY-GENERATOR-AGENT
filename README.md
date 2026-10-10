# 🎓 Smart Study Generator Agent

An AI-powered web application that helps students organise study materials, understand difficult concepts, and prepare effectively for examinations — powered by **IBM Granite LLM** via **IBM watsonx.ai**.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Student Profile** | Collects name, age, department, year, subjects, exam date, learning style & study hours |
| **Material Upload** | Supports PDF, DOCX, and TXT files; also accepts pasted lecture notes |
| **Personalised Study Plan** | Day-by-day, topic-wise schedule tailored to remaining time & learning style |
| **Concise Notes** | Exam-ready bullet-point notes generated from uploaded material |
| **Chapter Summaries** | 200–300 word summaries with key takeaways |
| **Important Questions** | Short and long-answer exam questions from uploaded material |
| **MCQ Quiz** | Interactive scored quiz with instant feedback and retry |
| **Flashcards** | Reveal/hide flashcard interface for active recall practice |
| **Concept Explainer** | Difficult topics explained simply with analogies |
| **AI Chatbot** | Conversational tutor that answers academic questions |
| **Progress Tracker** | Visual donut chart, topic status table, quiz score bar chart |
| **AI Recommendations** | Personalised advice based on weak topics and remaining time |

---

## 🏗️ Architecture

```
app.py                  ← Streamlit entry point + sidebar navigation
granite_client.py       ← IBM Granite LLM prompt templates & API calls
document_processor.py  ← PDF/DOCX/TXT extraction & chunking
session_state.py        ← Session state management helpers
pages/
  page_profile.py       ← Student profile form
  page_materials.py     ← File upload & manual text entry
  page_study_plan.py    ← Study plan & revision schedule
  page_notes.py         ← Concise notes & summaries
  page_quiz.py          ← MCQ quiz, important questions & flashcards
  page_concepts.py      ← Concept explainer
  page_chatbot.py       ← Interactive AI chatbot
  page_progress.py      ← Progress tracking & recommendations
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone <repo-url>
cd smart-study-agent
pip install -r requirements.txt
```

### 2. Configure IBM watsonx.ai credentials

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

> **Get credentials:** IBM Cloud → watsonx.ai → Manage → API key + Project ID

### 3. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 IBM Granite Model

This application uses **`ibm/granite-13b-instruct-v2`** via the `ibm-watsonx-ai` Python SDK.

The model is invoked for:
- Study plan generation
- Note & summary creation
- Quiz and flashcard generation
- Concept explanation
- Conversational Q&A
- Progress recommendations

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `ibm-watsonx-ai` | IBM Granite LLM API |
| `pdfplumber` / `PyPDF2` | PDF text extraction |
| `python-docx` | DOCX text extraction |
| `plotly` | Progress charts |
| `pandas` | Data display |
| `python-dotenv` | Environment variable management |

---

## 🎓 Agentic Workflow

```
Student Input (Profile + Materials)
        ↓
  Material Analysis (document_processor)
        ↓
  IBM Granite LLM (granite_client)
    ├─ Study Plan Generation
    ├─ Notes & Summaries
    ├─ Important Questions
    ├─ MCQ Quiz Generation
    ├─ Flashcard Generation
    ├─ Concept Explanation
    ├─ Chatbot Q&A
    └─ Progress Recommendations
        ↓
  Progress Tracking & Adaptation
```

---

## 📝 Notes

- Credentials are **never** hardcoded — always use `.env`
- The app gracefully shows `[LLM Error]` messages if watsonx.ai is unreachable
- All generated content can be downloaded as `.txt` files
