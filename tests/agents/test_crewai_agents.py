"""Tests for CrewAI multi-agent system.

This module tests the CrewAI implementation including:
- Agent creation
- Tool functionality
- Crew configuration
- Workflow execution (when CrewAI is available)
"""

import pytest
from unittest.mock import Mock, MagicMock

from src.agents.crewai_agents import (
    CREWAI_AVAILABLE,
    EstimationResult,
    FeatureSearchTool,
    EstimationTool,
    ValidationTool,
    create_analyst_agent,
    create_estimator_agent,
    create_reviewer_agent,
    create_estimation_crew,
    get_mock_llm_config,
)
from src.models import Feature, TeamType, FeatureEstimate, ConfidenceLevel, FeatureStatistics
from src.models.result import Result


class TestCrewAIAvailability:
    """Test CrewAI availability detection."""
    
    def test_crewai_availability_flag_exists(self):
        """Test that CREWAI_AVAILABLE flag is defined."""
        assert isinstance(CREWAI_AVAILABLE, bool)


class TestFeatureSearchTool:
    """Test the FeatureSearchTool."""
    
    def test_tool_initialization(self):
        """Test tool can be initialized with a feature service."""
        mock_service = Mock()
        tool = FeatureSearchTool(mock_service)
        
        assert tool.feature_service == mock_service
        assert tool.name == "search_features"
        assert "search" in tool.description.lower()
    
    def test_tool_run_with_results(self):
        """Test tool execution with matching features."""
        mock_service = Mock()
        mock_features = [
            Feature(
                id="f1",
                name="CRUD API",
                team=TeamType.BACKEND,
                process="Data Operations",
                seed_time_hours=4.0,
                synonyms=[],
                notes=""
            ),
            Feature(
                id="f2",
                name="REST CRUD",
                team=TeamType.BACKEND,
                process="Data Operations",
                seed_time_hours=5.0,
                synonyms=[],
                notes=""
            ),
        ]
        mock_service.search_features.return_value = mock_features
        
        tool = FeatureSearchTool(mock_service)
        result = tool._run("CRUD")
        
        assert "Found 2 matching features" in result
        assert "CRUD API" in result
        assert "REST CRUD" in result
        assert "4.0h" in result
        mock_service.search_features.assert_called_once_with("CRUD")
    
    def test_tool_run_no_results(self):
        """Test tool execution with no matching features."""
        mock_service = Mock()
        mock_service.search_features.return_value = []
        
        tool = FeatureSearchTool(mock_service)
        result = tool._run("NonExistent")
        
        assert "No features found" in result
        assert "NonExistent" in result


class TestEstimationTool:
    """Test the EstimationTool."""
    
    def test_tool_initialization(self):
        """Test tool can be initialized with an estimation service."""
        mock_service = Mock()
        tool = EstimationTool(mock_service)
        
        assert tool.estimation_service == mock_service
        assert tool.name == "estimate_feature"
        assert "estimate" in tool.description.lower()
    
    def test_tool_run_with_statistics(self):
        """Test tool execution with full statistics."""
        mock_service = Mock()
        estimate = FeatureEstimate(
            feature_name="CRUD",
            estimated_hours=4.5,
            confidence=ConfidenceLevel.HIGH,
            statistics=FeatureStatistics(
                mean=4.5,
                median=4.0,
                std_dev=1.0,
                p80=5.5,
                data_point_count=10
            )
        )
        mock_service.estimate_feature.return_value = Result.ok(estimate)
        
        tool = EstimationTool(mock_service)
        result = tool._run("CRUD")
        
        assert "CRUD" in result
        assert "4.5h" in result
        assert "high" in result.lower()
        assert "Mean:" in result
        assert "Median:" in result
        assert "P80:" in result
        assert "10" in result  # data point count
    
    def test_tool_run_without_statistics(self):
        """Test tool execution without statistics (seed time fallback)."""
        mock_service = Mock()
        estimate = FeatureEstimate(
            feature_name="NewFeature",
            estimated_hours=3.0,
            confidence=ConfidenceLevel.LOW,
            statistics=None
        )
        mock_service.estimate_feature.return_value = Result.ok(estimate)
        
        tool = EstimationTool(mock_service)
        result = tool._run("NewFeature")
        
        assert "NewFeature" in result
        assert "3.0h" in result
        assert "low" in result.lower()
    
    def test_tool_run_with_error(self):
        """Test tool execution when estimation fails."""
        mock_service = Mock()
        mock_service.estimate_feature.return_value = Result.err("Feature not found")
        
        tool = EstimationTool(mock_service)
        result = tool._run("Unknown")
        
        assert "Error" in result
        assert "Unknown" in result


