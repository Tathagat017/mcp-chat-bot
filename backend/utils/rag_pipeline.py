from typing import List, Dict, Any, Optional
from openai import OpenAI
from utils.vector_store import PineconeVectorStore
from config.settings import settings


class RAGPipeline:
    """RAG (Retrieval-Augmented Generation) pipeline for MCP Q&A"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_store = PineconeVectorStore()
        
    def retrieve_context(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector store"""
        if top_k is None:
            top_k = settings.TOP_K_RESULTS
        
        results = self.vector_store.search(query, top_k=top_k)
        return results
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string"""
        if not retrieved_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_part = f"""
Context {i} (Score: {doc['score']:.3f}):
Title: {doc['title']}
URL: {doc['url']}
Content: {doc['text']}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using OpenAI with retrieved context"""
        
        system_prompt = """You are an expert assistant specializing in Model Context Protocol (MCP). 
You help developers understand MCP concepts, implement MCP solutions, and troubleshoot MCP-related issues.

Your responses should be:
1. Accurate and based on the provided context
2. Developer-focused with practical examples when relevant
3. Clear and well-structured
4. Honest about limitations - if you don't know something, say so

When answering questions:
- Use the provided context as your primary source of information
- If the context doesn't contain enough information, acknowledge this
- Provide code examples when relevant and available in the context
- Reference specific parts of the documentation when helpful
- Suggest next steps or related topics when appropriate"""

        user_prompt = f"""Based on the following context about Model Context Protocol (MCP), please answer the user's question.

Context:
{context}

Question: {query}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to fully answer the question, please say so and provide what information you can."""

        try:
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I apologize, but I encountered an error while generating the answer. Please try again."
    
    def ask(self, query: str, include_sources: bool = True) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve context and generate answer"""
        
        # Retrieve relevant context
        retrieved_docs = self.retrieve_context(query)
        
        # Format context
        context = self.format_context(retrieved_docs)
        
        # Generate answer
        answer = self.generate_answer(query, context)
        
        # Prepare response
        response = {
            "query": query,
            "answer": answer,
            "context_used": len(retrieved_docs) > 0
        }
        
        if include_sources:
            sources = []
            for doc in retrieved_docs:
                source = {
                    "title": doc['title'],
                    "url": doc['url'],
                    "relevance_score": doc['score'],
                    "snippet": doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
                }
                sources.append(source)
            response["sources"] = sources
        
        return response
    
    def get_similar_questions(self, query: str, threshold: float = 0.8) -> List[str]:
        """Get similar questions based on context retrieval"""
        retrieved_docs = self.retrieve_context(query, top_k=10)
        
        # Extract potential questions from high-scoring documents
        similar_questions = []
        for doc in retrieved_docs:
            if doc['score'] > threshold:
                # Simple heuristic to extract question-like sentences
                text = doc['text']
                sentences = text.split('.')
                for sentence in sentences:
                    sentence = sentence.strip()
                    if any(sentence.lower().startswith(q) for q in ['how', 'what', 'when', 'where', 'why', 'which']):
                        if len(sentence) > 10 and len(sentence) < 100:
                            similar_questions.append(sentence + '?')
        
        return list(set(similar_questions))[:5]  # Return top 5 unique questions


def main():
    """Test the RAG pipeline"""
    rag = RAGPipeline()
    
    # Test questions
    test_questions = [
        "What is Model Context Protocol?",
        "How does MCP work?",
        "What are the benefits of using MCP?",
        "How do I implement MCP in my application?",
        "What are MCP servers and clients?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"Question: {question}")
        print('='*50)
        
        response = rag.ask(question)
        print(f"Answer: {response['answer']}")
        
        if response['sources']:
            print(f"\nSources ({len(response['sources'])}):")
            for i, source in enumerate(response['sources'], 1):
                print(f"{i}. {source['title']} (Score: {source['relevance_score']:.3f})")
                print(f"   {source['url']}")
                print(f"   {source['snippet']}")
                print()


if __name__ == "__main__":
    main() 