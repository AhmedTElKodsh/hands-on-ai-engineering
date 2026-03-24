# Chapter Enhancement & Scaffolding Workflow (Production)

**Status**: Active Standard
**Version**: 1.0
**Order**: Pedagogical Enhancement (Gold Master) → Scaffolding (Student Edition)
**Applies To**: All Curriculum Chapters (Phase 1-10)

---

## 🔁 The Core Loop

For every chapter, we execute this sequential process to ensure pedagogical depth before introducing active coding friction.

### Phase 1: The "Gold Master" (Pedagogical Enhancement)

**Goal**: Create the perfect "Teacher's Edition" of the chapter with working code, deep explanations, and 23-point framework alignment.

1.  **Pre-Analysis**:
    *   Identify the "Hook" (Analogy).
    *   Identify the "Unique Constraint" (Math, Infra, Logic).
    *   Review existing code for correctness.

2.  **Template Application**:
    *   Apply `MASTER-CHAPTER-TEMPLATE-V2.md`.
    *   **Metadata**: Update Phase/Time/Properties.
    *   **Visuals**: Add Mermaid diagrams (Concept Maps).
    *   **Metacognition**: Add "Stop and Think" checkpoints.
    *   **Error Prediction**: Add "Spot the Bug" challenges.
    *   **Narrative**: Rewrite Intro and Part 1-3 using "Cafe Style" (Three-Level Explanations).

3.  **Gold Master Verification**:
    *   Ensure the code examples in the chapter are **COMPLETE** and **WORKING**.
    *   Run the `verification` script against the complete code.

### Phase 2: The "Student Edition" (Scaffolding Transformation)

**Goal**: Convert the "Gold Master" into a challenge-based learning experience.

1.  **Code Transformation**:
    *   Follow `SCAFFOLDING-TRANSFORMATION-GUIDE`.
    *   **Target**: Core implementation functions (e.g., `get_embedding`, `Timer`, `RAG`).
    *   **Action**: Replace implementation logic with `pass`.
    *   **Inject**:
        *   **Docstrings**: Detailed specs of what to build.
        *   **TODOs**: Step-by-step comments.
        *   **Hints**: Collapsible `<details>` derived from the Gold Master code.

2.  **Preservation Rules**:
    *   **NEVER Scaffold**: Verification scripts (must remain complete to test the student).
    *   **NEVER Scaffold**: "Naive/Bad" examples (students need to see the problem).
    *   **NEVER Scaffold**: Setup/Boilerplate (imports, env var loading).

### Phase 3: Quality Control

1.  **Pedagogical Check**:
    *   Does the "Story" still make sense now that the code is empty?
    *   Do the hints accurately lead to the solution?

2.  **Technical Check**:
    *   Does the Verification Script still pass when the *Solution* (from Hints) is applied? (Mental check).

---

## Execution Commands

**Step 1: Create Gold Master**
```bash
/bmad-agent-core-bmad-master enhance chapter-[N] to Gold Master standard
```

**Step 2: Apply Scaffolding**
```bash
/bmad-agent-core-bmad-master transform chapter-[N] to Student Edition (Scaffolding)
```

**Combined Command (Standard)**
```bash
/bmad-agent-core-bmad-master run full enhancement workflow on chapter-[N]
```
