# Chapter 4: Abstract Classes & Interfaces

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-3  
**AITEA Component:** `src/services/interfaces.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Define abstract base classes (ABCs) for service interfaces
2. Use the `@abstractmethod` decorator correctly
3. Understand why interfaces enable testability and flexibility
4. Implement dependency injection patterns
5. Design clean service contracts

## 4.1 The Problem: Tight Coupling

Consider this estimation service that directly uses a database:

```python
# ❌ Tightly coupled
class EstimationService:
    def __init__(self):
        self.db = PostgresDatabase("localhost:5432")  # Hard-coded!

    def estimate(self, feature: str) -> float:
        data = self.db.query(f"SELECT * FROM features WHERE name='{feature}'")
        return data.seed_time
```

**Problems:**

- Can't test without a real database
- Can't switch to a different database
- Can't use mock data for development

## 4.2 The Solution: Interfaces

Define a contract (interface) that any implementation must follow:

```python
from abc import ABC, abstractmethod

# ✅ Interface defines the contract
class IFeatureRepository(ABC):
    @abstractmethod
    def get_feature(self, name: str) -> Feature:
        """Get a feature by name."""
        ...

# Implementation 1: Real database
class PostgresFeatureRepository(IFeatureRepository):
    def get_feature(self, name: str) -> Feature:
        # Real database query
        ...

# Implementation 2: In-memory for testing
class InMemoryFeatureRepository(IFeatureRepository):
    def get_feature(self, name: str) -> Feature:
        return self._features.get(name)
```

Now the service depends on the interface, not the implementation:

```python
class EstimationService:
    def __init__(self, repository: IFeatureRepository):  # Accepts any implementation!
        self.repository = repository
```

## 4.3 ABC and @abstractmethod

Python's `abc` module provides Abstract Base Classes:

```python
from abc import ABC, abstractmethod

class IFeatureLibraryService(ABC):
    """Interface for managing the feature library."""

    @abstractmethod
    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        """Add a new feature to the library."""
        ...  # No implementation - just the signature

    @abstractmethod
    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        """Retrieve a feature by its ID."""
        ...
```

**Key rules:**

1. Inherit from `ABC`
2. Mark methods with `@abstractmethod`
3. Use `...` (ellipsis) for the body
4. You cannot instantiate an ABC directly

```python
# This raises TypeError!
service = IFeatureLibraryService()  # ❌ Can't instantiate abstract class
```

### Your Turn: Exercise 4.1

What happens if you forget to implement an abstract method?

```python
class IAnimal(ABC):
    @abstractmethod
    def speak(self) -> str:
        ...

class Dog(IAnimal):
    pass  # Forgot to implement speak()!

dog = Dog()  # What happens?
```

**Answer:** `TypeError: Can't instantiate abstract class Dog with abstract method speak`

## 4.4 The Result Type Pattern

Before defining our interfaces, let's understand the Result type. Instead of raising exceptions, we return a Result that's either success or error:

```python
from models.result import Result
from models.errors import ValidationError, NotFoundError

# Success case
result = Result.ok(feature)
if result.is_ok():
    feature = result.unwrap()

# Error case
result = Result.err(NotFoundError("Feature", "f123"))
if result.is_err():
    error = result.unwrap_err()
```

**Why Result instead of exceptions?**

- Errors are explicit in the function signature
- Callers must handle both cases
- No hidden control flow

## 4.5 AITEA Service Interfaces

Let's define the three core service interfaces:

### IFeatureLibraryService

```python
class IFeatureLibraryService(ABC):
    """Interface for managing the feature library."""

    @abstractmethod
    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        """Add a new feature to the library.

        Args:
            feature: The feature to add

        Returns:
            Result containing the added feature on success,
            or ValidationError if invalid or already exists
        """
        ...

    @abstractmethod
    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        """Retrieve a feature by its ID."""
        ...

    @abstractmethod
    def search_features(self, query: str) -> List[Feature]:
        """Search for features matching a query string."""
        ...

    @abstractmethod
    def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
        """List all features, optionally filtered by team."""
        ...
```

