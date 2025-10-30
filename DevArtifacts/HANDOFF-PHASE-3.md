# Phase 3 Handoff Document

**Date**: 2025-10-29
**Project**: Career Lexicon Builder
**Current Status**: Phase 2 Complete (137/137 tests passing)
**Next Phase**: Phase 3 - Analysis Modules

---

## Executive Summary

Phases 1 and 2 are complete with 137/137 tests passing. We now have:
- Multi-format document extraction (.pages, .pdf, .docx, .txt, .md)
- Document classification (resume vs. cover letter vs. job description)
- State management with incremental processing

**Phase 3 Goal**: Build the four analysis modules that extract themes, qualifications, narratives, and keywords from the processed documents.

---

## Current Project State

### Directory Structure
```
/Users/anthonybyrnes/PycharmProjects/career-lexicon-builder/
├── analyzers/              # Empty - for Phase 3 ⭐
├── core/
│   ├── __init__.py              ✅ Complete
│   ├── confidence_scorer.py     ✅ Complete (138 lines)
│   ├── document_processor.py    ✅ Complete (277 lines)
│   └── state_manager.py         ✅ Complete (327 lines)
├── generators/             # Empty - for Phase 4
├── templates/              # Empty - for Phase 4
├── utils/
│   ├── __init__.py              ✅ Complete
│   ├── date_parser.py           ✅ Complete (148 lines)
│   └── text_extraction.py       ✅ Complete (593 lines)
├── tests/
│   ├── test_confidence_scorer.py      ✅ 22 tests
│   ├── test_date_parser.py            ✅ 25 tests
│   ├── test_document_processor.py     ✅ 27 tests
│   ├── test_state_manager.py          ✅ 33 tests
│   └── test_text_extraction.py        ✅ 30 tests
├── archive/
│   └── 2025-10-29-skill-based-implementation/
└── DesignDocuments/
    ├── 2025-01-27-career-lexicon-builder-design.md
    └── 2025-01-27-career-lexicon-builder-implementation.md
```

### What's Been Built

#### Phase 1: Foundation (55 tests)
1. **Date Parser** (`utils/date_parser.py`)
   - Extract dates from filenames
   - Format citations
   - Sort chronologically

2. **Text Extraction** (`utils/text_extraction.py`)
   - Multi-format support: .pages, .pdf, .docx, .txt, .md
   - Metadata extraction
   - Unified API

#### Phase 2: Document Processing (82 tests)
1. **Confidence Scorer** (`core/confidence_scorer.py`)
   - `calculate_confidence(criteria, weights)` - Weighted averaging
   - `should_flag_for_review(confidence, threshold)` - Review flagging
   - `get_confidence_category(confidence)` - High/medium/low categorization

2. **Document Processor** (`core/document_processor.py`)
   - `DocumentType` enum: RESUME, COVER_LETTER, JOB_DESCRIPTION, UNKNOWN
   - `classify_by_filename(filename)` - Pattern-based classification
   - `classify_by_content(text)` - Content analysis with confidence scoring
   - `classify_document(filepath, text)` - Main classification API

3. **State Manager** (`core/state_manager.py`)
   - `DocumentRecord` and `ProcessingManifest` dataclasses
   - `compute_file_hash(filepath)` - SHA-256 change detection
   - `load_manifest(path)` / `save_manifest(manifest, path)` - JSON persistence
   - `needs_processing(filepath, manifest)` - Incremental processing
   - `get_documents_by_type(manifest, doc_type)` - Filtering
   - `get_files_to_process(input_dir, manifest, extensions)` - Directory scanning

### Test Execution
```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
# Result: 137 passed in 0.27s
```

### Dependencies (requirements.txt)
```
pytest>=8.4.2
pdfplumber>=0.11.0
python-docx>=1.1.0
```

---

## Phase 3: Analysis Modules (8-10 hours)

### Overview
**Location**: Implementation plan lines 224-420
**Goal**: Build four analyzers to extract themes, qualifications, narratives, and keywords from documents

### What Needs to Be Built

Phase 3 consists of 5 tasks:
1. **Task 3.1**: Confidence Scorer (already done in Phase 2! ✅)
2. **Task 3.2**: Similarity Utilities
3. **Task 3.3**: Themes Analyzer
4. **Task 3.4**: Qualifications Analyzer
5. **Task 3.5**: Narratives Analyzer
6. **Task 3.6**: Keywords Analyzer

---

