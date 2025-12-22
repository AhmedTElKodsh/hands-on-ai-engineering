"""Examples demonstrating LangSmith integration for AITEA.

This module shows how to use LangSmith for tracing, evaluation,
and dataset management with AITEA chains and agents.
"""

import os
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .observability import (
    configure_langsmith,
    trace_chain,
    trace_agent,
    create_evaluator,
    evaluate_chain,
    create_dataset,
    add_examples,
    DatasetExample,
    create_feature_extraction_evaluator,
    create_estimation_accuracy_evaluator,
)
from .chains import create_feature_extraction_chain, create_estimation_chain
from .brd_parser_agent import create_brd_parser_agent


def example_1_configure_tracing():
    """Example 1: Configure LangSmith tracing.
    
    This example shows how to set up LangSmith tracing for your
    AITEA application.
    """
    print("=" * 60)
    print("Example 1: Configure LangSmith Tracing")
    print("=" * 60)
    
    # Option 1: Configure with explicit API key
    config = configure_langsmith(
        api_key=os.getenv("LANGSMITH_API_KEY"),
        project="aitea-demo",
        tracing_enabled=True,
    )
    
    print(f"\nTracing enabled: {config.tracing_enabled}")
    print(f"Project: {config.project}")
    
    # Option 2: Auto-configure from environment variables
    # Just set LANGSMITH_API_KEY and it will auto-configure on import
    
    print("\n✅ LangSmith configured!")


def example_2_trace_chain():
    """Example 2: Trace a chain execution.
    
    This example shows how to automatically trace chain executions
    using the @trace_chain decorator.
    """
    print("\n" + "=" * 60)
    print("Example 2: Trace Chain Execution")
    print("=" * 60)
    
    # Configure LangSmith
    configure_langsmith(project="aitea-demo")
    
    # Use decorator to automatically trace
    @trace_chain(name="feature_extraction", tags=["extraction", "brd"])
    def extract_features(brd_text: str) -> Dict[str, Any]:
        """Extract features from BRD text with automatic tracing."""
        chain = create_feature_extraction_chain()
        return chain.invoke({"brd_text": brd_text})
    
    # Execute - will be automatically traced
    brd_text = """
    Build a user authentication system with:
    - Login with email/password
    - Registration with email verification
    - Password reset functionality
    """
    
    result = extract_features(brd_text)
    print(f"\nExtracted {len(result.get('features', []))} features")
    print("✅ Check LangSmith dashboard for trace!")


def example_3_trace_agent():
    """Example 3: Trace an agent execution.
    
    This example shows how to trace agent executions with
    agent-specific tags.
    """
    print("\n" + "=" * 60)
    print("Example 3: Trace Agent Execution")
    print("=" * 60)
    
    # Configure LangSmith
    configure_langsmith(project="aitea-demo")
    
    # Use decorator to automatically trace agent
    @trace_agent(name="brd_parser", tags=["agent", "brd", "parsing"])
    def parse_brd(brd_text: str) -> Dict[str, Any]:
        """Parse BRD with automatic agent tracing."""
        agent = create_brd_parser_agent()
        return agent.invoke({"brd_text": brd_text})
    
    # Execute - will be automatically traced with agent tags
    brd_text = """
    Project: E-commerce Platform
    
    Features:
    1. Product catalog with search
    2. Shopping cart
    3. Payment processing
    """
    
    result = parse_brd(brd_text)
    print(f"\nParsed BRD with {len(result.get('features', []))} features")
    print("✅ Check LangSmith dashboard for agent trace!")


def example_4_create_dataset():
    """Example 4: Create evaluation dataset.
    
    This example shows how to create a dataset in LangSmith
    for evaluation purposes.
    """
    print("\n" + "=" * 60)
    print("Example 4: Create Evaluation Dataset")
    print("=" * 60)
    
    # Configure LangSmith
    configure_langsmith(project="aitea-demo")
    
    # Create examples
    examples = [
        DatasetExample(
            inputs={
                "brd_text": "Build a login feature with OAuth support"
            },
            outputs={
                "features": ["authentication", "login", "oauth"],
                "feature_count": 3,
            },
            metadata={"category": "authentication"},
        ),
        DatasetExample(
            inputs={
                "brd_text": "Create a CRUD API for managing users"
            },
            outputs={
                "features": ["CRUD", "api", "user-management"],
                "feature_count": 3,
            },
            metadata={"category": "data_operations"},
        ),
        DatasetExample(
            inputs={
                "brd_text": "Implement real-time notifications with WebSocket"
            },
            outputs={
                "features": ["websocket", "notifications", "real-time"],
                "feature_count": 3,
            },
            metadata={"category": "real_time"},
        ),
    ]
    
    # Create dataset
    dataset_id = create_dataset(
        name="feature_extraction_demo",
        description="Demo dataset for feature extraction",
        examples=examples,
    )
    
    if dataset_id:
        print(f"\n✅ Created dataset with ID: {dataset_id}")
        print("✅ Check LangSmith dashboard to view dataset!")
    else:
        print("\n⚠️  Failed to create dataset (check API key)")


