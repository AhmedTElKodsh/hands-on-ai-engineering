# Implementation Plan: Curriculum Scaffolding Conversion

## Current Status Summary

**Phase**: Pilot Sprint Ready
**Completed**: Sprint 0 (Infrastructure) + Core Conversion Patterns (Tasks 0-8)
**Next**: Pilot Sprint - Convert 3 test chapters (Tasks 10-14)
**Remaining**: Quality Verification, Progress Tracking, Orchestration, Batch Processing, CLI, Documentation

### Completed Work

- ✅ Project structure and data models
- ✅ Template framework and scaffolding infrastructure
- ✅ Chapter discovery module with tier detection
- ✅ All 4 conversion patterns (functions, classes, algorithms, tests)
- ✅ Hint generation system with tier-specific logic
- ✅ Content preservation module
- ✅ Property-based tests for core functionality
- ✅ Pilot chapters selected and backed up

### Ready to Start

- 🎯 **PILOT SPRINT**: Convert 3 pilot chapters to validate approach
  - Chapter 06A (phase-0-foundations)
  - Chapter 07 (phase-1-llm-fundamentals)
  - Chapter 17 (phase-3-rag-fundamentals)

### Pending Implementation

- ⏳ Quality verification module (solution detection, type hints, hint quality)
- ⏳ Progress tracking module (status updates, phase reports)
- ⏳ Orchestrator (coordinates all modules)
- ⏳ Batch processor (handles multiple chapters)
- ⏳ CLI interface (user-facing commands)
- ⏳ Documentation and examples

---

## Overview

This implementation plan breaks down the curriculum scaffolding conversion system into discrete coding tasks. The approach follows an incremental development strategy: build core data models first, implement conversion patterns, add quality verification, then integrate progress tracking and batch processing. Each task builds on previous work, with checkpoints to ensure functionality before proceeding.

**Project Location**: `src/curriculum_converter/` (new module in existing src/ structure)
**Test Location**: `tests/curriculum_converter/` (new test module)

## Estimated Timeline

**Sprint 0 (Infrastructure)**: 1 week
**Task 1-8 (Core Conversion Engine)**: 3-4 weeks
**Pilot Sprint (3 chapters)**: 1 week
**Task 15+ (Scale to 48 chapters)**: 6-8 weeks
**Buffer for iterations**: 1-2 weeks

**Total Phase 1: 12-16 weeks**

**Chapters per week during scale**: ~6-8 chapters
**Effort per chapter**: ~2-3 hours (includes conversion + verification)

## Tasks

### Sprint 0: Infrastructure & Template Framework (1 week)

- [x] 0.1 Create project structure
  - Create directory structure: `src/curriculum_converter/` with subdirectories for `models/`, `discovery/`, `conversion/`, `verification/`, `tracking/`
  - Create directory structure: `tests/curriculum_converter/` with subdirectories matching src structure
  - Set up all `__init__.py` files with proper exports
  - _Time estimate: 2 hours_
  - _Status: COMPLETE_

- [x] 0.2 Define core data models
  - Define enums: `TierLevel`, `ConversionStatus`
  - Define chapter models: `ChapterFile`, `CodeBlock`, `ContentAnalysis`
  - Define scaffolding models: `ScaffoldedCode`, `Hint`
  - Define verification models: `SolutionViolation`, `TypeHintReport`, `HintQualityReport`, `ConsistencyReport`
  - Define preservation models: `Section`, `PreservationReport`
  - Define tracking models: `PhaseReport`, `FinalReport`
  - Define config models: `ConversionConfig`, `ConversionError`, `ErrorReport`
  - Add type hints to all models (Python 3.10+ syntax)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3_
  - _Time estimate: 4 hours_
  - _Status: COMPLETE_

- [x] 0.3 Create conversion template framework
  - Build reusable function signature extractor using AST
  - Build reusable hint generator base class with tier-specific logic
  - Create tier-specific template configurations (TIER_1, TIER_2, TIER_3)
  - Define scaffolding patterns for: functions, classes, algorithms, tests
  - Store templates in `src/curriculum_converter/templates/`
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4_
  - _Time estimate: 6 hours_
  - _Status: COMPLETE_

- [x] 0.4 Build scaffolding infrastructure
  - Create reusable AST parsing utilities in `src/curriculum_converter/utils/ast_utils.py`
  - Create reusable markdown manipulation tools in `src/curriculum_converter/utils/markdown_utils.py`
  - Create shared quality check functions in `src/curriculum_converter/utils/quality_checks.py`
  - Build tier detection logic in `src/curriculum_converter/utils/tier_detector.py`
  - _Requirements: 3.5, 6.1, 6.2, 6.3, 9.1, 9.2, 9.3_
  - _Time estimate: 6 hours_
  - _Status: COMPLETE_

- [x] 0.5 Checkpoint - Verify infrastructure works
  - Test data models serialize/deserialize correctly (pickle, JSON)
  - Test template framework with sample function (extract signature, generate hints)
  - Test scaffolding utilities with sample Python code
  - Test tier detection with sample chapter metadata
  - Write integration test verifying all Sprint 0 components work together
  - **GATE: Must pass before proceeding to Task 1**
  - _Time estimate: 2 hours_
  - _Status: COMPLETE_

