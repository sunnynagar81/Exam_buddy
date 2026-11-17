from retrieval.hybrid import hybrid_search
from llm.client import ask_llm
from llm.prompts import QA_PROMPT


def answer_question(subject: str, question: str, source: str | None = None) -> dict:
    chunks = hybrid_search(subject, question, source=source)
    context = "\n\n".join(f"[Page {c['page']}] {c['text']}" for c in chunks)
    answer = ask_llm(QA_PROMPT.format(context=context, question=question))
    pages = sorted({c["page"] for c in chunks})
    return {"answer": answer, "pages": pages, "chunks": chunks}