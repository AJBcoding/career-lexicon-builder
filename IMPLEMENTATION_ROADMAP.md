# TEST IMPLEMENTATION ROADMAP

## Absolute File Paths for Code Review

### Critical Implementation Tasks

#### 1. Hierarchical Generator Tests - HIGHEST PRIORITY
**Files to modify:**
- `/home/user/career-lexicon-builder/tests/test_hierarchical_generator.py` (Lines 438-670)
- `/home/user/career-lexicon-builder/generators/hierarchical_generator.py` (Reference: Lines 183-760)

**Skipped tests to un-skip and implement:**
- `test_heading_formatting` (Line 439)
- `test_bullet_list_formatting` (Line 449)
- `test_code_block_formatting` (Line 459)
- `test_link_formatting` (Line 469)
- `test_citation_link_creation` (Line 483)
- `test_multiple_citations_per_entry` (Line 493)
- `test_citation_text_formatting` (Line 503)
- `test_section_ordering` (Line 517)
- `test_subsection_nesting` (Line 527)
- `test_section_metadata_inclusion` (Line 537)
- `test_aggregate_from_multiple_documents` (Line 551)
- `test_duplicate_content_detection` (Line 561)
- `test_content_merging` (Line 571)
- `test_write_markdown_file` (Line 585)
- `test_output_path_creation` (Line 595)
- `test_existing_file_overwrite` (Line 605)
- `test_malformed_data_handling` (Line 619)
- `test_missing_required_fields` (Line 629)
- `test_file_write_error_handling` (Line 639)
- `test_template_loading` (Line 653)
- `test_template_variable_substitution` (Line 663)

**Expected effort:** 8-10 hours
**Lines to cover:** +40-50

---

#### 2. Text Extraction Mocking - HIGH PRIORITY
**Files to modify:**
- `/home/user/career-lexicon-builder/tests/test_text_extraction.py` (Lines 159-958)
- `/home/user/career-lexicon-builder/utils/text_extraction.py` (Reference: Lines 133-659)

**Tests to convert from skip to mock:**

1. **Line 159-193:** `test_pdf_preview_extraction_missing_pdfplumber`
   - Currently tests import error handling but via monkeypatch
   - Convert to proper mock

2. **Line 584:** `test_pdf_with_metadata_extraction`
   - Add mock for pdfplumber.open
   - Mock PDF with metadata fields

3. **Line 684:** `test_docx_with_metadata_and_tables`
   - Add mock for docx.Document
   - Mock paragraphs and tables

4. **Line 788:** `test_pdf_preview_successful_extraction`
   - Mock pdfplumber for Pages PDF preview
   - Verify correct extraction method returned

5. **Lines 915, 926, 939, 949:** Add TODO test implementations
   - `test_document_type_detection_from_content`
   - `test_document_type_detection_edge_cases`
   - `test_extraction_error_recovery`
   - `test_partial_extraction_success`

**Expected effort:** 4-6 hours
**Lines to cover:** +30-40

---

#### 3. Document Processor Classification - MEDIUM PRIORITY
**File:** `/home/user/career-lexicon-builder/tests/test_document_processor.py`
**Source:** `/home/user/career-lexicon-builder/core/document_processor.py` (Lines 170-212)

**Add these tests to `TestClassifyByContent` class:**

```python
def test_resume_high_bullet_density_with_sufficient_text(self):
    """Test resume detection with high bullet point density (>0.02) and sufficient text length."""
    text = """
    Experience
    
    Senior Software Engineer | TechCorp | 2020-2024
    • Architected microservices platform serving 1M users
    • Led team of 8 engineers through major system redesign
    • Designed and implemented CI/CD pipeline reducing deployment time by 60%
    • Mentored 5 junior developers with code review process
    • Implemented real-time monitoring reducing incident response time by 40%
    
    Software Engineer | StartupCo | 2018-2020
    • Built REST API handling 10K requests per second
    • Optimized database queries improving performance by 50%
    • Implemented caching strategy reducing load time by 30%
    
    Education
    B.S. Computer Science | University of California | 2018
    
    Skills
    Python, JavaScript, AWS, Docker, Kubernetes, PostgreSQL
    """
    
    doc_type, conf, reasoning = classify_by_content(text)
    assert doc_type == DocumentType.RESUME
    assert conf > 0.7
    assert "bullet-heavy structure" in reasoning.lower()
    assert "date range" in reasoning.lower()

def test_job_description_single_phrase_signal(self):
    """Test job description with exactly one job posting phrase."""
    text = """
    Position Title: Software Engineer
    Location: San Francisco, CA
    
    We are seeking a talented engineer to join our team.
    
    Salary: $120,000 - $160,000
    Benefits: Health insurance, 401k, stock options
    
    Apply at: careers.example.com
    """
    
    doc_type, conf, reasoning = classify_by_content(text)
    assert doc_type == DocumentType.JOB_DESCRIPTION
    assert "1 job posting phrase" in reasoning.lower()
```

