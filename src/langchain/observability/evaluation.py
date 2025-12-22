"""LangSmith evaluation utilities.

This module provides functions for evaluating chains and agents
using LangSmith's evaluation framework.
"""

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List, Callable
from datetime import datetime
import warnings

try:
    from langsmith import Client
    from langsmith.evaluation import evaluate, EvaluationResult as LSEvaluationResult
    from langsmith.schemas import Example, Run
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    warnings.warn(
        "LangSmith not installed. Install with: pip install langsmith\n"
        "Evaluation will be disabled.",
        ImportWarning
    )

from .tracing import get_client, is_tracing_enabled


@dataclass
class EvaluationMetrics:
    """Metrics from an evaluation run.
    
    Attributes:
        accuracy: Accuracy score (0.0 to 1.0)
        precision: Precision score (0.0 to 1.0)
        recall: Recall score (0.0 to 1.0)
        f1_score: F1 score (0.0 to 1.0)
        latency_ms: Average latency in milliseconds
        token_usage: Total tokens used
        cost_usd: Estimated cost in USD
        custom_metrics: Additional custom metrics
    """
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    latency_ms: float = 0.0
    token_usage: int = 0
    cost_usd: float = 0.0
    custom_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result from evaluating a chain or agent.
    
    Attributes:
        dataset_name: Name of the dataset used for evaluation
        num_examples: Number of examples evaluated
        metrics: Aggregated metrics
        passed: Number of examples that passed
        failed: Number of examples that failed
        timestamp: When the evaluation was run
        details: Detailed results per example
    """
    dataset_name: str
    num_examples: int
    metrics: EvaluationMetrics
    passed: int
    failed: int
    timestamp: datetime = field(default_factory=datetime.now)
    details: List[Dict[str, Any]] = field(default_factory=list)
    
    def __str__(self) -> str:
        """Format evaluation result as string."""
        return (
            f"Evaluation Results for '{self.dataset_name}':\n"
            f"  Examples: {self.num_examples}\n"
            f"  Passed: {self.passed} ({self.passed/self.num_examples*100:.1f}%)\n"
            f"  Failed: {self.failed} ({self.failed/self.num_examples*100:.1f}%)\n"
            f"  Accuracy: {self.metrics.accuracy:.3f}\n"
            f"  Avg Latency: {self.metrics.latency_ms:.0f}ms\n"
            f"  Token Usage: {self.metrics.token_usage}\n"
        )


def create_evaluator(
    name: str,
    evaluator_fn: Callable[[Dict[str, Any], Dict[str, Any]], bool],
    description: Optional[str] = None,
) -> Callable:
    """Create a custom evaluator function for LangSmith.
    
    An evaluator takes the expected output and actual output and returns
    whether the result is correct.
    
    Args:
        name: Name of the evaluator
        evaluator_fn: Function that takes (expected, actual) and returns bool
        description: Description of what the evaluator checks
    
    Returns:
        Evaluator function compatible with LangSmith
    
    Example:
        >>> def check_feature_count(expected, actual):
        ...     return len(actual["features"]) == expected["feature_count"]
        >>> 
        >>> evaluator = create_evaluator(
        ...     name="feature_count",
        ...     evaluator_fn=check_feature_count,
        ...     description="Checks if correct number of features extracted"
        ... )
    """
    if not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not available - evaluator will be a no-op")
        return lambda x, y: True
    
    def evaluator(run: Run, example: Example) -> dict:
        """LangSmith evaluator wrapper."""
        try:
            expected = example.outputs
            actual = run.outputs
            
            passed = evaluator_fn(expected, actual)
            
            return {
                "key": name,
                "score": 1.0 if passed else 0.0,
                "comment": description or f"{name} evaluation",
            }
        except Exception as e:
            return {
                "key": name,
                "score": 0.0,
                "comment": f"Error: {str(e)}",
            }
    
    return evaluator


def evaluate_chain(
    chain: Any,
    dataset_name: str,
    evaluators: Optional[List[Callable]] = None,
    max_concurrency: int = 5,
) -> EvaluationResult:
    """Evaluate a chain against a LangSmith dataset.
    
    Args:
        chain: The LangChain chain to evaluate
        dataset_name: Name of the dataset in LangSmith
        evaluators: List of evaluator functions
        max_concurrency: Maximum concurrent evaluations
    
    Returns:
        EvaluationResult with metrics and details
    
    Example:
        >>> chain = create_feature_extraction_chain()
        >>> result = evaluate_chain(
        ...     chain,
        ...     dataset_name="feature_extraction_test",
        ...     evaluators=[feature_count_evaluator, feature_name_evaluator]
        ... )
        >>> print(result)
    """
    if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
        warnings.warn("LangSmith not configured - returning empty result")
        return EvaluationResult(
            dataset_name=dataset_name,
            num_examples=0,
            metrics=EvaluationMetrics(),
            passed=0,
            failed=0,
        )
    
    client = get_client()
    if not client:
        raise RuntimeError("LangSmith client not initialized")
    
    # Run evaluation
    results = evaluate(
        lambda inputs: chain.invoke(inputs),
        data=dataset_name,
        evaluators=evaluators or [],
        max_concurrency=max_concurrency,
        client=client,
    )
    
    # Aggregate metrics
    total_examples = 0
    passed = 0
    failed = 0
    total_latency = 0.0
    total_tokens = 0
    details = []
    
    for result in results:
        total_examples += 1
        
        # Check if all evaluators passed
        all_passed = all(
            score.get("score", 0) == 1.0
            for score in result.get("evaluation_results", {}).get("results", [])
        )
        
        if all_passed:
            passed += 1
        else:
            failed += 1
        
        # Collect metrics
        if "latency_ms" in result:
            total_latency += result["latency_ms"]
        if "token_usage" in result:
            total_tokens += result["token_usage"]
        
        details.append(result)
    
    # Calculate aggregated metrics
    accuracy = passed / total_examples if total_examples > 0 else 0.0
    avg_latency = total_latency / total_examples if total_examples > 0 else 0.0
    
    metrics = EvaluationMetrics(
        accuracy=accuracy,
        latency_ms=avg_latency,
        token_usage=total_tokens,
    )
    
    return EvaluationResult(
        dataset_name=dataset_name,
        num_examples=total_examples,
        metrics=metrics,
        passed=passed,
        failed=failed,
        details=details,
    )


def evaluate_agent(
    agent: Any,
    dataset_name: str,
    evaluators: Optional[List[Callable]] = None,
    max_concurrency: int = 5,
) -> EvaluationResult:
    """Evaluate an agent against a LangSmith dataset.
    
    Args:
        agent: The agent to evaluate (LangGraph or LangChain agent)
        dataset_name: Name of the dataset in LangSmith
        evaluators: List of evaluator functions
        max_concurrency: Maximum concurrent evaluations
    
    Returns:
        EvaluationResult with metrics and details
    
    Example:
        >>> agent = create_brd_parser_agent()
        >>> result = evaluate_agent(
        ...     agent,
        ...     dataset_name="brd_parsing_test",
        ...     evaluators=[feature_extraction_evaluator]
        ... )
        >>> print(result)
    """
    # Agent evaluation is similar to chain evaluation
    return evaluate_chain(agent, dataset_name, evaluators, max_concurrency)


# Common evaluators for AITEA

def create_feature_extraction_evaluator() -> Callable:
    """Create evaluator for feature extraction accuracy.
    
    Checks if the extracted features match the expected features.
    
    Returns:
        Evaluator function
    """
    def check_features(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """Check if extracted features match expected."""
        expected_features = set(expected.get("features", []))
        actual_features = set(f["name"] for f in actual.get("features", []))
        
        # Check if at least 80% of expected features were found
        if not expected_features:
            return True
        
        overlap = len(expected_features & actual_features)
        return overlap / len(expected_features) >= 0.8
    
    return create_evaluator(
        name="feature_extraction_accuracy",
        evaluator_fn=check_features,
        description="Checks if at least 80% of expected features were extracted",
    )


def create_estimation_accuracy_evaluator(tolerance: float = 0.2) -> Callable:
    """Create evaluator for estimation accuracy.
    
    Checks if the estimated hours are within tolerance of expected hours.
    
    Args:
        tolerance: Acceptable relative error (default: 20%)
    
    Returns:
        Evaluator function
    """
    def check_estimation(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """Check if estimation is within tolerance."""
        expected_hours = expected.get("total_hours", 0)
        actual_hours = actual.get("total_hours", 0)
        
        if expected_hours == 0:
            return actual_hours == 0
        
        relative_error = abs(actual_hours - expected_hours) / expected_hours
        return relative_error <= tolerance
    
    return create_evaluator(
        name="estimation_accuracy",
        evaluator_fn=check_estimation,
        description=f"Checks if estimation is within {tolerance*100}% of expected",
    )


def create_confidence_level_evaluator() -> Callable:
    """Create evaluator for confidence level correctness.
    
    Checks if the confidence level matches the expected level based on
    data point count.
    
    Returns:
        Evaluator function
    """
    def check_confidence(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """Check if confidence level is correct."""
        expected_confidence = expected.get("confidence", "").lower()
        actual_confidence = actual.get("confidence", "").lower()
        
        return expected_confidence == actual_confidence
    
    return create_evaluator(
        name="confidence_level_accuracy",
        evaluator_fn=check_confidence,
        description="Checks if confidence level matches expected",
    )
