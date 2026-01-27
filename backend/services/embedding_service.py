_model = None

def get_embedding_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )
    return _model

class EmbeddingService:
    def __init__(self):
        self.model = get_embedding_model()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()
