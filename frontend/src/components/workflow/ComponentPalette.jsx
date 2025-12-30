const components = [
  { type: "userQuery", label: "User Query" },
  { type: "knowledgeBase", label: "Knowledge Base" },
  { type: "llmEngine", label: "LLM Engine" },
  { type: "output", label: "Output" },
];

export default function ComponentPalette() {
  const onDragStart = (event, type) => {
    event.dataTransfer.setData("application/reactflow", type);
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <div className="w-64 border-r border-gray-800 p-4">
      <h2 className="text-sm font-semibold mb-4 text-gray-400">
        Components
      </h2>

      <div className="flex flex-col gap-3">
        {components.map((item) => (
          <div
            key={item.type}
            draggable
            onDragStart={(e) => onDragStart(e, item.type)}
            className="bg-gray-900 border border-gray-700 rounded p-3 cursor-move hover:bg-gray-800"
          >
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
}
