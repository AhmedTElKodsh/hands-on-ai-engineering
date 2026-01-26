# Infrastructure Module

Production-ready infrastructure components for AITEA AI Engineering curriculum.

## Components

### VectorStore

A simple, production-ready wrapper around ChromaDB for document storage and semantic search. Designed for educational use in RAG (Retrieval-Augmented Generation) systems.

## VectorStore API Reference

### Initialization

```python
from shared.infrastructure.vector_store import VectorStore

# Basic initialization
store = VectorStore(
    path="./chroma_db",
    collection_name="my_documents",
    embedding_model="text-embedding-3-small",  # OpenAI model
    api_key=None  # Uses OPENAI_API_KEY env var if None
)

# Or use convenience function
from shared.infrastructure.vector_store import create_vector_store
store = create_vector_store("./my_db", "documents")
```

**Parameters:**

- `path` (str): Directory path for persistent storage (default: "./chroma_db")
- `collection_name` (str): Name of the collection to use (default: "default_collection")
- `embedding_model` (str): OpenAI embedding model name (default: "text-embedding-3-small")
- `api_key` (Optional[str]): OpenAI API key (uses OPENAI_API_KEY env var if None)

**Raises:**

- `ValueError`: If API key is not provided and not in environment

---

### Adding Documents

#### `add_document(doc_id, text, metadata=None)`

Add a single document to the vector store.

```python
store.add_document(
    doc_id="doc1",
    text="RAG systems combine retrieval and generation",
    metadata={"source": "chapter17.md", "page": 1}
)
```

**Parameters:**

- `doc_id` (str): Unique identifier for the document
- `text` (str): Document text content
- `metadata` (Optional[Dict[str, Any]]): Optional metadata dictionary

---

#### `add_documents(doc_ids, texts, metadatas=None)`

Add multiple documents in batch (more efficient than multiple `add_document()` calls).

```python
store.add_documents(
    doc_ids=["1", "2", "3"],
    texts=["First doc", "Second doc", "Third doc"],
    metadatas=[
        {"source": "a.txt"},
        {"source": "b.txt"},
        {"source": "c.txt"}
    ]
)
```

**Parameters:**

- `doc_ids` (List[str]): List of unique document identifiers
- `texts` (List[str]): List of document text contents
- `metadatas` (Optional[List[Dict[str, Any]]]): Optional list of metadata dictionaries

**Raises:**

- `ValueError`: If lists have different lengths

---

### Searching Documents

#### `search(query, limit=5, where=None)` ✨ NEW

Search for similar documents using semantic similarity.

```python
# Basic search
results = store.search("What is RAG?", limit=3)
for doc in results:
    print(doc)

# Search with metadata filter
results = store.search(
    "machine learning",
    limit=5,
    where={"source": "chapter17.md"}
)
```

**Parameters:**

- `query` (str): Search query text
- `limit` (int): Maximum number of results to return (default: 5)
- `where` (Optional[Dict[str, Any]]): Optional metadata filter

**Returns:**

- `List[str]`: List of document texts, ordered by relevance (most similar first)

**Example Output:**

```python
[
    'RAG stands for Retrieval-Augmented Generation...',
    'RAG systems combine retrieval and generation...',
    'The RAG pattern has three steps...'
]
```

---

#### `search_with_metadata(query, limit=5, where=None)`

Search for similar documents and return both text and metadata. Essential for citation tracking in RAG systems.

```python
results = store.search_with_metadata("RAG", limit=2)
for doc, meta in results:
    print(f"Text: {doc}")
    print(f"Source: {meta['source']}")
```

**Parameters:**

- `query` (str): Search query text
- `limit` (int): Maximum number of results to return (default: 5)
- `where` (Optional[Dict[str, Any]]): Optional metadata filter

**Returns:**

- `List[Tuple[str, Dict[str, Any]]]`: List of (document_text, metadata_dict) tuples

**Example Output:**

```python
[
    ('RAG stands for...', {'source': 'chapter17.md', 'page': 1}),
    ('RAG systems combine...', {'source': 'chapter17.md', 'page': 2})
]
```

---

#### `search_with_scores(query, limit=5, where=None)`

Search for similar documents with relevance scores. Useful for debugging and understanding retrieval quality.

