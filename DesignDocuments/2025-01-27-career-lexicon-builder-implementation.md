# Career Application Lexicon Builder - Implementation Plan

**Date**: 2025-01-27  
**Design Document**: [2025-01-27-career-lexicon-builder-design.md](2025-01-27-career-lexicon-builder-design.md)  
**Estimated Total Effort**: 20-25 hours

## Overview

This implementation plan breaks down the Career Application Lexicon Builder skill into concrete, sequenced tasks. The skill will analyze existing cover letters and resumes to build reusable reference lexicons organized by themes, qualifications, narratives, and keywords.

## Project Structure

```
~/.claude/skills/career-lexicon-builder/
├── SKILL.md                          # Main skill entry point
├── core/
│   ├── orchestrator.py               # Central coordinator
│   ├── document_processor.py         # Extraction and classification
│   ├── state_manager.py              # Manifest and cache handling
│   └── confidence_scorer.py          # Confidence calculation logic
├── analyzers/
│   ├── themes_analyzer.py            # Theme detection and clustering
│   ├── qualifications_analyzer.py    # Position/skill tracking
│   ├── narratives_analyzer.py        # Narrative structure detection
│   └── keywords_indexer.py           # Keyword extraction and mapping
├── generators/
│   ├── themes_lexicon_generator.py
│   ├── qualifications_lexicon_generator.py
│   ├── narratives_lexicon_generator.py
│   └── keywords_index_generator.py
├── utils/
│   ├── text_extraction.py            # .pages file extraction
│   ├── similarity.py                 # Semantic similarity utilities
│   └── date_parser.py                # Date extraction from filenames
├── templates/
│   ├── themes_template.md
│   ├── qualifications_template.md
│   ├── narratives_template.md
│   └── keywords_template.md
└── tests/
    ├── test_extraction.py
    ├── test_classification.py
    ├── test_analyzers.py
    └── test_integration.py
```

## Implementation Phases

### Phase 1: Foundation (4-5 hours)

**Goal**: Set up project structure and core utilities

#### Task 1.1: Create Skill Structure
**Effort**: 30 minutes  
**Dependencies**: None

- [ ] Create skill directory: `~/.claude/skills/career-lexicon-builder/`
- [ ] Create subdirectories: `core/`, `analyzers/`, `generators/`, `utils/`, `templates/`, `tests/`
- [ ] Create empty `__init__.py` files for Python package structure
- [ ] Create `SKILL.md` with frontmatter and basic overview

**Deliverable**: Basic directory structure in place

---

#### Task 1.2: Implement Date Parser Utility
**Effort**: 1 hour  
**Dependencies**: 1.1

Create `utils/date_parser.py`:

- [ ] Regex patterns for date formats: `YYYY-MM-DD`, `YYYY-MM`, `MonthYYYY`
- [ ] Function: `extract_date_from_filename(filename) -> Optional[datetime.date]`
- [ ] Handle multiple date formats
- [ ] Return None if no date found
- [ ] Write unit tests for various filename patterns

**Test cases**:
- `2024-03-15-cover-letter.pages` → `2024-03-15`
- `2023-11-resume-company.pages` → `2023-11-01`
- `March2022-letter.pages` → `2022-03-01`
- `cover-letter.pages` → `None`

**Deliverable**: Working date parser with tests

---

#### Task 1.3: Implement Text Extraction from .pages Files
**Effort**: 2-3 hours  
**Dependencies**: 1.1

Create `utils/text_extraction.py`:

- [ ] Function: `extract_text_from_pages(filepath) -> dict`
  - Unzip .pages file (zipfile module)
  - Parse XML structure (xml.etree.ElementTree)
  - Extract text content
  - Preserve basic formatting markers (bold, bullets)
  - Return dict with text, formatting metadata, success status
  
- [ ] Handle extraction failures gracefully:
  - Return error info in dict
  - Log extraction method attempted
  
- [ ] Function: `extract_metadata(filepath, text) -> dict`
  - Extract target position/organization from text
  - Use date parser for date extraction
  - Return structured metadata

**Test cases**:
- Sample .pages file with text
- Sample .pages file with bullets and bold
- Corrupted .pages file (handle gracefully)

