# Career Application Lexicon Builder - Design Document

**Date**: 2025-01-27  
**Purpose**: Design a skill that analyzes existing cover letters and resumes to build reference lexicons for future application materials  
**Status**: Design Complete - Ready for Implementation

## Overview

This skill creates reusable reference lexicons from a large collection (30+) of existing career application materials. It processes Apple Pages documents (.pages), extracts and categorizes content, and generates organized markdown lexicons that serve as strategic resources for drafting future cover letters and resumes.

**Core principle**: Mine authentic past writing to create specific, quoted reference materials organized by theme, qualification, narrative strategy, and keyword - weighted toward recent writing while preserving historical context.

## Scope and Requirements

### Input Materials
- **Volume**: 30+ documents (large repository)
- **Format**: Apple Pages (.pages) files
- **Naming**: Consistently dated (e.g., "2024-01-15-cover-letter-company.pages")
- **Types**: Mix of cover letters and resumes/CVs

### Output Requirements
- Four separate lexicon documents (themes, qualifications, narratives, keywords)
- All three analysis dimensions equally important (thematic content, positioning/experience, narrative structures)
- Chronological organization (most recent first) without explicit recency weighting indicators
- Comprehensive keyword index covering skills, themes, and language patterns
- All information quoted specifically from existing writing (except summaries)

### Update Model
- Primary: Incremental updates (add new documents to existing lexicons)
- Secondary: Periodic regeneration (full re-analysis every 6-12 months)
- Storage: `lexicons/` directory with standardized filenames

## Architecture

### Modular Processor Design

Four independent analysis modules coordinated by central orchestrator:

1. **Themes Analyzer** - Identifies recurring values, approaches, and professional philosophies
2. **Qualifications Analyzer** - Tracks how roles, skills, and accomplishments have been positioned
3. **Narratives Analyzer** - Captures storytelling structures, metaphors, and rhetorical devices
4. **Keywords Indexer** - Creates comprehensive cross-reference of skills, themes, and language patterns

### Central Orchestrator Responsibilities

- Document ingestion and classification (cover letter vs. resume)
- Text extraction from .pages files with fallback mechanism
- State management (manifest + cache)
- Confidence scoring and human review flagging
- Lexicon generation and cross-referencing
- Incremental update coordination

### Hybrid State Management System

**Components**:
- `lexicons/processed-manifest.json` - Tracks which documents analyzed and when
- `lexicons/.cache/` - Stores extracted text and metadata from each document
- `lexicons/.review/` - Contains items flagged for human review

**Benefits**:
- Supports incremental updates (process only new/modified documents)
- Enables full regeneration (delete cache → re-analyze everything)
- Preserves processing state across sessions

## Document Processing Pipeline

### Phase 1: Discovery and Classification

**Two-stage classifier**:

1. **Filename analysis** (primary)
   - Regex patterns detect "cover", "letter", "CV", "resume" in filenames
   - Extract date from filename patterns: `YYYY-MM-DD`, `YYYY-MM`, `MonthYYYY`

2. **Content analysis** (fallback)
   - Structural heuristics identify document type:
     - Cover letters: Paragraph-based, salutation, narrative flow, < 2 pages
     - Resumes: Bullet-heavy, section headers (Experience, Education), tabular data
   
**Output**: Documents tagged as `cover_letter`, `resume`, or `ambiguous` (flagged for review)

### Phase 2: Text Extraction

**For each .pages file**:

1. **Attempt automated extraction**:
   - Unzip .pages archive (zip format internally)
   - Parse XML structure
   - Extract text with basic formatting markers (bold, bullets)

2. **On failure**:
   - Flag document in `lexicons/.review/needs-conversion/`
   - Provide instructions for manual export to .docx or PDF
   - User converts → re-run extraction

3. **Extract metadata**:
   - Date from filename or early content
   - Target position/company from filename or document content
   - Document structure markers

### Phase 3: Caching

**Cache structure** (`lexicons/.cache/{document-hash}.json`):

```json
{
  "filename": "2024-03-15-cover-letter-university-dean.pages",
  "type": "cover_letter",
  "date": "2024-03-15",
  "target_position": "Dean of Graduate Studies",
  "target_org": "University",
  "text": "...",
  "formatting": {
    "bold_spans": [...],
    "bullets": [...]
  },
  "metadata": {
    "extraction_date": "2025-01-27",
    "extraction_method": "automated",
    "file_hash": "..."
  }
}
```

**Purpose**: Enable incremental processing - unchanged files skipped; only new/modified documents analyzed

