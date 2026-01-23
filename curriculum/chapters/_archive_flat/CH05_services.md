# Chapter 5: Service Implementation

**Difficulty:** Intermediate  
**Time:** 3 hours  
**Prerequisites:** Chapters 1-4  
**AITEA Component:** `src/services/implementations.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Implement service interfaces with in-memory storage
2. Use the Result type pattern for error handling
3. Implement feature search with text normalization
4. Build an estimation service with statistics computation
5. Apply confidence levels based on data availability

## 5.1 FeatureLibraryService Implementation

Let's implement the feature library with in-memory storage:

```python
from typing import Dict, List, Optional

class FeatureLibraryService(IFeatureLibraryService):
    """In-memory implementation of the feature library service."""

    def __init__(self) -> None:
        """Initialize with empty feature storage."""
        self._features: Dict[str, Feature] = {}
```

### Adding Features

```python
def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
    """Add a new feature to the library."""
    if feature.id in self._features:
        return Result.err(ValidationError(
            field="id",
            message="Feature with this ID already exists",
            value=feature.id
        ))

    self._features[feature.id] = feature
    return Result.ok(feature)
```

**Key points:**

- Check for duplicates before adding
- Return `Result.err()` for validation failures
- Return `Result.ok()` with the added feature on success

### Getting Features

```python
def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
    """Retrieve a feature by its ID."""
    if feature_id not in self._features:
        return Result.err(NotFoundError(
            resource_type="Feature",
            identifier=feature_id
        ))

    return Result.ok(self._features[feature_id])
```

### Your Turn: Exercise 5.1

Implement the `list_features` method:

```python
def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
    """List all features, optionally filtered by team."""
    # TODO: If team is None, return all features
    # TODO: If team is specified, filter by team
    pass
```

**Expected behavior:**

```python
service = FeatureLibraryService()
service.add_feature(Feature("f1", "CRUD", TeamType.BACKEND, "Data", 4.0))
service.add_feature(Feature("f2", "UI", TeamType.FRONTEND, "Content", 6.0))

all_features = service.list_features()  # Returns both
backend_only = service.list_features(TeamType.BACKEND)  # Returns only f1
```

## 5.2 Search with Text Normalization

For flexible searching, we normalize text before comparison:

```python
from ..utils import normalize_text

def search_features(self, query: str) -> List[Feature]:
    """Search for features matching a query string."""
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
```

**How normalization helps:**

```python
# These all match "CRUD":
normalize_text("CRUD")      # "crud"
normalize_text("crud-api")  # "crud api"
normalize_text("CRUD_API")  # "crud api"
```

### Helper Method for Name Lookup

Add a helper for the estimation service:

```python
def get_feature_by_name(self, name: str) -> Optional[Feature]:
    """Get a feature by its name (case-insensitive)."""
    normalized_name = normalize_text(name)
    for feature in self._features.values():
        if normalize_text(feature.name) == normalized_name:
            return feature
        for synonym in feature.synonyms:
            if normalize_text(synonym) == normalized_name:
                return feature
    return None
```

## 5.3 TimeTrackingService Implementation

```python
class TimeTrackingService(ITimeTrackingService):
    """In-memory implementation of the time tracking service."""

    def __init__(self) -> None:
        self._entries: Dict[str, TrackedTimeEntry] = {}

    def add_entry(self, entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, ValidationError]:
        """Add a new tracked time entry."""
        if entry.id in self._entries:
            return Result.err(ValidationError(
                field="id",
                message="Entry with this ID already exists",
                value=entry.id
            ))

        self._entries[entry.id] = entry
        return Result.ok(entry)

    def get_entries_for_feature(self, feature_name: str) -> List[TrackedTimeEntry]:
        """Get all tracked time entries for a specific feature."""
        normalized_name = normalize_text(feature_name)
        return [
            entry for entry in self._entries.values()
            if normalize_text(entry.feature) == normalized_name
        ]
```

### Your Turn: Exercise 5.2

The `import_csv` method delegates to a helper. For now, create a stub:

```python
def import_csv(self, path: Path) -> Result[ImportResult, ImportError]:
    """Import tracked time entries from a CSV file."""
    # We'll implement this fully in Chapter 12
    # For now, return an error indicating not implemented
    return Result.err(ImportError(
        row_number=0,
        errors=[ValidationError("file", "CSV import not yet implemented", str(path))],
        source=str(path)
    ))
```

## 5.4 EstimationService Implementation

The estimation service is the heart of AITEA. It combines feature data with tracked time to produce estimates.

```python
class EstimationService(IEstimationService):
    """Implementation of the estimation service with statistics computation."""

    def __init__(
        self,
        feature_library: FeatureLibraryService,
        time_tracking: TimeTrackingService,
        config: Optional[EstimationConfig] = None
    ) -> None:
        self._feature_library = feature_library
        self._time_tracking = time_tracking
        self._config = config or EstimationConfig()
