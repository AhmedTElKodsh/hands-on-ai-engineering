# Implementation Plan: Curriculum Pedagogical Enhancement

## Overview

This implementation plan breaks down the curriculum pedagogical enhancement system into discrete coding tasks. The approach follows an incremental development strategy: build core data models first, implement context analysis, create enhancement generators for each of the 17 types, add quality verification, then integrate progress tracking and batch processing. Each task builds on previous work, with checkpoints to ensure functionality before proceeding.

**Project Location**: `src/curriculum_enhancer/` (new module in existing src/ structure)
**Test Location**: `tests/curriculum_enhancer/` (new test module)

**Key Difference from Scaffolding Conversion**: This system generates new pedagogical content rather than converting existing content. Enhancement generators use context analysis and LLM APIs to create educational improvements.

**Current Status**: No implementation exists yet. All tasks are pending.

## Tasks

- [ ] 1. Set up project structure and core data models
  - Create directory structure: `src/curriculum_enhancer/` with subdirectories for `models/`, `discovery/`, `context/`, `generators/`, `insertion/`, `verification/`, `tracking/`, `merge/`
  - Define all data models from design in `src/curriculum_enhancer/models/`:
    - `TierLevel`, `EnhancementStatus`, `EnhancementType` enums
    - `ChapterFile`, `Section`, `CodeBlock`, `ContentAnalysis` dataclasses
    - `Enhancement`, `EnhancementSet` dataclasses
    - `QualityScore`, `EnhancementPresenceReport`, `ContextAwarenessReport` dataclasses
    - `ContextViolation`, `PlaceholderViolation` dataclasses
    - `PhaseReport`, `FinalReport` dataclasses
    - `EnhancementConfig` dataclass
  - Create `__init__.py` files with proper exports
  - Add type hints to all models (use Python 3.10+ syntax)
  - _Requirements: 1.1-1.5, 2.1-2.5, 3.1-3.5, 4.1-4.5, 5.1-5.5, 6.1-6.5, 7.1-7.5, 8.1-8.5, 9.1-9.5, 10.1-10.5, 11.1-11.5, 12.1-12.5, 13.1-13.5, 14.1-14.5, 15.1-15.5, 16.1-16.5, 17.1-17.5_

- [ ]\* 1.1 Write property test for data model validation
  - Create `tests/curriculum_enhancer/properties/test_data_models.py`
  - **Property: Data Model Integrity**
  - Use hypothesis to generate random data model instances
  - Verify all fields have type hints
  - Verify dataclass instances can be created and serialized
  - **Validates: Requirements 18.1, 18.2, 18.3, 18.4, 18.5**

