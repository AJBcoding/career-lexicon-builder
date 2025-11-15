# Testing Guide

**Career Lexicon Builder - Comprehensive Testing Documentation**

---

## 📊 Coverage Achievement

**Current Status: 81% Test Coverage** 🎯

| Metric | Value |
|--------|-------|
| **Overall Coverage** | 81% |
| **Passing Tests** | 194 tests |
| **Test Files** | 8+ files |
| **Lines Tested** | 856 of 1,052 statements |

### Coverage by Module

| Module | Coverage | Status |
|--------|----------|--------|
| **Core Systems** | 97% | ⭐ Exceptional |
| └─ confidence_scorer.py | 100% | ✅ Perfect |
| └─ orchestrator.py | 100% | ✅ Perfect |
| └─ state_manager.py | 96% | ✅ Excellent |
| └─ document_processor.py | 96% | ✅ Excellent |
| **Utilities** | 85% avg | ✅ Excellent |
| └─ date_parser.py | 96% | ✅ Excellent |
| └─ text_extraction.py | 74% | ✅ Good |
| **Generators** | 75% | ✅ Strong |
| └─ hierarchical_generator.py | 75% | ✅ Strong |

---

## 🚀 Quick Start

### Running Tests

```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run specific test file
PYTHONPATH=. pytest tests/test_core_orchestrator.py -v

# Run with coverage report
PYTHONPATH=. coverage run -m pytest tests/ -v
coverage report --include="core/*,utils/*,generators/*"

# Run tests matching a pattern
PYTHONPATH=. pytest tests/ -k "test_achievement" -v
```

### Coverage Commands

```bash
# Generate coverage for specific modules
PYTHONPATH=. coverage run -m pytest tests/test_core_state_manager.py
coverage report -m --include="core/state_manager.py"

# Generate HTML coverage report
coverage html --include="core/*,utils/*,generators/*"
# Open htmlcov/index.html in browser

# Check overall coverage
PYTHONPATH=. coverage run -m pytest tests/ --ignore=tests/wrapper-backend
coverage report --include="core/*,utils/*,generators/*"
```

---

## 📁 Test Organization

### Test File Structure

```
tests/
├── test_core_state_manager.py         # State management (22 tests, 96% coverage)
├── test_core_orchestrator.py          # Orchestration (13 tests, 100% coverage)
├── test_document_processor.py         # Classification (27 tests, 96% coverage)
├── test_confidence_scorer.py          # Confidence scoring (24 tests, 100% coverage)
├── test_date_parser.py                # Date extraction (24 tests, 96% coverage)
├── test_text_extraction.py            # Text extraction (47 tests, 74% coverage)
├── test_hierarchical_generator.py     # Lexicon generation (17 tests, 75% coverage)
└── test_hierarchical_optional_fields.py # Optional fields (20 tests)
```

### Test Organization Principles

Tests are organized by **dependency order**:

1. **Foundation Layer** (utils/): Date parsing, text extraction
2. **Core Layer** (core/): State management, orchestration, processing
3. **Analysis Layer** (analyzers/): LLM integration, prompt templates
4. **Generation Layer** (generators/): Lexicon generation, formatting

---

## 🎯 Testing Patterns

### 1. Arrange-Act-Assert Pattern

```python
def test_calculate_confidence_with_weights():
    # Arrange - Set up test data
    criteria = {'accuracy': 0.9, 'completeness': 0.8}
    weights = {'accuracy': 2.0, 'completeness': 1.0}

    # Act - Execute the function
    result = calculate_confidence(criteria, weights)

    # Assert - Verify results
    assert result == 0.8666666666666667
```

### 2. Tempfile Testing for File Operations

```python
def test_manifest_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = os.path.join(tmpdir, 'manifest.json')

        # Create and save manifest
        manifest = ProcessingManifest(...)
        save_manifest(manifest, manifest_path)

        # Load and verify
        loaded = load_manifest(manifest_path)
        assert loaded.version == manifest.version
```

### 3. Mocking External Dependencies

```python
@patch('pdfplumber.open')
def test_pdf_extraction_with_metadata(mock_open):
    # Mock PDF object
    mock_pdf = MagicMock()
    mock_pdf.pages = [MagicMock()]
    mock_pdf.pages[0].extract_text.return_value = "Test content"
    mock_pdf.metadata = {'Title': 'Test Doc'}

    # Set up context manager
    mock_open.return_value.__enter__.return_value = mock_pdf

    result = extract_text_from_document('test.pdf')
    assert result['success'] is True
```

