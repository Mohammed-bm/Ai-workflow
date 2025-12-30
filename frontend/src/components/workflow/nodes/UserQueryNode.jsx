import { Handle, Position } from "reactflow";

export default function UserQueryNode() {
  return (
    <div className="bg-white border rounded p-3 w-40 shadow">
      <div className="font-semibold text-sm mb-2">User Query</div>

      <Handle type="source" position={Position.Right} />
    </div>
  );
}
