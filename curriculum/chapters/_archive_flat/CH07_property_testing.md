# Chapter 7: Property-Based Testing

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-6  
**AITEA Component:** `tests/properties/`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Understand the difference between example-based and property-based testing
2. Write property tests using Hypothesis
3. Create custom strategies for domain objects
4. Use shrinking to find minimal failing examples
5. Apply property testing to AITEA models and services

## 7.1 The Limits of Example-Based Testing

Traditional tests check specific examples:

```python
def test_calculate_mean():
    assert calculate_mean([1.0, 2.0, 3.0]) == 2.0
    assert calculate_mean([10.0]) == 10.0
    assert calculate_mean([0.0, 100.0]) == 50.0
```

**Problems:**

- You might miss edge cases
- Tests only cover examples you thought of
- Tedious to write many examples

## 7.2 Property-Based Testing

Instead of examples, describe **properties** that should always hold:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=0.1, max_value=1000.0), min_size=1))
def test_mean_is_between_min_and_max(values):
    """Mean should always be between min and max values."""
    result = calculate_mean(values)
    assert min(values) <= result <= max(values)
```

Hypothesis generates hundreds of random inputs and checks the property holds for all of them!

## 7.3 Getting Started with Hypothesis

Install Hypothesis:

```bash
pip install hypothesis
```

Basic structure:

```python
from hypothesis import given, settings, strategies as st

@given(st.integers())  # Generate random integers
def test_something(x):
    # x is a random integer
    assert some_property(x)
```

### Common Strategies

```python
# Basic types
st.integers()                    # Any integer
st.integers(min_value=0)         # Non-negative integers
st.floats(min_value=0.1)         # Positive floats
st.text()                        # Any string
st.booleans()                    # True or False

# Collections
st.lists(st.integers())          # List of integers
st.lists(st.integers(), min_size=1)  # Non-empty list
st.dictionaries(st.text(), st.integers())  # Dict[str, int]

# Choices
st.sampled_from([1, 2, 3])       # One of these values
st.sampled_from(TeamType)        # One enum member
```

### Your Turn: Exercise 7.1

Write a property test for `calculate_median`:

```python
@given(st.lists(st.floats(min_value=0.1, max_value=1000.0), min_size=1))
def test_median_is_in_sorted_list(values):
    """Median should be a value that exists in the sorted list (for odd length)
    or between two values (for even length)."""
    result = calculate_median(values)
    sorted_values = sorted(values)
    # TODO: Assert that result is >= min and <= max
    pass
```

## 7.4 Properties for Statistics

### Property: Mean equals sum divided by count

```python
@given(st.lists(st.floats(min_value=0.1, max_value=1000.0), min_size=1))
def test_mean_equals_sum_over_count(values):
    """
    **Property 4: Statistics Mathematical Correctness**
    Mean SHALL equal sum of values divided by count.
    """
    result = calculate_mean(values)
    expected = sum(values) / len(values)
    assert abs(result - expected) < 1e-10  # Float comparison tolerance
```

### Property: P80 >= Median

```python
@given(st.lists(st.floats(min_value=0.1, max_value=1000.0), min_size=1))
def test_p80_greater_than_or_equal_to_median(values):
    """
    **Property 4: Statistics Mathematical Correctness**
    P80 SHALL be greater than or equal to median.
    """
    p80 = calculate_p80(values)
    median = calculate_median(values)
    assert p80 >= median - 1e-10  # Allow tiny float errors
```

### Property: Standard deviation is non-negative

```python
@given(st.lists(st.floats(min_value=0.1, max_value=1000.0), min_size=1))
def test_std_dev_non_negative(values):
    """Standard deviation SHALL be non-negative."""
    result = calculate_std_dev(values)
    assert result >= 0
```

## 7.5 Custom Strategies for Domain Objects

Create strategies for AITEA models:

```python
from hypothesis import strategies as st
from models import Feature, TeamType, TrackedTimeEntry
from datetime import date

# Strategy for TeamType enum
team_type_strategy = st.sampled_from(list(TeamType))

