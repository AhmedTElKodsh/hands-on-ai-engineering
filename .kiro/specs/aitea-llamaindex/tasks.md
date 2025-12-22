# Implementation Plan: AITEA LlamaIndex

## Prerequisites

- aitea-core package must be installed
- OpenAI API key configured
- (Optional) Neo4j for knowledge graph

## 1. Project Setup

- [ ] 1.1 Initialize LlamaIndex package structure

  - Create pyproject.toml with package metadata (name: aitea-llamaindex)
  - Add dependencies: llama-index, llama-index-llms-openai, sentence-transformers
  - Create src/aitea_llamaindex/ directory structure
  - Create indices/, retrievers/, query_engines/, agents/, evaluation/, ingestion/ subdirectories
  - Add **init**.py files to all packages
  - Create .env.example with required environment variables
  - _Requirements: All_

- [ ] 1.2 Create configuration module
  - Create src/aitea_llamaindex/config.py
  - Implement LlamaIndexConfig with Pydantic settings
  - Support environment variables and .env file
  - Include LLM, embedding, and storage settings
  - _Requirements: All_

## 2. Ingestion Pipeline

- [ ] 2.1 Implement document loaders

  - Create src/aitea_llamaindex/ingestion/loaders.py
  - Implement FeatureDocumentLoader converting features to Documents
  - Implement BRDDocumentLoader for BRD files
  - Support PDF, DOCX, TXT, JSON formats
  - _Requirements: 7.1_

- [ ] 2.2 Implement transformations

  - Create src/aitea_llamaindex/ingestion/transformations.py
  - Implement custom node parser for features
  - Add metadata extraction (team, process, seed_time)
  - Configure chunk size and overlap
  - _Requirements: 7.2, 7.3_

- [ ] 2.3 Implement ingestion pipeline

  - Create src/aitea_llamaindex/ingestion/pipeline.py
  - Build IngestionPipeline with loaders and transformations
  - Support incremental updates
  - Add progress tracking
  - _Requirements: 7.4, 7.5_

- [ ]\* 2.4 Write tests for ingestion
  - Test document loading
  - Test node creation with metadata
  - Test incremental updates

## 3. Index Types

- [ ] 3.1 Implement VectorStoreIndex

  - Create src/aitea_llamaindex/indices/vector.py
  - Configure OpenAI embeddings
  - Implement build_vector_index() function
  - Add persistence to Chroma
  - _Requirements: 1.1_

- [ ] 3.2 Implement TreeIndex

  - Create src/aitea_llamaindex/indices/tree.py
  - Configure tree parameters (num_children, build_tree)
  - Implement build_tree_index() function
  - Add persistence
  - _Requirements: 1.2_

- [ ] 3.3 Implement KeywordTableIndex

  - Create src/aitea_llamaindex/indices/keyword.py
  - Configure keyword extraction
  - Implement build_keyword_index() function
  - Add persistence
  - _Requirements: 1.3_

- [ ] 3.4 Implement KnowledgeGraphIndex

  - Create src/aitea_llamaindex/indices/knowledge_graph.py
  - Configure triplet extraction
  - Implement build_kg_index() function
  - Add optional Neo4j integration
  - _Requirements: 1.4_

- [ ] 3.5 Implement MultiIndexManager

  - Create src/aitea_llamaindex/indices/manager.py
  - Implement build_all_indices() method
  - Implement persist_all() and load_all() methods
  - Add index selection utilities
  - _Requirements: 1.5_

- [ ]\* 3.6 Write tests for indices
  - Test each index type creation
  - Test persistence and loading
  - Test retrieval from each index

## 4. Retrievers