## Analysis Modules

### Module 1: Themes Analyzer

**Purpose**: Identify and categorize recurring professional values, approaches, and philosophies

**Process**:

1. **Extract candidate themes**
   - NLP analysis identifies repeated concepts using semantic similarity (not just keyword matching)
   - Detect values language: "committed to", "believe in", "driven by"
   - Identify approach descriptions: "I focus on", "my work emphasizes"

2. **Cluster into categories**
   - Group similar themes using semantic similarity scoring
   - Analyze co-occurrence patterns (themes appearing together)
   - Natural granularity detection - let data determine optimal number of categories (typically 10-20)
   - Skill proposes organizational scheme; user can refine in review

3. **Confidence scoring**
   - **High (0.8-1.0)**: Clear pattern, repeated 5+ documents, consistent framing
   - **Medium (0.5-0.8)**: Appears 2-4 times, some variation in expression
   - **Low (<0.5)**: Single occurrence or highly variable framing

4. **Generate theme entries**
   - Category name (auto-generated, reviewable)
   - Summary (synthesized description)
   - Evolution analysis (how theme changed over time, if pattern detected)
   - Chronological quotes with (Date, Position, Document) citations
   - Cross-references to related themes and keywords

**Review workflow**: High-confidence → auto-include; Low-confidence → flag in `lexicons/.review/flagged-items.md`

### Module 2: Qualifications Analyzer

**Purpose**: Track how each role, skill, and accomplishment has been positioned across different resumes/CVs

**Process**:

1. **Identify positions**
   - Extract all professional roles from resumes
   - Detect title variations ("Director of Communications" vs "Communications Director")
   - Group same position across multiple resume versions
   - Track organization names and date ranges

2. **Extract description variations**
   - Capture all bullet points ever used to describe each position
   - Document how bullets were reworded for different contexts
   - Track skills emphasized in each version
   - Note accomplishments included vs. omitted
   - Record quantitative metrics and their variations

3. **Contextual analysis**
   - Identify emphasis patterns: teaching vs. research vs. management
   - Detect skill clustering (e.g., "leadership + budget oversight" for admin roles)
   - Map accomplishments to application types (academic vs. corporate vs. nonprofit)
   - Track evolution in how same role described over time

4. **Generate position entries**
   - Position heading (canonical title, organization, dates)
   - Summary (core responsibilities synthesized across versions)
   - Bullet variations (chronologically organized, all phrasings)
   - Contextual notes (patterns in emphasis)
   - Skills inventory (all skills associated with role, with contexts)
   - Inclusion patterns (which resumes included/omitted role or details)

**Confidence scoring**:
- **High**: Position appears 3+ resume versions with consistent core narrative
- **Medium**: Position appears 1-2 times or with significant variation
- **Low**: Ambiguous mapping (unclear if same position or different role)

### Module 3: Narratives Analyzer

**Purpose**: Capture storytelling structures, metaphors, rhetorical devices, and compositional patterns from cover letters

**Process**:

1. **Identify narrative elements across multiple dimensions**

   **Structural patterns**:
   - Opening strategies (hook types: question, anecdote, mission alignment, bold statement)
   - Development patterns (chronological, thematic, problem-solution, comparison)
   - Closing techniques (forward-looking, reflection, call-to-action, values restatement)
   - Paragraph transitions and flow devices

   **Rhetorical devices**:
   - Metaphors and analogies ("building bridges", "weaving together")
   - Parallelism and repetition patterns
   - Framing devices (before/after, challenge/response)
   - Storytelling arcs (transformation, journey, alignment, growth)

   **Language patterns**:
   - Sentence structure tendencies (short/punchy vs. complex/developed)
   - Voice and tone indicators (formal, conversational, reflective)
   - Connective tissue ("This taught me", "I came to understand", "Through this work")

2. **Cluster into narrative categories**
   - Skill proposes organizational scheme based on detected patterns
   - May separate by dimension (Structure, Rhetoric, Language)
   - May identify hybrid categories (e.g., "Mission-Alignment Opening with Anecdote")
   - Uses pattern frequency to determine what merits separate category
   - User reviews and can refine categorization

3. **Evolution tracking**
   - Analyze how narrative approaches changed over time
   - Track metaphor usage patterns (increase/decrease)
   - Identify structural strategy shifts (e.g., more direct openings recently)
   - Correlate devices with application contexts (which worked where)

