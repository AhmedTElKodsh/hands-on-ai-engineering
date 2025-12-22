"""AutoGen conversational agents for AITEA estimation workflow.

This module implements a conversational multi-agent system using Microsoft's
AutoGen framework. The system supports:
- AssistantAgent: AI agent for estimation tasks
- UserProxyAgent: Human-in-the-loop proxy with code execution
- GroupChat: Multi-agent conversations with dynamic speaker selection

AutoGen enables natural conversational workflows where agents can:
- Discuss and refine estimates collaboratively
- Execute code for calculations and data analysis
- Request human input at critical decision points
- Maintain conversation context across multiple turns
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
import json

try:
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    from autogen.agentchat import Agent as AutoGenAgent
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    # Define placeholder classes for type hints when AutoGen is not installed
    AssistantAgent = Any
    UserProxyAgent = Any
    GroupChat = Any
    GroupChatManager = Any
    AutoGenAgent = Any

from ..services import (
    IFeatureLibraryService,
    IEstimationService,
    ITimeTrackingService,
)
from ..models import Feature, ProjectEstimate, FeatureEstimate


@dataclass
class ConversationResult:
    """Result of a multi-agent conversation.
    
    Attributes:
        messages: List of conversation messages
        final_estimate: Final project estimate if produced
        summary: Summary of the conversation
        human_inputs: List of human inputs provided during conversation
    """
    messages: List[Dict[str, Any]]
    final_estimate: Optional[ProjectEstimate]
    summary: str
    human_inputs: List[str]


def create_estimation_assistant(
    feature_service: IFeatureLibraryService,
    estimation_service: IEstimationService,
    llm_config: Optional[Dict[str, Any]] = None,
    name: str = "EstimationAssistant",
) -> AssistantAgent:
    """Create an AssistantAgent for estimation tasks.
    
    The AssistantAgent is an AI-powered agent that can:
    - Search the feature library for similar features
    - Compute time estimates based on historical data
    - Explain estimation methodology
    - Suggest improvements to estimates
    
    Args:
        feature_service: Service for accessing the feature library
        estimation_service: Service for computing estimates
        llm_config: LLM configuration (model, temperature, etc.)
        name: Name for the assistant agent
        
    Returns:
        Configured AssistantAgent
        
    Raises:
        ImportError: If AutoGen is not installed
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    # Default LLM config if not provided
    if llm_config is None:
        llm_config = {
            "model": "gpt-4",
            "temperature": 0.7,
            "timeout": 120,
        }
    
    # System message defines the agent's role and capabilities
    system_message = """You are an AI estimation assistant specializing in software development time estimation.

Your capabilities:
1. Search the feature library for similar historical features
2. Compute statistical estimates (mean, median, P80) from historical data
3. Explain estimation methodology and confidence levels
4. Identify risks and suggest improvements

When estimating:
- Always search for similar features first
- Use historical data when available
- Clearly state confidence levels (low/medium/high)
- Explain your reasoning
- Flag estimates that deviate from historical normssearch for similar features first
- Use historical data when available
- Clearly state confidence levels (low/medium/high)
- Explain your reasoning
- Flag estimates that deviate from historical norms

Available functions:
- search_features(query: str) -> List[Feature]
- estimate_feature(feature_name: str) -> FeatureEstimate
- estimate_project(feature_names: List[str]) -> ProjectEstimate

Be conversational, helpful, and transparent about limitations."""
    
    # Create function definitions for the agent
    functions = [
        {
            "name": "search_features",
            "description": "Search the feature library for matching features",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "estimate_feature",
            "description": "Estimate time for a specific feature based on historical data",
            "parameters": {
                "type": "object",
                "properties": {
                    "feature_name": {
                        "type": "string",
                        "description": "Name of the feature to estimate"
                    }
                },
                "required": ["feature_name"]
            }
        },
        {
            "name": "estimate_project",
            "description": "Estimate total time for a project with multiple features",
            "parameters": {
                "type": "object",
                "properties": {
                    "feature_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of feature names to estimate"
                    }
                },
                "required": ["feature_names"]
            }
        }
    ]
    
    # Add functions to LLM config
    llm_config_with_functions = llm_config.copy()
    llm_config_with_functions["functions"] = functions
    
    # Create the assistant agent
    assistant = AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=llm_config_with_functions,
    )
    
    # Register function implementations
    def search_features_impl(query: str) -> str:
        """Implementation of search_features function."""
        features = feature_service.search_features(query)
        if not features:
            return f"No features found matching '{query}'"
        
        result = f"Found {len(features)} matching features:\n"
        for feature in features[:5]:  # Limit to top 5
            result += f"- {feature.name} ({feature.team.value}): {feature.seed_time_hours}h seed time\n"
            if feature.synonyms:
                result += f"  Synonyms: {', '.join(feature.synonyms)}\n"
        
        if len(features) > 5:
            result += f"... and {len(features) - 5} more\n"
        
        return result
    
    def estimate_feature_impl(feature_name: str) -> str:
        """Implementation of estimate_feature function."""
        result = estimation_service.estimate_feature(feature_name)
        if result.is_err():
            return f"Error estimating '{feature_name}': {result.unwrap_err()}"
        
        estimate = result.unwrap()
        output = f"Estimate for '{feature_name}':\n"
        output += f"- Estimated hours: {estimate.estimated_hours}h\n"
        output += f"- Confidence: {estimate.confidence.value}\n"
        
        if estimate.statistics:
            stats = estimate.statistics
            output += f"\nStatistics from {stats.data_point_count} data points:\n"
            output += f"- Mean: {stats.mean:.1f}h\n"
            output += f"- Median: {stats.median:.1f}h\n"
            output += f"- P80: {stats.p80:.1f}h\n"
            output += f"- Std Dev: {stats.std_dev:.1f}h\n"
        else:
            output += "\nUsing seed time (limited historical data)\n"
        
        return output
    
    def estimate_project_impl(feature_names: List[str]) -> str:
        """Implementation of estimate_project function."""
        result = estimation_service.estimate_project(feature_names)
        if result.is_err():
            return f"Error estimating project: {result.unwrap_err()}"
        
        estimate = result.unwrap()
        output = f"Project Estimate:\n"
        output += f"Total hours: {estimate.total_hours}h\n"
        output += f"Overall confidence: {estimate.confidence.value}\n\n"
        output += "Feature breakdown:\n"
        
        for feat_est in estimate.features:
            output += f"- {feat_est.feature_name}: {feat_est.estimated_hours}h "
            output += f"({feat_est.confidence.value} confidence)\n"
        
        return output
    
    # Register functions with the assistant
    assistant.register_function(
        function_map={
            "search_features": search_features_impl,
            "estimate_feature": estimate_feature_impl,
            "estimate_project": estimate_project_impl,
        }
    )
    
    return assistant


