# Comprehensive Testing Implementation Plan

**Date:** 2025-11-14
**Goal:** Achieve 80%+ test coverage across entire codebase while validating actual functionality
**Focus:** Areas where TDD wasn't initially followed

## Overview

### Objectives

1. **Comprehensive Coverage:** Achieve 80%+ test coverage project-wide
2. **Functional Validation:** Ensure code actually works, not just coverage metrics
3. **Gap-Focused:** Prioritize areas where tests were written after code
4. **Systematic Approach:** Use data-driven coverage analysis to guide testing

### Two-Phase Coverage Analysis

The project has two distinct testing contexts:

1. **Root-level tests** (`tests/`) - Core lexicon generation, CV formatting, Phase 2/3/4 integration
2. **Wrapper-backend tests** (`wrapper-backend/tests/`) - FastAPI application, services, APIs

We'll generate separate coverage reports for each, then create a unified implementation plan.

## Three-Stage Implementation

### Stage 1: Discovery & Planning

**Objective:** Generate coverage reports and create comprehensive inventory of missing tests.

#### Step 1.1: Root-Level Coverage Analysis

```bash
# Install coverage tools if needed
pip install pytest pytest-cov

# Run coverage on root-level tests
pytest tests/ \
  --cov=analyzers \
  --cov=core \
  --cov=cv_formatting \
  --cov=generators \
  --cov=utils \
  --cov-report=html:coverage-root \
  --cov-report=term-missing
```

**Outputs:**
- `coverage-root/index.html` - Interactive HTML coverage report
- Terminal output showing missing line numbers
- Baseline coverage metrics

#### Step 1.2: Wrapper-Backend Coverage Analysis

```bash
# Navigate to wrapper-backend
cd wrapper-backend

# Run coverage on backend tests
pytest tests/ \
  --cov=api \
  --cov=services \
  --cov=models \
  --cov=utils \
  --cov-report=html:coverage-backend \
  --cov-report=term-missing
```

**Outputs:**
- `coverage-backend/index.html` - Interactive HTML coverage report
- Terminal output with missing coverage
- Baseline backend coverage metrics

#### Step 1.3: Analysis & Inventory Creation

For each uncovered function/class, document:
- Module path
- Function/class name
- Current coverage %
- Lines not covered
- Complexity estimate (simple/medium/complex)
- Dependencies (what it relies on)
- Priority (critical/important/nice-to-have)

**Output:** `docs/plans/2025-11-14-testing-inventory.md` with complete gap analysis

### Stage 2: Stub Creation

**Objective:** Create test stubs for all identified gaps, providing complete visibility into scope.

#### Step 2.1: Determine Test File Structure

For each source file without tests, create corresponding test file:

```
Source: analyzers/llm_analyzer.py
→ Test: tests/test_llm_analyzer.py

Source: cv_formatting/metadata_inference.py
→ Test: tests/test_metadata_inference.py

Source: wrapper-backend/services/chat_service.py
→ Test: wrapper-backend/tests/test_chat_service.py
```

#### Step 2.2: Generate Test Stubs

For each uncovered function, create stub with:

```python
@pytest.mark.skip("TODO: Implement - test basic functionality")
def test_function_name_basic():
    """
    Test that function_name handles normal inputs correctly.

    Coverage gap: Lines 45-67 in module.py
    Priority: High - core business logic
    """
    pass

@pytest.mark.skip("TODO: Implement - test error handling")
def test_function_name_error_cases():
    """
    Test that function_name handles errors gracefully.

    Coverage gap: Lines 68-75 in module.py
    Priority: Medium - error handling
    """
    pass
```

#### Step 2.3: Organize Stubs by Dependency Groups

- **Group 1 (Foundation):** `utils/`, `generators/`
- **Group 2 (Core):** `core/orchestrator.py`, `core/state_manager.py`, `core/document_processor.py`
- **Group 3 (Analysis):** `analyzers/llm_analyzer.py`, `analyzers/llm_prompt_templates.py`
- **Group 4 (Formatting):** `cv_formatting/` modules
- **Group 5 (Backend Foundation):** `wrapper-backend/models/`, `wrapper-backend/utils/`
- **Group 6 (Backend Services):** `wrapper-backend/services/`
- **Group 7 (Backend APIs):** `wrapper-backend/api/`
- **Group 8 (Integration):** Cross-module integration tests

### Stage 3: Systematic Implementation

**Objective:** Fill in test stubs following dependency order, ensuring foundational code works before testing dependent code.

#### Implementation Order

**Phase 1: Foundation (Group 1)**
- `utils/text_extraction.py` - Text processing utilities
- `utils/date_parser.py` - Date parsing logic
- `generators/hierarchical_generator.py` - Markdown generation

**Phase 2: Core Systems (Group 2)**
- `core/state_manager.py` - State persistence
- `core/document_processor.py` - Document processing pipeline
- `core/orchestrator.py` - Orchestration logic

**Phase 3: Analysis Layer (Group 3)**
- `analyzers/llm_prompt_templates.py` - Prompt template generation
- `analyzers/llm_analyzer.py` - LLM API integration (with mocking)

