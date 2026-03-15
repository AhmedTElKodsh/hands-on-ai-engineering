#!/usr/bin/env python3
"""
Day 00 Python Diagnostic — Student Task File

Purpose: Assess Python proficiency before starting Week 1
Time: 90 minutes (no AI assistance)

Instructions:
1. Replace ALL TODO comments with your implementation
2. Do NOT use AI assistance during this diagnostic
3. Run the grader: python grade_diagnostic.py
4. Check your results in diagnostic_results/

Strict Failure Rule:
- Incomplete/Partial solutions = 0 points (Weakness)
- Incorrect/Failing solutions = 0 points (Weakness)
- AI usage detected = Immediate reset of diagnostic

Scoring: 5 tasks × 1 point each = 5 points total

Path Recommendations:
- 5/5: Skip to Week 1
- 3-4/5: Compressed Week 0 (3 days)
- 0-2/5: Full Week 0 (5 days)
"""

import pandas as pd
import requests
from typing import List, Dict, Optional, TypedDict


# ============================================================================
# TASK 1: CSV Data Pipeline (20 minutes)
# ============================================================================
# Requirements:
# 1. Load the CSV file from data/sample_data.csv
# 2. Clean missing values (drop rows with NaN OR fill with appropriate values)
# 3. Compute groupby statistics (group by 'category', calculate sum and mean of 'value')
# 4. Output results to results.json
#
# Expected output format:
# {
#     "total_rows": 100,
#     "cleaned_rows": 95,
#     "by_category": {
#         "A": {"sum": 1234, "mean": 56.7},
#         "B": {"sum": 2345, "mean": 67.8}
#     }
# }
# ============================================================================

def load_and_clean_csv(file_path: str) -> pd.DataFrame:
    """
    Load CSV and clean missing values.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Cleaned DataFrame with no null values
    """
    df = pd.read_csv(file_path)
    
    # TODO: Handle missing values
    # Hint: Use df.dropna() to drop rows with NaN
    # OR use df.fillna() to fill with appropriate values
    # Return the cleaned DataFrame
    
    return df


def compute_groupby_stats(df: pd.DataFrame) -> Dict:
    """
    Compute groupby statistics by category.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        Dictionary with 'by_category' key containing sum and mean for each category
    """
    # TODO: Group by 'category' column
    # TODO: Calculate sum and mean of 'value' column
    # TODO: Return as dictionary with structure: {"by_category": {"Electronics": {"sum": X, "mean": Y}, ...}}
    
    pass


def main_task_1():
    """Main pipeline function for Task 1."""
    # TODO: Load and clean data
    # TODO: Compute statistics
    # TODO: Save to results.json
    # TODO: Print summary
    pass


# ============================================================================
# TASK 2: OOP Class Implementation (15 minutes)
# ============================================================================
# Requirements:
# 1. Create a class called `BankAccount`
# 2. Implement `__init__` with parameters: owner (str), balance (float)
# 3. Implement at least 2 methods:
#    - deposit(amount: float) -> bool: Add money, return True if successful
#    - withdraw(amount: float) -> bool: Remove money, return False if insufficient funds
# 4. Implement `__repr__` that returns a useful string representation
#
# Example usage:
# >>> account = BankAccount("Alice", 1000.0)
# >>> account.deposit(500.0)
# True
# >>> account.withdraw(200.0)
# True
# >>> account.withdraw(5000.0)  # Insufficient funds
# False
# >>> repr(account)
# "BankAccount(owner='Alice', balance=1300.0)"
# ============================================================================

class BankAccount:
    """Bank account class with deposit and withdraw functionality."""

    def __init__(self, owner: str, balance: float):
        """
        Initialize account with owner and balance.
        
        Args:
            owner: Account owner's name
            balance: Initial balance
        """
        # TODO: Set up instance variables for owner and balance
        pass

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful, False if amount is invalid
        """
        # TODO: Implement deposit logic
        # Return True if successful, False if amount is invalid (negative or zero)
        pass

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful, False if insufficient funds
        """
        # TODO: Implement withdraw logic
        # Return True if successful, False if insufficient funds
        pass

    def __repr__(self) -> str:
        """Return string representation of account."""
        # TODO: Return useful string representation like "BankAccount(owner='Alice', balance=1300.0)"
        pass


# ============================================================================
# TASK 3: REST API Client (20 minutes)
# ============================================================================
# Requirements:
# 1. Use `requests` to call a REST API
# 2. Parse the JSON response
# 3. Handle errors with try/except (network errors, HTTP errors, JSON parsing errors)
# 4. Return structured data
#
# Use this API for testing: https://jsonplaceholder.typicode.com
#
# Implement a function that:
# - Fetches posts from /posts endpoint
# - Filters posts by userId
# - Returns list of post titles for that user
# - Handles errors gracefully
# ============================================================================

class APIError(Exception):
    """Custom exception for API errors."""
    pass


