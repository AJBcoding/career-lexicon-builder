# Cover Letter Formatting System Design

**Date:** 2025-11-10
**Project:** Career Lexicon Builder - Cover Letter Support
**Status:** ✅ Design Complete - Ready for Implementation
**Related:** [System Extension Brainstorm Handoff](../HANDOFF_SYSTEM_EXTENSION_BRAINSTORM.md)

---

## Executive Summary

This document details the design for extending the Career Lexicon Builder's formatting system to support cover letters alongside CVs. The design follows a brainstorming session (Questions 1-10) and presentation of 8 validated design sections.

**Key Decisions:**
- Two separate skills: `format-resume` (existing) + new `format-cover-letter`
- Unified template with 13 styles (12 existing CV + 1 new Date Line)
- Minimal Python changes (add document type parameter, context-aware Section Headers)
- Shared infrastructure, skill-specific semantic understanding
- Document comparison and additional document types deferred to Phase 2

**Estimated Implementation Time:** 9-12 hours across 3 phases

---

## Design Validation: Questions & Answers

### Q1: Relationship Between CV and Cover Letter Formatting?
**Answer:** C - Unified document system
- One shared template contains styles for both document types
- Both skills leverage same Python infrastructure
- User note: "same styles - not sure if the source template should be different or not"

### Q2: Cover Letter Style Needs?
**Answer:** C - Academic context-aware (minimal new styles)
- Analysis of actual .pages files showed only 1 new style needed
- Cover letter thematic headers use black (not orange) Section Header variant
- Reuse all existing content styles (Play Title, Institution, Job Title)

### Q3: Document Detection Strategy?
**Answer:** B - User explicitly invokes skill (modified from auto-detection)
- User chooses: "Format this CV" vs "Format this cover letter"
- No complex auto-detection needed
- Intent is clear from skill invocation

### Q4: Template Structure?
**Answer:** A - Single unified template
- `~/.claude/skills/career/shared/career-documents-template.docx`
- Contains all 13 styles for both document types
- Single source of truth

### Q5: Section Header Handling?
**Answer:** C - Auto-detect header type via context
- Same "Section Header" style applies differently by document type
- CV: Orange (#FF6D49), 11pt Bold - domain headers (EDUCATION)
- Cover Letter: Black, 13pt Bold - thematic essay headers (Why UCLA?)

### Q6: Additional Cover Letter Style Needs?
**Answer:** A - Minimal approach (1 new style only)
- Only **Date Line** paragraph style needed (right-aligned, 11pt)
- All other elements reuse existing styles or Body Text
- Analysis showed orange style barely used in actual cover letters

### Q7: Document Comparison Tool Scope?
**Answer:** E - Minimal/Skip for now
- **Deferred to Phase 2** future development
- Focus current implementation on formatting only
- Future options: version tracking, requirement coverage, consistency checking

### Q8: Additional Document Types?
**Answer:** D - Just CV and Cover Letters
- **Deferred to future phase**
- Teaching statements, research statements, etc. flagged for later
- Current scope: CV and cover letter formatting only

### Q9: Skill Naming & Architecture?
**Answer:** D - Create separate `format-cover-letter` skill
- Two distinct skills with shared infrastructure
- User explicitly chooses which to invoke
- Helps with document type identification (user intent)
- More modular, easier to maintain independently

### Q10: Template Sharing Strategy?
**Answer:** A - Both skills reference same template file
- No serious drawbacks to shared template approach
- Single source of truth for styles
- `~/.claude/skills/career/shared/career-documents-template.docx`

---

## System Architecture

### Overview

**Two Separate Skills, Shared Infrastructure**

```
~/.claude/skills/career/
├── shared/
│   └── career-documents-template.docx    # 13 styles (12 CV + 1 Date Line)
├── format-resume/
│   ├── skill.md
│   ├── style-mappings.yaml               # CV semantic patterns
│   └── learned-preferences.yaml          # CV corrections
└── format-cover-letter/                  # NEW
    ├── skill.md
    ├── style-mappings.yaml               # Cover letter semantic patterns
    └── learned-preferences.yaml          # Cover letter corrections
```

**Python Module Structure (Existing)**

```
cv_formatting/
├── style_parser.py          # Unchanged
├── style_mapping.py         # Unchanged
├── template_builder.py      # Enhanced: Add Date Line style
├── style_applicator.py      # Enhanced: Document type parameter
├── pdf_converter.py         # Unchanged
└── image_generator.py       # Unchanged
```

### Key Architectural Principles

1. **Separation of Concerns:** Semantic understanding (Claude skill) vs mechanical application (Python)
2. **DRY:** Shared template and Python modules, skill-specific YAML configurations
3. **Explicit Intent:** User invocation determines document type, no auto-detection
4. **Backward Compatible:** All existing CV functionality unchanged
5. **Future-Proof:** Design accommodates additional document types in Phase 2

---

## Template Structure

### Unified Template: 13 Semantic Styles

**Location:** `~/.claude/skills/career/shared/career-documents-template.docx`

#### Existing 12 CV Styles (Unchanged)

**Paragraph Styles (7):**
1. **CV Name** - Name/header paragraph
2. **Section Header** - Bold headers (context-aware formatting)
3. **Body Text** - Standard content paragraphs
4. **Timeline Entry** - Dates with 72pt hanging indent
5. **Bullet Standard** - Standard bulleted lists
6. **Bullet Gray** - Secondary info bullets
7. **Bullet Emphasis** - Important bullets

**Character Styles (5):**
8. **Play Title** - Bold italic for artistic works (e.g., "Romeo & Juliet", "Kirk Douglas Theatre")
9. **Institution** - Bold for schools/employers (e.g., "UCLA", "Center Theatre Group")
10. **Job Title** - Bold italic for positions (e.g., "Associate Dean", "Interim Associate Dean")
11. **Orange Emphasis** - Bold orange (#FF6D49) for key highlights
12. **Gray Text** - Dates and secondary info

#### New Style Added

**Paragraph Style (1):**
13. **Date Line** - Right-aligned, 11pt Helvetica (e.g., "November 25, 2024")

### Section Header Context Awareness

The **Section Header** style applies differently by document type:

| Document Type | Color | Size | Weight | Use Case |
|--------------|-------|------|--------|----------|
| CV | Orange (#FF6D49) | 11pt | Bold | Domain headers: EDUCATION, EXPERIENCE, SKILLS |
| Cover Letter | Black | 13pt | Bold | Thematic essay headers: Why UCLA?, Enhancing Scholarship... |

**Implementation:** Python's `style_applicator.py` checks `--document-type` flag and applies appropriate formatting.

---

## Cover Letter Semantic Patterns

The `format-cover-letter` skill understands cover letter structure:

### Structural Elements (Paragraph-level)

| Element | Style Applied | Pattern/Example |
|---------|---------------|-----------------|
| Date Line | **Date Line** | Right-aligned date: "November 25, 2024" |
| Salutation | **Body Text** | "Dear Members of the UCLA School..." |
| Body Paragraphs | **Body Text** | All narrative content |
| Thematic Section Headers | **Section Header** (Black, 13pt) | "Why UCLA?", "Transformational Philanthropy" |
| Closing | **Body Text** | "Thank you for your time and attention," |
| Signature | **Body Text** | "Anthony Byrnes" |

### Content Elements (Character-level)

When mentioning achievements within body paragraphs:

| Content Type | Style Applied | Example |
|--------------|---------------|---------|
| Productions/Venues | **Play Title** | "Kirk Douglas Theatre", "Romeo & Juliet" |
| Organizations | **Institution** | "UCLA", "Center Theatre Group", "CSULB" |
| Positions | **Job Title** | "Associate Dean", "Interim Associate Dean" |
| Key Highlights | **Orange Emphasis** | Statistics, critical achievements |
| Dates/Secondary Info | **Gray Text** | Parenthetical dates |

### Example Semantic Application

Input text:
> "At Center Theatre Group, I stewarded the $18 million adaptive re-use of the Kirk Douglas Theatre where I nurtured over 100 new plays."

Styled output:
> "At **Center Theatre Group** [Institution], I stewarded the $18 million adaptive re-use of the **Kirk Douglas Theatre** [Play Title/Venue] where I nurtured over 100 new plays."

**Key Insight:** Cover letters reference the same content as CVs (productions, positions, institutions), so content styles are naturally reused.

---

## Skill Integration & Workflow

### User Invocation

```
User → Claude: "Format this cover letter: [content]"
        ↓
Claude invokes: format-cover-letter skill
        ↓
Skill analyzes content semantically
        ↓
Calls: python format_cv.py input.md output.docx --document-type=cover-letter --preview
        ↓
Visual preview displayed to user
```

### Format-Cover-Letter Workflow

**1. Content Analysis**
- Claude reads cover letter content
- Applies semantic understanding via `style-mappings.yaml`
- Identifies structural elements: date, salutation, headers, body, closing, signature
- Detects content mentions: productions, institutions, positions

**2. Style Application**
- Creates markdown with style annotations:
  ```markdown
  [Date Line]November 25, 2024[/Date Line]

  [Body Text]Dear Members of the UCLA School...[/Body Text]

  [Section Header]Why UCLA? Why TFT? Why now?[/Section Header]

  [Body Text]At [Institution]Center Theatre Group[/Institution]...[/Body Text]
  ```
- Calls Python `format_cv.py` script with `--document-type=cover-letter` flag
- Python applies styles from shared template with cover-letter-specific formatting
- Generates formatted `.docx`

**3. Visual Preview**
- Converts `.docx` → PDF (via LibreOffice)
- Converts PDF → images (via Poppler)
- Displays preview images to user for validation

**4. Learning Loop**
- User reviews and provides corrections
- Corrections saved to `~/.claude/skills/career/format-cover-letter/learned-preferences.yaml`
- Future formatting incorporates learned preferences per document type

### Shared vs Skill-Specific Components

| Component | Shared | format-resume | format-cover-letter |
|-----------|--------|---------------|---------------------|
| Template file | ✓ | | |
| Python modules | ✓ | | |
| skill.md | | ✓ | ✓ |
| style-mappings.yaml | | ✓ | ✓ |
| learned-preferences.yaml | | ✓ | ✓ |

---

## Python Module Changes

### 1. template_builder.py - Add Date Line Style

**File:** `cv_formatting/template_builder.py`

```python
def create_template(output_path):
    """Create .docx template with all 13 semantic styles."""

    # ... existing 12 styles ...

    # NEW: Add Date Line style
    date_line_style = template.styles.add_style('Date Line', WD_STYLE_TYPE.PARAGRAPH)
    date_line_style.font.name = 'Helvetica'
    date_line_style.font.size = Pt(11)
    date_line_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    template.save(output_path)
```

**Test:** `tests/test_template_builder.py::test_date_line_style_creation()`

### 2. style_applicator.py - Context-Aware Section Headers

**File:** `cv_formatting/style_applicator.py`

```python
def apply_styles(doc, content, document_type='cv'):
    """
    Apply semantic styles to content.

    Args:
        doc: python-docx Document object
        content: Markdown with style annotations
        document_type: 'cv' or 'cover-letter'
    """

    # ... existing style application logic ...

    if style_name == 'Section Header':
        if document_type == 'cv':
            # Orange, 11pt Bold (existing behavior)
            run.font.color.rgb = RGBColor(255, 109, 73)  # #FF6D49
            run.font.size = Pt(11)
        elif document_type == 'cover-letter':
            # Black, 13pt Bold (new behavior)
            run.font.color.rgb = RGBColor(0, 0, 0)
            run.font.size = Pt(13)
        run.font.bold = True
```

**Test:** `tests/test_style_applicator.py::test_section_header_cv_mode()`
**Test:** `tests/test_style_applicator.py::test_section_header_cover_letter_mode()`

### 3. format_cv.py - Add Document Type Flag

**File:** `format_cv.py`

```python
import argparse

parser = argparse.ArgumentParser(description='Format CV or cover letter')
parser.add_argument('input', help='Input markdown file')
parser.add_argument('output', help='Output .docx file')
parser.add_argument('--document-type',
                    choices=['cv', 'cover-letter'],
                    default='cv',
                    help='Type of document to format (default: cv)')
parser.add_argument('--preview',
                    action='store_true',
                    help='Generate PDF and image previews')

args = parser.parse_args()

# Pass document_type to style_applicator
apply_styles(doc, content, document_type=args.document_type)
```

**Backward Compatibility:** Default `--document-type=cv` maintains existing behavior.

### 4. generate_cv_template.py - Update for Shared Location

**File:** `generate_cv_template.py`

```python
from pathlib import Path

# OLD: output_path = Path.home() / '.claude/skills/career/format-resume/cv-template.docx'
# NEW:
output_path = Path.home() / '.claude/skills/career/shared/career-documents-template.docx'

# Ensure shared directory exists
output_path.parent.mkdir(parents=True, exist_ok=True)

create_template(output_path)
print(f"Template created at: {output_path}")
```

### 5. Unchanged Modules (Work As-Is)

- **style_parser.py** - HTML/CSS parsing logic unchanged
- **style_mapping.py** - Semantic mapping driven by YAML configs
- **pdf_converter.py** - Works for any .docx file
- **image_generator.py** - Works for any PDF file

---

## Testing Strategy

### Regression Tests (All Must Pass)

Existing 15 tests must continue passing after changes:

| Test File | Purpose | Count |
|-----------|---------|-------|
| `test_style_parser.py` | Template style extraction | 3 tests |
| `test_style_mapping.py` | Semantic style inference | 4 tests |
| `test_template_builder.py` | Template generation | 2 tests |
| `test_style_applicator.py` | Style application to content | 3 tests |
| `test_pdf_converter.py` | PDF generation (optional) | 2 tests (skipped if no LibreOffice) |
| `test_image_generator.py` | Image preview (optional) | 1 test (skipped if no Poppler) |

### New Cover Letter Tests

**Create:** `tests/test_cover_letter_formatting.py`

#### Test Suite Structure

```python
class TestCoverLetterFormatting:
    """Test cover letter specific formatting."""

    def test_date_line_style_exists(self):
        """Verify Date Line style in shared template."""

    def test_date_line_right_aligned(self):
        """Verify Date Line is right-aligned, 11pt Helvetica."""

    def test_section_header_cv_mode(self):
        """Verify Section Header in CV mode: Orange, 11pt."""

    def test_section_header_cover_letter_mode(self):
        """Verify Section Header in cover letter mode: Black, 13pt."""

    def test_cover_letter_structure_detection(self):
        """Test detection of: date, salutation, headers, body, closing."""

    def test_content_style_reuse(self):
        """Play titles, institutions, job titles styled correctly in cover letters."""

    def test_template_sharing(self):
        """Both skills can access shared template at correct path."""
```

#### Integration Tests

**Test 1: Real UCLA CAO Letter**
```python
def test_ucla_cao_cover_letter_formatting(self):
    """Format actual UCLA CAO v3 cover letter and validate."""
    input_md = Path('/tmp/cao-cover-letter-v3.md')
    output_docx = Path('/tmp/cao-cover-letter-formatted.docx')

    format_cover_letter(input_md, output_docx)

    # Validate:
    # - Date line right-aligned
    # - Section headers (Why UCLA?) in black, 13pt
    # - Institutions (UCLA, CSULB) styled correctly
    # - Body text properly formatted
```

**Test 2: Cross-Document Consistency**
```python
def test_cross_document_content_consistency(self):
    """Verify same content styled identically across CV and cover letter."""

    # Format CV with "Kirk Douglas Theatre"
    cv_doc = format_cv(cv_content)

    # Format cover letter mentioning "Kirk Douglas Theatre"
    cl_doc = format_cover_letter(cl_content)

    # Both should apply Play Title style (bold italic) to "Kirk Douglas Theatre"
    assert_same_style_applied(cv_doc, cl_doc, "Kirk Douglas Theatre")
```

### Template Validation Tests

**Create:** `tests/test_shared_template.py`

```python
def test_shared_template_exists():
    """Verify shared template at correct path."""
    template_path = Path.home() / '.claude/skills/career/shared/career-documents-template.docx'
    assert template_path.exists()

def test_shared_template_contains_13_styles():
    """Verify template contains all expected styles."""
    template = Document(template_path)
    style_names = [s.name for s in template.styles]

    expected_styles = [
        'CV Name', 'Section Header', 'Body Text', 'Timeline Entry',
        'Bullet Standard', 'Bullet Gray', 'Bullet Emphasis',
        'Play Title', 'Institution', 'Job Title', 'Orange Emphasis', 'Gray Text',
        'Date Line'  # NEW
    ]

    for style in expected_styles:
        assert style in style_names

def test_both_skills_can_load_template():
    """Verify format-resume and format-cover-letter can both access template."""
    # Test from CV perspective
    cv_template = load_template_for_cv()
    assert cv_template is not None

    # Test from cover letter perspective
    cl_template = load_template_for_cover_letter()
    assert cl_template is not None

    # Should be same file
    assert cv_template == cl_template
```

---

## Implementation Phases

### Phase 1: Shared Template Foundation (Est. 2-3 hours)

**Goal:** Create shared template infrastructure and migrate format-resume to use it.

#### Tasks

1. **Create Shared Directory Structure**
   ```bash
   mkdir -p ~/.claude/skills/career/shared
   ```

2. **Enhance Template Builder (TDD)**
   - Write test: `test_template_builder.py::test_date_line_style_creation()`
   - Implement: Add Date Line style to `template_builder.py`
   - Run test: Verify passes
   - Write test: `test_template_builder.py::test_template_contains_13_styles()`
   - Run test: Verify passes

3. **Generate New Shared Template**
   - Update `generate_cv_template.py` output path
   - Run: `python generate_cv_template.py`
   - Validate: Template created at `~/.claude/skills/career/shared/career-documents-template.docx`
   - Validate: Template contains 13 styles (use `validate_template.py` if exists)

4. **Update format-resume Skill**
   - Edit `~/.claude/skills/career/format-resume/skill.md`
   - Change template reference to shared location
   - Test: Run all existing CV tests
   - Validate: All 15 tests pass (regression)

5. **Visual Validation**
   - Format existing CV with updated skill
   - Compare output to previous version
   - Ensure no visual differences

**Acceptance Criteria:**
- ✓ Shared template exists with 13 styles
- ✓ format-resume uses shared template
- ✓ All existing CV tests pass
- ✓ CV visual output unchanged

---

### Phase 2: Python Cover Letter Support (Est. 3-4 hours)

**Goal:** Add document type parameter and context-aware formatting to Python modules.

#### Tasks

1. **Add Document Type Parameter (TDD)**
   - Write test: `test_format_cv_cli.py::test_document_type_flag()`
   - Implement: Update `format_cv.py` argparse with `--document-type` flag
   - Run test: Verify passes
   - Write test: `test_format_cv_cli.py::test_document_type_defaults_to_cv()`
   - Run test: Verify backward compatibility

2. **Implement Section Header Context Awareness (TDD)**
   - Write test: `test_style_applicator.py::test_section_header_cv_mode()`
     - CV mode → Orange (#FF6D49), 11pt Bold
   - Write test: `test_style_applicator.py::test_section_header_cover_letter_mode()`
     - Cover letter mode → Black, 13pt Bold
   - Implement: Update `style_applicator.py` with conditional formatting
   - Run tests: Verify both pass

3. **Create Cover Letter Test Fixtures**
   - Create `tests/fixtures/sample_cover_letter.md` with representative content:
     - Date line
     - Salutation
     - Body paragraphs mentioning institutions, positions, productions
     - Thematic section headers
     - Closing and signature
   - Create `tests/fixtures/expected_cover_letter_output.docx` (manually formatted reference)

4. **Integration Test Full Formatting Pipeline**
   - Write test: `test_cover_letter_formatting.py::test_full_cover_letter_formatting()`
   - Format sample cover letter with `--document-type=cover-letter`
   - Validate all styles applied correctly
   - Run test: Verify passes

5. **Regression Check**
   - Run all existing CV tests
   - Verify no regressions from changes

**Acceptance Criteria:**
- ✓ `--document-type` flag implemented
- ✓ Section Header context-aware formatting works
- ✓ Sample cover letter formats correctly
- ✓ All existing CV tests still pass

---

### Phase 3: Format-Cover-Letter Skill (Est. 4-5 hours)

**Goal:** Create format-cover-letter skill with semantic understanding and user-facing workflow.

#### Tasks

1. **Create Skill Directory Structure**
   ```bash
   mkdir -p ~/.claude/skills/career/format-cover-letter
   touch ~/.claude/skills/career/format-cover-letter/skill.md
   touch ~/.claude/skills/career/format-cover-letter/style-mappings.yaml
   touch ~/.claude/skills/career/format-cover-letter/learned-preferences.yaml
   ```

2. **Write skill.md**
   - Cover letter workflow description
   - How to invoke skill
   - What semantic patterns it understands
   - Integration with Python formatter
   - Visual preview workflow
   - Learning loop explanation
   - Examples with actual cover letter excerpts
   - Troubleshooting section

3. **Create style-mappings.yaml**

   **Structural Patterns:**
   ```yaml
   structural_patterns:
     date_line:
       pattern: "^(January|February|March|...) \\d{1,2}, \\d{4}$"
       style: "Date Line"
       context: "Right-aligned date at document start"

     salutation:
       pattern: "^Dear .+[,:]$"
       style: "Body Text"
       context: "Opening greeting"

     section_header:
       pattern: "^(Why .+\\?|Enhancing .+|Transformational .+|.+Infrastructure)$"
       style: "Section Header"
       context: "Thematic essay headers (Black, 13pt)"

     closing:
       pattern: "^(Thank you|Sincerely|Best regards|Warm regards).+[,]?$"
       style: "Body Text"
       context: "Closing phrase"
   ```

   **Content Patterns (Reused from CV):**
   ```yaml
   content_patterns:
     play_title:
       indicators:
         - Italic production/venue names
         - Theater/play titles referenced
         - Creative work titles
       examples:
         - "Kirk Douglas Theatre"
         - "Romeo & Juliet"
         - "Angels in America"

     institution:
       indicators:
         - University names
         - Organization names
         - Theater companies
       examples:
         - "UCLA"
         - "Center Theatre Group"
         - "CSULB"

     job_title:
       indicators:
         - Positions held or mentioned
         - Leadership roles
       examples:
         - "Associate Dean"
         - "Interim Associate Dean"
         - "Artistic Director"
   ```

4. **Integration Testing with Real Cover Letter**
   - Use actual UCLA CAO v3 cover letter as test case
   - Invoke format-cover-letter skill with content
   - Review formatted output
   - Validate:
     - Date line right-aligned
     - Salutation and body styled correctly
     - Thematic headers in black, 13pt
     - Institutions, positions, productions styled correctly
     - Closing and signature formatted properly
   - Generate PDF and image previews
   - Visual validation by user

5. **Refinement Based on Output**
   - Identify any misapplied styles
   - Update style-mappings.yaml patterns
   - Re-test with UCLA CAO letter
   - Iterate until output matches expectations

6. **Test with CSULB Cover Letter**
   - Format CSULB Associate Dean cover letter (second test case)
   - Validate consistency with UCLA letter styling
   - Ensure patterns generalize beyond single example

7. **Documentation**
   - Create or update `docs/guides/format-cover-letter-skill-guide.md`
   - Cover letter formatting workflow
   - Semantic pattern examples
   - Comparison to CV formatting
   - Troubleshooting common issues
   - FAQ section

**Acceptance Criteria:**
- ✓ format-cover-letter skill fully functional
- ✓ UCLA CAO letter formats correctly
- ✓ CSULB letter formats correctly
- ✓ Visual previews work
- ✓ Documentation complete
- ✓ User can successfully invoke and use skill

---

### Phase 4: Future Enhancements (Deferred)

**Not part of current implementation. Flagged for future development.**

#### Potential Phase 2 Features

**A. Document Comparison Tool**
- Version tracking & change analysis
- Requirement coverage analysis (job description → CV/cover letter)
- Consistency checker (cross-document validation)
- Holistic application review

**B. Additional Document Types**
- Teaching statements/philosophy
- Research statements
- Diversity/equity statements
- Artist statements
- Administrative philosophy statements

**C. Advanced Semantic Understanding**
- Auto-suggest improvements based on job description
- Tone/style consistency analysis
- Length optimization
- Keyword density analysis

**Decision:** Focus current effort on core CV + cover letter formatting. Assess Phase 2 needs after deployment and user feedback.

---

## Migration & Compatibility

### Backward Compatibility: Fully Maintained

**No Breaking Changes to format-resume Skill:**
- Same user-facing API
- Same semantic understanding
- Same visual output
- All existing learned preferences preserved
- All 15 existing tests must pass

### Template Migration Path

**Current State:**
- Template: `~/.claude/skills/career/format-resume/cv-template.docx`
- Contains 12 styles

**Target State:**
- Template: `~/.claude/skills/career/shared/career-documents-template.docx`
- Contains 13 styles (12 existing + Date Line)

**Migration Steps:**

1. **Phase 1 creates shared template** with 13 styles
2. **format-resume updated** to reference new shared path
3. **Old template remains** temporarily (can be deleted after validation)
4. **Validation:** Format existing CV, compare to previous output
5. **Cleanup:** Delete old template after confirming no regressions

### Learned Preferences: Independent by Skill

Each skill maintains separate learning files:

| File | Purpose | Created |
|------|---------|---------|
| `~/.claude/skills/career/format-resume/learned-preferences.yaml` | CV corrections | Existing |
| `~/.claude/skills/career/format-cover-letter/learned-preferences.yaml` | Cover letter corrections | New (empty) |

**Rationale:** Independent learning prevents cross-contamination. CV corrections shouldn't affect cover letter formatting and vice versa.

### Python CLI Backward Compatibility

**Default Behavior Unchanged:**
```bash
# Old usage (still works)
python format_cv.py input.md output.docx --preview

# Explicit CV mode (equivalent to above)
python format_cv.py input.md output.docx --document-type=cv --preview

# New: Cover letter mode
python format_cv.py input.md output.docx --document-type=cover-letter --preview
```

**Backward Compatibility Guarantee:** `--document-type` defaults to `'cv'`, so existing scripts and invocations continue working.

### Validation Checklist Before Release

**Pre-Release Validation:**

- [ ] All 15 existing CV tests pass
- [ ] format-resume produces identical output to before migration
- [ ] Shared template accessible from both skills
- [ ] New format-cover-letter skill functions independently
- [ ] Visual validation: Format existing CV, compare to previous version (pixel-perfect match)
- [ ] Visual validation: Format UCLA CAO letter, verify expected styling
- [ ] Visual validation: Format CSULB letter, verify expected styling
- [ ] PDF generation works for both document types
- [ ] Image preview generation works for both document types
- [ ] Learned preferences saving/loading works for both skills
- [ ] Documentation complete and accurate

### Rollback Plan

**If Critical Issues Arise:**

1. **Immediate Rollback (format-resume only):**
   - Revert `format-resume/skill.md` to point to old template location
   - Old template file still exists, no data loss
   - format-resume returns to pre-migration state
   - format-cover-letter remains separate, doesn't impact CV formatting

2. **Investigation:**
   - Identify root cause of issue
   - Fix without time pressure (CV formatting still works)
   - Re-test thoroughly

3. **Re-Deploy:**
   - Apply fix
   - Re-validate
   - Migrate format-resume to shared template again

**Low-Risk Migration:** Separate skills + backward compatibility + rollback plan = minimal risk to existing functionality.

---

## Success Criteria

### Functional Requirements

**Format-Resume (Existing Functionality):**
- ✓ All 15 existing tests pass
- ✓ Visual output unchanged from pre-migration
- ✓ Uses shared template successfully
- ✓ Learned preferences continue working

**Format-Cover-Letter (New Functionality):**
- ✓ User can invoke: "Format this cover letter: [content]"
- ✓ Date line right-aligned, 11pt
- ✓ Salutation and body styled as Body Text
- ✓ Thematic section headers styled in black, 13pt Bold
- ✓ Content mentions (institutions, positions, productions) styled correctly
- ✓ Closing and signature formatted properly
- ✓ Visual preview (PDF + images) generated successfully
- ✓ Learned preferences save and apply correctly

### Quality Requirements

**Code Quality:**
- ✓ All tests pass (15 existing + new cover letter tests)
- ✓ Test coverage maintained or improved
- ✓ No regressions in existing functionality
- ✓ Code follows existing style/patterns

**Documentation:**
- ✓ Design document complete (this document)
- ✓ User guide for format-cover-letter skill
- ✓ Updated main README if needed
- ✓ Inline code comments for changes

**User Experience:**
- ✓ Clear invocation: User knows when to use which skill
- ✓ Visual preview aids validation
- ✓ Learning loop improves accuracy over time
- ✓ Error messages helpful and actionable

### Performance Requirements

- ✓ Cover letter formatting completes in < 5 seconds (excluding PDF/image generation)
- ✓ PDF generation completes in < 10 seconds (LibreOffice dependent)
- ✓ Image generation completes in < 5 seconds (Poppler dependent)
- ✓ No performance regression for CV formatting

---

## Technical Specifications

### Template File Format

**Format:** Microsoft Word .docx (Office Open XML)
**Location:** `~/.claude/skills/career/shared/career-documents-template.docx`
**Tool:** Created via `python-docx` library

**Style Definitions:**

| Style Name | Type | Font | Size | Weight | Color | Alignment | Other |
|------------|------|------|------|--------|-------|-----------|-------|
| CV Name | Para | Helvetica | 18pt | Bold | Black | Left | - |
| Section Header | Para | Helvetica | 11pt (CV) / 13pt (CL) | Bold | Orange (CV) / Black (CL) | Left | Context-aware |
| Body Text | Para | Helvetica | 11pt | Normal | Black | Left | - |
| Timeline Entry | Para | Helvetica | 11pt | Normal | Black | Left | 72pt hanging indent |
| Bullet Standard | Para | Helvetica | 11pt | Normal | Black | Left | Bullet list |
| Bullet Gray | Para | Helvetica | 11pt | Normal | Gray | Left | Bullet list |
| Bullet Emphasis | Para | Helvetica | 11pt | Bold | Black | Left | Bullet list |
| Date Line | Para | Helvetica | 11pt | Normal | Black | **Right** | **NEW** |
| Play Title | Char | - | - | Bold | Black | - | Italic |
| Institution | Char | - | - | Bold | Black | - | - |
| Job Title | Char | - | - | Bold | Black | - | Italic |
| Orange Emphasis | Char | - | - | Bold | #FF6D49 | - | - |
| Gray Text | Char | - | - | Normal | Gray | - | - |

### Python Dependencies

**Existing (Unchanged):**
- `python-docx` - .docx manipulation
- `Pillow` - Image handling
- `PyYAML` - YAML config parsing

**Optional (Unchanged):**
- LibreOffice - PDF generation (graceful degradation if unavailable)
- Poppler (pdftoppm) - Image preview (graceful degradation if unavailable)

**Version Requirements:** (Same as current CV system)
- Python 3.8+
- python-docx >= 0.8.11
- Pillow >= 8.0.0
- PyYAML >= 5.4

### File Paths

**Skill Files:**
```
~/.claude/skills/career/
├── shared/
│   └── career-documents-template.docx
├── format-resume/
│   ├── skill.md
│   ├── style-mappings.yaml
│   └── learned-preferences.yaml
└── format-cover-letter/
    ├── skill.md
    ├── style-mappings.yaml
    └── learned-preferences.yaml
```

**Python Modules:**
```
{project_root}/
├── cv_formatting/
│   ├── __init__.py
│   ├── style_parser.py
│   ├── style_mapping.py
│   ├── template_builder.py
│   ├── style_applicator.py
│   ├── pdf_converter.py
│   └── image_generator.py
├── format_cv.py
└── generate_cv_template.py
```

**Tests:**
```
{project_root}/tests/
├── test_style_parser.py
├── test_style_mapping.py
├── test_template_builder.py
├── test_style_applicator.py
├── test_pdf_converter.py
├── test_image_generator.py
├── test_cover_letter_formatting.py  # NEW
└── test_shared_template.py          # NEW
```

---

## Risks & Mitigations

### Risk 1: Template Migration Breaks CV Formatting

**Likelihood:** Low
**Impact:** High
**Mitigation:**
- Comprehensive regression testing (all 15 tests must pass)
- Visual validation (pixel-perfect comparison)
- Rollback plan in place (revert to old template path)
- Old template remains until validation complete

### Risk 2: Section Header Context Awareness Complexity

**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- TDD approach (write tests first)
- Clear conditional logic in style_applicator.py
- Integration tests with real cover letters
- User can correct via learning loop if misapplied

### Risk 3: Cover Letter Semantic Patterns Too Specific

**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Test with multiple cover letters (UCLA, CSULB)
- Iterative refinement of style-mappings.yaml
- Learning loop captures user corrections
- Patterns can be updated post-deployment

### Risk 4: Shared Template Creates Maintenance Burden

**Likelihood:** Low
**Impact:** Low
**Mitigation:**
- Single source of truth simplifies maintenance (vs duplicated templates)
- Both skills benefit from any template improvements
- Clear ownership: template managed via generate_cv_template.py

### Risk 5: User Confusion About Which Skill to Use

**Likelihood:** Low
**Impact:** Low
**Mitigation:**
- Explicit naming: format-resume vs format-cover-letter
- Clear documentation
- User invocation makes intent explicit
- Error messages guide if wrong skill used

---

## Future Considerations

### Phase 2: Document Comparison Tool

**Deferred for future development. Potential approaches:**

**A. Version Tracking & Change Analysis**
- Compare drafts of same document
- Highlight what changed between versions
- Track evolution of specific sections
- Use case: "Show me what changed from yesterday's draft"

**B. Requirement Coverage Analysis**
- Parse job description for requirements
- Check if CV/cover letter address each requirement
- Generate coverage report
- Use case: "Does my cover letter address all key qualifications?"

**C. Consistency Checker**
- Compare CV and cover letter for consistency
- Flag discrepancies (dates, titles, institution names)
- Ensure productions/positions mentioned in cover letter exist in CV
- Use case: "I mentioned Romeo & Juliet in my cover letter - is it in my CV?"

**D. Holistic Application Review**
- Combination of B & C
- Job requirements coverage
- Cross-document consistency validation
- Style/tone consistency
- Use case: "Review my complete UCLA TFT application package"

**Decision Point:** Assess after Phase 1 deployment. Gather user feedback on which comparison features would be most valuable.

### Phase 3: Additional Document Types

**Deferred for future development. Potential document types:**

- Teaching statements/philosophy
- Research statements
- Diversity/equity statements
- Artist statements
- Administrative philosophy statements

**Design Considerations:**
- Would these share the same 13-style template?
- Or need distinct styles/formatting?
- Separate skills per document type?
- Or unified "format-academic-document" with type detection?

**Decision Point:** Wait for user need. Avoid premature abstraction.

### Phase 4: Advanced Semantic Understanding

**Long-term potential enhancements:**

- Auto-suggest improvements based on job description analysis
- Tone/style consistency analysis across documents
- Length optimization recommendations
- Keyword density analysis for ATS (Applicant Tracking Systems)
- AI-powered content suggestions

**Decision Point:** These require significant AI/NLP work. Assess ROI vs manual review process.

---

## Appendix A: Style Mapping Examples

### CV Section Headers (Existing)

**Input:**
```
EDUCATION

Stanford University
PhD in Theater Arts, 2010
```

**Styled:**
```
[Section Header]EDUCATION[/Section Header]  # Orange, 11pt Bold

[Institution]Stanford University[/Institution]
[Job Title]PhD in Theater Arts[/Job Title], [Gray Text]2010[/Gray Text]
```

### Cover Letter Thematic Headers (New)

**Input:**
```
Why UCLA? Why TFT? Why now?

UCLA, TFT, and the arts at UCLA more broadly stand at the threshold...
```

**Styled:**
```
[Section Header]Why UCLA? Why TFT? Why now?[/Section Header]  # Black, 13pt Bold

[Body Text][Institution]UCLA[/Institution], [Institution]TFT[/Institution], and the arts at [Institution]UCLA[/Institution] more broadly stand at the threshold...[/Body Text]
```

### Content Mentions (Same Across CV and Cover Letter)

**Input:**
```
At Center Theatre Group, I built the Kirk Douglas Theatre where I
nurtured productions of Angels in America.
```

**Styled:**
```
At [Institution]Center Theatre Group[/Institution], I built the
[Play Title]Kirk Douglas Theatre[/Play Title] where I nurtured
productions of [Play Title]Angels in America[/Play Title].
```

---

## Appendix B: Implementation Checklist

Use this checklist during implementation:

### Phase 1: Shared Template Foundation

- [ ] Create `~/.claude/skills/career/shared/` directory
- [ ] Write test: `test_date_line_style_creation()`
- [ ] Implement: Add Date Line style to template_builder.py
- [ ] Run test: Verify passes
- [ ] Write test: `test_template_contains_13_styles()`
- [ ] Run test: Verify passes
- [ ] Update `generate_cv_template.py` output path
- [ ] Run: Generate new shared template
- [ ] Validate: Template exists at correct path
- [ ] Validate: Template contains 13 styles
- [ ] Update format-resume skill.md (template path)
- [ ] Run all existing CV tests
- [ ] Validate: All 15 tests pass
- [ ] Format existing CV
- [ ] Visual validation: Compare to previous output

### Phase 2: Python Cover Letter Support

- [ ] Write test: `test_document_type_flag()`
- [ ] Implement: Update format_cv.py argparse
- [ ] Run test: Verify passes
- [ ] Write test: `test_document_type_defaults_to_cv()`
- [ ] Run test: Verify backward compatibility
- [ ] Write test: `test_section_header_cv_mode()`
- [ ] Write test: `test_section_header_cover_letter_mode()`
- [ ] Implement: Update style_applicator.py conditional formatting
- [ ] Run tests: Verify both pass
- [ ] Create `tests/fixtures/sample_cover_letter.md`
- [ ] Create `tests/fixtures/expected_cover_letter_output.docx`
- [ ] Write test: `test_full_cover_letter_formatting()`
- [ ] Run test: Verify passes
- [ ] Run all existing CV tests
- [ ] Validate: No regressions

### Phase 3: Format-Cover-Letter Skill

- [ ] Create skill directory structure
- [ ] Write skill.md (workflow, patterns, examples)
- [ ] Create style-mappings.yaml (structural patterns)
- [ ] Create style-mappings.yaml (content patterns)
- [ ] Create empty learned-preferences.yaml
- [ ] Test: Invoke skill with UCLA CAO letter
- [ ] Validate: Date line correct
- [ ] Validate: Salutation/body correct
- [ ] Validate: Thematic headers correct (black, 13pt)
- [ ] Validate: Institutions/positions/productions styled correctly
- [ ] Validate: Closing/signature correct
- [ ] Generate PDF preview
- [ ] Generate image preview
- [ ] Visual validation by user
- [ ] Refine style-mappings.yaml based on output
- [ ] Re-test with UCLA CAO letter
- [ ] Test: Invoke skill with CSULB letter
- [ ] Validate: Consistent styling with UCLA letter
- [ ] Write or update format-cover-letter user guide
- [ ] Update main README if needed
- [ ] Run all tests (CV + cover letter)
- [ ] Final validation: All acceptance criteria met

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-10 | 1.0 | System | Initial design document created from validated brainstorming session |

---

**End of Design Document**

*Ready for implementation via TDD approach across 3 phases.*
