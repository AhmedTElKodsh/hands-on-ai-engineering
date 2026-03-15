"""
Anthropic LLM Provider Implementation.
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


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider implementation."""
    
    def __init__(self, config: LLMConfig, api_key: str):
        super().__init__(config)
        self.api_key = api_key
        
        # Lazy import
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        
        self._update_pricing()
    
    def _update_pricing(self):
        """Update pricing based on model."""
        # Anthropic pricing (approximate)
        pricing = {
            "claude-3-haiku-20240307": (0.00025, 0.00125),
            "claude-3-sonnet-20240229": (0.003, 0.015),
            "claude-3-opus-20240229": (0.015, 0.075),
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
        """Get a completion from Anthropic."""
        import anthropic
        
        retries = 0
        last_error = None
        
        while retries < self.config.max_retries:
            try:
                response = await asyncio.wait_for(
                    self.client.messages.create(
                        model=self.config.model,
                        max_tokens=self.config.max_tokens,
                        system=system_prompt or anthropic.NOT_GIVEN,
                        messages=[{"role": "user", "content": prompt}],
                    ),
                    timeout=self.config.timeout,
                )
                
                content = response.content[0].text if response.content else ""
                tokens_in = response.usage.input_tokens if response.usage else 0
                tokens_out = response.usage.output_tokens if response.usage else 0
                
                return LLMResponse(
                    content=content,
                    model=self.config.model,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    cost_usd=self.calculate_cost(tokens_in, tokens_out),
                    finish_reason=response.stop_reason,
                )
                
            except asyncio.TimeoutError as e:
                last_error = TimeoutError(f"Request timed out after {self.config.timeout}s", provider="anthropic")
                retries += 1
                await asyncio.sleep(2 ** retries)
                
            except anthropic.RateLimitError as e:
                raise RateLimitError(f"Anthropic rate limit exceeded: {e}", provider="anthropic")
                
            except anthropic.AuthenticationError as e:
                raise AuthenticationError(f"Anthropic authentication failed: {e}", provider="anthropic")
                
            except anthropic.BadRequestError as e:
                raise InvalidRequestError(f"Invalid request to Anthropic: {e}", provider="anthropic")
                
            except anthropic.APIError as e:
                last_error = ProviderError(f"Anthropic API error: {e}", provider="anthropic")
                retries += 1
                await asyncio.sleep(2 ** retries)
        
        raise last_error or ProviderError("Anthropic request failed after all retries", provider="anthropic")
    
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream a completion from Anthropic."""
        import anthropic
        
        try:
            async with self.client.messages.stream(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=system_prompt or anthropic.NOT_GIVEN,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                async for text in stream.text_stream:
                    yield LLMStreamChunk(
                        content=text,
                        is_final=False,
                    )
                
                # Final chunk
                response = await stream.get_final_message()
                yield LLMStreamChunk(
                    content="",
                    is_final=True,
                    finish_reason=response.stop_reason,
                )
                
        except asyncio.TimeoutError:
            raise TimeoutError(f"Stream request timed out after {self.config.timeout}s", provider="anthropic")
        except anthropic.RateLimitError:
            raise RateLimitError("Anthropic rate limit exceeded", provider="anthropic")
        except anthropic.AuthenticationError:
            raise AuthenticationError("Anthropic authentication failed", provider="anthropic")