- [ ] 4.1 Implement base retrievers

  - Create src/aitea_llamaindex/retrievers/**init**.py
  - Wrap VectorIndexRetriever
  - Wrap KeywordTableSimpleRetriever
  - Add configurable parameters
  - _Requirements: 2.1_

- [ ] 4.2 Implement HybridRetriever

  - Create src/aitea_llamaindex/retrievers/hybrid.py
  - Combine vector and keyword retrieval
  - Implement result merging and deduplication
  - Add configurable weights
  - _Requirements: 2.1, 2.2, 2.5_

- [ ] 4.3 Implement reranking

  - Create src/aitea_llamaindex/retrievers/rerank.py
  - Integrate SentenceTransformerRerank
  - Implement LLMRerank option
  - Add score normalization
  - _Requirements: 2.3, 2.4_

- [ ] 4.4 Implement query transformation

  - Create src/aitea_llamaindex/retrievers/transform.py
  - Implement HyDE transformation
  - Implement multi-query generation
  - Add query expansion
  - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [ ]\* 4.5 Write tests for retrievers
  - Test hybrid retrieval
  - Test reranking improvement
  - Test query transformation

## 5. Query Engines

- [ ] 5.1 Implement QueryEngineFactory

  - Create src/aitea_llamaindex/query_engines/factory.py
  - Implement create_simple_engine()
  - Add configurable parameters
  - _Requirements: 4.1_

- [ ] 5.2 Implement RouterQueryEngine

  - Create src/aitea_llamaindex/query_engines/router.py
  - Configure query engine tools with descriptions
  - Implement routing logic
  - Add fallback handling
  - _Requirements: 4.2_

- [ ] 5.3 Implement SubQuestionQueryEngine

  - Create src/aitea_llamaindex/query_engines/sub_question.py
  - Configure sub-question generation
  - Implement answer synthesis
  - Add async support
  - _Requirements: 4.3_

- [ ] 5.4 Implement CitationQueryEngine

  - Create src/aitea_llamaindex/query_engines/citation.py
  - Configure citation chunk size
  - Implement citation formatting
  - _Requirements: 4.4, 4.5_

- [ ]\* 5.5 Write tests for query engines
  - Test each engine type
  - Test routing decisions
  - Test citation generation

## 6. ReAct Agent

- [ ] 6.1 Implement custom tools

  - Create src/aitea_llamaindex/agents/tools.py
  - Implement search_features tool
  - Implement get_statistics tool
  - Implement generate_estimate tool
  - Add query engine tool
  - _Requirements: 5.2, 5.3_

- [ ] 6.2 Implement EstimationAgent

  - Create src/aitea_llamaindex/agents/estimation_agent.py
  - Build ReActAgent with tools
  - Configure verbose mode
  - Implement chat() method
  - Add conversation memory
  - _Requirements: 5.1, 5.2, 5.4_

- [ ] 6.3 Add error handling

  - Implement graceful error recovery
  - Add retry logic for tool failures
  - Log reasoning trace
  - _Requirements: 5.5_

- [ ]\* 6.4 Write tests for agent
  - Test tool execution
  - Test multi-step reasoning
  - Test error handling

## 7. Evaluation Framework

- [ ] 7.1 Implement response evaluators

  - Create src/aitea_llamaindex/evaluation/evaluator.py
  - Implement faithfulness evaluation
  - Implement relevancy evaluation
  - Implement correctness evaluation
  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 7.2 Implement retrieval metrics

  - Create src/aitea_llamaindex/evaluation/metrics.py
  - Implement precision calculation
  - Implement recall calculation
  - Implement MRR calculation
  - _Requirements: 6.4_

- [ ] 7.3 Create evaluation datasets

  - Create src/aitea_llamaindex/evaluation/datasets.py
  - Create feature search test cases
  - Create estimation query test cases
  - Create BRD parsing test cases
  - _Requirements: 6.4_

- [ ] 7.4 Implement comparison utilities

  - Create src/aitea_llamaindex/evaluation/comparison.py
  - Implement run_comparison() for LangChain vs LlamaIndex
  - Generate comparison reports
  - Visualize results
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ]\* 7.5 Write tests for evaluation
  - Test metric calculations
  - Test evaluator accuracy

## 8. Integration & CLI Extension

- [ ] 8.1 Create service container

  - Create src/aitea_llamaindex/container.py
  - Initialize all components with dependencies
  - Wire up indices, retrievers, engines, and agent
  - _Requirements: All_

- [ ] 8.2 Extend CLI with LlamaIndex commands

  - Create src/aitea_llamaindex/cli/llamaindex.py
  - Implement `aitea li build-indices` command
  - Implement `aitea li query "<query>"` command
  - Implement `aitea li agent` interactive mode
  - Implement `aitea li evaluate` command
  - _Requirements: All_

- [ ] 8.3 Create package exports
  - Update src/aitea_llamaindex/**init**.py
  - Export main classes and functions
  - Create convenience factory functions
  - _Requirements: All_

## 9. Documentation & Examples

- [ ] 9.1 Create usage examples

  - Create examples/multi_index.py
  - Create examples/hybrid_retrieval.py
  - Create examples/query_engines.py
  - Create examples/react_agent.py
  - Create examples/evaluation.py
  - _Requirements: All_

- [ ] 9.2 Create Jupyter notebooks

  - Create notebooks/01_index_types.ipynb
  - Create notebooks/02_advanced_retrieval.ipynb
  - Create notebooks/03_query_engines.ipynb
  - Create notebooks/04_react_agent.ipynb
  - Create notebooks/05_evaluation_comparison.ipynb
  - _Requirements: All_

- [ ] 9.3 Create comparison documentation

  - Document LangChain vs LlamaIndex differences
  - Provide recommendations for each use case
  - Include benchmark results
  - _Requirements: 8.4, 8.5_

- [ ] 9.4 Checkpoint - Ensure all tests pass
  - Run pytest
  - Verify CLI commands work
  - Run evaluation suite
  - Compare with LangChain version
  - _Requirements: All_
