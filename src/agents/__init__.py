"""Agent foundations module for AITEA.

This module provides the core agent patterns and implementations
for building AI agents from scratch before using frameworks.

Components:
- SimpleAgent: Basic agent implementing Observe-Think-Act-Reflect loop
- AgentState: Enumeration of agent states
- AgentTransition: Record of state transitions
- Memory Classes: ShortTermMemory, LongTermMemory, SummarizationMemory
- Safety: Prompt injection detection and safe tool usage validation
- CrewAI: Multi-agent system with Analyst, Estimator, and Reviewer agents
- AutoGen: Conversational agents with human-in-the-loop and code execution
"""

from .simple_agent import (
    AgentState,
    AgentTransition,
    AgentContext,
    SimpleAgent,
)

from .memory import (
    MemoryItem,
    BaseMemory,
    ShortTermMemory,
    LongTermMemory,
    SummarizationMemory,
)

from .safety import (
    InjectionDetectionResult,
    ToolUsageValidationResult,
    detect_prompt_injection,
    validate_tool_usage,
    sanitize_user_input,
    INJECTION_PATTERNS,
    DANGEROUS_PATH_PATTERNS,
    DANGEROUS_COMMAND_PATTERNS,
    HIGH_RISK_TOOLS,
    BLOCKED_TOOLS,
)

from .crewai_agents import (
    EstimationResult,
    FeatureSearchTool,
    EstimationTool,
    ValidationTool,
    create_analyst_agent,
    create_estimator_agent,
    create_reviewer_agent,
    create_estimation_crew,
    run_estimation_workflow,
    get_mock_llm_config,
    CREWAI_AVAILABLE,
)

from .autogen_agents import (
    ConversationResult,
    create_estimation_assistant,
    create_user_proxy,
    create_group_chat,
    run_estimation_conversation,
    run_group_estimation,
    add_code_execution_tool,
    AUTOGEN_AVAILABLE,
)

__all__ = [
    # Agent components
    "AgentState",
    "AgentTransition",
    "AgentContext",
    "SimpleAgent",
    # Memory components
    "MemoryItem",
    "BaseMemory",
    "ShortTermMemory",
    "LongTermMemory",
    "SummarizationMemory",
    # Safety components
    "InjectionDetectionResult",
    "ToolUsageValidationResult",
    "detect_prompt_injection",
    "validate_tool_usage",
    "sanitize_user_input",
    "INJECTION_PATTERNS",
    "DANGEROUS_PATH_PATTERNS",
    "DANGEROUS_COMMAND_PATTERNS",
    "HIGH_RISK_TOOLS",
    "BLOCKED_TOOLS",
    # CrewAI multi-agent components
    "EstimationResult",
    "FeatureSearchTool",
    "EstimationTool",
    "ValidationTool",
    "create_analyst_agent",
    "create_estimator_agent",
    "create_reviewer_agent",
    "create_estimation_crew",
    "run_estimation_workflow",
    "get_mock_llm_config",
    "CREWAI_AVAILABLE",
    # AutoGen conversational agents
    "ConversationResult",
    "create_estimation_assistant",
    "create_user_proxy",
    "create_group_chat",
    "run_estimation_conversation",
    "run_group_estimation",
    "add_code_execution_tool",
    "AUTOGEN_AVAILABLE",
]
