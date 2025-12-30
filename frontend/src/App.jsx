import { useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import TopBar from "./components/layout/TopBar";
import Sidebar from "./components/layout/Sidebar";
import WorkflowCanvas from "./components/workflow/WorkFlowCanvas";
import ChatModal from "./components/chat/ChatModal";

export default function App() {
  const [showChat, setShowChat] = useState(false);
  const [workflow, setWorkflow] = useState(null);

  return (
    <AppLayout>
      <TopBar onChat={() => setShowChat(true)} />

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
