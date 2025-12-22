"""LangSmith tracing configuration and utilities.

This module provides functions to configure LangSmith tracing for
monitoring LLM calls, chains, and agents.
"""

import os
from dataclasses import dataclass
from typing import Optional, Any, Dict, List
from functools import wraps
import warnings

try:
    from langsmith import Client
    from langchain.callbacks import LangChainTracer
    from langchain_core.tracers.context import tracing_v2_enabled
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    warnings.warn(
        "LangSmith not installed. Install with: pip install langsmith\n"
        "Tracing will be disabled.",
        ImportWarning
    )


@dataclass
class LangSmithConfig:
    """Configuration for LangSmith integration.
    
    Attributes:
        api_key: LangSmith API key (defaults to LANGSMITH_API_KEY env var)
        project: Project name for organizing traces (default: "aitea")
        endpoint: LangSmith API endpoint (default: "https://api.smith.langchain.com")
        tracing_enabled: Whether to enable tracing (default: True)
        auto_trace_chains: Automatically trace all chain executions (default: True)
        auto_trace_agents: Automatically trace all agent executions (default: True)
    """
    api_key: Optional[str] = None
    project: str = "aitea"
    endpoint: str = "https://api.smith.langchain.com"
    tracing_enabled: bool = True
    auto_trace_chains: bool = True
    auto_trace_agents: bool = True
    
    def __post_init__(self):
        """Set API key from environment if not provided."""
        if self.api_key is None:
            self.api_key = os.getenv("LANGSMITH_API_KEY")
        
        if self.tracing_enabled and not self.api_key:
            warnings.warn(
                "LangSmith tracing enabled but LANGSMITH_API_KEY not set. "
                "Tracing will be disabled. Set LANGSMITH_API_KEY environment variable "
                "or pass api_key to LangSmithConfig.",
                UserWarning
            )
            self.tracing_enabled = False


# Global configuration
_config: Optional[LangSmithConfig] = None
_client: Optional[Any] = None
_tracer: Optional[Any] = None


def configure_langsmith(
    api_key: Optional[str] = None,
    project: str = "aitea",
    endpoint: str = "https://api.smith.langchain.com",
    tracing_enabled: bool = True,
    auto_trace_chains: bool = True,
    auto_trace_agents: bool = True,
) -> LangSmithConfig:
    """Configure LangSmith integration.
    
    This function sets up the global LangSmith configuration and initializes
    the client and tracer. Call this once at application startup.
    
    Args:
        api_key: LangSmith API key (defaults to LANGSMITH_API_KEY env var)
        project: Project name for organizing traces
        endpoint: LangSmith API endpoint
        tracing_enabled: Whether to enable tracing
        auto_trace_chains: Automatically trace all chain executions
        auto_trace_agents: Automatically trace all agent executions
    
    Returns:
        LangSmithConfig: The configured LangSmith settings
    
    Example:
        >>> config = configure_langsmith(project="my-aitea-project")
        >>> print(f"Tracing enabled: {config.tracing_enabled}")
    """
    global _config, _client, _tracer
    
    _config = LangSmithConfig(
        api_key=api_key,
        project=project,
        endpoint=endpoint,
        tracing_enabled=tracing_enabled,
        auto_trace_chains=auto_trace_chains,
        auto_trace_agents=auto_trace_agents,
    )
    
    if _config.tracing_enabled and LANGSMITH_AVAILABLE:
        # Set environment variables for LangSmith
        if _config.api_key:
            os.environ["LANGSMITH_API_KEY"] = _config.api_key
        os.environ["LANGSMITH_PROJECT"] = _config.project
        os.environ["LANGSMITH_ENDPOINT"] = _config.endpoint
        os.environ["LANGSMITH_TRACING"] = "true"
        
        # Initialize client and tracer
        _client = Client(api_key=_config.api_key, api_url=_config.endpoint)
        _tracer = LangChainTracer(project_name=_config.project, client=_client)
        
        print(f"✅ LangSmith tracing enabled for project: {_config.project}")
    else:
        if not LANGSMITH_AVAILABLE:
            print("⚠️  LangSmith not installed - tracing disabled")
        else:
            print("⚠️  LangSmith tracing disabled (no API key)")
    
    return _config


