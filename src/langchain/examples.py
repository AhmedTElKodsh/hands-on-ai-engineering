"""Example usage of LCEL chains.

This module provides examples of how to use the LCEL chains for
feature extraction and estimation.
"""

from typing import Optional
from langchain_core.language_models import BaseChatModel


def example_feature_extraction(llm: BaseChatModel) -> None:
    """Example: Extract features from a project description.
    
    Args:
        llm: The language model to use
    """
    from .chains import create_feature_extraction_chain
    
    # Create the chain
    chain = create_feature_extraction_chain(llm)
    
    # Example project description
    project_description = """
    Build a task management web application with the following features:
    - User registration and authentication with JWT tokens
    - Create, read, update, and delete tasks
    - Real-time notifications when tasks are assigned
    - Export tasks to CSV format
    - Admin dashboard for user management
    """
    
    # Invoke the chain
    result = chain.invoke({"project_description": project_description})
    
    print("Extracted Features:")
    print(f"Total: {result['total_features']}")
    for feature in result['features']:
        print(f"\n- {feature['name']}")
        print(f"  Team: {feature['team']}")
        print(f"  Process: {feature['process']}")
        print(f"  Estimated: {feature['estimated_hours']} hours")
        if feature.get('notes'):
            print(f"  Notes: {feature['notes']}")


def example_estimation(llm: BaseChatModel, retriever: Optional[Any] = None) -> None:
    """Example: Estimate time for a feature.
    
    Args:
        llm: The language model to use
        retriever: Optional retriever for RAG
    """
    from .chains import create_estimation_chain
    
    # Create the chain
    chain = create_estimation_chain(llm, retriever)
    
    # Example feature
    feature_input = {
        "feature_name": "User Authentication",
        "feature_description": "Implement JWT-based authentication with refresh tokens, password reset, and email verification"
    }
    
    # Invoke the chain
    result = chain.invoke(feature_input)
    
    print("Estimation Result:")
    print(f"Feature: {result['feature_name']}")
    print(f"Estimated Hours: {result['estimated_hours']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")


def example_passthrough(llm: BaseChatModel) -> None:
    """Example: Simple RunnablePassthrough usage.
    
    Args:
        llm: The language model to use
    """
    from .chains import create_simple_passthrough_chain
    
    # Create the chain
    chain = create_simple_passthrough_chain(llm)
    
    # Example text
    text = "LangChain Expression Language (LCEL) is a declarative way to compose chains. It uses the pipe operator to connect components."
    
    # Invoke the chain
    result = chain.invoke({"text": text})
    
    print("Original text:")
    print(text)
    print("\nSummary:")
    print(result)


def example_multi_input(llm: BaseChatModel) -> None:
    """Example: Multiple inputs with RunnablePassthrough.
    
    Args:
        llm: The language model to use
    """
    from .chains import create_multi_input_chain
    
    # Create the chain
    chain = create_multi_input_chain(llm)
    
    # Example inputs
    inputs = {
        "feature": "Real-time Chat",
        "team": "fullstack",
        "complexity": "high"
    }
    
    # Invoke the chain
    result = chain.invoke(inputs)
    
    print("Estimation for multi-input:")
    print(f"Feature: {inputs['feature']}")
    print(f"Team: {inputs['team']}")
    print(f"Complexity: {inputs['complexity']}")
    print(f"\nResult: {result}")


if __name__ == "__main__":
    # This would require actual LLM setup
    print("Import this module and call the example functions with your LLM instance.")
    print("\nExample:")
    print("  from langchain_openai import ChatOpenAI")
    print("  from langchain.examples import example_feature_extraction")
    print("  llm = ChatOpenAI(model='gpt-4')")
    print("  example_feature_extraction(llm)")