class TestValidationTool:
    """Test the ValidationTool."""
    
    def test_tool_initialization(self):
        """Test tool can be initialized with an estimation service."""
        mock_service = Mock()
        tool = ValidationTool(mock_service)
        
        assert tool.estimation_service == mock_service
        assert tool.name == "validate_estimate"
        assert "validate" in tool.description.lower()
    
    def test_tool_run_within_normal_range(self):
        """Test validation when estimate is within normal range."""
        mock_service = Mock()
        estimate = FeatureEstimate(
            feature_name="CRUD",
            estimated_hours=4.5,
            confidence=ConfidenceLevel.HIGH,
            statistics=FeatureStatistics(
                mean=4.5,
                median=4.0,
                std_dev=1.0,
                p80=5.5,
                data_point_count=10
            )
        )
        mock_service.estimate_feature.return_value = Result.ok(estimate)
        
        tool = ValidationTool(mock_service)
        result = tool._run("CRUD", 4.8)
        
        assert "CRUD" in result
        assert "4.8h" in result
        assert "4.5h" in result  # historical mean
        assert "✓" in result or "within normal range" in result.lower()
    
    def test_tool_run_high_deviation(self):
        """Test validation when estimate deviates significantly."""
        mock_service = Mock()
        estimate = FeatureEstimate(
            feature_name="CRUD",
            estimated_hours=4.5,
            confidence=ConfidenceLevel.HIGH,
            statistics=FeatureStatistics(
                mean=4.5,
                median=4.0,
                std_dev=1.0,
                p80=5.5,
                data_point_count=10
            )
        )
        mock_service.estimate_feature.return_value = Result.ok(estimate)
        
        tool = ValidationTool(mock_service)
        result = tool._run("CRUD", 10.0)  # 5.5 std devs away
        
        assert "CRUD" in result
        assert "10.0h" in result
        assert "WARNING" in result or "⚠️" in result
    
    def test_tool_run_no_historical_data(self):
        """Test validation when no historical data exists."""
        mock_service = Mock()
        mock_service.estimate_feature.return_value = Result.err("No data")
        
        tool = ValidationTool(mock_service)
        result = tool._run("NewFeature", 5.0)
        
        assert "Cannot validate" in result
        assert "NewFeature" in result


@pytest.mark.skipif(not CREWAI_AVAILABLE, reason="CrewAI not installed")
class TestAgentCreation:
    """Test agent creation functions (requires CrewAI)."""
    
    def test_create_analyst_agent(self):
        """Test Analyst agent creation."""
        mock_service = Mock()
        agent = create_analyst_agent(mock_service)
        
        assert agent.role == "Requirements Analyst"
        assert "extract" in agent.goal.lower() or "clarify" in agent.goal.lower()
        assert len(agent.tools) > 0
        assert not agent.allow_delegation
    
    def test_create_estimator_agent(self):
        """Test Estimator agent creation."""
        mock_service = Mock()
        agent = create_estimator_agent(mock_service)
        
        assert agent.role == "Estimation Specialist"
        assert "estimate" in agent.goal.lower()
        assert len(agent.tools) > 0
        assert not agent.allow_delegation
    
    def test_create_reviewer_agent(self):
        """Test Reviewer agent creation."""
        mock_service = Mock()
        agent = create_reviewer_agent(mock_service)
        
        assert agent.role == "Estimate Reviewer"
        assert "validate" in agent.goal.lower() or "review" in agent.goal.lower()
        assert len(agent.tools) > 0
        assert not agent.allow_delegation


@pytest.mark.skipif(not CREWAI_AVAILABLE, reason="CrewAI not installed")
class TestCrewCreation:
    """Test crew creation and configuration (requires CrewAI)."""
    
    def test_create_sequential_crew(self):
        """Test creating a crew with sequential process."""
        mock_feature_service = Mock()
        mock_estimation_service = Mock()
        
        crew = create_estimation_crew(
            mock_feature_service,
            mock_estimation_service,
            process_type="sequential"
        )
        
        assert len(crew.agents) == 3
        assert len(crew.tasks) == 3
        assert crew.verbose is True
    
    def test_create_hierarchical_crew(self):
        """Test creating a crew with hierarchical process."""
        mock_feature_service = Mock()
        mock_estimation_service = Mock()
        
        crew = create_estimation_crew(
            mock_feature_service,
            mock_estimation_service,
            process_type="hierarchical"
        )
        
        assert len(crew.agents) == 3
        assert len(crew.tasks) == 3
    
    def test_invalid_process_type(self):
        """Test that invalid process type raises ValueError."""
        mock_feature_service = Mock()
        mock_estimation_service = Mock()
        
        with pytest.raises(ValueError, match="Invalid process_type"):
            create_estimation_crew(
                mock_feature_service,
                mock_estimation_service,
                process_type="invalid"
            )


class TestCrewAINotInstalled:
    """Test behavior when CrewAI is not installed."""
    
    @pytest.mark.skipif(CREWAI_AVAILABLE, reason="CrewAI is installed")
    def test_agent_creation_raises_import_error(self):
        """Test that agent creation raises ImportError when CrewAI not installed."""
        mock_service = Mock()
        
        with pytest.raises(ImportError, match="CrewAI is not installed"):
            create_analyst_agent(mock_service)
        
        with pytest.raises(ImportError, match="CrewAI is not installed"):
            create_estimator_agent(mock_service)
        
        with pytest.raises(ImportError, match="CrewAI is not installed"):
            create_reviewer_agent(mock_service)
    
    @pytest.mark.skipif(CREWAI_AVAILABLE, reason="CrewAI is installed")
    def test_crew_creation_raises_import_error(self):
        """Test that crew creation raises ImportError when CrewAI not installed."""
        mock_feature_service = Mock()
        mock_estimation_service = Mock()
        
        with pytest.raises(ImportError, match="CrewAI is not installed"):
            create_estimation_crew(mock_feature_service, mock_estimation_service)


class TestMockLLMConfig:
    """Test mock LLM configuration helper."""
    
    def test_get_mock_llm_config(self):
        """Test that mock LLM config is returned correctly."""
        config = get_mock_llm_config()
        
        assert isinstance(config, dict)
        assert "model" in config
        assert config["model"] == "mock"
        assert "temperature" in config


class TestEstimationResult:
    """Test EstimationResult dataclass."""
    
    def test_estimation_result_creation(self):
        """Test creating an EstimationResult."""
        result = EstimationResult(
            features_extracted=["CRUD", "Auth", "Search"],
            estimates=None,
            review_notes="Estimates look reasonable",
            risks_identified=["Limited historical data for Auth"],
            confidence_assessment="Medium"
        )
        
        assert len(result.features_extracted) == 3
        assert result.estimates is None
        assert "reasonable" in result.review_notes
        assert len(result.risks_identified) == 1
        assert result.confidence_assessment == "Medium"
