# Chapter 21: Memory Patterns

**Difficulty:** Intermediate  
**Time:** 2.5 hours  
**Prerequisites:** Chapters 18-20  
**AITEA Component:** `src/agents/memory.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Implement ShortTermMemory with capacity limits
2. Create LongTermMemory with persistence
3. Build SummarizationMemory for context compression
4. Choose the right memory type for different use cases
5. Integrate memory with agents

## 21.1 Why Agents Need Memory

Without memory, agents:

- Forget previous interactions
- Repeat the same mistakes
- Can't learn from experience
- Lose context in long conversations

```
# Without memory
User: "My name is Alice"
Agent: "Nice to meet you, Alice!"
User: "What's my name?"
Agent: "I don't know your name."  # Forgot!

# With memory
User: "My name is Alice"
Agent: "Nice to meet you, Alice!" [Stores: user_name=Alice]
User: "What's my name?"
Agent: "Your name is Alice."  # Remembers!
```

## 21.2 Memory Types

| Type                    | Capacity     | Persistence  | Use Case           |
| ----------------------- | ------------ | ------------ | ------------------ |
| **ShortTermMemory**     | Fixed (FIFO) | Session only | Recent context     |
| **LongTermMemory**      | Unlimited    | Disk/DB      | Important facts    |
| **SummarizationMemory** | Compressed   | Session      | Long conversations |

## 21.3 The MemoryItem Class

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class MemoryItem:
    """A single item stored in memory."""
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "importance": self.importance,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        return cls(
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
            importance=data.get("importance", 0.5),
        )
```

## 21.4 ShortTermMemory

Fixed-capacity memory using FIFO eviction:

```python
from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, List


class BaseMemory(ABC):
    """Abstract base class for memory implementations."""

    @abstractmethod
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        ...

    @abstractmethod
    def get_all(self) -> List[MemoryItem]:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @abstractmethod
    def search(self, query: str) -> List[MemoryItem]:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...


class ShortTermMemory(BaseMemory):
    """Fixed-capacity memory with FIFO eviction.

    When capacity is reached, oldest items are removed.

    Example:
        >>> memory = ShortTermMemory(capacity=3)
        >>> memory.add("First")
        >>> memory.add("Second")
        >>> memory.add("Third")
        >>> memory.add("Fourth")  # Removes "First"
        >>> len(memory)
        3
    """

    def __init__(self, capacity: int = 10) -> None:
        if capacity < 1:
            raise ValueError(f"Capacity must be >= 1, got {capacity}")
        self._capacity = capacity
        self._items: Deque[MemoryItem] = deque(maxlen=capacity)

    @property
    def capacity(self) -> int:
        return self._capacity

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        item = MemoryItem(content=content, metadata=metadata or {})
        self._items.append(item)
        return item

    def get_all(self) -> List[MemoryItem]:
        return list(self._items)

    def get_recent(self, n: int = 5) -> List[MemoryItem]:
        """Get n most recent items."""
        items = list(self._items)
        return items[-n:] if n < len(items) else items

    def clear(self) -> None:
        self._items.clear()

    def search(self, query: str) -> List[MemoryItem]:
        """Case-insensitive substring search."""
        query_lower = query.lower()
        return [item for item in self._items if query_lower in item.content.lower()]

    def __len__(self) -> int:
        return len(self._items)

    def is_full(self) -> bool:
        return len(self._items) >= self._capacity

    def to_context_string(self, separator: str = "\n") -> str:
        """Convert to string for LLM context."""
        return separator.join(item.content for item in self._items)
```

## 21.5 LongTermMemory

Persistent storage with importance scoring:

```python
import json
from pathlib import Path


class LongTermMemory(BaseMemory):
    """Persistent memory with importance scoring.

    Stores items to JSON file for persistence across sessions.

    Example:
        >>> memory = LongTermMemory(storage_path=Path("memory.json"))
        >>> memory.add("User prefers backend team", importance=0.9)
        >>> memory.save()
        >>> # Later...
        >>> memory.load()
        >>> memory.get_by_importance(0.8)  # High importance items
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        auto_save: bool = True,
    ) -> None:
        self._storage_path = storage_path
        self._auto_save = auto_save
        self._items: List[MemoryItem] = []

        if storage_path and storage_path.exists():
            self.load()

    def add(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 0.5,
    ) -> MemoryItem:
        item = MemoryItem(
            content=content,
            metadata=metadata or {},
            importance=max(0.0, min(1.0, importance)),
        )
        self._items.append(item)

        if self._auto_save and self._storage_path:
            self.save()

        return item

    def get_all(self) -> List[MemoryItem]:
        return list(self._items)

    def get_by_importance(self, min_importance: float = 0.5) -> List[MemoryItem]:
        """Get items with importance >= threshold."""
        return [item for item in self._items if item.importance >= min_importance]

    def get_by_metadata(self, key: str, value: Any) -> List[MemoryItem]:
        """Get items with matching metadata."""
        return [item for item in self._items if item.metadata.get(key) == value]

    def clear(self) -> None:
        self._items.clear()
        if self._auto_save and self._storage_path:
            self.save()

    def search(self, query: str) -> List[MemoryItem]:
        query_lower = query.lower()
        return [item for item in self._items if query_lower in item.content.lower()]

    def remove(self, item: MemoryItem) -> bool:
        """Remove specific item."""
        try:
            self._items.remove(item)
            if self._auto_save and self._storage_path:
                self.save()
            return True
        except ValueError:
            return False

    def save(self) -> None:
        """Save to storage file."""
        if not self._storage_path:
            raise ValueError("No storage path configured")

        self._storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "items": [item.to_dict() for item in self._items],
            "saved_at": datetime.now().isoformat(),
        }

        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load from storage file."""
        if not self._storage_path or not self._storage_path.exists():
            return

        with open(self._storage_path) as f:
            data = json.load(f)

        self._items = [MemoryItem.from_dict(d) for d in data.get("items", [])]

    def __len__(self) -> int:
        return len(self._items)
```

