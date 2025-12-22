# Requirements Document

## Introduction

AITEA (AI Time Estimation Agent) is a comprehensive project-based learning curriculum that teaches AI agent development from fundamentals to advanced patterns. The curriculum merges learning and implementation: each phase teaches concepts AND delivers working increments of the AITEA system.

AITEA helps project managers estimate software development time by:

1. Maintaining a feature library with historical time data
2. Importing tracked time from team members
3. Computing statistics (mean, median, P80) from historical data
4. Generating project estimates from feature lists or BRD documents

The curriculum progresses through 10 phases, building 7 packages: aitea-core (foundation), aitea-cli (command-line), aitea-ingest (document processing), aitea-langchain (LangChain integration), aitea-agents (multi-framework agents), aitea-llamaindex (advanced RAG), and aitea-web (web application).

## Glossary

- **AITEA**: AI Time Estimation Agent - the system being built throughout the curriculum
- **Feature Library**: A collection of software features with associated time estimates and metadata
- **Tracked Time Entry**: A record of actual time spent by a team member on a feature
- **BRD**: Business Requirements Document - a document describing project features to be estimated
- **RAG**: Retrieval-Augmented Generation - a pattern combining retrieval with LLM generation (context augmentation)
- **Agentic RAG**: RAG patterns where agents decide when/how to retrieve (Self-RAG, CRAG, Adaptive RAG)
- **Property-Based Testing**: Testing approach using Hypothesis to verify properties across many inputs
- **LangChain**: Platform for agent engineering - quickly build agents with any model provider
- **LangGraph**: Low-level orchestration framework for custom agents with memory and human-in-the-loop support
- **Deep Agents**: LangChain pattern for agents that tackle complex, multi-step tasks
- **LangSmith**: Platform for observability, evaluation, prompt engineering, and agent deployment
- **LlamaIndex Agents**: LLM-powered knowledge assistants that use tools (including RAG) to perform tasks
- **LlamaIndex Workflows**: Event-driven multi-step processes combining agents, data connectors, and tools
- **LlamaCloud**: Enterprise managed service for document parsing, extraction, indexing, and retrieval
- **CrewAI**: Multi-agent orchestration framework with roles, goals, and tasks
- **AutoGen**: Microsoft's multi-agent conversation framework
- **Strands Agents SDK**: AWS's agent framework for building AI agents
- **MCP**: Model Context Protocol - standard for tool integration with LLMs
- **Chunking**: Process of splitting documents into smaller pieces for embedding
- **Guardrails**: Safety mechanisms to prevent harmful or incorrect LLM outputs
- **Mock LLM**: A simulated LLM for learning without API keys
- **Graph RAG**: RAG using knowledge graphs for structured retrieval
- **Context Augmentation**: Making your data available to LLMs to solve problems (RAG is one example)

## Requirements

### Requirement 1: Phase 1 - Python Foundations (aitea-core)

**User Story:** As a learner, I want to build the core data models and services from scratch, so that I understand Python fundamentals before using AI frameworks.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 1 THEN the System SHALL provide a working Python environment with Conda environment management, UV package installer, and pyproject.toml configuration
2. WHEN the learner completes Chapter 2 THEN the System SHALL produce a models/enums.py file with Team, Process, and ConfidenceLevel enums using type hints verified by mypy
3. WHEN the learner completes Chapter 3 THEN the System SHALL produce dataclass models for Feature, TrackedTimeEntry, ProjectEstimate, and EstimationConfig with proper field definitions and Optional/List types
4. WHEN the learner completes Chapter 4 THEN the System SHALL produce abstract base classes defining service interfaces using ABC and @abstractmethod decorators
5. WHEN the learner completes Chapter 5 THEN the System SHALL produce FeatureLibraryService, TimeTrackingService, and EstimationService implementations with Result type pattern
6. WHEN the learner completes Chapter 6 THEN the System SHALL produce utility functions for statistics calculation (mean, median, P80), text normalization, and outlier detection
7. WHEN the learner completes Chapter 7 THEN the System SHALL produce property-based tests using Hypothesis with custom strategies for all core models
8. WHEN the learner completes Chapter 8 THEN the System SHALL produce ValidationError types and Result[T, E] pattern implementations for error handling

