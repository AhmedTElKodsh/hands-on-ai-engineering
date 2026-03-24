# Project Templates & Starter Code

**Philosophy:** Provide structure, not solutions. Students implement core logic.

---

## Template Structure

Each project follows this structure:
```
project-name/
├── README.md                 # Problem statement, requirements, learning goals
├── ARCHITECTURE.md           # System design (student fills this in)
├── starter_code/            # Scaffolding with TODOs
│   ├── models.py            # Pydantic models (partially complete)
│   ├── core.py              # Core logic (TODOs only)
│   └── utils.py             # Helper functions (some provided)
├── tests/                   # Test templates (student completes)
│   ├── test_core.py
│   └── test_integration.py
├── examples/                # Example inputs/outputs
│   ├── sample_input.txt
│   └── expected_output.json
├── hints/                   # Progressive hints (read only if stuck)
│   ├── hint_01_architecture.md
│   ├── hint_02_implementation.md
│   └── hint_03_debugging.md
└── solution_guide/          # NOT full solution, just design patterns
    └── design_patterns.md
```

---

## Mini-Project Template: Structured LLM Client

### README.md
```markdown
# Mini-Project 1: Multi-Provider LLM Client

## Problem Statement
Build a production-grade LLM client that:
- Supports multiple providers (OpenAI, Anthropic, Groq)
- Implements automatic fallback on failure
- Tracks token usage and cost
- Handles rate limits and retries
- Logs all requests for debugging

## Learning Goals
- API design and error handling
- Async programming patterns
- Cost tracking and observability
- Testing external APIs

## Requirements
- [ ] Support 3+ providers with priority order
- [ ] Automatic fallback if primary fails
- [ ] Track tokens and cost per request
- [ ] Retry with exponential backoff
- [ ] Structured logging (JSON format)
- [ ] Unit tests with mocked APIs
- [ ] Integration test with real API

## Success Criteria
- All tests pass
- Can explain fallback logic
- Can calculate cost accurately
- Logs are readable and useful

## Time Estimate
- Design: 1 hour
- Implementation: 4-6 hours
- Testing: 2-3 hours
- Documentation: 1 hour

## Getting Started
1. Read ARCHITECTURE.md and sketch your design
2. Fill in TODOs in starter_code/
3. Run tests: `pytest tests/`
4. Check hints/ if stuck (but try first!)
```

### starter_code/models.py
```python
"""
Data models for LLM client.
Some models are complete, some need your implementation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
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
    
    @validator('providers')
    def validate_providers(cls, v):
        if not v:
            raise ValueError("Must specify at least one provider")
        return v

# TODO: Complete this model
class LLMRequest(BaseModel):
    """
    Request to LLM.
    
    TODO: Add fields for:
    - prompt (str)
    - model (str, optional)
    - temperature (float, default 0.7)
    - max_tokens (int, optional)
    - system_message (str, optional)
    
    HINT: Use Field() for defaults and validation
    """
    pass

# TODO: Complete this model
class LLMResponse(BaseModel):
    """
    Response from LLM.
    
    TODO: Add fields for:
    - content (str) - the generated text
    - provider (Provider) - which provider was used
    - model (str) - which model was used
    - tokens_used (int) - total tokens
    - cost (float) - estimated cost in USD
    - latency (float) - response time in seconds
    - timestamp (datetime)
    
    HINT: Use Field(default_factory=...) for timestamp
    """
    pass

# TODO: Complete this model
class ProviderError(BaseModel):
    """
    Error from a provider attempt.
    
    TODO: Add fields for:
    - provider (Provider)
    - error_type (str) - e.g., "rate_limit", "timeout", "auth_error"
    - error_message (str)
    - timestamp (datetime)
    
    This will be used for logging failed attempts.
    """
    pass
```