## 21.6 SummarizationMemory

Compresses context using LLM summarization:

```python
from src.services.llm import LLMProvider


class SummarizationMemory(BaseMemory):
    """Memory that compresses context via summarization.

    Maintains a running summary, compressing when buffer exceeds threshold.

    Example:
        >>> memory = SummarizationMemory(llm=MockLLM(), buffer_size=5)
        >>> for i in range(10):
        ...     await memory.add_async(f"Event {i}")
        >>> # After 5 items, summarization triggers
        >>> print(memory.get_summary())
    """

    SUMMARIZATION_PROMPT = """Summarize the following into a concise summary.
Preserve key facts and important details.

Previous Summary:
{previous_summary}

New Content:
{new_content}

Consolidated summary:"""

    def __init__(
        self,
        llm: LLMProvider,
        buffer_size: int = 5,
    ) -> None:
        if buffer_size < 1:
            raise ValueError(f"Buffer size must be >= 1")

        self._llm = llm
        self._buffer_size = buffer_size
        self._buffer: List[MemoryItem] = []
        self._summary: str = ""
        self._all_items: List[MemoryItem] = []
        self._summarization_count: int = 0

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def summarization_count(self) -> int:
        return self._summarization_count

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add item (sync, no auto-summarization)."""
        item = MemoryItem(content=content, metadata=metadata or {})
        self._buffer.append(item)
        self._all_items.append(item)
        return item

    async def add_async(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add item with auto-summarization when buffer is full."""
        item = self.add(content, metadata)

        if len(self._buffer) >= self._buffer_size:
            await self.summarize_async()

        return item

    async def summarize_async(self) -> str:
        """Summarize buffer into running summary."""
        if not self._buffer:
            return self._summary

        new_content = "\n".join(item.content for item in self._buffer)

        prompt = self.SUMMARIZATION_PROMPT.format(
            previous_summary=self._summary or "No previous summary.",
            new_content=new_content,
        )

        self._summary = await self._llm.complete(prompt)
        self._summarization_count += 1
        self._buffer.clear()

        return self._summary

    def get_summary(self) -> str:
        """Get summary + any unsummarized buffer content."""
        if not self._buffer:
            return self._summary

        buffer_content = "\n".join(item.content for item in self._buffer)

        if self._summary:
            return f"{self._summary}\n\nRecent:\n{buffer_content}"
        return buffer_content

    def get_all(self) -> List[MemoryItem]:
        return list(self._all_items)

    def get_buffer(self) -> List[MemoryItem]:
        """Get unsummarized items."""
        return list(self._buffer)

    def clear(self) -> None:
        self._buffer.clear()
        self._all_items.clear()
        self._summary = ""
        self._summarization_count = 0

    def search(self, query: str) -> List[MemoryItem]:
        query_lower = query.lower()
        return [item for item in self._all_items if query_lower in item.content.lower()]

    def __len__(self) -> int:
        return len(self._all_items)

    def to_context_string(self) -> str:
        """Get context string for LLM prompts."""
        return self.get_summary()
```

## 21.7 Integrating Memory with Agents

```python
from src.agents.simple_agent import SimpleAgent


class MemoryAgent(SimpleAgent):
    """Agent with memory capabilities."""

    def __init__(
        self,
        llm: LLMProvider,
        short_term: Optional[ShortTermMemory] = None,
        long_term: Optional[LongTermMemory] = None,
        **kwargs
    ):
        super().__init__(llm, **kwargs)
        self.short_term = short_term or ShortTermMemory(capacity=10)
        self.long_term = long_term

    async def _observe(self) -> str:
        """Observe with memory context."""
        self._transition_to(AgentState.OBSERVE, message="Observing with memory")

        # Build context from memory
        memory_context = ""
        if self.short_term:
            recent = self.short_term.to_context_string()
            if recent:
                memory_context += f"\nRecent context:\n{recent}"

        if self.long_term:
            important = self.long_term.get_by_importance(0.7)
            if important:
                facts = "\n".join(f"- {item.content}" for item in important)
                memory_context += f"\nImportant facts:\n{facts}"

        prompt = f"""Task: {self._context.task}
{memory_context}

What do you observe?"""

        observation = await self.llm.complete(prompt)
        self._context.add_observation(observation)

        # Store in short-term memory
        self.short_term.add(f"Observed: {observation[:100]}...")

        return observation

    def remember(self, content: str, importance: float = 0.5) -> None:
        """Store something in long-term memory."""
        if self.long_term:
            self.long_term.add(content, importance=importance)

    def recall(self, query: str) -> List[MemoryItem]:
        """Search both memory types."""
        results = []
        if self.short_term:
            results.extend(self.short_term.search(query))
        if self.long_term:
            results.extend(self.long_term.search(query))
        return results
```