### Task 3.2: Similarity Utilities
**Effort**: 1.5 hours
**Dependencies**: None (can start immediately)

Create `utils/similarity.py`:

**Purpose**: Provide semantic similarity and clustering for all analyzers

**Library Choice**: Use **sentence-transformers** (simpler than spaCy, no large model downloads)
- Lightweight and easy to install
- Pre-trained models for sentence embeddings
- Good balance of accuracy and simplicity

**Functions to implement**:

```python
def calculate_semantic_similarity(text1: str, text2: str) -> float
```
- Use sentence embeddings from sentence-transformers
- Calculate cosine similarity
- Return score 0.0-1.0

```python
def cluster_similar_items(items: List[str], threshold: float = 0.7) -> List[List[str]]
```
- Group items by semantic similarity
- Use simple clustering (agglomerative or DBSCAN)
- Return list of clusters (each cluster is a list of similar items)

**Test requirements**:
- Test similarity between identical texts (should be ~1.0)
- Test similarity between unrelated texts (should be low)
- Test clustering with clear groups
- Test clustering with no similar items
- Test edge cases (empty input, single item)

**Deliverable**: Similarity utilities for use by all analyzers

---

### Task 3.3: Themes Analyzer
**Effort**: 2-3 hours
**Dependencies**: 3.2 (similarity utilities)

Create `analyzers/themes_analyzer.py`:

**Purpose**: Extract recurring themes/values from cover letters with chronological quotes

**Key insight from design document**:
> "I don't need to count how often I mention 'leadership.' I need to remember HOW I've framed leadership across different contexts."

**Data structures**:
```python
@dataclass
class ThemeOccurrence:
    quote: str                    # The actual quote
    context: str                  # Surrounding sentences for context
    source_document: str          # Filepath
    date: Optional[date]          # Document date

@dataclass
class Theme:
    theme_name: str               # e.g., "Leadership"
    occurrences: List[ThemeOccurrence]
    confidence: float             # How confident we are this is a real theme
    first_seen: Optional[date]    # Earliest occurrence
    last_seen: Optional[date]     # Most recent occurrence
```

**Functions to implement**:

```python
def extract_themes_from_document(text: str, filepath: str, doc_date: Optional[date]) -> List[ThemeOccurrence]
```
- Split text into sentences/paragraphs
- Identify value-laden or philosophy statements (avoid generic statements)
- Extract quotes with context
- Return list of occurrences

```python
def cluster_theme_occurrences(occurrences: List[ThemeOccurrence]) -> List[Theme]
```
- Use semantic similarity to group related quotes
- Name each theme based on common concepts
- Calculate confidence based on:
  - Frequency (how many occurrences)
  - Consistency (semantic similarity within cluster)
  - Temporal stability (appears across multiple documents/dates)
- Sort occurrences chronologically within each theme
- Return list of themes

```python
def analyze_themes(documents: List[Dict]) -> List[Theme]
```
- Main API: takes list of processed documents
- Filter to cover letters only
- Extract occurrences from each document
- Cluster into themes
- Return sorted by confidence (highest first)

**Heuristics for theme detection** (not exhaustive, can be refined):
- Look for first-person statements about values/beliefs
- Phrases like "I believe", "I'm passionate about", "I value"
- Recurring topics across multiple documents
- Avoid generic filler phrases

**Test requirements**:
- Test single document theme extraction
- Test clustering similar themes
- Test chronological ordering
- Test confidence calculation
- Test with multiple documents
- Test edge cases (no themes, very short documents)

**Deliverable**: Themes analyzer that produces chronologically-ordered theme examples

---

### Task 3.4: Qualifications Analyzer
**Effort**: 2-3 hours
**Dependencies**: 3.2 (similarity utilities)

Create `analyzers/qualifications_analyzer.py`:

**Purpose**: Track how you've phrased the same position/qualification across different resume versions

**Key insight from design document**:
> "When I update my resume, I want to see: here are the 7 ways you've described this role in past versions"

**Data structures**:
```python
@dataclass
class QualificationVariation:
    text: str                     # The bullet point or phrase
    source_document: str          # Filepath
    date: Optional[date]          # Document date
    position_context: str         # Job title/company if available

@dataclass
class Qualification:
    qualification_id: str         # Unique identifier (e.g., "senior_engineer_techcorp")
    position_title: str           # e.g., "Senior Software Engineer"
    organization: str             # e.g., "TechCorp"
    variations: List[QualificationVariation]
    confidence: float             # Confidence this is a real qualification
```

