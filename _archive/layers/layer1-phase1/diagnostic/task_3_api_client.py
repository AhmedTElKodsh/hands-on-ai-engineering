"""
Task 3: REST API Client

Requirements:
1. Use `requests` or `httpx` to call a REST API
2. Parse the JSON response
3. Handle errors with try/except (network errors, HTTP errors, JSON parsing errors)
4. Return structured data

Use this API for testing: https://jsonplaceholder.typicode.com

Implement a function that:
- Fetches posts from /posts endpoint
- Filters posts by userId
- Returns list of post titles for that user
- Handles errors gracefully

Time: 20 minutes
"""

import requests
from typing import Optional


class APIError(Exception):
    """Custom exception for API errors."""
    pass


def fetch_user_post_titles(user_id: int) -> Optional[list[str]]:
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

    # TODO: Make API request
    # TODO: Raise exception for HTTP errors
    # TODO: Parse JSON response
    # TODO: Extract and return list of titles
    # TODO: Handle errors with try/except
    pass


def fetch_post_by_id(post_id: int) -> Optional[dict]:
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
    pass


if __name__ == "__main__":
    # Manual testing
    titles = fetch_user_post_titles(1)
    print(f"User 1 post titles: {titles}")

    post = fetch_post_by_id(1)
    print(f"Post 1: {post}")

    # Test error handling
    try:
        post = fetch_post_by_id(99999)  # Should return None
        print(f"Post 99999: {post}")
    except APIError as e:
        print(f"API Error: {e}")
