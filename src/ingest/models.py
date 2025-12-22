"""Data models for document ingestion.

This module defines the core data structures used throughout
the document ingestion pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DocumentMetadata:
    """Metadata associated with a loaded document.
    
    Attributes:
        source: Original file path or URL of the document
        page_number: Page number within the document (if applicable)
        total_pages: Total number of pages in the source document
        title: Document title (if extractable)
        author: Document author (if extractable)
        created_date: Document creation date (if extractable)
        modified_date: Document modification date (if extractable)
        file_type: Type of the source file (pdf, docx, html, md)
        extra: Additional metadata specific to the document type
    """
    source: str
    page_number: Optional[int] = None
    total_pages: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    file_type: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for serialization."""
        result = {
            "source": self.source,
            "page_number": self.page_number,
            "total_pages": self.total_pages,
            "title": self.title,
            "author": self.author,
            "file_type": self.file_type,
            "extra": self.extra,
        }
        if self.created_date:
            result["created_date"] = self.created_date.isoformat()
        if self.modified_date:
            result["modified_date"] = self.modified_date.isoformat()
        return result


@dataclass
class Document:
    """A loaded document with content and metadata.
    
    Represents a single document or page extracted from a source file.
    Multiple Document instances may be created from a single source file
    (e.g., one per page in a PDF).
    
    Attributes:
        content: The text content of the document
        metadata: Associated metadata about the document source
    """
    content: str
    metadata: DocumentMetadata
    
    def __post_init__(self) -> None:
        """Validate document after initialization."""
        if self.content is None:
            raise ValueError("Document content cannot be None")
        if self.metadata is None:
            raise ValueError("Document metadata cannot be None")
    
    def __len__(self) -> int:
        """Return the length of the document content."""
        return len(self.content)
    
    def __str__(self) -> str:
        """Return a string representation of the document."""
        preview = self.content[:100] + "..." if len(self.content) > 100 else self.content
        return f"Document(source={self.metadata.source}, content={preview!r})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary for serialization."""
        return {
            "content": self.content,
            "metadata": self.metadata.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create a Document from a dictionary."""
        metadata_data = data["metadata"]
        # Handle datetime fields
        if "created_date" in metadata_data and metadata_data["created_date"]:
            metadata_data["created_date"] = datetime.fromisoformat(metadata_data["created_date"])
        if "modified_date" in metadata_data and metadata_data["modified_date"]:
            metadata_data["modified_date"] = datetime.fromisoformat(metadata_data["modified_date"])
        metadata = DocumentMetadata(**metadata_data)
        return cls(content=data["content"], metadata=metadata)


@dataclass
class ChunkMetadata:
    """Metadata associated with a document chunk.
    
    Attributes:
        source: Original file path or URL of the source document
        chunk_index: Index of this chunk within the document
        total_chunks: Total number of chunks from the source document
        start_char: Starting character position in the original document
        end_char: Ending character position in the original document
        page_number: Page number if applicable (from source document)
        section: Section or heading this chunk belongs to
        parent_id: ID of the parent chunk (for hierarchical chunking)
        extra: Additional metadata specific to the chunking strategy
    """
    source: str
    chunk_index: int = 0
    total_chunks: Optional[int] = None
    start_char: int = 0
    end_char: int = 0
    page_number: Optional[int] = None
    section: Optional[str] = None
    parent_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for serialization."""
        return {
            "source": self.source,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "page_number": self.page_number,
            "section": self.section,
            "parent_id": self.parent_id,
            "extra": self.extra,
        }


@dataclass
class Chunk:
    """A chunk of text extracted from a document.
    
    Represents a portion of a document created by a chunking strategy.
    Chunks maintain references to their source document and position
    within it.
    
    Attributes:
        content: The text content of the chunk
        metadata: Associated metadata about the chunk's origin
        id: Optional unique identifier for the chunk
    """
    content: str
    metadata: ChunkMetadata
    id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate chunk after initialization."""
        if self.content is None:
            raise ValueError("Chunk content cannot be None")
        if self.metadata is None:
            raise ValueError("Chunk metadata cannot be None")
    
    def __len__(self) -> int:
        """Return the length of the chunk content."""
        return len(self.content)
    
    def __str__(self) -> str:
        """Return a string representation of the chunk."""
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Chunk(index={self.metadata.chunk_index}, content={preview!r})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary for serialization."""
        return {
            "content": self.content,
            "metadata": self.metadata.to_dict(),
            "id": self.id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chunk":
        """Create a Chunk from a dictionary."""
        metadata = ChunkMetadata(**data["metadata"])
        return cls(
            content=data["content"],
            metadata=metadata,
            id=data.get("id"),
        )
