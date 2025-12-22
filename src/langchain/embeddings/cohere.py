"""
Cohere Embedding Model Implementation.

Provides access to Cohere's embedding models with support for English and
multilingual embeddings.

Requirements: 6.3
"""

from typing import List, Optional
import os
from ..vector_stores import EmbeddingModel


class CohereEmbedding(EmbeddingModel):
    """
    Cohere embedding model implementation.
    
    Supported models:
    - embed-english-v3.0 (1024 dimensions, English only)
    - embed-multilingual-v3.0 (1024 dimensions, 100+ languages)
    - embed-english-light-v3.0 (384 dimensions, faster)
    - embed-multilingual-light-v3.0 (384 dimensions, faster)
    
    Features:
    - Multilingual support
    - Compression-aware embeddings
    - Search and classification optimized variants
    """

    DIMENSIONS = {
        "embed-english-v3.0": 1024,
        "embed-multilingual-v3.0": 1024,
        "embed-english-light-v3.0": 384,
        "embed-multilingual-light-v3.0": 384
    }

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        input_type: str = "search_document"
    ):
        """
        Initialize Cohere embedding model.
        
        Args:
            model_name: Model name (default: embed-english-v3.0)
            api_key: Cohere API key (uses COHERE_API_KEY env var if None)
            input_type: Type of input - "search_document", "search_query", or "classification"
        """
        try:
            import cohere
        except ImportError:
            raise ImportError(
                "cohere is required for CohereEmbedding. "
                "Install with: pip install cohere"
            )

        self.model_name = model_name or "embed-english-v3.0"
        
        if self.model_name not in self.DIMENSIONS:
            raise ValueError(
                f"Unsupported model: {self.model_name}. "
                f"Supported models: {list(self.DIMENSIONS.keys())}"
            )
        
        if input_type not in ["search_document", "search_query", "classification"]:
            raise ValueError(
                f"Invalid input_type: {input_type}. "
                "Must be 'search_document', 'search_query', or 'classification'"
            )
        
        self.input_type = input_type
        
        api_key = api_key or os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError(
                "Cohere API key required. "
                "Set COHERE_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = cohere.AsyncClient(api_key=api_key)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        if not texts:
            raise ValueError("texts list cannot be empty")
        
        # Cohere API accepts up to 96 texts per request
        batch_size = 96
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self.client.embed(
                texts=batch,
                model=self.model_name,
                input_type="search_document"  # Always use search_document for documents
            )
            all_embeddings.extend(response.embeddings)
        
        return all_embeddings

    async def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query."""
        if not text:
            raise ValueError("text cannot be empty")
        
        response = await self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type="search_query"  # Use search_query for queries
        )
        return response.embeddings[0]

    def get_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.DIMENSIONS[self.model_name]
