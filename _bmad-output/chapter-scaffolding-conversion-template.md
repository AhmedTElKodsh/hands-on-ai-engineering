# Chapter Scaffolding Conversion Template

**Purpose**: Convert chapters with complete solutions into educational scaffolding with hints
**Target**: Chapters 06A through 54 (all phases)
**Date**: 2026-01-21

---

## 🎯 Conversion Principles

### ✅ KEEP (Educational Scaffolding)

- Conceptual explanations and theory
- Architecture diagrams and flowcharts
- Import statements and dependencies
- Function/class signatures with docstrings
- Type hints and interface definitions
- TODO comments marking implementation points
- Hints about approach and strategy
- References to documentation
- Test structure (without complete assertions)

### ❌ REMOVE (Complete Solutions)

- Full function/method implementations
- Complete business logic
- Detailed algorithm implementations
- Complete error handling code
- Full database queries
- Complete API integrations
- Finished UI components
- Complete test assertions

### 🔄 TRANSFORM (Solution → Scaffolding)

- Complete code → Skeleton with TODOs
- Working logic → Pseudocode comments
- Full implementations → Hints + starter code
- Finished tests → Test structure + assertion hints

---

## 📋 Step-by-Step Conversion Process

### Step 1: Identify Complete Solutions

Look for:

- [ ] Functions with full implementations (>5 lines of logic)
- [ ] Complete class methods
- [ ] Working algorithms
- [ ] Full database operations
- [ ] Complete API calls
- [ ] Finished UI components
- [ ] Complete test assertions

### Step 2: Extract Core Structure

Keep:

- [ ] Function/class signatures
- [ ] Docstrings
- [ ] Type hints
- [ ] Import statements
- [ ] Constants and configuration

### Step 3: Replace Implementation with Scaffolding

#### Pattern A: Function Implementation

**BEFORE** (Complete Solution):

```python
def calculate_embeddings(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Generate embeddings for the given text."""
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response['data'][0]['embedding']
```

**AFTER** (Scaffolding):

```python
def calculate_embeddings(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Generate embeddings for the given text.

    TODO: Implement this function
    Hints:
    - Use the OpenAI API client
    - Call the Embedding.create() method
    - Extract the embedding vector from the response
    - Handle potential API errors

    Returns:
        List[float]: The embedding vector
    """
    # TODO: Create the API call
    # TODO: Extract and return the embedding
    pass
```

#### Pattern B: Class Method

**BEFORE** (Complete Solution):

```python
class VectorStore:
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        similarities = []
        for doc_id, doc_vector in self.vectors.items():
            sim = cosine_similarity(query_vector, doc_vector)
            similarities.append((doc_id, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [{"id": doc_id, "score": score}
                for doc_id, score in similarities[:top_k]]
```

**AFTER** (Scaffolding):

```python
class VectorStore:
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar vectors.

        TODO: Implement vector similarity search
        Hints:
        - Calculate similarity between query_vector and each stored vector
        - Use cosine_similarity() function (you'll need to implement this)
        - Sort results by similarity score (highest first)
        - Return top_k results

        Args:
            query_vector: The query embedding
            top_k: Number of results to return

        Returns:
            List of dicts with 'id' and 'score' keys
        """
        # TODO: Calculate similarities for all vectors
        # TODO: Sort by similarity score
        # TODO: Return top_k results
        pass
```

#### Pattern C: Algorithm Implementation

**BEFORE** (Complete Solution):

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
```

**AFTER** (Scaffolding):

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks.

    TODO: Implement text chunking with overlap
    Hints:
    - Use a sliding window approach
    - Start at position 0
    - Move forward by (chunk_size - overlap) each iteration
    - Continue until you've processed all text

    Example:
        text = "ABCDEFGHIJ"
        chunk_size = 4, overlap = 1
        Result: ["ABCD", "DEFG", "GHIJ"]

    Args:
        text: The text to chunk
        chunk_size: Size of each chunk
        overlap: Number of overlapping characters

    Returns:
        List of text chunks
    """
    chunks = []
    # TODO: Implement sliding window chunking
    # Hint: Think about where to start and how much to advance each iteration
    return chunks
```

#### Pattern D: Test Cases

**BEFORE** (Complete Solution):

```python
def test_embedding_generation():
    text = "Hello world"
    embeddings = calculate_embeddings(text)
    assert len(embeddings) == 1536
    assert all(isinstance(x, float) for x in embeddings)
    assert -1 <= max(embeddings) <= 1
```

**AFTER** (Scaffolding):

```python
def test_embedding_generation():
    """Test that embeddings are generated correctly.

    TODO: Complete this test
    Hints:
    - OpenAI ada-002 embeddings have 1536 dimensions
    - Each value should be a float
    - Values are typically normalized between -1 and 1
    """
    text = "Hello world"
    embeddings = calculate_embeddings(text)

    # TODO: Assert the embedding has correct dimensions
    # TODO: Assert all values are floats
    # TODO: Assert values are in expected range
    pass
```

### Step 4: Add Strategic Hints

#### Hint Categories:

**1. Conceptual Hints** (What to think about)

