"""
Test suite for Chapter 17: Your First RAG System

Tests verify that students can implement:
1. Knowledge base ingestion with metadata tracking
2. RAG query pipeline (retrieve, augment, generate)
3. Citation tracking with source metadata
4. Hallucination prevention through grounding
5. Property P20: Consistency with Context

These tests are designed to run with stub implementations (will skip until implemented).
"""

import pytest
from typing import List, Tuple, Dict, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestKnowledgeBaseIngestion:
    """Tests for knowledge base ingestion functionality."""

    def test_ingest_function_exists(self):
        """Test that ingest_knowledge_base function exists."""
        try:
            # Try to import from the expected location
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "simple_rag",
                "simple_rag.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                assert hasattr(module, 'ingest_knowledge_base')
                assert callable(module.ingest_knowledge_base)
            else:
                pytest.skip("simple_rag.py not yet created")
        except (FileNotFoundError, ImportError, AttributeError):
            pytest.skip("ingest_knowledge_base function not yet implemented")

    def test_ingest_adds_documents_to_store(self):
        """Test that ingestion adds documents with correct IDs and metadata."""
        try:
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Create test store
                store = VectorStore(path="./test_ingest_db", collection_name="test_ingest")
                
                # Test data
                test_docs = [
                    "Test document 1",
                    "Test document 2"
                ]
                
                # Ingest
                module.ingest_knowledge_base(store, test_docs)
                
                # Verify documents were added (search should return results)
                results = store.search("Test document", limit=2)
                assert len(results) > 0, "Documents should be searchable after ingestion"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Ingestion not yet fully implemented")

    def test_ingest_preserves_metadata(self):
        """Test that metadata is preserved during ingestion."""
        try:
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                store = VectorStore(path="./test_metadata_db", collection_name="test_metadata")
                test_docs = ["Document with metadata"]
                
                module.ingest_knowledge_base(store, test_docs)
                
                # If store has search_with_metadata, verify metadata exists
                if hasattr(store, 'search_with_metadata'):
                    results = store.search_with_metadata("Document", limit=1)
                    assert len(results) > 0
                    doc, metadata = results[0]
                    assert 'source' in metadata, "Metadata should include source field"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Metadata tracking not yet implemented")


class TestRAGQueryPipeline:
    """Tests for RAG query pipeline (retrieve, augment, generate)."""

    def test_ask_rag_function_exists(self):
        """Test that ask_rag function exists and is callable."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                assert hasattr(module, 'ask_rag')
                assert callable(module.ask_rag)
            else:
                pytest.skip("simple_rag.py not yet created")
        except (FileNotFoundError, ImportError, AttributeError):
            pytest.skip("ask_rag function not yet implemented")

    def test_ask_rag_returns_string(self):
        """Test that ask_rag returns a string answer."""
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Setup
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_rag_db", collection_name="test_rag")
                
                # Add test data
                test_docs = ["The capital of France is Paris."]
                module.ingest_knowledge_base(store, test_docs)
                
                # Query
                answer = module.ask_rag("What is the capital of France?", store, client)
                
                assert isinstance(answer, str), "ask_rag should return a string"
                assert len(answer) > 0, "Answer should not be empty"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("RAG pipeline not yet fully implemented")

    def test_ask_rag_retrieves_relevant_context(self):
        """Test that RAG retrieves relevant documents from vector store."""
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_retrieval_db", collection_name="test_retrieval")
                
                # Add specific knowledge
                test_docs = [
                    "Project Alpha is a bridge construction project.",
                    "The lead engineer is Sarah Jones.",
                    "Unrelated fact about bananas."
                ]
                module.ingest_knowledge_base(store, test_docs)
                
                # Query about Project Alpha
                answer = module.ask_rag("What is Project Alpha?", store, client)
                
                # Answer should mention bridge or construction (from relevant docs)
                assert "bridge" in answer.lower() or "construction" in answer.lower(), \
                    "Answer should be based on relevant retrieved context"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Context retrieval not yet implemented") spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_retrieval_db", collection_name="test_retrieval")
                
                # Add specific knowledge
                test_docs = [
                    "Project Alpha is a bridge construction project.",
                    "The lead engineer is Sarah Jones.",
                    "Unrelated fact about bananas."
                ]
                module.ingest_knowledge_base(store, test_docs)
                
                # Query about Project Alpha
                answer = module.ask_rag("What is Project Alpha?", store, client)
                
                # Answer should mention bridge or construction (from relevant docs)
                assert "bridge" in answer.lower() or "construction" in answer.lower(), \
                    "Answer should be based on relevant retrieved context"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Context retrieval not yet implemented")

    def test_ask_rag_handles_unknown_questions(self):
        """Test that RAG says 'I don't know' for questions without context."""
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_unknown_db", collection_name="test_unknown")
                
                # Add knowledge about bridges only
                test_docs = ["Project Alpha is a bridge project."]
                module.ingest_knowledge_base(store, test_docs)
                
                # Ask about something completely unrelated
                answer = module.ask_rag("Who is the CEO of Google?", store, client)
                
                # Should indicate lack of knowledge
                unknown_indicators = ["don't know", "do not know", "not in the context", 
                                     "cannot answer", "no information"]
                assert any(indicator in answer.lower() for indicator in unknown_indicators), \
                    "RAG should indicate when answer is not in context"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Unknown question handling not yet implemented")