4. **Generate narrative entries**
   - Category name (e.g., "Problem-Solution Arc with Quantified Impact")
   - Summary (description of device/structure)
   - Evolution analysis (temporal patterns if detected)
   - Chronological examples (full quotes in context with citations)
   - Usage notes (when approach was used, potential applications)
   - Cross-references (related strategies, relevant themes)

**Confidence scoring**:
- **High**: Clear pattern used 3+ times, easily identifiable structure
- **Medium**: Pattern appears 2 times or hybrid approach mixing devices
- **Low**: Unique usage or unclear if intentional pattern vs. one-off phrasing

### Module 4: Keywords Indexer

**Purpose**: Create comprehensive cross-reference glossary linking keywords to themes, qualifications, narratives, and source documents

**Process**:

1. **Extract keyword candidates from three domains**

   **Technical skills and tools**:
   - Hard skills (programming languages, methodologies, certifications)
   - Tools and platforms (software, systems)
   - Functional areas (budget management, curriculum development)

   **Thematic/values keywords**:
   - Values terminology (equity, innovation, collaboration)
   - Approach descriptors (data-driven, community-centered, strategic)
   - Mission language (access, impact, excellence)

   **Action language**:
   - Action verbs (spearheaded, facilitated, transformed)
   - Descriptive phrases (cross-functional leadership, stakeholder engagement)
   - Impact language (increased by X%, reduced timeline, expanded reach)

2. **Build keyword mappings** - For each keyword create:
   - Frequency analysis (how often, in which document types)
   - Theme associations (which themes this keyword relates to)
   - Qualification links (which positions/roles used this keyword)
   - Narrative contexts (which narrative structures featured this language)
   - Document citations (specific usage with Date, Position, Context)
   - Synonym clusters (related terms used interchangeably)

3. **Identify keyword patterns**
   - Co-occurrence networks (keywords appearing together)
   - Job-type specificity (academic vs. corporate vs. nonprofit)
   - Temporal trends (more/less usage in recent applications)
   - High-value keywords (those in successful applications - if success data available)

4. **Generate index structure**
   - Keyword entries with category, frequency, associations
   - Co-occurrence cluster analysis
   - Keyword applications by job type
   - Temporal trends (increasing/decreasing/stable usage)
   - Alphabetical master index for quick lookup

## Confidence Scoring and Review System

### Confidence Score Calculation

**Formula components** (final score 0.0-1.0):

1. **Frequency base**:
   - 1 occurrence: 0.2 base
   - 2 occurrences: 0.5 base
   - 3-4 occurrences: 0.7 base
   - 5+ occurrences: 0.9 base

2. **Consistency adjustment**:
   - High semantic similarity (>0.8): +0.1 bonus
   - Medium similarity (0.5-0.8): no adjustment
   - Low similarity (<0.5): -0.1 penalty

3. **Temporal stability**:
   - Used in last 2 years: +0.05 bonus
   - Used consistently across entire timeline: +0.05 bonus
   - Only in older documents (>3 years): -0.05 penalty

### Review Thresholds

- **Confidence ≥ 0.75**: Auto-include in lexicon (high confidence)
- **0.4 ≤ Confidence < 0.75**: Flag for review (medium confidence)
- **Confidence < 0.4**: Flag for review or auto-exclude based on preference (low confidence)

### Review Workflow

1. **Skill generates** `lexicons/.review/flagged-items.md` with:
   - Medium-confidence items with checkboxes for user decisions
   - Low-confidence items for inclusion/exclusion decisions
   - Proposed category names for user approval/modification

2. **User reviews** and marks decisions:
   - Include as-is
   - Merge with another category
   - Rename/reframe
   - Exclude

3. **Skill incorporates** decisions into final lexicons

4. **Review file preserved** for reference in future updates

## Lexicon Output Structure

### Output Location and Naming

All lexicons stored in: `lexicons/`

**Primary documents**:
- `themes-lexicon.md`
- `qualifications-lexicon.md`
- `narratives-lexicon.md`
- `keywords-index.md`

**Supporting files**:
- `.cache/` - Extracted document data
- `.review/` - Items needing review
- `processed-manifest.json` - Processing state

### Lexicon Format Standards

**All lexicons follow consistent structure**:

1. **Header section**:
   - Title
   - Generation date and document count
   - Overview with auto-generated summary

2. **Main content**:
   - Category/entry headings
   - Summary for each entry
   - Evolution analysis (when applicable)
   - Chronological examples with full citations
   - Cross-references

3. **Supporting sections**:
   - Appendices (clusters, relationships, trends)
   - Indexes (where applicable)

