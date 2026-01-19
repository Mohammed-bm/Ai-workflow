import { useState } from "react";
import { Handle, Position } from "reactflow";

export default function UserQueryNode({ data }) {
  const [query, setQuery] = useState("");

  return (
    <div className="w-64 rounded-xl bg-white border border-gray-200 shadow-sm p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-800">
          User Query
        </h3>
      </div>

      {/* Input */}
      <textarea
        className="w-full resize-none rounded-md border px-3 py-2 text-s"
        rows={3}
        placeholder="Type your question here..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* Action */}
      <button
        onClick={() => {
          data.onRun(query);
        }}
        className="mt-3 w-full rounded-md bg-blue-600 text-white text-sm font-medium
                   py-2 hover:bg-blue-700 active:bg-blue-800 transition"
      >
        ▶ Run
      </button>

      {/* Output handle */}
      <Handle
        type="source"
        position={Position.Right}
        className="bg-blue-600 w-3 h-3"
      />
    </div>
  );
}
