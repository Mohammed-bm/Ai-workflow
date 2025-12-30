# core/workflow_validator.py

from collections import defaultdict, deque

REQUIRED_SINGLE = ["userQuery"]
REQUIRED_AT_LEAST_ONE = ["llmEngine", "output"]

def validate_workflow(nodes, edges):
    errors = []
    warnings = []
    
    # Input validation - check if nodes/edges are valid
    if not isinstance(nodes, list):
        errors.append("Nodes must be a list")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    if not isinstance(edges, list):
        errors.append("Edges must be a list")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # Check if all nodes have required fields
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node at index {i} must be an object")
            continue
            
        if "id" not in node:
            errors.append(f"Node at index {i} is missing 'id' field")
        
        if "type" not in node:
            errors.append(f"Node at index {i} is missing 'type' field")
    
    # If basic validation failed, return early
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # Now safe to access node["id"] and node["type"]
    node_ids = {n["id"] for n in nodes}
    node_types = defaultdict(list)
    for n in nodes:
        node_types[n["type"]].append(n["id"])
    
    # Rule 1: Required components
    for t in REQUIRED_SINGLE:
        if len(node_types[t]) != 1:
            errors.append(f"Exactly one {t} component required")
    
    for t in REQUIRED_AT_LEAST_ONE:
        if len(node_types[t]) < 1:
            errors.append(f"At least one {t} component required")
    
    # Build graph
    graph = defaultdict(list)
    indegree = defaultdict(int)
    
    for e in edges:
        if not isinstance(e, dict):
            errors.append("Invalid edge format")
            continue
        
        source = e.get("source")
        target = e.get("target")
        
        if not source:
            errors.append("Edge missing 'source' field")
            continue
        
        if not target:
            errors.append("Edge missing 'target' field")
            continue
        
        if source not in node_ids:
            errors.append(f"Edge source '{source}' does not exist")
            continue
        
        if target not in node_ids:
            errors.append(f"Edge target '{target}' does not exist")
            continue
        
        graph[source].append(target)
        indegree[target] += 1
    
    # Rule 2: No isolated nodes
    for node_id in node_ids:
        if node_id not in graph and indegree[node_id] == 0:
            errors.append(f"Node {node_id} is isolated (not connected)")
    
    # Rule 3: Specific node constraints
    for n in nodes:
        if n["type"] == "userQuery" and indegree[n["id"]] > 0:
            errors.append("User Query cannot have incoming edges")
        
        if n["type"] == "output" and graph[n["id"]]:
            errors.append("Output cannot have outgoing edges")
    
    # Rule 4: Configuration checks
    for n in nodes:
        if n["type"] == "knowledgeBase":
            if not n.get("data", {}).get("documents"):
                warnings.append("Knowledge Base has no documents uploaded")
        
        if n["type"] == "llmEngine":
            if not n.get("data", {}).get("api_key"):
                warnings.append("LLM Engine missing API key")
            if not n.get("data", {}).get("model"):
                warnings.append("LLM Engine missing model selection")
    
    # Rule 5: Cycle detection (Kahn's algorithm)
    q = deque([n for n in node_ids if indegree[n] == 0])
    visited = 0
    
    while q:
        cur = q.popleft()
        visited += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    
    if visited != len(node_ids):
        errors.append("Workflow contains a cycle (circular dependency)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }