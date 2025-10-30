# Phase 4 Handoff Document: Lexicon Generators

**Date**: 2025-10-29
**Project**: Career Lexicon Builder
**Current Status**: Phase 3 Complete (256/256 core tests passing)
**Next Phase**: Phase 4 - Lexicon Generators

---

## Executive Summary

**Phase 3 Status**: ✅ COMPLETE
- All 4 analyzers implemented and tested (Themes, Qualifications, Narratives, Keywords)
- Similarity utilities working
- 256 core tests passing in ~29 seconds
- Integration tests created (may still be running in background)

**Phase 4 Goal**: Build lexicon generators that take analyzer outputs and produce formatted, human-readable reference documents.

**Estimated Effort**: 3-4 hours

---

## Current Project State

### Test Execution
```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Result: 256+ passed (integration tests may add 8 more)
```

### What's Been Built (Phases 1-3)

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
│   └── state_manager.py              ✅ Complete
├── generators/                       ⏳ EMPTY - Phase 4 work here
├── templates/                        ⏳ EMPTY - Phase 4 work here
├── utils/
│   ├── date_parser.py                ✅ Complete
│   ├── text_extraction.py            ✅ Complete
│   └── similarity.py                 ✅ Complete (156 lines)
└── tests/
    ├── fixtures/                     ✅ Sample documents for testing
    └── test_*.py                     ✅ 256+ tests passing
```

---

## Phase 4 Overview

### What Needs to Be Built

Phase 4 creates **lexicon generators** that transform analyzer outputs into human-readable reference documents. Each generator formats data for easy lookup when writing resumes, cover letters, or preparing for interviews.

### The Four Generators

1. **Themes Lexicon Generator** - "My Values Reference"
2. **Qualifications Lexicon Generator** - "Resume Bullet Variations"
3. **Narratives Lexicon Generator** - "Storytelling Patterns Catalog"
4. **Keywords Lexicon Generator** - "Usage Index"

### Key Design Principle

From the design document:
> "The output isn't meant to be read cover-to-cover. It's meant to be searched when I need it."

**Output format**: Markdown files that are:
- Searchable (clear headings, keywords)
- Skimmable (bullet points, short paragraphs)
- Chronologically organized (where relevant)
- Citation-rich (links back to source documents)

---

## Requirements from Design Document

### Reference: Implementation Plan Lines 422-520

**Location**: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md`

### Task 4.1: Themes Lexicon Generator

**Effort**: 1 hour

**File**: `generators/themes_lexicon_generator.py`

**Purpose**: Generate "My Values" reference document from themes analysis

**Input**: List of `Theme` objects from themes analyzer

**Output**: Markdown document structured as:
```markdown
# My Values and Themes

Generated: 2024-01-15

## Theme: Leadership
Confidence: 0.85 | First seen: 2020-06 | Last seen: 2024-01

### Occurrences (chronological)

#### 2020-06-15 - cover_letter_techcorp.txt
> "I believe in collaborative leadership that empowers individuals..."

**Context**: When managing teams, I believe in collaborative leadership...

#### 2024-01-15 - cover_letter_newco.txt
> "My approach to leadership focuses on transparency..."

**Context**: Throughout my career, my approach to leadership...

---

## Theme: Innovation
...
```

**Functions to implement**:

```python
def generate_themes_lexicon(themes: List[Theme], output_path: str) -> None
```
- Takes themes from analyzer
- Sorts by confidence (high to low)
- Formats as markdown with:
  - Theme name as heading
  - Metadata (confidence, dates)
  - Chronological occurrences with quotes
  - Source citations
- Writes to output file

**Template structure**:
- Header with generation date
- Table of contents (optional)
- Each theme as H2 section
- Occurrences as H3 subsections

---

### Task 4.2: Qualifications Lexicon Generator

**Effort**: 1 hour

**File**: `generators/qualifications_lexicon_generator.py`

**Purpose**: Generate "Resume Bullet Variations" reference from qualifications analysis

**Input**: List of `Qualification` objects

