# Chapter 8: Error Handling & Validation

**Difficulty:** Intermediate  
**Time:** 1.5 hours  
**Prerequisites:** Chapters 1-7  
**AITEA Component:** `src/models/errors.py`, `src/models/result.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create structured error types for different failure scenarios
2. Implement the Result[T, E] pattern for explicit error handling
3. Use pattern matching with Result types
4. Chain operations that may fail
5. Understand when to use Result vs exceptions

## 8.1 The Problem with Exceptions

Exceptions hide error handling in the control flow:

```python
# ❌ Hidden error paths
def get_feature(feature_id: str) -> Feature:
    feature = db.query(feature_id)
    if feature is None:
        raise NotFoundError(f"Feature {feature_id} not found")
    return feature

# Caller might forget to handle the exception!
feature = get_feature("f123")  # 💥 Might raise!
```

**Problems:**

- Errors aren't visible in the function signature
- Easy to forget to handle exceptions
- Control flow is implicit

## 8.2 The Result Pattern

Make errors explicit in the return type:

```python
# ✅ Explicit error handling
def get_feature(feature_id: str) -> Result[Feature, NotFoundError]:
    feature = db.query(feature_id)
    if feature is None:
        return Result.err(NotFoundError("Feature", feature_id))
    return Result.ok(feature)

# Caller MUST handle both cases
result = get_feature("f123")
if result.is_ok():
    feature = result.unwrap()
else:
    error = result.unwrap_err()
```

## 8.3 Structured Error Types

Create specific error types for different scenarios:

```python
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ValidationError:
    """Error indicating invalid field data."""
    field: str
    message: str
    value: Any

    def __str__(self) -> str:
        return f"Validation error on '{self.field}': {self.message} (got: {self.value!r})"


@dataclass
class NotFoundError:
    """Error indicating a resource was not found."""
    resource_type: str
    identifier: str
    message: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.resource_type} with identifier '{self.identifier}' not found"
        return f"{base}: {self.message}" if self.message else base


@dataclass
class ImportError:
    """Error indicating a failure during data import."""
    row_number: int
    errors: List[ValidationError]
    source: Optional[str] = None

    def __str__(self) -> str:
        error_details = "; ".join(str(e) for e in self.errors)
        return f"Import error at row {self.row_number}: {error_details}"


@dataclass
class EstimationError:
    """Error indicating a failure during estimation."""
    feature_name: str
    reason: str
    details: Optional[Any] = None

    def __str__(self) -> str:
        base = f"Estimation error for '{self.feature_name}': {self.reason}"
        return f"{base} (details: {self.details!r})" if self.details else base
```

### Your Turn: Exercise 8.1

Create error instances and print them:

```python
# Create a ValidationError
val_err = ValidationError(
    field="seed_time_hours",
    message="must be positive",
    value=-5.0
)
print(val_err)
# Expected: Validation error on 'seed_time_hours': must be positive (got: -5.0)

# Create a NotFoundError
not_found = NotFoundError(
    resource_type="Feature",
    identifier="f999"
)
print(not_found)
# Expected: Feature with identifier 'f999' not found
```

## 8.4 Implementing the Result Type

The Result type is a discriminated union - it's either Ok or Err:

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Union, Callable

T = TypeVar('T')  # Success type
E = TypeVar('E')  # Error type


@dataclass(frozen=True)
class Ok(Generic[T]):
    """Represents a successful result."""
    _value: T

    @property
    def value(self) -> T:
        return self._value


@dataclass(frozen=True)
class Err(Generic[E]):
    """Represents an error result."""
    _error: E

    @property
    def error(self) -> E:
        return self._error


class UnwrapError(Exception):
    """Raised when unwrapping a Result in an invalid state."""
    pass


class Result(Generic[T, E]):
    """A discriminated union for success/error handling."""

    def __init__(self, inner: Union[Ok[T], Err[E]]) -> None:
        self._inner = inner

    @staticmethod
    def ok(value: T) -> 'Result[T, E]':
        """Create a successful Result."""
        return Result(Ok(value))

    @staticmethod
    def err(error: E) -> 'Result[T, E]':
        """Create an error Result."""
        return Result(Err(error))

    def is_ok(self) -> bool:
        """Check if this Result is a success."""
        return isinstance(self._inner, Ok)

    def is_err(self) -> bool:
        """Check if this Result is an error."""
        return isinstance(self._inner, Err)

    def unwrap(self) -> T:
        """Extract the success value. Raises if error."""
        if isinstance(self._inner, Ok):
            return self._inner.value
        raise UnwrapError(f"Called unwrap() on an Err: {self._inner.error}")

    def unwrap_err(self) -> E:
        """Extract the error value. Raises if success."""
        if isinstance(self._inner, Err):
            return self._inner.error
        raise UnwrapError(f"Called unwrap_err() on an Ok: {self._inner.value}")
```

