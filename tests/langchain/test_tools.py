"""Tests for LangChain tools wrapping AITEA services.

This module tests the LangChain tool implementations that wrap
the core AITEA services.
"""

import pytest
from datetime import date

from src.langchain.tools import create_feature_tools
from src.services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)
from src.models import Feature, TrackedTimeEntry, TeamType


@pytest.fixture
def services():
    """Create service instances for testing."""
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    return feature_lib, time_track, estimator


@pytest.fixture
def tools(services):
    """Create tools from services."""
    feature_lib, time_track, estimator = services
    return create_feature_tools(feature_lib, time_track, estimator)


@pytest.fixture
def populated_services(services):
    """Create services with some test data."""
    feature_lib, time_track, estimator = services
    
    # Add some features
    feature_lib.add_feature(Feature(
        id="feat_001",
        name="User Authentication",
        team=TeamType.BACKEND,
        process="Authentication",
        seed_time_hours=8.0,
        synonyms=["auth", "login"],
        notes="JWT-based authentication"
    ))
    
    feature_lib.add_feature(Feature(
        id="feat_002",
        name="Dashboard UI",
        team=TeamType.FRONTEND,
        process="Content Management",
        seed_time_hours=12.0,
        synonyms=["dashboard", "ui"],
        notes="Main dashboard interface"
    ))
    
    # Add some tracked time entries
    time_track.add_entry(TrackedTimeEntry(
        id="entry_001",
        team=TeamType.BACKEND,
        member_name="BE-1",
        feature="User Authentication",
        tracked_time_hours=7.5,
        process="Authentication",
        date=date(2025, 1, 15)
    ))
    
    time_track.add_entry(TrackedTimeEntry(
        id="entry_002",
        team=TeamType.BACKEND,
        member_name="BE-2",
        feature="User Authentication",
        tracked_time_hours=8.5,
        process="Authentication",
        date=date(2025, 1, 16)
    ))
    
    time_track.add_entry(TrackedTimeEntry(
        id="entry_003",
        team=TeamType.BACKEND,
        member_name="BE-1",
        feature="User Authentication",
        tracked_time_hours=9.0,
        process="Authentication",
        date=date(2025, 1, 17)
    ))
    
    return feature_lib, time_track, estimator


class TestToolCreation:
    """Test tool creation and structure."""
    
    def test_create_feature_tools_returns_list(self, tools):
        """Test that create_feature_tools returns a list of tools."""
        assert isinstance(tools, list)
        assert len(tools) == 6
    
    def test_all_tools_have_names(self, tools):
        """Test that all tools have proper names."""
        expected_names = [
            "add_feature",
            "search_features",
            "list_features",
            "estimate_feature",
            "estimate_project",
            "add_time_entry"
        ]
        
        tool_names = [tool.name for tool in tools]
        assert tool_names == expected_names
    
    def test_all_tools_have_descriptions(self, tools):
        """Test that all tools have descriptions."""
        for tool in tools:
            assert tool.description
            assert len(tool.description) > 10


class TestAddFeatureTool:
    """Test the add_feature tool."""
    
    def test_add_feature_success(self, tools, services):
        """Test successfully adding a feature."""
        feature_lib, _, _ = services
        add_feature_tool = tools[0]
        
        result = add_feature_tool.invoke({
            "id": "feat_test",
            "name": "Test Feature",
            "team": "backend",
            "process": "Data Operations",
            "seed_time_hours": 5.0,
            "synonyms": ["test"],
            "notes": "Test notes"
        })
        
        assert "Successfully added feature" in result
        assert "Test Feature" in result
        
        # Verify feature was added
        features = feature_lib.list_features()
        assert len(features) == 1
        assert features[0].name == "Test Feature"
    
    def test_add_feature_invalid_team(self, tools):
        """Test adding a feature with invalid team."""
        add_feature_tool = tools[0]
        
        result = add_feature_tool.invoke({
            "id": "feat_test",
            "name": "Test Feature",
            "team": "invalid_team",
            "process": "Data Operations",
            "seed_time_hours": 5.0
        })
        
        assert "Error" in result
        assert "Invalid team" in result
    
    def test_add_feature_duplicate_id(self, tools, services):
        """Test adding a feature with duplicate ID."""
        feature_lib, _, _ = services
        add_feature_tool = tools[0]
        
        # Add first feature
        add_feature_tool.invoke({
            "id": "feat_dup",
            "name": "Feature 1",
            "team": "backend",
            "process": "Data Operations",
            "seed_time_hours": 5.0
        })
        
        # Try to add duplicate
        result = add_feature_tool.invoke({
            "id": "feat_dup",
            "name": "Feature 2",
            "team": "frontend",
            "process": "Content Management",
            "seed_time_hours": 3.0
        })
        
        assert "Error" in result
        assert "already exists" in result


