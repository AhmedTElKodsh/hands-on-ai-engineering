# Application Scaffolding Pattern

**Pattern Type**: Application (API Integration Chapters)
**Source**: Chapter 38 - Hybrid Search & Reranking
**Date**: 2026-01-23
**Version**: 1.0

---

## When to Use This Pattern

**Chapter Characteristics**:

- External API dependencies (OpenAI, ChromaDB, LlamaIndex, etc.)
- Multi-step workflows (load → process → store → retrieve)
- Integration complexity (combining multiple libraries)
- Error handling for API failures

**Example Chapters**:

- Chapter 17: First RAG System (OpenAI + ChromaDB + LangChain)
- Chapter 38: Hybrid Search & Reranking (LlamaIndex + BM25 + Reranking)
- Chapters 7-12: LLM API calls
- Chapters 17-22: RAG systems

---

## Scaffolding Template

### Function Signature Pattern

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    [One-line description of what function does]

    [Optional: 2-3 sentences explaining the pattern/approach]

    TODO: Implement this function
    HINT: [Step 1 - High-level approach]
    HINT: [Step 2 - Specific API/library to use with method name]
    HINT: [Step 3 - Response structure and how to navigate it]
    HINT: [Step 4 - How to extract/return the desired data]
    HINT: [Step 5 - Error handling strategy (optional)]

    Args:
        param1: [Description of parameter]
        param2: [Description of parameter]

    Returns:
        ReturnType: [Description of return value]

    Raises:
        [API-specific exceptions]
        [Network/timeout exceptions]

    Example:
        >>> result = function_name(arg1, arg2)
        >>> print(result)
        [Expected output]
    """
    pass  # Your code here
```

### Solution Section Pattern

````markdown
<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
[Complete working implementation with comments]
```
````

**Why this implementation works**:

1. **[Pattern/Technique 1]**: [Explanation]
2. **[Pattern/Technique 2]**: [Explanation]
3. **[Pattern/Technique 3]**: [Explanation]
4. **[Key Insight]**: [Why this approach is correct]

**Key Pattern**: [Name the pattern being demonstrated]

[Optional: Performance notes, common pitfalls, alternatives]

</details>
```

---

## HINT Writing Guidelines for Application Chapters

### HINT Structure (5-Step Pattern)

**HINT 1: High-Level Approach**

- Describe the overall strategy
- Example: "Create sample documents and build an index"

**HINT 2: Specific API/Library**

- Name the exact library and method to use
- Example: "Use VectorStoreIndex.from_documents(docs)"

**HINT 3: Response Structure**

- Explain what the API returns
- Example: "Response structure: response.data[0].embedding"

**HINT 4: Data Extraction**

- Show how to get the desired result
- Example: "Extract embeddings using list comprehension"

**HINT 5: Error Handling (Optional)**

- Suggest error handling strategy
- Example: "Handle RateLimitError by waiting and retrying"

### HINT Quality Checklist

- [ ] Specific, not generic ("Use requests.get()" not "Make API call")
- [ ] Mentions exact method names from the API
- [ ] Includes parameter names when helpful
- [ ] Explains response structure when non-obvious
- [ ] Suggests error types to catch
- [ ] Progressive (each hint builds on previous)

---

## Type Hint Guidelines for Application Chapters

### Required Type Hints

1. **All Parameters**: Include type for every parameter
2. **Return Types**: Always specify return type
3. **API Response Types**: Use TypedDict or Protocol when available
4. **Optional Parameters**: Use `Optional[T]` or `T | None`
5. **Collections**: Use specific types (`list[str]` not `list`)

### Example Type Hints

```python
from typing import Optional, List, Dict, Any
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.retrievers import QueryFusionRetriever

def create_index(
    documents: List[Document],
    chunk_size: int = 512,
    chunk_overlap: int = 50
) -> VectorStoreIndex:
    """Create vector index from documents."""
    pass

def search(
    index: VectorStoreIndex,
    query: str,
    top_k: int = 5
) -> List[Document]:
    """Search index for relevant documents."""
    pass

def process_results(
    results: List[Document],
    format: Optional[str] = None
) -> Dict[str, Any]:
    """Process search results into structured format."""
    pass
```

---

## Test Structure for Application Chapters

### Test Categories

**1. Function Existence Tests**

```python
def test_function_exists():
    """Test that function exists and is callable."""
    try:
        from module import function_name
        assert callable(function_name)
    except ImportError:
        pytest.skip("Module not yet created")
```

**2. Return Type Tests**

```python
def test_function_returns_correct_type():
    """Test that function returns expected type."""
    try:
        from module import function_name
        result = function_name(args)
        assert isinstance(result, ExpectedType)
    except (ImportError, NotImplementedError):
        pytest.skip("Function not yet implemented")
```

**3. Integration Tests**

```python
def test_function_with_real_api():
    """Test function with actual API calls."""
    try:
        from module import function_name
        result = function_name(real_args)

        # Verify result structure
        assert hasattr(result, 'expected_attribute')

        # Verify result content
        assert len(result) > 0

    except ImportError:
        pytest.skip("Dependencies not installed")
```

**4. Error Handling Tests**

```python
def test_function_handles_api_errors():
    """Test that function handles API errors gracefully."""
    try:
        from module import function_name

        # Test with invalid input that should trigger error
        result = function_name(invalid_args)

        # Should handle error, not crash
        assert result is not None or result == expected_error_value

    except ImportError:
        pytest.skip("Function not yet implemented")
```

### Test File Template

```python
"""
Test suite for Chapter X: [Chapter Title]

