# MCP Chatbot - Model Context Protocol Q&A System

A full-stack intelligent Q&A chatbot system for Model Context Protocol (MCP) documentation, featuring automated document crawling, vector embeddings, and conversational AI.

## 🚀 Features

### Backend (FastAPI + Python)

- **Intelligent Q&A**: RAG-powered question answering using OpenAI GPT
- **Document Crawling**: Automated MCP documentation scraping
- **Vector Search**: Pinecone-based semantic search with embeddings
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Document Processing**: Intelligent chunking and preprocessing

### Frontend (React + TypeScript)

- **Interactive Chat**: Real-time Q&A interface with message history
- **Knowledge Management**: Document ingestion and processing controls
- **Source References**: View source documents with relevance scores
- **Modern UI**: Built with Mantine UI components
- **State Management**: MobX for reactive state handling

## 🏗️ Architecture

```
MCP Chatbot
├── backend/           # FastAPI Python backend
│   ├── app/          # Main application code
│   ├── config/       # Configuration settings
│   ├── crawlers/     # Web scraping modules
│   ├── utils/        # RAG pipeline & vector store
│   └── data/         # Processed documentation
└── frontend/         # React TypeScript frontend
    ├── src/
    │   ├── components/   # UI components
    │   ├── stores/      # MobX state management
    │   ├── services/    # API communication
    │   └── types/       # TypeScript interfaces
    └── public/
```

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **OpenAI GPT** - Language model for Q&A
- **Pinecone** - Vector database for embeddings
- **BeautifulSoup** - Web scraping
- **Pydantic** - Data validation and serialization
- **Python 3.8+**

### Frontend

- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Mantine UI 6.0.21** - Component library
- **MobX** - State management
- **FontAwesome** - Icons

## 🚦 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Pinecone API key

### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   cp env.template .env
   # Edit .env with your API keys:
   # OPENAI_API_KEY=your_openai_key
   # PINECONE_API_KEY=your_pinecone_key
   # PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

5. **Initialize the system**

   ```bash
   python setup_pipeline.py
   ```

6. **Start the backend server**
   ```bash
   python run_server.py
   ```

The backend will be available at `http://localhost:8080`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, visit `http://localhost:8080/docs` for interactive API documentation.

### Key Endpoints

- `POST /ask` - Ask questions about MCP
- `POST /ingest` - Ingest and process documentation
- `GET /health` - Health check and system status

## 🎯 Usage

### 1. Initial Setup

1. Start the backend server
2. Run document ingestion to populate the knowledge base
3. Start the frontend application

### 2. Chat Interface

- Ask questions about Model Context Protocol
- View AI-generated responses with source references
- See processing times and relevance scores
- Clear chat history as needed

### 3. Knowledge Management

- Force recrawl of MCP documentation
- Update vector embeddings
- Monitor processing statistics
- View ingestion results

## 🔧 Configuration

### Backend Configuration (`backend/config/settings.py`)

- API keys and endpoints
- Vector store settings
- Document processing parameters
- Crawling configurations

### Frontend Configuration

- API endpoint URLs
- UI theme settings
- Component configurations

## 🧪 Testing

### Backend Tests

```bash
cd backend
python test_api.py
```

### Frontend Tests

```bash
cd frontend
npm run lint
npm run build
```

## 📁 Project Structure

```
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   └── models.py       # Pydantic models
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py     # Configuration
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── mcp_spider.py   # Web scraper
│   │   └── run_crawler.py  # Crawler runner
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── rag_pipeline.py
│   │   └── vector_store.py
│   ├── data/               # Processed documents
│   ├── requirements.txt    # Python dependencies
│   ├── env.template       # Environment template
│   └── run_server.py      # Server startup
└── frontend/              # React TypeScript frontend
    ├── src/
    │   ├── components/    # React components
    │   ├── stores/       # MobX stores
    │   ├── services/     # API services
    │   ├── types/        # TypeScript types
    │   └── App.tsx       # Main app component
    ├── public/           # Static assets
    ├── package.json      # Node dependencies
    └── vite.config.ts    # Vite configuration
```

## 🚀 Deployment

### Backend Deployment

1. Set up production environment variables
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure reverse proxy (e.g., Nginx)
4. Set up SSL certificates

### Frontend Deployment

1. Build the production bundle: `npm run build`
2. Serve the `dist` folder with a static file server
3. Configure API endpoint for production backend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Backend not starting**

   - Check if all environment variables are set
   - Verify Python dependencies are installed
   - Ensure virtual environment is activated

2. **Frontend not connecting to backend**

   - Verify backend is running on port 8080
   - Check CORS settings in backend
   - Confirm API endpoint URLs in frontend

3. **Vector store errors**
   - Verify Pinecone API key and environment
   - Check if index exists
   - Run the setup pipeline again

### Getting Help

- Check the API documentation at `http://localhost:8080/docs`
- Review the backend logs for error messages
- Ensure all dependencies are properly installed
- Verify environment variables are correctly set

## 🔗 Related Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Mantine UI Documentation](https://mantine.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Pinecone Documentation](https://docs.pinecone.io/)