**Functions to implement**:

```python
def extract_qualifications_from_resume(text: str, filepath: str, doc_date: Optional[date]) -> List[QualificationVariation]
```
- Parse resume structure (sections like Experience, Education)
- Extract position titles and organizations
- Extract bullet points under each position
- Return list of variations with context

```python
def cluster_qualification_variations(variations: List[QualificationVariation]) -> List[Qualification]
```
- Group variations by position/organization (using similarity)
- Generate qualification_id from position/org
- Sort variations chronologically (most recent first)
- Calculate confidence based on how well-defined the position is
- Return list of qualifications

```python
def analyze_qualifications(documents: List[Dict]) -> List[Qualification]
```
- Main API: takes list of processed documents
- Filter to resumes only
- Extract variations from each document
- Cluster into qualifications
- Return sorted by date (most recent first)

**Test requirements**:
- Test extraction from resume with clear structure
- Test clustering variations of same position
- Test chronological ordering
- Test confidence calculation
- Test with multiple resume versions
- Test edge cases (ambiguous structure, missing dates)

**Deliverable**: Qualifications analyzer showing phrasing variations over time

---

### Task 3.5: Narratives Analyzer
**Effort**: 2-3 hours
**Dependencies**: None (pattern-based, not similarity-based)

Create `analyzers/narratives_analyzer.py`:

**Purpose**: Extract storytelling patterns, metaphors, and rhetorical devices from cover letters

**Key insight from design document**:
> "Catalog how I've structured stories, what metaphors resonate, rhetorical patterns that worked"

**Data structures**:
```python
@dataclass
class NarrativePattern:
    pattern_type: str             # e.g., "metaphor", "problem-solution", "call-to-action"
    text: str                     # The actual text
    context: str                  # Surrounding paragraphs
    source_document: str          # Filepath
    date: Optional[date]          # Document date

@dataclass
class NarrativeCategory:
    category_name: str            # e.g., "Opening Hooks", "Metaphors"
    patterns: List[NarrativePattern]
    confidence: float             # Confidence in categorization
```

**Functions to implement**:

```python
def extract_narrative_patterns(text: str, filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]
```
- Detect opening hooks (first paragraph patterns)
- Identify metaphors and analogies (pattern matching for "like", "as", comparisons)
- Find problem-solution structures
- Detect calls-to-action (closing paragraphs)
- Extract transition phrases
- Return list of patterns with types

```python
def categorize_narrative_patterns(patterns: List[NarrativePattern]) -> List[NarrativeCategory]
```
- Group patterns by type
- Sort chronologically within each category
- Calculate confidence based on clarity of pattern
- Return list of categories

```python
def analyze_narratives(documents: List[Dict]) -> List[NarrativeCategory]
```
- Main API: takes list of processed documents
- Filter to cover letters only
- Extract patterns from each document
- Categorize patterns
- Return sorted by category

**Pattern detection heuristics**:
- **Metaphors**: "like", "as", "similar to", comparison language
- **Problem-Solution**: "challenge/problem" followed by "solution/approach"
- **Opening Hooks**: Question, bold statement, personal anecdote (first paragraph)
- **Calls-to-Action**: "I look forward to", "I would welcome", "excited to discuss"
- **Transitions**: "Furthermore", "Additionally", "In addition to", "Building on"

**Test requirements**:
- Test metaphor detection
- Test problem-solution detection
- Test opening hook detection
- Test categorization
- Test with multiple documents
- Test edge cases (very short letters, no patterns)

**Deliverable**: Narratives analyzer cataloging rhetorical patterns

---

### Task 3.6: Keywords Analyzer
**Effort**: 1.5 hours
**Dependencies**: 3.2 (similarity utilities)

Create `analyzers/keywords_analyzer.py`:

**Purpose**: Build cross-referenced keyword index showing where and how terms are used

**Key insight from design document**:
> "When I need to write about 'stakeholder management,' show me the 3 contexts where I've used it before"

**Data structures**:
```python
@dataclass
class KeywordUsage:
    keyword: str                  # The keyword/phrase
    context: str                  # Sentence containing the keyword
    source_document: str          # Filepath
    document_type: str            # resume, cover_letter, job_description
    date: Optional[date]          # Document date

@dataclass
class KeywordEntry:
    keyword: str                  # The main keyword
    aliases: List[str]            # Similar terms (e.g., "leadership", "leading")
    usages: List[KeywordUsage]    # All usages across documents
    frequency: int                # Total count
    document_types: Set[str]      # Which doc types it appears in
```

