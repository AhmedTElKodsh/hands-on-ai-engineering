# Requirements Document: AITEA LlamaIndex

## Introduction

AITEA LlamaIndex provides advanced RAG capabilities using LlamaIndex's specialized features. This module focuses on learning LlamaIndex's unique strengths: multiple index types, advanced retrieval strategies, and comprehensive evaluation.

## Dependencies

- **aitea-core**: Shared models, services, and utilities
- **llama-index**: Advanced RAG framework

## Glossary

- **Index**: Data structure optimized for specific retrieval patterns
- **VectorStoreIndex**: Index using embedding similarity for retrieval
- **TreeIndex**: Hierarchical index for summarization queries
- **KeywordTableIndex**: Index using keyword extraction for exact matching
- **KnowledgeGraphIndex**: Index storing entity relationships as a graph
- **HyDE**: Hypothetical Document Embeddings - query transformation technique
- **Reranking**: Re-scoring retrieved documents for better relevance
- **ReAct**: Reasoning + Acting agent pattern

## Requirements

### Requirement 1: Multi-Index Architecture

**User Story:** As a Developer, I want to understand different index types and when to use each for optimal retrieval.

#### Acceptance Criteria

1. WHEN building a VectorStoreIndex, THE System SHALL create embeddings for all feature documents and store them for similarity search
2. WHEN building a TreeIndex, THE System SHALL create a hierarchical structure for summarization queries
3. WHEN building a KeywordTableIndex, THE System SHALL extract keywords for exact matching retrieval
4. WHEN building a KnowledgeGraphIndex, THE System SHALL extract entity relationships and store them as a graph
5. WHEN persisting indices, THE System SHALL save all index types to disk for later loading

### Requirement 2: Hybrid Retrieval

**User Story:** As a Developer, I want to combine multiple retrieval strategies for better results.

#### Acceptance Criteria

1. WHEN performing hybrid retrieval, THE System SHALL query both vector and keyword indices
2. WHEN merging results, THE System SHALL deduplicate nodes by ID
3. WHEN reranking results, THE System SHALL use a cross-encoder model to re-score relevance
4. WHEN returning results, THE System SHALL include relevance scores for each node
5. WHEN configuring retrieval, THE System SHALL allow adjusting the number of results from each source

### Requirement 3: Query Transformation

**User Story:** As a Developer, I want to learn query transformation techniques for improved retrieval.

#### Acceptance Criteria

1. WHEN using HyDE, THE System SHALL generate a hypothetical answer and use it for retrieval
2. WHEN using multi-query, THE System SHALL generate query variations and merge results
3. WHEN transforming queries, THE System SHALL preserve the original query intent
4. WHEN evaluating transformations, THE System SHALL compare retrieval quality with and without transformation
5. WHEN configuring transformation, THE System SHALL allow selecting the transformation strategy

### Requirement 4: Query Engines

**User Story:** As a Developer, I want to understand different query engine types for various use cases.

#### Acceptance Criteria

1. WHEN creating a simple query engine, THE System SHALL use a single index with configurable parameters
2. WHEN creating a router engine, THE System SHALL select the best index based on query characteristics
3. WHEN creating a sub-question engine, THE System SHALL break complex queries into simpler sub-questions
4. WHEN creating a citation engine, THE System SHALL include source citations in responses
5. WHEN querying, THE System SHALL return structured responses with metadata

### Requirement 5: ReAct Agent

**User Story:** As a Developer, I want to build an interactive agent that can reason and use tools.

#### Acceptance Criteria

1. WHEN creating a ReAct agent, THE System SHALL register tools for feature search, statistics, and estimation
2. WHEN the agent reasons, THE System SHALL show the thought process (verbose mode)
3. WHEN the agent uses tools, THE System SHALL execute the appropriate aitea-core service method
4. WHEN the agent completes, THE System SHALL provide a final answer with reasoning trace
5. WHEN errors occur, THE System SHALL handle them gracefully and continue reasoning

### Requirement 6: Evaluation Framework

**User Story:** As a Developer, I want to evaluate and compare RAG system quality.

#### Acceptance Criteria

1. WHEN evaluating faithfulness, THE System SHALL check if responses are grounded in retrieved context
2. WHEN evaluating relevancy, THE System SHALL check if responses answer the query
3. WHEN evaluating correctness, THE System SHALL compare responses against reference answers
4. WHEN evaluating retrieval, THE System SHALL compute precision, recall, and MRR metrics
5. WHEN comparing systems, THE System SHALL run the same evaluation on LangChain and LlamaIndex versions

### Requirement 7: Ingestion Pipeline

**User Story:** As a Developer, I want to understand document processing and transformation.

#### Acceptance Criteria

1. WHEN loading documents, THE System SHALL support multiple formats (PDF, DOCX, TXT, JSON)
2. WHEN transforming documents, THE System SHALL split into appropriately sized chunks
3. WHEN creating nodes, THE System SHALL include metadata (source, page, feature info)
4. WHEN building indices, THE System SHALL use the ingestion pipeline for consistent processing
5. WHEN updating indices, THE System SHALL support incremental updates without full rebuild

### Requirement 8: Comparison with LangChain

**User Story:** As a Developer, I want to understand the differences between LlamaIndex and LangChain approaches.

#### Acceptance Criteria

1. WHEN comparing retrieval, THE System SHALL run identical queries on both systems
2. WHEN comparing response quality, THE System SHALL use the same evaluation metrics
3. WHEN comparing latency, THE System SHALL measure end-to-end response time
4. WHEN documenting differences, THE System SHALL highlight unique features of each framework
5. WHEN recommending, THE System SHALL provide guidance on when to use each framework
