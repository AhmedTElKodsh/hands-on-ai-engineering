"""
Task 5: Pytest Tests

Requirements:
1. Write at least 2 pytest tests for the task_4 functions
2. Include at least one test for happy path and one for edge case
3. Use proper assertions

Write tests for:
- filter_and_sort_products with various inputs
- Edge cases: empty list, no matching products, all matching products

Time: 10 minutes
"""

import pytest
from diagnostic.task_4_type_hints import (
    filter_and_sort_products,
    filter_products_by_category,
    Product,
)


# Sample test data
SAMPLE_PRODUCTS: list[Product] = [
    {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
    {"name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": True},
    {"name": "Keyboard", "price": 79.99, "category": "Electronics", "in_stock": False},
    {"name": "Desk Chair", "price": 199.99, "category": "Furniture", "in_stock": True},
]


def test_filter_and_sort_products_basic():
    """Test basic filtering and sorting."""
    # TODO: Write test for basic functionality
    # Filter by max_price=100, expect ['Mouse']
    pass


def test_filter_and_sort_products_empty():
    """Test with empty product list."""
    # TODO: Write test for edge case: empty list
    pass


def test_filter_and_sort_products_no_matches():
    """Test when no products match criteria."""
    # TODO: Write test for edge case: no matches
    pass


def test_filter_and_sort_products_all_match():
    """Test when all products match criteria."""
    # TODO: Write test for edge case: all match
    pass


def test_filter_products_by_category():
    """Test category filtering."""
    # TODO: Write test for filter_products_by_category
    pass


# Run with: pytest diagnostic/task_5_pytest.py -v
