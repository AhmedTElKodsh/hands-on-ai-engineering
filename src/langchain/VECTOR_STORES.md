# Vector Store Abstraction

This module provides a unified interface for working with different vector databases in AITEA's RAG (Retrieval-Augmented Generation) pipelines.

## Overview

The vector store abstraction supports three backends:

1. **ChromaDB** - Local development and prototyping
2. **Pinecone** - Production managed service
3. **Qdrant** - Hybrid search and self-hosted deployments

And three embedding providers:

1. **OpenAI** - High-quality commercial embeddings
2. **Cohere** - Multilingual embeddings with compression
3. **BGE** - Open-source local embeddings (no API key required)

## Quick Start

### ChromaDB (Development)

```python
import asyncio
from src.langchain import ChromaDBStore, BGEEmbedding, Document

async def main():
    # Create embedding model (no API key needed for BGE)
    embedding_model = BGEEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # Create ChromaDB store
    store = ChromaDBStore(
        collection_name="aitea_features",
        embedding_model=embedding_model,
        persist_directory="./chroma_db"  # None for in-memory
    )

    # Add documents
    documents = [
        Document(
            content="CRUD API endpoints for user management",
            metadata={"team": "backend", "feature": "user-crud"}
        ),
        Document(
            content="React component library with Material-UI",
            metadata={"team": "frontend", "feature": "component-library"}
        )
    ]

    doc_ids = await store.add_documents(documents)
    print(f"Added {len(doc_ids)} documents")

    # Search
    results = await store.similarity_search("user management API", k=2)
    for result in results:
        print(f"Score: {result.score:.3f}")
        print(f"Content: {result.document.content}")
        print(f"Metadata: {result.document.metadata}")
        print()

asyncio.run(main())
```

### Pinecone (Production)

```python
import asyncio
from src.langchain import PineconeStore, OpenAIEmbedding, Document

async def main():
    # Create OpenAI embedding model
    embedding_model = OpenAIEmbedding(
        model_name="text-embedding-3-small"
        # api_key will be read from OPENAI_API_KEY env var
    )

    # Create Pinecone store
    store = PineconeStore(
        index_name="aitea-features",
        embedding_model=embedding_model,
        # api_key and environment will be read from env vars:
        # PINECONE_API_KEY and PINECONE_ENVIRONMENT
        namespace="production"
    )

    # Add documents
    documents = [
        Document(
            content="Authentication with JWT tokens",
            metadata={"team": "backend", "process": "Authentication"}
        )
    ]

    await store.add_documents(documents)

    # Search with metadata filter
    results = await store.similarity_search(
        "login system",
        k=5,
        filter={"team": "backend"}
    )

    for result in results:
        print(f"{result.score:.3f}: {result.document.content}")

asyncio.run(main())
```

### Qdrant (Hybrid Search)

```python
import asyncio
from src.langchain import QdrantStore, CohereEmbedding, Document

async def main():
    # Create Cohere embedding model
    embedding_model = CohereEmbedding(
        model_name="embed-english-v3.0"
        # api_key will be read from COHERE_API_KEY env var
    )

    # Create Qdrant store
    store = QdrantStore(
        collection_name="aitea_features",
        embedding_model=embedding_model,
        url="http://localhost:6333"  # or Qdrant Cloud URL
    )

    # Add documents
    documents = [
        Document(
            content="Real-time WebSocket chat implementation",
            metadata={"team": "backend", "process": "Real-time"}
        ),
        Document(
            content="WebSocket client with React hooks",
            metadata={"team": "frontend", "process": "Real-time"}
        )
    ]

    await store.add_documents(documents)

    # Hybrid search (dense + sparse)
    results = await store.hybrid_search(
        "websocket chat",
        k=5,
        alpha=0.7  # 0.7 weight to dense, 0.3 to sparse
    )

    for result in results:
        print(f"{result.score:.3f}: {result.document.content}")

asyncio.run(main())
```

## Embedding Model Comparison

| Provider | Model                   | Dimensions | Cost            | Best For                      |
| -------- | ----------------------- | ---------- | --------------- | ----------------------------- |
| OpenAI   | text-embedding-3-small  | 1536       | $0.02/1M tokens | General purpose, high quality |
| OpenAI   | text-embedding-3-large  | 3072       | $0.13/1M tokens | Maximum quality               |
| Cohere   | embed-english-v3.0      | 1024       | $0.10/1M tokens | English text                  |
| Cohere   | embed-multilingual-v3.0 | 1024       | $0.10/1M tokens | 100+ languages                |
| BGE      | bge-small-en-v1.5       | 384        | Free (local)    | Development, privacy          |
| BGE      | bge-base-en-v1.5        | 768        | Free (local)    | Balanced quality/speed        |
| BGE      | bge-large-en-v1.5       | 1024       | Free (local)    | Best local quality            |