**Deliverable**: Text extraction utility with error handling

---

### Phase 2: Document Processing Pipeline (3-4 hours)

**Goal**: Build document ingestion, classification, and caching

#### Task 2.1: Implement Document Classifier
**Effort**: 1.5 hours  
**Dependencies**: 1.3

Create `core/document_processor.py`:

- [ ] Function: `classify_by_filename(filename) -> Optional[str]`
  - Regex patterns for "cover", "letter", "CV", "resume"
  - Return "cover_letter", "resume", or None
  
- [ ] Function: `classify_by_content(text) -> str`
  - Detect paragraph-based vs. bullet-heavy structure
  - Look for salutations (cover letter indicator)
  - Check for section headers like "Experience", "Education" (resume indicator)
  - Return "cover_letter", "resume", or "ambiguous"
  
- [ ] Function: `classify_document(filepath, text) -> str`
  - Try filename classification first
  - Fall back to content classification
  - Return classification with confidence note

**Test cases**:
- Cover letter with clear filename
- Resume with clear filename
- Generic filename requiring content analysis
- Ambiguous document

**Deliverable**: Document classifier with fallback logic

---

#### Task 2.2: Implement State Manager
**Effort**: 1.5 hours  
**Dependencies**: 1.1, 1.2

Create `core/state_manager.py`:

- [ ] Function: `load_manifest() -> dict`
  - Load `lexicons/processed-manifest.json`
  - Return empty dict if not exists
  
- [ ] Function: `save_manifest(manifest_data)`
  - Write manifest to JSON
  - Include timestamps, file hashes
  
- [ ] Function: `get_files_to_process(input_dir, manifest) -> list`
  - Compare input directory against manifest
  - Identify new files (not in manifest)
  - Identify modified files (different hash)
  - Return list of filepaths to process
  
- [ ] Function: `compute_file_hash(filepath) -> str`
  - Use hashlib to generate file hash
  - For change detection
  
- [ ] Function: `cache_document_data(doc_hash, data)`
  - Save extracted data to `lexicons/.cache/{hash}.json`
  
- [ ] Function: `load_cached_document(doc_hash) -> Optional[dict]`
  - Load cached data if exists
  - Return None if not in cache

**Deliverable**: State management with manifest and cache

---

#### Task 2.3: Integrate Document Processing Pipeline
**Effort**: 1 hour  
**Dependencies**: 2.1, 2.2

Update `core/document_processor.py`:

- [ ] Function: `process_document(filepath) -> dict`
  - Extract text (Task 1.3)
  - Classify document (Task 2.1)
  - Extract metadata (Task 1.3)
  - Return complete document dict
  
- [ ] Function: `process_documents_batch(filepaths) -> list`
  - Process multiple documents
  - Cache results
  - Handle failures gracefully
  - Return list of processed document dicts
  
- [ ] Function: `process_input_directory(input_dir, incremental=True) -> list`
  - Load manifest
  - Get files to process
  - Process documents
  - Update manifest
  - Return processed documents

**Test cases**:
- Process single document
- Process batch of mixed documents
- Incremental update (skip unchanged files)
- Full regeneration

**Deliverable**: Complete document processing pipeline

---

### Phase 3: Analysis Modules (8-10 hours)

**Goal**: Implement all four analysis modules

#### Task 3.1: Implement Confidence Scorer
**Effort**: 1 hour  
**Dependencies**: 1.1

Create `core/confidence_scorer.py`:

- [ ] Function: `calculate_confidence(pattern_data) -> float`
  - Implement frequency base scoring
  - Apply consistency adjustment (semantic similarity)
  - Apply temporal stability adjustment
  - Return score 0.0-1.0
  
- [ ] Function: `should_flag_for_review(confidence, threshold=0.75) -> bool`
  - Return True if confidence < threshold
  
- [ ] Function: `get_confidence_category(confidence) -> str`
  - Return "high", "medium", or "low"

**Deliverable**: Confidence scoring utility

---

#### Task 3.2: Implement Similarity Utilities
**Effort**: 1.5 hours  
**Dependencies**: 1.1

Create `utils/similarity.py`:

