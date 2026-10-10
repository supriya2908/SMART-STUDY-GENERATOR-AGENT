"""
IBM Granite LLM client via watsonx.ai
Handles all LLM calls with structured prompt templates.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Lazy import so the app can run without credentials for UI preview
# ---------------------------------------------------------------------------
_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    try:
        from ibm_watsonx_ai import APIClient, Credentials
        credentials = Credentials(
            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            api_key=os.getenv("WATSONX_API_KEY", ""),
        )
        _client = APIClient(credentials)
    except Exception as e:
        raise RuntimeError(f"Failed to initialise watsonx.ai client: {e}")
    return _client


def _generate(prompt: str, max_tokens: int = 1500, temperature: float = 0.7) -> str:
    """Core generation call to IBM Granite via watsonx.ai."""
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as Params

        model = ModelInference(
            model_id="ibm/granite-13b-instruct-v2",
            api_client=_get_client(),
            project_id=os.getenv("WATSONX_PROJECT_ID", ""),
            params={
                Params.MAX_NEW_TOKENS: max_tokens,
                Params.TEMPERATURE: temperature,
                Params.REPETITION_PENALTY: 1.1,
                Params.STOP_SEQUENCES: ["<|endoftext|>"],
            },
        )
        response = model.generate_text(prompt=prompt)
        return response.strip()
    except Exception as e:
        return f"[LLM Error] {e}"


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def generate_study_plan(profile: dict, topics: list[str], material_summary: str) -> str:
    days = profile.get("days_until_exam", 14)
    hours = profile.get("study_hours_per_day", 3)
    style = profile.get("learning_style", "visual")
    prompt = f"""You are an expert academic tutor. Create a detailed, day-by-day study plan.

Student profile:
- Name: {profile.get('name')}
- Department: {profile.get('department')}
- Year: {profile.get('year')}
- Subjects / Topics: {', '.join(topics)}
- Days until exam: {days}
- Study hours per day: {hours}
- Learning style: {style}

Study material overview:
{material_summary[:800]}

Generate a structured day-by-day study plan with specific goals per session,
revision slots, and practice days. Format as a clear numbered schedule."""
    return _generate(prompt, max_tokens=1800)


def generate_concise_notes(topic: str, content: str) -> str:
    prompt = f"""You are an expert academic note-maker. Create concise, exam-ready notes.

Topic: {topic}

Source material:
{content[:2000]}

Generate:
1. Key definitions (bullet points)
2. Core concepts and principles
3. Important formulas or rules (if any)
4. Common exam pitfalls
Keep the language clear and simple."""
    return _generate(prompt, max_tokens=1500)


def generate_summary(topic: str, content: str) -> str:
    prompt = f"""Summarize the following study material on "{topic}" in 200–300 words.
Use clear, student-friendly language. Highlight the 3–5 most important takeaways.

Material:
{content[:2500]}"""
    return _generate(prompt, max_tokens=600)


def generate_important_questions(topic: str, content: str) -> str:
    prompt = f"""You are an experienced examiner. Based on the material below, generate
10 important exam questions on "{topic}" — include short-answer and long-answer types.
Number each question.

Material:
{content[:2000]}"""
    return _generate(prompt, max_tokens=1000)


def generate_mcq_quiz(topic: str, content: str, num_questions: int = 5) -> str:
    prompt = f"""Create a {num_questions}-question multiple-choice quiz on "{topic}".

For each question provide:
Q<n>. <question>
A) ...  B) ...  C) ...  D) ...
Answer: <letter>
Explanation: <one sentence>

Base questions on this material:
{content[:2000]}"""
    return _generate(prompt, max_tokens=1400)


def generate_flashcards(topic: str, content: str, num_cards: int = 8) -> str:
    prompt = f"""Create {num_cards} flashcards for the topic "{topic}".
Format each card as:
CARD <n>
Front: <term or question>
Back: <definition or answer>

Use the material below:
{content[:2000]}"""
    return _generate(prompt, max_tokens=1000)


def explain_concept(concept: str, context: str = "") -> str:
    ctx = f"\nAdditional context:\n{context[:800]}" if context else ""
    prompt = f"""Explain "{concept}" in simple, student-friendly language.{ctx}

Include:
- A plain-language definition
- A real-world analogy
- Why it matters in academics
- One example"""
    return _generate(prompt, max_tokens=700)


def answer_query(question: str, profile: dict, history: list[dict]) -> str:
    recent = "\n".join(
        f"{'Student' if m['role'] == 'user' else 'Tutor'}: {m['content']}"
        for m in history[-6:]
    )
    prompt = f"""You are a helpful AI academic tutor for {profile.get('name', 'the student')}
studying {profile.get('department', 'their subject')}.

Conversation so far:
{recent}

Student question: {question}

Answer clearly and concisely. If the question is subject-specific, give a textbook-accurate answer."""
    return _generate(prompt, max_tokens=800, temperature=0.6)


def generate_revision_schedule(topics: list[str], days: int, hours_per_day: float) -> str:
    prompt = f"""Create a topic-wise revision schedule.

Topics: {', '.join(topics)}
Available days: {days}
Hours per day: {hours_per_day}

Distribute topics proportionally. Include daily goals, revision sessions, and
a final 2-day full-revision block. Output as a table with columns: Day | Topic | Goals | Duration."""
    return _generate(prompt, max_tokens=1200)
