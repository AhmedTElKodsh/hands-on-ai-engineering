"""Service implementations for AITEA.

This module provides concrete implementations of the service interfaces
using in-memory storage for features and tracked time entries.
"""

from typing import Dict, List, Optional
from pathlib import Path

from .interfaces import (
    IFeatureLibraryService,
    ITimeTrackingService,
    IEstimationService,
    ImportResult,
)
from ..models import (
    Feature,
    TrackedTimeEntry,
    FeatureEstimate,
    FeatureStatistics,
    ProjectEstimate,
    EstimationConfig,
    ValidationError,
    NotFoundError,
    ImportError,
    EstimationError,
    TeamType,
    ConfidenceLevel,
)
from ..models.result import Result
from ..utils import (
    calculate_mean,
    calculate_median,
    calculate_std_dev,
    calculate_p80,
    normalize_text,
)


class FeatureLibraryService(IFeatureLibraryService):
    """In-memory implementation of the feature library service.
    
    Stores features in a dictionary keyed by feature ID.
    Supports searching by name and synonyms using normalized text matching.
    """
    
    def __init__(self) -> None:
        """Initialize with empty feature storage."""
        self._features: Dict[str, Feature] = {}
    
    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        """Add a new feature to the library.
        
        Args:
            feature: The feature to add
            
        Returns:
            Result containing the added feature on success,
            or ValidationError if the feature ID already exists
        """
        if feature.id in self._features:
            return Result.err(ValidationError(
                field="id",
                message="Feature with this ID already exists",
                value=feature.id
            ))
        
        self._features[feature.id] = feature
        return Result.ok(feature)
    
    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        """Retrieve a feature by its ID.
        
        Args:
            feature_id: The unique identifier of the feature
            
        Returns:
            Result containing the feature on success,
            or NotFoundError if no feature with that ID exists
        """
        if feature_id not in self._features:
            return Result.err(NotFoundError(
                resource_type="Feature",
                identifier=feature_id
            ))
        
        return Result.ok(self._features[feature_id])
    
    def search_features(self, query: str) -> List[Feature]:
        """Search for features matching a query string.
        
        Searches feature names and synonyms for matches using
        normalized text comparison.
        
        Args:
            query: The search query string
            
        Returns:
            List of features matching the query (may be empty)
        """
        normalized_query = normalize_text(query)
        if not normalized_query:
            return []
        
        results: List[Feature] = []
        for feature in self._features.values():
            # Check feature name
            if normalized_query in normalize_text(feature.name):
                results.append(feature)
                continue
            
            # Check synonyms
            for synonym in feature.synonyms:
                if normalized_query in normalize_text(synonym):
                    results.append(feature)
                    break
        
        return results
    
    def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
        """List all features, optionally filtered by team.
        
        Args:
            team: Optional team filter. If None, returns all features.
            
        Returns:
            List of features (may be empty)
        """
        if team is None:
            return list(self._features.values())
        
        return [f for f in self._features.values() if f.team == team]
    
    def get_feature_by_name(self, name: str) -> Optional[Feature]:
        """Get a feature by its name (case-insensitive).
        
        This is a helper method for the estimation service.
        
        Args:
            name: The feature name to search for
            
        Returns:
            The feature if found, None otherwise
        """
        normalized_name = normalize_text(name)
        for feature in self._features.values():
            if normalize_text(feature.name) == normalized_name:
                return feature
            # Also check synonyms for exact match
            for synonym in feature.synonyms:
                if normalize_text(synonym) == normalized_name:
                    return feature
        return None



class TimeTrackingService(ITimeTrackingService):
    """In-memory implementation of the time tracking service.
    
    Stores tracked time entries in a dictionary keyed by entry ID.
    Supports retrieval by feature name using normalized text matching.
    """
    
    def __init__(self) -> None:
        """Initialize with empty entry storage."""
        self._entries: Dict[str, TrackedTimeEntry] = {}
    
    def add_entry(self, entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, ValidationError]:
        """Add a new tracked time entry.
        
        Args:
            entry: The time entry to add
            
        Returns:
            Result containing the added entry on success,
            or ValidationError if the entry ID already exists
        """
        if entry.id in self._entries:
            return Result.err(ValidationError(
                field="id",
                message="Entry with this ID already exists",
                value=entry.id
            ))
        
        self._entries[entry.id] = entry
        return Result.ok(entry)
    
    def import_csv(self, path: Path) -> Result[ImportResult, ImportError]:
        """Import tracked time entries from a CSV file.
        
        Uses pandas to read and validate CSV data. Valid entries are
        added to the service, while invalid rows are collected with
        specific error messages.
        
        Args:
            path: Path to the CSV file to import
            
        Returns:
            Result containing import statistics on success,
            or ImportError if the file cannot be read
        """
        from .csv_import import import_csv_file
        
        try:
            entries, import_result = import_csv_file(path)
        except FileNotFoundError:
            return Result.err(ImportError(
                row_number=0,
                errors=[ValidationError(
                    field="path",
                    message="File does not exist",
                    value=str(path)
                )],
                source=str(path)
            ))
        except ValueError as e:
            return Result.err(ImportError(
                row_number=0,
                errors=[ValidationError(
                    field="file",
                    message=str(e),
                    value=str(path)
                )],
                source=str(path)
            ))
        
        # Add valid entries to the service
        for entry in entries:
            self._entries[entry.id] = entry
        
        return Result.ok(import_result)
    
    def get_entries_for_feature(self, feature_name: str) -> List[TrackedTimeEntry]:
        """Get all tracked time entries for a specific feature.
        
        Uses normalized text matching to find entries.
        
        Args:
            feature_name: Name of the feature to get entries for
            
        Returns:
            List of tracked time entries for the feature (may be empty)
        """
        normalized_name = normalize_text(feature_name)
        return [
            entry for entry in self._entries.values()
            if normalize_text(entry.feature) == normalized_name
        ]