- [ ] Choose NLP library (spaCy recommended for balance of accuracy/simplicity)
- [ ] Install and configure chosen library
- [ ] Function: `calculate_semantic_similarity(text1, text2) -> float`
  - Use sentence embeddings
  - Calculate cosine similarity
  - Return score 0.0-1.0
  
- [ ] Function: `cluster_similar_items(items, threshold=0.7) -> list[list]`
  - Group items by semantic similarity
  - Use hierarchical or density-based clustering
  - Return clusters of similar items

**Note**: This is critical infrastructure for all analyzers

**Deliverable**: Semantic similarity and clustering utilities

---

#### Task 3.3: Implement Themes Analyzer
**Effort**: 2-3 hours  
**Dependencies**: 3.1, 3.2

Create `analyzers/themes_analyzer.py`:

- [ ] Function: `extract_candidate_themes(documents) -> list`
  - Identify values language patterns
  - Detect approach descriptions
  - Extract repeated concepts using similarity
  - Return candidate themes with quotes and sources
  
- [ ] Function: `cluster_themes(candidates) -> list`
  - Use similarity clustering (Task 3.2)
  - Determine natural granularity (aim for 10-20 themes)
  - Generate theme category names
  - Return theme clusters
  
- [ ] Function: `analyze_theme_evolution(theme_data) -> Optional[str]`
  - Analyze temporal patterns in theme usage
  - Detect changes in framing over time
  - Return evolution description or None
  
- [ ] Function: `score_theme_confidence(theme_data) -> float`
  - Use confidence scorer (Task 3.1)
  - Return confidence score
  
- [ ] Function: `generate_theme_entries(clusters, documents) -> list`
  - Create theme entry dicts
  - Include: name, summary, evolution, quotes, cross-refs
  - Return list of theme entries

**Deliverable**: Complete themes analyzer

---

#### Task 3.4: Implement Qualifications Analyzer
**Effort**: 2-3 hours  
**Dependencies**: 3.1, 3.2

Create `analyzers/qualifications_analyzer.py`:

- [ ] Function: `identify_positions(resume_documents) -> list`
  - Extract job titles, organizations, date ranges
  - Detect title variations
  - Group same position across resume versions
  - Return position data structures
  
- [ ] Function: `extract_bullet_variations(position, resume_docs) -> dict`
  - For each position, extract all bullet points used
  - Track which resume version used which bullet
  - Note rewording and emphasis differences
  - Return bullet variations with contexts
  
- [ ] Function: `analyze_contextual_patterns(position, variations) -> dict`
  - Identify emphasis patterns (teaching vs. research vs. management)
  - Detect skill clustering
  - Map accomplishments to application types
  - Return contextual analysis
  
- [ ] Function: `generate_position_entries(positions, documents) -> list`
  - Create position entry dicts
  - Include: title, summary, variations, contexts, skills, cross-refs
  - Return list of position entries

**Deliverable**: Complete qualifications analyzer

---

#### Task 3.5: Implement Narratives Analyzer
**Effort**: 2-3 hours  
**Dependencies**: 3.1, 3.2

Create `analyzers/narratives_analyzer.py`:

- [ ] Function: `identify_structural_patterns(cover_letters) -> dict`
  - Detect opening strategies
  - Identify development patterns
  - Recognize closing techniques
  - Analyze paragraph transitions
  - Return structural pattern data
  
- [ ] Function: `identify_rhetorical_devices(cover_letters) -> dict`
  - Extract metaphors and analogies
  - Detect parallelism and repetition
  - Identify framing devices
  - Recognize storytelling arcs
  - Return rhetorical device data
  
- [ ] Function: `analyze_language_patterns(cover_letters) -> dict`
  - Analyze sentence structure tendencies
  - Identify voice and tone indicators
  - Extract connective phrases
  - Return language pattern data
  
- [ ] Function: `cluster_narrative_elements(all_patterns) -> list`
  - Propose organizational scheme
  - Cluster by dimension or hybrid categories
  - Use frequency to determine categories
  - Return narrative clusters
  
- [ ] Function: `analyze_narrative_evolution(pattern_data) -> Optional[str]`
  - Track how approaches changed over time
  - Return evolution description or None
  
