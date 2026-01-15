export default function TopBar({ onBuild, onSave }) {
  return (
    <div className="h-14 flex items-center justify-between px-6 border-b border-gray-800">
      <h1 className="text-lg font-semibold">AI Workflow Builder</h1>

      <div className="flex gap-3">
        <button
          onClick={onBuild}
          className="px-3 py-1 bg-gray-800 rounded text-sm"
        >
          Build Stack
        </button>

        <button
          onClick={onSave}
          className="px-3 py-1 bg-blue-600 rounded text-sm"
        >
          Save Workflow
        </button>
      </div>
    </div>
  );
}
