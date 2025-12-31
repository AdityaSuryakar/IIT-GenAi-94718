import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = r"D:\GenAi Internship CDAC\My_Project\Scraper"
VECTOR_DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db_no_split")

EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
LLM_MODEL = "google/gemma-3n-e4b"

BASE_URL = "http://127.0.0.1:1234/v1"
DUMMY_API_KEY = "Dummy-key"
