import re
import streamlit as st
from config import DATA_DIR
from ingestion.loader import load_pdf
from ingestion.chunker import chunk_pages
from retrieval.vector_store import add_chunks, list_sources
from features.qa import answer_question
from features.summarizer import summarize_subject
from features.quiz import generate_quiz
from landing import STYLE, render_landing
from auth_ui import render_auth

st.set_page_config(page_title="Exam Buddy", page_icon="📚", layout="wide")
st.markdown(STYLE, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "user" not in st.session_state:
    st.session_state.user = None


def go_app():
    st.session_state.page = "app"


def go_home():
    st.session_state.page = "landing"


def logout():
    for key in ["user", "history", "summaries", "quiz"]:
        st.session_state.pop(key, None)
    st.session_state.page = "landing"


def make_key(user: str, name: str) -> str:
    """Make a safe internal name so each user's subjects stay separate."""
    key = re.sub(r"[^a-z0-9]+", "_", f"{user}_{name}".lower()).strip("_")
    return key[:60] or f"{user}_default"


# ---------- Landing page ----------
if st.session_state.page == "landing":
    render_landing(on_start=go_app)
    st.stop()

# ---------- Login / sign up ----------
if not st.session_state.user:
    st.sidebar.button("🏠 Back to home", on_click=go_home, use_container_width=True)
    render_auth()
    st.stop()

# ---------- App page (logged in) ----------
user = st.session_state.user

st.sidebar.button("🏠 Back to home", on_click=go_home, use_container_width=True)
st.sidebar.success(f"👤 Logged in as {user}")
st.sidebar.button("🚪 Logout", on_click=logout, use_container_width=True)

menu = st.sidebar.radio(
    "📌 Menu",
    ["📤 Upload", "💬 Ask", "📝 Summary", "🧠 Quiz"],
    key="nav",
)

subject_name = st.sidebar.text_input("📘 Subject name", value="Test")
subject = make_key(user, subject_name)
st.sidebar.caption("Each subject's notes are stored separately.")

sources = list_sources(subject)
file_choice = st.sidebar.selectbox("📄 File", ["All files"] + sources)
source = None if file_choice == "All files" else file_choice
st.sidebar.caption("Summary, quiz, and Q&A will use only the selected file.")

st.markdown(
    """
    <div class="app-hero">
        <h1>📚 Exam Buddy</h1>
        <p>Learn from your notes, understand concepts, and prepare for exams in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- 1. Upload ----------
if menu == "📤 Upload":
    with st.container(border=True):
        st.subheader("Upload study material")
        st.caption("Upload your PDF notes. Text-based PDFs work best.")
        files = st.file_uploader("Upload PDF notes", type=["pdf"], accept_multiple_files=True)
        if st.button("Save and index", use_container_width=True) and files:
            folder = DATA_DIR / subject
            folder.mkdir(parents=True, exist_ok=True)
            for f in files:
                path = folder / f.name
                path.write_bytes(f.getbuffer())
                pages = load_pdf(path)
                count = add_chunks(chunk_pages(pages, f.name, subject))
                st.success(f"✅ {f.name}: {len(pages)} pages, {count} chunks stored")
            st.info("Refresh the page (F5) to update the file list in the sidebar.")

# ---------- 2. Ask ----------
elif menu == "💬 Ask":
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.container(border=True):
        st.subheader("Ask from your notes")
        question = st.text_input("Type your question", placeholder="e.g. Why is overlap useful?")
        is_follow_up = st.checkbox("This is a follow-up to the previous question")
        if st.button("Ask", use_container_width=True) and question:
            last = st.session_state.history[-1]["question"] if st.session_state.history else None
            full_question = (
                f"Previous question: {last}\nFollow-up: {question}"
                if is_follow_up and last else question
            )
            with st.spinner("Searching your notes..."):
                result = answer_question(subject, full_question, source=source)
            st.session_state.history.append({
                "question": question,
                "answer": result["answer"],
                "pages": result["pages"],
            })

    for item in reversed(st.session_state.history):
        with st.container(border=True):
            st.markdown(f"**❓ {item['question']}**")
            st.markdown(f"<div class='answer-text'>{item['answer']}</div>", unsafe_allow_html=True)
            pills = "".join(f"<span class='source-pill'>Page {p}</span>" for p in item["pages"])
            st.markdown(f"📎 Sources: {pills}", unsafe_allow_html=True)

# ---------- 3. Summary ----------
elif menu == "📝 Summary":
    with st.container(border=True):
        st.subheader("Revision notes")
        st.caption(f"Source: {file_choice}")
        if st.button("Generate summary", use_container_width=True):
            with st.spinner("Creating summary..."):
                st.session_state.summaries = summarize_subject(subject, source=source)

    for part in st.session_state.get("summaries", []):
        with st.container(border=True):
            st.subheader(f"📖 Pages {part['pages'][0]} to {part['pages'][-1]}")
            st.markdown(part["summary"])

# ---------- 4. Quiz ----------
elif menu == "🧠 Quiz":
    with st.container(border=True):
        st.subheader("Practice quiz")
        st.caption(f"Source: {file_choice}")
        col1, col2 = st.columns(2)
        n = col1.slider("Number of questions", 1, 10, 5)
        difficulty = col2.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)

        if st.button("Generate quiz", use_container_width=True):
            with st.spinner("Generating questions..."):
                st.session_state.quiz = generate_quiz(subject, n=n, difficulty=difficulty, source=source)
            for key in list(st.session_state.keys()):
                if key.startswith("q") and key[1:].isdigit():
                    del st.session_state[key]

    quiz = st.session_state.get("quiz", [])
    for i, item in enumerate(quiz):
        with st.container(border=True):
            st.radio(f"{i + 1}. {item['question']}", item["options"], index=None, key=f"q{i}")

    if quiz and st.button("Check answers", use_container_width=True):
        score = sum(
            1 for i, item in enumerate(quiz)
            if st.session_state.get(f"q{i}") == item["options"][item["answer"]]
        )
        st.success(f"🎉 Score: {score} / {len(quiz)}")