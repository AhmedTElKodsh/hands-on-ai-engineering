"""Examples demonstrating the LangGraph BRD Parser Agent.

This module provides examples of using the BRD parser agent with:
- Basic BRD parsing
- Streaming updates
- Memory persistence
- Human-in-the-loop review

Requirements: 6.4
"""

from typing import Optional
from langchain_core.language_models import BaseChatModel

try:
    from .brd_parser_agent import create_brd_parser_agent, BRDParseResult
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False


# Sample BRD document for testing
SAMPLE_BRD = """
# Project: E-Commerce Platform Enhancement

## Overview
Enhance the existing e-commerce platform with new features to improve user experience
and increase conversion rates.

## Requirements

### 1. User Authentication
Implement JWT-based authentication with refresh tokens. Users should be able to:
- Register with email/password
- Login with social providers (Google, Facebook)
- Reset password via email
- Enable two-factor authentication

Team: Backend
Estimated Time: 40 hours

### 2. Product Recommendation Engine
Build a recommendation system that suggests products based on:
- User browsing history
- Purchase history
- Similar user preferences
- Trending products

This feature depends on User Authentication for personalized recommendations.

Team: Backend + Data Science
Estimated Time: 80 hours

### 3. Shopping Cart Improvements
Enhance the shopping cart with:
- Save for later functionality
- Quantity updates with real-time price calculation
- Apply discount codes
- Estimate shipping costs

Team: Frontend + Backend
Estimated Time: 32 hours

### 4. Payment Gateway Integration
Integrate Stripe payment gateway with support for:
- Credit/debit cards
- Digital wallets (Apple Pay, Google Pay)
- Buy now, pay later options
- Subscription billing

Team: Backend
Estimated Time: 48 hours

### 5. Admin Dashboard
Create an admin dashboard for:
- Product management (CRUD operations)
- Order management and fulfillment
- Customer support ticket system
- Analytics and reporting

Team: Fullstack
Estimated Time: 120 hours

## Notes
- All features should be mobile-responsive
- Performance target: Page load < 2 seconds
- Security: PCI DSS compliance required for payment processing
"""


def example_basic_parsing(llm: BaseChatModel) -> None:
    """Example: Basic BRD parsing.
    
    Demonstrates the simplest use case - parsing a BRD document
    and extracting features with estimates.
    
    Args:
        llm: Language model to use
    """
    if not AGENT_AVAILABLE:
        print("⚠️  LangGraph not available. Install with: pip install langgraph")
        return
    
    print("=" * 60)
    print("Example 1: Basic BRD Parsing")
    print("=" * 60)
    
    # Create the agent
    agent = create_brd_parser_agent(llm, enable_memory=False)
    
    # Parse the BRD
    print("\n📄 Parsing BRD document...")
    result = agent.parse_brd(SAMPLE_BRD)
    
    # Display results
    print(f"\n✅ Parsing complete!")
    print(f"   Features extracted: {result.total_features}")
    print(f"   Total estimated hours: {result.total_hours}")
    print(f"   Items needing clarification: {len(result.needs_clarification)}")
    
    print("\n📋 Extracted Features:")
    for i, feature in enumerate(result.features, 1):
        print(f"\n{i}. {feature.name}")
        print(f"   Team: {feature.team}")
        print(f"   Estimate: {feature.estimated_hours} hours")
        print(f"   Confidence: {feature.confidence}")
        if feature.dependencies:
            print(f"   Dependencies: {', '.join(feature.dependencies)}")
    
    if result.needs_clarification:
        print("\n⚠️  Items Needing Clarification:")
        for item in result.needs_clarification:
            print(f"   - {item}")


def example_streaming_parsing(llm: BaseChatModel) -> None:
    """Example: Streaming BRD parsing with progress updates.
    
    Demonstrates streaming the agent's progress through the workflow,
    allowing for real-time monitoring and UI updates.
    
    Args:
        llm: Language model to use
    """
    if not AGENT_AVAILABLE:
        print("⚠️  LangGraph not available. Install with: pip install langgraph")
        return
    
    print("\n" + "=" * 60)
    print("Example 2: Streaming BRD Parsing")
    print("=" * 60)
    
    # Create the agent
    agent = create_brd_parser_agent(llm, enable_memory=False)
    
    # Parse with streaming
    print("\n📄 Parsing BRD document with streaming updates...")
    
    for state_update in agent.parse_brd_stream(SAMPLE_BRD):
        # Each state_update is a dict with the node name as key
        for node_name, node_state in state_update.items():
            current_step = node_state.get("current_step", "unknown")
            print(f"   ⏳ Step: {current_step}")
            
            # Show progress based on step
            if current_step == "extract_features":
                features_count = len(node_state.get("features", []))
                print(f"      Extracted {features_count} features so far...")
            elif current_step == "validate_features":
                print(f"      Validating extracted features...")
            elif current_step == "identify_clarifications":
                clarifications = len(node_state.get("clarifications_needed", []))
                print(f"      Found {clarifications} items needing clarification...")
            elif current_step == "finalize_results":
                result = node_state.get("result")
                if result:
                    print(f"      ✅ Complete! {result.total_features} features, {result.total_hours} hours")


