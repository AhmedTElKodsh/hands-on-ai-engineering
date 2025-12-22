"""Memory classes for AI agents.

This module provides memory implementations for agents to store and retrieve
information across interactions. Memory is a key component of agent systems,
enabling context retention and learning from past interactions.

Memory Types:
- ShortTermMemory: Fixed-capacity memory that removes oldest items when full
- LongTermMemory: Persistent storage for important information
- SummarizationMemory: Compresses context using LLM summarization

Requirements: 5.5 - Memory classes for short-term, long-term, and summarization memory patterns
"""

import json
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Deque, Dict, Generic, List, Optional, TypeVar

from src.services.llm import LLMProvider


T = TypeVar("T")


@dataclass
class MemoryItem:
    """A single item stored in memory.
    
    Attributes:
        content: The actual content stored
        timestamp: When the item was added
        metadata: Optional additional information about the item
        importance: Optional importance score (0.0 to 1.0)
    """
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "importance": self.importance,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        """Create from dictionary."""
        return cls(
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
            importance=data.get("importance", 0.5),
        )


class BaseMemory(ABC):
    """Abstract base class for all memory implementations.
    
    All memory classes must implement these core operations:
    - add: Store a new item in memory
    - get_all: Retrieve all stored items
    - clear: Remove all items from memory
    - search: Find items matching a query
    """
    
    @abstractmethod
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add a new item to memory.
        
        Args:
            content: The content to store
            metadata: Optional metadata about the content
            
        Returns:
            The created MemoryItem
        """
        ...
    
    @abstractmethod
    def get_all(self) -> List[MemoryItem]:
        """Get all items in memory.
        
        Returns:
            List of all MemoryItems
        """
        ...
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all items from memory."""
        ...
    
    @abstractmethod
    def search(self, query: str) -> List[MemoryItem]:
        """Search for items matching a query.
        
        Args:
            query: The search query
            
        Returns:
            List of matching MemoryItems
        """
        ...
    
    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items in memory."""
        ...


class ShortTermMemory(BaseMemory):
    """Fixed-capacity memory that removes oldest items when full.
    
    ShortTermMemory maintains a fixed number of recent items using a
    FIFO (First-In-First-Out) eviction policy. When the capacity is
    reached, the oldest item is automatically removed to make room
    for new items.
    
    This is useful for maintaining recent conversation context or
    tracking the most recent observations in an agent loop.
    
    Attributes:
        capacity: Maximum number of items to store
        
    Example:
        >>> memory = ShortTermMemory(capacity=3)
        >>> memory.add("First item")
        >>> memory.add("Second item")
        >>> memory.add("Third item")
        >>> len(memory)
        3
        >>> memory.add("Fourth item")  # Removes "First item"
        >>> len(memory)
        3
        >>> memory.get_all()[0].content
        'Second item'
    
    Property 10: Memory Capacity Constraints
    For any short-term memory instance with capacity N, adding more than N items
    SHALL result in exactly N items being retained (oldest items removed).
    Validates: Requirements 5.5
    """
    
    def __init__(self, capacity: int = 10) -> None:
        """Initialize ShortTermMemory with a fixed capacity.
        
        Args:
            capacity: Maximum number of items to store (must be > 0)
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError(f"Capacity must be at least 1, got {capacity}")
        
        self._capacity = capacity
        self._items: Deque[MemoryItem] = deque(maxlen=capacity)
    
    @property
    def capacity(self) -> int:
        """Get the maximum capacity of this memory."""
        return self._capacity
    
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add a new item to memory.
        
        If the memory is at capacity, the oldest item is automatically
        removed before adding the new item.
        
        Args:
            content: The content to store
            metadata: Optional metadata about the content
            
        Returns:
            The created MemoryItem
        """
        item = MemoryItem(
            content=content,
            metadata=metadata or {},
        )
        self._items.append(item)
        return item
    
    def get_all(self) -> List[MemoryItem]:
        """Get all items in memory, oldest first.
        
        Returns:
            List of all MemoryItems in order of addition
        """
        return list(self._items)
    
    def get_recent(self, n: int = 5) -> List[MemoryItem]:
        """Get the n most recent items.
        
        Args:
            n: Number of recent items to retrieve
            
        Returns:
            List of the n most recent MemoryItems
        """
        items = list(self._items)
        return items[-n:] if n < len(items) else items
    
    def clear(self) -> None:
        """Clear all items from memory."""
        self._items.clear()
    
    def search(self, query: str) -> List[MemoryItem]:
        """Search for items containing the query string.
        
        Performs a simple case-insensitive substring search.
        
        Args:
            query: The search query
            
        Returns:
            List of MemoryItems containing the query
        """
        query_lower = query.lower()
        return [
            item for item in self._items
            if query_lower in item.content.lower()
        ]
    
    def __len__(self) -> int:
        """Return the number of items in memory."""
        return len(self._items)
    
    def is_full(self) -> bool:
        """Check if memory is at capacity."""
        return len(self._items) >= self._capacity
    
    def to_context_string(self, separator: str = "\n") -> str:
        """Convert memory contents to a context string for LLM prompts.
        
        Args:
            separator: String to use between items
            
        Returns:
            Concatenated string of all memory contents
        """
        return separator.join(item.content for item in self._items)



class LongTermMemory(BaseMemory):
    """Persistent storage for important information.
    
    LongTermMemory stores items persistently to a JSON file, allowing
    information to survive across agent sessions. Items can be tagged
    with importance scores and metadata for better organization and
    retrieval.
    
    Unlike ShortTermMemory, LongTermMemory has no capacity limit and
    persists data to disk automatically.
    
    Attributes:
        storage_path: Path to the JSON file for persistence
        
    Example:
        >>> memory = LongTermMemory(storage_path=Path("./memory.json"))
        >>> memory.add("Important fact", metadata={"category": "facts"})
        >>> memory.save()  # Persist to disk
        >>> 
        >>> # Later, in a new session:
        >>> memory2 = LongTermMemory(storage_path=Path("./memory.json"))
        >>> memory2.load()  # Load from disk
        >>> len(memory2)
        1
    
    Requirements: 5.5 - Memory classes for long-term persistent storage
    """
    
    def __init__(
        self,
        storage_path: Optional[Path] = None,
        auto_save: bool = True,
    ) -> None:
        """Initialize LongTermMemory.
        
        Args:
            storage_path: Path to JSON file for persistence (optional)
            auto_save: Whether to automatically save after each add operation
        """
        self._storage_path = storage_path
        self._auto_save = auto_save
        self._items: List[MemoryItem] = []
        
        # Load existing data if storage path exists
        if storage_path and storage_path.exists():
            self.load()
    
    @property
    def storage_path(self) -> Optional[Path]:
        """Get the storage path for this memory."""
        return self._storage_path
    
    def add(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 0.5,
    ) -> MemoryItem:
        """Add a new item to long-term memory.
        
        Args:
            content: The content to store
            metadata: Optional metadata about the content
            importance: Importance score from 0.0 to 1.0
            
        Returns:
            The created MemoryItem
        """
        item = MemoryItem(
            content=content,
            metadata=metadata or {},
            importance=max(0.0, min(1.0, importance)),  # Clamp to [0, 1]
        )
        self._items.append(item)
        
        if self._auto_save and self._storage_path:
            self.save()
        
        return item
    
    def get_all(self) -> List[MemoryItem]:
        """Get all items in memory.
        
        Returns:
            List of all MemoryItems
        """
        return list(self._items)
    
    def get_by_importance(self, min_importance: float = 0.5) -> List[MemoryItem]:
        """Get items with importance at or above the threshold.
        
        Args:
            min_importance: Minimum importance score (0.0 to 1.0)
            
        Returns:
            List of MemoryItems meeting the importance threshold
        """
        return [
            item for item in self._items
            if item.importance >= min_importance
        ]
    
    def get_by_metadata(self, key: str, value: Any) -> List[MemoryItem]:
        """Get items with matching metadata.
        
        Args:
            key: Metadata key to match
            value: Metadata value to match
            
        Returns:
            List of MemoryItems with matching metadata
        """
        return [
            item for item in self._items
            if item.metadata.get(key) == value
        ]
    
    def clear(self) -> None:
        """Clear all items from memory."""
        self._items.clear()
        if self._auto_save and self._storage_path:
            self.save()
    
    def search(self, query: str) -> List[MemoryItem]:
        """Search for items containing the query string.
        
        Performs a case-insensitive substring search on content.
        
        Args:
            query: The search query
            
        Returns:
            List of MemoryItems containing the query
        """
        query_lower = query.lower()
        return [
            item for item in self._items
            if query_lower in item.content.lower()
        ]
    
    def remove(self, item: MemoryItem) -> bool:
        """Remove a specific item from memory.
        
        Args:
            item: The MemoryItem to remove
            
        Returns:
            True if item was found and removed, False otherwise
        """
        try:
            self._items.remove(item)
            if self._auto_save and self._storage_path:
                self.save()
            return True
        except ValueError:
            return False
    
    def save(self) -> None:
        """Save memory contents to the storage file.
        
        Raises:
            ValueError: If no storage path is configured
        """
        if not self._storage_path:
            raise ValueError("No storage path configured for LongTermMemory")
        
        # Ensure parent directory exists
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "items": [item.to_dict() for item in self._items],
            "saved_at": datetime.now().isoformat(),
        }
        
        with open(self._storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> None:
        """Load memory contents from the storage file.
        
        Raises:
            ValueError: If no storage path is configured
            FileNotFoundError: If the storage file doesn't exist
        """
        if not self._storage_path:
            raise ValueError("No storage path configured for LongTermMemory")
        
        if not self._storage_path.exists():
            raise FileNotFoundError(f"Storage file not found: {self._storage_path}")
        
        with open(self._storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self._items = [
            MemoryItem.from_dict(item_data)
            for item_data in data.get("items", [])
        ]
    
    def __len__(self) -> int:
        """Return the number of items in memory."""
        return len(self._items)



class SummarizationMemory(BaseMemory):
    """Memory that compresses context using LLM summarization.
    
    SummarizationMemory maintains a running summary of all added content,
    using an LLM to compress information when the buffer exceeds a
    threshold. This allows agents to maintain context over long
    conversations without exceeding token limits.
    
    The memory works by:
    1. Accumulating new items in a buffer
    2. When buffer exceeds threshold, summarizing buffer + existing summary
    3. Replacing the summary with the new compressed version
    
    Attributes:
        llm: The LLM provider for generating summaries
        buffer_size: Number of items before triggering summarization
        
    Example:
        >>> from src.services.llm import MockLLM
        >>> memory = SummarizationMemory(llm=MockLLM(), buffer_size=5)
        >>> for i in range(10):
        ...     memory.add(f"Event {i} happened")
        >>> # After 5 items, summarization is triggered
        >>> print(memory.get_summary())
    
    Requirements: 5.5 - Memory classes for summarization memory patterns
    """
    
    # Default prompt template for summarization
    SUMMARIZATION_PROMPT = """Summarize the following conversation/context into a concise summary.
