# Pilot Scaffolding Enhancement Workflow

**Status**: Active
**Pilot Target**: Chapter 13 (Embeddings)
**Standard**: Enhanced-23 (v2.2)

## 1. Pre-Analysis Phase (The "Investigator")

Before touching the file, analyze the existing content to identify:

1.  **The "Hook"**: What is the current intro? Is it boring? (e.g., "Embeddings are vectors" vs "The Infinite Library").
2.  **The "Gap"**: What specific pedagogical elements are missing?
    *   Missing visual diagrams?
    *   Missing "Stop and Think" checkpoints?
    *   Missing "War Stories"?
3.  **The "Unique Constraints"**: Does this chapter have heavy math, heavy infra, or heavy logic?
    *   *Math*: Needs visual intuition (graphs).
    *   *Infra*: Needs mental models (architecture diagrams).
    *   *Logic*: Needs decision matrices.

**Output**: A brief "Enhancement Strategy" list.

## 2. Template Application Phase (The "Architect")

Apply the `MASTER-CHAPTER-TEMPLATE-V2.md` structure (The 23-Point Framework).

*   **Retain**:
    *   Core logic (but prepare to scaffold it).
    *   Learning objectives.
*   **Inject**:
    *   **Metadata**: Update correct phase/time/properties.
    *   **Concept Map**: Create a Mermaid diagram showing flow.
    *   **Metacognition**: Insert 2-3 reflection boxes.
    *   **Error Prediction**: Create 1-2 "Spot the Bug" challenges.

## 3. Code Transformation Phase (The "Scaffolder")

**CRITICAL**: Apply the `SCAFFOLDING-TRANSFORMATION-GUIDE` principles.
*   **Goal**: Transform "passive reading" into "active building".
*   **Action**: Convert complete code examples into "Starter Code" with TODOs.
*   **Rules**:
    *   **Keep**: Function signatures, imports, docstrings, and verification scripts.
    *   **Remove**: The actual implementation logic inside the functions.
    *   **Add**: Rich comments, hints, and TODOs guiding the student.
    *   **Example**: Change `return x * 2` to `# TODO: Return x multiplied by 2`.

## 4. Customization Phase (The "Teacher")

Apply specific enhancements based on the "Unique Constraints" identified in Phase 1.

*   **For Ch 13 (Math)**: Add "The Geometry of Meaning" visual analogy.
*   **For Ch 14 (Db)**: Add "The Persistent Memory" analogy.
*   **For Ch 15 (Algo)**: Add "The Goldilocks Chunking" decision matrix.

## 4. Verification Phase (The "Tester")

Run the `verify_embeddings.py` (or equivalent) to ensure the code still works.
*   **Check**: Does the new "Scaffolding" break the flow?
*   **Check**: Are the analogies consistent?

## 5. Phase Completion Review

After all chapters in a phase are enhanced:
1.  **Link Check**: Do Ch 13 -> 14 transitions make sense?
2.  **Recall Check**: Does Ch 16 reference Ch 13 correctly?
3.  **Project Thread**: Is the "Semantic Search" mini-project consistent?

---

## Execution Command

To execute this workflow on a chapter:

```bash
/bmad-agent-core-bmad-master implement scaffolding for chapter-[N] using PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md
```