import { useCallback, useRef } from "react";
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

import { validateWorkflow } from "../../utils/validation";
import { exportWorkflow } from "../../utils/exportWorkflow";

const nodeTypes = {
  userQuery: UserQueryNode,
  knowledgeBase: KnowledgeBaseNode,
  llmEngine: LLMEngineNode,
  output: OutputNode,
};

export default function WorkflowCanvas({ onSave }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const wrapperRef = useRef(null);

  // 🔥 IMPORTANT: live refs to avoid stale closure
  const nodesRef = useRef([]);
  const edgesRef = useRef([]);

  nodesRef.current = nodes;
  edgesRef.current = edges;

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  // ✅ CORE EXECUTION LOGIC (FIXED)
  const runWorkflow = async (query) => {
    const liveNodes = nodesRef.current;
    const liveEdges = edgesRef.current;

    console.log("RUN CLICKED", {
      nodesCount: liveNodes.length,
      edgesCount: liveEdges.length,
      liveNodes,
      liveEdges,
    });

    if (!liveNodes.length || !liveEdges.length) {
      alert("Connect nodes before running");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          nodes: liveNodes,
          edges: liveEdges,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || data.detail);

      // Inject answer into Output node
      setNodes((nds) =>
        nds.map((n) =>
          n.type === "output"
            ? { ...n, data: { ...n.data, answer: data.answer } }
            : n
        )
      );
    } catch (err) {
      console.error("Execution failed:", err);
      setNodes((nds) =>
        nds.map((n) =>
          n.type === "output"
            ? {
                ...n,
                data: { ...n.data, answer: "❌ Execution failed" },
              }
            : n
        )
      );
    }
  };

  const onDrop = useCallback(
    (event) => {
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
            onRun: runWorkflow, // ✅ SAFE: uses refs
            onUpload: (fileInfo) => {
              setNodes((all) =>
                all.map((n) =>
                  n.id === id
                    ? { ...n, data: { ...n.data, ...fileInfo } }
                    : n
                )
              );
            },
          },
        })
      );
    },
    [] // ❗ do NOT add nodes/edges here
  );

  const saveWorkflow = () => {
    const errors = validateWorkflow(nodes, edges);
    if (errors.length) {
      alert(errors.join("\n"));
      return;
    }

    const workflow = exportWorkflow(nodes, edges);
    onSave(workflow);
    alert("💾 Workflow saved");
  };

  return (
    <div
      ref={wrapperRef}
      onDrop={onDrop}
      onDragOver={(e) => e.preventDefault()}
      className="h-full w-full relative
        bg-[radial-gradient(#2a2a2a_1px,transparent_1px)]
        bg-[size:20px_20px]"
    >
      <button
        onClick={saveWorkflow}
        className="absolute top-4 right-4 bg-black text-white px-4 py-2 rounded z-10"
      >
        Save Workflow
      </button>

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
