# Document Formatting Skills Design

**Date:** 2025-11-09
**Status:** Design Complete - Ready for Implementation
**Goal:** Create Claude skills that intelligently format resume/CV and cover letter content using semantic understanding and visual verification

---

## Background

The career-lexicon-builder project generates high-quality career content through AI-powered analysis and Socratic career skills. The final step—formatting this content into professionally styled documents—remains manual and error-prone.

**Current Pain Points:**
1. Manual copy-paste into existing .pages/.docx files
2. Inconsistent style application
3. Time-consuming formatting corrections
4. No learning from past formatting decisions

**Vision:**
Conversational, context-aware formatting skills that learn user preferences and provide visual verification before delivery.

---

## Key Design Decisions

### 1. Two Separate Skills
- **`format-resume`** - Handles CV/resume formatting with complex structure (sections, bullets, hierarchical content)
- **`format-cover-letter`** - Handles cover letter formatting with narrative structure (date, salutation, paragraphs, signature)

**Rationale:** Different structural patterns, different inference rules, different learning needs.

### 2. Document Type Detection
- **Primary:** Auto-detect based on content patterns
- **Fallback:** Ask for confirmation when uncertain
- **Override:** User can explicitly specify type

**Detection Signals:**

**Cover Letter:**
- Starts with date pattern
- Contains "Dear [Name]" or salutation
- Has "RE:" reference line
- Contains narrative paragraphs
- Ends with closing/signature

**Resume/CV:**
- Starts with name (2-3 words)
- Has ALL CAPS section headers
- Contains bullet points
- Has date ranges
- Has hierarchical indentation

### 3. Three Operating Modes

**Mode 1: Format New Content**
- Input: Plain text or markdown content (clipboard, file, or conversation)
- Template: Default template from skill directory
- Output: New formatted .docx file

**Mode 2: Reformat Existing Document**
- Input: Path to existing .docx
- Template: Document's own styles
- Output: Reformatted document (in place or new version)
- Use cases: Fix inconsistent styling, iterate on previous formatting

**Mode 3: Clone and Adapt**
- Input: Base document path + new content (conversational specification)
- Template: Base document's styles and structure
- Output: New document with base structure + updated content
- Use case: "Use my Colburn resume for UCLA position"

### 4. Semantic Style Inference

**Approach:** Claude analyzes content semantically, not just pattern-matching.

**Why:** Context matters
- "2023 - Present ***Interim Associate Dean***" (job title, use style X)
- "***Truth, Racial Healing & Transformation Toolkit***" (document title, use style Y)

Traditional regex can't distinguish these. Claude understands context.

### 5. Learning System

**Storage:** Skill-level preferences
- `~/.claude/skills/career/format-resume/learned-preferences.yaml`
- `~/.claude/skills/career/format-cover-letter/learned-preferences.yaml`

**Learning Trigger:** User corrections during conversation
- User: "That committee role should be indent-3 not indent-2"
- Skill: "✓ I've updated my formatting rules to remember this"

**Notification:** Automatic with notification (not silent, not requiring explicit save)

### 6. Visual Verification

**Workflow:**
1. Format document
2. Convert to PDF → JPEG images
3. Display images to user in conversation
4. User confirms or requests corrections

**Tools:**
```bash
soffice --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 150 output.pdf page
```

**Rationale:** High-stakes documents (job applications) need visual confidence, not just structural correctness.

### 7. Output Handling

**Naming Strategy:** Context-aware with confirmation
- Skill suggests name based on conversation context
- Example: User says "Format my UCLA resume" → suggests `ucla-resume.docx`
- Always confirms location/name before saving

**Directory Structure:**
```
~/.claude/skills/career/
├── format-resume/
│   ├── skill.md
│   ├── cv-template.docx              # User provides (manual .pages → .docx)
│   ├── style-mappings.yaml           # Base inference rules
│   └── learned-preferences.yaml      # Accumulated corrections
│
└── format-cover-letter/
    ├── skill.md
    ├── cover-letter-template.docx
    ├── style-mappings.yaml
    └── learned-preferences.yaml
```

### 8. Template Management

**Setup:** Manual one-time conversion
- User converts .pages templates to .docx using AppleScript (per original plan)
- User places templates in skill directories
- Skills reference these templates for new documents

**Rationale:** Keeps skills focused on formatting logic, not template conversion complexity.

