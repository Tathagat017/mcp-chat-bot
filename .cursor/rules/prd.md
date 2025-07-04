---
description:
globs:
alwaysApply: true
---

# �� Product Requirements Document (PRD)

## �� Project Title

**MCP Q&A Chatbot**

---

## �� Objective

Build an intelligent, developer-focused Q&A chatbot that answers questions about Model Context Protocol (MCP). The chatbot will understand MCP terminology, explain concepts clearly, provide code examples, and help developers troubleshoot or implement MCP-based solutions.

---

## �� Target Users

- Developers learning about or working with Model Context Protocol (MCP)
- Engineering teams evaluating MCP for integration
- Technical documentation readers who want an interactive interface

---

## �� Functional Requirements

1. **Question Answering**

   - Accept natural language questions related to MCP
   - Provide accurate, context-rich answers using documentation and code samples

2. **Documentation Crawler**

   - Crawl and extract all text from: `https://www.anthropic.com/news/model-context-protocol`
   - Follow internal links within that domain
   - Store cleaned content in structured format (JSON)

3. **RAG Pipeline**

   - Embed the documentation text
   - Retrieve top relevant chunks based on semantic similarity to the question
   - Combine with question and feed into LLM prompt
   - Return the answer

4. **FastAPI Backend**

   - Endpoint: `/ask` to accept a question and return an answer
   - (Optional) Endpoint: `/ingest` to trigger re-crawling and vector store update

5. **Vector Store**

   - Store text embeddings for semantic search
   - Use Pinecone DB

6. **Local Hosting**

   - Hosted on `localhost` for MVP/demo purposes
   - No cloud deployment at this stage

---

## �� Tech Stack & Tools

### Backend

- **Framework**: FastAPI

### Crawling

- **Library**: Scrapy (for structured, recursive, scalable crawling)
- **Parser**: BeautifulSoup (if required)

### RAG Components

- **Embedding Model**: `text-embedding-ada-002` (via OpenAI)
- **Vector DB**: Pinecone
- **Retriever**: Semantic similarity search using top-k (e.g., top 3-5 matches)
- **LLM**: OpenAI GPT-3.5 Turbo (via API)

### Data Format

- Extracted text saved as: `List[Dict]`, e.g., `{ "url": ..., "text": ... }`

---

## �� Deliverables

- Python backend (FastAPI)
- Crawler script (Scrapy-based)
- Document processing & embedding script
- Pinecone indexer & retriever
- RAG-based answer generator
- `.env` file template for keys
- JSON documentation dump

---

## �� Timeline (Suggested)

| Week | Task                                         |
| ---- | -------------------------------------------- |
| 1    | Build crawler and scrape MCP docs            |
| 2    | Implement embedding + vector DB ingestion    |
| 3    | Implement RAG pipeline and FastAPI endpoints |
| 4    | Testing and refinement                       |

---

## �� Required Secrets (in .env)

```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=...
PINECONE_INDEX_NAME=mcp-docs
```

---

## ✅ Success Criteria

- Chatbot answers 80%+ of MCP questions accurately
- Response latency < 3 seconds on average
- Clean, structured documentation ingestion from Anthropic site
- MVP ready to demo on local environment

---

## ❓Future Enhancements (Post-MVP)

- Web-based frontend
- Authentication (API key or login)
- LangChain pipeline abstraction
- Feedback loop for answer rating
- Offline mode with local vector DB (FAISS/Chroma)

Frontend :

A simple chatbot UI with ability to chat created in vite React , Typescript , Mantine UI