**Functions to implement**:

```python
def extract_keywords_from_document(text: str, filepath: str, doc_type: str, doc_date: Optional[date]) -> List[KeywordUsage]
```
- Extract significant terms (2-4 word phrases, not stopwords)
- Use TF-IDF or simple frequency filtering to identify key terms
- Capture surrounding context (sentence)
- Return list of keyword usages

```python
def build_keyword_index(usages: List[KeywordUsage]) -> List[KeywordEntry]
```
- Group usages by keyword
- Use similarity to identify aliases (similar terms)
- Aggregate statistics (frequency, document types)
- Sort usages by date (most recent first)
- Return list of keyword entries sorted by frequency (highest first)

```python
def analyze_keywords(documents: List[Dict], min_frequency: int = 2) -> List[KeywordEntry]
```
- Main API: takes list of processed documents
- Extract keywords from all documents (resumes and cover letters)
- Build index
- Filter by minimum frequency
- Return sorted by frequency

**Test requirements**:
- Test keyword extraction from document
- Test building index from multiple documents
- Test alias detection
- Test frequency filtering
- Test cross-document usage tracking
- Test edge cases (very short documents, no keywords)

**Deliverable**: Keywords analyzer providing usage context lookup

---

## Implementation Plan for Phase 3

### Recommended Order

**Batch 1: Similarity Utilities** (Task 3.2)
1. Install sentence-transformers: Add to requirements.txt
2. Implement `calculate_semantic_similarity()`
3. Implement `cluster_similar_items()`
4. Write comprehensive tests
5. Verify all tests pass

**Batch 2: Themes Analyzer** (Task 3.3)
1. Implement data structures (ThemeOccurrence, Theme)
2. Implement `extract_themes_from_document()`
3. Implement `cluster_theme_occurrences()`
4. Implement `analyze_themes()` main API
5. Write comprehensive tests
6. Verify all tests pass

**Batch 3: Qualifications & Narratives** (Tasks 3.4 & 3.5)
1. Implement qualifications_analyzer.py
2. Write tests for qualifications
3. Implement narratives_analyzer.py
4. Write tests for narratives
5. Verify all tests pass

**Batch 4: Keywords Analyzer** (Task 3.6)
1. Implement keywords_analyzer.py
2. Write comprehensive tests
3. Verify all tests pass

**Batch 5: Integration Testing**
1. Create integration test using real document samples
2. Test full pipeline: extraction → classification → analysis
3. Verify all 4 analyzers work together
4. Run full test suite (Phase 1 + 2 + 3)

### Success Criteria
- All tests passing (Phase 1 + Phase 2 + Phase 3)
- Each analyzer produces sensible output
- Confidence scores are reasonable
- Chronological ordering works correctly
- Semantic similarity clustering is coherent

---

## Key Architecture Decisions

### 1. Sentence-Transformers for Similarity
**Decision**: Use sentence-transformers instead of spaCy or OpenAI embeddings
**Rationale**:
- Simpler installation (no large model downloads like spaCy)
- Good accuracy for semantic similarity
- Self-contained (no API keys needed)
- Fast enough for ~30 documents

**Impact**: Add `sentence-transformers` to requirements.txt

### 2. Pattern-Based Narrative Detection
**Decision**: Use regex/heuristics rather than ML for narrative patterns
**Rationale**:
- Patterns are well-defined (metaphors, transitions, hooks)
- Interpretable and debuggable
- No training data needed
- Sufficient for personal documents

**Impact**: Narratives analyzer is simpler than other analyzers

### 3. Document Type Filtering
**Decision**: Each analyzer filters to relevant document types
**Rationale**:
- Themes come from cover letters (conversational, personal)
- Qualifications come from resumes (structured, factual)
- Narratives come from cover letters (storytelling)
- Keywords come from all documents (cross-reference)

**Impact**: Analyzers should filter documents by type before processing

### 4. Chronological Ordering
**Decision**: Sort all occurrences by date (most recent first, or oldest first where it makes sense)
**Rationale**: User wants to see evolution of phrasing over time
**Impact**: All data structures include date fields; sorting is core feature

### 5. Confidence Scoring Throughout
**Decision**: Use confidence_scorer for all analysis outputs
**Rationale**: User should know which results are reliable vs. ambiguous
**Impact**: Every analyzer returns confidence scores with results

---

## Common Pitfalls to Avoid

