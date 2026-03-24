# Layer 1: The Mechanic-Level AI Engineer — Day-by-Day Curriculum

**Total Duration**: ~40 days (4-6 focused hours/day)
**Philosophy**: Build first, understand after. You're a Mechanic — you USE tools expertly before studying how they're made.
**Pedagogy**: Action-First (quick win in first 15 min of each day), then guided deep-dive
**Code Policy**: This plan tells you WHAT to build and HOW to think about it. You write every line yourself.

---

## How to Use This Plan

Each day follows the **Mechanic's Workflow**:

1. **Warm the Engine** (10 min) — Read the day's goal and analogy. Know what you're building before you touch code.
2. **First Wrench Turn** (30-45 min) — Get something working. Ugly code that runs beats beautiful code that doesn't.
3. **Tighten the Bolts** (1.5-2 hrs) — Improve, extend, handle edge cases. This is where real learning happens.
4. **Road Test** (30-45 min) — Run it, break it, fix it. Verify with the provided checklist.
5. **Logbook Entry** (15 min) — Write down what you learned, what confused you, what you'd do differently.

**Ground Rules**:
- Never copy-paste code from tutorials. Type everything yourself.
- When stuck for >20 minutes, search docs/Stack Overflow. That IS the job.
- Every mini-project must run. No half-finished notebooks.
- Commit to Git daily. Your commit history IS your portfolio.

---

# PHASE 1: FOUNDATIONS (Days 1-8)
## "I can talk to AI and search through documents"

**What you're building toward**: By Day 8, you'll have a working document Q&A system and a containerized API. These are the building blocks for everything that follows.

---

## Day 1: Hello LLM — Your First AI Conversation
**Mini-Project 1 | ~4 hours | Difficulty: ⭐**

### The Mechanic's Analogy
> You're about to start a car for the first time. You don't need to know how the engine works — you need to know where the key goes, what the pedals do, and how to steer. Today, the "key" is an API key, the "pedal" is a Python script, and the "steering" is a prompt.

### Warm the Engine
- Set up your workspace: Python 3.10+, virtual environment, `.env` file
- Get an OpenAI API key (and optionally Anthropic)
- Install: `openai`, `python-dotenv`

### First Wrench Turn — Get AI Talking (aim for 15 minutes)
Build the simplest possible script: send one message to an LLM, print the response. Five lines. Run it. See AI respond to YOUR code.

**You just did something remarkable.** Your code communicated with one of the most advanced AI systems ever built. Sit with that for a moment.

### Tighten the Bolts
Now build a proper **CLI chatbot** with these features:
1. **Conversation loop** — Keep chatting until the user types "quit"
2. **Message history** — The AI remembers what you said earlier (hint: you accumulate messages in a list)
3. **System prompt** — Give your chatbot a personality ("You are a helpful coding assistant who explains things simply")
4. **Basic Streamlit UI** — Wrap your chatbot in a simple web interface

### Guidance (NOT code):
- The OpenAI chat API uses a `messages` list with roles: `system`, `user`, `assistant`
- Each new user message gets appended. Each AI response also gets appended. That's how "memory" works.
- For Streamlit: `st.chat_input()` for user input, `st.chat_message()` for display, `st.session_state` to persist messages across reruns

### Road Test Checklist
- [ ] Script runs without errors
- [ ] AI responds to your messages
- [ ] Conversation remembers context (ask "What did I just ask you?")
- [ ] Streamlit UI shows chat history
- [ ] `.env` file is in `.gitignore` (NEVER commit API keys)

### Logbook Prompts
- What surprised you about the API response format?
- What happens when the messages list gets very long? (Think about costs)
- How would you make this work with Anthropic's Claude API instead?

---

## Day 2: Structured Outputs & Prompt Engineering
**Mini-Project 2 | ~5 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> Yesterday you learned to start the car. Today you learn to steer precisely. A vague prompt is like vague directions — "go somewhere nice" vs "take I-95 North to Exit 12." Prompt engineering is learning to give precise directions to AI.

