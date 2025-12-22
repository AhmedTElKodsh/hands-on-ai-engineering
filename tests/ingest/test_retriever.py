"""Tests for parent document retrieval.

This module tests the ParentDocumentRetriever and related classes
for the parent document retrieval pattern.
"""

import json
import pytest
from src.ingest.models import Document, DocumentMetadata, Chunk, ChunkMetadata
from src.ingest.chunkers import RecursiveChunker, FixedSizeChunker
from src.ingest.retriever import (
    ParentChunk,
    ChunkMapping,
    ParentDocumentRetriever,
)


# Test fixtures
@pytest.fixture
def sample_document() -> Document:
    """Create a sample document for testing."""
    content = """This is the first paragraph. It contains multiple sentences. Each sentence is important.

This is the second paragraph. It also has multiple sentences. The content is different here.

This is the third paragraph. More content follows. Testing chunking strategies."""
    
    metadata = DocumentMetadata(
        source="test_document.txt",
        page_number=1,
        file_type="txt",
    )
    return Document(content=content, metadata=metadata)


@pytest.fixture
def long_document() -> Document:
    """Create a longer document for testing."""
    paragraphs = []
    for i in range(10):
        paragraphs.append(
            f"This is paragraph number {i+1}. "
            f"It contains some text that will be used for testing. "
            f"The chunking strategies should handle this properly. "
            f"Each paragraph is roughly the same length."
        )
    
    content = "\n\n".join(paragraphs)
    metadata = DocumentMetadata(source="long_document.txt", file_type="txt")
    return Document(content=content, metadata=metadata)


class TestParentChunk:
    """Tests for ParentChunk dataclass."""
    
    def test_create_parent_chunk(self) -> None:
        """Test creating a parent chunk."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(
            id="parent_1",
            content="This is parent content.",
            metadata=metadata,
        )
        assert parent.id == "parent_1"
        assert parent.content == "This is parent content."
        assert len(parent.child_ids) == 0
    
    def test_parent_chunk_with_children(self) -> None:
        """Test parent chunk with child IDs."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(
            id="parent_1",
            content="Parent content",
            metadata=metadata,
            child_ids=["child_1", "child_2"],
        )
        assert len(parent.child_ids) == 2
        assert "child_1" in parent.child_ids
    
    def test_parent_chunk_len(self) -> None:
        """Test parent chunk length."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(
            id="parent_1",
            content="12345",
            metadata=metadata,
        )
        assert len(parent) == 5
    
    def test_parent_chunk_serialization(self) -> None:
        """Test parent chunk to_dict and from_dict."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(
            id="parent_1",
            content="Parent content",
            metadata=metadata,
            child_ids=["child_1"],
        )
        
        data = parent.to_dict()
        restored = ParentChunk.from_dict(data)
        
        assert restored.id == parent.id
        assert restored.content == parent.content
        assert restored.child_ids == parent.child_ids


class TestChunkMapping:
    """Tests for ChunkMapping class."""
    
    def test_empty_mapping(self) -> None:
        """Test empty chunk mapping."""
        mapping = ChunkMapping()
        assert len(mapping) == 0
        assert mapping.get_parent("nonexistent") is None
    
    def test_add_mapping(self) -> None:
        """Test adding a child-parent mapping."""
        mapping = ChunkMapping()
        
        child_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        child = Chunk(content="Child content", metadata=child_metadata, id="child_1")
        
        parent_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(id="parent_1", content="Parent content", metadata=parent_metadata)
        
        mapping.add_mapping(child, parent)
        
        assert len(mapping) == 1
        assert mapping.get_parent("child_1") == parent
        assert "child_1" in parent.child_ids
    
    def test_get_children(self) -> None:
        """Test getting children for a parent."""
        mapping = ChunkMapping()
        
        parent_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(id="parent_1", content="Parent", metadata=parent_metadata)
        
        for i in range(3):
            child_metadata = ChunkMetadata(source="test.txt", chunk_index=i)
            child = Chunk(content=f"Child {i}", metadata=child_metadata, id=f"child_{i}")
            mapping.add_mapping(child, parent)
        
        children = mapping.get_children("parent_1")
        assert len(children) == 3
    
    def test_get_parents_for_children(self) -> None:
        """Test getting unique parents for multiple children."""
        mapping = ChunkMapping()
        
        # Create two parents
        for p in range(2):
            parent_metadata = ChunkMetadata(source="test.txt", chunk_index=p)
            parent = ParentChunk(id=f"parent_{p}", content=f"Parent {p}", metadata=parent_metadata)
            
            for c in range(2):
                child_metadata = ChunkMetadata(source="test.txt", chunk_index=c)
                child = Chunk(content=f"Child {p}_{c}", metadata=child_metadata, id=f"child_{p}_{c}")
                mapping.add_mapping(child, parent)
        
        # Get parents for children from both parents
        parents = mapping.get_parents_for_children(["child_0_0", "child_0_1", "child_1_0"])
        assert len(parents) == 2  # Should be deduplicated
    
    def test_mapping_serialization(self) -> None:
        """Test mapping serialization and deserialization."""
        mapping = ChunkMapping()
        
        parent_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(id="parent_1", content="Parent", metadata=parent_metadata)
        
        child_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        child = Chunk(content="Child", metadata=child_metadata, id="child_1")
        mapping.add_mapping(child, parent)
        
        data = mapping.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored = ChunkMapping.from_dict(restored_data)
        
        assert len(restored) == 1
        assert restored.get_parent("child_1") is not None
    
    def test_clear_mapping(self) -> None:
        """Test clearing the mapping."""
        mapping = ChunkMapping()
        
        parent_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        parent = ParentChunk(id="parent_1", content="Parent", metadata=parent_metadata)
        child_metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        child = Chunk(content="Child", metadata=child_metadata, id="child_1")
        mapping.add_mapping(child, parent)
        
        assert len(mapping) == 1
        mapping.clear()
        assert len(mapping) == 0


