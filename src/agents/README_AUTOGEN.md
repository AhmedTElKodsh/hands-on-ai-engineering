# AutoGen Conversational Agents for AITEA

This module implements conversational multi-agent systems using Microsoft's AutoGen framework. AutoGen enables natural, human-like conversations between AI agents and humans, with support for code execution, tool calling, and dynamic multi-agent collaboration.

## Overview

AutoGen provides a conversational interface for AI agents that can:

- Engage in natural back-and-forth conversations
- Execute code in sandboxed environments
- Request human input at critical decision points
- Collaborate with multiple agents in group chats
- Maintain conversation context across multiple turns

## Key Components

### 1. AssistantAgent

AI-powered agent that can use tools and engage in conversations:

```python
from src.agents import create_estimation_assistant

assistant = create_estimation_assistant(
    feature_service=feature_library,
    estimation_service=estimator,
    llm_config={
        "model": "gpt-4",
        "temperature": 0.7,
    }
)
```

The assistant can:

- Search the feature library
- Compute time estimates
- Explain estimation methodology
- Suggest improvements

### 2. UserProxyAgent

Proxy for human users with code execution capabilities:

```python
from src.agents import create_user_proxy

user_proxy = create_user_proxy(
    name="ProjectManager",
    human_input_mode="TERMINATE",  # Request input only at termination
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False,
        "timeout": 60,
    }
)
```

Human input modes:

- `ALWAYS`: Request input for every message
- `TERMINATE`: Request input only when termination is suggested
- `NEVER`: Fully autonomous (no human input)

### 3. GroupChat

Multi-agent conversations with dynamic speaker selection:

```python
from src.agents import create_group_chat

agents = [analyst, estimator, reviewer, user_proxy]
group_chat, manager = create_group_chat(
    agents=agents,
    max_round=10,
    speaker_selection_method="auto"
)
```

Speaker selection methods:

- `auto`: Automatically select based on context
- `round_robin`: Rotate through agents in order
- `manual`: Request human selection

## Usage Examples

### Simple Conversation

```python
from src.agents import run_estimation_conversation
from src.services import FeatureLibraryService, EstimationService

# Initialize services
feature_service = FeatureLibraryService()
estimation_service = EstimationService(...)

# Run conversation
result = run_estimation_conversation(
    initial_message="I need to estimate a CRUD feature for a backend API",
    feature_service=feature_service,
    estimation_service=estimation_service,
    human_input_mode="TERMINATE"
)

print(f"Conversation summary: {result.summary}")
print(f"Messages exchanged: {len(result.messages)}")
```

### Group Chat with Multiple Agents

```python
from src.agents import run_group_estimation

result = run_group_estimation(
    initial_message="Estimate these features: CRUD, Authentication, Search",
    feature_service=feature_service,
    estimation_service=estimation_service,
    max_round=10
)

# The group includes:
# - Analyst: Clarifies features
# - Estimator: Provides estimates
# - Reviewer: Validates estimates
# - User Proxy: Represents the human
```

### Code Execution

```python
from src.agents import create_user_proxy, add_code_execution_tool

user_proxy = create_user_proxy()

# Enable code execution with safety restrictions
add_code_execution_tool(
    user_proxy,
    allowed_operations=["math", "statistics", "numpy", "pandas"]
)

# Now the agent can execute Python code for calculations
```

## Conversation Flow

### 1. Simple Two-Agent Conversation

```
User Proxy: "Estimate CRUD feature"
    ↓
Assistant: [Searches feature library]
           "Found 5 similar features. Mean: 4.2h, Median: 4.0h"
    ↓
User Proxy: "What's the confidence level?"
    ↓
Assistant: "High confidence (12 data points)"
    ↓
User Proxy: "TERMINATE"
```

### 2. Group Chat Conversation

```
User Proxy: "Estimate CRUD, Auth, Search"
    ↓
Analyst: [Searches library]
         "CRUD: Found 12 matches
          Auth: Found 8 matches
          Search: Found 5 matches"
    ↓
Estimator: [Computes estimates]
           "CRUD: 4.2h (high confidence)
            Auth: 6.5h (medium confidence)
            Search: 8.0h (low confidence)"
    ↓
Reviewer: [Validates estimates]
          "CRUD and Auth look good.
           Search estimate is 2 std devs above mean.
           Recommend investigating complexity."
    ↓
User Proxy: "TERMINATE"
```

## Comparison with CrewAI

| Feature                | AutoGen                          | CrewAI                                  |
| ---------------------- | -------------------------------- | --------------------------------------- |
| **Conversation Style** | Natural, back-and-forth          | Task-based, sequential                  |
| **Human-in-the-Loop**  | Built-in, flexible               | Limited                                 |
| **Code Execution**     | Native support                   | Requires custom tools                   |
| **Multi-Agent**        | Dynamic speaker selection        | Fixed process (sequential/hierarchical) |
| **Learning Curve**     | Moderate                         | Easy                                    |
| **Best For**           | Interactive workflows, debugging | Production pipelines                    |

## When to Use AutoGen

Use AutoGen when you need:

- **Interactive conversations**: Natural back-and-forth with users
- **Human oversight**: Critical decisions require human approval
- **Code execution**: Agents need to run calculations or scripts
- **Flexible workflows**: Dynamic agent selection based on context
- **Debugging**: Step-by-step conversation helps identify issues

Use CrewAI when you need:

- **Production pipelines**: Automated, repeatable workflows
- **Role-based teams**: Clear agent roles and responsibilities
- **Sequential processes**: Fixed order of operations
- **Simpler setup**: Quick to configure and deploy

## Advanced Features

### Custom Function Registration

```python
assistant = create_estimation_assistant(...)

# Register custom functions
def custom_analysis(data: str) -> str:
    # Your custom logic
    return result

assistant.register_function(
    function_map={"custom_analysis": custom_analysis}
)
```

### Conversation Termination

```python
user_proxy = create_user_proxy(
    is_termination_msg=lambda msg: "DONE" in msg.get("content", "").upper()
)
```

### Docker Sandboxing

For production use, enable Docker for safer code execution:

```python
user_proxy = create_user_proxy(
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": True,  # Requires Docker installed
        "timeout": 60,
    }
)
```

## Error Handling

AutoGen handles errors gracefully:

```python
try:
    result = run_estimation_conversation(...)
except ImportError:
    print("AutoGen not installed. Install with: pip install pyautogen")
except Exception as e:
    print(f"Conversation error: {e}")
```

## Installation

```bash
# Install AutoGen
pip install pyautogen

# Or install with AITEA agents extras
pip install -e ".[agents]"
```

## Testing

AutoGen agents can be tested with mock LLMs:

```python
llm_config = {
    "model": "mock",
    "temperature": 0.7,
}

assistant = create_estimation_assistant(
    feature_service,
    estimation_service,
    llm_config=llm_config
)
```

## Best Practices

1. **Set clear termination conditions**: Define when conversations should end
2. **Limit max rounds**: Prevent infinite conversations
3. **Use Docker for code execution**: Sandbox untrusted code
4. **Monitor conversation length**: Long conversations can be expensive
5. **Provide clear system messages**: Help agents understand their roles
6. **Test with mock LLMs first**: Validate logic before using real APIs
7. **Log conversations**: Keep records for debugging and improvement

## Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [AutoGen Examples](https://github.com/microsoft/autogen/tree/main/notebook)

## Next Steps

After implementing AutoGen agents, consider:

1. Implementing Strands Agents SDK (Task 45)
2. Creating MCP tool definitions (Task 46)
3. Building a framework comparison guide (Task 47)
