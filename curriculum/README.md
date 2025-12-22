# AITEA Curriculum: AI Time Estimation Agent

A project-based learning curriculum that teaches AI agent development from fundamentals to advanced patterns by building a real-world time estimation system.

## Curriculum Overview

| Phase | Chapters | Focus              | Package Built       |
| ----- | -------- | ------------------ | ------------------- |
| 1     | 1-8      | Python Foundations | aitea-core          |
| 2     | 9-12     | CLI Development    | aitea-cli           |
| 3     | 13-16    | LLM Fundamentals   | Mock LLM system     |
| 4     | 17-22    | Agent Foundations  | From-scratch agents |
| 5     | 23-28    | LangChain Track    | aitea-langchain     |
| 6     | 29-34    | LlamaIndex Track   | aitea-llamaindex    |

## How to Use This Curriculum

1. **Start with Phase 1** - Build the core data models and services
2. **Complete chapters in order** - Each builds on previous concepts
3. **Run the exercises** - Hands-on practice is essential
4. **Check your work** - Run tests after each chapter

## Prerequisites

- Basic Python syntax (functions, classes, loops)
- A code editor (VS Code recommended)
- Conda installed (Miniconda or Anaconda)

## Quick Start

```bash
# Create conda environment with Python 3.11
conda create -n aitea python=3.11 -y
conda activate aitea

# Install UV for fast package management
pip install uv

# Install dependencies (10-100x faster than pip!)
uv pip install -r requirements.txt
uv pip install -e .

# Run tests to verify setup
python -m pytest tests/ -v
```

**For detailed setup instructions, see [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)**

## Chapter Index

### Phase 1: Python Foundations

- [Chapter 1: Environment & Project Setup](chapters/CH01_environment_setup.md)
- [Chapter 2: Enums & Type Hints](chapters/CH02_enums_type_hints.md)
- [Chapter 3: Dataclasses & Data Models](chapters/CH03_dataclasses.md)
- [Chapter 4: Abstract Classes & Interfaces](chapters/CH04_abstract_classes.md)
- [Chapter 5: Service Implementation](chapters/CH05_services.md)
- [Chapter 6: Utility Functions](chapters/CH06_utilities.md)
- [Chapter 7: Property-Based Testing](chapters/CH07_property_testing.md)
- [Chapter 8: Error Handling & Validation](chapters/CH08_error_handling.md)

### Phase 2: CLI Development

- [Chapter 9: CLI with Typer](chapters/CH09_cli_typer.md)
- [Chapter 10: Rich Terminal UI](chapters/CH10_rich_ui.md)
- [Chapter 11: JSON Persistence](chapters/CH11_json_persistence.md)
- [Chapter 12: CSV Import Pipeline](chapters/CH12_csv_import.md)

### Phase 3: LLM Fundamentals

- [Chapter 13: LLM Basics & Mock Client](chapters/CH13_llm_basics.md) ✅
- [Chapter 14: Prompt Engineering](chapters/CH14_prompt_engineering.md) ✅
- [Chapter 15: Structured Outputs](chapters/CH15_structured_outputs.md) ✅
- [Chapter 16: Tool Calling Patterns](chapters/CH16_tool_calling.md) ✅

### Phase 4: Agent Foundations

- [Chapter 17: What Are Agents?](chapters/CH17_agent_concepts.md) ✅
- [Chapter 18: Agent Loop from Scratch](chapters/CH18_agent_loop.md) ✅
- [Chapter 19: Tool Registry](chapters/CH19_tool_registry.md) ✅
- [Chapter 20: Planning Patterns (ReAct)](chapters/CH20_react_pattern.md) ✅
- [Chapter 21: Memory Patterns](chapters/CH21_memory.md) ✅
- [Chapter 22: Guardrails & Safety](chapters/CH22_safety.md) ✅

### Phase 5: LangChain Track

- Chapter 23: LangChain Agents (Coming Soon)
- Chapter 24: Custom Tools (Coming Soon)
- Chapter 25: RAG Pipeline (Coming Soon)
- Chapter 26: LangGraph Orchestration (Coming Soon)
- Chapter 27: LangSmith Platform (Coming Soon)
- Chapter 28: Deep Agents (Coming Soon)

### Phase 6: LlamaIndex Track

- Chapter 29: LlamaIndex Agents (Coming Soon)
- Chapter 30: Event-Driven Workflows (Coming Soon)
- Chapter 31: Advanced Retrieval (Coming Soon)
- Chapter 32: Agentic RAG Patterns (Coming Soon)
- Chapter 33: RAG Evaluation (Coming Soon)
- Chapter 34: Workflow Deployment (Coming Soon)
