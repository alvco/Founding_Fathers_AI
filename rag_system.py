# rag_system.py
import chromadb
from sentence_transformers import SentenceTransformer
import os
import re
from typing import List

class RAGSystem:
    """Manages loading, chunking, embedding, and retrieving documents."""
    
    def __init__(self, corpora_path: str, collection_name: str = "founding_fathers"):
        print("Initializing RAG System...")
        # 1. Initialize embedding model and vector database client
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print(" -> SentenceTransformer model loaded successfully.")
        self.client = chromadb.Client()
        
        # Clear any old collection to start fresh
        if collection_name in [c.name for c in self.client.list_collections()]:
            self.client.delete_collection(name=collection_name)
        
        self.collection = self.client.create_collection(name=collection_name)
        
        # 2. Process and embed the documents
        self._build_knowledge_base(corpora_path)
        print("RAG System successfully built.")

# Inside RAGSystem class in rag_system.py

    def _load_and_chunk_document(self, filepath: str) -> List[str]:
        """Loads a document and splits it into chunks based on paragraphs."""
        print(f"  - Processing file: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        # Split the text by double newlines (common paragraph separator)
        chunks = text.split('\n\n')

        # Filter out very small or empty chunks
        min_chunk_size = 100 # Adjust this number if needed
        valid_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > min_chunk_size]

        print(f"  - Extracted {len(valid_chunks)} valid chunks from {filepath}.")
        return valid_chunks

    def _build_knowledge_base(self, corpora_path: str):
        """Loads all documents from the corpora path and embeds them."""
        doc_id_counter = 0
        for filename in os.listdir(corpora_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(corpora_path, filename)
                author_name = os.path.splitext(filename)[0]
                
                # Use our custom chunking logic
                chunks = self._load_and_chunk_document(filepath)
                
                if not chunks:
                    print(f"  - No valid chunks found for {filename}.")
                    continue

                # Embed and store the chunks with metadata
                embeddings = self.embedding_model.encode(chunks)
                metadata = [{"author": author_name} for _ in chunks]
                ids = [f"{author_name}_{doc_id_counter + i}" for i in range(len(chunks))]
                
                self.collection.add(
                    embeddings=embeddings,
                    documents=chunks,
                    metadatas=metadata,
                    ids=ids
                )
                doc_id_counter += len(chunks)

    def query(self, topic: str, author: str, top_k: int = 3) -> str:
        """Searches the knowledge base for relevant passages for a specific author."""
        query_embedding = self.embedding_model.encode([topic])
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where={"author": author} # Filter results by author
        )
        
        retrieved_chunks = results['documents'][0] if results['documents'] else []
        return "\n---\n".join(retrieved_chunks)