- [ ] Function: `generate_narrative_entries(clusters, documents) -> list`
  - Create narrative entry dicts
  - Include: name, summary, evolution, examples, usage notes, cross-refs
  - Return list of narrative entries

**Deliverable**: Complete narratives analyzer

---

#### Task 3.6: Implement Keywords Indexer
**Effort**: 2 hours  
**Dependencies**: 3.1, 3.2

Create `analyzers/keywords_indexer.py`:

- [ ] Function: `extract_keywords(documents) -> dict`
  - Extract technical skills and tools
  - Extract thematic/values keywords
  - Extract action language
  - Categorize keywords by type
  - Return keyword data with contexts
  
- [ ] Function: `build_keyword_mappings(keywords, theme_data, qual_data, narr_data) -> dict`
  - Link keywords to themes
  - Link keywords to qualifications
  - Link keywords to narratives
  - Track document citations
  - Identify synonym clusters
  - Return comprehensive keyword mappings
  
- [ ] Function: `identify_keyword_patterns(keywords, documents) -> dict`
  - Calculate co-occurrence networks
  - Identify job-type specificity
  - Analyze temporal trends
  - Return pattern analysis
  
- [ ] Function: `generate_keyword_entries(mappings, patterns) -> list`
  - Create keyword entry dicts
  - Include: category, frequency, associations, citations, trends
  - Return list of keyword entries

**Deliverable**: Complete keywords indexer

---

### Phase 4: Lexicon Generators (3-4 hours)

**Goal**: Generate markdown lexicons from analysis data

#### Task 4.1: Create Lexicon Templates
**Effort**: 1 hour  
**Dependencies**: None (can be done in parallel with Phase 3)

Create markdown templates in `templates/`:

- [ ] `themes_template.md` - Structure for themes lexicon
- [ ] `qualifications_template.md` - Structure for qualifications lexicon
- [ ] `narratives_template.md` - Structure for narratives lexicon
- [ ] `keywords_template.md` - Structure for keywords index

Each template should:
- Define section structure
- Include placeholder variables
- Show example formatting
- Document cross-reference syntax

**Deliverable**: Four lexicon templates

---

#### Task 4.2: Implement Themes Lexicon Generator
**Effort**: 45 minutes  
**Dependencies**: 3.3, 4.1

Create `generators/themes_lexicon_generator.py`:

- [ ] Function: `generate_themes_lexicon(theme_entries, output_path)`
  - Use template from Task 4.1
  - Generate overview with summary
  - Create theme category sections
  - Include summaries, evolution analysis, chronological quotes
  - Add cross-references with proper links
  - Write appendix with theme clusters
  - Save to output path

**Deliverable**: Themes lexicon generator

---

#### Task 4.3: Implement Qualifications Lexicon Generator
**Effort**: 45 minutes  
**Dependencies**: 3.4, 4.1

Create `generators/qualifications_lexicon_generator.py`:

- [ ] Function: `generate_qualifications_lexicon(position_entries, output_path)`
  - Use template from Task 4.1
  - Generate overview
  - Create position sections with all components
  - Add skills inventory summary
  - Include cross-references
  - Save to output path

**Deliverable**: Qualifications lexicon generator

---

#### Task 4.4: Implement Narratives Lexicon Generator
**Effort**: 45 minutes  
**Dependencies**: 3.5, 4.1

Create `generators/narratives_lexicon_generator.py`:

- [ ] Function: `generate_narratives_lexicon(narrative_entries, output_path)`
  - Use template from Task 4.1
  - Generate overview
  - Create sections for structural patterns, rhetorical devices, compositional patterns
  - Include language patterns section
  - Add appendix on narrative relationships
  - Include cross-references
  - Save to output path

**Deliverable**: Narratives lexicon generator

---

#### Task 4.5: Implement Keywords Index Generator
**Effort**: 45 minutes  
**Dependencies**: 3.6, 4.1

Create `generators/keywords_index_generator.py`:

- [ ] Function: `generate_keywords_index(keyword_entries, patterns, output_path)`
  - Use template from Task 4.1
  - Generate overview
  - Create sections by keyword category
  - Include co-occurrence networks
  - Add job-type and temporal trend sections
  - Generate alphabetical master index
  - Include cross-references
  - Save to output path

