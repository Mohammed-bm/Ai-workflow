# api/execute.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from services.workflow_executor import execute_workflow

router = APIRouter(prefix="/api/execute", tags=["execute"])

class ExecuteRequest(BaseModel):
    query: str
    nodes: List[Dict]
    edges: List[Dict]

class ExecuteResponse(BaseModel):
    success: bool
    answer: str = None
    sources: List[Dict] = []
    has_context: bool = False
    metadata: Dict = {}
    error: str = None

@router.post("/", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    """
    Execute workflow with given query
    
    Example request:
    {
        "query": "What is your refund policy?",
        "nodes": [...],
        "edges": [...]
    }
    """
    
    try:
        print(f"\n🔵 Execute API called")
        print(f"Query: {request.query}")
        
        # Execute workflow
        result = await execute_workflow(
            query=request.query,
            nodes=request.nodes,
            edges=request.edges
        )
        
        return ExecuteResponse(
            success=True,
            answer=result["answer"],
            sources=result["sources"],
            has_context=result["has_context"],
            metadata=result["metadata"]
        )
        
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        print(f"❌ Execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")