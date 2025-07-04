#!/usr/bin/env python3
"""
Script to run the MCP Q&A Chatbot API server
"""
import uvicorn
from config.settings import settings

def main():
    """Run the FastAPI server"""
    print("🚀 Starting MCP Q&A Chatbot API server...")
    print(f"📍 Server will be available at: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API documentation at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Alternative docs at: http://{settings.HOST}:{settings.PORT}/redoc")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 