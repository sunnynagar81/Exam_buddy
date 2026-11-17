from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_pages(pages: list[dict], source: str, subject: str) -> list[dict]:
    """Split each page into overlapping chunks and keep the page number on every chunk."""
    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP
    for item in pages:
        text = item["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + CHUNK_SIZE]
            if piece.strip():
                chunks.append({
                    "text": piece,
                    "source": source,
                    "subject": subject,
                    "page": item["page"],
                })
    return chunks