class TestParentDocumentRetriever:
    """Tests for ParentDocumentRetriever class."""
    
    def test_default_initialization(self) -> None:
        """Test default retriever initialization."""
        retriever = ParentDocumentRetriever()
        assert retriever.parent_splitter.chunk_size == 2000
        assert retriever.child_splitter.chunk_size == 400
        assert len(retriever) == 0
    
    def test_custom_splitters(self) -> None:
        """Test retriever with custom splitters."""
        parent_splitter = RecursiveChunker(chunk_size=1000, chunk_overlap=100)
        child_splitter = RecursiveChunker(chunk_size=200, chunk_overlap=20)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        assert retriever.parent_splitter.chunk_size == 1000
        assert retriever.child_splitter.chunk_size == 200
    
    def test_invalid_chunk_sizes(self) -> None:
        """Test that child chunk size must be smaller than parent."""
        parent_splitter = RecursiveChunker(chunk_size=100, chunk_overlap=10)
        child_splitter = RecursiveChunker(chunk_size=200, chunk_overlap=20)
        
        with pytest.raises(ValueError, match="Child chunk size"):
            ParentDocumentRetriever(
                parent_splitter=parent_splitter,
                child_splitter=child_splitter,
            )
    
    def test_add_document(self, sample_document: Document) -> None:
        """Test adding a document to the retriever."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        child_chunks = retriever.add_document(sample_document)
        
        assert len(child_chunks) > 0
        assert len(retriever.get_parent_chunks()) > 0
        assert len(retriever) == len(child_chunks)
    
    def test_child_chunks_have_parent_reference(self, sample_document: Document) -> None:
        """Test that child chunks reference their parent."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        child_chunks = retriever.add_document(sample_document)
        
        for child in child_chunks:
            assert child.metadata.parent_id is not None
            assert "parent_index" in child.metadata.extra
    
    def test_get_parent_for_child(self, sample_document: Document) -> None:
        """Test retrieving parent for a child chunk."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        child_chunks = retriever.add_document(sample_document)
        
        for child in child_chunks:
            parent = retriever.get_parent(child.id)
            assert parent is not None
            assert child.id in parent.child_ids
            # Parent content should contain child content (approximately)
            # Note: Due to chunking, this may not always be exact
    
    def test_get_parents_for_children(self, sample_document: Document) -> None:
        """Test retrieving unique parents for multiple children."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        child_chunks = retriever.add_document(sample_document)
        child_ids = [c.id for c in child_chunks]
        
        parents = retriever.get_parents_for_children(child_ids)
        
        # Should have fewer or equal parents than children (deduplicated)
        assert len(parents) <= len(child_chunks)
        assert len(parents) > 0
    
    def test_add_multiple_documents(self, sample_document: Document, long_document: Document) -> None:
        """Test adding multiple documents."""
        parent_splitter = RecursiveChunker(chunk_size=200, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        all_chunks = retriever.add_documents([sample_document, long_document])
        
        assert len(all_chunks) > 0
        assert len(retriever.get_parent_chunks()) > 0
    
    def test_get_children_for_parent(self, sample_document: Document) -> None:
        """Test getting all children for a parent."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        retriever.add_document(sample_document)
        parents = retriever.get_parent_chunks()
        
        for parent in parents:
            children = retriever.get_children_for_parent(parent.id)
            assert len(children) > 0
            assert len(children) == len(parent.child_ids)
    
    def test_clear_retriever(self, sample_document: Document) -> None:
        """Test clearing the retriever."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        retriever.add_document(sample_document)
        assert len(retriever) > 0
        
        retriever.clear()
        assert len(retriever) == 0
        assert len(retriever.get_parent_chunks()) == 0
    
    def test_serialization_round_trip(self, sample_document: Document) -> None:
        """Test serialization and deserialization of retriever state."""
        parent_splitter = RecursiveChunker(chunk_size=150, chunk_overlap=20)
        child_splitter = RecursiveChunker(chunk_size=50, chunk_overlap=10)
        
        retriever = ParentDocumentRetriever(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        child_chunks = retriever.add_document(sample_document)
        original_count = len(child_chunks)
        
        # Serialize
        data = retriever.to_dict()
        json_str = json.dumps(data)
        
        # Deserialize
        loaded_data = json.loads(json_str)
        restored = ParentDocumentRetriever.from_dict(loaded_data)
        
        # Verify
        assert len(restored) == original_count
        assert len(restored.get_parent_chunks()) == len(retriever.get_parent_chunks())
        
        # Verify mappings work
        for child in child_chunks:
            parent = restored.get_parent(child.id)
            assert parent is not None
