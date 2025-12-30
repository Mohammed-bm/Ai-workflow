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

// Register custom nodes
const nodeTypes = {
  userQuery: UserQueryNode,
  knowledgeBase: KnowledgeBaseNode,
  llmEngine: LLMEngineNode,
  output: OutputNode,
};

export default function WorkflowCanvas({ onSave }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const reactFlowWrapper = useRef(null);

  // Connect nodes
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Allow drag over canvas
  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  // Handle drop from sidebar
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const type = event.dataTransfer.getData("application/reactflow");
      if (!type) return;

      const bounds = reactFlowWrapper.current.getBoundingClientRect();

      const position = {
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      };

      const id = `${Date.now()}`;

      const newNode = {
        id,
        type,
        position,
        data: {
          // Used by KnowledgeBase node
          onUpload: (fileInfo) => {
            setNodes((nds) =>
              nds.map((n) =>
                n.id === id
                  ? { ...n, data: { ...n.data, ...fileInfo } }
                  : n
              )
            );
          },
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes]
  );

  return (
    <div
      ref={reactFlowWrapper}
      onDrop={onDrop}
      onDragOver={onDragOver}
      className="h-full w-full relative
        bg-[radial-gradient(#2a2a2a_1px,transparent_1px)]
        bg-[size:20px_20px]"
    >
      {/* Save Workflow */}
      <button
        onClick={() => {
          const errors = validateWorkflow(nodes, edges);
          if (errors.length) {
            alert(errors.join("\n"));
            return;
          }

          const workflow = exportWorkflow(nodes, edges);
          console.log("WORKFLOW JSON:", workflow);

          // 🔥 Send workflow to App
          if (onSave) {
            onSave(workflow);
          }
        }}
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
