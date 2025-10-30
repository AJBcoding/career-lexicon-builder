# Phase 2 Handoff Document

**Date**: 2025-10-29
**Project**: Career Lexicon Builder
**Current Status**: Phase 1 Complete (100% tests passing)
**Next Phase**: Phase 2 - Document Classification & State Management

---

## Executive Summary

Phase 1 (Foundation) is complete with 55/55 tests passing. The project has been restarted from scratch following the original design document after discovering the previous implementation (phases 1-4) didn't match the design intent. We now have a solid foundation for multi-format document extraction.

**Key Achievement**: Unified text extraction from .pages, .pdf, .docx, .txt, and .md files.

---

## Current Project State

### Directory Structure
```
/Users/anthonybyrnes/PycharmProjects/career-lexicon-builder/
├── analyzers/              # Empty - for Phase 3
├── core/                   # Empty - for Phase 2
├── generators/             # Empty - for Phase 4
├── templates/              # Empty - for Phase 4
├── utils/
│   ├── __init__.py
│   ├── date_parser.py         ✅ Complete (148 lines)
│   └── text_extraction.py     ✅ Complete (593 lines)
├── tests/
│   ├── test_date_parser.py        ✅ 25 tests passing
│   └── test_text_extraction.py    ✅ 30 tests passing
├── archive/
│   └── 2025-10-29-skill-based-implementation/  # Previous wrong implementation
└── DesignDocuments/
    ├── 2025-01-27-career-lexicon-builder-design.md
    └── 2025-01-27-career-lexicon-builder-implementation.md
```

### What's Been Built (Phase 1)

#### 1. Date Parser (`utils/date_parser.py`)
**Purpose**: Extract dates from document filenames

**Functions**:
- `extract_date_from_filename(filename: str) -> Optional[date]`
  - Supports: YYYY-MM-DD, YYYY-MM, MonthYYYY formats
  - Case-insensitive month names
  - Returns `date` object or None
- `format_date_citation(doc_date: Optional[date]) -> str`
  - Formats for lexicon citations
- `compare_dates(date1, date2) -> int`
  - For chronological sorting (most recent first)

**Test Coverage**: 25/25 tests passing

#### 2. Text Extraction (`utils/text_extraction.py`)
**Purpose**: Extract text from multiple document formats

**Supported Formats**:
- `.pages` - Apple Pages (XML extraction + PDF preview fallback)
- `.pdf` - PDF documents (requires pdfplumber)
- `.docx` - Microsoft Word (requires python-docx)
- `.txt` - Plain text
- `.md` - Markdown

**Main Function**:
```python
extract_text_from_document(filepath: str) -> Dict
```

**Returns**:
```python
{
    'text': str,
    'success': bool,
    'extraction_method': str,  # 'xml', 'pdf', 'docx', 'text'
    'formatting': {
        'bold_spans': [],
        'bullets': []
    },
    'metadata': {
        'filename': str,
        'file_type': str,
        'file_hash': str,
        'extraction_date': str,
        # Format-specific metadata...
    },
    'error': Optional[str]
}
```

**Helper Function**:
```python
extract_metadata(filepath: str, text: str) -> Dict
```
- Extracts: date, target_position, target_organization
- Uses filename patterns and text content analysis

**Test Coverage**: 30/30 tests passing

### Dependencies (requirements.txt)
```
pytest>=8.4.2
pdfplumber>=0.11.0
python-docx>=1.1.0
```

### Test Execution
```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Result: 55 passed in 0.17s
```

---

## What Was Archived

The `archive/2025-10-29-skill-based-implementation/` directory contains the previous implementation that:
- Built a **skill extraction and gap analysis system**
- Had 151 tests passing but **didn't match the design document**
- Focused on: WHAT skills you have (quantitative analysis)
- Design document wants: HOW you've phrased content (qualitative reference library)

**See**: `archive/2025-10-29-skill-based-implementation/ARCHIVE-README.md` for details.

---

## Design Intent vs. Implementation

### Design Document Vision
**File**: `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`

**Goal**: Build reference lexicons from 30+ existing career documents

**Four Lexicons**:
1. **Themes Lexicon** - Values, philosophies with **chronological quotes**
2. **Qualifications Lexicon** - Position variations and **bullet point phrasings** across resume versions
3. **Narratives Lexicon** - **Storytelling structures, metaphors, rhetorical devices** from cover letters
4. **Keywords Index** - Cross-referenced terms with **specific usage examples**

**Output**: Markdown documents with quoted examples for reference when writing new materials

