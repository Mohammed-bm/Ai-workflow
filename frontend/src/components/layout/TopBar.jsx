export default function TopBar({ onChat }) {
  return (
    <div className="h-14 flex items-center justify-between px-6 border-b border-gray-800">
      <h1 className="text-lg font-semibold">
        AI Workflow Builder
      </h1>

      <div className="flex gap-3">
        <button className="px-3 py-1 bg-gray-800 rounded text-sm">
          Build Stack
        </button>

        <button
          onClick={onChat}
          className="px-3 py-1 bg-blue-600 rounded text-sm"
        >
          Chat with Stack
        </button>
      </div>
    </div>
  );
}
