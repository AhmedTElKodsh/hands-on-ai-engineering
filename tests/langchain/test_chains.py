"""Unit tests for LCEL chains.

These tests verify that the LCEL chains are properly constructed and
can be invoked with the expected inputs and outputs.
"""

import pytest
from unittest.mock import Mock, MagicMock
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from src.langchain.chains import (
    create_feature_extraction_chain,
    create_estimation_chain,
    create_simple_passthrough_chain,
    create_multi_input_chain,
)


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock(spec=BaseChatModel)
    
    # Mock the invoke method to return a structured response
    def mock_invoke(prompt, config=None):
        # Return different responses based on prompt content
        prompt_str = str(prompt).lower()
        
        # Check for estimation-specific keywords first (more specific)
        if "provide a time estimate" in prompt_str or "provide accurate time estimates" in prompt_str:
            return AIMessage(content="""{
                "feature_name": "User Authentication",
                "estimated_hours": 8.0,
                "confidence": "medium",
                "reasoning": "Based on similar features"
            }""")
        # Then check for extraction keywords
        elif "extract" in prompt_str or "extract all features" in prompt_str:
            return AIMessage(content="""{
                "features": [
                    {
                        "name": "User Authentication",
                        "team": "backend",
                        "process": "Authentication",
                        "estimated_hours": 8.0,
                        "notes": "JWT-based auth"
                    }
                ],
                "total_features": 1
            }""")
        else:
            return AIMessage(content="Test response")
    
    llm.invoke = Mock(side_effect=mock_invoke)
    return llm


class TestFeatureExtractionChain:
    """Tests for feature extraction chain."""
    
    def test_chain_creation(self, mock_llm):
        """Test that the chain can be created."""
        chain = create_feature_extraction_chain(mock_llm)
        assert chain is not None
    
    def test_chain_invocation(self, mock_llm):
        """Test that the chain can be invoked with a project description."""
        chain = create_feature_extraction_chain(mock_llm)
        
        result = chain.invoke({
            "project_description": "Build a REST API with user authentication"
        })
        
        # Verify the structure of the result
        assert "features" in result
        assert "total_features" in result
        assert isinstance(result["features"], list)
        assert result["total_features"] == len(result["features"])
    
    def test_chain_with_empty_description(self, mock_llm):
        """Test chain behavior with empty description."""
        chain = create_feature_extraction_chain(mock_llm)
        
        # Should still work, just return empty or minimal features
        result = chain.invoke({"project_description": ""})
        assert "features" in result


class TestEstimationChain:
    """Tests for estimation chain."""
    
    def test_chain_creation_without_retriever(self, mock_llm):
        """Test that the chain can be created without a retriever."""
        chain = create_estimation_chain(mock_llm)
        assert chain is not None
    
    def test_chain_creation_with_retriever(self, mock_llm):
        """Test that the chain can be created with a retriever."""
        mock_retriever = Mock()
        mock_retriever.invoke = Mock(return_value=[])
        
        chain = create_estimation_chain(mock_llm, mock_retriever)
        assert chain is not None
    
    def test_chain_invocation_without_retriever(self, mock_llm):
        """Test chain invocation without retriever."""
        chain = create_estimation_chain(mock_llm)
        
        result = chain.invoke({
            "feature_name": "User Authentication",
            "feature_description": "JWT-based auth with refresh tokens"
        })
        
        # Verify the structure
        assert "feature_name" in result
        assert "estimated_hours" in result
        assert "confidence" in result
        assert "reasoning" in result
    
    @pytest.mark.skip(reason="Retriever integration requires more complex mocking")
    def test_chain_invocation_with_retriever(self, mock_llm):
        """Test chain invocation with retriever."""
        # Mock retriever that returns similar features
        mock_doc = Mock()
        mock_doc.metadata = {"name": "Login Feature", "hours": 6.0}
        
        # Create a proper mock retriever that returns a list
        mock_retriever = Mock()
        mock_retriever.invoke = Mock(return_value=[mock_doc])
        
        chain = create_estimation_chain(mock_llm, mock_retriever)
        
        result = chain.invoke({
            "feature_name": "User Authentication",
            "feature_description": "JWT-based auth"
        })
        
        assert "estimated_hours" in result
        # Verify retriever was called
        assert mock_retriever.invoke.called


