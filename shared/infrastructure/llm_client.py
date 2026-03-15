"""
Simple LLM client for curriculum examples.
Provides basic OpenAI integration without complex multi-provider logic.
"""
from typing import Optional, Dict, Any
from openai import OpenAI
from pydantic import BaseModel


class LLMResponse(BaseModel):
    """Response from LLM."""
    content: str
    model: str
    tokens_used: Optional[int] = None


class SimpleLLMClient:
    """
    Simple LLM client for curriculum examples.
    Uses OpenAI by default.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize client with API key."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Get completion from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional OpenAI parameters
        
        Returns:
            LLMResponse with content and metadata
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            tokens_used=response.usage.total_tokens if response.usage else None
        )