**Citation format** (used throughout):
```
**YYYY-MM-DD | Position Title | Organization Type**
> "[Full quote from document]"
```

### 1. Themes Lexicon Structure

```markdown
# Cover Letter Themes Lexicon
*Generated: [Date] | Documents analyzed: [N]*

## Overview
[Auto-generated summary of major themes and patterns across date range]

---

## [Theme Category Name]

**Summary**: [2-3 sentence description of theme and usage]

**Evolution**: [How theme changed over time - omitted if no clear pattern]

### Chronological Usage

**2024-03-15 | Dean of Graduate Studies | University**
> "[Full quote demonstrating this theme]"

**2023-11-08 | Director of Programs | Nonprofit**
> "[Full quote demonstrating this theme]"

**Cross-references**: 
- Related themes: [[Theme A]], [[Theme B]]
- Key skills: [[keyword]], [[keyword]]
- Narrative structures: [[Structure A]], [[Structure B]]

---

[Additional theme entries...]

## Appendix: Theme Clusters
[Visualization or description of theme relationships]
```

### 2. Qualifications Lexicon Structure

```markdown
# Resume and CV Qualifications Lexicon
*Generated: [Date] | Documents analyzed: [N]*

## Overview
[Summary of how roles/skills positioned across documents]

---

## [Position Title] | [Organization] | [Date Range]

**Summary**: [Core responsibilities synthesized across versions]

### Title Variations
- "Director of Communications" (2023-2024 resumes)
- "Communications Director" (2022 resumes)

### Bullet Point Variations

#### [Thematic Grouping - e.g., Leadership and Management]

**Version 1 (2024-03)**: "[Full bullet point text]"
**Version 2 (2023-11)**: "[Alternative phrasing]"
**Version 3 (2023-06)**: "[Another variation]"

**Context notes**: [Patterns in when each version used]

### Skills Associated with This Role
*High frequency*: [skills]
*Medium frequency*: [skills]
*Context-specific*: [skill] emphasized in [context]

### Inclusion Patterns
- Included in: [Which resumes]
- Emphasized heavily in: [Application types]
- De-emphasized in: [Application types]

### Accomplishments Inventory

**"[Accomplishment statement]"**
- Used in: [Dates/contexts]
- Variations: [Alternative phrasings]
- Context: [When included/emphasized]

**Cross-references**:
- Themes: [[Theme A]], [[Theme B]]
- Keywords: [[keyword]], [[keyword]]

---

[Additional position entries...]

## Skills Inventory Summary
[Comprehensive list of all skills with frequency and contexts]
```

### 3. Narratives Lexicon Structure

```markdown
# Cover Letter Narratives and Structures Lexicon
*Generated: [Date] | Documents analyzed: [N]*

## Overview
[Summary of storytelling patterns across documents]

---

## STRUCTURAL PATTERNS

### [Opening Strategy Name]

**Summary**: [Description of how strategy works]

**Evolution**: [How usage changed over time]

### Examples

**2024-03-15 | Dean of Graduate Studies | University**
> "[Full opening paragraph]"

**Analysis**: [What makes this example work, context]

**Usage notes**: [When this strategy works best]

**Cross-references**:
- Related structures: [[Structure A]]
- Themes employed: [[Theme A]]
- Keywords: [[keyword]]

---

## RHETORICAL DEVICES

### [Metaphor/Device Name]

**Summary**: [Description of device and function]

### Examples

**2023-06-22 | Senior Manager | Corporation**
> "[Full quote showing device in context]"

**Analysis**: [How device functions, effect]

**Usage notes**: [When to use, when to avoid]

**Cross-references**: [Related devices, contexts]

---

## COMPOSITIONAL PATTERNS

### [Development Pattern Name]

**Summary**: [How body develops argument/narrative]

### Examples

**2024-03-15 | Dean of Graduate Studies | University**

**Structure breakdown**:
- Para 1: [Function]
- Para 2: [Function]
- Para 3: [Function]

**Full text**: [Relevant paragraphs quoted]

**Usage notes**: [When this structure works, variations]

---

## LANGUAGE PATTERNS

### Sentence Structure Tendencies
[Analysis of sentence length, rhythm patterns over time]

### Voice and Tone Indicators
[Examples by tone type with citations]

### Connective Phrases
[Commonly used transition/connection phrases with citations]

---

## Appendix: Narrative Device Relationships
[How elements work together]
```

### 4. Keywords Index Structure

