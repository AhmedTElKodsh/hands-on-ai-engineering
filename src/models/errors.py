"""Error types for AITEA services.

This module provides structured error types for validation, not-found,
import, and estimation errors, following the Result pattern for
explicit error handling.
"""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ValidationError:
    """Error indicating invalid field data.
    
    Attributes:
        field: Name of the field that failed validation
        message: Human-readable error description
        value: The invalid value that was provided
    """
    field: str
    message: str
    value: Any
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        return f"Validation error on '{self.field}': {self.message} (got: {self.value!r})"


@dataclass
class NotFoundError:
    """Error indicating a requested resource was not found.
    
    Attributes:
        resource_type: Type of resource (e.g., "Feature", "TrackedTimeEntry")
        identifier: The identifier that was searched for
        message: Optional additional context
    """
    resource_type: str
    identifier: str
    message: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        base = f"{self.resource_type} with identifier '{self.identifier}' not found"
        if self.message:
            return f"{base}: {self.message}"
        return base


@dataclass
class ImportError:
    """Error indicating a failure during data import.
    
    Attributes:
        row_number: The row number where the error occurred (1-indexed)
        errors: List of validation errors for this row
        source: Optional source file or identifier
    """
    row_number: int
    errors: List[ValidationError]
    source: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        error_details = "; ".join(str(e) for e in self.errors)
        base = f"Import error at row {self.row_number}: {error_details}"
        if self.source:
            return f"{base} (source: {self.source})"
        return base


@dataclass
class EstimationError:
    """Error indicating a failure during estimation.
    
    Attributes:
        feature_name: Name of the feature that failed estimation
        reason: Description of why estimation failed
        details: Optional additional context or data
    """
    feature_name: str
    reason: str
    details: Optional[Any] = None
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        base = f"Estimation error for '{self.feature_name}': {self.reason}"
        if self.details:
            return f"{base} (details: {self.details!r})"
        return base
