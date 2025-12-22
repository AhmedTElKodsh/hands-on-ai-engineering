"""LangChain tools wrapping aitea-core services.

This module provides LangChain tool implementations that wrap the core
AITEA services (FeatureLibraryService, TimeTrackingService, EstimationService)
for use in LangChain agents and chains.

Tools are created using both the @tool decorator for simple functions and
StructuredTool for more complex operations with detailed schemas.
"""

from typing import List, Optional, Dict, Any
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

from ..services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)
from ..models import Feature, TrackedTimeEntry, TeamType


# ============================================================================
# Tool Input Schemas (Pydantic Models)
# ============================================================================

class AddFeatureInput(BaseModel):
    """Input schema for adding a feature to the library."""
    id: str = Field(description="Unique identifier for the feature")
    name: str = Field(description="Name of the feature")
    team: str = Field(description="Team responsible (backend, frontend, fullstack, design, qa, devops)")
    process: str = Field(description="Process type (Data Operations, Content Management, Real-time, Authentication, Integration)")
    seed_time_hours: float = Field(description="Initial time estimate in hours", gt=0)
    synonyms: List[str] = Field(default_factory=list, description="Alternative names for the feature")
    notes: str = Field(default="", description="Additional notes or context")


class SearchFeaturesInput(BaseModel):
    """Input schema for searching features."""
    query: str = Field(description="Search query to match against feature names and synonyms")


class ListFeaturesInput(BaseModel):
    """Input schema for listing features."""
    team: Optional[str] = Field(default=None, description="Optional team filter (backend, frontend, fullstack, design, qa, devops)")


class EstimateFeatureInput(BaseModel):
    """Input schema for estimating a single feature."""
    feature_name: str = Field(description="Name of the feature to estimate")


class EstimateProjectInput(BaseModel):
    """Input schema for estimating a project."""
    features: List[str] = Field(description="List of feature names to include in the project estimate")


class AddTimeEntryInput(BaseModel):
    """Input schema for adding a tracked time entry."""
    id: str = Field(description="Unique identifier for the entry")
    team: str = Field(description="Team that worked on the feature")
    member_name: str = Field(description="Name of the team member")
    feature: str = Field(description="Name of the feature worked on")
    tracked_time_hours: float = Field(description="Actual time spent in hours", gt=0)
    process: str = Field(description="Process type")
    date: str = Field(description="Date of work in YYYY-MM-DD format")


# ============================================================================
# Service-Backed Tool Functions (using @tool decorator)
# ============================================================================

