# Hint 1: Architecture Design

## Before you code, answer these questions:

### 1. Provider Priority

**Question:** How do you store the provider order?

**Think about:**
- Should it be a list? A dict? A priority queue?
- Where does the order come from? (Config)
- Can the order change at runtime?

**Suggested approach:**
```python
# Use a list from config - simple and clear
providers_to_try = self.config.providers  # [Provider.OPENAI, Provider.ANTHROPIC, ...]

# Loop through in order
for provider in providers_to_try:
    try:
        result = await self._call_provider(provider, request)
        return result  # Success! Stop here
    except Exception as e:
        # Log and continue to next provider
        pass
```

---

### 2. Error Handling

**Question:** What errors can happen?

**Common errors:**
- `RateLimitError` - Too many requests (should retry)
- `AuthenticationError` - Invalid API key (should fail fast)
- `TimeoutError` - Request took too long (should retry or fallback)
- `InvalidRequestError` - Bad parameters (should fail fast)
- `APIError` - Server error (should retry or fallback)

**Decision tree:**
```
Error occurs
    ↓
Is it RateLimitError?
    Yes → Retry with backoff (same provider)
    No → Continue
    ↓
Is it AuthenticationError?
    Yes → Skip this provider, try next
    No → Continue
    ↓
Is it TimeoutError?
    Yes → Try next provider
    No → Continue
    ↓
Other error?
    → Try next provider
```

**Suggested approach:**
```python
try:
    response = await self._call_provider(provider, request)
    return response
except RateLimitError as e:
    # Retry with backoff
    await self._retry_with_backoff(...)
except AuthenticationError as e:
    # Log and skip to next provider
    logger.error(f"{provider} auth failed: {e}")
    continue
except Exception as e:
    # Log and try next provider
    logger.warning(f"{provider} failed: {e}")
    continue
```

---

### 3. Cost Tracking

**Question:** Where do you get token counts?

**Answer:** From the API response!

**OpenAI response structure:**
```python
response = await client.chat.completions.create(...)
# Token counts are in response.usage
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens
```

**Anthropic response structure:**
```python
response = await client.messages.create(...)
# Token counts are in response.usage
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
```

**Question:** Where do you get pricing?

**Answer:** From COST_TABLE (in models.py)

**Cost calculation:**
```python
def _calculate_cost(self, provider, model, input_tokens, output_tokens):
    # Look up rates
    rates = COST_TABLE.get(provider, {}).get(model)
    
    if not rates:
        logger.warning(f"Unknown model {model}, returning 0 cost")
        return 0.0
    
    # Calculate cost (rates are per 1K tokens)
    cost = (
        (input_tokens * rates["input"]) + 
        (output_tokens * rates["output"])
    ) / 1000
    
    return round(cost, 6)  # Round to 6 decimal places
```

---

### 4. Testing Strategy

**Question:** How do you test without real API calls?

**Answer:** Use mocking!

**Pattern:**
```python
from unittest.mock import Mock, AsyncMock, patch

@patch('starter_code.core.AsyncOpenAI')
async def test_successful_call(mock_openai_class):
    # Create mock response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="4"))]
    mock_response.usage = Mock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15
    )
    
    # Make the mock client return this response
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    # Now test your client
    config = LLMConfig(providers=[Provider.OPENAI], openai_api_key="test")
    client = MultiProviderClient(config)
    
    request = LLMRequest(prompt="What is 2+2?")
    response = await client.complete(request)
    
    assert response.content == "4"
    assert response.tokens_used == 15
```

---

## Draw This Before Coding

### Flow Diagram

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ MultiProviderClient     │
│ .complete(request)      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Loop through providers  │
│ [OpenAI, Anthropic, ...] │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Try Provider 1 (OpenAI) │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │         │
Success?    Fail?
    │         │
    │         ▼
    │    ┌─────────────────┐
    │    │ Log Error       │
    │    │ Add to history  │
    │    └────────┬────────┘
    │             │
    │             ▼
    │    ┌─────────────────┐
    │    │ Try Provider 2  │
    │    └────────┬────────┘
    │             │
    │        ┌────┴────┐
    │        │         │
    │    Success?    Fail?
    │        │         │
    │        │         ▼
    │        │    ┌─────────────┐
    │        │    │ All Failed? │
    │        │    │ Raise Error │
    │        │    └─────────────┘
    │        │
    ▼        ▼
┌─────────────────────────┐
│ Return LLMResponse      │
│ - content               │
│ - provider used         │
│ - tokens & cost         │
│ - latency               │
└─────────────────────────┘
```

### Data Flow

```
LLMRequest
    ↓
[prompt, model, temperature, ...]
    ↓
Provider Client (OpenAI/Anthropic/...)
    ↓
API Call
    ↓
Raw Response
    ↓
Parse & Extract
    ↓
[content, tokens, ...]
    ↓
Calculate Cost
    ↓
LLMResponse
```

---

## Key Design Decisions

### Decision 1: Sync vs Async?

**Recommendation:** Async

**Why?**
- LLM calls are I/O bound (waiting for network)
- Async allows concurrent requests
- Better for production use

**Trade-off:**
- More complex code
- Need to understand async/await

---

### Decision 2: Retry vs Fallback?

**Recommendation:** Both!

**Retry:** For transient errors on same provider
- Rate limits (wait and retry)
- Temporary network issues

**Fallback:** For persistent errors
- Authentication failures
- Provider outages
- Timeouts

**Pattern:**
```python
for provider in providers:
    try:
        # Try with retries
        response = await self._retry_with_backoff(
            lambda: self._call_provider(provider, request)
        )
        return response
    except Exception:
        # Fallback to next provider
        continue
```

---

### Decision 3: Where to Store Cost Table?

**Options:**
1. Hardcode in models.py (current approach)
2. Load from config file (YAML/JSON)
3. Fetch from API (dynamic pricing)

**Recommendation:** Start with #1, move to #2 later

**Why?**
- Simple to start
- Easy to update
- Can refactor later

---

### Decision 4: How to Handle Unknown Models?

**Options:**
1. Raise exception
2. Return 0 cost
3. Use default rate

**Recommendation:** Log warning + return 0

**Why?**
- Doesn't break the system
- Alerts you to missing data
- Can fix later

---

## Implementation Order

**Do this in order:**

1. **Models first** (models.py)
   - Complete LLMRequest
   - Complete LLMResponse
   - Complete ProviderError

2. **Client initialization** (core.py)
   - Initialize provider clients
   - Validate API keys

3. **Single provider** (core.py)
   - Implement _call_openai()
   - Test with real API
   - Verify cost calculation

4. **Fallback logic** (core.py)
   - Implement complete()
   - Add error handling
   - Test with mocked failures

5. **Retry logic** (core.py)
   - Implement _retry_with_backoff()
   - Test with rate limits

6. **Tests** (tests/)
   - Unit tests with mocks
   - Integration tests with real API

---

## Questions to Answer Before Coding

1. **How do you store provider clients?**
   - Dict? List? Class attributes?

2. **How do you handle provider-specific parameters?**
   - Map generic request to provider format?

3. **When to retry vs when to fallback?**
   - Which errors are transient?

4. **How to make this extensible?**
   - How would you add a new provider?

5. **How to test this?**
   - Mock strategy? Integration tests?

---

## Next Steps

1. Draw the flow diagram on paper
2. Answer the questions above
3. Write pseudocode for complete()
4. Review with someone (or rubber duck)
5. Start implementing models.py

**Don't start coding until you can explain the architecture!**

---

**Still stuck? Check hint_02_implementation.md for code patterns.**
