import { useState } from "react";
import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { Navigation } from "./components/Navigation";
import { ChatInterface } from "./components/ChatInterface";
import { IngestInterface } from "./components/IngestInterface";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  const handleTabChange = (tab: string | null) => {
    if (tab) {
      setActiveTab(tab);
    }
  };

  return (
    <MantineProvider
      theme={{
        colorScheme: "light",
        primaryColor: "blue",
        fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif",
        headings: {
          fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif",
        },
      }}
      withGlobalStyles
      withNormalizeCSS
    >
      <Notifications />
      <div style={{ minHeight: "100vh", backgroundColor: "#f8f9fa" }}>
        <Navigation activeTab={activeTab} onTabChange={handleTabChange} />

        {activeTab === "chat" && <ChatInterface />}
        {activeTab === "ingest" && <IngestInterface />}
      </div>
    </MantineProvider>
  );
}

export default App;
