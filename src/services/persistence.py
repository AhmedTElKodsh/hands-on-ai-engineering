"""JSON persistence services for AITEA.

This module provides persistence services that serialize and deserialize
Feature Library and Tracked Time data to/from JSON files.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any

from ..models import (
    Feature,
    TrackedTimeEntry,
    ValidationError,
)
from ..models.result import Result
from ..utils import save_json, load_json


class FeatureLibraryPersistence:
    """Persistence service for Feature Library JSON file operations.
    
    Handles serialization and deserialization of Feature objects to/from
    JSON files. Supports loading, saving, and managing a collection of
    features with atomic file operations.
    
    Attributes:
        file_path: Path to the JSON file for persistence.
    """
    
    def __init__(self, file_path: Path) -> None:
        """Initialize the persistence service with a file path.
        
        Args:
            file_path: Path to the JSON file for storing features.
        """
        self.file_path = Path(file_path)
    
    def save(self, features: List[Feature]) -> Result[int, ValidationError]:
        """Save a list of features to the JSON file.
        
        Serializes all features to JSON format and writes them to the
        configured file path. Creates parent directories if needed.
        
        Args:
            features: List of Feature objects to save.
            
        Returns:
            Result containing the number of features saved on success,
            or ValidationError if serialization or file write fails.
        """
        try:
            data = {
                "features": [feature.to_dict() for feature in features]
            }
            save_json(data, self.file_path)
            return Result.ok(len(features))
        except (TypeError, OSError) as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to save features: {str(e)}",
                value=str(self.file_path)
            ))
    
    def load(self) -> Result[List[Feature], ValidationError]:
        """Load features from the JSON file.
        
        Reads and deserializes features from the configured file path.
        Returns an empty list if the file doesn't exist.
        
        Returns:
            Result containing a list of Feature objects on success,
            or ValidationError if the file is invalid or cannot be read.
        """
        if not self.file_path.exists():
            return Result.ok([])
        
        try:
            data = load_json(self.file_path)
            
            if not isinstance(data, dict):
                return Result.err(ValidationError(
                    field="file",
                    message="Invalid JSON structure: expected object with 'features' key",
                    value=str(self.file_path)
                ))
            
            features_data = data.get("features", [])
            if not isinstance(features_data, list):
                return Result.err(ValidationError(
                    field="features",
                    message="Invalid JSON structure: 'features' must be an array",
                    value=str(type(features_data).__name__)
                ))
            
            features = []
            for idx, feature_data in enumerate(features_data):
                try:
                    feature = Feature.from_dict(feature_data)
                    features.append(feature)
                except (KeyError, ValueError, TypeError) as e:
                    return Result.err(ValidationError(
                        field=f"features[{idx}]",
                        message=f"Invalid feature data: {str(e)}",
                        value=str(feature_data)
                    ))
            
            return Result.ok(features)
        except FileNotFoundError:
            return Result.ok([])
        except Exception as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to load features: {str(e)}",
                value=str(self.file_path)
            ))
    
    def exists(self) -> bool:
        """Check if the persistence file exists.
        
        Returns:
            True if the file exists, False otherwise.
        """
        return self.file_path.exists()
    
    def delete(self) -> Result[bool, ValidationError]:
        """Delete the persistence file.
        
        Returns:
            Result containing True on success,
            or ValidationError if deletion fails.
        """
        try:
            if self.file_path.exists():
                self.file_path.unlink()
            return Result.ok(True)
        except OSError as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to delete file: {str(e)}",
                value=str(self.file_path)
            ))



class TimeTrackingPersistence:
    """Persistence service for Tracked Time Entry JSON file operations.
    
    Handles serialization and deserialization of TrackedTimeEntry objects
    to/from JSON files. Supports loading, saving, and managing a collection
    of time entries with atomic file operations.
    
    Attributes:
        file_path: Path to the JSON file for persistence.
    """
    
    def __init__(self, file_path: Path) -> None:
        """Initialize the persistence service with a file path.
        
        Args:
            file_path: Path to the JSON file for storing time entries.
        """
        self.file_path = Path(file_path)
    
    def save(self, entries: List[TrackedTimeEntry]) -> Result[int, ValidationError]:
        """Save a list of tracked time entries to the JSON file.
        
        Serializes all entries to JSON format and writes them to the
        configured file path. Creates parent directories if needed.
        
        Args:
            entries: List of TrackedTimeEntry objects to save.
            
        Returns:
            Result containing the number of entries saved on success,
            or ValidationError if serialization or file write fails.
        """
        try:
            data = {
                "tracked_time": [entry.to_dict() for entry in entries]
            }
            save_json(data, self.file_path)
            return Result.ok(len(entries))
        except (TypeError, OSError) as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to save time entries: {str(e)}",
                value=str(self.file_path)
            ))
    
    def load(self) -> Result[List[TrackedTimeEntry], ValidationError]:
        """Load tracked time entries from the JSON file.
        
        Reads and deserializes entries from the configured file path.
        Returns an empty list if the file doesn't exist.
        
        Returns:
            Result containing a list of TrackedTimeEntry objects on success,
            or ValidationError if the file is invalid or cannot be read.
        """
        if not self.file_path.exists():
            return Result.ok([])
        
        try:
            data = load_json(self.file_path)
            
            if not isinstance(data, dict):
                return Result.err(ValidationError(
                    field="file",
                    message="Invalid JSON structure: expected object with 'tracked_time' key",
                    value=str(self.file_path)
                ))
            
            entries_data = data.get("tracked_time", [])
            if not isinstance(entries_data, list):
                return Result.err(ValidationError(
                    field="tracked_time",
                    message="Invalid JSON structure: 'tracked_time' must be an array",
                    value=str(type(entries_data).__name__)
                ))
            
            entries = []
            for idx, entry_data in enumerate(entries_data):
                try:
                    entry = TrackedTimeEntry.from_dict(entry_data)
                    entries.append(entry)
                except (KeyError, ValueError, TypeError) as e:
                    return Result.err(ValidationError(
                        field=f"tracked_time[{idx}]",
                        message=f"Invalid time entry data: {str(e)}",
                        value=str(entry_data)
                    ))
            
            return Result.ok(entries)
        except FileNotFoundError:
            return Result.ok([])
        except Exception as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to load time entries: {str(e)}",
                value=str(self.file_path)
            ))
    
    def exists(self) -> bool:
        """Check if the persistence file exists.
        
        Returns:
            True if the file exists, False otherwise.
        """
        return self.file_path.exists()
    
    def delete(self) -> Result[bool, ValidationError]:
        """Delete the persistence file.
        
        Returns:
            Result containing True on success,
            or ValidationError if deletion fails.
        """
        try:
            if self.file_path.exists():
                self.file_path.unlink()
            return Result.ok(True)
        except OSError as e:
            return Result.err(ValidationError(
                field="file",
                message=f"Failed to delete file: {str(e)}",
                value=str(self.file_path)
            ))
