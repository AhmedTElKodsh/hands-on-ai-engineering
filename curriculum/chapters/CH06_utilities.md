# Chapter 6: Utility Functions

**Difficulty:** Beginner  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-5  
**AITEA Component:** `src/utils/__init__.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Implement statistical functions (mean, median, std_dev, P80)
2. Create outlier detection using standard deviation
3. Build text normalization for flexible matching
4. Implement JSON file persistence utilities
5. Write pure functions with proper error handling

## 6.1 Why Utility Functions?

Utility functions are pure, reusable building blocks:

- **Pure**: Same input always produces same output
- **Reusable**: Used across multiple services
- **Testable**: Easy to test in isolation
- **Focused**: Each function does one thing well

## 6.2 Statistical Functions

### Calculate Mean

The arithmetic mean (average) is the sum divided by count:

```python
def calculate_mean(values: List[float]) -> float:
    """Calculate the arithmetic mean of a list of floats.

    Args:
        values: A non-empty list of float values.

    Returns:
        The arithmetic mean (sum of values divided by count).

    Raises:
        ValueError: If the list is empty.

    Example:
        >>> calculate_mean([4.0, 5.0, 6.0])
        5.0
    """
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)
```

### Calculate Median

The median is the middle value when sorted:

```python
def calculate_median(values: List[float]) -> float:
    """Calculate the median of a list of floats.

    For even-length lists, returns the average of the two middle values.

    Args:
        values: A non-empty list of float values.

    Returns:
        The median value.

    Raises:
        ValueError: If the list is empty.

    Example:
        >>> calculate_median([1.0, 3.0, 5.0])
        3.0
        >>> calculate_median([1.0, 2.0, 3.0, 4.0])
        2.5
    """
    if not values:
        raise ValueError("Cannot calculate median of empty list")

    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2

    if n % 2 == 0:
        # Even: average of two middle values
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    else:
        # Odd: middle value
        return sorted_values[mid]
```

### Your Turn: Exercise 6.1

Trace through `calculate_median` for these inputs:

```python
# Input 1: [3.0, 1.0, 2.0]
# sorted: [1.0, 2.0, 3.0]
# n = 3, mid = 1
# n % 2 = 1 (odd)
# Result: sorted_values[1] = ???

# Input 2: [4.0, 1.0, 3.0, 2.0]
# sorted: [1.0, 2.0, 3.0, 4.0]
# n = 4, mid = 2
# n % 2 = 0 (even)
# Result: (sorted_values[1] + sorted_values[2]) / 2 = ???
```

### Calculate Standard Deviation

Standard deviation measures how spread out values are:

```python
import math

def calculate_std_dev(values: List[float]) -> float:
    """Calculate the population standard deviation.

    Args:
        values: A non-empty list of float values.

    Returns:
        The population standard deviation (non-negative).

    Raises:
        ValueError: If the list is empty.

    Example:
        >>> calculate_std_dev([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        2.0
    """
    if not values:
        raise ValueError("Cannot calculate standard deviation of empty list")

    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)
```

**The formula:**

1. Calculate the mean
2. For each value, compute (value - mean)²
3. Average those squared differences (variance)
4. Take the square root

### Calculate P80 (80th Percentile)

P80 means 80% of values are at or below this point:

```python
def calculate_p80(values: List[float]) -> float:
    """Calculate the 80th percentile (P80).

    Uses linear interpolation between data points.

    Args:
        values: A non-empty list of float values.

    Returns:
        The 80th percentile value (>= median).

    Raises:
        ValueError: If the list is empty.

    Example:
        >>> calculate_p80([1.0, 2.0, 3.0, 4.0, 5.0])
        4.2
    """
    if not values:
        raise ValueError("Cannot calculate P80 of empty list")

    sorted_values = sorted(values)
    n = len(sorted_values)

    # Position in the sorted array (0-indexed)
    position = 0.8 * (n - 1)
    lower_idx = int(position)
    upper_idx = lower_idx + 1

    if upper_idx >= n:
        return sorted_values[-1]

    # Linear interpolation
    fraction = position - lower_idx
    return sorted_values[lower_idx] + fraction * (sorted_values[upper_idx] - sorted_values[lower_idx])
```

**Why P80 for estimates?**

- Mean can be skewed by outliers
- Median might be too optimistic
- P80 is conservative but realistic - 80% of the time, actual work takes this long or less

### Your Turn: Exercise 6.2

Calculate P80 for `[2.0, 4.0, 6.0, 8.0, 10.0]`:

```python
# n = 5
# position = 0.8 * (5 - 1) = 3.2
# lower_idx = 3, upper_idx = 4
# fraction = 3.2 - 3 = 0.2
# sorted_values[3] = 8.0
# sorted_values[4] = 10.0
# Result = 8.0 + 0.2 * (10.0 - 8.0) = ???
```

## 6.3 Outlier Detection

Outliers are values that are unusually far from the mean:

```python
from typing import Tuple

