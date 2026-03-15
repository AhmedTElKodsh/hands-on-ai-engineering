# 🎓 Student Navigation Guide

**Welcome to Hands-On AI Engineering!** This guide provides a clear, single path through the curriculum.

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Clone and setup
git clone https://github.com/AhmedTElKodsh/hands-on-ai-engineering.git
cd hands-on-ai-engineering
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 4. Start learning
cd Layer2-Curriculum/chapters/phase-0-foundations
# Open chapter-01-environment-setup.md
```

---

## 📚 Learning Path

### The Single Path Forward

Follow this sequence for the complete learning experience:

```
Phase 0: Foundations (9h)
  ↓
Phase 1: LLM Fundamentals (9h)
  ↓
Phase 2: Embeddings & Vectors (6h) [IN PROGRESS]
  ↓
Phase 3: RAG Fundamentals (9h) [PLANNED]
  ↓
Phase 4-10: Advanced Topics [PLANNED]
```

---

## 📖 Chapter-by-Chapter Guide

### ✅ Phase 0: Foundations (9 hours)

**Status**: COMPLETE  
**Prerequisites**: Basic Python knowledge  
**Goal**: Master Python fundamentals for AI engineering

| Chapter | Topic | Time | Status |
|---------|-------|------|--------|
| 01 | Environment Setup | 1.5h | ✅ |
| 02 | Python Fundamentals | 1.5h | ✅ |
| 03 | Type Hints & Validation | 1.5h | ✅ |
| 04 | Pydantic Basics | 1.5h | ✅ |
| 05 | Advanced Pydantic | 1.5h | ✅ |
| 06 | Configuration Management | 1.5h | ✅ |

**Learning Checkpoint**: Can you create a Pydantic model with validation and load configuration from environment variables?

---

### ✅ Phase 1: LLM Fundamentals (9 hours)

**Status**: COMPLETE  
**Prerequisites**: Phase 0  
**Goal**: Master LLM APIs and prompt engineering

| Chapter | Topic | Time | Status |
|---------|-------|------|--------|
| 07 | First LLM Call | 1.5h | ✅ |
| 08 | Structured Outputs | 1.5h | ✅ |
| 09 | Prompt Engineering | 1.5h | ✅ |
| 10 | Streaming Responses | 1.5h | ✅ |
| 11 | Error Handling | 1.5h | ✅ |
| 12 | Cost Tracking | 1.5h | ✅ |

**Mini-Project**: Build a multi-provider LLM client with fallback  
**Learning Checkpoint**: Can you make structured LLM calls with error handling and cost tracking?

---

### 🔄 Phase 2: Embeddings & Vectors (6 hours)

**Status**: IN PROGRESS (2/4 chapters complete)  
**Prerequisites**: Phase 1  
**Goal**: Understand semantic search and vector databases

| Chapter | Topic | Time | Status |
|---------|-------|------|--------|
| 13 | Introduction to Embeddings | 1.5h | ✅ |
| 14 | Vector Stores with Chroma | 1.5h | ✅ |
| 15 | Chunking Strategies | 1.5h | 🔄 In Progress |
| 16 | Document Loaders | 1.5h | ⏳ Planned |

**Mini-Project**: Build a document indexer with semantic search  
**Learning Checkpoint**: Can you chunk documents, create embeddings, and perform semantic search?

---

### ⏳ Phase 3: RAG Fundamentals (9 hours)

**Status**: PLANNED  
**Prerequisites**: Phase 2  
**Goal**: Build production-ready RAG systems

| Chapter | Topic | Time | Status |
|---------|-------|------|--------|
| 17 | Simple RAG Pipeline | 1.5h | ⏳ |
| 18 | Query Enhancement | 1.5h | ⏳ |
| 19 | Contextual Compression | 1.5h | ⏳ |
| 20 | Hybrid Search | 1.5h | ⏳ |
| 21 | RAG Evaluation | 1.5h | ⏳ |
| 22 | Production RAG | 1.5h | ⏳ |

**Flagship Project 1**: Civil Engineering Document RAG System  
**Learning Checkpoint**: Can you build a RAG system that retrieves and generates accurate answers with citations?

---

### ⏳ Phases 4-10 (Coming Soon)

**Phase 4**: LangChain Core (4.5h)  
**Phase 5**: Agents (7.5h)  
**Phase 6**: LangGraph (6h)  
**Phase 7**: LlamaIndex (6h)  
**Phase 8**: Production Engineering (6h)  
**Phase 9**: Multi-Agent Systems (9h)  
**Phase 10**: Civil Engineering Application (9h)

---

## 🎯 Learning Methodology

### For Each Chapter:

1. **📖 Read** (20 min)
   - Understand concepts with cafe-style explanations
   - Review code examples
   - Note key takeaways

2. **💻 Code** (40 min)
   - Complete TODOs in starter code
   - Follow hints and architecture guidance
   - Explain your design decisions

3. **✅ Verify** (15 min)
   - Run verification scripts
   - Fix any issues
   - Ensure all tests pass

4. **🎯 Practice** (15 min)
   - Complete "Try This!" exercises
   - Experiment with variations
   - Build understanding through exploration

---

## 📊 Progress Tracking

### Current Status

- **Completed**: 14/54 chapters (25.9%)
- **Functional**: Phase 0-1 fully working
- **In Progress**: Phase 2 (50% complete)
- **Estimated Time to Phase 3**: 3 hours

### Your Progress

Track your progress by creating a checklist:

```markdown
## My Progress

