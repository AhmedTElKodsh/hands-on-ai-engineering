"""
BGE (BAAI General Embedding) Model Implementation.

BGE models are open-source embedding models from Beijing Academy of Artificial Intelligence.
They can be run locally without API keys, making them ideal for development and privacy-sensitive applications.

Requirements: 6.3
"""

from typing import List, Optional
from ..vector_stores import EmbeddingModel


class BGEEmbedding(EmbeddingModel):
    """
    BGE embedding model implementation using sentence-transformers.
    
    Supported models:
    - BAAI/bge-small-en-v1.5 (384 dimensions, fast)
    - BAAI/bge-base-en-v1.5 (768 dimensions, balanced)
    - BAAI/bge-large-en-v1.5 (1024 dimensions, best quality)
    
    Features:
    - Runs locally (no API key required)
    - Privacy-friendly (no data sent to external services)
    - Good performance on retrieval tasks
    - Free to use
    """

    DIMENSIONS = {
        "BAAI/bge-small-en-v1.5": 384,
        "BAAI/bge-base-en-v1.5": 768,
        "BAAI/bge-large-en-v1.5": 1024
    }

    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize BGE embedding model.
        
        Args:
            model_name: Model name (default: BAAI/bge-small-en-v1.5)
            device: Device to run on - "cpu", "cuda", or None for auto-detect
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for BGEEmbedding. "
                "Install with: pip install sentence-transformers"
            )

        self.model_name = model_name or "BAAI/bge-small-en-v1.5"
        
        if self.model_name not in self.DIMENSIONS:
            raise ValueError(
                f"Unsupported model: {self.model_name}. "
                f"Supported models: {list(self.DIMENSIONS.keys())}"
            )
        
        # Load model
        self.model = SentenceTransformer(self.model_name, device=device)
        
        # BGE models benefit from adding instruction prefix for queries
        self.query_instruction = "Represent this sentence for searching relevant passages: "

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        if not texts:
            raise ValueError("texts list cannot be empty")
        
        # sentence-transformers encode is synchronous, but we wrap in async
        # For true async, you'd need to use asyncio.to_thread or similar
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,  # Normalize for cosine similarity
            show_progress_bar=False
        )
        
        # Convert numpy arrays to lists
        return [emb.tolist() for emb in embeddings]

    async def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query."""
        if not text:
            raise ValueError("text cannot be empty")
        
        # Add instruction prefix for queries (improves retrieval performance)
        query_text = self.query_instruction + text
        
        embedding = self.model.encode(
            query_text,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        
        return embedding.tolist()

    def get_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.DIMENSIONS[self.model_name]
