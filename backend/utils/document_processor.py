import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from config.settings import settings


class DocumentProcessor:
    """Process and chunk documents for embedding"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def load_documents(self, file_path: str) -> List[Dict[str, Any]]:
        """Load documents from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            return documents
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
            return []
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into chunks with overlap"""
        if chunk_size is None:
            chunk_size = settings.CHUNK_SIZE
        if overlap is None:
            overlap = settings.CHUNK_OVERLAP
            
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
                else:
                    # Look for word boundaries
                    word_end = text.rfind(' ', start, end)
                    if word_end > start + chunk_size // 2:
                        end = word_end
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
                
        return chunks
    
    def process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process documents into chunks with metadata"""
        processed_chunks = []
        
        for doc in documents:
            text = doc.get('text', '')
            if not text:
                continue
                
            # Clean the text
            text = self.clean_text(text)
            
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Create chunk objects with metadata
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    'id': f"{doc['url']}#chunk_{i}",
                    'text': chunk,
                    'url': doc['url'],
                    'title': doc.get('title', 'Untitled'),
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'timestamp': doc.get('timestamp', ''),
                    'word_count': len(chunk.split())
                }
                processed_chunks.append(chunk_data)
        
        return processed_chunks
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.!?]){2,}', r'\1', text)
        
        return text.strip()
    
    def create_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create embeddings for text chunks"""
        print(f"Creating embeddings for {len(chunks)} chunks...")
        
        # Extract texts for embedding
        texts = [chunk['text'] for chunk in chunks]
        
        # Create embeddings in batches
        batch_size = 100
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
            
            try:
                response = self.client.embeddings.create(
                    model=settings.OPENAI_EMBEDDING_MODEL,
                    input=batch_texts
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                print(f"Error creating embeddings for batch {i//batch_size + 1}: {e}")
                # Add zero embeddings as fallback
                embeddings.extend([[0.0] * 1536 for _ in batch_texts])
        
        # Combine chunks with embeddings
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding
        
        print(f"Created {len(embeddings)} embeddings")
        return chunks
    
    def save_processed_data(self, chunks: List[Dict[str, Any]], output_file: str):
        """Save processed chunks to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(chunks)} processed chunks to {output_file}")


def main():
    """Main function to process documents"""
    processor = DocumentProcessor()
    
    # Load documents
    documents = processor.load_documents(settings.DOCUMENTATION_FILE)
    if not documents:
        print("No documents found to process")
        return
    
    print(f"Loaded {len(documents)} documents")
    
    # Process documents into chunks
    chunks = processor.process_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    # Create embeddings
    chunks_with_embeddings = processor.create_embeddings(chunks)
    
    # Save processed data
    output_file = settings.DOCUMENTATION_FILE.replace('.json', '_processed.json')
    processor.save_processed_data(chunks_with_embeddings, output_file)


if __name__ == "__main__":
    main() 