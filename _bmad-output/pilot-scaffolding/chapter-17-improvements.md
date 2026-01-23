# Chapter 17 Improvements: Error Handling, Testing, & Debugging

**Date**: 2026-01-23
**Task**: Improve Chapter 17 with error handling hints, test execution guidance, and debugging notes
**Status**: ✅ COMPLETE

---

## Part 1: Error Handling Hints for Complex Functions

### Improvement 1: Add Error Handling to `ingest_knowledge_base()`

**Location**: After existing hints in the scaffolded function

**Add these additional hints**:

```python
def ingest_knowledge_base(store: VectorStore, knowledge_base: list[str]) -> None:
    """
    Ingest documents into the vector store.

    TODO: Implement this function
    HINT: Iterate through knowledge_base with enumerate() to get index and text
    HINT: Use store.add_document() with doc_id=str(i), text=text
    HINT: Add metadata={"source": "internal_memo.txt"} to track document origin
    HINT: Print progress message after adding all documents

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Wrap add_document() in try/except to catch VectorStoreError
    HINT (Error Handling): On error, print warning but continue: f"⚠️  Failed to add doc {i}: {error}"
    HINT (Error Handling): Track failed_count and report at end if any failures occurred

    Args:
        store: VectorStore instance to add documents to
        knowledge_base: List of text strings to ingest

    Returns:
        None

    Raises:
        None (errors are logged but don't stop ingestion)
    """
    pass  # Your code here
```

**Rationale**: Ingestion should be resilient - one bad document shouldn't crash the entire process.

---

### Improvement 2: Add Error Handling to `ask_rag()`

**Location**: After existing hints in the scaffolded function

**Add these additional hints**:

```python
def ask_rag(question: str, store: VectorStore, client: MultiProviderClient, limit: int = 2) -> str:
    """
    Answer a question using RAG (Retrieval-Augmented Generation).

    TODO: Implement this function
    HINT: Use store.search(question, limit=limit) to retrieve relevant documents
    HINT: Join results with "\n".join(results) to create context_text
    HINT: Build a prompt with three parts: instructions, context, question
    HINT: Instructions should say "Answer using ONLY the context provided"
    HINT: Use client.generate(prompt) to get the answer
    HINT: Print the question, found context, and answer for debugging

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Wrap store.search() in try/except to catch VectorStoreError
    HINT (Error Handling): If search fails, return "Error: Unable to search knowledge base. Please try again."
    HINT (Error Handling): Wrap client.generate() in try/except to catch APIError and RateLimitError
    HINT (Error Handling): On APIError, return f"Error: LLM service unavailable ({error})"
    HINT (Error Handling): On RateLimitError, return "Error: Rate limit exceeded. Please wait a moment and retry."
    HINT (Error Handling): If results is empty list, return "I don't have any relevant information about that topic."

    Args:
        question: User's question to answer
        store: VectorStore to search for relevant context
        client: LLM client to generate answer
        limit: Number of relevant documents to retrieve (default: 2)

    Returns:
        str: AI-generated answer based on retrieved context, or error message

    Raises:
        None (all errors are caught and returned as error messages)
    """
    pass  # Your code here
```

**Rationale**: RAG systems have two failure points (vector store, LLM API) - both need graceful handling.

---

### Improvement 3: Add Error Handling to `search_with_sources()`

**Location**: After existing hints in rag_citations.py

**Add these additional hints**:

```python
def search_with_sources(store: VectorStore, query: str, limit: int = 1) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Search for documents and return both content and source metadata.

    TODO: Implement this function
    HINT: Use store.search_with_metadata(query, limit=limit) to get results with metadata
    HINT: The method returns a list of tuples: [(doc_text, metadata_dict), ...]
    HINT: Iterate through results and print both the document text and source
    HINT: Format output clearly with separators for readability

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Wrap search_with_metadata() in try/except to catch AttributeError
    HINT (Error Handling): If method doesn't exist, fall back to: store.search(query, limit)
    HINT (Error Handling): Return empty list [(doc, {"source": "unknown"})] if fallback used
    HINT (Error Handling): Print warning: "⚠️  Metadata not available, using basic search"

    Args:
        store: VectorStore instance to search
        query: Search query string
        limit: Maximum number of results to return (default: 1)

    Returns:
        List of tuples containing (document_text, metadata_dict)
        Empty list if search fails
    """
    pass  # Your code here
```