### 4. Edge Case Testing

```python
def test_date_parser_leap_year():
    """Test date parsing with leap year edge case."""
    result = extract_date_from_filename("2024-02-29-resume.pdf")
    assert result == date(2024, 2, 29)

def test_date_parser_invalid_date():
    """Test graceful handling of invalid dates."""
    result = extract_date_from_filename("2024-02-30-invalid.pdf")
    assert result is None
```

### 5. Parametrized Testing

```python
@pytest.mark.parametrize("input_val,expected", [
    (0.9, "high"),
    (0.6, "medium"),
    (0.3, "low"),
])
def test_confidence_categories(input_val, expected):
    assert get_confidence_category(input_val) == expected
```

---

## 🔧 Common Testing Scenarios

### Testing File Hash Computation

```python
def test_file_hash_changes_on_modification():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("Original content")
        tmp_path = tmp.name

    try:
        hash1 = compute_file_hash(tmp_path)

        # Modify file
        with open(tmp_path, 'w') as f:
            f.write("Modified content")

        hash2 = compute_file_hash(tmp_path)
        assert hash1 != hash2
    finally:
        os.unlink(tmp_path)
```

### Testing Change Detection

```python
def test_needs_processing_modified_file():
    # Create file and record in manifest
    original_hash = compute_file_hash(file_path)
    record = DocumentRecord(filepath=file_path, file_hash=original_hash, ...)
    manifest = ProcessingManifest(documents={file_path: record}, ...)

    # Modify file
    modify_file(file_path)

    # Verify detected as needing processing
    assert needs_processing(file_path, manifest) is True
```

### Testing Optional Fields in Data Structures

```python
def test_achievement_with_all_optional_fields():
    """Test achievement generation with comprehensive optional fields."""
    data = {
        'categories': [{
            'name': 'Test',
            'achievements': [{
                'name': 'Achievement',
                'overview': {'summary': 'Test'},
                'variations': [...],
                'quantifiable_outcomes': [...],
                'usage_recommendations': {...},
                'related_achievements': [...],
                'keywords': [...]
            }]
        }]
    }

    result = generator.generate_achievements(data, output_path)

    with open(output_path, 'r') as f:
        content = f.read()
        # Verify all optional fields rendered
        assert 'Overview' in content
        assert 'Variations' in content
        # ... etc
```

---

## 📝 Best Practices

### ✅ DO

1. **Test One Thing Per Test**
   - Each test should verify a single behavior
   - Use descriptive test names that explain what is being tested

2. **Use Descriptive Assertions**
   ```python
   # Good
   assert result['success'] is True
   assert 'test content' in result['text']

   # Avoid
   assert result
   ```

3. **Clean Up Resources**
   ```python
   # Use try/finally for cleanup
   try:
       result = process_file(tmp_path)
       assert result is not None
   finally:
       os.unlink(tmp_path)
   ```

4. **Test Both Success and Failure Paths**
   ```python
   def test_extraction_success():
       result = extract_text_from_document(valid_file)
       assert result['success'] is True

   def test_extraction_failure():
       result = extract_text_from_document(invalid_file)
       assert result['success'] is False
       assert 'error' in result
   ```

5. **Document Coverage Gaps**
   ```python
   def test_feature():
       """
       Test feature X with scenario Y.

       Coverage gap: Lines 125-130 (error handling)
       Priority: HIGH - Critical path
       """
   ```

### ❌ DON'T

1. **Don't Test Implementation Details**
   - Test behavior, not internal structure
   - Avoid testing private methods directly

2. **Don't Use Sleep for Timing**
   - Use proper mocking instead of time.sleep()

3. **Don't Create Dependencies Between Tests**
   - Each test should be independent
   - Tests should pass in any order

4. **Don't Skip Cleanup**
   - Always clean up temporary files and resources

5. **Don't Commit Commented-Out Tests**
   - Use `@pytest.mark.skip("reason")` instead

---

## 🐛 Common Issues and Solutions

### Issue: ImportError for modules

**Problem:**
```
ModuleNotFoundError: No module named 'core'
```

**Solution:**
```bash
# Always run pytest with PYTHONPATH
PYTHONPATH=. pytest tests/test_core_orchestrator.py
```

### Issue: Tests hang on authorization tests

**Problem:**
Tests in wrapper-backend hang during execution

**Solution:**
```bash
# Exclude wrapper-backend tests
PYTHONPATH=. pytest tests/ --ignore=tests/wrapper-backend
```

### Issue: Coverage not showing all files

