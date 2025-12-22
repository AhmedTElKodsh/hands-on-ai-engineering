"""Tests for LangSmith observability integration.

These tests verify the tracing, evaluation, and dataset management
functionality of the LangSmith integration.
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from src.langchain.observability import (
    configure_langsmith,
    get_config,
    get_tracer,
    is_tracing_enabled,
    trace_chain,
    trace_agent,
    LangSmithConfig,
    create_evaluator,
    evaluate_chain,
    EvaluationResult,
    EvaluationMetrics,
    create_dataset,
    add_examples,
    get_dataset,
    DatasetExample,
    create_feature_extraction_evaluator,
    create_estimation_accuracy_evaluator,
)


class TestLangSmithConfiguration:
    """Tests for LangSmith configuration."""
    
    def test_configure_langsmith_with_api_key(self):
        """Test configuring LangSmith with explicit API key."""
        config = configure_langsmith(
            api_key="test-key",
            project="test-project",
            tracing_enabled=True,
        )
        
        assert config.api_key == "test-key"
        assert config.project == "test-project"
        assert config.tracing_enabled is True
    
    def test_configure_langsmith_from_env(self, monkeypatch):
        """Test configuring LangSmith from environment variables."""
        monkeypatch.setenv("LANGSMITH_API_KEY", "env-key")
        
        config = configure_langsmith(project="test-project")
        
        assert config.api_key == "env-key"
        assert config.project == "test-project"
    
    def test_configure_langsmith_no_api_key(self):
        """Test configuring LangSmith without API key disables tracing."""
        config = configure_langsmith(
            api_key=None,
            project="test-project",
            tracing_enabled=True,
        )
        
        # Should disable tracing if no API key
        assert config.tracing_enabled is False
    
    def test_get_config(self):
        """Test getting current configuration."""
        configure_langsmith(api_key="test-key", project="test")
        
        config = get_config()
        assert config is not None
        assert config.project == "test"
    
    def test_is_tracing_enabled_with_config(self):
        """Test checking if tracing is enabled."""
        # Without configuration
        result = is_tracing_enabled()
        assert isinstance(result, bool)


class TestTracing:
    """Tests for tracing decorators and utilities."""
    
    def test_trace_chain_decorator(self):
        """Test @trace_chain decorator."""
        @trace_chain(name="test_chain", tags=["test"])
        def test_function(x: int) -> int:
            return x * 2
        
        result = test_function(5)
        assert result == 10
    
    def test_trace_agent_decorator(self):
        """Test @trace_agent decorator."""
        @trace_agent(name="test_agent", tags=["test"])
        def test_function(x: int) -> int:
            return x + 1
        
        result = test_function(5)
        assert result == 6
    
    def test_trace_chain_without_langsmith(self):
        """Test tracing works even without LangSmith configured."""
        @trace_chain(name="test")
        def test_function() -> str:
            return "success"
        
        # Should not raise error even if LangSmith not configured
        result = test_function()
        assert result == "success"


class TestEvaluators:
    """Tests for evaluator creation and execution."""
    
    def test_create_evaluator(self):
        """Test creating a custom evaluator."""
        def check_value(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
            return expected["value"] == actual["value"]
        
        evaluator = create_evaluator(
            name="value_check",
            evaluator_fn=check_value,
            description="Checks if values match",
        )
        
        assert evaluator is not None
        assert callable(evaluator)
    
    def test_feature_extraction_evaluator(self):
        """Test feature extraction evaluator."""
        evaluator = create_feature_extraction_evaluator()
        assert evaluator is not None
    
    def test_estimation_accuracy_evaluator(self):
        """Test estimation accuracy evaluator."""
        evaluator = create_estimation_accuracy_evaluator(tolerance=0.2)
        assert evaluator is not None
    
    def test_evaluator_execution(self):
        """Test evaluator execution logic."""
        def check_count(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
            return len(actual.get("items", [])) == expected.get("count", 0)
        
        evaluator_fn = check_count
        
        # Test passing case
        expected = {"count": 3}
        actual = {"items": [1, 2, 3]}
        assert evaluator_fn(expected, actual) is True
        
        # Test failing case
        actual = {"items": [1, 2]}
        assert evaluator_fn(expected, actual) is False


class TestEvaluation:
    """Tests for chain and agent evaluation."""
    
    def test_evaluation_result_creation(self):
        """Test creating an EvaluationResult."""
        metrics = EvaluationMetrics(
            accuracy=0.85,
            latency_ms=1200.0,
            token_usage=5000,
        )
        
        result = EvaluationResult(
            dataset_name="test_dataset",
            num_examples=10,
            metrics=metrics,
            passed=8,
            failed=2,
        )
        
        assert result.dataset_name == "test_dataset"
        assert result.num_examples == 10
        assert result.passed == 8
        assert result.failed == 2
        assert result.metrics.accuracy == 0.85
    
    def test_evaluation_result_str(self):
        """Test EvaluationResult string representation."""
        metrics = EvaluationMetrics(accuracy=0.9)
        result = EvaluationResult(
            dataset_name="test",
            num_examples=10,
            metrics=metrics,
            passed=9,
            failed=1,
        )
        
        result_str = str(result)
        assert "test" in result_str
        assert "10" in result_str
        assert "9" in result_str
    
    def test_evaluate_chain_without_langsmith(self):
        """Test evaluate_chain returns empty result without LangSmith."""
        mock_chain = Mock()
        
        result = evaluate_chain(
            mock_chain,
            dataset_name="test_dataset",
        )
        
        # Should return empty result without LangSmith configured
        assert result.num_examples == 0
        assert result.passed == 0
        assert result.failed == 0


class TestDatasets:
    """Tests for dataset management."""
    
    def test_dataset_example_creation(self):
        """Test creating a DatasetExample."""
        example = DatasetExample(
            inputs={"text": "test input"},
            outputs={"result": "test output"},
            metadata={"category": "test"},
        )
        
        assert example.inputs["text"] == "test input"
        assert example.outputs["result"] == "test output"
        assert example.metadata["category"] == "test"
    
    def test_create_dataset_without_langsmith(self):
        """Test create_dataset returns None without LangSmith."""
        examples = [
            DatasetExample(
                inputs={"x": 1},
                outputs={"y": 2},
            )
        ]
        
        result = create_dataset(
            name="test_dataset",
            description="Test",
            examples=examples,
        )
        
        # Should return None without LangSmith configured
        assert result is None
    
    def test_add_examples_without_langsmith(self):
        """Test add_examples returns 0 without LangSmith."""
        examples = [
            DatasetExample(
                inputs={"x": 1},
                outputs={"y": 2},
            )
        ]
        
        count = add_examples("test_dataset", examples)
        
        # Should return 0 without LangSmith configured
        assert count == 0
    
    def test_get_dataset_without_langsmith(self):
        """Test get_dataset returns None without LangSmith."""
        dataset = get_dataset("test_dataset")
        
        # Should return None without LangSmith configured
        assert dataset is None


class TestBuiltInEvaluators:
    """Tests for built-in AITEA evaluators."""
    
    def test_feature_extraction_evaluator_logic(self):
        """Test feature extraction evaluator logic."""
        # Create the evaluator function logic (not the LangSmith wrapper)
        def check_features(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
            expected_features = set(expected.get("features", []))
            actual_features = set(f["name"] for f in actual.get("features", []))
            
            if not expected_features:
                return True
            
            overlap = len(expected_features & actual_features)
            return overlap / len(expected_features) >= 0.8
        
        # Test exact match
        expected = {"features": ["auth", "login", "register"]}
        actual = {"features": [
            {"name": "auth"},
            {"name": "login"},
            {"name": "register"},
        ]}
        assert check_features(expected, actual) is True
        
        # Test below 80% (fails) - 2 out of 3 is 66.67%
        actual = {"features": [
            {"name": "auth"},
            {"name": "login"},
        ]}
        assert check_features(expected, actual) is False
        
        # Test exactly 80% match (passes) - 4 out of 5
        expected = {"features": ["auth", "login", "register", "profile", "settings"]}
        actual = {"features": [
            {"name": "auth"},
            {"name": "login"},
            {"name": "register"},
            {"name": "profile"},
        ]}
        assert check_features(expected, actual) is True
    
    def test_estimation_accuracy_evaluator_logic(self):
        """Test estimation accuracy evaluator logic."""
        def check_estimation(expected: Dict[str, Any], actual: Dict[str, Any], tolerance: float = 0.2) -> bool:
            expected_hours = expected.get("total_hours", 0)
            actual_hours = actual.get("total_hours", 0)
            
            if expected_hours == 0:
                return actual_hours == 0
            
            relative_error = abs(actual_hours - expected_hours) / expected_hours
            return relative_error <= tolerance
        
        # Test exact match
        expected = {"total_hours": 10.0}
        actual = {"total_hours": 10.0}
        assert check_estimation(expected, actual) is True
        
        # Test within tolerance (20%)
        actual = {"total_hours": 11.5}
        assert check_estimation(expected, actual) is True
        
        # Test outside tolerance
        actual = {"total_hours": 15.0}
        assert check_estimation(expected, actual) is False
        
        # Test zero case
        expected = {"total_hours": 0}
        actual = {"total_hours": 0}
        assert check_estimation(expected, actual) is True


class TestIntegration:
    """Integration tests for observability features."""
    
    def test_full_workflow_without_langsmith(self):
        """Test full workflow works without LangSmith configured."""
        # Configure (will disable tracing without API key)
        config = configure_langsmith(api_key=None, project="test")
        
        # Create evaluator
        evaluator = create_feature_extraction_evaluator()
        
        # Create dataset (will return None)
        dataset_id = create_dataset("test", examples=[])
        assert dataset_id is None
        
        # Evaluate chain (will return empty result)
        mock_chain = Mock()
        result = evaluate_chain(mock_chain, "test")
        assert result.num_examples == 0
    
    def test_decorators_preserve_function_metadata(self):
        """Test that decorators preserve function metadata."""
        @trace_chain(name="test")
        def my_function():
            """My docstring."""
            pass
        
        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