class EstimationService(IEstimationService):
    """Implementation of the estimation service with statistics computation.
    
    Uses historical tracked time data to compute statistical estimates.
    Falls back to seed time when insufficient data is available.
    """
    
    def __init__(
        self,
        feature_library: FeatureLibraryService,
        time_tracking: TimeTrackingService,
        config: Optional[EstimationConfig] = None
    ) -> None:
        """Initialize with required services and optional configuration.
        
        Args:
            feature_library: Service for accessing feature data
            time_tracking: Service for accessing tracked time entries
            config: Optional estimation configuration (uses defaults if None)
        """
        self._feature_library = feature_library
        self._time_tracking = time_tracking
        self._config = config or EstimationConfig()
    
    def estimate_feature(self, feature_name: str) -> Result[FeatureEstimate, EstimationError]:
        """Estimate time for a single feature.
        
        Uses historical tracked time data if available (>= min_data_points_for_stats),
        otherwise falls back to the feature's seed time estimate.
        
        Args:
            feature_name: Name of the feature to estimate
            
        Returns:
            Result containing the feature estimate on success,
            or EstimationError if the feature is not found
        """
        # Find the feature in the library
        feature = self._feature_library.get_feature_by_name(feature_name)
        if feature is None:
            return Result.err(EstimationError(
                feature_name=feature_name,
                reason="Feature not found in library"
            ))
        
        # Get tracked time entries for this feature
        entries = self._time_tracking.get_entries_for_feature(feature_name)
        
        # Determine confidence level based on data point count
        data_point_count = len(entries)
        confidence = self._get_confidence_level(data_point_count)
        
        # If we have enough data points, use statistics
        if data_point_count >= self._config.min_data_points_for_stats:
            statistics = self.compute_statistics(entries)
            # Use P80 as the estimate for conservative planning
            estimated_hours = statistics.p80
            
            return Result.ok(FeatureEstimate(
                feature_name=feature_name,
                estimated_hours=estimated_hours,
                confidence=confidence,
                statistics=statistics,
                used_seed_time=False
            ))
        
        # Fall back to seed time
        return Result.ok(FeatureEstimate(
            feature_name=feature_name,
            estimated_hours=feature.seed_time_hours,
            confidence=confidence,
            statistics=None,
            used_seed_time=True
        ))
    
    def estimate_project(self, features: List[str]) -> Result[ProjectEstimate, EstimationError]:
        """Estimate time for a project consisting of multiple features.
        
        Aggregates individual feature estimates into a project-level
        estimate with total hours and overall confidence level.
        
        Args:
            features: List of feature names to include in the estimate
            
        Returns:
            Result containing the project estimate on success,
            or EstimationError if any feature estimation fails
        """
        if not features:
            return Result.err(EstimationError(
                feature_name="<project>",
                reason="No features provided for estimation"
            ))
        
        feature_estimates: List[FeatureEstimate] = []
        
        for feature_name in features:
            result = self.estimate_feature(feature_name)
            if result.is_err():
                return Result.err(result.unwrap_err())
            feature_estimates.append(result.unwrap())
        
        # Calculate total hours
        total_hours = sum(fe.estimated_hours for fe in feature_estimates)
        
        # Determine overall confidence (use the lowest confidence level)
        overall_confidence = self._get_overall_confidence(feature_estimates)
        
        return Result.ok(ProjectEstimate(
            features=feature_estimates,
            total_hours=total_hours,
            confidence=overall_confidence
        ))
    
    def compute_statistics(self, entries: List[TrackedTimeEntry]) -> FeatureStatistics:
        """Compute statistical measures from tracked time entries.
        
        Calculates mean, median, standard deviation, and P80 (80th
        percentile) from the provided time entries.
        
        Args:
            entries: List of tracked time entries to analyze
            
        Returns:
            FeatureStatistics containing computed measures
            
        Raises:
            ValueError: If entries list is empty
        """
        if not entries:
            raise ValueError("Cannot compute statistics from empty entries list")
        
        # Extract time values
        times = [entry.tracked_time_hours for entry in entries]
        
        return FeatureStatistics(
            mean=calculate_mean(times),
            median=calculate_median(times),
            std_dev=calculate_std_dev(times),
            p80=calculate_p80(times),
            data_point_count=len(times)
        )
    
    def _get_confidence_level(self, data_point_count: int) -> ConfidenceLevel:
        """Determine confidence level based on data point count.
        
        - 1-2 data points: LOW
        - 3-9 data points: MEDIUM
        - 10+ data points: HIGH
        
        Args:
            data_point_count: Number of tracked time entries
            
        Returns:
            The appropriate confidence level
        """
        if data_point_count >= 10:
            return ConfidenceLevel.HIGH
        elif data_point_count >= 3:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _get_overall_confidence(self, estimates: List[FeatureEstimate]) -> ConfidenceLevel:
        """Determine overall project confidence from feature estimates.
        
        Uses the lowest confidence level among all features.
        
        Args:
            estimates: List of feature estimates
            
        Returns:
            The lowest confidence level found
        """
        confidence_order = [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
        
        min_confidence = ConfidenceLevel.HIGH
        for estimate in estimates:
            if confidence_order.index(estimate.confidence) < confidence_order.index(min_confidence):
                min_confidence = estimate.confidence
        
        return min_confidence
