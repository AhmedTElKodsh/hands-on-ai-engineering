"""
Task 4: Type Hints + Filtering

Requirements:
1. Write a function with proper type hints
2. Filter a list of dictionaries by a condition
3. Return sorted results

Implement a function that:
- Takes a list of product dicts (each has: name, price, category, in_stock)
- Filters products by: in_stock=True AND price <= max_price
- Returns sorted list of product names (alphabetically)

Time: 20 minutes
"""

from typing import TypedDict


class Product(TypedDict):
    """Product data structure."""
    name: str
    price: float
    category: str
    in_stock: bool


def filter_and_sort_products(
    products: list[Product],
    max_price: float
) -> list[str]:
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
    products: list[Product],
    category: str
) -> list[Product]:
    """
    Filter products by category.

    Args:
        products: List of product dictionaries
        category: Category to filter by

    Returns:
        List of products in the specified category
    """
    # TODO: Implement filtering by category
    pass


if __name__ == "__main__":
    # Sample data for testing
    sample_products: list[Product] = [
        {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
        {"name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": True},
        {"name": "Keyboard", "price": 79.99, "category": "Electronics", "in_stock": False},
        {"name": "Desk Chair", "price": 199.99, "category": "Furniture", "in_stock": True},
        {"name": "Monitor", "price": 349.99, "category": "Electronics", "in_stock": True},
    ]

    # Test filter_and_sort_products
    result = filter_and_sort_products(sample_products, max_price=100.0)
    print(f"Products under $100: {result}")
    # Expected: ['Mouse']

    result = filter_and_sort_products(sample_products, max_price=500.0)
    print(f"Products under $500: {result}")
    # Expected: ['Desk Chair', 'Laptop', 'Monitor', 'Mouse']
