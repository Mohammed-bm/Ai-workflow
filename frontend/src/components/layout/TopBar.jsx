import { useEffect, useState } from "react";

export default function TopBar({ onBuild, onSave, onSelectWorkflow }) {
  const [workflows, setWorkflows] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/workflows")
      .then((res) => res.json())
      .then(setWorkflows)
      .catch(console.error);
  }, []);

  return (
    <div className="h-14 flex items-center justify-between px-6 border-b border-gray-800 bg-slate-100">
      <h1 className="text-lg font-semibold black">
        AI Workflow Builder
      </h1>

      <div className="flex items-center gap-4">
        {/* Workflow dropdown */}
        <select
          defaultValue=""
          onChange={(e) => onSelectWorkflow(e.target.value)}
          className="
            px-3 py-1.5
            bg-sky-600
            border border-gray-700
            rounded
            text-sm font-medium text-white
            hover:bg-sky-700
            focus:outline-none focus:ring-1 focus:ring-sky-500
            transition
          "
        >
          <option value="" disabled>
            Select workflow
          </option>

          {workflows.map((wf) => (
            <option key={wf.workflow_id} value={wf.workflow_id}>
              {wf.name}
            </option>
          ))}
        </select>

        {/* Build button */}
        <button
          onClick={onBuild}
          className="
            px-4 py-1.5
            bg-sky-600
            border border-gray-700
            rounded
            text-sm font-medium text-white
            hover:bg-sky-700
            hover:border-gray-600
            transition
          "
        >
          Build Stack
        </button>

        {/* Save button */}
        <button
          onClick={onSave}
          className="
            px-4 py-1.5
            bg-sky-600
            rounded
            text-sm font-medium text-white
            hover:bg-sky-700
            focus:outline-none focus:ring-1 focus:ring-blue-400
            transition
          "
        >
          Save Workflow
        </button>
      </div>
    </div>
  );
}
