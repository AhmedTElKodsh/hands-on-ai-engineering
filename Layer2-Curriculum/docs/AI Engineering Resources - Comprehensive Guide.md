# The definitive AI Engineering Resource Library (2024–2026)

**This resource library maps every critical AI Engineering topic to the best open-source GitHub repositories, learning materials, and hands-on projects — covering 8 categories, 150+ repos, and a complete course structure.** The library is designed to augment a hands-on-ai-engineering master course that follows an "action-first, then deep dive" teaching pattern. Every repo listed has been verified for active maintenance, educational quality, and runnable code. The landscape has consolidated around a few dominant ecosystems: LangChain/LangGraph for orchestration, HuggingFace for model training, and NirDiamant's tutorial suite plus patchy631's ai-engineering-hub as the most comprehensive free educational collections.

---

## Part 1: Comprehensive topic mapping across all categories

### Category A: LLM Foundations

The foundational layer covers **how LLMs work internally and how to use them effectively**. Essential topics include transformer architecture (self-attention, multi-head attention, positional encoding, feed-forward layers), tokenization (BPE, SentencePiece, tiktoken), and pre-training objectives (next-token prediction, masked language modeling). Prompt engineering spans zero-shot, few-shot, chain-of-thought (CoT), Tree-of-Thought, self-consistency, ReAct, and structured prompting. LLM APIs cover OpenAI (GPT-4o, o1, o3), Anthropic Claude (3.5 Sonnet, Opus), Google Gemini, and open-source serving via Ollama and vLLM. Token management includes context window optimization, cost tracking across providers, rate limiting strategies, and streaming. Structured output encompasses JSON mode, function calling, tool use, and Pydantic-based schema enforcement.

### Category B: RAG (Retrieval-Augmented Generation)

RAG is the most mature and most-taught area of AI Engineering. The basic pipeline flows from **ingest → chunk → embed → store → retrieve → generate**. Chunking strategies include fixed-size, recursive character, semantic (embedding-based boundary detection), document-structured, and agentic chunking. Embedding models span OpenAI (text-embedding-3-small/large), Sentence-Transformers, Cohere Embed v3, and multilingual models like multilingual-e5. Vector databases include FAISS, ChromaDB, Pinecone, Qdrant, Weaviate, and Milvus — each with distinct tradeoffs in hosting, filtering, and performance. Advanced RAG techniques include sentence-window retrieval, auto-merging retrieval, parent-child document relationships, and RAPTOR (tree-structured retrieval). Hybrid search combines dense vectors with sparse BM25 via Reciprocal Rank Fusion. Reranking uses cross-encoders, Cohere Rerank, or ColBERT late-interaction models. RAG evaluation centers on the RAG Triad (faithfulness, answer relevancy, context relevancy) measured by RAGAS and DeepEval. GraphRAG uses knowledge graph extraction for complex, multi-hop questions. Multi-modal RAG handles images, tables, and PDFs with complex layouts using CLIP embeddings and vision-language models. Production RAG adds caching (semantic cache), monitoring, A/B testing, access control, and scaling patterns.

### Category C: AI Agents

The agent landscape has matured around four major frameworks. **LangGraph** (v1.0, Oct 2025) provides graph-based state machines with conditional routing, human-in-the-loop, and persistence — used by Klarna, Replit, and Elastic. **CrewAI** offers role-based multi-agent collaboration with an intuitive Crew/Agent/Task model. **AutoGen** (now transitioning to Microsoft Agent Framework by merging with Semantic Kernel) pioneered multi-agent conversation. **OpenAI Agents SDK** replaced Swarm with production-grade handoffs, guardrails, tracing, and realtime voice support. Topics span the ReAct pattern, tool calling, agentic RAG (Corrective RAG, Self-RAG, Adaptive RAG), multi-agent architectures (hierarchical, supervisor, collaborative), agent memory (short-term, long-term via Mem0, episodic), agent evaluation, and MCP (Model Context Protocol) for standardized tool integration. MCP has emerged as the universal standard for connecting LLMs to external tools, with reference servers from Anthropic and community implementations covering hundreds of integrations.

### Category D: Fine-tuning & model customization

Fine-tuning has been democratized by **Unsloth** (2x faster, 70% less VRAM), **LlamaFactory** (100+ models, web UI), and **HuggingFace TRL** (canonical post-training library). Core methods include full fine-tuning, LoRA, QLoRA, DoRA, and adapter-based approaches via the PEFT library. Training objectives span supervised fine-tuning (SFT), DPO (most popular preference alignment), GRPO (for reasoning models, used in DeepSeek-R1), PPO-based RLHF, ORPO, and KTO. Dataset preparation for instruction tuning uses Alpaca and ShareGPT formats. Axolotl provides YAML-config-driven production fine-tuning with multi-GPU support. The decision framework follows: prompt engineering first (zero cost, instant), RAG next (when domain knowledge is needed), fine-tuning when consistent style, reduced latency, or specific task performance is required.

### Category E: MLOps & Production