# Strategy for Feature
feature_strategy = st.builds(
    Feature,
    id=st.text(min_size=1, max_size=20).filter(lambda x: x.strip()),
    name=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
    team=team_type_strategy,
    process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    seed_time_hours=st.floats(min_value=0.5, max_value=200.0),
    synonyms=st.lists(st.text(min_size=1, max_size=50), max_size=10),
    notes=st.text(max_size=500)
)

# Strategy for TrackedTimeEntry
tracked_time_strategy = st.builds(
    TrackedTimeEntry,
    id=st.text(min_size=1, max_size=20).filter(lambda x: x.strip()),
    team=team_type_strategy,
    member_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    feature=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
    tracked_time_hours=st.floats(min_value=0.1, max_value=100.0),
    process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    date=st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))
)
```

### Using Custom Strategies

```python
@given(feature_strategy)
def test_feature_instantiation_validity(feature):
    """
    **Property 2: Dataclass Instantiation Validity**
    For any valid combination of field values, the dataclass
    SHALL instantiate without error.
    """
    # If we get here, instantiation succeeded
    assert feature.id
    assert feature.name
    assert feature.seed_time_hours > 0
```

## 7.6 Testing Serialization Round-Trips

A key property: serializing and deserializing should produce equivalent objects.

```python
@given(feature_strategy)
def test_feature_serialization_round_trip(feature):
    """
    **Property 5: Model Serialization Round-Trip**
    Serializing to JSON and deserializing back SHALL produce
    an equivalent instance.
    """
    # Serialize
    data = feature.to_dict()

    # Deserialize
    loaded = Feature.from_dict(data)

    # Should be equivalent
    assert loaded.id == feature.id
    assert loaded.name == feature.name
    assert loaded.team == feature.team
    assert loaded.seed_time_hours == feature.seed_time_hours
    assert loaded.synonyms == feature.synonyms
