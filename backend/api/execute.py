# api/execute.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.workflow_executor import execute_workflow
from core.workflow_registry import get_workflow  # ← Add

router = APIRouter(prefix="/api/execute", tags=["execute"])

class ExecuteRequest(BaseModel):
    workflow_id: Optional[str] = None  # ← New: workflow_id
    query: str
    nodes: Optional[List[Dict]] = None  # ← Optional (for backward compatibility)
    edges: Optional[List[Dict]] = None

class ExecuteResponse(BaseModel):
    success: bool
    answer: str = None
    sources: List[Dict] = []
    has_context: bool = False
    metadata: Dict = {}
    error: str = None

@router.post("", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    """
    Execute workflow with query
    
    Can accept either:
    - workflow_id + query (preferred)
    - nodes + edges + query (legacy)
    """
    
    try:
        print(f"\n🔵 Execute API called")
        print(f"Query: {request.query}")
        
        # Get workflow from ID or use provided nodes/edges
        if request.workflow_id:
            print(f"Using workflow_id: {request.workflow_id}")
            workflow = get_workflow(request.workflow_id)
            
            if not workflow:
                raise HTTPException(
                    status_code=404,
                    detail=f"Workflow {request.workflow_id} not found"
                )
            
            nodes = workflow["nodes"]
            edges = workflow["edges"]
            
        elif request.nodes and request.edges:
            print(f"Using provided nodes/edges (legacy mode)")
            nodes = request.nodes
            edges = request.edges
            
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either workflow_id or nodes+edges"
            )
        
        # Execute workflow
        result = await execute_workflow(
            query=request.query,
            nodes=nodes,
            edges=edges
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