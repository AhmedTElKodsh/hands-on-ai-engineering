"""CrewAI multi-agent system for AITEA estimation workflow.

This module implements a multi-agent system using CrewAI framework with three
specialized agents working collaboratively:
- Analyst: Extracts and clarifies features from BRD documents
- Estimator: Provides time estimates based on historical data
- Reviewer: Validates estimates and identifies risks

The agents work in a sequential process to analyze requirements, estimate time,
and review the estimates for accuracy and completeness.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Define placeholder classes for type hints when CrewAI is not installed
    Agent = Any
    Task = Any
    Crew = Any
    Process = Any
    BaseTool = Any

from ..services import (
    IFeatureLibraryService,
    IEstimationService,
    get_llm_provider,
)
from ..models import Feature, ProjectEstimate


@dataclass
class EstimationResult:
    """Result of the multi-agent estimation process.
    
    Attributes:
        features_extracted: List of features identified from the BRD
        estimates: Project estimate with feature breakdown
        review_notes: Reviewer's notes on the estimates
        risks_identified: List of identified risks
        confidence_assessment: Overall confidence in the estimates
    """
    features_extracted: List[str]
    estimates: Optional[ProjectEstimate]
    review_notes: str
    risks_identified: List[str]
    confidence_assessment: str


class FeatureSearchTool(BaseTool if CREWAI_AVAILABLE else object):
    """Tool for searching the feature library."""
    
    name: str = "search_features"
    description: str = (
        "Search the feature library for matching features. "
        "Use this to find similar features and their historical data."
    )
    
    def __init__(self, feature_service: IFeatureLibraryService):
        """Initialize the tool with a feature library service.
        
        Args:
            feature_service: Service for accessing the feature library
        """
        if CREWAI_AVAILABLE:
            super().__init__()
        self.feature_service = feature_service
    
    def _run(self, query: str) -> str:
        """Execute the feature search.
        
        Args:
            query: Search query string
            
        Returns:
            Formatted string with search results
        """
        features = self.feature_service.search_features(query)
        if not features:
            return f"No features found matching '{query}'"
        
        result = f"Found {len(features)} matching features:\n"
        for feature in features:
            result += f"- {feature.name} ({feature.team.value}): {feature.seed_time_hours}h seed time\n"
        return result


class EstimationTool(BaseTool if CREWAI_AVAILABLE else object):
    """Tool for estimating feature time."""
    
    name: str = "estimate_feature"
    description: str = (
        "Estimate time for a specific feature based on historical data. "
        "Returns mean, median, P80, and confidence level."
    )
    
    def __init__(self, estimation_service: IEstimationService):
        """Initialize the tool with an estimation service.
        
        Args:
            estimation_service: Service for computing estimates
        """
        if CREWAI_AVAILABLE:
            super().__init__()
        self.estimation_service = estimation_service
    
    def _run(self, feature_name: str) -> str:
        """Execute the feature estimation.
        
        Args:
            feature_name: Name of the feature to estimate
            
        Returns:
            Formatted string with estimation results
        """
        result = self.estimation_service.estimate_feature(feature_name)
        if result.is_err():
            return f"Error estimating '{feature_name}': {result.unwrap_err()}"
        
        estimate = result.unwrap()
        output = f"Estimate for '{feature_name}':\n"
        output += f"- Hours: {estimate.estimated_hours}h\n"
        output += f"- Confidence: {estimate.confidence.value}\n"
        
        if estimate.statistics:
            stats = estimate.statistics
            output += f"- Mean: {stats.mean:.1f}h\n"
            output += f"- Median: {stats.median:.1f}h\n"
            output += f"- P80: {stats.p80:.1f}h\n"
            output += f"- Data points: {stats.data_point_count}\n"
        
        return output


class ValidationTool(BaseTool if CREWAI_AVAILABLE else object):
    """Tool for validating estimates against historical data."""
    
    name: str = "validate_estimate"
    description: str = (
        "Validate an estimate by comparing it to historical data and "
        "identifying potential risks or outliers."
    )
    
    def __init__(self, estimation_service: IEstimationService):
        """Initialize the tool with an estimation service.
        
        Args:
            estimation_service: Service for computing estimates
        """
        if CREWAI_AVAILABLE:
            super().__init__()
        self.estimation_service = estimation_service
    
    def _run(self, feature_name: str, proposed_hours: float) -> str:
        """Validate a proposed estimate.
        
        Args:
            feature_name: Name of the feature
            proposed_hours: Proposed time estimate in hours
            
        Returns:
            Formatted string with validation results
        """
        result = self.estimation_service.estimate_feature(feature_name)
        if result.is_err():
            return f"Cannot validate - no historical data for '{feature_name}'"
        
        estimate = result.unwrap()
        
        if not estimate.statistics:
            return f"Limited data for '{feature_name}' - validation inconclusive"
        
        stats = estimate.statistics
        deviation = abs(proposed_hours - stats.mean) / stats.std_dev if stats.std_dev > 0 else 0
        
        output = f"Validation for '{feature_name}' ({proposed_hours}h):\n"
        output += f"- Historical mean: {stats.mean:.1f}h\n"
        output += f"- Deviation: {deviation:.1f} standard deviations\n"
        
        if deviation > 2:
            output += "⚠️ WARNING: Estimate is >2 std devs from historical mean\n"
        elif deviation > 1:
            output += "⚠️ CAUTION: Estimate is >1 std dev from historical mean\n"
        else:
            output += "✓ Estimate is within normal range\n"
        
        return output


def create_analyst_agent(
    feature_service: IFeatureLibraryService,
    llm_config: Optional[Dict[str, Any]] = None
) -> Agent:
    """Create the Analyst agent for BRD feature extraction.
    
    The Analyst agent is responsible for:
    - Reading and understanding BRD documents
    - Extracting feature lists
    - Clarifying ambiguous requirements
    - Searching for similar features in the library
    
    Args:
        feature_service: Service for accessing the feature library
        llm_config: Optional LLM configuration
        
    Returns:
        Configured Analyst agent
        
    Raises:
        ImportError: If CrewAI is not installed
    """
    if not CREWAI_AVAILABLE:
        raise ImportError(
            "CrewAI is not installed. Install it with: pip install crewai"
        )
    
    search_tool = FeatureSearchTool(feature_service)
    
    return Agent(
        role="Requirements Analyst",
        goal="Extract and clarify features from BRD documents with precision",
        backstory=(
            "You are an expert business analyst with 10+ years of experience "
            "in software requirements analysis. You excel at reading technical "
            "documents, identifying features, and breaking down complex requirements "
            "into clear, estimable work items. You always search for similar "
            "features in the historical library to ensure consistency."
        ),
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
        llm_config=llm_config or {},
    )


def create_estimator_agent(
    estimation_service: IEstimationService,
    llm_config: Optional[Dict[str, Any]] = None
) -> Agent:
    """Create the Estimator agent for time estimation.
    
    The Estimator agent is responsible for:
    - Analyzing feature complexity
    - Retrieving historical data
    - Computing statistical estimates
    - Providing confidence levels
    
    Args:
        estimation_service: Service for computing estimates
        llm_config: Optional LLM configuration
        
    Returns:
        Configured Estimator agent
        
    Raises:
        ImportError: If CrewAI is not installed
    """
    if not CREWAI_AVAILABLE:
        raise ImportError(
            "CrewAI is not installed. Install it with: pip install crewai"
        )
    
    estimation_tool = EstimationTool(estimation_service)
    
    return Agent(
        role="Estimation Specialist",
        goal="Provide accurate time estimates based on historical data and feature complexity",
        backstory=(
            "You are a senior software engineer with extensive experience in "
            "project estimation. You understand that good estimates come from "
            "historical data, not guesswork. You always use statistical methods "
            "(mean, median, P80) and clearly communicate confidence levels. "
            "You know that low-confidence estimates need more investigation."
        ),
        tools=[estimation_tool],
        verbose=True,
        allow_delegation=False,
        llm_config=llm_config or {},
    )


def create_reviewer_agent(
    estimation_service: IEstimationService,
    llm_config: Optional[Dict[str, Any]] = None
) -> Agent:
    """Create the Reviewer agent for estimate validation.
    
    The Reviewer agent is responsible for:
    - Validating estimates against historical data
    - Identifying risks and outliers
    - Checking for missing features
    - Providing overall confidence assessment
    
    Args:
        estimation_service: Service for computing estimates
        llm_config: Optional LLM configuration
        
    Returns:
        Configured Reviewer agent
        
    Raises:
        ImportError: If CrewAI is not installed
    """
    if not CREWAI_AVAILABLE:
        raise ImportError(
            "CrewAI is not installed. Install it with: pip install crewai"
        )
    
    validation_tool = ValidationTool(estimation_service)
    
    return Agent(
        role="Estimate Reviewer",
        goal="Validate estimates and identify risks to ensure realistic project planning",
        backstory=(
            "You are an experienced project manager who has seen many projects "
            "fail due to poor estimation. You are skeptical by nature and always "
            "look for red flags: estimates that deviate significantly from "
            "historical data, missing features, or overly optimistic timelines. "
            "You provide constructive feedback to improve estimate accuracy."
        ),
        tools=[validation_tool],
        verbose=True,
        allow_delegation=False,
        llm_config=llm_config or {},
    )


def create_estimation_crew(
    feature_service: IFeatureLibraryService,
    estimation_service: IEstimationService,
    process_type: str = "sequential",
    llm_config: Optional[Dict[str, Any]] = None
) -> Crew:
    """Create a Crew for the estimation workflow.
    
    The crew consists of three agents working together:
    1. Analyst extracts features from BRD
    2. Estimator provides time estimates
    3. Reviewer validates and identifies risks
    
    Args:
        feature_service: Service for accessing the feature library
        estimation_service: Service for computing estimates
        process_type: Either "sequential" or "hierarchical"
        llm_config: Optional LLM configuration
        
    Returns:
        Configured Crew ready to execute
        
    Raises:
        ImportError: If CrewAI is not installed
        ValueError: If process_type is invalid
    """
    if not CREWAI_AVAILABLE:
        raise ImportError(
            "CrewAI is not installed. Install it with: pip install crewai"
        )
    
    if process_type not in ["sequential", "hierarchical"]:
        raise ValueError(
            f"Invalid process_type: {process_type}. "
            "Must be 'sequential' or 'hierarchical'"
        )
    
    # Create agents
    analyst = create_analyst_agent(feature_service, llm_config)
    estimator = create_estimator_agent(estimation_service, llm_config)
    reviewer = create_reviewer_agent(estimation_service, llm_config)
    
    # Define tasks
    analyze_task = Task(
        description=(
            "Analyze the provided BRD document and extract a comprehensive list "
            "of features. For each feature, search the feature library to find "
            "similar historical features. Provide a clear, structured list of "
            "features with any clarifications needed."
        ),
        agent=analyst,
        expected_output=(
            "A structured list of features extracted from the BRD, with notes "
            "on similar historical features found in the library."
        ),
    )
    
    estimate_task = Task(
        description=(
            "For each feature identified by the Analyst, provide a time estimate "
            "using historical data. Use the estimation tool to get statistical "
            "estimates (mean, median, P80) and confidence levels. Aggregate the "
            "estimates into a total project estimate."
        ),
        agent=estimator,
        expected_output=(
            "A detailed project estimate with individual feature estimates, "
            "total hours, and confidence levels for each estimate."
        ),
    )
    
    review_task = Task(
        description=(
            "Review the estimates provided by the Estimator. Validate each "
            "estimate against historical data using the validation tool. "
            "Identify any estimates that deviate significantly from historical "
            "norms. Flag potential risks, missing features, or areas needing "
            "more investigation. Provide an overall confidence assessment."
        ),
        agent=reviewer,
        expected_output=(
            "A review report with validation results, identified risks, "
            "recommendations for improvement, and overall confidence assessment."
        ),
    )
    
    # Create crew
    process = Process.sequential if process_type == "sequential" else Process.hierarchical
    
    return Crew(
        agents=[analyst, estimator, reviewer],
        tasks=[analyze_task, estimate_task, review_task],
        process=process,
        verbose=True,
    )


def run_estimation_workflow(
    brd_content: str,
    feature_service: IFeatureLibraryService,
    estimation_service: IEstimationService,
    process_type: str = "sequential",
    llm_config: Optional[Dict[str, Any]] = None
) -> str:
    """Run the complete estimation workflow on a BRD document.
    
    This is a convenience function that creates the crew and executes
    the workflow in one call.
    
    Args:
        brd_content: Content of the BRD document to analyze
        feature_service: Service for accessing the feature library
        estimation_service: Service for computing estimates
        process_type: Either "sequential" or "hierarchical"
        llm_config: Optional LLM configuration
        
    Returns:
        Final output from the crew execution
        
    Raises:
        ImportError: If CrewAI is not installed
    """
    crew = create_estimation_crew(
        feature_service,
        estimation_service,
        process_type,
        llm_config
    )
    
    # Execute the crew with the BRD content as input
    result = crew.kickoff(inputs={"brd_content": brd_content})
    
    return result


# Example usage and testing utilities
def get_mock_llm_config() -> Dict[str, Any]:
    """Get LLM configuration for testing with MockLLM.
    
    Returns:
        Configuration dictionary for MockLLM
    """
    return {
        "model": "mock",
        "temperature": 0.7,
    }


def example_usage():
    """Example of how to use the CrewAI multi-agent system.
    
    This function demonstrates the typical workflow for using the
    estimation crew with AITEA services.
    """
    if not CREWAI_AVAILABLE:
        print("CrewAI is not installed. Install it with: pip install crewai")
        return
    
    # This is just an example - in real usage, you would import actual services
    print("Example: Creating estimation crew")
    print("=" * 60)
    print()
    print("1. Initialize AITEA services:")
    print("   feature_service = FeatureLibraryService()")
    print("   estimation_service = EstimationService(...)")
    print()
    print("2. Create the crew:")
    print("   crew = create_estimation_crew(")
    print("       feature_service,")
    print("       estimation_service,")
    print("       process_type='sequential'")
    print("   )")
    print()
    print("3. Run the workflow:")
    print("   result = crew.kickoff(inputs={'brd_content': brd_text})")
    print()
    print("The crew will:")
    print("  - Analyst: Extract features from BRD")
    print("  - Estimator: Provide time estimates")
    print("  - Reviewer: Validate and identify risks")
    print()


if __name__ == "__main__":
    example_usage()