def create_user_proxy(
    name: str = "ProjectManager",
    human_input_mode: str = "TERMINATE",
    max_consecutive_auto_reply: int = 10,
    code_execution_config: Optional[Dict[str, Any]] = None,
) -> UserProxyAgent:
    """Create a UserProxyAgent with human-in-the-loop capabilities.
    
    The UserProxyAgent acts as a proxy for human users and can:
    - Execute code in a sandboxed environment
    - Request human input at decision points
    - Terminate conversations when goals are met
    - Validate agent outputs
    
    Args:
        name: Name for the user proxy agent
        human_input_mode: When to request human input:
            - "ALWAYS": Request input for every message
            - "TERMINATE": Request input only when termination is suggested
            - "NEVER": Never request input (fully autonomous)
        max_consecutive_auto_reply: Maximum auto-replies before requesting input
        code_execution_config: Configuration for code execution:
            - work_dir: Directory for code execution
            - use_docker: Whether to use Docker for sandboxing
            - timeout: Execution timeout in seconds
            
    Returns:
        Configured UserProxyAgent
        
    Raises:
        ImportError: If AutoGen is not installed
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    # Default code execution config if not provided
    if code_execution_config is None:
        code_execution_config = {
            "work_dir": "workspace",
            "use_docker": False,  # Set to True for better sandboxing
            "timeout": 60,
            "last_n_messages": 3,
        }
    
    # System message for the user proxy
    system_message = """You are a project manager working with an AI estimation assistant.

Your role:
- Review estimates provided by the assistant
- Ask clarifying questions when needed
- Validate that estimates are reasonable
- Request human input for critical decisions
- Execute code to verify calculations

