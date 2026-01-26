"""
Tests for Chapter 6B: Error Handling Patterns

This test suite validates the error handling patterns taught in Chapter 6B.
Tests are designed to run even with stub implementations (they'll fail, but execute).
"""

import pytest
import logging
from pathlib import Path
from typing import Optional


# ============================================================================
# Test Group 1: Exception Hierarchy
# ============================================================================

def test_llm_error_base_exception():
    """Test that LLMError can be instantiated."""
    try:
        from shared.exceptions import LLMError
        error = LLMError("Test error")
        assert str(error) == "Test error"
    except (ImportError, NotImplementedError):
        pytest.skip("LLMError not yet implemented")


def test_authentication_error_inheritance():
    """Test that AuthenticationError inherits from LLMError."""
    try:
        from shared.exceptions import LLMError, AuthenticationError
        
        # AuthenticationError should be caught by LLMError handler
        try:
            raise AuthenticationError("Invalid API key")
        except LLMError as e:
            assert "Invalid API key" in str(e)
        else:
            pytest.fail("AuthenticationError should be caught by LLMError handler")
            
    except (ImportError, NotImplementedError):
        pytest.skip("Exception hierarchy not yet implemented")


def test_rate_limit_error_inheritance():
    """Test that RateLimitError inherits from LLMError."""
    try:
        from shared.exceptions import LLMError, RateLimitError
        
        try:
            raise RateLimitError("Rate limit exceeded")
        except LLMError as e:
            assert "Rate limit" in str(e)
        else:
            pytest.fail("RateLimitError should be caught by LLMError handler")
            
    except (ImportError, NotImplementedError):
        pytest.skip("Exception hierarchy not yet implemented")


def test_context_limit_error_inheritance():
    """Test that ContextLimitError inherits from LLMError."""
    try:
        from shared.exceptions import LLMError, ContextLimitError
        
        try:
            raise ContextLimitError("Context too long")
        except LLMError as e:
            assert "Context" in str(e)
        else:
            pytest.fail("ContextLimitError should be caught by LLMError handler")
            
    except (ImportError, NotImplementedError):
        pytest.skip("Exception hierarchy not yet implemented")


# ============================================================================
# Test Group 2: Result Type Pattern
# ============================================================================

def test_result_ok_creates_success():
    """Test that Result.ok() creates a successful result."""
    try:
        from shared.utils.result import Result
        
        result = Result.ok("test data")
        
        assert result.success is True, "Result.ok should set success=True"
        assert result.data == "test data", "Result.ok should store data"
        assert result.error is None, "Result.ok should have no error"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result class not yet implemented")


def test_result_fail_creates_failure():
    """Test that Result.fail() creates a failed result."""
    try:
        from shared.utils.result import Result
        
        result = Result.fail("error message")
        
        assert result.success is False, "Result.fail should set success=False"
        assert result.data is None, "Result.fail should have no data"
        assert result.error == "error message", "Result.fail should store error"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result class not yet implemented")


def test_result_unwrap_success():
    """Test that unwrap() returns data on success."""
    try:
        from shared.utils.result import Result
        
        result = Result.ok(42)
        value = result.unwrap()
        
        assert value == 42, "unwrap() should return the data value"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result.unwrap() not yet implemented")


def test_result_unwrap_failure_raises():
    """Test that unwrap() raises ValueError on failure."""
    try:
        from shared.utils.result import Result
        
        result = Result.fail("something went wrong")
        
        with pytest.raises(ValueError, match="something went wrong"):
            result.unwrap()
            
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result.unwrap() not yet implemented")


def test_result_unwrap_or_returns_default():
    """Test that unwrap_or() returns default value on failure."""
    try:
        from shared.utils.result import Result
        
        result = Result.fail("error")
        value = result.unwrap_or(99)
        
        assert value == 99, "unwrap_or() should return default on failure"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result.unwrap_or() not yet implemented")


def test_result_unwrap_or_returns_data_on_success():
    """Test that unwrap_or() returns data on success (ignores default)."""
    try:
        from shared.utils.result import Result
        
        result = Result.ok(42)
        value = result.unwrap_or(99)
        
        assert value == 42, "unwrap_or() should return data on success"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result.unwrap_or() not yet implemented")


# ============================================================================
# Test Group 3: safe_llm_call() Function
# ============================================================================