Tests verify that students can implement:
1. [Key functionality 1]
2. [Key functionality 2]
3. [Property/Correctness requirement]

These tests are designed to run with stub implementations (will fail until implemented).
"""

import pytest
from typing import List
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class Test[FunctionalityName]:
    """Tests for [functionality] implementation."""

    def test_function_exists(self):
        """Test that function exists."""
        try:
            from module import function_name
            assert callable(function_name)
        except ImportError:
            pytest.skip("Module not yet created")

    def test_function_returns_correct_type(self):
        """Test return type."""
        # Implementation
        pass

    def test_function_with_valid_input(self):
        """Test with valid input."""
        # Implementation
        pass

    def test_function_handles_errors(self):
        """Test error handling."""
        # Implementation
        pass


class TestIntegration:
    """Integration tests combining multiple components."""

    def test_full_pipeline(self):
        """Test complete workflow."""
        # Implementation
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

---

## Common Patterns from Chapter 38

### Pattern 1: Multi-Retriever Combination

**Use Case**: Combining different search strategies (vector + keyword)

**Scaffold Template**:

```python
def create_hybrid_retriever() -> QueryFusionRetriever:
    """
    Combine multiple retrievers for hybrid search.

    TODO: Implement this function
    HINT: Create retriever 1 (e.g., vector_retriever)
    HINT: Create retriever 2 (e.g., bm25_retriever)
    HINT: Combine with QueryFusionRetriever([retriever1, retriever2])
    HINT: Set mode="reciprocal_rerank" for fusion algorithm
    """
    pass
```

### Pattern 2: Post-Processor Pipeline

**Use Case**: Adding reranking or filtering after retrieval

**Scaffold Template**:

```python
def create_pipeline_with_postprocessor() -> QueryEngine:
    """
    Create query engine with post-processing.

    TODO: Implement this function
    HINT: Create base index/retriever
    HINT: Create post-processor (e.g., SentenceTransformerRerank)
    HINT: Combine with index.as_query_engine(node_postprocessors=[processor])
    """
    pass
```

### Pattern 3: Two-Stage Retrieval

**Use Case**: Fast retrieval followed by precise reranking

**Scaffold Template**:

```python
def two_stage_search(query: str, top_k_retrieve: int = 50, top_k_final: int = 5) -> List[Document]:
    """
    Perform two-stage retrieval: fast then precise.

    TODO: Implement this function
    HINT: Stage 1 - Retrieve top_k_retrieve results with fast method (vectors)
    HINT: Stage 2 - Rerank with slow but accurate method (cross-encoder)
    HINT: Return top_k_final results after reranking
    """
    pass
```

---

## Verification Script Pattern

**Keep verification scripts COMPLETE** (do not scaffold)

**Reason**: Students need working tests to verify their implementations

**Template**:

```python
"""
Verification script for Chapter X.
Property PXX: [Property Name]