```markdown
# Keywords and Cross-Reference Index
*Generated: [Date] | Documents analyzed: [N]*

## Overview
[Summary of keyword coverage and patterns]

---

## TECHNICAL SKILLS AND TOOLS

### [Keyword]

**Category**: Technical Skill
**Frequency**: [N] mentions across [M] documents
**Document types**: [Distribution]
**Temporal trend**: [Pattern description]

**Recent usage (last 3)**:
1. [Date | Position | Doc Type]
   > "[Quote showing usage]"

**Associated themes**: [[Theme A]]
**Used in positions**: [[Position A]]
**Narrative contexts**: [[Narrative A]]

**Related keywords**: [Synonyms, related terms]
**Co-occurs with**: [Frequently paired keywords]

**All citations**: [Complete chronological list]

---

## THEMATIC AND VALUES KEYWORDS

[Same structure as Technical Skills]

---

## ACTION LANGUAGE

[Same structure focusing on verbs/phrases]

---

## KEYWORD CO-OCCURRENCE NETWORKS

### High Co-Occurrence Clusters
[Keyword sets appearing together with contexts]

---

## KEYWORD APPLICATIONS BY JOB TYPE

### Academic Positions
[Most frequent keywords, distinctive keywords]

### Nonprofit Positions
[Most frequent keywords, distinctive keywords]

### Corporate Positions
[Most frequent keywords, distinctive keywords]

---

## TEMPORAL KEYWORD TRENDS

### Increasing Usage
[Keywords used more in recent applications]

### Decreasing Usage
[Keywords used less recently]

### Stable Keywords
[Consistently used keywords]

---

## ALPHABETICAL MASTER INDEX
[Quick-lookup index with section references]
```

## Incremental Update Workflow

### Adding New Documents

**Process**:

1. **Check manifest**: Compare input directory against `processed-manifest.json`
   - Identify new files (not in manifest)
   - Identify modified files (different timestamp/hash)
   - Skip unchanged files

2. **Process delta only**:
   - Extract text from new/modified documents
   - Run through classification and all analysis modules
   - Cache results in `.cache/`

3. **Merge with existing lexicons**:
   
   **Themes**:
   - Add new quotes to existing categories chronologically
   - Propose new themes (if confidence threshold met or flagged)
   - Update evolution analysis with new data points
   
   **Qualifications**:
   - Add new bullet variations to existing positions
   - Add new positions as separate entries
   - Expand skills inventory with new associations
   - Update contextual notes with new patterns
   
   **Narratives**:
   - Add new examples to existing categories
   - Propose new devices (if pattern detected or flagged)
   - Update evolution analysis
   
   **Keywords**:
   - Update frequency counts
   - Add new citations chronologically
   - Recalculate co-occurrence networks
   - Update temporal trends

4. **Update manifest**: Record processed files with timestamps

5. **Generate review file**: Flag any medium/low confidence items from new analysis

### Regeneration from Scratch

**When to regenerate**:
- Want to reorganize categories
- Apply new analysis logic
- Clean up accumulated inconsistencies
- Periodic refresh (every 6-12 months)

**Process**:
1. Delete `lexicons/.cache/` directory (or use `--regenerate` flag)
2. Skill processes all documents fresh
3. May identify new patterns based on corpus-wide analysis
4. Generates new lexicons with current categorization logic

### User Control Flags

- **Default mode**: Incremental (process only new/changed files)
- `--regenerate`: Process everything from scratch
- `--skip-review`: Auto-apply confidence thresholds without human review
- `--review-all`: Flag all items for review regardless of confidence

## Implementation Considerations

### Technical Requirements

**Text Extraction from .pages Files**:
- Python's `zipfile` module to unzip archive
- XML parsing (likely `xml.etree.ElementTree` or `lxml`)
- Text extraction logic from .pages XML structure
- Fallback handling for extraction failures

**NLP and Analysis**:
- Semantic similarity calculation (sentence transformers, spaCy, or similar)
- Clustering algorithms (k-means, hierarchical clustering, or density-based)
- Pattern detection (regex for some, ML for others)
- Co-occurrence network building (graph structures)

**State Management**:
- JSON for manifest and cache files
- File hashing for change detection
- Timestamp tracking
- Efficient merge algorithms for incremental updates

### Error Handling

**Document Processing Failures**:
- Log failed extractions to review file
- Provide clear instructions for manual conversion
- Continue processing other documents
- Re-attempt failed documents in subsequent runs