### 1. Don't Over-Engineer
The goal is a **reference lexicon**, not a sophisticated NLP system. Simple pattern matching and similarity clustering are sufficient. You're processing ~30 personal documents, not millions of web pages.

### 2. Preserve Original Text
Always include the **actual quotes** and **context**. Don't just store summaries or extracted keywords. The user needs to see their original phrasing.

### 3. Handle Missing Dates Gracefully
Not all documents will have dates. Chronological features should work with partial date information.

### 4. Test with Realistic Text
Use test cases that resemble real resume/cover letter content. Avoid trivial "test 123" examples.

### 5. Balance Precision vs. Recall
For themes and keywords: Better to miss some occurrences than to produce too many false positives. Confidence scoring helps flag uncertain results.

---

## Testing Strategy

### Unit Tests
Each analyzer module should have:
- Data structure tests (creation, serialization)
- Individual function tests
- Edge case handling
- Confidence score validation

### Integration Tests
Create `tests/test_phase3_integration.py`:
- Test full pipeline with sample documents
- Verify analyzers work together
- Check output format consistency

### Sample Test Data
Create minimal test documents in `tests/fixtures/`:
- `sample_resume.txt` - Simple resume with 2-3 positions
- `sample_cover_letter.txt` - Cover letter with clear themes
- `sample_resume_v2.txt` - Updated version of resume (for variation testing)

---

## Resources

### Design Documents
- Primary: `DesignDocuments/2025-01-27-career-lexicon-builder-design.md`
- Implementation: `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md` (lines 224-420)

### Current Code (Phase 1 & 2)
- Utils: `utils/date_parser.py`, `utils/text_extraction.py`
- Core: `core/confidence_scorer.py`, `core/document_processor.py`, `core/state_manager.py`
- Tests: `tests/test_*.py`

### Dependencies to Add
```bash
# Add to requirements.txt
sentence-transformers>=2.2.0
scikit-learn>=1.3.0  # For clustering algorithms
```

---

## Estimated Timeline

**Phase 3 Total**: 8-10 hours

- Task 3.2 (Similarity): 1.5 hours
- Task 3.3 (Themes): 2-3 hours
- Task 3.4 (Qualifications): 2-3 hours
- Task 3.5 (Narratives): 2 hours
- Task 3.6 (Keywords): 1.5 hours
- Integration testing: 1 hour

**Remaining Phases**:
- Phase 4 (Lexicon Generators): 3-4 hours
- Phase 5 (Orchestrator): 2-3 hours
- Phase 6 (Testing): 2-3 hours
- Phase 7 (CLI): 1-2 hours

**Total Project**: 20-27 hours

---

## Next Steps for New Session

1. **Load context**: Read this handoff document
2. **Verify state**: Run `pytest tests/ -v` (should see 137 passing)
3. **Review design**: Read implementation plan lines 224-420
4. **Install dependencies**: Add sentence-transformers to requirements.txt
5. **Start coding**: Begin with Task 3.2 (similarity utilities)
6. **Use TDD**: Write tests first, then implementation
7. **Track progress**: Use TodoWrite tool for each batch

---

## Session Handoff Checklist

- ✅ Phase 1 complete (55/55 tests passing)
- ✅ Phase 2 complete (82/82 tests passing)
- ✅ Total: 137/137 tests passing
- ✅ Multi-format extraction working
- ✅ Document classification functional
- ✅ State management with incremental processing
- ✅ Confidence scoring utilities ready
- ✅ All code documented and tested
- ✅ Ready for Phase 3

**Status**: Ready to begin Phase 3 - Analysis Modules

---

## Quick Reference: Phase 3 Modules

| Module | Purpose | Input | Output |
|--------|---------|-------|--------|
| `utils/similarity.py` | Semantic similarity & clustering | Text pairs, lists | Similarity scores, clusters |
| `analyzers/themes_analyzer.py` | Extract recurring themes from cover letters | Cover letter documents | Themes with chronological quotes |
| `analyzers/qualifications_analyzer.py` | Track position phrasing variations | Resume documents | Qualifications with phrasing history |
| `analyzers/narratives_analyzer.py` | Catalog storytelling patterns | Cover letter documents | Narrative patterns by category |
| `analyzers/keywords_analyzer.py` | Build keyword usage index | All documents | Keywords with usage contexts |

---

**Generated**: 2025-10-29
**By**: Claude (Sonnet 4.5)
**For**: Career Lexicon Builder Project
**Session**: Phase 2 → Phase 3 Transition
