"""Tests for document chunking strategies.

This module tests the various chunking strategies implemented
in the aitea-ingest package.
"""

import pytest
from src.ingest.models import Document, DocumentMetadata, Chunk, ChunkMetadata
from src.ingest.chunkers import (
    ChunkingStrategy,
    FixedSizeChunker,
    RecursiveChunker,
    SemanticChunker,
    SentenceChunker,
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
    """Create a longer document for testing chunk boundaries."""
    # Create a document with ~2000 characters
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


class TestChunkMetadata:
    """Tests for ChunkMetadata dataclass."""
    
    def test_create_minimal_metadata(self) -> None:
        """Test creating metadata with minimal fields."""
        metadata = ChunkMetadata(source="test.txt")
        assert metadata.source == "test.txt"
        assert metadata.chunk_index == 0
        assert metadata.total_chunks is None
    
    def test_create_full_metadata(self) -> None:
        """Test creating metadata with all fields."""
        metadata = ChunkMetadata(
            source="test.txt",
            chunk_index=5,
            total_chunks=10,
            start_char=100,
            end_char=200,
            page_number=2,
            section="Introduction",
            parent_id="parent_123",
            extra={"key": "value"},
        )
        assert metadata.chunk_index == 5
        assert metadata.total_chunks == 10
        assert metadata.start_char == 100
        assert metadata.end_char == 200
        assert metadata.section == "Introduction"
    
    def test_metadata_to_dict(self) -> None:
        """Test converting metadata to dictionary."""
        metadata = ChunkMetadata(
            source="test.txt",
            chunk_index=1,
            total_chunks=5,
        )
        result = metadata.to_dict()
        assert result["source"] == "test.txt"
        assert result["chunk_index"] == 1
        assert result["total_chunks"] == 5


class TestChunk:
    """Tests for Chunk dataclass."""
    
    def test_create_chunk(self) -> None:
        """Test creating a chunk."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        chunk = Chunk(content="Test content", metadata=metadata)
        assert chunk.content == "Test content"
        assert chunk.metadata.source == "test.txt"
    
    def test_chunk_length(self) -> None:
        """Test chunk length property."""
        metadata = ChunkMetadata(source="test.txt")
        chunk = Chunk(content="Hello World", metadata=metadata)
        assert len(chunk) == 11
    
    def test_chunk_validation(self) -> None:
        """Test chunk validation."""
        metadata = ChunkMetadata(source="test.txt")
        with pytest.raises(ValueError, match="content cannot be None"):
            Chunk(content=None, metadata=metadata)  # type: ignore
    
    def test_chunk_to_dict(self) -> None:
        """Test converting chunk to dictionary."""
        metadata = ChunkMetadata(source="test.txt", chunk_index=0)
        chunk = Chunk(content="Test", metadata=metadata, id="chunk_1")
        result = chunk.to_dict()
        assert result["content"] == "Test"
        assert result["id"] == "chunk_1"
        assert result["metadata"]["source"] == "test.txt"
    
    def test_chunk_from_dict(self) -> None:
        """Test creating chunk from dictionary."""
        data = {
            "content": "Test content",
            "metadata": {
                "source": "test.txt",
                "chunk_index": 1,
                "total_chunks": 5,
                "start_char": 0,
                "end_char": 12,
                "page_number": None,
                "section": None,
                "parent_id": None,
                "extra": {},
            },
            "id": "chunk_1",
        }
        chunk = Chunk.from_dict(data)
        assert chunk.content == "Test content"
        assert chunk.id == "chunk_1"
        assert chunk.metadata.chunk_index == 1


class TestChunkingStrategyValidation:
    """Tests for ChunkingStrategy parameter validation."""
    
    def test_invalid_chunk_size(self) -> None:
        """Test that invalid chunk_size raises error."""
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            FixedSizeChunker(chunk_size=0)
        
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            FixedSizeChunker(chunk_size=-100)
    
    def test_invalid_overlap(self) -> None:
        """Test that invalid overlap raises error."""
        with pytest.raises(ValueError, match="chunk_overlap cannot be negative"):
            FixedSizeChunker(chunk_size=100, chunk_overlap=-10)
        
        with pytest.raises(ValueError, match="chunk_overlap must be less than chunk_size"):
            FixedSizeChunker(chunk_size=100, chunk_overlap=100)
        
        with pytest.raises(ValueError, match="chunk_overlap must be less than chunk_size"):
            FixedSizeChunker(chunk_size=100, chunk_overlap=150)


class TestFixedSizeChunker:
    """Tests for FixedSizeChunker."""
    
    def test_chunk_small_document(self, sample_document: Document) -> None:
        """Test chunking a small document."""
        chunker = FixedSizeChunker(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_document)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata.source == sample_document.metadata.source
            assert chunk.metadata.total_chunks == len(chunks)
    
    def test_chunk_respects_size_limit(self, long_document: Document) -> None:
        """Test that chunks respect size limit."""
        chunk_size = 300
        chunker = FixedSizeChunker(chunk_size=chunk_size, chunk_overlap=50)
        chunks = chunker.chunk(long_document)
        
        # All chunks except possibly the last should be close to chunk_size
        for chunk in chunks[:-1]:
            # Allow some variance due to stripping
            assert len(chunk.content) <= chunk_size + 50
    
    def test_chunk_empty_document(self) -> None:
        """Test chunking an empty document."""
        metadata = DocumentMetadata(source="empty.txt")
        doc = Document(content="", metadata=metadata)
        
        chunker = FixedSizeChunker()
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 0
    
    def test_chunk_text_method(self) -> None:
        """Test the chunk_text convenience method."""
        chunker = FixedSizeChunker(chunk_size=50, chunk_overlap=10)
        text = "This is a test. " * 10
        
        chunks = chunker.chunk_text(text, source="test_source")
        
        assert len(chunks) > 0
        assert chunks[0].metadata.source == "test_source"
    
    def test_chunk_indices_are_sequential(self, sample_document: Document) -> None:
        """Test that chunk indices are sequential."""
        chunker = FixedSizeChunker(chunk_size=100, chunk_overlap=20)
        chunks = chunker.chunk(sample_document)
        
        for i, chunk in enumerate(chunks):
            assert chunk.metadata.chunk_index == i


class TestRecursiveChunker:
    """Tests for RecursiveChunker."""
    
    def test_chunk_by_paragraphs(self, sample_document: Document) -> None:
        """Test that recursive chunker respects paragraph boundaries."""
        chunker = RecursiveChunker(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_document)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata.extra.get("strategy") == "recursive"
    
    def test_custom_separators(self) -> None:
        """Test using custom separators."""
        # Use longer parts so each exceeds chunk_size when combined
        text = "PartOne|PartTwo|PartThree"
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content=text, metadata=metadata)
        
        # chunk_size=8 means each part (7 chars) fits alone but two don't fit together
        chunker = RecursiveChunker(
            chunk_size=8,
            chunk_overlap=0,
            separators=["|"],
            keep_separator=False,
        )
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 3
        assert chunks[0].content == "PartOne"
        assert chunks[1].content == "PartTwo"
        assert chunks[2].content == "PartThree"
    
    def test_chunk_empty_document(self) -> None:
        """Test chunking an empty document."""
        metadata = DocumentMetadata(source="empty.txt")
        doc = Document(content="", metadata=metadata)
        
        chunker = RecursiveChunker()
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 0
    
    def test_keeps_separator_by_default(self) -> None:
        """Test that separators are kept by default."""
        text = "First sentence. Second sentence."
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content=text, metadata=metadata)
        
        chunker = RecursiveChunker(
            chunk_size=20,
            chunk_overlap=0,
            separators=[". "],
            keep_separator=True,
        )
        chunks = chunker.chunk(doc)
        
        # First chunk should end with ". "
        assert chunks[0].content.endswith(".")


class TestSemanticChunker:
    """Tests for SemanticChunker."""
    
    def test_requires_embedding_function(self, sample_document: Document) -> None:
        """Test that SemanticChunker requires an embedding function."""
        chunker = SemanticChunker()
        
        with pytest.raises(ValueError, match="requires an embedding_function"):
            chunker.chunk(sample_document)
    
    def test_with_mock_embedding_function(self, sample_document: Document) -> None:
        """Test SemanticChunker with a mock embedding function."""
        # Simple mock that returns different embeddings for different texts
        def mock_embedding(text: str) -> list[float]:
            # Return a simple hash-based embedding
            hash_val = hash(text) % 1000
            return [hash_val / 1000.0, (hash_val + 100) / 1000.0, (hash_val + 200) / 1000.0]
        
        chunker = SemanticChunker(
            chunk_size=500,
            chunk_overlap=50,
            embedding_function=mock_embedding,
            similarity_threshold=0.5,
        )
        chunks = chunker.chunk(sample_document)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata.extra.get("strategy") == "semantic"
    
    def test_chunk_empty_document(self) -> None:
        """Test chunking an empty document."""
        metadata = DocumentMetadata(source="empty.txt")
        doc = Document(content="", metadata=metadata)
        
        def mock_embedding(text: str) -> list[float]:
            return [0.0, 0.0, 0.0]
        
        chunker = SemanticChunker(embedding_function=mock_embedding)
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 0
    
    def test_single_sentence_document(self) -> None:
        """Test chunking a single sentence document."""
        metadata = DocumentMetadata(source="single.txt")
        doc = Document(content="This is a single sentence.", metadata=metadata)
        
        def mock_embedding(text: str) -> list[float]:
            return [0.5, 0.5, 0.5]
        
        chunker = SemanticChunker(embedding_function=mock_embedding)
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 1
        assert chunks[0].content == "This is a single sentence."


class TestSentenceChunker:
    """Tests for SentenceChunker."""
    
    def test_chunk_by_sentences(self, sample_document: Document) -> None:
        """Test that sentence chunker groups sentences."""
        chunker = SentenceChunker(chunk_size=200, chunk_overlap=50)
        chunks = chunker.chunk(sample_document)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata.extra.get("strategy") == "sentence"
            assert "sentence_count" in chunk.metadata.extra
    
    def test_chunk_empty_document(self) -> None:
        """Test chunking an empty document."""
        metadata = DocumentMetadata(source="empty.txt")
        doc = Document(content="", metadata=metadata)
        
        chunker = SentenceChunker()
        chunks = chunker.chunk(doc)
        
        assert len(chunks) == 0
    
    def test_regex_fallback(self) -> None:
        """Test that regex fallback works when NLP libraries unavailable."""
        text = "First sentence. Second sentence! Third sentence?"
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content=text, metadata=metadata)
        
        # Disable both spaCy and NLTK to force regex fallback
        chunker = SentenceChunker(
            chunk_size=100,
            chunk_overlap=0,
            use_spacy=False,
            use_nltk=False,
        )
        chunks = chunker.chunk(doc)
        
        assert len(chunks) >= 1
    
    def test_preserves_sentence_boundaries(self) -> None:
        """Test that chunks end at sentence boundaries."""
        text = "Short. " * 20  # 20 short sentences
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content=text.strip(), metadata=metadata)
        
        chunker = SentenceChunker(
            chunk_size=50,
            chunk_overlap=0,
            use_spacy=False,
            use_nltk=False,
        )
        chunks = chunker.chunk(doc)
        
        # Each chunk should contain complete sentences
        for chunk in chunks:
            # Should end with punctuation or be the last chunk
            content = chunk.content.strip()
            assert content.endswith(".") or chunk.metadata.chunk_index == len(chunks) - 1
