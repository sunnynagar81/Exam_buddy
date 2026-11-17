from retrieval.vector_store import get_collection
from llm.client import ask_llm

SUMMARY_PROMPT = """Summarize the notes below for exam revision. Give:
1. A short summary (3 to 5 lines)
2. Important points as bullet points
3. Key terms with one-line meanings

Notes:
{context}
"""


def summarize_subject(subject: str, pages_per_batch: int = 5, source: str | None = None) -> list[dict]:
    where = {"source": source} if source else None
    data = get_collection(subject).get(where=where)

    pages = {}
    for doc, meta in zip(data["documents"], data["metadatas"]):
        key = (meta["source"], meta["page"])
        pages.setdefault(key, [])
        if doc not in pages[key]:
            pages[key].append(doc)

    keys = sorted(pages)
    results = []
    for i in range(0, len(keys), pages_per_batch):
        batch = keys[i:i + pages_per_batch]
        context = "\n\n".join(
            f"[{src}, Page {page}] " + " ".join(pages[(src, page)])
            for src, page in batch
        )
        summary = ask_llm(SUMMARY_PROMPT.format(context=context))
        results.append({"pages": [page for _, page in batch], "summary": summary})
    return results