from pathlib import Path
from pypdf import PdfReader


def load_pdf(path: Path) -> list[dict]:
    """Return a list of {'page': int, 'text': str}, one entry per non-empty page."""
    reader = PdfReader(str(path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": number, "text": text})
    return pages