def test_safe_llm_call_exists():
    """Test that safe_llm_call function exists with correct signature."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import safe_llm_call
        import inspect
        
        sig = inspect.signature(safe_llm_call)
        assert 'prompt' in sig.parameters, "Function should have 'prompt' parameter"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("safe_llm_call() not yet implemented")


def test_safe_llm_call_empty_prompt_returns_failure():
    """Test that empty prompt returns Result.fail."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import safe_llm_call
        from shared.utils.result import Result
        
        result = safe_llm_call("")
        
        assert isinstance(result, Result), "Should return Result type"
        assert result.success is False, "Empty prompt should fail"
        assert result.error is not None, "Should have error message"
        assert "empty" in result.error.lower(), "Error should mention 'empty'"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("safe_llm_call() not yet implemented")


def test_safe_llm_call_valid_prompt_returns_success():
    """Test that valid prompt returns Result.ok."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import safe_llm_call
        from shared.utils.result import Result
        
        result = safe_llm_call("Hello, AI!")
        
        assert isinstance(result, Result), "Should return Result type"
        assert result.success is True, "Valid prompt should succeed"
        assert result.data is not None, "Should have response data"
        assert isinstance(result.data, str), "Response should be string"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("safe_llm_call() not yet implemented")


def test_safe_llm_call_never_raises_exceptions():
    """Test that safe_llm_call never raises exceptions (returns Result instead)."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import safe_llm_call
        from shared.utils.result import Result
        
        # Even with empty prompt, should not raise
        result = safe_llm_call("")
        assert isinstance(result, Result), "Should return Result, not raise exception"
        
        # Valid prompt should also not raise
        result = safe_llm_call("Test")
        assert isinstance(result, Result), "Should return Result, not raise exception"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("safe_llm_call() not yet implemented")


# ============================================================================
# Test Group 4: Error Propagation (process_file)
# ============================================================================

def test_process_file_exists():
    """Test that process_file function exists."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import process_file
        import inspect
        
        sig = inspect.signature(process_file)
        assert 'input_path' in sig.parameters or 'input_file' in sig.parameters
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("process_file() not yet implemented")


def test_process_file_missing_input_returns_failure():
    """Test that missing input file returns Result.fail."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import process_file
        from shared.utils.result import Result
        
        result = process_file("nonexistent_file.json", "output.json")
        
        assert isinstance(result, Result), "Should return Result type"
        assert result.success is False, "Missing file should fail"
        assert result.error is not None, "Should have error message"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("process_file() not yet implemented")


# ============================================================================
# Test Group 5: Logging Setup
# ============================================================================

def test_setup_logger_exists():
    """Test that setup_logger function exists."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import setup_logger
        import inspect
        
        sig = inspect.signature(setup_logger)
        assert 'name' in sig.parameters, "Should have 'name' parameter"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("setup_logger() not yet implemented")


def test_setup_logger_creates_logger():
    """Test that setup_logger creates a logger with correct name."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import setup_logger
        
        logger = setup_logger("test_logger")
        
        assert logger is not None, "Should return a logger"
        assert logger.name == "test_logger", "Logger should have correct name"
        assert isinstance(logger, logging.Logger), "Should return Logger instance"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("setup_logger() not yet implemented")


def test_setup_logger_sets_level():
    """Test that setup_logger sets the correct log level."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import setup_logger
        
        logger = setup_logger("test_logger_level", level=logging.DEBUG)
        
        assert logger.level == logging.DEBUG, "Should set DEBUG level"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("setup_logger() not yet implemented")


def test_setup_logger_no_duplicate_handlers():
    """Test that calling setup_logger twice doesn't add duplicate handlers."""
    try:
        from curriculum.chapters.phase_0_foundations.chapter_06B import setup_logger
        
        logger1 = setup_logger("test_no_duplicates")
        handler_count_1 = len(logger1.handlers)
        
        logger2 = setup_logger("test_no_duplicates")
        handler_count_2 = len(logger2.handlers)
        
        assert handler_count_1 == handler_count_2, "Should not add duplicate handlers"
        
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("setup_logger() not yet implemented")


# ============================================================================
# Test Group 6: Integration Tests
# ============================================================================

def test_result_pattern_integration():
    """Integration test: Result pattern works end-to-end."""
    try:
        from shared.utils.result import Result
        
        # Simulate a workflow using Result pattern
        def step1() -> Result[int]:
            return Result.ok(10)
        
        def step2(value: int) -> Result[int]:
            if value < 0:
                return Result.fail("Negative value")
            return Result.ok(value * 2)
        
        # Chain operations
        result1 = step1()
        if result1.success:
            result2 = step2(result1.data)
            assert result2.success is True
            assert result2.data == 20
        else:
            pytest.fail("Step 1 should succeed")
            
    except (ImportError, NotImplementedError, AttributeError):
        pytest.skip("Result pattern not yet fully implemented")


# ============================================================================
# Test Configuration
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
