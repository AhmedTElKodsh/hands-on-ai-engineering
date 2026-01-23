"""
Vector Store Implementation for AITEA.

Provides a simple, production-ready wrapper around ChromaDB for document storage
and semantic search. Designed for educational use in RAG systems.

Requirements: Chapter 14 (Vector Store), Chapter 17 (First RAG System)
"""

from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from pathlib import Path


class VectorStore:
    """
    Simple vector store wrapper around ChromaDB.
    
    Provides easy-to-use methods for storing documents with metadata
    and performing semantic search. Uses OpenAI embeddings by default.
    
    Example:
        >>> store = VectorStore(path="./my_db", collection_name="docs")
        >>> store.add_document("doc1", "Python is great", {"source": "tutorial.txt"})
        >>> results = store.search("programming language", limit=1)
        >>> print(results[0])
        'Python is great'
    """
    
    def __init__(
        self,
        path: str = "./chroma_db",
        collection_name: str = "default_collection",
        embedding_model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize the vector store.
        
        Args:
            path: Directory path for persistent storage
            collection_name: Name of the collection to use
            embedding_model: OpenAI embedding model name
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if None)
        
        Raises:
            ValueError: If API key is not provided and not in environment
        """
        self.path = Path(path)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Create directory if it doesn't exist
        self.path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=str(self.path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Set up OpenAI embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.api_key,
            model_name=self.embedding_model
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "AITEA vector store collection"}
        )
    
    def add_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a single document to the vector store.
        
        Args:
            doc_id: Unique identifier for the document
            text: Document text content
            metadata: Optional metadata dictionary (e.g., {"source": "file.txt"})
        
        Example:
            >>> store.add_document(
            ...     doc_id="1",
            ...     text="RAG systems combine retrieval and generation",
            ...     metadata={"source": "chapter17.md", "page": 1}
            ... )
        """
        if metadata is None:
            metadata = {}
        
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata]
        )
    
    def add_documents(
        self,
        doc_ids: List[str],
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add multiple documents to the vector store in batch.
        
        More efficient than calling add_document() multiple times.
        
        Args:
            doc_ids: List of unique document identifiers
            texts: List of document text contents
            metadatas: Optional list of metadata dictionaries
        
        Raises:
            ValueError: If lists have different lengths
        
        Example:
            >>> store.add_documents(
            ...     doc_ids=["1", "2"],
            ...     texts=["First doc", "Second doc"],
            ...     metadatas=[{"source": "a.txt"}, {"source": "b.txt"}]
            ... )
        """
        if len(doc_ids) != len(texts):
            raise ValueError("doc_ids and texts must have same length")
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        elif len(metadatas) != len(texts):
            raise ValueError("metadatas must have same length as texts")
        
        self.collection.add(
            ids=doc_ids,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(
        self,
        query: str,
        limit: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Search for similar documents using semantic similarity.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            where: Optional metadata filter (e.g., {"source": "file.txt"})
        
        Returns:
            List of document texts, ordered by relevance (most similar first)
        
        Example:
            >>> results = store.search("What is RAG?", limit=3)
            >>> for doc in results:
            ...     print(doc)
            'RAG stands for Retrieval-Augmented Generation...'
            'RAG systems combine retrieval and generation...'
            'The RAG pattern has three steps...'
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where
        )
        
        # Extract documents from results
        # ChromaDB returns nested structure: {'documents': [[doc1, doc2, ...]]}
        if results and results['documents'] and len(results['documents']) > 0:
            return results['documents'][0]
        return []
    
    def search_with_metadata(
        self,
        query: str,
        limit: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Search for similar documents and return both text and metadata.
        
        This is essential for citation tracking in RAG systems.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            where: Optional metadata filter
        
        Returns:
            List of (document_text, metadata_dict) tuples
        
        Example:
            >>> results = store.search_with_metadata("RAG", limit=2)
            >>> for doc, meta in results:
            ...     print(f"Text: {doc}")
            ...     print(f"Source: {meta['source']}")
            Text: RAG stands for...
            Source: chapter17.md
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where,
            include=['documents', 'metadatas']
        )
        
        # Combine documents and metadatas into tuples
        if (results and 
            results['documents'] and 
            results['metadatas'] and
            len(results['documents']) > 0 and
            len(results['metadatas']) > 0):
            
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            return list(zip(documents, metadatas))
        
        return []
    
    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for similar documents with relevance scores.
        
        Useful for debugging and understanding retrieval quality.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            where: Optional metadata filter
        
        Returns:
            List of (document_text, distance_score, metadata_dict) tuples
            Lower distance = more similar
        
        Example:
            >>> results = store.search_with_scores("RAG", limit=2)
            >>> for doc, score, meta in results:
            ...     print(f"Score: {score:.3f} - {doc[:50]}...")
            Score: 0.234 - RAG stands for Retrieval-Augmented...
            Score: 0.456 - RAG systems combine retrieval...
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where,
            include=['documents', 'metadatas', 'distances']
        )
        
        if (results and 
            results['documents'] and 
            results['metadatas'] and
            results['distances'] and
            len(results['documents']) > 0):
            
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            return list(zip(documents, distances, metadatas))
        
        return []
    
    def get_document(self, doc_id: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Retrieve a specific document by ID.
        
        Args:
            doc_id: Document identifier
        
        Returns:
            Tuple of (document_text, metadata_dict) or None if not found
        
        Example:
            >>> doc, meta = store.get_document("doc1")
            >>> print(doc)
            'RAG stands for...'
        """
        results = self.collection.get(
            ids=[doc_id],
            include=['documents', 'metadatas']
        )
        
        if (results and 
            results['documents'] and 
            results['metadatas'] and
            len(results['documents']) > 0):
            return (results['documents'][0], results['metadatas'][0])
        
        return None
    
    def delete_document(self, doc_id: str) -> None:
        """
        Delete a document by ID.
        
        Args:
            doc_id: Document identifier to delete
        
        Example:
            >>> store.delete_document("doc1")
        """
        self.collection.delete(ids=[doc_id])
    
    def delete_documents(self, doc_ids: List[str]) -> None:
        """
        Delete multiple documents by ID.
        
        Args:
            doc_ids: List of document identifiers to delete
        
        Example:
            >>> store.delete_documents(["doc1", "doc2", "doc3"])
        """
        self.collection.delete(ids=doc_ids)
    
    def clear(self) -> None:
        """
        Delete all documents from the collection.
        
        Warning: This operation cannot be undone!
        
        Example:
            >>> store.clear()  # Removes all documents
        """
        # Delete and recreate collection
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "AITEA vector store collection"}
        )
    
    def count(self) -> int:
        """
        Get the number of documents in the collection.
        
        Returns:
            Number of documents stored
        
        Example:
            >>> print(f"Store contains {store.count()} documents")
            Store contains 42 documents
        """
        return self.collection.count()
    
    def __repr__(self) -> str:
        """String representation of the vector store."""
        return (
            f"VectorStore(path='{self.path}', "
            f"collection='{self.collection_name}', "
            f"documents={self.count()})"
        )


# Convenience function for quick setup
def create_vector_store(
    path: str = "./chroma_db",
    collection_name: str = "default_collection"
) -> VectorStore:
    """
    Create a vector store with default settings.
    
    Args:
        path: Directory path for persistent storage
        collection_name: Name of the collection
    
    Returns:
        Configured VectorStore instance
    
    Example:
        >>> store = create_vector_store("./my_rag_db", "documents")
        >>> store.add_document("1", "Hello world", {"source": "test"})
    """
    return VectorStore(path=path, collection_name=collection_name)