### Implementation Plan
**File**: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md`

Breaks work into 7 phases (estimated 20-25 hours total).

---

## Phase 2: Document Classification & State Management

### Overview
**Location**: Implementation plan lines 115-235
**Estimated Effort**: 4-5 hours
**Goal**: Classify documents (resume vs. cover letter vs. job description) and manage processing state

### What Needs to Be Built

#### Task 2.1: Document Classifier (`core/document_processor.py`)
**Dependencies**: Phase 1 complete ✅

**Functions to implement**:

1. `classify_document(text: str) -> Tuple[DocumentType, float, str]`
   - Uses heuristic patterns to classify document type
   - Returns: (type, confidence, reasoning)
   - Document types: RESUME, COVER_LETTER, JOB_DESCRIPTION, UNKNOWN

2. Pattern matching:
   - Resume indicators: "education", "experience", "skills", date ranges
   - Cover letter indicators: "Dear", "Sincerely", "I am writing to"
   - Job description indicators: "responsibilities", "requirements", "we are seeking"

**Deliverable**: Document classifier with confidence scoring

**Test requirements**:
- Test clear resume identification
- Test clear cover letter identification
- Test ambiguous documents
- Test confidence thresholds
- Test edge cases (very short, empty)

#### Task 2.2: State Manager (`core/state_manager.py`)
**Dependencies**: Phase 1 complete ✅

**Purpose**: Track processed documents, avoid re-processing, enable incremental updates

**Data structures**:
```python
@dataclass
class DocumentRecord:
    filepath: str
    file_hash: str
    document_type: DocumentType
    date_processed: datetime
    date_from_filename: Optional[date]
    extraction_success: bool

@dataclass
class ProcessingManifest:
    last_updated: datetime
    documents: Dict[str, DocumentRecord]  # filepath -> record
    version: str
