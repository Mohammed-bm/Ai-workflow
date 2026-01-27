import { useCallback, useRef, useState, useEffect } from "react";
import ReactFlow, {
  useNodesState,
  useEdgesState,
  addEdge,
} from "reactflow";
import "reactflow/dist/style.css";

import UserQueryNode from "./nodes/UserQueryNode";
import KnowledgeBaseNode from "./nodes/KnowledgeBaseNode";
import LLMEngineNode from "./nodes/LLMEngineNode";
import OutputNode from "./nodes/OutputNode";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

const nodeTypes = {
  userQuery: UserQueryNode,
  knowledgeBase: KnowledgeBaseNode,
  llmEngine: LLMEngineNode,
  output: OutputNode,
};

export default function WorkflowCanvas({ onBuilt, exposeActions }) {
  /* -------------------- STATE (UI only) -------------------- */
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [built, setBuilt] = useState(false);

  const wrapperRef = useRef(null);

  /* -------------------- REFS (execution) -------------------- */
  const nodesRef = useRef([]);
  const edgesRef = useRef([]);
  const builtRef = useRef(false);
  const workflowIdRef = useRef(null);

  nodesRef.current = nodes;
  edgesRef.current = edges;

  /* -------------------- CONNECT -------------------- */
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  /* -------------------- BUILD STACK -------------------- */
  const buildStack = useCallback(async () => {
    if (!nodesRef.current.length || !edgesRef.current.length) {
      alert("Connect nodes before building stack");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/workflows/build`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes: nodesRef.current,
          edges: edgesRef.current,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(
          data.detail?.errors?.join("\n") ||
          data.detail?.message ||
          "Workflow validation failed"
        );
        return;
      }

      workflowIdRef.current = data.workflow_id;
      builtRef.current = true;

      setBuilt(true);
      onBuilt?.();

      alert(`✅ Stack built successfully\nID: ${data.workflow_id}`);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to build stack");
    }
  }, []);

  /* -------------------- SAVE WORKFLOW -------------------- */
  const saveWorkflow = async () => {
  if (!builtRef.current || !workflowIdRef.current) {
    alert("Build stack before saving workflow");
    return;
  }

  const name = prompt("Enter workflow name");
  if (!name) return;

  const res = await fetch(`${API_BASE}/api/workflows/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      workflow_id: workflowIdRef.current,
      name,
      nodes: nodesRef.current,
      edges: edgesRef.current,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Failed to save workflow");
    return;
  }

  alert("✅ Workflow saved successfully");
};

/* -------------------- LOAD WORKFLOW (TEMP) -------------------- */
const loadWorkflow = async (workflowId) => {
  try {
    const res = await fetch(
      `${API_BASE}/api/workflows/${workflowId}`
    );

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Failed to load workflow");
      return;
    }

    setNodes(
      data.nodes.map((node) => ({
        ...node,
        data: {
          ...node.data,
          onRun: runWorkflow, // 🔥 reattach runtime function
        },
      }))
    );
    setEdges(data.edges);

    workflowIdRef.current = data.workflow_id;
    builtRef.current = true;
    setBuilt(true);

    alert(`📂 Loaded workflow: ${data.name}`);
  } catch (err) {
    console.error(err);
    alert("❌ Failed to load workflow");
  }
};


  /* -------------------- RUN WORKFLOW -------------------- */
  const runWorkflow = async (query) => {
    if (!builtRef.current || !workflowIdRef.current) {
      alert("Build stack before running");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflow_id: workflowIdRef.current,
          query,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || data.detail);

      setNodes((nds) =>
        nds.map((n) =>
          n.type === "output"
            ? { ...n, data: { ...n.data, answer: data.answer } }
            : n
        )
      );
    } catch (err) {
      console.error(err);
      setNodes((nds) =>
        nds.map((n) =>
          n.type === "output"
            ? { ...n, data: { ...n.data, answer: "❌ Execution failed" } }
            : n
        )
      );
    }
  };

  /* -------------------- DRAG & DROP -------------------- */
  const onDrop = useCallback((event) => {
    event.preventDefault();

    const type = event.dataTransfer.getData("application/reactflow");
    if (!type) return;

    const bounds = wrapperRef.current.getBoundingClientRect();
    const position = {
      x: event.clientX - bounds.left,
      y: event.clientY - bounds.top,
    };

    const id = `${Date.now()}`;

    setNodes((nds) =>
      nds.concat({
        id,
        type,
        position,
        data: {
          onRun: runWorkflow, // SAFE: uses refs
        },
      })
    );
  }, []);

    /* expose build to App.jsx ONCE */
  useEffect(() => {
  exposeActions?.({
    buildStack,
    saveWorkflow,
    loadWorkflow,
  });
}, [exposeActions, buildStack, saveWorkflow]);

  /* -------------------- UI -------------------- */
  return (
    <div
      ref={wrapperRef}
      onDrop={onDrop}
      onDragOver={(e) => e.preventDefault()}
      className="h-full w-full relative bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] bg-size-[20px_20px]"
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      />
    </div>
  );
}
