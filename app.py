"""
Smart Study Generator Agent
Main Streamlit application entry point.
Run: streamlit run app.py
"""

import streamlit as st

# Page config must be the very first Streamlit call
st.set_page_config(
    page_title="Smart Study Generator Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

import session_state as ss

# Initialise session on every run
ss.init_session()

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Sidebar nav */
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        padding: 0.5rem 0.75rem;
        font-size: 0.95rem;
        border-radius: 6px;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: #f0f4ff;
    }
    /* Main content padding */
    .block-container { padding-top: 1.5rem; }
    /* Metric cards */
    [data-testid="metric-container"] {
        background: #f7f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.75rem 1rem;
    }
    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
        width=80,
    )
    st.markdown("## 🎓 Smart Study Generator")
    st.markdown("*Powered by IBM Granite LLM*")
    st.markdown("---")

    # Navigation
    NAV_ITEMS = [
        ("👤 Profile",          "Profile"),
        ("📚 Materials",         "Materials"),
        ("📅 Study Plan",        "Study Plan"),
        ("📝 Notes & Summaries", "Notes"),
        ("🧠 Quiz & Flashcards", "Quiz"),
        ("💡 Concept Explainer", "Concepts"),
        ("🤖 AI Chatbot",        "Chatbot"),
        ("📊 Progress",          "Progress"),
    ]

    for label, key in NAV_ITEMS:
        active = st.session_state.get("active_tab") == key
        btn_style = "primary" if active else "secondary"
        if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_style):
            st.session_state["active_tab"] = key
            st.rerun()

    st.markdown("---")

    # Quick stats in sidebar
    profile = ss.get_profile()
    if profile:
        st.markdown(f"**👤 {profile.get('name', '—')}**")
        st.markdown(f"📅 {profile.get('days_until_exam', '?')} days to exam")
        pct = ss.progress_pct()
        st.progress(pct / 100)
        st.caption(f"Progress: {pct}%")
        st.markdown(f"📂 {len(st.session_state.get('materials', []))} materials loaded")
        st.markdown(f"🏷️ {len(st.session_state.get('topics', []))} topics")
    else:
        st.info("Complete your profile to get started.")

    st.markdown("---")
    st.caption("IBM Granite 13B Instruct v2  \nvia watsonx.ai")


# ── Page Routing ─────────────────────────────────────────────────────────────
active = st.session_state.get("active_tab", "Profile")

if active == "Profile":
    from pages import page_profile
    page_profile.render()

elif active == "Materials":
    from pages import page_materials
    page_materials.render()

elif active == "Study Plan":
    from pages import page_study_plan
    page_study_plan.render()

elif active == "Notes":
    from pages import page_notes
    page_notes.render()

elif active == "Quiz":
    from pages import page_quiz
    page_quiz.render()

elif active == "Concepts":
    from pages import page_concepts
    page_concepts.render()

elif active == "Chatbot":
    from pages import page_chatbot
    page_chatbot.render()

elif active == "Progress":
    from pages import page_progress
    page_progress.render()