```python
results = store.search_with_scores("RAG", limit=2)
for doc, score, meta in results:
    print(f"Score: {score:.3f} - {doc[:50]}...")
```

**Parameters:**

- `query` (str): Search query text
- `limit` (int): Maximum number of results to return (default: 5)
- `where` (Optional[Dict[str, Any]]): Optional metadata filter

**Returns:**

- `List[Tuple[str, float, Dict[str, Any]]]`: List of (document_text, distance_score, metadata_dict) tuples
- **Note**: Lower distance = more similar

**Example Output:**

```python
[
    ('RAG stands for...', 0.234, {'source': 'chapter17.md'}),
    ('RAG systems combine...', 0.456, {'source': 'chapter18.md'})
]
```

---

### Document Management

#### `get_document(doc_id)`

Retrieve a specific document by ID.

```python
doc, meta = store.get_document("doc1")
print(doc)  # 'RAG stands for...'
print(meta)  # {'source': 'chapter17.md'}
```

**Parameters:**

- `doc_id` (str): Document identifier

**Returns:**

- `Optional[Tuple[str, Dict[str, Any]]]`: Tuple of (document_text, metadata_dict) or None if not found

---

#### `delete_document(doc_id)`

Delete a document by ID.

```python
store.delete_document("doc1")
```

**Parameters:**

- `doc_id` (str): Document identifier to delete

---

#### `delete_documents(doc_ids)`

Delete multiple documents by ID.

```python
store.delete_documents(["doc1", "doc2", "doc3"])
```

**Parameters:**

- `doc_ids` (List[str]): List of document identifiers to delete

---

#### `clear()`

Delete all documents from the collection.

⚠️ **Warning**: This operation cannot be undone!

```python
store.clear()  # Removes all documents
```

---

#### `count()`

Get the number of documents in the collection.

```python
print(f"Store contains {store.count()} documents")
# Output: Store contains 42 documents
```

**Returns:**

- `int`: Number of documents stored

---

## Complete Example: Building a RAG System

```python
from shared.infrastructure.vector_store import VectorStore
import os

# Set up API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# 1. Initialize vector store
store = VectorStore(
    path="./rag_db",
    collection_name="knowledge_base"
)

# 2. Add documents with metadata
documents = [
    ("1", "RAG stands for Retrieval-Augmented Generation", {"source": "intro.md"}),
    ("2", "RAG systems combine retrieval and generation", {"source": "intro.md"}),
    ("3", "Vector stores enable semantic search", {"source": "vectors.md"}),
]

for doc_id, text, metadata in documents:
    store.add_document(doc_id, text, metadata)

print(f"Added {store.count()} documents")

# 3. Search for relevant documents
query = "What is RAG?"
results = store.search(query, limit=2)

print(f"\nSearch results for: '{query}'")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc}")

# 4. Search with metadata for citations
results_with_meta = store.search_with_metadata(query, limit=2)

print(f"\nResults with citations:")
for doc, meta in results_with_meta:
    print(f"- {doc}")
    print(f"  Source: {meta['source']}")

# 5. Search with scores for debugging
results_with_scores = store.search_with_scores(query, limit=2)

print(f"\nResults with relevance scores:")
for doc, score, meta in results_with_scores:
    print(f"- Score: {score:.3f}")
    print(f"  Text: {doc[:50]}...")
    print(f"  Source: {meta['source']}")
```

**Output:**

```
Added 3 documents

Search results for: 'What is RAG?'
1. RAG stands for Retrieval-Augmented Generation
2. RAG systems combine retrieval and generation

Results with citations:
- RAG stands for Retrieval-Augmented Generation
  Source: intro.md
- RAG systems combine retrieval and generation
  Source: intro.md

Results with relevance scores:
- Score: 0.234
  Text: RAG stands for Retrieval-Augmented Generatio...
  Source: intro.md
- Score: 0.456
  Text: RAG systems combine retrieval and generation...
  Source: intro.md
```

---

## Metadata Filtering

Use the `where` parameter to filter search results by metadata:

