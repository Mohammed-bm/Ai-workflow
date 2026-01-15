# services/workflow_executor.py

from typing import List, Dict, Optional
from services.embedding_service import EmbeddingService
from services.vector_store_service import vector_store
from services.llm_service import LLMService
# from services.web_search_service import WebSearchService  # Add if you have this

embedding_service = EmbeddingService()
llm_service = LLMService()
# web_search_service = WebSearchService()  # Uncomment when ready

def find_node_by_type(nodes: List[Dict], node_type: str) -> Optional[Dict]:
    """Find first node of given type"""
    for node in nodes:
        if node.get("type") == node_type:
            return node
    return None

def find_node_by_id(nodes: List[Dict], node_id: str) -> Optional[Dict]:
    """Find node by ID"""
    for node in nodes:
        if node.get("id") == node_id:
            return node
    return None

async def execute_workflow(query: str, nodes: List[Dict], edges: List[Dict]) -> Dict:
    """
    Executes workflow based on node configuration
    
    Flow: User Query → (Optional) Knowledge Base → LLM Engine → Output
    """
    
    print(f"\n🟢 ===== WORKFLOW EXECUTION START =====")
    print(f"Query: {query}")
    print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
    
    # Step 1: Find components in workflow
    user_query_node = find_node_by_type(nodes, "userQuery")
    kb_node = find_node_by_type(nodes, "knowledgeBase")
    llm_node = find_node_by_type(nodes, "llmEngine")
    output_node = find_node_by_type(nodes, "output")
    
    # Validation
    if not user_query_node:
        raise ValueError("User Query component not found in workflow")
    if not llm_node:
        raise ValueError("LLM Engine component not found in workflow")
    if not output_node:
        raise ValueError("Output component not found in workflow")
    
    print(f"✅ All required components found")
    
    # Step 2: Execute Knowledge Base (if exists)
    context = None
    sources = []
    
    if kb_node:
        print(f"\n🟡 Step 1: Knowledge Base Component")
        try:
            print(f"  - Generating query embedding...")
            query_embedding = embedding_service.embed_query(query)
            
            print(f"  - Searching vector store...")
            results = vector_store.similarity_search(
                query_embedding=query_embedding,
                k=5  # Get top 5 chunks
            )
            
            if not results:
                print("❌ KnowledgeBase retrieval failed (no relevant chunks)")
                context = None
                sources = []
            else:
                print(f"  ✅ KnowledgeBase returned {len(results)} chunks")
                context = "\n\n".join(r["text"] for r in results)
                sources = [r["metadata"] for r in results]
                
        except Exception as e:
            print(f"  ⚠️ Knowledge Base failed: {e}")
            context = None
    else:
        print(f"\n⚪ Knowledge Base not in workflow - skipping")
    
    # Step 3: Execute LLM Engine
    print(f"\n🟡 Step 2: LLM Engine Component")
    
    llm_config = llm_node.get("data", {})
    
    #Web search
    #web_results = None
    #if llm_config.get("use_web_search", False):
    #    print(f"  - Performing web search...")
    #    try:
    #       web_results = web_search_service.search(query)
    #        print(f"  ✅ Web search completed")
    #   except Exception as e:
    #       print(f"  ⚠️ Web search failed: {e}")
    
    # Build final context
    final_context = context if context else None
    
    print(f"  - Calling LLM...")
    print(f"    Model: {llm_config.get('model', 'default')}")
    print(f"    Has context: {final_context is not None}")
    
    try:
        # Call your LLM service (adjust based on your implementation)
        answer = llm_service.generate(
            question=query,
            context=final_context
        )
        print(f"  ✅ LLM response generated")
        
    except Exception as e:
        print(f"  ❌ LLM generation failed: {e}")
        raise ValueError(f"LLM generation failed: {str(e)}")
    
    # Step 4: Output Component
    print(f"\n🟡 Step 3: Output Component")
    print(f"  - Formatting response...")
    
    result = {
        "answer": answer,
        "sources": sources,
        "has_context": context is not None,
        "metadata": {
            "query": query,
            "model": llm_config.get("model", "unknown"),
            "chunks_used": len(sources)
        }
    }
    
    print(f"\n✅ ===== WORKFLOW EXECUTION COMPLETE =====\n")
    
    return result