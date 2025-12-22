"""
Tests for Pinecone Vector Store Implementation.

Requirements: 6.3
"""

import pytest
import asyncio
from typing import List
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Import the Pinecone store and related classes
from src.langchain.stores import PineconeStore
from src.langchain.vector_stores import Document, SearchResult, EmbeddingModel


class MockEmbeddingModel(EmbeddingModel):
    """Mock embedding model for testing."""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
    
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return mock embeddings."""
        return [[0.1] * self.dimension for _ in texts]
    
    async def embed_query(self, text: str) -> List[float]:
        """Return mock query embedding."""
        return [0.1] * self.dimension
    
    def get_dimension(self) -> int:
        """Return embedding dimension."""
        return self.dimension


class TestPineconeStore:
    """Test suite for Pinecone store implementation."""

    @pytest.fixture
    def mock_embedding_model(self):
        """Create a mock embedding model."""
        return MockEmbeddingModel(dimension=1536)

    @pytest.fixture
    def mock_pinecone_index(self):
        """Create a mock Pinecone index."""
        mock_index = MagicMock()
        mock_index.upsert = MagicMock()
        mock_index.query = MagicMock()
        mock_index.delete = MagicMock()
        return mock_index

    @pytest.fixture
    def store(self, mock_embedding_model, mock_pinecone_index):
        """Create a Pinecone store with mocked dependencies."""
        # Mock the pinecone import inside __init__
        mock_pinecone_module = MagicMock()
        mock_pinecone_module.init = MagicMock()
        mock_pinecone_module.list_indexes = MagicMock(return_value=['test-index'])
        mock_pinecone_module.Index = MagicMock(return_value=mock_pinecone_index)
        
        with patch.dict('sys.modules', {'pinecone': mock_pinecone_module}):
            store = PineconeStore(
                index_name="test-index",
                embedding_model=mock_embedding_model,
                api_key="test-api-key",
                environment="test-env",
                namespace="test-namespace"
            )
            store.index = mock_pinecone_index
            return store

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

    def test_init_requires_embedding_model(self):
        """Test that initialization requires an embedding model."""
        mock_pinecone_module = MagicMock()
        with patch.dict('sys.modules', {'pinecone': mock_pinecone_module}):
            with pytest.raises(ValueError, match="embedding_model is required"):
                PineconeStore(
                    index_name="test-index",
                    embedding_model=None,
                    api_key="test-key",
                    environment="test-env"
                )

    def test_init_requires_api_key(self, mock_embedding_model):
        """Test that initialization requires API key."""
        mock_pinecone_module = MagicMock()
        with patch.dict('sys.modules', {'pinecone': mock_pinecone_module}):
            with patch('os.getenv', return_value=None):
                with pytest.raises(ValueError, match="Pinecone API key required"):
                    PineconeStore(
                        index_name="test-index",
                        embedding_model=mock_embedding_model,
                        api_key=None,
                        environment="test-env"
                    )

    def test_init_requires_environment(self, mock_embedding_model):
        """Test that initialization requires environment."""
        mock_pinecone_module = MagicMock()
        with patch.dict('sys.modules', {'pinecone': mock_pinecone_module}):
            with patch('os.getenv', side_effect=lambda x: "test-key" if x == "PINECONE_API_KEY" else None):
                with pytest.raises(ValueError, match="Pinecone environment required"):
                    PineconeStore(
                        index_name="test-index",
                        embedding_model=mock_embedding_model,
                        api_key=None,
                        environment=None
                    )

    def test_init_creates_index_if_not_exists(self, mock_embedding_model):
        """Test that initialization creates index if it doesn't exist."""
        mock_pinecone_module = MagicMock()
        mock_pinecone_module.init = MagicMock()
        mock_pinecone_module.list_indexes = MagicMock(return_value=[])
        mock_pinecone_module.create_index = MagicMock()
        mock_pinecone_module.Index = MagicMock()
        
        with patch.dict('sys.modules', {'pinecone': mock_pinecone_module}):
            store = PineconeStore(
                index_name="new-index",
                embedding_model=mock_embedding_model,
                api_key="test-key",
                environment="test-env"
            )
            
            # Verify create_index was called
            mock_pinecone_module.create_index.assert_called_once()
            call_args = mock_pinecone_module.create_index.call_args
            assert call_args[1]['name'] == "new-index"
            assert call_args[1]['dimension'] == 1536
            assert call_args[1]['metric'] == "cosine"

    @pytest.mark.asyncio
    async def test_add_documents(self, store, sample_documents):
        """Test adding documents to the store."""
        ids = await store.add_documents(sample_documents)
        
        assert len(ids) == 3
        assert all(isinstance(id, str) for id in ids)
        
        # Verify upsert was called
        store.index.upsert.assert_called()

    @pytest.mark.asyncio
    async def test_add_documents_empty_raises(self, store):
        """Test that adding empty documents raises ValueError."""
        with pytest.raises(ValueError, match="documents list cannot be empty"):
            await store.add_documents([])

    @pytest.mark.asyncio
    async def test_add_documents_batching(self, store, mock_embedding_model):
        """Test that large document sets are batched correctly."""
        # Create 250 documents (should be split into 3 batches: 100, 100, 50)
        large_doc_set = [
            Document(content=f"Document {i}", metadata={"index": i})
            for i in range(250)
        ]
        
        await store.add_documents(large_doc_set)
        
        # Verify upsert was called 3 times
        assert store.index.upsert.call_count == 3

    @pytest.mark.asyncio
    async def test_add_documents_preserves_custom_ids(self, store):
        """Test that custom document IDs are preserved."""
        doc = Document(
            content="Test content",
            metadata={"test": True},
            id="custom-id-123"
        )
        
        ids = await store.add_documents([doc])
        assert ids[0] == "custom-id-123"

    @pytest.mark.asyncio
    async def test_similarity_search(self, store, sample_documents):
        """Test similarity search returns relevant results."""
        # Mock the query response
        store.index.query.return_value = MagicMock(
            matches=[
                MagicMock(
                    id="doc1",
                    score=0.95,
                    metadata={"content": "Python is great", "category": "programming"}
                ),
                MagicMock(
                    id="doc2",
                    score=0.85,
                    metadata={"content": "JavaScript is useful", "category": "programming"}
                )
            ]
        )
        
        results = await store.similarity_search("programming language", k=2)
        
        assert len(results) == 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert all(0 <= r.score <= 1 for r in results)
        assert results[0].score == 0.95
        assert results[1].score == 0.85

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
    async def test_similarity_search_with_filter(self, store):
        """Test similarity search with metadata filter."""
        filter_dict = {"category": "programming"}
        
        store.index.query.return_value = MagicMock(matches=[])
        
        await store.similarity_search("test", k=5, filter=filter_dict)
        
        # Verify filter was passed to query
        call_args = store.index.query.call_args
        assert call_args[1]['filter'] == filter_dict

    @pytest.mark.asyncio
    async def test_hybrid_search_fallback(self, store):
        """Test hybrid search falls back to similarity search with warning."""
        store.index.query.return_value = MagicMock(matches=[])
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            results = await store.hybrid_search("programming", k=2, alpha=0.5)
            
            # Check warning was issued
            assert len(w) > 0
            assert any("hybrid search" in str(warning.message).lower() for warning in w)

    @pytest.mark.asyncio
    async def test_hybrid_search_invalid_alpha_raises(self, store):
        """Test that alpha outside [0, 1] raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be in"):
            await store.hybrid_search("test", alpha=1.5)

    @pytest.mark.asyncio
    async def test_delete_documents(self, store):
        """Test deleting documents by ID."""
        ids = ["doc1", "doc2", "doc3"]
        
        await store.delete(ids)
        
        # Verify delete was called
        store.index.delete.assert_called_once()
        call_args = store.index.delete.call_args
        assert call_args[1]['ids'] == ids
        assert call_args[1]['namespace'] == "test-namespace"

    @pytest.mark.asyncio
    async def test_delete_empty_raises(self, store):
        """Test that deleting empty list raises ValueError."""
        with pytest.raises(ValueError, match="ids list cannot be empty"):
            await store.delete([])

    @pytest.mark.asyncio
    async def test_delete_batching(self, store):
        """Test that large delete operations are batched correctly."""
        # Create 2500 IDs (should be split into 3 batches: 1000, 1000, 500)
        large_id_set = [f"doc{i}" for i in range(2500)]
        
        await store.delete(large_id_set)
        
        # Verify delete was called 3 times
        assert store.index.delete.call_count == 3

    @pytest.mark.asyncio
    async def test_clear(self, store):
        """Test clearing all documents from namespace."""
        await store.clear()
        
        # Verify delete was called with delete_all=True
        store.index.delete.assert_called_once()
        call_args = store.index.delete.call_args
        assert call_args[1]['delete_all'] is True
        assert call_args[1]['namespace'] == "test-namespace"

    def test_get_embedding_dimension(self, store):
        """Test getting embedding dimension."""
        dim = store.get_embedding_dimension()
        assert dim == 1536

    @pytest.mark.asyncio
    async def test_metadata_stored_correctly(self, store):
        """Test that metadata is stored correctly in Pinecone format."""
        doc = Document(
            content="Test content",
            metadata={"category": "test", "score": 95}
        )
        
        await store.add_documents([doc])
        
        # Verify upsert was called with correct metadata format
        call_args = store.index.upsert.call_args
        vectors = call_args[1]['vectors']
        
        assert len(vectors) == 1
        assert vectors[0]['metadata']['content'] == "Test content"
        assert vectors[0]['metadata']['category'] == "test"
        assert vectors[0]['metadata']['score'] == 95

    def test_import_error_without_pinecone(self, mock_embedding_model):
        """Test that ImportError is raised if pinecone-client is not installed."""
        with patch('builtins.__import__', side_effect=ImportError):
            with pytest.raises(ImportError, match="pinecone-client is required"):
                PineconeStore(
                    index_name="test-index",
                    embedding_model=mock_embedding_model,
                    api_key="test-key",
                    environment="test-env"
                )