## 21.8 Your Turn: Exercise 21.1

Implement a memory that combines all three types:

```python
class HybridMemory:
    """Combines short-term, long-term, and summarization memory."""

    def __init__(
        self,
        llm: LLMProvider,
        short_term_capacity: int = 10,
        summarize_threshold: int = 5,
        storage_path: Optional[Path] = None,
    ):
        self.short_term = ShortTermMemory(capacity=short_term_capacity)
        self.long_term = LongTermMemory(storage_path=storage_path)
        self.summarization = SummarizationMemory(llm=llm, buffer_size=summarize_threshold)

    async def add(self, content: str, importance: float = 0.5) -> None:
        """Add to appropriate memory based on importance."""
        # Always add to short-term
        self.short_term.add(content)

        # Add to summarization for context compression
        await self.summarization.add_async(content)

        # High importance goes to long-term
        if importance >= 0.7:
            self.long_term.add(content, importance=importance)

    def get_context(self) -> str:
        """Get combined context for LLM."""
        parts = []

        # Summary of conversation
        summary = self.summarization.get_summary()
        if summary:
            parts.append(f"Conversation summary:\n{summary}")

        # Recent items
        recent = self.short_term.get_recent(3)
        if recent:
            parts.append(f"Recent:\n" + "\n".join(f"- {r.content}" for r in recent))

        # Important facts
        important = self.long_term.get_by_importance(0.7)
        if important:
            parts.append(f"Key facts:\n" + "\n".join(f"- {i.content}" for i in important))

        return "\n\n".join(parts)
```

## 21.9 Debugging Scenario

**The Bug:** Memory fills up but old items aren't removed.

```python
memory = ShortTermMemory(capacity=3)
for i in range(10):
    memory.add(f"Item {i}")
print(len(memory))  # Expected: 3, Got: 10
```

**The Problem:** Using a regular list instead of deque with maxlen.

**The Fix:** Ensure deque is initialized with maxlen:

```python
def __init__(self, capacity: int = 10) -> None:
    self._capacity = capacity
    # CORRECT: deque with maxlen auto-evicts
    self._items: Deque[MemoryItem] = deque(maxlen=capacity)

    # WRONG: Regular list doesn't auto-evict
    # self._items: List[MemoryItem] = []
```

## 21.10 Quick Check Questions

1. What eviction policy does ShortTermMemory use?
2. How does LongTermMemory persist data?
3. When does SummarizationMemory compress content?
4. What's the importance score range?
5. Why use different memory types together?

<details>
<summary>Answers</summary>

1. FIFO (First-In-First-Out) - oldest items removed first
2. JSON file storage with save/load methods
3. When buffer reaches buffer_size threshold
4. 0.0 to 1.0 (clamped in add method)
5. Different retention needs: recent context, important facts, compressed history

</details>

## 21.11 AITEA Integration

This chapter implements:

- **Requirement 5.5**: Memory classes for short-term, long-term, summarization
- **Property 10**: Memory Capacity Constraints

**Verification:**

```python
import asyncio
from pathlib import Path
from src.agents.memory import ShortTermMemory, LongTermMemory, SummarizationMemory
from src.services.llm import get_llm_provider


async def test_memory():
    # Test ShortTermMemory capacity
    stm = ShortTermMemory(capacity=3)
    for i in range(5):
        stm.add(f"Item {i}")
    assert len(stm) == 3, f"Expected 3, got {len(stm)}"
    assert stm.get_all()[0].content == "Item 2"  # Oldest remaining
    print("✅ ShortTermMemory capacity verified")

    # Test LongTermMemory persistence
    path = Path("test_memory.json")
    ltm = LongTermMemory(storage_path=path)
    ltm.add("Important fact", importance=0.9)
    ltm.save()

    ltm2 = LongTermMemory(storage_path=path)
    ltm2.load()
    assert len(ltm2) == 1
    print("✅ LongTermMemory persistence verified")
    path.unlink()  # Cleanup

    # Test SummarizationMemory
    llm = get_llm_provider("mock", show_warning=False)
    sm = SummarizationMemory(llm=llm, buffer_size=3)
    for i in range(5):
        await sm.add_async(f"Event {i}")
    assert sm.summarization_count >= 1
    print("✅ SummarizationMemory compression verified")


asyncio.run(test_memory())
```

## What's Next

In Chapter 22, you'll implement guardrails and safety checks to protect agents from prompt injection and unsafe tool usage.

**Before proceeding:**

- Experiment with different capacity settings
- Test persistence with LongTermMemory
- Try the HybridMemory implementation
