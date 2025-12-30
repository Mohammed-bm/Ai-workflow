import { Handle, Position } from "reactflow";

export default function LLMEngineNode() {
  return (
    <div className="bg-white border rounded p-3 w-40 shadow">
      <div className="font-semibold text-sm mb-2">LLM Engine</div>

      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
}
