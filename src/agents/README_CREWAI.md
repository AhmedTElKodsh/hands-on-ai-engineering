# CrewAI Multi-Agent System for AITEA

This module implements a multi-agent system using the CrewAI framework for collaborative project estimation.

## Overview

The CrewAI implementation consists of three specialized agents working together in a sequential or hierarchical process:

1. **Analyst Agent**: Extracts and clarifies features from BRD documents
2. **Estimator Agent**: Provides time estimates based on historical data
3. **Reviewer Agent**: Validates estimates and identifies risks

## Installation

CrewAI is an optional dependency. Install it with:

```bash
pip install crewai
# or
pip install -e ".[agents]"
```

## Quick Start

```python
from src.services import FeatureLibraryService, EstimationService
from src.agents import create_estimation_crew

# Initialize services
feature_service = FeatureLibraryService()
estimation_service = EstimationService(feature_service, time_tracking_service)

# Create the crew
crew = create_estimation_crew(
    feature_service,
    estimation_service,
    process_type="sequential"
)

# Run the workflow
brd_content = """
Project: E-commerce Platform
Features:
- User authentication
- Product catalog
- Shopping cart
- Payment processing
"""

result = crew.kickoff(inputs={"brd_content": brd_content})
print(result)
```

## Agents

### Analyst Agent

**Role**: Requirements Analyst

**Responsibilities**:

- Read and understand BRD documents
- Extract comprehensive feature lists
- Search for similar historical features
- Clarify ambiguous requirements

**Tools**:

- `search_features`: Search the feature library for matching features

**Example Output**:

```
Features extracted from BRD:
1. User Authentication
   - Similar features: "Auth System" (backend, 8h), "Login/Signup" (fullstack, 12h)
2. Product Catalog
   - Similar features: "CRUD API" (backend, 4h), "Product Management" (fullstack, 16h)
...
```

### Estimator Agent

**Role**: Estimation Specialist

**Responsibilities**:

- Analyze feature complexity
- Retrieve historical data
- Compute statistical estimates (mean, median, P80)
- Provide confidence levels
- Aggregate feature estimates into project totals

**Tools**:

- `estimate_feature`: Get time estimates with statistics

**Example Output**:

```
Project Estimate:
1. User Authentication: 10h (confidence: HIGH)
   - Mean: 9.5h, Median: 10h, P80: 12h
   - Based on 15 historical data points
2. Product Catalog: 14h (confidence: MEDIUM)
   - Mean: 14.2h, Median: 13h, P80: 16h
   - Based on 5 historical data points
...
Total: 48h (Overall confidence: MEDIUM)
```

### Reviewer Agent

**Role**: Estimate Reviewer

**Responsibilities**:

- Validate estimates against historical data
- Identify outliers and risks
- Check for missing features
- Provide overall confidence assessment
- Suggest improvements

**Tools**:

- `validate_estimate`: Compare estimates to historical norms

**Example Output**:

```
Review Report:
✓ User Authentication (10h): Within normal range
⚠️ Product Catalog (14h): 1.2 std devs from mean - acceptable but monitor
⚠️ Payment Processing (20h): >2 std devs from mean - HIGH RISK

Risks Identified:
- Payment Processing estimate significantly exceeds historical data
- Limited data for Product Catalog (only 5 data points)
- Missing features: Admin dashboard, reporting

Recommendations:
- Break down Payment Processing into smaller features
- Gather more data on Product Catalog implementations
- Add missing features to estimate

Overall Confidence: MEDIUM-LOW
```

## Process Types

### Sequential Process

Agents work one after another in a fixed order:

1. Analyst extracts features
2. Estimator provides estimates
3. Reviewer validates and identifies risks

```python
crew = create_estimation_crew(
    feature_service,
    estimation_service,
    process_type="sequential"
)
```

**Best for**: Straightforward estimation workflows with clear dependencies

### Hierarchical Process

A manager agent coordinates the specialist agents:

- Manager delegates tasks to specialists
- Specialists report back to manager
- Manager synthesizes final output

```python
crew = create_estimation_crew(
    feature_service,
    estimation_service,
    process_type="hierarchical"
)
```

**Best for**: Complex workflows requiring dynamic task allocation

## Tools

### FeatureSearchTool

Search the feature library for matching features.

```python
from src.agents import FeatureSearchTool

tool = FeatureSearchTool(feature_service)
result = tool._run("authentication")
# Returns: "Found 3 matching features: Auth System (8h), Login (6h), ..."
```

