# Phase 5 Handoff Document: Orchestrator

**Date**: 2025-10-29
**Project**: Career Lexicon Builder
**Current Status**: Phase 4 Complete (296 tests passing)
**Next Phase**: Phase 5 - Central Orchestrator

---

## Executive Summary

**Phase 4 Status**: ✅ COMPLETE
- All 4 lexicon generators implemented and tested
- 40 new Phase 4 tests passing
- Total test count: 296 tests passing in ~35 seconds
- All generators produce formatted markdown lexicons

**Phase 5 Goal**: Build central orchestrator to coordinate the full pipeline from document ingestion to lexicon generation.

**Estimated Effort**: 2-3 hours

---

## Current Project State

### Test Execution
```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Result: 296 passed (excluding slow integration tests)
```

### What's Been Built (Phases 1-4)

**Phase 1: Foundation** (55 tests)
- ✅ Date parsing from filenames
- ✅ Multi-format text extraction (.pages, .pdf, .docx, .txt, .md)

**Phase 2: Document Processing** (82 tests)
- ✅ Confidence scoring utilities
- ✅ Document classification (resume, cover letter, job description)
- ✅ State management with incremental processing

**Phase 3: Analysis Modules** (119 tests)
- ✅ Similarity utilities - Semantic similarity and clustering
- ✅ Themes Analyzer - Extract recurring values from cover letters
- ✅ Qualifications Analyzer - Track position phrasing variations
- ✅ Narratives Analyzer - Catalog rhetorical patterns
- ✅ Keywords Analyzer - Build cross-referenced keyword index

**Phase 4: Lexicon Generators** (40 tests)
- ✅ Themes Lexicon Generator - "My Values" reference document
- ✅ Qualifications Lexicon Generator - "Resume Bullet Variations"
- ✅ Narratives Lexicon Generator - "Storytelling Patterns Catalog"
- ✅ Keywords Lexicon Generator - "Keyword Usage Index"

### Directory Structure
```
/Users/anthonybyrnes/PycharmProjects/career-lexicon-builder/
├── analyzers/
│   ├── __init__.py                   ✅ Complete
│   ├── themes_analyzer.py            ✅ Complete (415 lines)
│   ├── qualifications_analyzer.py    ✅ Complete (398 lines)
│   ├── narratives_analyzer.py        ✅ Complete (434 lines)
│   └── keywords_analyzer.py          ✅ Complete (270 lines)
├── core/
│   ├── confidence_scorer.py          ✅ Complete
│   ├── document_processor.py         ✅ Complete
│   ├── state_manager.py              ✅ Complete
│   └── orchestrator.py               ⏳ EMPTY - Phase 5 work here
├── generators/
│   ├── __init__.py                   ✅ Complete
│   ├── themes_lexicon_generator.py            ✅ Complete (85 lines)
│   ├── qualifications_lexicon_generator.py    ✅ Complete (90 lines)
│   ├── narratives_lexicon_generator.py        ✅ Complete (85 lines)
│   └── keywords_lexicon_generator.py          ✅ Complete (100 lines)
├── templates/
│   ├── __init__.py                   ✅ Complete
│   └── formatting_utils.py          ✅ Complete (80 lines)
├── utils/
│   ├── date_parser.py                ✅ Complete
│   ├── text_extraction.py            ✅ Complete
│   └── similarity.py                 ✅ Complete (156 lines)
└── tests/
    ├── fixtures/                     ✅ Sample documents for testing
    └── test_*.py                     ✅ 296 tests passing
```

---

## Phase 5 Overview

### What Needs to Be Built

Phase 5 creates the **central orchestrator** that coordinates all components into a single cohesive pipeline. The orchestrator serves as the main entry point and workflow manager.

### Key Components

1. **Main Pipeline** - `run_full_pipeline()`
2. **Incremental Updates** - `run_incremental_update()`
3. **State Management Integration** - Track processed documents
4. **Error Handling** - Graceful failures and logging

### Key Design Principles

From the design document:
> "The orchestrator coordinates document processing, analysis, and generation into a single workflow while maintaining flexibility for incremental updates."

