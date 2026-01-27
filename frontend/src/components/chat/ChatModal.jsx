import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export default function ChatModal({ workflow, onClose }) {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Ask me anything about your workflow." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
  if (!input.trim()) return;

  const userMessage = input;
  setInput("");

  setMessages((m) => [
    ...m,
    { role: "user", content: userMessage },
  ]);

  try {
    const res = await fetch(`${API_BASE}/api/execute`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: userMessage,
        nodes: workflow.nodes,
        edges: workflow.edges,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Execution failed");
    }

    setMessages((m) => [
      ...m,
      { role: "assistant", content: data.answer },
    ]);
  } catch (err) {
    setMessages((m) => [
      ...m,
      { role: "assistant", content: "❌ Error executing workflow" },
    ]);
  }
};


  return (
    <div className="fixed bottom-4 right-4 w-96 h-500 bg-gray-900 border border-gray-700 rounded-lg flex flex-col z-50">
      {/* Header */}
      <div className="p-3 border-b border-gray-700 flex justify-between">
        <span className="font-semibold">Chat with Stack</span>
        <button onClick={onClose}>✕</button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-3 overflow-y-auto space-y-2 text-sm">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`p-2 rounded max-w-[80%] ${
              m.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-gray-700"
            }`}
          >
            {m.content}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-700 p-2 rounded w-fit">
            ⏳ Thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-gray-700 flex gap-2">
        <input
          className="flex-1 bg-gray-800 p-2 rounded text-sm"
          placeholder="Ask a question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="px-3 bg-blue-600 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}