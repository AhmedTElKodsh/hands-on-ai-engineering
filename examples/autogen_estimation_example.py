"""Example: Using AutoGen Conversational Agents for Estimation

This example demonstrates how to use Microsoft's AutoGen framework
with AITEA for conversational, interactive estimation workflows.

AutoGen enables:
- Natural back-and-forth conversations
- Human-in-the-loop decision making
- Code execution for calculations
- Multi-agent collaboration

Run this example:
    python examples/autogen_estimation_example.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import (
    AUTOGEN_AVAILABLE,
    create_estimation_assistant,
    create_user_proxy,
    create_group_chat,
)
from src.services import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)
from src.models import Feature, TeamType, TrackedTimeEntry, EstimationConfig
from datetime import date


def setup_services():
    """Set up AITEA services with sample data."""
    # Initialize services
    feature_service = FeatureLibraryService()
    time_service = TimeTrackingService()
    estimation_service = EstimationService(
        feature_service=feature_service,
        time_service=time_service,
        config=EstimationConfig(),
    )
    
    # Add sample features
    features = [
        Feature(
            id="feat_001",
            name="CRUD",
            team=TeamType.BACKEND,
            process="Data Operations",
            seed_time_hours=4.0,
            synonyms=["crud-api", "rest-crud"],
            notes="Basic CRUD operations for REST API"
        ),
        Feature(
            id="feat_002",
            name="Authentication",
            team=TeamType.BACKEND,
            process="Authentication",
            seed_time_hours=6.0,
            synonyms=["auth", "login", "user-auth"],
            notes="User authentication with JWT"
        ),
        Feature(
            id="feat_003",
            name="Search",
            team=TeamType.BACKEND,
            process="Data Operations",
            seed_time_hours=8.0,
            synonyms=["search-api", "full-text-search"],
            notes="Full-text search functionality"
        ),
    ]
    
    for feature in features:
        feature_service.add_feature(feature)
    
    # Add sample tracked time entries
    entries = [
        # CRUD entries
        TrackedTimeEntry(
            id="track_001",
            team=TeamType.BACKEND,
            member_name="BE-1",
            feature="CRUD",
            tracked_time_hours=4.5,
            process="Data Operations",
            date=date(2025, 1, 15)
        ),
        TrackedTimeEntry(
            id="track_002",
            team=TeamType.BACKEND,
            member_name="BE-2",
            feature="CRUD",
            tracked_time_hours=3.8,
            process="Data Operations",
            date=date(2025, 1, 16)
        ),
        TrackedTimeEntry(
            id="track_003",
            team=TeamType.BACKEND,
            member_name="BE-3",
            feature="CRUD",
            tracked_time_hours=4.2,
            process="Data Operations",
            date=date(2025, 1, 17)
        ),
        # Authentication entries
        TrackedTimeEntry(
            id="track_004",
            team=TeamType.BACKEND,
            member_name="BE-1",
            feature="Authentication",
            tracked_time_hours=6.5,
            process="Authentication",
            date=date(2025, 1, 18)
        ),
        TrackedTimeEntry(
            id="track_005",
            team=TeamType.BACKEND,
            member_name="BE-2",
            feature="Authentication",
            tracked_time_hours=7.0,
            process="Authentication",
            date=date(2025, 1, 19)
        ),
    ]
    
    for entry in entries:
        time_service.add_entry(entry)
    
    return feature_service, estimation_service


def example_simple_conversation():
    """Example 1: Simple two-agent conversation."""
    print("\n" + "=" * 70)
    print("Example 1: Simple Conversation with Assistant")
    print("=" * 70)
    
    if not AUTOGEN_AVAILABLE:
        print("\n⚠️  AutoGen is not installed.")
        print("Install it with: pip install pyautogen")
        print("\nThis example demonstrates what the conversation would look like:")
        print("\nUser: 'I need to estimate a CRUD feature for a backend API'")
        print("\nAssistant: [Searches feature library]")
        print("'I found 3 similar CRUD features in the library.")
        print(" Based on historical data:")
        print(" - Mean: 4.2 hours")
        print(" - Median: 4.2 hours")
        print(" - P80: 4.5 hours")
        print(" - Confidence: HIGH (3 data points)")
        print("\n I recommend estimating 4.5 hours (P80) for this feature.'")
        print("\nUser: 'That sounds reasonable. TERMINATE'")
        return
    
    # Set up services
    feature_service, estimation_service = setup_services()
    
    # Create agents
    llm_config = {
        "model": "gpt-4",
        "temperature": 0.7,
    }
    
    assistant = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
    )
    
    user_proxy = create_user_proxy(
        human_input_mode="TERMINATE",
    )
    
    print("\nStarting conversation...")
    print("(In a real scenario, this would be an interactive conversation)")
    print("\nInitial message: 'I need to estimate a CRUD feature for a backend API'")
    
    # In a real scenario, you would call:
    # user_proxy.initiate_chat(assistant, message="I need to estimate a CRUD feature")
    
    print("\nConversation flow:")
    print("1. User asks for estimate")
    print("2. Assistant searches feature library")
    print("3. Assistant computes statistics from historical data")
    print("4. Assistant provides estimate with confidence level")
    print("5. User reviews and terminates")


def example_group_chat():
    """Example 2: Group chat with multiple specialized agents."""
    print("\n" + "=" * 70)
    print("Example 2: Group Chat with Multiple Agents")
    print("=" * 70)
    
    if not AUTOGEN_AVAILABLE:
        print("\n⚠️  AutoGen is not installed.")
        print("Install it with: pip install pyautogen")
        print("\nThis example demonstrates a multi-agent conversation:")
        print("\nUser: 'Estimate features: CRUD, Authentication, Search'")
        print("\nAnalyst: [Searches library]")
        print("'Found historical data for all three features.")
        print(" CRUD: 3 data points")
        print(" Authentication: 2 data points")
        print(" Search: 0 data points (will use seed time)'")
        print("\nEstimator: [Computes estimates]")
        print("'Based on the data:")
        print(" - CRUD: 4.2h (high confidence)")
        print(" - Authentication: 6.8h (low confidence)")
        print(" - Search: 8.0h (seed time, low confidence)")
        print(" Total: 19.0 hours'")
        print("\nReviewer: [Validates estimates]")
        print("'CRUD estimate looks good.")
        print(" Authentication has limited data - recommend gathering more.")
        print(" Search has no historical data - high risk.")
        print(" Overall confidence: MEDIUM'")
        print("\nUser: 'Thanks for the analysis. TERMINATE'")
        return
    
    # Set up services
    feature_service, estimation_service = setup_services()
    
    # Create specialized agents
    llm_config = {
        "model": "gpt-4",
        "temperature": 0.7,
    }
    
    analyst = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Analyst",
    )
    
    estimator = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Estimator",
    )
    
    reviewer = create_estimation_assistant(
        feature_service,
        estimation_service,
        llm_config,
        name="Reviewer",
    )
    
    user_proxy = create_user_proxy(
        name="ProjectManager",
        human_input_mode="TERMINATE",
    )
    
    # Create group chat
    agents = [analyst, estimator, reviewer, user_proxy]
    group_chat, manager = create_group_chat(
        agents=agents,
        max_round=10,
        speaker_selection_method="auto",
    )
    
    print("\nGroup chat created with 4 agents:")
    print("- Analyst: Searches and clarifies features")
    print("- Estimator: Provides time estimates")
    print("- Reviewer: Validates and identifies risks")
    print("- Project Manager: Represents the human user")
    
    print("\nIn a real scenario, the agents would:")
    print("1. Discuss features collaboratively")
    print("2. Share insights and data")
    print("3. Challenge each other's assumptions")
    print("4. Arrive at consensus estimates")


def example_code_execution():
    """Example 3: Code execution for validation."""
    print("\n" + "=" * 70)
    print("Example 3: Code Execution for Validation")
    print("=" * 70)
    
    if not AUTOGEN_AVAILABLE:
        print("\n⚠️  AutoGen is not installed.")
        print("Install it with: pip install pyautogen")
        print("\nThis example demonstrates code execution:")
        print("\nUser: 'Calculate the P80 for these times: [4.5, 3.8, 4.2, 6.5, 7.0]'")
        print("\nAssistant: 'I'll write Python code to calculate that.'")
        print("\nCode executed:")
        print("```python")
        print("import numpy as np")
        print("times = [4.5, 3.8, 4.2, 6.5, 7.0]")
        print("p80 = np.percentile(times, 80)")
        print("print(f'P80: {p80}h')")
        print("```")
        print("\nOutput: P80: 6.62h")
        print("\nAssistant: 'The P80 (80th percentile) is 6.62 hours.'")
        return
    
    from src.agents import add_code_execution_tool
    
    user_proxy = create_user_proxy(
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False,  # Set to True for production
            "timeout": 60,
        }
    )
    
    # Add code execution capabilities
    add_code_execution_tool(
        user_proxy,
        allowed_operations=["math", "statistics", "numpy", "pandas"]
    )
    
    print("\nUser proxy configured with code execution:")
    print("- Work directory: workspace/")
    print("- Docker sandboxing: Disabled (for demo)")
    print("- Timeout: 60 seconds")
    print("- Allowed imports: math, statistics, numpy, pandas")
    
    print("\nThe agent can now:")
    print("- Execute Python code for calculations")
    print("- Validate estimates programmatically")
    print("- Perform statistical analysis")
    print("- Generate reports")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("AutoGen Conversational Agents for AITEA")
    print("=" * 70)
    
    if not AUTOGEN_AVAILABLE:
        print("\n⚠️  AutoGen is not installed.")
        print("\nTo run these examples with real conversations:")
        print("1. Install AutoGen: pip install pyautogen")
        print("2. Set your OpenAI API key: export OPENAI_API_KEY=your-key")
        print("3. Run this script again")
        print("\nFor now, showing example conversation flows...\n")
    
    # Run examples
    example_simple_conversation()
    example_group_chat()
    example_code_execution()
    
    print("\n" + "=" * 70)
    print("Examples Complete")
    print("=" * 70)
    
    if AUTOGEN_AVAILABLE:
        print("\nNext steps:")
        print("1. Modify the examples to use your own data")
        print("2. Experiment with different human_input_modes")
        print("3. Try different speaker_selection_methods")
        print("4. Enable Docker for safer code execution")
    else:
        print("\nTo enable real conversations:")
        print("pip install pyautogen")


if __name__ == "__main__":
    main()
