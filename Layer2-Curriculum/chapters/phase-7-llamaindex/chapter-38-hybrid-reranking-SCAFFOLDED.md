# Chapter 38: Hybrid Search & Reranking — The Perfect Match

<!--
METADATA
Phase: 7 - LlamaIndex
Time: 1.5 hours (30 min reading + 60 min hands-on)
Difficulty: ⭐⭐⭐
Type: Implementation
Prerequisites: Chapter 35 (LlamaIndex)
Builds Toward: Production Deployment (Ch 40)
Correctness Properties: P23 (Query Diversity), P54 (Reranking Monotonicity)
Project Thread: Search Optimization

SCAFFOLDING STATUS: ✅ SCAFFOLDED VERSION
- All code examples converted to TODO/HINT pattern
- Complete solutions in <details> sections
- Type hints: 100% coverage
- Tests: Runnable with stubs

NAVIGATION
→ Quick Reference: #quick-reference-card
→ Verification: #verification-required-section
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

**Imagine this**: You're looking for "The Rock".
**Vector Search** sees "Rock" and thinks "Stone, Mountain, Mineral". 🪨
**Keyword Search** sees "The Rock" and matches "Dwayne Johnson" because that phrase appears exactly in the text. 💪

Neither is perfect.

- **Vectors** are great for concepts ("Action movies").
- **Keywords** are great for exact matches ("Part Number XJ-900").

**Hybrid Search** combines them. It uses both methods and merges the results.
**Reranking** is the cherry on top. It takes the top 50 results and uses a super-smart (but slow) model to carefully re-read and rank them, ensuring the absolute best document is #1.

**By the end of this chapter**, you will build a search pipeline that captures _everything_—concepts and keywords—and ranks them with precision. 🎯

---

## Prerequisites Check

We need the reranking library.

```bash
pip install llama-index-postprocessor-colbert-rerank
# Or just use standard:
pip install llama-index-embeddings-huggingface
pip install llama-index-retrievers-bm25
pip install rank-bm25
```

---

## The Story: The "SKU" Problem

### The Problem (Exact Matches)

User: _"Where is part XJ-900?"_
Vector Search: Finds documents about "X-rays" and "90s music" because vectors are fuzzy.
Result: The user gets unrelated junk.

### The Solution (Hybrid + Rerank)

1.  **Hybrid**: Run BM25 (Keywords) to catch "XJ-900". Run Vector to catch "Spare Parts".
2.  **Merge**: Combine lists. (Now we have 50 items).
3.  **Rerank**: Use a Cross-Encoder to score each of the 50 items against the query "Where is part XJ-900?".
4.  **Result**: The manual for XJ-900 bubbles to the top.

---

## Part 1: Hybrid Search

LlamaIndex supports hybrid search by combining multiple retrievers using `QueryFusionRetriever`.

### 🔬 Exercise #1: Build Hybrid Search Pipeline

**Your Mission**: Create a hybrid search system that combines vector similarity and keyword matching.

**Create `hybrid_test.py`**:

```python
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from typing import List

def create_hybrid_search_pipeline() -> QueryFusionRetriever:
    """
    Create a hybrid search pipeline combining vector and keyword search.

    This demonstrates the power of combining semantic (vector) and lexical (BM25)
    search to capture both conceptual similarity and exact keyword matches.

    TODO: Implement this function
    HINT: Create 3 sample documents using Document(text="...")
    HINT: Include one with "XJ-900", one unrelated, one about engines
    HINT: Build VectorStoreIndex.from_documents(docs)
    HINT: Create vector_retriever = index.as_retriever(similarity_top_k=2)
    HINT: Create BM25Retriever.from_defaults(nodes=index.docstore.docs.values(), similarity_top_k=2)
    HINT: Combine with QueryFusionRetriever([vector_retriever, bm25_retriever], mode="reciprocal_rerank")

    Args:
        None

    Returns:
        QueryFusionRetriever: Configured hybrid retriever that combines vector and BM25 search

    Example:
        >>> retriever = create_hybrid_search_pipeline()
        >>> nodes = retriever.retrieve("XJ-900")
        >>> print(nodes[0].node.get_text())
        'The XJ-900 is a high-performance engine.'
    """
    pass  # Your code here


def test_hybrid_search():
    """
    Test the hybrid search pipeline.

    TODO: Implement this test function
    HINT: Call create_hybrid_search_pipeline()
    HINT: Use retriever.retrieve("XJ-900") to search
    HINT: Print the top result's text
    HINT: Verify it contains "XJ-900"
    """
    pass  # Your code here


if __name__ == "__main__":
    test_hybrid_search()
```

