"""
OpenAI Embedding Model Implementation.

Provides access to OpenAI's embedding models including text-embedding-3-small
and text-embedding-3-large.

Requirements: 6.3
"""

from typing import List, Optional
import os
from ..vector_stores import EmbeddingModel


class OpenAIEmbedding(EmbeddingModel):
    """
    OpenAI embedding model implementation.
    
    Supported models:
    - text-embedding-3-small (1536 dimensions, $0.02/1M tokens)
    - text-embedding-3-large (3072 dimensions, $0.13/1M tokens)
    - text-embedding-ada-002 (1536 dimensions, legacy)
    
    Features:
    - High quality embeddings
    - Fast inference
    - Multilingual support
    """

    DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536
    }

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize OpenAI embedding model.
        
        Args:
            model_name: Model name (default: text-embedding-3-small)
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if None)
        """
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai is required for OpenAIEmbedding. "
                "Install with: pip install openai"
            )

        self.model_name = model_name or "text-embedding-3-small"
        
        if self.model_name not in self.DIMENSIONS:
            raise ValueError(
                f"Unsupported model: {self.model_name}. "
                f"Supported models: {list(self.DIMENSIONS.keys())}"
            )
        
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key required. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.client = AsyncOpenAI(api_key=api_key)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        if not texts:
            raise ValueError("texts list cannot be empty")
        
        # OpenAI API accepts up to 2048 texts per request
        batch_size = 2048
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self.client.embeddings.create(
                model=self.model_name,
                input=batch
            )
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)
        
        return all_embeddings

    async def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query."""
        if not text:
            raise ValueError("text cannot be empty")
        
        response = await self.client.embeddings.create(
            model=self.model_name,
            input=[text]
        )
        return response.data[0].embedding

    def get_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.DIMENSIONS[self.model_name]