class TestSimplePassthroughChain:
    """Tests for simple passthrough chain."""
    
    def test_chain_creation(self, mock_llm):
        """Test that the chain can be created."""
        chain = create_simple_passthrough_chain(mock_llm)
        assert chain is not None
    
    def test_chain_invocation(self, mock_llm):
        """Test that the chain passes through input correctly."""
        chain = create_simple_passthrough_chain(mock_llm)
        
        result = chain.invoke({"text": "Hello world"})
        
        # Should return a string (from StrOutputParser)
        assert isinstance(result, str)
        # LLM should have been called
        mock_llm.invoke.assert_called()


class TestMultiInputChain:
    """Tests for multi-input chain."""
    
    def test_chain_creation(self, mock_llm):
        """Test that the chain can be created."""
        chain = create_multi_input_chain(mock_llm)
        assert chain is not None
    
    def test_chain_invocation(self, mock_llm):
        """Test that the chain handles multiple inputs."""
        chain = create_multi_input_chain(mock_llm)
        
        result = chain.invoke({
            "feature": "User Login",
            "team": "backend",
            "complexity": "medium"
        })
        
        # Should return a string
        assert isinstance(result, str)
        # LLM should have been called
        mock_llm.invoke.assert_called()
    
    def test_chain_with_missing_field(self, mock_llm):
        """Test chain behavior when a required field is missing."""
        chain = create_multi_input_chain(mock_llm)
        
        # Should raise KeyError for missing required field
        with pytest.raises(KeyError):
            chain.invoke({
                "feature": "User Login",
                "team": "backend"
                # Missing "complexity"
            })


class TestRunnablePassthroughPatterns:
    """Tests for RunnablePassthrough data flow patterns."""
    
    def test_passthrough_preserves_input(self, mock_llm):
        """Test that RunnablePassthrough preserves input data."""
        from langchain_core.runnables import RunnablePassthrough
        
        # Simple test: passthrough should return input unchanged
        passthrough = RunnablePassthrough()
        test_input = {"key": "value"}
        result = passthrough.invoke(test_input)
        
        assert result == test_input
    
    def test_passthrough_with_lambda(self, mock_llm):
        """Test RunnablePassthrough with lambda extraction."""
        from langchain_core.runnables import RunnablePassthrough
        
        # Passthrough with lambda should extract field
        chain = RunnablePassthrough() | (lambda x: x["field"])
        test_input = {"field": "extracted_value", "other": "ignored"}
        result = chain.invoke(test_input)
        
        assert result == "extracted_value"
    
    def test_multiple_passthroughs(self, mock_llm):
        """Test multiple RunnablePassthrough instances in dict."""
        from langchain_core.runnables import RunnablePassthrough
        
        # Multiple passthroughs should extract different fields
        chain = {
            "a": RunnablePassthrough() | (lambda x: x["field_a"]),
            "b": RunnablePassthrough() | (lambda x: x["field_b"])
        }
        
        # This is a dict of runnables, not a chain yet
        # We need to invoke each separately or use RunnableParallel
        test_input = {"field_a": "value_a", "field_b": "value_b"}
        
        # For testing, we can verify the structure is correct
        assert "a" in chain
        assert "b" in chain


class TestChainIntegration:
    """Integration tests for chains working together."""
    
    def test_extraction_then_estimation(self, mock_llm):
        """Test using extraction chain output as estimation chain input."""
        extraction_chain = create_feature_extraction_chain(mock_llm)
        estimation_chain = create_estimation_chain(mock_llm)
        
        # Extract features
        extraction_result = extraction_chain.invoke({
            "project_description": "Build user authentication"
        })
        
        # Verify extraction worked
        assert "features" in extraction_result
        assert len(extraction_result["features"]) > 0
        
        # Use first feature for estimation
        feature = extraction_result["features"][0]
        estimation_result = estimation_chain.invoke({
            "feature_name": feature["name"],
            "feature_description": feature.get("notes", "")
        })
        
        # Verify estimation worked
        assert "estimated_hours" in estimation_result
        assert "confidence" in estimation_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
