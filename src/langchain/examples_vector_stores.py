"""
Example usage of vector stores for AITEA feature library RAG.

This demonstrates how to use different vector stores and embedding models
for building a retrieval-augmented generation system for feature estimation.

Requirements: 6.3
"""

import asyncio
from typing import List
from .vector_stores import Document, SearchResult, EmbeddingProvider, create_embedding_model
from .stores import ChromaDBStore


async def example_chromadb_with_bge():
    """
    Example: ChromaDB with BGE embeddings (no API key required).
    
    Perfect for local development and testing.
    """
    print("=" * 60)
    print("Example 1: ChromaDB with BGE Embeddings")
    print("=" * 60)
    
    # Create BGE embedding model (runs locally)
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.BGE,
        model_name="BAAI/bge-small-en-v1.5"
    )
    
    # Create ChromaDB store (in-memory)
    store = ChromaDBStore(
        collection_name="aitea_features_example",
        embedding_model=embedding_model,
        persist_directory=None  # In-memory for this example
    )
    
    # Sample feature library documents
    documents = [
        Document(
            content="CRUD API endpoints with REST for user management. Includes create, read, update, delete operations with validation.",
            metadata={
                "feature": "user-crud",
                "team": "backend",
                "process": "Data Operations",
                "seed_hours": 8.0
            }
        ),
        Document(
            content="JWT authentication system with refresh tokens. Secure token generation and validation.",
            metadata={
                "feature": "jwt-auth",
                "team": "backend",
                "process": "Authentication",
                "seed_hours": 16.0
            }
        ),
        Document(
            content="React component library with Material-UI. Reusable UI components following design system.",
            metadata={
                "feature": "component-library",
                "team": "frontend",
                "process": "Content Management",
                "seed_hours": 24.0
            }
        ),
        Document(
            content="WebSocket real-time chat with message persistence. Bidirectional communication with Redis pub/sub.",
            metadata={
                "feature": "realtime-chat",
                "team": "fullstack",
                "process": "Real-time",
                "seed_hours": 32.0
            }
        ),
        Document(
            content="OAuth2 integration with Google and GitHub. Social login with profile synchronization.",
            metadata={
                "feature": "oauth-integration",
                "team": "backend",
                "process": "Authentication",
                "seed_hours": 20.0
            }
        )
    ]
    
    # Add documents to store
    print(f"\nAdding {len(documents)} documents to ChromaDB...")
    doc_ids = await store.add_documents(documents)
    print(f"✓ Added documents with IDs: {doc_ids[:2]}... (showing first 2)")
    
    # Example 1: Search for authentication features
    print("\n" + "-" * 60)
    print("Query 1: 'user login and authentication'")
    print("-" * 60)
    
    results = await store.similarity_search(
        query="user login and authentication",
        k=3
    )
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (score: {result.score:.3f}):")
        print(f"  Content: {result.document.content[:80]}...")
        print(f"  Feature: {result.document.metadata.get('feature')}")
        print(f"  Team: {result.document.metadata.get('team')}")
        print(f"  Seed Hours: {result.document.metadata.get('seed_hours')}")
    
    # Example 2: Search for frontend features
    print("\n" + "-" * 60)
    print("Query 2: 'UI components and design'")
    print("-" * 60)
    
    results = await store.similarity_search(
        query="UI components and design",
        k=2
    )
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (score: {result.score:.3f}):")
        print(f"  Content: {result.document.content[:80]}...")
        print(f"  Feature: {result.document.metadata.get('feature')}")
        print(f"  Team: {result.document.metadata.get('team')}")
    
    # Example 3: Search for real-time features
    print("\n" + "-" * 60)
    print("Query 3: 'websocket messaging'")
    print("-" * 60)
    
    results = await store.similarity_search(
        query="websocket messaging",
        k=2
    )
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (score: {result.score:.3f}):")
        print(f"  Content: {result.document.content[:80]}...")
        print(f"  Feature: {result.document.metadata.get('feature')}")
        print(f"  Seed Hours: {result.document.metadata.get('seed_hours')}")
    
    # Clean up
    await store.clear()
    print("\n✓ Cleaned up ChromaDB collection")


