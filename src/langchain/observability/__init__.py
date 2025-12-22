"""LangSmith observability integration for AITEA.

This module provides tracing, evaluation, and dataset management
using LangSmith for monitoring and improving LLM interactions.
"""

from .tracing import (
    configure_langsmith,
    get_config,
    get_tracer,
    is_tracing_enabled,
    trace_chain,
    trace_agent,
    LangSmithConfig,
    create_trace_metadata,
)
from .evaluation import (
    create_evaluator,
    evaluate_chain,
    evaluate_agent,
    EvaluationResult,
    EvaluationMetrics,
    create_feature_extraction_evaluator,
    create_estimation_accuracy_evaluator,
    create_confidence_level_evaluator,
)
from .datasets import (
    create_dataset,
    add_examples,
    get_dataset,
    list_datasets,
    delete_dataset,
    DatasetExample,
    create_feature_extraction_dataset,
    create_estimation_dataset,
    create_brd_parsing_dataset,
)

__all__ = [
    # Tracing
    "configure_langsmith",
    "get_config",
    "get_tracer",
    "is_tracing_enabled",
    "trace_chain",
    "trace_agent",
    "LangSmithConfig",
    "create_trace_metadata",
    # Evaluation
    "create_evaluator",
    "evaluate_chain",
    "evaluate_agent",
    "EvaluationResult",
    "EvaluationMetrics",
    "create_feature_extraction_evaluator",
    "create_estimation_accuracy_evaluator",
    "create_confidence_level_evaluator",
    # Datasets
    "create_dataset",
    "add_examples",
    "get_dataset",
    "list_datasets",
    "delete_dataset",
    "DatasetExample",
    "create_feature_extraction_dataset",
    "create_estimation_dataset",
    "create_brd_parsing_dataset",
]