This property ensures [what the property guarantees].
"""
import sys

print("🧪 Running [Chapter Name] Verification...\n")

# Setup
[Create test data]

# Test Property
print("Test 1: [Property Name]...")
[Test implementation]

# Verify
if [condition]:
    print("✅ PXX Passed: [Success message]")
else:
    print("❌ Failed: [Failure message]")
    sys.exit(1)

print("\n🎉 Chapter X Complete! [Success message]")
```

---

## Documentation Enhancements

### Performance Guidelines Table

Add for chapters with performance considerations:

```markdown
| Stage     | Method     | Speed | Accuracy | When to Use |
| --------- | ---------- | ----- | -------- | ----------- |
| [Stage 1] | [Method 1] | Fast  | Medium   | [Use case]  |
| [Stage 2] | [Method 2] | Slow  | High     | [Use case]  |
```

### Common Mistakes Section

Add for chapters with known pitfalls:

````markdown
### Mistake #1: [Mistake Name]

**Problem**: [What goes wrong]
**Symptom**: [How you know it's happening]
**Fix**: [How to fix it]

```python
# ❌ BAD: [Bad example]
[code]

# ✅ GOOD: [Good example]
[code]
```
````

````

### Quick Reference Card

Add for chapters with multiple patterns:

```markdown
### [Pattern Name]

```python
# 1. [Step 1]
[code]

# 2. [Step 2]
[code]

# 3. [Step 3]
[code]
````

```

---

## Checklist for Application Chapter Scaffolding

### Before Scaffolding
- [ ] Identify all complete code examples (>5 lines)
- [ ] Identify which examples are exercises vs reference
- [ ] Note all external APIs/libraries used
- [ ] Check for verification scripts (keep complete)

### During Scaffolding
- [ ] Convert each example to function with TODO/HINT
- [ ] Add complete type hints (100% coverage)
- [ ] Write 5-step HINT progression
- [ ] Move complete code to <details> section
- [ ] Add "Why this works" explanation
- [ ] Document key patterns

### After Scaffolding
- [ ] Create comprehensive test suite
- [ ] Verify tests run with stubs (skip gracefully)
- [ ] Add performance guidelines if relevant
- [ ] Add common mistakes section
- [ ] Add quick reference card
- [ ] Verify type hint coverage ≥95%

---

## Token Budget Estimates

**Per Application Chapter**:
- Analysis: ~5k tokens
- Scaffolding: ~15k tokens
- Test creation: ~5k tokens
- Documentation: ~3k tokens
- **Total**: ~28k tokens

**Factors that increase cost**:
- More code examples (>3)
- Complex multi-step workflows
- Multiple API integrations
- Extensive error handling

**Factors that decrease cost**:
- Fewer examples (<3)
- Simple single-API integration
- Existing test patterns to reuse

---

## Examples from Chapter 38

### Example 1: Hybrid Search
- **Lines**: 33 → Scaffolded function + 40-line solution
- **HINTs**: 5 specific steps
- **Type Hints**: 100% (QueryFusionRetriever return type)
- **Test Coverage**: 4 tests

### Example 2: Reranking
- **Lines**: 26 → Scaffolded function + 35-line solution
- **HINTs**: 5 specific steps
- **Type Hints**: 100% (RetrieverQueryEngine return type)
- **Test Coverage**: 4 tests

### Verification Script
- **Status**: Kept complete (41 lines)
- **Purpose**: Property P54 testing
- **Tests**: 1 property test

---

## Next Steps

1. **Apply to Chapter 17** - Use this pattern for RAG system
2. **Refine Based on Feedback** - Adjust HINT specificity
3. **Create Foundation Pattern** - Extract from Chapter 6B
4. **Create Capstone Pattern** - Extract from Chapter 52
5. **Build Automation** - Template-based scaffolding scripts

---

**Pattern Status**: ✅ Ready for Application to Chapter 17
```