### starter_code/core.py
```python
"""
Core LLM client implementation.
All functions are TODOs - implement them yourself!
"""
import asyncio
import logging
from typing import Optional, List
from .models import (
    LLMConfig, LLMRequest, LLMResponse, 
    Provider, ProviderError
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
    """
    
    def __init__(self, config: LLMConfig):
        """
        TODO: Initialize the client.
        
        Steps:
        1. Store config
        2. Initialize provider clients (OpenAI, Anthropic, etc.)
        3. Set up logging
        
        HINT: You'll need to import openai, anthropic libraries
        HINT: Store provider clients in a dict: {Provider.OPENAI: client, ...}
        """
        self.config = config
        self.providers = {}  # TODO: Initialize provider clients
        self.attempt_history: List[ProviderError] = []
        
        # TODO: Initialize each provider client
        # Example structure:
        # if Provider.OPENAI in config.providers:
        #     self.providers[Provider.OPENAI] = OpenAI(api_key=...)
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """
        TODO: Get completion with automatic fallback.
        
        Steps:
        1. Loop through providers in order
        2. Try each provider with _call_provider()
        3. If success, return response
        4. If failure, log error and try next
        5. If all fail, raise exception
        
        HINT: Use try/except for each provider
        HINT: Track start time for latency calculation
        
        DESIGN QUESTION: Should you try all providers or stop after first success?
        """
        pass
    
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
        
        DESIGN QUESTION: How do you handle provider-specific parameters?
        """
        pass
    
    async def _call_openai(self, request: LLMRequest) -> LLMResponse:
        """
        TODO: Call OpenAI API.
        
        Steps:
        1. Build messages list (system + user)
        2. Call client.chat.completions.create()
        3. Extract content and usage
        4. Calculate cost (see COST_TABLE below)
        5. Return LLMResponse
        
        COST_TABLE (as of 2024, update as needed):
        - gpt-4: $0.03/1K input, $0.06/1K output
        - gpt-3.5-turbo: $0.0015/1K input, $0.002/1K output
        """
        pass
    
    async def _call_anthropic(self, request: LLMRequest) -> LLMResponse:
        """
        TODO: Call Anthropic API.
        
        Steps:
        1. Build messages (Anthropic format is different!)
        2. Call client.messages.create()
        3. Extract content and usage
        4. Calculate cost
        5. Return LLMResponse
        
        HINT: Anthropic uses 'messages' not 'chat.completions'
        """
        pass
    
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
        1. Define cost table (dict of model -> rates)
        2. Look up rates for this model
        3. Calculate: (input_tokens * input_rate + output_tokens * output_rate) / 1000
        4. Return cost
        
        HINT: Use a nested dict: {Provider.OPENAI: {"gpt-4": {"input": 0.03, ...}}}
        
        DESIGN QUESTION: Where should cost table live? Config? Constants file?
        """
        pass
    
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
        
        DESIGN QUESTION: Which errors should retry? Which should fail fast?
        """
        pass
```