def create_feature_tools(
    feature_library: FeatureLibraryService,
    time_tracking: TimeTrackingService,
    estimation: EstimationService
) -> List[StructuredTool]:
    """Create LangChain tools for AITEA services.
    
    This function creates a suite of tools that wrap the core AITEA services,
    making them available for use in LangChain agents and chains.
    
    Args:
        feature_library: The feature library service instance
        time_tracking: The time tracking service instance
        estimation: The estimation service instance
        
    Returns:
        List of StructuredTool instances ready for use in agents
        
    Example:
        >>> feature_lib = FeatureLibraryService()
        >>> time_track = TimeTrackingService()
        >>> estimator = EstimationService(feature_lib, time_track)
        >>> tools = create_feature_tools(feature_lib, time_track, estimator)
        >>> agent = create_react_agent(llm, tools)
    """
    
    # Tool 1: Add Feature
    def add_feature_func(
        id: str,
        name: str,
        team: str,
        process: str,
        seed_time_hours: float,
        synonyms: List[str] = None,
        notes: str = ""
    ) -> str:
        """Add a new feature to the feature library.
        
        Use this tool when you need to register a new software feature
        with its initial time estimate and metadata.
        """
        if synonyms is None:
            synonyms = []
            
        try:
            team_enum = TeamType(team.lower())
        except ValueError:
            return f"Error: Invalid team '{team}'. Must be one of: backend, frontend, fullstack, design, qa, devops"
        
        feature = Feature(
            id=id,
            name=name,
            team=team_enum,
            process=process,
            seed_time_hours=seed_time_hours,
            synonyms=synonyms,
            notes=notes
        )
        
        result = feature_library.add_feature(feature)
        if result.is_ok():
            return f"Successfully added feature '{name}' with ID '{id}'"
        else:
            error = result.unwrap_err()
            return f"Error adding feature: {error.message}"
    
    add_feature_tool = StructuredTool.from_function(
        func=add_feature_func,
        name="add_feature",
        description="Add a new feature to the feature library with seed time estimate",
        args_schema=AddFeatureInput
    )
    
    # Tool 2: Search Features
    def search_features_func(query: str) -> str:
        """Search for features in the library by name or synonym.
        
        Use this tool to find existing features that match a search query.
        """
        features = feature_library.search_features(query)
        
        if not features:
            return f"No features found matching '{query}'"
        
        results = [f"- {f.name} ({f.team.value}, {f.seed_time_hours}h)" for f in features]
        return f"Found {len(features)} feature(s):\n" + "\n".join(results)
    
    search_features_tool = StructuredTool.from_function(
        func=search_features_func,
        name="search_features",
        description="Search for features by name or synonym",
        args_schema=SearchFeaturesInput
    )
    
    # Tool 3: List Features
    def list_features_func(team: Optional[str] = None) -> str:
        """List all features, optionally filtered by team.
        
        Use this tool to see all available features in the library.
        """
        team_enum = None
        if team:
            try:
                team_enum = TeamType(team.lower())
            except ValueError:
                return f"Error: Invalid team '{team}'. Must be one of: backend, frontend, fullstack, design, qa, devops"
        
        features = feature_library.list_features(team_enum)
        
        if not features:
            team_str = f" for team '{team}'" if team else ""
            return f"No features found{team_str}"
        
        results = [f"- {f.name} ({f.team.value}, {f.seed_time_hours}h)" for f in features]
        return f"Found {len(features)} feature(s):\n" + "\n".join(results)
    
    list_features_tool = StructuredTool.from_function(
        func=list_features_func,
        name="list_features",
        description="List all features in the library, optionally filtered by team",
        args_schema=ListFeaturesInput
    )
    
    # Tool 4: Estimate Feature
    def estimate_feature_func(feature_name: str) -> str:
        """Estimate time for a single feature based on historical data.
        
        Use this tool to get a time estimate for a specific feature.
        The estimate uses historical tracked time data when available,
        otherwise falls back to the seed time estimate.
        """
        result = estimation.estimate_feature(feature_name)
        
        if result.is_err():
            error = result.unwrap_err()
            return f"Error estimating feature: {error.reason}"
        
        estimate = result.unwrap()
        source = "historical data" if not estimate.used_seed_time else "seed time"
        
        output = f"Feature: {estimate.feature_name}\n"
        output += f"Estimated Hours: {estimate.estimated_hours:.1f}h\n"
        output += f"Confidence: {estimate.confidence.value}\n"
        output += f"Source: {source}\n"
        
        if estimate.statistics:
            stats = estimate.statistics
            output += f"\nStatistics (from {stats.data_point_count} data points):\n"
            output += f"  Mean: {stats.mean:.1f}h\n"
            output += f"  Median: {stats.median:.1f}h\n"
            output += f"  P80: {stats.p80:.1f}h\n"
            output += f"  Std Dev: {stats.std_dev:.1f}h\n"
        
        return output
    
    estimate_feature_tool = StructuredTool.from_function(
        func=estimate_feature_func,
        name="estimate_feature",
        description="Estimate time for a single feature using historical data or seed time",
        args_schema=EstimateFeatureInput
    )
    
    # Tool 5: Estimate Project
    def estimate_project_func(features: List[str]) -> str:
        """Estimate total time for a project with multiple features.
        
        Use this tool to get a comprehensive project estimate that
        aggregates estimates for multiple features.
        """
        result = estimation.estimate_project(features)
        
        if result.is_err():
            error = result.unwrap_err()
            return f"Error estimating project: {error.reason}"
        
        project = result.unwrap()
        
        output = f"Project Estimate\n"
        output += f"================\n"
        output += f"Total Hours: {project.total_hours:.1f}h\n"
        output += f"Overall Confidence: {project.confidence.value}\n\n"
        output += f"Feature Breakdown:\n"
        
        for fe in project.features:
            source = "data" if not fe.used_seed_time else "seed"
            output += f"  - {fe.feature_name}: {fe.estimated_hours:.1f}h ({fe.confidence.value}, {source})\n"
        
        return output
    
    estimate_project_tool = StructuredTool.from_function(
        func=estimate_project_func,
        name="estimate_project",
        description="Estimate total time for a project consisting of multiple features",
        args_schema=EstimateProjectInput
    )
    
    # Tool 6: Add Time Entry
    def add_time_entry_func(
        id: str,
        team: str,
        member_name: str,
        feature: str,
        tracked_time_hours: float,
        process: str,
        date: str
    ) -> str:
        """Add a tracked time entry for a feature.
        
        Use this tool to record actual time spent on a feature,
        which improves future estimates.
        """
        from datetime import datetime
        
        try:
            team_enum = TeamType(team.lower())
        except ValueError:
            return f"Error: Invalid team '{team}'. Must be one of: backend, frontend, fullstack, design, qa, devops"
        
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return f"Error: Invalid date format '{date}'. Use YYYY-MM-DD format"
        
        entry = TrackedTimeEntry(
            id=id,
            team=team_enum,
            member_name=member_name,
            feature=feature,
            tracked_time_hours=tracked_time_hours,
            process=process,
            date=date_obj
        )
        
        result = time_tracking.add_entry(entry)
        if result.is_ok():
            return f"Successfully added time entry: {member_name} spent {tracked_time_hours}h on '{feature}'"
        else:
            error = result.unwrap_err()
            return f"Error adding time entry: {error.message}"
    
    add_time_entry_tool = StructuredTool.from_function(
        func=add_time_entry_func,
        name="add_time_entry",
        description="Add a tracked time entry to record actual time spent on a feature",
        args_schema=AddTimeEntryInput
    )
    
    # Return all tools
    return [
        add_feature_tool,
        search_features_tool,
        list_features_tool,
        estimate_feature_tool,
        estimate_project_tool,
        add_time_entry_tool,
    ]


