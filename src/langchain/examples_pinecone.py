"""
Example usage of Pinecone Vector Store for AITEA.

This module demonstrates how to use the Pinecone vector store
for production RAG applications.

Requirements: 6.3
"""

import asyncio
import os
from typing import List

from .stores import PineconeStore
from .vector_stores import Document, EmbeddingProvider, create_embedding_model


async def example_basic_usage():
    """Basic example of using Pinecone store."""
    print("=== Basic Pinecone Usage ===\n")
    
    # Check for API keys
    if not os.getenv("PINECONE_API_KEY"):
        print("⚠️  PINECONE_API_KEY not set. This example requires a Pinecone API key.")
        print("Set it with: export PINECONE_API_KEY='your-key-here'")
        return
    
    if not os.getenv("PINECONE_ENVIRONMENT"):
        print("⚠️  PINECONE_ENVIRONMENT not set. This example requires a Pinecone environment.")
        print("Set it with: export PINECONE_ENVIRONMENT='us-west1-gcp'")
        return
    
    # Create embedding model
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.OPENAI,
        model_name="text-embedding-3-small"
    )
    
    # Initialize Pinecone store
    store = PineconeStore(
        index_name="aitea-examples",
        embedding_model=embedding_model,
        namespace="demo"
    )
    
    print(f"✓ Connected to Pinecone index: aitea-examples")
    print(f"✓ Using namespace: demo")
    print(f"✓ Embedding dimension: {store.get_embedding_dimension()}\n")
    
    # Create sample documents
    documents = [
        Document(
            content="CRUD API endpoints for user management with authentication",
            metadata={"category": "backend", "team": "api", "complexity": "medium"}
        ),
        Document(
            content="Real-time chat interface using WebSocket connections",
            metadata={"category": "frontend", "team": "ui", "complexity": "high"}
        ),
        Document(
            content="Database migration scripts for PostgreSQL schema updates",
            metadata={"category": "backend", "team": "data", "complexity": "low"}
        ),
        Document(
            content="Responsive dashboard with charts and data visualization",
            metadata={"category": "frontend", "team": "ui", "complexity": "medium"}
        ),
    ]
    
    # Add documents
    print("Adding documents to Pinecone...")
    ids = await store.add_documents(documents)
    print(f"✓ Added {len(ids)} documents\n")
    
    # Search for similar documents
    print("Searching for 'user authentication features'...")
    results = await store.similarity_search(
        query="user authentication features",
        k=3
    )
    
    print(f"Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result.score:.3f}")
        print(f"   Content: {result.document.content}")
        print(f"   Team: {result.document.metadata.get('team')}")
        print(f"   Complexity: {result.document.metadata.get('complexity')}\n")
    
    # Search with metadata filter
    print("Searching for 'interface' in frontend category...")
    results = await store.similarity_search(
        query="interface",
        k=5,
        filter={"category": "frontend"}
    )
    
    print(f"Found {len(results)} frontend results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result.score:.3f}")
        print(f"   Content: {result.document.content}\n")
    
    # Clean up
    print("Cleaning up demo namespace...")
    await store.clear()
    print("✓ Demo complete!")


async def example_batch_operations():
    """Example of batch operations with Pinecone."""
    print("\n=== Batch Operations Example ===\n")
    
    if not os.getenv("PINECONE_API_KEY") or not os.getenv("PINECONE_ENVIRONMENT"):
        print("⚠️  Pinecone credentials not set. Skipping batch example.")
        return
    
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.OPENAI,
        model_name="text-embedding-3-small"
    )
    
    store = PineconeStore(
        index_name="aitea-examples",
        embedding_model=embedding_model,
        namespace="batch-demo"
    )
    
    # Create a large batch of documents (will be automatically batched)
    print("Creating 250 documents (will be batched automatically)...")
    large_batch = [
        Document(
            content=f"Feature {i}: Implementation of component {i}",
            metadata={"index": i, "batch": i // 100}
        )
        for i in range(250)
    ]
    
    print("Adding documents in batches of 100...")
    ids = await store.add_documents(large_batch)
    print(f"✓ Added {len(ids)} documents in {(len(ids) + 99) // 100} batches\n")
    
    # Delete in batches
    print("Deleting documents in batches...")
    await store.delete(ids)
    print(f"✓ Deleted {len(ids)} documents\n")
    
    print("✓ Batch operations complete!")


async def example_namespace_isolation():
    """Example of using namespaces for multi-tenancy."""
    print("\n=== Namespace Isolation Example ===\n")
    
    if not os.getenv("PINECONE_API_KEY") or not os.getenv("PINECONE_ENVIRONMENT"):
        print("⚠️  Pinecone credentials not set. Skipping namespace example.")
        return
    
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.OPENAI,
        model_name="text-embedding-3-small"
    )
    
    # Create stores for different tenants
    tenant_a_store = PineconeStore(
        index_name="aitea-examples",
        embedding_model=embedding_model,
        namespace="tenant-a"
    )
    
    tenant_b_store = PineconeStore(
        index_name="aitea-examples",
        embedding_model=embedding_model,
        namespace="tenant-b"
    )
    
    # Add documents to tenant A
    print("Adding documents to Tenant A namespace...")
    await tenant_a_store.add_documents([
        Document(content="Tenant A feature 1", metadata={"tenant": "a"}),
        Document(content="Tenant A feature 2", metadata={"tenant": "a"}),
    ])
    
    # Add documents to tenant B
    print("Adding documents to Tenant B namespace...")
    await tenant_b_store.add_documents([
        Document(content="Tenant B feature 1", metadata={"tenant": "b"}),
        Document(content="Tenant B feature 2", metadata={"tenant": "b"}),
    ])
    
    # Search in tenant A - should only return tenant A docs
    print("\nSearching in Tenant A namespace...")
    results_a = await tenant_a_store.similarity_search("feature", k=10)
    print(f"Found {len(results_a)} results in Tenant A")
    for result in results_a:
        print(f"  - {result.document.content}")
    
    # Search in tenant B - should only return tenant B docs
    print("\nSearching in Tenant B namespace...")
    results_b = await tenant_b_store.similarity_search("feature", k=10)
    print(f"Found {len(results_b)} results in Tenant B")
    for result in results_b:
        print(f"  - {result.document.content}")
    
    # Clean up
    print("\nCleaning up namespaces...")
    await tenant_a_store.clear()
    await tenant_b_store.clear()
    print("✓ Namespace isolation example complete!")


async def main():
    """Run all Pinecone examples."""
    print("=" * 60)
    print("Pinecone Vector Store Examples for AITEA")
    print("=" * 60)
    
    try:
        await example_basic_usage()
        await example_batch_operations()
        await example_namespace_isolation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set PINECONE_API_KEY environment variable")
        print("2. Set PINECONE_ENVIRONMENT environment variable")
        print("3. Set OPENAI_API_KEY environment variable")
        print("4. Installed pinecone-client: pip install pinecone-client")


if __name__ == "__main__":
    asyncio.run(main())
