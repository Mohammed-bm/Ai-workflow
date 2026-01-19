from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from core.workflow_validator import validate_workflow
from core.workflow_registry import create_workflow, get_workflow 
from sqlalchemy.orm import Session
from fastapi import Depends
from db.deps import get_db
from db.models.workflow import Workflow

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class BuildRequest(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

class BuildResponse(BaseModel):
    workflow_id: str
    status: str

class SaveWorkflowRequest(BaseModel):
    workflow_id: str
    name: str
    nodes: List[Dict]
    edges: List[Dict]

# NEW: Build endpoint
@router.post("/build", response_model=BuildResponse)
def build(request: BuildRequest):
    """
    Validate and store workflow, return workflow_id
    """
    
    # Validate first
    validation = validate_workflow(request.nodes, request.edges)
    
    if not validation["valid"]:
        raise HTTPException(
            status_code=400, 
            detail={
                "message": "Workflow validation failed",
                "errors": validation["errors"]
            }
        )
    
    # Store workflow
    workflow_id = create_workflow(request.nodes, request.edges)
    
    return BuildResponse(
        workflow_id=workflow_id,
        status="ready"
    )

@router.post("/save")
def save_workflow(
    request: SaveWorkflowRequest,
    db: Session = Depends(get_db)
):
    # Check if workflow already saved
    existing = (
        db.query(Workflow)
        .filter(Workflow.workflow_id == request.workflow_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Workflow already saved"
        )

    workflow = Workflow(
        workflow_id=request.workflow_id,
        name=request.name,
        nodes=request.nodes,
        edges=request.edges,
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return {
        "message": "Workflow saved successfully",
        "workflow_id": request.workflow_id
    }

@router.get("/{workflow_id}")
def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.query(Workflow).filter(
        Workflow.workflow_id == workflow_id
    ).first()

    if not wf:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "workflow_id": wf.workflow_id,
        "name": wf.name,
        "nodes": wf.nodes,
        "edges": wf.edges
    }

@router.get("/")
def list_workflows(db: Session = Depends(get_db)):
    workflows = db.query(Workflow).all()

    return [
        {
            "workflow_id": wf.workflow_id,
            "name": wf.name,
        }
        for wf in workflows
    ]