---

### Requirement 2: Phase 2 - CLI Development (aitea-cli)

**User Story:** As a learner, I want to build a command-line interface for AITEA, so that I can interact with the core services through terminal commands.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 9 THEN the System SHALL produce a Typer-based CLI application with commands for feature management, time tracking, and estimation
2. WHEN the learner completes Chapter 10 THEN the System SHALL produce Rich-formatted terminal output with tables, panels, and progress bars for all CLI commands
3. WHEN the learner completes Chapter 11 THEN the System SHALL produce JSON persistence services that serialize and deserialize Feature Library and Tracked Time data
4. WHEN the learner completes Chapter 12 THEN the System SHALL produce a CSV import pipeline using pandas with validation and error collection for tracked time entries

---

### Requirement 3: Phase 3 - LLM Fundamentals

**User Story:** As a learner, I want to understand LLM concepts before using frameworks, so that I can make informed decisions about AI integration patterns.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 13 THEN the System SHALL produce a MockLLM client that simulates LLM responses for learning without API keys
2. WHEN the learner completes Chapter 14 THEN the System SHALL produce prompt templates demonstrating system/user messages, few-shot examples, and chain-of-thought patterns
3. WHEN the learner completes Chapter 15 THEN the System SHALL produce output parsers that extract structured JSON from LLM responses using Pydantic validation
4. WHEN the learner completes Chapter 16 THEN the System SHALL produce tool definitions with JSON schemas for function calling patterns
5. WHEN the learner completes Chapter 17 THEN the System SHALL produce a multi-provider abstraction supporting OpenAI, Anthropic, and AWS Bedrock with unified interface
6. WHEN the learner completes Chapter 18 THEN the System SHALL produce streaming response handlers using async generators for real-time output
7. WHEN the learner completes Chapter 19 THEN the System SHALL produce token counting utilities and context window management for different model families

---

### Requirement 4: Phase 4 - Document Processing & Chunking (aitea-ingest)

**User Story:** As a learner, I want to build document ingestion pipelines, so that I can prepare real-world documents for RAG systems.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 20 THEN the System SHALL produce document loaders for PDF, DOCX, HTML, and Markdown formats
2. WHEN the learner completes Chapter 21 THEN the System SHALL produce multiple chunking strategies: fixed-size, recursive, semantic, and sentence-based
3. WHEN the learner completes Chapter 22 THEN the System SHALL produce chunk overlap handling and parent-document retrieval patterns
4. WHEN the learner completes Chapter 23 THEN the System SHALL produce metadata extraction and enrichment for chunks (source, page, section)
5. WHEN the learner completes Chapter 24 THEN the System SHALL produce table extraction from PDFs and structured data handling

---

### Requirement 5: Phase 5 - Agent Foundations (From Scratch)

**User Story:** As a learner, I want to build agents from scratch before using frameworks, so that I understand the fundamental patterns that frameworks abstract.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 25 THEN the System SHALL provide conceptual understanding distinguishing agents from chatbots and workflows
2. WHEN the learner completes Chapter 26 THEN the System SHALL produce a SimpleAgent class implementing the Observe-Think-Act-Reflect loop
3. WHEN the learner completes Chapter 27 THEN the System SHALL produce a ToolRegistry class with tool registration and schema validation
4. WHEN the learner completes Chapter 28 THEN the System SHALL produce a ReAct implementation demonstrating reasoning and acting patterns
5. WHEN the learner completes Chapter 29 THEN the System SHALL produce memory classes for short-term, long-term, and summarization memory patterns
6. WHEN the learner completes Chapter 30 THEN the System SHALL produce safety checks for prompt injection prevention and safe tool usage

---

### Requirement 6: Phase 6 - LangChain Track (aitea-langchain)