**Phase 4: Formatting System (Group 4)**
- `cv_formatting/style_parser.py` - Style parsing
- `cv_formatting/style_mapping.py` - Style mapping logic
- `cv_formatting/metadata_inference.py` - Metadata extraction
- `cv_formatting/learning_system.py` - Learning/correction system
- `cv_formatting/style_applicator.py` - Style application
- `cv_formatting/template_builder.py` - Template generation
- `cv_formatting/pdf_converter.py` - PDF conversion
- `cv_formatting/image_generator.py` - Image generation
- Remaining cv_formatting modules

**Phase 5: Backend Foundation (Group 5)**
- `wrapper-backend/models/` - Database models
- `wrapper-backend/utils/auth.py` - Authentication utilities
- `wrapper-backend/utils/logging_config.py` - Logging configuration

**Phase 6: Backend Services (Group 6)**
- `wrapper-backend/services/anthropic_service.py` - Claude API integration
- `wrapper-backend/services/project_service.py` - Project management
- `wrapper-backend/services/skill_service.py` - Skill execution
- `wrapper-backend/services/chat_service.py` - Chat logic
- `wrapper-backend/services/suggestions_service.py` - Suggestions
- `wrapper-backend/services/preview_service.py` - Document preview
- `wrapper-backend/services/watcher_service.py` - File watching
- `wrapper-backend/services/project_watcher_manager.py` - Watcher management

**Phase 7: Backend APIs (Group 7)**
- `wrapper-backend/api/auth.py` - Auth endpoints
- `wrapper-backend/api/projects.py` - Project endpoints
- `wrapper-backend/api/files.py` - File endpoints
- `wrapper-backend/api/skills.py` - Skill endpoints
- `wrapper-backend/api/chat.py` - Chat endpoints
- `wrapper-backend/api/preview.py` - Preview endpoints
- `wrapper-backend/api/suggestions.py` - Suggestions endpoints
- `wrapper-backend/api/websocket.py` - WebSocket endpoints

**Phase 8: Integration Testing (Group 8)**
- End-to-end workflows
- Cross-module interactions
- API integration tests

#### Per-Module Implementation Process

For each module:
1. Review source code to understand functionality
2. Identify test fixtures/mocks needed
3. Implement stubbed tests one by one
4. Run tests to verify they pass
5. Run coverage to confirm lines are covered
6. Refactor tests for clarity/maintainability
7. Mark module as complete

#### Progress Tracking

After completing each phase:
- Re-run coverage report
- Update inventory document with completion status
- Document any issues/blockers discovered
- Commit tests with clear message: `test: add comprehensive tests for <module>`

## Testing Patterns & Best Practices

### Unit Test Structure

```python
def test_function_name_should_behavior():
    """Test that function does X when given Y."""
    # Arrange - set up test data
    input_data = ...
    expected_output = ...

    # Act - call the function
    result = function_name(input_data)

    # Assert - verify behavior
    assert result == expected_output
```

### Mocking External Dependencies

- Mock LLM API calls (anthropic, Claude API)
- Mock file I/O where appropriate
- Mock database calls in service tests
- Use `pytest.fixture` for reusable test data

### Test Categories

- **Happy path** - Normal, expected usage
- **Edge cases** - Boundary conditions, empty inputs, None values
- **Error handling** - Invalid inputs, API failures, exceptions
- **Integration** - Multiple modules working together

### Coverage Goals

- **Critical business logic:** 90%+ coverage
- **Services/APIs:** 85%+ coverage
- **Utilities:** 80%+ coverage
- **Overall project:** 80%+ coverage

## Deliverables

### 1. Testing Inventory
**File:** `docs/plans/2025-11-14-testing-inventory.md`

- Complete gap analysis from coverage reports
- Organized by module with priority levels
- Dependency mapping

### 2. Implementation Plan
**File:** `docs/plans/2025-11-14-testing-implementation-plan.md` (this document)

- Phase-by-phase implementation guide
- Progress tracking template

### 3. Test Files

- All stubbed test files with TODO markers
- Completed test implementations
- Updated existing tests to fill gaps

### 4. Coverage Reports

- Initial baseline reports (root + backend)
- Post-implementation reports showing improvement
- Final coverage metrics

### 5. Git Commits

- Organized by phase: `test: add Phase 1 foundation tests`
- Clear commit messages referencing coverage improvements
- Each phase pushed to branch for review

## Success Criteria

1. **Coverage Metrics:**
   - Root-level code: 80%+ coverage
   - Wrapper-backend: 80%+ coverage
   - Critical business logic: 90%+ coverage

2. **Functional Validation:**
   - All tests pass
   - Tests validate actual behavior, not just execution
   - Edge cases and error handling covered

3. **Completeness:**
   - Every module has corresponding test file
   - All public functions/methods have tests
   - Integration points tested

4. **Maintainability:**
   - Tests are clear and well-documented
   - Fixtures/mocks are reusable
   - Test organization mirrors source structure

## Next Steps

1. Run Stage 1 coverage analysis
2. Create testing inventory document
3. Generate test stubs (Stage 2)
4. Begin Phase 1 implementation
5. Track progress and iterate through all phases
