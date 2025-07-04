import React from "react";
import { Tabs, Container, Paper } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faComments,
  faCloudUploadAlt,
} from "@fortawesome/free-solid-svg-icons";

interface NavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  onTabChange,
}) => {
  return (
    <Container size="xl" mb="md">
      <Paper p="xs" radius="md">
        <Tabs value={activeTab} onTabChange={onTabChange}>
          <Tabs.List>
            <Tabs.Tab value="chat" icon={<FontAwesomeIcon icon={faComments} />}>
              Chat
            </Tabs.Tab>
            <Tabs.Tab
              value="ingest"
              icon={<FontAwesomeIcon icon={faCloudUploadAlt} />}
            >
              Knowledge Ingestion
            </Tabs.Tab>
          </Tabs.List>
        </Tabs>
      </Paper>
    </Container>
  );
};
