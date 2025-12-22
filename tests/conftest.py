"""
Pytest configuration and Hypothesis settings for AITEA test suite.
"""
from hypothesis import settings

# Configure Hypothesis defaults for all tests
settings.register_profile("default", max_examples=100)
settings.load_profile("default")