class TestSearchFeaturesTool:
    """Test the search_features tool."""
    
    def test_search_features_found(self, tools, populated_services):
        """Test searching for features that exist."""
        search_tool = tools[1]
        
        result = search_tool.invoke({"query": "auth"})
        
        assert "Found" in result
        assert "User Authentication" in result
    
    def test_search_features_not_found(self, tools, populated_services):
        """Test searching for features that don't exist."""
        search_tool = tools[1]
        
        result = search_tool.invoke({"query": "nonexistent"})
        
        assert "No features found" in result
    
    def test_search_features_by_synonym(self, tools, populated_services):
        """Test searching by synonym."""
        search_tool = tools[1]
        
        result = search_tool.invoke({"query": "login"})
        
        assert "Found" in result
        assert "User Authentication" in result


class TestListFeaturesTool:
    """Test the list_features tool."""
    
    def test_list_all_features(self, tools, populated_services):
        """Test listing all features."""
        list_tool = tools[2]
        
        result = list_tool.invoke({})
        
        assert "Found 2 feature(s)" in result
        assert "User Authentication" in result
        assert "Dashboard UI" in result
    
    def test_list_features_by_team(self, tools, populated_services):
        """Test listing features filtered by team."""
        list_tool = tools[2]
        
        result = list_tool.invoke({"team": "backend"})
        
        assert "Found 1 feature(s)" in result
        assert "User Authentication" in result
        assert "Dashboard UI" not in result
    
    def test_list_features_invalid_team(self, tools, populated_services):
        """Test listing with invalid team."""
        list_tool = tools[2]
        
        result = list_tool.invoke({"team": "invalid"})
        
        assert "Error" in result
        assert "Invalid team" in result
    
    def test_list_features_empty(self, tools, services):
        """Test listing when no features exist."""
        list_tool = tools[2]
        
        result = list_tool.invoke({})
        
        assert "No features found" in result


class TestEstimateFeatureTool:
    """Test the estimate_feature tool."""
    
    def test_estimate_with_historical_data(self, tools, populated_services):
        """Test estimating a feature with historical data."""
        estimate_tool = tools[3]
        
        result = estimate_tool.invoke({"feature_name": "User Authentication"})
        
        assert "Feature: User Authentication" in result
        assert "Estimated Hours:" in result
        assert "Confidence:" in result
        assert "historical data" in result
        assert "Statistics" in result
    
    def test_estimate_with_seed_time(self, tools, populated_services):
        """Test estimating a feature with only seed time."""
        estimate_tool = tools[3]
        
        result = estimate_tool.invoke({"feature_name": "Dashboard UI"})
        
        assert "Feature: Dashboard UI" in result
        assert "Estimated Hours: 12.0h" in result
        assert "seed time" in result
    
    def test_estimate_feature_not_found(self, tools, populated_services):
        """Test estimating a non-existent feature."""
        estimate_tool = tools[3]
        
        result = estimate_tool.invoke({"feature_name": "Nonexistent Feature"})
        
        assert "Error" in result
        assert "not found" in result


class TestEstimateProjectTool:
    """Test the estimate_project tool."""
    
    def test_estimate_project_success(self, tools, populated_services):
        """Test estimating a project with multiple features."""
        estimate_tool = tools[4]
        
        result = estimate_tool.invoke({
            "features": ["User Authentication", "Dashboard UI"]
        })
        
        assert "Project Estimate" in result
        assert "Total Hours:" in result
        assert "Overall Confidence:" in result
        assert "User Authentication" in result
        assert "Dashboard UI" in result
    
    def test_estimate_project_single_feature(self, tools, populated_services):
        """Test estimating a project with one feature."""
        estimate_tool = tools[4]
        
        result = estimate_tool.invoke({
            "features": ["User Authentication"]
        })
        
        assert "Project Estimate" in result
        assert "User Authentication" in result
    
    def test_estimate_project_feature_not_found(self, tools, populated_services):
        """Test estimating a project with non-existent feature."""
        estimate_tool = tools[4]
        
        result = estimate_tool.invoke({
            "features": ["User Authentication", "Nonexistent"]
        })
        
        assert "Error" in result


