import React, { useState } from "react";
import { observer } from "mobx-react-lite";
import {
  Container,
  Paper,
  Stack,
  Text,
  Button,
  Group,
  Switch,
  Alert,
  Progress,
  Card,
  Badge,
  Loader,
  Divider,
} from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCloudUploadAlt,
  faCheckCircle,
  faExclamationTriangle,
  faInfoCircle,
  faRefresh,
  faCog,
} from "@fortawesome/free-solid-svg-icons";
import { ingestStore } from "../stores";

export const IngestInterface: React.FC = observer(() => {
  const [forceRecrawl, setForceRecrawl] = useState(false);
  const [updateEmbeddings, setUpdateEmbeddings] = useState(true);

  const handleIngest = async () => {
    try {
      await ingestStore.ingestDocuments(forceRecrawl, updateEmbeddings);
    } catch {
      // Error is already handled in the store
    }
  };

  const handleClearResult = () => {
    ingestStore.clearResult();
    ingestStore.clearError();
  };

  return (
    <Container
      size="md"
      style={{ height: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Paper p="md" radius="md" style={{ flex: 1 }}>
        {/* Header */}
        <Group position="apart" mb="xl">
          <Text size="xl" weight={600}>
            Knowledge Ingestion
          </Text>
          <FontAwesomeIcon icon={faCloudUploadAlt} size="lg" />
        </Group>

        {/* Description */}
        <Alert
          icon={<FontAwesomeIcon icon={faInfoCircle} />}
          title="About Knowledge Ingestion"
          color="blue"
          mb="xl"
        >
          <Text size="sm">
            This process crawls the MCP documentation, processes it into chunks,
            creates embeddings, and updates the vector store for improved Q&A
            accuracy.
          </Text>
        </Alert>

        {/* Configuration */}
        <Card p="md" radius="md" mb="xl">
          <Text size="lg" weight={500} mb="md">
            <FontAwesomeIcon icon={faCog} style={{ marginRight: 8 }} />
            Configuration
          </Text>

          <Stack spacing="md">
            <Switch
              label="Force Recrawl"
              description="Recrawl documents even if they already exist"
              checked={forceRecrawl}
              onChange={(event) => setForceRecrawl(event.currentTarget.checked)}
              disabled={ingestStore.isLoading}
            />

            <Switch
              label="Update Embeddings"
              description="Create and update embeddings in the vector store"
              checked={updateEmbeddings}
              onChange={(event) =>
                setUpdateEmbeddings(event.currentTarget.checked)
              }
              disabled={ingestStore.isLoading}
            />
          </Stack>
        </Card>

        {/* Error Alert */}
        {ingestStore.error && (
          <Alert
            icon={<FontAwesomeIcon icon={faExclamationTriangle} />}
            title="Error"
            color="red"
            mb="md"
            onClose={ingestStore.clearError}
            withCloseButton
          >
            {ingestStore.error}
          </Alert>
        )}

        {/* Loading State */}
        {ingestStore.isLoading && (
          <Card p="md" radius="md" mb="xl">
            <Group position="center" spacing="md">
              <Loader size="sm" />
              <Text size="sm" color="dimmed">
                Processing documents... This may take a few minutes.
              </Text>
            </Group>
            <Progress value={50} animate mt="md" />
          </Card>
        )}

        {/* Results */}
        {ingestStore.lastIngestResult && (
          <Card p="md" radius="md" mb="xl">
            <Group position="apart" mb="md">
              <Text size="lg" weight={500}>
                <FontAwesomeIcon
                  icon={faCheckCircle}
                  style={{ marginRight: 8, color: "green" }}
                />
                Ingestion Complete
              </Text>
              <Badge
                color={ingestStore.lastIngestResult.success ? "green" : "red"}
                variant="light"
              >
                {ingestStore.lastIngestResult.success ? "Success" : "Failed"}
              </Badge>
            </Group>

            <Text size="sm" color="dimmed" mb="md">
              {ingestStore.lastIngestResult.message}
            </Text>

            <Divider mb="md" />

            <Stack spacing="sm">
              <Group position="apart">
                <Text size="sm">Documents Processed:</Text>
                <Badge variant="light">
                  {ingestStore.lastIngestResult.documents_processed}
                </Badge>
              </Group>

              <Group position="apart">
                <Text size="sm">Chunks Created:</Text>
                <Badge variant="light">
                  {ingestStore.lastIngestResult.chunks_created}
                </Badge>
              </Group>

              <Group position="apart">
                <Text size="sm">Embeddings Created:</Text>
                <Badge variant="light">
                  {ingestStore.lastIngestResult.embeddings_created}
                </Badge>
              </Group>

              <Group position="apart">
                <Text size="sm">Processing Time:</Text>
                <Badge variant="light">
                  {ingestStore.lastIngestResult.processing_time.toFixed(2)}s
                </Badge>
              </Group>
            </Stack>
          </Card>
        )}

        {/* Actions */}
        <Group position="center" spacing="md">
          <Button
            size="lg"
            leftIcon={<FontAwesomeIcon icon={faRefresh} />}
            onClick={handleIngest}
            disabled={ingestStore.isLoading}
            loading={ingestStore.isLoading}
          >
            {ingestStore.isLoading ? "Processing..." : "Start Ingestion"}
          </Button>

          {ingestStore.lastIngestResult && (
            <Button
              variant="light"
              onClick={handleClearResult}
              disabled={ingestStore.isLoading}
            >
              Clear Results
            </Button>
          )}
        </Group>
      </Paper>
    </Container>
  );
});
