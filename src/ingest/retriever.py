"""Parent Document Retrieval for document processing.

This module provides the ParentDocumentRetriever class which implements
a retrieval pattern where small chunks are stored for embedding/search
but larger parent documents are retrieved for context.

This pattern is useful for RAG systems where:
- Small chunks provide precise semantic matching
- Larger parent documents provide better context for generation
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
import uuid

from .models import Chunk, ChunkMetadata, Document, DocumentMetadata
from .chunkers import ChunkingStrategy, FixedSizeChunker, RecursiveChunker


@dataclass
class ParentChunk:
    """A parent chunk that contains multiple child chunks.
    
    Attributes:
        id: Unique identifier for the parent chunk
        content: The text content of the parent chunk
        metadata: Metadata about the parent chunk's origin
        child_ids: List of child chunk IDs that belong to this parent
    """
    id: str
    content: str
    metadata: ChunkMetadata
    child_ids: List[str] = field(default_factory=list)
    
    def __len__(self) -> int:
        """Return the length of the parent chunk content."""
        return len(self.content)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parent chunk to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata.to_dict(),
            "child_ids": self.child_ids,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParentChunk":
        """Create a ParentChunk from a dictionary."""
        metadata = ChunkMetadata(**data["metadata"])
        return cls(
            id=data["id"],
            content=data["content"],
            metadata=metadata,
            child_ids=data.get("child_ids", []),
        )


@dataclass
class ChunkMapping:
    """Mapping between child chunks and their parent chunks.
    
    This class stores the relationship between child chunks (used for
    embedding/search) and parent chunks (used for retrieval/context).
    
    Attributes:
        child_to_parent: Maps child chunk ID to parent chunk ID
        parent_to_children: Maps parent chunk ID to list of child chunk IDs
        parents: Storage for parent chunks by ID
        children: Storage for child chunks by ID
    """
    child_to_parent: Dict[str, str] = field(default_factory=dict)
    parent_to_children: Dict[str, List[str]] = field(default_factory=dict)
    parents: Dict[str, ParentChunk] = field(default_factory=dict)
    children: Dict[str, Chunk] = field(default_factory=dict)
    
    def add_mapping(
        self,
        child_chunk: Chunk,
        parent_chunk: ParentChunk,
    ) -> None:
        """Add a child-to-parent mapping.
        
        Args:
            child_chunk: The child chunk
            parent_chunk: The parent chunk containing the child
        """
        if child_chunk.id is None:
            child_chunk.id = str(uuid.uuid4())
        
        child_id = child_chunk.id
        parent_id = parent_chunk.id
        
        # Store the mapping
        self.child_to_parent[child_id] = parent_id
        
        # Update parent's child list
        if parent_id not in self.parent_to_children:
            self.parent_to_children[parent_id] = []
        if child_id not in self.parent_to_children[parent_id]:
            self.parent_to_children[parent_id].append(child_id)
        
        # Store the chunks
        self.children[child_id] = child_chunk
        self.parents[parent_id] = parent_chunk
        
        # Update parent's child_ids list
        if child_id not in parent_chunk.child_ids:
            parent_chunk.child_ids.append(child_id)
    
    def get_parent(self, child_id: str) -> Optional[ParentChunk]:
        """Get the parent chunk for a given child chunk ID.
        
        Args:
            child_id: The child chunk ID
            
        Returns:
            The parent chunk, or None if not found
        """
        parent_id = self.child_to_parent.get(child_id)
        if parent_id is None:
            return None
        return self.parents.get(parent_id)
    
    def get_children(self, parent_id: str) -> List[Chunk]:
        """Get all child chunks for a given parent chunk ID.
        
        Args:
            parent_id: The parent chunk ID
            
        Returns:
            List of child chunks
        """
        child_ids = self.parent_to_children.get(parent_id, [])
        return [self.children[cid] for cid in child_ids if cid in self.children]
    
    def get_parents_for_children(self, child_ids: List[str]) -> List[ParentChunk]:
        """Get unique parent chunks for a list of child chunk IDs.
        
        Args:
            child_ids: List of child chunk IDs
            
        Returns:
            List of unique parent chunks (deduplicated)
        """
        seen_parent_ids: Set[str] = set()
        parents: List[ParentChunk] = []
        
        for child_id in child_ids:
            parent = self.get_parent(child_id)
            if parent is not None and parent.id not in seen_parent_ids:
                seen_parent_ids.add(parent.id)
                parents.append(parent)
        
        return parents
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert mapping to dictionary for serialization."""
        return {
            "child_to_parent": self.child_to_parent,
            "parent_to_children": self.parent_to_children,
            "parents": {pid: p.to_dict() for pid, p in self.parents.items()},
            "children": {cid: c.to_dict() for cid, c in self.children.items()},
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkMapping":
        """Create a ChunkMapping from a dictionary."""
        mapping = cls(
            child_to_parent=data.get("child_to_parent", {}),
            parent_to_children=data.get("parent_to_children", {}),
        )
        
        # Reconstruct parents
        for pid, pdata in data.get("parents", {}).items():
            mapping.parents[pid] = ParentChunk.from_dict(pdata)
        
        # Reconstruct children
        for cid, cdata in data.get("children", {}).items():
            mapping.children[cid] = Chunk.from_dict(cdata)
        
        return mapping
    
    def clear(self) -> None:
        """Clear all mappings and stored chunks."""
        self.child_to_parent.clear()
        self.parent_to_children.clear()
        self.parents.clear()
        self.children.clear()
    
    def __len__(self) -> int:
        """Return the number of child chunks stored."""
        return len(self.children)


class ParentDocumentRetriever:
    """Retriever that stores small chunks but retrieves parent documents.
    
    This class implements the parent document retrieval pattern where:
    1. Documents are split into large "parent" chunks
    2. Parent chunks are further split into small "child" chunks
    3. Child chunks are used for embedding and similarity search
    4. When a child chunk matches, the parent chunk is retrieved
    
    This provides the best of both worlds:
    - Small chunks for precise semantic matching
    - Large parent chunks for better context in generation
    
    Example:
        >>> parent_splitter = RecursiveChunker(chunk_size=2000, chunk_overlap=200)
        >>> child_splitter = RecursiveChunker(chunk_size=400, chunk_overlap=50)
        >>> retriever = ParentDocumentRetriever(
        ...     parent_splitter=parent_splitter,
        ...     child_splitter=child_splitter,
        ... )
        >>> child_chunks = retriever.add_document(document)
        >>> # Use child_chunks for embedding/indexing
        >>> # Later, retrieve parent chunks from child matches
        >>> parent_chunks = retriever.get_parents_for_children([child.id for child in matches])
    
    Attributes:
        parent_splitter: ChunkingStrategy for creating parent chunks
        child_splitter: ChunkingStrategy for creating child chunks from parents
        mapping: Storage for chunk-to-parent mappings
    """
    
    def __init__(
        self,
        parent_splitter: Optional[ChunkingStrategy] = None,
        child_splitter: Optional[ChunkingStrategy] = None,
    ) -> None:
        """Initialize the ParentDocumentRetriever.
        
        Args:
            parent_splitter: Strategy for creating parent chunks.
                Defaults to RecursiveChunker with chunk_size=2000.
            child_splitter: Strategy for creating child chunks.
                Defaults to RecursiveChunker with chunk_size=400.
                
        Raises:
            ValueError: If child chunk size >= parent chunk size
        """
        # Default splitters if not provided
        self.parent_splitter = parent_splitter or RecursiveChunker(
            chunk_size=2000,
            chunk_overlap=200,
        )
        self.child_splitter = child_splitter or RecursiveChunker(
            chunk_size=400,
            chunk_overlap=50,
        )
        
        # Validate that child chunks are smaller than parent chunks
        if self.child_splitter.chunk_size >= self.parent_splitter.chunk_size:
            raise ValueError(
                f"Child chunk size ({self.child_splitter.chunk_size}) must be "
                f"smaller than parent chunk size ({self.parent_splitter.chunk_size})"
            )
        
        # Initialize mapping storage
        self.mapping = ChunkMapping()
    
    def add_document(self, document: Document) -> List[Chunk]:
        """Process a document and return child chunks for indexing.
        
        This method:
        1. Splits the document into parent chunks
        2. Splits each parent chunk into child chunks
        3. Stores the parent-child mappings
        4. Returns the child chunks for embedding/indexing
        
        Args:
            document: The document to process
            
        Returns:
            List of child chunks (use these for embedding/indexing)
        """
        all_child_chunks: List[Chunk] = []
        
        # Create parent chunks from the document
        parent_chunks = self.parent_splitter.chunk(document)
        
        for parent_idx, parent_chunk_data in enumerate(parent_chunks):
            # Create a ParentChunk from the Chunk
            parent_chunk = ParentChunk(
                id=parent_chunk_data.id or str(uuid.uuid4()),
                content=parent_chunk_data.content,
                metadata=parent_chunk_data.metadata,
            )
            
            # Create a temporary document from the parent chunk content
            # to split into child chunks
            parent_doc = Document(
                content=parent_chunk.content,
                metadata=DocumentMetadata(
                    source=document.metadata.source,
                    page_number=document.metadata.page_number,
                    file_type=document.metadata.file_type,
                    extra={
                        "parent_id": parent_chunk.id,
                        "parent_index": parent_idx,
                    },
                ),
            )
            
            # Create child chunks from the parent
            child_chunks = self.child_splitter.chunk(parent_doc)
            
            # Update child chunk metadata and create mappings
            for child_chunk in child_chunks:
                # Ensure child has an ID
                if child_chunk.id is None:
                    child_chunk.id = str(uuid.uuid4())
                
                # Add parent reference to child metadata
                child_chunk.metadata.parent_id = parent_chunk.id
                child_chunk.metadata.extra["parent_index"] = parent_idx
                child_chunk.metadata.extra["retrieval_type"] = "parent_document"
                
                # Store the mapping
                self.mapping.add_mapping(child_chunk, parent_chunk)
                
                all_child_chunks.append(child_chunk)
        
        return all_child_chunks
    
    def add_documents(self, documents: List[Document]) -> List[Chunk]:
        """Process multiple documents and return all child chunks.
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of all child chunks from all documents
        """
        all_chunks: List[Chunk] = []
        for document in documents:
            chunks = self.add_document(document)
            all_chunks.extend(chunks)
        return all_chunks
    
    def get_parent(self, child_id: str) -> Optional[ParentChunk]:
        """Get the parent chunk for a child chunk ID.
        
        Args:
            child_id: The child chunk ID
            
        Returns:
            The parent chunk, or None if not found
        """
        return self.mapping.get_parent(child_id)
    
    def get_parents_for_children(self, child_ids: List[str]) -> List[ParentChunk]:
        """Get unique parent chunks for a list of child chunk IDs.
        
        This is the main retrieval method. After performing similarity
        search on child chunks, pass the matching child IDs here to
        get the corresponding parent chunks for context.
        
        Args:
            child_ids: List of child chunk IDs from search results
            
        Returns:
            List of unique parent chunks (deduplicated)
        """
        return self.mapping.get_parents_for_children(child_ids)
    
    def get_child_chunks(self) -> List[Chunk]:
        """Get all stored child chunks.
        
        Returns:
            List of all child chunks
        """
        return list(self.mapping.children.values())
    
    def get_parent_chunks(self) -> List[ParentChunk]:
        """Get all stored parent chunks.
        
        Returns:
            List of all parent chunks
        """
        return list(self.mapping.parents.values())
    
    def get_children_for_parent(self, parent_id: str) -> List[Chunk]:
        """Get all child chunks for a parent chunk ID.
        
        Args:
            parent_id: The parent chunk ID
            
        Returns:
            List of child chunks belonging to the parent
        """
        return self.mapping.get_children(parent_id)
    
    def clear(self) -> None:
        """Clear all stored chunks and mappings."""
        self.mapping.clear()
    
    def __len__(self) -> int:
        """Return the number of child chunks stored."""
        return len(self.mapping)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert retriever state to dictionary for serialization.
        
        Note: This only serializes the mapping data, not the splitter
        configurations. When deserializing, you'll need to provide
        the splitters again.
        
        Returns:
            Dictionary containing the mapping data
        """
        return {
            "mapping": self.mapping.to_dict(),
            "parent_chunk_size": self.parent_splitter.chunk_size,
            "parent_chunk_overlap": self.parent_splitter.chunk_overlap,
            "child_chunk_size": self.child_splitter.chunk_size,
            "child_chunk_overlap": self.child_splitter.chunk_overlap,
        }
    
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        parent_splitter: Optional[ChunkingStrategy] = None,
        child_splitter: Optional[ChunkingStrategy] = None,
    ) -> "ParentDocumentRetriever":
        """Create a ParentDocumentRetriever from a dictionary.
        
        Args:
            data: Dictionary containing mapping data
            parent_splitter: Optional parent splitter (uses defaults if not provided)
            child_splitter: Optional child splitter (uses defaults if not provided)
            
        Returns:
            A new ParentDocumentRetriever with restored state
        """
        # Create splitters from saved config if not provided
        if parent_splitter is None:
            parent_splitter = RecursiveChunker(
                chunk_size=data.get("parent_chunk_size", 2000),
                chunk_overlap=data.get("parent_chunk_overlap", 200),
            )
        
        if child_splitter is None:
            child_splitter = RecursiveChunker(
                chunk_size=data.get("child_chunk_size", 400),
                chunk_overlap=data.get("child_chunk_overlap", 50),
            )
        
        retriever = cls(
            parent_splitter=parent_splitter,
            child_splitter=child_splitter,
        )
        
        # Restore mapping
        if "mapping" in data:
            retriever.mapping = ChunkMapping.from_dict(data["mapping"])
        
        return retriever
