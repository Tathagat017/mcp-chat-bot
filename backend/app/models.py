from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str = Field(..., description="The question to ask about MCP", min_length=1)
    include_sources: bool = Field(True, description="Whether to include source information in response")
    top_k: Optional[int] = Field(None, description="Number of top results to retrieve", ge=1, le=20)


class Source(BaseModel):
    """Source information for answers"""
    title: str
    url: str
    relevance_score: float
    snippet: str


class QuestionResponse(BaseModel):
    """Response model for questions"""
    query: str
    answer: str
    context_used: bool
    sources: Optional[List[Source]] = None
    processing_time: Optional[float] = None


class IngestRequest(BaseModel):
    """Request model for ingesting documents"""
    force_recrawl: bool = Field(False, description="Force recrawling even if data exists")
    update_embeddings: bool = Field(True, description="Update embeddings after crawling")


class IngestResponse(BaseModel):
    """Response model for ingestion"""
    success: bool
    message: str
    documents_processed: int
    chunks_created: int
    embeddings_created: int
    processing_time: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: str 