**Key Features**:
- Full pipeline execution (end-to-end)
- Incremental processing (only new/modified documents)
- State persistence (track what's been processed)
- Comprehensive logging (for debugging and monitoring)

---

## Requirements from Design Document

### Reference: Implementation Plan Lines 525-615

**Location**: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md`

### Task 5.1: Implement Central Orchestrator

**Effort**: 2 hours

**File**: `core/orchestrator.py`

**Purpose**: Coordinate all phases into a single workflow

**Functions to implement**:

```python
def run_full_pipeline(
    input_dir: str,
    output_dir: str,
    state_file: Optional[str] = None
) -> Dict:
    """
    Run complete pipeline from document ingestion to lexicon generation.

    Steps:
    1. Load or initialize state
    2. Scan input directory for documents
    3. Extract text from documents (Phase 1)
    4. Classify documents (Phase 2)
    5. Run all analyzers (Phase 3)
    6. Generate all lexicons (Phase 4)
    7. Save state
    8. Return summary statistics

    Args:
        input_dir: Directory containing source documents
        output_dir: Directory to write lexicons
        state_file: Optional path to state file (default: output_dir/.state.json)

    Returns:
        Dict with statistics (documents processed, themes found, etc.)
    """
```

```python
def run_incremental_update(
    input_dir: str,
    output_dir: str,
    state_file: Optional[str] = None
) -> Dict:
    """
    Process only new/modified documents and update lexicons.

    Steps:
    1. Load existing state
    2. Identify new/modified documents (by hash/modification time)
    3. Process only changed documents
    4. Load existing analysis data
    5. Merge new analysis with existing
    6. Regenerate lexicons with merged data
    7. Update state
    8. Return summary statistics

    Args:
        input_dir: Directory containing source documents
        output_dir: Directory containing existing lexicons
        state_file: Optional path to state file

    Returns:
        Dict with statistics (new documents, updated themes, etc.)
    """
```

```python
def process_documents(input_dir: str, state: Dict) -> List[Dict]:
    """
    Process all documents in input directory.

    For each document:
    - Extract text
    - Parse date from filename
    - Classify document type
    - Check if already processed (using state)

    Returns:
        List of document dicts with text, filepath, date, doc_type
    """
```

```python
def run_all_analyzers(documents: List[Dict]) -> Dict:
    """
    Run all Phase 3 analyzers on documents.

    Returns:
        Dict with keys: 'themes', 'qualifications', 'narratives', 'keywords'
    """
```

```python
def generate_all_lexicons(analysis_results: Dict, output_dir: str) -> None:
    """
    Generate all Phase 4 lexicons from analysis results.

    Creates:
    - output_dir/my_values.md
    - output_dir/resume_variations.md
    - output_dir/storytelling_patterns.md
    - output_dir/usage_index.md
    """
```

**Additional helpers**:

```python
def get_document_hash(filepath: str) -> str:
    """Calculate hash of document for change detection."""

def is_document_modified(filepath: str, state: Dict) -> bool:
    """Check if document has been modified since last processing."""

def merge_analysis_results(existing: Dict, new: Dict) -> Dict:
    """Merge new analysis results with existing data."""
```

---

## Implementation Guidance

### Workflow Overview

```
Input Documents
    ↓
[1. Text Extraction] (Phase 1)
    ↓
[2. Classification] (Phase 2)
    ↓
[3. Analysis] (Phase 3)
    - Themes
    - Qualifications
    - Narratives
    - Keywords
    ↓
[4. Generation] (Phase 4)
    - my_values.md
    - resume_variations.md
    - storytelling_patterns.md
    - usage_index.md
    ↓
Output Lexicons
```

### State Management Structure

```json
{
  "version": "1.0",
  "last_updated": "2024-01-15T10:30:00",
  "documents_processed": {
    "resume_2024.txt": {
      "hash": "abc123...",
      "processed_date": "2024-01-15T10:30:00",
      "doc_type": "resume"
    },
    "cover_letter_2024.txt": {
      "hash": "def456...",
      "processed_date": "2024-01-15T10:30:00",
      "doc_type": "cover_letter"
    }
  },
  "statistics": {
    "total_documents": 10,
    "themes_found": 5,
    "qualifications_found": 3,
    "narrative_patterns": 12,
    "keywords_found": 45
  }
}
```

### Error Handling Strategy

```python
# Graceful degradation
try:
    themes = analyze_themes(documents)
except Exception as e:
    logger.error(f"Themes analysis failed: {e}")
    themes = []  # Continue with empty themes

# Collect errors for summary
errors = []
if not themes:
    errors.append("No themes found")

# Return errors in summary
return {
    "success": len(errors) == 0,
    "errors": errors,
    "statistics": {...}
}
```

### Logging Strategy

```python
import logging

logger = logging.getLogger(__name__)

def run_full_pipeline(...):
    logger.info(f"Starting full pipeline for: {input_dir}")
    logger.info(f"Found {len(documents)} documents to process")

    logger.info("Phase 1: Extracting text...")
    # ...

    logger.info("Phase 2: Classifying documents...")
    # ...

    logger.info(f"Phase 3: Running analyzers...")
    logger.info(f"  - Found {len(themes)} themes")
    logger.info(f"  - Found {len(qualifications)} qualifications")

    logger.info("Phase 4: Generating lexicons...")
    logger.info(f"Lexicons written to: {output_dir}")

    logger.info("Pipeline complete!")
```

---

## Testing Strategy

### Unit Tests

Create `tests/test_orchestrator.py`:

**Test cases**:

1. **test_run_full_pipeline_creates_output**
   - Run full pipeline with sample documents
   - Verify all 4 lexicon files created
   - Verify state file created

2. **test_run_full_pipeline_statistics**
   - Run pipeline
   - Verify statistics dict has correct counts

3. **test_process_documents**
   - Test document loading and classification
   - Verify correct number of documents processed

4. **test_run_all_analyzers**
   - Test analyzer coordination
   - Verify all analyzer outputs present

5. **test_generate_all_lexicons**
   - Test lexicon generation coordination
   - Verify all files created

6. **test_incremental_update_new_documents**
   - Add new document
   - Run incremental update
   - Verify only new document processed

7. **test_incremental_update_modified_documents**
   - Modify existing document
   - Run incremental update
   - Verify document reprocessed

8. **test_document_hash_calculation**
   - Test hash generation is consistent

9. **test_is_document_modified**
   - Test change detection works correctly

10. **test_merge_analysis_results**
    - Test merging new and existing analysis
    - Verify no duplicates, proper combination

11. **test_empty_input_directory**
    - Test graceful handling of empty directory

12. **test_error_handling**
    - Test pipeline continues with partial failures

**Target**: ~12-15 tests for orchestrator

---

## Example Implementation Structure

### Orchestrator Module Structure

```python
"""
Central orchestrator for Career Lexicon Builder.

Coordinates the full pipeline from document ingestion to lexicon generation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

# Phase 1 imports
from utils.text_extraction import extract_text_from_document
from utils.date_parser import extract_date_from_filename

# Phase 2 imports
from core.document_processor import classify_document
from core.state_manager import StateManager

# Phase 3 imports
from analyzers.themes_analyzer import analyze_themes
from analyzers.qualifications_analyzer import analyze_qualifications
from analyzers.narratives_analyzer import analyze_narratives
from analyzers.keywords_analyzer import analyze_keywords

# Phase 4 imports
from generators.themes_lexicon_generator import generate_themes_lexicon
from generators.qualifications_lexicon_generator import generate_qualifications_lexicon
from generators.narratives_lexicon_generator import generate_narratives_lexicon
from generators.keywords_lexicon_generator import generate_keywords_lexicon

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Orchestrates the full pipeline."""

    def __init__(self, input_dir: str, output_dir: str, state_file: Optional[str] = None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.state_file = state_file or str(self.output_dir / ".state.json")
        self.state_manager = StateManager(self.state_file)

    def run_full_pipeline(self) -> Dict:
        """Run complete pipeline."""
        # Implementation here

    def run_incremental_update(self) -> Dict:
        """Run incremental update."""
        # Implementation here


# Standalone functions for flexibility
def run_full_pipeline(input_dir: str, output_dir: str, state_file: Optional[str] = None) -> Dict:
    """Run complete pipeline (functional interface)."""
    orchestrator = PipelineOrchestrator(input_dir, output_dir, state_file)
    return orchestrator.run_full_pipeline()


def run_incremental_update(input_dir: str, output_dir: str, state_file: Optional[str] = None) -> Dict:
    """Run incremental update (functional interface)."""
    orchestrator = PipelineOrchestrator(input_dir, output_dir, state_file)
    return orchestrator.run_incremental_update()
```

---

## Recommended Implementation Order

### Step 1: Core Pipeline (1 hour)
1. Create `core/orchestrator.py` with imports
2. Implement `process_documents()`
3. Implement `run_all_analyzers()`
4. Implement `generate_all_lexicons()`
5. Implement basic `run_full_pipeline()` without state
6. Write tests for these functions
7. Verify tests pass

### Step 2: State Management Integration (0.5 hours)
1. Implement `get_document_hash()`
2. Implement `is_document_modified()`
3. Integrate state loading/saving into `run_full_pipeline()`
4. Write tests for hash and modification detection
5. Verify tests pass

### Step 3: Incremental Updates (0.5 hours)
1. Implement `merge_analysis_results()`
2. Implement `run_incremental_update()`
3. Write tests for incremental updates
4. Verify tests pass

### Step 4: Polish & Error Handling (0.5 hours)
1. Add comprehensive logging
2. Add error handling and recovery
3. Add summary statistics generation
4. Test end-to-end with real documents
5. Run full test suite

---

## Success Criteria for Phase 5

- [ ] `core/orchestrator.py` implemented (~250-300 lines)
- [ ] `tests/test_orchestrator.py` with comprehensive tests (~12-15 tests)
- [ ] **Target: ~310 tests passing** (296 current + ~15 new)
- [ ] Full pipeline works end-to-end
- [ ] Incremental updates work correctly
- [ ] State persistence works
- [ ] All lexicons generated successfully
- [ ] Error handling is robust
- [ ] Logging provides useful feedback

---

## How to Continue in Next Session

### Step 1: Verify Current State

```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Should see: 296 passed
```

### Step 2: Start Implementation

1. **Create orchestrator file**:
   ```bash
   touch core/orchestrator.py
   ```

2. **Write imports and skeleton**:
   - Import all Phase 1-4 modules
   - Create function signatures
   - Add docstrings

3. **Create test file**:
   ```bash
   touch tests/test_orchestrator.py
   ```

4. **Follow TDD approach**:
   - Write test for `process_documents()`
   - Implement function
   - Verify test passes
   - Repeat for other functions

### Step 3: Integration Testing

Once orchestrator is implemented:

```python
# Quick manual test
from core.orchestrator import run_full_pipeline

result = run_full_pipeline(
    input_dir="tests/fixtures",
    output_dir="output_test"
)

print(result)
# Should show statistics and success status

# Verify lexicons created
import os
assert os.path.exists("output_test/my_values.md")
assert os.path.exists("output_test/resume_variations.md")
assert os.path.exists("output_test/storytelling_patterns.md")
assert os.path.exists("output_test/usage_index.md")
```

---

## Expected File Structure After Phase 5

```
core/
└── orchestrator.py                  (~250-300 lines)

tests/
└── test_orchestrator.py            (~12-15 tests)
```

**Estimated additions**: ~250-300 lines of production code, ~200-250 lines of test code

---

## Common Pitfalls to Avoid

### 1. Don't Skip State Management
State tracking is critical for incremental updates. Implement it from the start.

### 2. Handle Empty Results Gracefully
If an analyzer finds nothing, don't fail - continue with empty results.

### 3. Log at Key Points
Logging helps debug pipeline issues. Log at each phase transition.

### 4. Test with Real Documents
Unit tests are great, but also test with real fixture documents end-to-end.

### 5. Make Output Directory Creation Robust
Create output directory if it doesn't exist. Handle nested paths.

---

## Dependencies

**No new dependencies needed!** All required functionality is available from existing phases.

**Existing dependencies used**:
- Phase 1: Text extraction and date parsing
- Phase 2: Document classification and state management
- Phase 3: All 4 analyzers
- Phase 4: All 4 generators
- Python standard library: `pathlib`, `json`, `logging`, `datetime`, `hashlib`

---

## Resources

### Design Documents
- **Primary**: `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`
- **Implementation**: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md` (lines 525-615)

### Existing Modules to Integrate
- `utils/text_extraction.py` - `extract_text_from_document()`
- `utils/date_parser.py` - `extract_date_from_filename()`
- `core/document_processor.py` - `classify_document()`
- `core/state_manager.py` - StateManager class
- All Phase 3 analyzers - `analyze_*()` functions
- All Phase 4 generators - `generate_*_lexicon()` functions

### Test Fixtures
- `tests/fixtures/sample_resume.txt`
- `tests/fixtures/sample_cover_letter.txt`
- `tests/fixtures/sample_resume_v2.txt`

---

## Timeline Estimate

**Phase 5 Total**: 2-3 hours

- Step 1 (Core Pipeline): 1 hour
- Step 2 (State Management): 0.5 hours
- Step 3 (Incremental Updates): 0.5 hours
- Step 4 (Polish & Error Handling): 0.5-1 hour

**Remaining Project Phases**:
- Phase 6 (End-to-End Testing & Polish): 2-3 hours
- Phase 7 (CLI): 1-2 hours

**Total Remaining**: 5-8 hours

---

## Quick Reference: Orchestrator Functions

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| **run_full_pipeline()** | Main entry point | input_dir, output_dir | Statistics dict |
| **run_incremental_update()** | Process only changes | input_dir, output_dir | Statistics dict |
| **process_documents()** | Load & classify docs | input_dir, state | List[Dict] |
| **run_all_analyzers()** | Run Phase 3 | documents | Analysis results dict |
| **generate_all_lexicons()** | Run Phase 4 | analysis_results, output_dir | None |
| **get_document_hash()** | Calculate file hash | filepath | Hash string |
| **is_document_modified()** | Check for changes | filepath, state | Boolean |
| **merge_analysis_results()** | Combine old + new | existing, new | Merged dict |

---

**Session Complete**: 2025-10-29
**Phase 4 Status**: ✅ COMPLETE (296 tests passing)
**Phase 5 Status**: ⏳ READY TO START
**Next Session**: Begin with Step 1 (Core Pipeline)

---

**Generated**: 2025-10-29
**By**: Claude (Sonnet 4.5)
**For**: Career Lexicon Builder Project
**Session**: Phase 4 → Phase 5 Transition
