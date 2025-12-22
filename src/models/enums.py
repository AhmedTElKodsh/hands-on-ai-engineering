"""Enumerations for AITEA models."""

from enum import Enum


class TeamType(str, Enum):
    """Team types for feature categorization."""
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DESIGN = "design"
    QA = "qa"
    DEVOPS = "devops"


class ProcessType(str, Enum):
    """Process types for feature categorization."""
    DATA_OPERATIONS = "Data Operations"
    CONTENT_MANAGEMENT = "Content Management"
    REAL_TIME = "Real-time"
    AUTHENTICATION = "Authentication"
    INTEGRATION = "Integration"


class ConfidenceLevel(str, Enum):
    """Confidence levels for estimates based on data point count."""
    LOW = "low"      # 1-2 data points
    MEDIUM = "medium"  # 3-9 data points
    HIGH = "high"    # 10+ data points



