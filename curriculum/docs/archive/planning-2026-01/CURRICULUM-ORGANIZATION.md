# Curriculum Organization Structure

## Clear Guide to All Curriculum Resources

**Last Updated**: January 20, 2026  
**Purpose**: Central index for all curriculum development and teaching resources

---

## 📁 Directory Structure Overview

```
curriculum/
├── README.md                          # Main curriculum entry point (YOU ARE HERE guide)
├── CURRICULUM-ORGANIZATION.md         # This file - master index
│
├── chapters/                          # 📚 All curriculum chapters organized by phase
│   ├── phase-0-foundations/           # Ch 1-6: Python & Environment Setup
│   ├── phase-1-llm-fundamentals/      # Ch 7-12: First LLM Calls
│   ├── phase-2-embeddings-vectors/    # Ch 13-16: Embeddings & Vector Stores
│   ├── phase-3-rag-fundamentals/      # Ch 17-22: RAG Systems
│   ├── phase-4-langchain-core/        # Ch 23-25: LangChain Basics
│   ├── phase-5-agents/                # Ch 26-30: Agent Foundations
│   ├── phase-6-langgraph/             # Ch 31-34: Workflow Orchestration
│   ├── phase-7-llamaindex/            # Ch 35-38: Advanced RAG
│   ├── phase-8-production/            # Ch 39-42: Production Systems
│   ├── phase-9-multi-agent/           # Ch 43-48: Multi-Agent Coordination
│   └── phase-10-civil-engineering/    # Ch 49-54: CE Application
│
├── templates/                         # 🎨 Chapter creation templates & guides
│   ├── MASTER-CHAPTER-TEMPLATE-V2.md  # Primary chapter template (USE THIS)
│   ├── chapter-template-cafe-style.md # Cafe-style writing examples
│   ├── chapter-template-guide.md      # How to use templates
│   └── section-templates/             # Individual section templates
│
├── guides/                            # 📖 Writing & teaching reference guides
│   ├── LANGUAGE-EXPANSION-GUIDE.md    # How to write comprehensive content (15 principles)
│   ├── WRITING-STYLE-GUIDE.md         # Voice, tone, structure, pedagogical patterns
│   ├── ANALOGY-LIBRARY.md             # 50+ tested analogies (to be created)
│   └── QUALITY-CHECKLIST.md           # Chapter review checklist (to be created)
│
├── prompts/                           # 🤖 AI prompts for curriculum generation
│   └── UNIFIED_CURRICULUM_PROMPT_v6.md # Primary teaching prompt
│
├── docs/                              # 📋 Planning & roadmap documents
│   ├── roadmap-v6.md                  # Complete curriculum roadmap
│   ├── ROADMAP-V6.1-ENHANCEMENTS.md   # Latest enhancements
│   ├── EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md # 15 pedagogical principles
│   ├── CURRICULUM-ENHANCEMENT-ANALYSIS-2026-01-20.md # Enhancement recommendations
│   ├── ENHANCEMENT-ACTION-PLAN-2026-01-20.md        # Implementation plan
│   ├── PATH-D-STRATEGIC-HYBRID.md     # Strategic direction
│   └── [version logs]                 # Historical planning docs
│
├── reference/                         # 🔍 Domain & context reference
│   ├── PROJECT-THREAD.md              # Project continuity tracking
│   └── ce-contexts.md                 # Civil Engineering domain context
│
└── examples/                          # 💡 Example implementations by phase
    ├── phase-1-llm/                   # Example code for Phase 1
    ├── phase-2-embeddings/            # Example code for Phase 2
    └── [other phases]/                #

```

---

## 🎯 Quick Navigation - "I Want To..."

### For Chapter Authors

