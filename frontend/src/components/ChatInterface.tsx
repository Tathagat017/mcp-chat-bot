import React, { useState, useRef, useEffect } from "react";
import { observer } from "mobx-react-lite";
import {
  Container,
  Paper,
  Stack,
  TextInput,
  Button,
  ScrollArea,
  Text,
  Group,
  Badge,
  Anchor,
  Loader,
  Alert,
  ActionIcon,
  Divider,
} from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPaperPlane,
  faUser,
  faRobot,
  faClock,
  faExternalLinkAlt,
  faTrash,
  faExclamationTriangle,
} from "@fortawesome/free-solid-svg-icons";
import { chatStore } from "../stores";
import type { ChatMessage } from "../stores";

const ChatBubble: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.type === "user";

  return (
    <Group
      align="flex-start"
      spacing="sm"
      style={{
        flexDirection: isUser ? "row-reverse" : "row",
        marginBottom: 16,
      }}
    >
      <Paper
        p="xs"
        radius="xl"
        style={{
          backgroundColor: isUser ? "#228be6" : "#f8f9fa",
          color: isUser ? "white" : "black",
          minWidth: 40,
          minHeight: 40,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <FontAwesomeIcon icon={isUser ? faUser : faRobot} size="sm" />
      </Paper>

      <Paper
        p="md"
        radius="lg"
        style={{
          backgroundColor: isUser ? "#228be6" : "#f8f9fa",
          color: isUser ? "white" : "black",
          maxWidth: "70%",
          wordBreak: "break-word",
        }}
      >
        <Text size="sm">{message.content}</Text>

        {message.sources && message.sources.length > 0 && (
          <Stack spacing="xs" mt="sm">
            <Divider color={isUser ? "white" : "gray"} />
            <Text size="xs" weight={500}>
              Sources:
            </Text>
            {message.sources.map((source, index) => (
              <Paper
                key={index}
                p="xs"
                radius="sm"
                style={{ backgroundColor: "rgba(255,255,255,0.1)" }}
              >
                <Group position="apart" spacing="xs">
                  <Text size="xs" truncate style={{ flex: 1 }}>
                    {source.title}
                  </Text>
                  <Badge size="xs" variant="light">
                    {(source.relevance_score * 100).toFixed(1)}%
                  </Badge>
                </Group>
                <Anchor
                  href={source.url}
                  target="_blank"
                  size="xs"
                  style={{ color: isUser ? "white" : "#228be6" }}
                >
                  <FontAwesomeIcon icon={faExternalLinkAlt} size="xs" /> View
                </Anchor>
                <Text size="xs" mt="xs" opacity={0.8}>
                  {source.snippet}
                </Text>
              </Paper>
            ))}
          </Stack>
        )}

        <Group position="apart" mt="xs">
          <Text size="xs" opacity={0.7}>
            {message.timestamp.toLocaleTimeString()}
          </Text>
          {message.processing_time && (
            <Group spacing="xs">
              <FontAwesomeIcon icon={faClock} size="xs" />
              <Text size="xs" opacity={0.7}>
                {message.processing_time.toFixed(2)}s
              </Text>
            </Group>
          )}
        </Group>
      </Paper>
    </Group>
  );
};

export const ChatInterface: React.FC = observer(() => {
  const [question, setQuestion] = useState("");
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to bottom when new messages are added
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [chatStore.messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || chatStore.isLoading) return;

    const currentQuestion = question.trim();
    setQuestion("");
    await chatStore.askQuestion(currentQuestion);
  };

  const handleClearChat = () => {
    chatStore.clearMessages();
    chatStore.clearError();
  };

  return (
    <Container
      size="lg"
      style={{ height: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Paper
        p="md"
        radius="md"
        style={{ flex: 1, display: "flex", flexDirection: "column" }}
      >
        {/* Header */}
        <Group position="apart" mb="md">
          <Text size="xl" weight={600}>
            MCP Assistant
          </Text>
          <ActionIcon
            variant="light"
            color="red"
            onClick={handleClearChat}
            disabled={chatStore.messages.length === 0}
          >
            <FontAwesomeIcon icon={faTrash} />
          </ActionIcon>
        </Group>

        {/* Error Alert */}
        {chatStore.error && (
          <Alert
            icon={<FontAwesomeIcon icon={faExclamationTriangle} />}
            title="Error"
            color="red"
            mb="md"
            onClose={chatStore.clearError}
            withCloseButton
          >
            {chatStore.error}
          </Alert>
        )}

        {/* Messages */}
        <ScrollArea
          style={{ flex: 1, minHeight: 400 }}
          viewportRef={scrollAreaRef}
          type="auto"
        >
          <Stack spacing="md" p="md">
            {chatStore.messages.length === 0 ? (
              <Text align="center" color="dimmed" size="lg" mt="xl">
                Ask me anything about Model Context Protocol (MCP)!
              </Text>
            ) : (
              chatStore.messages.map((message) => (
                <ChatBubble key={message.id} message={message} />
              ))
            )}

            {chatStore.isLoading && (
              <Group position="center" mt="md">
                <Loader size="sm" />
                <Text size="sm" color="dimmed">
                  Thinking...
                </Text>
              </Group>
            )}
          </Stack>
        </ScrollArea>

        {/* Input */}
        <form onSubmit={handleSubmit}>
          <Group spacing="sm" mt="md">
            <TextInput
              placeholder="Ask your question about MCP..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              style={{ flex: 1 }}
              disabled={chatStore.isLoading}
            />
            <Button
              type="submit"
              disabled={!question.trim() || chatStore.isLoading}
              leftIcon={<FontAwesomeIcon icon={faPaperPlane} />}
            >
              Send
            </Button>
          </Group>
        </form>
      </Paper>
    </Container>
  );
});
