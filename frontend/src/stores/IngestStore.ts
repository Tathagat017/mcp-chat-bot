import { makeAutoObservable, runInAction } from "mobx";
import { apiService } from "../services/api";
import type { IngestResponse } from "../types/api";

export class IngestStore {
  isLoading = false;
  error: string | null = null;
  lastIngestResult: IngestResponse | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  async ingestDocuments(forceRecrawl = false, updateEmbeddings = true) {
    this.isLoading = true;
    this.error = null;

    try {
      const response = await apiService.ingestDocuments({
        force_recrawl: forceRecrawl,
        update_embeddings: updateEmbeddings,
      });

      runInAction(() => {
        this.lastIngestResult = response;
        this.isLoading = false;
      });

      return response;
    } catch (error) {
      runInAction(() => {
        this.error =
          error instanceof Error ? error.message : "An error occurred";
        this.isLoading = false;
      });
      throw error;
    }
  }

  clearError() {
    this.error = null;
  }

  clearResult() {
    this.lastIngestResult = null;
  }
}
