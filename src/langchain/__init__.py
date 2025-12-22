"""LangChain integration for AITEA.

This package provides LangChain Expression Language (LCEL) chains and tools
for feature extraction, estimation, and agent integration using the AITEA
core services.
"""

from .chains import (
    create_feature_extraction_chain,
    create_estimation_chain,
    create_simple_passthrough_chain,
    create_multi_input_chain,
)
from .tools import (
    create_feature_tools,
    get_feature_info,
    calculate_team_velocity,
)
from .vector_stores import (
    VectorStore,
    EmbeddingModel,
    Document,
    SearchResult,
    EmbeddingProvider,
    create_embedding_model,
)
from .stores import (
    ChromaDBStore,
    PineconeStore,
    QdrantStore,
)
from .embeddings import (
    OpenAIEmbedding,
    CohereEmbedding,
    BGEEmbedding,
)
from .brd_parser_agent import (
    BRDParserAgent,
    create_brd_parser_agent,
    ExtractedFeature,
    BRDParseResult,
    AgentState,
)
from .observability import (
    configure_langsmith,
    get_tracer,
    trace_chain,
    trace_agent,
    LangSmithConfig,
    create_evaluator,
    evaluate_chain,
    evaluate_agent,
    EvaluationResult,
    EvaluationMetrics,
    create_dataset,
    add_examples,
    get_dataset,
    DatasetExample,
)

__all__ = [
    # Chains
    "create_feature_extraction_chain",
    "create_estimation_chain",
    "create_simple_passthrough_chain",
    "create_multi_input_chain",
    # Tools
    "create_feature_tools",
    "get_feature_info",
    "calculate_team_velocity",
    # Vector Stores
    "VectorStore",
    "EmbeddingModel",
    "Document",
    "SearchResult",
    "EmbeddingProvider",
    "create_embedding_model",
    "ChromaDBStore",
    "PineconeStore",
    "QdrantStore",
    # Embeddings
    "OpenAIEmbedding",
    "CohereEmbedding",
    "BGEEmbedding",
    # BRD Parser Agent
    "BRDParserAgent",
    "create_brd_parser_agent",
    "ExtractedFeature",
    "BRDParseResult",
    "AgentState",
    # Observability
    "configure_langsmith",
    "get_tracer",
    "trace_chain",
    "trace_agent",
    "LangSmithConfig",
    "create_evaluator",
    "evaluate_chain",
    "evaluate_agent",
    "EvaluationResult",
    "EvaluationMetrics",
    "create_dataset",
    "add_examples",
    "get_dataset",
    "DatasetExample",
]
