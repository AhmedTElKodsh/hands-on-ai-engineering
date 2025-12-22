"""LangSmith dataset management utilities.

This module provides functions for creating and managing datasets
in LangSmith for evaluation and testing.
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict, List
import warnings

try:
    from langsmith import Client
    from langsmith.schemas import Dataset, Example
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    warnings.warn(
        "LangSmith not installed. Install with: pip install langsmith\n"
        "Dataset management will be disabled.",
        ImportWarning
    )

from .tracing import get_client, is_tracing_enabled


@dataclass
class DatasetExample:
    """Example for a LangSmith dataset.
    
    Attributes:
        inputs: Input data for the example
        outputs: Expected output data
        metadata: Additional metadata for the example
    """
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


def create_dataset(
    name: str,
    description: Optional[str] = None,
    examples: Optional[List[DatasetExample]] = None,
) -> Optional[str]:
    """Create a new dataset in LangSmith.
    
    Args:
        name: Name of the dataset
        description: Description of the dataset
        examples: Initial examples to add to the dataset
    
    Returns:
        Dataset ID if successful, None otherwise
    
    Example:
        >>> examples = [
        ...     DatasetExample(
        ...         inputs={"brd_text": "Build a login feature"},
        ...         outputs={"features": ["authentication", "login-ui"]},
        ...     ),
        ... ]
        >>> dataset_id = create_dataset(
        ...     name="feature_extraction_test",
        ...     description="Test cases for feature extraction",
        ...     examples=examples,
        ... )
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - cannot create dataset")
        return None
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    try:
        # Create dataset
        dataset = client.create_dataset(
            dataset_name=name,
            description=description or f"Dataset: {name}",
        )
        
        print(f"✅ Created dataset: {name} (ID: {dataset.id})")
        
        # Add examples if provided
        if examples:
            add_examples(name, examples)
        
        return str(dataset.id)
    
    except Exception as e:
        warnings.warn(f"Failed to create dataset: {e}")
        return None


def add_examples(
    dataset_name: str,
    examples: List[DatasetExample],
) -> int:
    """Add examples to an existing dataset.
    
    Args:
        dataset_name: Name of the dataset
        examples: Examples to add
    
    Returns:
        Number of examples successfully added
    
    Example:
        >>> examples = [
        ...     DatasetExample(
        ...         inputs={"feature": "CRUD"},
        ...         outputs={"hours": 4.0, "confidence": "high"},
        ...     ),
        ... ]
        >>> count = add_examples("estimation_test", examples)
        >>> print(f"Added {count} examples")
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - cannot add examples")
        return 0
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    try:
        # Get dataset
        dataset = client.read_dataset(dataset_name=dataset_name)
        
        # Add examples
        added = 0
        for example in examples:
            client.create_example(
                inputs=example.inputs,
                outputs=example.outputs,
                metadata=example.metadata,
                dataset_id=dataset.id,
            )
            added += 1
        
        print(f"✅ Added {added} examples to dataset: {dataset_name}")
        return added
    
    except Exception as e:
        warnings.warn(f"Failed to add examples: {e}")
        return 0


def get_dataset(dataset_name: str) -> Optional[Any]:
    """Get a dataset from LangSmith.
    
    Args:
        dataset_name: Name of the dataset
    
    Returns:
        Dataset object if found, None otherwise
    
    Example:
        >>> dataset = get_dataset("feature_extraction_test")
        >>> if dataset:
        ...     print(f"Dataset has {len(dataset.examples)} examples")
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - cannot get dataset")
        return None
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    try:
        return client.read_dataset(dataset_name=dataset_name)
    except Exception as e:
        warnings.warn(f"Failed to get dataset: {e}")
        return None