**User Story:** As a learner, I want to implement AITEA features using LangChain's agent engineering platform, so that I can build production-ready agents with proper orchestration and observability.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 31 THEN the System SHALL produce agents using LangChain's high-level agent APIs with any model provider
2. WHEN the learner completes Chapter 32 THEN the System SHALL produce custom tools wrapping aitea-core services using @tool decorator and StructuredTool
3. WHEN the learner completes Chapter 33 THEN the System SHALL produce a RAG pipeline with multiple vector stores (ChromaDB, Pinecone, Qdrant) and embedding model selection
4. WHEN the learner completes Chapter 34 THEN the System SHALL produce a LangGraph agent with StateGraph, nodes, conditional edges, memory, and human-in-the-loop support
5. WHEN the learner completes Chapter 35 THEN the System SHALL produce LangSmith integration for observability (tracing, metrics), evaluation, and prompt engineering
6. WHEN the learner completes Chapter 36 THEN the System SHALL produce Deep Agents patterns for complex multi-step estimation tasks

---

### Requirement 7: Phase 7 - Multi-Agent Frameworks (aitea-agents)

**User Story:** As a learner, I want to build multi-agent systems using industry-standard frameworks, so that I can orchestrate complex AI workflows.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 37 THEN the System SHALL produce a CrewAI implementation with specialized agents (Analyst, Estimator, Reviewer) working collaboratively
2. WHEN the learner completes Chapter 38 THEN the System SHALL produce an AutoGen implementation with conversational agents and human-in-the-loop patterns
3. WHEN the learner completes Chapter 39 THEN the System SHALL produce a Strands Agents SDK implementation for AWS-native agent development
4. WHEN the learner completes Chapter 40 THEN the System SHALL produce MCP (Model Context Protocol) tool definitions for cross-framework tool sharing
5. WHEN the learner completes Chapter 41 THEN the System SHALL produce a framework comparison guide with decision criteria for selecting the right framework

---

### Requirement 8: Phase 8 - LlamaIndex Agents & Workflows (aitea-llamaindex)

**User Story:** As a learner, I want to build LLM-powered agents and event-driven workflows using LlamaIndex, so that I can create production-quality agentic applications.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 42 THEN the System SHALL produce LlamaIndex Agents that use RAG pipelines as tools for knowledge-assisted estimation
2. WHEN the learner completes Chapter 43 THEN the System SHALL produce event-driven Workflows combining multiple agents, data connectors, and tools
3. WHEN the learner completes Chapter 44 THEN the System SHALL produce advanced retrievers with hybrid search, HyDE, and reranking capabilities
4. WHEN the learner completes Chapter 45 THEN the System SHALL produce Agentic RAG patterns: Self-RAG, Corrective RAG (CRAG), and Adaptive RAG with reflection and error-correction
5. WHEN the learner completes Chapter 46 THEN the System SHALL produce Graph RAG implementation with Neo4j for knowledge graph-based retrieval
6. WHEN the learner completes Chapter 47 THEN the System SHALL produce an evaluation framework using RAGAS metrics (faithfulness, relevancy, context precision)
7. WHEN the learner completes Chapter 48 THEN the System SHALL produce deployable agentic workflows as production microservices

---

### Requirement 9: Phase 9 - Production Hardening (aitea-web)

**User Story:** As a learner, I want to build production-ready AI systems with proper safety, observability, and reliability patterns.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 49 THEN the System SHALL produce guardrails implementation using NeMo Guardrails and Guardrails AI for input/output validation
2. WHEN the learner completes Chapter 50 THEN the System SHALL produce observability integration with LangFuse, Phoenix, and OpenTelemetry for tracing
3. WHEN the learner completes Chapter 51 THEN the System SHALL produce reliability patterns including retries, timeouts, circuit breakers, and fallback chains
4. WHEN the learner completes Chapter 52 THEN the System SHALL produce async patterns with asyncio for concurrent tool execution and parallel RAG queries
5. WHEN the learner completes Chapter 53 THEN the System SHALL produce streaming responses with Server-Sent Events (SSE) for real-time agent updates
6. WHEN the learner completes Chapter 54 THEN the System SHALL produce cost optimization with semantic caching, token budgeting, and model routing

