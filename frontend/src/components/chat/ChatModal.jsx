import { useState } from "react";

export default function ChatModal({ workflow, onClose }) {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Ask me anything about your workflow." },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
  if (!input.trim()) return;

  const userMessage = input;

  setMessages((msgs) => [
    ...msgs,
    { role: "user", content: userMessage },
  ]);

  setInput("");

  try {
    const res = await fetch("http://localhost:8000/api/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        workflow,
        query: userMessage,
      }),
    });

    const data = await res.json();

    setMessages((msgs) => [
      ...msgs,
      { role: "assistant", content: data.output },
    ]);
  } catch (err) {
    setMessages((msgs) => [
      ...msgs,
      {
        role: "assistant",
        content: "❌ Error executing workflow",
      },
    ]);
  }
};


  return (
    <div className="fixed bottom-4 right-4 w-96 h-[500px] bg-gray-900 border border-gray-700 rounded-lg flex flex-col z-50">
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
