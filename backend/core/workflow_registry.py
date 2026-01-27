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

def get_workflow(workflow_id: str, db=None) -> Optional[dict]:
    """
    Retrieve workflow by ID:
    1. Check in-memory cache
    2. Fallback to database
    """

    # 1️⃣ In-memory (fast path)
    workflow = WORKFLOWS.get(workflow_id)
    if workflow:
        print(f"⚡ Workflow {workflow_id} found in memory")
        return workflow

    print(f"🗄️ Workflow {workflow_id} not in memory, checking DB")

    # 2️⃣ Database fallback
    if db:
        db_workflow = (
            db.query(Workflow)
            .filter(Workflow.id == workflow_id)
            .first()
        )

        if db_workflow:
            workflow_data = {
                "nodes": db_workflow.nodes,
                "edges": db_workflow.edges,
            }

            # 🔁 Warm the cache
            WORKFLOWS[workflow_id] = workflow_data
            print(f"✅ Workflow {workflow_id} loaded from DB into memory")

            return workflow_data

    print(f"❌ Workflow {workflow_id} not found anywhere")
    return None

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