When reviewing estimates:
- Check if confidence levels are appropriate
- Verify that similar features were considered
- Question estimates that seem too high or too low
- Ensure all requested features are estimated

Reply "TERMINATE" when you are satisfied with the estimates."""
    
    user_proxy = UserProxyAgent(
        name=name,
        system_message=system_message,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        code_execution_config=code_execution_config,
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(),
    )
    
    return user_proxy


def create_group_chat(
    agents: List[AutoGenAgent],
    max_round: int = 10,
    admin_name: str = "Admin",
    speaker_selection_method: str = "auto",
) -> tuple[GroupChat, GroupChatManager]:
    """Create a GroupChat for multi-agent conversations.
    
    GroupChat enables multiple agents to converse with dynamic speaker selection.
    The system can automatically select the next speaker based on context or
    use a round-robin approach.
    
    Args:
        agents: List of agents participating in the group chat
        max_round: Maximum number of conversation rounds
        admin_name: Name for the admin/manager agent
        speaker_selection_method: Method for selecting next speaker:
            - "auto": Automatically select based on context
            - "round_robin": Rotate through agents in order
            - "manual": Request human selection
            
    Returns:
        Tuple of (GroupChat, GroupChatManager)
        
    Raises:
        ImportError: If AutoGen is not installed
        ValueError: If agents list is empty
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    if not agents:
        raise ValueError("At least one agent is required for group chat")
    
    # Create the group chat
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=max_round,
        speaker_selection_method=speaker_selection_method,
    )
    
    # Create the manager to orchestrate the conversation
    manager = GroupChatManager(
        groupchat=group_chat,
        name=admin_name,
    )
    
    return group_chat, manager


def run_estimation_conversation(
    initial_message: str,
    feature_service: IFeatureLibraryService,
    estimation_service: IEstimationService,
    human_input_mode: str = "TERMINATE",
    llm_config: Optional[Dict[str, Any]] = None,
) -> ConversationResult:
    """Run a conversational estimation workflow.
    
    This creates an assistant and user proxy, then initiates a conversation
    about estimating features. The conversation continues until the user
    proxy terminates it.
    
    Args:
        initial_message: Initial message to start the conversation
        feature_service: Service for accessing the feature library
        estimation_service: Service for computing estimates
        human_input_mode: When to request human input
        llm_config: LLM configuration
        
    Returns:
        ConversationResult with messages and final estimate
        
    Raises:
        ImportError: If AutoGen is not installed
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    # Create agents
    assistant = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
    )
    
    user_proxy = create_user_proxy(
        human_input_mode=human_input_mode,
    )
    
    # Initiate the conversation
    user_proxy.initiate_chat(
        assistant,
        message=initial_message,
    )
    
    # Extract conversation results
    messages = user_proxy.chat_messages[assistant]
    
    # Try to extract final estimate from conversation
    final_estimate = None
    for msg in reversed(messages):
        content = msg.get("content", "")
        if "Total hours:" in content or "Project Estimate:" in content:
            # Found an estimate in the conversation
            # In a real implementation, you'd parse this more carefully
            break
    
    # Create summary
    summary = f"Conversation completed with {len(messages)} messages"
    
    # Collect human inputs (if any)
    human_inputs = [
        msg.get("content", "")
        for msg in messages
        if msg.get("role") == "user" and msg.get("name") == user_proxy.name
    ]
    
    return ConversationResult(
        messages=messages,
        final_estimate=final_estimate,
        summary=summary,
        human_inputs=human_inputs,
    )


def run_group_estimation(
    initial_message: str,
    feature_service: IFeatureLibraryService,
    estimation_service: IEstimationService,
    llm_config: Optional[Dict[str, Any]] = None,
    max_round: int = 10,
) -> ConversationResult:
    """Run a group chat estimation workflow with multiple agents.
    
    This creates multiple specialized agents that discuss and refine
    estimates collaboratively:
    - Analyst: Focuses on feature extraction and clarification
    - Estimator: Provides time estimates
    - Reviewer: Validates estimates and identifies risks
    - User Proxy: Represents the human user
    
    Args:
        initial_message: Initial message to start the conversation
        feature_service: Service for accessing the feature library
        estimation_service: Service for computing estimates
        llm_config: LLM configuration
        max_round: Maximum conversation rounds
        
    Returns:
        ConversationResult with messages and final estimate
        
    Raises:
        ImportError: If AutoGen is not installed
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    # Create specialized agents
    analyst = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Analyst",
    )
    analyst.update_system_message(
        "You are a requirements analyst. Focus on understanding and clarifying "
        "features. Search for similar features in the library. Ask questions "
        "to ensure features are well-defined before estimation."
    )
    
    estimator = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Estimator",
    )
    estimator.update_system_message(
        "You are an estimation specialist. Provide time estimates based on "
        "historical data. Use statistical methods and clearly communicate "
        "confidence levels. Explain your reasoning."
    )
    
    reviewer = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Reviewer",
    )
    reviewer.update_system_message(
        "You are an estimate reviewer. Validate estimates against historical "
        "data. Identify risks, outliers, and missing features. Provide "
        "constructive feedback to improve estimate accuracy."
    )
    
    user_proxy = create_user_proxy(
        name="ProjectManager",
        human_input_mode="TERMINATE",
    )
    
    # Create group chat
    agents = [analyst, estimator, reviewer, user_proxy]
    group_chat, manager = create_group_chat(
        agents=agents,
        max_round=max_round,
        speaker_selection_method="auto",
    )
    
    # Start the group conversation
    user_proxy.initiate_chat(
        manager,
        message=initial_message,
    )
    
    # Extract results
    messages = group_chat.messages
    
    summary = f"Group chat completed with {len(messages)} messages across {len(agents)} agents"
    
    human_inputs = [
        msg.get("content", "")
        for msg in messages
        if msg.get("name") == user_proxy.name
    ]
    
    return ConversationResult(
        messages=messages,
        final_estimate=None,
        summary=summary,
        human_inputs=human_inputs,
    )


