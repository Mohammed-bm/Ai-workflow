class EmbeddingService:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # Temporary dummy embeddings (dimension = 3)
        return [[0.0, 0.0, 0.0] for _ in texts]
    
    def embed_query(self, text: str):
        # Reuse the same embedding model
        return self.embed_texts([text])[0]