def detect_outliers(
    values: List[float],
    threshold_std: float = 2.0
) -> List[Tuple[int, float]]:
    """Detect outliers using standard deviation threshold.

    An outlier exceeds threshold_std standard deviations from the mean.

    Args:
        values: List of float values (need at least 2 for meaningful detection).
        threshold_std: Number of standard deviations for outlier threshold.

    Returns:
        List of (index, value) tuples for each outlier.

    Example:
        >>> detect_outliers([4.0, 4.5, 5.0, 4.8, 50.0])  # 50.0 is an outlier
        [(4, 50.0)]
    """
    if len(values) < 2:
        return []

    mean = calculate_mean(values)
    std_dev = calculate_std_dev(values)

    if std_dev == 0:
        return []  # All values identical

    outliers = []
    for idx, value in enumerate(values):
        if abs(value - mean) > threshold_std * std_dev:
            outliers.append((idx, value))

    return outliers
```

**Example:**

```python
times = [4.0, 4.5, 5.0, 4.8, 50.0]  # Someone logged 50 hours for a 4-hour task!
outliers = detect_outliers(times)
print(outliers)  # [(4, 50.0)]
```

## 6.4 Text Normalization

For flexible feature matching, normalize text:

```python
import re

def normalize_text(text: str) -> str:
    """Normalize text for feature name matching.

    Performs:
    - Lowercase conversion
    - Replace hyphens and underscores with spaces
    - Remove extra whitespace
    - Strip leading/trailing whitespace

    Args:
        text: The text to normalize.

    Returns:
        The normalized text string.

    Example:
        >>> normalize_text("CRUD-API")
        'crud api'
        >>> normalize_text("  User_Authentication  ")
        'user authentication'
    """
    result = text.lower()
    result = result.replace('-', ' ').replace('_', ' ')
    result = re.sub(r'\s+', ' ', result)
    return result.strip()
```

**Why normalize?**

```python
# All of these should match the same feature:
normalize_text("CRUD")           # "crud"
normalize_text("crud-api")       # "crud api"
normalize_text("CRUD_API")       # "crud api"
normalize_text("  crud   api ")  # "crud api"
```

## 6.5 JSON Persistence

For saving and loading data:

```python
from pathlib import Path
from typing import Any, Union
import json

def save_json(data: Any, path: Union[str, Path], indent: int = 2) -> None:
    """Save data to a JSON file.

    Creates parent directories if they don't exist.

    Args:
        data: JSON-serializable data (dict, list, etc.)
        path: Output file path
        indent: Indentation spaces (default: 2)

    Raises:
        TypeError: If data is not JSON serializable
        OSError: If file cannot be written

    Example:
        >>> save_json({"name": "CRUD", "hours": 4.0}, "data/feature.json")
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(path: Union[str, Path]) -> Any:
    """Load data from a JSON file.

    Args:
        path: Path to JSON file

    Returns:
        Deserialized JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If invalid JSON

    Example:
        >>> data = load_json("data/feature.json")
        >>> print(data["name"])
        'CRUD'
    """
    file_path = Path(path)

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Your Turn: Exercise 6.3

Use the JSON utilities with a Feature:

```python
from models import Feature, TeamType

# Create a feature
feature = Feature(
    id="f1",
    name="Authentication",
    team=TeamType.BACKEND,
    process="Auth",
    seed_time_hours=8.0,
    synonyms=["auth", "login"]
)

# Save to JSON
save_json(feature.to_dict(), "data/auth_feature.json")

# Load back
data = load_json("data/auth_feature.json")
loaded_feature = Feature.from_dict(data)

# Verify round-trip
assert loaded_feature == feature
print("✅ JSON round-trip successful!")
```

## 6.6 Complete Implementation

Here's the complete `src/utils/__init__.py`:

```python
"""Utility functions for AITEA."""

from typing import List, Tuple, Any, Union
from pathlib import Path
import math
import re
import json


def calculate_mean(values: List[float]) -> float:
    """Calculate the arithmetic mean of a list of floats."""
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)


def calculate_median(values: List[float]) -> float:
    """Calculate the median of a list of floats."""
    if not values:
        raise ValueError("Cannot calculate median of empty list")
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    return sorted_values[mid]


def calculate_std_dev(values: List[float]) -> float:
    """Calculate the population standard deviation."""
    if not values:
        raise ValueError("Cannot calculate standard deviation of empty list")
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def calculate_p80(values: List[float]) -> float:
    """Calculate the 80th percentile (P80)."""
    if not values:
        raise ValueError("Cannot calculate P80 of empty list")
    sorted_values = sorted(values)
    n = len(sorted_values)
    position = 0.8 * (n - 1)
    lower_idx = int(position)
    upper_idx = lower_idx + 1
    if upper_idx >= n:
        return sorted_values[-1]
    fraction = position - lower_idx
    return sorted_values[lower_idx] + fraction * (sorted_values[upper_idx] - sorted_values[lower_idx])


def detect_outliers(values: List[float], threshold_std: float = 2.0) -> List[Tuple[int, float]]:
    """Detect outliers using standard deviation threshold."""
    if len(values) < 2:
        return []
    mean = calculate_mean(values)
    std_dev = calculate_std_dev(values)
    if std_dev == 0:
        return []
    outliers = []
    for idx, value in enumerate(values):
        if abs(value - mean) > threshold_std * std_dev:
            outliers.append((idx, value))
    return outliers


def normalize_text(text: str) -> str:
    """Normalize text for feature name matching."""
    result = text.lower()
    result = result.replace('-', ' ').replace('_', ' ')
    result = re.sub(r'\s+', ' ', result)
    return result.strip()


def save_json(data: Any, path: Union[str, Path], indent: int = 2) -> None:
    """Save data to a JSON file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(path: Union[str, Path]) -> Any:
    """Load data from a JSON file."""
    file_path = Path(path)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

