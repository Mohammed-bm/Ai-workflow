# api/workflows.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from core.workflow_validator import validate_workflow
from core.workflow_registry import create_workflow, get_workflow  # ← Add

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class ValidateRequest(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

class BuildRequest(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

class BuildResponse(BaseModel):
    workflow_id: str
    status: str

# Existing validate endpoint
@router.post("/validate")
def validate(request: ValidateRequest):
    """Validates workflow structure"""
    validation = validate_workflow(request.nodes, request.edges)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Workflow validation failed",
                "errors": validation["errors"]
            }
        )

    return {"valid": True}

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

# NEW: Get workflow by ID
@router.get("/{workflow_id}")
def get_workflow_by_id(workflow_id: str):
    """Retrieve workflow by ID"""
    workflow = get_workflow(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow