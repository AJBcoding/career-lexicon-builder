# CV Style Extraction and Formatting Design

**Date:** 2025-11-09
**Status:** Design Complete - Ready for Implementation
**Goal:** Extract styles from .pages documents, create clean .docx templates, and build an intelligent formatting skill

---

## Background

The career-lexicon-builder project generates high-quality CV content through AI-powered analysis and Socratic career skills. The final formatting step—applying professional styles to this content—remains manual and error-prone.

**Current State:**
- CV source: `my_documents/AJB CV 2024.pages` with 97 styles (21 duplicates)
- iwork-converter successfully extracts styles and content
- Comprehensive style analysis completed

**Vision:**
Create clean templates with semantic style names, then build a Claude skill that intelligently formats CV content using semantic understanding.

---

## Key Design Decisions

### 1. Two-Phase Approach

**Phase 1: Template Creation (One-Time)**
- Python script extracts and consolidates styles
- Creates clean .docx template with 12 semantic styles
- Runs once or when updating templates

**Phase 2: Intelligent Formatting (Repeated Use)**
- Claude skill understands content semantically
- Applies styles based on context and meaning
- Learns from user corrections over time

**Rationale:** Separation of concerns—template creation is data extraction (no AI needed), formatting is semantic understanding (needs Claude).

### 2. Style Consolidation: 97 → 12

**Analysis Results:**
- Total styles in source: 97
- Actually used: 75
- Duplicates identified: 21
- Most used style: `ss2578` (bold italic) with 468 uses

**Core Style Set (12 styles):**

**Paragraph Styles (7):**
1. `CV Name` - Name at top (13pt Helvetica, potentially bold/orange)
2. `Section Header` - "EDUCATION", "PROFESSIONAL EXPERIENCE" (10pt Helvetica bold orange #FF6D49)
3. `Body Text` - Standard paragraphs (9pt Helvetica)
4. `Timeline Entry` - Date + institution with 72pt hanging indent
5. `Bullet Standard` - Regular bullet points
6. `Bullet Gray` - Bullets for dates/education (gray text)
7. `Bullet Emphasis` - Bold italic bullets for highlighted items

**Character Styles (5):**
8. `Play Title` - Bold italic for productions/plays
9. `Institution` - Bold for institution names
10. `Job Title` - Bold italic for job positions
11. `Orange Emphasis` - Bold orange for section emphasis
12. `Gray Text` - For dates and secondary info

**Rationale:** Based on actual usage analysis, these 12 styles cover 100% of formatting needs while eliminating duplication.

### 3. Semantic Understanding over Pattern Matching

**Problem:** Bold italic is used for both job titles AND play titles. Regex can't distinguish.

**Solution:** Claude analyzes semantic context:
- "2023 - Present ***Interim Associate Dean***" → Job Title (follows date range)
- "***Romeo & Juliet***" → Play Title (in production list context)

**Rationale:** Context matters. AI semantic understanding enables accurate style inference that regex cannot achieve.

### 4. Learning System

**Approach:** Automatic learning from conversational corrections

**Example:**
- User: "That committee role should be gray text, not body text"
- Skill: Updates `learned-preferences.yaml` with contextual rule
- Future: Automatically applies to similar content

**Storage:** `~/.claude/skills/career/format-resume/learned-preferences.yaml`

**Rationale:** Improves accuracy over time without manual configuration.

### 5. Visual Verification

**Workflow:**
1. Format document → .docx
2. Convert to PDF (LibreOffice)
3. Convert PDF to images (Poppler)
4. Display in conversation
5. User confirms or corrects

**Rationale:** High-stakes documents (job applications) require visual confidence, not just structural correctness.

---

## System Architecture

### Overall Flow

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Template Creation (One-Time Setup)                 │
└─────────────────────────────────────────────────────────────┘

AJB CV 2024.pages
    ↓
iwork-converter → /tmp/cv_output.html (CSS with style definitions)
    ↓
extract_and_build_template.py
    ↓
Analyzes HTML/CSS, consolidates 97 → 12 styles
    ↓
Creates cv-template.docx with python-docx
    ↓
Saves to ~/.claude/skills/career/format-resume/cv-template.docx

┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Document Formatting (Repeated Use)                 │
└─────────────────────────────────────────────────────────────┘

User: "Format this CV: [content]"
    ↓
format-resume skill (Claude semantic analysis)
    ↓
Identifies: sections, dates, institutions, titles, etc.
    ↓
Creates structured style mapping
    ↓
apply_styles.py (Python helper)
    ↓
Loads cv-template.docx, applies styles
    ↓
Generates formatted-cv.docx
    ↓
Converts to PDF → JPEG images
    ↓
Displays preview to user
    ↓
User confirms or requests corrections
    ↓
(if corrections) → Updates learned-preferences.yaml
```

---

## Detailed Component Specifications

### Component 1: Template Creation Script

**File:** `extract_and_build_template.py`

**Purpose:** One-time script to create clean .docx template from .pages source

**Process:**

1. **Extract Style Definitions**
   - Run iwork-converter on source .pages
   - Parse HTML/CSS output
   - Extract properties for each style class

2. **Consolidate Styles**
   - Use mapping dictionary (97 old → 12 new)
   - Merge duplicate styles
   - Assign semantic names

3. **Create Clean Template**
   - Use python-docx to create new document
   - Define 12 styles with extracted properties
   - Test style accessibility
   - Save template

**Style Consolidation Mapping:**

```python
STYLE_CONSOLIDATION = {
    # Character styles → semantic names
    'ss2578': 'Play Title',      # 468 uses - bold italic
    'ss2592': 'Job Title',        # 28 uses - bold italic
    'ss2508': 'Play Title',       # 22 uses - bold italic
    'ss2505': 'Institution',      # 48 uses - bold
    'ss93858': 'Institution',     # duplicate
    'ss2543': 'Institution',      # duplicate
    'ss2555': 'Orange Emphasis',  # 18 uses - bold orange
    'ss2561': 'Orange Emphasis',  # duplicate
    'ss2507': 'Gray Text',        # 5 uses - gray
    'ss40419': 'Gray Text',       # duplicate

    # Paragraph styles → semantic names
    'ps2539': 'Section Header',   # 19 uses - bold orange
    'ps2557': 'Section Header',   # duplicate with indent
    'ps2554': 'CV Name',          # Light intro text
    'ps81934': 'Body Text',       # 25 uses - standard
    'ps2548': 'Body Text',        # 85 uses - duplicate
    'ps2597': 'Body Text',        # 20 uses - duplicate
    'ps53936': 'Body Text',       # 57 uses - duplicate
    'ps8131': 'Body Text',        # duplicate
    'ps2532': 'Timeline Entry',   # 103 uses - gray with indent
    'ps81930': 'Timeline Entry',  # black variant
    'ps2541': 'Timeline Entry',   # plain variant

    # Bullet lists
    'ps40376': 'Bullet Standard', # 254 uses - most common
    'ps40524': 'Bullet Standard', # 79 uses - duplicate
    'ps40420': 'Bullet Standard', # duplicate
    'ps40357': 'Bullet Standard', # duplicate
    'ps2532': 'Bullet Gray',      # 103 uses - gray bullets
    'ps40350': 'Bullet Gray',     # duplicate
    'ps40465': 'Bullet Emphasis', # 16 uses - bold italic
    'ps46257': 'Bullet Emphasis', # 24 uses - duplicate
    'ps40394': 'Bullet Emphasis', # duplicate
}
```

**Output:** `cv-template.docx` with 12 clean, semantic styles

---

### Component 2: Style Application Helper

**File:** `apply_styles.py`

**Purpose:** Python helper that applies styles to content based on Claude's semantic analysis

**Interface:**

```python
def apply_styles_to_document(template_path, content_mapping, output_path):
    """
    Args:
        template_path: Path to cv-template.docx
        content_mapping: List of {line, style, reasoning} dicts
        output_path: Where to save formatted document

    Returns:
        success: bool, formatted document created
    """
    pass
```

**Example Content Mapping:**

```python
content_mapping = [
    {
        "line": "Anthony Byrnes",
        "style": "CV Name",
        "reasoning": "First line, short, proper name"
    },
    {
        "line": "EDUCATION",
        "style": "Section Header",
        "reasoning": "All caps, section divider"
    },
    {
        "line": "2023 - Present",
        "style": "Timeline Entry",
        "reasoning": "Date range pattern"
    },
    {
        "line": "California State University Long Beach",
        "style": "Institution",
        "inline": True,
        "reasoning": "Institution name after date"
    },
    # ... more
]
```

**Process:**
1. Load template document
2. For each line in mapping:
   - If inline: add run with character style
   - Else: add paragraph with paragraph style
3. Save formatted document

---

### Component 3: Format Resume Skill

**Location:** `~/.claude/skills/career/format-resume/`

**Files:**
```
format-resume/
├── skill.md                    # Main skill definition
├── cv-template.docx            # Clean template (from script)
├── apply_styles.py             # Style application helper
├── style-mappings.yaml         # Base semantic inference rules
└── learned-preferences.yaml    # User corrections (accumulated)
```

**Skill Workflow:**

1. **Input Detection**
   - Clipboard content
   - File path (.txt, .md, .docx)
   - Conversational specification

2. **Content Analysis**
   - Parse structure
   - Identify semantic elements
   - Create style mapping
   - Apply base rules + learned preferences

3. **Document Generation**
   - Call apply_styles.py
   - Generate .docx

4. **Visual Verification**
   - Convert to PDF (soffice)
   - Convert to images (pdftoppm)
   - Display in conversation

5. **User Review**
   - Confirm → save and exit
   - Correct → update mapping, regenerate
   - Learn → save correction to learned-preferences.yaml

**Semantic Inference Rules:**

```yaml
# style-mappings.yaml
patterns:
  - name: cv_name
    condition: "First line, ≤5 words, proper case, capitalized"
    style: "CV Name"

  - name: section_header
    condition: "ALL CAPS, short line, likely section divider"
    style: "Section Header"

  - name: timeline_entry
    condition: "Starts with date range (YYYY - YYYY or YYYY - Present)"
    style: "Timeline Entry"
    inline_styles:
      institution: "Institution"

  - name: job_title
    condition: "Follows institution line, italic markers or context"
    style: "Job Title"
    inline: true

  - name: play_title
    condition: "Italic text in production/work context"
    style: "Play Title"
    inline: true

  - name: bullet
    condition: "Starts with •, -, *, or detected list item"
    style: "Bullet Standard"
```

**Learning System:**

```yaml
# learned-preferences.yaml (example after corrections)
version: 1.0
last_updated: "2025-11-09T18:30:00"

rules:
  - id: "committee_roles_gray"
    pattern: "committee|advisory"
    context: "appears under service section or as secondary role"
    preferred_style: "Gray Text"
    learned_date: "2025-11-09"
    example: "Graduate Studies Advisory Committee"
    correction_count: 1

  - id: "course_names_small"
    pattern: "course titles in list"
    context: "teaching section with multiple courses"
    preferred_style: "Gray Text"
    learned_date: "2025-11-09"
    correction_count: 2
```

---

## Technology Stack

**Core Libraries:**
- `python-docx` - Document creation and style application
- `BeautifulSoup4` - HTML/CSS parsing
- `LibreOffice (soffice)` - PDF conversion
- `Poppler (pdftoppm)` - PDF to image conversion

**Why python-docx:**
- Templates use only paragraph and character styles (confirmed by analysis)
- No tables, text boxes, or multi-column layouts
- Full support for all required features
- Simpler than Document library (XML manipulation)

**System Requirements:**
- Python 3.8+
- LibreOffice installed (`soffice` command)
- Poppler installed (`pdftoppm` command)

---

## Implementation Plan

### Phase 1: Template Creation (2-3 hours)

**Tasks:**
1. Write `extract_and_build_template.py`
   - Parse iwork-converter HTML/CSS
   - Implement style consolidation mapping
   - Create template with python-docx
   - Validate all 12 styles accessible
2. Run script on `AJB CV 2024.pages`
3. Test template by manually applying styles
4. Verify visual match with original

**Deliverable:** `cv-template.docx` with 12 semantic styles

**Validation:**
- All 12 styles present and named correctly
- Style properties match original (fonts, colors, spacing)
- Can open template in Word/LibreOffice
- python-docx can access all styles

---

### Phase 2: Basic Formatting (3-4 hours)

**Tasks:**
1. Write `apply_styles.py` helper
   - Template loading
   - Style mapping input processing
   - Style application (paragraph and inline)
   - Document saving
2. Create test content with manual style mapping
3. Verify formatted output matches expected
4. Test edge cases (empty lines, special characters)

**Deliverable:** Working Python formatter

**Validation:**
- Can format simple CV from style mapping
- Paragraph styles apply correctly
- Inline character styles work
- Output visually matches expectations

---

### Phase 3: Claude Skill (4-5 hours)

**Tasks:**
1. Write `skill.md` for format-resume
2. Implement semantic analysis workflow
   - Content parsing
   - Element identification
   - Style mapping generation
3. Connect to `apply_styles.py`
4. Add error handling and user feedback
5. Test end-to-end with real CV content

**Deliverable:** Working skill (basic version)

**Validation:**
- Skill correctly identifies 90%+ of elements
- Can format CV from plain text in < 2 minutes
- Style application works correctly
- Error messages are helpful

---

### Phase 4: Visual Verification (1-2 hours)

**Tasks:**
1. Add PDF conversion (soffice command)
2. Add image generation (pdftoppm command)
3. Display images in conversation
4. Test iteration cycle (review → correct → regenerate)

**Deliverable:** Skill shows visual previews

**Validation:**
- PDF conversion works reliably
- Images display clearly in conversation
- Can iterate corrections quickly
- Visual preview matches final document

---

### Phase 5: Learning System (2-3 hours)

**Tasks:**
1. Implement correction detection
2. Generate learned preference rules
3. Save to `learned-preferences.yaml`
4. Apply learned rules on future runs
5. Add user notifications

**Deliverable:** Skill learns from corrections

**Validation:**
- Corrections are detected and saved
- Learned rules apply to new documents
- User sees notification of what was learned
- Preferences persist across sessions

---

**Total Estimated Time:** 12-17 hours

---

## Success Criteria

### Must Have (MVP):
- ✅ Template has exactly 12 styles with semantic names
- ✅ Template formatting matches original CV visually
- ✅ Skill correctly identifies 90%+ of elements semantically
- ✅ Can format new CV from plain text in < 2 minutes
- ✅ Visual preview shows formatted document
- ✅ Learning system saves and applies corrections
- ✅ No manual style application required

### Validation Tests:

**Test 1: Template Fidelity**
- Format actual CV using template
- Compare side-by-side with original .pages export
- Success: Visual match, all formatting preserved

**Test 2: Semantic Understanding**
- Provide plain text CV (no formatting hints)
- Check element identification accuracy
- Success: 90%+ correct on first pass

**Test 3: Learning Persistence**
- Correct style choice: "committee roles → gray text"
- Format different CV with committee roles
- Success: Automatically applies gray without prompting

**Test 4: Context Discrimination**
- Test bold italic in different contexts (job title vs play title)
- Verify skill uses surrounding context correctly
- Success: Distinguishes based on semantic context

**Test 5: Visual Accuracy**
- Format CV, review preview images
- Compare with manually formatted version
- Success: Preview matches final document appearance

---

## Future Enhancements

**Post-MVP Features:**

1. **Cover Letter Support**
   - Analyze if 12 core styles work for cover letters
   - Add 2-3 additional styles if needed
   - Create `format-cover-letter` skill variant

2. **Batch Processing**
   - Format multiple documents in sequence
   - Apply same preferences across batch

3. **Template Variants**
   - Academic vs corporate style variations
   - Easy switching between visual styles
   - Maintain content, change presentation

4. **Preference Management**
   - View all learned preferences
   - Edit/delete specific rules
   - Export/import preferences

5. **Integration with Career Lexicon Builder**
   - Automatic formatting after content generation
   - Seamless Socratic skills → formatted document flow

---

## Related Documents

**Previous Research:**
- `HANDOFF_PAGES_STYLE_EXTRACTION.md` - iwork-converter investigation
- `CV_STYLES_LIST.md` - Complete 97-style inventory
- `CV_DUPLICATE_STYLES.md` - Duplication analysis
- `docs/plans/2025-11-09-document-formatting-skills-design.md` - Original .docx formatting design

**Project Context:**
- `README.md` - Career lexicon builder overview
- `QUICKSTART_SOCRATIC_SKILLS.md` - Socratic skills usage

---

## Key Design Insights

### Why This Approach Works

1. **Separation of Concerns**
   - Template creation = data extraction (Python)
   - Formatting = semantic understanding (Claude)
   - Each tool does what it's best at

2. **Semantic Understanding is the Differentiator**
   - Traditional tools use regex/patterns
   - Claude understands context and meaning
   - Enables accurate style inference that regex cannot achieve

3. **Learning Makes It Personal**
   - Your CV style preferences are unique
   - System learns your decisions over time
   - Gets better with use, not more configuration

4. **Visual Verification Builds Confidence**
   - High-stakes documents need visual confirmation
   - Quick iteration: see → correct → see updated
   - Reduces anxiety about "is this right?"

5. **Clean Templates Enable Clean Skills**
   - 12 semantic styles vs 97 cryptic ones
   - Skill code is readable and maintainable
   - User understands what's happening

### Evolution from Original Concept

**Started with:** Document formatting skill using .docx templates

**Evolved to:** Style extraction → clean templates → intelligent formatting skill

**Key insight:** Need to solve the template problem first. Can't build an intelligent skill on messy foundations.

---

## Risks and Mitigations

### Risk 1: Template Fidelity
**Problem:** Created template might not match original formatting exactly
**Mitigation:**
- Side-by-side visual comparison testing
- Iterate on style properties until match is perfect
- Document any intentional differences

### Risk 2: Semantic Analysis Accuracy
**Problem:** Claude might misidentify elements
**Mitigation:**
- Always show interpretation before formatting
- Easy correction workflow
- Learning system improves over time
- User can provide explicit hints

### Risk 3: LibreOffice/Poppler Availability
**Problem:** PDF tools might not be installed
**Mitigation:**
- Check for tools on first run
- Provide clear installation instructions
- Graceful degradation (skip preview if unavailable)

### Risk 4: Learning System Conflicts
**Problem:** Learned rules might contradict each other
**Mitigation:**
- Show user which rule is being applied
- Rule specificity ordering (most specific wins)
- Allow preference editing/deletion

---

**End of Design Document**

*Created: 2025-11-09*
*Status: Validated and Ready for Implementation*
*Estimated Implementation Time: 12-17 hours across 5 phases*