### Phase 0: Foundations
- [ ] Chapter 01: Environment Setup
- [ ] Chapter 02: Python Fundamentals
- [ ] Chapter 03: Type Hints
- [ ] Chapter 04: Pydantic Basics
- [ ] Chapter 05: Advanced Pydantic
- [ ] Chapter 06: Configuration

### Phase 1: LLM Fundamentals
- [ ] Chapter 07: First LLM Call
- [ ] Chapter 08: Structured Outputs
...
```

---

## 🗺️ Dependency Map

```
Chapter 01 (Setup)
    ↓
Chapter 02-03 (Python Basics)
    ↓
Chapter 04-06 (Pydantic & Config)
    ↓
Chapter 07-08 (LLM Basics)
    ↓
Chapter 09-12 (Advanced LLM)
    ↓
Chapter 13-14 (Embeddings)
    ↓
Chapter 15-16 (Document Processing)
    ↓
Chapter 17-22 (RAG Systems)
    ↓
[Future Phases]
```

---

## ⏱️ Time Estimates

### By Phase

| Phase | Hours | Chapters | Avg per Chapter |
|-------|-------|----------|-----------------|
| Phase 0 | 9h | 6 | 1.5h |
| Phase 1 | 9h | 6 | 1.5h |
| Phase 2 | 6h | 4 | 1.5h |
| Phase 3 | 9h | 6 | 1.5h |
| **Total (0-3)** | **33h** | **22** | **1.5h** |

### By Activity

- Reading & Understanding: 20 min/chapter
- Coding & Implementation: 40 min/chapter
- Verification & Testing: 15 min/chapter
- Exercises & Practice: 15 min/chapter
- **Total**: 90 min (1.5h) per chapter

---

## 🎓 Learning Paths

### Path 1: Rapid Implementation (4-6 weeks)

**Goal**: Build working RAG system quickly  
**Time**: 33 hours (Phase 0-3)

```
Week 1-2: Phase 0-1 (18h)
Week 3-4: Phase 2-3 (15h)
Week 5-6: Flagship Project 1
```

### Path 2: Comprehensive Mastery (8-10 weeks)

**Goal**: Master all frameworks  
**Time**: 71 hours (All phases)

```
Week 1-2: Phase 0-1
Week 3-4: Phase 2-3
Week 5-6: Phase 4-5
Week 7-8: Phase 6-7
Week 9-10: Phase 8-10
```

### Path 3: Weekend Warrior (12-16 weeks)

**Goal**: Learn at comfortable pace  
**Time**: 5-6 hours per week

```
1 chapter per weekend
Complete in 3-4 months
```

---

## 🛠️ Technical Setup

### Required Tools

- Python 3.10+
- Text editor (VS Code recommended)
- Git
- Terminal/Command Prompt

### API Keys Needed

**Phase 0-1**: None (uses mock LLM)  
**Phase 2+**: 
- OpenAI API key (for embeddings)
- Optional: Anthropic, Groq for multi-provider

### Development Environment

```bash
# Check Python version
python --version  # Should be 3.10+

# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import openai; print('✅ Setup complete')"
```

---

## 📁 Directory Structure

```
hands-on-ai-engineering/
├── Layer2-Curriculum/          # 👈 START HERE
│   ├── chapters/
│   │   ├── phase-0-foundations/
│   │   ├── phase-1-llm-fundamentals/
│   │   └── phase-2-embeddings-vectors/
│   ├── guides/
│   └── docs/
├── shared/                     # Shared utilities
│   ├── models/
│   └── infrastructure/
├── examples/                   # Working examples
├── tests/                      # Test suites
└── requirements.txt
```

---

## ❓ FAQ

### Q: Which chapters are actually complete and working?

**A**: Phase 0 (Ch 1-6) and Phase 1 (Ch 7-12) are fully functional. Phase 2 is 50% complete.

### Q: Can I skip chapters?

**A**: Not recommended. Each chapter builds on previous ones. The dependency map shows required prerequisites.

### Q: What if I get stuck?

**A**: 
1. Review the chapter's "Common Mistakes" section
2. Check verification script output for hints
3. Review previous chapters for foundational concepts
4. Open an issue on GitHub with specific error details

### Q: Do I need all API keys to start?

**A**: No! Phase 0-1 work with mock LLM (no API keys). You'll need OpenAI API key starting Phase 2.

### Q: How do I know if I'm ready for the next chapter?

**A**: Complete the "Learning Checkpoint" question at the end of each phase. If you can answer confidently, you're ready!

---

## 🎯 Success Criteria

### Phase 0 Complete When You Can:
- ✅ Create Pydantic models with validation
- ✅ Use type hints effectively
- ✅ Manage configuration with environment variables

### Phase 1 Complete When You Can:
- ✅ Make LLM API calls with error handling
- ✅ Get structured outputs from LLMs
- ✅ Implement streaming responses
- ✅ Track costs and usage

### Phase 2 Complete When You Can:
- ✅ Generate embeddings for text
- ✅ Store and query vectors in Chroma
- ✅ Chunk documents effectively
- ✅ Load various document formats

### Phase 3 Complete When You Can:
- ✅ Build end-to-end RAG pipeline
- ✅ Implement hybrid search
- ✅ Evaluate RAG system quality
- ✅ Deploy production-ready RAG

---

## 📞 Support

- **Documentation**: See `QUICKSTART.md` for setup help
- **Progress Tracking**: See `PROGRESS-SUMMARY.md` for detailed status
- **Issues**: Open GitHub issue with `[student-question]` tag
- **Examples**: Check `examples/` directory for working code

---

## 🎉 Ready to Start?

1. Complete the Quick Start setup above
2. Open `Layer2-Curriculum/chapters/phase-0-foundations/chapter-01-environment-setup.md`
3. Follow the chapter structure: Read → Code → Verify → Practice
4. Track your progress using the checklist
5. Celebrate each completed chapter! 🎊

**Remember**: This is a marathon, not a sprint. Take breaks, experiment, and enjoy the learning journey!

---

*Last Updated: March 8, 2026*  
*Current Curriculum Status: Phase 0-1 Complete, Phase 2 In Progress*
