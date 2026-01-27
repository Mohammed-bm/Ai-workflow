import chromadb
from chromadb.config import Settings
import os
import shutil
import uuid
from typing import List

class VectorStoreService:
    def __init__(self):
        self.persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
        self._init_client()

    def _init_client(self):
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"📦 ChromaDB initialized at {self.persist_dir}")

    def clear_collection(self):
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        print("🧹 ChromaDB collection cleared")


    def add_text(self, texts: List[str], embeddings: List[List[float]], metadatas: List[dict]):
        ids = [str(uuid.uuid4()) for _ in texts]
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"✅ Added {len(texts)} vectors")

    def similarity_search(self, query_embedding: List[float], k: int = 5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        documents = []
        for i, doc in enumerate(results["documents"][0]):
            documents.append({
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            })

        print(f"🔍 Found {len(documents)} documents")
        return documents

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        print("🚀 Initializing Chroma lazily")
        _vector_store = VectorStoreService()
    return _vector_store

