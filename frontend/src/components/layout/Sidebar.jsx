const items = [
  { type: "userQuery", label: "User Query" },
  { type: "knowledgeBase", label: "Knowledge Base" },
  { type: "llmEngine", label: "LLM Engine" },
  { type: "output", label: "Output" },
];

export default function Sidebar() {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <div className="w-64 border-r bg-slate-50 p-4">
      <div className="flex flex-col gap-3">
        {items.map((item) => (
          <div
            key={item.type}
            draggable
            onDragStart={(e) => onDragStart(e, item.type)}
            className="bg-sky-600 border border-gray-700 rounded p-3 cursor-grab hover:bg-sky-700 text-white"
          >
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
}