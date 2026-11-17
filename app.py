import streamlit as st
from config import DATA_DIR
from ingestion.loader import load_pdf
from ingestion.chunker import chunk_pages
from retrieval.vector_store import add_chunks, list_sources
from features.qa import answer_question
from features.summarizer import summarize_subject
from features.quiz import generate_quiz

st.set_page_config(page_title="Exam Buddy", page_icon="📚", layout="wide")

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(1200px 600px at 10% -10%, #1e1b4b 0%, #0b0f19 45%, #05070d 100%);
    color: #e5e7eb;
}
#MainMenu, footer { visibility: hidden; }

.hero {
    padding: 2rem 2.2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(99,102,241,.35), rgba(168,85,247,.25) 50%, rgba(236,72,153,.2));
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 20px 60px rgba(0,0,0,.35);
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 2.6rem; font-weight: 800; margin: 0;
    background: linear-gradient(90deg, #c4b5fd, #f0abfc, #fda4af);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #cbd5e1; margin: .5rem 0 0; font-size: 1.05rem; }

.pill {
    display: inline-block; padding: .3rem .8rem; border-radius: 999px; margin: .6rem .4rem 0 0;
    background: rgba(99,102,241,.18); color: #c7d2fe; font-size: .78rem; font-weight: 600;
    border: 1px solid rgba(129,140,248,.35);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: rgba(255,255,255,.04); padding: 6px; border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; padding: .5rem 1.1rem; color: #94a3b8; font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #6366f1, #a855f7) !important; color: white !important;
}

.stButton > button {
    border-radius: 12px; border: none; padding: .6rem 1.3rem; font-weight: 700; color: white;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    box-shadow: 0 8px 24px rgba(168,85,247,.35);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 12px 30px rgba(168,85,247,.5); color: white;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
    padding: .4rem .6rem;
}

[data-testid="stSidebar"] { background: #0a0d16; border-right: 1px solid rgba(255,255,255,.06); }
.stTextInput input { border-radius: 12px !important; }
[data-testid="stFileUploader"] section {
    border-radius: 16px; border: 1.5px dashed rgba(129,140,248,.5); background: rgba(99,102,241,.06);
}
.answer-text { border-left: 3px solid #a855f7; padding-left: 1rem; line-height: 1.7; }
.source-pill {
    display: inline-block; padding: .2rem .6rem; border-radius: 8px; font-size: .75rem;
    background: rgba(168,85,247,.2); color: #e9d5ff; margin-right: .3rem;
}
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <h1>📚 Exam Buddy</h1>
        <p>Learn from your notes, understand concepts, and prepare for exams in one place.</p>
        <span class="pill">AI Q&amp;A</span><span class="pill">Smart Summaries</span><span class="pill">Practice Quizzes</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar: subject and file choice ----------
subject = st.sidebar.text_input("📘 Subject name", value="Test")
st.sidebar.caption("Each subject has its own set of notes.")

sources = list_sources(subject)
file_choice = st.sidebar.selectbox("📄 File", ["All files"] + sources)
source = None if file_choice == "All files" else file_choice
st.sidebar.caption("Summary, quiz and Q&A will be generated only from the selected file.")

tab_upload, tab_ask, tab_summary, tab_quiz = st.tabs(
    ["📤 Upload", "💬 Ask", "📝 Summary", "🧠 Quiz"]
)

# ---------- 1. Upload ----------
with tab_upload:
    with st.container(border=True):
        st.subheader("Upload study material")
        st.caption("Upload PDF notes.")
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
with tab_ask:
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.container(border=True):
        st.subheader("Ask from your notes")
        question = st.text_input("Your question", placeholder="e.g. Why is overlap useful?")
        is_follow_up = st.checkbox("This is a follow-up to the previous question")
        if st.button("Ask", use_container_width=True) and question:
            last = st.session_state.history[-1]["question"] if st.session_state.history else None
            full_question = (
                f"Previous question: {last}\nFollow-up: {question}"
                if is_follow_up and last else question
            )
            with st.spinner("Searching for answers..."):
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
with tab_summary:
    with st.container(border=True):
        st.subheader("Revision notes")
        st.caption(f"Source: {file_choice}")
        if st.button("Generate summary", use_container_width=True):
            with st.spinner("Summarizing notes..."):
                st.session_state.summaries = summarize_subject(subject, source=source)

    for part in st.session_state.get("summaries", []):
        with st.container(border=True):
            st.subheader(f"📖 Pages {part['pages'][0]} to {part['pages'][-1]}")
            st.markdown(part["summary"])

# ---------- 4. Quiz ----------
with tab_quiz:
    with st.container(border=True):
        st.subheader("Practice quiz")
        st.caption(f"Source: {file_choice}")
        col1, col2 = st.columns(2)
        n = col1.slider("Number of questions", 1, 10, 5)
        difficulty = col2.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)

        if st.button("Generate quiz", use_container_width=True):
            with st.spinner("Generating quiz..."):
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