import { Handle, Position } from "reactflow";

export default function OutputNode({ data }) {
  return (
    <div className="bg-white border border-gray-300 rounded-xl p-5 shadow-md min-w-60 max-w-120">
      <div className="font-semibold text-sm mb-3 text-gray-700">
        Output
      </div>

      <div className="text-sm text-gray-800 whitespace-normal wrap-break-word">
        {data?.answer || "No output yet"}
      </div>

      <Handle type="target" position={Position.Left} />
    </div>
  );
}
