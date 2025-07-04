#!/usr/bin/env python3
"""
Complete setup script for the MCP Q&A RAG pipeline
This script will:
1. Crawl MCP documentation
2. Process and chunk documents
3. Create embeddings
4. Set up Pinecone vector store
"""
import os
import sys
import time
from config.settings import settings
from crawlers.run_crawler import run_crawler
from utils.document_processor import DocumentProcessor
from utils.vector_store import PineconeVectorStore


def setup_pipeline():
    """Set up the complete RAG pipeline"""
    print("🔧 Setting up MCP Q&A RAG Pipeline...")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Step 1: Validate settings
        print("1️⃣ Validating configuration...")
        settings.validate()
        print("✅ Configuration validated")
        
        # Step 2: Crawl documentation
        print("\n2️⃣ Crawling MCP documentation...")
        if not os.path.exists(settings.DOCUMENTATION_FILE):
            print("📥 Starting web crawling...")
            run_crawler()
            print("✅ Documentation crawled successfully")
        else:
            print("📄 Documentation file already exists, skipping crawl")
        
        # Step 3: Process documents
        print("\n3️⃣ Processing documents...")
        processor = DocumentProcessor()
        
        # Load documents
        documents = processor.load_documents(settings.DOCUMENTATION_FILE)
        print(f"📖 Loaded {len(documents)} documents")
        
        # Process into chunks
        chunks = processor.process_documents(documents)
        print(f"🔪 Created {len(chunks)} text chunks")
        
        # Create embeddings
        print("🧠 Creating embeddings...")
        chunks_with_embeddings = processor.create_embeddings(chunks)
        print(f"✅ Created {len(chunks_with_embeddings)} embeddings")
        
        # Save processed data
        processed_file = settings.DOCUMENTATION_FILE.replace('.json', '_processed.json')
        processor.save_processed_data(chunks_with_embeddings, processed_file)
        print(f"💾 Saved processed data to {processed_file}")
        
        # Step 4: Set up vector store
        print("\n4️⃣ Setting up Pinecone vector store...")
        vector_store = PineconeVectorStore()
        
        # Create index
        vector_store.create_index()
        print("✅ Pinecone index created/connected")
        
        # Upsert documents
        vector_store.upsert_documents(chunks_with_embeddings)
        print("✅ Documents uploaded to vector store")
        
        # Show stats
        stats = vector_store.get_index_stats()
        if stats:
            print(f"📊 Index stats: {stats}")
        
        total_time = time.time() - start_time
        print(f"\n🎉 Pipeline setup completed successfully in {total_time:.2f} seconds!")
        print("\n🚀 You can now start the API server with: python run_server.py")
        
    except Exception as e:
        print(f"\n❌ Pipeline setup failed: {e}")
        print("\n🔍 Please check your configuration and try again.")
        sys.exit(1)


def main():
    """Main function"""
    print("MCP Q&A RAG Pipeline Setup")
    print("=" * 30)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found!")
        print("📝 Please create a .env file based on env.template")
        print("🔑 Make sure to add your OpenAI and Pinecone API keys")
        sys.exit(1)
    
    setup_pipeline()


if __name__ == "__main__":
    main() 