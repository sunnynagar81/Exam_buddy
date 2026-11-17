import time
from google import genai
from google.genai import types
from config import GOOGLE_API_KEY, GEMINI_MODEL

_client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options=types.HttpOptions(timeout=60000),  # 60 seconds, in milliseconds
)


def ask_llm(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = _client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            return response.text
        except Exception:
            # Retries on 503 (busy), network drops, and timeouts
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise