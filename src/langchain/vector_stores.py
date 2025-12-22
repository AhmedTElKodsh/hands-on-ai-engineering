"""
Vector Store Abstraction for AITEA LangChain Integration.

This module provides abstract interfaces and concrete implementations for vector stores
used in RAG (Retrieval-Augmented Generation) pipelines. Supports multiple backends
including ChromaDB, Pinecone, and Qdrant.

Requirements: 6.3
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EmbeddingProvider(str, Enum):
    """Supported embedding model providers."""
    OPENAI = "openai"
    COHERE = "cohere"
    BGE = "bge"


@dataclass
class Document:
    """Document with content and metadata for vector storage."""
    content: str
    metadata: Dict[str, Any]
    id: Optional[str] = None

    def __post_init__(self):
        """Ensure metadata is a dictionary."""
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary")


@dataclass
class SearchResult:
    """Result from vector similarity search."""
    document: Document
    score: float
    
    def __post_init__(self):
        """Validate score is between 0 and 1."""
        if not 0 <= self.score <= 1:
            raise ValueError(f"Score must be between 0 and 1, got {self.score}")


class VectorStore(ABC):
    """
    Abstract base class for vector store implementations.
    
    Provides a unified interface for storing documents as embeddings and
    performing similarity searches across different vector database backends.
    """

    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            List of document IDs assigned by the store
            
        Raises:
            ValueError: If documents list is empty or contains invalid documents
        """
        pass

    @abstractmethod
    async def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform similarity search using dense embeddings.
        
        Args:
            query: Query text to search for
            k: Number of results to return (default: 4)
            filter: Optional metadata filter
            
        Returns:
            List of search results ordered by relevance (highest score first)
            
        Raises:
            ValueError: If k <= 0 or query is empty
        """
        pass

    @abstractmethod
    async def hybrid_search(
        self, 
        query: str, 
        k: int = 4,
        alpha: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining dense and sparse retrieval.
        
        Args:
            query: Query text to search for
            k: Number of results to return (default: 4)
            alpha: Weight for dense vs sparse (0=sparse only, 1=dense only, default: 0.5)
            filter: Optional metadata filter
            
        Returns:
            List of search results ordered by combined relevance score
            
        Raises:
            ValueError: If k <= 0, query is empty, or alpha not in [0, 1]
        """
        pass

    @abstractmethod
    async def delete(self, ids: List[str]) -> None:
        """
        Delete documents by ID.
        
        Args:
            ids: List of document IDs to delete
            
        Raises:
            ValueError: If ids list is empty
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """
        Clear all documents from the store.
        
        This operation cannot be undone.
        """
        pass

    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings used by this store.
        
        Returns:
            Embedding dimension (e.g., 1536 for OpenAI text-embedding-3-small)
        """
        pass


class EmbeddingModel(ABC):
    """
    Abstract base class for embedding models.
    
    Provides a unified interface for generating embeddings from text
    across different embedding providers.
    """

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            ValueError: If texts list is empty
        """
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
            
        Raises:
            ValueError: If text is empty
        """
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.
        
        Returns:
            Embedding dimension
        """
        pass


def create_embedding_model(
    provider: EmbeddingProvider,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None
) -> EmbeddingModel:
    """
    Factory function to create embedding models.
    
    Args:
        provider: Embedding provider to use
        model_name: Optional specific model name (uses provider default if None)
        api_key: Optional API key (uses environment variable if None)
        
    Returns:
        Configured embedding model instance
        
    Raises:
        ValueError: If provider is not supported
        ImportError: If required provider library is not installed
    """
    if provider == EmbeddingProvider.OPENAI:
        from .embeddings.openai import OpenAIEmbedding
        return OpenAIEmbedding(model_name=model_name, api_key=api_key)
    elif provider == EmbeddingProvider.COHERE:
        from .embeddings.cohere import CohereEmbedding
        return CohereEmbedding(model_name=model_name, api_key=api_key)
    elif provider == EmbeddingProvider.BGE:
        from .embeddings.bge import BGEEmbedding
        return BGEEmbedding(model_name=model_name)
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
