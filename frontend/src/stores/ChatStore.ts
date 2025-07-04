import { makeAutoObservable, runInAction } from "mobx";
import { apiService } from "../services/api";
import type { QuestionResponse, Source } from "../types/api";

export interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: Source[];
  processing_time?: number;
}

export class ChatStore {
  messages: ChatMessage[] = [];
  isLoading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  addUserMessage(content: string) {
    const message: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content,
      timestamp: new Date(),
    };
    this.messages.push(message);
  }

  addAssistantMessage(response: QuestionResponse) {
    const message: ChatMessage = {
      id: Date.now().toString(),
      type: "assistant",
      content: response.answer,
      timestamp: new Date(),
      sources: response.sources,
      processing_time: response.processing_time,
    };
    this.messages.push(message);
  }

  async askQuestion(question: string, includeSources = true) {
    this.isLoading = true;
    this.error = null;

    try {
      // Add user message
      this.addUserMessage(question);

      // Call API
      const response = await apiService.askQuestion({
        question,
        include_sources: includeSources,
      });

      // Add assistant response
      runInAction(() => {
        this.addAssistantMessage(response);
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error =
          error instanceof Error ? error.message : "An error occurred";
        this.isLoading = false;
      });
    }
  }

  clearMessages() {
    this.messages = [];
  }

  clearError() {
    this.error = null;
  }
}