def get_config() -> Optional[LangSmithConfig]:
    """Get the current LangSmith configuration.
    
    Returns:
        LangSmithConfig or None if not configured
    """
    return _config


def get_client() -> Optional[Any]:
    """Get the LangSmith client.
    
    Returns:
        Client or None if not configured
    """
    return _client


def get_tracer() -> Optional[Any]:
    """Get the LangChain tracer for LangSmith.
    
    Returns:
        LangChainTracer or None if not configured
    
    Example:
        >>> tracer = get_tracer()
        >>> if tracer:
        ...     chain.invoke(input, config={"callbacks": [tracer]})
    """
    return _tracer


def is_tracing_enabled() -> bool:
    """Check if LangSmith tracing is enabled.
    
    Returns:
        bool: True if tracing is enabled and configured
    """
    return _config is not None and _config.tracing_enabled and _tracer is not None


def trace_chain(name: Optional[str] = None, tags: Optional[List[str]] = None):
    """Decorator to automatically trace a chain execution.
    
    This decorator wraps a function that returns or executes a LangChain chain,
    automatically adding tracing context.
    
    Args:
        name: Custom name for the trace (defaults to function name)
        tags: Tags to add to the trace for filtering
    
    Example:
        >>> @trace_chain(name="feature_extraction", tags=["extraction", "brd"])
        ... def extract_features(brd_text: str):
        ...     chain = create_feature_extraction_chain()
        ...     return chain.invoke({"brd_text": brd_text})
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
                return func(*args, **kwargs)
            
            trace_name = name or func.__name__
            trace_tags = tags or []
            
            # Use LangSmith tracing context
            with tracing_v2_enabled(
                project_name=_config.project,
                tags=trace_tags,
            ):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def trace_agent(name: Optional[str] = None, tags: Optional[List[str]] = None):
    """Decorator to automatically trace an agent execution.
    
    This decorator wraps a function that executes an agent, automatically
    adding tracing context with agent-specific tags.
    
    Args:
        name: Custom name for the trace (defaults to function name)
        tags: Tags to add to the trace for filtering
    
    Example:
        >>> @trace_agent(name="brd_parser", tags=["agent", "brd"])
        ... def parse_brd(brd_text: str):
        ...     agent = create_brd_parser_agent()
        ...     return agent.invoke({"brd_text": brd_text})
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_tracing_enabled() or not LANGSMITH_AVAILABLE:
                return func(*args, **kwargs)
            
            trace_name = name or func.__name__
            trace_tags = ["agent"] + (tags or [])
            
            # Use LangSmith tracing context
            with tracing_v2_enabled(
                project_name=_config.project,
                tags=trace_tags,
            ):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def create_trace_metadata(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create metadata dictionary for trace context.
    
    Args:
        user_id: User identifier for the trace
        session_id: Session identifier for grouping related traces
        metadata: Additional custom metadata
    
    Returns:
        Dict containing trace metadata
    
    Example:
        >>> metadata = create_trace_metadata(
        ...     user_id="user123",
        ...     session_id="session456",
        ...     metadata={"feature": "estimation"}
        ... )
        >>> chain.invoke(input, config={"metadata": metadata})
    """
    trace_metadata = {}
    
    if user_id:
        trace_metadata["user_id"] = user_id
    if session_id:
        trace_metadata["session_id"] = session_id
    if metadata:
        trace_metadata.update(metadata)
    
    return trace_metadata


# Auto-configure on import if environment variables are set
if os.getenv("LANGSMITH_API_KEY"):
    configure_langsmith()