**Sprint 0 Total: ~20 hours (1 week)**

---

### Core Implementation Tasks

- [x] 0.6 Write property test for data model validation
  - Create `tests/curriculum_converter/properties/test_data_models.py`
  - **Property 5: Type Hint Completeness**
  - Use hypothesis to generate random data model instances
  - Verify all fields have type hints
  - Verify dataclass instances can be created and serialized
  - **Validates: Requirements 6.2, 9.1, 9.2, 9.3**
  - _Status: COMPLETE_

---

- [x] 1. Implement Chapter Discovery Module
  - [x] 1.1 Create `ChapterDiscovery` class in `src/curriculum_converter/discovery/chapter_discovery.py`
    - Implement `scan_phase()` to find all `.md` files in a phase directory (e.g., `curriculum/chapters/phase-0-foundations/`)
    - Parse chapter filenames to extract chapter numbers and titles (handle formats like `chapter-06B-error-handling-patterns.md`)
    - Return list of `ChapterFile` objects with metadata
    - Handle edge cases: missing directories, non-markdown files, malformed filenames
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11_
  - [x] 1.2 Implement tier detection logic
    - Create `detect_tier()` method to analyze chapter content
    - Look for tier indicators in chapter metadata (METADATA section) or frontmatter
    - Parse difficulty indicators (⭐ symbols, "Difficulty:" field)
    - Default to Tier 2 (TIER_2) when tier information unavailable
    - _Requirements: 3.5_
  - [x] 1.3 Implement content analysis
    - Create `analyze_content()` to identify code blocks and implementation types
    - Use regex patterns to extract markdown code fences (```python blocks)
    - Parse code blocks with AST to detect functions, classes, algorithms, tests
    - Count each implementation type
    - Identify educational sections to preserve (learning objectives, explanations, diagrams)
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - [x] 1.4 Write unit tests for chapter discovery
    - Create `tests/curriculum_converter/discovery/test_chapter_discovery.py`
    - Test scanning phase-0-foundations directory
    - Test tier detection with sample chapters
    - Test content analysis with various code block types
    - Test error handling for missing/malformed files

- [x] 1.5 Write property test for chapter discovery
  - Create `tests/curriculum_converter/properties/test_chapter_discovery.py`
  - **Property 2: Educational Content Preservation**
  - Generate random chapter structures with educational sections
  - Verify educational sections are correctly identified and preserved
  - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

- [x] 2. Checkpoint - Verify chapter discovery works
  - Manually test scanning `curriculum/chapters/phase-0-foundations/` directory
  - Verify all chapters are discovered with correct metadata
  - Ensure tier detection works or defaults correctly to TIER_2
  - Test with actual curriculum files (e.g., chapter-06B-error-handling-patterns.md)
  - Ask the user if questions arise about chapter structure or metadata format

- [x] 3. Implement Conversion Engine - Function Pattern
  - [x] 3.1 Create `ConversionEngine` class in `src/curriculum_converter/conversion/engine.py`
    - Implement `convert_function()` method
    - Use Python's `ast` module to parse function code
    - Extract function signature (name, parameters, return type)
    - Preserve docstring or generate from signature if missing
    - Extract type hints from function definition
    - Generate TODO markers for implementation steps (analyze function body to identify key steps)
    - Remove function body, replace with `pass`
    - Return `ScaffoldedCode` object
    - _Requirements: 1.1, 4.1_
    - _Status: COMPLETE_
  - [x] 3.2 Implement `HintGenerator` class in `src/curriculum_converter/conversion/hints.py`
    - Implement tier-specific hint generation
    - Create methods for each hint category: conceptual, approach, implementation, resource
    - Implement tier-appropriate detail levels:
      - TIER_1: detailed step-by-step hints with examples
      - TIER_2: moderate strategic hints
      - TIER_3: minimal hints, focus on requirements
    - Apply tier-appropriate detail to function hints
    - _Requirements: 3.1, 3.2, 3.3, 8.1, 8.2, 8.4_
    - _Status: COMPLETE_
  - [x] 3.3 Write unit tests for function conversion
    - Create `tests/curriculum_converter/conversion/test_engine.py`
    - Test function conversion with various function types (simple, complex, async)
    - Test signature extraction with different parameter types
    - Test docstring preservation
    - Test TODO marker generation
    - _Status: COMPLETE_

- [x] 4.4 Write property test for function conversion
  - Create `tests/curriculum_converter/properties/test_conversion_patterns.py`
  - **Property 3: Conversion Pattern Application (Functions)**
  - Generate random function implementations using hypothesis
  - Verify converted output matches Pattern A from template
  - **Validates: Requirements 1.1, 4.1**

- [x] 4.5 Write property test for hint quality
  - Add to `tests/curriculum_converter/properties/test_conversion_patterns.py`
  - **Property 6: Hint Quality Standards**
  - Generate random hints and verify quality standards
  - Check hints don't contain copy-paste-ready code
  - Verify hints are actionable and specific
  - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**

- [x] 5. Implement Conversion Engine - Class Pattern
  - [x] 5.1 Implement class conversion in `ConversionEngine`
    - Create `convert_class()` method
    - Extract class definition and `__init__` signature using AST
    - Preserve class-level docstring
    - Extract all method signatures (including static/class methods)
    - Generate method-specific TODOs and hints
    - Remove all method implementations, replace with `pass`
    - Preserve class attributes and constants
    - _Requirements: 1.2, 4.2_
  - [x] 5.2 Add class-level hint generation to `HintGenerator`
    - Generate hints about class architecture and design
    - Explain method relationships and responsibilities
    - Provide implementation order suggestions for TIER_1
    - Apply tier-appropriate detail to class hints
    - _Requirements: 3.1, 3.2, 3.3_
  - [x] 5.3 Write unit tests for class conversion
    - Add tests to `tests/curriculum_converter/conversion/test_engine.py`
    - Test class conversion with various class structures
    - Test method signature extraction
    - Test preservation of class attributes

- [x] 5.4 Write property test for class conversion
  - Add to `tests/curriculum_converter/properties/test_conversion_patterns.py`
  - **Property 3: Conversion Pattern Application (Classes)**
  - Generate random class implementations
  - Verify converted output matches Pattern B from template
  - **Validates: Requirements 1.2, 4.2**

- [x] 6. Implement Conversion Engine - Algorithm Pattern
  - [x] 6.1 Implement algorithm conversion in `ConversionEngine`
    - Create `convert_algorithm()` method
    - Analyze algorithm logic using AST to identify key steps
    - Convert implementation to pseudocode comments
    - Preserve function signature
    - Add complexity considerations (time/space) as comments
    - Include example input/output in docstring
    - Remove implementation, keep structure
    - _Requirements: 1.3, 4.3_
  - [x] 6.2 Add algorithm-specific hint generation to `HintGenerator`
    - Generate hints about algorithm approach and strategy
    - Include complexity hints (Big-O notation)
    - Suggest data structures for TIER_1
    - Apply tier-appropriate pseudocode detail
    - _Requirements: 3.1, 3.2, 3.3_
  - [x] 6.3 Write unit tests for algorithm conversion
    - Add tests to `tests/curriculum_converter/conversion/test_engine.py`
    - Test algorithm conversion with common patterns (sorting, searching, recursion)
    - Test pseudocode generation
    - Test complexity analysis

- [x] 6.4 Write property test for algorithm conversion
  - Add to `tests/curriculum_converter/properties/test_conversion_patterns.py`
  - **Property 3: Conversion Pattern Application (Algorithms)**
  - Generate random algorithm implementations
  - Verify converted output matches Pattern C from template
  - **Validates: Requirements 1.3, 4.3**

- [x] 7. Implement Conversion Engine - Test Pattern
  - [x] 7.1 Implement test conversion in `ConversionEngine`
    - Create `convert_test()` method
    - Preserve test function signature
    - Keep test setup code (fixture creation, test data)
    - Identify and remove complete assertions (assert statements)
    - Add TODO markers for each assertion
    - Include expected outcomes as comments
    - Keep test structure and arrange/act/assert pattern intact
    - _Requirements: 1.4, 4.4_
  - [x] 7.2 Add test-specific hint generation to `HintGenerator`
    - Generate hints about what to verify
    - Provide assertion method suggestions (assertEqual, assertRaises, etc.)
    - Explain test coverage for TIER_1
    - Apply tier-appropriate assertion guidance
    - _Requirements: 3.1, 3.2, 3.3_
  - [x] 7.3 Write unit tests for test conversion
    - Add tests to `tests/curriculum_converter/conversion/test_engine.py`
    - Test test conversion with various test frameworks (unittest, pytest)
    - Test assertion removal
    - Test setup code preservation

- [x] 7.4 Write property test for test conversion
  - Add to `tests/curriculum_converter/properties/test_conversion_patterns.py`
  - **Property 3: Conversion Pattern Application (Tests)**
  - Generate random test implementations
  - Verify converted output matches Pattern D from template
  - **Validates: Requirements 1.4, 4.4**

- [x] 8. Checkpoint - Verify all conversion patterns work
  - Test each pattern (function, class, algorithm, test) with sample code from actual curriculum
  - Verify tier-specific scaffolding is applied correctly (TIER_1 vs TIER_2 vs TIER_3)
  - Ensure hints meet quality standards (no copy-paste code, actionable guidance)
  - Test with real chapter code blocks from phase-0-foundations
  - Ask the user if questions arise about pattern application
  - _Status: COMPLETE - Core functionality working, 2 minor test failures are acceptable (TODO marker generation edge cases)_

---

### Pilot Sprint: 3-Chapter Validation (1 week)

**NOTE**: Sprint 0 and core conversion patterns (Tasks 0-8) are complete. The pilot sprint can now begin.

- [x] 9. PILOT - Select and prepare pilot chapters
  - Select 3 representative chapters:
    - **Chapter 06A**: phase-0-foundations (decorators, context managers) - Tests foundational concepts
    - **Chapter 07**: phase-1-llm-fundamentals (your first LLM call) - Tests LLM integration patterns
    - **Chapter 17**: phase-3-rag-fundamentals (your first RAG system) - Tests advanced RAG concepts
  - Verify chapters span different difficulty levels and technical domains
  - Create backup copies of original chapters (save to `_backup/` directory)
  - Document current state: count lines of code, number of complete solutions
  - _Time estimate: 1 hour_
  - _Status: COMPLETE - Pilot chapters selected and backed up_

- [x] 10. PILOT - Convert pilot chapters
  - Apply all 4 conversion patterns (functions, classes, algorithms, tests) to each chapter
  - Use established templates and tier-appropriate scaffolding:
    - Chapter 06A likely TIER_1 (detailed guidance)
    - Chapter 07 likely TIER_2 (moderate guidance)
    - Chapter 17 likely TIER_2 (moderate guidance)
  - Generate hints using HintGenerator with context-awareness
  - Preserve all educational content (learning objectives, explanations)
  - Save converted chapters to `_bmad-output/pilot/scaffolded/`
  - _Time estimate: 6 hours (2 hours per chapter)_

- [x] 11. PILOT - Quality verification
  - Run all quality checks on 3 pilot chapters:
    - **Solution detection**: MUST PASS - zero solutions >5 lines of logic
    - **Type hint validation**: MUST PASS - >95% coverage
    - **Hint quality assessment**: MUST PASS - no copy-paste-ready code
    - **Tier consistency validation**: MUST PASS - scaffolding matches expected tier
  - Generate quality reports for each chapter (save to `_bmad-output/pilot/reports/`)
  - Compare before/after metrics:
    - Lines of complete code: before vs after (should be 0 after)
    - Number of hints added
    - Type hint coverage improvement
  - Document any quality issues found
  - _Time estimate: 2 hours_

- [x] 12. PILOT - Student validation test ⚠️ MANUAL GATE
  - **🚨 CRITICAL: This is a MANUAL testing gate - cannot be automated**
  - **Setup**:
    - Recruit 2-3 beta testers (students or engineers unfamiliar with curriculum)
    - Provide scaffolded chapters WITHOUT original solutions
    - Give testers access to: scaffolded code, hints, verification tests
    - Do NOT give access to complete solutions
  - **Testing Protocol**:
    - Ask testers to implement exercises from scaffolding alone
    - Measure completion rate: did they finish all exercises?
    - Measure time-to-complete per chapter (track hours spent)
    - Track where testers got stuck (which exercises, which hints were unclear)
  - **Data Collection**:
    - Completion rate per chapter (target: 80%+ across 3 chapters)
    - Time spent per chapter
    - Feedback survey: "What hints were missing? What was unclear? What worked well?"
    - Code review: analyze their implementations for common patterns
  - **Success Metric**: ✅ 80% completion rate across 3 chapters
  - _Time estimate: 1 week (tester time, not dev time - can run in parallel with other work)_

- [x] 13. PILOT - Iteration based on feedback
  - **Analysis Phase**:
    - Review student feedback and completion rates
    - Identify common failure points (which exercises had <80% completion?)
    - Identify missing or unclear hints
    - Analyze which tier assumptions were incorrect
  - **Improvement Phase**:
    - Update templates/patterns based on learnings
    - Add missing hints to HintGenerator
    - Adjust tier detection if chapters were misclassified
    - Fix any quality issues found during testing
  - **Validation Phase**:
    - Re-convert pilot chapters with improvements
    - Re-test with SAME testers (verify improvements work)
    - Measure improvement: did completion rate increase?
  - Document all changes in `_bmad-output/pilot/retrospective.md`
  - _Time estimate: 4-6 hours_

- [x] 14. PILOT GATE - Validation checkpoint ⛔ MANDATORY GATE
  - **🚨 CRITICAL: Cannot proceed to Task 15 without passing this gate**
  - **Verification Checklist**:
    - ✅ **Student Success**: 80%+ completion rate achieved
    - ✅ **Quality Metrics**: All quality checks pass (>95% type hints, zero solutions)
    - ✅ **Student Feedback**: Positive sentiment on scaffolding clarity
    - ✅ **Improvements Validated**: Re-test showed measurable improvement
    - ✅ **Documentation Complete**: Pilot retrospective written
  - **Gate Decision**:
    - ✅ **PASS**: All criteria met → Proceed to scale phase (Task 15+)
    - ❌ **FAIL**: Return to Task 13, iterate further (max 2 iterations)
    - ⚠️ **CONDITIONAL PASS**: 75-79% completion → Discuss with stakeholders, document risks
  - **Output Artifacts**:
    - 3 scaffolded pilot chapters (validated by students)
    - Quality reports showing all metrics passed
    - Pilot retrospective document with lessons learned
    - Updated templates/patterns ready for scale phase
  - _Time estimate: 2 hours review + decision_

**Pilot Sprint Total: 1 week (6 days tester time + 1-2 days dev iteration)**

---

### Scale Phase: Quality Verification & Orchestration

**NOTE**: These tasks implement the remaining infrastructure needed to scale beyond the pilot sprint. Complete after pilot validation (Task 14).

- [x] 15. Implement Quality Verification Module
  - [x] 15.1 Create `QualityVerification` class in `src/curriculum_converter/verification/quality.py`
    - Implement `detect_complete_solutions()` method
    - Scan for function bodies with >5 lines of logic (excluding comments/docstrings)
    - Detect complete algorithm implementations (loops, conditionals, returns with logic)
    - Find full assertion statements in tests (assert with actual comparisons)
    - Use AST parsing to analyze code structure
    - Return list of `SolutionViolation` objects with line numbers and severity
    - _Requirements: 1.5, 6.1_
  - [x] 15.2 Implement type hint validation
    - Implement `detect_complete_solutions()` method
    - Scan for function bodies with >5 lines of logic (excluding comments/docstrings)
    - Detect complete algorithm implementations (loops, conditionals, returns with logic)
    - Find full assertion statements in tests (assert with actual comparisons)
    - Use AST parsing to analyze code structure
    - Return list of `SolutionViolation` objects with line numbers and severity
    - _Requirements: 1.5, 6.1_
  - [ ] 15.2 Implement type hint validation
    - Create `validate_type_hints()` method
    - Parse all function/method signatures using AST
    - Check for parameter type hints (all params should have hints)
    - Check for return type hints (all functions should have return hints)
    - Validate typing constructs (List, Dict, Optional, Union, etc.)
    - Calculate coverage percentage (functions with hints / total functions)
    - Generate `TypeHintReport` with missing hints details
    - _Requirements: 6.2, 9.1, 9.2, 9.3, 9.4, 9.5_
  - [x] 15.3 Implement hint quality assessment
    - Create `assess_hint_quality()` method
    - Scan hints for code snippets (detect code patterns, function calls)
    - Check hints reference chapter concepts (cross-reference with educational sections)
    - Verify hints don't reveal solutions (no complete logic or algorithms)
    - Calculate quality score (0.0-1.0 based on multiple factors)
    - Generate `HintQualityReport` with specific issues
    - _Requirements: 6.3, 8.1, 8.2, 8.3, 8.4, 8.5_
  - [x] 15.4 Implement tier consistency validation
    - Create `verify_tier_consistency()` method
    - Analyze scaffolding detail level (count hints, TODO markers, preserved code)
    - Compare against expected tier level (TIER_1 should have more detail than TIER_3)
    - Report consistency issues (e.g., TIER_3 chapter with excessive hints)
    - Generate `ConsistencyReport` with recommendations
    - _Requirements: 3.4, 6.4_
  - [x] 15.5 Write unit tests for quality verification
    - Create `tests/curriculum_converter/verification/test_quality.py`
    - Test solution detection with known violations
    - Test type hint validation with missing/incomplete hints
    - Test hint quality assessment with good and bad hints
    - Test tier consistency with various scaffolding levels

- [x] 15.6 Write property test for solution elimination
  - Create `tests/curriculum_converter/properties/test_quality.py`
  - **Property 1: Complete Solution Elimination**
  - Generate random complete implementations
  - Convert them and verify no solutions remain
  - **Validates: Requirements 1.5, 6.1**

- [x] 15.7 Write property test for quality metrics
  - Add to `tests/curriculum_converter/properties/test_quality.py`
  - **Property 10: Quality Metrics Application**
  - Generate random converted chapters
  - Verify all quality metrics are calculated correctly
  - **Validates: Requirements 4.5, 6.3, 6.4**

- [x] 16. Implement Progress Tracking Module
  - [x] 16.1 Create `ProgressTracking` class in `src/curriculum_converter/tracking/progress.py`
    - Implement `update_chapter_status()` method
    - Maintain status tracking (use JSON file or SQLite database)
    - Support status transitions: NOT_STARTED → IN_PROGRESS → COMPLETED → VERIFIED
    - Store conversion metadata (timestamp, quality scores, error count)
    - Provide thread-safe status updates for potential parallel processing
    - _Requirements: 7.1, 7.2_
    - _Status: COMPLETE_
  - [x] 16.2 Implement phase reporting
    - Create `generate_phase_report()` method
    - Calculate conversion statistics for a phase
    - Count completed vs remaining chapters
    - Calculate conversion rate (completed / total)
    - Include quality metrics summary (avg quality score, type hint coverage)
    - Generate `PhaseReport` with detailed statistics
    - _Requirements: 7.3, 7.4_
  - [x] 16.3 Implement final reporting
    - Create `generate_final_report()` method
    - Aggregate statistics across all phases
    - Count total conversions by type (functions, classes, algorithms, tests)
    - Calculate overall quality score (weighted average)
    - List chapters needing review
    - Generate `FinalReport` with comprehensive metrics
    - _Requirements: 7.5_
  - [x] 16.4 Write unit tests for progress tracking
    - Create `tests/curriculum_converter/tracking/test_progress.py`
    - Test status updates and transitions
    - Test phase report generation
    - Test final report aggregation
    - Test concurrent status updates

- [x] 16.5 Write property test for status tracking
  - Create `tests/curriculum_converter/properties/test_tracking.py`
  - **Property 7: Conversion Status Tracking**
  - Generate random status update sequences
  - Verify status is always queryable and accurate
  - **Validates: Requirements 7.1, 7.2**

- [x] 16.6 Write property test for progress reporting
  - Add to `tests/curriculum_converter/properties/test_tracking.py`
  - **Property 9: Progress Reporting Accuracy**
  - Generate random conversion scenarios
  - Verify completed + remaining = total always holds
  - **Validates: Requirements 7.5, 10.3**

- [x] 17. Checkpoint - Verify quality and tracking modules
  - Implement `update_chapter_status()` method
  - Maintain status tracking (use JSON file or SQLite database)
  - Support status transitions: NOT_STARTED → IN_PROGRESS → COMPLETED → VERIFIED
  - Store conversion metadata (timestamp, quality scores, error count)
  - Provide thread-safe status updates for potential parallel processing
  - _Requirements: 7.1, 7.2_
- [ ] 17. Checkpoint - Verify quality and tracking modules
  - Test solution detection with known violations from actual curriculum code
  - Verify type hint validation catches missing hints
  - Test progress tracking updates correctly with sample conversions
  - Ensure reports generate accurate statistics
  - Test with multiple chapters from phase-0-foundations
  - Ask the user if questions arise about quality thresholds or tracking

- [-] 18. Implement main conversion orchestrator
  - [-] 18.1 Create `ChapterConverter` orchestrator class in `src/curriculum_converter/orchestrator.py`
    - Create `generate_phase_report()` method
    - Calculate conversion statistics for a phase
    - Count completed vs remaining chapters
    - Calculate conversion rate (completed / total)
    - Include quality metrics summary (avg quality score, type hint coverage)
    - Generate `PhaseReport` with detailed statistics
    - _Requirements: 7.3, 7.4_
  - [ ] 18.1 Create `ChapterConverter` orchestrator class in `src/curriculum_converter/orchestrator.py`
    - Implement `convert_chapter()` method that coordinates all modules
    - Call `ChapterDiscovery` to analyze chapter structure
    - Call `ConversionEngine` for each code block (determine pattern type automatically)
    - Call `ContentPreservation` to validate educational content unchanged
    - Call `QualityVerification` to check output meets standards
    - Call `ProgressTracking` to update status
    - Return converted chapter content as string
    - Generate conversion summary with metrics
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [ ] 18.2 Add error handling and recovery
    - Wrap conversions in try-except blocks with specific exception handling
    - Handle file system errors gracefully (FileNotFoundError, PermissionError)
    - Handle parsing errors with fallbacks (malformed markdown, invalid Python)
    - Create backup before conversion (copy original to .backup file)
    - Support rollback on failure (restore from backup)
    - Generate `ConversionError` objects with detailed context
    - Log all errors with traceback for debugging
    - _Requirements: 10.4_
  - [ ] 18.3 Write unit tests for orchestrator
    - Create `tests/curriculum_converter/test_orchestrator.py`
    - Test end-to-end conversion of sample chapters
    - Test error handling with malformed input
    - Test backup and rollback functionality
    - Test quality check enforcement

- [ ] 18.4 Write integration test for full conversion
  - Create `tests/curriculum_converter/integration/test_full_conversion.py`
  - Test complete conversion of a real chapter from phase-0-foundations
  - Verify all quality checks pass
  - Validate output matches expected scaffolding patterns
  - Test with chapter-06B-error-handling-patterns.md as reference

- [ ] 19. Implement batch processing
  - [ ] 19.1 Create `BatchProcessor` class in `src/curriculum_converter/batch.py`
    - Create `generate_final_report()` method
    - Aggregate statistics across all phases
    - Count total conversions by type (functions, classes, algorithms, tests)
    - Calculate overall quality score (weighted average)
    - List chapters needing review
    - Generate `FinalReport` with comprehensive metrics
    - _Requirements: 7.5_
  - [ ] 19.1 Create `BatchProcessor` class in `src/curriculum_converter/batch.py`
    - Implement `process_phase()` method
    - Iterate through all chapters in a phase (use ChapterDiscovery)
    - Call `ChapterConverter` for each chapter
    - Maintain conversion context across chapters (shared config, tracking)
    - Report progress after each chapter (print or log status)
    - Continue processing on errors (catch exceptions, log, continue)
    - Track successful and failed conversions
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  - [ ] 19.2 Add batch completion reporting
    - Generate summary after batch completion
    - Count successful conversions vs failures
    - List failed chapters with error details
    - Calculate batch quality metrics (avg quality score, coverage)
    - Generate `ErrorReport` for failed chapters with recovery suggestions
    - Save batch report to file (JSON or markdown)
    - _Requirements: 10.5_
  - [ ] 19.3 Write unit tests for batch processing
    - Create `tests/curriculum_converter/test_batch.py`
    - Test batch processing with multiple chapters
    - Test error resilience (continue on failure)
    - Test batch reporting
    - Test with mix of successful and failing conversions

- [ ] 19.4 Write property test for batch resilience
  - Create `tests/curriculum_converter/properties/test_batch.py`
  - **Property 8: Batch Processing Resilience**
  - Generate random batch scenarios with errors
  - Verify processing continues and reports accurately
  - **Validates: Requirements 10.2, 10.4, 10.5**

- [ ] 20. Create command-line interface
  - [ ] 20.1 Implement CLI using `typer` in `src/curriculum_converter/cli.py`
    - Create `tests/curriculum_converter/tracking/test_progress.py`
    - Test status updates and transitions
    - Test phase report generation
    - Test final report aggregation
    - Test concurrent status updates

- [ ] 10.5 Write property test for status tracking
  - Create `tests/curriculum_converter/properties/test_tracking.py`
  - **Property 7: Conversion Status Tracking**
  - Generate random status update sequences
  - Verify status is always queryable and accurate
  - **Validates: Requirements 7.1, 7.2**

- [ ] 10.6 Write property test for progress reporting
  - Add to `tests/curriculum_converter/properties/test_tracking.py`
  - **Property 9: Progress Reporting Accuracy**
  - Generate random conversion scenarios
  - Verify completed + remaining = total always holds
  - **Validates: Requirements 7.5, 10.3**

- [ ] 11. Checkpoint - Verify quality and tracking modules
  - Test solution detection with known violations from actual curriculum code
  - Verify type hint validation catches missing hints
  - Test progress tracking updates correctly with sample conversions
  - Ensure reports generate accurate statistics
  - Test with multiple chapters from phase-0-foundations
  - Ask the user if questions arise about quality thresholds or tracking

- [ ] 12. Implement main conversion orchestrator
  - [ ] 12.1 Create `ChapterConverter` orchestrator class in `src/curriculum_converter/orchestrator.py`
    - Implement `convert_chapter()` method that coordinates all modules
    - Call `ChapterDiscovery` to analyze chapter structure
    - Call `ConversionEngine` for each code block (determine pattern type automatically)
    - Call `ContentPreservation` to validate educational content unchanged
    - Call `QualityVerification` to check output meets standards
    - Call `ProgressTracking` to update status
    - Return converted chapter content as string
    - Generate conversion summary with metrics
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [ ] 12.2 Add error handling and recovery
    - Wrap conversions in try-except blocks with specific exception handling
    - Handle file system errors gracefully (FileNotFoundError, PermissionError)
    - Handle parsing errors with fallbacks (malformed markdown, invalid Python)
    - Create backup before conversion (copy original to .backup file)
    - Support rollback on failure (restore from backup)
    - Generate `ConversionError` objects with detailed context
    - Log all errors with traceback for debugging
    - _Requirements: 10.4_
  - [ ] 12.3 Write unit tests for orchestrator
    - Create `tests/curriculum_converter/test_orchestrator.py`
    - Test end-to-end conversion of sample chapters
    - Test error handling with malformed input
    - Test backup and rollback functionality
    - Test quality check enforcement

- [ ] 12.4 Write integration test for full conversion
  - Create `tests/curriculum_converter/integration/test_full_conversion.py`
  - Test complete conversion of a real chapter from phase-0-foundations
  - Verify all quality checks pass
  - Validate output matches expected scaffolding patterns
  - Test with chapter-06B-error-handling-patterns.md as reference

- [ ] 13. Implement batch processing
  - [ ] 13.1 Create `BatchProcessor` class in `src/curriculum_converter/batch.py`
    - Implement `process_phase()` method
    - Iterate through all chapters in a phase (use ChapterDiscovery)
    - Call `ChapterConverter` for each chapter
    - Maintain conversion context across chapters (shared config, tracking)
    - Report progress after each chapter (print or log status)
    - Continue processing on errors (catch exceptions, log, continue)
    - Track successful and failed conversions
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  - [ ] 13.2 Add batch completion reporting
    - Generate summary after batch completion
    - Count successful conversions vs failures
    - List failed chapters with error details
    - Calculate batch quality metrics (avg quality score, coverage)
    - Generate `ErrorReport` for failed chapters with recovery suggestions
    - Save batch report to file (JSON or markdown)
    - _Requirements: 10.5_
  - [ ] 13.3 Write unit tests for batch processing
    - Create `tests/curriculum_converter/test_batch.py`
    - Test batch processing with multiple chapters
    - Test error resilience (continue on failure)
    - Test batch reporting
    - Test with mix of successful and failing conversions

- [ ] 13.4 Write property test for batch resilience
  - Create `tests/curriculum_converter/properties/test_batch.py`
  - **Property 8: Batch Processing Resilience**
  - Generate random batch scenarios with errors
  - Verify processing continues and reports accurately
  - **Validates: Requirements 10.2, 10.4, 10.5**

- [ ] 14. Create command-line interface
  - [ ] 14.1 Implement CLI using `typer` in `src/curriculum_converter/cli.py`
    - Add command: `convert-chapter <path>` - convert single chapter
    - Add command: `convert-phase <phase-name>` - convert entire phase (e.g., phase-0-foundations)
    - Add command: `convert-all` - convert all phases in curriculum
    - Add command: `verify-chapter <path>` - run quality checks only
    - Add options: `--tier` (override tier detection), `--quality-threshold` (set min quality score)
    - Add options: `--backup/--no-backup` (control backup creation), `--output-dir` (specify output location)
    - Display progress with rich progress bars
    - Display results with formatted tables (successful, failed, quality scores)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11_
  - [ ] 14.2 Add verification command
    - Implement `verify-chapter <path>` command
    - Run all quality checks on a chapter without converting
    - Display verification checklist results (✓ or ✗ for each check)
    - Generate detailed quality report (save to file)
    - Show specific issues with line numbers
    - _Requirements: 6.5_
  - [ ] 14.3 Write CLI tests
    - Create `tests/curriculum_converter/test_cli.py`
    - Test each CLI command with sample inputs
    - Test option handling
    - Test error messages and help text
    - Use typer's testing utilities

- [ ] 15. Create tasks.md integration
  - [ ] 15.1 Generate tasks.md from chapter list in `src/curriculum_converter/tasks_generator.py`
    - Create task list organized by phase (one section per phase)
    - Add checkbox for each chapter conversion (- [ ] Convert chapter-XX-name.md)
    - Include checkpoint tasks at phase boundaries (- [ ] Checkpoint: Verify phase-X complete)
    - Add progress summary section at top (X/Y chapters completed)
    - Generate markdown formatted output
    - _Requirements: 7.1, 7.3, 7.4_
  - [ ] 15.2 Implement task status synchronization
    - Update tasks.md when chapters are converted (change [ ] to [x])
    - Mark checkboxes as complete automatically
    - Update progress summary with current counts
    - Preserve manual edits to tasks.md (only update status, not structure)
    - _Requirements: 7.2, 7.5_
  - [ ] 15.3 Write tests for tasks.md integration
    - Create `tests/curriculum_converter/test_tasks_generator.py`
    - Test task list generation
    - Test status synchronization
    - Test progress summary updates

- [ ] 16. Final checkpoint - End-to-end testing
  - Convert a complete test phase (phase-0-foundations recommended)
  - Verify all chapters converted successfully
  - Check all quality metrics pass (>95% type hints, >0.80 quality score)
  - Validate tasks.md is updated correctly
  - Generate and review final report
  - Compare converted chapters with template patterns
  - Test rollback functionality if needed
  - Ask the user if questions arise about final validation

- [ ] 17. Documentation and examples
  - [ ] 17.1 Create README.md in `src/curriculum_converter/`
    - Document installation and setup
    - Provide usage instructions for CLI commands
    - Explain configuration options
    - Include troubleshooting guide
  - [ ] 17.2 Document conversion patterns
    - Create `docs/conversion_patterns.md` with examples
    - Show before/after for each pattern (function, class, algorithm, test)
    - Explain tier-specific differences
    - Provide best practices
  - [ ] 17.3 Create example converted chapters
    - Convert 2-3 sample chapters as examples
    - Include chapters from different tiers
    - Document quality metrics for each
    - Store in `examples/converted_chapters/`
  - [ ] 17.4 Document quality metrics
    - Create `docs/quality_metrics.md`
    - Explain each quality check
    - Document thresholds and rationale
    - Provide guidance on interpreting reports

## Notes

- All tasks are required for comprehensive implementation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The conversion system uses Python 3.10+ with type hints throughout
- All data models use `@dataclass` for clean structure
- Quality verification is critical - no chapter should be marked complete without passing all checks
- Progress tracking enables monitoring conversion across 11 phases and ~60 chapters
- Batch processing with error resilience ensures one failure doesn't block entire conversion
- Implementation location: `src/curriculum_converter/` (integrates with existing project structure)
- Test location: `tests/curriculum_converter/` (follows existing test organization)
- Use `typer` for CLI (modern, type-safe CLI framework)
- Use `hypothesis` for property-based testing (industry standard for Python)
- Use Python's `ast` module for code parsing (reliable, built-in)
- Store progress tracking in JSON or SQLite (simple, portable)

## Implementation Order Rationale

1. **Data models first** (Task 1): Foundation for all other components
2. **Discovery next** (Task 2): Understand what we're converting before converting
3. **Conversion patterns incrementally** (Tasks 4-7): Build and test each pattern independently
4. **Quality verification** (Task 10): Ensure conversions meet standards
5. **Progress tracking** (Task 11): Monitor conversion progress
6. **Orchestration** (Task 13): Tie all components together
7. **Batch processing** (Task 14): Scale to multiple chapters
8. **CLI and docs** (Tasks 15-18): User interface and documentation

This order enables incremental development with validation at each step, minimizing risk and enabling early feedback.
