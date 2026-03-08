"""
Core LLM client implementation.
All functions are TODOs - implement them yourself!
"""
import asyncio
import logging
from typing import Optional, List
from datetime import datetime
import time

from .models import (
    LLMConfig, LLMRequest, LLMResponse, 
    Provider, ProviderError, COST_TABLE
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)


class MultiProviderClient:
    """
    LLM client with automatic fallback.
    
    ARCHITECTURE NOTES:
    - Try providers in order from config
    - On failure, log error and try next provider
    - Track all attempts for debugging
    - Calculate cost based on token usage
    
    DESIGN DECISIONS TO MAKE:
    - How to store provider clients?
    - How to handle provider-specific parameters?
    - When to retry vs when to fallback?
    - How to make this extensible for new providers?
    """
    
    def __init__(self, config: LLMConfig):
        """
        TODO: Initialize the client.
        
        Steps:
        1. Store config
        2. Initialize provider clients (OpenAI, Anthropic, etc.)
        3. Set up logging
        4. Initialize attempt history
        
        HINT: You'll need to import openai, anthropic libraries
        HINT: Store provider clients in a dict: {Provider.OPENAI: client, ...}
        HINT: Only initialize providers that are in config.providers
        
        DESIGN QUESTION: Should you validate API keys here or lazily?
        """
        self.config = config
        self.providers = {}  # TODO: Initialize provider clients
        self.attempt_history: List[ProviderError] = []
        
        # TODO: Initialize each provider client
        # Example structure:
        # if Provider.OPENAI in config.providers:
        #     if not config.openai_api_key:
        #         raise ValueError("OpenAI provider requires api_key")
        #     from openai import AsyncOpenAI
        #     self.providers[Provider.OPENAI] = AsyncOpenAI(api_key=...)
        
        logger.info(f"Initialized MultiProviderClient with providers: {config.providers}")
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """
        TODO: Get completion with automatic fallback.
        
        Steps:
        1. Clear attempt history for this request
        2. Loop through providers in order
        3. Try each provider with _call_provider()
        4. If success, return response
        5. If failure, log error and try next
        6. If all fail, raise exception with all errors
        
        HINT: Use try/except for each provider
        HINT: Track start time for latency calculation
        HINT: Log each attempt (success or failure)
        
        DESIGN QUESTION: Should you try all providers or stop after first success?
        DESIGN QUESTION: What exception should you raise if all fail?
        """
        pass  # TODO: Implement
    
    async def _call_provider(
        self, 
        provider: Provider, 
        request: LLMRequest
    ) -> LLMResponse:
        """
        TODO: Call a specific provider.
        
        Steps:
        1. Get provider client from self.providers
        2. Make API call (different for each provider)
        3. Parse response
        4. Calculate tokens and cost
        5. Return LLMResponse
        
        HINT: Use if/elif to handle different providers
        HINT: Each provider has different API format
        HINT: Wrap in try/except to catch provider-specific errors
        
        DESIGN QUESTION: How do you handle provider-specific parameters?
        DESIGN QUESTION: Should this method handle retries or should complete()?
        """
        start_time = time.time()
        
        # TODO: Implement provider-specific logic
        # if provider == Provider.OPENAI:
        #     return await self._call_openai(request, start_time)
        # elif provider == Provider.ANTHROPIC:
        #     return await self._call_anthropic(request, start_time)
        # ...
        
        raise NotImplementedError(f"Provider {provider} not implemented")
    
    async def _call_openai(self, request: LLMRequest, start_time: float) -> LLMResponse:
        """
        TODO: Call OpenAI API.
        
        Steps:
        1. Get OpenAI client from self.providers
        2. Build messages list (system + user)
        3. Call client.chat.completions.create()
        4. Extract content and usage
        5. Calculate cost using COST_TABLE
        6. Calculate latency
        7. Return LLMResponse
        
        HINT: OpenAI response has .choices[0].message.content
        HINT: Usage is in .usage (prompt_tokens, completion_tokens)
        HINT: Use _calculate_cost() helper
        
        DESIGN QUESTION: How do you handle streaming vs non-streaming?
        """
        pass  # TODO: Implement
    
    async def _call_anthropic(self, request: LLMRequest, start_time: float) -> LLMResponse:
        """
        TODO: Call Anthropic API.
        
        Steps:
        1. Get Anthropic client from self.providers
        2. Build messages (Anthropic format is different!)
        3. Call client.messages.create()
        4. Extract content and usage
        5. Calculate cost
        6. Calculate latency
        7. Return LLMResponse
        
        HINT: Anthropic uses 'messages' not 'chat.completions'
        HINT: System message is a separate parameter
        HINT: Response format is different from OpenAI
        
        DESIGN QUESTION: How do you map request.model to Anthropic models?
        """
        pass  # TODO: Implement
    
    def _calculate_cost(
        self, 
        provider: Provider, 
        model: str, 
        input_tokens: int, 
        output_tokens: int
    ) -> float:
        """
        TODO: Calculate cost in USD.
        
        Steps:
        1. Look up rates in COST_TABLE for this provider and model
        2. If model not found, log warning and return 0.0
        3. Calculate: (input_tokens * input_rate + output_tokens * output_rate) / 1000
        4. Return cost rounded to 6 decimal places
        
        HINT: COST_TABLE is imported from models.py
        HINT: Rates are per 1K tokens
        
        DESIGN QUESTION: What should you do if model is not in COST_TABLE?
        DESIGN QUESTION: Should you use a default rate or return 0?
        """
        pass  # TODO: Implement
    
    async def _retry_with_backoff(
        self, 
        func,
        max_retries: int = 3
    ):
        """
        TODO: Retry with exponential backoff.
        
        Steps:
        1. Loop up to max_retries
        2. Try func()
        3. If success, return result
        4. If rate limit error, wait and retry (2^attempt seconds)
        5. If other error, raise immediately
        
        HINT: Use asyncio.sleep() for waiting
        HINT: Catch specific exceptions (RateLimitError, etc.)
        HINT: Wait time: 2^attempt (1s, 2s, 4s, 8s...)
        
        DESIGN QUESTION: Which errors should retry? Which should fail fast?
        DESIGN QUESTION: Should max wait time be capped?
        """
        pass  # TODO: Implement
    
    def get_attempt_history(self) -> List[ProviderError]:
        """
        Get history of failed attempts.
        Useful for debugging and monitoring.
        """
        return self.attempt_history
    
    def clear_attempt_history(self):
        """Clear the attempt history."""
        self.attempt_history = []


# DESIGN QUESTIONS TO CONSIDER:
# 1. Should this be a class or a set of functions?
# 2. How would you add a new provider?
# 3. How would you make this thread-safe?
# 4. How would you add caching?
# 5. How would you add metrics/monitoring?
