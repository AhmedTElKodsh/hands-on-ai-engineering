# LangGraph BRD Parser Agent

## Overview

The BRD Parser Agent is a LangGraph-based agent that parses Business Requirements Documents (BRDs) and extracts features with time estimates. It demonstrates advanced LangGraph concepts including:

- **StateGraph**: Multi-node workflow orchestration
- **Conditional Edges**: Dynamic workflow control based on state
- **Memory Persistence**: State preservation across runs
- **Human-in-the-Loop**: Interactive review and feedback
- **Streaming**: Real-time progress updates

## Requirements

This implementation satisfies **Requirement 6.4**:

> WHEN the learner completes Chapter 34 THEN the System SHALL produce a LangGraph agent with StateGraph, nodes, conditional edges, memory, and human-in-the-loop support

## Architecture

### Workflow Graph

```
┌─────────────────┐
│ extract_features│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│validate_features│
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│identify_clarifications│
└──────────┬───────────┘
           │
           ├─── needs_human_review? ───┐
           │                            │
           ▼ (yes)                      ▼ (no)
┌──────────────────────┐      ┌─────────────────┐
│request_human_review  │      │finalize_results │
└──────────┬───────────┘      └────────┬────────┘
           │                            │
           └────────────────────────────┤
                                        ▼
                                      [END]
```

### Nodes

1. **extract_features**: Extracts features from BRD text using LLM
2. **validate_features**: Validates extracted features for completeness
3. **identify_clarifications**: Identifies items needing clarification
4. **request_human_review**: Requests human feedback (human-in-the-loop)
5. **finalize_results**: Packages final results

### Conditional Edges

The agent uses a conditional edge after `identify_clarifications`:

- If `needs_human_review == True` → go to `request_human_review`
- If `needs_human_review == False` → go to `finalize_results`

This demonstrates dynamic workflow control based on state.

### State Schema

```python
class AgentState(TypedDict):
    # Input
    brd_text: str

    # Messages for conversation history
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # Extracted features (accumulated)
    features: Annotated[List[ExtractedFeature], operator.add]

    # Items needing clarification
    clarifications_needed: Annotated[List[str], operator.add]

    # Current step in the workflow
    current_step: str

    # Whether human review is needed
    needs_human_review: bool

    # Human feedback (if provided)
    human_feedback: Optional[str]

    # Final result
    result: Optional[BRDParseResult]
```

## Installation

```bash
pip install langgraph langchain-core langchain-openai
```

## Usage

### Basic Usage

```python
from langchain_openai import ChatOpenAI
from src.langchain import create_brd_parser_agent

# Create LLM
llm = ChatOpenAI(model="gpt-4")

# Create agent
agent = create_brd_parser_agent(llm)

# Parse BRD
brd_text = """
# Project Requirements

## Feature 1: User Authentication
Implement JWT-based authentication.
Team: Backend
Estimate: 40 hours
"""

result = agent.parse_brd(brd_text)

# Display results
print(f"Features: {result.total_features}")
print(f"Total hours: {result.total_hours}")

for feature in result.features:
    print(f"- {feature.name}: {feature.estimated_hours}h")
```

### Streaming Updates

```python
# Stream progress updates
for state_update in agent.parse_brd_stream(brd_text):
    for node_name, node_state in state_update.items():
        step = node_state.get("current_step", "unknown")
        print(f"Step: {step}")
```

### With Memory Persistence

```python
# Create agent with memory
agent = create_brd_parser_agent(llm, enable_memory=True)

# First run
result1 = agent.parse_brd(brd_text, thread_id="project-123")

# Second run - memory preserved
result2 = agent.parse_brd(brd_text, thread_id="project-123")
```

### Human-in-the-Loop

```python
# Parse and provide human feedback
result = agent.parse_brd(
    brd_text,
    human_feedback="Approved - estimates look reasonable"
)
```

## Data Models

### ExtractedFeature

```python
class ExtractedFeature(BaseModel):
    name: str
    description: str
    team: str
    estimated_hours: float
    confidence: str  # "low", "medium", "high"
    dependencies: List[str]
```

### BRDParseResult