**Output**: Markdown document structured as:
```markdown
# Resume Bullet Variations

Generated: 2024-01-15

## Senior Software Engineer at TechCorp
ID: senior_engineer_techcorp | Confidence: 0.90

### Variations (most recent first)

#### Version 1 - resume_2024.txt (2024-02-01)
- Managed engineering team of 5 developers building cloud infrastructure
- Designed and implemented microservices architecture handling 100K+ users
- Created automated deployment pipeline cutting release time by 60%

#### Version 2 - resume_2020.txt (2020-06-01)
- Led cross-functional team of 5 engineers in developing cloud-based applications
- Architected microservices platform serving 100K+ daily active users
- Implemented CI/CD pipeline reducing deployment time by 60%

---

## Software Developer at StartupCo
...
```

**Functions to implement**:

```python
def generate_qualifications_lexicon(qualifications: List[Qualification], output_path: str) -> None
```
- Takes qualifications from analyzer
- Sorts by most recent date
- Formats as markdown with:
  - Position title and organization as heading
  - Metadata (ID, confidence)
  - Variations sorted by date (most recent first)
  - Side-by-side comparison of phrasing evolution
- Writes to output file

---

### Task 4.3: Narratives Lexicon Generator

**Effort**: 1 hour

**File**: `generators/narratives_lexicon_generator.py`

**Purpose**: Generate "Storytelling Patterns Catalog" from narratives analysis

**Input**: List of `NarrativeCategory` objects

**Output**: Markdown document structured as:
```markdown
# Storytelling Patterns Catalog

Generated: 2024-01-15

## Metaphors
Confidence: 0.78 | Patterns found: 5

### 2024-01-15 - cover_letter.txt
**Pattern**: "I approach problems like a detective solving a mystery"

**Context**: Throughout my career at TechCorp, I approach problems like a detective...

---

### 2023-06-20 - cover_letter_old.txt
**Pattern**: "My work is like building bridges between teams"

**Context**: I see my role as like building bridges between technical...

---

## Opening Hooks
Confidence: 0.85 | Patterns found: 3

### 2024-01-15 - cover_letter.txt
**Pattern**: "What if technology could transform how we collaborate?"

**Context**: Dear Hiring Manager, What if technology could transform...

---

## Transitions
...
```

**Functions to implement**:

```python
def generate_narratives_lexicon(narratives: List[NarrativeCategory], output_path: str) -> None
```
- Takes narrative categories from analyzer
- Sorts categories alphabetically
- Within each category, sort chronologically
- Formats as markdown with:
  - Category name as heading
  - Metadata (confidence, count)
  - Each pattern with full text and context
  - Source citations
- Writes to output file

---

### Task 4.4: Keywords Lexicon Generator

**Effort**: 1 hour

**File**: `generators/keywords_lexicon_generator.py`

**Purpose**: Generate "Usage Index" from keywords analysis

**Input**: List of `KeywordEntry` objects

**Output**: Markdown document structured as:
```markdown
# Keyword Usage Index

Generated: 2024-01-15

Total keywords: 45 | Minimum frequency: 2

## stakeholder management
Frequency: 5 | Aliases: project management, client relations
Document types: resume, cover_letter

### Usage contexts (most recent first)

#### resume_2024.txt (resume) - 2024-02-01
> "Strong **stakeholder management** skills across technical and business teams"

#### cover_letter_2024.txt (cover_letter) - 2024-01-15
> "I bring extensive experience in **stakeholder management** to complex projects"

#### resume_2020.txt (resume) - 2020-06-01
> "Demonstrated **stakeholder management** through successful client engagements"

---

## software engineering
Frequency: 8 | Aliases: software development, engineering
Document types: resume, cover_letter, job_description

...
```

**Functions to implement**:

```python
def generate_keywords_lexicon(keywords: List[KeywordEntry], output_path: str, min_frequency: int = 2) -> None
```
- Takes keyword entries from analyzer
- Filters by minimum frequency
- Sorts alphabetically
- Formats as markdown with:
  - Keyword as heading
  - Metadata (frequency, aliases, document types)
  - Usage contexts with highlighted keywords
  - Chronological ordering (most recent first)
  - Source citations with document type
- Writes to output file

---

## Implementation Guidance

### Common Patterns Across All Generators

