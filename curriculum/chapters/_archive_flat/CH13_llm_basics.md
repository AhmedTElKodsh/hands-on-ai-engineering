# Chapter 13: LLM Basics & Mock Client

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-12  
**AITEA Component:** `src/services/llm.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Explain how Large Language Models (LLMs) work at a high level
2. Understand tokens, temperature, and context windows
3. Implement a MockLLM for learning without API keys
4. Create an LLM provider abstraction for multiple backends
5. Use the no-key fallback pattern for development

## 13.1 What Are LLMs?

Large Language Models are neural networks trained on vast amounts of text to predict the next token in a sequence. Key concepts:

**Tokens**: LLMs don't see words—they see tokens (subword units):

- "Hello" → 1 token
- "authentication" → might be 2-3 tokens
- Roughly 4 characters ≈ 1 token

**Temperature**: Controls randomness in outputs:

- 0.0 = Deterministic (same input → same output)
- 0.7 = Balanced creativity
- 1.0+ = More random/creative

**Context Window**: Maximum tokens the model can process:

- GPT-4: 8K-128K tokens
- Claude: 100K-200K tokens
- Affects how much history/context you can include

## 13.2 The LLM Provider Abstraction

AITEA supports multiple LLM providers through a common interface:

```python
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, List
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """A message in a chat conversation."""
    role: str  # "system", "user", or "assistant"
    content: str


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    All providers (OpenAI, Anthropic, Bedrock, Mock) implement
    this interface for consistent behavior.
    """

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion for the given prompt."""
        ...

    @abstractmethod
    async def chat(self, messages: List[ChatMessage], **kwargs: Any) -> str:
        """Generate a response for a chat conversation."""
        ...

    @abstractmethod
    async def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        ...
```

**Why an abstraction?**

- Swap providers without changing application code
- Test with MockLLM, deploy with real providers
- Handle provider-specific quirks in one place

## 13.3 The MockLLM Implementation

MockLLM provides deterministic responses for learning without API keys:

```python
import json
from typing import Any, AsyncIterator, Dict, List


