"""Tests for LangGraph BRD Parser Agent.

These tests verify the BRD parser agent implementation including:
- StateGraph construction
- Node execution
- Conditional edges
- Memory persistence
- Human-in-the-loop workflow

Requirements: 6.4
"""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any

try:
    from src.langchain.brd_parser_agent import (
        BRDParserAgent,
        create_brd_parser_agent,
        ExtractedFeature,
        BRDParseResult,
        AgentState,
        LANGGRAPH_AVAILABLE,
    )
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="LangGraph not available")


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock()
    llm.invoke = Mock(return_value=Mock(content="Mock LLM response"))
    return llm


@pytest.fixture
def sample_brd_text():
    """Sample BRD text for testing."""
    return """
    # Project Requirements
    
    ## Feature 1: User Authentication
    Implement JWT-based authentication.
    Team: Backend
    Estimate: 40 hours
    
    ## Feature 2: Dashboard
    Create admin dashboard.
    Team: Frontend
    Estimate: 60 hours
    """


class TestBRDParserAgent:
    """Test suite for BRD Parser Agent."""
    
    def test_agent_creation(self, mock_llm):
        """Test that agent can be created successfully."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        assert agent is not None
        assert agent.llm == mock_llm
        assert agent.graph is not None
    
    def test_agent_creation_with_memory(self, mock_llm):
        """Test that agent can be created with memory enabled."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=True)
        assert agent is not None
        assert agent.enable_memory is True
    
    def test_factory_function(self, mock_llm):
        """Test the factory function creates agent correctly."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = create_brd_parser_agent(mock_llm)
        assert isinstance(agent, BRDParserAgent)
        assert agent.llm == mock_llm
    
    def test_extract_features_node(self, mock_llm, sample_brd_text):
        """Test the extract_features node."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # Create initial state
        state: AgentState = {
            "brd_text": sample_brd_text,
            "messages": [],
            "features": [],
            "clarifications_needed": [],
            "current_step": "start",
            "needs_human_review": False,
            "human_feedback": None,
            "result": None,
        }
        
        # Execute node
        result = agent._extract_features_node(state)
        
        # Verify results
        assert "messages" in result
        assert "features" in result
        assert "current_step" in result
        assert result["current_step"] == "extract_features"
        assert len(result["features"]) > 0
    
    def test_validate_features_node(self, mock_llm):
        """Test the validate_features node."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # Create state with features
        feature = ExtractedFeature(
            name="Test Feature",
            description="Test description",
            team="backend",
            estimated_hours=10.0,
            confidence="high",
            dependencies=[]
        )
        
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": [feature],
            "clarifications_needed": [],
            "current_step": "extract_features",
            "needs_human_review": False,
            "human_feedback": None,
            "result": None,
        }
        
        # Execute node
        result = agent._validate_features_node(state)
        
        # Verify results
        assert "messages" in result
        assert "current_step" in result
        assert result["current_step"] == "validate_features"
    
    def test_identify_clarifications_node(self, mock_llm):
        """Test the identify_clarifications node."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # Create state with low confidence feature
        feature = ExtractedFeature(
            name="Test Feature",
            description="Test description",
            team="backend",
            estimated_hours=10.0,
            confidence="low",  # Low confidence should trigger clarification
            dependencies=[]
        )
        
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": [feature],
            "clarifications_needed": [],
            "current_step": "validate_features",
            "needs_human_review": False,
            "human_feedback": None,
            "result": None,
        }
        
        # Execute node
        result = agent._identify_clarifications_node(state)
        
        # Verify results
        assert "messages" in result
        assert "clarifications_needed" in result
        assert "needs_human_review" in result
        assert result["current_step"] == "identify_clarifications"
        # Low confidence should trigger clarification
        assert len(result["clarifications_needed"]) > 0
        assert result["needs_human_review"] is True
    
    def test_conditional_edge_human_review_needed(self, mock_llm):
        """Test conditional edge when human review is needed."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # State with human review needed
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": [],
            "clarifications_needed": ["Item 1"],
            "current_step": "identify_clarifications",
            "needs_human_review": True,
            "human_feedback": None,
            "result": None,
        }
        
        # Test conditional edge
        next_node = agent._should_request_human_review(state)
        assert next_node == "human_review"
    
    def test_conditional_edge_no_human_review(self, mock_llm):
        """Test conditional edge when human review is not needed."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # State without human review needed
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": [],
            "clarifications_needed": [],
            "current_step": "identify_clarifications",
            "needs_human_review": False,
            "human_feedback": None,
            "result": None,
        }
        
        # Test conditional edge
        next_node = agent._should_request_human_review(state)
        assert next_node == "finalize"
    
    def test_request_human_review_node(self, mock_llm):
        """Test the request_human_review node."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": [],
            "clarifications_needed": ["Item 1", "Item 2"],
            "current_step": "identify_clarifications",
            "needs_human_review": True,
            "human_feedback": "Approved",
            "result": None,
        }
        
        # Execute node
        result = agent._request_human_review_node(state)
        
        # Verify results
        assert "messages" in result
        assert "current_step" in result
        assert result["current_step"] == "request_human_review"
    
    def test_finalize_results_node(self, mock_llm):
        """Test the finalize_results node."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        agent = BRDParserAgent(mock_llm, enable_memory=False)
        
        # Create state with features
        features = [
            ExtractedFeature(
                name="Feature 1",
                description="Description 1",
                team="backend",
                estimated_hours=10.0,
                confidence="high",
                dependencies=[]
            ),
            ExtractedFeature(
                name="Feature 2",
                description="Description 2",
                team="frontend",
                estimated_hours=15.0,
                confidence="medium",
                dependencies=[]
            ),
        ]
        
        state: AgentState = {
            "brd_text": "",
            "messages": [],
            "features": features,
            "clarifications_needed": [],
            "current_step": "identify_clarifications",
            "needs_human_review": False,
            "human_feedback": None,
            "result": None,
        }
        
        # Execute node
        result = agent._finalize_results_node(state)
        
        # Verify results
        assert "messages" in result
        assert "result" in result
        assert "current_step" in result
        assert result["current_step"] == "finalize_results"
        
        # Check result structure
        parse_result = result["result"]
        assert isinstance(parse_result, BRDParseResult)
        assert parse_result.total_features == 2
        assert parse_result.total_hours == 25.0
        assert len(parse_result.features) == 2