All generators should:

1. **Accept analyzer output** + **output path**
2. **Format as markdown** with consistent structure
3. **Include metadata** (generation date, confidence scores, counts)
4. **Cite sources** (document names, dates)
5. **Write to file** (create directories if needed)

### Markdown Formatting Guidelines

**Headers**:
- `# Title` - Document title
- `## Section` - Major sections (themes, positions, categories, keywords)
- `### Subsection` - Individual occurrences/variations
- `#### Detail` - Specific versions or dates

**Emphasis**:
- `**bold**` - Keywords, important terms
- `> quote` - Actual quotes from documents
- `` `code` `` - IDs, technical terms

**Metadata format**:
```markdown
Confidence: 0.85 | First seen: 2020-06 | Last seen: 2024-01
```

**Citations**:
```markdown
Source: resume_2024.txt (2024-02-01)
```

### Helper Functions (Recommended)

Create a `templates/formatting_utils.py` module with:

```python
def format_date(d: Optional[date]) -> str:
    """Format date as YYYY-MM-DD or 'Unknown'."""
    return d.strftime('%Y-%m-%d') if d else 'Unknown'

def format_confidence(conf: float) -> str:
    """Format confidence as percentage."""
    return f"{conf*100:.0f}%"

def format_citation(source: str, doc_date: Optional[date] = None) -> str:
    """Format source citation."""
    if doc_date:
        return f"{source} ({format_date(doc_date)})"
    return source

def create_markdown_file(path: str, content: str) -> None:
    """Create markdown file, creating directories if needed."""
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
```

---

## Testing Strategy

### Unit Tests

For each generator, create corresponding test file:

- `tests/test_themes_lexicon_generator.py`
- `tests/test_qualifications_lexicon_generator.py`
- `tests/test_narratives_lexicon_generator.py`
- `tests/test_keywords_lexicon_generator.py`

**Test cases for each generator**:
1. Test with sample data (from Phase 3 analyzers)
2. Test markdown structure (headers, sections present)
3. Test content accuracy (data appears in output)
4. Test file creation (file exists, readable)
5. Test metadata inclusion (dates, confidence scores)
6. Test chronological ordering
7. Test empty input handling
8. Test output directory creation

### Integration Test

Create `tests/test_phase4_integration.py`:

```python
def test_full_pipeline_phases_1_to_4():
    """Test complete pipeline from extraction to lexicon generation."""
    # Load sample documents
    # Process with Phase 2 (classification, state)
    # Analyze with Phase 3 (all 4 analyzers)
    # Generate with Phase 4 (all 4 generators)
    # Verify all output files exist and contain expected content
```

---

## Recommended Implementation Order

### Batch 1: Setup + Themes Generator (1-1.5 hours)
1. Create `templates/formatting_utils.py` with helper functions
2. Write tests for themes generator
3. Implement `generators/themes_lexicon_generator.py`
4. Verify tests pass

### Batch 2: Qualifications + Narratives Generators (1.5-2 hours)
1. Write tests for qualifications generator
2. Implement `generators/qualifications_lexicon_generator.py`
3. Write tests for narratives generator
4. Implement `generators/narratives_lexicon_generator.py`
5. Verify tests pass

### Batch 3: Keywords Generator (1 hour)
1. Write tests for keywords generator
2. Implement `generators/keywords_lexicon_generator.py`
3. Verify tests pass

### Batch 4: Integration + Polish (0.5-1 hour)
1. Create integration test (full pipeline)
2. Test with real sample documents from Phase 3 fixtures
3. Review output quality
4. Polish formatting if needed
5. Run full test suite

---

## How to Continue in Next Session

### Step 1: Verify Current State

```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Should see: 256+ passed
```

### Step 2: Review Requirements

- Read this handoff document completely
- Review design document sections on lexicon generators
- Look at Phase 3 analyzer outputs (data structures) to understand inputs

### Step 3: Start with Batch 1

1. **Create formatting utilities**:
   ```bash
   mkdir -p templates
   touch templates/__init__.py
   touch templates/formatting_utils.py
   ```