```python
# Hint: Consider how vector similarity relates to document relevance
# Hint: Think about edge cases like empty input or missing data
```

**2. Approach Hints** (How to solve)

```python
# Hint: Use a dictionary to store document vectors for fast lookup
# Hint: Consider using numpy for efficient vector operations
```

**3. Implementation Hints** (Specific guidance)

```python
# Hint: Use the formula: cosine_sim = dot(a,b) / (norm(a) * norm(b))
# Hint: The OpenAI client is already imported as 'openai'
```

**4. Resource Hints** (Where to learn more)

```python
# Hint: See OpenAI embeddings documentation: https://platform.openai.com/docs/guides/embeddings
# Hint: Review numpy.dot() and numpy.linalg.norm() documentation
```

### Step 5: Preserve Learning Structure

Keep these elements intact:

- [ ] Section introductions and context
- [ ] Conceptual explanations before code
- [ ] Architecture diagrams
- [ ] Learning objectives
- [ ] Key concepts lists
- [ ] "Why This Matters" sections
- [ ] Common pitfalls warnings
- [ ] Best practices notes

### Step 6: Add Verification Checkpoints

Add these after major sections:

````markdown
## ✅ Checkpoint: [Feature Name]

Before moving forward, verify:

- [ ] Your function signature matches the specification
- [ ] You've handled the main use case
- [ ] You've considered edge cases
- [ ] Your code includes error handling
- [ ] You've added appropriate type hints

Test your implementation:

```python
# Run this to verify your implementation works
result = your_function(test_input)
print(f"Result: {result}")
# Expected output: [describe expected output]
```
````

````

---

## 🔧 Conversion Checklist (Per Chapter)

### Pre-Conversion
- [ ] Read entire chapter to understand learning objectives
- [ ] Identify all code blocks with complete implementations
- [ ] Note which concepts are being taught
- [ ] Review any existing projects or exercises

### During Conversion
- [ ] Replace complete implementations with scaffolding
- [ ] Add TODO comments at implementation points
- [ ] Include strategic hints (not solutions)
- [ ] Preserve all conceptual explanations
- [ ] Keep function signatures and type hints
- [ ] Maintain test structure (remove complete assertions)
- [ ] Add verification checkpoints

### Post-Conversion
- [ ] Verify no complete solutions remain
- [ ] Ensure scaffolding is clear and helpful
- [ ] Check that hints guide without solving
- [ ] Confirm learning objectives are still achievable
- [ ] Test that imports and setup code still work
- [ ] Review for consistency with educational philosophy

---

## 📊 Quality Metrics

### Good Scaffolding Has:
- ✅ Clear function signatures with docstrings
- ✅ Strategic hints that guide thinking
- ✅ TODO markers at implementation points
- ✅ Working imports and setup code
- ✅ Type hints for all parameters
- ✅ Example inputs/outputs
- ✅ References to documentation

### Bad Scaffolding Has:
- ❌ Complete working implementations
- ❌ Hints that give away the solution
- ❌ No guidance on approach
- ❌ Missing function signatures
- ❌ No indication of what to implement
- ❌ Overly complex starter code

---

## 🎓 Educational Philosophy Alignment

### Tier 1 (Foundations): More Scaffolding
- Provide more complete structure
- Include more detailed hints
- Show example patterns
- Guide step-by-step

### Tier 2 (Intermediate): Balanced Scaffolding
- Provide function signatures and docstrings
- Include strategic hints
- Show architecture, not implementation
- Encourage problem-solving

### Tier 3 (Advanced): Minimal Scaffolding
- Provide specifications and requirements
- Include architectural guidance
- Minimal implementation hints
- Expect independent problem-solving

---

## 🚀 Quick Conversion Workflow

For each chapter file:

1. **Scan**: Identify complete implementations
2. **Extract**: Pull out signatures, types, docstrings
3. **Replace**: Swap implementation with TODO + hints
4. **Enhance**: Add strategic guidance
5. **Verify**: Check no solutions remain
6. **Test**: Ensure scaffolding is clear

---

## 📝 Example: Complete Chapter Conversion

### Original Section (Complete Solution)
```python
## Vector Search Implementation

Let's implement a simple vector search:

```python
import numpy as np
from typing import List, Dict

class SimpleVectorStore:
    def __init__(self):
        self.vectors = {}
        self.metadata = {}

    def add(self, doc_id: str, vector: List[float], metadata: Dict):
        self.vectors[doc_id] = np.array(vector)
        self.metadata[doc_id] = metadata

    def search(self, query: List[float], top_k: int = 5) -> List[Dict]:
        query_vec = np.array(query)
        results = []

        for doc_id, doc_vec in self.vectors.items():
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )
            results.append({
                'id': doc_id,
                'score': float(similarity),
                'metadata': self.metadata[doc_id]
            })

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
````

Now you can use it like this:

```python
store = SimpleVectorStore()
store.add("doc1", [0.1, 0.2, 0.3], {"title": "First Doc"})
results = store.search([0.15, 0.25, 0.35], top_k=3)
```

````