**Deliverable**: Keywords index generator

---

### Phase 5: Orchestration and Integration (3-4 hours)

**Goal**: Coordinate all components and implement review workflow

#### Task 5.1: Implement Central Orchestrator
**Effort**: 2 hours  
**Dependencies**: All Phase 2, 3, and 4 tasks

Create `core/orchestrator.py`:

- [ ] Function: `run_analysis(input_dir, incremental=True, skip_review=False)`
  - Main entry point for skill
  - Process documents (Phase 2)
  - Run all analyzers (Phase 3)
  - Collect analysis results
  - Generate review file if needed
  - Return analysis data
  
- [ ] Function: `generate_lexicons(analysis_data, output_dir)`
  - Call all lexicon generators (Phase 4)
  - Write lexicons to output directory
  - Log generation completion
  
- [ ] Function: `incremental_update(input_dir, existing_lexicons)`
  - Load existing lexicon data
  - Process only new/modified documents
  - Merge new analysis with existing
  - Regenerate lexicons with merged data
  
- [ ] Function: `full_regeneration(input_dir)`
  - Clear cache
  - Process all documents fresh
  - Generate lexicons from scratch

**Deliverable**: Complete orchestration logic

---

#### Task 5.2: Implement Review Workflow
**Effort**: 1.5 hours  
**Dependencies**: 5.1

Update `core/orchestrator.py`:

- [ ] Function: `generate_review_file(flagged_items, output_path)`
  - Create `lexicons/.review/flagged-items.md`
  - Format medium-confidence items with checkboxes
  - Include examples and questions
  - Provide options for user decisions
  
- [ ] Function: `parse_review_decisions(review_file_path) -> dict`
  - Read review file
  - Parse user checkbox selections
  - Extract merge/rename decisions
  - Return decisions dict
  
- [ ] Function: `apply_review_decisions(analysis_data, decisions) -> analysis_data`
  - Incorporate user decisions
  - Merge categories as specified
  - Rename categories as specified
  - Exclude flagged items as specified
  - Return updated analysis data
  
- [ ] Update `run_analysis()` to:
  - Generate review file
  - If not `skip_review`, pause and wait for user review
  - Parse review decisions
  - Apply decisions to analysis data
  - Continue with lexicon generation

**Deliverable**: Review workflow implementation

---

#### Task 5.3: Create SKILL.md Entry Point
**Effort**: 30 minutes  
**Dependencies**: 5.1, 5.2

Update `SKILL.md`:

- [ ] Write comprehensive frontmatter (name, description)
- [ ] Document usage instructions
- [ ] Explain incremental vs. regeneration modes
- [ ] Describe review workflow
- [ ] Provide examples of running the skill
- [ ] Document expected outputs
- [ ] Include troubleshooting section

**Deliverable**: Complete skill documentation

---

### Phase 6: Testing and Refinement (3-4 hours)

**Goal**: Ensure quality and reliability

#### Task 6.1: Unit Tests
**Effort**: 1.5 hours  
**Dependencies**: All implementation tasks

Create test files in `tests/`:

- [ ] `test_extraction.py` - Test text extraction and date parsing
- [ ] `test_classification.py` - Test document classification
- [ ] `test_confidence.py` - Test confidence scoring
- [ ] `test_similarity.py` - Test semantic similarity
- [ ] `test_themes.py` - Test themes analyzer
- [ ] `test_qualifications.py` - Test qualifications analyzer
- [ ] `test_narratives.py` - Test narratives analyzer
- [ ] `test_keywords.py` - Test keywords indexer

Each test file should:
- Cover main functions
- Test edge cases
- Verify error handling

**Deliverable**: Comprehensive unit test suite

---

#### Task 6.2: Integration Testing
**Effort**: 1 hour  
**Dependencies**: 6.1

Create `tests/test_integration.py`:

- [ ] Test end-to-end pipeline with sample documents
- [ ] Verify incremental updates work correctly
- [ ] Test full regeneration
- [ ] Verify lexicon output format
- [ ] Test review workflow
- [ ] Verify cross-references are valid

