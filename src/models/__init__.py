"""Data models and types for AITEA."""

from .dataclasses import (
    Feature,
    TrackedTimeEntry,
    ProjectEstimate,
    EstimationConfig,
    FeatureEstimate,
    FeatureStatistics,
)
from .enums import TeamType, ProcessType, ConfidenceLevel
from .errors import (
    ValidationError,
    NotFoundError,
    ImportError,
    EstimationError,
)
from .result import Result, Ok, Err, UnwrapError

__all__ = [
    # Dataclasses
    "Feature",
    "TrackedTimeEntry",
    "ProjectEstimate",
    "EstimationConfig",
    "FeatureEstimate",
    "FeatureStatistics",
    # Enums
    "TeamType",
    "ProcessType",
    "ConfidenceLevel",
    # Error types
    "ValidationError",
    "NotFoundError",
    "ImportError",
    "EstimationError",
    # Result pattern
    "Result",
    "Ok",
    "Err",
    "UnwrapError",
]
