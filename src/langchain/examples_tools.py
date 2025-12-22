"""Examples demonstrating LangChain tools usage.

This module provides practical examples of using the AITEA LangChain tools
both directly and with agents.
"""

from src.langchain.tools import create_feature_tools
from src.services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)


def example_1_direct_tool_usage():
    """Example 1: Using tools directly without an agent."""
    print("=" * 70)
    print("Example 1: Direct Tool Usage")
    print("=" * 70)
    
    # Create services
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    
    # Create tools
    tools = create_feature_tools(feature_lib, time_track, estimator)
    add_feature_tool = tools[0]
    estimate_tool = tools[3]
    
    # Add a feature
    print("\n1. Adding a feature...")
    result = add_feature_tool.invoke({
        "id": "feat_001",
        "name": "User Authentication",
        "team": "backend",
        "process": "Authentication",
        "seed_time_hours": 8.0,
        "synonyms": ["auth", "login"],
        "notes": "JWT-based authentication with refresh tokens"
    })
    print(result)
    
    # Estimate the feature
    print("\n2. Estimating the feature...")
    result = estimate_tool.invoke({
        "feature_name": "User Authentication"
    })
    print(result)


def example_2_multiple_tools():
    """Example 2: Using multiple tools in sequence."""
    print("\n" + "=" * 70)
    print("Example 2: Multiple Tools in Sequence")
    print("=" * 70)
    
    # Create services
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    
    # Create tools
    tools = create_feature_tools(feature_lib, time_track, estimator)
    add_feature_tool = tools[0]
    add_entry_tool = tools[5]
    estimate_tool = tools[3]
    
    # Add features
    print("\n1. Adding features...")
    features_to_add = [
        {
            "id": "feat_001",
            "name": "User Authentication",
            "team": "backend",
            "process": "Authentication",
            "seed_time_hours": 8.0
        },
        {
            "id": "feat_002",
            "name": "Dashboard UI",
            "team": "frontend",
            "process": "Content Management",
            "seed_time_hours": 12.0
        },
        {
            "id": "feat_003",
            "name": "API Integration",
            "team": "backend",
            "process": "Integration",
            "seed_time_hours": 6.0
        }
    ]
    
    for feat in features_to_add:
        result = add_feature_tool.invoke(feat)
        print(f"  {result}")
    
    # Add time entries for User Authentication
    print("\n2. Adding tracked time entries...")
    time_entries = [
        {
            "id": "entry_001",
            "team": "backend",
            "member_name": "BE-1",
            "feature": "User Authentication",
            "tracked_time_hours": 7.5,
            "process": "Authentication",
            "date": "2025-01-15"
        },
        {
            "id": "entry_002",
            "team": "backend",
            "member_name": "BE-2",
            "feature": "User Authentication",
            "tracked_time_hours": 8.5,
            "process": "Authentication",
            "date": "2025-01-16"
        },
        {
            "id": "entry_003",
            "team": "backend",
            "member_name": "BE-3",
            "feature": "User Authentication",
            "tracked_time_hours": 9.0,
            "process": "Authentication",
            "date": "2025-01-17"
        }
    ]
    
    for entry in time_entries:
        result = add_entry_tool.invoke(entry)
        print(f"  {result}")
    
    # Estimate with historical data
    print("\n3. Estimating with historical data...")
    result = estimate_tool.invoke({
        "feature_name": "User Authentication"
    })
    print(result)


def example_3_project_estimation():
    """Example 3: Project estimation workflow."""
    print("\n" + "=" * 70)
    print("Example 3: Project Estimation Workflow")
    print("=" * 70)
    
    # Create services
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    
    # Create tools
    tools = create_feature_tools(feature_lib, time_track, estimator)
    add_feature_tool = tools[0]
    list_tool = tools[2]
    estimate_project_tool = tools[4]
    
    # Add project features
    print("\n1. Setting up project features...")
    project_features = [
        {
            "id": "feat_001",
            "name": "User Registration",
            "team": "backend",
            "process": "Authentication",
            "seed_time_hours": 6.0
        },
        {
            "id": "feat_002",
            "name": "User Login",
            "team": "backend",
            "process": "Authentication",
            "seed_time_hours": 4.0
        },
        {
            "id": "feat_003",
            "name": "Password Reset",
            "team": "backend",
            "process": "Authentication",
            "seed_time_hours": 5.0
        },
        {
            "id": "feat_004",
            "name": "Profile Page",
            "team": "frontend",
            "process": "Content Management",
            "seed_time_hours": 8.0
        },
        {
            "id": "feat_005",
            "name": "Settings Page",
            "team": "frontend",
            "process": "Content Management",
            "seed_time_hours": 6.0
        }
    ]
    
    for feat in project_features:
        add_feature_tool.invoke(feat)
    
    # List all features
    print("\n2. Listing all features...")
    result = list_tool.invoke({})
    print(result)
    
    # Estimate the project
    print("\n3. Estimating the complete project...")
    result = estimate_project_tool.invoke({
        "features": [
            "User Registration",
            "User Login",
            "Password Reset",
            "Profile Page",
            "Settings Page"
        ]
    })
    print(result)


def example_4_search_and_filter():
    """Example 4: Searching and filtering features."""
    print("\n" + "=" * 70)
    print("Example 4: Search and Filter Operations")
    print("=" * 70)
    
    # Create services
    feature_lib = FeatureLibraryService()
    time_track = TimeTrackingService()
    estimator = EstimationService(feature_lib, time_track)
    
    # Create tools
    tools = create_feature_tools(feature_lib, time_track, estimator)
    add_feature_tool = tools[0]
    search_tool = tools[1]
    list_tool = tools[2]
    
    # Add diverse features
    print("\n1. Adding diverse features...")
    features = [
        {
            "id": "feat_001",
            "name": "User Authentication",
            "team": "backend",
            "process": "Authentication",
            "seed_time_hours": 8.0,
            "synonyms": ["auth", "login", "signin"]
        },
        {
            "id": "feat_002",
            "name": "Dashboard UI",
            "team": "frontend",
            "process": "Content Management",
            "seed_time_hours": 12.0,
            "synonyms": ["dashboard", "home"]
        },
        {
            "id": "feat_003",
            "name": "API Gateway",
            "team": "backend",
            "process": "Integration",
            "seed_time_hours": 10.0,
            "synonyms": ["gateway", "api"]
        },
        {
            "id": "feat_004",
            "name": "User Profile",
            "team": "fullstack",
            "process": "Content Management",
            "seed_time_hours": 7.0,
            "synonyms": ["profile", "account"]
        }
    ]
    
    for feat in features:
        add_feature_tool.invoke(feat)
    
    # Search by name
    print("\n2. Searching for 'auth'...")
    result = search_tool.invoke({"query": "auth"})
    print(result)
    
    # Search by synonym
    print("\n3. Searching for 'dashboard'...")
    result = search_tool.invoke({"query": "dashboard"})
    print(result)
    
    # List backend features
    print("\n4. Listing backend features...")
    result = list_tool.invoke({"team": "backend"})
    print(result)
    
    # List frontend features
    print("\n5. Listing frontend features...")
    result = list_tool.invoke({"team": "frontend"})
    print(result)


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("AITEA LangChain Tools - Usage Examples")
    print("=" * 70)
    
    try:
        example_1_direct_tool_usage()
        example_2_multiple_tools()
        example_3_project_estimation()
        example_4_search_and_filter()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