```python
# Add documents with different sources
store.add_document("1", "Python basics", {"source": "python.md", "level": "beginner"})
store.add_document("2", "Advanced Python", {"source": "python.md", "level": "advanced"})
store.add_document("3", "JavaScript intro", {"source": "js.md", "level": "beginner"})

# Search only in Python documents
results = store.search(
    "programming concepts",
    limit=5,
    where={"source": "python.md"}
)

# Search only beginner-level content
results = store.search(
    "programming concepts",
    limit=5,
    where={"level": "beginner"}
)
```

---

## Best Practices

### 1. Use Batch Operations

```python
# ❌ Inefficient: Multiple single adds
for doc_id, text in documents:
    store.add_document(doc_id, text)

# ✅ Efficient: Single batch add
doc_ids = [doc[0] for doc in documents]
texts = [doc[1] for doc in documents]
store.add_documents(doc_ids, texts)
```

### 2. Always Include Metadata

```python
# ❌ No metadata = no citations
store.add_document("1", "Some text")

# ✅ Include source information
store.add_document("1", "Some text", {
    "source": "document.pdf",
    "page": 5,
    "author": "John Doe",
    "date": "2024-01-15"
})
```

### 3. Use Appropriate Search Methods

```python
# For simple retrieval
results = store.search(query)

# For RAG with citations
results = store.search_with_metadata(query)

# For debugging retrieval quality
results = store.search_with_scores(query)
```

### 4. Handle Empty Results

```python
results = store.search(query, limit=5)
if not results:
    print("No relevant documents found")
else:
    for doc in results:
        print(doc)
```

---

## Curriculum Integration

This VectorStore is used in the following chapters:

- **Chapter 14**: Vector Stores with Chroma (Introduction)
- **Chapter 17**: Your First RAG System (Basic usage)
- **Chapter 18**: RAG with Citations (Metadata tracking)
- **Chapter 19**: Advanced RAG Patterns (Hybrid search)
- **Chapter 35-38**: LlamaIndex Integration (Query engines)

---

## Requirements

- Python 3.10+
- chromadb
- openai (for embeddings)
- sentence-transformers (optional, for local embeddings)

Install dependencies:

```bash
pip install chromadb openai
```

---

## Environment Setup

Set your OpenAI API key:

```bash
# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Or use .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

---

## Troubleshooting

### "OpenAI API key required" Error

**Problem**: API key not found in environment.

**Solution**:

```python
# Option 1: Set environment variable
import os
os.environ["OPENAI_API_KEY"] = "your-key"

# Option 2: Pass directly to VectorStore
store = VectorStore(api_key="your-key")
```

### Empty Search Results

**Problem**: Search returns empty list.

**Possible causes**:

1. No documents added to collection
2. Query doesn't match any documents semantically
3. Metadata filter too restrictive

**Solution**:

```python
# Check document count
print(f"Documents in store: {store.count()}")

# Try broader search
results = store.search(query, limit=10)

# Remove metadata filter
results = store.search(query, where=None)
```

### Slow Search Performance

**Problem**: Search takes too long.

**Solutions**:

1. Reduce `limit` parameter
2. Use metadata filters to narrow search space
3. Consider using local embeddings (sentence-transformers) instead of API calls

---

## API Changes (Latest Update)

### New in Latest Version

#### ✨ `search()` Method

- **Added**: Complete implementation of semantic search
- **Returns**: List of document texts ordered by relevance
- **Use case**: Simple retrieval without metadata
- **Status**: ✅ Fully implemented

#### ✨ `search_with_metadata()` Method

- **Added**: Complete implementation with metadata tracking
- **Returns**: List of (document_text, metadata_dict) tuples
- **Use case**: RAG systems requiring source attribution and citations
- **Status**: ✅ Fully implemented

### Implementation Details

The recent update completed the `add_documents()` method and added two new search methods:

1. **`search()`**: Basic semantic search returning only document texts
2. **`search_with_metadata()`**: Advanced search returning documents with their metadata for citation tracking

Both methods support:

- Configurable result limits
- Metadata filtering via `where` parameter
- ChromaDB's semantic similarity ranking

---

## License

MIT License - See [LICENSE](../../LICENSE) for details

---

## Support

For issues or questions:

1. Check the [curriculum chapters](../../curriculum/chapters/) for usage examples
2. Review the [test files](../../tests/) for working code
3. Consult the main [README](../../README.md) for project overview