**File location:** `/home/user/career-lexicon-builder/tests/test_document_processor.py::TestClassifyByContent`
**Expected effort:** 1 hour
**Lines to cover:** +2

---

#### 4. State Manager Error Handling - MEDIUM PRIORITY
**File:** `/home/user/career-lexicon-builder/tests/test_core_state_manager.py`
**Source:** `/home/user/career-lexicon-builder/core/state_manager.py` (Lines 177-227)

**Add to `TestManifestLoadSave` class:**

```python
def test_save_manifest_creates_nested_directory_structure(self):
    """Test that save_manifest creates nested directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_path = os.path.join(tmpdir, "level1", "level2", "manifest.json")
        
        record = DocumentRecord(
            filepath="doc.pdf", file_hash="testhash123",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None, extraction_success=True
        )
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={"doc.pdf": record}, version="1.0.0"
        )
        
        save_manifest(manifest, nested_path)
        assert os.path.exists(nested_path)
        assert os.path.isdir(os.path.dirname(nested_path))

def test_needs_processing_handles_file_permission_error(self):
    """Test that needs_processing handles file permission errors gracefully."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"test content for permission test")
        tmp.flush()
        tmp_path = tmp.name
    
    try:
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={}, version="1.0.0"
        )
        
        # Make file unreadable
        os.chmod(tmp_path, 0o000)
        
        # Should return False (skip unreadable files)
        result = needs_processing(tmp_path, manifest)
        assert result is False
    finally:
        # Restore permissions for cleanup
        os.chmod(tmp_path, 0o644)
        os.unlink(tmp_path)
```

**File location:** `/home/user/career-lexicon-builder/tests/test_core_state_manager.py::TestManifestLoadSave`
**Expected effort:** 2-3 hours
**Lines to cover:** +3

---

#### 5. Date Parser Exception Handling - LOW PRIORITY
**File:** `/home/user/career-lexicon-builder/tests/test_date_parser.py`
**Source:** `/home/user/career-lexicon-builder/utils/date_parser.py` (Lines 85-94)

**Add to `TestExtractDateFromFilename` class:**

```python
def test_invalid_month_name_with_year(self):
    """Test that invalid month names return None gracefully."""
    # Pattern won't match but won't raise KeyError
    result = extract_date_from_filename("InvalidMonth2024-letter.pages")
    assert result is None
```

**File location:** `/home/user/career-lexicon-builder/tests/test_date_parser.py::TestExtractDateFromFilename`
**Expected effort:** 0.5 hours
**Lines to cover:** +1

---

## Implementation Priority Matrix

```
Priority | Module                   | Effort | Impact | Status
---------|-------------------------|--------|--------|--------
CRITICAL | hierarchical_generator  | 8-10h  | HIGH   | 21 tests skipped
CRITICAL | text_extraction         | 4-6h   | HIGH   | 6-8 tests skipped  
HIGH     | document_processor      | 1h     | MED    | 2 lines missing
HIGH     | state_manager           | 2-3h   | MED    | 3 lines missing
LOW      | date_parser             | 0.5h   | LOW    | 1 line missing
```

## Expected Coverage Progression

**Current:** 81% (1,052 statements, 196 missing)

After Phase 1 (hierarchical + text extraction):
- hierarchical_generator: 75% → 95% (adds 40-50 lines)
- text_extraction: 74% → 92% (adds 30-40 lines)
- **Overall: 81% → 85-86%**

After Phase 2 (remaining gaps):
- document_processor: 96% → 98% (adds 2 lines)
- state_manager: 96% → 98% (adds 3 lines)
- date_parser: 96% → 98% (adds 1 line)
- **Overall: 85-86% → 87-88%**

## Verification Commands

After implementing tests, verify coverage with:

```bash
# Full coverage report
python -m pytest tests/test_core_state_manager.py tests/test_core_orchestrator.py tests/test_document_processor.py tests/test_confidence_scorer.py tests/test_date_parser.py tests/test_text_extraction.py tests/test_hierarchical_generator.py tests/test_hierarchical_optional_fields.py --cov=core --cov=utils --cov=generators --cov-report=term-missing -v

# Check specific module
python -m pytest tests/test_hierarchical_generator.py --cov=generators.hierarchical_generator --cov-report=term-missing

# Run only new tests
python -m pytest tests/test_hierarchical_generator.py::TestMarkdownFormatting -v
```

## Code Review Checklist

- [ ] All 21 skipped hierarchical generator tests implemented
- [ ] All 6-8 text extraction tests converted to mocks
- [ ] Bullet density test added to document_processor
- [ ] Job phrase test added to document_processor
- [ ] Directory creation test added to state_manager
- [ ] Permission error test added to state_manager
- [ ] Invalid month name test added to date_parser
- [ ] All tests passing with no errors
- [ ] Coverage >= 87% overall
- [ ] All assertions are specific and clear
- [ ] No new tests skipped