```

### Computing Statistics

```python
def compute_statistics(self, entries: List[TrackedTimeEntry]) -> FeatureStatistics:
    """Compute statistical measures from tracked time entries."""
    if not entries:
        raise ValueError("Cannot compute statistics from empty entries list")

    times = [entry.tracked_time_hours for entry in entries]

    return FeatureStatistics(
        mean=calculate_mean(times),
        median=calculate_median(times),
        std_dev=calculate_std_dev(times),
        p80=calculate_p80(times),
        data_point_count=len(times)
    )
```

### Confidence Levels

Confidence depends on how much data we have:

```python
def _get_confidence_level(self, data_point_count: int) -> ConfidenceLevel:
    """Determine confidence level based on data point count."""
    if data_point_count >= 10:
        return ConfidenceLevel.HIGH
    elif data_point_count >= 3:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW
```

| Data Points | Confidence | Reasoning                      |
| ----------- | ---------- | ------------------------------ |
| 0-2         | LOW        | Not enough data, use seed time |
| 3-9         | MEDIUM     | Some historical data available |
| 10+         | HIGH       | Reliable statistical basis     |

### Estimating a Single Feature

```python
def estimate_feature(self, feature_name: str) -> Result[FeatureEstimate, EstimationError]:
    """Estimate time for a single feature."""
    # Find the feature
    feature = self._feature_library.get_feature_by_name(feature_name)
    if feature is None:
        return Result.err(EstimationError(
            feature_name=feature_name,
            reason="Feature not found in library"
        ))

    # Get tracked time entries
    entries = self._time_tracking.get_entries_for_feature(feature_name)
    data_point_count = len(entries)
    confidence = self._get_confidence_level(data_point_count)

    # If enough data, use statistics
    if data_point_count >= self._config.min_data_points_for_stats:
        statistics = self.compute_statistics(entries)
        return Result.ok(FeatureEstimate(
            feature_name=feature_name,
            estimated_hours=statistics.p80,  # Use P80 for conservative estimate
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
```

**Key decisions:**

- Use P80 (80th percentile) for estimates - conservative but realistic
- Fall back to seed time when data is insufficient
- Always include confidence level

### Your Turn: Exercise 5.3

Implement `estimate_project`:

```python
def estimate_project(self, features: List[str]) -> Result[ProjectEstimate, EstimationError]:
    """Estimate time for a project with multiple features."""
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

    # TODO: Calculate total_hours (sum of all estimates)
    # TODO: Calculate overall_confidence (lowest confidence among features)

    return Result.ok(ProjectEstimate(
        features=feature_estimates,
        total_hours=total_hours,
        confidence=overall_confidence
    ))
```

**Hint for overall confidence:**

```python
def _get_overall_confidence(self, estimates: List[FeatureEstimate]) -> ConfidenceLevel:
    """Use the lowest confidence level among all features."""
    confidence_order = [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
    min_confidence = ConfidenceLevel.HIGH

    for estimate in estimates:
        if confidence_order.index(estimate.confidence) < confidence_order.index(min_confidence):
            min_confidence = estimate.confidence

    return min_confidence
```

## 5.5 Putting It All Together

Here's how the services work together:

```python
# Create services
feature_library = FeatureLibraryService()
time_tracking = TimeTrackingService()
estimation = EstimationService(feature_library, time_tracking)

# Add features
feature_library.add_feature(Feature(
    id="f1",
    name="CRUD",
    team=TeamType.BACKEND,
    process="Data Operations",
    seed_time_hours=4.0,
    synonyms=["crud-api", "rest-crud"]
))

# Add tracked time
from datetime import date
time_tracking.add_entry(TrackedTimeEntry(
    id="t1", team=TeamType.BACKEND, member_name="BE-1",
    feature="CRUD", tracked_time_hours=4.5,
    process="Data Operations", date=date(2025, 1, 15)
))
time_tracking.add_entry(TrackedTimeEntry(
    id="t2", team=TeamType.BACKEND, member_name="BE-2",
    feature="CRUD", tracked_time_hours=3.5,
    process="Data Operations", date=date(2025, 1, 16)
))
time_tracking.add_entry(TrackedTimeEntry(
    id="t3", team=TeamType.BACKEND, member_name="BE-1",
    feature="CRUD", tracked_time_hours=5.0,
    process="Data Operations", date=date(2025, 1, 17)
))

# Estimate
result = estimation.estimate_feature("CRUD")
if result.is_ok():
    estimate = result.unwrap()
    print(f"Feature: {estimate.feature_name}")
    print(f"Estimated hours: {estimate.estimated_hours:.1f}")
    print(f"Confidence: {estimate.confidence.value}")
    print(f"Used seed time: {estimate.used_seed_time}")
```

**Output:**

```
Feature: CRUD
Estimated hours: 4.7
Confidence: medium
Used seed time: False
```

## 5.6 Debugging Scenario

**The Bug:** Feature search returns nothing even though features exist.

```python
service = FeatureLibraryService()
service.add_feature(Feature("f1", "CRUD API", TeamType.BACKEND, "Data", 4.0))

results = service.search_features("crud")
print(results)  # [] - Empty! Why?
```

**The Problem:** The search implementation doesn't normalize the feature name.

**The Fix:** Ensure both query and feature name are normalized:

```python
def search_features(self, query: str) -> List[Feature]:
    normalized_query = normalize_text(query)  # "crud"

    for feature in self._features.values():
        if normalized_query in normalize_text(feature.name):  # "crud api"
            results.append(feature)  # ✅ Now matches!
```

## 5.7 Quick Check Questions

1. Why use `Dict[str, Feature]` instead of `List[Feature]` for storage?
2. What does P80 mean and why use it for estimates?
3. When does the estimation service use seed time?
4. How is overall project confidence determined?
5. Why normalize text for searching?

<details>
<summary>Answers</summary>

1. O(1) lookup by ID vs O(n) for lists
2. 80th percentile - 80% of actual times are at or below this value. Conservative but realistic.
3. When fewer than `min_data_points_for_stats` (default 3) entries exist
4. Uses the lowest confidence level among all features
5. To match regardless of case, hyphens, underscores, or extra spaces

</details>

## 5.8 Mini-Project: Service Integration Test

Create a test that exercises all three services together:

```python
def test_full_estimation_workflow():
    """Test the complete estimation workflow."""
    # Setup
    feature_lib = FeatureLibraryService()
    time_tracking = TimeTrackingService()
    estimation = EstimationService(feature_lib, time_tracking)

    # Add features
    feature_lib.add_feature(Feature(
        "f1", "Authentication", TeamType.BACKEND, "Auth", 8.0,
        synonyms=["auth", "login"]
    ))
    feature_lib.add_feature(Feature(
        "f2", "Dashboard", TeamType.FRONTEND, "Content", 12.0
    ))

    # Add tracked time for auth (10 entries = HIGH confidence)
    for i in range(10):
        time_tracking.add_entry(TrackedTimeEntry(
            id=f"auth_{i}",
            team=TeamType.BACKEND,
            member_name=f"BE-{i % 3}",
            feature="Authentication",
            tracked_time_hours=7.0 + (i * 0.5),  # 7.0 to 11.5
            process="Auth",
            date=date(2025, 1, i + 1)
        ))

    # Estimate auth - should use statistics
    result = estimation.estimate_feature("auth")  # Using synonym!
    assert result.is_ok()
    auth_estimate = result.unwrap()
    assert auth_estimate.confidence == ConfidenceLevel.HIGH
    assert not auth_estimate.used_seed_time

    # Estimate dashboard - should use seed time (no tracked data)
    result = estimation.estimate_feature("Dashboard")
    assert result.is_ok()
    dash_estimate = result.unwrap()
    assert dash_estimate.confidence == ConfidenceLevel.LOW
    assert dash_estimate.used_seed_time
    assert dash_estimate.estimated_hours == 12.0

    # Project estimate
    result = estimation.estimate_project(["Authentication", "Dashboard"])
    assert result.is_ok()
    project = result.unwrap()
    assert len(project.features) == 2
    assert project.confidence == ConfidenceLevel.LOW  # Lowest of the two

    print("✅ Full workflow test passed!")


test_full_estimation_workflow()
```

**Acceptance Criteria:**

- [ ] All assertions pass
- [ ] Synonym search works ("auth" finds "Authentication")
- [ ] Confidence levels are correct
- [ ] Project estimate aggregates correctly

## 5.9 AITEA Integration

This chapter implements:

- **Requirement 1.5**: FeatureLibraryService, TimeTrackingService, EstimationService
- **Requirement 9.1-9.5**: Statistics computation and confidence levels
- **Property 18**: Low Data Point Fallback
- **Property 20**: Project Estimate Aggregation
- **Property 21**: Confidence Level Thresholds

**Verification:**

```bash
# Run the property tests
python -m pytest tests/properties/test_model_props.py::TestLowDataPointFallback -v

# Type check
mypy src/services/implementations.py
```

## What's Next

In Chapter 6, we'll implement the utility functions for statistics calculation. You'll learn:

- Mean, median, standard deviation, and P80 calculations
- Outlier detection algorithms
- Text normalization for search

**Before proceeding:**

- Ensure all service methods return proper Result types
- Test the estimation workflow end-to-end
- Understand the confidence level thresholds
