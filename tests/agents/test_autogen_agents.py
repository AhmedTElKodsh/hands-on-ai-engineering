"""Tests for AutoGen conversational agents.

These tests verify the AutoGen agent implementations for AITEA,
including AssistantAgent, UserProxyAgent, and GroupChat functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from src.agents.autogen_agents import (
    AUTOGEN_AVAILABLE,
    ConversationResult,
    create_estimation_assistant,
    create_user_proxy,
    create_group_chat,
    run_estimation_conversation,
    run_group_estimation,
    add_code_execution_tool,
)
from src.models import Feature, TeamType, ConfidenceLevel, FeatureEstimate, FeatureStatistics, Result


# Skip all tests if AutoGen is not installed
pytestmark = pytest.mark.skipif(
    not AUTOGEN_AVAILABLE,
    reason="AutoGen not installed"
)


@pytest.fixture
def mock_feature_service():
    """Create a mock feature library service."""
    service = Mock()
    
    # Mock search_features
    service.search_features.return_value = [
        Feature(
            id="feat_001",
            name="CRUD",
            team=TeamType.BACKEND,
            process="Data Operations",
            seed_time_hours=4.0,
            synonyms=["crud-api"],
            notes="Basic CRUD operations"
        ),
        Feature(
            id="feat_002",
            name="Authentication",
            team=TeamType.BACKEND,
            process="Authentication",
            seed_time_hours=6.0,
            synonyms=["auth", "login"],
            notes="User authentication"
        ),
    ]
    
    return service


@pytest.fixture
def mock_estimation_service():
    """Create a mock estimation service."""
    service = Mock()
    
    # Mock estimate_feature
    estimate = FeatureEstimate(
        feature_name="CRUD",
        estimated_hours=4.2,
        confidence=ConfidenceLevel.HIGH,
        statistics=FeatureStatistics(
            mean=4.2,
            median=4.0,
            std_dev=0.8,
            p80=5.0,
            data_point_count=12,
        )
    )
    service.estimate_feature.return_value = Result.ok(estimate)
    
    # Mock estimate_project
    from src.models import ProjectEstimate
    project_estimate = ProjectEstimate(
        features=[estimate],
        total_hours=4.2,
        confidence=ConfidenceLevel.HIGH,
    )
    service.estimate_project.return_value = Result.ok(project_estimate)
    
    return service


@pytest.fixture
def llm_config():
    """LLM configuration for testing."""
    return {
        "model": "gpt-4",
        "temperature": 0.7,
        "timeout": 120,
    }


class TestAssistantAgent:
    """Tests for AssistantAgent creation and configuration."""
    
    def test_create_estimation_assistant(self, mock_feature_service, mock_estimation_service, llm_config):
        """Test creating an estimation assistant agent."""
        assistant = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
        )
        
        assert assistant is not None
        assert assistant.name == "EstimationAssistant"
        assert "estimation assistant" in assistant.system_message.lower()
    
    def test_assistant_with_custom_name(self, mock_feature_service, mock_estimation_service, llm_config):
        """Test creating assistant with custom name."""
        assistant = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
            name="CustomAssistant",
        )
        
        assert assistant.name == "CustomAssistant"
    
    def test_assistant_without_llm_config(self, mock_feature_service, mock_estimation_service):
        """Test creating assistant with default LLM config."""
        assistant = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config=None,
        )
        
        assert assistant is not None
        # Should use default config
        assert assistant.llm_config is not None


class TestUserProxyAgent:
    """Tests for UserProxyAgent creation and configuration."""
    
    def test_create_user_proxy_default(self):
        """Test creating user proxy with default settings."""
        user_proxy = create_user_proxy()
        
        assert user_proxy is not None
        assert user_proxy.name == "ProjectManager"
        assert user_proxy.human_input_mode == "TERMINATE"
    
    def test_create_user_proxy_custom_settings(self):
        """Test creating user proxy with custom settings."""
        user_proxy = create_user_proxy(
            name="CustomManager",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=5,
        )
        
        assert user_proxy.name == "CustomManager"
        assert user_proxy.human_input_mode == "ALWAYS"
        assert user_proxy.max_consecutive_auto_reply == 5
    
    def test_user_proxy_code_execution_config(self):
        """Test user proxy with code execution configuration."""
        code_config = {
            "work_dir": "test_workspace",
            "use_docker": True,
            "timeout": 30,
        }
        
        user_proxy = create_user_proxy(
            code_execution_config=code_config
        )
        
        assert user_proxy.code_execution_config is not None
        assert user_proxy.code_execution_config["work_dir"] == "test_workspace"
    
    def test_user_proxy_termination_message(self):
        """Test user proxy termination message detection."""
        user_proxy = create_user_proxy()
        
        # Test termination detection
        assert user_proxy.is_termination_msg({"content": "TERMINATE"})
        assert user_proxy.is_termination_msg({"content": "Let's terminate this"})
        assert not user_proxy.is_termination_msg({"content": "Continue working"})


class TestGroupChat:
    """Tests for GroupChat creation and configuration."""
    
    def test_create_group_chat(self, mock_feature_service, mock_estimation_service, llm_config):
        """Test creating a group chat with multiple agents."""
        # Create agents
        assistant1 = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
            name="Agent1",
        )
        assistant2 = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
            name="Agent2",
        )
        user_proxy = create_user_proxy()
        
        agents = [assistant1, assistant2, user_proxy]
        
        group_chat, manager = create_group_chat(
            agents=agents,
            max_round=10,
        )
        
        assert group_chat is not None
        assert manager is not None
        assert len(group_chat.agents) == 3
        assert group_chat.max_round == 10
    
    def test_create_group_chat_empty_agents(self):
        """Test that creating group chat with empty agents raises error."""
        with pytest.raises(ValueError, match="At least one agent is required"):
            create_group_chat(agents=[])
    
    def test_group_chat_speaker_selection(self, mock_feature_service, mock_estimation_service, llm_config):
        """Test group chat with different speaker selection methods."""
        assistant = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
        )
        user_proxy = create_user_proxy()
        
        # Test auto selection
        group_chat, _ = create_group_chat(
            agents=[assistant, user_proxy],
            speaker_selection_method="auto",
        )
        assert group_chat.speaker_selection_method == "auto"
        
        # Test round robin
        group_chat, _ = create_group_chat(
            agents=[assistant, user_proxy],
            speaker_selection_method="round_robin",
        )
        assert group_chat.speaker_selection_method == "round_robin"


class TestCodeExecution:
    """Tests for code execution capabilities."""
    
    def test_add_code_execution_tool(self):
        """Test adding code execution tool to user proxy."""
        user_proxy = create_user_proxy(
            code_execution_config={"work_dir": "workspace"}
        )
        
        # Add code execution tool
        add_code_execution_tool(user_proxy)
        
        # Verify configuration was updated
        assert user_proxy.code_execution_config is not None
    
    def test_add_code_execution_with_allowed_operations(self):
        """Test adding code execution with specific allowed operations."""
        user_proxy = create_user_proxy(
            code_execution_config={"work_dir": "workspace"}
        )
        
        allowed_ops = ["math", "statistics"]
        add_code_execution_tool(user_proxy, allowed_operations=allowed_ops)
        
        # Verify allowed operations were set
        assert "allowed_imports" in user_proxy.code_execution_config
        assert user_proxy.code_execution_config["allowed_imports"] == allowed_ops


class TestConversationWorkflows:
    """Tests for conversation workflow functions."""
    
    @patch('src.agents.autogen_agents.AssistantAgent')
    @patch('src.agents.autogen_agents.UserProxyAgent')
    def test_run_estimation_conversation_structure(
        self,
        mock_user_proxy_class,
        mock_assistant_class,
        mock_feature_service,
        mock_estimation_service,
    ):
        """Test the structure of run_estimation_conversation."""
        # Mock the agents
        mock_assistant = MagicMock()
        mock_user_proxy = MagicMock()
        
        mock_assistant_class.return_value = mock_assistant
        mock_user_proxy_class.return_value = mock_user_proxy
        
        # Mock chat messages
        mock_user_proxy.chat_messages = {
            mock_assistant: [
                {"role": "user", "content": "Estimate CRUD"},
                {"role": "assistant", "content": "Total hours: 4.2h"},
            ]
        }
        
        # This would normally run a real conversation, but we're testing structure
        # In a real test, you'd need to mock the entire conversation flow
        # For now, we just verify the function exists and has correct signature
        assert callable(run_estimation_conversation)
    
    @patch('src.agents.autogen_agents.AssistantAgent')
    @patch('src.agents.autogen_agents.UserProxyAgent')
    @patch('src.agents.autogen_agents.GroupChat')
    @patch('src.agents.autogen_agents.GroupChatManager')
    def test_run_group_estimation_structure(
        self,
        mock_manager_class,
        mock_group_chat_class,
        mock_user_proxy_class,
        mock_assistant_class,
        mock_feature_service,
        mock_estimation_service,
    ):
        """Test the structure of run_group_estimation."""
        # This would normally run a real group conversation
        # For now, we just verify the function exists and has correct signature
        assert callable(run_group_estimation)


class TestConversationResult:
    """Tests for ConversationResult dataclass."""
    
    def test_conversation_result_creation(self):
        """Test creating a ConversationResult."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]
        
        result = ConversationResult(
            messages=messages,
            final_estimate=None,
            summary="Test conversation",
            human_inputs=["Hello"],
        )
        
        assert len(result.messages) == 2
        assert result.summary == "Test conversation"
        assert len(result.human_inputs) == 1
        assert result.final_estimate is None


