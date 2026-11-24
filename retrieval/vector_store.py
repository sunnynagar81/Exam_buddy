import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from config import CHROMA_DIR, GOOGLE_API_KEY, TOP_K

EMBED_MODEL = "gemini-embedding-001"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
_gemini = genai.Client(api_key=GOOGLE_API_KEY)


class GeminiEmbedder(EmbeddingFunction):
    """Gemini API se embeddings banata hai, taaki server par local model load na ho."""

    def __call__(self, input: Documents) -> Embeddings:
        texts = list(input)
        vectors = []
        for i in range(0, len(texts), 50):
            batch = texts[i:i + 50]
            res = _gemini.models.embed_content(model=EMBED_MODEL, contents=batch)
            vectors.extend(e.values for e in res.embeddings)
        return vectors

    @staticmethod
    def name() -> str:
        return "gemini-embedder"


def get_collection(subject: str):
    name = subject.lower().replace(" ", "_")
    return client.get_or_create_collection(name=name, embedding_function=GeminiEmbedder())


def list_sources(subject: str) -> list[str]:
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
    collection = get_collection(subject)
    where = {"source": source} if source else None
    results = collection.query(query_texts=[question], n_results=k, where=where)
    found = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        found.append({"text": text, "source": meta["source"], "page": meta["page"]})
    return found