```

## 7.7 Testing Enum Properties

```python
class TestEnumProperties:
    """Property tests for AITEA enumerations."""

    @given(st.sampled_from(list(TeamType)))
    def test_team_type_string_inheritance(self, team: TeamType):
        """
        **Property 1: Enum Completeness and Type Safety**
        TeamType members SHALL be usable as strings.
        """
        # Should work as a string
        assert isinstance(team, str)
        assert team == team.value

        # Should be JSON serializable
        import json
        json.dumps({"team": team})  # Should not raise

    @given(st.sampled_from(list(ConfidenceLevel)))
    def test_confidence_level_ordering(self, level: ConfidenceLevel):
        """Confidence levels should have a logical ordering."""
        levels = [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
        assert level in levels
```

## 7.8 Shrinking: Finding Minimal Examples

When Hypothesis finds a failing case, it **shrinks** to find the simplest example:

```python
@given(st.lists(st.integers(), min_size=1))
def test_always_positive(values):
    """This will fail for negative values."""
    assert all(v > 0 for v in values)

# Hypothesis might first find: [-847, 293, -12, 0, 55]
# Then shrinks to: [-1]  # Minimal failing example!
```

This makes debugging much easier!

## 7.9 Settings and Configuration

Control test behavior with `@settings`:

```python
from hypothesis import settings, Verbosity

@settings(max_examples=100)  # Run 100 random examples
@given(st.integers())
def test_with_many_examples(x):
    pass

@settings(max_examples=1000, deadline=None)  # More thorough, no time limit
@given(feature_strategy)
def test_thorough_feature_testing(feature):
    pass

# For debugging
@settings(verbosity=Verbosity.verbose)
@given(st.integers())
def test_verbose(x):
    pass
```

## 7.10 Complete Test File

Here's a complete property test file:

```python
"""Property-based tests for AITEA models."""

from datetime import date
from hypothesis import given, settings, strategies as st
import pytest

from models import Feature, TrackedTimeEntry, TeamType, ConfidenceLevel
from utils import calculate_mean, calculate_median, calculate_std_dev, calculate_p80


# Custom strategies
team_strategy = st.sampled_from(list(TeamType))

feature_strategy = st.builds(
    Feature,
    id=st.text(min_size=1, max_size=20).filter(lambda x: x.strip()),
    name=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
    team=team_strategy,
    process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    seed_time_hours=st.floats(min_value=0.5, max_value=200.0),
    synonyms=st.lists(st.text(max_size=50), max_size=5),
    notes=st.text(max_size=200)
)

positive_floats = st.floats(min_value=0.1, max_value=1000.0)
float_list = st.lists(positive_floats, min_size=1, max_size=100)


class TestStatisticsProperties:
    """Property tests for statistical functions."""

    @settings(max_examples=100)
    @given(float_list)
    def test_mean_between_min_and_max(self, values):
        """Mean is always between min and max."""
        result = calculate_mean(values)
        assert min(values) <= result <= max(values)

    @settings(max_examples=100)
    @given(float_list)
    def test_p80_gte_median(self, values):
        """P80 is always >= median."""
        p80 = calculate_p80(values)
        median = calculate_median(values)
        assert p80 >= median - 1e-10

    @settings(max_examples=100)
    @given(float_list)
    def test_std_dev_non_negative(self, values):
        """Standard deviation is never negative."""
        result = calculate_std_dev(values)
        assert result >= 0


class TestFeatureProperties:
    """Property tests for Feature model."""

    @settings(max_examples=100)
    @given(feature_strategy)
    def test_feature_instantiation(self, feature):
        """Features instantiate with valid data."""
        assert feature.id
        assert feature.name
        assert feature.seed_time_hours > 0

    @settings(max_examples=100)
    @given(feature_strategy)
    def test_feature_round_trip(self, feature):
        """Serialization round-trip preserves data."""
        data = feature.to_dict()
        loaded = Feature.from_dict(data)
        assert loaded.id == feature.id
        assert loaded.name == feature.name
        assert loaded.team == feature.team
```

## 7.11 Debugging Scenario

**The Bug:** Property test fails with a cryptic error.

```
Falsifying example: test_feature_round_trip(
    feature=Feature(id='', name='Test', ...)
)
```

**The Problem:** The strategy generated an empty string for `id`, which fails validation.

**The Fix:** Filter out invalid values in the strategy:

```python
# Before
id=st.text(max_size=20)  # Can generate empty string!

# After
id=st.text(min_size=1, max_size=20).filter(lambda x: x.strip())
```

## 7.12 Quick Check Questions

1. What's the main advantage of property-based testing?
2. What does "shrinking" do?
3. How do you create a strategy for an enum?
4. What does `@settings(max_examples=100)` do?
5. Why use `.filter()` on strategies?

<details>
<summary>Answers</summary>

1. Tests many random inputs automatically, finding edge cases you didn't think of
2. Finds the simplest failing example for easier debugging
3. `st.sampled_from(list(MyEnum))`
4. Runs 100 random test cases instead of the default
5. To exclude invalid values that would fail validation

</details>

## 7.13 Mini-Project: Comprehensive Property Tests

Add property tests for the estimation service:

```python
class TestEstimationProperties:
    """Property tests for estimation logic."""

    @given(st.integers(min_value=0, max_value=2))
    def test_low_confidence_threshold(self, count):
        """0-2 data points should give LOW confidence."""
        service = EstimationService(...)
        confidence = service._get_confidence_level(count)
        assert confidence == ConfidenceLevel.LOW

    @given(st.integers(min_value=3, max_value=9))
    def test_medium_confidence_threshold(self, count):
        """3-9 data points should give MEDIUM confidence."""
        service = EstimationService(...)
        confidence = service._get_confidence_level(count)
        assert confidence == ConfidenceLevel.MEDIUM

    @given(st.integers(min_value=10, max_value=1000))
    def test_high_confidence_threshold(self, count):
        """10+ data points should give HIGH confidence."""
        service = EstimationService(...)
        confidence = service._get_confidence_level(count)
        assert confidence == ConfidenceLevel.HIGH
```

## 7.14 AITEA Integration

This chapter implements:

- **Requirement 1.7**: Property-based tests using Hypothesis
- **Property 1-5**: Core model and statistics properties

**Verification:**

```bash
# Run all property tests
python -m pytest tests/properties/ -v

# Run with verbose Hypothesis output
python -m pytest tests/properties/ -v --hypothesis-show-statistics
```

## What's Next

In Chapter 8, we'll implement error handling with the Result type pattern. You'll learn:

- Creating custom error types
- The Result[T, E] pattern
- Explicit error handling without exceptions

**Before proceeding:**

- Write at least 5 property tests
- Understand how shrinking works
- Create custom strategies for your domain objects