Preserve key facts, decisions, and important details.
Keep the summary under 200 words.

Previous Summary:
{previous_summary}

New Content:
{new_content}

Provide a consolidated summary:"""
    
    def __init__(
        self,
        llm: LLMProvider,
        buffer_size: int = 5,
        max_summary_tokens: int = 500,
    ) -> None:
        """Initialize SummarizationMemory.
        
        Args:
            llm: The LLM provider for generating summaries
            buffer_size: Number of items before triggering summarization
            max_summary_tokens: Target maximum tokens for the summary
            
        Raises:
            ValueError: If buffer_size is less than 1
        """
        if buffer_size < 1:
            raise ValueError(f"Buffer size must be at least 1, got {buffer_size}")
        
        self._llm = llm
        self._buffer_size = buffer_size
        self._max_summary_tokens = max_summary_tokens
        
        self._buffer: List[MemoryItem] = []
        self._summary: str = ""
        self._all_items: List[MemoryItem] = []  # Keep track of all items for get_all()
        self._summarization_count: int = 0
    
    @property
    def buffer_size(self) -> int:
        """Get the buffer size threshold for summarization."""
        return self._buffer_size
    
    @property
    def summary(self) -> str:
        """Get the current summary."""
        return self._summary
    
    @property
    def summarization_count(self) -> int:
        """Get the number of times summarization has been performed."""
        return self._summarization_count
    
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add a new item to memory.
        
        If the buffer exceeds the threshold, summarization is triggered
        synchronously. For async summarization, use add_async().
        
        Args:
            content: The content to store
            metadata: Optional metadata about the content
            
        Returns:
            The created MemoryItem
        """
        item = MemoryItem(
            content=content,
            metadata=metadata or {},
        )
        self._buffer.append(item)
        self._all_items.append(item)
        
        # Note: Synchronous add doesn't trigger summarization
        # Use add_async() or manually call summarize_async() for compression
        
        return item
    
    async def add_async(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        """Add a new item to memory with async summarization.
        
        If the buffer exceeds the threshold, summarization is triggered
        automatically.
        
        Args:
            content: The content to store
            metadata: Optional metadata about the content
            
        Returns:
            The created MemoryItem
        """
        item = self.add(content, metadata)
        
        # Check if we need to summarize
        if len(self._buffer) >= self._buffer_size:
            await self.summarize_async()
        
        return item
    
    async def summarize_async(self) -> str:
        """Summarize the current buffer and update the summary.
        
        This compresses the buffer contents into the running summary
        and clears the buffer.
        
        Returns:
            The new summary
        """
        if not self._buffer:
            return self._summary
        
        # Build the content to summarize
        new_content = "\n".join(item.content for item in self._buffer)
        
        # Build the prompt
        prompt = self.SUMMARIZATION_PROMPT.format(
            previous_summary=self._summary if self._summary else "No previous summary.",
            new_content=new_content,
        )
        
        # Generate the summary
        self._summary = await self._llm.complete(prompt)
        self._summarization_count += 1
        
        # Clear the buffer
        self._buffer.clear()
        
        return self._summary
    
    def get_summary(self) -> str:
        """Get the current summary including unsummarized buffer content.
        
        Returns:
            The summary combined with any buffered content
        """
        if not self._buffer:
            return self._summary
        
        buffer_content = "\n".join(item.content for item in self._buffer)
        
        if self._summary:
            return f"{self._summary}\n\nRecent:\n{buffer_content}"
        return buffer_content
    
    def get_all(self) -> List[MemoryItem]:
        """Get all items that have been added to memory.
        
        Note: This returns all original items, not the summarized content.
        
        Returns:
            List of all MemoryItems
        """
        return list(self._all_items)
    
    def get_buffer(self) -> List[MemoryItem]:
        """Get items currently in the buffer (not yet summarized).
        
        Returns:
            List of buffered MemoryItems
        """
        return list(self._buffer)
    
    def clear(self) -> None:
        """Clear all memory including summary and buffer."""
        self._buffer.clear()
        self._all_items.clear()
        self._summary = ""
        self._summarization_count = 0
    
    def clear_buffer(self) -> None:
        """Clear only the buffer, keeping the summary."""
        self._buffer.clear()
    
    def search(self, query: str) -> List[MemoryItem]:
        """Search for items containing the query string.
        
        Searches both the buffer and all historical items.
        
        Args:
            query: The search query
            
        Returns:
            List of MemoryItems containing the query
        """
        query_lower = query.lower()
        return [
            item for item in self._all_items
            if query_lower in item.content.lower()
        ]
    
    def __len__(self) -> int:
        """Return the total number of items added to memory."""
        return len(self._all_items)
    
    def to_context_string(self) -> str:
        """Convert memory to a context string for LLM prompts.
        
        Returns the summary plus any buffered content.
        
        Returns:
            Context string suitable for LLM prompts
        """
        return self.get_summary()