async def example_rag_estimation():
    """
    Example: Using vector store for RAG-based feature estimation.
    
    This shows how to retrieve similar features and use them for estimation.
    """
    print("\n\n" + "=" * 60)
    print("Example 2: RAG-Based Feature Estimation")
    print("=" * 60)
    
    # Create embedding model
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.BGE,
        model_name="BAAI/bge-small-en-v1.5"
    )
    
    # Create store
    store = ChromaDBStore(
        collection_name="aitea_estimation",
        embedding_model=embedding_model
    )
    
    # Add historical features with actual time data
    historical_features = [
        Document(
            content="REST API for product catalog with search and filtering",
            metadata={
                "feature": "product-api",
                "actual_hours": 12.5,
                "team": "backend"
            }
        ),
        Document(
            content="User authentication with email/password and session management",
            metadata={
                "feature": "basic-auth",
                "actual_hours": 14.0,
                "team": "backend"
            }
        ),
        Document(
            content="Shopping cart with add/remove items and quantity updates",
            metadata={
                "feature": "shopping-cart",
                "actual_hours": 18.0,
                "team": "fullstack"
            }
        )
    ]
    
    await store.add_documents(historical_features)
    print(f"\n✓ Added {len(historical_features)} historical features")
    
    # New feature to estimate
    new_feature = "Implement user registration with email verification"
    
    print(f"\n📝 Estimating: '{new_feature}'")
    print("\nRetrieving similar historical features...")
    
    # Retrieve similar features
    similar_features = await store.similarity_search(
        query=new_feature,
        k=2
    )
    
    print("\nSimilar features found:")
    total_hours = 0
    for i, result in enumerate(similar_features, 1):
        actual_hours = result.document.metadata.get('actual_hours', 0)
        total_hours += actual_hours
        print(f"\n  {i}. {result.document.content}")
        print(f"     Similarity: {result.score:.3f}")
        print(f"     Actual hours: {actual_hours}")
    
    # Simple estimation based on similar features
    if similar_features:
        avg_hours = total_hours / len(similar_features)
        print(f"\n💡 Estimated hours: {avg_hours:.1f} (average of similar features)")
        print(f"   Range: {avg_hours * 0.8:.1f} - {avg_hours * 1.2:.1f} hours")
    
    # Clean up
    await store.clear()
    print("\n✓ Cleaned up")


async def example_metadata_filtering():
    """
    Example: Using metadata filters to narrow search results.
    """
    print("\n\n" + "=" * 60)
    print("Example 3: Metadata Filtering")
    print("=" * 60)
    
    # Create embedding model
    embedding_model = create_embedding_model(
        provider=EmbeddingProvider.BGE,
        model_name="BAAI/bge-small-en-v1.5"
    )
    
    # Create store
    store = ChromaDBStore(
        collection_name="aitea_filtered",
        embedding_model=embedding_model
    )
    
    # Add features from different teams
    documents = [
        Document(
            content="Backend API for user management",
            metadata={"team": "backend", "priority": "high"}
        ),
        Document(
            content="Frontend dashboard with charts",
            metadata={"team": "frontend", "priority": "medium"}
        ),
        Document(
            content="Backend payment processing integration",
            metadata={"team": "backend", "priority": "high"}
        ),
        Document(
            content="Frontend mobile responsive design",
            metadata={"team": "frontend", "priority": "low"}
        )
    ]
    
    await store.add_documents(documents)
    print(f"\n✓ Added {len(documents)} features")
    
    # Search without filter
    print("\n" + "-" * 60)
    print("Search: 'user interface' (no filter)")
    print("-" * 60)
    
    results = await store.similarity_search("user interface", k=3)
    for result in results:
        print(f"  • {result.document.content} [{result.document.metadata['team']}]")
    
    # Search with team filter
    print("\n" + "-" * 60)
    print("Search: 'user interface' (team=backend only)")
    print("-" * 60)
    
    results = await store.similarity_search(
        "user interface",
        k=3,
        filter={"team": "backend"}
    )
    for result in results:
        print(f"  • {result.document.content} [{result.document.metadata['team']}]")
    
    # Clean up
    await store.clear()
    print("\n✓ Cleaned up")


async def main():
    """Run all examples."""
    print("\n🚀 AITEA Vector Store Examples\n")
    
    try:
        # Example 1: Basic ChromaDB usage
        await example_chromadb_with_bge()
        
        # Example 2: RAG-based estimation
        await example_rag_estimation()
        
        # Example 3: Metadata filtering
        await example_metadata_filtering()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\nTo run these examples, install:")
        print("  pip install chromadb sentence-transformers")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
