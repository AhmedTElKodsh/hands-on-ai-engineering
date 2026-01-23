# Chapter 3: Dataclasses & Data Models

**Difficulty:** Beginner  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-2  
**AITEA Component:** `src/models/dataclasses.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create dataclasses with proper field definitions
2. Use `Optional` and `List` types for complex fields
3. Implement `__post_init__` for validation
4. Add serialization methods (`to_dict`, `from_dict`)
5. Design nested data structures

## 3.1 The Problem with Regular Classes

Without dataclasses, defining a simple data container is verbose:

```python
# ❌ Verbose: Regular class
class Feature:
    def __init__(self, id, name, team, seed_time_hours):
        self.id = id
        self.name = name
        self.team = team
        self.seed_time_hours = seed_time_hours

    def __repr__(self):
        return f"Feature(id={self.id!r}, name={self.name!r}, ...)"

    def __eq__(self, other):
        if not isinstance(other, Feature):
            return False
        return (self.id == other.id and
                self.name == other.name and ...)
```

That's a lot of boilerplate for a simple data container!

## 3.2 Dataclasses to the Rescue

Dataclasses generate `__init__`, `__repr__`, and `__eq__` automatically:

```python
from dataclasses import dataclass

# ✅ Clean: Dataclass
@dataclass
class Feature:
    id: str
    name: str
    team: TeamType
    seed_time_hours: float
```

That's it! Python generates all the boilerplate for you.

```python
# These all work automatically:
f = Feature("feat_001", "CRUD", TeamType.BACKEND, 4.0)
print(f)  # Feature(id='feat_001', name='CRUD', ...)
f == Feature("feat_001", "CRUD", TeamType.BACKEND, 4.0)  # True
```

## 3.3 Field Defaults and Factories

Some fields should have default values:

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Feature:
    id: str
    name: str
    team: TeamType
    process: str
    seed_time_hours: float
    synonyms: List[str] = field(default_factory=list)  # Mutable default
    notes: str = ""  # Immutable default
```

**⚠️ Important:** Never use mutable defaults directly!

```python
# ❌ WRONG: Mutable default
@dataclass
class Bad:
    items: List[str] = []  # All instances share the same list!

# ✅ CORRECT: Use field(default_factory=...)
@dataclass
class Good:
    items: List[str] = field(default_factory=list)  # Each instance gets its own list
```

### Your Turn: Exercise 3.1

Create a `TrackedTimeEntry` dataclass:

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class TrackedTimeEntry:
    """A record of actual time spent on a feature."""
    # TODO: Add these fields:
    # id: str
    # team: TeamType
    # member_name: str
    # feature: str
    # tracked_time_hours: float
    # process: str
    # date: date
    pass

# Test it:
entry = TrackedTimeEntry(
    id="track_001",
    team=TeamType.BACKEND,
    member_name="BE-1",
    feature="CRUD",
    tracked_time_hours=4.5,
    process="Data Operations",
    date=date(2025, 1, 15)
)
print(entry)
```

## 3.4 Validation with **post_init**

Dataclasses call `__post_init__` after `__init__`. Use it for validation:

```python
@dataclass
class Feature:
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
```

Now invalid data is caught immediately:

```python
# This raises ValueError: seed_time_hours must be positive
Feature("f1", "Test", TeamType.BACKEND, "Process", -5.0)
```

### Your Turn: Exercise 3.2

Add validation to `TrackedTimeEntry`:

```python
def __post_init__(self) -> None:
    """Validate field values after initialization."""
    # TODO: Validate:
    # - id cannot be empty
    # - member_name cannot be empty
    # - feature cannot be empty
    # - tracked_time_hours must be positive
    pass
```

## 3.5 Optional Fields

Use `Optional` for fields that might be `None`:

```python
from typing import Optional

@dataclass
class FeatureEstimate:
    feature_name: str
    estimated_hours: float
    confidence: ConfidenceLevel
    statistics: Optional[FeatureStatistics] = None  # May not have stats
    used_seed_time: bool = False
```

**When to use Optional:**

- Field might not have a value
- Field is computed later
- Field depends on external data availability

## 3.6 Nested Dataclasses

AITEA has nested structures. A `ProjectEstimate` contains multiple `FeatureEstimate` objects:

```python
@dataclass
class FeatureStatistics:
    """Statistical measures for feature time estimates."""
    mean: float
    median: float
    std_dev: float
    p80: float
    data_point_count: int


