"""Example: Using CrewAI Multi-Agent System for Project Estimation

This example demonstrates how to use the CrewAI multi-agent system to:
1. Extract features from a BRD document
2. Estimate time for each feature
3. Validate estimates and identify risks

Requirements:
- CrewAI installed: pip install crewai
- AITEA services initialized with sample data
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)
from src.agents import (
    CREWAI_AVAILABLE,
    create_estimation_crew,
    run_estimation_workflow,
)
from src.models import Feature, TeamType, TrackedTimeEntry, EstimationConfig
from datetime import date


def setup_sample_data():
    """Set up sample feature library and tracked time data."""
    # Initialize services
    feature_service = FeatureLibraryService()
    time_tracking_service = TimeTrackingService()
    
    # Add sample features
    features = [
        Feature(
            id="f1",
            name="User Authentication",
            team=TeamType.BACKEND,
            process="Authentication",
            seed_time_hours=8.0,
            synonyms=["auth", "login", "signup"],
            notes="Standard user authentication with JWT"
        ),
        Feature(
            id="f2",
            name="CRUD API",
            team=TeamType.BACKEND,
            process="Data Operations",
            seed_time_hours=4.0,
            synonyms=["rest-api", "crud-endpoints"],
            notes="Basic CRUD operations for a resource"
        ),
        Feature(
            id="f3",
            name="Product Catalog",
            team=TeamType.FULLSTACK,
            process="Content Management",
            seed_time_hours=16.0,
            synonyms=["product-list", "catalog-ui"],
            notes="Product listing with search and filters"
        ),
        Feature(
            id="f4",
            name="Payment Integration",
            team=TeamType.BACKEND,
            process="Integration",
            seed_time_hours=12.0,
            synonyms=["payment", "stripe", "checkout"],
            notes="Payment processing with Stripe"
        ),
    ]
    
    for feature in features:
        feature_service.add_feature(feature)
    
    # Add sample tracked time entries
    tracked_entries = [
        # User Authentication entries
        TrackedTimeEntry(
            id="t1",
            team=TeamType.BACKEND,
            member_name="BE-1",
            feature="User Authentication",
            tracked_time_hours=9.5,
            process="Authentication",
            date=date(2024, 1, 15)
        ),
        TrackedTimeEntry(
            id="t2",
            team=TeamType.BACKEND,
            member_name="BE-2",
            feature="User Authentication",
            tracked_time_hours=8.0,
            process="Authentication",
            date=date(2024, 2, 10)
        ),
        TrackedTimeEntry(
            id="t3",
            team=TeamType.BACKEND,
            member_name="BE-3",
            feature="User Authentication",
            tracked_time_hours=10.5,
            process="Authentication",
            date=date(2024, 3, 5)
        ),
        # CRUD API entries
        TrackedTimeEntry(
            id="t4",
            team=TeamType.BACKEND,
            member_name="BE-1",
            feature="CRUD API",
            tracked_time_hours=4.5,
            process="Data Operations",
            date=date(2024, 1, 20)
        ),
        TrackedTimeEntry(
            id="t5",
            team=TeamType.BACKEND,
            member_name="BE-2",
            feature="CRUD API",
            tracked_time_hours=3.5,
            process="Data Operations",
            date=date(2024, 2, 15)
        ),
        TrackedTimeEntry(
            id="t6",
            team=TeamType.BACKEND,
            member_name="BE-3",
            feature="CRUD API",
            tracked_time_hours=5.0,
            process="Data Operations",
            date=date(2024, 3, 10)
        ),
        # Product Catalog entries (fewer data points)
        TrackedTimeEntry(
            id="t7",
            team=TeamType.FULLSTACK,
            member_name="FS-1",
            feature="Product Catalog",
            tracked_time_hours=18.0,
            process="Content Management",
            date=date(2024, 2, 1)
        ),
        TrackedTimeEntry(
            id="t8",
            team=TeamType.FULLSTACK,
            member_name="FS-2",
            feature="Product Catalog",
            tracked_time_hours=14.5,
            process="Content Management",
            date=date(2024, 3, 1)
        ),
    ]
    
    for entry in tracked_entries:
        time_tracking_service.add_entry(entry)
    
    return feature_service, time_tracking_service


def main():
    """Run the CrewAI estimation example."""
    print("=" * 70)
    print("CrewAI Multi-Agent Estimation Example")
    print("=" * 70)
    print()
    
    # Check if CrewAI is available
    if not CREWAI_AVAILABLE:
        print("❌ CrewAI is not installed!")
        print()
        print("To run this example, install CrewAI:")
        print("  pip install crewai")
        print()
        print("Or install with AITEA agents extras:")
        print("  pip install -e '.[agents]'")
        print()
        return
    
    print("✓ CrewAI is available")
    print()
    
    # Set up sample data
    print("Setting up sample data...")
    feature_service, time_tracking_service = setup_sample_data()
    
    config = EstimationConfig(
        use_outlier_detection=True,
        outlier_threshold_std=2.0,
        min_data_points_for_stats=3
    )
    estimation_service = EstimationService(
        feature_service,
        time_tracking_service,
        config
    )
    print(f"✓ Added {len(feature_service.list_features())} features to library")
    print(f"✓ Added {len(time_tracking_service.entries)} tracked time entries")
    print()
    
    # Sample BRD document
    brd_content = """
    Project: E-commerce Platform MVP
    
    Business Requirements:
    
    1. User Management
       - Users should be able to register and login
       - Support for email/password authentication
       - JWT-based session management
    
    2. Product Management
       - Display product catalog with images and descriptions
       - Search and filter functionality
       - Product detail pages
    
    3. Shopping Cart
       - Add/remove items from cart
       - Update quantities
       - Persist cart across sessions
    
    4. Checkout Process
       - Collect shipping information
       - Integrate with Stripe for payments
       - Order confirmation emails
    
    Timeline: 6 weeks
    Team: 2 backend developers, 1 fullstack developer
    """
    
    print("BRD Document:")
    print("-" * 70)
    print(brd_content)
    print("-" * 70)
    print()
    
    # Create the crew
    print("Creating CrewAI estimation crew...")
    print("  - Analyst Agent: Extract features from BRD")
    print("  - Estimator Agent: Provide time estimates")
    print("  - Reviewer Agent: Validate and identify risks")
    print()
    
    crew = create_estimation_crew(
        feature_service,
        estimation_service,
        process_type="sequential"
    )
    
    print("✓ Crew created with 3 agents")
    print()
    
    # Run the workflow
    print("Running estimation workflow...")
    print("(This may take a minute as agents collaborate)")
    print()
    
    try:
        result = crew.kickoff(inputs={"brd_content": brd_content})
        
        print("=" * 70)
        print("ESTIMATION RESULTS")
        print("=" * 70)
        print()
        print(result)
        print()
        
    except Exception as e:
        print(f"❌ Error running crew: {e}")
        print()
        print("Note: This example requires valid LLM API keys.")
        print("Set OPENAI_API_KEY environment variable to use OpenAI models.")
        print()
        return
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
