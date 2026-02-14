# The definitive resource guide for building an AI Engineering bootcamp

**Over 100 open-source repos, courses, and tutorials can power an 8–12 week AI Engineering bootcamp — and the best ones have emerged in the past 18 months.** The ecosystem has matured dramatically since 2023, with Microsoft, Hugging Face, LangChain, and community contributors publishing structured curricula that cover LLM fundamentals through production deployment. The most impactful resources share three traits: they teach by building, they use multi-provider stacks, and they progress from fundamentals to production patterns. This report maps every major resource to specific bootcamp modules, with GitHub star counts, difficulty levels, and direct URLs.

---

## Structured courses that can anchor the entire curriculum

Several open-source repositories now offer full bootcamp-style curricula. The strongest foundation comes from combining **three flagship courses** that together cover every topic in your scope.

**Microsoft's Generative AI for Beginners** (github.com/microsoft/generative-ai-for-beginners, **~103k stars**) provides 21 lessons covering GenAI fundamentals, prompt engineering, chat applications, search apps, function calling, RAG, agents, and LLMOps. Lessons are labeled "Learn" or "Build" with code in Python and TypeScript. It is actively maintained with 1,700+ commits and works perfectly for weeks 1–3 of a bootcamp.

**mlabonne/llm-course** (github.com/mlabonne/llm-course, **~73.7k stars**) divides into three tracks: LLM Fundamentals (math, Python, neural networks), LLM Scientist (training, fine-tuning, RLHF, quantization), and LLM Engineer (RAG, vector storage, deployment, agents). It includes interactive Colab notebooks and an associated book ("LLM Engineer's Handbook"). This serves as the overall roadmap and reference curriculum for the entire bootcamp.

**Microsoft's AI Agents for Beginners** (github.com/microsoft/ai-agents-for-beginners, **~44.9k stars**) offers 12 lessons on agent fundamentals: tool use, agentic RAG, multi-agent systems, planning, MCP, evaluation, and deployment. This slots directly into weeks 5–6 as the agent-building module.

Additional structured curricula worth integrating include:

- **rasbt/LLMs-from-scratch** (github.com/rasbt/LLMs-from-scratch, **~78.7k stars**) — Build a GPT-like LLM from the ground up in PyTorch. Companion book by Sebastian Raschka (Manning, 2024). Best for a deep-dive week on LLM internals.
- **patchy631/ai-engineering-hub** (github.com/patchy631/ai-engineering-hub, **~22.3k stars**) — 93+ production-ready projects across beginner, intermediate, and advanced levels. Ideal as the project library students pick from.
- **aishwaryanr/awesome-generative-ai-guide** (github.com/aishwaryanr/awesome-generative-ai-guide, **~24.2k stars**) — Includes a 10-week "Applied LLMs Mastery" course plus interview prep with 60+ GenAI questions.
- **ed-donner/llm_engineering** (github.com/ed-donner/llm_engineering) — 8-week course covering Ollama, OpenAI API, prompt engineering, LangChain, RAG, fine-tuning, evaluation, and autonomous agents. Maps directly to a bootcamp week-by-week structure.
- **huggingface/smol-course** (github.com/huggingface/smol-course, **~6.4k stars**) — Practical course on fine-tuning and alignment built around SmolLM3. Covers SFT, DPO, quantization, and deployment with minimal GPU requirements.
- **openai/openai-cookbook** (github.com/openai/openai-cookbook, **~71.4k stars**) — Extensive collection of examples: embeddings, function calling, Assistants API, vision, fine-tuning, RAG, moderation. Reference throughout the bootcamp.

---

## RAG resources from foundations through production patterns

RAG has the richest tutorial ecosystem of any AI engineering topic. The progression from simple retrieval to production systems is well-documented.

**NirDiamant/RAG_Techniques** (github.com/NirDiamant/RAG_Techniques, **~24k stars**) is the single most comprehensive RAG resource available. It implements **30+ techniques** in individual Jupyter notebooks: semantic chunking, query transformation, context compression, CRAG, self-RAG, hybrid search, reranking, multi-representation indexing, agentic RAG, and the GroUSE evaluation framework. Each technique is self-contained with full explanations. This belongs in weeks 3–4 of the bootcamp, where students pick 3–4 techniques to implement and compare.

