# Pinecone Vector Store Implementation

## Overview

The Pinecone vector store implementation provides a production-ready interface for storing and retrieving document embeddings using Pinecone's fully managed vector database service.

## Implementation Status

✅ **COMPLETED** - Task 39.3

## Features

### Core Functionality

- ✅ Document storage with automatic embedding generation
- ✅ Similarity search with metadata filtering
- ✅ Hybrid search (falls back to similarity search with warning)
- ✅ Document deletion by ID
- ✅ Namespace support for multi-tenancy
- ✅ Automatic index creation if not exists
- ✅ Batch operations for large datasets

### Production Features

- ✅ Fully managed service (no infrastructure maintenance)
- ✅ Horizontal scaling capabilities
- ✅ Low latency queries
- ✅ Metadata filtering support
- ✅ Namespace isolation
- ✅ Automatic batching (100 docs for upsert, 1000 for delete)

## Usage Example

```python
from src.langchain.stores import PineconeStore
from src.langchain.vector_stores import Document, EmbeddingProvider, create_embedding_model

# Create embedding model
embedding_model = create_embedding_model(
    provider=EmbeddingProvider.OPENAI,
    model_name="text-embedding-3-small"
)

# Initialize Pinecone store
store = PineconeStore(
    index_name="aitea-features",
    embedding_model=embedding_model,
    api_key="your-pinecone-api-key",  # or set PINECONE_API_KEY env var
    environment="us-west1-gcp",        # or set PINECONE_ENVIRONMENT env var
    namespace="production"
)

# Add documents
documents = [
    Document(
        content="CRUD operations for user management",
        metadata={"category": "backend", "team": "api"}
    ),
    Document(
        content="Real-time chat interface with WebSocket",
        metadata={"category": "frontend", "team": "ui"}
    )
]

ids = await store.add_documents(documents)

# Search for similar documents
results = await store.similarity_search(
    query="user authentication features",
    k=5,
    filter={"category": "backend"}
)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.document.content}")
    print(f"Metadata: {result.document.metadata}")
```

## Configuration

### Environment Variables

- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Your Pinecone environment (e.g., "us-west1-gcp")

### Constructor Parameters

- `index_name` (str): Name of the Pinecone index
- `embedding_model` (EmbeddingModel): Embedding model for generating vectors (required)
- `api_key` (Optional[str]): Pinecone API key (uses env var if None)
- `environment` (Optional[str]): Pinecone environment (uses env var if None)
- `namespace` (str): Namespace for organizing vectors (default: "default")

## Batch Limits

The implementation automatically handles Pinecone's batch limits:

- **Upsert**: 100 documents per batch
- **Delete**: 1000 IDs per batch

Large operations are automatically split into multiple batches.

## Limitations

### Hybrid Search

Pinecone does not natively support hybrid search (dense + sparse retrieval). The `hybrid_search` method falls back to `similarity_search` and emits a warning. For true hybrid search capabilities, use Qdrant instead.

### Metadata Constraints

Pinecone metadata must be a flat dictionary with string, number, or boolean values. Nested objects are not supported.

## Testing

Comprehensive test suite with 21 tests covering:

- ✅ Initialization validation (API key, environment, embedding model)
- ✅ Document operations (add, delete, clear)
- ✅ Search operations (similarity, hybrid fallback, filters)
- ✅ Batch processing
- ✅ Custom ID preservation
- ✅ Metadata handling
- ✅ Error handling

Run tests:

```bash
python -m pytest tests/langchain/test_pinecone_store.py -v
```

## Requirements

- `pinecone-client`: Install with `pip install pinecone-client`
- Valid Pinecone API key and environment

## When to Use Pinecone

**Good for:**

- Production deployments requiring high availability
- Large-scale applications (millions of vectors)
- Teams wanting minimal operational overhead
- Applications requiring low latency queries
- Multi-tenant applications (namespace support)

**Consider alternatives if:**

- You need hybrid search (use Qdrant)
- You prefer self-hosted solutions (use Qdrant or Weaviate)
- You're in early development (use ChromaDB)
- You need graph-based retrieval (use Neo4j with pgvector)

## Related Files

- Implementation: `src/langchain/stores/pinecone_store.py`
- Tests: `tests/langchain/test_pinecone_store.py`
- Abstract Interface: `src/langchain/vector_stores.py`
- Other Stores: `chromadb_store.py`, `qdrant_store.py`

## Requirements Validation

**Validates: Requirements 6.3**

- ✅ Vector store abstraction with multiple backends
- ✅ Pinecone implementation for production use
- ✅ Metadata filtering support
- ✅ Namespace support for multi-tenancy