### EstimationTool

Estimate time for a specific feature.

```python
from src.agents import EstimationTool

tool = EstimationTool(estimation_service)
result = tool._run("User Authentication")
# Returns: "Estimate for 'User Authentication': 10h (HIGH confidence)..."
```

### ValidationTool

Validate an estimate against historical data.

```python
from src.agents import ValidationTool

tool = ValidationTool(estimation_service)
result = tool._run("User Authentication", 15.0)
# Returns: "Validation for 'User Authentication' (15h): WARNING - >2 std devs..."
```

## Advanced Usage

### Custom LLM Configuration

```python
llm_config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
}

crew = create_estimation_crew(
    feature_service,
    estimation_service,
    llm_config=llm_config
)
```

### Individual Agent Creation

```python
from src.agents import (
    create_analyst_agent,
    create_estimator_agent,
    create_reviewer_agent
)

# Create agents individually
analyst = create_analyst_agent(feature_service)
estimator = create_estimator_agent(estimation_service)
reviewer = create_reviewer_agent(estimation_service)

# Use agents independently or in custom workflows
```

### Mock LLM for Testing

```python
from src.agents import get_mock_llm_config

# Use mock LLM for testing without API keys
mock_config = get_mock_llm_config()
crew = create_estimation_crew(
    feature_service,
    estimation_service,
    llm_config=mock_config
)
```

## Error Handling

The implementation gracefully handles missing CrewAI installation:

```python
from src.agents import CREWAI_AVAILABLE

if not CREWAI_AVAILABLE:
    print("CrewAI is not installed. Install with: pip install crewai")
else:
    # Use CrewAI functionality
    crew = create_estimation_crew(...)
```

## Testing

Run the CrewAI tests:

```bash
# Run all CrewAI tests
pytest tests/agents/test_crewai_agents.py -v

# Run only tests that don't require CrewAI installation
pytest tests/agents/test_crewai_agents.py -v -k "not (AgentCreation or CrewCreation)"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BRD Document Input                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Analyst Agent                           │
│  - Extracts features from BRD                                │
│  - Searches for similar historical features                  │
│  - Clarifies requirements                                    │
│  Tool: FeatureSearchTool                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Estimator Agent                          │
│  - Computes time estimates                                   │
│  - Uses historical data and statistics                       │
│  - Provides confidence levels                                │
│  Tool: EstimationTool                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Reviewer Agent                          │
│  - Validates estimates                                       │
│  - Identifies risks and outliers                             │
│  - Provides recommendations                                  │
│  Tool: ValidationTool                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Final Estimation Report                   │
│  - Feature list with estimates                               │
│  - Validation results                                        │
│  - Risk assessment                                           │
│  - Overall confidence                                        │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Populate Feature Library**: Ensure your feature library has historical data for accurate estimates
2. **Use Sequential for Simple Workflows**: Start with sequential process for straightforward estimation
3. **Review Agent Output**: Always review the Reviewer agent's risk assessment
4. **Iterate on Estimates**: Use the crew's output to refine your BRD and re-estimate
5. **Monitor Confidence Levels**: Pay attention to low-confidence estimates
6. **Handle Edge Cases**: The tools gracefully handle missing data and errors

## Limitations

- Requires CrewAI installation (optional dependency)
- LLM API keys needed for production use (can use MockLLM for testing)
- Quality depends on historical data in feature library
- Sequential process may be slower than parallel approaches
- Agent reasoning quality depends on LLM model capabilities

## Future Enhancements

- [ ] Add parallel task execution for independent features
- [ ] Implement feedback loops for estimate refinement
- [ ] Add support for custom agent roles
- [ ] Integrate with external project management tools
- [ ] Add visualization of estimation workflow
- [ ] Support for multi-language BRD documents

## Related Documentation

- [Agent Foundations](./simple_agent.py) - Basic agent patterns
- [Memory Systems](./memory.py) - Agent memory implementations
- [Safety Checks](./safety.py) - Prompt injection detection
- [Service Interfaces](../services/interfaces.py) - AITEA service contracts

## Support

For issues or questions:

1. Check the test file for usage examples: `tests/agents/test_crewai_agents.py`
2. Review the CrewAI documentation: https://docs.crewai.com/
3. Ensure all dependencies are installed: `pip install -e ".[agents]"`