**LangChain's rag-from-scratch** (github.com/langchain-ai/rag-from-scratch, **~5.9k stars**) provides 14 progressive notebooks that accompany a video playlist by Lance Martin. It covers indexing, retrieval, generation, multi-query retrieval, RAG fusion, query decomposition, step-back prompting, HyDE, RAPTOR, routing, CRAG, and self-RAG. This is the ideal week-1 RAG introduction.

**mrdbourke/simple-local-rag** (github.com/mrdbourke/simple-local-rag, **~930 stars**) builds a complete local RAG pipeline from scratch — PDF ingestion, text chunking, embeddings, vector search, and LLM generation — all running locally without API costs. Excellent for teaching RAG internals before introducing frameworks.

For **vector databases**, the bootcamp should use Chroma for prototyping (simplest setup, in-memory option), then introduce Qdrant or pgvector for production. The Firecrawl 2025 comparison guide (firecrawl.dev/blog/best-vector-databases-2025) benchmarks 14 databases with performance data.

For **chunking strategies**, the IBM tutorial (ibm.com/think/tutorials/chunking-strategies-for-rag-with-langchain-watsonx-ai) covers fixed, recursive, semantic, and agentic chunking with LangChain. Greg Kamradt's "5 Levels of Text Splitting" (github.com/FullStackRetrieval-com/RetrievalTutorials) remains the canonical reference.

For **RAG evaluation**, the **RAGAS framework** (github.com/explodinggradients/ragas, **~8k stars**) is the de facto standard, measuring context precision, context recall, faithfulness, and answer relevancy. The DeepLearning.AI short course "Building and Evaluating Advanced RAG" (with LlamaIndex and TruLens) is the best structured course for evaluation-driven RAG development.

Advanced RAG resources include the **Hugging Face Advanced RAG Cookbook** (huggingface.co/learn/cookbook/en/advanced_rag) for open-source reranking with ColBERT, **Neo4j's GraphRAG guides** (graphrag.com) for knowledge graph-enhanced retrieval, and the **DeepLearning.AI RAG Course on Coursera** for the full production pathway including monitoring, observability, and cost optimization.

---

## AI agents across every major framework

The agent ecosystem has exploded with frameworks, and the bootcamp should teach both framework-free fundamentals and multiple production frameworks.

**Start from scratch before frameworks.** Two excellent tutorials teach agent-building without any framework: Analytics Vidhya's "Build AI Agents from Scratch" (analyticsvidhya.com/blog/2024/07/build-ai-agents-from-scratch/) implements the ReAct pattern in pure Python + OpenAI, and Leonie Monigatti's tutorial (leoniemonigatti.com/blog/ai-agent-from-scratch-in-python.html) does the same with Anthropic's API. Both reinforce that **agents are models using tools in a loop**.

**NirDiamant/GenAI_Agents** (github.com/NirDiamant/GenAI_Agents, **~17.7k stars**) provides the broadest tutorial collection: from basic QA agents through LangGraph workflows, multi-agent collaboration, MCP integration, and production deployment. Its companion repo **agents-towards-production** covers Docker, FastAPI, security guardrails, GPU scaling, observability, and CI/CD.

For **LangGraph**, **LangChain Academy's free course** (academy.langchain.com/courses/intro-to-langgraph) is the official starting point with 6 progressive modules covering state, nodes, edges, memory, ReAct agents, persistence, streaming, and human-in-the-loop. The **langchain-ai/agents-from-scratch** repo builds a deployable email assistant with HITL and evaluation using LangSmith.

For **other frameworks**, key resources include:

