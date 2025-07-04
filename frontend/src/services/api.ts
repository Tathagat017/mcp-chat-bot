import type {
  QuestionRequest,
  QuestionResponse,
  IngestRequest,
  IngestResponse,
  HealthResponse,
} from "../types/api";

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = "http://localhost:8080") {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }

  async askQuestion(request: QuestionRequest): Promise<QuestionResponse> {
    return this.request<QuestionResponse>("/ask", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async ingestDocuments(request: IngestRequest): Promise<IngestResponse> {
    return this.request<IngestResponse>("/ingest", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>("/health");
  }
}

export const apiService = new ApiService();