```python
class BRDParseResult(BaseModel):
    features: List[ExtractedFeature]
    total_features: int
    total_hours: float
    needs_clarification: List[str]
```

## Examples

See `examples_brd_parser.py` for comprehensive examples:

1. **Basic Parsing**: Simple BRD parsing
2. **Streaming**: Real-time progress updates
3. **Memory**: State persistence across runs
4. **Human-in-the-Loop**: Interactive review workflow
5. **Workflow Visualization**: Understanding the graph structure

Run examples:

```python
from src.langchain.examples_brd_parser import run_all_examples
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
run_all_examples(llm)
```

## Testing

Run tests:

```bash
pytest tests/langchain/test_brd_parser_agent.py -v
```

Tests cover:

- Agent creation
- Node execution
- Conditional edges
- Memory persistence
- Human-in-the-loop workflow
- Data model validation

## Key Concepts Demonstrated

### 1. StateGraph

LangGraph's `StateGraph` orchestrates the workflow:

```python
workflow = StateGraph(AgentState)
workflow.add_node("extract_features", self._extract_features_node)
workflow.add_node("validate_features", self._validate_features_node)
# ... more nodes
```

### 2. Conditional Edges

Dynamic routing based on state:

```python
workflow.add_conditional_edges(
    "identify_clarifications",
    self._should_request_human_review,
    {
        "human_review": "request_human_review",
        "finalize": "finalize_results"
    }
)
```

### 3. Memory Persistence

State preservation using `MemorySaver`:

```python
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
```

### 4. Human-in-the-Loop

Pausing for human input:

```python
def _request_human_review_node(self, state: AgentState):
    # Request human feedback
    # In production, this would pause and wait for user input
    feedback = state.get("human_feedback", "default")
    # Process feedback and continue
```

### 5. Streaming

Real-time progress updates:

```python
for state in graph.stream(initial_state, config):
    # Process each state update
    print(f"Step: {state['current_step']}")
```

## Integration with AITEA

The BRD Parser Agent integrates with AITEA core services:

1. **Feature Extraction**: Extracts features that can be added to the Feature Library
2. **Time Estimation**: Provides initial estimates that can be refined with historical data
3. **Validation**: Ensures extracted features meet AITEA's data model requirements
4. **Human Review**: Allows project managers to validate and adjust estimates

## Advanced Patterns

### Custom Node Logic

Each node can implement complex logic:

```python
def _extract_features_node(self, state: AgentState):
    # Custom extraction logic
    # Can call multiple LLMs, tools, or services
    # Returns updated state
    return {
        "features": extracted_features,
        "messages": [response],
        "current_step": "extract_features"
    }
```

### State Accumulation

Using `Annotated` with `operator.add` for accumulation:

```python
features: Annotated[List[ExtractedFeature], operator.add]
# New features are appended, not replaced
```

### Error Handling

Nodes can handle errors and update state accordingly:

```python
try:
    features = extract_features(brd_text)
except Exception as e:
    return {
        "clarifications_needed": [f"Error: {str(e)}"],
        "needs_human_review": True
    }
```

## Comparison with Other Patterns

| Pattern         | Use Case                         | Complexity |
| --------------- | -------------------------------- | ---------- |
| **LCEL Chains** | Linear workflows                 | Low        |
| **LangGraph**   | Complex workflows with branching | Medium     |
| **ReAct Agent** | Tool-based reasoning             | Medium     |
| **Multi-Agent** | Specialized agent collaboration  | High       |

LangGraph is ideal when you need:

- Multiple decision points
- State persistence
- Human-in-the-loop
- Complex workflow orchestration

## Future Enhancements

Potential improvements:

1. **Tool Integration**: Add tools for database lookup, API calls
2. **Multi-Agent**: Decompose into specialized agents (extractor, validator, estimator)
3. **Parallel Execution**: Process multiple BRD sections concurrently
4. **Advanced Memory**: Use vector store for semantic memory
5. **Evaluation**: Add metrics for extraction quality

## References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [StateGraph Guide](https://langchain-ai.github.io/langgraph/concepts/low_level/)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
- [Memory & Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)

## License

Part of the AITEA curriculum project.
