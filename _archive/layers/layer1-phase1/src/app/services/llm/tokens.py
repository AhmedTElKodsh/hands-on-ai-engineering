"""
Token counting utilities for cost tracking.
"""

from typing import Optional


def count_tokens_openai(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count tokens using tiktoken (OpenAI's tokenizer).
    
    Args:
        text: Text to tokenize
        model: Model name for encoding
        
    Returns:
        Number of tokens
    """
    try:
        import tiktoken
        
        encoder = tiktoken.encoding_for_model(model)
        tokens = encoder.encode(text)
        return len(tokens)
    except ImportError:
        # Fallback: rough estimate (4 chars per token)
        return len(text) // 4
    except Exception:
        # Fallback for unknown models
        return len(text) // 4


def estimate_cost(
    tokens_in: int,
    tokens_out: int,
    provider: str = "openai",
    model: str = "gpt-3.5-turbo",
) -> float:
    """
    Estimate cost for token usage.
    
    Args:
        tokens_in: Input tokens
        tokens_out: Output tokens
        provider: Provider name
        model: Model name
        
    Returns:
        Estimated cost in USD
    """
    # Pricing per 1K tokens (approximate, update as needed)
    pricing = {
        "openai": {
            "gpt-3.5-turbo": (0.0005, 0.0015),
            "gpt-4": (0.03, 0.06),
            "gpt-4-turbo": (0.01, 0.03),
            "gpt-4o": (0.005, 0.015),
        },
        "anthropic": {
            "claude-3-haiku-20240307": (0.00025, 0.00125),
            "claude-3-sonnet-20240229": (0.003, 0.015),
            "claude-3-opus-20240229": (0.015, 0.075),
        },
    }
    
    try:
        input_cost, output_cost = pricing.get(provider, {}).get(model, (0.0005, 0.0015))
    except (KeyError, TypeError):
        input_cost, output_cost = 0.0005, 0.0015
    
    total_cost = (tokens_in / 1000) * input_cost + (tokens_out / 1000) * output_cost
    return round(total_cost, 6)