def add_code_execution_tool(
    user_proxy: UserProxyAgent,
    allowed_operations: Optional[List[str]] = None,
) -> None:
    """Add code execution capabilities to a UserProxyAgent.
    
    This enables the agent to execute Python code for:
    - Statistical calculations
    - Data analysis
    - Validation checks
    - Custom computations
    
    Code execution is sandboxed for safety.
    
    Args:
        user_proxy: UserProxyAgent to enhance with code execution
        allowed_operations: List of allowed operations (for safety)
            If None, allows common safe operations
            
    Raises:
        ImportError: If AutoGen is not installed
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError(
            "AutoGen is not installed. Install it with: pip install pyautogen"
        )
    
    if allowed_operations is None:
        allowed_operations = [
            "math",
            "statistics",
            "numpy",
            "pandas",
            "json",
        ]
    
    # Update code execution config to enable sandboxing
    if user_proxy.code_execution_config:
        user_proxy.code_execution_config["use_docker"] = True
        user_proxy.code_execution_config["timeout"] = 60
        
        # Add safety restrictions
        user_proxy.code_execution_config["allowed_imports"] = allowed_operations


# Example usage
def example_usage():
    """Example of how to use AutoGen conversational agents.
    
    This demonstrates the typical workflow for using AutoGen agents
    with AITEA services.
    """
    if not AUTOGEN_AVAILABLE:
        print("AutoGen is not installed. Install it with: pip install pyautogen")
        return
    
    print("Example: AutoGen Conversational Agents")
    print("=" * 60)
    print()
    print("1. Simple conversation with assistant:")
    print("   assistant = create_estimation_assistant(feature_service, estimation_service)")
    print("   user_proxy = create_user_proxy(human_input_mode='TERMINATE')")
    print("   user_proxy.initiate_chat(assistant, message='Estimate CRUD feature')")
    print()
    print("2. Group chat with multiple agents:")
    print("   result = run_group_estimation(")
    print("       'Estimate features: CRUD, Authentication, Search',")
    print("       feature_service,")
    print("       estimation_service")
    print("   )")
    print()
    print("3. Code execution for validation:")
    print("   user_proxy = create_user_proxy()")
    print("   add_code_execution_tool(user_proxy)")
    print("   # Agent can now execute Python code for calculations")
    print()
    print("Key features:")
    print("  - Conversational interface for natural interaction")
    print("  - Human-in-the-loop at critical decision points")
    print("  - Code execution for calculations and validation")
    print("  - Multi-agent collaboration with dynamic speaker selection")
    print()


if __name__ == "__main__":
    example_usage()
