import { Handle, Position } from "reactflow";

export default function OutputNode({ data }) {
  return (
    <div className="bg-white border rounded p-3 w-64 shadow">
      <div className="font-semibold text-sm mb-2">Output</div>

      <div className="text-sm whitespace-pre-wrap min-h-[60px]">
        {data?.answer || "No output yet"}
      </div>

      <Handle type="target" position={Position.Left} />
    </div>
  );
}
