from fastapi import APIRouter
from pydantic import BaseModel
from services.vector_store_service import vector_store
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService

router = APIRouter(prefix="/chat", tags=["chat"])

embedding_service = EmbeddingService()
llm_service = LLMService()

class ChatRequest(BaseModel):
    question: str

@router.post("/")
def chat(req: ChatRequest):
    query_embedding = embedding_service.embed_query(req.question)

    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        k=5
    )

    context = "\n".join([r["text"] for r in results])

    answer = llm_service.generate(
        question=req.question,
        context=context
    )

    return {
        "answer": answer,
        "sources": [r["metadata"] for r in results]
    }