**Rationale**: Not all vector stores support metadata - code should degrade gracefully.

---

## Part 2: Test Execution Guidance

### New Section: Add After "Common Mistakes to Avoid" (Before Quick Reference Card)

**Insert this complete section**:

---

## 🧪 Running Your Tests

After implementing your RAG functions, verify your work with the comprehensive test suite.

### Prerequisites

Ensure you have pytest installed:

```bash
pip install pytest pytest-asyncio
```

### Running All Tests

Execute the full test suite for Chapter 17:

```bash
pytest tests/test_chapter_17.py -v
```

**Expected Output** (when fully implemented):

```
tests/test_chapter_17.py::TestKnowledgeBaseIngestion::test_ingest_function_exists PASSED
tests/test_chapter_17.py::TestKnowledgeBaseIngestion::test_ingest_adds_documents_to_store PASSED
tests/test_chapter_17.py::TestKnowledgeBaseIngestion::test_ingest_preserves_metadata PASSED
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_function_exists PASSED
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_returns_string PASSED
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_retrieves_relevant_context PASSED
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_handles_unknown_questions PASSED
tests/test_chapter_17.py::TestCitationTracking::test_search_with_sources_function_exists PASSED
tests/test_chapter_17.py::TestCitationTracking::test_search_with_sources_returns_metadata PASSED
tests/test_chapter_17.py::TestHallucinationPrevention::test_hallucination_prevention_function_exists PASSED
tests/test_chapter_17.py::TestHallucinationPrevention::test_grounding_overrides_training_data PASSED
tests/test_chapter_17.py::TestPropertyP20::test_p20_rag_uses_context_not_training PASSED
tests/test_chapter_17.py::TestPropertyP20::test_p20_empty_context_returns_unknown PASSED
tests/test_chapter_17.py::TestIntegration::test_full_rag_pipeline PASSED

========================= 14 passed in 8.42s =========================
```

### Running Specific Test Categories

**Test only ingestion**:
```bash
pytest tests/test_chapter_17.py::TestKnowledgeBaseIngestion -v
```

**Test only RAG query pipeline**:
```bash
pytest tests/test_chapter_17.py::TestRAGQueryPipeline -v
```

**Test only Property P20 (correctness)**:
```bash
pytest tests/test_chapter_17.py::TestPropertyP20 -v
```

### Understanding Test Results

#### ✅ When Tests Pass

```
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_returns_string PASSED
```

**Meaning**: Your `ask_rag()` function correctly returns a string (not None or other type).

---

#### ⏭️ When Tests Skip

```
tests/test_chapter_17.py::TestRAGQueryPipeline::test_ask_rag_returns_string SKIPPED
```

**Meaning**: Test was skipped because:
- Function doesn't exist yet (`pass` is still in place)
- Required dependencies not installed
- Implementation incomplete

**Action**: Implement the function and rerun tests.

---

#### ❌ When Tests Fail

```
tests/test_chapter_17.py::TestPropertyP20::test_p20_rag_uses_context_not_training FAILED

E AssertionError: RAG system is using training data instead of context!
E Expected answer to mention 'cheese' (from context: moon is cheese)
E Got: 'The moon is made of rock'
```

**Meaning**: Your implementation has a bug. The assertion message tells you exactly what's wrong.

**Action**: Read the assertion message carefully - it explains the expected vs actual behavior. Fix your implementation and rerun.

---

### Test-Driven Development (TDD) Workflow

**Step 1**: Run tests before implementing (they should skip):
```bash
pytest tests/test_chapter_17.py::TestKnowledgeBaseIngestion -v
```

**Step 2**: Implement the function (e.g., `ingest_knowledge_base()`)

**Step 3**: Run tests again (they should pass or fail with helpful messages):
```bash
pytest tests/test_chapter_17.py::TestKnowledgeBaseIngestion -v
```

**Step 4**: Fix any failures based on assertion messages

**Step 5**: Repeat until all tests pass ✅

---

### Running the Verification Script

After all implementation tests pass, run the correctness verification:

```bash
python verify_rag.py
```

