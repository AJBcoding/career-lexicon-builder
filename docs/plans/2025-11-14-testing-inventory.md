# Testing Inventory - Coverage Gap Analysis

**Date:** 2025-11-14
**Baseline Coverage:** 30%
**Goal:** 80%+ coverage

## Executive Summary

Initial coverage analysis reveals significant testing gaps across the codebase. Out of 1,951 total statements, 1,364 lines (70%) are untested. Major gaps exist in:

- **LLM Analysis Layer** (`analyzers/`): 0% coverage
- **Core Systems** (`core/`): 0% coverage
- **Markdown Generation** (`generators/`): 0% coverage
- **Document Formatting** (`cv_formatting/`): 0-97% coverage (highly variable)
- **Utilities** (`utils/`): 58-92% coverage

## Coverage Analysis by Module

### Group 1: Foundation - Utils & Generators

#### utils/text_extraction.py
- **Current Coverage:** 58% (148/253 lines covered)
- **Missing:** 105 lines
- **Priority:** HIGH - Core functionality for document processing
- **Complexity:** HIGH - Complex parsing logic with multiple edge cases
- **Dependencies:** None (leaf module)

**Untested Areas:**
- Lines 129, 131, 135: XML extraction edge cases
- Lines 170: Error handling paths
- Lines 269-270: Document type detection
- Lines 301-366: Pages document XML extraction (66 lines)
- Lines 384-440: Keynote document processing (57 lines)
- Lines 458-531: PowerPoint processing (74 lines)
- Lines 575-587: Text cleanup functions
- Lines 653-659: Helper functions

**Test Strategy:**
- Mock XML parsing for .pages/.keynote formats
- Test error handling for malformed documents
- Test text cleanup and normalization functions
- Integration tests with actual document samples

#### utils/date_parser.py
- **Current Coverage:** 92% (47/51 lines covered)
- **Missing:** 4 lines
- **Priority:** MEDIUM - Well-tested, minor gaps
- **Complexity:** LOW - Simple parsing logic
- **Dependencies:** None (leaf module)

**Untested Areas:**
- Lines 81-82: Edge case handling
- Lines 93-94: Error path

**Test Strategy:**
- Add edge case tests for missing gaps
- Test malformed date strings

#### generators/hierarchical_generator.py
- **Current Coverage:** 0% (0/491 lines covered)
- **Missing:** 491 lines
- **Priority:** HIGH - Core output generation
- **Complexity:** VERY HIGH - Complex markdown generation with hierarchical structures
- **Dependencies:** None (generates output)

**Untested Areas:**
- Entire module untested (491 lines)
- Hierarchical structure generation
- Markdown formatting
- Citation handling
- Section organization

**Test Strategy:**
- Unit tests for individual formatting functions
- Integration tests for complete lexicon generation
- Validate markdown output format
- Test citation link generation

### Group 2: Core Systems

#### core/state_manager.py
- **Current Coverage:** 0% (0/82 lines covered)
- **Missing:** 82 lines
- **Priority:** HIGH - Critical for state persistence
- **Complexity:** MEDIUM - File I/O and state tracking
- **Dependencies:** utils (for file operations)

**Untested Areas:**
- Entire module untested
- State persistence to disk
- State loading and validation
- Incremental processing logic
- Hash-based change detection

**Test Strategy:**
- Mock file I/O operations
- Test state save/load cycle
- Test incremental update detection
- Test hash computation and comparison

#### core/document_processor.py
- **Current Coverage:** 0% (0/106 lines covered)
- **Missing:** 106 lines
- **Priority:** HIGH - Core document processing pipeline
- **Complexity:** HIGH - Orchestrates multiple analyzers
- **Dependencies:** utils/text_extraction, analyzers

**Untested Areas:**
- Entire module untested
- Document classification
- Text extraction pipeline
- Analyzer orchestration
- Error handling and recovery

**Test Strategy:**
- Mock text extraction
- Mock analyzer calls
- Test document type detection
- Test error handling for malformed documents
- Integration tests with real documents