```

**Functions to implement**:

1. `load_manifest(manifest_path: str) -> ProcessingManifest`
   - Loads existing manifest JSON or creates new one

2. `save_manifest(manifest: ProcessingManifest, manifest_path: str)`
   - Saves manifest as JSON

3. `needs_processing(filepath: str, manifest: ProcessingManifest) -> bool`
   - Checks if file is new or changed (hash comparison)

4. `add_document_record(manifest: ProcessingManifest, record: DocumentRecord)`
   - Adds/updates document record in manifest

5. `get_documents_by_type(manifest: ProcessingManifest, doc_type: DocumentType) -> List[DocumentRecord]`
   - Filters documents by type

**Storage**: `.lexicon-cache/manifest.json`

**Deliverable**: State management system with JSON persistence

**Test requirements**:
- Test manifest creation
- Test manifest save/load round-trip
- Test needs_processing logic (new, changed, unchanged files)
- Test document record management
- Test filtering by document type
- Test hash change detection

#### Task 2.3: Confidence Scorer (`core/confidence_scorer.py`)
**Dependencies**: None (can be done in parallel)

**Purpose**: Calculate confidence scores for all analysis outputs

**Function to implement**:
```python
def calculate_confidence(
    criteria: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float
```

**Logic**:
- Takes multiple scoring criteria (0.0-1.0 each)
- Applies optional weights
- Returns weighted average confidence score
- Clamps result to 0.0-1.0 range

**Example usage**:
```python
# Document classification
confidence = calculate_confidence({
    'pattern_matches': 0.8,  # 4 out of 5 patterns matched
    'text_length': 1.0,      # Sufficient text length
    'clarity': 0.9           # Clear indicators present
})

# Theme identification
confidence = calculate_confidence({
    'frequency': 0.7,        # Appears in 7/10 documents
    'similarity': 0.85,      # High semantic similarity
    'context_match': 0.6     # Moderate context match
}, weights={
    'frequency': 2.0,        # Frequency matters most
    'similarity': 1.5,
    'context_match': 1.0
})
```

**Deliverable**: Confidence scoring utility

**Test requirements**:
- Test equal weights
- Test custom weights
- Test edge cases (all zeros, all ones)
- Test weight normalization
- Test clamping to [0.0, 1.0]

---

## How to Start Phase 2

### 1. Verify Current State
```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v

# Should see: 55 passed in 0.17s
```

### 2. Review Design Documents
Read these files to understand the full vision:
- `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`
- `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md` (lines 115-235 for Phase 2)

### 3. Create Phase 2 Modules

**Order of implementation** (suggested):

1. **Start with `core/confidence_scorer.py`** (independent, simple)
   - Write tests first (TDD approach)
   - ~30 minutes

2. **Then `core/document_processor.py`** (depends on confidence scorer)
   - Write tests for document classification
   - Implement pattern-based classification
   - ~2 hours

3. **Finally `core/state_manager.py`** (uses document processor)
   - Write tests for manifest management
   - Implement JSON persistence
   - Implement incremental processing logic
   - ~2 hours

### 4. Integration Test
Create `tests/test_phase2_integration.py`:
- Extract text from sample documents
- Classify each document
- Build processing manifest
- Verify incremental updates work

### 5. Success Criteria
- All tests passing (Phase 1 + Phase 2)
- Document classifier correctly identifies resumes vs. cover letters
- Manifest tracks processed documents
- Incremental processing skips unchanged files
- Confidence scores calculated correctly

---

## Key Architecture Decisions

### 1. Multi-Format Support
**Decision**: Support .pages, .pdf, .docx, .txt, .md
**Rationale**: Users have documents in various formats; manual conversion is friction
**Impact**: Optional dependencies (pdfplumber, python-docx) must be handled gracefully

### 2. Unified Extraction API
**Decision**: Single function `extract_text_from_document()` for all formats
**Rationale**: Simplifies downstream code; format routing handled internally
**Impact**: All format-specific logic is private (`_extract_pages`, `_extract_pdf`, etc.)

### 3. Hash-Based Change Detection
**Decision**: Use SHA-256 file hashes in manifest
**Rationale**: Reliable detection of file changes; enables incremental processing
**Impact**: Must recalculate hash on every check (acceptable for ~30 documents)

### 4. Pattern-Based Classification
**Decision**: Use regex patterns rather than ML for document classification
**Rationale**: Simple, fast, interpretable, sufficient for cover letters vs. resumes
**Impact**: May need manual rules for edge cases; confidence scoring helps flag uncertain cases

### 5. JSON Manifest Storage
**Decision**: Store processing state as JSON in `.lexicon-cache/manifest.json`
**Rationale**: Human-readable, easy to debug, no database dependency
**Impact**: Must handle concurrent access carefully (not required for single-user tool)

---

## Common Pitfalls to Avoid

### 1. Don't Rebuild the Archived Implementation
The archived implementation focused on **skill extraction and gap analysis**. That's not what the design document calls for. The design wants:
- Quoted examples from your past writing
- How you've phrased things in different contexts
- Reference materials for drafting new documents

### 2. Don't Skip Test Coverage
Every module should have comprehensive tests before moving forward. TDD approach works well.

### 3. Don't Mix Concerns
- `document_processor.py`: Classification only
- `state_manager.py`: Manifest persistence only
- Don't put extraction logic in Phase 2 modules (already done in Phase 1)

### 4. Match the Implementation Plan Exactly
The implementation plan is well-thought-out. Follow the function signatures and data structures it specifies. This will make integration with Phase 3+ smoother.

---

## Questions to Resolve (if any)

1. **Confidence threshold for classification**: What confidence score should flag documents for manual review? (Suggest: < 0.6)

2. **Job description handling**: Design mentions analyzing job postings but doesn't specify where they're stored. Should they be in the same input directory or separate?

3. **Manifest location**: `.lexicon-cache/` in project root? Or user-configurable?

4. **Date extraction fallback**: If no date in filename, should we try to extract from document metadata (PDF creation date, DOCX properties)?

---

## Resources

### Design Documents
- Primary: `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`
- Implementation: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md`

### Current Code
- Date parser: `utils/date_parser.py`
- Text extraction: `utils/text_extraction.py`
- All tests: `tests/test_*.py`

### Archived Implementation
- Location: `archive/2025-10-29-skill-based-implementation/`
- Don't use for reference (wrong approach)
- Kept for historical record only

### Dependencies
```bash
# Already in requirements.txt
pytest>=8.4.2
pdfplumber>=0.11.0
python-docx>=1.1.0
```

---

## Estimated Timeline

**Phase 2 Total**: 4-5 hours

- Confidence scorer: 30 minutes
- Document classifier: 2 hours
- State manager: 2 hours
- Integration testing: 30 minutes

**Remaining Phases**:
- Phase 3 (Analysis Modules): 8-10 hours
- Phase 4 (Lexicon Generators): 3-4 hours
- Phase 5 (Orchestrator): 2-3 hours
- Phase 6 (Testing): 2-3 hours
- Phase 7 (CLI): 1-2 hours

**Total Project**: 20-27 hours

---

## Next Steps for New Session

1. **Load context**: Read this handoff document
2. **Verify state**: Run `pytest tests/ -v` (should see 55 passing)
3. **Review design**: Skim the implementation plan (Phase 2 section)
4. **Start coding**: Begin with `core/confidence_scorer.py` (simplest, independent)
5. **Use TDD**: Write tests first, then implementation
6. **Track progress**: Use TodoWrite tool to track Phase 2 tasks

---

## Session Handoff Checklist

- ✅ Phase 1 complete (55/55 tests passing)
- ✅ Multi-format extraction working (.pages, .pdf, .docx, .txt, .md)
- ✅ Date parser functional
- ✅ Metadata extraction functional
- ✅ Previous wrong implementation archived
- ✅ Project structure matches design document
- ✅ All code documented and tested
- ✅ Ready for Phase 2

**Status**: Ready to begin Phase 2 - Document Classification & State Management

---

**Generated**: 2025-10-29
**By**: Claude (Sonnet 4.5)
**For**: Career Lexicon Builder Project