**Expected Behavior**:

- Should confidently return the document containing "XJ-900"
- BM25 catches the exact keyword match
- Vector search provides semantic context
- Fusion combines both signals

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from typing import List

def create_hybrid_search_pipeline() -> QueryFusionRetriever:
    """Create a hybrid search pipeline combining vector and keyword search."""

    # 1. Create sample documents
    docs = [
        Document(text="The XJ-900 is a high-performance engine."),
        Document(text="Bananas are rich in potassium."),
        Document(text="Engine maintenance requires skill."),
    ]

    # 2. Build vector index
    index = VectorStoreIndex.from_documents(docs)

    # 3. Create vector retriever (semantic search)
    vector_retriever = index.as_retriever(similarity_top_k=2)

    # 4. Create BM25 retriever (keyword search)
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=index.docstore.docs.values(),
        similarity_top_k=2
    )

    # 5. Combine with QueryFusionRetriever (hybrid)
    retriever = QueryFusionRetriever(
        [vector_retriever, bm25_retriever],
        similarity_top_k=2,
        num_queries=1,  # No query expansion for now
        mode="reciprocal_rerank",  # Fusion algorithm
        use_async=False
    )

    return retriever


def test_hybrid_search():
    """Test the hybrid search pipeline."""
    retriever = create_hybrid_search_pipeline()

    # Search for exact keyword
    nodes = retriever.retrieve("XJ-900")

    print(f"Top Result: {nodes[0].node.get_text()}")
    assert "XJ-900" in nodes[0].node.get_text(), "Should find XJ-900 document"
    print("✅ Hybrid search working correctly!")


if __name__ == "__main__":
    test_hybrid_search()
```

**Why this implementation works**:

1. **Vector Retriever**: Captures semantic similarity (e.g., "engine" relates to "maintenance")
2. **BM25 Retriever**: Captures exact keyword matches (e.g., "XJ-900")
3. **Reciprocal Rerank**: Combines scores from both retrievers using reciprocal rank fusion
4. **Complementary Strengths**: Vector search handles concepts, BM25 handles exact terms

**Key Pattern**: Hybrid search increases **recall** (finding more relevant documents) by combining different retrieval strategies.

</details>

---

## Part 2: Reranking (The Judge)

Now let's add a Reranker. This is a "Post-Processor" in LlamaIndex that re-scores retrieved documents using a more sophisticated model.

### 🔬 Exercise #2: Add Reranking to Search

**Your Mission**: Implement a reranking pipeline that uses a cross-encoder to improve result quality.

**Create `rerank_test.py`**:

```python
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine
from typing import List

def create_reranking_pipeline() -> RetrieverQueryEngine:
    """
    Create a search pipeline with reranking post-processor.

    Reranking uses a cross-encoder model that reads both the query and document
    together, providing more accurate relevance scores than vector similarity alone.

    TODO: Implement this function
    HINT: Create 3 documents about Python (snake, programming, jungle)
    HINT: Build VectorStoreIndex from documents
    HINT: Create SentenceTransformerRerank with model="cross-encoder/ms-marco-MiniLM-L-6-v2"
    HINT: Set top_n=1 to return only the best result
    HINT: Use index.as_query_engine(similarity_top_k=3, node_postprocessors=[reranker])

    Args:
        None

    Returns:
        RetrieverQueryEngine: Query engine with reranking enabled

    Example:
        >>> engine = create_reranking_pipeline()
        >>> response = engine.query("How do I write code?")
        >>> print(response.source_nodes[0].node.get_text())
        'Python is a programming language.'
    """
    pass  # Your code here


