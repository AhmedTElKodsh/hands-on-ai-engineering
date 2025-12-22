"""
Pinecone Vector Store Implementation.

Pinecone is a fully managed vector database designed for production use cases.
It provides high performance, scalability, and reliability with minimal operational overhead.

Requirements: 6.3
"""

from typing import List, Dict, Any, Optional
import uuid
from ..vector_stores import VectorStore, Document, SearchResult, EmbeddingModel


class PineconeStore(VectorStore):
    """
    Pinecone implementation of VectorStore.
    
    Good for:
    - Production deployments
    - Large-scale applications
    - High-performance requirements
    
    Features:
    - Fully managed (no infrastructure to maintain)
    - Horizontal scaling
    - Low latency queries
    - Metadata filtering
    - Namespace support for multi-tenancy
    """

    def __init__(
        self,
        index_name: str,
        embedding_model: EmbeddingModel,
        api_key: Optional[str] = None,
        environment: Optional[str] = None,
        namespace: str = "default"
    ):
        """
        Initialize Pinecone store.
        
        Args:
            index_name: Name of the Pinecone index
            embedding_model: Embedding model for generating vectors (required)
            api_key: Pinecone API key (uses PINECONE_API_KEY env var if None)
            environment: Pinecone environment (uses PINECONE_ENVIRONMENT env var if None)
            namespace: Namespace for organizing vectors (default: "default")
        """
        try:
            import pinecone
        except ImportError:
            raise ImportError(
                "pinecone-client is required for PineconeStore. "
                "Install with: pip install pinecone-client"
            )

        if not embedding_model:
            raise ValueError("embedding_model is required for PineconeStore")

        self.index_name = index_name
        self.embedding_model = embedding_model
        self.namespace = namespace
        
        # Initialize Pinecone
        import os
        api_key = api_key or os.getenv("PINECONE_API_KEY")
        environment = environment or os.getenv("PINECONE_ENVIRONMENT")
        
        if not api_key:
            raise ValueError(
                "Pinecone API key required. "
                "Set PINECONE_API_KEY environment variable or pass api_key parameter."
            )
        
        if not environment:
            raise ValueError(
                "Pinecone environment required. "
                "Set PINECONE_ENVIRONMENT environment variable or pass environment parameter."
            )
        
        pinecone.init(api_key=api_key, environment=environment)
        
        # Get or create index
        if index_name not in pinecone.list_indexes():
            dimension = embedding_model.get_dimension()
            pinecone.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine"
            )
        
        self.index = pinecone.Index(index_name)

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to Pinecone index."""
        if not documents:
            raise ValueError("documents list cannot be empty")
        
        # Generate IDs for documents without them
        ids = []
        for doc in documents:
            if doc.id:
                ids.append(doc.id)
            else:
                doc.id = str(uuid.uuid4())
                ids.append(doc.id)
        
        # Extract content
        contents = [doc.content for doc in documents]
        
        # Generate embeddings
        embeddings = await self.embedding_model.embed_documents(contents)
        
        # Prepare vectors for upsert
        vectors = []
        for i, doc in enumerate(documents):
            # Pinecone metadata must be flat dict with string/number/bool values
            metadata = {
                "content": doc.content,
                **doc.metadata
            }
            vectors.append({
                "id": doc.id,
                "values": embeddings[i],
                "metadata": metadata
            })
        
        # Upsert in batches of 100 (Pinecone limit)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch, namespace=self.namespace)
        
        return ids

    async def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Perform similarity search in Pinecone."""
        if not query:
            raise ValueError("query cannot be empty")
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        
        # Generate query embedding
        query_embedding = await self.embedding_model.embed_query(query)
        
        # Perform search
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            namespace=self.namespace,
            filter=filter,
            include_metadata=True
        )
        
        # Convert to SearchResult objects
        search_results = []
        for match in results.matches:
            # Extract content from metadata
            content = match.metadata.pop("content", "")
            document = Document(
                content=content,
                metadata=match.metadata,
                id=match.id
            )
            search_results.append(
                SearchResult(document=document, score=match.score)
            )
        
        return search_results

    async def hybrid_search(
        self,
        query: str,
        k: int = 4,
        alpha: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search in Pinecone.
        
        Note: Pinecone doesn't natively support hybrid search (dense + sparse).
        This falls back to similarity search. For true hybrid search, use Qdrant.
        """
        if not 0 <= alpha <= 1:
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
        
        # Pinecone doesn't support hybrid search natively
        import warnings
        warnings.warn(
            "Pinecone does not support hybrid search. "
            "Falling back to similarity search. "
            "Consider using Qdrant for hybrid search capabilities."
        )
        
        return await self.similarity_search(query, k, filter)

    async def delete(self, ids: List[str]) -> None:
        """Delete documents by ID from Pinecone."""
        if not ids:
            raise ValueError("ids list cannot be empty")
        
        # Delete in batches of 1000 (Pinecone limit)
        batch_size = 1000
        for i in range(0, len(ids), batch_size):
            batch = ids[i:i + batch_size]
            self.index.delete(ids=batch, namespace=self.namespace)

    async def clear(self) -> None:
        """Clear all documents from the namespace."""
        # Delete all vectors in the namespace
        self.index.delete(delete_all=True, namespace=self.namespace)

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension from the model."""
        return self.embedding_model.get_dimension()
