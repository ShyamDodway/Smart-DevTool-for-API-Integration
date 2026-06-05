import chromadb
from sentence_transformers import SentenceTransformer

from src.config import VECTOR_DB_DIR


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
        self.collection = self.client.get_or_create_collection(
            name="api_docs"
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, chunks):
        embeddings = self.embedding_model.encode(chunks).tolist()

        ids = [f"chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_model.encode([query]).tolist()[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0]