def test_reranking():
    """
    Test the reranking pipeline.

    TODO: Implement this test function
    HINT: Call create_reranking_pipeline()
    HINT: Query with "How do I write code?"
    HINT: Print the answer and source
    HINT: Verify the source is about programming, not snakes
    """
    pass  # Your code here


if __name__ == "__main__":
    test_reranking()
```

**Expected Behavior**:

- Vector search might rank "Python is a snake" highly (word overlap)
- Reranker reads the full context and correctly identifies "Python is a programming language" as most relevant
- Final result is the correct document

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine

def create_reranking_pipeline() -> RetrieverQueryEngine:
    """Create a search pipeline with reranking post-processor."""

    # 1. Create documents with subtle differences
    docs = [
        Document(text="Python is a snake."),
        Document(text="Python is a programming language."),
        Document(text="Pythons live in the jungle.")
    ]

    # 2. Build vector index
    index = VectorStoreIndex.from_documents(docs)

    # 3. Setup reranker (cross-encoder model)
    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_n=1  # Return only the best result after reranking
    )

    # 4. Create query engine with reranking
    # First retrieves top 3 with vectors, then reranks to top 1
    engine = index.as_query_engine(
        similarity_top_k=3,  # Retrieve broadly
        node_postprocessors=[reranker]  # Rerank precisely
    )

    return engine


def test_reranking():
    """Test the reranking pipeline."""
    engine = create_reranking_pipeline()

    # Query about programming
    response = engine.query("How do I write code?")

    print(f"Answer: {response}")
    print(f"Source: {response.source_nodes[0].node.get_text()}")

    # Verify correct document was selected
    source_text = response.source_nodes[0].node.get_text()
    assert "programming language" in source_text, "Should select programming doc, not snake doc"
    print("✅ Reranking working correctly!")


if __name__ == "__main__":
    test_reranking()
```

**Why this implementation works**:

1. **Vector Search (First Stage)**: Fast but imprecise - retrieves top 3 candidates
2. **Cross-Encoder (Second Stage)**: Slow but precise - reads query + document together
3. **Contextual Understanding**: Cross-encoder understands "write code" relates to "programming language", not "snake"
4. **Two-Stage Pipeline**: Balances speed (vectors) and accuracy (reranking)

**Key Pattern**: Reranking is a **precision** optimization. Use it after retrieval to improve the quality of top results.

**Performance Note**: Cross-encoders are O(N) - they process each document separately. Only rerank the top K results (e.g., top 50), never thousands.

</details>

---

## Common Mistakes

### Mistake #1: Reranking EVERYTHING

**Problem**: Rerankers are **slow**. Cross-encoders run `O(N)` BERT passes.
**Symptom**: Query takes 30+ seconds
**Fix**: Retrieve top 50 with Vectors → Rerank top 50 → Keep top 5

```python
# ❌ BAD: Reranking 1000 documents
engine = index.as_query_engine(
    similarity_top_k=1000,  # Too many!
    node_postprocessors=[reranker]
)

# ✅ GOOD: Rerank only top candidates
engine = index.as_query_engine(
    similarity_top_k=50,  # Reasonable number
    node_postprocessors=[reranker]
)
```

### Mistake #2: Ignoring Score Threshold

**Problem**: Sometimes _none_ of the documents are relevant
**Symptom**: Reranker returns low scores (e.g., 0.1) but you still use the results
**Fix**: Filter out nodes with `score < 0.5`

```python
# Check reranked scores
reranked_nodes = reranker.postprocess_nodes(nodes, query_str=query)
relevant_nodes = [n for n in reranked_nodes if n.score > 0.5]

if not relevant_nodes:
    return "No relevant documents found"
```

### Mistake #3: Missing Dependencies

**Problem**: BM25 and Rerankers need extra packages
**Symptom**: `ImportError: No module named 'rank_bm25'`
**Fix**: Install all required packages

```bash
pip install rank-bm25
pip install torch
pip install sentence-transformers
```

