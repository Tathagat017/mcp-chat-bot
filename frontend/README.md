# MCP Chatbot Frontend

A React-based frontend for the Model Context Protocol (MCP) chatbot system.

## Features

- **Chat Interface**: Interactive chat interface to ask questions about MCP
- **Knowledge Ingestion**: Interface to crawl and process MCP documentation
- **Real-time Responses**: Live chat with processing indicators
- **Source References**: View source documents and relevance scores
- **Modern UI**: Built with Mantine UI components

## Tech Stack

- **React 18** with TypeScript
- **Vite** for build tooling
- **Mantine UI 6.0.21** for components
- **MobX** for state management
- **FontAwesome** for icons

## Getting Started

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Backend Connection

The frontend connects to the FastAPI backend running on `http://localhost:8080`. Make sure the backend server is running before using the application.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Endpoints

The frontend communicates with these backend endpoints:

- `POST /ask` - Ask questions about MCP
- `POST /ingest` - Ingest and process documentation
- `GET /health` - Health check

## Usage

### Chat Interface

1. Navigate to the Chat tab
2. Type your question about MCP in the input field
3. Press Send or hit Enter
4. View the response with optional source references

### Knowledge Ingestion

1. Navigate to the Knowledge Ingestion tab
2. Configure options:
   - Force Recrawl: Re-crawl documents even if they exist
   - Update Embeddings: Create and update vector embeddings
3. Click "Start Ingestion" to begin the process
4. Monitor progress and view results