| I Want To...                        | Go To...                                                               |
| ----------------------------------- | ---------------------------------------------------------------------- |
| **Create a new chapter**            | `/templates/MASTER-CHAPTER-TEMPLATE-V2.md`                             |
| **See chapter examples**            | `/chapters/phase-1-llm-fundamentals/chapter-07-your-first-llm-call.md` |
| **Learn writing guidelines**        | `/guides/WRITING-STYLE-GUIDE.md`                                       |
| **Understand 15 principles**        | `/docs/EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md`              |
| **Find analogies for concepts**     | `/guides/ANALOGY-LIBRARY.md` (to be created)                           |
| **Expand abbreviated content**      | `/guides/LANGUAGE-EXPANSION-GUIDE.md`                                  |
| **Check chapter quality**           | `/guides/QUALITY-CHECKLIST.md` (to be created)                         |
| **Understand curriculum structure** | `/docs/roadmap-v6.md`                                                  |
| **Review quality standards**        | `/docs/ENHANCEMENT-ACTION-PLAN-2026-01-20.md`                          |

### For AI Teaching Assistants

| I Want To...                    | Go To...                                                  |
| ------------------------------- | --------------------------------------------------------- |
| **Get teaching instructions**   | `/prompts/UNIFIED_CURRICULUM_PROMPT_v6.md`                |
| **Learn 15 principles**         | `/docs/EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md` |
| **Understand curriculum goals** | `/docs/roadmap-v6.md`                                     |
| **See teaching philosophy**     | `/docs/PATH-D-STRATEGIC-HYBRID.md`                        |
| **Find domain context**         | `/reference/ce-contexts.md`                               |
| **Track project connections**   | `/reference/PROJECT-THREAD.md`                            |

### For Students

| I Want To...               | Go To...                              |
| -------------------------- | ------------------------------------- |
| **Start the curriculum**   | Root `/curriculum/README.md`          |
| **Find Phase 1 chapters**  | `/chapters/phase-1-llm-fundamentals/` |
| **See example code**       | `/examples/phase-1-llm/`              |
| **Understand the roadmap** | `/docs/roadmap-v6.md`                 |

### For Reviewers

| I Want To...                 | Go To...                                              |
| ---------------------------- | ----------------------------------------------------- |
| **Review a chapter**         | `/guides/QUALITY-CHECKLIST.md`                        |
| **Check enhancement status** | `/docs/ENHANCEMENT-ACTION-PLAN-2026-01-20.md`         |
| **See what's changed**       | `/docs/CURRICULUM-ENHANCEMENT-ANALYSIS-2026-01-20.md` |
| **Verify standards**         | `/guides/WRITING-STYLE-GUIDE.md`                      |

---

## 📚 Detailed Directory Descriptions

### `/chapters/` - The Curriculum Content

**Purpose**: All learning chapters organized by teaching phase  
**Structure**: Phases 0-10, each containing related chapters  
**Naming**: `chapter-[XX]-[slug].md` format

**Key Files**:

- Each phase directory contains 4-7 related chapters
- Chapters build progressively within each phase
- See `/docs/roadmap-v6.md` for complete chapter listing

### `/templates/` - Chapter Creation Tools

**Purpose**: Templates and guides for creating new chapters  
**Primary Template**: `MASTER-CHAPTER-TEMPLATE-V2.md`

**Contents**:

1. **MASTER-CHAPTER-TEMPLATE-V2.md**: Complete chapter scaffold with enhancement guidelines
2. **chapter-template-cafe-style.md**: Examples of cafe-style conversational teaching
3. **chapter-template-guide.md**: How to use the templates effectively
4. **section-templates/**: Individual section examples (Coffee Shop Intro, Try This!, etc.)

**When to Use**: Every time you create a new chapter

### `/guides/` - Writing Reference Materials

**Purpose**: Comprehensive writing guidelines for content creators  
**Use**: Reference while writing, especially for enhancing existing content

**Contents**:

1. **LANGUAGE-EXPANSION-GUIDE.md**: How to transform abbreviated → comprehensive content (includes all 15 principles with examples)
2. **WRITING-STYLE-GUIDE.md**: Voice, tone, sentence structure, paragraph guidelines, 10 pedagogical patterns
3. **ANALOGY-LIBRARY.md**: 50+ tested analogies for common AI/Python concepts (to be created)
4. **QUALITY-CHECKLIST.md**: What every chapter must have before completion (to be created)

**Why These Exist**: To ensure consistent, friendly, comprehensive educational content that implements the "More is More" philosophy

**Core Philosophy**: All guides implement the 15 pedagogical principles documented in `/docs/EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md`

### `/prompts/` - AI Generation Prompts

**Purpose**: Prompts for AI assistants generating curriculum content  
**Primary File**: `UNIFIED_CURRICULUM_PROMPT_v6.md`

**What It Contains**:

- Teaching philosophy and approach
- Cafe-style language guidelines
- Property-based testing requirements
- Section structure requirements
- Example formats

**Who Uses This**: AI teaching assistants, curriculum generators

### `/docs/` - Planning & Roadmap Documents

**Purpose**: High-level planning, roadmaps, enhancement tracking  
**Key Documents**:

| Document                                            | Purpose                                        |
| --------------------------------------------------- | ---------------------------------------------- |
| `roadmap-v6.md`                                     | Complete 72-chapter curriculum structure       |
| `ROADMAP-V6.1-ENHANCEMENTS.md`                      | Latest additions (GraphRAG, Phoenix, etc.)     |
| `EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md` | **15 pedagogical principles (CORE REFERENCE)** |
| `CURRICULUM-ENHANCEMENT-ANALYSIS-2026-01-20.md`     | Comprehensive enhancement recommendations      |
| `ENHANCEMENT-ACTION-PLAN-2026-01-20.md`             | Implementation timeline & priorities           |
| `PATH-D-STRATEGIC-HYBRID.md`                        | Strategic curriculum direction                 |

**Version Logs** (Historical):

- `SESSION-COMPLETION-2026-01-17-FINAL.md`
- `ENHANCEMENT-IMPLEMENTATION-PLAN.md`
- `roadmap-v6-backup-20260118.md`

### `/reference/` - Domain & Context Materials

**Purpose**: Background context for the curriculum domain  
**Contents**:

- **PROJECT-THREAD.md**: How mini-projects connect across chapters
- **ce-contexts.md**: Civil Engineering domain explanations & terminology

**Why This Exists**: Later phases apply AI to Civil Engineering - this provides domain knowledge

### `/examples/` - Example Code Implementations

**Purpose**: Working code examples organized by phase  
**Structure**: Phase-based directories with runnable examples  
**Use**: Students can run these to see concepts in action

---

## 🚀 Workflow for Creating New Content

### Creating a New Chapter

1. **Read the Roadmap** → `/docs/roadmap-v6.md` to understand where your chapter fits
2. **Copy the Template** → `/templates/MASTER-CHAPTER-TEMPLATE-V2.md`
3. **Reference Writing Guidelines** → `/guides/WRITING-STYLE-GUIDE.md`
4. **Find Analogies** → `/guides/ANALOGY-LIBRARY.md`
5. **Write the Chapter** → Use expansion patterns from `/guides/LANGUAGE-EXPANSION-GUIDE.md`
6. **Review Quality** → Check against `/guides/QUALITY-CHECKLIST.md`
7. **Save** → `/chapters/phase-X-name/chapter-YY-slug.md`

### Enhancing an Existing Chapter

1. **Review Enhancement Guidelines** → `/docs/ENHANCEMENT-ACTION-PLAN-2026-01-20.md`
2. **Check Current Chapter** → `/chapters/phase-X/chapter-YY.md`
3. **Apply Expansion Patterns** → `/guides/LANGUAGE-EXPANSION-GUIDE.md`
4. **Add Analogies** → `/guides/ANALOGY-LIBRARY.md`
5. **Verify Quality** → `/guides/QUALITY-CHECKLIST.md`
6. **Update** → Overwrite the chapter file

### Generating with AI

1. **Provide Teaching Prompt** → `/prompts/UNIFIED_CURRICULUM_PROMPT_v6.md`
2. **Specify Chapter Details** → From `/docs/roadmap-v6.md`
3. **Reference Template** → `/templates/MASTER-CHAPTER-TEMPLATE-V2.md`
4. **Provide Domain Context** → `/reference/ce-contexts.md` (if needed)
5. **Review Output** → Against `/guides/QUALITY-CHECKLIST.md`

---

## 🗑️ Deprecated/Archive Locations

The following directories exist for historical reference but are NOT part of active curriculum:

- `/curriculum/references/` (note the 's') - Old structure, being consolidated
- Root level logs (`CURRICULUM-UPDATE-SUMMARY-2026-01-18.md`, `REBUILD_V2_COMPLETION_LOG.md`, etc.)

**TODO**: Migrate root-level logs to `/docs/archive/`

---

## 📝 File Naming Conventions

### Chapters

Format: `chapter-[NN]-[slug].md`

- `NN`: Two-digit chapter number (01, 07, 23)
- `slug`: Descriptive kebab-case identifier
- Example: `chapter-07-your-first-llm-call.md`

### Templates

Format: `[purpose]-template-[variant].md` or `MASTER-CHAPTER-TEMPLATE-V[X].md`

- Template files use CAPS for emphasis
- Variants describe the style/use case

### Guides

Format: `[TOPIC]-GUIDE.md`

- ALL CAPS for high-level guides
- Descriptive topic name
- Example: `LANGUAGE-EXPANSION-GUIDE.md`

### Documentation

Format: `[TITLE]-[date].md` for versioned docs, `[title]-v[X].md` for versioned specs

- Dates: `YYYY-MM-DD` format
- Versions: Major version numbers only
- Example: `roadmap-v6.md`, `ENHANCEMENT-ACTION-PLAN-2026-01-20.md`

---

## 🆕 Recent Changes (January 20, 2026)

### Session 1: Philosophy & Enhancement Framework

1. ✅ Created `/docs/EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md` (15 pedagogical principles)
2. ✅ Enhanced `/guides/LANGUAGE-EXPANSION-GUIDE.md` with all 15 principles
3. ✅ Enhanced `/guides/WRITING-STYLE-GUIDE.md` with 10 pedagogical patterns
4. ✅ Enhanced `/prompts/UNIFIED_CURRICULUM_PROMPT_v6.md` with teaching principles
5. ✅ Updated `/curriculum/CURRICULUM-ORGANIZATION.md` with philosophy references

### Pending Work

6. ⏳ TODO: Create `/guides/ANALOGY-LIBRARY.md` (50+ tested analogies)
7. ⏳ TODO: Create `/guides/QUALITY-CHECKLIST.md` (comprehensive review checklist)
8. ⏳ TODO: Update `/templates/MASTER-CHAPTER-TEMPLATE-V2.md` with expansion guidelines
9. ⏳ TODO: Create enhanced chapter examples (Ch 7, 17, 27)
10. ⏳ TODO: Apply principles systematically to all chapters

---

## 📞 Need Help?

**Can't find something?**

1. Check this file's Quick Navigation section
2. Look in the most logical directory based on file purpose
3. Search for keywords in `/docs/roadmap-v6.md`

**Creating new content?**

1. Start with `/templates/MASTER-CHAPTER-TEMPLATE-V2.md`
2. Reference `/guides/WRITING-STYLE-GUIDE.md`
3. Check quality with `/guides/QUALITY-CHECKLIST.md`

**Understanding the curriculum?**

1. Read `/curriculum/README.md` (student-facing intro)
2. Read `/docs/roadmap-v6.md` (complete structure)
3. Read `/docs/PATH-D-STRATEGIC-HYBRID.md` (philosophy)

---

**Remember**: This organization exists to make curriculum development easier and more consistent. When in doubt, consult the roadmap and templates!

**Last Updated**: January 20, 2026 by AI Engineering Tutor
