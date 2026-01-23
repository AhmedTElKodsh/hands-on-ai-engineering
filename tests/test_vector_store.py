"""
Test suite for VectorStore implementation.

Verifies that the VectorStore wrapper around ChromaDB works correctly
for document storage, retrieval, and metadata tracking.
"""

import pytest
import os
import shutil
from pathlib import Path
from shared.infrastructure.vector_store import VectorStore, create_vector_store


@pytest.fixture
def test_db_path(tmp_path):
    """Provide a temporary database path for testing."""
    db_path = tmp_path / "test_chroma_db"
    yield str(db_path)
    # Cleanup after test
    if db_path.exists():
        shutil.rmtree(db_path)


@pytest.fixture
def vector_store(test_db_path):
    """Create a VectorStore instance for testing."""
    # Skip if no API key available
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    
    store = VectorStore(
        path=test_db_path,
        collection_name="test_collection"
    )
    yield store
    # Cleanup
    store.clear()


class TestVectorStoreInitialization:
    """Tests for VectorStore initialization."""
    
    def test_init_creates_directory(self, test_db_path):
        """Test that initialization creates the storage directory."""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        store = VectorStore(path=test_db_path, collection_name="test")
        assert Path(test_db_path).exists()
        assert Path(test_db_path).is_dir()
    
    def test_init_without_api_key_raises_error(self, test_db_path, monkeypatch):
        """Test that initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="OpenAI API key required"):
            VectorStore(path=test_db_path, collection_name="test", api_key=None)
    
    def test_create_vector_store_convenience_function(self, test_db_path):
        """Test the convenience function for creating stores."""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        store = create_vector_store(path=test_db_path, collection_name="test")
        assert isinstance(store, VectorStore)
        assert store.collection_name == "test"


class TestDocumentOperations:
    """Tests for adding, retrieving, and deleting documents."""
    
    def test_add_single_document(self, vector_store):
        """Test adding a single document."""
        vector_store.add_document(
            doc_id="1",
            text="Test document",
            metadata={"source": "test"}
        )
        
        assert vector_store.count() == 1
    
    def test_add_document_without_metadata(self, vector_store):
        """Test adding document without metadata."""
        vector_store.add_document(doc_id="1", text="Test document")
        assert vector_store.count() == 1
    
    def test_add_multiple_documents(self, vector_store):
        """Test adding multiple documents in batch."""
        vector_store.add_documents(
            doc_ids=["1", "2", "3"],
            texts=["Doc 1", "Doc 2", "Doc 3"],
            metadatas=[
                {"source": "a.txt"},
                {"source": "b.txt"},
                {"source": "c.txt"}
            ]
        )
        
        assert vector_store.count() == 3
    
    def test_add_documents_mismatched_lengths_raises_error(self, vector_store):
        """Test that mismatched list lengths raise an error."""
        with pytest.raises(ValueError, match="same length"):
            vector_store.add_documents(
                doc_ids=["1", "2"],
                texts=["Doc 1"]  # Wrong length
            )
    
    def test_get_document_by_id(self, vector_store):
        """Test retrieving a specific document by ID."""
        vector_store.add_document(
            doc_id="test_id",
            text="Test content",
            metadata={"key": "value"}
        )
        
        doc, meta = vector_store.get_document("test_id")
        assert doc == "Test content"
        assert meta["key"] == "value"
    
    def test_get_nonexistent_document_returns_none(self, vector_store):
        """Test that getting a nonexistent document returns None."""
        result = vector_store.get_document("nonexistent")
        assert result is None
    
    def test_delete_single_document(self, vector_store):
        """Test deleting a single document."""
        vector_store.add_document(doc_id="1", text="Test")
        assert vector_store.count() == 1
        
        vector_store.delete_document("1")
        assert vector_store.count() == 0
    
    def test_delete_multiple_documents(self, vector_store):
        """Test deleting multiple documents."""
        vector_store.add_documents(
            doc_ids=["1", "2", "3"],
            texts=["Doc 1", "Doc 2", "Doc 3"]
        )
        assert vector_store.count() == 3
        
        vector_store.delete_documents(["1", "2"])
        assert vector_store.count() == 1
    
    def test_clear_removes_all_documents(self, vector_store):
        """Test that clear() removes all documents."""
        vector_store.add_documents(
            doc_ids=["1", "2", "3"],
            texts=["Doc 1", "Doc 2", "Doc 3"]
        )
        assert vector_store.count() == 3
        
        vector_store.clear()
        assert vector_store.count() == 0


class TestSemanticSearch:
    """Tests for semantic search functionality."""
    
    def test_search_returns_relevant_documents(self, vector_store):
        """Test that search returns semantically similar documents."""
        # Add documents about different topics
        vector_store.add_documents(
            doc_ids=["1", "2", "3"],
            texts=[
                "Python is a programming language",
                "Dogs are loyal pets",
                "JavaScript is used for web development"
            ]
        )
        
        # Search for programming-related content
        results = vector_store.search("coding and software", limit=2)
        
        assert len(results) <= 2
        # Should find programming-related docs, not the dog doc
        assert any("Python" in doc or "JavaScript" in doc for doc in results)
    
    def test_search_respects_limit(self, vector_store):
        """Test that search respects the limit parameter."""
        vector_store.add_documents(
            doc_ids=["1", "2", "3", "4", "5"],
            texts=["Doc 1", "Doc 2", "Doc 3", "Doc 4", "Doc 5"]
        )
        
        results = vector_store.search("Doc", limit=3)
        assert len(results) <= 3
    
    def test_search_empty_store_returns_empty_list(self, vector_store):
        """Test that searching an empty store returns empty list."""
        results = vector_store.search("anything")
        assert results == []
    
    def test_search_with_metadata_filter(self, vector_store):
        """Test searching with metadata filtering."""
        vector_store.add_documents(
            doc_ids=["1", "2", "3"],
            texts=["Doc A", "Doc B", "Doc C"],
            metadatas=[
                {"category": "tech"},
                {"category": "science"},
                {"category": "tech"}
            ]
        )
        
        # Search only in tech category
        results = vector_store.search(
            "Doc",
            limit=5,
            where={"category": "tech"}
        )
        
        # Should only return tech documents
        assert len(results) <= 2


class TestSearchWithMetadata:
    """Tests for search_with_metadata functionality."""
    
    def test_search_with_metadata_returns_tuples(self, vector_store):
        """Test that search_with_metadata returns (doc, metadata) tuples."""
        vector_store.add_document(
            doc_id="1",
            text="Test document",
            metadata={"source": "test.txt", "page": 1}
        )
        
        results = vector_store.search_with_metadata("Test", limit=1)
        
        assert len(results) == 1
        doc, meta = results[0]
        assert doc == "Test document"
        assert meta["source"] == "test.txt"
        assert meta["page"] == 1
    
    def test_search_with_metadata_empty_store(self, vector_store):
        """Test search_with_metadata on empty store."""
        results = vector_store.search_with_metadata("anything")
        assert results == []


class TestSearchWithScores:
    """Tests for search_with_scores functionality."""
    
    def test_search_with_scores_returns_distances(self, vector_store):
        """Test that search_with_scores returns distance scores."""
        vector_store.add_documents(
            doc_ids=["1", "2"],
            texts=["Python programming", "Dogs and cats"],
            metadatas=[{"type": "tech"}, {"type": "animals"}]
        )
        
        results = vector_store.search_with_scores("coding", limit=2)
        
        assert len(results) <= 2
        for doc, score, meta in results:
            assert isinstance(doc, str)
            assert isinstance(score, (int, float))
            assert isinstance(meta, dict)
            # Lower score = more similar
            assert score >= 0


class TestPersistence:
    """Tests for data persistence across sessions."""
    
    def test_data_persists_across_instances(self, test_db_path):
        """Test that data persists when creating new VectorStore instance."""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        # Create store and add data
        store1 = VectorStore(path=test_db_path, collection_name="persist_test")
        store1.add_document(doc_id="1", text="Persistent data")
        count1 = store1.count()
        
        # Create new instance with same path
        store2 = VectorStore(path=test_db_path, collection_name="persist_test")
        count2 = store2.count()
        
        assert count1 == count2 == 1
        
        # Cleanup
        store2.clear()


class TestRepr:
    """Tests for string representation."""
    
    def test_repr_shows_useful_info(self, vector_store):
        """Test that __repr__ shows useful information."""
        vector_store.add_documents(
            doc_ids=["1", "2"],
            texts=["Doc 1", "Doc 2"]
        )
        
        repr_str = repr(vector_store)
        assert "VectorStore" in repr_str
        assert "test_collection" in repr_str
        assert "documents=2" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
