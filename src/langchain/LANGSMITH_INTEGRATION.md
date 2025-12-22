# LangSmith Integration for AITEA

This document describes the LangSmith observability integration for AITEA, providing tracing, evaluation, and dataset management capabilities.

## Overview

LangSmith is a platform for observability, evaluation, and prompt engineering for LLM applications. The AITEA LangSmith integration provides:

- **Tracing**: Automatic tracing of chain and agent executions
- **Evaluation**: Evaluate chains/agents against test datasets
- **Dataset Management**: Create and manage test datasets for evaluation

## Setup

### 1. Install Dependencies

LangSmith is included in the langchain package dependencies:

```bash
pip install langsmith
```

### 2. Get API Key

1. Sign up at [smith.langchain.com](https://smith.langchain.com)
2. Create an API key in your settings
3. Set the environment variable:

```bash
export LANGSMITH_API_KEY='your-api-key-here'
```

### 3. Configure LangSmith

```python
from langchain.observability import configure_langsmith

# Configure with explicit settings
config = configure_langsmith(
    api_key="your-api-key",  # Optional if env var is set
    project="aitea",         # Project name for organizing traces
    tracing_enabled=True,    # Enable/disable tracing
)

# Or auto-configure from environment
# Just set LANGSMITH_API_KEY and it auto-configures on import
```

## Features

### 1. Automatic Tracing

#### Trace Chains

Use the `@trace_chain` decorator to automatically trace chain executions:

```python
from langchain.observability import trace_chain
from langchain.chains import create_feature_extraction_chain

@trace_chain(name="feature_extraction", tags=["extraction", "brd"])
def extract_features(brd_text: str):
    chain = create_feature_extraction_chain()
    return chain.invoke({"brd_text": brd_text})

# Execution is automatically traced
result = extract_features("Build a login feature")
```

#### Trace Agents

Use the `@trace_agent` decorator for agent executions:

```python
from langchain.observability import trace_agent
from langchain.brd_parser_agent import create_brd_parser_agent

@trace_agent(name="brd_parser", tags=["agent", "parsing"])
def parse_brd(brd_text: str):
    agent = create_brd_parser_agent()
    return agent.invoke({"brd_text": brd_text})

# Agent execution is automatically traced
result = parse_brd("Project requirements...")
```

#### Manual Tracing

For more control, use the tracer directly:

```python
from langchain.observability import get_tracer

tracer = get_tracer()
chain = create_feature_extraction_chain()

result = chain.invoke(
    {"brd_text": "Build a payment system"},
    config={"callbacks": [tracer]}
)
```

### 2. Evaluation

#### Create Evaluators

Create custom evaluators for your domain:

```python
from langchain.observability import create_evaluator

def check_features(expected, actual):
    """Check if extracted features match expected."""
    expected_features = set(expected.get("features", []))
    actual_features = set(f["name"] for f in actual.get("features", []))

    overlap = len(expected_features & actual_features)
    return overlap / len(expected_features) >= 0.8

evaluator = create_evaluator(
    name="feature_accuracy",
    evaluator_fn=check_features,
    description="Checks if at least 80% of features match",
)
```

#### Evaluate Chains

Evaluate a chain against a test dataset:

```python
from langchain.observability import evaluate_chain

chain = create_feature_extraction_chain()

result = evaluate_chain(
    chain,
    dataset_name="feature_extraction_test",
    evaluators=[feature_accuracy_evaluator],
)

print(result)
# Evaluation Results for 'feature_extraction_test':
#   Examples: 10
#   Passed: 8 (80.0%)
#   Failed: 2 (20.0%)
#   Accuracy: 0.800
#   Avg Latency: 1250ms
#   Token Usage: 5420
```

#### Evaluate Agents

Agent evaluation works the same way:

```python
from langchain.observability import evaluate_agent

agent = create_brd_parser_agent()

result = evaluate_agent(
    agent,
    dataset_name="brd_parsing_test",
    evaluators=[feature_extraction_evaluator],
)
```

### 3. Dataset Management

#### Create Datasets

Create test datasets for evaluation:

```python
from langchain.observability import create_dataset, DatasetExample

examples = [
    DatasetExample(
        inputs={"brd_text": "Build a login feature"},
        outputs={"features": ["authentication", "login"]},
        metadata={"category": "auth"},
    ),
    DatasetExample(
        inputs={"brd_text": "Create a CRUD API"},
        outputs={"features": ["CRUD", "api"]},
        metadata={"category": "data"},
    ),
]

dataset_id = create_dataset(
    name="feature_extraction_test",
    description="Test cases for feature extraction",
    examples=examples,
)
```

#### Add Examples

Add more examples to an existing dataset:

```python
from langchain.observability import add_examples

new_examples = [
    DatasetExample(
        inputs={"brd_text": "Implement WebSocket chat"},
        outputs={"features": ["websocket", "chat"]},
    ),
]

count = add_examples("feature_extraction_test", new_examples)
print(f"Added {count} examples")
```

#### Get Dataset

Retrieve a dataset:

```python
from langchain.observability import get_dataset

dataset = get_dataset("feature_extraction_test")
if dataset:
    print(f"Dataset has {len(dataset.examples)} examples")
```

## Built-in Evaluators

AITEA provides several pre-built evaluators:

### Feature Extraction Evaluator

Checks if extracted features match expected features (80% threshold):

```python
from langchain.observability import create_feature_extraction_evaluator

evaluator = create_feature_extraction_evaluator()
```

### Estimation Accuracy Evaluator

Checks if estimated hours are within tolerance of expected:

```python
from langchain.observability import create_estimation_accuracy_evaluator

evaluator = create_estimation_accuracy_evaluator(tolerance=0.2)  # 20%
```

### Confidence Level Evaluator

Checks if confidence level matches expected:

```python
from langchain.observability import create_confidence_level_evaluator

evaluator = create_confidence_level_evaluator()
```

## Configuration Options

### LangSmithConfig

```python
@dataclass
class LangSmithConfig:
    api_key: Optional[str] = None           # API key (or from env)
    project: str = "aitea"                  # Project name
    endpoint: str = "https://api.smith.langchain.com"
    tracing_enabled: bool = True            # Enable tracing
    auto_trace_chains: bool = True          # Auto-trace chains
    auto_trace_agents: bool = True          # Auto-trace agents
```

### Environment Variables

- `LANGSMITH_API_KEY`: Your LangSmith API key
- `LANGSMITH_PROJECT`: Project name (default: "aitea")
- `LANGSMITH_ENDPOINT`: API endpoint (default: official endpoint)
- `LANGSMITH_TRACING`: Enable tracing ("true"/"false")

## Examples

See `examples_langsmith.py` for complete examples:

```bash
python -m langchain.examples_langsmith
```

Examples include:

1. Configure tracing
2. Trace chain execution
3. Trace agent execution
4. Create evaluation dataset
5. Evaluate chain
6. Create custom evaluator
7. Manual tracing
8. Add examples to dataset

## Best Practices

### 1. Use Descriptive Names and Tags

```python
@trace_chain(
    name="feature_extraction_with_rag",
    tags=["extraction", "brd", "rag", "production"]
)
```

### 2. Add Metadata to Traces

```python
from langchain.observability import create_trace_metadata

metadata = create_trace_metadata(
    user_id="user123",
    session_id="session456",
    metadata={"feature": "estimation", "version": "1.0"}
)

chain.invoke(input, config={"metadata": metadata})
```

### 3. Create Comprehensive Datasets

Include diverse examples covering:

- Common cases
- Edge cases
- Error cases
- Different input formats

### 4. Use Multiple Evaluators

Combine evaluators for comprehensive evaluation:

```python
evaluators = [
    feature_extraction_evaluator,
    estimation_accuracy_evaluator,
    confidence_level_evaluator,
]

result = evaluate_chain(chain, dataset_name, evaluators=evaluators)
```

### 5. Monitor Production

Enable tracing in production to monitor:

- Latency trends
- Token usage
- Error rates
- User feedback

## Troubleshooting

### Tracing Not Working

1. Check API key is set:

   ```bash
   echo $LANGSMITH_API_KEY
   ```

2. Verify configuration:

   ```python
   from langchain.observability import get_config
   config = get_config()
   print(f"Tracing enabled: {config.tracing_enabled}")
   ```

3. Check LangSmith is installed:
   ```bash
   pip show langsmith
   ```

### Dataset Not Found

1. List available datasets:

   ```python
   from langchain.observability import list_datasets
   datasets = list_datasets()
   print(datasets)
   ```

2. Verify project name matches

### Evaluation Failing

1. Check dataset format matches chain inputs/outputs
2. Verify evaluator logic is correct
3. Test evaluator independently:
   ```python
   result = evaluator_fn(expected, actual)
   print(f"Passed: {result}")
   ```

## Integration with AITEA Components

### With Chains

```python
from langchain.chains import create_estimation_chain
from langchain.observability import trace_chain

@trace_chain(name="estimation", tags=["estimation"])
def estimate_project(features):
    chain = create_estimation_chain()
    return chain.invoke({"features": features})
```

### With Agents

```python
from langchain.brd_parser_agent import create_brd_parser_agent
from langchain.observability import trace_agent

@trace_agent(name="brd_parser", tags=["agent"])
def parse_brd_document(brd_text):
    agent = create_brd_parser_agent()
    return agent.invoke({"brd_text": brd_text})
```

### With RAG

```python
from langchain.chains import create_estimation_chain
from langchain.stores import ChromaDBStore
from langchain.observability import trace_chain

@trace_chain(name="rag_estimation", tags=["rag", "estimation"])
def estimate_with_rag(feature_name):
    store = ChromaDBStore()
    retriever = store.as_retriever()
    chain = create_estimation_chain(retriever=retriever)
    return chain.invoke({"feature": feature_name})
```

## Requirements Satisfied

This implementation satisfies:

- **Requirement 6.5**: LangSmith integration for observability (tracing, metrics), evaluation, and prompt engineering
- Automatic tracing of chains and agents
- Evaluation framework with custom evaluators
- Dataset management for test cases
- Built-in evaluators for AITEA domain

## Next Steps

1. Create evaluation datasets for your use cases
2. Set up continuous evaluation in CI/CD
3. Monitor production traces for insights
4. Use LangSmith playground for prompt engineering
5. Create custom evaluators for domain-specific validation

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Python SDK](https://github.com/langchain-ai/langsmith-sdk)
- [Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [Tracing Guide](https://docs.smith.langchain.com/tracing)
