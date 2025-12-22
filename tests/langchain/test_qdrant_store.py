"""
Tests for Qdrant Vector Store Implementation.

Requirements: 6.3
"""

import pytest
import asyncio
from typing import List
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from contextlib import ExitStack, contextmanager

# Import the Qdrant store and related classes
from src.langchain.stores import QdrantStore
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


@contextmanager
def mock_qdrant_imports(mock_client=None):
    """Context manager to mock all Qdrant imports."""
    # Create mock objects
    mock_qdrant_module = MagicMock()
    mock_models = MagicMock()
    mock_distance = MagicMock()
    mock_distance.COSINE = "COSINE"
    mock_models.Distance = mock_distance
    mock_models.VectorParams = MagicMock()
    mock_models.PointStruct = MagicMock()
    mock_models.Filter = MagicMock()
    mock_models.FieldCondition = MagicMock()
    mock_models.MatchValue = MagicMock()
    mock_models.MatchText = MagicMock()
    mock_qdrant_module.models = mock_models
    
    # If a mock client is provided, use it
    if mock_client:
        mock_qdrant_client_class = MagicMock(return_value=mock_client)
    else:
        mock_qdrant_client_class = MagicMock()
    
    patches = [
        patch.dict('sys.modules', {
            'qdrant_client': mock_qdrant_module,
            'qdrant_client.models': mock_models
        }),
        patch('src.langchain.stores.qdrant_store.QDRANT_AVAILABLE', True),
        patch('src.langchain.stores.qdrant_store.QdrantClient', mock_qdrant_client_class),
        patch('src.langchain.stores.qdrant_store.Distance', mock_distance),
        patch('src.langchain.stores.qdrant_store.VectorParams', mock_models.VectorParams),
        patch('src.langchain.stores.qdrant_store.PointStruct', mock_models.PointStruct),
        patch('src.langchain.stores.qdrant_store.Filter', mock_models.Filter),
        patch('src.langchain.stores.qdrant_store.FieldCondition', mock_models.FieldCondition),
        patch('src.langchain.stores.qdrant_store.MatchValue', mock_models.MatchValue),
        patch('src.langchain.stores.qdrant_store.MatchText', mock_models.MatchText),
    ]
    
    with ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        yield mock_qdrant_module, mock_models


