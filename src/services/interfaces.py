"""Abstract base classes defining service interfaces for AITEA.

This module provides the service interface contracts using Python's ABC
(Abstract Base Class) pattern. All service implementations must inherit
from these interfaces and implement the abstract methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from ..models import (
    Feature,
    TrackedTimeEntry,
    FeatureEstimate,
    FeatureStatistics,
    ProjectEstimate,
    ValidationError,
    NotFoundError,
    ImportError,
    EstimationError,
    TeamType,
)
from ..models.result import Result


@dataclass
class ImportResult:
    """Result of a CSV import operation.
    
    Attributes:
        successful_count: Number of entries successfully imported
        failed_count: Number of entries that failed to import
        total_count: Total number of entries processed
        errors: List of import errors for failed rows
    """
    successful_count: int
    failed_count: int
    total_count: int
    errors: List[ImportError]


class IFeatureLibraryService(ABC):
    """Interface for managing the feature library.
    
    The feature library stores software features with their metadata,
    including seed time estimates, team assignments, and synonyms for
    feature name matching.
    """
    
    @abstractmethod
    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        """Add a new feature to the library.

        Args:
            feature: The feature to add
            
        Returns:
            Result containing the added feature on success,
            or ValidationError if the feature is invalid or already exists
        """
        ...
    
    @abstractmethod
    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        """Retrieve a feature by its ID.
        
        Args:
            feature_id: The unique identifier of the feature
            
        Returns:
            Result containing the feature on success,
            or NotFoundError if no feature with that ID exists
        """
        ...
    
    @abstractmethod
    def search_features(self, query: str) -> List[Feature]:
        """Search for features matching a query string.
        
        Searches feature names and synonyms for matches.
        
        Args:
            query: The search query string
            
        Returns:
            List of features matching the query (may be empty)
        """
        ...
    
    @abstractmethod
    def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
        """List all features, optionally filtered by team.
        
        Args:
            team: Optional team filter. If None, returns all features.
            
        Returns:
            List of features (may be empty)
        """
        ...


class ITimeTrackingService(ABC):
    """Interface for managing tracked time entries.
    
    The time tracking service stores actual time spent by team members
    on features, which is used to compute statistics and improve
    estimation accuracy.
    """
    
    @abstractmethod
    def add_entry(self, entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, ValidationError]:
        """Add a new tracked time entry.
        
        Args:
            entry: The time entry to add
            
        Returns:
            Result containing the added entry on success,
            or ValidationError if the entry is invalid
        """
        ...
    
    @abstractmethod
    def import_csv(self, path: Path) -> Result[ImportResult, ImportError]:
        """Import tracked time entries from a CSV file.
        
        Args:
            path: Path to the CSV file to import
            
        Returns:
            Result containing import statistics on success,
            or ImportError if the import fails
        """
        ...
    
    @abstractmethod
    def get_entries_for_feature(self, feature_name: str) -> List[TrackedTimeEntry]:
        """Get all tracked time entries for a specific feature.
        
        Args:
            feature_name: Name of the feature to get entries for
            
        Returns:
            List of tracked time entries for the feature (may be empty)
        """
        ...


class IEstimationService(ABC):
    """Interface for computing time estimates.
    
    The estimation service uses historical tracked time data to compute
    statistical estimates for features and projects. When insufficient
    data is available, it falls back to seed time estimates.
    """
    
    @abstractmethod
    def estimate_feature(self, feature_name: str) -> Result[FeatureEstimate, EstimationError]:
        """Estimate time for a single feature.
        
        Uses historical tracked time data if available, otherwise
        falls back to the feature's seed time estimate.
        
        Args:
            feature_name: Name of the feature to estimate
            
        Returns:
            Result containing the feature estimate on success,
            or EstimationError if estimation fails
        """
        ...
    
    @abstractmethod
    def estimate_project(self, features: List[str]) -> Result[ProjectEstimate, EstimationError]:
        """Estimate time for a project consisting of multiple features.
        
        Aggregates individual feature estimates into a project-level
        estimate with total hours and overall confidence level.
        
        Args:
            features: List of feature names to include in the estimate
            
        Returns:
            Result containing the project estimate on success,
            or EstimationError if estimation fails
        """
        ...
    
    @abstractmethod
    def compute_statistics(self, entries: List[TrackedTimeEntry]) -> FeatureStatistics:
        """Compute statistical measures from tracked time entries.
        
        Calculates mean, median, standard deviation, and P80 (80th
        percentile) from the provided time entries.
        
        Args:
            entries: List of tracked time entries to analyze
            
        Returns:
            FeatureStatistics containing computed measures
        """
        ...