2. **Write helper functions** in `formatting_utils.py`:
   - `format_date()`
   - `format_confidence()`
   - `format_citation()`
   - `create_markdown_file()`

3. **Create themes generator tests**:
   ```bash
   touch tests/test_themes_lexicon_generator.py
   ```

4. **Write tests first** (TDD approach):
   - Import themes analyzer data structures
   - Create sample Theme objects
   - Write tests for expected markdown output

5. **Implement generator**:
   ```bash
   touch generators/__init__.py
   touch generators/themes_lexicon_generator.py
   ```

6. **Run tests**:
   ```bash
   python -m pytest tests/test_themes_lexicon_generator.py -v
   ```

### Step 4: Continue with Batches 2-4

Follow the same TDD pattern for each generator.

---

## Example: Themes Generator Implementation

### Sample Test

```python
"""Tests for themes_lexicon_generator module."""

import pytest
from datetime import date
from pathlib import Path
import tempfile

from analyzers.themes_analyzer import Theme, ThemeOccurrence
from generators.themes_lexicon_generator import generate_themes_lexicon


def test_generate_themes_lexicon():
    """Test generating themes lexicon markdown."""
    # Create sample themes
    occ1 = ThemeOccurrence(
        quote="I believe in collaborative leadership",
        context="When working with teams, I believe in collaborative leadership...",
        source_document="cover_letter_2024.txt",
        date=date(2024, 1, 15)
    )

    theme = Theme(
        theme_name="Leadership",
        occurrences=[occ1],
        confidence=0.85,
        first_seen=date(2024, 1, 15),
        last_seen=date(2024, 1, 15)
    )

    # Generate to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        output_path = f.name

    generate_themes_lexicon([theme], output_path)

    # Verify file exists
    assert Path(output_path).exists()

    # Read and verify content
    with open(output_path, 'r') as f:
        content = f.read()

    assert "# My Values and Themes" in content
    assert "## Leadership" in content
    assert "Confidence: 85%" in content
    assert "I believe in collaborative leadership" in content
    assert "cover_letter_2024.txt" in content

    # Cleanup
    Path(output_path).unlink()
```

### Sample Implementation

```python
"""
Themes lexicon generator - creates reference document for personal values.
"""

from typing import List
from pathlib import Path
from datetime import datetime

from analyzers.themes_analyzer import Theme
from templates.formatting_utils import (
    format_date, format_confidence, format_citation, create_markdown_file
)


def generate_themes_lexicon(themes: List[Theme], output_path: str) -> None:
    """
    Generate "My Values" reference document from themes analysis.

    Args:
        themes: List of Theme objects from themes analyzer
        output_path: Path to write markdown file

    Examples:
        >>> themes = analyze_themes(documents)
        >>> generate_themes_lexicon(themes, "output/my_values.md")
    """
    if not themes:
        content = "# My Values and Themes\n\nNo themes found.\n"
        create_markdown_file(output_path, content)
        return

    # Build markdown content
    lines = []

    # Header
    lines.append("# My Values and Themes\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"Total themes: {len(themes)}\n")
    lines.append("---\n\n")

    # Each theme
    for theme in themes:
        lines.append(f"## {theme.theme_name}\n")
        lines.append(f"Confidence: {format_confidence(theme.confidence)}")

        if theme.first_seen:
            lines.append(f" | First seen: {format_date(theme.first_seen)}")
        if theme.last_seen:
            lines.append(f" | Last seen: {format_date(theme.last_seen)}")
        lines.append("\n\n")

        # Occurrences
        lines.append("### Occurrences (chronological)\n\n")

        for occ in theme.occurrences:
            # Date and source
            date_str = format_date(occ.date) if occ.date else "Unknown date"
            lines.append(f"#### {date_str} - {occ.source_document}\n")

            # Quote
            lines.append(f'> "{occ.quote}"\n\n')

            # Context
            lines.append(f"**Context**: {occ.context}\n\n")
            lines.append("---\n\n")

    # Write to file
    content = ''.join(lines)
    create_markdown_file(output_path, content)
```

---

## Success Criteria for Phase 4