---

## Quick Reference Card

### Hybrid Search Pattern

```python
# 1. Create retrievers
vector_retriever = index.as_retriever(similarity_top_k=K)
bm25_retriever = BM25Retriever.from_defaults(nodes=..., similarity_top_k=K)

# 2. Combine with fusion
hybrid_retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    mode="reciprocal_rerank"
)

# 3. Search
nodes = hybrid_retriever.retrieve(query)
```

### Reranking Pattern

```python
# 1. Create reranker
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
    top_n=5
)

# 2. Add to query engine
engine = index.as_query_engine(
    similarity_top_k=20,  # Fetch broad
    node_postprocessors=[reranker]  # Filter deep
)

# 3. Query
response = engine.query(query)
```

### Performance Guidelines

| Stage     | Method        | Speed | Accuracy | When to Use                  |
| --------- | ------------- | ----- | -------- | ---------------------------- |
| Retrieval | Vector Search | Fast  | Medium   | Always (first stage)         |
| Retrieval | BM25          | Fast  | Medium   | When exact keywords matter   |
| Reranking | Cross-Encoder | Slow  | High     | Top K results only (K < 100) |

---

## Verification (REQUIRED SECTION)

We need to verify **P54 (Monotonicity)**. The scores returned by the reranker must be sorted descending.

**Create `verify_rerank.py`**:

```python
"""
Verification script for Chapter 38.
Property P54: Reranking Monotonicity.

This property ensures that reranked results are properly sorted by relevance score.
"""
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.postprocessor import SentenceTransformerRerank
import sys

print("🧪 Running Reranking Verification...\n")

# Setup
docs = [
    Document(text="A"),
    Document(text="B"),
    Document(text="C"),
    Document(text="D")
]
index = VectorStoreIndex.from_documents(docs)

# Reranker
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
    top_n=4
)

# Retrieve nodes directly (bypass query engine to inspect scores)
retriever = index.as_retriever(similarity_top_k=4)
nodes = retriever.retrieve("A")  # Should match A best

# Apply Reranker
reranked_nodes = reranker.postprocess_nodes(nodes, query_str="A")

# P54: Monotonicity
print("Test 1: Score Order...")
scores = [n.score for n in reranked_nodes]
print(f"Scores: {scores}")

# Check if sorted descending
is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))

if is_sorted:
    print("✅ P54 Passed: Results are sorted by relevance.")
else:
    print("❌ Failed: Reranker did not sort results.")
    sys.exit(1)

print("\n🎉 Chapter 38 Complete! Your search is optimized.")
```

**Run it:** `python verify_rerank.py`

**Expected Output**:

```
🧪 Running Reranking Verification...

Test 1: Score Order...
Scores: [0.95, 0.72, 0.45, 0.23]
✅ P54 Passed: Results are sorted by relevance.

🎉 Chapter 38 Complete! Your search is optimized.
```

---

## Summary

**What you learned:**

1. ✅ **The Limits of Vectors**: They miss exact keywords
2. ✅ **Hybrid Search**: Combining BM25 and Vectors increases recall
3. ✅ **Cross-Encoders**: Models that compare Query+Doc directly
4. ✅ **Two-Stage Retrieval**: Retrieve fast (Vectors), Rank slow (Cross-Encoder)
5. ✅ **LlamaIndex Pipelines**: Adding post-processors easily

**Key Takeaway**: Search is a funnel. Wide at the top (Hybrid), narrow at the bottom (Rerank).

**Skills unlocked**: 🎯

- Information Retrieval (IR)
- Search Relevance Tuning
- Pipeline Optimization

**Looking ahead**: We have finished **Phase 7: LlamaIndex**. We have mastered Data and Indexing.
In **Phase 8: Production**, we stop playing in notebooks. We will learn **Testing** (Property-Based), **Evaluation** (LangSmith), and **Deployment** patterns. The training wheels come off!

---

**Next**: [Phase 8: Production (Chapter 39) →](../phase-8-production/chapter-39-hypothesis-testing.md)
