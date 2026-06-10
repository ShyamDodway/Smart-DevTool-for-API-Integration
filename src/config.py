import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

GROQ_API_KEY = get_secret("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"

DATA_DIR = "data"
VECTOR_DB_DIR = "vector_db"
GENERATED_DIR = "generated"