def example_5_evaluate_chain():
    """Example 5: Evaluate chain against dataset.
    
    This example shows how to evaluate a chain's performance
    against a test dataset.
    """
    print("\n" + "=" * 60)
    print("Example 5: Evaluate Chain")
    print("=" * 60)
    
    # Configure LangSmith
    configure_langsmith(project="aitea-demo")
    
    # Create evaluators
    feature_evaluator = create_feature_extraction_evaluator()
    
    # Create chain
    chain = create_feature_extraction_chain()
    
    # Evaluate against dataset
    print("\nRunning evaluation...")
    result = evaluate_chain(
        chain,
        dataset_name="feature_extraction_demo",
        evaluators=[feature_evaluator],
    )
    
    # Print results
    print("\n" + str(result))
    print("✅ Check LangSmith dashboard for detailed results!")


def example_6_custom_evaluator():
    """Example 6: Create custom evaluator.
    
    This example shows how to create a custom evaluator
    for domain-specific validation.
    """
    print("\n" + "=" * 60)
    print("Example 6: Custom Evaluator")
    print("=" * 60)
    
    # Create custom evaluator
    def check_team_assignment(expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """Check if features have correct team assignments."""
        for feature in actual.get("features", []):
            if "team" not in feature:
                return False
            if feature["team"] not in ["backend", "frontend", "fullstack"]:
                return False
        return True
    
    team_evaluator = create_evaluator(
        name="team_assignment",
        evaluator_fn=check_team_assignment,
        description="Validates that all features have valid team assignments",
    )
    
    print("\n✅ Created custom evaluator: team_assignment")
    print("Use this evaluator in evaluate_chain() or evaluate_agent()")


def example_7_manual_tracing():
    """Example 7: Manual tracing with tracer.
    
    This example shows how to manually add tracing to
    chain invocations without decorators.
    """
    print("\n" + "=" * 60)
    print("Example 7: Manual Tracing")
    print("=" * 60)
    
    # Configure LangSmith
    from .observability import get_tracer
    configure_langsmith(project="aitea-demo")
    
    # Get tracer
    tracer = get_tracer()
    
    if tracer:
        # Create chain
        chain = create_feature_extraction_chain()
        
        # Invoke with tracer in config
        result = chain.invoke(
            {"brd_text": "Build a payment processing system"},
            config={"callbacks": [tracer]},
        )
        
        print(f"\nExtracted {len(result.get('features', []))} features")
        print("✅ Manually traced execution!")
    else:
        print("\n⚠️  Tracer not available (check API key)")


def example_8_add_examples_to_dataset():
    """Example 8: Add examples to existing dataset.
    
    This example shows how to add more examples to an
    existing dataset.
    """
    print("\n" + "=" * 60)
    print("Example 8: Add Examples to Dataset")
    print("=" * 60)
    
    # Configure LangSmith
    configure_langsmith(project="aitea-demo")
    
    # Create new examples
    new_examples = [
        DatasetExample(
            inputs={
                "brd_text": "Implement file upload with S3 integration"
            },
            outputs={
                "features": ["file-upload", "s3", "storage"],
                "feature_count": 3,
            },
            metadata={"category": "integration"},
        ),
        DatasetExample(
            inputs={
                "brd_text": "Add email notifications for order updates"
            },
            outputs={
                "features": ["email", "notifications", "orders"],
                "feature_count": 3,
            },
            metadata={"category": "notifications"},
        ),
    ]
    
    # Add to existing dataset
    count = add_examples("feature_extraction_demo", new_examples)
    
    if count > 0:
        print(f"\n✅ Added {count} examples to dataset!")
    else:
        print("\n⚠️  Failed to add examples (check dataset exists)")


def run_all_examples():
    """Run all LangSmith examples."""
    print("\n" + "=" * 70)
    print(" " * 15 + "LANGSMITH INTEGRATION EXAMPLES")
    print("=" * 70)
    
    # Check if API key is set
    if not os.getenv("LANGSMITH_API_KEY"):
        print("\n⚠️  LANGSMITH_API_KEY not set!")
        print("Set it to run these examples:")
        print("  export LANGSMITH_API_KEY='your-api-key'")
        print("\nRunning examples in demo mode (limited functionality)...\n")
    
    try:
        example_1_configure_tracing()
        example_2_trace_chain()
        example_3_trace_agent()
        example_4_create_dataset()
        example_5_evaluate_chain()
        example_6_custom_evaluator()
        example_7_manual_tracing()
        example_8_add_examples_to_dataset()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure OPENAI_API_KEY and LANGSMITH_API_KEY are set")


if __name__ == "__main__":
    run_all_examples()