**Deliverable**: Integration test suite

---

#### Task 6.3: Manual Testing with Real Documents
**Effort**: 1 hour  
**Dependencies**: 5.3

- [ ] Prepare test set of real .pages files (cover letters and resumes)
- [ ] Run skill on test set
- [ ] Review generated lexicons for quality
- [ ] Verify categorizations make sense
- [ ] Check cross-references work
- [ ] Test review workflow
- [ ] Identify and fix any issues

**Deliverable**: Validated skill with real data

---

#### Task 6.4: Performance Optimization
**Effort**: 30 minutes  
**Dependencies**: 6.3

- [ ] Profile analysis for bottlenecks
- [ ] Optimize slow operations
- [ ] Ensure reasonable performance for 30+ documents
- [ ] Add progress indicators for long operations
- [ ] Test incremental update performance

**Deliverable**: Performant implementation

---

### Phase 7: Documentation and Deployment (1-2 hours)

**Goal**: Finalize and deploy

#### Task 7.1: Create User Guide
**Effort**: 1 hour  
**Dependencies**: 6.4

Create `README.md` in skill directory:

- [ ] Overview of skill purpose and capabilities
- [ ] Installation instructions (dependencies)
- [ ] Quick start guide
- [ ] Detailed usage examples
- [ ] Review workflow explanation
- [ ] Troubleshooting guide
- [ ] FAQ section

**Deliverable**: User documentation

---

#### Task 7.2: Final Polish
**Effort**: 30 minutes  
**Dependencies**: 7.1

- [ ] Code cleanup and formatting
- [ ] Add docstrings to all functions
- [ ] Ensure consistent error messages
- [ ] Verify all cross-references work
- [ ] Final testing pass

**Deliverable**: Production-ready skill

---

#### Task 7.3: Deploy and Validate
**Effort**: 30 minutes  
**Dependencies**: 7.2

- [ ] Deploy to `~/.claude/skills/career-lexicon-builder/`
- [ ] Run on real document collection
- [ ] Verify outputs meet expectations
- [ ] Create initial lexicons
- [ ] Document any issues for future enhancement

**Deliverable**: Deployed, functional skill

---

## Task Dependency Graph

```
Phase 1: Foundation
├── 1.1 Create Structure
├── 1.2 Date Parser (← 1.1)
└── 1.3 Text Extraction (← 1.1)

Phase 2: Document Processing
├── 2.1 Classifier (← 1.3)
├── 2.2 State Manager (← 1.1, 1.2)
└── 2.3 Integration (← 2.1, 2.2)

Phase 3: Analysis Modules
├── 3.1 Confidence Scorer (← 1.1)
├── 3.2 Similarity Utils (← 1.1)
├── 3.3 Themes Analyzer (← 3.1, 3.2)
├── 3.4 Qualifications Analyzer (← 3.1, 3.2)
├── 3.5 Narratives Analyzer (← 3.1, 3.2)
└── 3.6 Keywords Indexer (← 3.1, 3.2)

Phase 4: Lexicon Generators
├── 4.1 Templates (parallel)
├── 4.2 Themes Generator (← 3.3, 4.1)
├── 4.3 Qualifications Generator (← 3.4, 4.1)
├── 4.4 Narratives Generator (← 3.5, 4.1)
└── 4.5 Keywords Generator (← 3.6, 4.1)

Phase 5: Orchestration
├── 5.1 Orchestrator (← Phase 2, 3, 4)
├── 5.2 Review Workflow (← 5.1)
└── 5.3 SKILL.md (← 5.1, 5.2)

Phase 6: Testing
├── 6.1 Unit Tests (← all implementation)
├── 6.2 Integration Tests (← 6.1)
├── 6.3 Manual Testing (← 5.3)
└── 6.4 Performance (← 6.3)

Phase 7: Documentation
├── 7.1 User Guide (← 6.4)
├── 7.2 Final Polish (← 7.1)
└── 7.3 Deploy (← 7.2)
```

## Implementation Timeline

### Week 1: Core Infrastructure (Phases 1-2)
- Days 1-2: Foundation and utilities
- Days 3-4: Document processing pipeline
- Day 5: Integration and testing