class MockLLM(LLMProvider):
    """Deterministic LLM simulator for no-key learning.

    Provides predefined responses for common AITEA tasks:
    - extract_features: Extract features from descriptions
    - estimate_project: Generate time estimates
    - parse_brd: Parse Business Requirements Documents
    """

    RESPONSES: Dict[str, Dict[str, Any]] = {
        "extract_features": {
            "default": {
                "features": [
                    {"name": "User Authentication", "team": "backend", "estimated_hours": 8},
                    {"name": "User Registration", "team": "backend", "estimated_hours": 6},
                    {"name": "Password Reset", "team": "backend", "estimated_hours": 4},
                ]
            },
            "crud": {
                "features": [
                    {"name": "CRUD API", "team": "backend", "estimated_hours": 4},
                    {"name": "Data Validation", "team": "backend", "estimated_hours": 2},
                ]
            },
        },
        "estimate_project": {
            "default": {
                "total_hours": 40,
                "confidence": "medium",
                "breakdown": [
                    {"feature": "Backend API", "hours": 16},
                    {"feature": "Frontend UI", "hours": 12},
                    {"feature": "Testing", "hours": 8},
                ]
            },
        },
    }

    def __init__(self) -> None:
        self._call_count: int = 0

    def _detect_task_type(self, text: str) -> str:
        """Detect task type from input text."""
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["extract", "feature", "identify"]):
            return "extract_features"
        elif any(kw in text_lower for kw in ["estimate", "time", "hours"]):
            return "estimate_project"
        elif any(kw in text_lower for kw in ["brd", "business requirement"]):
            return "parse_brd"

        return "extract_features"

    def _detect_variant(self, text: str, task_type: str) -> str:
        """Detect response variant based on input."""
        text_lower = text.lower()

        if task_type == "extract_features":
            if "crud" in text_lower:
                return "crud"

        return "default"

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a deterministic completion."""
        self._call_count += 1

        task_type = self._detect_task_type(prompt)
        variant = self._detect_variant(prompt, task_type)

        response = self.RESPONSES.get(task_type, {}).get(variant, {})
        return json.dumps(response, indent=2)

    async def chat(self, messages: List[ChatMessage], **kwargs: Any) -> str:
        """Generate response from last user message."""
        self._call_count += 1

        # Find last user message
        user_content = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_content = msg.content
                break

        task_type = self._detect_task_type(user_content)
        variant = self._detect_variant(user_content, task_type)

        response = self.RESPONSES.get(task_type, {}).get(variant, {})
        return json.dumps(response, indent=2)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """Simulate streaming by yielding chunks."""
        import asyncio

        response = await self.complete(prompt)

        # Yield in chunks of ~10 characters
        chunk_size = 10
        for i in range(0, len(response), chunk_size):
            yield response[i:i + chunk_size]
            await asyncio.sleep(0.01)  # Simulate latency

    def count_tokens(self, text: str) -> int:
        """Estimate tokens (~4 chars per token)."""
        return len(text) // 4 + 1

    @property
    def call_count(self) -> int:
        """Number of calls made to this instance."""
        return self._call_count
```

## 13.4 The No-Key Fallback Pattern

AITEA automatically falls back to MockLLM when no API keys are set:

```python
import os
import warnings
from typing import Any, Dict


MOCK_MODE_WARNING = """
╔══════════════════════════════════════════════════════════════════╗
║                    ⚠️  MOCK LLM MODE ACTIVE                      ║
╠══════════════════════════════════════════════════════════════════╣
║  No API keys detected. Using MockLLM with predefined responses.  ║
║                                                                  ║
║  To use a real LLM provider, set one of these environment vars:  ║
║    • OPENAI_API_KEY     - For OpenAI GPT models                  ║
║    • ANTHROPIC_API_KEY  - For Anthropic Claude models            ║
║    • AWS_ACCESS_KEY_ID  - For AWS Bedrock models                 ║
╚══════════════════════════════════════════════════════════════════╝
"""


def _check_api_keys() -> Dict[str, bool]:
    """Check which API keys are available."""
    return {
        "openai": bool(os.environ.get("OPENAI_API_KEY")),
        "anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "bedrock": bool(
            os.environ.get("AWS_ACCESS_KEY_ID") and
            os.environ.get("AWS_SECRET_ACCESS_KEY")
        ),
    }


def get_llm_provider(
    provider: str = "auto",
    show_warning: bool = True,
    **kwargs: Any
) -> LLMProvider:
    """Get an LLM provider based on available API keys.

    Args:
        provider: "auto", "mock", "openai", "anthropic", or "bedrock"
        show_warning: Whether to display mock mode warning
        **kwargs: Provider-specific parameters (model, temperature, etc.)

    Returns:
        An LLMProvider instance

    Example:
        >>> # Auto-select based on available keys
        >>> llm = get_llm_provider()

        >>> # Explicitly use MockLLM for testing
        >>> llm = get_llm_provider("mock", show_warning=False)
    """
    available_keys = _check_api_keys()

    if provider == "mock":
        if show_warning:
            print(MOCK_MODE_WARNING)
        return MockLLM()

    if provider == "auto":
        if available_keys["openai"]:
            from .providers import OpenAIProvider
            return OpenAIProvider(**kwargs)
        elif available_keys["anthropic"]:
            from .providers import AnthropicProvider
            return AnthropicProvider(**kwargs)
        elif available_keys["bedrock"]:
            from .providers import BedrockProvider
            return BedrockProvider(**kwargs)

        # No keys found - use MockLLM
        if show_warning:
            print(MOCK_MODE_WARNING)
        return MockLLM()

    # Handle explicit provider requests...
    raise ValueError(f"Unknown provider: {provider}")
```

## 13.5 Using the LLM Provider

```python
import asyncio
from src.services.llm import get_llm_provider, ChatMessage


async def main():
    # Get provider (auto-selects based on available keys)
    llm = get_llm_provider()

    # Simple completion
    response = await llm.complete("Extract features from: User login system")
    print(response)

    # Chat-style interaction
    messages = [
        ChatMessage(role="system", content="You are a project analyst."),
        ChatMessage(role="user", content="What features are in a shopping cart?"),
    ]
    response = await llm.chat(messages)
    print(response)

    # Streaming response
    print("Streaming: ", end="")
    async for chunk in llm.stream("Estimate time for CRUD API"):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
```

## 13.6 Your Turn: Exercise 13.1

Add a new task type to MockLLM for "summarize" operations:

```python
# Add to RESPONSES dictionary
"summarize": {
    "default": {
        "summary": "This is a summary of the provided content.",
        "key_points": ["Point 1", "Point 2", "Point 3"],
        "word_count": 150
    }
}

# Update _detect_task_type to recognize summarization requests
# Keywords: "summarize", "summary", "tldr", "brief"
```

## 13.7 Debugging Scenario

**The Bug:** MockLLM returns empty responses.

```python
llm = MockLLM()
response = await llm.complete("Tell me about Python")
print(response)  # {}
```

**The Problem:** The prompt doesn't match any task type keywords.

**The Fix:** Either:

1. Use keywords that match task types ("extract features from Python")
2. Add a fallback response for unrecognized prompts:

```python
def _get_response(self, text: str) -> Dict[str, Any]:
    task_type = self._detect_task_type(text)
    variant = self._detect_variant(text, task_type)

    task_responses = self.RESPONSES.get(task_type, {})
    response = task_responses.get(variant, task_responses.get("default", {}))

    # Fallback for completely unrecognized prompts
    if not response:
        return {"response": "Mock response for: " + text[:50]}

    return response
```

## 13.8 Quick Check Questions

1. What is a token in the context of LLMs?
2. What does temperature=0 mean for LLM outputs?
3. Why use an abstract base class for LLM providers?
4. When does `get_llm_provider()` return a MockLLM?
5. How does MockLLM determine which response to return?

<details>
<summary>Answers</summary>

1. A subword unit that LLMs process—roughly 4 characters on average
2. Deterministic output—same input always produces same output
3. To swap providers without changing application code and enable testing
4. When no API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, AWS credentials) are set
5. By detecting keywords in the prompt that match task types (extract, estimate, brd)

</details>

## 13.9 Mini-Project: Token Counter

Implement a more accurate token counter using tiktoken (OpenAI's tokenizer):

```python
# Install: pip install tiktoken

import tiktoken

class TokenCounter:
    """Count tokens for different model families."""

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def truncate(self, text: str, max_tokens: int) -> str:
        """Truncate text to max_tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])