**Expected Output**:
```
Testing Property P20: Consistency with Context
================================================

Test Context: The moon is made of cheese.
Question: What is the moon made of?

AI Answer: The moon is made of cheese.

✅ PASS: RAG system correctly uses context over training data
```

**If verification fails**:
```
❌ FAIL: RAG system is using training data (mentioned 'rock' instead of 'cheese')
```

→ Check your prompt grounding instructions in `ask_rag()`

---

### Debugging Failed Tests

**Problem**: `test_ingest_adds_documents_to_store` fails

**Common Causes**:
1. Forgot to call `store.add_document()`
2. Wrong parameter names (doc_id vs id)
3. Not storing documents properly

**Debug Steps**:
1. Print inside your function: `print(f"Adding doc {i}: {text[:50]}")`
2. After ingestion, verify: `print(f"Store has {len(store._collection.get()['ids'])} docs")`
3. Check if search returns results: `print(store.search("test", limit=5))`

---

**Problem**: `test_p20_rag_uses_context_not_training` fails

**Common Causes**:
1. Missing grounding instruction: "Answer using ONLY the context"
2. Context not properly injected into prompt
3. LLM ignoring instructions (prompt structure issue)

**Debug Steps**:
1. Print your full prompt: `print(f"Prompt sent to LLM:\n{prompt}")`
2. Verify context is in prompt: `assert "cheese" in prompt.lower()`
3. Check LLM response: `print(f"Raw LLM response: {answer}")`

---

### Performance Notes

**Test Suite Runtime**: ~5-10 seconds (with API calls mocked)

**If tests are slow** (>30 seconds):
- Tests may be making real API calls (check if mocks are working)
- ChromaDB may be loading large indexes (use test-specific DB path)
- Network latency (ensure local ChromaDB instance)

---

## Part 3: Common Errors & Debugging

### New Section: Add After "🧪 Running Your Tests" (Before Quick Reference Card)

**Insert this complete section**:

---

## 🐛 Common Errors & How to Fix Them

### Error 1: `ModuleNotFoundError: No module named 'chromadb'`

**Symptom**:
```python
Traceback (most recent call last):
  File "simple_rag.py", line 2, in <module>
    from shared.infrastructure.vector_store import VectorStore
ModuleNotFoundError: No module named 'chromadb'
```

**Cause**: ChromaDB not installed

**Fix**:
```bash
pip install chromadb
```

**Verify**:
```bash
python -c "import chromadb; print('ChromaDB installed:', chromadb.__version__)"
```

---

### Error 2: `openai.error.AuthenticationError: Incorrect API key`

**Symptom**:
```
openai.error.AuthenticationError: Incorrect API key provided
```

**Cause**:
- API key not set in environment
- Wrong API key format
- API key revoked

**Fix**:

**Step 1**: Verify your API key exists:
```bash
# Windows (PowerShell)
echo $env:OPENAI_API_KEY

# Mac/Linux
echo $OPENAI_API_KEY
```

**Step 2**: If empty, set it:
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-..."

# Mac/Linux
export OPENAI_API_KEY="sk-..."
```

**Step 3**: Verify format:
- OpenAI keys start with `sk-`
- Should be ~50 characters long
- No spaces or quotes

**Step 4**: Test authentication:
```python
from openai import OpenAI
client = OpenAI()  # Will fail if key is wrong
print("✅ API key is valid")
```

---

### Error 3: `AttributeError: 'VectorStore' object has no attribute 'search_with_metadata'`

**Symptom**:
```python
AttributeError: 'VectorStore' object has no attribute 'search_with_metadata'
```

**Cause**: Your VectorStore implementation doesn't have this method yet (from Chapter 14)

**Fix Option 1 - Implement the method**:
Go back to Chapter 14 and add `search_with_metadata()` to your VectorStore class.

**Fix Option 2 - Use fallback** (temporary workaround):
```python
def search_with_sources(store: VectorStore, query: str, limit: int = 1):
    """Search with graceful fallback if metadata not available."""
    try:
        # Try the metadata version
        return store.search_with_metadata(query, limit=limit)
    except AttributeError:
        # Fall back to basic search
        print("⚠️  Metadata not available, using basic search")
        results = store.search(query, limit=limit)
        return [(doc, {"source": "unknown"}) for doc in results]