---

### Requirement 10: Phase 10 - Deployment & Integration

**User Story:** As a learner, I want to deploy AITEA as a production service with proper infrastructure patterns.

#### Acceptance Criteria

1. WHEN the learner completes Chapter 55 THEN the System SHALL produce a FastAPI application with WebSocket support for bidirectional agent communication
2. WHEN the learner completes Chapter 56 THEN the System SHALL produce queue-based processing with Redis/Celery for long-running agent tasks
3. WHEN the learner completes Chapter 57 THEN the System SHALL produce containerization with Docker and orchestration patterns
4. WHEN the learner completes Chapter 58 THEN the System SHALL produce serverless deployment examples for AWS Lambda and Vercel

---

### Requirement 11: Data Models and Serialization

**User Story:** As a developer, I want well-defined data models with serialization support, so that I can persist and transfer AITEA data reliably.

#### Acceptance Criteria

1. THE Feature model SHALL contain id, name, team, process, seed_time_hours, synonyms list, and notes fields with appropriate types
2. THE TrackedTimeEntry model SHALL contain id, team, member_name, feature, tracked_time_hours, process, and date fields
3. THE ProjectEstimate model SHALL contain feature breakdown with hours, total hours, and confidence level
4. WHEN serializing models to JSON THEN the System SHALL produce valid JSON that can be deserialized back to equivalent model instances
5. WHEN parsing JSON data THEN the System SHALL validate all required fields and report specific validation errors

---

### Requirement 12: Statistics and Estimation Engine

**User Story:** As a project manager, I want accurate time estimates based on historical data, so that I can plan projects with confidence.

#### Acceptance Criteria

1. WHEN calculating statistics for a feature THEN the System SHALL compute mean, median, standard deviation, and P80 (80th percentile) from tracked time entries
2. WHEN fewer than 3 data points exist for a feature THEN the System SHALL use the seed time with low confidence indicator
3. WHEN outliers are detected in tracked time data THEN the System SHALL flag entries exceeding 2 standard deviations from the mean
4. WHEN estimating a project THEN the System SHALL aggregate feature estimates and provide total hours with confidence breakdown
5. THE confidence level SHALL be computed based on data point count: Low (1-2 entries), Medium (3-9 entries), High (10+ entries)

---

### Requirement 13: Multi-Provider Fallback Mode

**User Story:** As a learner, I want the system to automatically try multiple LLM providers, so that I can continue learning even if one provider fails.

#### Acceptance Criteria

1. WHEN no API keys are set THEN the System SHALL automatically use MockLLM for all LLM operations
2. WHEN at least one API key is set THEN the System SHALL attempt providers in priority order: OpenAI → Cohere → Gemini → Grok → Mistral → HuggingFace → Ollama (local)
3. WHEN a provider fails THEN the System SHALL automatically try the next available provider in the fallback chain
4. WHEN all real providers fail THEN the System SHALL fall back to MockLLM with a warning message
5. WHEN running in mock mode THEN the System SHALL display a warning message indicating mock mode is active
6. THE MockLLM SHALL provide deterministic responses for feature extraction, estimation, and BRD parsing tasks
7. THE System SHALL log which provider successfully handled each request for debugging purposes

---

### Requirement 14: Chapter Structure Consistency

**User Story:** As a learner, I want consistent chapter structure, so that I can navigate the curriculum predictably.

#### Acceptance Criteria

1. EACH chapter SHALL include header with difficulty level, time estimate, prerequisites, and AITEA component being built
2. EACH chapter SHALL include 3-5 measurable learning objectives using action verbs
3. EACH chapter SHALL include from-scratch implementation before framework implementation where applicable
4. EACH chapter SHALL include at least 2 interactive exercises with expected output shown
5. EACH chapter SHALL include a debugging scenario with broken code to fix
6. EACH chapter SHALL include a mini-project with clear requirements and acceptance criteria
7. EACH chapter SHALL include AITEA integration section explaining which requirement the chapter satisfies
