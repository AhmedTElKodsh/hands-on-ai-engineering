"""
ChromaDB Vector Store Implementation.

ChromaDB is an open-source embedding database designed for development and prototyping.
It provides in-memory and persistent storage options with a simple API.

Requirements: 6.3
"""

from typing import List, Dict, Any, Optional
import uuid
from ..vector_stores import VectorStore, Document, SearchResult, EmbeddingModel


class ChromaDBStore(VectorStore):
    """
    ChromaDB implementation of VectorStore.
    
    Good for:
    - Local development and testing
    - Prototyping RAG applications
    - Small to medium datasets
    
    Features:
    - In-memory or persistent storage
    - Simple setup with no external dependencies
    - Built-in embedding functions
    """

    def __init__(
        self,
        collection_name: str = "aitea_features",
        embedding_model: Optional[EmbeddingModel] = None,
        persist_directory: Optional[str] = None
    ):
        """
        Initialize ChromaDB store.
        
        Args:
            collection_name: Name of the collection to use
            embedding_model: Embedding model for generating vectors
            persist_directory: Directory for persistent storage (None for in-memory)
        """
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError(
                "chromadb is required for ChromaDBStore. "
                "Install with: pip install chromadb"
            )

        self.collection_name = collection_name
        self.embedding_model = embedding_model
        
        # Initialize ChromaDB client
        if persist_directory:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        else:
            self.client = chromadb.Client(
                settings=Settings(anonymized_telemetry=False)
            )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to ChromaDB collection."""
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
        
        # Extract content and metadata
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Generate embeddings if model provided
        if self.embedding_model:
            embeddings = await self.embedding_model.embed_documents(contents)
            self.collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas,
                embeddings=embeddings
            )
        else:
            # Let ChromaDB use default embedding function
            self.collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas
            )
        
        return ids

    async def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Perform similarity search in ChromaDB."""
        if not query:
            raise ValueError("query cannot be empty")
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        
        # Generate query embedding if model provided
        query_embedding = None
        if self.embedding_model:
            query_embedding = await self.embedding_model.embed_query(query)
        
        # Perform search
        results = self.collection.query(
            query_texts=[query] if not query_embedding else None,
            query_embeddings=[query_embedding] if query_embedding else None,
            n_results=k,
            where=filter
        )
        
        # Convert to SearchResult objects
        search_results = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                document = Document(
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {},
                    id=doc_id
                )
                # ChromaDB returns distances, convert to similarity scores (0-1)
                distance = results['distances'][0][i] if results['distances'] else 0.0
                score = 1.0 / (1.0 + distance)  # Convert distance to similarity
                
                search_results.append(SearchResult(document=document, score=score))
        
        return search_results

    async def hybrid_search(
        self,
        query: str,
        k: int = 4,
        alpha: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search in ChromaDB.
        
        Note: ChromaDB doesn't natively support hybrid search, so this falls back
        to similarity search. For true hybrid search, use Qdrant or Weaviate.
        """
        if not 0 <= alpha <= 1:
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
        
        # ChromaDB doesn't support hybrid search natively
        # Fall back to similarity search with a warning
        import warnings
        warnings.warn(
            "ChromaDB does not support hybrid search. "
            "Falling back to similarity search. "
            "Consider using Qdrant for hybrid search capabilities."
        )
        
        return await self.similarity_search(query, k, filter)

    async def delete(self, ids: List[str]) -> None:
        """Delete documents by ID from ChromaDB."""
        if not ids:
            raise ValueError("ids list cannot be empty")
        
        self.collection.delete(ids=ids)

    async def clear(self) -> None:
        """Clear all documents from the collection."""
        # Delete the collection and recreate it
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension from the model or ChromaDB default."""
        if self.embedding_model:
            return self.embedding_model.get_dimension()
        else:
            # ChromaDB default embedding function dimension
            return 384  # all-MiniLM-L6-v2 default
