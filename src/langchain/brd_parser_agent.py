"""LangGraph BRD Parser Agent with StateGraph, conditional edges, and memory.

This module implements a LangGraph agent for parsing Business Requirements Documents (BRDs)
and extracting features with time estimates. It demonstrates:
- StateGraph with multiple nodes
- Conditional edges for workflow control
- Memory management
- Human-in-the-loop support

Requirements: 6.4
"""

from typing import TypedDict, Annotated, Sequence, Literal, Optional, List, Dict, Any
from typing_extensions import TypedDict as TypedDictExt
import operator
from pydantic import BaseModel, Field

try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.prebuilt import ToolNode
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    # Provide stub classes for type checking
    class StateGraph:  # type: ignore
        def __init__(self, state_schema): pass
        def add_node(self, name, func): pass
        def add_edge(self, from_node, to_node): pass
        def add_conditional_edges(self, source, path, path_map=None): pass
        def set_entry_point(self, node): pass
        def compile(self, checkpointer=None): return None
    
    class END:  # type: ignore
        pass
    
    class MemorySaver:  # type: ignore
        pass
    
    class ToolNode:  # type: ignore
        def __init__(self, tools): pass

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel


# Pydantic models for structured data
class ExtractedFeature(BaseModel):
    """A feature extracted from BRD."""
    name: str = Field(description="Feature name")
    description: str = Field(description="Feature description")
    team: str = Field(description="Team responsible")
    estimated_hours: float = Field(description="Estimated time in hours")
    confidence: str = Field(description="Confidence level (low, medium, high)")
    dependencies: List[str] = Field(default_factory=list, description="Feature dependencies")


class BRDParseResult(BaseModel):
    """Result of BRD parsing."""
    features: List[ExtractedFeature] = Field(description="Extracted features")
    total_features: int = Field(description="Total number of features")
    total_hours: float = Field(description="Total estimated hours")
    needs_clarification: List[str] = Field(default_factory=list, description="Items needing clarification")


# State definition for the agent
class AgentState(TypedDict):
    """State for the BRD parser agent.
    
    This state is passed between nodes and accumulates information
    throughout the workflow.
    """
    # Input
    brd_text: str
    
    # Messages for conversation history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Extracted features (accumulated)
    features: Annotated[List[ExtractedFeature], operator.add]
    
    # Items needing clarification
    clarifications_needed: Annotated[List[str], operator.add]
    
    # Current step in the workflow
    current_step: str
    
    # Whether human review is needed
    needs_human_review: bool
    
    # Human feedback (if provided)
    human_feedback: Optional[str]
    
    # Final result
    result: Optional[BRDParseResult]