def fetch_user_post_titles(user_id: int) -> Optional[List[str]]:
    """
    Fetch post titles for a specific user from JSONPlaceholder API.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        List of post titles, or None if error occurs
        
    Raises:
        APIError: If API call fails
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = f"{base_url}/posts"
    params = {"userId": user_id}

    # TODO: Make API request using requests.get()
    # TODO: Raise exception for HTTP errors (response.raise_for_status())
    # TODO: Parse JSON response
    # TODO: Extract and return list of titles
    # TODO: Handle errors with try/except
    # TODO: Return None for invalid user (no posts found)
    pass


def fetch_post_by_id(post_id: int) -> Optional[Dict]:
    """
    Fetch a single post by ID.
    
    Args:
        post_id: The ID of the post
        
    Returns:
        Post data as dict, or None if not found
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = f"{base_url}/posts/{post_id}"

    # TODO: Implement similar to fetch_user_post_titles
    # TODO: Return the post dict or None if not found
    pass


# ============================================================================
# TASK 4: Type Hints + Filtering (20 minutes)
# ============================================================================
# Requirements:
# 1. Write a function with proper type hints
# 2. Filter a list of dictionaries by a condition
# 3. Return sorted results
#
# Implement a function that:
# - Takes a list of product dicts (each has: name, price, category, in_stock)
# - Filters products by: in_stock=True AND price <= max_price
# - Returns sorted list of product names (alphabetically)
# ============================================================================

class Product(TypedDict):
    """Product data structure."""
    name: str
    price: float
    category: str
    in_stock: bool


def filter_and_sort_products(
    products: List[Product],
    max_price: float
) -> List[str]:
    """
    Filter products by stock and price, return sorted names.
    
    Args:
        products: List of product dictionaries
        max_price: Maximum price to include
        
    Returns:
        Alphabetically sorted list of product names that match criteria
    """
    # TODO: Filter products where in_stock=True AND price <= max_price
    # TODO: Extract product names
    # TODO: Sort alphabetically
    # TODO: Return sorted list
    pass


def filter_products_by_category(
    products: List[Product],
    category: str
) -> List[Product]:
    """
    Filter products by category.
    
    Args:
        products: List of product dictionaries
        category: Category to filter by
        
    Returns:
        List of products in the specified category
    """
    # TODO: Implement filtering by category
    # Return only products that match the given category
    pass


# ============================================================================
# TASK 5: Pytest Tests (15 minutes)
# ============================================================================
# Requirements:
# 1. Write at least 2 pytest tests for the filter_and_sort_products function
# 2. Include at least one test for happy path and one for edge case
# 3. Use proper assertions
#
# Write tests for:
# - filter_and_sort_products with various inputs
# - Edge cases: empty list, no matching products, all matching products
# ============================================================================

import pytest

# Sample test data (you can use this or create your own)
SAMPLE_PRODUCTS: List[Product] = [
    {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
    {"name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": True},
    {"name": "Keyboard", "price": 79.99, "category": "Electronics", "in_stock": False},
    {"name": "Desk Chair", "price": 199.99, "category": "Furniture", "in_stock": True},
]


def test_filter_and_sort_products_basic():
    """Test basic filtering and sorting."""
    # TODO: Write test for basic functionality
    # Filter by max_price=100, expect ['Mouse']
    # Use assert to verify the result
    pass


def test_filter_and_sort_products_empty():
    """Test with empty product list."""
    # TODO: Write test for edge case: empty list
    # Should return empty list
    pass


def test_filter_and_sort_products_no_matches():
    """Test when no products match criteria."""
    # TODO: Write test for edge case: no matches
    # Filter by max_price=10, should return empty list
    pass


def test_filter_and_sort_products_all_match():
    """Test when all products match criteria."""
    # TODO: Write test for edge case: all match
    # Filter by high max_price where all in-stock products match
    pass


def test_filter_products_by_category():
    """Test category filtering."""
    # TODO: Write test for filter_products_by_category
    # Filter by "Electronics", expect 3 products (Laptop, Mouse, Keyboard)
    pass


# ============================================================================
# MAIN EXECUTION (DO NOT MODIFY)
# ============================================================================

if __name__ == "__main__":
    print("Day 00 Python Diagnostic")
    print("=" * 60)
    print("Instructions:")
    print("1. Complete all TODO sections above")
    print("2. Run: python grade_diagnostic.py")
    print("3. Check results in diagnostic_results/")
    print("=" * 60)
    print()
    
    # Quick self-test (optional)
    print("Quick self-test (Task 4):")
    test_products = [
        {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
        {"name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": True},
    ]
    try:
        result = filter_and_sort_products(test_products, max_price=100.0)
        print(f"  Result: {result}")
        print(f"  Expected: ['Mouse']")
        print(f"  Match: {result == ['Mouse']}")
    except Exception as e:
        print(f"  Error: {e}")
        print("  (Implement filter_and_sort_products to fix)")
