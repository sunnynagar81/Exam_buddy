import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import jwt
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import create_user, verify_user
from config import DATA_DIR
from ingestion.loader import load_pdf
from ingestion.chunker import chunk_pages
from retrieval.vector_store import add_chunks, list_sources
from features.qa import answer_question
from features.summarizer import summarize_subject
from features.quiz import generate_quiz
from features.study_plan import make_plan

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
TOKEN_DAYS = 7

app = FastAPI(title="Exam Buddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://exambuddy-site.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Models ----------
class AuthIn(BaseModel):
    username: str
    password: str


class AskIn(BaseModel):
    question: str
    source: str | None = None
    previous: str | None = None


class SummaryIn(BaseModel):
    source: str | None = None


class QuizIn(BaseModel):
    source: str | None = None
    n: int = 5
    difficulty: str = "medium"


# ---------- Helpers ----------
def make_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(default="")) -> str:
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Please login first.")
    return payload["sub"]


def user_key(user: str) -> str:
    """Har user ka ek alag notes store hota hai. Username letters/numbers hi hote hain."""
    return re.sub(r"[^a-z0-9]+", "_", f"user_{user}".lower()).strip("_")


def run_ai(func, *args, **kwargs):
    """AI function chalao aur common Gemini errors ko readable message me badlo."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        text = str(e)
        if "503" in text or "UNAVAILABLE" in text:
            raise HTTPException(status_code=503, detail="AI model is busy right now. Please try again in a minute.")
        if "429" in text or "RESOURCE_EXHAUSTED" in text:
            raise HTTPException(status_code=429, detail="Daily AI limit reached. Please try again later.")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")


# ---------- Auth ----------
@app.get("/")
def root():
    return {"status": "Exam Buddy API is running"}


@app.post("/api/signup")
def signup(body: AuthIn):
    ok, message = create_user(body.username, body.password)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@app.post("/api/login")
def login(body: AuthIn):
    if not verify_user(body.username, body.password):
        raise HTTPException(status_code=401, detail="Username ya password galat hai.")
    username = body.username.strip().lower()
    return {"token": make_token(username), "username": username}


@app.get("/api/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}


# ---------- Notes ----------
@app.post("/api/upload")
def upload(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    name = Path(file.filename or "").name
    if not name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    key = user_key(user)
    folder = DATA_DIR / key
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_bytes(file.file.read())

    pages = load_pdf(path)
    if not pages:
        raise HTTPException(
            status_code=400,
            detail="No readable text found. Please upload a text-based PDF, not a scanned one.",
        )
    count = add_chunks(chunk_pages(pages, name, key))
    return {"file": name, "pages": len(pages), "chunks": count}


@app.get("/api/files")
def files(user: str = Depends(get_current_user)):
    return {"files": list_sources(user_key(user))}


@app.post("/api/ask")
def ask(body: AskIn, user: str = Depends(get_current_user)):
    question = (
        f"Previous question: {body.previous}\nFollow-up: {body.question}"
        if body.previous else body.question
    )
    result = run_ai(answer_question, user_key(user), question, source=body.source)
    return {"answer": result["answer"], "pages": result["pages"]}


@app.post("/api/summary")
def summary(body: SummaryIn, user: str = Depends(get_current_user)):
    return {"parts": run_ai(summarize_subject, user_key(user), source=body.source)}


@app.post("/api/quiz")
def quiz(body: QuizIn, user: str = Depends(get_current_user)):
    n = min(max(body.n, 1), 10)
    difficulty = body.difficulty if body.difficulty in ("easy", "medium", "hard") else "medium"
    questions = run_ai(generate_quiz, user_key(user), n=n, difficulty=difficulty, source=body.source)
    return {"questions": questions}

class StudyPlanIn(BaseModel):
    exam: str
    exam_date: str
    hours: int = 2
    request: str = ""


@app.post("/api/study-plan")
def study_plan(body: StudyPlanIn, user: str = Depends(get_current_user)):
    try:
        exam_day = date.fromisoformat(body.exam_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Exam date YYYY-MM-DD format me honi chahiye.")

    days_left = (exam_day - date.today()).days
    if days_left < 1:
        raise HTTPException(status_code=400, detail="Exam date aaj ke baad ki honi chahiye.")

    if not list_sources(user_key(user)):
        raise HTTPException(status_code=400, detail="Pehle notes upload karo, phir study plan banega.")

    hours = min(max(body.hours, 1), 12)
    plan = run_ai(make_plan, user_key(user), body.exam, body.exam_date, days_left, hours, body.request)
    return {"plan": plan, "days_left": days_left}