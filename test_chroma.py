from services.vector_store_service import VectorStoreService

vs = VectorStoreService()

texts = ["Hello world", "Chroma works"]
embeddings = [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
]
metadatas = [{"source": "test"}, {"source": "test"}]

vs.add_text(
    texts=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Stored successfully")
