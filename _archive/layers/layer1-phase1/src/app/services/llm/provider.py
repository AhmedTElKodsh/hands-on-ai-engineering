"""
LLM Provider Interface and Error Types.

Defines the abstract interface for LLM providers and common error types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, AsyncGenerator, Literal


# Error Types
class LLMError(Exception):
    """Base exception for LLM errors."""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        self.message = message
        self.provider = provider
        super().__init__(self.message)


class RateLimitError(LLMError):
    """Raised when API rate limit is exceeded."""
    
    pass


class TimeoutError(LLMError):
    """Raised when request times out."""
    
    pass


class InvalidRequestError(LLMError):
    """Raised when request is invalid (bad prompt, invalid parameters)."""
    
    pass


class AuthenticationError(LLMError):
    """Raised when authentication fails."""
    
    pass


class ProviderError(LLMError):
    """Raised when provider has an internal error."""
    
    pass


# Response Types
@dataclass
class LLMResponse:
    """Standardized LLM response."""
    
    content: str
    model: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    finish_reason: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class LLMStreamChunk:
    """Streaming response chunk."""
    
    content: str
    is_final: bool = False
    finish_reason: Optional[str] = None


# Provider Types
ProviderType = Literal["openai", "anthropic", "ollama", "groq"]


@dataclass
class LLMConfig:
    """LLM configuration."""
    
    provider: ProviderType = "openai"
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1024
    temperature: float = 0.7
    timeout: int = 30
    max_retries: int = 3
    
    # Cost tracking
    cost_per_1k_input: float = 0.0005
    cost_per_1k_output: float = 0.0015


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def complete(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Get a completion from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLMResponse with completion
        """
        pass
    
    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        """
        Stream a completion from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Yields:
            LLMStreamChunk with completion chunks
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """
        Calculate cost for token usage.
        
        Args:
            tokens_in: Number of input tokens
            tokens_out: Number of output tokens
            
        Returns:
            Cost in USD
        """
        pass