- **CrewAI** (github.com/crewAIInc/crewAI) — Role-based agents with Crews, Tasks, and Flows architecture. The crewAI-examples repo has standalone projects (Game Builder, Instagram Post Generator, Marketing Strategy).
- **AutoGen** (github.com/microsoft/autogen, **~48k stars**) — Multi-agent conversations with group chat patterns. The "autogen_blueprint" repo provides a 16-chapter book companion.
- **OpenAI Agents SDK** (github.com/openai/openai-agents-python) — Lightweight SDK with Agents, Handoffs, Guardrails, Sessions, and Tracing. Supports 100+ LLMs despite the name.
- **smolagents** (github.com/huggingface/smolagents) — Hugging Face's ~1,000-line agent library. CodeAgents write actions as Python code. The **HF Agents Course** (huggingface.co/learn/agents-course) is free, certified, and covers smolagents, LlamaIndex agents, and LangGraph.
- **Agno** (github.com/agno-agi/agno, **~18.5k stars**) — Formerly Phidata. Multi-modal agents, learning agents with memory, team coordination. Known for minimal code (web search agent in 10 lines).

**Anthropic's tool use documentation** (docs.anthropic.com/en/docs/build-with-claude/tool-use) and **MCP guides** are essential reading for function calling patterns. The engineering blog posts on advanced tool use and code execution with MCP represent cutting-edge production patterns.

The **Langfuse framework comparison** (langfuse.com/blog/2025-03-19-ai-agent-comparison) provides an excellent decision guide comparing LangGraph, OpenAI Agents SDK, smolagents, CrewAI, AutoGen, and more.

---

## Prompt engineering from basics to context engineering

**DAIR.AI's Prompt Engineering Guide** (github.com/dair-ai/Prompt-Engineering-Guide, **~66.4k stars**) is the definitive reference. It covers every technique — zero-shot, few-shot, chain-of-thought, self-consistency, tree-of-thought, ReAct — with papers, lectures, and notebooks. The companion website (promptingguide.ai) provides a structured learning path.

**Anthropic's Interactive Tutorial** (github.com/anthropics/prompt-eng-interactive-tutorial, **~3k stars**) is the best hands-on exercise for bootcamp students. Nine chapters in Jupyter notebook format with exercises and answer keys cover prompt structure, clear instructions, role/system prompts, XML formatting, CoT, few-shot prompting, hallucination avoidance, and output formatting. Anthropic's **context engineering guide** (anthropic.com/engineering/effective-context-engineering-for-ai-agents) represents the evolution from prompt engineering to context engineering for agents.

**OpenAI's Prompt Engineering Guide** (platform.openai.com/docs/guides/prompt-engineering) provides six core strategies that serve as an excellent teaching framework. The **GPT-5 Prompting Guide** (cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide) covers agentic prompting and structured tool use.

**NirDiamant/Prompt_Engineering** (github.com/NirDiamant/Prompt_Engineering) provides 22 hands-on notebooks implementing each technique individually. **Brex's Prompt Engineering Guide** (github.com/brexhq/prompt-engineering, **~9k stars**) adds production context from a real company, covering system prompts, safety, jailbreak mitigation, and prompt injection prevention.

---

## Fine-tuning with modern tools and techniques

The fine-tuning module should progress from concepts through hands-on QLoRA to production training pipelines.

**Unsloth** (github.com/unslothai/unsloth, **~30k stars**) is the best starting point for beginners: **2x faster fine-tuning with 70% less VRAM**, free Google Colab notebooks, and support for the latest models (Llama 4, Qwen3, DeepSeek-R1). Its step-by-step tutorial for fine-tuning Llama 3 and deploying with Ollama is the ideal first hands-on exercise.

**Hugging Face TRL** (github.com/huggingface/trl, **~12k stars**) is the go-to library for all post-training: SFT, DPO, GRPO, PPO, and Reward Modeling, with a full CLI (`trl sft`, `trl dpo`). **PEFT** (github.com/huggingface/peft, **~16k stars**) provides the foundational LoRA/QLoRA implementation that TRL, Unsloth, and Axolotl all build upon.

**Axolotl** (github.com/axolotl-ai-cloud/axolotl, **~8k stars**) provides configuration-first fine-tuning via YAML files with support for multi-GPU training (FSDP, DeepSpeed), multimodal training, and sequence parallelism. This is the production-grade tool for advanced students.

**Phil Schmid's tutorial series** (philschmid.de) provides excellent progressive guides: "How to Fine-Tune Open LLMs in 2025" covers QLoRA, Spectrum, Flash Attention, and distributed training. His DPO alignment walkthrough is the best practical guide for preference optimization.