class TestAddTimeEntryTool:
    """Test the add_time_entry tool."""
    
    def test_add_time_entry_success(self, tools, services):
        """Test successfully adding a time entry."""
        _, time_track, _ = services
        add_entry_tool = tools[5]
        
        result = add_entry_tool.invoke({
            "id": "entry_test",
            "team": "backend",
            "member_name": "BE-1",
            "feature": "Test Feature",
            "tracked_time_hours": 5.5,
            "process": "Data Operations",
            "date": "2025-01-15"
        })
        
        assert "Successfully added time entry" in result
        assert "BE-1" in result
        assert "5.5h" in result
    
    def test_add_time_entry_invalid_team(self, tools):
        """Test adding time entry with invalid team."""
        add_entry_tool = tools[5]
        
        result = add_entry_tool.invoke({
            "id": "entry_test",
            "team": "invalid",
            "member_name": "BE-1",
            "feature": "Test Feature",
            "tracked_time_hours": 5.5,
            "process": "Data Operations",
            "date": "2025-01-15"
        })
        
        assert "Error" in result
        assert "Invalid team" in result
    
    def test_add_time_entry_invalid_date(self, tools):
        """Test adding time entry with invalid date format."""
        add_entry_tool = tools[5]
        
        result = add_entry_tool.invoke({
            "id": "entry_test",
            "team": "backend",
            "member_name": "BE-1",
            "feature": "Test Feature",
            "tracked_time_hours": 5.5,
            "process": "Data Operations",
            "date": "15-01-2025"  # Wrong format
        })
        
        assert "Error" in result
        assert "Invalid date format" in result
    
    def test_add_time_entry_duplicate_id(self, tools, services):
        """Test adding time entry with duplicate ID."""
        add_entry_tool = tools[5]
        
        # Add first entry
        add_entry_tool.invoke({
            "id": "entry_dup",
            "team": "backend",
            "member_name": "BE-1",
            "feature": "Test Feature",
            "tracked_time_hours": 5.5,
            "process": "Data Operations",
            "date": "2025-01-15"
        })
        
        # Try to add duplicate
        result = add_entry_tool.invoke({
            "id": "entry_dup",
            "team": "backend",
            "member_name": "BE-2",
            "feature": "Test Feature",
            "tracked_time_hours": 6.0,
            "process": "Data Operations",
            "date": "2025-01-16"
        })
        
        assert "Error" in result
        assert "already exists" in result


class TestToolIntegration:
    """Test integration between multiple tools."""
    
    def test_add_feature_then_estimate(self, tools, services):
        """Test adding a feature and then estimating it."""
        add_feature_tool = tools[0]
        estimate_tool = tools[3]
        
        # Add feature
        add_result = add_feature_tool.invoke({
            "id": "feat_int",
            "name": "Integration Test",
            "team": "backend",
            "process": "Data Operations",
            "seed_time_hours": 10.0
        })
        assert "Successfully added" in add_result
        
        # Estimate it
        estimate_result = estimate_tool.invoke({
            "feature_name": "Integration Test"
        })
        assert "Integration Test" in estimate_result
        assert "10.0h" in estimate_result
        assert "seed time" in estimate_result
    
    def test_add_time_entries_improve_estimate(self, tools, services):
        """Test that adding time entries improves estimate confidence."""
        add_feature_tool = tools[0]
        add_entry_tool = tools[5]
        estimate_tool = tools[3]
        
        # Add feature
        add_feature_tool.invoke({
            "id": "feat_conf",
            "name": "Confidence Test",
            "team": "backend",
            "process": "Data Operations",
            "seed_time_hours": 10.0
        })
        
        # Initial estimate (should use seed time, low confidence)
        result1 = estimate_tool.invoke({"feature_name": "Confidence Test"})
        assert "low" in result1.lower()
        assert "seed time" in result1
        
        # Add 3 time entries
        for i in range(3):
            add_entry_tool.invoke({
                "id": f"entry_conf_{i}",
                "team": "backend",
                "member_name": f"BE-{i+1}",
                "feature": "Confidence Test",
                "tracked_time_hours": 9.0 + i,
                "process": "Data Operations",
                "date": f"2025-01-{15+i:02d}"
            })
        
        # New estimate (should use historical data, medium confidence)
        result2 = estimate_tool.invoke({"feature_name": "Confidence Test"})
        assert "medium" in result2.lower()
        assert "historical data" in result2
        assert "Statistics" in result2
