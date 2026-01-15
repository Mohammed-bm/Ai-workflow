import { useState, useRef } from "react";
import AppLayout from "./components/layout/AppLayout";
import TopBar from "./components/layout/TopBar";
import Sidebar from "./components/layout/Sidebar";
import WorkflowCanvas from "./components/workflow/WorkFlowCanvas";
import ChatModal from "./components/chat/ChatModal";

export default function App() {
  const [showChat, setShowChat] = useState(false);
  const [built, setBuilt] = useState(false);

  const actionsRef = useRef({});

  return (
    <AppLayout>
      <TopBar
        onBuild={() => actionsRef.current.buildStack?.()}
        onSave={() => actionsRef.current.saveWorkflow?.()}
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
          <WorkflowCanvas
            onBuilt={() => setBuilt(true)}
            exposeActions={(actions) => {
              actionsRef.current = actions;
            }}
          />
        </div>
      </div>

      {showChat && <ChatModal onClose={() => setShowChat(false)} />}
    </AppLayout>
  );
}