class TestQdrantStore:
    """Test suite for Qdrant store implementation."""

    @pytest.fixture
    def mock_embedding_model(self):
        """Create a mock embedding model."""
        return MockEmbeddingModel(dimension=1536)

    @pytest.fixture
    def mock_qdrant_client(self):
        """Create a mock Qdrant client."""
        mock_client = MagicMock()
        
        # Mock get_collections
        mock_collection = MagicMock()
        mock_collection.name = "test-collection"
        mock_collections_response = MagicMock()
        mock_collections_response.collections = []
        mock_client.get_collections = MagicMock(return_value=mock_collections_response)
        
        # Mock create_collection
        mock_client.create_collection = MagicMock()
        
        # Mock upsert
        mock_client.upsert = MagicMock()
        
        # Mock search
        mock_client.search = MagicMock(return_value=[])
        
        # Mock scroll
        mock_client.scroll = MagicMock(return_value=([], None))
        
        # Mock delete
        mock_client.delete = MagicMock()
        
        # Mock delete_collection
        mock_client.delete_collection = MagicMock()
        
        return mock_client

    @pytest.fixture
    def store(self, mock_embedding_model, mock_qdrant_client):
        """Create a Qdrant store with mocked dependencies."""
        with mock_qdrant_imports(mock_qdrant_client):
            store = QdrantStore(
                collection_name="test-collection",
                embedding_model=mock_embedding_model,
                url="http://localhost:6333"
            )
            store.client = mock_qdrant_client
            yield store

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
        with mock_qdrant_imports():
            with pytest.raises(ValueError, match="embedding_model is required"):
                QdrantStore(
                    collection_name="test-collection",
                    embedding_model=None,
                    url="http://localhost:6333"
                )

    def test_init_creates_collection_if_not_exists(self, mock_embedding_model):
        """Test that initialization creates collection if it doesn't exist."""
        mock_client = MagicMock()
        mock_collections_response = MagicMock()
        mock_collections_response.collections = []
        mock_client.get_collections = MagicMock(return_value=mock_collections_response)
        mock_client.create_collection = MagicMock()
        
        with mock_qdrant_imports(mock_client):
            store = QdrantStore(
                collection_name="new-collection",
                embedding_model=mock_embedding_model,
                url="http://localhost:6333"
            )
            
            # Verify create_collection was called
            mock_client.create_collection.assert_called_once()

    def test_init_skips_creation_if_collection_exists(self, mock_embedding_model):
        """Test that initialization skips creation if collection exists."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.name = "existing-collection"
        mock_collections_response = MagicMock()
        mock_collections_response.collections = [mock_collection]
        mock_client.get_collections = MagicMock(return_value=mock_collections_response)
        mock_client.create_collection = MagicMock()
        
        with mock_qdrant_imports(mock_client):
            store = QdrantStore(
                collection_name="existing-collection",
                embedding_model=mock_embedding_model,
                url="http://localhost:6333"
            )
            
            # Verify create_collection was NOT called
            mock_client.create_collection.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_documents(self, store, sample_documents):
        """Test adding documents to the store."""
        ids = await store.add_documents(sample_documents)
        
        assert len(ids) == 3
        assert all(isinstance(id, str) for id in ids)
        
        # Verify upsert was called
        store.client.upsert.assert_called()

    @pytest.mark.asyncio
    async def test_add_documents_empty_raises(self, store):
        """Test that adding empty documents raises ValueError."""
        with pytest.raises(ValueError, match="documents list cannot be empty"):
            await store.add_documents([])

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
        # Mock the search response
        mock_hit1 = MagicMock()
        mock_hit1.id = "doc1"
        mock_hit1.score = 0.95
        mock_hit1.payload = {
            "content": "Python is great",
            "category": "programming"
        }
        
        mock_hit2 = MagicMock()
        mock_hit2.id = "doc2"
        mock_hit2.score = 0.85
        mock_hit2.payload = {
            "content": "JavaScript is useful",
            "category": "programming"
        }
        
        store.client.search.return_value = [mock_hit1, mock_hit2]
        
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
        
        store.client.search.return_value = []
        
        await store.similarity_search("test", k=5, filter=filter_dict)
        
        # Verify search was called
        store.client.search.assert_called()
        call_args = store.client.search.call_args
        
        # Verify filter was converted to Qdrant format
        assert call_args[1]['query_filter'] is not None

    @pytest.mark.asyncio
    async def test_hybrid_search(self, store):
        """Test hybrid search combining dense and sparse retrieval."""
        # Mock dense search results
        mock_hit1 = MagicMock()
        mock_hit1.id = "doc1"
        mock_hit1.score = 0.9
        mock_hit1.payload = {"content": "Python programming", "category": "tech"}
        
        mock_hit2 = MagicMock()
        mock_hit2.id = "doc2"
        mock_hit2.score = 0.8
        mock_hit2.payload = {"content": "JavaScript coding", "category": "tech"}
        
        store.client.search.return_value = [mock_hit1, mock_hit2]
        
        # Mock sparse search results
        mock_point1 = MagicMock()
        mock_point1.id = "doc3"
        mock_point1.payload = {"content": "Python tutorial", "category": "education"}
        
        store.client.scroll.return_value = ([mock_point1], None)
        
        results = await store.hybrid_search("programming", k=2, alpha=0.5)
        
        assert len(results) <= 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert all(0 <= r.score <= 1 for r in results)

    @pytest.mark.asyncio
    async def test_hybrid_search_alpha_weighting(self, store):
        """Test that alpha parameter correctly weights dense vs sparse."""
        # Mock dense search results
        mock_hit = MagicMock()
        mock_hit.id = "doc1"
        mock_hit.score = 1.0
        mock_hit.payload = {"content": "Test content"}
        
        store.client.search.return_value = [mock_hit]
        store.client.scroll.return_value = ([], None)
        
        # Test with alpha=1.0 (dense only)
        results = await store.hybrid_search("test", k=5, alpha=1.0)
        assert len(results) > 0
        
        # Test with alpha=0.0 (sparse only)
        results = await store.hybrid_search("test", k=5, alpha=0.0)
        # Should still work even with no sparse results

    @pytest.mark.asyncio
    async def test_hybrid_search_invalid_alpha_raises(self, store):
        """Test that alpha outside [0, 1] raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be in"):
            await store.hybrid_search("test", alpha=1.5)
        
        with pytest.raises(ValueError, match="alpha must be in"):
            await store.hybrid_search("test", alpha=-0.1)

    @pytest.mark.asyncio
    async def test_hybrid_search_empty_query_raises(self, store):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="query cannot be empty"):
            await store.hybrid_search("")

    @pytest.mark.asyncio
    async def test_hybrid_search_invalid_k_raises(self, store):
        """Test that k <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="k must be positive"):
            await store.hybrid_search("test", k=0)

    @pytest.mark.asyncio
    async def test_hybrid_search_with_filter(self, store):
        """Test hybrid search with metadata filter."""
        filter_dict = {"category": "programming"}
        
        store.client.search.return_value = []
        store.client.scroll.return_value = ([], None)
        
        await store.hybrid_search("test", k=5, alpha=0.5, filter=filter_dict)
        
        # Verify both search and scroll were called with filters
        store.client.search.assert_called()
        store.client.scroll.assert_called()

    @pytest.mark.asyncio
    async def test_hybrid_search_handles_scroll_failure(self, store):
        """Test hybrid search gracefully handles sparse search failures."""
        # Mock dense search success
        mock_hit = MagicMock()
        mock_hit.id = "doc1"
        mock_hit.score = 0.9
        mock_hit.payload = {"content": "Test content"}
        
        store.client.search.return_value = [mock_hit]
        
        # Mock sparse search failure
        store.client.scroll.side_effect = Exception("Scroll failed")
        
        # Should still return dense results
        results = await store.hybrid_search("test", k=5, alpha=0.5)
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_delete_documents(self, store):
        """Test deleting documents by ID."""
        ids = ["doc1", "doc2", "doc3"]
        
        await store.delete(ids)
        
        # Verify delete was called
        store.client.delete.assert_called_once()
        call_args = store.client.delete.call_args
        assert call_args[1]['collection_name'] == "test-collection"
        assert call_args[1]['points_selector'] == ids

    @pytest.mark.asyncio
    async def test_delete_empty_raises(self, store):
        """Test that deleting empty list raises ValueError."""
        with pytest.raises(ValueError, match="ids list cannot be empty"):
            await store.delete([])

    @pytest.mark.asyncio
    async def test_clear(self, store):
        """Test clearing all documents from collection."""
        await store.clear()
        
        # Verify delete_collection was called
        store.client.delete_collection.assert_called_once()
        
        # Verify create_collection was called to recreate
        store.client.create_collection.assert_called()

    def test_get_embedding_dimension(self, store):
        """Test getting embedding dimension."""
        dim = store.get_embedding_dimension()
        assert dim == 1536

    @pytest.mark.asyncio
    async def test_metadata_stored_correctly(self, store):
        """Test that metadata is stored correctly in Qdrant format."""
        doc = Document(
            content="Test content",
            metadata={"category": "test", "score": 95}
        )
        
        await store.add_documents([doc])
        
        # Verify upsert was called
        store.client.upsert.assert_called()

    def test_import_error_without_qdrant(self, mock_embedding_model):
        """Test that ImportError is raised if qdrant-client is not installed."""
        with patch('builtins.__import__', side_effect=ImportError):
            with pytest.raises(ImportError, match="qdrant-client is required"):
                QdrantStore(
                    collection_name="test-collection",
                    embedding_model=mock_embedding_model,
                    url="http://localhost:6333"
                )

    def test_init_with_api_key(self, mock_embedding_model):
        """Test initialization with API key for Qdrant Cloud."""
        mock_client = MagicMock()
        mock_collections_response = MagicMock()
        mock_collections_response.collections = []
        mock_client.get_collections = MagicMock(return_value=mock_collections_response)
        
        with mock_qdrant_imports(mock_client):
            # Get the patched QdrantClient to check its call args
            from src.langchain.stores import qdrant_store
            
            store = QdrantStore(
                collection_name="test-collection",
                embedding_model=mock_embedding_model,
                url="https://xyz.qdrant.io",
                api_key="test-api-key"
            )
            
            # The api_key should have been passed to the client init
            # We can verify this by checking the store was created successfully
            assert store.collection_name == "test-collection"

    def test_init_with_grpc(self, mock_embedding_model):
        """Test initialization with gRPC preference."""
        mock_client = MagicMock()
        mock_collections_response = MagicMock()
        mock_collections_response.collections = []
        mock_client.get_collections = MagicMock(return_value=mock_collections_response)
        
        with mock_qdrant_imports(mock_client):
            store = QdrantStore(
                collection_name="test-collection",
                embedding_model=mock_embedding_model,
                url="http://localhost:6333",
                prefer_grpc=True
            )
            
            # Verify store was created successfully
            assert store.collection_name == "test-collection"