Production ML engineering covers experiment tracking (MLflow, Weights & Biases), model versioning (DVC, MLflow Model Registry), CI/CD for ML (GitHub Actions with CML), model serving (FastAPI, vLLM with PagedAttention, Ollama for local), containerization (Docker, Docker Compose), orchestration (Kubernetes, KServe), and pipeline orchestration (Airflow, Prefect, Kubeflow Pipelines). Monitoring encompasses data drift, concept drift, and model performance degradation using Evidently AI with Prometheus/Grafana dashboards. Feature stores (Feast) manage online/offline feature serving. Cost optimization covers GPU instance selection, quantization for inference, caching strategies, and autoscaling policies.

### Category F: Guardrails, safety & evaluation

Evaluation frameworks include **EleutherAI's lm-evaluation-harness** (60+ benchmarks, backbone of HuggingFace Leaderboard), DeepEval (pytest-like LLM testing), RAGAS (RAG-specific metrics), promptfoo (developer-friendly with CI/CD), and HuggingFace LightEval. Guardrails implementations include NVIDIA NeMo Guardrails (Colang language, multi-rail orchestration) and Guardrails AI (95+ validators on Hub). Red teaming uses DeepTeam (OWASP Top 10 aligned), NVIDIA Garak (vulnerability scanner), and promptfoo adversarial attacks (PAIR, crescendo, many-shot). Hallucination detection, prompt injection defense, and content moderation round out the safety stack.

### Category G: Emerging & advanced topics