**OpenAI's fine-tuning platform** (platform.openai.com/docs/guides/supervised-fine-tuning) supports SFT, DPO, and reinforcement fine-tuning for GPT-4o models. This contrasts with open-source fine-tuning and teaches when to use each approach.

The **DeepLearning.AI short course "Finetuning Large Language Models"** (taught by Sharon Zhou) is the best 1–2 hour introduction for students new to fine-tuning concepts.

---

## MLOps, deployment, and production serving

Deployment resources range from local development with Ollama to production GPU serving with vLLM.

**Ollama** (github.com/ollama/ollama, **~120k stars**) is essential for local development: running open-source models locally with an OpenAI-compatible API, Modelfile customization, and Docker integration. Every student should set this up in week 1.

**vLLM** (github.com/vllm-project/vllm, **~50k stars**) is the production standard for high-throughput LLM serving with PagedAttention, tensor parallelism, and OpenAI-compatible endpoints. The vLLM + FastAPI + Docker tutorial (github.com/wpan36/vllm_in_docker) provides a complete containerized deployment.

**LangServe** (github.com/langchain-ai/langserve) deploys LangChain chains as production REST APIs with built-in playground, streaming, and auto-generated schemas. The CircleCI tutorial demonstrates a full CI/CD pipeline with LangServe on GCP Cloud Run. **LitServe** (github.com/Lightning-AI/LitServe, **~3k stars**) from Lightning AI offers an alternative with batching, GPU autoscaling, and compound AI system support.

For **Docker + FastAPI fundamentals**, the Full-Stack FastAPI Template (github.com/fastapi/full-stack-fastapi-template, **~28k stars**) includes built-in GitHub Actions CI/CD. The Evidently AI tutorial (evidentlyai.com/blog/fastapi-tutorial) demonstrates ML monitoring with FastAPI, PostgreSQL, and Streamlit dashboards.

The **tensorchord/Awesome-LLMOps** list (github.com/tensorchord/Awesome-LLMOps, **~4.1k stars**) provides a comprehensive landscape of serving, evaluation, monitoring, prompt management, and caching tools.

---

## Evaluation frameworks and guardrails for safety

**DeepEval** (github.com/confident-ai/deepeval, **~8k stars**) provides pytest-like unit testing for LLMs with **50+ metrics** (G-Eval, hallucination, faithfulness, toxicity), red teaming for 40+ safety vulnerabilities, synthetic dataset generation, and CI/CD integration. Version 3.0 released in 2025 represents the most feature-complete LLM testing framework available.

**RAGAS** (github.com/explodinggradients/ragas, **~8k stars**) remains the standard specifically for RAG evaluation, measuring context precision, context recall, faithfulness, and answer relevancy with synthetic test data generation.

**LangSmith** (langchain.com/langsmith) provides end-to-end observability: tracing, offline evaluation with datasets, online monitoring, prompt versioning, A/B testing, human-in-the-loop annotation, and cost/latency tracking. **Arize Phoenix** (github.com/Arize-ai/phoenix, **~8.5k stars**) is the open-source alternative with OpenTelemetry-based distributed tracing and no vendor lock-in.

For **safety guardrails**, **Guardrails AI** (github.com/guardrails-ai/guardrails, **~4k stars**) validates LLM inputs/outputs with pre-built validators (toxicity, PII, prompt injection). **NVIDIA NeMo Guardrails** (github.com/NVIDIA-NeMo/Guardrails, **~4k stars**) adds programmable dialog rails, jailbreak protection, and fact-checking using the Colang language. The OpenAI Cookbook's guardrails notebook demonstrates async input/output guardrail patterns for production.

---

## Curated awesome-lists and roadmaps for reference

These meta-resources help students navigate the ecosystem and serve as ongoing reference material:

