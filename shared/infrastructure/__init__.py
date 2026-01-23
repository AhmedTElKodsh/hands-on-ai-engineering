"""
Shared infrastructure components for AITEA.

This module provides reusable infrastructure components used across
the curriculum, including vector stores, LLM clients, and utilities.
"""

from .vector_store import VectorStore, create_vector_store

__all__ = [
    "VectorStore",
    "create_vector_store",
]