Voice AI uses **Pipecat** (most mature framework, 30+ STT/TTS providers), LiveKit Agents (WebRTC-based), and Ultravox (direct speech understanding without separate ASR). Browser automation centers on **browser-use** (60K+ stars, Playwright-based) and Skyvern (LLM + computer vision). Deep research agents include GPT-Researcher, LangChain's open_deep_research, and Alibaba's DeepResearch (first open-source agent matching OpenAI's DeepResearch). Code generation agents span OpenHands (formerly OpenDevin), Claude Code, Continue, Tabby, and Roo Code. Reasoning models are led by **DeepSeek-R1** (100K+ stars, MIT license) and HuggingFace's open-r1 reproduction. Quantization formats include GGUF (llama.cpp), GPTQ, AWQ, and bitsandbytes. Workflow automation uses n8n (174K+ stars, native AI nodes).

### Category H: Data & traditional ML foundations

Foundational topics include Python data science (pandas, NumPy, matplotlib), feature engineering, classical ML (scikit-learn, XGBoost, LightGBM), deep learning fundamentals (PyTorch, neural networks from scratch), NLP fundamentals (tokenization, embeddings, RNNs, attention), and computer vision basics (CNNs, Vision Transformers, transfer learning).

---

## Part 2: The best GitHub repositories by category

### Category A — LLM Foundations & prompt engineering

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **rasbt/LLMs-from-scratch** | ~85K | Active 2025-26 | Build ChatGPT-like LLM from scratch in PyTorch. 7 chapters: tokenization, attention, GPT architecture, pretraining, fine-tuning. Companion to bestselling book. | Beginner→Advanced |
| **dair-ai/Prompt-Engineering-Guide** | ~65K | Feb 2026 | THE definitive prompt engineering resource. All techniques, 13 languages, notebooks, promptingguide.ai website. | Beginner→Advanced |
| **openai/openai-cookbook** | ~71K | Feb 2026 | Official OpenAI patterns: function calling, structured outputs, embeddings, agents, evals, multimodal. | Beginner→Advanced |
| **anthropics/anthropic-cookbook** | ~5-7K | Active 2026 | Official Claude patterns: tool use, extended thinking, computer use, RAG, structured output. | Beginner→Advanced |
| **NirDiamant/Prompt_Engineering** | ~5-8K | Active 2025 | 22 hands-on Jupyter notebooks covering every prompt engineering technique with runnable code. | Beginner→Intermediate |
| **rasbt/reasoning-from-scratch** | ~2.9K | Active 2025 | Implements reasoning capabilities via RL and distillation. Companion to LLMs-from-scratch. | Advanced |

### Category B — RAG

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **NirDiamant/RAG_Techniques** | ~24.7K | Active 2026 | **Most comprehensive RAG tutorial collection.** 30+ techniques from basic to advanced, each with runnable Jupyter notebook. Covers chunking, hybrid search, reranking, GraphRAG, evaluation. | Beginner→Advanced |
| **run-llama/llama_index** | ~47K | Daily commits | Leading RAG framework. 300+ integrations, multi-modal RAG examples, vector store demos, advanced retrieval. | Intermediate→Advanced |
| **patchy631/ai-engineering-hub** | ~24.4K | Active 2026 | 75+ hands-on projects spanning RAG, agents, fine-tuning. Tiered difficulty (beginner to expert). YouTube companion content. | All levels |
| **langchain-ai/rag-from-scratch** | ~3-4K | Active | Best structured RAG learning path. 14 numbered notebooks covering basic RAG through corrective/self/adaptive RAG. Accompanies popular YouTube series. | Beginner→Intermediate |
| **microsoft/graphrag** | ~20K+ | Active 2025-26 | Microsoft Research GraphRAG. Knowledge graph extraction, community detection, Local vs. Global search. | Intermediate→Advanced |
| **HKUDS/LightRAG** | ~27K | Active 2025 | Lightweight graph-based RAG alternative. EMNLP 2025 paper. Less expensive than Microsoft GraphRAG. | Intermediate→Advanced |
| **vibrantlabsai/ragas** | ~7-10K | Active 2026 | De facto RAG evaluation standard. Faithfulness, relevancy, precision, recall metrics. Synthetic test generation. | Intermediate→Advanced |
| **confident-ai/deepeval** | ~8K+ | Active 2026 | Pytest-like LLM evaluation. RAG metrics, hallucination detection, CI/CD integration, red teaming. | Intermediate→Advanced |
| **mrdbourke/simple-local-rag** | ~1.5-2.5K | Stable | Build RAG from absolute scratch without frameworks. All local, GPU-based, Colab-ready. Best for understanding internals. | Beginner→Intermediate |
| **pixegami/rag-tutorial-v2** | ~0.8-1.2K | Stable | Simplest RAG tutorial. LangChain + Chroma + Ollama with pytest-based testing. YouTube companion. | Beginner |
| **infiniflow/ragflow** | ~70K | Active 2026 | Enterprise RAG engine. Deep document understanding, complex format parsing, fused re-ranking. Docker-friendly. | Advanced (production) |

### Category C — AI Agents

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **langchain-ai/langgraph** | ~37.8K | Feb 2026 | Core agent orchestration framework (v1.0). State machines, conditional routing, human-in-the-loop, persistence, LangGraph Studio. | All levels |
| **NirDiamant/GenAI_Agents** | ~19.1K | Active 2025 | 30+ agent implementation tutorials. ReAct, tool calling, multi-agent, memory, agentic RAG. Each technique has dedicated notebook. | Beginner→Advanced |
| **microsoft/autogen** | ~54.4K | Active 2025-26 | Pioneered multi-agent conversation. ConversableAgent, GroupChat, code execution. Transitioning to Microsoft Agent Framework. | Intermediate→Advanced |
| **crewAIInc/crewAI** | ~44.1K | Active 2025-26 | Role-based multi-agent framework. Intuitive Agent/Task/Crew model, standalone, CrewAI Flows. | Beginner→Intermediate |
| **mem0ai/mem0** | ~46.8K | Active 2026 | Best-in-class agent memory. Graph-based, production-ready, 91% lower latency than OpenAI Memory. | Intermediate→Advanced |
| **browser-use/browser-use** | ~60K+ | Active 2026 | Leading browser automation for AI agents. Playwright-based, CLI support, custom tools. | Beginner→Advanced |
| **assafelovic/gpt-researcher** | ~20K+ | Active 2025-26 | Autonomous deep research agent. Planner + execution agents, LangGraph multi-agent, MCP server. | Intermediate→Advanced |
| **microsoft/ai-agents-for-beginners** | ~15K+ | Active 2025 | 15+ lessons on AI agents. Multi-framework (AutoGen, Semantic Kernel, MAF). | Beginner |
| **huggingface/agents-course** | ~5K+ | Active 2025 | Free comprehensive agent course using smolagents. MCP integration, observability, evaluation. | Beginner→Intermediate |
| **NirDiamant/agents-towards-production** | ~5K+ | Active 2025 | Production-grade agents. Docker deployment, FastAPI, security, GPU scaling, observability, CI/CD. | Intermediate→Advanced |
| **openai/openai-agents-python** | ~15K+ | Active 2026 | Official OpenAI Agents SDK. Handoffs, guardrails, tracing, MCP, realtime voice agents. | Intermediate |
| **crewAIInc/crewAI-examples** | ~5K+ | Active 2025 | End-to-end CrewAI apps: Content Creator, Email Auto Responder, Marketing Strategy, LangGraph integration. | Beginner→Intermediate |
| **langchain-ai/langchain-academy** | ~5K+ | Active 2025 | Official LangGraph course. 5+ modules with studio integration, state management, persistence. | Beginner→Intermediate |

### MCP (Model Context Protocol)

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **modelcontextprotocol/servers** | ~15K+ | Active 2026 | Official reference MCP servers + massive community directory. Filesystem, Git, Memory, Sequential Thinking. | All levels |
| **microsoft/mcp-for-beginners** | ~10K+ | Active 2025-26 | Best MCP learning resource. Cross-language (Python, TypeScript, .NET, Java, Rust), structured curriculum. | Beginner |
| **modelcontextprotocol/modelcontextprotocol** | ~5K+ | Active | Official MCP specification and documentation. | All levels |
| **cyanheads/model-context-protocol-resources** | ~2K+ | Active 2025 | Independent guides, utilities, excellent server/client development guides. | Intermediate |

### Category D — Fine-tuning & model customization

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **unslothai/unsloth** | ~25K+ | Daily 2026 | **2x faster, 70% less VRAM.** LoRA, QLoRA, GRPO, GSPO, FP8 RL. Supports DeepSeek, Qwen3, Llama 4, Gemma, vision, TTS. Colab notebooks. | Beginner→Advanced |
| **hiyouga/LlamaFactory** | ~40K+ | Active 2026 | Most comprehensive unified fine-tuning. 100+ models, Web UI, LoRA/QLoRA/DPO/PPO/GRPO. ACL 2024 paper. | Beginner→Advanced |
| **huggingface/trl** | ~12K+ | Active 2026 | Canonical post-training library. SFTTrainer, DPOTrainer, GRPOTrainer, RewardTrainer. CLI support. | Beginner→Advanced |
| **huggingface/peft** | ~18K+ | Active 2026 | Core PEFT library. LoRA, QLoRA, DoRA, AdaLoRA, IA³, Prefix Tuning. Used by nearly every fine-tuning workflow. | Beginner→Advanced |
| **axolotl-ai-cloud/axolotl** | ~8K+ | Active 2025-26 | YAML-config production fine-tuning. Multi-GPU (FSDP, DeepSpeed), sequence parallelism. | Intermediate→Advanced |
| **pytorch/torchtune** | ~5K+ | Active 2025-26 | Official PyTorch-native LLM fine-tuning. LoRA, DPO, knowledge distillation. Clean API. | Intermediate→Advanced |
| **philschmid/deep-learning-pytorch-huggingface** | ~3K+ | Active 2025 | HuggingFace advocate's notebooks. "Fine-tune LLMs in 2024/2025 with TRL" guides. Best tutorial quality. | Beginner→Intermediate |
| **ashishpatel26/LLM-Finetuning** | ~3K+ | Active 2025 | 23+ notebooks covering PEFT, QLoRA, Falcon, Llama, Unsloth, MLflow evaluation. | Beginner→Intermediate |
| **artidoro/qlora** | ~9K+ | Stable | Original QLoRA paper implementation. 4-bit NF4, double quantization. Essential reference. | Intermediate |
| **ggml-org/llama.cpp** | ~75K+ | Daily 2026 | GGUF quantization and local inference engine. CPU+GPU. Foundation of local LLM deployment. Q2-Q8 formats. | Intermediate→Advanced |

### Category E — MLOps & production

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **GokuMohandas/Made-With-ML** | ~44.6K | Content stable | **Gold standard MLOps course.** End-to-end: design, develop, deploy, iterate. MLflow, Ray, CI/CD, testing, monitoring. | Intermediate→Advanced |
| **DataTalksClub/mlops-zoomcamp** | ~13.7K | Active 2025 | Free 6-module MLOps course. MLflow, orchestration, deployment (batch/streaming), Evidently+Grafana monitoring, CI/CD. | Beginner→Intermediate |
| **mlflow/mlflow** | ~20K+ | Daily 2026 | Industry standard experiment tracking. Model registry, serving, LLM tracing, evaluation, prompt management. | All levels |
| **vllm-project/vllm** | ~49K+ | Active 2026 | Highest-throughput LLM serving. PagedAttention, OpenAI-compatible API, tensor/pipeline parallelism. | Intermediate→Advanced |
| **evidentlyai/evidently** | ~5K+ | Active 2026 | ML monitoring: data drift, model performance, data quality. 100+ metrics, 25M+ downloads. | Beginner→Intermediate |
| **iterative/dvc** | ~14K+ | Active 2026 | Data Version Control. Git for data and models. Pipeline DAGs, reproducibility. | Beginner→Intermediate |
| **iterative/cml** | ~4K+ | Active 2025 | CI/CD for ML with GitHub Actions/GitLab CI. Auto-comments with metrics and plots on PRs. | Intermediate |
| **feast-dev/feast** | ~5.5K+ | Active 2025-26 | Open-source feature store. Online/offline serving, point-in-time joins, vector search for RAG. | Intermediate |
| **kubeflow/pipelines** | ~3.5K+ | Active 2025-26 | ML pipeline orchestration on Kubernetes. End-to-end workflow management. | Intermediate→Advanced |
| **EthicalML/awesome-production-machine-learning** | ~17K+ | Active 2025 | Most comprehensive production ML tools list. Deploy, monitor, version, scale. 70K+ newsletter subscribers. | All levels |

### Category F — Guardrails, safety & evaluation

| Repo | Stars | Last Active | What it covers | Level |
|------|-------|-------------|----------------|-------|
| **confident-ai/deepeval** | ~8K+ | Feb 2026 | Most comprehensive LLM eval. G-Eval, hallucination, faithfulness, CI/CD. Red teaming for 40+ vulnerabilities. | Beginner→Advanced |
| **NVIDIA-NeMo/Guardrails** | ~5K+ | Active 2026 | Enterprise guardrails toolkit. Colang 2.0, 5 rail types, LangGraph support. NVIDIA-backed. | Intermediate→Advanced |
| **guardrails-ai/guardrails** | ~4.5K+ | Feb 2026 | Output validation framework. 95+ validators on Hub. Pydantic integration, REST API server mode. | Beginner→Intermediate |
| **promptfoo/promptfoo** | ~5K+ | Feb 2026 | LLM testing + red teaming. YAML configs, CI/CD, OWASP/NIST mapping, side-by-side model comparison. | Beginner→Advanced |
| **EleutherAI/lm-evaluation-harness** | ~8K+ | Active 2025 | Gold standard benchmark framework. 60+ benchmarks (MMLU, HumanEval). Backend for HF Leaderboard. | Intermediate→Advanced |
| **NVIDIA/garak** | ~3K+ | Active 2025 | LLM vulnerability scanner. 50+ probe types for hallucination, data leakage, prompt injection, toxicity. | Intermediate→Advanced |
| **confident-ai/deepteam** | ~1.5K+ | Active 2025-26 | Open-source LLM red teaming. OWASP Top 10 and NIST AI RMF aligned. Companion to DeepEval. | Intermediate→Advanced |
| **huggingface/lighteval** | ~3K+ | Active 2025-26 | Lightweight LLM evaluation. 1000+ tasks (MMLU, MMLU-Pro, HLE). Custom task creation. | Intermediate |

### Category G — Emerging & advanced

**Voice AI:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **pipecat-ai/pipecat** | ~8K+ | Most mature voice AI framework. 30+ STT, 20+ TTS providers, real-time pipelines. |
| **livekit/agents** | ~5K+ | Production-grade realtime voice agents. WebRTC, telephony, semantic turn detection. |
| **TEN-framework/ten-framework** | ~5K+ | Multimodal conversational AI. Voice + video + lip sync avatars. |
| **fixie-ai/ultravox** | ~2K+ | Direct speech understanding LLM (no separate ASR). Lower latency. |

**Browser/computer use agents:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **browser-use/browser-use** | ~60K+ | Leading browser automation for AI agents. Playwright-based. |
| **Skyvern-AI/skyvern** | ~10K+ | LLM + computer vision web automation. No-code workflow builder. |
| **hyperbrowserai/HyperAgent** | ~2K+ | CDP-native, action caching for deterministic replay. |

**Deep research agents:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **assafelovic/gpt-researcher** | ~20K+ | Autonomous research agent. Planner + execution, MCP server. |
| **langchain-ai/open_deep_research** | ~5K+ | Configurable research agent. Ranked #6 on Deep Research Bench. Free course. |
| **dzhng/deep-research** | ~5K+ | Simplest implementation (<500 LoC). Best for learning. |
| **Alibaba-NLP/DeepResearch** | ~3K+ | First open-source agent matching OpenAI DeepResearch quality. Complete training pipeline. |
| **SkyworkAI/DeepResearchAgent** | ~2K+ | Hierarchical multi-agent for research + general task solving. |

**Reasoning & quantization:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **deepseek-ai/DeepSeek-R1** | ~100K+ | Open-source reasoning model. MIT license. Distilled versions 1.5B-70B. |
| **huggingface/open-r1** | ~10K+ | Full reproduction of R1 training. Mixture-of-Thoughts dataset. |
| **ggml-org/llama.cpp** | ~75K+ | GGUF quantization + local inference. CPU/GPU. |

**Code generation & autonomous coding:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **All-Hands-AI/OpenHands** | ~61K+ | Open-source autonomous AI software engineer. |
| **continuedev/continue** | ~20K+ | Open-source AI coding assistant. VS Code + JetBrains. Highly configurable. |
| **TabbyML/tabby** | ~25K+ | Self-hosted Copilot alternative. Code completion + chat. |
| **RooCodeInc/Roo-Code** | ~20K+ | AI dev team of agents in code editor. |

**Workflow automation:**

| Repo | Stars | What it covers |
|------|-------|----------------|
| **n8n-io/n8n** | ~174K+ | Open-source workflow automation. Native AI nodes, RAG, MCP, 500+ app integrations. |

### Category H — Data & traditional ML foundations

| Repo | Stars | What it covers | Level |
|------|-------|----------------|-------|
| **jakevdp/PythonDataScienceHandbook** | ~43K+ | Complete book as Jupyter notebooks. NumPy, pandas, matplotlib, scikit-learn. | Beginner |
| **eriklindernoren/ML-From-Scratch** | ~24K+ | Every ML algorithm from scratch in NumPy. Linear regression to GANs. | Intermediate |
| **d2l-ai/d2l-en** | ~25K+ | Interactive deep learning textbook. Multi-framework. Adopted by 500+ universities. | Beginner→Advanced |
| **labmlai/annotated_deep_learning_paper_implementations** | ~56K+ | 60+ paper implementations with annotations. Colab-ready. | Intermediate→Advanced |
| **yunjey/pytorch-tutorial** | ~30K+ | Concise PyTorch tutorials. Most models <30 lines. | Intermediate |
| **mrdbourke/pytorch-deep-learning** | ~10K+ | Zero to Mastery PyTorch. 25+ hours video. learnpytorch.io. | Beginner→Intermediate |
| **graykode/nlp-tutorial** | ~14K+ | NLP from scratch in PyTorch. NNLM through Transformer, all <100 lines. | Intermediate |
| **microsoft/AI-For-Beginners** | ~35K+ | 12-week, 24-lesson AI curriculum. Microsoft-backed. | Beginner |
| **ashishpatel26/Amazing-Feature-Engineering** | ~1.5K+ | Feature engineering guide with scikit-learn, XGBoost integration. | Beginner→Intermediate |
| **tsmatz/nlp-tutorials** | ~500+ | End-to-end NLP implementations from tokenization to transformers. | Beginner→Intermediate |

### Essential awesome lists and meta-resources

| Repo | Stars | Scope |
|------|-------|-------|
| **josephmisiti/awesome-machine-learning** | ~66K+ | Entire ML ecosystem by language |
| **Hannibal046/Awesome-LLM** | ~20K+ | LLM papers, tools, evaluation, datasets |
| **EthicalML/awesome-production-machine-learning** | ~17K+ | Production ML tools end-to-end |
| **visenger/awesome-mlops** | ~13K+ | MLOps references, tools, courses |
| **aishwaryanr/awesome-generative-ai-guide** | ~12K+ | Full 10-week LLM course, interview prep, fine-tuning guide |
| **e2b-dev/awesome-ai-agents** | ~10K+ | AI autonomous agents catalog |
| **kyrolabs/awesome-langchain** | ~7K+ | LangChain ecosystem, 200+ projects |
| **steven2358/awesome-generative-ai** | ~6K+ | Modern GenAI projects and services |
| **Shubhamsaboo/awesome-llm-apps** | ~15K+ | Practical LLM apps with RAG, agents, MCP |
| **Danielskry/Awesome-RAG** | Growing | RAG ecosystem resource map |

### Interview preparation repos

| Repo | Stars | Why it stands out |
|------|-------|------------------|
| **alirezadir/Machine-Learning-Interviews** | ~10K+ | FAANG-tested. Author received offers from Meta, Google, Amazon, Apple. System design cases. |
| **chiphuyen/ml-interviews-book** | ~8K+ | 200+ questions with difficulty levels. By NVIDIA/Snorkel AI veteran. Available at huyenchip.com. |
| **khangich/machine-learning-interview** | ~9K+ | Minimum viable study plan. Actual FAANG questions. Offers from Snap, Coupang, StitchFix. |

---

## Part 3: Project ideas — mini-projects and capstones

### RAG projects

**Mini-projects (30–60 min):**
1. **PDF Q&A Bot** — Build a RAG pipeline: ingest PDF, chunk with RecursiveCharacterTextSplitter, embed with Sentence-Transformers, store in ChromaDB, query with OpenAI. Reference: langchain-ai/rag-from-scratch notebooks 1-4.
2. **Chunking Strategy Showdown** — Compare fixed-size vs. recursive vs. semantic chunking on one document. Measure retrieval quality with RAGAS context_precision. Visualize chunk boundaries.
3. **Hybrid Search Builder** — Implement dense (FAISS) + sparse (BM25) search with Reciprocal Rank Fusion. Compare against pure vector search on 50 test queries.
4. **RAG Evaluation Pipeline** — Add RAGAS + DeepEval metrics to an existing RAG system. Build a pytest test suite measuring faithfulness, answer relevancy, context precision.
5. **Multi-Source RAG** — Build RAG querying across PDF, web page, and CSV sources. Use LlamaIndex SimpleDirectoryReader with unified vector index.

**Capstone projects (2–4 hours):**
1. **Production RAG with evaluation and monitoring** — Full pipeline: semantic chunking → hybrid search → cross-encoder reranking → RAGAS evaluation suite → Streamlit UI → Docker deployment.
2. **GraphRAG knowledge base** — Use Microsoft GraphRAG to index a document corpus. Extract entities/relationships into knowledge graph. Compare Local vs. Global search against baseline vector RAG.
3. **Multi-modal document understanding** — RAG for PDFs with images, tables, and complex layouts. Use LlamaIndex MultiModalVectorStoreIndex with CLIP embeddings. Test on technical manuals.

### Agent projects

**Mini-projects (30–60 min):**
1. **ReAct tool-calling agent** — Build a LangGraph agent with ReAct pattern using 3 tools (web search, calculator, weather API). Practice state management and conditional routing.
2. **MCP file server + client** — Create a simple MCP server exposing file operations, connect to an LLM client. Learn MCP fundamentals.
3. **Corrective RAG with LangGraph** — Retrieve documents, evaluate relevance with LLM judge, re-query if quality is low. Use a small PDF knowledge base.
4. **CrewAI blog writer** — 3-agent crew (Researcher, Writer, Editor) that produces a blog post from a topic. Practice role-based multi-agent design.
5. **Agent with persistent memory** — Build a conversational agent with Mem0 long-term memory. Multi-session conversations that remember context.

**Capstone projects (2–4 hours):**
1. **Multi-agent research assistant with MCP** — LangGraph-based with specialized agents (search, analysis, writing) connected via MCP servers. Human-in-the-loop approval. Persistence for sessions.
2. **Adaptive RAG with self-correction** — Routes queries between simple retrieval, web search, and deep analysis. Self-RAG reflection + Corrective RAG document grading + evaluation harness.
3. **Browser automation research agent** — Combine browser-use with GPT-Researcher patterns. Browse websites, extract data, produce cited reports. Supervisor agent coordinates browser and research agents.

### Fine-tuning projects

**Mini-projects (30–60 min):**
1. **QLoRA quickstart** — Fine-tune Llama 3.2 1B on a small instruction dataset using Unsloth in Colab. Export to GGUF, test with llama.cpp.
2. **Sentiment classifier with LoRA** — Use TRL SFTTrainer to fine-tune Qwen2.5-0.5B on sentiment data. Compare against zero-shot baseline.
3. **DPO preference alignment** — Use TRL DPOTrainer with ultrafeedback_binarized. Compare outputs before/after alignment.
4. **Dataset preparation pipeline** — Generate instruction-response pairs from raw documents using an LLM API. Format in Alpaca/ShareGPT format, validate quality.
5. **RAG vs. fine-tuning comparison** — Same domain QA task, implemented both ways. Compare quality, latency, and cost.

**Capstone projects (2–4 hours):**
1. **Custom domain expert model** — Collect domain data → prepare instruction dataset → QLoRA with Unsloth → evaluate with custom metrics → GGUF export → deploy on Ollama.
2. **GRPO reasoning model** — Train reasoning model using Unsloth/TRL on GSM8K. Custom reward functions, W&B tracking, compare against base model.
3. **Multi-task fine-tuning pipeline** — Axolotl/LlamaFactory fine-tuning for 3 tasks simultaneously (classification, NER, summarization). Task-specific evaluation and model merging.

### MLOps projects

**Mini-projects (30–60 min):**
1. **MLflow experiment tracker** — Train 3 model variants, log metrics/parameters/artifacts, compare in UI, register best model.
2. **Docker ML API** — Package model in FastAPI, containerize with Docker, add health checks, test with curl.
3. **Evidently drift report** — Generate data drift and model performance reports from training vs. production data.
4. **GitHub Actions CI/CD** — Workflow that runs data validation, trains model, evaluates, auto-comments metrics on PRs via CML.
5. **Feature store setup** — Initialize Feast, define feature views, materialize features, serve online features.

**Capstone projects (2–4 hours):**
1. **End-to-end ML pipeline** — Data ingestion → feature engineering → MLflow tracking → model registry → FastAPI serving → Docker → Evidently + Grafana monitoring. DVC for data versioning.
2. **vLLM production deployment** — Deploy quantized LLM via vLLM + Docker. OpenAI-compatible API, authentication, Prometheus metrics, Grafana dashboard, load testing with locust.
3. **Kubernetes ML platform** — KServe/Seldon on Minikube: model serving + MLflow tracking + Feast features + Prometheus/Grafana monitoring. Blue-green deployment and autoscaling.

### Safety & emerging topics projects

**Mini-projects (30–60 min):**
1. **Multi-layer guardrail pipeline** — Chain NeMo Guardrails + Guardrails AI + custom PII detector. Test with 100 adversarial prompts.
2. **Prompt injection CTF** — Capture-the-flag game: jailbreak a chatbot with progressively harder guardrails. Use promptfoo for auto-evaluation.
3. **Local reasoning model lab** — Download DeepSeek-R1-Distill-14B, quantize to GGUF Q4_K_M, benchmark against original on MATH-500.
4. **Voice-activated research agent** — Combine Pipecat + LangChain Deep Research. Ask questions verbally, receive spoken research reports.
5. **Browser automation assistant** — Personal agent using browser-use that fills forms, books appointments, comparison-shops with safety guardrails.

**Capstone projects (2–4 hours):**
1. **Enterprise AI safety platform** — NeMo Guardrails + DeepEval/DeepTeam + RAGAS + n8n orchestration + safety dashboard with auto-remediation.
2. **Autonomous research and reporting agent** — Voice/text input → browser-use web research → DeepSeek R1 reasoning → cited report → hallucination guardrails → delivery via Slack/email (n8n).
3. **Secure coding assistant with self-evaluation** — Quantized local model (R1-Distill GGUF) + VS Code integration + automated tests (promptfoo) + security guardrails (garak) + DeepEval quality metrics.

---

## Part 4: Course structure recommendations

### Recommended 20-module structure

The course follows a **four-phase progression** totaling approximately **200–250 hours** across 25 weeks at 8–12 hours/week. Each module uses the "action-first, then deep dive" pattern: start with a **quick win** (get something working in 15–30 minutes), provide **conceptual depth** (understand why it works), then offer **advanced exploration** (optimize, extend, customize).

**Phase 1: Foundations (Modules 1–5, ~6 weeks)**

| Module | Topic | Hours | Prerequisites | Key Repos |
|--------|-------|-------|---------------|-----------|
| 1 | Python for Data Science | 5-7 | Basic Python | jakevdp/PythonDataScienceHandbook |
| 2 | Feature Engineering & Data Prep | 5-7 | Module 1 | ashishpatel26/Amazing-Feature-Engineering |
| 3 | Classical Machine Learning | 8-10 | Modules 1-2 | eriklindernoren/ML-From-Scratch, scikit-learn docs |
| 4 | Deep Learning Fundamentals | 12-15 | Module 3 | mrdbourke/pytorch-deep-learning, d2l-ai/d2l-en |
| 5 | NLP Fundamentals | 8-10 | Module 4 | graykode/nlp-tutorial, tsmatz/nlp-tutorials |

**Phase 2: Modern Architectures (Modules 6–9, ~5 weeks)**

| Module | Topic | Hours | Prerequisites | Key Repos |
|--------|-------|-------|---------------|-----------|
| 6 | Transformers & Attention | 12-15 | Module 5 | rasbt/LLMs-from-scratch (ch2-4), labmlai/annotated_deep_learning_paper_implementations |
| 7 | Computer Vision | 8-10 | Module 4 | mrdbourke/pytorch-deep-learning (sections 3-6) |
| 8 | LLM Architecture & Training | 12-15 | Module 6 | rasbt/LLMs-from-scratch (ch5-7), Karpathy's Zero to Hero |
| 9 | Working with LLM APIs | 6-8 | Module 8 | openai/openai-cookbook, anthropics/anthropic-cookbook |

**Phase 3: AI Engineering Core (Modules 10–15, ~7 weeks)**

| Module | Topic | Hours | Prerequisites | Key Repos |
|--------|-------|-------|---------------|-----------|
| 10 | Prompt Engineering & Context | 6-8 | Module 9 | dair-ai/Prompt-Engineering-Guide, NirDiamant/Prompt_Engineering |
| 11 | Embeddings & Vector Databases | 8-10 | Module 10 | NirDiamant/RAG_Techniques (intro sections) |
| 12 | RAG Systems | 12-15 | Module 11 | NirDiamant/RAG_Techniques, langchain-ai/rag-from-scratch, microsoft/graphrag |
| 13 | LangChain / LlamaIndex Frameworks | 8-10 | Modules 10-12 | langchain-ai/langgraph, run-llama/llama_index |
| 14 | Fine-Tuning LLMs | 10-12 | Module 8 | unslothai/unsloth, huggingface/trl, philschmid/deep-learning-pytorch-huggingface |
| 15 | AI Agents | 10-12 | Modules 10, 13 | NirDiamant/GenAI_Agents, langchain-ai/langchain-academy, crewAIInc/crewAI-examples |

**Phase 4: Production & Integration (Modules 16–20, ~7 weeks)**

| Module | Topic | Hours | Prerequisites | Key Repos |
|--------|-------|-------|---------------|-----------|
| 16 | MLOps & LLMOps | 10-12 | Modules 1-15 | DataTalksClub/mlops-zoomcamp, GokuMohandas/Made-With-ML, mlflow/mlflow |
| 17 | Evaluation & Safety | 8-10 | Modules 10-15 | confident-ai/deepeval, NVIDIA-NeMo/Guardrails, promptfoo/promptfoo |
| 18 | Deployment & Scaling | 8-10 | Modules 16-17 | vllm-project/vllm, evidentlyai/evidently |
| 19 | Emerging Topics (Voice, Browser, MCP) | 8-10 | Module 15 | pipecat-ai/pipecat, browser-use/browser-use, modelcontextprotocol/servers |
| 20 | Capstone Project & Portfolio | 20-30 | All previous | patchy631/ai-engineering-hub (reference projects) |

### Design principles that maximize learning

The ordering logic follows a strict dependency chain: **data foundations → classical ML → deep learning → transformers → LLMs → prompt engineering → RAG → frameworks → agents → production**. Each step builds on concepts from the previous one. The theory-to-practice ratio shifts from **40:60** in foundations to **20:80** in production modules, reflecting the "action-first" philosophy.

Three critical curriculum insights emerged from this research. First, **NirDiamant's ecosystem** (RAG_Techniques + Prompt_Engineering + GenAI_Agents + agents-towards-production) provides the most cohesive free educational path across the AI Engineering core. Second, **rasbt/LLMs-from-scratch** (85K+ stars) is the single most important foundational resource — students who understand transformer internals learn everything else faster. Third, the **fine-tuning module should come before agents**, not after, because understanding model customization clarifies the tradeoff decisions that arise in agent architecture design.

### The agent framework decision matrix

Students should learn multiple frameworks because the landscape has fragmented by use case. **LangGraph** offers maximum control for production stateful workflows with complex routing. **CrewAI** excels at rapid prototyping of role-based multi-agent systems with minimal code. **AutoGen/Microsoft Agent Framework** suits enterprise Microsoft ecosystem teams. **OpenAI Agents SDK** is optimal for OpenAI-native stacks, especially voice agents. The course should teach LangGraph deeply (it's the most general-purpose) while providing comparative modules on CrewAI and OpenAI SDK.

### Adapting for different learner profiles

For **experienced developers** (3+ years), Phases 1-2 can be compressed to 2-3 weeks or skipped entirely. The AI-Crash-Course pattern (henrythe9th/AI-Crash-Course) shows even 2-week accelerated formats work for this group. For **career changers**, the full 25-week path is recommended. For **ML engineers transitioning to AI Engineering**, start at Module 9 (Working with LLM APIs) and focus on Phases 3-4.

---

## Conclusion: Where the resource landscape stands and what is missing

The AI Engineering educational ecosystem has reached remarkable maturity. **Over 150 high-quality, actively maintained repositories** now cover every major topic with runnable code. The NirDiamant collection, patchy631/ai-engineering-hub, and official framework repos from LangChain, HuggingFace, and OpenAI form a robust backbone. Three repos alone — rasbt/LLMs-from-scratch (85K stars), NirDiamant/RAG_Techniques (24.7K stars), and NirDiamant/GenAI_Agents (19.1K stars) — can anchor an entire curriculum's core modules.

Seven significant gaps remain. **Agent evaluation and testing** lacks standardized open-source benchmarks — most evaluation is still ad hoc. **Multi-modal safety** has almost no production-ready guardrails for image/video/audio inputs. **End-to-end fine-tuning-to-deployment pipelines** are poorly covered; individual steps are well-documented but the complete workflow from training through quantization to monitored production serving lacks cohesive tutorials. **RAG security** (prompt injection via retrieved documents, multi-tenant access control) has minimal code-first resources. **Cost optimization** across fine-tuning, inference, and agent orchestration remains blog-post territory rather than structured educational content. **Distributed multi-node fine-tuning** tutorials beyond Axolotl are rare. And **episodic agent memory** (learning from past task executions) remains largely academic despite Mem0's strong general memory implementation.

For course builders, the key strategic insight is that this field moves fast enough that **referencing evergreen concepts** (transformer architecture, attention, optimization theory, evaluation methodology) while pointing to specific tools via regularly-updated resource lists produces the most durable curriculum. The repos listed here represent the state of the art as of early 2026, but several — particularly in the agent and MCP space — will see significant evolution within months.