"""Shared data models for AI Knowledge Base.

This module provides Pydantic models for:
- Enums and type definitions
- Contract models
- Compliance checking
- Version management
- Result types for error handling
"""

from shared.models.enums import *
from shared.models.result import Result, Ok, Err, UnwrapError

__all__ = [
    'Result',
    'Ok',
    'Err',
    'UnwrapError',
]
