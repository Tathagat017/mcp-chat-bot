# MCP Q&A Chatbot Backend

An intelligent Q&A chatbot backend for Model Context Protocol (MCP) documentation using RAG (Retrieval-Augmented Generation) architecture.

## 🚀 Features

- **Web Crawling**: Automatically crawls MCP documentation from Anthropic's website
- **Document Processing**: Chunks and processes documents for optimal retrieval
- **Vector Search**: Uses Pinecone for semantic similarity search
- **RAG Pipeline**: Combines retrieval with OpenAI's GPT for accurate answers
- **FastAPI Backend**: RESTful API with automatic documentation
- **Health Monitoring**: Built-in health checks and monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Crawler   │───▶│  Document       │───▶│   Embeddings    │
│   (Scrapy)      │    │  Processor      │    │   (OpenAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │◀───│  RAG Pipeline   │◀───│  Vector Store   │
│   Server        │    │                 │    │  (Pinecone)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+ (tested with 3.13)
- OpenAI API key
- Pinecone API key
- Internet connection for crawling

## 🛠️ Installation

1. **Clone the repository and navigate to backend:**

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   ```bash
   cp env.template .env
   ```

   Edit `.env` and add your API keys:

   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   PINECONE_API_KEY=your-pinecone-key-here
   PINECONE_ENV=us-east-1-aws
   PINECONE_INDEX_NAME=mcp-docs
   ```

## 🚀 Quick Start

1. **Set up the complete pipeline:**

   ```bash
   python setup_pipeline.py
   ```

   This will:

   - Crawl MCP documentation
   - Process and chunk documents
   - Create embeddings
   - Set up Pinecone vector store

2. **Start the API server:**

   ```bash
   python run_server.py
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📡 API Endpoints

### `GET /`

Root endpoint with basic information.

### `GET /health`

Health check endpoint showing service status.

### `POST /ask`

Ask a question about MCP.

**Request:**

```json
{
  "question": "What is Model Context Protocol?",
  "include_sources": true,
  "top_k": 5
}
```

**Response:**

```json
{
  "query": "What is Model Context Protocol?",
  "answer": "Model Context Protocol (MCP) is...",
  "context_used": true,
  "sources": [
    {
      "title": "Model Context Protocol",
      "url": "https://www.anthropic.com/news/model-context-protocol",
      "relevance_score": 0.95,
      "snippet": "MCP is a protocol that..."
    }
  ],
  "processing_time": 1.23
}
```

### `POST /ingest`

Trigger document ingestion and processing.

**Request:**

```json
{
  "force_recrawl": false,
  "update_embeddings": true
}
```

## 🔧 Configuration

Edit `config/settings.py` or use environment variables:

| Variable              | Description             | Default       |
| --------------------- | ----------------------- | ------------- |
| `OPENAI_API_KEY`      | OpenAI API key          | Required      |
| `PINECONE_API_KEY`    | Pinecone API key        | Required      |
| `PINECONE_ENV`        | Pinecone environment    | us-east-1-aws |
| `PINECONE_INDEX_NAME` | Pinecone index name     | mcp-docs      |
| `HOST`                | Server host             | localhost     |
| `PORT`                | Server port             | 8000          |
| `CHUNK_SIZE`          | Text chunk size         | 1000          |
| `CHUNK_OVERLAP`       | Chunk overlap           | 200           |
| `TOP_K_RESULTS`       | Top results to retrieve | 5             |

## 🧪 Testing

Test individual components:

```bash
# Test crawler
cd crawlers
python run_crawler.py

# Test document processor
cd utils
python document_processor.py

# Test vector store
python vector_store.py

# Test RAG pipeline
python rag_pipeline.py
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   └── models.py            # Pydantic models
├── config/
│   └── settings.py          # Configuration
├── crawlers/
│   ├── mcp_spider.py        # Scrapy spider
│   └── run_crawler.py       # Crawler runner
├── utils/
│   ├── document_processor.py # Document processing
│   ├── vector_store.py      # Pinecone integration
│   └── rag_pipeline.py      # RAG implementation
├── data/                    # Data directory
├── requirements.txt         # Dependencies
├── env.template            # Environment template
├── setup_pipeline.py       # Complete setup script
├── run_server.py           # Server runner
└── README.md              # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the virtual environment and all dependencies are installed.

2. **API key errors**: Verify your `.env` file has the correct API keys.

3. **Pinecone connection issues**: Check your Pinecone API key and environment settings.

4. **Crawler issues**: Ensure you have internet connection and the target site is accessible.

### Debug Mode

Run with debug logging:

```bash
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('run_server.py').read())"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for MCP documentation
- [OpenAI](https://openai.com/) for embeddings and chat completion
- [Pinecone](https://www.pinecone.io/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Scrapy](https://scrapy.org/) for web crawling

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Create an issue in the repository

---

**Happy coding! 🚀**