## Vector Store Comparison

| Feature            | ChromaDB          | Pinecone            | Qdrant                |
| ------------------ | ----------------- | ------------------- | --------------------- |
| Deployment         | Local/Self-hosted | Managed Cloud       | Both                  |
| Hybrid Search      | ❌                | ❌                  | ✅                    |
| Metadata Filtering | ✅                | ✅                  | ✅ (Advanced)         |
| Scalability        | Medium            | High                | High                  |
| Setup Complexity   | Low               | Low                 | Medium                |
| Cost               | Free              | Pay-per-use         | Free (self-hosted)    |
| Best For           | Development       | Production (simple) | Production (advanced) |

## Factory Function

Use the factory function for easy embedding model creation:

```python
from src.langchain import create_embedding_model, EmbeddingProvider

# OpenAI
openai_model = create_embedding_model(
    provider=EmbeddingProvider.OPENAI,
    model_name="text-embedding-3-small"
)

# Cohere
cohere_model = create_embedding_model(
    provider=EmbeddingProvider.COHERE,
    model_name="embed-english-v3.0"
)

# BGE (local, no API key)
bge_model = create_embedding_model(
    provider=EmbeddingProvider.BGE,
    model_name="BAAI/bge-small-en-v1.5"
)
```

## Advanced Usage

### Batch Operations

```python
# Add many documents efficiently
documents = [Document(content=f"Feature {i}", metadata={"id": i})
             for i in range(1000)]

# ChromaDB and Pinecone handle batching internally
doc_ids = await store.add_documents(documents)
```

### Metadata Filtering

```python
# Pinecone filter syntax
results = await pinecone_store.similarity_search(
    "authentication",
    k=10,
    filter={"team": "backend", "process": "Authentication"}
)

# Qdrant supports more complex filters
results = await qdrant_store.similarity_search(
    "authentication",
    k=10,
    filter={"team": "backend"}  # Simplified in this implementation
)
```

### Hybrid Search Tuning

```python
# Alpha controls dense vs sparse weighting
# alpha=1.0: Pure dense (semantic) search
# alpha=0.5: Balanced hybrid search
# alpha=0.0: Pure sparse (keyword) search

results = await qdrant_store.hybrid_search(
    "user authentication JWT",
    k=10,
    alpha=0.7  # Favor semantic similarity
)
```

## Installation

### ChromaDB

```bash
uv add chromadb
```

### Pinecone

```bash
uv add pinecone-client
```

### Qdrant

```bash
uv add qdrant-client
```

### Embeddings

```bash
# OpenAI
uv add openai

# Cohere
uv add cohere

# BGE (local)
uv add sentence-transformers
```

## Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Cohere
export COHERE_API_KEY="..."

# Pinecone
export PINECONE_API_KEY="..."
export PINECONE_ENVIRONMENT="us-west1-gcp"

# Qdrant Cloud (optional)
export QDRANT_URL="https://..."
export QDRANT_API_KEY="..."
```

## Integration with AITEA

Use vector stores in RAG pipelines for feature estimation:

```python
from src.langchain import create_estimation_chain, ChromaDBStore, BGEEmbedding

# Create vector store with historical features
embedding_model = BGEEmbedding()
vector_store = ChromaDBStore(
    collection_name="feature_library",
    embedding_model=embedding_model
)

# Add historical features
await vector_store.add_documents([
    Document(
        content="User authentication with OAuth2",
        metadata={"hours": 16, "team": "backend"}
    ),
    # ... more features
])

# Create estimation chain with RAG
estimation_chain = create_estimation_chain(
    llm=llm,
    retriever=vector_store  # Pass vector store as retriever
)

# Estimate with context from similar features
result = await estimation_chain.ainvoke({
    "feature_description": "Implement JWT authentication"
})
```

## Testing

Comprehensive tests are available for each vector store implementation:

```bash
# Run all vector store tests
pytest tests/langchain/test_chromadb_store.py -v
pytest tests/langchain/test_pinecone_store.py -v
pytest tests/langchain/test_qdrant_store.py -v

