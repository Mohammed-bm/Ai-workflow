import { useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import TopBar from "./components/layout/TopBar";
import Sidebar from "./components/layout/Sidebar";
import WorkflowCanvas from "./components/workflow/WorkFlowCanvas";
import ChatModal from "./components/chat/ChatModal";

export default function App() {
  const [showChat, setShowChat] = useState(false);
  const [workflow, setWorkflow] = useState(null);
  const [built, setBuilt] = useState(false);

  const buildStack = async () => {
    if (!workflow) {
      alert("Please save workflow first.");
      return;
    }

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/workflows/validate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(workflow),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Workflow validation failed");
        return;
      }

      setBuilt(true);
      alert("✅ Stack built successfully");
    } catch (err) {
      alert("❌ Failed to build stack");
    }
  };

  return (
    <AppLayout>
      <TopBar
        onBuild={buildStack}
        onChat={() => {
          if (!built) {
            alert("Build stack first");
            return;
          }
          setShowChat(true);
        }}
      />

      <div className="flex flex-1">
        <Sidebar />
        <div className="flex-1">
          <WorkflowCanvas onSave={setWorkflow} />
        </div>
      </div>

      {showChat && (
        <ChatModal
          workflow={workflow}
          onClose={() => setShowChat(false)}
        />
      )}
    </AppLayout>
  );
}