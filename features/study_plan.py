from retrieval.hybrid import hybrid_search
from llm.client import ask_llm

PLAN_PROMPT = """You are an expert exam coach. Build a personalized study plan for this student.

Student details:
- Exam: {exam}
- Exam date: {exam_date}
- Days left: {days_left}
- Study time per day: {hours} hours
- Student's request: {request}

Rules:
- Plan ONLY topics that appear in the notes below.
- If the student asked for something specific, follow it.
- Spread the topics across the days, and include revision and practice tests.
- Keep the last 3 days for light revision.

Format the answer in Markdown with these sections:
### Strategy
(2 to 3 short lines)
### Week-by-week plan
For each week, use a "#### Week N" heading, then one bullet per day in this form: **Day X:** topic, task, time.
### Daily routine
(bullet points)
### Final 3 days
(bullet points)
### Tips
(3 short bullet points)

Notes:
{context}
"""


def make_plan(subject_key: str, exam: str, exam_date: str, days_left: int, hours: int, request: str) -> str:
    chunks = hybrid_search(subject_key, "main topics chapters key concepts", k=12)
    context = "\n\n".join(f"[Page {c['page']}] {c['text']}" for c in chunks)
    prompt = PLAN_PROMPT.format(
        exam=exam,
        exam_date=exam_date,
        days_left=days_left,
        hours=hours,
        request=request or "No special request",
        context=context,
    )
    return ask_llm(prompt)