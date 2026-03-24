"""
LLM Client Factory and Manager.

Provides a unified interface for creating and using LLM providers.
"""

from typing import Optional
from functools import lru_cache

from app.core.config import get_settings
from app.services.llm.provider import LLMProvider, LLMConfig, ProviderType
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.anthropic_provider import AnthropicProvider


settings = get_settings()


def create_llm_client(
    provider: Optional[ProviderType] = None,
    model: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    timeout: int = 30,
    max_retries: int = 3,
) -> LLMProvider:
    """
    Create an LLM client for the specified provider.
    
    Args:
        provider: LLM provider (openai, anthropic, ollama, groq)
        model: Model name
        max_tokens: Maximum tokens in response
        temperature: Response temperature (0-1)
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts
        
    Returns:
        LLMProvider instance
        
    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    provider = provider or settings.llm_provider
    config = LLMConfig(
        provider=provider,
        model=model or "gpt-3.5-turbo",
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
        max_retries=max_retries,
    )
    
    if provider == "openai":
        api_key = settings.openai_api_key
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        if not model:
            config.model = "gpt-3.5-turbo"
        
        return OpenAIProvider(config=config, api_key=api_key)
    
    elif provider == "anthropic":
        api_key = settings.anthropic_api_key
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        
        if not model:
            config.model = "claude-3-haiku-20240307"
        
        return AnthropicProvider(config=config, api_key=api_key)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported: openai, anthropic")


@lru_cache
def get_default_llm_client() -> LLMProvider:
    """
    Get default LLM client based on settings.
    
    Returns:
        LLMProvider instance
    """
    return create_llm_client()
