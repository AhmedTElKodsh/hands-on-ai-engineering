"""RunnablePassthrough patterns and examples.

This module demonstrates various ways to use RunnablePassthrough for
data flow in LCEL chains. RunnablePassthrough is a key component that
allows you to preserve input data while transforming specific fields.
"""

from typing import Dict, Any, List
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel


# Pattern 1: Simple Passthrough
def pattern_simple_passthrough(llm: BaseChatModel) -> Any:
    """Pattern 1: Pass entire input through unchanged.
    
    RunnablePassthrough() with no modifications passes the entire
    input dict to the next component.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that preserves input structure
        
    Example:
        >>> chain = pattern_simple_passthrough(llm)
        >>> result = chain.invoke({"text": "Hello"})
        # Input {"text": "Hello"} is passed to prompt as-is
    """
    prompt = PromptTemplate.from_template("Echo: {text}")
    
    chain = (
        RunnablePassthrough()  # Pass entire input through
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 2: Field Extraction
def pattern_field_extraction(llm: BaseChatModel) -> Any:
    """Pattern 2: Extract specific fields from input.
    
    Use RunnablePassthrough with lambda to extract specific fields
    from the input dict.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that extracts specific fields
        
    Example:
        >>> chain = pattern_field_extraction(llm)
        >>> result = chain.invoke({
        ...     "user_input": "Estimate this feature",
        ...     "metadata": {"team": "backend"}
        ... })
        # Only "user_input" is passed to prompt
    """
    prompt = PromptTemplate.from_template("Process: {input}")
    
    chain = (
        {"input": RunnablePassthrough() | (lambda x: x["user_input"])}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 3: Multiple Field Extraction
def pattern_multiple_fields(llm: BaseChatModel) -> Any:
    """Pattern 3: Extract multiple fields independently.
    
    Create a dict where each key extracts a different field from
    the input using RunnablePassthrough.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that extracts multiple fields
        
    Example:
        >>> chain = pattern_multiple_fields(llm)
        >>> result = chain.invoke({
        ...     "feature": "User Auth",
        ...     "team": "backend",
        ...     "priority": "high"
        ... })
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an estimator."),
        ("human", "Feature: {feature}\nTeam: {team}\nPriority: {priority}")
    ])
    
    chain = (
        {
            "feature": RunnablePassthrough() | (lambda x: x["feature"]),
            "team": RunnablePassthrough() | (lambda x: x["team"]),
            "priority": RunnablePassthrough() | (lambda x: x["priority"])
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 4: Nested Field Access
def pattern_nested_fields(llm: BaseChatModel) -> Any:
    """Pattern 4: Access nested fields in input.
    
    Use lambda functions to navigate nested dict structures.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that accesses nested fields
        
    Example:
        >>> chain = pattern_nested_fields(llm)
        >>> result = chain.invoke({
        ...     "project": {
        ...         "name": "AITEA",
        ...         "features": ["auth", "api"]
        ...     }
        ... })
    """
    prompt = PromptTemplate.from_template(
        "Project: {project_name}\nFeatures: {features}"
    )
    
    chain = (
        {
            "project_name": RunnablePassthrough() | (lambda x: x["project"]["name"]),
            "features": RunnablePassthrough() | (lambda x: ", ".join(x["project"]["features"]))
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 5: Conditional Field Access
def pattern_conditional_access(llm: BaseChatModel) -> Any:
    """Pattern 5: Conditionally access fields with defaults.
    
    Use .get() to safely access fields that might not exist.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain with safe field access
        
    Example:
        >>> chain = pattern_conditional_access(llm)
        >>> result = chain.invoke({"feature": "Auth"})
        # "notes" field is optional
    """
    prompt = PromptTemplate.from_template(
        "Feature: {feature}\nNotes: {notes}"
    )
    
    chain = (
        {
            "feature": RunnablePassthrough() | (lambda x: x["feature"]),
            "notes": RunnablePassthrough() | (lambda x: x.get("notes", "No notes provided"))
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 6: Field Transformation
def pattern_field_transformation(llm: BaseChatModel) -> Any:
    """Pattern 6: Transform fields before passing to prompt.
    
    Apply transformations to fields using lambda functions.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that transforms fields
        
    Example:
        >>> chain = pattern_field_transformation(llm)
        >>> result = chain.invoke({
        ...     "hours": 8.5,
        ...     "team_size": 3
        ... })
    """
    prompt = PromptTemplate.from_template(
        "Total effort: {total_hours} hours\nPer person: {per_person} hours"
    )
    
    chain = (
        {
            "total_hours": RunnablePassthrough() | (lambda x: x["hours"]),
            "per_person": RunnablePassthrough() | (lambda x: round(x["hours"] / x["team_size"], 2))
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 7: Preserving Original Input
def pattern_preserve_input(llm: BaseChatModel) -> Any:
    """Pattern 7: Preserve original input alongside processed output.
    
    Use RunnablePassthrough to keep original input available
    throughout the chain.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that preserves original input
        
    Example:
        >>> chain = pattern_preserve_input(llm)
        >>> result = chain.invoke({"query": "Estimate feature X"})
        # Original input is preserved in the output
    """
    prompt = PromptTemplate.from_template("Query: {query}")
    
    # This pattern preserves the original input
    def add_llm_response(x: Dict[str, Any]) -> Dict[str, Any]:
        """Add LLM response to original input."""
        return {
            **x,  # Preserve original input
            "llm_response": x.get("llm_output", "")
        }
    
    chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"query": x["query"], "original": x})
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 8: Parallel Processing
def pattern_parallel_processing(llm: BaseChatModel) -> Any:
    """Pattern 8: Process multiple fields in parallel.
    
    Use dict with multiple RunnablePassthrough instances to
    process different aspects of input simultaneously.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain with parallel field processing
        
    Example:
        >>> chain = pattern_parallel_processing(llm)
        >>> result = chain.invoke({
        ...     "feature": "API",
        ...     "complexity": "high"
        ... })
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze: {analysis_type}"),
        ("human", "{content}")
    ])
    
    # Multiple passthroughs can work in parallel
    chain = (
        {
            "analysis_type": RunnablePassthrough() | (lambda x: "feature estimation"),
            "content": RunnablePassthrough() | (lambda x: f"Feature: {x['feature']}, Complexity: {x['complexity']}")
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 9: List Processing
def pattern_list_processing(llm: BaseChatModel) -> Any:
    """Pattern 9: Process list fields.
    
    Handle list inputs and transform them for prompts.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain that processes lists
        
    Example:
        >>> chain = pattern_list_processing(llm)
        >>> result = chain.invoke({
        ...     "features": ["Auth", "API", "UI"]
        ... })
    """
    prompt = PromptTemplate.from_template(
        "Features to estimate:\n{feature_list}\n\nTotal count: {count}"
    )
    
    chain = (
        {
            "feature_list": RunnablePassthrough() | (lambda x: "\n".join(f"- {f}" for f in x["features"])),
            "count": RunnablePassthrough() | (lambda x: len(x["features"]))
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Pattern 10: Chained Transformations
def pattern_chained_transformations(llm: BaseChatModel) -> Any:
    """Pattern 10: Chain multiple transformations.
    
    Apply multiple transformations in sequence using pipe operator.
    
    Args:
        llm: Language model to use
        
    Returns:
        Chain with chained transformations
        
    Example:
        >>> chain = pattern_chained_transformations(llm)
        >>> result = chain.invoke({"text": "  HELLO WORLD  "})
    """
    prompt = PromptTemplate.from_template("Processed: {text}")
    
    # Chain multiple transformations
    chain = (
        {
            "text": (
                RunnablePassthrough()
                | (lambda x: x["text"])
                | (lambda text: text.strip())
                | (lambda text: text.lower())
                | (lambda text: text.title())
            )
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def demonstrate_all_patterns(llm: BaseChatModel) -> None:
    """Demonstrate all RunnablePassthrough patterns.
    
    Args:
        llm: Language model to use
    """
    print("=== RunnablePassthrough Patterns ===\n")
    
    patterns = [
        ("Simple Passthrough", pattern_simple_passthrough, {"text": "Hello"}),
        ("Field Extraction", pattern_field_extraction, {"user_input": "Test", "metadata": {}}),
        ("Multiple Fields", pattern_multiple_fields, {"feature": "Auth", "team": "backend", "priority": "high"}),
        ("Nested Fields", pattern_nested_fields, {"project": {"name": "AITEA", "features": ["auth", "api"]}}),
        ("Conditional Access", pattern_conditional_access, {"feature": "Auth"}),
        ("Field Transformation", pattern_field_transformation, {"hours": 8.5, "team_size": 3}),
        ("List Processing", pattern_list_processing, {"features": ["Auth", "API", "UI"]}),
    ]
    
    for name, pattern_func, test_input in patterns:
        print(f"\n--- {name} ---")
        try:
            chain = pattern_func(llm)
            result = chain.invoke(test_input)
            print(f"Input: {test_input}")
            print(f"Output: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Import this module to use RunnablePassthrough patterns.")
    print("\nAvailable patterns:")
    print("1. pattern_simple_passthrough")
    print("2. pattern_field_extraction")
    print("3. pattern_multiple_fields")
    print("4. pattern_nested_fields")
    print("5. pattern_conditional_access")
    print("6. pattern_field_transformation")
    print("7. pattern_preserve_input")
    print("8. pattern_parallel_processing")
    print("9. pattern_list_processing")
    print("10. pattern_chained_transformations")
