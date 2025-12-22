# Chapter 11: JSON Persistence

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 9-10  
**AITEA Component:** `src/services/persistence.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Persist features and time entries to JSON files
2. Load data automatically on CLI startup
3. Handle file I/O errors gracefully
4. Implement atomic file writes
5. Design a persistence layer that's independent of storage format

## 11.1 Persistence Architecture

We'll create persistence services that wrap our in-memory services:

```
┌─────────────────────────────────────────┐
│              CLI Commands               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Persistence Services            │
│  (Load on start, save on change)        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          In-Memory Services             │
│  (FeatureLibrary, TimeTracking)         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│            JSON Files                   │
│  (features.json, tracked_time.json)     │
└─────────────────────────────────────────┘
```

## 11.2 Data File Structure

**`data/features.json`:**

```json
{
  "version": "1.0",
  "features": [
    {
      "id": "f1",
      "name": "CRUD API",
      "team": "backend",
      "process": "Data Operations",
      "seed_time_hours": 4.0,
      "synonyms": ["crud", "rest-api"],
      "notes": ""
    }
  ]
}
```

**`data/tracked_time.json`:**

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "t1",
      "team": "backend",
      "member_name": "BE-1",
      "feature": "CRUD API",
      "tracked_time_hours": 4.5,
      "process": "Data Operations",
      "date": "2025-01-15"
    }
  ]
}
```

## 11.3 Feature Library Persistence

```python
from pathlib import Path
from typing import Optional
import json

from models import Feature
from services import FeatureLibraryService
from utils import save_json, load_json


class FeatureLibraryPersistence:
    """Persistence layer for the feature library."""

    DEFAULT_PATH = Path("data/features.json")
    VERSION = "1.0"

    def __init__(
        self,
        service: FeatureLibraryService,
        path: Optional[Path] = None
    ):
        self._service = service
        self._path = path or self.DEFAULT_PATH

    def load(self) -> int:
        """Load features from JSON file.

        Returns:
            Number of features loaded.
        """
        if not self._path.exists():
            return 0

        try:
            data = load_json(self._path)
            features = data.get("features", [])

            count = 0
            for feature_data in features:
                feature = Feature.from_dict(feature_data)
                result = self._service.add_feature(feature)
                if result.is_ok():
                    count += 1

            return count
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid features file: {e}")

    def save(self) -> None:
        """Save all features to JSON file."""
        features = self._service.list_features()

        data = {
            "version": self.VERSION,
            "features": [f.to_dict() for f in features]
        }

        save_json(data, self._path)

    def add_and_save(self, feature: Feature):
        """Add a feature and persist immediately."""
        result = self._service.add_feature(feature)
        if result.is_ok():
            self.save()
        return result
```

### Your Turn: Exercise 11.1

Implement `TimeTrackingPersistence`:

```python
class TimeTrackingPersistence:
    """Persistence layer for tracked time entries."""

    DEFAULT_PATH = Path("data/tracked_time.json")
    VERSION = "1.0"

    def __init__(self, service: TimeTrackingService, path: Optional[Path] = None):
        self._service = service
        self._path = path or self.DEFAULT_PATH

    def load(self) -> int:
        """Load entries from JSON file."""
        # TODO: Similar to FeatureLibraryPersistence.load()
        pass

    def save(self) -> None:
        """Save all entries to JSON file."""
        # TODO: Similar to FeatureLibraryPersistence.save()
        pass
```

## 11.4 Atomic File Writes

Prevent data corruption by writing to a temp file first:

```python
import tempfile
import shutil

def save_json_atomic(data: dict, path: Path) -> None:
    """Save JSON atomically to prevent corruption."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file first
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        dir=path.parent,
        delete=False
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = Path(tmp.name)

    # Atomic rename (works on same filesystem)
    shutil.move(str(tmp_path), str(path))
```

## 11.5 CLI Integration

Update the CLI to use persistence:

```python
# src/cli/__init__.py
from pathlib import Path
from services import FeatureLibraryService, TimeTrackingService, EstimationService
from services.persistence import FeatureLibraryPersistence, TimeTrackingPersistence

# Create services
feature_service = FeatureLibraryService()
time_service = TimeTrackingService()
estimation_service = EstimationService(feature_service, time_service)

# Create persistence layers
feature_persistence = FeatureLibraryPersistence(feature_service)
time_persistence = TimeTrackingPersistence(time_service)


def init_data():
    """Load data from files on startup."""
    try:
        feature_count = feature_persistence.load()
        time_count = time_persistence.load()
        return feature_count, time_count
    except ValueError as e:
        print(f"Warning: Could not load data: {e}")
        return 0, 0


# Load data when module is imported
_feature_count, _time_count = init_data()
```

Update commands to save after changes:

