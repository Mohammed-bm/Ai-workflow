from typing import List, Dict, Optional
from services.embedding_service import get_embedding_model
from services.vector_store_service import get_vector_store
from services.llm_service import LLMService


def find_node_by_type(nodes: List[Dict], node_type: str) -> Optional[Dict]:
    for node in nodes:
        if node.get("type") == node_type:
            return node
    return None


async def execute_workflow(query: str, nodes: List[Dict], edges: List[Dict]) -> Dict:
    print(f"\n🟢 ===== WORKFLOW EXECUTION START =====")
    print(f"Query: {query}")

    user_query_node = find_node_by_type(nodes, "userQuery")
    kb_node = find_node_by_type(nodes, "knowledgeBase")
    llm_node = find_node_by_type(nodes, "llmEngine")
    output_node = find_node_by_type(nodes, "output")

    if not user_query_node:
        raise ValueError("User Query component not found")
    if not llm_node:
        raise ValueError("LLM Engine component not found")
    if not output_node:
        raise ValueError("Output component not found")

    print("✅ All required components found")

    # --------------------------------------------------
    # Step 1: Knowledge Base (LAZY)
    # --------------------------------------------------
    context = None
    sources = []

    if kb_node:
        print("\n🟡 Step 1: Knowledge Base Component")

        try:
            print("  - Loading embedding model lazily")
            embedding_model = get_embedding_model()

            print("  - Loading vector store lazily")
            vector_store = get_vector_store()

            print("  - Generating query embedding")
            query_embedding = embedding_model.encode(
                query,
                convert_to_numpy=True,
                normalize_embeddings=True,
            ).tolist()

            print("  - Searching vector store")
            results = vector_store.similarity_search(
                query_embedding=query_embedding,
                k=5,
            )

            if results:
                context = "\n\n".join(r["text"] for r in results)
                sources = [r["metadata"] for r in results]
                print(f"  ✅ Retrieved {len(results)} chunks")
            else:
                print("  ⚠️ No KB results found")

        except Exception as e:
            print(f"  ⚠️ Knowledge Base failed: {e}")

    else:
        print("\n⚪ Knowledge Base not in workflow — skipped")

    # --------------------------------------------------
    # Step 2: LLM Engine (LAZY CLIENT)
    # --------------------------------------------------
    print("\n🟡 Step 2: LLM Engine Component")

    llm_service = LLMService()
    llm_config = llm_node.get("data", {})

    try:
        answer = llm_service.generate(
            question=query,
            context=context,
        )
        print("  ✅ LLM response generated")

    except Exception as e:
        print(f"  ❌ LLM generation failed: {e}")
        raise ValueError(f"LLM generation failed: {str(e)}")

    # --------------------------------------------------
    # Step 3: Output
    # --------------------------------------------------
    print("\n🟡 Step 3: Output Component")

    return {
        "answer": answer,
        "sources": sources,
        "has_context": context is not None,
        "metadata": {
            "query": query,
            "model": llm_config.get("model", "default"),
            "chunks_used": len(sources),
        },
    }