### ITimeTrackingService

```python
class ITimeTrackingService(ABC):
    """Interface for managing tracked time entries."""

    @abstractmethod
    def add_entry(self, entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, ValidationError]:
        """Add a new tracked time entry."""
        ...

    @abstractmethod
    def import_csv(self, path: Path) -> Result[ImportResult, ImportError]:
        """Import tracked time entries from a CSV file."""
        ...

    @abstractmethod
    def get_entries_for_feature(self, feature_name: str) -> List[TrackedTimeEntry]:
        """Get all tracked time entries for a specific feature."""
        ...
```

### IEstimationService

```python
class IEstimationService(ABC):
    """Interface for computing time estimates."""

    @abstractmethod
    def estimate_feature(self, feature_name: str) -> Result[FeatureEstimate, EstimationError]:
        """Estimate time for a single feature."""
        ...

    @abstractmethod
    def estimate_project(self, features: List[str]) -> Result[ProjectEstimate, EstimationError]:
        """Estimate time for a project with multiple features."""
        ...

    @abstractmethod
    def compute_statistics(self, entries: List[TrackedTimeEntry]) -> FeatureStatistics:
        """Compute statistical measures from tracked time entries."""
        ...
```

### Your Turn: Exercise 4.2

Add a helper dataclass for import results:

```python
@dataclass
class ImportResult:
    """Result of a CSV import operation."""
    # TODO: Add these fields:
    # successful_count: int
    # failed_count: int
    # total_count: int
    # errors: List[ImportError]
    pass
```

## 4.6 Dependency Injection

With interfaces defined, we can inject dependencies:

```python
class EstimationService(IEstimationService):
    def __init__(
        self,
        feature_library: IFeatureLibraryService,  # Interface, not implementation!
        time_tracking: ITimeTrackingService,
        config: Optional[EstimationConfig] = None
    ):
        self._feature_library = feature_library
        self._time_tracking = time_tracking
        self._config = config or EstimationConfig()
```

**Benefits:**

1. **Testability**: Inject mock services for testing
2. **Flexibility**: Swap implementations without changing code
3. **Clarity**: Dependencies are explicit in the constructor

### Production vs Testing

```python
# Production: Real services
feature_lib = PostgresFeatureLibrary(db_connection)
time_tracking = PostgresTimeTracking(db_connection)
estimation = EstimationService(feature_lib, time_tracking)

# Testing: Mock services
feature_lib = InMemoryFeatureLibrary()
time_tracking = InMemoryTimeTracking()
estimation = EstimationService(feature_lib, time_tracking)
```

## 4.7 Complete Implementation

Here's the complete `src/services/interfaces.py`:

```python
"""Abstract base classes defining service interfaces for AITEA."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

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
    """Result of a CSV import operation."""
    successful_count: int
    failed_count: int
    total_count: int
    errors: List[ImportError]


class IFeatureLibraryService(ABC):
    """Interface for managing the feature library."""

    @abstractmethod
    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        """Add a new feature to the library."""
        ...

    @abstractmethod
    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        """Retrieve a feature by its ID."""
        ...

    @abstractmethod
    def search_features(self, query: str) -> List[Feature]:
        """Search for features matching a query string."""
        ...

    @abstractmethod
    def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
        """List all features, optionally filtered by team."""
        ...


class ITimeTrackingService(ABC):
    """Interface for managing tracked time entries."""

    @abstractmethod
    def add_entry(self, entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, ValidationError]:
        """Add a new tracked time entry."""
        ...

    @abstractmethod
    def import_csv(self, path: Path) -> Result[ImportResult, ImportError]:
        """Import tracked time entries from a CSV file."""
        ...

    @abstractmethod
    def get_entries_for_feature(self, feature_name: str) -> List[TrackedTimeEntry]:
        """Get all tracked time entries for a specific feature."""
        ...


class IEstimationService(ABC):
    """Interface for computing time estimates."""

    @abstractmethod
    def estimate_feature(self, feature_name: str) -> Result[FeatureEstimate, EstimationError]:
        """Estimate time for a single feature."""
        ...

    @abstractmethod
    def estimate_project(self, features: List[str]) -> Result[ProjectEstimate, EstimationError]:
        """Estimate time for a project with multiple features."""
        ...

    @abstractmethod
    def compute_statistics(self, entries: List[TrackedTimeEntry]) -> FeatureStatistics:
        """Compute statistical measures from tracked time entries."""
        ...
```