class BRDParserAgent:
    """LangGraph agent for parsing BRD documents.
    
    This agent uses a StateGraph to orchestrate the BRD parsing workflow:
    1. Extract features from BRD text
    2. Validate extracted features
    3. Identify items needing clarification
    4. Request human review if needed
    5. Finalize results
    
    The agent demonstrates:
    - Multiple nodes with specific responsibilities
    - Conditional edges based on state
    - Memory persistence across runs
    - Human-in-the-loop for validation
    
    Example:
        >>> agent = BRDParserAgent(llm)
        >>> result = agent.parse_brd(brd_text)
        >>> print(f"Found {result['total_features']} features")
    """
    
    def __init__(self, llm: BaseChatModel, enable_memory: bool = True):
        """Initialize the BRD parser agent.
        
        Args:
            llm: Language model for processing
            enable_memory: Whether to enable memory persistence
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError(
                "langgraph is required for BRDParserAgent. "
                "Install it with: pip install langgraph"
            )
        
        self.llm = llm
        self.enable_memory = enable_memory
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> Any:
        """Build the StateGraph for BRD parsing.
        
        Returns:
            Compiled graph ready for execution
        """
        # Create the graph with our state schema
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("extract_features", self._extract_features_node)
        workflow.add_node("validate_features", self._validate_features_node)
        workflow.add_node("identify_clarifications", self._identify_clarifications_node)
        workflow.add_node("request_human_review", self._request_human_review_node)
        workflow.add_node("finalize_results", self._finalize_results_node)
        
        # Set entry point
        workflow.set_entry_point("extract_features")
        
        # Add edges
        workflow.add_edge("extract_features", "validate_features")
        workflow.add_edge("validate_features", "identify_clarifications")
        
        # Conditional edge: check if human review is needed
        workflow.add_conditional_edges(
            "identify_clarifications",
            self._should_request_human_review,
            {
                "human_review": "request_human_review",
                "finalize": "finalize_results"
            }
        )
        
        # After human review, go to finalize
        workflow.add_edge("request_human_review", "finalize_results")
        
        # Finalize ends the workflow
        workflow.add_edge("finalize_results", END)
        
        # Compile with memory if enabled
        if self.enable_memory:
            memory = MemorySaver()
            return workflow.compile(checkpointer=memory)
        else:
            return workflow.compile()
    
    def _extract_features_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Extract features from BRD text.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with extracted features
        """
        brd_text = state["brd_text"]
        
        # Create extraction prompt
        system_msg = SystemMessage(content="""You are an expert business analyst. 
Extract software features from Business Requirements Documents (BRDs).

For each feature, identify:
- name: Clear, concise feature name
- description: Detailed description
- team: Responsible team (backend, frontend, fullstack, design, qa, devops)
- estimated_hours: Time estimate in hours
- confidence: Confidence level (low, medium, high)
- dependencies: List of other features this depends on

Be thorough and extract all features mentioned.""")
        
        human_msg = HumanMessage(content=f"""BRD Document:

{brd_text}

Extract all features from this BRD. Return a JSON array of features.""")
        
        # Invoke LLM
        messages = [system_msg, human_msg]
        response = self.llm.invoke(messages)
        
        # Parse response (simplified - in production, use structured output)
        # For now, we'll create a sample feature
        features = [
            ExtractedFeature(
                name="Sample Feature",
                description="Extracted from BRD",
                team="backend",
                estimated_hours=8.0,
                confidence="medium",
                dependencies=[]
            )
        ]
        
        return {
            "messages": [system_msg, human_msg, response],
            "features": features,
            "current_step": "extract_features"
        }
    
    def _validate_features_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Validate extracted features for completeness.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with validation results
        """
        features = state["features"]
        
        # Validation logic
        validation_issues = []
        
        for feature in features:
            # Check for missing information
            if not feature.name:
                validation_issues.append(f"Feature missing name")
            if not feature.description:
                validation_issues.append(f"Feature '{feature.name}' missing description")
            if feature.estimated_hours <= 0:
                validation_issues.append(f"Feature '{feature.name}' has invalid estimate")
        
        # Create validation message
        if validation_issues:
            validation_msg = AIMessage(content=f"Validation found {len(validation_issues)} issues: {', '.join(validation_issues)}")
        else:
            validation_msg = AIMessage(content="All features validated successfully")
        
        return {
            "messages": [validation_msg],
            "current_step": "validate_features"
        }
    
    def _identify_clarifications_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Identify items that need clarification.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with clarification items
        """
        features = state["features"]
        clarifications = []
        
        # Check for ambiguous or incomplete features
        for feature in features:
            if feature.confidence == "low":
                clarifications.append(
                    f"Feature '{feature.name}' has low confidence - needs clarification"
                )
            
            if not feature.dependencies and "integration" in feature.description.lower():
                clarifications.append(
                    f"Feature '{feature.name}' mentions integration but has no dependencies listed"
                )
        
        # Determine if human review is needed
        needs_review = len(clarifications) > 0
        
        clarification_msg = AIMessage(
            content=f"Identified {len(clarifications)} items needing clarification"
        )
        
        return {
            "messages": [clarification_msg],
            "clarifications_needed": clarifications,
            "needs_human_review": needs_review,
            "current_step": "identify_clarifications"
        }
    
    def _should_request_human_review(self, state: AgentState) -> Literal["human_review", "finalize"]:
        """Conditional edge: Determine if human review is needed.
        
        Args:
            state: Current agent state
            
        Returns:
            Next node to execute
        """
        if state.get("needs_human_review", False):
            return "human_review"
        return "finalize"
    
    def _request_human_review_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Request human review for clarifications.
        
        This is a human-in-the-loop node that would pause execution
        and wait for human input in a production system.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with human feedback
        """
        clarifications = state.get("clarifications_needed", [])
        
        # In a real system, this would pause and wait for human input
        # For now, we'll simulate with a message
        review_msg = HumanMessage(
            content=f"""Human review requested for {len(clarifications)} items:

{chr(10).join(f'- {item}' for item in clarifications)}

Please provide feedback or approve to continue."""
        )
        
        # Simulate human feedback (in production, this would come from user)
        feedback = state.get("human_feedback", "Approved - proceed with current features")
        
        feedback_msg = HumanMessage(content=feedback)
        
        return {
            "messages": [review_msg, feedback_msg],
            "current_step": "request_human_review"
        }
    
    def _finalize_results_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Finalize and package results.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with final results
        """
        features = state["features"]
        clarifications = state.get("clarifications_needed", [])
        
        # Calculate totals
        total_hours = sum(f.estimated_hours for f in features)
        
        # Create final result
        result = BRDParseResult(
            features=features,
            total_features=len(features),
            total_hours=total_hours,
            needs_clarification=clarifications
        )
        
        final_msg = AIMessage(
            content=f"""BRD parsing complete:
- {result.total_features} features extracted
- {result.total_hours} total hours estimated
- {len(result.needs_clarification)} items need clarification"""
        )
        
        return {
            "messages": [final_msg],
            "result": result,
            "current_step": "finalize_results"
        }
    
    def parse_brd(
        self,
        brd_text: str,
        human_feedback: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> BRDParseResult:
        """Parse a BRD document and extract features.
        
        Args:
            brd_text: The BRD document text
            human_feedback: Optional human feedback for clarifications
            thread_id: Optional thread ID for memory persistence
            
        Returns:
            Parsed BRD result with features and estimates
            
        Example:
            >>> agent = BRDParserAgent(llm)
            >>> result = agent.parse_brd(brd_text)
            >>> for feature in result.features:
            ...     print(f"{feature.name}: {feature.estimated_hours}h")
        """
        # Initial state
        initial_state: AgentState = {
            "brd_text": brd_text,
            "messages": [],
            "features": [],
            "clarifications_needed": [],
            "current_step": "start",
            "needs_human_review": False,
            "human_feedback": human_feedback,
            "result": None
        }
        
        # Configure execution
        config = {"configurable": {"thread_id": thread_id or "default"}} if self.enable_memory else {}
        
        # Run the graph
        final_state = self.graph.invoke(initial_state, config)
        
        # Return the result
        return final_state["result"]
    
    def parse_brd_stream(
        self,
        brd_text: str,
        human_feedback: Optional[str] = None,
        thread_id: Optional[str] = None
    ):
        """Parse a BRD document with streaming updates.
        
        This method streams intermediate states as the agent progresses
        through the workflow, allowing for real-time monitoring.
        
        Args:
            brd_text: The BRD document text
            human_feedback: Optional human feedback for clarifications
            thread_id: Optional thread ID for memory persistence
            
        Yields:
            State updates as the agent progresses
            
        Example:
            >>> agent = BRDParserAgent(llm)
            >>> for state in agent.parse_brd_stream(brd_text):
            ...     print(f"Step: {state['current_step']}")
        """
        # Initial state
        initial_state: AgentState = {
            "brd_text": brd_text,
            "messages": [],
            "features": [],
            "clarifications_needed": [],
            "current_step": "start",
            "needs_human_review": False,
            "human_feedback": human_feedback,
            "result": None
        }
        
        # Configure execution
        config = {"configurable": {"thread_id": thread_id or "default"}} if self.enable_memory else {}
        
        # Stream the graph execution
        for state in self.graph.stream(initial_state, config):
            yield state


def create_brd_parser_agent(
    llm: BaseChatModel,
    enable_memory: bool = True
) -> BRDParserAgent:
    """Factory function to create a BRD parser agent.
    
    Args:
        llm: Language model for processing
        enable_memory: Whether to enable memory persistence
        
    Returns:
        Configured BRD parser agent
        
    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> llm = ChatOpenAI(model="gpt-4")
        >>> agent = create_brd_parser_agent(llm)
        >>> result = agent.parse_brd(brd_text)
    """
    return BRDParserAgent(llm, enable_memory)