#### core/orchestrator.py
- **Current Coverage:** 0% (0/44 lines covered)
- **Missing:** 44 lines
- **Priority:** HIGH - Main orchestration logic
- **Complexity:** MEDIUM - Coordinates processing workflow
- **Dependencies:** core/document_processor, core/state_manager

**Untested Areas:**
- Entire module untested
- Workflow orchestration
- Analyzer coordination
- Output generation coordination

**Test Strategy:**
- Mock document processor
- Mock state manager
- Test workflow execution
- Test error propagation

### Group 3: Analysis Layer

#### analyzers/llm_analyzer.py
- **Current Coverage:** 0% (0/88 lines covered)
- **Missing:** 88 lines
- **Priority:** CRITICAL - Core LLM integration
- **Complexity:** HIGH - API integration, error handling, streaming
- **Dependencies:** anthropic SDK

**Untested Areas:**
- Entire module untested
- Claude API integration
- Prompt construction
- Response parsing
- Error handling (rate limits, API errors)
- Retry logic

**Test Strategy:**
- Mock Anthropic API calls
- Test prompt template interpolation
- Test response parsing
- Test error handling (network, API errors)
- Test retry logic and backoff
- Mock streaming responses

#### analyzers/llm_prompt_templates.py
- **Current Coverage:** 0% (0/4 lines covered)
- **Missing:** 4 lines
- **Priority:** MEDIUM - Template definitions
- **Complexity:** LOW - Mostly string constants
- **Dependencies:** None

**Untested Areas:**
- Template string validation
- Template variable interpolation

**Test Strategy:**
- Validate template formats
- Test variable substitution
- Ensure all placeholders are valid

### Group 4: Formatting System

#### cv_formatting/style_applicator.py
- **Current Coverage:** 65% (114/175 lines covered)
- **Missing:** 61 lines
- **Priority:** HIGH - Core formatting logic
- **Complexity:** HIGH - Document manipulation
- **Dependencies:** python-docx, template_builder

**Untested Areas:**
- Lines 89-91: Edge case handling
- Lines 101-102: Error paths
- Lines 110-111: Style application errors
- Lines 136, 139: Validation logic
- Lines 193-249: Cover letter mode formatting (57 lines)
- Lines 257-282: Advanced styling (26 lines)
- Line 296: Cleanup logic

**Test Strategy:**
- Test cover letter formatting mode
- Test error handling for missing styles
- Test advanced styling features
- Integration tests with real templates

#### cv_formatting/template_builder.py
- **Current Coverage:** 97% (94/97 lines covered)
- **Missing:** 3 lines
- **Priority:** LOW - Well-tested
- **Complexity:** MEDIUM
- **Dependencies:** python-docx

**Untested Areas:**
- Lines 53-55: Minor edge case

**Test Strategy:**
- Add tests for missing edge case

#### cv_formatting/style_parser.py
- **Current Coverage:** 90% (35/39 lines covered)
- **Missing:** 4 lines
- **Priority:** LOW - Well-tested
- **Complexity:** LOW
- **Dependencies:** python-docx

**Untested Areas:**
- Lines 49, 69, 73, 77: Error handling paths

**Test Strategy:**
- Add error handling tests

#### cv_formatting/metadata_inference.py
- **Current Coverage:** 58% (60/103 lines covered)
- **Missing:** 43 lines
- **Priority:** MEDIUM - Metadata extraction
- **Complexity:** MEDIUM
- **Dependencies:** None

**Untested Areas:**
- Line 26: Initialization edge case
- Line 63: Error path
- Lines 78-99: Header detection logic (22 lines)
- Lines 103-118: Date extraction (16 lines)
- Lines 122-127: Name extraction (6 lines)
- Lines 140-145: Salutation detection (6 lines)
- Lines 196, 242: Helper functions

**Test Strategy:**
- Test header detection with various formats
- Test date extraction patterns
- Test name and salutation detection
- Test edge cases with malformed documents

