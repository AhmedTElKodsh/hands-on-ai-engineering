# Curriculum Transformation Glossary

This glossary defines shared terminology used across both curriculum transformation specifications.

## Tier Definitions (Shared Across Both Specs)

These tier definitions apply to **both** scaffolding conversion and pedagogical enhancement:

### TIER_1 (Foundations - Detailed Guidance)
**Target Audience**: Beginners learning fundamentals

**Scaffolding Characteristics**:
- Detailed step-by-step hints with examples
- More complete function signatures with type aliases explained
- TODO markers broken into granular steps
- Implementation approach guidance

**Enhancement Characteristics**:
- Detailed explanations in all 17 enhancement types
- More emotional support and encouragement
- Additional examples and analogies
- Extensive metacognitive prompting

**Chapters**: Typically phase-0 (foundations) and early phase-1

---

### TIER_2 (Intermediate - Moderate Guidance)
**Target Audience**: Students with foundation, building practical skills

**Scaffolding Characteristics**:
- Moderate strategic hints
- Standard function signatures with type hints
- TODO markers at logical boundaries
- Conceptual guidance without implementation details

**Enhancement Characteristics**:
- Moderate detail in enhancements
- Balanced support and autonomy
- Standard examples and analogies
- Regular metacognitive checkpoints

**Chapters**: Typically phase-1 through phase-7 (core skills building)

---

### TIER_3 (Advanced - Minimal Guidance)
**Target Audience**: Advanced students applying knowledge to complex problems

**Scaffolding Characteristics**:
- Minimal hints focusing on requirements only
- Basic function signatures (name, params, return type)
- TODO markers at high-level objectives
- Architectural guidance without tactical hints

**Enhancement Characteristics**:
- Minimal detail in enhancements
- Assumes prior knowledge and experience
- Brief examples, advanced analogies
- Sparse metacognitive prompting (student should self-regulate)

**Chapters**: Typically phase-8 through phase-10 (production, multi-agent, capstone)

---

## Core Terminology

### Chapter
A single curriculum markdown file (e.g., `chapter-07-your-first-llm-call.md`) containing:
- Learning objectives
- Conceptual explanations
- Code exercises
- Verification scripts
- Project threads

**Location**: `curriculum/chapters/phase-{N}-{name}/chapter-{NN}-{title}.md`

---

### Phase
A group of related chapters representing a major curriculum section:
- `phase-0-foundations`: Python fundamentals
- `phase-1-llm-fundamentals`: LLM basics
- `phase-2-embeddings-vectors`: Vector operations
- `phase-3-rag-fundamentals`: RAG systems
- `phase-4-langchain-core`: LangChain framework
- `phase-5-agents`: Agent patterns
- `phase-6-langgraph`: LangGraph orchestration
- `phase-7-llamaindex`: LlamaIndex framework
- `phase-8-production`: Observability, deployment
- `phase-9-multi-agent`: Multi-agent systems
- `phase-10-civil-engineering`: Capstone application

**Total**: 11 phases, ~55 chapters

---

### Scaffolding
Educational support structures that provide **guidance without complete solutions**:
- Function signatures (name, parameters, return types)
- Type hints (for IDE support and clarity)
- TODO markers (implementation steps)
- Strategic hints (approach, not code)
- Docstrings (expected behavior)

**Example**:
```python
def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate cosine similarity between two text embeddings.

    TODO:
    1. Generate embeddings for both texts using your embedding model
    2. Compute dot product of embedding vectors
    3. Divide by product of magnitudes (||a|| * ||b||)
    4. Return similarity score (0.0 to 1.0)

    Hint: Use numpy for vector operations (np.dot, np.linalg.norm)
    """
    pass  # Your implementation here
```

---

### Complete Solution
Working code implementation that provides the **full answer** to an exercise. This is what we are REMOVING during scaffolding conversion.

**Characteristics**:
- >5 lines of functional logic (not counting comments/docstrings)
- Complete algorithms with loops, conditionals, returns
- Full class implementations with all methods
- Complete test implementations with assertions

**Example of Complete Solution** (BEFORE conversion):
```python
def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate cosine similarity between two text embeddings."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)
    dot_product = np.dot(emb1, emb2)
    magnitude = np.linalg.norm(emb1) * np.linalg.norm(emb2)
    return float(dot_product / magnitude)
```

---

### Enhancement
A pedagogical improvement applied to a chapter. There are **17 enhancement types**:

1. **Metacognitive Prompts** (3 per chapter): Reflection questions
2. **Error Prediction Exercises** (2 per chapter): Debug challenges
3. **Real-World War Stories** (2 per chapter): Production failure examples
4. **Confidence Calibration** (1 per chapter): Self-assessment
5. **Emotional Checkpoints** (3-4 per chapter): Supportive moments
6. **Anticipatory Questions** (4-6 per chapter): Pre-learning activation
7. **Language Expansion**: Explain abbreviations, add "why" and "how"
8. **Descriptiveness Enhancement**: Add explanatory context
9. **Coffee Shop Intro Expansion** (250-350 words): Relatable scenario
10. **Spaced Repetition Callbacks** (2-3 per chapter): Review earlier concepts
11. **Graduated Scaffolding Indicator** (1 per chapter): Show learning progression
12. **Enhanced Analogies** (4 per chapter): Concrete mappings
13. **Failure-Forward Learning** (2-3 per chapter): Common mistakes
14. **Contextual Bridges** (2-3 per chapter): Connect to prior chapters
15. **Practical Application Hooks**: Real-world use cases
16. **Concept Map** (1 per chapter): Visual relationships
17. **Learning Style Indicators**: Icons for different learning modes