- [ ] 2. Implement Chapter Discovery Module
  - [ ] 2.1 Create `ChapterDiscovery` class in `src/curriculum_enhancer/discovery/chapter_discovery.py`
    - Implement `scan_phase()` to find all scaffolded `.md` files in a phase directory
    - Parse chapter filenames to extract chapter numbers and titles
    - Return list of `ChapterFile` objects with metadata
    - Handle edge cases: missing directories, non-markdown files, malformed filenames
    - _Requirements: 21.1, 21.2_
  - [ ] 2.2 Implement tier detection logic
    - Create `detect_tier()` method to analyze chapter metadata
    - Look for tier indicators in chapter frontmatter or METADATA section
    - Parse difficulty indicators (⭐ symbols, "Difficulty:" field, "TIER\_" markers)
    - Default to Tier 2 (TIER_2) when tier information unavailable
    - _Requirements: 19.1, 19.2, 19.3_
  - [ ] 2.3 Implement content analysis
    - Create `analyze_content()` to extract concepts and structure
    - Use regex patterns to extract markdown code fences and sections
    - Identify chapter sections by markdown headers (##, ###)
    - Extract code blocks with language and line numbers
    - Return `ContentAnalysis` object
    - _Requirements: 18.1, 18.2_
  - [ ] 2.4 Write unit tests for chapter discovery
    - Create `tests/curriculum_enhancer/discovery/test_chapter_discovery.py`
    - Test scanning phase-0-foundations directory
    - Test tier detection with sample chapters
    - Test content analysis with various chapter structures
    - Test error handling for missing/malformed files

- [ ]\* 2.5 Write property test for chapter discovery
  - Create `tests/curriculum_enhancer/properties/test_chapter_discovery.py`
  - **Property 12: Progress Tracking Accuracy**
  - Generate random chapter sets
  - Verify discovered chapters match expected counts
  - **Validates: Requirements 21.2, 21.3, 23.1, 23.2, 23.3, 23.4, 23.5**

- [ ] 3. Checkpoint - Verify chapter discovery works
  - Manually test scanning `curriculum/chapters/phase-0-foundations/` directory
  - Verify all scaffolded chapters are discovered with correct metadata
  - Ensure tier detection works or defaults correctly to TIER_2
  - Test with actual curriculum files
  - Ask the user if questions arise about chapter structure or metadata format

- [ ] 4. Implement Context Analysis Module
  - [ ] 4.1 Create `ContextAnalyzer` class in `src/curriculum_enhancer/context/analyzer.py`
    - Implement `extract_concepts()` using NLP-based keyword extraction
    - Use TF-IDF or similar to identify key terms and topics
    - Filter out common words and focus on domain-specific concepts
    - Return list of concepts (e.g., ["error handling", "exceptions", "Result type"])
    - _Requirements: 18.1, 18.2_
  - [ ] 4.2 Implement code structure parsing
    - Create `parse_code_structure()` method
    - Use Python's `ast` module to parse code blocks
    - Extract function names, signatures, and docstrings
    - Extract class names, methods, and docstrings
    - Identify algorithms by complexity patterns
    - Return `CodeStructure` object
    - _Requirements: 18.1, 18.2_
  - [ ] 4.3 Implement section identification
    - Create `identify_sections()` method
    - Parse markdown headers (##, ###, ####) to identify sections
    - Extract section titles, levels, and line boundaries
    - Build hierarchical section structure
    - Return list of `Section` objects
    - _Requirements: 18.1_
  - [ ] 4.4 Implement reference validation
    - Create `validate_references()` method
    - Check if enhancement text contains concepts from chapter
    - Check if enhancement references actual function/class names
    - Detect generic placeholders like "[concept]", "TODO", "example here"
    - Return boolean indicating context-awareness
    - _Requirements: 18.2, 18.3, 18.4, 18.5, 20.2_
  - [ ] 4.5 Write unit tests for context analysis
    - Create `tests/curriculum_enhancer/context/test_analyzer.py`
    - Test concept extraction with sample chapters
    - Test code structure parsing with various Python code
    - Test section identification with nested headers
    - Test reference validation with context-aware and generic text

- [ ]\* 4.6 Write property test for context-awareness
  - Create `tests/curriculum_enhancer/properties/test_context.py`
  - **Property 3: Context-Aware Enhancement Generation**
  - Generate random chapter content and enhancements
  - Verify enhancements reference actual chapter content
  - **Validates: Requirements 1.4, 3.3, 9.3, 18.1, 18.2, 18.3, 18.4, 18.5, 20.2**

- [ ] 5. Implement Insertion Point Detection Module
  - [ ] 5.1 Create `InsertionPointDetector` class in `src/curriculum_enhancer/insertion/detector.py`
    - Implement `find_section_boundaries()` to identify major conceptual sections
    - Parse markdown headers and identify section transitions
    - Return list of line numbers marking section boundaries
    - _Requirements: 1.2_
  - [ ] 5.2 Implement cognitive load detection
    - Create `find_cognitive_load_points()` method
    - Identify sections with complex code (nested loops, algorithms)
    - Identify sections with dense explanations (high word count, technical terms)
    - Use heuristics: code complexity, explanation density, concept count
    - Return list of line numbers for emotional checkpoint placement
    - _Requirements: 5.2_
  - [ ] 5.3 Implement concept introduction detection
    - Create `find_concept_introductions()` method
    - Identify where new concepts are first mentioned
    - Look for patterns: "What is X?", "X is a...", section headers with concept names
    - Return dict mapping concept to line number
    - _Requirements: 6.2_
  - [ ] 5.4 Implement section end detection
    - Create `find_section_ends()` method
    - Identify line numbers just before next section header
    - Return list of line numbers for application hook placement
    - _Requirements: 15.1_
  - [ ] 5.5 Implement final project location detection
    - Create `find_final_project_location()` method
    - Look for headers like "Bringing It All Together", "Final Project", "Capstone"
    - Return line number before final project section
    - _Requirements: 4.2_
  - [ ] 5.6 Write unit tests for insertion point detection
    - Create `tests/curriculum_enhancer/insertion/test_detector.py`
    - Test section boundary detection with sample chapters
    - Test cognitive load detection with complex code sections
    - Test concept introduction detection with various patterns
    - Test edge cases: chapters without final projects, very short chapters

- [ ]\* 5.7 Write property test for insertion point correctness
  - Create `tests/curriculum_enhancer/properties/test_insertion.py`
  - **Property 5: Enhancement Placement Correctness**
  - Generate random chapter structures
  - Verify insertion points match placement requirements
  - **Validates: Requirements 1.2, 4.2, 5.2, 6.2, 11.4, 14.5, 15.1, 16.4**

- [ ] 6. Checkpoint - Verify context analysis and insertion detection
  - Test context analysis with actual curriculum chapters
  - Verify concepts are extracted correctly
  - Test insertion point detection with sample chapters
  - Ensure cognitive load points are identified at complex sections
  - Ask the user if questions arise about heuristics or detection logic

- [ ] 7. Implement Enhancement Generators - Tier 1 (Part 1)
  - [ ] 7.1 Create base `EnhancementGenerator` class in `src/curriculum_enhancer/generators/base.py`
    - Initialize with `ContentAnalysis` and `TierLevel`
    - Provide helper methods for tier-specific detail adjustment
    - Implement common formatting utilities (icons, headers, markdown)
    - _Requirements: 18.1, 19.1, 19.2, 19.3_
  - [ ] 7.2 Implement Metacognitive Prompt Generator
    - Create `generate_metacognitive_prompts()` in `MetacognitiveGenerator` class
    - Generate 3 reflection questions per chapter
    - Reference concepts from chapter context
    - Use 🤔 icon and "Metacognitive Checkpoint" header
    - Adjust question depth based on tier (TIER_1: detailed, TIER_3: brief)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [ ] 7.3 Implement Error Prediction Generator
    - Create `generate_error_predictions()` in `ErrorPredictionGenerator` class
    - Generate 2 exercises per chapter with code snippets containing bugs
    - Include "Your prediction" prompt and collapsible explanation
    - Use 🔍 icon and "Error Prediction Challenge" header
    - Reference actual functions/patterns from chapter
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ] 7.4 Implement War Story Generator
    - Create `generate_war_stories()` in `WarStoryGenerator` class
    - Generate 2 stories per chapter with cost calculations
    - Include "The result", "The cost", "The fix", "Lesson" sections
    - Use ⚠️ icon and "Production War Story" header
    - Connect stories to chapter concepts
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  - [ ] 7.5 Write unit tests for Tier 1 generators (Part 1)
    - Create `tests/curriculum_enhancer/generators/test_tier1_part1.py`
    - Test metacognitive prompt generation with sample contexts
    - Test error prediction generation with code examples
    - Test war story generation with chapter concepts
    - Test tier-specific detail adjustment

- [ ]\* 7.6 Write property test for Tier 1 enhancements (Part 1)
  - Create `tests/curriculum_enhancer/properties/test_tier1_part1.py`
  - **Property 1: Enhancement Count Compliance (Tier 1 Part 1)**
  - Generate random chapter contexts
  - Verify metacognitive prompts (3), error predictions (2), war stories (2)
  - **Validates: Requirements 1.1, 2.1, 3.1**

- [ ] 8. Implement Enhancement Generators - Tier 1 (Part 2)
  - [ ] 8.1 Implement Confidence Calibration Generator
    - Create `generate_confidence_calibration()` in `ConfidenceCalibrationGenerator` class
    - Generate 1 calibration check per chapter
    - Include "Before" and "After" rating sections with calibration insights
    - Use 🎯 icon and "Confidence Calibration Check" header
    - Position before final project
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  - [ ] 8.2 Implement Emotional Checkpoint Generator
    - Create `generate_emotional_checkpoints()` in `EmotionalCheckpointGenerator` class
    - Generate 3-4 checkpoints per chapter
    - Use supportive, conversational language
    - Acknowledge difficulty and normalize struggle
    - Place at cognitively demanding sections
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  - [ ] 8.3 Implement Anticipatory Question Generator
    - Create `generate_anticipatory_questions()` in `AnticipatoryQuestionGenerator` class
    - Generate 4-6 questions per chapter
    - Create brief, thought-provoking prompts
    - Activate prior knowledge and connect to upcoming content
    - Place before concept introductions
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [ ] 8.4 Implement Language Expander
    - Create `expand_language()` in `LanguageExpander` class
    - Identify and expand abbreviations on first use
    - Add "why" and "how" explanations to technical statements
    - Preserve code blocks unchanged
    - Maintain technical accuracy while improving readability
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  - [ ] 8.5 Implement Descriptiveness Enhancer
    - Create `increase_descriptiveness()` in `DescriptivenessEnhancer` class
    - Add explanatory context to technical statements
    - Explain reasoning behind technical decisions
    - Connect concepts to practical applications
    - Maintain balance between detail and clarity
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  - [ ] 8.6 Write unit tests for Tier 1 generators (Part 2)
    - Create `tests/curriculum_enhancer/generators/test_tier1_part2.py`
    - Test confidence calibration generation
    - Test emotional checkpoint generation with supportive language
    - Test anticipatory question generation
    - Test language expansion and descriptiveness enhancement

- [ ]\* 8.7 Write property test for Tier 1 enhancements (Part 2)
  - Create `tests/curriculum_enhancer/properties/test_tier1_part2.py`
  - **Property 1: Enhancement Count Compliance (Tier 1 Part 2)**
  - **Property 7: Language Enhancement Preservation**
  - Verify confidence calibration (1), emotional checkpoints (3-4), anticipatory questions (4-6)
  - Verify code blocks unchanged after language enhancement
  - **Validates: Requirements 4.1, 5.1, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 8.5**

- [ ] 9. Checkpoint - Verify Tier 1 generators work
  - Test all 8 Tier 1 enhancement generators with sample chapters
  - Verify enhancements reference actual chapter content
  - Test tier-specific detail adjustment (TIER_1 vs TIER_2 vs TIER_3)
  - Ensure formatting is correct (icons, headers)
  - Ask the user if questions arise about enhancement generation

- [ ] 10. Implement Enhancement Generators - Tier 2
  - [ ] 10.1 Implement Coffee Shop Intro Expander
    - Create `expand_coffee_shop_intro()` in `CoffeeShopIntroExpander` class
    - Expand intro to 250-350 words
    - Create vivid, relatable scenario with specific details
    - Connect scenario to chapter concepts
    - Use ☕ icon
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  - [ ] 10.2 Implement Spaced Repetition Generator
    - Create `generate_spaced_repetition()` in `SpacedRepetitionGenerator` class
    - Generate 2-3 callbacks per chapter (when applicable)
    - Reference concepts from 3-4 chapters back
    - Include questions with collapsible answers
    - Explain relevance of earlier concept
    - Use 🔄 icon and "Quick Recall" header
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  - [ ] 10.3 Implement Scaffolding Indicator Generator
    - Create `generate_scaffolding_indicator()` in `ScaffoldingIndicatorGenerator` class
    - Generate 1 indicator per chapter
    - Show "Where we've been", "Where we are now", "Where we're going"
    - Explain current chapter's scaffolding level
    - Position early in chapter (after prerequisites)
    - Use 🎓 icon
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
  - [ ] 10.4 Implement Analogy Generator
    - Create `generate_analogies()` in `AnalogyGenerator` class
    - Generate 4 analogies per chapter with varied complexity
    - Map technical concepts to everyday experiences
    - Explain the mapping explicitly
    - Use descriptive headers and emoji icons
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_
  - [ ] 10.5 Implement Failure-Forward Generator
    - Create `generate_failure_forward()` in `FailureForwardGenerator` class
    - Generate 2-3 examples per chapter
    - Show common mistakes with explanations
    - Provide correct approach
    - Use "Common Mistake" and "Better Approach" sections
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
  - [ ] 10.6 Implement Contextual Bridge Generator
    - Create `generate_contextual_bridges()` in `ContextualBridgeGenerator` class
    - Generate 2-3 bridges per chapter
    - Connect current concepts to prior chapters
    - Explain how concepts build on each other
    - Reference specific chapter numbers and concepts
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_
  - [ ] 10.7 Implement Application Hook Generator
    - Create `generate_application_hooks()` in `ApplicationHookGenerator` class
    - Generate hooks at section ends
    - Provide specific use cases or scenarios (2-3 sentences)
    - Connect theory to practice
    - Use 💡 icon or "Real-World Application" header
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
  - [ ] 10.8 Write unit tests for Tier 2 generators
    - Create `tests/curriculum_enhancer/generators/test_tier2.py`
    - Test Coffee Shop Intro expansion with word count verification
    - Test spaced repetition with chapter history
    - Test scaffolding indicator generation
    - Test analogy generation with complexity variation
    - Test failure-forward and contextual bridge generation
    - Test application hook generation

- [ ]\* 10.9 Write property test for Tier 2 enhancements
  - Create `tests/curriculum_enhancer/properties/test_tier2.py`
  - **Property 1: Enhancement Count Compliance (Tier 2)**
  - **Property 8: Coffee Shop Intro Word Count**
  - Verify all Tier 2 enhancement counts
  - Verify Coffee Shop Intro is 250-350 words
  - **Validates: Requirements 9.1, 10.1, 11.1, 12.1, 13.1, 14.1, 15.1**

- [ ] 11. Implement Enhancement Generators - Tier 3
  - [ ] 11.1 Implement Concept Map Generator
    - Create `generate_concept_map()` in `ConceptMapGenerator` class
    - Generate 1 concept map per chapter
    - Show connections to prior and future chapters
    - Use ASCII art or markdown formatting
    - Position after "Where This Leads" section
    - Use 🗺️ icon and "Concept Map" header
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_
  - [ ] 11.2 Implement Learning Style Indicator Generator
    - Create `generate_learning_style_indicators()` in `LearningStyleIndicatorGenerator` class
    - Add icons throughout chapter: 📖 (reading), 👁️ (visual), 💻 (hands-on), 🎧 (auditory), 🤝 (social)
    - Place icons on section headers
    - Ensure all 5 learning styles represented
    - Add legend explaining icons
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_
  - [ ] 11.3 Write unit tests for Tier 3 generators
    - Create `tests/curriculum_enhancer/generators/test_tier3.py`
    - Test concept map generation with chapter connections
    - Test learning style indicator placement
    - Test legend generation
    - Verify all 5 icon types present

- [ ]\* 11.4 Write property test for Tier 3 enhancements
  - Create `tests/curriculum_enhancer/properties/test_tier3.py`
  - **Property 1: Enhancement Count Compliance (Tier 3)**
  - **Property 9: Learning Style Indicator Coverage**
  - Verify concept map (1) and learning style indicators present
  - Verify all 5 learning style icons appear
  - **Validates: Requirements 16.1, 17.1, 17.2, 17.3, 17.4, 17.5**

- [ ] 12. Checkpoint - Verify all 17 enhancement generators work
  - Test all 17 enhancement generators with sample chapters
  - Verify each generator produces context-aware content
  - Test tier-specific detail adjustment across all generators
  - Ensure all formatting requirements met (icons, headers, structure)
  - Test with chapters from different phases and tiers
  - Ask the user if questions arise about enhancement quality

---

### Pilot Sprint: 3-Chapter Enhancement Validation (1 week)

- [ ] 13. PILOT - Enhance pilot chapters
  - Enhance the **SAME 3 pilot chapters** from Phase 1 (scaffolding conversion):
    - **Chapter 06A** (already scaffolded in Phase 1)
    - **Chapter 07** (already scaffolded in Phase 1)
    - **Chapter 17** (already scaffolded in Phase 1)
  - Apply **ALL 17 enhancement types** to each chapter:
    1. Metacognitive prompts (3 per chapter)
    2. Error prediction exercises (2 per chapter)
    3. Real-world war stories (2 per chapter)
    4. Confidence calibration (1 per chapter)
    5. Emotional checkpoints (3-4 per chapter)
    6. Anticipatory questions (4-6 per chapter)
    7. Language expansion (throughout)
    8. Descriptiveness enhancement (throughout)
    9. Coffee Shop Intro expansion (250-350 words)
    10. Spaced repetition callbacks (2-3 per chapter, if applicable)
    11. Graduated scaffolding indicator (1 per chapter)
    12. Enhanced analogies (4 per chapter)
    13. Failure-forward learning (2-3 per chapter)
    14. Contextual bridges (2-3 per chapter)
    15. Practical application hooks (at section ends)
    16. Concept map (1 per chapter)
    17. Learning style indicators (throughout)
  - Use tier-appropriate detail levels (match tiers from Phase 1)
  - Ensure all enhancements reference **actual chapter content** (context-aware, not generic)
  - Save enhanced chapters to `_bmad-output/pilot/enhanced/`
  - _Time estimate: 6-9 hours (2-3 hours per chapter)_

- [ ] 14. PILOT - Quality verification
  - Run all quality checks on 3 enhanced chapters:
    - **Enhancement presence check**: MUST PASS - all 17 types present in each chapter
    - **Context-awareness validation**: MUST PASS - zero generic placeholders like "[concept]", "TODO", "[X]"
    - **Quality score calculation**: MUST PASS - 85%+ score for each chapter
    - **Placeholder detection**: MUST PASS - zero violations
    - **Formatting check**: All icons, headers, and structure correct
  - Generate quality reports for each chapter (save to `_bmad-output/pilot/reports/enhancement/`)
  - Compare enhancement distribution:
    - Count actual enhancements per type (verify meets requirements)
    - Measure context-awareness percentage (references to chapter concepts)
    - Assess tier consistency (detail level matches tier)
  - Document any quality issues found
  - _Time estimate: 2-3 hours_

- [ ] 15. PILOT - Educational impact test ⚠️ MANUAL GATE
  - **🚨 CRITICAL: This is a MANUAL testing gate - cannot be automated**
  - **Setup**:
    - Use **SAME 2-3 beta testers** from Phase 1 pilot (they already have scaffolded versions)
    - Provide enhanced chapters (scaffolding + all 17 enhancements)
    - Do NOT tell testers which parts are enhancements (let them discover naturally)
  - **Testing Protocol**:
    - Testers work through enhanced chapters as normal learning materials
    - Track engagement with enhancements:
      - Do they read war stories? (self-reported or eye-tracking)
      - Do they answer metacognitive prompts? (check written responses)
      - Do they interact with error prediction challenges?
      - Do analogies help understanding? (survey question)
    - Measure learning outcomes:
      - Pre/post confidence calibration comparison
      - Completion rate (should still be ≥80% from Phase 1)
      - Time-to-complete (faster or slower with enhancements?)
  - **Data Collection**:
    - **Engagement Rate**: % who interact with each enhancement type
      - Target: **60%+ overall engagement**
      - Measure per enhancement type (which get ignored? which get used?)
    - **Feedback Survey**:
      - "Which enhancements helped most?" (rank top 3)
      - "Which felt generic or irrelevant?" (flag for improvement)
      - "Did enhancements improve learning?" (Likert scale 1-5)
    - **Quality Assessment**:
      - Do war stories feel relevant or contrived?
      - Are analogies clear or confusing?
      - Are emotional checkpoints supportive or patronizing?
  - **Success Metrics**:
    - ✅ 85%+ quality score (automated check)
    - ✅ 60%+ engagement rate (manual measurement)
    - ✅ Positive feedback on enhancement relevance
  - _Time estimate: 3-5 days (tester time - can overlap with other work)_

- [ ] 16. PILOT - Iteration based on feedback
  - **Analysis Phase**:
    - Review engagement metrics and feedback
    - Identify which enhancement types had low engagement (<40%)
    - Identify which enhancements felt generic or irrelevant
    - Check if tier-specific detail was appropriate
  - **Improvement Phase**:
    - Update generators to improve context-awareness (more specific references)
    - Remove or redesign low-engagement enhancements
    - Adjust tier-specific templates based on feedback
    - Fix any generic placeholders found during testing
  - **Validation Phase**:
    - Re-enhance pilot chapters with improvements
    - Re-test engagement with SAME testers (measure improvement)
    - Verify quality score increased
  - Document all changes in `_bmad-output/pilot/enhancement-retrospective.md`
  - _Time estimate: 4-6 hours_

- [ ] 17. PILOT GATE - Validation checkpoint ⛔ MANDATORY GATE
  - **🚨 CRITICAL: Cannot proceed to Task 18 without passing this gate**
  - **Verification Checklist**:
    - ✅ **Quality Score**: 85%+ achieved for all 3 chapters
    - ✅ **Enhancement Presence**: All 17 types present and correctly formatted
    - ✅ **Context-Awareness**: Zero generic placeholders detected
    - ✅ **Engagement**: 60%+ interaction rate with enhancements
    - ✅ **Feedback**: Positive sentiment on relevance and helpfulness
    - ✅ **Improvements Validated**: Re-test showed measurable improvement
    - ✅ **Documentation Complete**: Enhancement retrospective written
  - **Gate Decision**:
    - ✅ **PASS**: All criteria met → Proceed to batch processing (Task 18+)
    - ❌ **FAIL**: Return to Task 16, iterate further (max 2 iterations)
    - ⚠️ **CONDITIONAL PASS**: 82-84% quality or 55-59% engagement → Discuss with stakeholders, document risks
  - **Output Artifacts**:
    - 3 enhanced pilot chapters (validated by students)
    - Quality reports showing 85%+ scores
    - Engagement metrics showing 60%+ interaction
    - Enhancement retrospective with lessons learned
    - Updated generators ready for scale phase
  - _Time estimate: 2 hours review + decision_

**Pilot Sprint Total: 1 week (3-5 days tester time + 1-2 days dev iteration)**

---

### Scale Phase

- [ ] 18. Implement Quality Verification Module
  - [ ] 13.1 Create `QualityVerification` class in `src/curriculum_enhancer/verification/quality.py`
    - Implement `verify_enhancement_presence()` method
    - Scan enhanced content for all 17 enhancement types
    - Check for required icons and headers for each type
    - Count occurrences of each enhancement type
    - Generate `EnhancementPresenceReport` with missing types
    - _Requirements: 20.1_
  - [ ] 13.2 Implement context-awareness verification
    - Create `verify_context_awareness()` method
    - Check each enhancement references chapter concepts
    - Validate function/class name references are accurate
    - Detect generic placeholders: "[concept]", "TODO", "example here", "[X]"
    - Calculate context-awareness percentage
    - Generate `ContextAwarenessReport` with violations
    - _Requirements: 18.2, 18.3, 18.4, 20.2, 20.4_
  - [ ] 13.3 Implement quality score calculation
    - Create `calculate_quality_score()` method
    - Calculate enhancement presence score (17/17 = 100%)
    - Calculate context-awareness score (% enhancements with references)
    - Calculate formatting score (% enhancements with correct format)
    - Calculate tier consistency score (detail level matches tier)
    - Compute overall score as weighted average
    - Generate `QualityScore` with breakdown
    - _Requirements: 20.3_
  - [ ] 13.4 Implement placeholder detection
    - Create `detect_placeholders()` method
    - Scan for placeholder patterns using regex
    - Check for template text like "Insert X here", "Add Y", "TODO"
    - Return list of `PlaceholderViolation` with line numbers
    - _Requirements: 18.3, 20.4_
  - [ ] 13.5 Write unit tests for quality verification
    - Create `tests/curriculum_enhancer/verification/test_quality.py`
    - Test enhancement presence detection with complete and incomplete chapters
    - Test context-awareness verification with generic and specific enhancements
    - Test quality score calculation with various scenarios
    - Test placeholder detection with known violations

- [ ]\* 13.6 Write property test for quality verification
  - Create `tests/curriculum_enhancer/properties/test_quality.py`
  - **Property 10: Quality Score Threshold Enforcement**
  - Generate random enhanced chapters with varying quality
  - Verify chapters below 85% are not marked complete
  - **Validates: Requirements 20.1, 20.3, 20.4, 20.5**

- [ ] 14. Implement Merge Utility Module
  - [ ] 14.1 Create `MergeUtility` class in `src/curriculum_enhancer/merge/utility.py`
    - Implement `create_continuation_file()` method
    - Generate continuation filename (e.g., chapter-06B-continuation-1.md)
    - Write continuation content to file in \_bmad-output/ directory
    - Return path to created continuation file
    - _Requirements: 22.1_
  - [ ] 14.2 Implement continuation merging
    - Create `merge_continuations()` method
    - Read main chapter file and all continuation files
    - Concatenate content in order with proper newline separation
    - Preserve content order and formatting
    - Return merged content as string
    - _Requirements: 22.2, 22.3_
  - [ ] 14.3 Implement markdown validation
    - Create `validate_markdown()` method
    - Parse merged content as markdown
    - Check for unclosed code fences, broken headers, malformed lists
    - Verify all sections have proper structure
    - Generate `MarkdownValidationReport` with errors and warnings
    - _Requirements: 22.4_
  - [ ] 14.4 Write unit tests for merge utility
    - Create `tests/curriculum_enhancer/merge/test_utility.py`
    - Test continuation file creation
    - Test merging with multiple continuation files
    - Test markdown validation with valid and invalid content
    - Test edge cases: empty continuations, missing files

- [ ]\* 14.5 Write property test for merge correctness
  - Create `tests/curriculum_enhancer/properties/test_merge.py`
  - **Property 13: Merge Utility Correctness**
  - Generate random chapter splits
  - Verify merged result equals single-file enhancement
  - **Validates: Requirements 22.1, 22.2, 22.3, 22.4**

- [ ] 15. Implement Progress Tracking Module
  - [ ] 15.1 Create `ProgressTracking` class in `src/curriculum_enhancer/tracking/progress.py`
    - Implement `update_chapter_status()` method
    - Maintain status tracking using JSON file (e.g., enhancement_status.json)
    - Support status transitions: NOT_STARTED → IN_PROGRESS → COMPLETED → VERIFIED
    - Store enhancement metadata (timestamp, quality score, enhancement counts)
    - Provide thread-safe status updates
    - _Requirements: 21.2, 23.1, 23.2_
  - [ ] 15.2 Implement phase reporting
    - Create `generate_phase_report()` method
    - Calculate enhancement statistics for a phase
    - Count completed vs remaining chapters
    - Calculate enhancement rate (completed / total)
    - Include quality metrics summary (avg quality score)
    - Generate `PhaseReport` with detailed statistics
    - _Requirements: 21.3, 23.5_
  - [ ] 15.3 Implement final reporting
    - Create `generate_final_report()` method
    - Aggregate statistics across all phases
    - Count total enhancements by type (metacognitive prompts, war stories, etc.)
    - Calculate overall quality score (weighted average)
    - List chapters needing review
    - Generate `FinalReport` with comprehensive metrics
    - _Requirements: 21.3, 23.4_
  - [ ] 15.4 Implement task list integration
    - Create `update_task_list()` method
    - Read tasks.md file
    - Update checkbox status for completed chapters ([ ] → [x])
    - Update progress summary with current counts
    - Preserve manual edits to tasks.md
    - _Requirements: 23.1, 23.2, 23.3_
  - [ ] 15.5 Write unit tests for progress tracking
    - Create `tests/curriculum_enhancer/tracking/test_progress.py`
    - Test status updates and transitions
    - Test phase report generation
    - Test final report aggregation
    - Test task list updates with sample tasks.md

- [ ]\* 15.6 Write property test for progress tracking
  - Create `tests/curriculum_enhancer/properties/test_progress.py`
  - **Property 12: Progress Tracking Accuracy**
  - Generate random enhancement scenarios
  - Verify completed + remaining = total always holds
  - **Validates: Requirements 21.2, 21.3, 23.1, 23.2, 23.3, 23.4, 23.5**

- [ ] 16. Checkpoint - Verify quality and tracking modules
  - Test quality verification with sample enhanced chapters
  - Verify quality score calculation is accurate
  - Test progress tracking updates correctly
  - Ensure reports generate accurate statistics
  - Test merge utility with large chapter splits
  - Ask the user if questions arise about quality thresholds or tracking

- [ ] 17. Implement main enhancement orchestrator
  - [ ] 17.1 Create `ChapterEnhancer` orchestrator class in `src/curriculum_enhancer/orchestrator.py`
    - Implement `enhance_chapter()` method that coordinates all modules
    - Call `ChapterDiscovery` to analyze chapter structure
    - Call `ContextAnalyzer` to extract concepts and code structure
    - Call `InsertionPointDetector` to find optimal placement locations
    - Call `EnhancementGenerator` for all 17 enhancement types
    - Insert enhancements at detected insertion points
    - Call `QualityVerification` to check output meets standards
    - Call `ProgressTracking` to update status
    - Return enhanced chapter content as string
    - Generate enhancement summary with metrics
    - _Requirements: 18.1, 18.2, 18.5, 19.1, 19.2, 19.3, 19.4, 19.5_
  - [ ] 17.2 Add error handling and recovery
    - Wrap enhancements in try-except blocks with specific exception handling
    - Handle file system errors gracefully (FileNotFoundError, PermissionError)
    - Handle LLM API errors with retry logic (rate limits, timeouts)
    - Create backup before enhancement (copy original to .backup file)
    - Support rollback on failure (restore from backup)
    - Log all errors with traceback for debugging
    - _Requirements: 21.5, 24.4_
  - [ ] 17.3 Write unit tests for orchestrator
    - Create `tests/curriculum_enhancer/test_orchestrator.py`
    - Test end-to-end enhancement of sample chapters
    - Test error handling with malformed input
    - Test backup and rollback functionality
    - Test quality check enforcement

- [ ]\* 17.4 Write integration test for full enhancement
  - Create `tests/curriculum_enhancer/integration/test_full_enhancement.py`
  - Test complete enhancement of a real chapter from phase-0-foundations
  - Verify all 17 enhancement types present
  - Validate output meets quality standards (85%+ score)
  - Test with chapter-06B-error-handling-patterns.md as reference

- [ ] 18. Implement batch processing
  - [ ] 18.1 Create `BatchProcessor` class in `src/curriculum_enhancer/batch.py`
    - Implement `process_phase()` method
    - Iterate through all chapters in a phase (use ChapterDiscovery)
    - Call `ChapterEnhancer` for each chapter
    - Maintain enhancement context across chapters (shared config, tracking)
    - Report progress after each chapter (print or log status)
    - Continue processing on errors (catch exceptions, log, continue)
    - Track successful and failed enhancements
    - _Requirements: 21.4, 21.5, 24.1, 24.2, 24.3, 24.4_
  - [ ] 18.2 Add batch completion reporting
    - Generate summary after batch completion
    - Count successful enhancements vs failures
    - List failed chapters with error details
    - Calculate batch quality metrics (avg quality score)
    - Save batch report to file (JSON or markdown)
    - _Requirements: 24.5_
  - [ ] 18.3 Write unit tests for batch processing
    - Create `tests/curriculum_enhancer/test_batch.py`
    - Test batch processing with multiple chapters
    - Test error resilience (continue on failure)
    - Test batch reporting
    - Test with mix of successful and failing enhancements

- [ ]\* 18.4 Write property test for batch resilience
  - Create `tests/curriculum_enhancer/properties/test_batch.py`
  - **Property 11: Batch Processing Resilience**
  - Generate random batch scenarios with errors
  - Verify processing continues and reports accurately
  - **Validates: Requirements 21.4, 21.5, 24.1, 24.2, 24.3, 24.4, 24.5**

- [ ] 19. Create command-line interface
  - [ ] 19.1 Implement CLI using `typer` in `src/curriculum_enhancer/cli.py`
    - Add command: `enhance-chapter <path>` - enhance single chapter
    - Add command: `enhance-phase <phase-name>` - enhance entire phase
    - Add command: `enhance-all` - enhance all phases in curriculum
    - Add command: `verify-chapter <path>` - run quality checks only
    - Add options: `--tier` (override tier detection), `--quality-threshold` (set min quality score)
    - Add options: `--backup/--no-backup` (control backup creation), `--output-dir` (specify output location)
    - Display progress with rich progress bars
    - Display results with formatted tables
    - _Requirements: 21.1, 21.4_
  - [ ] 19.2 Add verification command
    - Implement `verify-chapter <path>` command
    - Run all quality checks without enhancing
    - Display verification checklist results
    - Generate detailed quality report
    - Show specific issues with line numbers
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5_
  - [ ] 19.3 Write CLI tests
    - Create `tests/curriculum_enhancer/test_cli.py`
    - Test each CLI command with sample inputs
    - Test option handling
    - Test error messages and help text
    - Use typer's testing utilities

- [ ] 20. Create tasks.md integration
  - [ ] 20.1 Generate tasks.md from chapter list in `src/curriculum_enhancer/tasks_generator.py`
    - Create task list organized by phase
    - Add checkbox for each chapter enhancement
    - Include checkpoint tasks at phase boundaries
    - Add progress summary section at top
    - Generate markdown formatted output
    - _Requirements: 23.1, 23.3_
  - [ ] 20.2 Implement task status synchronization
    - Update tasks.md when chapters are enhanced
    - Mark checkboxes as complete automatically
    - Update progress summary with current counts
    - Preserve manual edits to tasks.md
    - _Requirements: 23.2, 23.4_
  - [ ] 20.3 Write tests for tasks.md integration
    - Create `tests/curriculum_enhancer/test_tasks_generator.py`
    - Test task list generation
    - Test status synchronization
    - Test progress summary updates

- [ ] 21. Final checkpoint - End-to-end testing
  - Enhance a complete test phase (phase-0-foundations recommended)
  - Verify all chapters enhanced successfully
  - Check all quality metrics pass (85%+ quality score, all 17 types present)
  - Validate tasks.md is updated correctly
  - Generate and review final report
  - Compare enhanced chapters with example (chapter-06B-enhancements-ALL-TIERS.md)
  - Test rollback functionality if needed
  - Ask the user if questions arise about final validation

- [ ] 22. Documentation and examples
  - [ ] 22.1 Create README.md in `src/curriculum_enhancer/`
    - Document installation and setup
    - Provide usage instructions for CLI commands
    - Explain configuration options
    - Include troubleshooting guide
  - [ ] 22.2 Document enhancement patterns
    - Create `docs/enhancement_patterns.md` with examples
    - Show before/after for each enhancement type
    - Explain tier-specific differences
    - Provide best practices
  - [ ] 22.3 Create example enhanced chapters
    - Use existing chapter-06B-enhancements-ALL-TIERS.md as reference
    - Document quality metrics for examples
    - Store in `examples/enhanced_chapters/`
  - [ ] 22.4 Document quality metrics
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
- The enhancement system uses Python 3.10+ with type hints throughout
- All data models use `@dataclass` for clean structure
- Quality verification is critical - no chapter should be marked complete without passing all checks (85%+ score, all 17 types)
- Progress tracking enables monitoring enhancement across 11 phases and ~55 chapters
- Batch processing with error resilience ensures one failure doesn't block entire enhancement
- Implementation location: `src/curriculum_enhancer/` (integrates with existing project structure)
- Test location: `tests/curriculum_enhancer/` (follows existing test organization)
- Use `typer` for CLI (modern, type-safe CLI framework)
- Use `hypothesis` for property-based testing (industry standard for Python)
- Use Python's `ast` module for code parsing (reliable, built-in)
- Store progress tracking in JSON (simple, portable)
- Enhancement generation may use LLM APIs for context-aware content creation

## Implementation Order Rationale

1. **Data models first** (Task 1): Foundation for all other components
2. **Discovery next** (Task 2): Understand what we're enhancing before enhancing
3. **Context analysis** (Task 4): Extract concepts and structure for context-aware generation
4. **Insertion point detection** (Task 5): Identify optimal placement locations
5. **Enhancement generators incrementally** (Tasks 7-11): Build and test each enhancement type independently
   - Tier 1 generators (8 types): Core pedagogical improvements
   - Tier 2 generators (7 types): Medium-effort enhancements
   - Tier 3 generators (2 types): Organizational enhancements
6. **Quality verification** (Task 13): Ensure enhancements meet standards
7. **Merge utility** (Task 14): Handle large chapters
8. **Progress tracking** (Task 15): Monitor enhancement progress
9. **Orchestration** (Task 17): Tie all components together
10. **Batch processing** (Task 18): Scale to multiple chapters
11. **CLI and docs** (Tasks 19-22): User interface and documentation

This order enables incremental development with validation at each step, minimizing risk and enabling early feedback.

## Key Differences from Scaffolding Conversion Spec

**Scaffolding Conversion** (curriculum-scaffolding-conversion):

- Transforms existing complete code into scaffolding
- Removes implementation details, adds TODOs and hints
- Primarily code transformation (AST manipulation)
- Input: Complete solutions → Output: Scaffolded exercises

**Pedagogical Enhancement** (curriculum-pedagogical-enhancement):

- Generates new pedagogical content
- Adds 17 enhancement types to existing scaffolded chapters
- Primarily content generation (LLM-based, context-aware)
- Input: Scaffolded chapters → Output: Enhanced chapters with pedagogical improvements

**Shared Patterns**:

- Both use modular pipeline architecture
- Both have quality verification with thresholds
- Both support batch processing with error resilience
- Both track progress across phases
- Both use Python 3.10+ with type hints and dataclasses

**Unique to Enhancement**:

- Context analysis for concept extraction
- 17 specialized enhancement generators
- Tier-appropriate detail adjustment
- Merge utility for large chapters
- Context-awareness validation (enhancements must reference actual chapter content)
