from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from core.workflow_validator import validate_workflow

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class ValidateRequest(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

@router.post("/validate")
def validate(request: ValidateRequest):
    """
    Validates workflow structure and configuration
    """
    result = validate_workflow(request.nodes, request.edges)
    return result