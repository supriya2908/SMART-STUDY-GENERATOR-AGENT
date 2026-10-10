"""
Session-state helpers for the Smart Study Generator Agent.
Manages student profile, uploaded materials, generated content, and chat history.
"""

import streamlit as st
from datetime import date


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def init_session():
    """Initialise all session state keys with defaults (idempotent)."""
    defaults = {
        # Student profile
        "profile": {},
        "profile_saved": False,

        # Uploaded / entered study materials
        "materials": [],          # list of {"name": str, "text": str, "topic": str}
        "topics": [],             # list of topic strings

        # Generated content cache  {topic: {type: content}}
        "study_plan": "",
        "notes": {},
        "summaries": {},
        "important_questions": {},
        "quizzes": {},
        "flashcards": {},
        "revision_schedule": "",

        # Progress tracking
        "completed_topics": [],   # topics marked done
        "quiz_scores": {},        # {topic: [scores]}

        # Chatbot
        "chat_history": [],       # [{"role": "user"|"assistant", "content": str}]

        # UI state
        "active_tab": "Profile",
        "generation_in_progress": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Profile helpers
# ---------------------------------------------------------------------------

def save_profile(data: dict):
    st.session_state["profile"] = data
    st.session_state["profile_saved"] = True


def get_profile() -> dict:
    return st.session_state.get("profile", {})


def days_until_exam() -> int:
    exam = st.session_state.get("profile", {}).get("exam_date")
    if exam and isinstance(exam, date):
        delta = (exam - date.today()).days
        return max(delta, 1)
    return 14


# ---------------------------------------------------------------------------
# Material helpers
# ---------------------------------------------------------------------------

def add_material(name: str, text: str, topic: str):
    st.session_state["materials"].append({"name": name, "text": text, "topic": topic})
    if topic and topic not in st.session_state["topics"]:
        st.session_state["topics"].append(topic)


def get_all_text() -> str:
    return "\n\n".join(m["text"] for m in st.session_state["materials"])


def get_text_for_topic(topic: str) -> str:
    texts = [m["text"] for m in st.session_state["materials"] if m["topic"] == topic]
    return "\n\n".join(texts) if texts else get_all_text()


# ---------------------------------------------------------------------------
# Progress helpers
# ---------------------------------------------------------------------------

def mark_topic_done(topic: str):
    if topic not in st.session_state["completed_topics"]:
        st.session_state["completed_topics"].append(topic)


def record_quiz_score(topic: str, score: int, total: int):
    scores = st.session_state["quiz_scores"].setdefault(topic, [])
    scores.append({"score": score, "total": total})


def progress_pct() -> float:
    topics = st.session_state.get("topics", [])
    done = st.session_state.get("completed_topics", [])
    if not topics:
        return 0.0
    return round(len(done) / len(topics) * 100, 1)