---

## Architecture

### System Flow

```
User invokes skill with content
         ↓
Detect input type (file/clipboard/conversation/existing doc)
         ↓
Detect mode (new/reformat/clone)
         ↓
    ┌────┴────┐
Mode 1        Mode 2           Mode 3
New Content   Reformat         Clone & Adapt
    ↓             ↓                 ↓
Load template  Use doc styles  Load base doc
    ↓             ↓                 ↓
Detect type    Parse content    Parse structure
    ↓             ↓                 ↓
Confirm type   ────┴────────────────┤
    ↓                               ↓
Analyze content semantically    Conversational merge
    ↓                               ↓
Apply styles (python-docx)      Apply styles
    ↓                               ↓
Generate .docx                  Generate .docx
    ↓                               ↓
Convert to PDF → images         Convert to PDF → images
    ↓                               ↓
Show preview                    Show preview
    ↓                               ↓
User confirms/corrects          User confirms/corrects
    ↓                               ↓
Update learned-preferences.yaml (if corrections made)
    ↓
Save final document with context-aware name
```

### Technology Stack

**Core Libraries:**
- `python-docx` - Style application and document generation
- `pandoc` - Document analysis and markdown conversion
- `LibreOffice (soffice)` - PDF conversion
- `poppler (pdftoppm)` - PDF to image conversion

**Rationale:**
- Templates use simple paragraph/character styles (confirmed by analysis)
- No tables, text boxes, or multi-column layouts
- python-docx fully supports all required features
- Document library (XML manipulation) is unnecessary complexity

---

## Skill Specifications

### format-resume Skill

**Invocation Examples:**
- "Format this resume: [paste content]"
- "Format my-draft.txt as a resume"
- "Reformat this existing resume.docx with proper styles"
- "Use my Colburn resume as the base, but update the experience section with [new content]"

**Style Mappings:**