## 4.8 Debugging Scenario

**The Bug:** Forgetting `ABC` inheritance.

```python
from abc import abstractmethod

class IService:  # ❌ Missing ABC!
    @abstractmethod
    def do_something(self) -> None:
        ...

class ConcreteService(IService):
    pass  # Forgot to implement do_something

service = ConcreteService()  # No error! 😱
service.do_something()  # TypeError at runtime
```

**The Fix:** Always inherit from `ABC`:

```python
from abc import ABC, abstractmethod

class IService(ABC):  # ✅ Inherit from ABC
    @abstractmethod
    def do_something(self) -> None:
        ...

class ConcreteService(IService):
    pass

service = ConcreteService()  # TypeError: Can't instantiate abstract class
```

## 4.9 Quick Check Questions

1. What module provides Abstract Base Classes?
2. What happens if you try to instantiate an ABC?
3. Why use interfaces instead of concrete classes?
4. What is dependency injection?
5. What does `...` (ellipsis) mean in an abstract method?

<details>
<summary>Answers</summary>

1. The `abc` module
2. `TypeError: Can't instantiate abstract class`
3. Enables testability, flexibility, and loose coupling
4. Passing dependencies to a class instead of creating them internally
5. It's a placeholder indicating no implementation (same as `pass`)

</details>

## 4.10 Mini-Project: Mock Service

Create a mock implementation of `IFeatureLibraryService` for testing:

```python
class MockFeatureLibraryService(IFeatureLibraryService):
    """Mock implementation for testing."""

    def __init__(self, features: Optional[List[Feature]] = None):
        self._features: Dict[str, Feature] = {}
        if features:
            for f in features:
                self._features[f.id] = f

    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        if feature.id in self._features:
            return Result.err(ValidationError("id", "Already exists", feature.id))
        self._features[feature.id] = feature
        return Result.ok(feature)

    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        if feature_id not in self._features:
            return Result.err(NotFoundError("Feature", feature_id))
        return Result.ok(self._features[feature_id])

    def search_features(self, query: str) -> List[Feature]:
        query_lower = query.lower()
        return [f for f in self._features.values()
                if query_lower in f.name.lower()]

    def list_features(self, team: Optional[TeamType] = None) -> List[Feature]:
        if team is None:
            return list(self._features.values())
        return [f for f in self._features.values() if f.team == team]


# Test it:
mock = MockFeatureLibraryService([
    Feature("f1", "CRUD API", TeamType.BACKEND, "Data Ops", 4.0),
    Feature("f2", "Auth", TeamType.BACKEND, "Auth", 8.0),
])

result = mock.get_feature("f1")
assert result.is_ok()
assert result.unwrap().name == "CRUD API"

result = mock.get_feature("nonexistent")
assert result.is_err()

print("✅ Mock service works!")
```

**Acceptance Criteria:**

- [ ] Implements all abstract methods
- [ ] Returns proper Result types
- [ ] Can be used in place of real implementation
- [ ] Passes mypy type checking

## 4.11 AITEA Integration

This chapter implements:

- **Requirement 1.4**: Abstract base classes defining service interfaces
- **Property 3**: Service Result Pattern Consistency

**Verification:**

```bash
# Type check the interfaces
mypy src/services/interfaces.py

# Verify you can't instantiate ABCs
python -c "from services.interfaces import IFeatureLibraryService; IFeatureLibraryService()"
# Should raise TypeError
```

## What's Next

In Chapter 5, we'll implement the concrete services using in-memory storage. You'll learn:

- How to implement abstract methods
- In-memory data storage patterns
- Using the Result type in practice

**Before proceeding:**

- Understand why interfaces enable testing
- Review the Result type pattern
- Ensure you can explain dependency injection