## 8.5 Using Result in Practice

### Basic Usage

```python
def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Result.err("Division by zero")
    return Result.ok(a / b)

result = divide(10, 2)
if result.is_ok():
    print(f"Result: {result.unwrap()}")  # Result: 5.0
else:
    print(f"Error: {result.unwrap_err()}")

result = divide(10, 0)
if result.is_err():
    print(f"Error: {result.unwrap_err()}")  # Error: Division by zero
```

### Safe Defaults with unwrap_or

```python
def unwrap_or(self, default: T) -> T:
    """Extract value or return default."""
    if isinstance(self._inner, Ok):
        return self._inner.value
    return default

# Usage
result = divide(10, 0)
value = result.unwrap_or(0.0)  # Returns 0.0 instead of raising
```

### Chaining with and_then

```python
def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
    """Chain operations that may fail."""
    if isinstance(self._inner, Ok):
        return f(self._inner.value)
    return Result(self._inner)

# Usage: Chain multiple operations
def parse_int(s: str) -> Result[int, str]:
    try:
        return Result.ok(int(s))
    except ValueError:
        return Result.err(f"Cannot parse '{s}' as int")

def double(n: int) -> Result[int, str]:
    return Result.ok(n * 2)

result = parse_int("5").and_then(double)  # Result.ok(10)
result = parse_int("abc").and_then(double)  # Result.err("Cannot parse...")
```

### Your Turn: Exercise 8.2

Implement `map` for Result:

```python
def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
    """Transform the success value if present."""
    # TODO: If Ok, apply f to the value and return new Ok
    # TODO: If Err, return the same Err
    pass

# Test:
result = Result.ok(5).map(lambda x: x * 2)
assert result.unwrap() == 10

result = Result.err("error").map(lambda x: x * 2)
assert result.unwrap_err() == "error"
```

## 8.6 Result in AITEA Services

Here's how Result is used in the feature library:

```python
class FeatureLibraryService(IFeatureLibraryService):

    def add_feature(self, feature: Feature) -> Result[Feature, ValidationError]:
        # Check for duplicate
        if feature.id in self._features:
            return Result.err(ValidationError(
                field="id",
                message="Feature with this ID already exists",
                value=feature.id
            ))

        self._features[feature.id] = feature
        return Result.ok(feature)

    def get_feature(self, feature_id: str) -> Result[Feature, NotFoundError]:
        if feature_id not in self._features:
            return Result.err(NotFoundError(
                resource_type="Feature",
                identifier=feature_id
            ))

        return Result.ok(self._features[feature_id])
```

### Handling Results in Callers

```python
# Pattern 1: Check and unwrap
result = service.get_feature("f123")
if result.is_ok():
    feature = result.unwrap()
    print(f"Found: {feature.name}")
else:
    error = result.unwrap_err()
    print(f"Error: {error}")

# Pattern 2: Use unwrap_or for defaults
feature = service.get_feature("f123").unwrap_or(default_feature)

# Pattern 3: Chain operations
result = (
    service.get_feature("f123")
    .map(lambda f: f.seed_time_hours)
    .unwrap_or(0.0)
)
```

## 8.7 When to Use Result vs Exceptions

