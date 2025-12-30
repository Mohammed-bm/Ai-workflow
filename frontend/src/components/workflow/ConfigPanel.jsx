export default function ConfigPanel({ node, updateNode }) {
  if (!node) {
    return (
      <div className="p-4 text-gray-500">
        Select a node to configure
      </div>
    );
  }

  const handleChange = (key, value) => {
    updateNode(node.id, {
      ...node.data,
      [key]: value,
    });
  };

  switch (node.type) {
    case "userQuery":
      return (
        <div className="p-4">
          <h3 className="font-bold mb-2">User Query</h3>
          <input
            className="border p-2 w-full"
            placeholder="Default query"
            value={node.data.prompt || ""}
            onChange={(e) =>
              handleChange("prompt", e.target.value)
            }
          />
        </div>
      );

    case "llmEngine":
      return (
        <div className="p-4">
          <h3 className="font-bold mb-2">LLM Config</h3>

          <input
            className="border p-2 w-full mb-2"
            placeholder="Model (e.g. gpt-4)"
            value={node.data.model || ""}
            onChange={(e) =>
              handleChange("model", e.target.value)
            }
          />

          <input
            type="number"
            step="0.1"
            className="border p-2 w-full"
            placeholder="Temperature"
            value={node.data.temperature || 0.7}
            onChange={(e) =>
              handleChange("temperature", e.target.value)
            }
          />
        </div>
      );

    default:
      return (
        <div className="p-4 text-gray-500">
          No config required
        </div>
      );
  }
}