class TestExtractedFeature:
    """Test suite for ExtractedFeature model."""
    
    def test_feature_creation(self):
        """Test creating an ExtractedFeature."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        feature = ExtractedFeature(
            name="User Auth",
            description="JWT authentication",
            team="backend",
            estimated_hours=40.0,
            confidence="high",
            dependencies=["Database Setup"]
        )
        
        assert feature.name == "User Auth"
        assert feature.description == "JWT authentication"
        assert feature.team == "backend"
        assert feature.estimated_hours == 40.0
        assert feature.confidence == "high"
        assert len(feature.dependencies) == 1
    
    def test_feature_default_dependencies(self):
        """Test that dependencies default to empty list."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        feature = ExtractedFeature(
            name="Test",
            description="Test",
            team="backend",
            estimated_hours=10.0,
            confidence="medium"
        )
        
        assert feature.dependencies == []


class TestBRDParseResult:
    """Test suite for BRDParseResult model."""
    
    def test_result_creation(self):
        """Test creating a BRDParseResult."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        features = [
            ExtractedFeature(
                name="Feature 1",
                description="Desc 1",
                team="backend",
                estimated_hours=10.0,
                confidence="high",
                dependencies=[]
            )
        ]
        
        result = BRDParseResult(
            features=features,
            total_features=1,
            total_hours=10.0,
            needs_clarification=["Item 1"]
        )
        
        assert len(result.features) == 1
        assert result.total_features == 1
        assert result.total_hours == 10.0
        assert len(result.needs_clarification) == 1
    
    def test_result_default_clarifications(self):
        """Test that needs_clarification defaults to empty list."""
        if not AGENT_AVAILABLE:
            pytest.skip("LangGraph not available")
        
        result = BRDParseResult(
            features=[],
            total_features=0,
            total_hours=0.0
        )
        
        assert result.needs_clarification == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