**Analysis Failures**:
- Graceful degradation (skip problematic analysis, continue others)
- Log errors with context for debugging
- Flag documents causing issues for review

**State Corruption**:
- Validate manifest/cache integrity on startup
- Offer rebuild option if corruption detected
- Backup previous lexicon versions before regeneration

### Performance Considerations

**For Large Document Sets (30+)**:
- Process documents in parallel where possible
- Cache aggressively to avoid reprocessing
- Incremental updates critical for performance
- Progress indicators for long-running operations

**Memory Management**:
- Don't load all documents into memory at once
- Stream processing where feasible
- Clear caches of processed documents
- Efficient data structures for co-occurrence networks

### Testing Strategy

**Test categories**:
1. Document extraction (various .pages file structures)
2. Classification accuracy (cover letters vs. resumes)
3. Confidence scoring (verify thresholds work as expected)
4. Incremental updates (merge logic correctness)
5. Regeneration (full corpus reprocessing)
6. Cross-referencing (link integrity)

**Test data needs**:
- Sample .pages files (both cover letters and resumes)
- Documents with various naming conventions
- Documents from different time periods
- Edge cases (ambiguous classification, extraction failures)

## Usage Patterns

### First-Time Setup

1. Organize all .pages files in input directory
2. Run skill with all documents
3. Review flagged items in `lexicons/.review/flagged-items.md`
4. Make decisions on category names, merges, exclusions
5. Skill generates final lexicons
6. Explore lexicons to verify quality

### Ongoing Use (Incremental Updates)

1. Add new cover letter or resume to input directory
2. Run skill (automatically detects new file)
3. Review any newly flagged items
4. Updated lexicons reflect new materials
5. Use updated lexicons for next application

### Periodic Refresh (Regeneration)

1. Run skill with `--regenerate` flag
2. Reconsider category organizations
3. Review newly proposed clusters
4. Fresh lexicons with current structure

### Using Lexicons for New Applications

**When drafting cover letter**:
1. Open `themes-lexicon.md` for values/approach language
2. Open `narratives-lexicon.md` for structural inspiration
3. Open `keywords-index.md` to ensure key terms included
4. Cross-reference between lexicons as needed

**When tailoring resume**:
1. Open `qualifications-lexicon.md` for position descriptions
2. Review bullet variations for target role
3. Check `keywords-index.md` for skills to emphasize
4. Consult contextual notes for application-type patterns

## Future Enhancements

**Potential additions** (not in initial design):
- Success tracking (which materials led to interviews/offers)
- Job-type auto-detection (academic vs. corporate vs. nonprofit)
- Automatic keyword extraction from new job descriptions
- Suggestion engine ("For this job posting, consider these themes...")
- Visual network graphs of keyword/theme relationships
- Version control integration for lexicon evolution
- Export formats (PDF, searchable database)

## Success Criteria

**Quality indicators**:
- Comprehensive coverage of all documents
- Accurate classification (cover letters vs. resumes)
- Meaningful categorization (not too granular or too broad)
- Useful cross-referencing (links provide value)
- Evolution analysis reveals actual patterns
- Incremental updates work smoothly
- Review workflow efficient and useful

**User satisfaction**:
- Lexicons save time when drafting new materials
- Categories feel intuitive and discoverable
- Quotes provide specific, reusable language
- Cross-references help find related content
- Confidence scoring reduces review burden
- Updates feel seamless

## Open Questions for Implementation

1. **NLP library choice**: Which library provides best balance of accuracy and simplicity?
2. **Clustering algorithm**: K-means vs. hierarchical vs. density-based for theme detection?
3. **Similarity threshold**: What semantic similarity score constitutes "same theme"?
4. **Category naming**: Use extractive (pull from documents) or abstractive (generate) names?
5. **Co-occurrence threshold**: How frequently must keywords co-occur to be considered a "cluster"?
6. **Review UI**: Command-line checklist vs. separate review tool vs. markdown with checkboxes?
7. **Performance target**: How fast should initial analysis be? (acceptable wait time)

These will be resolved during implementation based on testing and user feedback.

---

## Next Steps

1. **Create skill structure** in appropriate location
2. **Implement document processing pipeline** (extraction, classification, caching)
3. **Build analysis modules** one at a time (themes → qualifications → narratives → keywords)
4. **Develop confidence scoring** and review workflow
5. **Create lexicon generation** logic with templates
6. **Implement incremental update** mechanism
7. **Test with sample documents** and refine
8. **Deploy and iterate** based on real usage

**Design Status**: ✅ Complete and validated