```python
@feature_app.command("add")
def feature_add(...):
    """Add a new feature."""
    feature = Feature(...)
    result = feature_persistence.add_and_save(feature)  # Save immediately

    if result.is_ok():
        print_success(f"Added feature: {feature.name}")
    else:
        print_error(str(result.unwrap_err()))
```

## 11.6 Backup and Recovery

Add backup functionality:

```python
from datetime import datetime

class FeatureLibraryPersistence:
    # ... existing code ...

    def backup(self) -> Path:
        """Create a timestamped backup."""
        if not self._path.exists():
            raise FileNotFoundError("No data file to backup")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self._path.with_suffix(f".{timestamp}.backup.json")

        shutil.copy(self._path, backup_path)
        return backup_path

    def restore(self, backup_path: Path) -> int:
        """Restore from a backup file."""
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Clear current data
        self._service._features.clear()

        # Load from backup
        old_path = self._path
        self._path = backup_path
        count = self.load()
        self._path = old_path

        # Save to main file
        self.save()

        return count
```

## 11.7 Error Handling

Handle common file errors:

```python
def load(self) -> int:
    """Load features with comprehensive error handling."""
    if not self._path.exists():
        return 0  # No file yet, that's OK

    try:
        data = load_json(self._path)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {self._path}: {e}")
    except PermissionError:
        raise ValueError(f"Permission denied reading {self._path}")
    except OSError as e:
        raise ValueError(f"Cannot read {self._path}: {e}")

    # Validate structure
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {self._path}, got {type(data)}")

    if "features" not in data:
        raise ValueError(f"Missing 'features' key in {self._path}")

    # Load features
    count = 0
    errors = []

    for i, feature_data in enumerate(data["features"]):
        try:
            feature = Feature.from_dict(feature_data)
            result = self._service.add_feature(feature)
            if result.is_ok():
                count += 1
            else:
                errors.append(f"Feature {i}: {result.unwrap_err()}")
        except (KeyError, ValueError) as e:
            errors.append(f"Feature {i}: {e}")

    if errors:
        print(f"Warning: {len(errors)} features failed to load")
        for err in errors[:5]:  # Show first 5
            print(f"  - {err}")

    return count
```

## 11.8 Debugging Scenario

**The Bug:** Data disappears after a crash during save.

```python
def save(self):
    with open(self._path, 'w') as f:
        # Crash here = empty file!
        json.dump(data, f)
```

**The Fix:** Use atomic writes:

```python
def save(self):
    # Write to temp file first
    tmp_path = self._path.with_suffix('.tmp')
    with open(tmp_path, 'w') as f:
        json.dump(data, f, indent=2)

    # Atomic rename - either succeeds completely or fails
    tmp_path.rename(self._path)
```

## 11.9 Quick Check Questions

1. Why use atomic file writes?
2. What happens if the JSON file doesn't exist on load?
3. How do you handle invalid JSON in a data file?
4. Why include a version field in the JSON structure?
5. When should you call `save()`?

<details>
<summary>Answers</summary>

1. To prevent data corruption if the program crashes during write
2. Return 0 (no features loaded) - it's not an error
3. Catch `json.JSONDecodeError` and raise a descriptive error
4. For future migrations when the data format changes
5. After any operation that modifies data (add, update, delete)

</details>

## 11.10 Mini-Project: Data Migration

Create a migration system for schema changes:

```python
class DataMigrator:
    """Handle data format migrations."""

    CURRENT_VERSION = "1.1"

    MIGRATIONS = {
        "1.0": "migrate_1_0_to_1_1",
    }

    def migrate(self, data: dict) -> dict:
        """Migrate data to current version."""
        version = data.get("version", "1.0")

        while version != self.CURRENT_VERSION:
            if version not in self.MIGRATIONS:
                raise ValueError(f"Unknown version: {version}")

            migration_method = getattr(self, self.MIGRATIONS[version])
            data = migration_method(data)
            version = data["version"]

        return data

    def migrate_1_0_to_1_1(self, data: dict) -> dict:
        """Add 'created_at' field to features."""
        for feature in data.get("features", []):
            if "created_at" not in feature:
                feature["created_at"] = "2025-01-01"

        data["version"] = "1.1"
        return data
```

## 11.11 AITEA Integration

This chapter implements:

- **Requirement 2.3**: JSON persistence services for Feature Library and Tracked Time

**Verification:**

```bash
# Add a feature
aitea feature add f1 "CRUD" -t backend -p "Data Ops" -h 4.0

# Check the file was created
cat data/features.json

# Restart and verify data persists
aitea feature list
```

## What's Next

In Chapter 12, we'll implement CSV import for bulk time entry loading. You'll learn:

- Parsing CSV with pandas
- Validating and transforming data
- Collecting and reporting errors

**Before proceeding:**

- Ensure data persists across CLI restarts
- Test error handling with invalid JSON
- Try the backup/restore functionality
