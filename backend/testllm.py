def test_view_chromadb_contents():
    from services.vector_store_service import vector_store

    results = vector_store.collection.get(
        include=["documents", "metadatas", "embeddings"]
    )

    print("\n📦 ChromaDB CONTENTS")
    print("────────────────────")

    print(f"Total vectors: {len(results['ids'])}\n")

    for i, doc_id in enumerate(results["ids"]):
        print(f"🔹 ID: {doc_id}")
        print(f"📄 Text (first 200 chars): {results['documents'][i][:200]}")
        print(f"🧾 Metadata: {results['metadatas'][i]}")
        print(f"🧠 Embedding length: {len(results['embeddings'][i])}")
        print("-" * 40)

    # Basic assertion so pytest doesn't treat this as empty
    assert len(results["ids"]) >= 0