### Converted Section (Scaffolding)
```python
## Vector Search Implementation

In this section, you'll implement a simple vector store with similarity search capabilities.

### Learning Objectives
- Understand vector similarity concepts
- Implement cosine similarity calculation
- Build a searchable vector store
- Handle vector operations efficiently

### Architecture Overview
````

VectorStore
├── Storage: vectors (dict) + metadata (dict)
├── add(): Store vector with metadata
└── search(): Find similar vectors using cosine similarity

````

### Implementation

```python
import numpy as np
from typing import List, Dict

class SimpleVectorStore:
    """A simple in-memory vector store with similarity search.

    This class stores document vectors and enables similarity-based retrieval.
    """

    def __init__(self):
        """Initialize the vector store.

        TODO: Set up storage for vectors and metadata
        Hints:
        - Use dictionaries for fast lookup by document ID
        - Store vectors as numpy arrays for efficient computation
        """
        # TODO: Initialize storage structures
        pass

    def add(self, doc_id: str, vector: List[float], metadata: Dict) -> None:
        """Add a document vector to the store.

        TODO: Implement document storage
        Hints:
        - Convert the vector list to a numpy array
        - Store both the vector and metadata
        - Use doc_id as the key

        Args:
            doc_id: Unique identifier for the document
            vector: The document's embedding vector
            metadata: Additional information about the document
        """
        # TODO: Store the vector (convert to numpy array)
        # TODO: Store the metadata
        pass

    def search(self, query: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar vectors using cosine similarity.

        TODO: Implement similarity search
        Hints:
        - Convert query to numpy array
        - Calculate cosine similarity with each stored vector
        - Cosine similarity formula: dot(a,b) / (norm(a) * norm(b))
        - Sort results by similarity (highest first)
        - Return top_k results

        Args:
            query: The query vector
            top_k: Number of results to return

        Returns:
            List of dicts with 'id', 'score', and 'metadata' keys

        Example:
            results = store.search([0.1, 0.2, 0.3], top_k=3)
            # Returns: [{'id': 'doc1', 'score': 0.95, 'metadata': {...}}, ...]
        """
        # TODO: Convert query to numpy array
        # TODO: Calculate similarity for each stored vector
        # TODO: Sort by similarity score (descending)
        # TODO: Return top_k results with id, score, and metadata
        pass
````

### Testing Your Implementation

```python
# Test your vector store
store = SimpleVectorStore()

# Add some test documents
store.add("doc1", [0.1, 0.2, 0.3], {"title": "First Doc"})
store.add("doc2", [0.9, 0.8, 0.7], {"title": "Second Doc"})

# Search for similar documents
results = store.search([0.15, 0.25, 0.35], top_k=2)

# TODO: Verify your results
# Expected: doc1 should have higher similarity than doc2
print(f"Top result: {results[0]['id']}")  # Should be 'doc1'
print(f"Similarity: {results[0]['score']}")  # Should be close to 1.0
```

### ✅ Checkpoint

Before moving forward, verify:

- [ ] Your `add()` method stores vectors and metadata correctly
- [ ] Your `search()` method calculates cosine similarity
- [ ] Results are sorted by similarity (highest first)
- [ ] The method returns the correct number of results (top_k)
- [ ] Each result includes id, score, and metadata

### 💡 Key Concepts

**Cosine Similarity**: Measures the cosine of the angle between two vectors. Values range from -1 (opposite) to 1 (identical).

**Why Cosine Similarity?**: It's scale-invariant, meaning it measures direction rather than magnitude. Perfect for comparing embeddings.

### 🔗 Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [Understanding Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Vector Search Fundamentals](https://www.pinecone.io/learn/vector-search/)

````

---

## 📋 Batch Conversion Script Template

```python
# conversion_script.py
"""
Batch convert chapters to scaffolding format.
Usage: python conversion_script.py --phase 1 --chapters 06A-10
"""

import re
from pathlib import Path
from typing import List

def identify_complete_implementations(content: str) -> List[tuple]:
    """Find code blocks that look like complete implementations."""
    # TODO: Implement pattern matching for complete solutions
    pass

def extract_scaffolding(code_block: str) -> str:
    """Extract signature, docstring, and create TODO scaffolding."""
    # TODO: Implement scaffolding extraction
    pass

def add_hints(code_block: str, context: str) -> str:
    """Add strategic hints based on the code context."""
    # TODO: Implement hint generation
    pass

def convert_chapter(chapter_path: Path) -> str:
    """Convert a single chapter to scaffolding format."""
    # TODO: Implement full chapter conversion
    pass

if __name__ == "__main__":
    # TODO: Implement batch processing
    pass
````

---

## ✅ Success Criteria

A successfully converted chapter:

1. Contains NO complete working implementations
2. Provides clear function signatures and type hints
3. Includes strategic hints that guide without solving
4. Maintains all conceptual explanations
5. Preserves learning objectives
6. Includes verification checkpoints
7. Aligns with tier-appropriate scaffolding levels
8. Enables students to learn by implementing

---

**Template Version**: 1.0  
**Created**: 2026-01-21  
**For**: BMAD Curriculum Enhancement Project  
**Owner**: Ahmed
