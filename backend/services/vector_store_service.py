import math

class VectorStoreService:
    def __init__(self):
        self.store = []

    def _cosine_similarity(self, a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot / (norm_a * norm_b + 1e-8)

    def similarity_search(self, query_embedding, k=5):
        print("VECTOR STORE SIZE:", len(self.store))

        scored = []
        for item in self.store:
            score = self._cosine_similarity(
                query_embedding,
                item["embedding"]
            )
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:k]]

    def add_text(self, texts, embeddings, metadatas):
        for t, e, m in zip(texts, embeddings, metadatas):
            self.store.append({
                "text": t,
                "embedding": e,
                "metadata": m
            })

        print(f"🧠 Stored {len(texts)} vectors in memory")


# ✅ SINGLETON INSTANCE (THIS is what everyone imports)
vector_store = VectorStoreService()