### Warm the Engine
- Read about prompt patterns: zero-shot, few-shot, chain-of-thought, system roles
- Resource: [DeepLearning.AI — ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) (1.5 hrs, Free — code along, don't just watch)

### First Wrench Turn — Extract Structured Data
Build a script that takes a restaurant review (plain text) and extracts structured JSON:
- Restaurant name, cuisine type, rating (1-5), price range, pros, cons

Get it working with a simple prompt first. Don't worry about edge cases yet.

### Tighten the Bolts
Now build a **Prompt Engineering Toolkit** — a collection of scripts demonstrating different patterns:

| Pattern | What to Build | Key Concept |
|---------|--------------|-------------|
| Zero-shot | Classify movie reviews as positive/negative | No examples needed |
| Few-shot | Extract entity data with 3 examples in the prompt | Examples guide the format |
| Chain-of-thought | Solve a multi-step math word problem | "Let's think step by step" |
| System role | Create a persona (strict teacher, friendly coach) | System message controls behavior |
| Structured output | Force JSON output with a defined schema | Use `response_format` or function calling |
| Temperature test | Same prompt at temp 0.0, 0.7, and 1.0 | Temperature = creativity dial |
| Token counting | Count tokens with `tiktoken`, estimate cost | Every token costs money |
| Prompt chaining | Output of prompt 1 feeds into prompt 2 | Decompose complex tasks |

### Guidance:
- **OpenAI JSON mode**: Pass `response_format={"type": "json_object"}` and mention "JSON" in your prompt
- **Function calling**: Define a Pydantic model for your expected output, pass it as a tool/function
- **Pydantic validation**: After getting JSON back, parse it with your Pydantic model. If it fails, re-prompt with the error message (this is a retry pattern you'll use constantly)
- **tiktoken**: `tiktoken.encoding_for_model("gpt-4o-mini")` gives you a tokenizer. `.encode(text)` returns token list, `len()` counts them

### Road Test Checklist
- [ ] Restaurant extractor produces valid JSON for 5 different reviews
- [ ] Each prompt pattern script runs and demonstrates its concept
- [ ] Temperature test shows measurable difference between 0.0 and 1.0
- [ ] Token counter accurately counts tokens and estimates cost
- [ ] At least one script uses Pydantic to validate LLM output

### Logbook Prompts
- Which prompt pattern surprised you the most? Why?
- What happens when the LLM returns malformed JSON? How did you handle it?
- Why would you choose function calling over JSON mode?

---

## Day 3: RAG from Scratch — No Frameworks
**Mini-Project 3 | ~6 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> Today you build a car engine from individual parts — pistons, crankshaft, spark plugs — before ever using a pre-assembled engine. This is the most important day of the entire curriculum. You're building RAG (Retrieval-Augmented Generation) from scratch, with NO frameworks, so you understand every moving part.

### Why This Matters
> An LLM without RAG is like taking a closed-book exam — it can only use what it memorized during training. RAG is the open-book version — it looks up information in YOUR documents before answering.

### Warm the Engine
- Understand the RAG pipeline: **Load → Chunk → Embed → Store → Query → Retrieve → Generate**
- Resource: Watch the first 45 minutes of [freeCodeCamp — RAG From Scratch](https://www.youtube.com/watch?v=sVcwVQRHIc8) for the mental model

### First Wrench Turn — Simplest Possible RAG
1. Take a text file with 10-20 paragraphs (copy any Wikipedia article)
2. Split it into chunks (just split on "\n\n" for now)
3. Embed each chunk using OpenAI's `text-embedding-3-small`
4. Store embeddings in a Python list (yes, just a list)
5. When a user asks a question, embed the question, compute cosine similarity with every chunk, grab the top 3
6. Feed those 3 chunks + the question into the LLM as context
7. Print the answer

**That's RAG.** Everything else is optimization.

### Tighten the Bolts
Now improve each piece:

**Better Chunking**:
- Don't split on "\n\n" — implement a simple recursive splitter that tries paragraph breaks first, then sentence breaks, then word breaks
- Add overlap: the last N characters of chunk 1 should be the first N characters of chunk 2
- Experiment: try chunk sizes of 200, 500, and 1000 characters. Ask the same question against each. Which gives better answers?

**Better Search**:
- Implement cosine similarity yourself (dot product / product of norms)
- Compare with L2 (Euclidean) distance. Same results? Different?
- What happens when you retrieve top-1 vs top-3 vs top-10?

**Better Prompt**:
- Write a prompt template that clearly separates context from question
- Add instructions: "Answer ONLY based on the provided context. If the context doesn't contain the answer, say 'I don't have enough information.'"
- Test: ask something NOT in the documents. Does it refuse to hallucinate?

### Guidance:
- Cosine similarity formula: `dot(A, B) / (norm(A) * norm(B))`. Use `numpy` for this.
- OpenAI embeddings return a list of floats. Store as numpy arrays for math.
- Your prompt template should look like: `"Context:\n{chunks}\n\nQuestion: {question}\n\nAnswer based only on the context above:"`
- The "no framework" constraint is intentional. You MUST understand these pieces before LangChain abstracts them away.

### Road Test Checklist
- [ ] RAG answers questions correctly about your document
- [ ] Asks about something NOT in the document → refuses to hallucinate
- [ ] 3 different chunk sizes tested, results documented
- [ ] Cosine similarity implemented manually (not using a library's built-in)
- [ ] Overlap between chunks is working (verify by printing chunk boundaries)

### Logbook Prompts
- What breaks when chunks are too small? Too large?
- What's the relationship between chunk size and answer quality?
- Where are the bottlenecks in your pipeline? What's slow?

---

## Day 4: Embeddings & Vector Stores
**Mini-Project 4 | ~5 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> Yesterday you stored embeddings in a Python list and searched linearly. That's like a mechanic who keeps every bolt in one big bucket — it works for 10 bolts, not for 10,000. Today you get a proper parts organizer: a vector database.

### Why Vector Databases?
> Imagine searching for a song on Spotify. Keyword search finds "Happy Birthday" only if you type those exact words. Semantic search (embeddings) finds it when you type "celebratory song for birthdays" because it understands MEANING, not just words. Vector databases make semantic search fast.

### Warm the Engine
- Install ChromaDB: `pip install chromadb`
- Resource: [DeepLearning.AI — Vector Databases: from Embeddings to Applications](https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/) (55 min, free)

### First Wrench Turn — ChromaDB Basics
1. Create a ChromaDB collection
2. Add your Day 3 document chunks with their embeddings
3. Query: pass a question, get back the top-k similar chunks
4. Compare results with your Day 3 manual search — they should match!

### Tighten the Bolts
Build a **Semantic Search Engine** over 50+ text documents:

1. **Create a corpus**: Gather 50+ text snippets. Ideas: movie descriptions, FAQ answers, product descriptions, or a mix. Store in a JSON or text file.
2. **Embed and store**: Use OpenAI `text-embedding-3-small` to embed all 50+ documents. Store in ChromaDB with persistence (so you don't re-embed every time).
3. **Query interface**: Build a simple CLI or Streamlit interface where you type a query and get the top-5 most similar documents.
4. **Compare metrics**: Run the same queries using cosine similarity AND L2 distance. Do the rankings differ?
5. **Keyword vs Semantic**: For 5 queries, compare results from exact keyword matching (Python `in` operator) vs semantic search. Document cases where semantic search wins.

### Guidance:
- ChromaDB can auto-embed with `SentenceTransformer` or you can provide your own embeddings via `embeddings` parameter
- Persistence: `chromadb.PersistentClient(path="./chroma_db")` saves to disk
- Metadata: Store source info (filename, page number) as metadata with each chunk. You'll need this for source attribution later.
- Distance metrics: ChromaDB supports `cosine`, `l2`, `ip` (inner product). Try switching between them.

### Road Test Checklist
- [ ] ChromaDB collection created with 50+ documents
- [ ] Queries return semantically relevant results
- [ ] Results persist across script restarts (database saved to disk)
- [ ] Cosine vs L2 comparison documented with examples
- [ ] At least 3 queries where semantic search beats keyword search

### Logbook Prompts
- How does ChromaDB compare to your Day 3 manual approach?
- What metadata would you store in a real production system?
- How would this scale to 1 million documents? What would break?

---

## Day 5: FastAPI + Docker Basics
**Mini-Project 5 | ~5 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> You've built a working engine (RAG). Now you need a chassis (FastAPI) so other people can use it, and a shipping container (Docker) so it runs the same everywhere. No one cares about your engine if they can't drive the car.

### Warm the Engine
- Install: `pip install fastapi uvicorn`
- Install Docker Desktop
- Resource: Skim the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) first 3 sections (~20 min)

### First Wrench Turn — Wrap Your Search in an API
Take your Day 4 semantic search engine and expose it as a REST API:
- `POST /search` — takes a query string, returns top-5 results
- `GET /health` — returns `{"status": "healthy"}`

Run it with `uvicorn`. Test with `curl` or the auto-generated Swagger UI at `/docs`.

### Tighten the Bolts

**Enhance the API**:
1. **Pydantic request/response models**: Define `SearchRequest` and `SearchResponse` with proper types
2. **Error handling**: What if the query is empty? What if ChromaDB is down?
3. **CORS**: Add CORS middleware so a frontend could call your API
4. **Query parameters**: Support `top_k` parameter (how many results to return)
5. **Metadata in response**: Return source info with each result

**Dockerize It**:
1. Create a `Dockerfile` for your API
2. Create a `requirements.txt` with all dependencies
3. Build the image: `docker build -t my-search-api .`
4. Run it: `docker run -p 8000:8000 my-search-api`
5. Test: hit `http://localhost:8000/docs` — same API, now in a container

**Docker Compose** (stretch goal):
- Create `docker-compose.yml` that runs your API
- Add environment variable support for API keys

### Guidance:
- FastAPI auto-generates OpenAPI docs. Use Pydantic models for request/response and you get free documentation.
- Dockerfile pattern: `FROM python:3.10-slim` → `COPY requirements.txt` → `RUN pip install` → `COPY . .` → `CMD ["uvicorn", "main:app"]`
- NEVER put API keys in Docker images. Use environment variables: `docker run -e OPENAI_API_KEY=sk-... my-image`
- If Docker is new to you, don't panic. The Dockerfile is just a recipe: "start with Python, install dependencies, copy code, run it."

### Road Test Checklist
- [ ] FastAPI `/search` endpoint returns results
- [ ] `/health` endpoint works
- [ ] Swagger UI shows all endpoints with proper types
- [ ] Docker image builds without errors
- [ ] Container runs and API is accessible from host
- [ ] No API keys hardcoded anywhere

### Logbook Prompts
- Why is Docker important for AI applications specifically?
- What's the difference between running locally vs in a container?
- How would you deploy this container to the cloud?

---

## Days 6-7: Full RAG Pipeline with LangChain
**Mini-Project 6 | ~8-10 hours over 2 days | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> Days 3-4 you built the engine from scratch — pistons, crankshaft, the works. Now you're switching to a pre-built engine (LangChain) that you can drop in and customize. You EARNED this shortcut by understanding the internals first.

### Why LangChain Now (Not Before)?
> "Build from scratch to learn, build with libraries to scale." — Jerry Liu (LlamaIndex creator). You know what chunking, embedding, and retrieval ARE because you built them. Now LangChain does the plumbing so you can focus on the architecture.

### Day 6: LangChain Foundations

#### Warm the Engine
- Install: `pip install langchain langchain-openai langchain-community chromadb`
- Resource: [DeepLearning.AI — LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/) — Watch lessons 1-4 (Models, Prompts, Parsers, Memory, Chains). ~1 hour.

#### First Wrench Turn — Rebuild Day 3 in LangChain
Take your Day 3 RAG pipeline and rebuild it using LangChain:
1. `PyPDFLoader` to load a PDF (find any 10+ page PDF)
2. `RecursiveCharacterTextSplitter` to chunk it
3. `OpenAIEmbeddings` to embed chunks
4. `Chroma` vectorstore to store them
5. `RetrievalQA` chain to query

The goal: see how LangChain does the SAME things you did manually, but with less code.

#### Tighten the Bolts
- Try different text splitters: `CharacterTextSplitter`, `RecursiveCharacterTextSplitter`, `TokenTextSplitter`. Which gives the best results for your document?
- Experiment with retrieval parameters: `search_type="similarity"` vs `search_type="mmr"` (Maximum Marginal Relevance)
- Add `return_source_documents=True` so you can see WHICH chunks the answer came from

### Day 7: Multi-Document RAG with Source Attribution

#### Build a Document Q&A System
Build something more ambitious:
1. Load 3-5 different documents (PDFs, text files, or web pages)
2. Store all chunks in a single ChromaDB collection with metadata (source filename, page number)
3. Build a RetrievalQA chain that answers questions across ALL documents
4. Show source attribution: for every answer, display which document(s) and page(s) it came from
5. Add a simple Streamlit chat interface

#### Guidance:
- LangChain's `PyPDFLoader` and `WebBaseLoader` handle different formats
- Store metadata with each chunk: `{"source": filename, "page": page_number}`
- The `RetrievalQA` chain with `return_source_documents=True` gives you the chunks that were used
- Streamlit: use `st.expander("Sources")` to show source documents below each answer

### Road Test Checklist (Both Days)
- [ ] LangChain RAG pipeline works end-to-end
- [ ] At least 3 documents loaded and searchable
- [ ] Source attribution shows correct document and page
- [ ] Streamlit interface allows multi-turn conversation
- [ ] Can explain the difference between your Day 3 manual RAG and LangChain RAG

### Logbook Prompts
- What does LangChain abstract away? What does it make harder?
- When would you NOT use LangChain?
- What's the difference between similarity search and MMR?

---

## Day 8: Multi-Document RAG + RAGAS Evaluation
**Mini-Project 7 | ~5 hours | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> A mechanic doesn't just fix a car and declare it done — they test drive it, check the gauges, and verify everything works under stress. Today you add a diagnostic system to your RAG pipeline. Without evaluation, you're just HOPING it works.

### The RAG Triad — Your Diagnostic Gauges
Think of three gauges on your dashboard:
1. **Context Relevance** — Did the retriever find the right documents? (Are you looking in the right filing cabinet?)
2. **Groundedness** — Is the answer based on the retrieved documents? (Is the mechanic reading the manual, or guessing?)
3. **Answer Relevance** — Does the answer actually address the question? (Did the car go where you steered it?)

### First Wrench Turn — Quick Evaluation
Take your Day 7 system and write 10 test questions with known answers. For each:
1. Run the question through your RAG pipeline
2. Manually check: Did it retrieve relevant chunks? Is the answer grounded? Does it answer the question?
3. Score each dimension 0-1

### Tighten the Bolts
**Automated Evaluation with RAGAS or DeepEval**:
1. Install `ragas` or `deepeval`
2. Create a test dataset: 15 questions with expected answers and expected source documents
3. Run automated evaluation measuring faithfulness, context relevance, and answer relevance
4. Generate a report with scores
5. Identify your weakest dimension and improve it (better chunking? better prompt? more retrieved documents?)

**Chunking Experiment** (builds on Day 3 insights):
- Chunk the SAME document 3 different ways: fixed-500, recursive-1000, and recursive-500-with-200-overlap
- Run the SAME 10 questions against each
- Compare RAGAS scores — which chunking strategy works best for YOUR documents?

### Guidance:
- RAGAS quickstart: `from ragas import evaluate` with a dataset of questions, answers, contexts, and ground truths
- DeepEval alternative: `from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric`
- For the chunking experiment, create 3 separate ChromaDB collections (one per strategy) and query each
- Document your results in a markdown table — this IS your portfolio evidence

### Road Test Checklist
- [ ] 15 test questions with expected answers created
- [ ] Automated evaluation runs and produces scores
- [ ] At least 3 chunking strategies compared with metrics
- [ ] Results documented in a table
- [ ] Can articulate which chunking strategy works best and WHY

### Logbook Prompts
- What was your weakest RAG Triad dimension? How would you improve it?
- What surprised you about the chunking comparison?
- How would you set up continuous evaluation in production?

---

# PHASE 2: INTERMEDIATE (Days 9-20)
## "I can build agents that reason, use tools, and self-correct"

**What you're building toward**: By Day 20, you'll have a self-correcting research agent with LangGraph and a complete evaluation framework. These are the skills that separate tutorial-followers from AI engineers.

---

## Day 9: Simple ReAct Agent (No Frameworks)
**Mini-Project 8 | ~4 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> Until now, your AI has been a one-trick pony — you ask, it answers. An agent is different. It's like giving the mechanic a toolbox: "Here are wrenches, screwdrivers, and a diagnostic scanner. Figure out what the car needs and fix it yourself." The agent DECIDES which tool to use.

### The ReAct Pattern
> **Re**ason + **Act**. The agent thinks ("I need weather data"), acts (calls a weather API), observes the result, then thinks again. It's a loop: Thought → Action → Observation → repeat until done.

### First Wrench Turn — ReAct in 50 Lines
Build a ReAct agent in PURE PYTHON (no LangChain, no LangGraph):
1. Define 3 simple tools: `calculator(expression)`, `get_weather(city)` (mock it — return fake data), `search(query)` (mock it)
2. The agent receives a user query
3. It uses the LLM to generate a "Thought" (what it needs) and an "Action" (which tool to call with what arguments)
4. You execute the tool and feed the result back as an "Observation"
5. Loop until the LLM generates a "Final Answer"

### Tighten the Bolts
- Add a **max_iterations** limit (prevent infinite loops — cap at 5)
- Add **error handling**: what if the LLM outputs an invalid tool name?
- Add **logging**: print each Thought → Action → Observation step so you can see the agent's reasoning
- Test with 5 queries that require different tools:
  - "What's 15% of 340?" → calculator
  - "What's the weather in Cairo?" → get_weather
  - "Who invented the internet?" → search
  - "What's the weather in Tokyo in Fahrenheit?" → get_weather + calculator (multi-step!)
  - "Tell me a joke" → no tool needed (direct answer)

### Guidance:
- The "magic" is in the prompt. Tell the LLM: "You have access to these tools: [list]. For each step, output: Thought: ...\nAction: tool_name(args)\n. After receiving an Observation, continue reasoning. When you have the final answer, output: Final Answer: ..."
- Parse the LLM output with string matching (look for "Action:" and "Final Answer:")
- The multi-step query is the real test — the agent must call get_weather, then calculator to convert C to F

### Road Test Checklist
- [ ] Agent correctly routes to the right tool for each query
- [ ] Multi-step query (weather + conversion) works
- [ ] Direct answer queries don't trigger unnecessary tool calls
- [ ] Max iterations prevents infinite loops
- [ ] Full reasoning trace is logged

### Logbook Prompts
- What's the difference between a chain and an agent?
- How does the LLM "know" which tool to use? (Hint: it's all in the prompt)
- What happens when the LLM hallucinates a tool that doesn't exist?

---

## Days 10-11: LangGraph — Tool-Using Stateful Agent
**Mini-Project 9 | ~8-10 hours over 2 days | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> Your Day 9 agent was a solo mechanic with basic tools. LangGraph is like upgrading to a full shop with specialized stations — each station (node) does one thing, and the car (state) moves between stations based on what it needs. The shop manager (graph) decides the routing.

### Day 10: LangGraph Fundamentals

#### Warm the Engine
- Install: `pip install langgraph langchain-openai`
- Resource: [DeepLearning.AI — AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) (1.5 hrs, Free — code along)
- Also watch: [James Briggs — LangGraph 101](https://www.youtube.com/watch?v=qaWOwbFw3cs) (32 min)

#### First Wrench Turn — LangGraph Hello World
Build a simple LangGraph agent:
1. Define a `TypedDict` state with `messages` list
2. Create a "chatbot" node that calls the LLM
3. Create a "tools" node that executes tool calls
4. Wire them together with conditional edges (if LLM calls a tool → go to tools node → back to chatbot; if no tool call → end)
5. Give it 2-3 tools (web search mock, calculator, etc.)

#### Tighten the Bolts
- Add **state persistence**: save conversation state so the agent can resume
- Add **human-in-the-loop**: before executing a tool, ask the user "The agent wants to call X with Y. Allow? (y/n)"
- Visualize the graph: LangGraph can render the graph structure — print/display it

### Day 11: Self-Correcting RAG Agent (Corrective RAG)

#### The Big Build
Follow the [LangGraph CRAG Tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/) to build a self-correcting RAG agent:

The graph flow:
```
User Query → Retrieve Documents → Grade Relevance
  → If relevant: Generate Answer → Check Hallucination → If grounded: END
  → If irrelevant: Rewrite Query → Retrieve Again (max 2 retries) → Web Search Fallback
```

**Build these nodes** (each is a function that takes state, returns updated state):
1. `retrieve` — Gets documents from your vector store
2. `grade_documents` — Uses LLM to grade if each document is relevant to the query
3. `generate` — Generates answer from relevant documents
4. `transform_query` — Rewrites the query if documents were irrelevant
5. `web_search` — Falls back to web search (use Tavily API or mock it)
6. `check_hallucination` — Checks if the answer is grounded in the documents

**Wire conditional edges**:
- grade_documents → (relevant) generate / (irrelevant) transform_query
- transform_query → retrieve (max 2 rewrites, then web_search)
- check_hallucination → (grounded) END / (not grounded) generate (retry)

### Guidance:
- State is a `TypedDict`. Add fields: `question`, `documents`, `generation`, `web_search_needed`, `rewrite_count`
- Conditional edges use a function that inspects state and returns the next node name
- For document grading, use the LLM with a simple prompt: "Is this document relevant to the question? Answer 'yes' or 'no'."
- Cap rewrites at 2 to prevent infinite loops

### Road Test Checklist (Both Days)
- [ ] Basic LangGraph agent works with tools
- [ ] CRAG pipeline retrieves, grades, and generates correctly
- [ ] Irrelevant documents trigger query rewriting
- [ ] After 2 rewrites, falls back to web search
- [ ] Hallucination check catches ungrounded answers
- [ ] Graph visualization shows the full flow

### Logbook Prompts
- Why is LangGraph better than a simple chain for this use case?
- What's the difference between your Day 9 agent and the LangGraph agent?
- When would self-correction hurt more than it helps? (Think about latency/cost)

---

## Day 12: Agentic RAG — Multi-Source Intelligence
**Mini-Project 10 | ~5 hours | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> Your Day 11 agent searches ONE filing cabinet. Today's agent has access to THREE filing cabinets plus the internet. It DECIDES which to search based on the question — like a librarian who knows which section of the library to check.

### Build a Multi-Document Agent
1. Create 3 separate ChromaDB collections:
   - **Technical docs** — Python/AI documentation snippets
   - **FAQs** — Common Q&A pairs
   - **Policies** — Company policy documents (make up realistic ones)
2. Create 3 retriever tools, one per collection
3. Build a LangGraph agent that:
   - Analyzes the query to determine which collection(s) to search
   - Retrieves from the appropriate collection(s)
   - Synthesizes a combined answer when info comes from multiple sources
   - Falls back to web search when no collection has the answer

### Test Queries
Write 10 test queries spanning different scenarios:
- Single-source: "What's the refund policy?" → policies collection
- Multi-source: "How do I technically implement the refund policy?" → policies + technical
- None: "What's the weather in Cairo?" → web search fallback
- Ambiguous: "What's the policy on Python usage?" → could be policies OR technical

### Guidance:
- Each retriever is a LangGraph tool with a clear description. The LLM reads the descriptions to decide which to call.
- Tool descriptions matter enormously. "Searches technical documentation about Python, AI, and software engineering" is better than "Searches docs."
- For multi-source queries, the agent should call multiple tools in sequence, then synthesize.

### Road Test Checklist
- [ ] Agent correctly routes to the right collection for 8/10 queries
- [ ] Multi-source queries pull from multiple collections
- [ ] Web search fallback works for out-of-scope queries
- [ ] Source attribution shows which collection each piece of information came from

---

## Day 13: Custom Evaluation Framework
**Mini-Project 11 | ~5 hours | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> A good shop has a quality inspection station. Every car gets checked before it leaves — not by the mechanic who fixed it, but by an independent inspector. Today you build that inspection station for your AI systems.

### Build a Reusable Evaluation Harness
This is a cross-cutting tool you'll use for every project going forward:

1. **Test Case Format**: Define a JSON schema for test cases:
   - `question`: The input query
   - `expected_answer`: What the correct answer looks like
   - `expected_sources`: Which documents should be retrieved
   - `tags`: Categories (e.g., "factual", "reasoning", "multi-step")

2. **Runner**: A script that:
   - Loads test cases from JSON
   - Runs each through your RAG/Agent system
   - Collects: actual answer, retrieved documents, latency, token count

3. **Scorer**: Multiple scoring methods:
   - **LLM-as-Judge**: Use a second LLM to score answer quality (0-10)
   - **Semantic Similarity**: Compare actual vs expected answer embeddings
   - **Keyword Match**: Check if key facts appear in the answer

4. **Reporter**: Generate a markdown report with:
   - Overall scores by dimension
   - Worst-performing queries
   - Cost and latency statistics
   - Before/after comparisons (when you improve the system)

### Guidance:
- The LLM-as-Judge prompt: "You are an expert evaluator. Given the question, expected answer, and actual answer, score the actual answer from 0-10 on correctness and completeness. Explain your reasoning."
- Store results in a JSON file so you can track improvement over time
- This framework should work with ANY system — RAG, agent, or chain. Make it system-agnostic.

### Road Test Checklist
- [ ] 15+ test cases created in JSON format
- [ ] Runner executes all test cases and collects results
- [ ] LLM-as-Judge produces consistent, reasonable scores
- [ ] Markdown report generated with tables and statistics
- [ ] Framework is reusable (can evaluate any system by swapping the "system under test")

---

## Day 14: CI/CD and Monitoring for AI Apps
**Mini-Project 12 | ~5 hours | Difficulty: ⭐⭐**

### The Mechanic's Analogy
> You've built the car, tested it, and it runs great. But what happens when it's on the road 24/7? You need a maintenance schedule (CI/CD) and a dashboard (monitoring) to catch problems before they become breakdowns.

### CI/CD with GitHub Actions
1. Create a `.github/workflows/test.yml` that:
   - Runs on every push to main
   - Installs dependencies
   - Runs your evaluation harness (from Day 13) on a small test set
   - Fails the build if scores drop below a threshold

2. Create a simple deployment workflow:
   - Builds your Docker image
   - (Optionally) pushes to Docker Hub or GitHub Container Registry

### Monitoring Basics
Add monitoring to your FastAPI app (from Day 5):
1. **Latency tracking**: Log how long each request takes
2. **Token counting**: Log tokens used per request
3. **Cost estimation**: Calculate estimated cost per query
4. **Error rates**: Track and log errors
5. **Simple dashboard**: Build a Streamlit page that reads your logs and shows:
   - Average latency over time
   - Total tokens used today
   - Estimated daily cost
   - Error count

### Guidance:
- GitHub Actions: start from a template, don't write YAML from scratch
- For monitoring, start simple: log to a JSON file, then read it with Streamlit
- Calculate cost: `(input_tokens * input_price + output_tokens * output_price)` per model
- This doesn't need to be production-grade — the goal is understanding the CONCEPTS

### Road Test Checklist
- [ ] GitHub Actions workflow runs on push
- [ ] Tests pass/fail based on evaluation scores
- [ ] Monitoring logs are being written per request
- [ ] Dashboard shows latency, cost, and errors
- [ ] Can estimate monthly cost at various request volumes

---

## Days 15-16: Hybrid Search & Reranking
**Mini-Project 13 | ~8-10 hours over 2 days | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> Your search engine has one eye (semantic/vector search). Today you give it a second eye (keyword/BM25 search) and glasses (reranking). Two eyes see better than one — keyword search catches exact matches that semantic search misses, and vice versa.

### Day 15: Hybrid Search

**BM25 + Dense Vector Fusion**:
1. Install: `pip install rank_bm25`
2. Implement BM25 keyword search over your document chunks
3. Implement dense vector search (your existing ChromaDB setup)
4. Combine results using **Reciprocal Rank Fusion (RRF)**:
   - `RRF_score = sum(1 / (k + rank_i))` for each result list, where k=60
   - Documents that rank highly in BOTH lists get the highest combined score

**Test hybrid vs single-mode**:
Write 10 queries:
- 5 where semantic search wins (synonyms, paraphrases)
- 5 where keyword search wins (exact terms, acronyms, IDs)
- Show that hybrid search does well on ALL 10

### Day 16: Reranking + Query Techniques

**Cross-Encoder Reranking**:
1. Retrieve top-20 with hybrid search
2. Rerank to top-5 using a cross-encoder (use `sentence-transformers` cross-encoder model, or Cohere Rerank API)
3. Compare: top-5 from hybrid alone vs top-5 after reranking. Better?

**Advanced Query Techniques**:
1. **Multi-query**: Generate 3 variations of the user's question, retrieve for each, merge results
2. **HyDE**: Generate a hypothetical answer, embed THAT, search for similar documents
3. Compare both with standard single-query retrieval

### Guidance:
- RRF is simple math. For each document, look up its rank in each result list, apply the formula, sort by combined score.
- Cross-encoders: `from sentence_transformers import CrossEncoder` → `model.predict([(query, doc) for doc in candidates])`
- Multi-query: prompt the LLM with "Generate 3 different ways to ask this question: {original_question}"
- HyDE: prompt the LLM with "Write a short paragraph that would answer this question: {question}" → embed the paragraph → search

### Road Test Checklist
- [ ] BM25 search works independently
- [ ] Hybrid search (BM25 + dense) with RRF produces combined rankings
- [ ] Cross-encoder reranking improves result quality on at least 7/10 queries
- [ ] Multi-query and HyDE implemented and compared
- [ ] Results documented in comparison tables

---

## Days 17-18: Multi-Agent System
**Mini-Project 14 | ~8-10 hours over 2 days | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> One mechanic can fix a car. Three specialized mechanics — engine, electrical, bodywork — working together can fix it better and faster. Today you build a team of AI agents that collaborate on a task.

### Day 17: Agent Architecture

**Build a 3-Agent Research Team**:
- **Researcher Agent**: Given a subtopic, searches the web and knowledge base, returns findings
- **Writer Agent**: Takes research findings and writes a structured section
- **Reviewer Agent**: Reads the draft, identifies gaps, factual issues, and quality problems

**Orchestration with LangGraph**:
1. Define a state that includes: `topic`, `subtopics`, `research_findings`, `draft`, `review_feedback`, `final_report`
2. Build the graph:
   - Planner node → decomposes topic into subtopics
   - Researcher node → researches each subtopic (loop)
   - Writer node → produces draft from findings
   - Reviewer node → reviews draft
   - Conditional: if review passes → END; if fails → back to Researcher/Writer

### Day 18: Polish & Observe

**Add Observability**:
- Log every agent's input, output, and reasoning
- Track time and cost per agent
- Build a simple dashboard showing agent activity

**Test with Real Tasks**:
- "Write a 500-word report on the current state of RAG technology"
- "Research and summarize the pros and cons of LangChain vs LlamaIndex"
- "Create a comparison of 3 vector databases for production use"

### Guidance:
- Each agent is a LangGraph node with its own system prompt defining its role
- The Reviewer should output structured feedback: `{"passes": bool, "issues": [list], "suggestions": [list]}`
- Limit review iterations (max 2 rounds) to prevent infinite loops
- Consider cost: each agent call costs tokens. Track the total cost per task.

### Road Test Checklist
- [ ] All 3 agents function independently
- [ ] Orchestration graph routes correctly between agents
- [ ] Review loop catches real issues and triggers improvements
- [ ] 3 test tasks produce reasonable reports
- [ ] Cost per task tracked and documented

---

## Days 19-20: Fine-Tuning with QLoRA + Cloud Deployment
**Mini-Projects 15 & 16 | ~8-10 hours over 2 days | Difficulty: ⭐⭐⭐**

### Day 19: Fine-Tuning (Mini-Project 15)

### The Mechanic's Analogy
> So far you've been using stock engines (base models). Fine-tuning is like adding a turbocharger tuned for YOUR specific use case. You don't redesign the engine — you adjust it.

**Fine-Tune a Small Model**:
1. Choose a task: classification, extraction, or Q&A in a specific domain
2. Prepare a dataset: 50-200 examples in the correct format
3. Use OpenAI's fine-tuning API (simplest path):
   - Format data as JSONL: `{"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}`
   - Upload and start training
   - Test the fine-tuned model vs base model

**Alternative (local)**: If you have a GPU, use HuggingFace + QLoRA to fine-tune a small model (Phi-2 or similar). This is harder but impressive on a resume.

### Day 20: Cloud Deployment (Mini-Project 16)

**Deploy to the Cloud**:
1. Choose a platform: AWS (ECS), GCP (Cloud Run), or Railway/Render (simpler)
2. Push your Docker image
3. Deploy with environment variable configuration
4. Get a live URL that anyone can access
5. Test it from your phone

**Add Production Touches**:
- Rate limiting (prevent abuse)
- API key authentication (protect your endpoint)
- Health check endpoint
- Logging to a persistent store

### Road Test Checklist
- [ ] Fine-tuned model shows improvement over base model on your task
- [ ] Cloud deployment accessible via public URL
- [ ] API key authentication working
- [ ] Health check responds correctly
- [ ] Live demo works from a different device

---

# PHASE 3: ADVANCED (Days 21-28)
## "I can monitor, optimize, and harden production AI systems"

---

## Day 21: Model Monitoring & Drift Detection
**Mini-Project 17 | ~5 hours | Difficulty: ⭐⭐⭐**

### The Mechanic's Analogy
> A car fresh off the lot runs perfectly. After 50,000 miles, parts wear out. AI models drift the same way — the data they see in production gradually diverges from training data. Today you build the early warning system.

### Build Monitoring Infrastructure
1. Install Evidently AI: `pip install evidently`
2. Create a reference dataset (what "normal" looks like)
3. Simulate production data with gradual drift
4. Build dashboards showing:
   - Output quality degradation over time
   - Data distribution shifts
   - Anomaly detection
5. Set up alerts: when drift exceeds threshold → notification

### Guidance:
- Evidently has prebuilt reports for data drift, classification performance, and text quality
- Simulate drift by gradually changing the topic distribution of incoming queries
- This is a proof-of-concept — in production, you'd connect this to real request logs

### Road Test Checklist
- [ ] Reference dataset established
- [ ] Drift detection identifies simulated shifts
- [ ] Dashboard visualizes drift over time
- [ ] Alert triggers when drift exceeds threshold

---

## Days 22-27: Capstone Projects

### Days 22-24: Capstone 1 — Domain-Specific RAG Knowledge Assistant
**~12-15 hours over 3 days**

**This is your flagship portfolio project.** Not a generic "chat with PDF" — a specialized RAG system for a real domain.

**Requirements**:
- Multi-format ingestion (PDF with tables, web pages, markdown)
- Semantic chunking with tuned overlap (document your experiments!)
- Hybrid search (BM25 + dense) with cross-encoder reranking
- Agentic fallback to web search when corpus doesn't have the answer
- RAGAS evaluation showing faithfulness >0.85, context precision >0.80
- Streamlit interface with source attribution
- Docker containerization
- README with architecture diagram, results table, design decisions

**Day 22**: Ingestion pipeline + chunking experiments
**Day 23**: Retrieval (hybrid + reranking) + generation + evaluation
**Day 24**: UI + Docker + README + polish

### Days 25-26: Capstone 2 — Multi-Agent Research System
**~10-12 hours over 2 days**

**Build an autonomous research system** where specialized agents collaborate:
- Planner: decomposes topic into sub-questions
- Researchers: gather info from multiple sources
- Analyst: synthesizes findings
- Writer: produces structured report with citations
- Critic: reviews for quality

**Requirements**:
- LangGraph orchestration with conditional routing
- Full observability (log every agent decision)
- Cost metering per agent per task
- Guardrails (input validation, output safety)
- Evaluation metrics: task completion rate, quality scores
- Architecture diagram in README

**Day 25**: Agent nodes + graph wiring + basic flow
**Day 26**: Observability + evaluation + README + polish

### Day 27: Capstone 3 — MLOps Platform
**~5-6 hours**

**Wrap Capstone 1 or 2 in production infrastructure**:
- GitHub Actions CI/CD: push → test → evaluate → deploy
- Docker + Docker Compose deployment
- MLflow experiment tracking (if applicable)
- Monitoring dashboard (latency, cost, errors)
- Load testing results
- Rollback strategy documented
- Cost analysis at various scales

---

## Day 28: Portfolio Polish & Documentation
**~4-5 hours**

### For Each Capstone
1. **README**: Title → Problem Statement → Architecture Diagram → Live Demo Link → Results Table → Tech Stack → Setup Instructions → Design Decisions → Evaluation Results → Future Improvements
2. **Live Demo**: Deploy to Streamlit Cloud, Hugging Face Spaces, or a cloud service
3. **Architecture Diagram**: Create with Mermaid or Excalidraw
4. **Results**: Bold your quantified metrics — "Reduced hallucination from 23% to 7%"

---

# PHASE 4: INTERVIEW PREP (Days 29-40)
## "I can explain everything I built and design systems on a whiteboard"

---

## Days 29-32: Interview Question Deep Dive

### Day 29: RAG Pipeline Questions (20 questions)
Study and practice answering the RAG questions from `AI-Engineer-Interview-100-Questions-Answers.md` (Q1-Q20). For each:
- Read the answer
- Close the file and explain it OUT LOUD in your own words
- If you can't explain it clearly, go back and re-read

### Day 30: AI Agents & LangGraph Questions (20 questions)
Same process for Q21-Q40 (Agents topic).

### Day 31: LLM Fundamentals Questions (20 questions)
Same process for Q41-Q60 (LLM Fundamentals).

### Day 32: MLOps + Production + Traditional ML (40 questions)
Same process for Q61-Q100 (MLOps and ML).

---

## Days 33-36: System Design Practice

### Day 33: RAG System Design
Practice designing a RAG system from scratch on paper:
- Draw the architecture
- Explain every component choice
- Discuss trade-offs
- Handle follow-up questions: "What if the corpus grows to 1M documents?" "How do you handle multi-language?"

### Day 34: Agent System Design
Practice designing an agent system:
- When to use agents vs chains
- How to prevent infinite loops
- How to handle failures gracefully
- How to optimize cost

### Day 35: Production Architecture
Practice designing production AI infrastructure:
- CI/CD pipeline for ML
- Monitoring and alerting
- Scaling strategies
- Cost optimization

### Day 36: Mock Interview
Do a full mock interview (with a friend, or use ChatGPT as interviewer):
- 5 min intro
- 15 min technical deep-dive (RAG or Agents)
- 15 min system design
- 10 min behavioral

---

## Days 37-40: Final Preparation

### Day 37: Project Walkthroughs
Practice 5-minute walkthroughs of each capstone project:
- What problem does it solve?
- What's the architecture?
- What were the key design decisions?
- What are the results/metrics?
- What would you improve?

### Day 38: Weakness Areas
Identify your weakest topic from the 100 questions and spend the day strengthening it.

### Day 39: Live Demo Practice
Make sure you can demo each capstone smoothly:
- Capstone 1: Ask a question, show source documents, show evaluation scores
- Capstone 2: Show agent reasoning trace, demonstrate self-correction
- Capstone 3: Show CI/CD pipeline, monitoring dashboard, deployment

### Day 40: Rest and Review
- Light review of key concepts
- Get a good night's sleep
- You've built 20 mini-projects, 3 capstones, and studied 100 interview questions
- **You're ready.**

---

# Appendix: Resource Schedule

| Day | Primary Resource | Time |
|-----|-----------------|------|
| 1 | OpenAI API docs + Streamlit quickstart | 30 min reading |
| 2 | DeepLearning.AI Prompt Engineering course | 1.5 hrs video |
| 3 | freeCodeCamp RAG From Scratch (first 45 min) | 45 min video |
| 4 | DeepLearning.AI Vector Databases course | 55 min video |
| 5 | FastAPI tutorial + Docker quickstart | 30 min reading |
| 6 | DeepLearning.AI LangChain course (lessons 1-4) | 1 hr video |
| 7 | DeepLearning.AI LangChain Chat with Data (lessons 1-3) | 30 min video |
| 8 | RAGAS/DeepEval documentation | 30 min reading |
| 9 | — (build from concepts) | — |
| 10 | DeepLearning.AI AI Agents in LangGraph | 1.5 hrs video |
| 10 | James Briggs LangGraph 101 | 32 min video |
| 11 | LangGraph CRAG Tutorial | 1 hr reading |
| 12 | DeepLearning.AI Agentic RAG with LlamaIndex | 44 min video |
| 15 | rank_bm25 + sentence-transformers docs | 30 min reading |
| 17 | DeepLearning.AI Multi-Agent Systems with CrewAI (lessons 1-3) | 30 min video |
| 19 | OpenAI Fine-tuning guide OR HuggingFace QLoRA guide | 1 hr reading |
| 29-32 | AI-Engineer-Interview-100-Questions-Answers.md | Self-study |

**Total Video/Reading**: ~12 hours (spread across 40 days)
**Total Build Time**: ~160-200 hours
**Build-to-Learn Ratio**: ~90/10 (this is a Mechanic curriculum)

---

# Quick Reference: What You Build Each Day

| Day | Mini-Project | What You Have After |
|-----|-------------|-------------------|
| 1 | Hello LLM Chatbot | Working chatbot with Streamlit UI |
| 2 | Prompt Engineering Toolkit | 8 prompt pattern scripts + structured extractor |
| 3 | RAG from Scratch | Working RAG with manual embeddings (no framework) |
| 4 | Semantic Search Engine | ChromaDB-powered search over 50+ documents |
| 5 | FastAPI + Docker | Containerized search API |
| 6-7 | LangChain RAG | Multi-document Q&A with source attribution |
| 8 | Evaluation Framework | RAGAS-scored RAG with chunking experiments |
| 9 | ReAct Agent | Pure Python agent with 3 tools |
| 10-11 | LangGraph CRAG Agent | Self-correcting RAG with conditional routing |
| 12 | Agentic RAG | Multi-source agent that routes queries |
| 13 | Evaluation Harness | Reusable eval framework for any AI system |
| 14 | CI/CD + Monitoring | GitHub Actions pipeline + monitoring dashboard |
| 15-16 | Hybrid Search + Reranking | BM25+dense fusion with cross-encoder reranking |
| 17-18 | Multi-Agent System | 3-agent research team with orchestration |
| 19 | Fine-Tuned Model | QLoRA fine-tuned model beating base model |
| 20 | Cloud Deployment | Live, authenticated API endpoint |
| 21 | Monitoring & Drift | Evidently AI drift detection dashboard |
| 22-24 | **Capstone 1** | **Production RAG Knowledge Assistant** |
| 25-26 | **Capstone 2** | **Multi-Agent Research System** |
| 27 | **Capstone 3** | **MLOps Platform** |
| 28 | Portfolio Polish | 3 deployable projects with READMEs |
| 29-40 | Interview Prep | 100 questions mastered + system design skills |

---

**You've got this, Ahmed. 40 days. 20 builds. 3 capstones. One portfolio that stands out.**
