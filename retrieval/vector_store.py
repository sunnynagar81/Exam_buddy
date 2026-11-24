import time

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from google.genai import errors as genai_errors
from config import CHROMA_DIR, GOOGLE_API_KEY, TOP_K

EMBED_MODEL = "gemini-embedding-001"
BATCH_SIZE = 20
MAX_RETRIES = 6

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
_gemini = genai.Client(api_key=GOOGLE_API_KEY)


class GeminiEmbedder(EmbeddingFunction):
    """Gemini API se embeddings banata hai. Quota (429) aane par wait karke dobara try karta hai."""

    def __call__(self, input: Documents) -> Embeddings:
        texts = list(input)
        vectors = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            vectors.extend(self._embed_with_retry(batch))
            time.sleep(1)  # batches ke beech thoda gap, quota bachane ke liye
        return vectors

    def _embed_with_retry(self, batch):
        for attempt in range(MAX_RETRIES):
            try:
                res = _gemini.models.embed_content(model=EMBED_MODEL, contents=batch)
                return [e.values for e in res.embeddings]
            except genai_errors.ClientError as e:
                if "429" in str(e) and attempt < MAX_RETRIES - 1:
                    time.sleep(20 * (attempt + 1))  # 20s, 40s, 60s... wait karega
                    continue
                raise

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