---

### Context-Aware
An enhancement or hint that **references actual chapter content** rather than using generic templates.

**Generic (NOT context-aware)**:
```
⚠️ Production War Story: A company once had a bug in [system_name] that cost them [amount].
```

**Context-Aware (GOOD)**:
```
⚠️ Production War Story: In 2023, a startup using RAG for customer support had their ChromaDB index corrupted during a deployment. Without proper backup strategies, they lost 50,000 customer conversation embeddings. Recovery took 3 days and cost $15K in re-processing. This is why Chapter 17's vector store initialization includes backup configuration.
```

---

### Quality Gate
A **checkpoint requiring validation** before proceeding to the next phase.

**Types**:
- **Sprint 0 Gate**: Infrastructure works with sample code
- **Pattern Gate**: Each conversion/enhancement pattern tested
- **Pilot Gate**: 3-chapter validation with real students
- **Scale Gate**: Quality metrics maintained during batch processing

**Characteristics**:
- Measurable pass/fail criteria
- Manual approval required for pilot gates
- Automated checks for technical gates
- Block progression until passed

---

### Pilot Validation
Testing with **3 representative chapters** before full-scale execution.

**Purpose**: De-risk the transformation by validating approach early

**Pilot Chapters**:
- Chapter 06A (foundations)
- Chapter 07 (LLM fundamentals)
- Chapter 17 (RAG fundamentals)

**Why These 3**:
- Span different difficulty levels
- Cover different technical domains
- Representative of curriculum diversity

**Success Metrics**:
- Phase 1: 80% student completion rate
- Phase 3: 85% quality score + 60% engagement

---

### Conversion Pattern
A **specific approach** for converting different code types to scaffolding:

**Pattern A (Functions)**: Extract signature, add TODO markers, strategic hints
**Pattern B (Classes)**: Preserve structure, remove method bodies, class-level hints
**Pattern C (Algorithms)**: Convert to pseudocode, add complexity notes
**Pattern D (Tests)**: Keep setup, remove assertions, add verification hints

---

### Type Hint
Python type annotations that specify expected types for parameters and return values:

```python
def search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    pass
```

**Coverage Threshold**: >95% of all function signatures must have complete type hints

---

### Hint
Strategic guidance that helps students **approach** a problem without revealing the solution.

**Hint Categories**:
1. **Conceptual**: What concepts apply? (e.g., "This requires vector similarity")
2. **Approach**: How to structure the solution? (e.g., "Break into 3 steps: embed, compute, normalize")
3. **Implementation**: What tools to use? (e.g., "Use numpy for vector operations")
4. **Resource**: Where to learn more? (e.g., "See Chapter 13 for embedding basics")

**Quality Standard**: Hints must NOT contain copy-paste-ready code

---

### Batch Processing
Processing **multiple chapters sequentially** with error resilience.

**Characteristics**:
- Continue on errors (don't halt entire batch)
- Report progress after each chapter
- Aggregate statistics at end
- Generate summary reports

**Typical Batch**: All chapters in a phase (e.g., phase-0-foundations: ~10 chapters)

---

## Quality Metrics

### Quality Score
A **0-100% score** measuring enhancement quality:
- Enhancement presence (all 17 types present)
- Context-awareness (no generic placeholders)
- Formatting correctness (icons, headers, structure)
- Tier consistency (detail matches tier level)

**Threshold**: 85% minimum for chapter completion

---

### Type Hint Coverage
Percentage of functions with **complete type hints** (all params + return type)

**Calculation**: (functions with hints / total functions) × 100%

**Threshold**: 95% minimum

---

### Student Completion Rate
Percentage of students who can **complete scaffolded exercises** without viewing original solutions.

**Measurement**: Manual testing with beta testers

**Threshold**: 80% minimum (pilot validation)

---

### Engagement Rate
Percentage of students who **interact with enhancements** (read war stories, answer metacognitive prompts, etc.)

**Measurement**: Survey + analytics (if available)

**Threshold**: 60% minimum

---

## Phase-Specific Terms

### Sprint 0
The **infrastructure sprint** that builds reusable components before implementation:
- Data models
- Template frameworks
- Parsing utilities
- Quality check functions

**Duration**: 1 week per phase

---

### Conversion Engine
The **core component** that converts complete code to scaffolding (Phase 1)

**Components**:
- Pattern matcher (identifies code type)
- Function/Class/Algorithm/Test converters
- Hint generator
- AST parser

---

### Enhancement Generator
The **core component** that generates pedagogical improvements (Phase 3)

**Components**:
- 17 specialized generators (one per enhancement type)
- Context analyzer (extracts concepts)
- Insertion point detector (finds optimal placement)
- Tier-specific detail adjuster

---

## Cross-References

**Phase 1 (Scaffolding) References Phase 3 (Enhancement)**:
- Phase 1 output = Phase 3 input
- Tier definitions shared
- Quality verification patterns similar
- Batch processing approach identical

**Both Phases Reference This Glossary**:
- All tier definitions
- All core terminology
- All quality metrics

---

## Document Control

**Version**: 1.0
**Created**: 2026-01-21
**Last Updated**: 2026-01-21
**Maintained By**: Curriculum Transformation Team
**Shared By**: curriculum-scaffolding-conversion + curriculum-pedagogical-enhancement specs