- **Hannibal046/Awesome-LLM** (github.com/Hannibal046/Awesome-LLM, **~25k stars**) — The canonical LLM awesome-list with milestone papers, training frameworks, and model checkpoints
- **Shubhamsaboo/awesome-llm-apps** (github.com/Shubhamsaboo/awesome-llm-apps) — Curated practical LLM apps built with RAG, agents, and multi-agent teams across OpenAI, Anthropic, and open-source models
- **kyrolabs/awesome-langchain** (github.com/kyrolabs/awesome-langchain, **~8.3k stars**) — 200+ curated LangChain tools, projects, and tutorials
- **kyrolabs/awesome-agents** (github.com/kyrolabs/awesome-agents) — Agent frameworks, coding agents, research agents, and multi-agent systems
- **e2b-dev/awesome-ai-agents** (github.com/e2b-dev/awesome-ai-agents) — Categorized list with web filtering interface
- **Danielskry/Awesome-RAG** (github.com/Danielskry/Awesome-RAG) — RAG architectures, frameworks, evaluation, and production patterns
- **ashishps1/learn-ai-engineering** (github.com/ashishps1/learn-ai-engineering, **~3k stars**) — Curated learning path from math foundations through agents and MCP
- **EthicalML/awesome-production-genai** — Production GenAI tools: serving, agents, security, evaluation, and UI frameworks
- **Awesome-LLMSecOps** (github.com/wearetyomsmnv/Awesome-LLMSecOps) — OWASP Top 10 for LLMs, red teaming frameworks, prompt injection detection

---

## Recommended 10-week bootcamp curriculum mapping

| Week | Topic | Primary Resources | Stars |
|------|-------|------------------|-------|
| **1** | LLM Fundamentals + First App | Microsoft GenAI for Beginners (lessons 1–7), Ollama setup | 103k, 120k |
| **2** | Prompt Engineering + API Mastery | DAIR.AI Guide, Anthropic Interactive Tutorial, OpenAI Cookbook | 66k, 3k, 71k |
| **3** | RAG Foundations | LangChain rag-from-scratch, mrdbourke/simple-local-rag, Chroma | 5.9k, 930 |
| **4** | Advanced RAG + Evaluation | NirDiamant/RAG_Techniques, RAGAS framework, HF Advanced RAG | 24k, 8k |
| **5** | AI Agents Fundamentals | Microsoft AI Agents for Beginners, LangChain Academy LangGraph | 44.9k |
| **6** | Multi-Agent Systems + Tool Use | NirDiamant/GenAI_Agents, CrewAI, OpenAI Agents SDK, MCP | 17.7k |
| **7** | Fine-Tuning LLMs | Unsloth tutorials, HF TRL + PEFT, Phil Schmid guides | 30k, 12k, 16k |
| **8** | Evaluation + Guardrails | DeepEval, LangSmith, Guardrails AI, NeMo Guardrails | 8k, 4k, 4k |
| **9** | MLOps + Deployment | vLLM + Docker + FastAPI, LangServe, CI/CD pipeline | 50k, 28k |
| **10** | Capstone Project | ai-engineering-hub projects, awesome-llm-apps | 22.3k |

**Pre-work**: mlabonne/llm-course as the roadmap, rasbt/LLMs-from-scratch for motivated students who want to understand transformer internals.

---

## Conclusion

The AI Engineering education ecosystem reached a tipping point in 2024–2025. **Three resources alone — Microsoft's GenAI for Beginners (103k stars), mlabonne's LLM Course (73.7k stars), and NirDiamant's RAG Techniques (24k stars) — cover roughly 60% of a bootcamp curriculum** with high-quality, tested content. The remaining 40% is well-served by specialized resources: LangChain Academy for agents, Unsloth for fine-tuning, DeepEval for evaluation, and vLLM for deployment. 

The most notable gap in the ecosystem is Anthropic-specific tutorial content — while Anthropic's official documentation and prompt engineering tutorial are excellent, community-built project tutorials overwhelmingly default to OpenAI APIs. Building bootcamp projects that use both providers (and open-source models via Ollama) will differentiate your curriculum. The strongest pedagogical pattern across all top-starred repos is **"build from scratch first, then introduce frameworks"** — mrdbourke's local RAG, the ReAct agent tutorials, and rasbt's LLMs-from-scratch all demonstrate that students who understand internals before touching LangChain or LlamaIndex become significantly stronger engineers.