**Problem:**
Coverage report doesn't include all modules

**Solution:**
```bash
# Specify include pattern explicitly
coverage report --include="core/*,utils/*,generators/*"
```

### Issue: Temporary files not cleaned up

**Problem:**
/tmp directory filling up with test files

**Solution:**
```python
# Always use try/finally
try:
    result = test_function(tmp_path)
finally:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

# Or use context managers
with tempfile.TemporaryDirectory() as tmpdir:
    # Files automatically cleaned up
```

---

## 🎯 Adding New Tests

### Step 1: Identify Coverage Gaps

```bash
# Run coverage and identify missing lines
PYTHONPATH=. coverage run -m pytest tests/test_your_module.py
coverage report -m --include="your/module.py"
```

### Step 2: Create Test File

```python
"""
Tests for your_module.

Coverage: X% -> Y% (target)
"""

import pytest
import tempfile
import os
from your.module import function_to_test


class TestYourFeature:
    """Tests for your feature."""

    def test_basic_functionality(self):
        """Test basic happy path."""
        result = function_to_test(valid_input)
        assert result == expected_output

    def test_edge_case(self):
        """Test edge case handling."""
        result = function_to_test(edge_case_input)
        assert result is not None

    def test_error_handling(self):
        """Test error conditions."""
        result = function_to_test(invalid_input)
        assert result['success'] is False
```

### Step 3: Run and Verify

```bash
# Run new tests
PYTHONPATH=. pytest tests/test_your_module.py -v

# Check coverage improvement
PYTHONPATH=. coverage run -m pytest tests/test_your_module.py
coverage report -m --include="your/module.py"
```

### Step 4: Document

- Add docstrings explaining what is tested
- Note coverage gaps addressed
- Document any special setup required

---

## 📈 Coverage Goals

### Current Targets

- **Core Systems**: 90%+ (currently 97% ✅)
- **Utilities**: 80%+ (currently 85% ✅)
- **Generators**: 75%+ (currently 75% ✅)
- **Overall**: 80%+ (currently 81% ✅)

### Priority Areas

1. **Critical Business Logic** (90%+)
   - State management
   - Document orchestration
   - Classification logic

2. **Utility Functions** (85%+)
   - Text extraction
   - Date parsing
   - File operations

3. **Generation Logic** (75%+)
   - Lexicon generation
   - Template rendering

---

## 🔍 Test Quality Metrics

### Characteristics of Good Tests

- ✅ **Fast**: Runs in milliseconds
- ✅ **Independent**: No dependencies on other tests
- ✅ **Repeatable**: Same results every time
- ✅ **Self-validating**: Clear pass/fail
- ✅ **Timely**: Written alongside code

### Code Review Checklist

When reviewing tests:

- [ ] Tests are independent and can run in any order
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Resources are properly cleaned up
- [ ] Test names clearly describe what is being tested
- [ ] Assertions are specific and descriptive
- [ ] Coverage for both success and failure paths
- [ ] No commented-out test code

---

## 📚 Additional Resources

### Running Tests in CI/CD

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    PYTHONPATH=. pytest tests/ -v --ignore=tests/wrapper-backend

- name: Check Coverage
  run: |
    PYTHONPATH=. coverage run -m pytest tests/ --ignore=tests/wrapper-backend
    coverage report --include="core/*,utils/*,generators/*" --fail-under=80
```

### Useful pytest Flags

```bash
# Verbose output
pytest tests/ -v

# Show print statements
pytest tests/ -s

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Show slowest tests
pytest tests/ --durations=10

# Run tests in parallel (requires pytest-xdist)
pytest tests/ -n auto
```

---

## 🎉 Achievement Summary

**Testing Journey: 30% → 81% Coverage**

### What We Built

- **194 passing tests** across 8+ test files
- **97% coverage** on critical core systems
- **Comprehensive edge case testing** (leap years, encoding issues, malformed data)
- **Integration testing** (manifest persistence, workflow orchestration)
- **Professional mocking strategies** (external APIs, file I/O)

### Key Accomplishments

1. ✅ Created `core/confidence_scorer.py` from test requirements (100% coverage)
2. ✅ Achieved 97% coverage on core business logic
3. ✅ Built systematic test suite following dependency order
4. ✅ Implemented comprehensive optional field testing
5. ✅ Exceeded 80% coverage goal (reached 81%)

---

**Last Updated**: 2025-11-15
**Coverage Status**: 81% (194 passing tests)
**Status**: ✅ Production-Ready Test Suite