# Usage
counter = TokenCounter("gpt-4")
text = "Hello, how are you today?"
print(f"Tokens: {counter.count(text)}")  # ~6 tokens
```

## 13.10 AITEA Integration

This chapter implements:

- **Requirement 3.1**: MockLLM class with predefined response map
- **Requirement 13.1**: LLM provider abstraction
- **Requirement 13.2**: Mock mode warning display
- **Requirement 13.3**: Deterministic MockLLM responses
- **Requirement 13.4**: API key checking with `get_llm_provider()`

**Verification:**

```python
# Test MockLLM
import asyncio
from src.services.llm import get_llm_provider

async def test_mock():
    llm = get_llm_provider("mock", show_warning=False)

    # Test feature extraction
    response = await llm.complete("Extract features from: CRUD API")
    print("Feature extraction:", response)

    # Test estimation
    response = await llm.complete("Estimate time for this project")
    print("Estimation:", response)

    # Verify determinism
    r1 = await llm.complete("Extract features")
    r2 = await llm.complete("Extract features")
    assert r1 == r2, "MockLLM should be deterministic"
    print("✅ Determinism verified")

asyncio.run(test_mock())
```

## What's Next

In Chapter 14, you'll learn prompt engineering—how to craft effective prompts using templates, few-shot examples, and chain-of-thought patterns.

**Before proceeding:**

- Understand the LLMProvider interface
- Test MockLLM with different prompts
- Try the token counter mini-project
