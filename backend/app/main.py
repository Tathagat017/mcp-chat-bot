import os
import sys
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import (
    QuestionRequest, QuestionResponse, IngestRequest, IngestResponse,
    HealthResponse, ErrorResponse, Source
)
from config.settings import settings
from utils.rag_pipeline import RAGPipeline
from utils.document_processor import DocumentProcessor
from utils.vector_store import PineconeVectorStore
from crawlers.run_crawler import run_crawler

# Initialize FastAPI app
app = FastAPI(
    title="MCP Q&A Chatbot API",
    description="Intelligent Q&A chatbot for Model Context Protocol (MCP) documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
rag_pipeline = None
vector_store = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global rag_pipeline, vector_store
    
    try:
        # Validate settings
        settings.validate()
        
        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline()
        vector_store = PineconeVectorStore()
        
        print("✅ MCP Q&A Chatbot API started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        raise


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "MCP Q&A Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check OpenAI connection
        openai_status = "ok" if settings.OPENAI_API_KEY else "missing_key"
        
        # Check Pinecone connection
        pinecone_status = "ok" if settings.PINECONE_API_KEY else "missing_key"
        
        # Check if vector store is accessible
        vector_store_status = "ok"
        try:
            if vector_store:
                vector_store.get_index_stats()
        except Exception:
            vector_store_status = "error"
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            services={
                "openai": openai_status,
                "pinecone": pinecone_status,
                "vector_store": vector_store_status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about MCP"""
    start_time = time.time()
    
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
        
        # Get answer from RAG pipeline
        response = rag_pipeline.ask(
            query=request.question,
            include_sources=request.include_sources
        )
        
        # Convert sources to Pydantic models
        sources = None
        if request.include_sources and response.get("sources"):
            sources = [
                Source(
                    title=source["title"],
                    url=source["url"],
                    relevance_score=source["relevance_score"],
                    snippet=source["snippet"]
                )
                for source in response["sources"]
            ]
        
        processing_time = time.time() - start_time
        
        return QuestionResponse(
            query=response["query"],
            answer=response["answer"],
            context_used=response["context_used"],
            sources=sources,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest, background_tasks: BackgroundTasks):
    """Ingest and process MCP documentation"""
    start_time = time.time()
    
    try:
        # Check if we need to recrawl
        should_crawl = request.force_recrawl or not os.path.exists(settings.DOCUMENTATION_FILE)
        
        documents_processed = 0
        chunks_created = 0
        embeddings_created = 0
        
        if should_crawl:
            # Run crawler
            print("Starting document crawling...")
            run_crawler()
            
            # Load crawled documents
            if os.path.exists(settings.DOCUMENTATION_FILE):
                with open(settings.DOCUMENTATION_FILE, 'r', encoding='utf-8') as f:
                    import json
                    documents = json.load(f)
                    documents_processed = len(documents)
        
        if request.update_embeddings:
            # Process documents
            processor = DocumentProcessor()
            
            if os.path.exists(settings.DOCUMENTATION_FILE):
                documents = processor.load_documents(settings.DOCUMENTATION_FILE)
                chunks = processor.process_documents(documents)
                chunks_created = len(chunks)
                
                # Create embeddings
                chunks_with_embeddings = processor.create_embeddings(chunks)
                embeddings_created = len(chunks_with_embeddings)
                
                # Save processed data
                processed_file = settings.DOCUMENTATION_FILE.replace('.json', '_processed.json')
                processor.save_processed_data(chunks_with_embeddings, processed_file)
                
                # Update vector store
                if vector_store:
                    vector_store.create_index()
                    vector_store.upsert_documents(chunks_with_embeddings)
        
        processing_time = time.time() - start_time
        
        return IngestResponse(
            success=True,
            message="Documents ingested successfully",
            documents_processed=documents_processed,
            chunks_created=chunks_created,
            embeddings_created=embeddings_created,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        return IngestResponse(
            success=False,
            message=f"Error during ingestion: {str(e)}",
            documents_processed=0,
            chunks_created=0,
            embeddings_created=0,
            processing_time=processing_time
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    ) 