### Week 2: Analysis and Generation (Phases 3-4)
- Days 1-2: Confidence scoring and similarity utilities
- Days 3-4: Themes and qualifications analyzers
- Day 5: Narratives and keywords analyzers

### Week 3: Completion (Phases 5-7)
- Days 1-2: Lexicon generators and orchestration
- Days 3-4: Testing and refinement
- Day 5: Documentation and deployment

**Total: ~15 working days (3 weeks part-time or 2 weeks full-time)**

## Success Criteria

**Phase Completion Checklist**:
- [ ] All documents can be processed without errors
- [ ] Classification accuracy >90% for clear cases
- [ ] Themes analyzer produces meaningful categories (10-20)
- [ ] Qualifications analyzer tracks all position variations
- [ ] Narratives analyzer identifies structural patterns
- [ ] Keywords indexer creates comprehensive cross-references
- [ ] Lexicons generate with proper formatting
- [ ] Review workflow functions smoothly
- [ ] Incremental updates work correctly
- [ ] All tests pass
- [ ] Documentation complete

**Quality Metrics**:
- Unit test coverage >80%
- Integration tests cover all major workflows
- Performance: Process 30 documents in <5 minutes
- Manual review time: <10 minutes for typical flagged items

## Risk Management

**Identified Risks**:

1. **Text extraction from .pages files fails**
   - Mitigation: Fallback to manual conversion with clear instructions
   - Fallback: Support .docx/.pdf as alternative input formats

2. **Clustering produces too many/too few categories**
   - Mitigation: Make granularity tunable parameter
   - Fallback: Manual category refinement in review workflow

3. **Semantic similarity library performance issues**
   - Mitigation: Benchmark multiple libraries before choosing
   - Fallback: Simpler keyword-based similarity for large collections

4. **Review workflow too cumbersome**
   - Mitigation: Make review optional with `--skip-review` flag
   - Fallback: Provide web-based review interface (future enhancement)

5. **Cross-references break when categories renamed**
   - Mitigation: Use stable IDs internally, display names externally
   - Fallback: Regeneration fixes broken links

## Future Enhancements (Post-MVP)

**Phase 8: Advanced Features** (Not in initial implementation)
- Success tracking integration (track which materials led to interviews)
- Job description analysis integration (suggest relevant themes/narratives)
- Suggestion engine (recommend content for new applications)
- Visual network graphs of relationships
- Export to additional formats (PDF, searchable database)
- Web interface for review workflow

## Open Questions for Implementation

These will be resolved during implementation:

1. **NLP Library**: spaCy vs. sentence-transformers vs. alternatives?
   - Decision point: Task 3.2
   - Criteria: Accuracy, performance, ease of installation

2. **Clustering Algorithm**: K-means vs. hierarchical vs. DBSCAN?
   - Decision point: Task 3.2
   - Criteria: Result quality, robustness, parameter sensitivity

3. **Similarity Threshold**: What score constitutes "same theme"?
   - Decision point: Task 3.3
   - Criteria: Manual inspection of results, user feedback

4. **Category Naming**: Extractive vs. abstractive?
   - Decision point: Task 3.3
   - Criteria: Clarity, meaningfulness, consistency

5. **Review Interface**: Markdown with checkboxes vs. interactive CLI?
   - Decision point: Task 5.2
   - Criteria: User experience, implementation complexity

These decisions should be made through experimentation and user testing during implementation.

---

## Getting Started

**Prerequisites**:
- Python 3.8+
- NLP library (TBD in Task 3.2)
- Standard libraries: zipfile, xml.etree.ElementTree, json, hashlib

**First Steps**:
1. Begin with Phase 1, Task 1.1 (Create Structure)
2. Set up development environment
3. Install required dependencies
4. Proceed sequentially through tasks
5. Run tests after each phase
6. Document decisions and issues

**Questions During Implementation?**
- Refer to design document for context
- Make pragmatic decisions and document them
- Test frequently with real data
- Prioritize working over perfect

---

**Implementation Status**: 🔴 Not Started

**Next Action**: Begin Phase 1, Task 1.1 - Create Skill Structure