class TestImportError:
    """Tests for handling missing AutoGen installation."""
    
    @patch('src.agents.autogen_agents.AUTOGEN_AVAILABLE', False)
    def test_create_assistant_without_autogen(self, mock_feature_service, mock_estimation_service):
        """Test that creating assistant without AutoGen raises ImportError."""
        with pytest.raises(ImportError, match="AutoGen is not installed"):
            create_estimation_assistant(
                mock_feature_service,
                mock_estimation_service,
            )
    
    @patch('src.agents.autogen_agents.AUTOGEN_AVAILABLE', False)
    def test_create_user_proxy_without_autogen(self):
        """Test that creating user proxy without AutoGen raises ImportError."""
        with pytest.raises(ImportError, match="AutoGen is not installed"):
            create_user_proxy()
    
    @patch('src.agents.autogen_agents.AUTOGEN_AVAILABLE', False)
    def test_create_group_chat_without_autogen(self):
        """Test that creating group chat without AutoGen raises ImportError."""
        with pytest.raises(ImportError, match="AutoGen is not installed"):
            create_group_chat(agents=[Mock()])


# Integration-style tests (would require actual AutoGen installation)
class TestIntegration:
    """Integration tests for AutoGen agents.
    
    These tests verify the actual behavior with AutoGen installed.
    They are more comprehensive but require the library to be available.
    """
    
    @pytest.mark.skipif(not AUTOGEN_AVAILABLE, reason="Requires AutoGen")
    def test_assistant_has_functions(self, mock_feature_service, mock_estimation_service, llm_config):
        """Test that assistant has function calling capabilities."""
        assistant = create_estimation_assistant(
            mock_feature_service,
            mock_estimation_service,
            llm_config,
        )
        
        # Verify functions are registered
        assert hasattr(assistant, 'llm_config')
        assert 'functions' in assistant.llm_config
        
        functions = assistant.llm_config['functions']
        function_names = [f['name'] for f in functions]
        
        assert 'search_features' in function_names
        assert 'estimate_feature' in function_names
        assert 'estimate_project' in function_names
    
    @pytest.mark.skipif(not AUTOGEN_AVAILABLE, reason="Requires AutoGen")
    def test_user_proxy_has_termination_check(self):
        """Test that user proxy has termination message checking."""
        user_proxy = create_user_proxy()
        
        # Test termination detection
        assert callable(user_proxy.is_termination_msg)
        
        # Test with various messages
        assert user_proxy.is_termination_msg({"content": "TERMINATE"})
        assert user_proxy.is_termination_msg({"content": "terminate"})
        assert user_proxy.is_termination_msg({"content": "Let's TERMINATE"})
        assert not user_proxy.is_termination_msg({"content": "Continue"})
        assert not user_proxy.is_termination_msg({"content": ""})