From template analysis, the CV template uses:
- `Header` - Name (bold, 13pt Helvetica, #ff6c49 color, hanging indent)
- `Heading 3 A` - Section headers like "EDUCATION" (bold, 11pt Times New Roman)
- `full-cv-indent 2` - Main body text (11pt Helvetica, hanging indent, exact line spacing)
- `full-cv-indent 3` - Secondary text (7pt Helvetica)
- `full-cv-main bold` - Bold inline emphasis (9pt Helvetica bold)
- `full-cv_main ital` - Bold italic emphasis (9pt Helvetica)
- `Bullet` - List formatting
- `numbers` - Small numbers/dates (7pt)
- `BOLD TITLES GREEN` - Special highlighting
- `Free Form` - Flexible paragraph formatting

**Semantic Inference Rules:**

```yaml
# style-mappings.yaml structure
patterns:
  - pattern: first_line_short
    condition: "First line, ≤5 words, proper case"
    style: "Header"

  - pattern: section_header
    condition: "ALL CAPS, short line, follows previous section"
    style: "Heading 3 A"

  - pattern: date_range_institution
    condition: "Line starts with date range (YYYY - YYYY or YYYY - Present)"
    style: "full-cv-indent 2"
    inline_styles:
      institution_name: "full-cv-main bold"

  - pattern: job_title
    condition: "Follows institution line, italic markers or all caps"
    style: "full-cv-indent 2"
    inline_styles:
      title: "full-cv_main ital"

  - pattern: bullet_point
    condition: "Starts with •, -, *, or marker"
    style: "Bullet"

  - pattern: body_paragraph
    condition: "Default paragraph under job/role"
    style: "full-cv-indent 2"
```

**Learning Examples:**

```yaml
# learned-preferences.yaml (accumulated over time)
learned_rules:
  - context: "committee_roles"
    original_style: "full-cv-indent 2"
    preferred_style: "full-cv-indent 3"
    learned_from: "2025-11-09 correction: 'Graduate Studies Advisory Committee should be smaller'"

  - context: "course_lists"
    handling: "compress"
    preferred_style: "full-cv-indent 3"
    learned_from: "2025-11-10 correction: 'Course names should use smaller font'"
```

### format-cover-letter Skill

**Invocation Examples:**
- "Format this cover letter: [paste content]"
- "Format cover-letter-draft.md"
- "Use my Colburn cover letter for UCLA position, replace opening and achievements paragraph"

**Style Mappings:**

From template analysis, the cover letter template uses:
- `Header` - Name (bold, 13pt Helvetica, #ff6c49 color)
- `full-cv-indent 2` - All body paragraphs (11pt Helvetica)
- `Normal.0` - Date/address block (12pt Courier)

**Semantic Inference Rules:**

```yaml
# style-mappings.yaml structure
patterns:
  - pattern: date
    condition: "First line, date format"
    style: "Normal.0"

  - pattern: reference_line
    condition: "Starts with 'RE:'"
    style: "Normal.0"

  - pattern: salutation
    condition: "Starts with 'Dear'"
    style: "full-cv-indent 2"

  - pattern: body_paragraph
    condition: "Regular paragraph between salutation and closing"
    style: "full-cv-indent 2"

  - pattern: closing
    condition: "Short line at end (Sincerely, Best regards, etc.)"
    style: "full-cv-indent 2"

  - pattern: signature
    condition: "Name after closing"
    style: "Header"
```

---

## Workflows

### Workflow 1: Format New Content

**User:** "Format this resume: [pastes content]"

**Skill:**
1. Detects input type: clipboard content
2. Analyzes content structure
3. Detects document type: Resume (has section headers, bullets, date ranges)
4. **Confirms:** "I detected this is a CV with 5 sections (EDUCATION, PROFESSIONAL EXPERIENCE, UNIVERSITY SERVICE, etc.), 3 major positions, 12 bullet points. I'll apply your resume template styles. Correct? (Y/n)"
5. User confirms
6. Generates formatting script using python-docx
7. Applies styles based on semantic analysis
8. Creates `formatted-resume.docx`
9. Converts to PDF → images
10. **Shows preview:** Displays page images
11. **Reports:** "Applied Header to 'Anthony Byrnes', Heading 3 A to 5 section headers, full-cv-indent 2 to 47 paragraphs, Bullet style to 12 items"
12. **Suggests name:** "Save as `anthony-byrnes-resume.docx`? (Y/n)"
13. User confirms
14. Saves file

### Workflow 2: Reformat Existing Document

**User:** "Fix the styling in my-messy-resume.docx"

**Skill:**
1. Detects input type: file path
2. Opens document, analyzes current state
3. Detects mode: reformat (existing .docx)
4. Reads content structure
5. **Reports:** "I see inconsistent styling - mix of Arial and Times New Roman, some bullets are manual dashes, section headers use different fonts. I'll standardize everything to match your CV template styles. Proceed? (Y/n)"
6. User confirms
7. Parses content, applies consistent styles
8. Saves reformatted document
9. Shows preview
10. User confirms or requests corrections

### Workflow 3: Clone and Adapt

**User:** "Use my Colburn resume as the base for UCLA CAO position. Keep the structure but replace the opening bio and update the CSULB section with these new achievements: [pastes content]"

**Skill:**
1. Detects mode: clone (base document + new content)
2. Opens `colburn-resume.docx`
3. Parses structure: identifies sections, hierarchy
4. **Shows structure:** "Colburn resume has: Header (bio), EDUCATION (2 degrees), PROFESSIONAL EXPERIENCE (3 positions: CSULB, CTG, Shakespeare), UNIVERSITY SERVICE..."
5. **Confirms changes:** "I'll keep all sections but replace: (1) opening bio, (2) CSULB achievements under PROFESSIONAL EXPERIENCE. Everything else unchanged. Correct?"
6. User confirms
7. Merges new content while preserving structure
8. Applies consistent styles from base document
9. Creates `ucla-cao-resume.docx`
10. Shows preview
11. User reviews

**User:** "Actually, that second CSULB achievement should be in smaller font - it's a committee role, not a major responsibility"

**Skill:**
12. Identifies paragraph
13. Changes style from `full-cv-indent 2` to `full-cv-indent 3`
14. **Learns:** "✓ I've updated my formatting rules to remember that committee roles use full-cv-indent 3"
15. Saves to `learned-preferences.yaml`
16. Regenerates document
17. Shows updated preview
18. User confirms
19. Saves final document

---

## Technical Implementation

### python-docx Integration

**Template Loading:**
```python
from docx import Document

# Load template (preserves all styles)
template_path = Path.home() / '.claude/skills/career/format-resume/cv-template.docx'
doc = Document(template_path)
```

**Style Application:**
```python
# Paragraph style
doc.add_paragraph('PROFESSIONAL EXPERIENCE', style='Heading 3 A')

# Character style (inline formatting)
p = doc.add_paragraph(style='full-cv-indent 2')
p.add_run('2023 - Present ')
p.add_run('California State University Long Beach', style='full-cv-main bold')
```

**Style Verification:**
```python
# List available styles in document
for style in doc.styles:
    if style.type == WD_STYLE_TYPE.PARAGRAPH:
        print(f"Paragraph style: {style.name}")
    elif style.type == WD_STYLE_TYPE.CHARACTER:
        print(f"Character style: {style.name}")
```

### Semantic Analysis Pattern

The skill uses Claude's language understanding to analyze content:

```python
# Pseudo-code for skill logic
def analyze_content(text):
    """Claude analyzes text and returns structured understanding"""

    # Example analysis result:
    {
        "document_type": "resume",
        "confidence": 0.95,
        "structure": [
            {
                "type": "header",
                "content": "Anthony Byrnes",
                "style": "Header"
            },
            {
                "type": "section_header",
                "content": "PROFESSIONAL EXPERIENCE",
                "style": "Heading 3 A"
            },
            {
                "type": "position",
                "date_range": "2023 - Present",
                "institution": "California State University Long Beach",
                "title": "Interim Associate Dean",
                "style": "full-cv-indent 2",
                "inline_styles": {
                    "institution": "full-cv-main bold",
                    "title": "full-cv_main ital"
                }
            },
            # ... more elements
        ]
    }
```

### Learning System Structure

**learned-preferences.yaml:**
```yaml
version: 1.0
last_updated: "2025-11-09T14:30:00"

rules:
  - id: "committee_roles_indent"
    pattern: "committee|advisory|service role"
    context: "appears under university service or as secondary role"
    action:
      original_style: "full-cv-indent 2"
      preferred_style: "full-cv-indent 3"
    learned_date: "2025-11-09"
    correction_count: 1

  - id: "course_names_compress"
    pattern: "course titles in list"
    context: "teaching section with multiple course names"
    action:
      style: "full-cv-indent 3"
      inline_style: "none"
    learned_date: "2025-11-10"
    correction_count: 2

  - id: "grant_amounts_emphasis"
    pattern: "dollar amounts for grants/budgets"
    context: "achievement or responsibility description"
    action:
      inline_style: "full-cv-main bold"
    learned_date: "2025-11-10"
    correction_count: 1
```

**Preference Application:**
```python
def apply_learned_preferences(element, preferences):
    """Apply learned preferences to formatting decision"""

    for rule in preferences['rules']:
        if matches_pattern(element.content, rule['pattern']):
            if matches_context(element, rule['context']):
                # Override default style inference
                element.style = rule['action']['preferred_style']
                # Log application
                log(f"Applied learned rule: {rule['id']}")
```

---

## Validation and Testing

### Template Compatibility Verification

**Already completed** - Analysis of actual templates confirms:
- ✅ Both templates (CV and cover letter) use consistent style system
- ✅ No tables, text boxes, or multi-column layouts
- ✅ All styles are paragraph or character styles
- ✅ python-docx can access and apply all styles
- ✅ Custom style names preserved through .pages → .docx conversion

**Style Inventory:**
- Header (paragraph)
- Heading 3 A (paragraph)
- full-cv-indent 2 (paragraph)
- full-cv-indent 3 (paragraph)
- full-cv-main bold (character)
- full-cv_main ital (character)
- Normal.0 (paragraph)
- Bullet (numbering)
- Free Form (paragraph)

### Test Cases

**Test 1: New Resume from Plain Text**
- Input: Plain text resume content
- Expected: Proper detection, correct styles, visual preview
- Success criteria: All sections, bullets, emphasis correct

**Test 2: Cover Letter with Date Detection**
- Input: Cover letter starting with "November 9, 2025"
- Expected: Auto-detect cover letter type, confirm with user
- Success criteria: Date in Normal.0, body in full-cv-indent 2

**Test 3: Clone UCLA Resume from Colburn**
- Input: Colburn resume + replacement content
- Expected: Structure preserved, content merged correctly
- Success criteria: Same sections, new content, consistent styles

**Test 4: Learning from Correction**
- Input: Formatted document + correction "Make this indent-3"
- Expected: Style changed, preference saved, notification shown
- Success criteria: learned-preferences.yaml updated, rule applied to future documents

**Test 5: Mixed Content (Markdown + Plain)**
- Input: Content with `**bold**` markers and plain text
- Expected: Smart interpretation of markdown where present
- Success criteria: Bold converted to character style, plain text styled by context

---

## Dependencies

**Required:**
- python-docx (already installed in project)
- defusedxml (installed in project .venv)
- LibreOffice (`soffice` command for PDF conversion)
- Poppler (`pdftoppm` for PDF to image conversion)
- pandoc (for markdown conversion and analysis)

**Installation Check:**
```bash
# Verify dependencies
python -c "import docx; print('python-docx OK')"
python -c "import defusedxml; print('defusedxml OK')"
which soffice  # Should return path
which pdftoppm # Should return path
which pandoc   # Should return path
```

---

## Integration Points

### Career Lexicon Builder Integration

**Current Flow:**
```
Lexicons → Socratic Skills → Markdown Content → [Manual formatting]
```

**Enhanced Flow:**
```
Lexicons → Socratic Skills → Markdown Content → format-resume/cover-letter skill → Formatted .docx
```

**Optional Integration:**
Socratic career skills could invoke formatting skills automatically:
```
User: "Create resume for UCLA position"
  ↓
Socratic skill generates content
  ↓
Automatically invokes format-resume skill
  ↓
User receives both markdown and formatted .docx
```

### Existing Document Export System

The project already has PDF export capability (`export_to_pdf.py`). The formatting skills complement this:

**Use Case:**
1. Generate content with career-lexicon-builder
2. Format with format-resume skill → .docx
3. Export to PDF using existing export_to_pdf.py → final submission format

---

## Success Criteria

**Must Have:**
- ✅ Two separate skills (resume and cover letter)
- ✅ Three operating modes (new, reformat, clone)
- ✅ Semantic content analysis (not just regex patterns)
- ✅ Auto-detect document type with confirmation
- ✅ Visual verification (PDF → images)
- ✅ Learning system with automatic save
- ✅ Context-aware output naming
- ✅ All template styles correctly applied

**Should Have:**
- ✅ Conversational corrections during iteration
- ✅ Support for markdown input
- ✅ Intelligent merge for clone mode
- ✅ Preference explanations (why a rule was applied)

**Nice to Have:**
- Batch formatting (multiple documents at once)
- Template variants (academic vs corporate style)
- Style diff visualization (show what changed)
- Export learned preferences for sharing/backup
- Integration with career-lexicon-builder Socratic skills

---

## Implementation Plan

### Phase 1: Core Infrastructure (4-6 hours)
1. Create skill directory structure
2. Write base skill.md for format-resume
3. Implement basic content detection
4. Implement python-docx formatting logic
5. Test with simple resume content

**Deliverable:** Working format-resume skill (Mode 1 only)

### Phase 2: Visual Verification (2-3 hours)
1. Add PDF conversion workflow
2. Add image generation
3. Integrate preview display
4. Test verification workflow

**Deliverable:** Skills show visual previews

### Phase 3: Learning System (3-4 hours)
1. Design learned-preferences.yaml schema
2. Implement preference detection from corrections
3. Implement preference application
4. Add notification system
5. Test learning across sessions

**Deliverable:** Skills learn from user corrections

### Phase 4: Advanced Modes (4-5 hours)
1. Implement Mode 2 (reformat existing)
2. Implement Mode 3 (clone and adapt)
3. Add conversational merge logic
4. Test complex clone scenarios

**Deliverable:** All three modes working

### Phase 5: Cover Letter Skill (2-3 hours)
1. Create format-cover-letter skill
2. Adapt inference rules for narrative structure
3. Test with actual cover letters
4. Verify style consistency with resume skill

**Deliverable:** Both skills operational

### Phase 6: Polish and Integration (3-4 hours)
1. Refine error messages
2. Improve confirmation prompts
3. Add edge case handling
4. Document user guide
5. Test end-to-end workflows

**Deliverable:** Production-ready skills

**Total Estimated Time:** 18-25 hours

---

## Risks and Mitigations

### Risk 1: Semantic Analysis Accuracy
**Problem:** Claude might misinterpret content structure
**Mitigation:**
- Always show interpretation before formatting
- Easy correction workflow
- Learning system improves over time
- User can provide explicit hints when needed

### Risk 2: Template Style Changes
**Problem:** User updates template, breaks style mappings
**Mitigation:**
- Version templates in git
- Style verification before formatting
- Clear error messages if styles missing
- Fallback to similar styles

### Risk 3: Learning System Conflicts
**Problem:** Learned preferences might contradict each other
**Mitigation:**
- Preference conflict detection
- Show user which rule is being applied
- Allow preference editing/deletion
- Rule specificity ordering (most specific wins)

### Risk 4: LibreOffice/Poppler Availability
**Problem:** PDF conversion tools might not be installed
**Mitigation:**
- Graceful degradation (skip preview if unavailable)
- Clear installation instructions
- Alternative: use docx → markdown for text-based verification

### Risk 5: Complex Content Edge Cases
**Problem:** Unusual content structure breaks inference
**Mitigation:**
- Conservative inference (ask when uncertain)
- Explicit style override mechanism
- Manual formatting mode as escape hatch
- Collect edge cases, improve rules

---

## Future Enhancements

### Phase 2 Features (Post-MVP)

**1. Batch Processing**
- Format multiple documents in sequence
- Apply same preferences across batch
- Useful for updating multiple applications

**2. Style Diff Visualization**
- Show before/after comparison
- Highlight what changed
- Useful for verifying reformatting

**3. Template Variants**
- Multiple visual styles (academic, corporate, creative)
- User can switch between templates
- Maintain content, change presentation

**4. Preference Management**
- View all learned preferences
- Edit/delete specific rules
- Export/import preferences
- Share preferences across machines

**5. Integration with Socratic Skills**
- Automatic formatting invocation
- Seamless content → formatted document flow
- Job-specific template selection

**6. Advanced Clone Features**
- Merge multiple base documents
- Intelligent section reordering
- Automatic de-duplication
- Version tracking for document families

**7. Collaboration Features**
- Track who made formatting decisions
- Team preference sharing
- Comment/annotation system
- Review workflow integration

---

## Related Documents

**Original Research:**
- `docs/plans/2025-11-09-pages-document-automation-design.md` - Technical approach research for .pages automation

**Skills Documentation:**
- docx skill (`~/.claude/skills/docx/`) - Document manipulation patterns and workflows

**Project Context:**
- `README.md` - Career lexicon builder overview
- `QUICKSTART_SOCRATIC_SKILLS.md` - Socratic career skills usage

---

## Appendix: Brainstorming Session Summary

### Key Questions Explored

1. **Document type detection** → Auto-detect with confirmation
2. **Style inference approach** → Semantic understanding via Claude, not regex
3. **python-docx vs Document library** → python-docx sufficient (templates confirmed simple)
4. **Template complexity** → Analyzed actual templates, confirmed no tables/text boxes/columns
5. **Number of skills** → Two separate (resume and cover letter) for focused learning
6. **Learning persistence** → Skill-level with automatic save and notification
7. **Verification method** → Visual (PDF → images) for high-stakes confidence
8. **Operating modes** → Three modes (new, reformat, clone) for flexibility
9. **Clone workflow** → Conversational merge with smart content replacement
10. **Output handling** → Context-aware naming with confirmation
11. **Template storage** → User profile (~/.claude/skills/) for global availability
12. **Setup complexity** → Manual template conversion, focused skills

### Decisions That Shaped the Design

**"Actually, we need context for this"** → Led to Claude-powered semantic analysis instead of pattern-matching

**"Two different skills, one for each document type"** → Led to focused, learnable skills instead of one complex skill

**"C" (confirm when uncertain)** → Led to transparent, confidence-building workflow

**"A with remember your corrections"** → Led to learning system that improves over time

**"B" (visual verification)** → Led to PDF → image preview for quality assurance

**"D" (multiple input types)** → Led to flexible invocation supporting all workflows

**"Clone and adapt"** → Led to Mode 3 supporting real-world resume reuse patterns

### Evolution of the Concept

**Started with:** Simple python-docx automation for style application

**Evolved to:** Intelligent, learning skills that understand document structure semantically, verify visually, and improve through use

**Key insight:** This is a **context interpretation problem**, not a template-filling problem. Claude's semantic understanding is the differentiator.

---

**End of Design Document**