| Use Result                                | Use Exceptions                            |
| ----------------------------------------- | ----------------------------------------- |
| Expected failures (not found, validation) | Unexpected failures (bugs, system errors) |
| Caller should handle the error            | Error should propagate up                 |
| Error is part of the API contract         | Error is exceptional                      |
| Multiple error types possible             | Single error type                         |

```python
# Result: Expected failure
def get_feature(id: str) -> Result[Feature, NotFoundError]:
    ...

# Exception: Unexpected failure (bug)
def calculate_mean(values: List[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate mean of empty list")  # Bug in caller!
    ...
```

## 8.8 Debugging Scenario

**The Bug:** Forgetting to check Result before unwrapping.

```python
result = service.get_feature("nonexistent")
feature = result.unwrap()  # 💥 UnwrapError!
```

**The Fix:** Always check before unwrapping:

```python
result = service.get_feature("nonexistent")
if result.is_ok():
    feature = result.unwrap()
else:
    # Handle the error
    print(f"Feature not found: {result.unwrap_err()}")
```

Or use `unwrap_or`:

```python
feature = service.get_feature("nonexistent").unwrap_or(None)
if feature:
    # Use feature
```

## 8.9 Quick Check Questions

1. What's the main advantage of Result over exceptions?
2. What does `unwrap()` do if called on an Err?
3. When should you use `unwrap_or()`?
4. What does `and_then()` do?
5. Why are error types dataclasses?

<details>
<summary>Answers</summary>

1. Errors are explicit in the function signature
2. Raises `UnwrapError`
3. When you have a sensible default value
4. Chains operations that may fail, short-circuiting on first error
5. For automatic `__init__`, `__repr__`, `__eq__`, and structured data

</details>

## 8.10 Mini-Project: Validation Pipeline

Create a validation pipeline using Result:

```python
def validate_feature_name(name: str) -> Result[str, ValidationError]:
    """Validate feature name is not empty and not too long."""
    if not name or not name.strip():
        return Result.err(ValidationError("name", "cannot be empty", name))
    if len(name) > 100:
        return Result.err(ValidationError("name", "too long (max 100)", name))
    return Result.ok(name.strip())


def validate_seed_time(hours: float) -> Result[float, ValidationError]:
    """Validate seed time is positive and reasonable."""
    if hours <= 0:
        return Result.err(ValidationError("seed_time_hours", "must be positive", hours))
    if hours > 1000:
        return Result.err(ValidationError("seed_time_hours", "unreasonably large", hours))
    return Result.ok(hours)


def validate_feature_input(
    name: str,
    seed_time: float
) -> Result[tuple, ValidationError]:
    """Validate all feature inputs."""
    name_result = validate_feature_name(name)
    if name_result.is_err():
        return Result.err(name_result.unwrap_err())

    time_result = validate_seed_time(seed_time)
    if time_result.is_err():
        return Result.err(time_result.unwrap_err())

    return Result.ok((name_result.unwrap(), time_result.unwrap()))


# Test it:
result = validate_feature_input("CRUD API", 4.0)
assert result.is_ok()
print(f"Valid: {result.unwrap()}")

result = validate_feature_input("", 4.0)
assert result.is_err()
print(f"Error: {result.unwrap_err()}")

result = validate_feature_input("CRUD", -5.0)
assert result.is_err()
print(f"Error: {result.unwrap_err()}")
```

## 8.11 AITEA Integration

This chapter implements:

- **Requirement 1.8**: ValidationError types and Result[T, E] pattern
- **Requirement 8.5**: JSON validation error specificity
- **Property 3**: Service Result Pattern Consistency
- **Property 17**: JSON Validation Error Specificity

**Verification:**

```bash
# Run the property tests
python -m pytest tests/properties/test_model_props.py -k "result" -v

# Type check
mypy src/models/errors.py src/models/result.py
```

## What's Next

Phase 1 is complete! In Chapter 9, we'll start Phase 2: CLI Development. You'll learn:

- Building CLI applications with Typer
- Creating beautiful terminal output with Rich
- Connecting the CLI to our services

**Before proceeding:**

- Ensure you understand when to use Result vs exceptions
- Practice chaining Result operations
- Review all Phase 1 implementations
