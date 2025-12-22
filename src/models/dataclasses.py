"""Core dataclass models for AITEA."""

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List, Optional, Dict, Any

from .enums import TeamType, ConfidenceLevel


@dataclass
class Feature:
    """A software feature with time estimation metadata.
    
    Attributes:
        id: Unique identifier for the feature
        name: Display name of the feature
        team: Team responsible for implementation
        process: Process type (e.g., "Data Operations")
        seed_time_hours: Initial time estimate before historical data
        synonyms: Alternative names for feature matching
        notes: Additional context or implementation notes
    """
    id: str
    name: str
    team: TeamType
    process: str
    seed_time_hours: float
    synonyms: List[str] = field(default_factory=list)
    notes: str = ""
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if not self.id:
            raise ValueError("Feature id cannot be empty")
        if not self.name:
            raise ValueError("Feature name cannot be empty")
        if self.seed_time_hours <= 0:
            raise ValueError("seed_time_hours must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON persistence."""
        data = asdict(self)
        data['team'] = self.team.value  # Convert enum to string
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feature':
        """Deserialize from dictionary."""
        data = data.copy()
        data['team'] = TeamType(data['team'])  # Convert string to enum
        return cls(**data)


@dataclass
class TrackedTimeEntry:
    """A record of actual time spent on a feature.
    
    Attributes:
        id: Unique identifier for the entry
        team: Team that performed the work
        member_name: Name/identifier of the team member
        feature: Name of the feature worked on
        tracked_time_hours: Actual time spent in hours
        process: Process type used
        date: Date when the work was performed
    """
    id: str
    team: TeamType
    member_name: str
    feature: str
    tracked_time_hours: float
    process: str
    date: date
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if not self.id:
            raise ValueError("TrackedTimeEntry id cannot be empty")
        if not self.member_name:
            raise ValueError("member_name cannot be empty")
        if not self.feature:
            raise ValueError("feature cannot be empty")
        if self.tracked_time_hours <= 0:
            raise ValueError("tracked_time_hours must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON persistence."""
        data = asdict(self)
        data['team'] = self.team.value  # Convert enum to string
        data['date'] = self.date.isoformat()  # Convert date to ISO string
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrackedTimeEntry':
        """Deserialize from dictionary."""
        data = data.copy()
        data['team'] = TeamType(data['team'])  # Convert string to enum
        # Handle date as string or date object
        if isinstance(data['date'], str):
            data['date'] = date.fromisoformat(data['date'])
        return cls(**data)


@dataclass
class FeatureStatistics:
    """Statistical measures for feature time estimates.
    
    Attributes:
        mean: Average time across all entries
        median: Middle value of time entries
        std_dev: Standard deviation of time entries
        p80: 80th percentile value
        data_point_count: Number of tracked time entries used
    """
    mean: float
    median: float
    std_dev: float
    p80: float
    data_point_count: int
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if self.std_dev < 0:
            raise ValueError("std_dev cannot be negative")
        if self.data_point_count < 0:
            raise ValueError("data_point_count cannot be negative")
        if self.p80 < 0:
            raise ValueError("p80 cannot be negative")


@dataclass
class FeatureEstimate:
    """Estimate for a single feature within a project.
    
    Attributes:
        feature_name: Name of the feature being estimated
        estimated_hours: Calculated time estimate in hours
        confidence: Confidence level based on data availability
        statistics: Statistical breakdown (if available)
        used_seed_time: Whether seed time was used (vs historical data)
    """
    feature_name: str
    estimated_hours: float
    confidence: ConfidenceLevel
    statistics: Optional[FeatureStatistics] = None
    used_seed_time: bool = False
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if not self.feature_name:
            raise ValueError("feature_name cannot be empty")
        if self.estimated_hours <= 0:
            raise ValueError("estimated_hours must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON persistence."""
        data = asdict(self)
        data['confidence'] = self.confidence.value  # Convert enum to string
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FeatureEstimate':
        """Deserialize from dictionary."""
        data = data.copy()
        data['confidence'] = ConfidenceLevel(data['confidence'])  # Convert string to enum
        # Handle nested FeatureStatistics if present
        if data.get('statistics') is not None:
            data['statistics'] = FeatureStatistics(**data['statistics'])
        return cls(**data)


@dataclass
class ProjectEstimate:
    """Complete project estimation with feature breakdown.
    
    Attributes:
        features: List of individual feature estimates
        total_hours: Sum of all feature estimates
        confidence: Overall confidence level for the project
    """
    features: List[FeatureEstimate]
    total_hours: float
    confidence: ConfidenceLevel
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if self.total_hours < 0:
            raise ValueError("total_hours cannot be negative")
        if not self.features:
            raise ValueError("features list cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON persistence."""
        return {
            'features': [f.to_dict() for f in self.features],
            'total_hours': self.total_hours,
            'confidence': self.confidence.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectEstimate':
        """Deserialize from dictionary."""
        data = data.copy()
        data['confidence'] = ConfidenceLevel(data['confidence'])
        data['features'] = [FeatureEstimate.from_dict(f) for f in data['features']]
        return cls(**data)


@dataclass
class EstimationConfig:
    """Configuration for estimation calculations.
    
    Attributes:
        use_outlier_detection: Whether to detect and flag outliers
        outlier_threshold_std: Standard deviations for outlier detection
        min_data_points_for_stats: Minimum entries needed for statistics
    """
    use_outlier_detection: bool = True
    outlier_threshold_std: float = 2.0
    min_data_points_for_stats: int = 3
    
    def __post_init__(self) -> None:
        """Validate field values after initialization."""
        if self.outlier_threshold_std <= 0:
            raise ValueError("outlier_threshold_std must be positive")
        if self.min_data_points_for_stats < 1:
            raise ValueError("min_data_points_for_stats must be at least 1")


