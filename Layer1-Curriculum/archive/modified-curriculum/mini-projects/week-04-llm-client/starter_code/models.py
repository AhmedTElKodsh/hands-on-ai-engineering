"""
Data models for LLM client.
Some models are complete (use as reference), some need your implementation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum
from datetime import datetime


# ✅ COMPLETE - Use this as reference
class Provider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"


# ✅ COMPLETE - Use this as reference
class LLMConfig(BaseModel):
    """Configuration for LLM client"""
    providers: List[Provider] = [Provider.OPENAI, Provider.ANTHROPIC]
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    
    @field_validator('providers')
    @classmethod
    def validate_providers(cls, v):
        if not v:
            raise ValueError("Must specify at least one provider")
        return v


# TODO: Complete this model
class LLMRequest(BaseModel):
    """
    Request to LLM.
    
    TODO: Add fields for:
    - prompt (str, required)
    - model (str, optional, default="gpt-4o-mini")
    - temperature (float, optional, default=0.7, must be between 0 and 2)
    - max_tokens (int, optional)
    - system_message (str, optional)
    
    HINT: Use Field() for defaults and validation
    HINT: Add validators for temperature range
    
    Example usage:
        request = LLMRequest(
            prompt="What is 2+2?",
            temperature=0.5
        )
    """
    pass  # TODO: Implement


# TODO: Complete this model
class LLMResponse(BaseModel):
    """
    Response from LLM.
    
    TODO: Add fields for:
    - content (str) - the generated text
    - provider (Provider) - which provider was used
    - model (str) - which model was used
    - tokens_used (int) - total tokens (input + output)
    - input_tokens (int) - input tokens only
    - output_tokens (int) - output tokens only
    - cost (float) - estimated cost in USD
    - latency (float) - response time in seconds
    - timestamp (datetime) - when response was generated
    
    HINT: Use Field(default_factory=datetime.now) for timestamp
    HINT: All fields should be required except timestamp
    
    Example usage:
        response = LLMResponse(
            content="4",
            provider=Provider.OPENAI,
            model="gpt-4o-mini",
            tokens_used=15,
            input_tokens=10,
            output_tokens=5,
            cost=0.000015,
            latency=0.5
        )
    """
    pass  # TODO: Implement


# TODO: Complete this model
class ProviderError(BaseModel):
    """
    Error from a provider attempt.
    
    TODO: Add fields for:
    - provider (Provider) - which provider failed
    - error_type (str) - e.g., "rate_limit", "timeout", "auth_error"
    - error_message (str) - detailed error message
    - timestamp (datetime) - when error occurred
    
    This will be used for logging failed attempts.
    
    Example usage:
        error = ProviderError(
            provider=Provider.OPENAI,
            error_type="rate_limit",
            error_message="Rate limit exceeded. Retry after 60s"
        )
    """
    pass  # TODO: Implement


# ✅ COMPLETE - Cost table for reference
# Update these values as pricing changes
COST_TABLE = {
    Provider.OPENAI: {
        "gpt-4o": {"input": 0.0025, "output": 0.01},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    },
    Provider.ANTHROPIC: {
        "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
        "claude-3-5-haiku-20241022": {"input": 0.001, "output": 0.005},
    },
    Provider.GROQ: {
        "llama-3.1-70b-versatile": {"input": 0.00059, "output": 0.00079},
        "llama-3.1-8b-instant": {"input": 0.00005, "output": 0.00008},
    }
}


# DESIGN QUESTION: Should COST_TABLE be in models.py or a separate config file?
# What are the trade-offs?