class TestCitationTracking:
    """Tests for citation and source tracking functionality."""

    def test_search_with_sources_function_exists(self):
        """Test that search_with_sources function exists."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("rag_citations", "rag_citations.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                assert hasattr(module, 'search_with_sources')
                assert callable(module.search_with_sources)
            else:
                pytest.skip("rag_citations.py not yet created")
        except (FileNotFoundError, ImportError, AttributeError):
            pytest.skip("search_with_sources function not yet implemented")

    def test_search_with_sources_returns_metadata(self):
        """Test that search returns both documents and metadata."""
        try:
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("rag_citations", "rag_citations.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Setup store with metadata
                store = VectorStore(path="./test_citation_db", collection_name="test_citation")
                store.add_document(
                    doc_id="1",
                    text="Test fact about citations",
                    metadata={"source": "test_document.txt"}
                )
                
                # Search with sources
                results = module.search_with_sources(store, "citations", limit=1)
                
                assert isinstance(results, list), "Should return a list"
                assert len(results) > 0, "Should find at least one result"
                
                # Check tuple structure
                doc, metadata = results[0]
                assert isinstance(doc, str), "Document should be a string"
                assert isinstance(metadata, dict), "Metadata should be a dictionary"
                assert 'source' in metadata, "Metadata should include source"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Citation tracking not yet implemented")


class TestHallucinationPrevention:
    """Tests for hallucination prevention through grounding."""

    def test_hallucination_prevention_function_exists(self):
        """Test that test_hallucination_prevention function exists."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("hallucination_test", "hallucination_test.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                assert hasattr(module, 'test_hallucination_prevention')
                assert callable(module.test_hallucination_prevention)
            else:
                pytest.skip("hallucination_test.py not yet created")
        except (FileNotFoundError, ImportError, AttributeError):
            pytest.skip("test_hallucination_prevention function not yet implemented")

    def test_grounding_overrides_training_data(self):
        """Test that grounded prompts override LLM training data."""
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("hallucination_test", "hallucination_test.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                
                # Counter-factual context
                context = "In this hypothetical world, the sky is neon green."
                question = "What color is the sky?"
                
                bad_answer, good_answer = module.test_hallucination_prevention(client, context, question)
                
                # Good answer should mention green (from context)
                assert "green" in good_answer.lower(), \
                    "Grounded prompt should use context (green) not training data (blue)"
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Hallucination prevention not yet implemented")


class TestPropertyP20Consistency:
    """Property-based tests for P20: Consistency with Context."""

    def test_p20_rag_uses_context_not_training(self):
        """
        Property P20: RAG system must use provided context, not LLM training data.
        
        This is the core correctness property for RAG systems.
        """
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_p20_db", collection_name="test_p20")
                
                # Counter-factual knowledge: Override real-world facts
                counter_factual_docs = [
                    "The Eiffel Tower is located in London, England.",
                    "Water boils at 50 degrees Celsius at sea level.",
                    "The moon is made of aged cheddar cheese."
                ]
                module.ingest_knowledge_base(store, counter_factual_docs)
                
                # Test 1: Eiffel Tower location
                answer1 = module.ask_rag("Where is the Eiffel Tower?", store, client)
                assert "london" in answer1.lower(), \
                    "P20 Failed: Should use context (London) not training data (Paris)"
                
                # Test 2: Water boiling point
                answer2 = module.ask_rag("At what temperature does water boil?", store, client)
                assert "50" in answer2, \
                    "P20 Failed: Should use context (50°C) not training data (100°C)"
                
                # Test 3: Moon composition
                answer3 = module.ask_rag("What is the moon made of?", store, client)
                assert "cheese" in answer3.lower(), \
                    "P20 Failed: Should use context (cheese) not training data (rock)"
                
                print("✅ P20 Passed: RAG system consistently uses context over training data")
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("P20 property test requires full RAG implementation")

    def test_p20_empty_context_returns_unknown(self):
        """
        Property P20 (Edge Case): When no relevant context exists, RAG must not hallucinate.
        """
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_p20_empty_db", collection_name="test_p20_empty")
                
                # Add knowledge about topic A only
                docs = ["Topic A: Information about bridges and construction."]
                module.ingest_knowledge_base(store, docs)
                
                # Ask about completely unrelated topic B
                answer = module.ask_rag("What is quantum entanglement?", store, client)
                
                # Should indicate lack of knowledge
                unknown_indicators = ["don't know", "do not know", "not in the context",
                                     "cannot answer", "no information", "unknown"]
                assert any(indicator in answer.lower() for indicator in unknown_indicators), \
                    "P20 Failed: Should say 'I don't know' when context is irrelevant"
                
                print("✅ P20 Edge Case Passed: RAG refuses to answer without relevant context")
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("P20 edge case test requires full RAG implementation")


class TestIntegration:
    """Integration tests for complete RAG pipeline."""

    def test_full_rag_pipeline(self):
        """Test complete RAG workflow: ingest → query → answer with citations."""
        try:
            from shared.infrastructure.llm.client import MultiProviderClient
            from shared.infrastructure.vector_store import VectorStore
            import importlib.util
            
            # Load both modules
            rag_spec = importlib.util.spec_from_file_location("simple_rag", "simple_rag.py")
            citation_spec = importlib.util.spec_from_file_location("rag_citations", "rag_citations.py")
            
            if rag_spec and rag_spec.loader and citation_spec and citation_spec.loader:
                rag_module = importlib.util.module_from_spec(rag_spec)
                rag_spec.loader.exec_module(rag_module)
                
                citation_module = importlib.util.module_from_spec(citation_spec)
                citation_spec.loader.exec_module(citation_module)
                
                # Setup
                client = MultiProviderClient(provider="openai")
                store = VectorStore(path="./test_integration_db", collection_name="test_integration")
                
                # Phase 1: Ingest
                knowledge = [
                    "Project Alpha is a floating bridge construction project.",
                    "The lead engineer for Project Alpha is Sarah Jones.",
                    "The budget is $500 million."
                ]
                rag_module.ingest_knowledge_base(store, knowledge)
                
                # Phase 2: Query
                answer = rag_module.ask_rag("Who is the lead engineer?", store, client)
                assert "sarah" in answer.lower() and "jones" in answer.lower(), \
                    "Should correctly identify Sarah Jones from context"
                
                # Phase 3: Citations
                results = citation_module.search_with_sources(store, "Sarah Jones", limit=1)
                assert len(results) > 0, "Should find source for Sarah Jones"
                doc, metadata = results[0]
                assert "sarah" in doc.lower(), "Retrieved document should mention Sarah"
                assert 'source' in metadata, "Should have source metadata"
                
                print("✅ Integration Test Passed: Full RAG pipeline works end-to-end")
                
        except (ImportError, NotImplementedError, AttributeError):
            pytest.skip("Integration test requires all RAG components implemented")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
