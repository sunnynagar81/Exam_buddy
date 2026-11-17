from rank_bm25 import BM25Okapi
from config import TOP_K
from retrieval.vector_store import get_collection, search as vector_search


def hybrid_search(subject: str, question: str, k: int = TOP_K, source: str | None = None) -> list[dict]:
    collection = get_collection(subject)
    where = {"source": source} if source else None
    data = collection.get(where=where)
    docs = data["documents"]
    metas = data["metadatas"]
    if not docs:
        return []

    # 1. Keyword search
    bm25 = BM25Okapi([d.lower().split() for d in docs])
    scores = bm25.get_scores(question.lower().split())
    keyword_order = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)[:k]
    keyword_hits = [
        {"text": docs[i], "source": metas[i]["source"], "page": metas[i]["page"]}
        for i in keyword_order
    ]

    # 2. Meaning search
    vector_hits = vector_search(subject, question, k, source)

    # 3. Merge both lists
    merged = {}
    for hits in (keyword_hits, vector_hits):
        for rank, hit in enumerate(hits):
            key = hit["text"]
            if key not in merged:
                merged[key] = {"hit": hit, "score": 0.0}
            merged[key]["score"] += 1 / (60 + rank)

    ranked = sorted(merged.values(), key=lambda m: m["score"], reverse=True)
    return [m["hit"] for m in ranked[:k]]