```

---

### Error 4: `openai.error.RateLimitError: Rate limit reached`

**Symptom**:
```
openai.error.RateLimitError: Rate limit reached for gpt-4 in organization org-...
```

**Cause**:
- Exceeded requests per minute (RPM) limit
- Exceeded tokens per minute (TPM) limit
- Free tier limits hit

**Fix**:

**Immediate**: Add retry logic with exponential backoff:
```python
import time

def ask_rag_with_retry(question, store, client, max_retries=3):
    """RAG with automatic retry on rate limits."""
    for attempt in range(max_retries):
        try:
            return ask_rag(question, store, client)
        except openai.error.RateLimitError as e:
            if attempt == max_retries - 1:
                return f"Error: Rate limit exceeded after {max_retries} retries. Please wait."

            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"⏳ Rate limited, waiting {wait_time}s before retry...")
            time.sleep(wait_time)
```

**Long-term**:
1. Check your usage: https://platform.openai.com/usage
2. Upgrade to paid tier for higher limits
3. Implement request queuing to stay under limits

---

### Error 5: Vector Store Returns Empty Results

**Symptom**:
```python
print(store.search("Project Alpha", limit=5))
# Output: []
```

**Cause**:
- Documents not ingested properly
- Query doesn't semantically match any documents
- Wrong collection name

**Debug Steps**:

**Step 1**: Verify documents were added:
```python
# After ingestion, check collection
collection = store._collection
ids = collection.get()['ids']
print(f"Collection has {len(ids)} documents: {ids}")
```

**Expected**: Should print `['0', '1', '2', '3']` (or however many you ingested)

**Step 2**: Verify embeddings were created:
```python
# Check if embeddings exist
embeddings = collection.get(include=['embeddings'])['embeddings']
print(f"First embedding: {embeddings[0][:5]}...")  # Print first 5 dims
```

**Expected**: Should print something like `[0.023, -0.145, 0.089, ...]`

**Step 3**: Test with exact text match:
```python
# Try searching for exact text you ingested
knowledge = ["Project Alpha is a confidential initiative."]
store.add_document("test", knowledge[0], metadata={})
results = store.search("Project Alpha", limit=1)
print(f"Exact match search: {results}")
```

**Expected**: Should find the document

**Step 4**: Check collection name:
```python
print(f"Active collection: {store.collection_name}")
```

**Common mistake**: Ingesting into "collection_A" but searching "collection_B"

---

### Error 6: LLM Ignores Context and Hallucinates

**Symptom**:
```python
# You provide context: "Project Alpha costs $500 million"
# But LLM responds: "I don't have information about Project Alpha's cost"

# OR worse, it hallucinates: "Project Alpha costs approximately $2 billion"
```

**Cause**:
- Grounding instructions not clear enough
- Context not properly injected into prompt
- LLM interpreting instructions too strictly

**Fix**:

**Step 1**: Verify context is in prompt:
```python
def ask_rag(question, store, client, limit=2):
    results = store.search(question, limit=limit)
    context_text = "\n".join(results)

    # DEBUG: Print what LLM sees
    print(f"🔍 Context being sent to LLM:\n{context_text}\n")

    prompt = f"""
    Answer using ONLY this context:
    {context_text}

    Question: {question}
    """

    # DEBUG: Print full prompt
    print(f"📝 Full prompt:\n{prompt}\n")

    answer = client.generate(prompt)
    return answer
```

**Step 2**: Strengthen grounding instructions:
```python
# WEAK (LLM may ignore):
prompt = f"Context: {context}\nQuestion: {question}"

# STRONG (explicit constraints):
prompt = f"""You MUST answer using ONLY the context below.
Do NOT use any external knowledge.
If the answer is not in the context, respond: "Not found in provided context."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER (based solely on context above):"""
```

**Step 3**: Test with counter-factual context:
```python
# This should prove grounding works
context = "The sky is bright orange."
question = "What color is the sky?"

answer = ask_rag(question, store, client)
# Should say "orange" NOT "blue"
assert "orange" in answer.lower(), "Grounding failed!"
```

---

### Error 7: Tests Pass But Verify Script Fails

**Symptom**:
```bash
pytest tests/test_chapter_17.py -v  # All pass ✅

