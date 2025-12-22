# AITEA LangChain Integration

This module provides LangChain integration for the AITEA (AI Time Estimation Agent) system.

## Components

### 1. Chains (`chains.py`)

LCEL (LangChain Expression Language) chains for feature extraction and estimation:

- **Feature Extraction Chain**: Extracts features from natural language project descriptions
- **Estimation Chain**: Estimates time for features with optional RAG integration
- **Passthrough Examples**: Demonstrates RunnablePassthrough for data flow

Example:

```python
from langchain_openai import ChatOpenAI
from src.langchain.chains import create_feature_extraction_chain

llm = ChatOpenAI(model="gpt-4o-mini")
chain = create_feature_extraction_chain(llm)

result = chain.invoke({
    "project_description": "Build a REST API with user authentication"
})
print(result["features"])
```

### 2. Tools (`tools.py`)

LangChain tools wrapping aitea-core services for use in agents:

#### Available Tools

1. **add_feature**: Add a new feature to the library
2. **search_features**: Search for features by name or synonym
3. **list_features**: List all features, optionally filtered by team
4. **estimate_feature**: Estimate time for a single feature
5. **estimate_project**: Estimate time for a project with multiple features
6. **add_time_entry**: Record actual time spent on a feature

#### Tool Implementation Approaches

**StructuredTool (Recommended for Production)**

All main tools use `StructuredTool.from_function()` with Pydantic schemas for:

- Type validation
- Automatic schema generation
- Better error messages
- IDE autocomplete support

Example:

```python
from src.langchain.tools import create_feature_tools
from src.services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService
)

# Create service instances
feature_lib = FeatureLibraryService()
time_track = TimeTrackingService()
estimator = EstimationService(feature_lib, time_track)

# Create tools
tools = create_feature_tools(feature_lib, time_track, estimator)

# Use with an agent
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

**@tool Decorator (Simple Functions)**

For simple, stateless tools, use the `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def calculate_velocity(team: str, weeks: int = 4) -> str:
    """Calculate team velocity over recent weeks."""
    # Implementation
    return f"Team {team} velocity: ..."
```

## Testing

Comprehensive tests are available for all components:

```bash
# Run all LangChain tests
pytest tests/langchain/ -v

# Run tool tests
pytest tests/langchain/test_tools.py -v

# Run vector store tests
pytest tests/langchain/test_chromadb_store.py -v
pytest tests/langchain/test_pinecone_store.py -v
pytest tests/langchain/test_qdrant_store.py -v

# Run specific test class
pytest tests/langchain/test_tools.py::TestAddFeatureTool -v
pytest tests/langchain/test_chromadb_store.py::TestChromaDBStore -v
pytest tests/langchain/test_qdrant_store.py::TestQdrantStore -v
```

### Vector Store Tests

All vector stores have comprehensive async test coverage:

**ChromaDB** (13 tests):

- Document addition and retrieval
- Similarity search with metadata filtering
- Document deletion and clearing
- Input validation (empty queries, invalid k values)
- Hybrid search fallback behavior
- Custom document IDs

**Qdrant** (25 tests):

- All ChromaDB features plus:
- Native hybrid search (dense + sparse)
- Alpha parameter weighting for hybrid search
- Advanced metadata filtering
- Collection initialization and management
- gRPC and API key authentication
- Graceful error handling for sparse search failures

## Integration with Agents

### ReAct Agent Example

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# Setup
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = create_feature_tools(feature_lib, time_track, estimator)

# Create ReAct prompt
prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

# Create and run agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "Add a User Authentication feature for backend team with 8 hours, then estimate it"
})
```

### OpenAI Functions Agent Example

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Create prompt with message placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant helping with software project estimation."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent (automatically uses function calling)
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "What features do we have for the backend team?"
})
```

## Tool Schemas

Each tool has a well-defined Pydantic schema for inputs:

### AddFeatureInput

```python
{
    "id": str,              # Unique identifier
    "name": str,            # Feature name
    "team": str,            # backend, frontend, fullstack, design, qa, devops
    "process": str,         # Process type
    "seed_time_hours": float,  # Initial estimate (> 0)
    "synonyms": List[str],  # Optional alternative names
    "notes": str            # Optional notes
}
```

### EstimateProjectInput

```python
{
    "features": List[str]   # List of feature names
}
```

### AddTimeEntryInput

```python
{
    "id": str,                    # Unique identifier
    "team": str,                  # Team name
    "member_name": str,           # Team member
    "feature": str,               # Feature name
    "tracked_time_hours": float,  # Actual time (> 0)
    "process": str,               # Process type
    "date": str                   # YYYY-MM-DD format
}
```

## Best Practices

1. **Service Injection**: Always inject service instances when creating tools to maintain proper state
2. **Error Handling**: Tools return descriptive error messages as strings for agent consumption
3. **Validation**: Use Pydantic schemas for automatic input validation
4. **Testing**: Test tools both individually and in integration scenarios
5. **Documentation**: Keep tool descriptions clear and concise for LLM understanding

### 3. Vector Stores (`vector_stores.py`, `stores/`, `embeddings/`)

Vector store abstraction for RAG (Retrieval-Augmented Generation) pipelines:

#### Supported Vector Stores

1. **ChromaDB**: Local development and prototyping
2. **Pinecone**: Production managed service
3. **Qdrant**: Hybrid search and self-hosted deployments

#### Supported Embedding Models

1. **OpenAI**: text-embedding-3-small, text-embedding-3-large
2. **Cohere**: embed-english-v3.0, embed-multilingual-v3.0
3. **BGE**: BAAI/bge-small-en-v1.5 (local, no API key required)

Example:

```python
from src.langchain import ChromaDBStore, BGEEmbedding, Document

# Create embedding model (runs locally, no API key)
embedding_model = BGEEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Create vector store
store = ChromaDBStore(
    collection_name="aitea_features",
    embedding_model=embedding_model
)

# Add documents
documents = [
    Document(
        content="CRUD API endpoints",
        metadata={"team": "backend", "hours": 8}
    )
]
await store.add_documents(documents)

# Search
results = await store.similarity_search("API development", k=5)
```

See [VECTOR_STORES.md](./VECTOR_STORES.md) for comprehensive documentation and examples.

## Requirements Satisfied

This implementation satisfies:

- **Requirement 6.2**: Custom tools wrapping aitea-core services using @tool decorator and StructuredTool
- **Requirement 6.3**: RAG pipeline with multiple vector stores (ChromaDB, Pinecone, Qdrant) and embedding model selection

## Next Steps

- Implement LangGraph agents with these tools (Phase 6)
- Add advanced retrievers (HyDE, reranking) (Phase 8)
- Implement Agentic RAG patterns (Self-RAG, CRAG) (Phase 8)
- Create multi-agent workflows with CrewAI/AutoGen (Phase 7)
