export interface QuestionRequest {
  question: string;
  include_sources?: boolean;
  top_k?: number;
}

export interface Source {
  title: string;
  url: string;
  relevance_score: number;
  snippet: string;
}

export interface QuestionResponse {
  query: string;
  answer: string;
  context_used: boolean;
  sources?: Source[];
  processing_time?: number;
}

export interface IngestRequest {
  force_recrawl?: boolean;
  update_embeddings?: boolean;
}

export interface IngestResponse {
  success: boolean;
  message: string;
  documents_processed: number;
  chunks_created: number;
  embeddings_created: number;
  processing_time: number;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  services: Record<string, string>;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
  timestamp: string;
}
