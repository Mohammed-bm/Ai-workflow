import { Handle, Position } from "reactflow";

export default function OutputNode() {
  return (
    <div className="bg-white border rounded p-3 w-44 shadow">
      <div className="font-semibold text-sm mb-2">Output</div>

      <Handle type="target" position={Position.Left} />
    </div>
  );
}