- [ ] All 4 generators implemented
- [ ] Each generator has comprehensive tests
- [ ] **Target: ~280-300 tests passing** (256 current + ~30-50 new)
- [ ] All generators produce valid markdown
- [ ] Output files are human-readable and searchable
- [ ] Integration test passes (full pipeline)
- [ ] Sample outputs generated from Phase 3 fixtures

---

## Expected File Structure After Phase 4

```
generators/
├── __init__.py
├── themes_lexicon_generator.py          (~150 lines)
├── qualifications_lexicon_generator.py  (~150 lines)
├── narratives_lexicon_generator.py      (~150 lines)
└── keywords_lexicon_generator.py        (~150 lines)

templates/
├── __init__.py
└── formatting_utils.py                  (~80 lines)

tests/
├── test_themes_lexicon_generator.py     (~8 tests)
├── test_qualifications_lexicon_generator.py (~8 tests)
├── test_narratives_lexicon_generator.py (~8 tests)
├── test_keywords_lexicon_generator.py   (~8 tests)
└── test_phase4_integration.py           (~5 tests)
```

**Estimated additions**: ~680 lines of production code, ~500 lines of test code

---

## Common Pitfalls to Avoid

### 1. Don't Over-Format
Keep markdown simple and readable. Don't add excessive styling or complex tables.

### 2. Preserve Chronological Order
Users want to see evolution over time. Always sort by date where applicable.

### 3. Include Full Context
Don't just show keywords - show the full quote and surrounding context.

### 4. Handle Missing Data Gracefully
Not all data has dates or complete metadata. Use "Unknown" or skip gracefully.

### 5. Make it Searchable
Use clear headings and keywords so users can Ctrl+F to find what they need.

---

## Dependencies

**No new dependencies needed!** All required functionality is available in:
- Python standard library (`datetime`, `pathlib`, `typing`)
- Existing Phase 3 analyzers (for data structures)

---

## Resources

### Design Documents
- **Primary**: `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`
- **Implementation**: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md` (lines 422-520)

### Phase 3 Analyzer Outputs (Inputs for Phase 4)
- `analyzers/themes_analyzer.py` - `Theme` and `ThemeOccurrence` classes
- `analyzers/qualifications_analyzer.py` - `Qualification` and `QualificationVariation` classes
- `analyzers/narratives_analyzer.py` - `NarrativeCategory` and `NarrativePattern` classes
- `analyzers/keywords_analyzer.py` - `KeywordEntry` and `KeywordUsage` classes

### Test Fixtures
- `tests/fixtures/sample_resume.txt`
- `tests/fixtures/sample_cover_letter.txt`
- `tests/fixtures/sample_resume_v2.txt`

---

## Timeline Estimate

**Phase 4 Total**: 3-4 hours

- Batch 1 (Setup + Themes): 1-1.5 hours
- Batch 2 (Qualifications + Narratives): 1.5-2 hours
- Batch 3 (Keywords): 1 hour
- Batch 4 (Integration + Polish): 0.5-1 hour

**Remaining Project Phases**:
- Phase 5 (Orchestrator): 2-3 hours
- Phase 6 (End-to-End Testing): 2-3 hours
- Phase 7 (CLI): 1-2 hours

**Total Remaining**: 8-13 hours

---

## Quick Reference: Phase 4 Generators

| Generator | Input | Output | Purpose |
|-----------|-------|--------|---------|
| **Themes** | `List[Theme]` | `my_values.md` | Reference for personal values/beliefs |
| **Qualifications** | `List[Qualification]` | `resume_variations.md` | Track position phrasing evolution |
| **Narratives** | `List[NarrativeCategory]` | `storytelling_patterns.md` | Catalog of rhetorical devices |
| **Keywords** | `List[KeywordEntry]` | `usage_index.md` | Cross-referenced keyword lookup |

---

**Session Complete**: 2025-10-29
**Phase 3 Status**: ✅ COMPLETE (256+ tests passing)
**Phase 4 Status**: ⏳ READY TO START
**Next Session**: Begin with Batch 1 (Setup + Themes Generator)

---

**Generated**: 2025-10-29
**By**: Claude (Sonnet 4.5)
**For**: Career Lexicon Builder Project
**Session**: Phase 3 → Phase 4 Transition
