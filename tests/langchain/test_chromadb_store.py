"""
Tests for ChromaDB Vector Store Implementation.

Requirements: 6.3
"""

import pytest
import asyncio
from typing import List

# Import the ChromaDB store and related classes
from src.langchain.stores import ChromaDBStore
from src.langchain.vector_stores import Document, SearchResult


class TestChromaDBStore:
    """Test suite for ChromaDB store implementation."""

    @pytest.fixture
    def store(self):
        """Create a fresh in-memory ChromaDB store for each test."""
        return ChromaDBStore(
            collection_name="test_collection",
            embedding_model=None,  # Use ChromaDB's default embedding
            persist_directory=None  # In-memory
        )

    @pytest.fixture
    def sample_documents(self) -> List[Document]:
        """Sample documents for testing."""
        return [
            Document(
                content="Python is a programming language",
                metadata={"category": "programming", "language": "python"}
            ),
            Document(
                content="JavaScript is used for web development",
                metadata={"category": "programming", "language": "javascript"}
            ),
            Document(
                content="Machine learning uses algorithms to learn from data",
                metadata={"category": "ai", "topic": "ml"}
            ),
        ]

    @pytest.mark.asyncio
    async def test_add_documents(self, store, sample_documents):
        """Test adding documents to the store."""
        ids = await store.add_documents(sample_documents)
        
        assert len(ids) == 3
        assert all(isinstance(id, str) for id in ids)

    @pytest.mark.asyncio
    async def test_add_documents_empty_raises(self, store):
        """Test that adding empty documents raises ValueError."""
        with pytest.raises(ValueError, match="documents list cannot be empty"):
            await store.add_documents([])

    @pytest.mark.asyncio
    async def test_similarity_search(self, store, sample_documents):
        """Test similarity search returns relevant results."""
        await store.add_documents(sample_documents)
        
        results = await store.similarity_search("programming language", k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert all(0 <= r.score <= 1 for r in results)

    @pytest.mark.asyncio
    async def test_similarity_search_empty_query_raises(self, store):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="query cannot be empty"):
            await store.similarity_search("")

    @pytest.mark.asyncio
    async def test_similarity_search_invalid_k_raises(self, store):
        """Test that k <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="k must be positive"):
            await store.similarity_search("test", k=0)

    @pytest.mark.asyncio
    async def test_delete_documents(self, store, sample_documents):
        """Test deleting documents by ID."""
        ids = await store.add_documents(sample_documents)
        
        # Delete first document
        await store.delete([ids[0]])
        
        # Search should not return deleted document
        results = await store.similarity_search("Python programming", k=10)
        result_ids = [r.document.id for r in results]
        assert ids[0] not in result_ids

    @pytest.mark.asyncio
    async def test_delete_empty_raises(self, store):
        """Test that deleting empty list raises ValueError."""
        with pytest.raises(ValueError, match="ids list cannot be empty"):
            await store.delete([])

    @pytest.mark.asyncio
    async def test_clear(self, store, sample_documents):
        """Test clearing all documents."""
        await store.add_documents(sample_documents)
        await store.clear()
        
        # Search should return no results
        results = await store.similarity_search("programming", k=10)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_hybrid_search_fallback(self, store, sample_documents):
        """Test hybrid search falls back to similarity search."""
        await store.add_documents(sample_documents)
        
        # Should work but emit warning
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            results = await store.hybrid_search("programming", k=2, alpha=0.5)
            
            assert len(results) <= 2
            # Check warning was issued
            assert any("hybrid search" in str(warning.message).lower() for warning in w)

    @pytest.mark.asyncio
    async def test_hybrid_search_invalid_alpha_raises(self, store):
        """Test that alpha outside [0, 1] raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be in"):
            await store.hybrid_search("test", alpha=1.5)

    def test_get_embedding_dimension(self, store):
        """Test getting embedding dimension."""
        dim = store.get_embedding_dimension()
        assert dim == 384  # ChromaDB default (all-MiniLM-L6-v2)

    @pytest.mark.asyncio
    async def test_document_with_custom_id(self, store):
        """Test adding document with custom ID."""
        doc = Document(
            content="Test content",
            metadata={"test": True},
            id="custom-id-123"
        )
        
        ids = await store.add_documents([doc])
        assert ids[0] == "custom-id-123"

    @pytest.mark.asyncio
    async def test_metadata_filter(self, store, sample_documents):
        """Test similarity search with metadata filter."""
        await store.add_documents(sample_documents)
        
        # Filter by category
        results = await store.similarity_search(
            "programming",
            k=10,
            filter={"category": "programming"}
        )
        
        # All results should have category=programming
        for r in results:
            assert r.document.metadata.get("category") == "programming"