#### cv_formatting/learning_system.py
- **Current Coverage:** 74% (51/69 lines covered)
- **Missing:** 18 lines
- **Priority:** MEDIUM - Adaptive behavior
- **Complexity:** MEDIUM
- **Dependencies:** File I/O

**Untested Areas:**
- Lines 26, 37-38, 45: Initialization paths
- Lines 51-53, 57: Configuration loading
- Lines 73-74: Save operations
- Lines 160, 163, 170, 174-179: Learning update logic (9 lines)

**Test Strategy:**
- Mock file I/O
- Test configuration persistence
- Test learning updates
- Test correction application

#### cv_formatting/image_generator.py
- **Current Coverage:** 29% (10/34 lines covered)
- **Missing:** 24 lines
- **Priority:** MEDIUM - Image handling
- **Complexity:** MEDIUM
- **Dependencies:** PIL/Pillow

**Untested Areas:**
- Lines 31-73: Most image generation logic (43 lines)

**Test Strategy:**
- Mock PIL operations
- Test image generation with various inputs
- Test error handling for invalid images

#### cv_formatting/pdf_converter.py
- **Current Coverage:** 26% (9/34 lines covered)
- **Missing:** 25 lines
- **Priority:** MEDIUM - PDF conversion
- **Complexity:** MEDIUM
- **Dependencies:** python-docx, external tools

**Untested Areas:**
- Lines 28-71: PDF conversion logic (44 lines)

**Test Strategy:**
- Mock PDF conversion operations
- Test with sample .docx files
- Test error handling

#### cv_formatting/play_titles_lookup.py
- **Current Coverage:** 15% (8/53 lines covered)
- **Missing:** 45 lines
- **Priority:** LOW - Domain-specific lookup
- **Complexity:** LOW
- **Dependencies:** None

**Untested Areas:**
- Lines 18-25: Initialization (8 lines)
- Lines 29-54: Lookup logic (26 lines)
- Lines 66-98: Data loading (33 lines)
- Lines 111-115: Helper functions (5 lines)

**Test Strategy:**
- Test title lookup with known titles
- Test fuzzy matching
- Test data loading

#### cv_formatting/edit_cv_content.py
- **Current Coverage:** 0% (0/103 lines covered)
- **Missing:** 103 lines
- **Priority:** MEDIUM - Content editing
- **Complexity:** MEDIUM
- **Dependencies:** python-docx

**Untested Areas:**
- Entire module untested

**Test Strategy:**
- Test content editing operations
- Test document manipulation
- Integration tests with templates

#### cv_formatting/regenerate_cv.py
- **Current Coverage:** 0% (0/42 lines covered)
- **Missing:** 42 lines
- **Priority:** MEDIUM - CV regeneration
- **Complexity:** MEDIUM
- **Dependencies:** style_applicator, template_builder

**Untested Areas:**
- Entire module untested

**Test Strategy:**
- Test CV regeneration workflow
- Integration tests with templates

#### cv_formatting/update_template_margins.py
- **Current Coverage:** 0% (0/66 lines covered)
- **Missing:** 66 lines
- **Priority:** LOW - Template maintenance
- **Complexity:** LOW
- **Dependencies:** python-docx

**Untested Areas:**
- Entire module untested

**Test Strategy:**
- Test margin updates
- Validate template modifications

### Group 5-7: Wrapper Backend

**Note:** Wrapper-backend coverage analysis encountered test execution issues (hanging on authorization tests). This needs to be addressed separately.

**Known Status:**
- Some tests exist (47 collected)
- Tests passing: anthropic_service, api_preview, authorization (partial)
- Tests failing: api_projects, api_skills, auth (authentication issues)
- Test hanging: authorization tests (database-related)

**Action Required:**
- Debug test hanging issue
- Fix database test isolation
- Re-run coverage analysis once tests are stable

## Summary by Dependency Group

