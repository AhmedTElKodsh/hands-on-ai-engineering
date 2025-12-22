"""LCEL chains for feature extraction and estimation.

This module implements LangChain Expression Language (LCEL) chains that
demonstrate the composable chain syntax using the pipe operator (|).
"""

from typing import Dict, Any, List, Optional
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field


# Pydantic models for structured output parsing
class ExtractedFeature(BaseModel):
    """A feature extracted from natural language description."""
    name: str = Field(description="Name of the feature")
    team: str = Field(description="Team responsible (backend, frontend, fullstack, design, qa, devops)")
    process: str = Field(description="Process type (Data Operations, Content Management, Real-time, Authentication, Integration)")
    estimated_hours: float = Field(description="Estimated time in hours")
    notes: str = Field(default="", description="Additional notes or context")


class FeatureExtractionOutput(BaseModel):
    """Output from feature extraction chain."""
    features: List[ExtractedFeature] = Field(description="List of extracted features")
    total_features: int = Field(description="Total number of features extracted")


class EstimationOutput(BaseModel):
    """Output from estimation chain."""
    feature_name: str = Field(description="Name of the feature being estimated")
    estimated_hours: float = Field(description="Estimated time in hours")
    confidence: str = Field(description="Confidence level (low, medium, high)")
    reasoning: str = Field(description="Explanation of the estimate")


def create_feature_extraction_chain(llm: BaseChatModel) -> Any:
    """Create an LCEL chain for extracting features from natural language.
    
    This chain demonstrates the pipe operator (|) for composing operations:
    1. Input processing with RunnablePassthrough
    2. Prompt template formatting
    3. LLM invocation
    4. JSON output parsing
    
    Args:
        llm: The language model to use for extraction
        
    Returns:
        A runnable chain that takes a project description and returns
        extracted features as structured data
        
    Example:
        >>> chain = create_feature_extraction_chain(llm)
        >>> result = chain.invoke({
        ...     "project_description": "Build a REST API with user authentication"
        ... })
        >>> print(result["features"])
    """
    # Define the prompt template for feature extraction
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert software analyst. Extract software features from project descriptions.
        
For each feature, identify:
- name: A clear, concise feature name
- team: The team responsible (backend, frontend, fullstack, design, qa, devops)
- process: The process type (Data Operations, Content Management, Real-time, Authentication, Integration)
- estimated_hours: Initial time estimate in hours
- notes: Any additional context

Be specific and break down complex requirements into individual features."""),
        ("human", "Project Description:\n{project_description}\n\nExtract all features from this description.")
    ])
    
    # Create JSON output parser with Pydantic model
    parser = JsonOutputParser(pydantic_object=FeatureExtractionOutput)
    
    # Add format instructions to the prompt
    extraction_prompt_with_format = extraction_prompt.partial(
        format_instructions=parser.get_format_instructions()
    )
    
    # Build the chain using LCEL pipe operator
    # RunnablePassthrough() passes input through unchanged
    chain = (
        {"project_description": RunnablePassthrough()}
        | extraction_prompt_with_format
        | llm
        | parser
    )
    
    return chain


def create_estimation_chain(
    llm: BaseChatModel,
    retriever: Optional[Any] = None
) -> Any:
    """Create an LCEL chain for estimating feature time with context.
    
    This chain demonstrates:
    1. RunnablePassthrough for preserving input data
    2. Optional retriever integration for RAG pattern
    3. Context injection into prompts
    4. Structured output parsing
    
    Args:
        llm: The language model to use for estimation
        retriever: Optional retriever for fetching similar features (RAG)
        
    Returns:
        A runnable chain that takes a feature description and returns
        a time estimate with reasoning
        
    Example:
        >>> chain = create_estimation_chain(llm)
        >>> result = chain.invoke({
        ...     "feature_name": "User Authentication",
        ...     "feature_description": "JWT-based auth with refresh tokens"
        ... })
        >>> print(f"{result['estimated_hours']} hours")
    """
    # Define the prompt template for estimation
    if retriever:
        # With RAG: include similar features as context
        estimation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert software estimator. Provide accurate time estimates for features.

Similar features from our database:
{context}

Use these examples to inform your estimate, but adjust based on the specific requirements."""),
            ("human", """Feature: {feature_name}
Description: {feature_description}

Provide a time estimate in hours with detailed reasoning.""")
        ])
        
        # Helper function to format retriever results
        def format_context(docs: List[Any]) -> str:
            """Format retrieved documents as context."""
            if not docs:
                return "No similar features found."
            return "\n".join([
                f"- {doc.metadata.get('name', 'Unknown')}: {doc.metadata.get('hours', 'N/A')} hours"
                for doc in docs
            ])
        
        # Chain with retriever
        chain = (
            {
                "feature_name": RunnablePassthrough() | (lambda x: x["feature_name"]),
                "feature_description": RunnablePassthrough() | (lambda x: x["feature_description"]),
                "context": RunnablePassthrough() 
                    | (lambda x: x.get("feature_description", ""))
                    | retriever 
                    | RunnableLambda(format_context)
            }
            | estimation_prompt
            | llm
            | JsonOutputParser(pydantic_object=EstimationOutput)
        )
    else:
        # Without RAG: direct estimation
        estimation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert software estimator. Provide accurate time estimates for features.