def example_with_memory(llm: BaseChatModel) -> None:
    """Example: BRD parsing with memory persistence.
    
    Demonstrates using memory to persist state across multiple runs,
    allowing for resumable workflows and conversation history.
    
    Args:
        llm: Language model to use
    """
    if not AGENT_AVAILABLE:
        print("⚠️  LangGraph not available. Install with: pip install langgraph")
        return
    
    print("\n" + "=" * 60)
    print("Example 3: BRD Parsing with Memory")
    print("=" * 60)
    
    # Create the agent with memory enabled
    agent = create_brd_parser_agent(llm, enable_memory=True)
    
    # First run - parse the BRD
    print("\n📄 First run: Parsing BRD...")
    thread_id = "project-123"
    result1 = agent.parse_brd(SAMPLE_BRD, thread_id=thread_id)
    print(f"   ✅ Extracted {result1.total_features} features")
    
    # Second run - same thread, memory is preserved
    print("\n📄 Second run: Using same thread (memory preserved)...")
    result2 = agent.parse_brd(SAMPLE_BRD, thread_id=thread_id)
    print(f"   ✅ Extracted {result2.total_features} features")
    print("   💾 Memory from first run was available")
    
    # Third run - different thread, fresh start
    print("\n📄 Third run: Using different thread (fresh start)...")
    result3 = agent.parse_brd(SAMPLE_BRD, thread_id="project-456")
    print(f"   ✅ Extracted {result3.total_features} features")
    print("   🆕 Started with clean state")


def example_human_in_the_loop(llm: BaseChatModel) -> None:
    """Example: BRD parsing with human review.
    
    Demonstrates the human-in-the-loop pattern where the agent
    requests human feedback for items needing clarification.
    
    Args:
        llm: Language model to use
    """
    if not AGENT_AVAILABLE:
        print("⚠️  LangGraph not available. Install with: pip install langgraph")
        return
    
    print("\n" + "=" * 60)
    print("Example 4: BRD Parsing with Human Review")
    print("=" * 60)
    
    # Create the agent
    agent = create_brd_parser_agent(llm, enable_memory=False)
    
    # Parse without human feedback first
    print("\n📄 First pass: Parsing without human feedback...")
    result1 = agent.parse_brd(SAMPLE_BRD)
    
    if result1.needs_clarification:
        print(f"\n⚠️  Agent identified {len(result1.needs_clarification)} items needing clarification:")
        for item in result1.needs_clarification:
            print(f"   - {item}")
        
        # Simulate human providing feedback
        print("\n👤 Human provides feedback...")
        human_feedback = """
        Regarding the low confidence items:
        - Product Recommendation Engine: Confirmed 80 hours is reasonable
        - Admin Dashboard: Break down into smaller features for better estimation
        
        Approved to proceed with current estimates.
        """
        
        # Parse again with human feedback
        print("\n📄 Second pass: Parsing with human feedback...")
        result2 = agent.parse_brd(SAMPLE_BRD, human_feedback=human_feedback)
        print(f"   ✅ Complete with human input incorporated")
        print(f"   Features: {result2.total_features}")
        print(f"   Total hours: {result2.total_hours}")
    else:
        print("\n✅ No clarifications needed - parsing complete!")


def example_workflow_visualization() -> None:
    """Example: Visualize the agent workflow.
    
    Shows the structure of the StateGraph including nodes and edges.
    This helps understand the agent's decision-making process.
    """
    print("\n" + "=" * 60)
    print("Example 5: Agent Workflow Visualization")
    print("=" * 60)
    
    print("""
    BRD Parser Agent Workflow:
    
    ┌─────────────────┐
    │ extract_features│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │validate_features│
    └────────┬────────┘
             │
             ▼
    ┌──────────────────────┐
    │identify_clarifications│
    └──────────┬───────────┘
               │
               ├─── needs_human_review? ───┐
               │                            │
               ▼ (yes)                      ▼ (no)
    ┌──────────────────────┐      ┌─────────────────┐
    │request_human_review  │      │finalize_results │
    └──────────┬───────────┘      └────────┬────────┘
               │                            │
               └────────────────────────────┤
                                            ▼
                                          [END]
    
    Key Features:
    - StateGraph with 5 nodes
    - Conditional edge based on needs_human_review flag
    - Memory persistence across runs
    - Human-in-the-loop support
    - Streaming updates available
    """)


def run_all_examples(llm: Optional[BaseChatModel] = None) -> None:
    """Run all BRD parser agent examples.
    
    Args:
        llm: Optional language model. If not provided, examples will
             show structure without actual LLM calls.
    """
    if llm is None:
        print("⚠️  No LLM provided. Showing workflow visualization only.")
        example_workflow_visualization()
        return
    
    # Run all examples
    example_basic_parsing(llm)
    example_streaming_parsing(llm)
    example_with_memory(llm)
    example_human_in_the_loop(llm)
    example_workflow_visualization()
    
    print("\n" + "=" * 60)
    print("All examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    # Show workflow visualization without requiring LLM
    example_workflow_visualization()
    
    print("\n💡 To run with actual LLM:")
    print("   from langchain_openai import ChatOpenAI")
    print("   llm = ChatOpenAI(model='gpt-4')")
    print("   run_all_examples(llm)")