### Phase 1: Foundation (Ready to Test)
- **utils/text_extraction.py** - 58% → Target: 85%
- **utils/date_parser.py** - 92% → Target: 95%
- **generators/hierarchical_generator.py** - 0% → Target: 80%

### Phase 2: Core Systems (Depends on Phase 1)
- **core/state_manager.py** - 0% → Target: 85%
- **core/document_processor.py** - 0% → Target: 85%
- **core/orchestrator.py** - 0% → Target: 80%

### Phase 3: Analysis Layer (Depends on Phase 2)
- **analyzers/llm_analyzer.py** - 0% → Target: 85%
- **analyzers/llm_prompt_templates.py** - 0% → Target: 90%

### Phase 4: Formatting System (Parallel to Phase 2-3)
- **cv_formatting/style_applicator.py** - 65% → Target: 85%
- **cv_formatting/metadata_inference.py** - 58% → Target: 80%
- **cv_formatting/learning_system.py** - 74% → Target: 85%
- **cv_formatting/image_generator.py** - 29% → Target: 75%
- **cv_formatting/pdf_converter.py** - 26% → Target: 75%
- **cv_formatting/play_titles_lookup.py** - 15% → Target: 70%
- **cv_formatting/edit_cv_content.py** - 0% → Target: 75%
- **cv_formatting/regenerate_cv.py** - 0% → Target: 75%
- **cv_formatting/update_template_margins.py** - 0% → Target: 70%
- **cv_formatting/template_builder.py** - 97% → Target: 98%
- **cv_formatting/style_parser.py** - 90% → Target: 95%

## Test Stub Creation Plan

### Immediate Actions

1. **Create missing test files:**
   - `tests/test_llm_analyzer.py` (expand existing)
   - `tests/test_llm_prompt_templates.py`
   - `tests/test_hierarchical_generator.py`
   - `tests/test_metadata_inference.py`
   - `tests/test_edit_cv_content.py`
   - `tests/test_regenerate_cv.py`
   - `tests/test_update_template_margins.py`
   - `tests/test_play_titles_lookup.py`

2. **Expand existing test files:**
   - `tests/test_text_extraction.py` - Add 105 missing line coverage
   - `tests/test_date_parser.py` - Add 4 missing lines
   - `tests/test_style_applicator.py` - Add cover letter mode tests (61 lines)
   - `tests/test_metadata_inference.py` - Add 43 missing lines
   - `tests/test_learning_system.py` - Add 18 missing lines
   - `tests/test_image_generator.py` - Add 24 missing lines
   - `tests/test_pdf_converter.py` - Add 25 missing lines
   - `tests/test_template_builder.py` - Add 3 missing lines
   - `tests/test_style_parser.py` - Add 4 missing lines

3. **Fix wrapper-backend test issues:**
   - Debug authorization test hanging
   - Fix database test isolation
   - Re-run coverage analysis

## Estimated Effort

### Lines to Test
- **Root-level:** 1,364 untested lines
- **Estimated test code:** ~2,700-4,000 lines (2-3x source code)

### Time Estimate by Phase
- **Phase 1 (Foundation):** 8-12 hours
- **Phase 2 (Core Systems):** 10-15 hours
- **Phase 3 (Analysis Layer):** 8-10 hours
- **Phase 4 (Formatting System):** 15-20 hours
- **Wrapper Backend (Phases 5-7):** TBD after fixing test issues
- **Phase 8 (Integration):** 6-8 hours

**Total Estimated:** 47-65 hours for root-level code

## Success Metrics

- **Overall Coverage:** 30% → 80%+
- **Critical Modules:** 0% → 90%+ (analyzers, core)
- **Services/APIs:** TBD → 85%+
- **Utilities:** 58-92% → 80%+
- **All Tests Passing:** Currently 97/104 passing → 100% passing

## Next Steps

1. Begin Phase 1 stub creation for foundation modules
2. Implement tests following dependency order
3. Address wrapper-backend test stability issues in parallel
4. Track progress with updated coverage reports after each phase