@dataclass
class FeatureEstimate:
    """Estimate for a single feature."""
    feature_name: str
    estimated_hours: float
    confidence: ConfidenceLevel
    statistics: Optional[FeatureStatistics] = None
    used_seed_time: bool = False


@dataclass
class ProjectEstimate:
    """Complete project estimation with feature breakdown."""
    features: List[FeatureEstimate]  # Nested list!
    total_hours: float
    confidence: ConfidenceLevel
```

## 3.7 Serialization: to_dict and from_dict

For JSON persistence, add serialization methods:

```python
from dataclasses import dataclass, field, asdict
from typing import Dict, Any

@dataclass
class Feature:
    id: str
    name: str
    team: TeamType
    process: str
    seed_time_hours: float
    synonyms: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON persistence."""
        data = asdict(self)
        data['team'] = self.team.value  # Convert enum to string
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feature':
        """Deserialize from dictionary."""
        data = data.copy()  # Don't modify original
        data['team'] = TeamType(data['team'])  # Convert string to enum
        return cls(**data)
```

**Usage:**

```python
# Serialize
feature = Feature("f1", "CRUD", TeamType.BACKEND, "Data Ops", 4.0)
data = feature.to_dict()
print(data)  # {'id': 'f1', 'name': 'CRUD', 'team': 'backend', ...}

# Deserialize
loaded = Feature.from_dict(data)
assert loaded == feature  # ✅
```

### Your Turn: Exercise 3.3

Add `to_dict` and `from_dict` to `TrackedTimeEntry`. Remember to handle:

- `team` enum conversion
- `date` to ISO string conversion

```python
def to_dict(self) -> Dict[str, Any]:
    """Serialize to dictionary for JSON persistence."""
    data = asdict(self)
    data['team'] = self.team.value
    data['date'] = self.date.isoformat()  # "2025-01-15"
    return data

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'TrackedTimeEntry':
    """Deserialize from dictionary."""
    data = data.copy()
    data['team'] = TeamType(data['team'])
    if isinstance(data['date'], str):
        data['date'] = date.fromisoformat(data['date'])
    return cls(**data)
```

## 3.8 Complete Implementation

Here's the complete `src/models/dataclasses.py`:

```python
"""Core dataclass models for AITEA."""

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List, Optional, Dict, Any

from .enums import TeamType, ConfidenceLevel


@dataclass
class Feature:
    """A software feature with time estimation metadata."""
    id: str
    name: str
    team: TeamType
    process: str
    seed_time_hours: float
    synonyms: List[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Feature id cannot be empty")
        if not self.name:
            raise ValueError("Feature name cannot be empty")
        if self.seed_time_hours <= 0:
            raise ValueError("seed_time_hours must be positive")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['team'] = self.team.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feature':
        data = data.copy()
        data['team'] = TeamType(data['team'])
        return cls(**data)


@dataclass
class TrackedTimeEntry:
    """A record of actual time spent on a feature."""
    id: str
    team: TeamType
    member_name: str
    feature: str
    tracked_time_hours: float
    process: str
    date: date

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("TrackedTimeEntry id cannot be empty")
        if not self.member_name:
            raise ValueError("member_name cannot be empty")
        if not self.feature:
            raise ValueError("feature cannot be empty")
        if self.tracked_time_hours <= 0:
            raise ValueError("tracked_time_hours must be positive")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['team'] = self.team.value
        data['date'] = self.date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrackedTimeEntry':
        data = data.copy()
        data['team'] = TeamType(data['team'])
        if isinstance(data['date'], str):
            data['date'] = date.fromisoformat(data['date'])
        return cls(**data)


@dataclass
class FeatureStatistics:
    """Statistical measures for feature time estimates."""
    mean: float
    median: float
    std_dev: float
    p80: float
    data_point_count: int

    def __post_init__(self) -> None:
        if self.std_dev < 0:
            raise ValueError("std_dev cannot be negative")
        if self.data_point_count < 0:
            raise ValueError("data_point_count cannot be negative")


@dataclass
class FeatureEstimate:
    """Estimate for a single feature within a project."""
    feature_name: str
    estimated_hours: float
    confidence: ConfidenceLevel
    statistics: Optional[FeatureStatistics] = None
    used_seed_time: bool = False

    def __post_init__(self) -> None:
        if not self.feature_name:
            raise ValueError("feature_name cannot be empty")
        if self.estimated_hours <= 0:
            raise ValueError("estimated_hours must be positive")


@dataclass
class ProjectEstimate:
    """Complete project estimation with feature breakdown."""
    features: List[FeatureEstimate]
    total_hours: float
    confidence: ConfidenceLevel

    def __post_init__(self) -> None:
        if self.total_hours < 0:
            raise ValueError("total_hours cannot be negative")
        if not self.features:
            raise ValueError("features list cannot be empty")


@dataclass
class EstimationConfig:
    """Configuration for estimation calculations."""
    use_outlier_detection: bool = True
    outlier_threshold_std: float = 2.0
    min_data_points_for_stats: int = 3

    def __post_init__(self) -> None:
        if self.outlier_threshold_std <= 0:
            raise ValueError("outlier_threshold_std must be positive")
        if self.min_data_points_for_stats < 1:
            raise ValueError("min_data_points_for_stats must be at least 1")
```

## 3.9 Debugging Scenario

**The Bug:** Mutable default argument causes shared state.

```python
@dataclass
class Task:
    name: str
    tags: List[str] = []  # ❌ Bug!

t1 = Task("Task 1")
t1.tags.append("urgent")

t2 = Task("Task 2")
print(t2.tags)  # ['urgent'] - Wait, why does t2 have t1's tag?!
```

**The Fix:** Use `field(default_factory=list)`:

```python
@dataclass
class Task:
    name: str
    tags: List[str] = field(default_factory=list)  # ✅ Fixed!

t1 = Task("Task 1")
t1.tags.append("urgent")

t2 = Task("Task 2")
print(t2.tags)  # [] - Correct!
```

## 3.10 Quick Check Questions

1. What decorator creates a dataclass?
2. How do you specify a mutable default value?
3. When is `__post_init__` called?
4. What does `asdict()` do?
5. Why use `data.copy()` in `from_dict`?

<details>
<summary>Answers</summary>

1. `@dataclass`
2. `field(default_factory=list)` or `field(default_factory=dict)`
3. After `__init__` completes
4. Converts a dataclass instance to a dictionary
5. To avoid modifying the original dictionary passed in

</details>

## 3.11 Mini-Project: Feature Library

Create a simple in-memory feature library:

```python
from typing import Dict, List, Optional

class SimpleFeatureLibrary:
    """In-memory storage for features."""

    def __init__(self):
        self._features: Dict[str, Feature] = {}

    def add(self, feature: Feature) -> bool:
        """Add a feature. Returns False if ID already exists."""
        if feature.id in self._features:
            return False
        self._features[feature.id] = feature
        return True

    def get(self, feature_id: str) -> Optional[Feature]:
        """Get a feature by ID. Returns None if not found."""
        return self._features.get(feature_id)

    def list_all(self) -> List[Feature]:
        """List all features."""
        return list(self._features.values())

    def to_json_data(self) -> List[Dict[str, Any]]:
        """Export all features as JSON-serializable data."""
        return [f.to_dict() for f in self._features.values()]


# Test it:
library = SimpleFeatureLibrary()

library.add(Feature("f1", "CRUD", TeamType.BACKEND, "Data Ops", 4.0))
library.add(Feature("f2", "Auth", TeamType.BACKEND, "Auth", 8.0))

assert library.get("f1").name == "CRUD"
assert len(library.list_all()) == 2
assert library.add(Feature("f1", "Duplicate", TeamType.QA, "Test", 1.0)) == False

print("✅ Mini-project complete!")
```

**Acceptance Criteria:**

- [ ] All methods have type hints
- [ ] Duplicate IDs are rejected
- [ ] `to_json_data()` produces valid JSON-serializable output
- [ ] Passes mypy without errors

## 3.12 AITEA Integration

This chapter implements:

- **Requirement 1.3**: Dataclass models for Feature, TrackedTimeEntry, ProjectEstimate, EstimationConfig
- **Requirement 8.1-8.3**: Data model field definitions
- **Property 2**: Dataclass Instantiation Validity

**Verification:**

```bash
# Type check the models
mypy src/models/dataclasses.py

# Run the property tests
python -m pytest tests/properties/test_model_props.py::TestDataclassInstantiationValidity -v
```

## What's Next

In Chapter 4, we'll define service interfaces using Abstract Base Classes. You'll learn:

- How to define contracts with ABC
- The `@abstractmethod` decorator
- Dependency injection patterns

**Before proceeding:**

- Ensure all dataclasses have validation in `__post_init__`
- Test serialization round-trips work correctly
- Run mypy on the models module
