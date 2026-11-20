import streamlit as st

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(1200px 600px at 10% -10%, #1e1b4b 0%, #0b0f19 45%, #05070d 100%);
    color: #e5e7eb;
}
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1150px; padding-top: 2rem; }

.badge {
    display: inline-block; padding: .4rem 1rem; border-radius: 999px; font-size: .8rem; font-weight: 700;
    background: rgba(99,102,241,.15); border: 1px solid rgba(129,140,248,.4); color: #c7d2fe;
}
.grad {
    background: linear-gradient(90deg, #a5b4fc, #f0abfc 50%, #fda4af);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.glass {
    background: linear-gradient(160deg, rgba(255,255,255,.07), rgba(255,255,255,.02));
    border: 1px solid rgba(255,255,255,.08); border-radius: 20px;
    box-shadow: 0 16px 40px rgba(0,0,0,.3);
}

/* Landing page */
.hero { text-align: center; padding: 3.5rem 1rem 1rem; }
.hero h1 { font-size: clamp(2.4rem, 6vw, 4.2rem); font-weight: 900; line-height: 1.1; letter-spacing: -1px; margin: 1.2rem 0; }
.hero .sub { color: #94a3b8; font-size: 1.15rem; max-width: 640px; margin: 0 auto; line-height: 1.7; }
.stats { display: flex; justify-content: center; gap: 3rem; margin-top: 2.5rem; flex-wrap: wrap; }
.stat b { display: block; font-size: 1.6rem; color: #e0e7ff; }
.stat span { color: #64748b; font-size: .85rem; }
.section-title { text-align: center; margin: 4.5rem 0 2rem; }
.eyebrow { color: #a5b4fc; font-weight: 700; font-size: .8rem; letter-spacing: 2px; text-transform: uppercase; }
.section-title h2 { font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 800; margin-top: .5rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 1.2rem; }
.card { padding: 1.7rem; transition: transform .25s ease, border-color .25s ease; }
.card:hover { transform: translateY(-6px); border-color: rgba(168,85,247,.5); }
.icon {
    width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; background: linear-gradient(135deg, rgba(99,102,241,.3), rgba(236,72,153,.25)); margin-bottom: 1rem;
}
.card h3 { font-size: 1.15rem; font-weight: 700; margin-bottom: .5rem; }
.card p { color: #94a3b8; line-height: 1.6; font-size: .95rem; margin: 0; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.2rem; }
.step { padding: 1.5rem; }
.num {
    width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 800; background: linear-gradient(135deg,#6366f1,#ec4899); margin-bottom: .9rem;
}
.step h4 { font-size: 1.05rem; font-weight: 700; margin-bottom: .4rem; }
.step p { color: #94a3b8; font-size: .92rem; line-height: 1.55; margin: 0; }
.cta {
    text-align: center; padding: 3.5rem 2rem; margin-top: 4rem; border-radius: 28px;
    background: linear-gradient(135deg, rgba(99,102,241,.3), rgba(168,85,247,.2), rgba(236,72,153,.2));
    border: 1px solid rgba(255,255,255,.1);
}
.cta h2 { font-size: 2rem; font-weight: 800; margin: 0; }
.cta p { color: #cbd5e1; margin: .6rem 0 0; }
.footer { text-align: center; color: #475569; font-size: .85rem; padding: 2.5rem 0 1rem; }

/* App page */
.app-hero {
    padding: 1.8rem 2rem; border-radius: 20px; margin-bottom: 1.5rem;
    background: linear-gradient(135deg, rgba(99,102,241,.35), rgba(168,85,247,.25) 50%, rgba(236,72,153,.2));
    border: 1px solid rgba(255,255,255,.08); box-shadow: 0 20px 60px rgba(0,0,0,.35);
}
.app-hero h1 { font-size: 2.2rem; font-weight: 800; margin: 0; }
.app-hero p { color: #cbd5e1; margin: .4rem 0 0; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: rgba(255,255,255,.04); padding: 6px; border-radius: 14px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: .5rem 1.1rem; color: #94a3b8; font-weight: 600; }
.stTabs [aria-selected="true"] { background: linear-gradient(90deg,#6366f1,#a855f7) !important; color: white !important; }
.stButton > button {
    border-radius: 12px; border: none; padding: .6rem 1.3rem; font-weight: 700; color: white;
    background: linear-gradient(90deg,#6366f1,#a855f7,#ec4899); box-shadow: 0 8px 24px rgba(168,85,247,.35);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(168,85,247,.5); color: white; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.04); border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,.25);
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


def render_landing(on_start):
    st.markdown(
        """
        <div class="hero">
            <span class="badge">✨ AI-powered study assistant</span>
            <h1>Prepare smarter with <span class="grad">your own notes</span></h1>
            <p class="sub">Upload your PDF notes, ask questions, get short summaries and practice quizzes. Every answer comes from your own material, with page numbers shown.</p>
            <div class="stats">
                <div class="stat"><b>4</b><span>study tools in one place</span></div>
                <div class="stat"><b>Notes only</b><span>answers grounded in your files</span></div>
                <div class="stat"><b>Page-wise</b><span>source references</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1.2, 1, 1.2])
    with mid:
        st.button("🚀 Get Started", on_click=on_start, use_container_width=True, key="landing_start")

    st.markdown(
        """
        <div class="section-title">
            <div class="eyebrow">Features</div>
            <h2>Everything you need to revise</h2>
        </div>
        <div class="grid">
            <div class="glass card"><div class="icon">📤</div><h3>Upload notes</h3><p>Save PDF notes by subject. Each subject's data is stored separately.</p></div>
            <div class="glass card"><div class="icon">💬</div><h3>Ask questions</h3><p>Get simple explanations, ask follow-ups, and see the source page for every answer.</p></div>
            <div class="glass card"><div class="icon">📝</div><h3>Smart summaries</h3><p>Get short summaries and important points for any file, section by section.</p></div>
            <div class="glass card"><div class="icon">🧠</div><h3>Practice quizzes</h3><p>Pick the number of questions and difficulty, then check your score.</p></div>
        </div>
        <div class="section-title">
            <div class="eyebrow">How it works</div>
            <h2>4 simple steps</h2>
        </div>
        <div class="steps">
            <div class="glass step"><div class="num">1</div><h4>Add your notes</h4><p>Enter a subject name and upload your PDF files.</p></div>
            <div class="glass step"><div class="num">2</div><h4>Ask questions</h4><p>Type any question and get an answer with source pages.</p></div>
            <div class="glass step"><div class="num">3</div><h4>Get a summary</h4><p>Pick a file and generate revision notes in seconds.</p></div>
            <div class="glass step"><div class="num">4</div><h4>Take a quiz</h4><p>Choose the count and difficulty, then test yourself.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cta">
            <h2>Start your exam preparation now</h2>
            <p>Upload your notes and start practicing right away.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, mid2, _ = st.columns([1.2, 1, 1.2])
    with mid2:
        st.button("🚀 Open Exam Buddy", on_click=on_start, use_container_width=True, key="landing_cta")

    st.markdown('<div class="footer">© 2026 Exam Buddy · Built with Python, Streamlit, ChromaDB and Gemini</div>', unsafe_allow_html=True)