### tests/test_core.py
```python
"""
Tests for LLM client.
Some tests are complete, some need your implementation.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from starter_code.core import MultiProviderClient
from starter_code.models import LLMConfig, LLMRequest, Provider

# ✅ COMPLETE - Use this as reference
@pytest.fixture
def mock_config():
    """Test configuration with mocked API keys"""
    return LLMConfig(
        providers=[Provider.OPENAI, Provider.ANTHROPIC],
        openai_api_key="test-key-openai",
        anthropic_api_key="test-key-anthropic",
        timeout=10,
        max_retries=2
    )

# ✅ COMPLETE - Use this as reference
@pytest.fixture
def sample_request():
    """Sample LLM request"""
    return LLMRequest(
        prompt="What is 2+2?",
        temperature=0.7,
        max_tokens=100
    )

# TODO: Complete this test
@pytest.mark.asyncio
async def test_successful_completion(mock_config, sample_request):
    """
    Test successful completion with primary provider.
    
    TODO:
    1. Create client with mock_config
    2. Mock the OpenAI API call to return success
    3. Call client.complete(sample_request)
    4. Assert response is correct
    5. Assert provider is OPENAI
    6. Assert cost is calculated
    
    HINT: Use @patch to mock OpenAI client
    HINT: Mock response should match OpenAI's response format
    """
    pass

# TODO: Complete this test
@pytest.mark.asyncio
async def test_fallback_on_failure(mock_config, sample_request):
    """
    Test fallback to secondary provider when primary fails.
    
    TODO:
    1. Create client
    2. Mock OpenAI to raise exception
    3. Mock Anthropic to return success
    4. Call client.complete()
    5. Assert response provider is ANTHROPIC
    6. Assert attempt_history has OpenAI error logged
    
    DESIGN QUESTION: What exceptions should trigger fallback?
    """
    pass

# TODO: Complete this test
@pytest.mark.asyncio
async def test_all_providers_fail(mock_config, sample_request):
    """
    Test behavior when all providers fail.
    
    TODO:
    1. Create client
    2. Mock all providers to fail
    3. Call client.complete()
    4. Assert it raises appropriate exception
    5. Assert all failures are logged
    
    DESIGN QUESTION: What exception should be raised?
    """
    pass

# TODO: Write this test
@pytest.mark.asyncio
async def test_cost_calculation(mock_config):
    """
    Test cost calculation for different models.
    
    TODO:
    1. Create client
    2. Test cost calculation for GPT-4 (known token counts)
    3. Test cost calculation for GPT-3.5
    4. Assert costs match expected values
    
    HINT: Use client._calculate_cost() directly
    """
    pass

# TODO: Write this test
@pytest.mark.asyncio
async def test_retry_on_rate_limit(mock_config, sample_request):
    """
    Test retry logic for rate limit errors.
    
    TODO:
    1. Create client
    2. Mock provider to fail with rate limit first 2 times, succeed on 3rd
    3. Call client.complete()
    4. Assert it eventually succeeds
    5. Assert retry count is correct
    
    HINT: Use side_effect=[error, error, success] in mock
    """
    pass
```

### hints/hint_01_architecture.md
```markdown
# Hint 1: Architecture Design

## Before you code, answer these questions:

### 1. Provider Priority
- How do you store the provider order?
- How do you iterate through providers?
- When do you stop trying providers?

**Suggested approach:** Use a list of providers from config. Loop through with for loop. Break on first success.

### 2. Error Handling
- What errors can happen? (rate limit, timeout, auth error, invalid response)
- Which errors should retry? (rate limit, timeout)
- Which errors should fallback? (all of them)
- Which errors should fail immediately? (invalid config)

**Suggested approach:** Create error hierarchy. Catch specific exceptions. Log all attempts.

### 3. Cost Tracking
- Where do you get token counts? (from API response)
- Where do you get pricing? (hardcoded table or config)
- How do you handle unknown models? (default rate or error?)

**Suggested approach:** Hardcode pricing table as constant. Update periodically.

### 4. Testing Strategy
- How do you test without real API calls? (mocking)
- What scenarios to test? (success, fallback, all fail, retry)
- How do you verify cost calculation? (known inputs/outputs)

**Suggested approach:** Use unittest.mock. Test each scenario separately.

## Draw this before coding:
```
[User Request]
      ↓
[Try Provider 1] → Success? → [Return Response]
      ↓ Fail
[Log Error]
      ↓
[Try Provider 2] → Success? → [Return Response]
      ↓ Fail
[Log Error]
      ↓
[Raise Exception]
```
```

### hints/hint_02_implementation.md
```markdown
# Hint 2: Implementation Tips

## If you're stuck on provider initialization:
```python
# Pattern for initializing providers
if Provider.OPENAI in self.config.providers:
    if not self.config.openai_api_key:
        raise ValueError("OpenAI provider requires api_key")
    from openai import AsyncOpenAI
    self.providers[Provider.OPENAI] = AsyncOpenAI(
        api_key=self.config.openai_api_key,
        timeout=self.config.timeout
    )
```

## If you're stuck on the fallback loop:
```python
# Pattern for trying providers in order
for provider in self.config.providers:
    try:
        response = await self._call_provider(provider, request)
        return response  # Success! Return immediately
    except Exception as e:
        # Log the error
        error = ProviderError(
            provider=provider,
            error_type=type(e).__name__,
            error_message=str(e),
            timestamp=datetime.now()
        )
        self.attempt_history.append(error)
        logger.warning(f"Provider {provider} failed: {e}")
        # Continue to next provider

