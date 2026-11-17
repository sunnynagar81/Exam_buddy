import chromadb
from config import CHROMA_DIR, TOP_K

client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(subject: str):
    name = subject.lower().replace(" ", "_")
    return client.get_or_create_collection(name=name)


def list_sources(subject: str) -> list[str]:
    """Return the names of all uploaded files in a subject."""
    data = get_collection(subject).get()
    return sorted({m["source"] for m in data["metadatas"]})


def add_chunks(chunks: list[dict]) -> int:
    if not chunks:
        return 0
    collection = get_collection(chunks[0]["subject"])
    collection.upsert(
        ids=[f"{c['source']}-{c['page']}-{i}" for i, c in enumerate(chunks)],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {"source": c["source"], "page": c["page"], "subject": c["subject"]}
            for c in chunks
        ],
    )
    return len(chunks)


def search(subject: str, question: str, k: int = TOP_K, source: str | None = None) -> list[dict]:
    """Return the most relevant chunks, optionally only from one file."""
    collection = get_collection(subject)
    where = {"source": source} if source else None
    results = collection.query(query_texts=[question], n_results=k, where=where)
    found = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        found.append({"text": text, "source": meta["source"], "page": meta["page"]})
    return found