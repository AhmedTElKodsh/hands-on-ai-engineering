"""
OpenAI LLM Provider Implementation.
"""

import asyncio
from typing import Optional, AsyncGenerator

from app.services.llm.provider import (
    LLMProvider,
    LLMConfig,
    LLMResponse,
    LLMStreamChunk,
    RateLimitError,
    TimeoutError,
    InvalidRequestError,
    AuthenticationError,
    ProviderError,
)


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config: LLMConfig, api_key: str):
        super().__init__(config)
        self.api_key = api_key
        
        # Lazy import to avoid dependency if not using OpenAI
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        
        # Update cost based on model
        self._update_pricing()
    
    def _update_pricing(self):
        """Update pricing based on model."""
        # OpenAI pricing (approximate, update as needed)
        pricing = {
            "gpt-3.5-turbo": (0.0005, 0.0015),
            "gpt-4": (0.03, 0.06),
            "gpt-4-turbo": (0.01, 0.03),
            "gpt-4o": (0.005, 0.015),
        }
        
        if self.config.model in pricing:
            input_cost, output_cost = pricing[self.config.model]
            self.config.cost_per_1k_input = input_cost
            self.config.cost_per_1k_output = output_cost
    
    def calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost for token usage."""
        input_cost = (tokens_in / 1000) * self.config.cost_per_1k_input
        output_cost = (tokens_out / 1000) * self.config.cost_per_1k_output
        return round(input_cost + output_cost, 6)
    
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """Get a completion from OpenAI."""
        import openai
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        retries = 0
        last_error = None
        
        while retries < self.config.max_retries:
            try:
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=self.config.model,
                        messages=messages,
                        max_tokens=self.config.max_tokens,
                        temperature=self.config.temperature,
                    ),
                    timeout=self.config.timeout,
                )
                
                content = response.choices[0].message.content or ""
                tokens_in = response.usage.prompt_tokens if response.usage else 0
                tokens_out = response.usage.completion_tokens if response.usage else 0
                
                return LLMResponse(
                    content=content,
                    model=self.config.model,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    cost_usd=self.calculate_cost(tokens_in, tokens_out),
                    finish_reason=response.choices[0].finish_reason,
                )
                
            except asyncio.TimeoutError as e:
                last_error = TimeoutError(f"Request timed out after {self.config.timeout}s", provider="openai")
                retries += 1
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                
            except openai.RateLimitError as e:
                raise RateLimitError(f"OpenAI rate limit exceeded: {e}", provider="openai")
                
            except openai.AuthenticationError as e:
                raise AuthenticationError(f"OpenAI authentication failed: {e}", provider="openai")
                
            except openai.BadRequestError as e:
                raise InvalidRequestError(f"Invalid request to OpenAI: {e}", provider="openai")
                
            except openai.APIError as e:
                last_error = ProviderError(f"OpenAI API error: {e}", provider="openai")
                retries += 1
                await asyncio.sleep(2 ** retries)
        
        # All retries exhausted
        raise last_error or ProviderError("OpenAI request failed after all retries", provider="openai")
    
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream a completion from OpenAI."""
        import openai
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
            )
            
            async for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                finish_reason = chunk.choices[0].finish_reason
                
                yield LLMStreamChunk(
                    content=delta,
                    is_final=finish_reason is not None,
                    finish_reason=finish_reason,
                )
                
        except asyncio.TimeoutError:
            raise TimeoutError(f"Stream request timed out after {self.config.timeout}s", provider="openai")
        except openai.RateLimitError:
            raise RateLimitError("OpenAI rate limit exceeded", provider="openai")
        except openai.AuthenticationError:
            raise AuthenticationError("OpenAI authentication failed", provider="openai")