python verify_rag.py  # FAIL ❌
```

**Cause**:
- Tests use mocked data (might not reflect real behavior)
- Verify script uses real API (stricter validation)
- Implementation passes basic tests but fails property tests

**Fix**:

**Step 1**: Read the verify script output carefully:
```
❌ FAIL: Expected answer to use context (cheese) but got training data (rock)
```

**Step 2**: Run your implementation manually with verify script's test case:
```python
# Manually test the exact case from verify_rag.py
context = "The moon is made of cheese."
question = "What is the moon made of?"

# Use your ask_rag function
answer = ask_rag(question, store, client)
print(f"Answer: {answer}")

# Check if grounding worked
if "cheese" in answer.lower():
    print("✅ Grounding works")
else:
    print("❌ Grounding failed - answer used training data")
```

**Step 3**: If grounding fails, check your prompt structure (see Error 6 fix)

---

### Debugging Checklist

When your RAG system isn't working, check these in order:

**1. Dependencies**
- [ ] ChromaDB installed: `pip install chromadb`
- [ ] OpenAI installed: `pip install openai`
- [ ] API key set: `echo $OPENAI_API_KEY`

**2. Ingestion**
- [ ] Documents were added: Print collection size
- [ ] Embeddings were created: Check collection embeddings
- [ ] Metadata was stored: Use `search_with_metadata()`

**3. Retrieval**
- [ ] Search returns results: Test with exact text match
- [ ] Results are relevant: Print search results
- [ ] Correct collection: Verify collection name

**4. Prompt Construction**
- [ ] Context is in prompt: Print full prompt before sending
- [ ] Grounding instructions are clear: Use explicit constraints
- [ ] Question is formatted correctly: Check prompt structure

**5. LLM Response**
- [ ] API call succeeds: Catch and print exceptions
- [ ] Response is not empty: Check `if answer:`
- [ ] Response uses context: Test with counter-factual

---

### Getting Help

If you're still stuck after debugging:

**1. Check test assertion messages** - They explain exactly what's wrong:
```
AssertionError: Expected 'cheese' in response but got 'rock'
```

**2. Add print statements everywhere**:
```python
print(f"🔍 Searching for: {question}")
print(f"📄 Found {len(results)} documents")
print(f"📝 Context length: {len(context_text)} chars")
print(f"🤖 LLM response: {answer}")
```

**3. Compare with solution code** (in `<details>` sections) - How does your implementation differ?

**4. Test components individually**:
- Does vector store work? Test search separately
- Does LLM work? Test generate separately
- Does RAG work? Only test together after both work alone

---

## Summary of Improvements

**Added to Chapter 17**:

1. ✅ **Error Handling Hints**: 3 functions enhanced with 12 additional hints
   - `ingest_knowledge_base()`: Resilient ingestion with error tracking
   - `ask_rag()`: Graceful handling of search failures and API errors
   - `search_with_sources()`: Fallback when metadata unavailable

2. ✅ **Test Execution Guidance**: Complete "🧪 Running Your Tests" section
   - How to run all tests
   - How to run specific test categories
   - Understanding PASSED/SKIPPED/FAILED results
   - Test-driven development workflow
   - Debugging failed tests

3. ✅ **Common Errors & Debugging**: Complete "🐛 Common Errors" section
   - 7 common error scenarios with fixes
   - Debug checklists for systematic troubleshooting
   - Step-by-step debugging procedures
   - Tips for getting help

**Total New Content**: ~1500 words of practical guidance

---

## Insertion Points in Chapter 17

**Error Handling Hints**: Update the three scaffolded functions directly with new hints

**Test Execution Section**: Insert after "Common Mistakes to Avoid" (line ~607), before "Quick Reference Card" (line ~609)

**Debugging Section**: Insert after "🧪 Running Your Tests", before "Quick Reference Card"

**Final Structure**:
1. Coffee Shop Intro
2. Prerequisites
3. RAG Story
4. Part 1: simple_rag.py (with error hints)
5. Part 2: rag_citations.py (with error hints)
6. Part 3: hallucination_test.py (with error hints)
7. Common Mistakes to Avoid
8. **🧪 Running Your Tests** ← NEW
9. **🐛 Common Errors & Debugging** ← NEW
10. Quick Reference Card
11. Verification (P20)
12. Summary
13. What's Next

---

**Status**: ✅ COMPLETE - Ready to merge into Chapter 17
