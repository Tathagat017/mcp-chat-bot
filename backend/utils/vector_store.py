import json
import time
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from config.settings import settings


class PineconeVectorStore:
    """Pinecone vector store for document embeddings"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.index = None
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def create_index(self, dimension: int = 1536, metric: str = "cosine"):
        """Create Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            if self.index_name in self.pc.list_indexes().names():
                print(f"Index '{self.index_name}' already exists")
                self.index = self.pc.Index(self.index_name)
                return
            
            # Create new index
            print(f"Creating index '{self.index_name}'...")
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            
            # Wait for index to be ready
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)
            
            self.index = self.pc.Index(self.index_name)
            print(f"Index '{self.index_name}' created successfully")
            
        except Exception as e:
            print(f"Error creating index: {e}")
            raise
    
    def connect_to_index(self):
        """Connect to existing index"""
        try:
            if self.index_name not in self.pc.list_indexes().names():
                raise ValueError(f"Index '{self.index_name}' does not exist")
            
            self.index = self.pc.Index(self.index_name)
            print(f"Connected to index '{self.index_name}'")
            
        except Exception as e:
            print(f"Error connecting to index: {e}")
            raise
    
    def upsert_documents(self, chunks: List[Dict[str, Any]], batch_size: int = 100):
        """Upsert document chunks to Pinecone"""
        if not self.index:
            self.connect_to_index()
        
        print(f"Upserting {len(chunks)} chunks to Pinecone...")
        
        # Prepare vectors for upsert
        vectors = []
        for chunk in chunks:
            vector = {
                'id': chunk['id'],
                'values': chunk['embedding'],
                'metadata': {
                    'text': chunk['text'][:1000],  # Truncate for metadata limits
                    'url': chunk['url'],
                    'title': chunk['title'],
                    'chunk_index': chunk['chunk_index'],
                    'total_chunks': chunk['total_chunks'],
                    'word_count': chunk['word_count']
                }
            }
            vectors.append(vector)
        
        # Upsert in batches
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            try:
                self.index.upsert(vectors=batch)
                print(f"Upserted batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size}")
            except Exception as e:
                print(f"Error upserting batch {i//batch_size + 1}: {e}")
        
        print(f"Successfully upserted {len(vectors)} vectors")
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not self.index:
            self.connect_to_index()
        
        if top_k is None:
            top_k = settings.TOP_K_RESULTS
        
        try:
            # Create query embedding
            response = self.openai_client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=query
            )
            query_embedding = response.data[0].embedding
            
            # Search in Pinecone
            search_response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            results = []
            for match in search_response['matches']:
                result = {
                    'id': match['id'],
                    'score': match['score'],
                    'text': match['metadata']['text'],
                    'url': match['metadata']['url'],
                    'title': match['metadata']['title'],
                    'chunk_index': match['metadata']['chunk_index'],
                    'total_chunks': match['metadata']['total_chunks'],
                    'word_count': match['metadata']['word_count']
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def delete_index(self):
        """Delete the index"""
        try:
            if self.index_name in self.pc.list_indexes().names():
                self.pc.delete_index(self.index_name)
                print(f"Index '{self.index_name}' deleted")
            else:
                print(f"Index '{self.index_name}' does not exist")
        except Exception as e:
            print(f"Error deleting index: {e}")
    
    def get_index_stats(self):
        """Get index statistics"""
        if not self.index:
            self.connect_to_index()
        
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            print(f"Error getting index stats: {e}")
            return None


def main():
    """Main function to initialize and populate vector store"""
    vector_store = PineconeVectorStore()
    
    # Create index
    vector_store.create_index()
    
    # Load processed documents
    processed_file = settings.DOCUMENTATION_FILE.replace('.json', '_processed.json')
    try:
        with open(processed_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f"Loaded {len(chunks)} processed chunks")
        
        # Upsert to Pinecone
        vector_store.upsert_documents(chunks)
        
        # Show stats
        stats = vector_store.get_index_stats()
        if stats:
            print(f"Index stats: {stats}")
        
    except FileNotFoundError:
        print(f"Processed file not found: {processed_file}")
        print("Please run document processing first")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 