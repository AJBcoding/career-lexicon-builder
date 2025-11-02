# Append Document References to Lexicons - Design Document

**Date**: 2025-11-02
**Status**: Approved for Implementation

## Overview

Add a "Files Referenced" section to each lexicon file listing all source documents from `my_documents/converted/`, organized by document type and sorted in reverse chronological order.

## Goals

1. **One-Time Update**: Append references to existing lexicon files
2. **Future Integration**: Design to support LLM-based pipeline integration (Approach 3)
3. **File Renaming**: Standardize filenames to include dates (`YYYY-MM-DD - name.pdf`)
4. **User Confirmation**: Interactive review only for dates extracted from PDF content

## Implementation Approach

### Approach 1: Interactive Python Script (Current Implementation)

**Script**: `append_document_references.py`

#### Phase 1: Document Discovery & Date Extraction

Scan `my_documents/converted/` for all files:

1. **Try filename date parsing** using existing `utils/date_parser.py`
   - If successful: use date, skip to classification
   - If fails: proceed to content extraction

2. **Extract date from PDF content** using `utils/text_extraction.py`
   - Search for date patterns: `YYYY-MM-DD`, `Month DD, YYYY`, etc.
   - Extract top candidate dates from first 2 pages
   - Present to user for confirmation

3. **Build file inventory**
   ```python
   FileEntry = {
       'original_path': str,
       'filename': str,
       'date': datetime | None,
       'date_source': 'filename' | 'content' | 'none',
       'needs_confirmation': bool,
       'needs_rename': bool
   }
   ```

#### Phase 2: Interactive Date Confirmation

**Only for files without filename dates:**

```
File: Annenberg COO Letter Formatted.pdf
Found Date: 2014-03-15 (from PDF content)
Confirm? [y/n/enter new date]:
```

- **'y' or Enter**: Accept extracted date, schedule rename
- **'n' + new date**: Use provided date, schedule rename
- **'n' + skip**: Mark as "Other" category, no date

**Renaming Operations**:
- New filename format: `YYYY-MM-DD - original_name.pdf`
- Batch all renames at end (safer than mid-process)
- Validate no filename collisions before executing

#### Phase 3: Document Classification

Extend `core/document_processor.py` logic with new patterns:

```python
CATEGORIES = {
    'CVs': [r'\bcv\b', r'curriculum.vitae'],
    'Resumes': [r'resume'],
    'Cover Letters': [r'cover', r'\bletter\b'],  # exclude diversity
    'Diversity Statements': [r'diversity.*statement', r'statement.*diversity'],
    'Other': []  # fallback
}
```

**Classification Process**:
1. Check filename against patterns (case-insensitive)
2. Diversity Statements checked before generic "letter" pattern
3. Fallback to "Other" if no matches

#### Phase 4: Sorting & Formatting

**Per Category**:
- Sort by date descending (newest first)
- Files without dates go to bottom of category
- Format as markdown list with date prefix

**Output Format**:
```markdown
## Files Referenced

### CVs
- 2024 AJB CV 2024.pdf
- 2015-11 AJB CV 2015 v2.pdf
- 2014-02 AJB CV Feb 2014 CSULB.pdf
- 2014-02 AJB CV Feb 2014.pdf

### Resumes
- 2025-10-13 Byrnes, Anthony Resume - Colburn School submitted.pdf
- 2020-11-23 ajb resume.pdf
- 2016-01-29 AJB resume v2.pdf
- 2015-12-01 DCA Anthony Byrnes Resume.pdf

### Cover Letters
- 2025-01-15 CSULB AD cover letter.pdf
- 2024-11-25 UCLA cover letter v. 2.pdf
- 2023-08-01 Byrnes, Anthony COTA AD cover letter.pdf
- 2023-02-25 CSULB cover letter.pdf
- 2023-01-27 csuf cover final.pdf

### Diversity Statements
- 2025-01-15 CSULB AD Diversity Statement.pdf
- 2024-11-25 UCLA Diversity Statement.pdf
- 2023-02-26 diversity statement.pdf

### Other
- 18th Street Arts Center.pdf
- Annenberg COO Letter Formatted.pdf
```

#### Phase 5: Append to Lexicons

For each file in `lexicons_llm/`:
1. Read current content
2. Check if "Files Referenced" section already exists (idempotent)
3. Append separator: `\n\n---\n\n`
4. Append formatted document list
5. Write back to file

**Target Files**:
- `lexicons_llm/01_career_philosophy.md`
- `lexicons_llm/02_achievement_library.md`
- `lexicons_llm/03_narrative_patterns.md`
- `lexicons_llm/04_language_bank.md`

## Future Integration: Approach 3 (LLM-Based)

For integration into `run_llm_analysis.py` pipeline:

### Date Extraction via Claude API

**When**: During document ingestion in `core/orchestrator.py`

**Process**:
1. After text extraction, before lexicon generation
2. For files without filename dates:
   - Send first 2 pages to Claude with prompt:
     ```
     Extract the date from this document (format: YYYY-MM-DD).
     Look for: creation date, document date, letter date.
     Return: {"date": "YYYY-MM-DD", "confidence": 0.0-1.0}
     ```
3. Store extracted date in document metadata
4. Auto-rename files with high confidence (>0.9)
5. Flag low confidence for user review

### Integration Points

**File**: `analyzers/llm_analyzer.py`

Add method:
```python
def extract_document_date(self, text: str) -> tuple[datetime, float]:
    """Extract date from document using Claude API."""
    # Implementation using existing _call_api() method
```

**File**: `core/orchestrator.py`

Update document processing:
```python
# After text extraction
if not date_from_filename(doc.filename):
    date, confidence = llm_analyzer.extract_document_date(doc.text)
    if confidence > 0.9:
        rename_document(doc, date)
```

**File**: `generators/hierarchical_generator.py`

Add method:
```python
def append_document_references(self, lexicon_path: str, documents: list):
    """Append formatted document list to lexicon."""
```

### Cost Considerations

- Date extraction: ~500 tokens per document
- 37 documents × $0.003/1K tokens ≈ $0.05 per full run
- Only runs for new documents (incremental updates)

## Testing Strategy

### One-Time Script Testing

1. **Dry Run Mode**: Print all operations without executing
2. **Backup**: Copy lexicons before modification
3. **Validation**: Check no duplicate "Files Referenced" sections
4. **Manual Review**: Verify date extraction accuracy on sample files

### Pipeline Integration Testing

1. Add test documents with various date formats
2. Verify correct date extraction and file renaming
3. Ensure incremental updates only process new files
4. Validate lexicon formatting remains consistent

## Success Criteria

### Immediate (Approach 1)
- [ ] All 37 documents classified correctly
- [ ] Files without dates renamed with extracted dates
- [ ] All 4 lexicons updated with "Files Referenced" section
- [ ] Documents sorted by type and date (newest first)

### Future (Approach 3)
- [ ] Automated date extraction integrated into pipeline
- [ ] High-confidence dates auto-applied
- [ ] Low-confidence dates flagged for review
- [ ] Document references auto-update with each lexicon generation

## Security & Safety

1. **Backup Strategy**: Copy lexicons before modification
2. **Atomic Renames**: Validate all renames before executing
3. **Collision Detection**: Check for duplicate filenames
4. **Rollback**: Keep original filenames in memory for undo

## Open Questions

None - design approved for implementation.