# If we get here, all providers failed
raise Exception("All providers failed")
```

## If you're stuck on cost calculation:
```python
# Pattern for cost table
COST_TABLE = {
    Provider.OPENAI: {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    },
    Provider.ANTHROPIC: {
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    }
}

def _calculate_cost(self, provider, model, input_tokens, output_tokens):
    rates = COST_TABLE.get(provider, {}).get(model)
    if not rates:
        logger.warning(f"Unknown model {model}, using default rate")
        return 0.0  # or use default rate
    
    cost = (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1000
    return round(cost, 6)
```

## If you're stuck on testing:
```python
# Pattern for mocking OpenAI
@patch('starter_code.core.AsyncOpenAI')
async def test_example(mock_openai_class, mock_config):
    # Create mock response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="4"))]
    mock_response.usage = Mock(prompt_tokens=10, completion_tokens=5)
    
    # Make the mock client return this response
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    # Now test your client
    client = MultiProviderClient(mock_config)
    response = await client.complete(sample_request)
    
    assert response.content == "4"
    assert response.tokens_used == 15
```
```

### solution_guide/design_patterns.md
```markdown
# Design Patterns (NOT full solution)

## Pattern 1: Strategy Pattern for Providers
Each provider is a strategy. Client delegates to the right strategy.

```
Client → [Provider Interface] ← OpenAI Provider
                              ← Anthropic Provider
                              ← Groq Provider
```

## Pattern 2: Chain of Responsibility for Fallback
Each provider tries to handle the request. If it fails, passes to next.

```
Request → Provider1 → Provider2 → Provider3 → Exception
            ↓ success
          Response
```

## Pattern 3: Retry with Exponential Backoff
For transient failures (rate limits), wait progressively longer.

```
Attempt 1 → Fail → Wait 1s
Attempt 2 → Fail → Wait 2s
Attempt 3 → Fail → Wait 4s
Attempt 4 → Success
```

## Pattern 4: Observer Pattern for Logging
Log every attempt for debugging and cost tracking.

```
[Client] → [Logger] → [File/Console]
         → [Metrics] → [Dashboard]
```

## Key Design Decisions:

### 1. Sync vs Async?
**Recommendation:** Async. LLM calls are I/O bound. Async allows concurrent requests.

### 2. Retry vs Fallback?
**Recommendation:** Both. Retry for transient errors (rate limit). Fallback for persistent errors (auth).

### 3. Where to store cost table?
**Recommendation:** Constants file or config. Update periodically. Don't hardcode in functions.

### 4. How to handle unknown models?
**Recommendation:** Log warning, use default rate or return 0. Don't crash.

### 5. Should you cache responses?
**Recommendation:** Not in this project. Add in advanced version with semantic caching.
```

---

## How to Use These Templates

### For Students:
1. **Read README first** - Understand the problem
2. **Sketch architecture** - Draw before coding
3. **Fill in TODOs** - Implement one function at a time
4. **Run tests frequently** - Test as you go
5. **Check hints only if stuck** - Try for 30min first
6. **Review design patterns** - After you finish, compare your approach

### For AI Assistants:
1. **Don't give full solutions** - Point to hints instead
2. **Ask guiding questions** - "What happens if all providers fail?"
3. **Explain concepts** - "Exponential backoff means..."
4. **Debug specific errors** - "That error means your API key isn't set"
5. **Review code** - "Your error handling looks good, but consider..."
6. **Encourage experimentation** - "Try it and see what happens"

### For Instructors:
1. **Customize TODOs** - Adjust difficulty for your students
2. **Add more hints** - If students get stuck frequently
3. **Update cost tables** - Keep pricing current
4. **Add more tests** - Cover edge cases you see students miss
5. **Share student solutions** - Showcase different approaches

---

## Template Checklist

Every project template should have:
- [ ] Clear problem statement
- [ ] Learning goals
- [ ] Success criteria
- [ ] Starter code with TODOs
- [ ] Some complete code as reference
- [ ] Test templates
- [ ] Progressive hints (3+ levels)
- [ ] Design patterns guide (not full solution)
- [ ] Example inputs/outputs
- [ ] Time estimate

**Remember:** The goal is guided discovery, not copy-paste. Students should struggle a bit—that's where learning happens.