## 6.7 Debugging Scenario

**The Bug:** P80 calculation returns wrong value for single-element list.

```python
values = [5.0]
result = calculate_p80(values)
# Expected: 5.0
# Got: IndexError or wrong value
```

**The Problem:** Edge case not handled properly.

**The Fix:** Check if `upper_idx >= n`:

```python
if upper_idx >= n:
    return sorted_values[-1]  # Return the last (only) value
```

## 6.8 Quick Check Questions

1. What's the difference between mean and median?
2. Why use P80 instead of mean for estimates?
3. What does a standard deviation of 0 mean?
4. Why normalize text before searching?
5. What does `ensure_ascii=False` do in `json.dump`?

<details>
<summary>Answers</summary>

1. Mean is the average; median is the middle value when sorted
2. P80 is more conservative and less affected by outliers
3. All values are identical
4. To match regardless of case, hyphens, underscores, or spacing
5. Allows non-ASCII characters (like é, ñ) to be written directly

</details>

## 6.9 Mini-Project: Statistics Report

Create a function that generates a statistics report:

```python
def generate_stats_report(values: List[float], name: str = "Data") -> str:
    """Generate a formatted statistics report.

    Args:
        values: List of numeric values
        name: Name for the report header

    Returns:
        Formatted report string
    """
    if not values:
        return f"{name}: No data available"

    mean = calculate_mean(values)
    median = calculate_median(values)
    std_dev = calculate_std_dev(values)
    p80 = calculate_p80(values)
    outliers = detect_outliers(values)

    report = f"""
{name} Statistics Report
{'=' * (len(name) + 19)}
Count:     {len(values)}
Mean:      {mean:.2f}
Median:    {median:.2f}
Std Dev:   {std_dev:.2f}
P80:       {p80:.2f}
Outliers:  {len(outliers)} detected
"""

    if outliers:
        report += "\nOutlier values:\n"
        for idx, val in outliers:
            report += f"  - Index {idx}: {val:.2f}\n"

    return report.strip()


# Test it:
times = [4.0, 4.5, 5.0, 4.8, 4.2, 50.0, 4.7, 5.2]
print(generate_stats_report(times, "CRUD Feature"))
```

**Expected output:**

```
CRUD Feature Statistics Report
==============================
Count:     8
Mean:      10.30
Median:    4.75
Std Dev:   15.23
P80:       5.08
Outliers:  1 detected

Outlier values:
  - Index 5: 50.00
```

## 6.10 AITEA Integration

This chapter implements:

- **Requirement 1.6**: Statistics calculation utilities
- **Requirement 9.1**: Mean, median, std_dev, P80 computation
- **Requirement 9.3**: Outlier detection
- **Property 4**: Statistics Mathematical Correctness
- **Property 19**: Outlier Detection Accuracy

**Verification:**

```bash
# Run the property tests
python -m pytest tests/properties/test_model_props.py -k "statistics or outlier" -v

# Type check
mypy src/utils/__init__.py
```

## What's Next

In Chapter 7, we'll learn property-based testing with Hypothesis. You'll learn:

- How to generate random test data
- Writing properties instead of examples
- Custom strategies for domain objects

**Before proceeding:**

- Ensure all statistical functions handle edge cases
- Test with various input sizes
- Understand the mathematical formulas
