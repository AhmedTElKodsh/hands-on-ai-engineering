# Chapter 2: Enums & Type Hints

**Difficulty:** Beginner  
**Time:** 1.5 hours  
**Prerequisites:** Chapter 1  
**AITEA Component:** `src/models/enums.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create Python enumerations for type-safe constants
2. Use string-based enums for JSON serialization
3. Apply type hints to function signatures
4. Run mypy for static type checking
5. Understand why enums are better than string constants

## 2.1 The Problem with String Constants

Consider this code for categorizing team members:

```python
# ❌ Bad: Using raw strings
def assign_task(team: str, task: str):
    if team == "backend":
        # ...
    elif team == "fronted":  # Typo! "frontend" misspelled
        # ...
```

**Problems:**

- Typos aren't caught until runtime
- No autocomplete in your IDE
- Easy to use invalid values
- Hard to see all valid options

## 2.2 Enums to the Rescue

Enums define a fixed set of named constants:

```python
from enum import Enum

class TeamType(Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
```

Now the IDE catches typos immediately:

```python
# ✅ Good: Using enums
def assign_task(team: TeamType, task: str):
    if team == TeamType.BACKEND:
        # ...
    elif team == TeamType.FRONTED:  # ❌ IDE error: FRONTED doesn't exist!
        # ...
```

## 2.3 String-Based Enums

For AITEA, we need enums that serialize nicely to JSON. The trick is inheriting from both `str` and `Enum`:

```python
from enum import Enum


class TeamType(str, Enum):
    """Team types for feature categorization."""
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DESIGN = "design"
    QA = "qa"
    DEVOPS = "devops"
```

**Why `str, Enum`?**

```python
# Regular Enum
class Color(Enum):
    RED = "red"

print(Color.RED)        # Color.RED
print(Color.RED.value)  # "red"

# String Enum
class Color(str, Enum):
    RED = "red"

print(Color.RED)        # "red" (acts like a string!)
print(Color.RED.value)  # "red"
```

This makes JSON serialization seamless:

```python
import json

team = TeamType.BACKEND
data = {"team": team}  # Works directly!
print(json.dumps(data))  # {"team": "backend"}
```

### Your Turn: Exercise 2.1

Create the `ProcessType` enum with these values:

```python
class ProcessType(str, Enum):
    """Process types for feature categorization."""
    # TODO: Add these members:
    # DATA_OPERATIONS = "Data Operations"
    # CONTENT_MANAGEMENT = "Content Management"
    # REAL_TIME = "Real-time"
    # AUTHENTICATION = "Authentication"
    # INTEGRATION = "Integration"
    pass
```

**Test your implementation:**

```python
assert ProcessType.DATA_OPERATIONS.value == "Data Operations"
assert str(ProcessType.REAL_TIME) == "Real-time"
print("✅ ProcessType enum works!")
```

## 2.4 The ConfidenceLevel Enum

AITEA estimates have confidence levels based on how much historical data exists:

```python
class ConfidenceLevel(str, Enum):
    """Confidence levels for estimates based on data point count.

    - LOW: 1-2 data points (using seed time)
    - MEDIUM: 3-9 data points (some historical data)
    - HIGH: 10+ data points (reliable statistics)
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

The docstring documents the business rules - this is crucial for maintainability!

## 2.5 Type Hints Fundamentals

Type hints tell Python (and your IDE) what types to expect:

```python
# Without type hints
def calculate_estimate(hours, confidence):
    return hours * confidence

# With type hints
def calculate_estimate(hours: float, confidence: float) -> float:
    return hours * confidence
```

**Common type hints:**

```python
from typing import List, Optional, Dict, Tuple

def process_features(
    names: List[str],                    # List of strings
    config: Optional[Dict[str, int]],    # Dict or None
    default_hours: float = 4.0           # Float with default
) -> Tuple[int, float]:                  # Returns tuple
    ...
```

### Your Turn: Exercise 2.2

Add type hints to this function:

```python
# Before: No type hints
def get_team_members(team, include_leads):
    if include_leads:
        return ["Alice", "Bob", "Charlie"]
    return ["Alice", "Bob"]

# After: Add type hints
def get_team_members(team: ???, include_leads: ???) -> ???:
    ...
```

**Expected signature:**

```python
def get_team_members(team: TeamType, include_leads: bool) -> List[str]:
```

## 2.6 Static Type Checking with mypy

Type hints are just documentation unless you check them. Enter mypy:

```bash
# Install mypy
pip install mypy

# Check a file
mypy src/models/enums.py

# Check the whole project
mypy src/
```

**Example mypy output:**

```
src/services/estimation.py:42: error: Argument 1 to "estimate" has
incompatible type "str"; expected "TeamType"
```

### mypy Configuration

Add to `mypy.ini` or `pyproject.toml`:

```ini
# mypy.ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_ignores = True
disallow_untyped_defs = True
```

Or in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
disallow_untyped_defs = true
```

### Your Turn: Exercise 2.3

Create a file with a type error and run mypy:

```python
# type_error_example.py
from models.enums import TeamType

def assign_team(team: TeamType) -> str:
    return f"Assigned to {team}"

# This should cause a mypy error:
result = assign_team("backend")  # Wrong! Should be TeamType.BACKEND
```

Run: `mypy type_error_example.py`

## 2.7 Complete Implementation

Here's the complete `src/models/enums.py`:

```python
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
    """Confidence levels for estimates based on data point count.

    Thresholds:
    - LOW: 1-2 data points
    - MEDIUM: 3-9 data points
    - HIGH: 10+ data points
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

## 2.8 Debugging Scenario

**The Bug:** JSON serialization fails with a regular enum.

```python
import json
from enum import Enum

class Status(Enum):  # Missing str inheritance!
    ACTIVE = "active"
    INACTIVE = "inactive"

data = {"status": Status.ACTIVE}
json.dumps(data)  # TypeError: Object of type Status is not JSON serializable
```

**The Fix:** Inherit from `str`:

```python
class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

data = {"status": Status.ACTIVE}
json.dumps(data)  # '{"status": "active"}' ✅
```

## 2.9 Quick Check Questions

1. Why inherit from both `str` and `Enum`?
2. What's the difference between `TeamType.BACKEND` and `TeamType.BACKEND.value`?
3. What tool checks type hints at development time?
4. How do you specify a function returns nothing?
5. What type hint means "string or None"?

<details>
<summary>Answers</summary>

1. So the enum values serialize directly to JSON as strings
2. With `str, Enum`, they're the same. Without `str`, `.value` gives the string
3. mypy
4. `-> None`
5. `Optional[str]` or `str | None` (Python 3.10+)

</details>

## 2.10 Mini-Project: Team Statistics

Create a function that counts team members by type:

```python
from typing import Dict, List
from models.enums import TeamType


def count_by_team(members: List[Dict[str, TeamType]]) -> Dict[TeamType, int]:
    """Count how many members are in each team.

    Args:
        members: List of dicts with 'name' and 'team' keys

    Returns:
        Dictionary mapping TeamType to count

    Example:
        >>> members = [
        ...     {"name": "Alice", "team": TeamType.BACKEND},
        ...     {"name": "Bob", "team": TeamType.BACKEND},
        ...     {"name": "Charlie", "team": TeamType.FRONTEND},
        ... ]
        >>> count_by_team(members)
        {TeamType.BACKEND: 2, TeamType.FRONTEND: 1}
    """
    # Your implementation here
    pass


# Test your implementation
members = [
    {"name": "Alice", "team": TeamType.BACKEND},
    {"name": "Bob", "team": TeamType.BACKEND},
    {"name": "Charlie", "team": TeamType.FRONTEND},
    {"name": "Diana", "team": TeamType.QA},
]

result = count_by_team(members)
assert result[TeamType.BACKEND] == 2
assert result[TeamType.FRONTEND] == 1
assert result[TeamType.QA] == 1
print("✅ Mini-project complete!")
```

**Acceptance Criteria:**

- [ ] Function has complete type hints
- [ ] Passes mypy without errors
- [ ] All test assertions pass
- [ ] Handles empty list input

## 2.11 AITEA Integration

This chapter implements:

- **Requirement 1.2**: Enums for Team, Process, and ConfidenceLevel
- **Property 1**: Enum Completeness and Type Safety

**Verification:**

```bash
# Type check the enums module
mypy src/models/enums.py

# Run the property tests
python -m pytest tests/properties/test_model_props.py::TestEnumProperties -v
```

**Expected output:**

```
tests/properties/test_model_props.py::TestEnumProperties::test_team_type_string_inheritance PASSED
tests/properties/test_model_props.py::TestEnumProperties::test_process_type_string_inheritance PASSED
tests/properties/test_model_props.py::TestEnumProperties::test_confidence_level_string_inheritance PASSED
```

## What's Next

In Chapter 3, we'll use these enums to build dataclass models for Features, TrackedTimeEntries, and ProjectEstimates. You'll learn:

- How dataclasses reduce boilerplate
- Field defaults and validation
- Nested data structures with type hints

**Before proceeding:**

- Ensure mypy passes on `src/models/enums.py`
- Run the enum property tests
- Understand why string enums are used for JSON serialization
