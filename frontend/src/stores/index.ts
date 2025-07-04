import { ChatStore } from "./ChatStore";
import { IngestStore } from "./IngestStore";

export const chatStore = new ChatStore();
export const ingestStore = new IngestStore();

export { ChatStore, IngestStore };
export type { ChatMessage } from "./ChatStore";