# ============================================================================
# Simple @tool decorator examples
# ============================================================================

@tool
def get_feature_info(feature_name: str) -> str:
    """Get detailed information about a specific feature.
    
    This is a simple tool example using the @tool decorator.
    For production use, prefer the service-backed tools above.
    
    Args:
        feature_name: Name of the feature to look up
        
    Returns:
        Feature information as a formatted string
    """
    # This is a simplified example - in practice, you'd inject the service
    return f"Feature '{feature_name}' - Use search_features tool for actual data"


@tool
def calculate_team_velocity(team: str, weeks: int = 4) -> str:
    """Calculate average velocity for a team over recent weeks.
    
    This tool would analyze tracked time entries to compute team velocity.
    
    Args:
        team: Team name (backend, frontend, etc.)
        weeks: Number of recent weeks to analyze (default: 4)
        
    Returns:
        Team velocity metrics as a formatted string
    """
    return f"Team '{team}' velocity over {weeks} weeks - Use time tracking service for actual data"


# ============================================================================
# Tool Usage Examples
# ============================================================================

def example_tool_usage():
    """Example demonstrating how to use the AITEA tools with LangChain agents.
    
    This function shows the complete workflow of:
    1. Creating service instances
    2. Creating tools from services
    3. Using tools in an agent
    """
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_react_agent, AgentExecutor
    from langchain_core.prompts import PromptTemplate
    
    # Step 1: Create service instances
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    
    # Step 2: Create tools
    tools = create_feature_tools(feature_lib, time_track, estimator)
    
    # Step 3: Create agent with tools
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

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
Thought: {agent_scratchpad}""")
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Step 4: Use the agent
    result = agent_executor.invoke({
        "input": "Add a new feature called 'User Authentication' for the backend team with 8 hours seed time"
    })
    
    print(result["output"])


if __name__ == "__main__":
    # Run example if this module is executed directly
    print("AITEA LangChain Tools")
    print("=" * 50)
    print("\nThis module provides LangChain tools for AITEA services.")
    print("\nAvailable tools:")
    print("  - add_feature: Add a new feature to the library")
    print("  - search_features: Search for features by name")
    print("  - list_features: List all features")
    print("  - estimate_feature: Estimate time for a feature")
    print("  - estimate_project: Estimate time for a project")
    print("  - add_time_entry: Record actual time spent")
    print("\nSee example_tool_usage() for usage examples.")
