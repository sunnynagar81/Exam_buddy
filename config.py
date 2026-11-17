import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads the .env file

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"          # uploaded study files
CHROMA_DIR = BASE_DIR / "chroma_db"   # vector database storage

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CHUNK_SIZE = 800      # characters per chunk
CHUNK_OVERLAP = 100   # characters shared between neighboring chunks
TOP_K = 5             # number of chunks to retrieve per question

GEMINI_MODEL = "models/gemini-3.5-flash-lite"