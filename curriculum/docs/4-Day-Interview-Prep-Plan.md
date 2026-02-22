# The 32-Hour AI Engineer Interview Prep: 4-Day Plan

**Goal**: Go from zero RAG/agent experience to interview-ready in 4 days  
**Structure**: 8 hours/day × 4 days = 32 hours  
**Philosophy**: Build first, understand deeply after — every block ends with working code  
**Companion**: See `AI-Engineer-Interview-Resource-Collection.md` for all URLs and alternatives

---

## Before You Start (30 min setup, night before Day 1)

**Environment Setup**:
1. Install Python 3.10+, create a virtual environment
2. Get an OpenAI API key ($5 credit is enough for 4 days): [platform.openai.com](https://platform.openai.com)
3. Install core packages: `pip install openai langchain langchain-openai chromadb faiss-cpu langchain-community`
4. Install project packages: `pip install streamlit python-dotenv tiktoken`
5. Create `.env` file with `OPENAI_API_KEY=sk-...`
6. Optional: Get a free [Anthropic API key](https://console.anthropic.com/) for Claude comparison

**Mindset**: You are building 3 portfolio projects over 4 days. Each day ends with something you can demo and explain in an interview.

---

# DAY 1: Foundations — Prompt Engineering, LLM APIs, Embeddings & Vectors
**Hours 1–8 | Theme: "I can talk to AI and search through documents"**

---

## Block 1: Prompt Engineering (Hours 1–2.5)

### Watch + Code Along (1.5 hours)
**Resource**: [DeepLearning.AI — ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) (1h 30m, Free)

Work through all lessons in the browser notebooks. Don't just watch — modify every prompt and observe changes.

### Mini-Project 1: Prompt Engineering Notebook (1 hour)

**Build**: A Jupyter notebook with 10 categorized prompt patterns.

Write Python code that demonstrates each pattern using the OpenAI API:

```
prompt_patterns/
├── 01_zero_shot.py          # "Classify this review as positive/negative: ..."
├── 02_few_shot.py           # Provide 3 examples, then new input
├── 03_chain_of_thought.py   # "Let's think step by step..."
├── 04_system_role.py        # System message defining persona + constraints
├── 05_structured_output.py  # Force JSON output with schema
├── 06_temperature_test.py   # Same prompt at temp 0.0 vs 0.7 vs 1.0
├── 07_react_pattern.py      # Thought → Action → Observation loop
├── 08_openai_vs_claude.py   # Same prompt to both APIs, compare responses
├── 09_token_counting.py     # Count tokens with tiktoken, estimate cost
└── 10_prompt_chaining.py    # Output of prompt 1 → input of prompt 2
```

**What you'll explain in interview**: "I built a systematic prompt engineering toolkit demonstrating 10 patterns. I learned that CoT prompting dramatically improves multi-step reasoning, that temperature 0 gives deterministic outputs for structured tasks, and that Claude's system prompt goes in a separate parameter while OpenAI's is a message role."

---

## Block 2: LLM APIs Deep Dive (Hours 2.5–4)

### Watch + Code Along (1 hour)
**Resource**: [DeepLearning.AI — LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/) — Watch lessons 1-4 only (Models/Prompts/Parsers, Memory, Chains). **1 hour of the 1h 38m course**

### Mini-Project 2: Multi-Provider LLM Client (30 min)

**Build**: A Python class that calls OpenAI and Anthropic with the same interface.

```python
# multi_llm_client.py
# - Unified ask() function that takes provider="openai" or provider="anthropic"
# - Handles streaming responses from both
# - Implements exponential backoff retry (3 attempts)
# - Logs token usage and estimated cost
# - Falls back to Anthropic if OpenAI fails (and vice versa)
```

**What you'll explain in interview**: "Both APIs use a messages-based chat format, but Claude takes the system prompt as a separate parameter. I implemented fallback logic because production systems need resilience — if one provider has an outage, the other takes over."

### Mini-Project 3: Structured Output Extractor (30 min)

**Build**: An LLM that extracts structured data from unstructured text.

```python
# structured_extractor.py
# - Takes a restaurant review as input
# - Extracts: restaurant_name, cuisine, rating, price_range, pros, cons
# - Uses OpenAI JSON mode OR function calling
# - Validates output with Pydantic model
# - Handles malformed LLM output with retry logic
```

**What you'll explain in interview**: "I used Pydantic to define the expected output schema, then passed it to the LLM via function calling. This guarantees type-safe, parseable responses. When the LLM occasionally returns malformed JSON, the retry logic re-prompts with the error message."

---

## Block 3: Embeddings & Vector Databases (Hours 4–6)

### Watch + Code Along (1 hour)
**Resource**: [DeepLearning.AI — Vector Databases: from Embeddings to Applications](https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/) (55m, Free)

### Mini-Project 4: Semantic Search Engine (1 hour)

**Build**: A semantic search engine over a collection of 50+ text documents.

```python
# semantic_search/
# ├── embed_documents.py    # Load 50+ text snippets, embed with OpenAI, store in FAISS
# ├── search.py             # Query interface: input text → top-5 similar results
# ├── compare_metrics.py    # Compare cosine similarity vs L2 distance results
# └── visualize.py          # (optional) t-SNE/UMAP visualization of embedding space
```

Steps:
1. Create a file with 50+ text snippets (movie descriptions, FAQ answers, or product descriptions)
2. Embed all documents using `text-embedding-3-small`
3. Store in a FAISS index (`IndexFlatIP` for cosine similarity)
4. Build a query function that embeds the query and retrieves top-k
5. Compare results with keyword search (exact match) to show semantic advantage

**What you'll explain in interview**: "Embeddings capture semantic meaning — 'happy' and 'joyful' have high cosine similarity even though they share no characters. I used FAISS with IndexFlatIP for exact nearest-neighbor search. In production with millions of documents, you'd switch to HNSW or IVF for approximate search — trading a small amount of recall for O(log n) query time instead of O(n)."

---

## Block 4: LangChain Foundations + Day 1 Integration (Hours 6–8)

### Watch + Code Along (1 hour)
**Resource**: [DeepLearning.AI — LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/) — Watch remaining lessons 5-7 (QA, Agents, Evaluation). **38 min remaining**

Plus: [DeepLearning.AI — LangChain: Chat with Your Data](https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/) — Watch lessons 1-3 only (Document loading, splitting, vectorstores). **30 min**

### Mini-Project 5: Document Q&A Chain (1 hour)

**Build**: A LangChain chain that answers questions about a PDF document.

```python
# doc_qa/
# ├── load_and_split.py    # Load PDF with PyPDFLoader, split with RecursiveCharacterTextSplitter
# ├── create_vectorstore.py # Embed chunks, store in Chroma (persistent)
# ├── qa_chain.py           # RetrievalQA chain: query → retrieve → generate
# └── main.py               # CLI interface: ask questions, see source documents
```

This is your **first RAG pipeline** (even though we formalize RAG tomorrow). You're experiencing the pattern before learning the theory.

**What you'll explain in interview**: "This is a basic RAG pipeline using LangChain. I split the PDF into chunks using RecursiveCharacterTextSplitter with 1000-char chunks and 200-char overlap — recursive splitting tries paragraph boundaries first, then sentences, then words. Retrieved chunks are injected into the prompt as context."

---

## Day 1 Evening: Interview Prep Review (30 min at home)

Read through these and write your own 2-sentence answers:
- What are embeddings and why do they matter for search?
- What's the difference between cosine similarity and L2 distance?
- Explain the OpenAI chat completions API message format
- What is temperature and how does it affect outputs?
- What's the difference between OpenAI and Anthropic APIs?

---

# DAY 2: RAG Pipelines Deep Dive — The Main Event
**Hours 9–16 | Theme: "I can build and evaluate a production RAG system"**

---

## Block 1: RAG Theory + First Complete Pipeline (Hours 9–11.5)

### Watch + Code Along (2.5 hours)
**Resource**: [Lance Martin — RAG From Scratch on freeCodeCamp](https://www.youtube.com/watch?v=sVcwVQRHIc8) (2h 30m)

This is the cornerstone. Code along with the notebooks from [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch). Cover at minimum: indexing, retrieval, generation, multi-query, RAG-Fusion, and HyDE.

---

## Block 2: Advanced Retrieval Techniques (Hours 11.5–13.5)

### Watch (1 hour)
**Resource**: [DeepLearning.AI — Building and Evaluating Advanced RAG](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) — Focus on sentence-window retrieval, auto-merging retrieval, and the RAG Triad evaluation framework. **1 hour of 1h 55m**

### Mini-Project 6: Chunking Strategy Comparison (1 hour)

**Build**: A notebook that chunks the same document 4 different ways and compares retrieval quality.

```python
# chunking_comparison/
# ├── document.txt           # A 10+ page document (use any technical doc or Wikipedia article)
# ├── fixed_chunking.py      # Split every 500 tokens with 100 overlap
# ├── recursive_chunking.py  # RecursiveCharacterTextSplitter (paragraph → sentence → word)
# ├── semantic_chunking.py   # Use embedding similarity to detect topic shifts
# ├── evaluate.py            # 10 test questions → retrieve from each strategy → compare
# └── results.md             # Which strategy returned the most relevant chunks?
```

Steps:
1. Load a long document (10+ pages)
2. Chunk it with 4 strategies (fixed-500, fixed-1000, recursive-1000, semantic)
3. Store each in a separate Chroma collection
4. Write 10 test questions with known answers
5. Retrieve top-3 chunks from each collection for each question
6. Manually score: does the retrieved chunk contain the answer?

**What you'll explain in interview**: "I compared 4 chunking strategies on the same document. Fixed-size chunking is fastest but breaks mid-sentence. Recursive chunking respects paragraph boundaries and gave the best results for my dataset. Semantic chunking groups by topic shifts — it's best when a document has clear topic changes but adds embedding cost during ingestion. The right strategy depends on your document structure."

---

## Block 3: Capstone Project 1 — RAG Application with Evaluation (Hours 13.5–17)

### 🏗️ CAPSTONE PROJECT 1: Document Q&A with RAG Triad Evaluation

**Build time**: 3.5 hours  
**What you'll build**: A complete RAG application over your own documents (PDFs) with a Streamlit chat interface and automated evaluation.

```
rag_capstone/
├── README.md                 # Architecture diagram + design decisions
├── requirements.txt
├── .env
├── ingest.py                 # PDF loading → recursive chunking → OpenAI embeddings → Chroma
├── retriever.py              # Similarity search with optional reranking
├── generator.py              # LLM generation with retrieved context injection
├── evaluator.py              # RAG Triad: context relevance, groundedness, answer relevance
├── app.py                    # Streamlit chat UI
├── test_questions.json       # 15 test questions with expected answers
└── data/
    └── documents/            # 3-5 PDF files (your resume, a technical paper, any docs)
```

**Step-by-step build order**:

1. **Ingestion pipeline** (45 min): Load PDFs with PyPDFLoader. Chunk with RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200). Embed with text-embedding-3-small. Store in Chroma with persistence.

2. **Retrieval + Generation** (45 min): Build retriever (top-k=4 with similarity search). Implement prompt template that injects retrieved chunks. Add source attribution (which document/page each answer came from).

3. **RAG Triad Evaluation** (45 min): Following [Mete Atamel's DeepEval tutorial](https://github.com/meteatamel/genai-beyond-basics/tree/main/samples/evaluation/deepeval/rag_eval), implement 3 metrics:
   - **Context Relevance**: Are retrieved chunks relevant to the question?
   - **Groundedness**: Is the answer supported by the retrieved chunks?
   - **Answer Relevance**: Does the answer actually address the question?

4. **Streamlit UI** (30 min): Simple chat interface with source display. Show which chunks were retrieved for each answer.

5. **Testing + README** (45 min): Run 15 test questions, record evaluation scores. Write README with architecture diagram and results.

### Design Decisions You'll Explain in Interview

**"Why RecursiveCharacterTextSplitter over fixed-size?"**  
"Recursive splitting tries paragraph boundaries first, then sentences, then words. This preserves semantic coherence within chunks. Fixed-size splitting is simpler but breaks mid-thought, which degrades retrieval quality."

**"Why chunk_size=1000 and overlap=200?"**  
"1000 tokens gives enough context for the LLM to understand the passage without exceeding the context window budget. 200-token overlap prevents information loss at chunk boundaries — if an answer spans two chunks, the overlap ensures at least one chunk contains the complete information."

**"Why top-k=4 instead of top-k=10?"**  
"More chunks means more context for the LLM, but also more noise and higher token cost. I found 4 chunks gave the best balance of recall and precision for my document set. In production, you'd tune this with your evaluation metrics."

**"How would you improve retrieval quality?"**  
"Three approaches: (1) Add a reranker — a cross-encoder like Cohere Rerank scores query-document pairs more accurately than embedding similarity. (2) Implement hybrid search — combine dense vector search with sparse BM25 via Reciprocal Rank Fusion. (3) Use multi-query retrieval — generate 3 variations of the question and merge results."

**"What's the RAG Triad and why does it matter?"**  
"It evaluates three dimensions: Is the context relevant? Is the answer grounded in that context? Does the answer address the question? Without evaluation, you can't tell if your RAG system is hallucinating, retrieving irrelevant documents, or generating off-topic answers."

---

## Day 2 Evening: Interview Prep Review (30 min)

Write your own answers to these questions:
- Walk me through a RAG pipeline end-to-end
- What chunking strategies exist and when would you use each?
- How do you evaluate a RAG system?
- What is HyDE and when would you use it?
- What's the difference between dense retrieval and hybrid search?
- How would you handle a RAG system that hallucinates?

---

# DAY 3: AI Agents & LangGraph — Autonomous Systems
**Hours 17–24 | Theme: "I can build agents that reason, use tools, and self-correct"**

---

## Block 1: Agent Fundamentals (Hours 17–19)

### Watch + Code Along (1.5 hours)
**Resource**: [DeepLearning.AI — AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) (1h 32m, Free)

This covers: building agents from scratch, LangGraph components, human-in-the-loop, persistence. Code along with every notebook.

### Mini-Project 7: ReAct Agent from Scratch (30 min)

**Build**: A simple ReAct agent in pure Python (no frameworks) that uses tools.

```python
# react_agent/
# ├── agent.py           # ReAct loop: Thought → Action → Observation → repeat
# ├── tools.py           # 3 tools: calculator, web_search (mock), get_weather (mock)
# └── main.py            # Run agent with 5 test queries
```

The agent receives a query, thinks about what tool to use, calls the tool, observes the result, and either answers or calls another tool. Implement the loop in ~50 lines of Python.

**What you'll explain in interview**: "ReAct interleaves reasoning and action. The LLM generates a Thought (what it needs), an Action (which tool to call), gets an Observation (tool result), and iterates. This is the core loop behind every agent framework — LangGraph, CrewAI, and LlamaIndex all implement variations of this pattern."

---

## Block 2: LangGraph Deep Dive (Hours 19–21)

### Watch (30 min)
**Resource**: [James Briggs — LangGraph 101](https://www.youtube.com/watch?v=qaWOwbFw3cs) (32 min)

### Follow Official Tutorial (1.5 hours)
**Resource**: [LangGraph — Corrective RAG (CRAG) Tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/)

Work through the complete CRAG tutorial. This builds a graph where:
- Retrieve documents → Grade relevance → If irrelevant, rewrite query → Web search fallback → Generate

### Mini-Project 8: Self-Correcting RAG Agent (included in tutorial)

The CRAG tutorial IS the mini-project. When you finish, you have a working self-correcting RAG agent with conditional routing. Save your implementation.

---

## Block 3: Agentic RAG + Multi-Agent Systems (Hours 21–23)

### Watch + Code Along (45 min)
**Resource**: [DeepLearning.AI — Building Agentic RAG with LlamaIndex](https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/) (44m, Free)

### Watch (30 min — selective viewing)
**Resource**: [DeepLearning.AI — Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/) — Watch lessons 1-3 only (Multi-agent concepts, role definitions, delegation patterns). **30 min of 2h 41m**

### Mini-Project 9: Multi-Document Agent (45 min)

**Build**: An agent that can query across 3 different document collections and synthesize answers.

```python
# multi_doc_agent/
# ├── collections/
# │   ├── technical_docs/    # Collection 1: Technical documentation
# │   ├── faqs/              # Collection 2: FAQ documents
# │   └── policies/          # Collection 3: Policy documents
# ├── agent.py               # LangGraph agent with 3 retriever tools
# ├── router.py              # Routes queries to the right collection(s)
# └── main.py                # Test with queries that need info from multiple collections
```

**What you'll explain in interview**: "The agent has access to 3 retriever tools, one per document collection. For a query like 'What's the refund policy and how do I technically implement it?', the agent routes to both the policy and technical collections, retrieves from each, and synthesizes a combined answer. This is agentic RAG — the LLM decides which tools to call rather than always retrieving from a single source."

---

## Block 4: Capstone Project 2 — Research Agent (Hours 23–25)

### 🏗️ CAPSTONE PROJECT 2: Self-Correcting Research Agent with LangGraph

**Build time**: 2 hours  
**What you'll build**: A research agent that searches documents, evaluates relevance, rewrites queries if needed, and generates grounded answers with self-reflection.

```
research_agent/
├── README.md                  # Architecture diagram (draw the graph!)
├── requirements.txt
├── .env
├── graph.py                   # LangGraph StateGraph definition
├── nodes/
│   ├── retrieve.py            # Retrieves documents from vector store
│   ├── grade_documents.py     # Grades if retrieved docs are relevant to query
│   ├── generate.py            # Generates answer from relevant docs
│   ├── transform_query.py     # Rewrites query if documents were irrelevant
│   ├── web_search.py          # Tavily web search fallback (or mock it)
│   └── check_hallucination.py # Checks if answer is grounded in documents
├── state.py                   # TypedDict state definition
├── tools.py                   # Tool definitions
├── app.py                     # Streamlit interface showing graph execution steps
└── test_queries.json          # 10 test queries with expected behaviors
```

**Step-by-step build order**:

1. **Define state** (15 min): Create TypedDict with fields: question, documents, generation, web_search_needed, query_rewrite_count

2. **Build nodes** (45 min): Each node is a function that takes state and returns updated state. Follow the CRAG + Self-RAG patterns from the official tutorials

3. **Wire the graph** (30 min): Connect nodes with conditional edges:
   - retrieve → grade_documents
   - grade_documents → (relevant) generate / (irrelevant) transform_query
   - transform_query → retrieve (max 2 rewrites, then web_search)
   - generate → check_hallucination
   - check_hallucination → (grounded) END / (not grounded) generate

4. **Add Streamlit UI** (15 min): Show each step of the graph execution. Display which nodes fired and what decisions were made

5. **Test + document** (15 min): Run 10 test queries, verify self-correction works

### Design Decisions You'll Explain in Interview

**"Why LangGraph instead of a simple chain?"**  
"Chains are linear — query → retrieve → generate. But real-world queries sometimes retrieve irrelevant documents. LangGraph lets me add conditional routing: if retrieved docs score below a relevance threshold, the query gets rewritten and we try again. This self-correction loop dramatically improves answer quality."

**"How does the document grading work?"**  
"I use the LLM itself as a grader — it receives the query and each retrieved document and outputs 'yes' or 'no' for relevance. This is cheaper than a cross-encoder reranker and works surprisingly well. In production, you'd fine-tune a small model specifically for grading."

**"When would you use an agent vs a simple RAG chain?"**  
"Use a simple chain when the query type is predictable and documents are from a single source. Use an agent when: (1) queries might need multiple data sources, (2) retrieval quality varies and self-correction helps, (3) the system needs to decide between retrieval and web search, or (4) multi-step reasoning is required."

**"How do you prevent infinite loops in the agent?"**  
"I cap query rewrites at 2 attempts. If documents are still irrelevant after 2 rewrites, it falls back to web search. The state tracks query_rewrite_count and the conditional edge checks this. In production, you'd also add a timeout and total token budget."

---

## Day 3 Evening: Interview Prep Review (30 min)

Write your own answers:
- Explain the ReAct pattern
- What is LangGraph and how is it different from LangChain?
- When would you use an agent vs a chain?
- What is Corrective RAG?
- Compare LangChain, LlamaIndex, and CrewAI — when would you use each?
- What is human-in-the-loop and why does it matter for agents?

---

# DAY 4: MLOps, Traditional ML & Interview Readiness
**Hours 25–32 | Theme: "I can deploy models, track experiments, and explain everything"**

---

## Block 1: MLOps Fundamentals (Hours 25–27.5)

### Watch + Code Along (1.5 hours — selective)
**Resource**: [DataTalks.Club MLOps Zoomcamp — Module 2: Experiment Tracking](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK) — Watch Module 2 videos only (MLflow tracking, model registry). **~1.5 hours**

GitHub materials: [DataTalksClub/mlops-zoomcamp/02-experiment-tracking](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/02-experiment-tracking)

### Mini-Project 10: Docker Basics for ML (30 min)

**Build**: A Dockerfile that packages a simple ML model for serving.

```dockerfile
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model/ ./model/
COPY serve.py .
EXPOSE 8000
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# serve.py — FastAPI endpoint
# POST /predict → takes features as JSON → returns prediction
# GET /health → returns {"status": "healthy"}
```

**What you'll explain in interview**: "Docker packages the model with its exact environment — Python version, dependencies, model weights — into a portable container. This eliminates 'works on my machine' problems. The Dockerfile uses a slim base image to minimize container size, and I expose a health endpoint for load balancer checks."

---

## Block 2: Capstone Project 3 — MLflow-Tracked Model (Hours 27.5–30)

### 🏗️ CAPSTONE PROJECT 3: XGBoost Model with Full MLflow Tracking

**Build time**: 2.5 hours  
**What you'll build**: A complete ML pipeline with experiment tracking, hyperparameter tuning, model registry, and basic CI/CD concepts.

```
mlflow_capstone/
├── README.md                 # MLOps architecture diagram
├── requirements.txt
├── Dockerfile
├── data/
│   └── dataset.csv           # Any tabular dataset (use sklearn's built-in or download one)
├── src/
│   ├── preprocess.py         # Data cleaning, feature engineering, train/test split
│   ├── train.py              # XGBoost training with MLflow tracking
│   ├── tune.py               # Hyperparameter search (grid or random) logged to MLflow
│   ├── evaluate.py           # Evaluate best model, log metrics + confusion matrix
│   ├── register.py           # Register best model in MLflow Model Registry
│   └── serve.py              # FastAPI endpoint using registered model
├── mlruns/                   # MLflow tracking data (auto-generated)
└── tests/
    └── test_pipeline.py      # Basic tests for preprocessing and prediction
```

**Step-by-step build order**:

1. **Data + Preprocessing** (30 min): Use a dataset (sklearn's California Housing, or download from Kaggle). Clean data, engineer 2-3 features (e.g., interaction terms, binning). Split 80/20.

2. **MLflow Tracking** (30 min): 
   ```python
   import mlflow
   mlflow.set_experiment("xgboost-housing")
   with mlflow.start_run():
       mlflow.log_params({"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1})
       model = xgb.XGBRegressor(**params)
       model.fit(X_train, y_train)
       predictions = model.predict(X_test)
       mlflow.log_metrics({"rmse": rmse, "mae": mae, "r2": r2})
       mlflow.sklearn.log_model(model, "model")
   ```

3. **Hyperparameter Tuning** (30 min): Run 10+ experiments with different hyperparameter combinations. All logged automatically to MLflow. Compare runs in the MLflow UI.

4. **Model Registry** (15 min): Register the best model, transition to "Staging" then "Production" stage.

5. **FastAPI Serving** (30 min): Load the production model from MLflow registry, create `/predict` endpoint.

6. **Dockerfile + README** (15 min): Containerize the serving app. Document the full pipeline.

### Design Decisions You'll Explain in Interview

**"What is MLflow and why use it?"**  
"MLflow tracks experiments — every training run logs parameters, metrics, and model artifacts. When I ran 15 hyperparameter combinations, I could compare them in the MLflow UI and see exactly which configuration gave the best RMSE. The model registry provides versioning and stage management (staging → production)."

**"Explain your CI/CD concept for ML"**  
"The pipeline would be: push code → GitHub Actions runs tests → triggers training → evaluates against baseline → if better, registers new model → deploys with canary strategy (10% traffic to new model). This is Continuous Training — the model automatically retrains when data drift is detected or performance drops."

**"Why XGBoost for this problem?"**  
"XGBoost excels on tabular data — it handles missing values natively, provides feature importance, and trains fast. For tabular problems, gradient boosting consistently outperforms deep learning. LightGBM would be 5-10x faster for very large datasets, and CatBoost would be better if I had many categorical features."

**"What is data drift and how do you detect it?"**  
"Data drift means the production data distribution has shifted from training data. Detection methods include PSI (Population Stability Index) for feature distributions, and monitoring prediction confidence over time. Tools like Evidently AI automate this. When drift is detected, you trigger retraining."

---

## Block 3: Traditional ML Refresher (Hours 30–31)

### Watch (1 hour — selective)
**Resource**: [StatQuest — XGBoost Playlist](https://www.youtube.com/playlist?list=PLblh5JKOoLULU0irPgs1SnKO6wqVjKUsQ) — Watch Parts 1 and 4 (Regression + Python walkthrough). **~1 hour of the full series**

### Transformer Quick Understanding (30 min — optional, if time allows)
**Resource**: [Andrej Karpathy — Let's Build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Watch the self-attention explanation segment (timestamp ~20:00–50:00 only). **30 min of 1h 56m**

---

## Block 4: Interview Simulation & Final Prep (Hours 31–32)

### Practice Explaining Your Projects Out Loud (1 hour)

This is the most important hour of the entire 4 days. Set a timer and practice answering these questions out loud (not in your head — speaking forces you to organize your thoughts):

**5-minute walkthrough questions** (practice each one):

1. **"Walk me through how you'd build a RAG system from scratch."**
   - Start: "I'd begin with the ingestion pipeline — loading documents, chunking them with RecursiveCharacterTextSplitter..."
   - Cover: chunking strategy choice, embedding model, vector store, retrieval (top-k selection), prompt augmentation, generation, evaluation with RAG Triad
   - End: "For production, I'd add reranking, hybrid search, and monitoring for answer quality degradation"

2. **"Your RAG system is giving wrong answers. How do you debug it?"**
   - Check retrieval first (are the right chunks being retrieved?)
   - Check the prompt (is the context being injected correctly?)
   - Check generation (is the LLM grounding its answer in the context?)
   - Mention: RAG Triad evaluation pinpoints which stage is failing

3. **"When would you use an agent instead of a simple chain?"**
   - Simple chain: predictable queries, single data source, linear flow
   - Agent: multiple tools/sources, variable query types, need for self-correction, multi-step reasoning
   - Give your capstone example: "My research agent decides between document retrieval and web search based on document relevance scores"

4. **"Explain your MLOps pipeline."**
   - Experiment tracking with MLflow → model registry → containerization with Docker → CI/CD with GitHub Actions → monitoring
   - Mention Continuous Training concept

5. **"Compare LangChain, LlamaIndex, and CrewAI."**
   - LangChain/LangGraph: Graph-based orchestration, best for complex workflows with conditional routing
   - LlamaIndex: Data-first, best when the agent primarily searches and synthesizes from private data
   - CrewAI: Role-based multi-agent, best for collaborative tasks requiring team-like delegation
   - "I'd use LangGraph for branching business logic, CrewAI for rapid multi-agent prototyping, LlamaIndex for data-heavy retrieval"

### Final 30 Minutes: Review Your Portfolio

Make sure you can quickly demo each project:
- **Project 1 (RAG App)**: Show the Streamlit UI, ask a question, show source documents, show evaluation scores
- **Project 2 (Research Agent)**: Show the graph execution steps, demonstrate self-correction when irrelevant documents are retrieved
- **Project 3 (MLflow)**: Show the MLflow UI with experiment comparisons, show the model registry, hit the FastAPI endpoint

---

# Summary: What You Built Over 4 Days

## 3 Capstone Projects
| # | Project | Demonstrates | Interview Topics |
|---|---------|-------------|-----------------|
| 1 | RAG App with Evaluation | End-to-end RAG pipeline + RAG Triad metrics | Chunking, retrieval, evaluation, production improvements |
| 2 | Research Agent | LangGraph self-correcting agent with conditional routing | Agent architectures, ReAct, tool use, when agents vs chains |
| 3 | MLflow-Tracked Model | Full ML lifecycle with experiment tracking + Docker | MLOps, experiment tracking, deployment, CI/CD concepts |

## 7 Mini-Projects
| # | Mini-Project | Day | Time | Key Skill |
|---|-------------|-----|------|-----------|
| 1 | Prompt Engineering Notebook | 1 | 1h | 10 prompt patterns with code |
| 2 | Multi-Provider LLM Client | 1 | 30m | OpenAI + Claude unified interface |
| 3 | Structured Output Extractor | 1 | 30m | Pydantic + JSON mode |
| 4 | Semantic Search Engine | 1 | 1h | FAISS + embeddings |
| 5 | Document Q&A Chain | 1 | 1h | First RAG with LangChain |
| 6 | Chunking Strategy Comparison | 2 | 1h | 4 strategies evaluated |
| 7 | ReAct Agent from Scratch | 3 | 30m | Agent loop in pure Python |
| 8 | Self-Correcting RAG (CRAG) | 3 | 1.5h | LangGraph conditional routing |
| 9 | Multi-Document Agent | 3 | 45m | Agentic RAG across collections |
| 10 | Docker for ML | 4 | 30m | Containerized model serving |

## Total Watch Time vs Build Time
| Activity | Hours | % |
|----------|-------|---|
| Watch/Learn | 14 | 44% |
| Build (projects + mini-projects) | 15 | 47% |
| Interview practice | 3 | 9% |
| **Total** | **32** | **100%** |

---

# Post-Sprint: If You Have Extra Days

**Day 5-6 (Optional — deeper practice)**:
- Complete Ed Donner's Udemy LLM Engineering course ($14) — builds 8 more projects
- Work through [LangChain Academy Intro to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) — all 6 modules for deeper agent mastery
- Run through interview question banks: [RAG Questions](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub), [LLM Questions](https://github.com/llmgenai/LLMInterviewQuestions)
- Read [Chip Huyen's ML Interviews Book](https://huyenchip.com/ml-interviews-book/) for ML fundamentals review

**Day 7 (Optional — mock interview)**:
- Practice with a friend or use ChatGPT as interviewer
- Do a complete 45-minute mock: 5 min intro → 15 min technical deep-dive → 15 min system design → 10 min behavioral
- Record yourself and watch it back

---

**Good luck with the interview. You've got this. 🚀**
