"""Utility functions for AITEA."""

from typing import List, Tuple, Any, Dict, TypeVar, Type, Union
from pathlib import Path
import math
import re
import json


def calculate_mean(values: List[float]) -> float:
    """Calculate the arithmetic mean of a list of floats.
    
    Args:
        values: A non-empty list of float values.
        
    Returns:
        The arithmetic mean (sum of values divided by count).
        
    Raises:
        ValueError: If the list is empty.
    """
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)


def calculate_median(values: List[float]) -> float:
    """Calculate the median of a list of floats.
    
    Args:
        values: A non-empty list of float values.
        
    Returns:
        The median value. For even-length lists, returns the average
        of the two middle values.
        
    Raises:
        ValueError: If the list is empty.
    """
    if not values:
        raise ValueError("Cannot calculate median of empty list")
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    return sorted_values[mid]


def calculate_std_dev(values: List[float]) -> float:
    """Calculate the population standard deviation of a list of floats.
    
    Args:
        values: A non-empty list of float values.
        
    Returns:
        The population standard deviation (non-negative).
        
    Raises:
        ValueError: If the list is empty.
    """
    if not values:
        raise ValueError("Cannot calculate standard deviation of empty list")
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def calculate_p80(values: List[float]) -> float:
    """Calculate the 80th percentile (P80) of a list of floats.
    
    Uses linear interpolation between data points when the percentile
    falls between two values.
    
    Args:
        values: A non-empty list of float values.
        
    Returns:
        The 80th percentile value, which is >= median.
        
    Raises:
        ValueError: If the list is empty.
    """
    if not values:
        raise ValueError("Cannot calculate P80 of empty list")
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    # Use linear interpolation for percentile calculation
    # Position in the sorted array (0-indexed)
    position = 0.8 * (n - 1)
    lower_idx = int(position)
    upper_idx = lower_idx + 1
    
    if upper_idx >= n:
        return sorted_values[-1]
    
    # Linear interpolation
    fraction = position - lower_idx
    return sorted_values[lower_idx] + fraction * (sorted_values[upper_idx] - sorted_values[lower_idx])


def detect_outliers(values: List[float], threshold_std: float = 2.0) -> List[Tuple[int, float]]:
    """Detect outliers in a list of floats using standard deviation threshold.
    
    An outlier is defined as a value that exceeds the specified number of
    standard deviations from the mean.
    
    Args:
        values: A list of float values (at least 2 values needed for meaningful detection).
        threshold_std: Number of standard deviations from mean to consider as outlier.
                      Default is 2.0.
        
    Returns:
        A list of tuples (index, value) for each detected outlier.
        Returns empty list if fewer than 2 values provided.
    """
    if len(values) < 2:
        return []
    
    mean = calculate_mean(values)
    std_dev = calculate_std_dev(values)
    
    if std_dev == 0:
        return []  # All values are identical, no outliers
    
    outliers = []
    for idx, value in enumerate(values):
        if abs(value - mean) > threshold_std * std_dev:
            outliers.append((idx, value))
    
    return outliers


def normalize_text(text: str) -> str:
    """Normalize text for feature name matching.
    
    Performs the following normalizations:
    - Converts to lowercase
    - Replaces hyphens and underscores with spaces
    - Removes extra whitespace
    - Strips leading/trailing whitespace
    
    Args:
        text: The text to normalize.
        
    Returns:
        The normalized text string.
    """
    # Convert to lowercase
    result = text.lower()
    # Replace hyphens and underscores with spaces
    result = result.replace('-', ' ').replace('_', ' ')
    # Remove extra whitespace (multiple spaces become single space)
    result = re.sub(r'\s+', ' ', result)
    # Strip leading/trailing whitespace
    return result.strip()


def save_json(data: Any, path: Union[str, Path], indent: int = 2) -> None:
    """Save data to a JSON file.
    
    Serializes the provided data to JSON format and writes it to the specified
    file path. Creates parent directories if they don't exist.
    
    Args:
        data: The data to serialize. Can be a dict, list, or any JSON-serializable
              object. For dataclass instances, use their to_dict() method first.
        path: Path to the output JSON file (string or Path object).
        indent: Number of spaces for indentation (default: 2).
        
    Raises:
        TypeError: If the data is not JSON serializable.
        OSError: If the file cannot be written.
        
    Example:
        >>> feature_data = feature.to_dict()
        >>> save_json(feature_data, "data/features.json")
    """
    file_path = Path(path)
    
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(path: Union[str, Path]) -> Any:
    """Load data from a JSON file.
    
    Reads and parses a JSON file, returning the deserialized data.
    
    Args:
        path: Path to the JSON file to read (string or Path object).
        
    Returns:
        The deserialized JSON data (dict, list, or primitive types).
        
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        OSError: If the file cannot be read.
        
    Example:
        >>> data = load_json("data/features.json")
        >>> feature = Feature.from_dict(data)
    """
    file_path = Path(path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