def list_datasets() -> List[str]:
    """List all datasets in the current LangSmith project.
    
    Returns:
        List of dataset names
    
    Example:
        >>> datasets = list_datasets()
        >>> for name in datasets:
        ...     print(f"- {name}")
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - cannot list datasets")
        return []
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    try:
        datasets = client.list_datasets()
        return [dataset.name for dataset in datasets]
    except Exception as e:
        warnings.warn(f"Failed to list datasets: {e}")
        return []


def delete_dataset(dataset_name: str) -> bool:
    """Delete a dataset from LangSmith.
    
    Args:
        dataset_name: Name of the dataset to delete
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> success = delete_dataset("old_test_dataset")
        >>> if success:
        ...     print("Dataset deleted")
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - cannot delete dataset")
        return False
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        client.delete_dataset(dataset_id=dataset.id)
        print(f"✅ Deleted dataset: {dataset_name}")
        return True
    except Exception as e:
        warnings.warn(f"Failed to delete dataset: {e}")
        return False


# Predefined dataset creators for AITEA

def create_feature_extraction_dataset() -> Optional[str]:
    """Create a sample dataset for feature extraction evaluation.
    
    Returns:
        Dataset ID if successful
    """
    examples = [
        DatasetExample(
            inputs={"brd_text": "Build a user authentication system with login and registration"},
            outputs={
                "features": ["authentication", "login", "registration"],
                "feature_count": 3,
            },
            metadata={"category": "authentication"},
        ),
        DatasetExample(
            inputs={"brd_text": "Create a CRUD API for managing products with search functionality"},
            outputs={
                "features": ["CRUD", "search", "api"],
                "feature_count": 3,
            },
            metadata={"category": "data_operations"},
        ),
        DatasetExample(
            inputs={"brd_text": "Implement real-time chat with WebSocket support and message history"},
            outputs={
                "features": ["websocket", "chat", "message-history"],
                "feature_count": 3,
            },
            metadata={"category": "real_time"},
        ),
    ]
    
    return create_dataset(
        name="feature_extraction_test",
        description="Test cases for BRD feature extraction",
        examples=examples,
    )


def create_estimation_dataset() -> Optional[str]:
    """Create a sample dataset for estimation evaluation.
    
    Returns:
        Dataset ID if successful
    """
    examples = [
        DatasetExample(
            inputs={"feature": "CRUD", "team": "backend"},
            outputs={
                "hours": 4.0,
                "confidence": "high",
            },
            metadata={"process": "Data Operations"},
        ),
        DatasetExample(
            inputs={"feature": "authentication", "team": "backend"},
            outputs={
                "hours": 8.0,
                "confidence": "medium",
            },
            metadata={"process": "Authentication"},
        ),
        DatasetExample(
            inputs={"feature": "websocket", "team": "backend"},
            outputs={
                "hours": 12.0,
                "confidence": "medium",
            },
            metadata={"process": "Real-time"},
        ),
    ]
    
    return create_dataset(
        name="estimation_test",
        description="Test cases for feature estimation",
        examples=examples,
    )


def create_brd_parsing_dataset() -> Optional[str]:
    """Create a sample dataset for BRD parsing evaluation.
    
    Returns:
        Dataset ID if successful
    """
    examples = [
        DatasetExample(
            inputs={
                "brd_text": """
                Project: E-commerce Platform
                
                Features:
                1. User authentication with OAuth
                2. Product catalog with search
                3. Shopping cart functionality
                4. Payment processing with Stripe
                5. Order history and tracking
                """
            },
            outputs={
                "features": [
                    {"name": "authentication", "team": "backend", "hours": 8.0},
                    {"name": "search", "team": "backend", "hours": 6.0},
                    {"name": "cart", "team": "fullstack", "hours": 10.0},
                    {"name": "payment", "team": "backend", "hours": 12.0},
                    {"name": "order-tracking", "team": "fullstack", "hours": 8.0},
                ],
                "total_hours": 44.0,
            },
            metadata={"project_type": "ecommerce"},
        ),
    ]
    
    return create_dataset(
        name="brd_parsing_test",
        description="Test cases for full BRD parsing and estimation",
        examples=examples,
    )