# Run specific test
pytest tests/langchain/test_chromadb_store.py::TestChromaDBStore::test_similarity_search -v
pytest tests/langchain/test_qdrant_store.py::TestQdrantStore::test_hybrid_search -v
```

### Test Coverage

All vector store implementations have comprehensive test coverage:

#### ChromaDB Store Tests

| Test                                        | Description                           |
| ------------------------------------------- | ------------------------------------- |
| `test_add_documents`                        | Adding documents to the store         |
| `test_add_documents_empty_raises`           | Validation for empty document list    |
| `test_similarity_search`                    | Basic similarity search functionality |
| `test_similarity_search_empty_query_raises` | Validation for empty queries          |
| `test_similarity_search_invalid_k_raises`   | Validation for k parameter            |
| `test_delete_documents`                     | Deleting documents by ID              |
| `test_delete_empty_raises`                  | Validation for empty ID list          |
| `test_clear`                                | Clearing all documents                |
| `test_hybrid_search_fallback`               | Hybrid search falls back with warning |
| `test_hybrid_search_invalid_alpha_raises`   | Validation for alpha parameter        |
| `test_get_embedding_dimension`              | Getting embedding dimension           |
| `test_document_with_custom_id`              | Custom document IDs                   |
| `test_metadata_filter`                      | Filtering by metadata                 |

#### Qdrant Store Tests

| Test                                            | Description                                 |
| ----------------------------------------------- | ------------------------------------------- |
| `test_init_requires_embedding_model`            | Validation for required embedding model     |
| `test_init_creates_collection_if_not_exists`    | Collection creation on initialization       |
| `test_init_skips_creation_if_collection_exists` | Skip creation for existing collections      |
| `test_add_documents`                            | Adding documents to the store               |
| `test_add_documents_empty_raises`               | Validation for empty document list          |
| `test_add_documents_preserves_custom_ids`       | Custom document IDs are preserved           |
| `test_similarity_search`                        | Basic similarity search functionality       |
| `test_similarity_search_empty_query_raises`     | Validation for empty queries                |
| `test_similarity_search_invalid_k_raises`       | Validation for k parameter                  |
| `test_similarity_search_with_filter`            | Filtering by metadata                       |
| `test_hybrid_search`                            | Hybrid search (dense + sparse)              |
| `test_hybrid_search_alpha_weighting`            | Alpha parameter controls dense/sparse mix   |
| `test_hybrid_search_invalid_alpha_raises`       | Validation for alpha parameter              |
| `test_hybrid_search_empty_query_raises`         | Validation for empty queries                |
| `test_hybrid_search_invalid_k_raises`           | Validation for k parameter                  |
| `test_hybrid_search_with_filter`                | Hybrid search with metadata filtering       |
| `test_hybrid_search_handles_scroll_failure`     | Graceful handling of sparse search failures |
| `test_delete_documents`                         | Deleting documents by ID                    |
| `test_delete_empty_raises`                      | Validation for empty ID list                |
| `test_clear`                                    | Clearing all documents                      |
| `test_get_embedding_dimension`                  | Getting embedding dimension                 |
| `test_metadata_stored_correctly`                | Metadata storage in Qdrant format           |
| `test_import_error_without_qdrant`              | Error handling for missing dependencies     |
| `test_init_with_api_key`                        | Qdrant Cloud authentication                 |
| `test_init_with_grpc`                           | gRPC connection preference                  |

### Writing Tests

When testing vector stores, use in-memory mode for fast, isolated tests:

```python
import pytest
from src.langchain.stores import ChromaDBStore
from src.langchain.vector_stores import Document

@pytest.fixture
def store():
    """Create fresh in-memory store for each test."""
    return ChromaDBStore(
        collection_name="test_collection",
        embedding_model=None,  # Use ChromaDB default
        persist_directory=None  # In-memory
    )

@pytest.mark.asyncio
async def test_my_feature(store):
    docs = [Document(content="Test content", metadata={"key": "value"})]
    ids = await store.add_documents(docs)
    assert len(ids) == 1
```

## Requirements

This implementation satisfies:

- **Requirement 6.3**: RAG pipeline with multiple vector stores (ChromaDB, Pinecone, Qdrant) and embedding model selection

## Next Steps

1. Implement advanced retrievers (HyDE, reranking) - Phase 8
2. Add evaluation metrics (RAGAS) - Phase 8
3. Implement Graph RAG with Neo4j - Phase 8
4. Add Agentic RAG patterns (Self-RAG, CRAG) - Phase 8
