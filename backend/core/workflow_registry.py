# core/workflow_registry.py

from typing import Dict, Optional
import uuid

# In-memory storage for workflows
WORKFLOWS: Dict[str, dict] = {}

def create_workflow(nodes: list, edges: list) -> str:
    """
    Store workflow and return workflow_id
    """
    workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
    
    WORKFLOWS[workflow_id] = {
        "nodes": nodes,
        "edges": edges,
        "created_at": __import__('datetime').datetime.utcnow().isoformat()
    }
    
    return workflow_id

def get_workflow(workflow_id: str) -> Optional[dict]:
    """
    Retrieve workflow by ID
    """
    return WORKFLOWS.get(workflow_id)

def delete_workflow(workflow_id: str) -> bool:
    """
    Delete workflow
    """
    if workflow_id in WORKFLOWS:
        del WORKFLOWS[workflow_id]
        return True
    return False

def list_workflows() -> list:
    """
    List all workflow IDs
    """
    return list(WORKFLOWS.keys())