Consider:
- Complexity of the feature
- Team experience level
- Dependencies and integration points
- Testing and documentation time"""),
            ("human", """Feature: {feature_name}
Description: {feature_description}

Provide a time estimate in hours with detailed reasoning.""")
        ])
        
        # Chain without retriever - simpler data flow
        chain = (
            {
                "feature_name": RunnablePassthrough() | (lambda x: x.get("feature_name", "")),
                "feature_description": RunnablePassthrough() | (lambda x: x.get("feature_description", ""))
            }
            | estimation_prompt
            | llm
            | JsonOutputParser(pydantic_object=EstimationOutput)
        )
    
    return chain


def create_simple_passthrough_chain(llm: BaseChatModel) -> Any:
    """Create a simple chain demonstrating RunnablePassthrough.
    
    This is a minimal example showing how RunnablePassthrough preserves
    input data while allowing transformation of specific fields.
    
    Args:
        llm: The language model to use
        
    Returns:
        A chain that echoes input with LLM processing
        
    Example:
        >>> chain = create_simple_passthrough_chain(llm)
        >>> result = chain.invoke({"text": "Hello world"})
    """
    prompt = PromptTemplate.from_template(
        "Summarize this text in one sentence: {text}"
    )
    
    # RunnablePassthrough() preserves the entire input dict
    # We extract just the "text" field for the prompt
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def create_multi_input_chain(llm: BaseChatModel) -> Any:
    """Create a chain with multiple inputs using RunnablePassthrough.
    
    Demonstrates how to handle multiple input fields and pass them
    through to different parts of the chain.
    
    Args:
        llm: The language model to use
        
    Returns:
        A chain that processes multiple inputs
        
    Example:
        >>> chain = create_multi_input_chain(llm)
        >>> result = chain.invoke({
        ...     "feature": "User Login",
        ...     "team": "backend",
        ...     "complexity": "medium"
        ... })
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a software estimation expert."),
        ("human", """Estimate the time for this feature:
Feature: {feature}
Team: {team}
Complexity: {complexity}

Provide an estimate in hours.""")
    ])
    
    # RunnablePassthrough preserves all inputs
    # We can selectively extract fields for the prompt
    chain = (
        {
            "feature": RunnablePassthrough() | (lambda x: x["feature"]),
            "team": RunnablePassthrough() | (lambda x: x["team"]),
            "complexity": RunnablePassthrough() | (lambda x: x["complexity"])
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
