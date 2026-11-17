import json
import re
from retrieval.hybrid import hybrid_search
from llm.client import ask_llm

QUIZ_PROMPT = """Create {n} multiple-choice questions at {difficulty} difficulty from the notes below.
Return ONLY a JSON list. Each item must have these keys:
"question": a string
"options": a list of exactly 4 strings
"answer": the index (0 to 3) of the correct option
"page": the page number the question comes from

Notes:
{context}
"""


def generate_quiz(subject: str, n: int = 5, difficulty: str = "medium",
                  topic: str = "main concepts", source: str | None = None) -> list[dict]:
    chunks = hybrid_search(subject, topic, k=8, source=source)
    context = "\n\n".join(f"[Page {c['page']}] {c['text']}" for c in chunks)
    raw = ask_llm(QUIZ_PROMPT.format(n=n, difficulty=difficulty, context=context))

    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        raise ValueError("The model did not return a valid quiz. Try again.")
    questions = json.loads(match.group())

    valid = [
        q for q in questions
        if isinstance(q.get("options"), list)
        and len(q["options"]) == 4
        and isinstance(q.get("answer"), int)
        and 0 <= q["answer"] <= 3
    ]
    return valid[:n]