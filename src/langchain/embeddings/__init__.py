"""
Embedding model implementations for AITEA.

Supports multiple embedding providers:
- OpenAI (text-embedding-3-small, text-embedding-3-large)
- Cohere (embed-english-v3.0, embed-multilingual-v3.0)
- BGE (BAAI/bge-small-en-v1.5, BAAI/bge-base-en-v1.5)

Requirements: 6.3
"""

from .openai import OpenAIEmbedding
from .cohere import CohereEmbedding
from .bge import BGEEmbedding

__all__ = ["OpenAIEmbedding", "CohereEmbedding", "BGEEmbedding"]
