import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"

DATA_DIR = "data"
VECTOR_DB_DIR = "vector_db"
GENERATED_DIR = "generated"