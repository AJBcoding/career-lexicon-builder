# CV Template Guide

A comprehensive guide to understanding and working with the CV formatting template.

## Overview

The CV template is a clean .docx document with 12 carefully designed semantic styles. These styles replaced 97 duplicate and overlapping styles from the original .pages CV through intelligent consolidation based on usage analysis.

**Key concept:** Semantic styles are named for their **meaning** (what they represent), not their **appearance** (how they look).

## The Template Creation Story

### The Problem: 97 Styles, Massive Duplication

Analysis of the original .pages CV revealed:

**Style duplication example:**
- `ps81934`, `ps2548`, `ps2597`, `ps53936`, `ps8131`, `ps2573`, `ps2570`, `ps8343`, `ps8957`, `ps2599`
- All of these were "Body Text" - same font, size, color
- Just created at different times as the CV evolved
- Each had cryptic auto-generated names

**Usage analysis:**
```
ss2578: 468 uses - bold italic (play titles)
ps2548: 85 uses - body text
ps81934: 25 uses - body text (duplicate of ps2548)
ss2505: 48 uses - bold (institution names)
ps2532: 103 uses - gray with hanging indent (timeline entries)
...
```

### The Solution: Semantic Consolidation

Instead of 97 cryptic style names, we created 12 meaningful styles:

**Before:** `ss2578`, `ss40454`, `ss2547` (all bold italic, used for plays)
**After:** `Play Title` (one semantic style)

**Before:** `ps81934`, `ps2548`, `ps2597`, `ps53936`, `ps8131`, etc. (all body text)
**After:** `Body Text` (one semantic style)

**Before:** `ss2505`, `ss93858`, `ss2543`, `ss138597` (all bold, used for institutions)
**After:** `Institution` (one semantic style)

This reduced complexity by 87% while maintaining full formatting capability.

## The 12 Semantic Styles

### Design Principles

Each style was designed with three criteria:

1. **Semantic clarity** - Name describes meaning, not appearance
2. **Visual distinctiveness** - Each serves a unique purpose
3. **Usage-based** - Derived from actual CV content patterns

### Paragraph Styles (7)

Paragraph styles control the structure and layout of entire paragraphs.

#### CV Name

**Purpose:** Your name at the document top

**Visual properties:**
- Font: Helvetica 13pt
- Weight: Bold
- Color: Black
- Spacing: Standard paragraph spacing

**Usage frequency:** Once per document (1 use)

**Consolidates:** `ps2554`, `ps27686` (2 original styles)

**Why semantic naming matters:**
This isn't "Big Bold Text" or "Title Style" - it's specifically your name. This semantic meaning helps Claude understand document structure.

**Code (from template_builder.py):**
```python
def _create_cv_name_style(self, doc: Document):
    """Create CV Name paragraph style (name at top)"""
    style = doc.styles.add_style('CV Name', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(13)
    style.font.bold = True
```

#### Section Header

**Purpose:** Major section dividers (EDUCATION, EXPERIENCE, etc.)

**Visual properties:**
- Font: Helvetica 10pt
- Weight: Bold
- Color: Orange (#FF6D49)
- Spacing: Standard paragraph spacing

**Usage frequency:** ~20 times per document (varies by CV length)

**Consolidates:** `ps2539`, `ps2557`, `ps2551` (3 original styles)

**Why this color?**
Orange (#FF6D49) was the brand color used consistently in the original CV for section headers. It provides visual hierarchy without overwhelming the document.

**Code:**
```python
def _create_section_header_style(self, doc: Document):
    """Create Section Header style (EDUCATION, PROFESSIONAL EXPERIENCE)"""
    style = doc.styles.add_style('Section Header', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(10)
    style.font.bold = True
    style.font.color.rgb = self.ORANGE_RGB  # RGBColor(255, 109, 73)
```

#### Body Text

**Purpose:** Standard paragraph content - descriptions, details, responsibilities

**Visual properties:**
- Font: Helvetica 9pt
- Weight: Regular
- Color: Black
- Spacing: Standard paragraph spacing

**Usage frequency:** ~200+ times per document (most common after bullets)

**Consolidates:** `ps81934`, `ps2548`, `ps2597`, `ps53936`, `ps8131`, `ps2573`, `ps2570`, `ps8343`, `ps8957`, `ps2599` (10 original styles)

**Special note:**
"Body Text" is a built-in Word style, so we modify the existing style rather than creating a new one. This ensures compatibility with Word's style inheritance system.

**Code:**
```python
def _create_body_text_style(self, doc: Document):
    """Create Body Text paragraph style (standard paragraphs)"""
    # Body Text is a built-in style, so modify it instead of creating new
    style = doc.styles['Body Text']
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)
```

#### Timeline Entry

**Purpose:** Date ranges with institutions/employers

**Visual properties:**
- Font: Helvetica 9pt
- Weight: Regular
- Color: Black
- Indent: 72pt hanging indent (first line -72pt, left margin +72pt)

**Usage frequency:** ~100 times per document (every job, degree, production)

**Consolidates:** `ps2532`, `ps81930`, `ps2541`, `ps52931`, `ps176105`, `ps49520` (6 original styles)

**The hanging indent:**
```
2023 - Present California State University Long Beach
               Interim Associate Dean for Student Success
               Oversee 12 academic advisors...
```

First line starts at left margin (date), subsequent lines indent 72pt. This creates visual alignment of dates while allowing for varying institution name lengths.

**Why 72pt?**
This is exactly 1 inch (72 points = 1 inch). Standard, professional spacing that works well for most institution names.

**Code:**
```python
def _create_timeline_entry_style(self, doc: Document):
    """Create Timeline Entry style (date + institution with hanging indent)"""
    style = doc.styles.add_style('Timeline Entry', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)

    # 72pt hanging indent (from analysis)
    style.paragraph_format.left_indent = Pt(72)
    style.paragraph_format.first_line_indent = Pt(-72)
```

#### Bullet Standard

**Purpose:** Regular bullet lists for achievements, responsibilities

**Visual properties:**
- Font: Helvetica 9pt
- Weight: Regular
- Color: Black
- Indent: 72pt left margin (aligns with timeline entries)
- Bullet: Standard disc

**Usage frequency:** ~250+ times per document (most common style)

**Consolidates:** `ps40376`, `ps40524`, `ps40420`, `ps40357`, `ps40270`, `ps40470`, `ps40339`, `ps40585` (8 original styles)

**Visual alignment:**
```
2023 - Present California State University Long Beach
               Interim Associate Dean
               • Developed strategic initiatives
               • Led team of 12 advisors
               • Increased retention by 15%
```

Bullets align with the timeline entry indent (72pt) creating visual consistency.

**Code:**
```python
def _create_bullet_standard_style(self, doc: Document):
    """Create Bullet Standard style (regular bullets)"""
    style = doc.styles.add_style('Bullet Standard', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)

    # Bullet formatting
    style.paragraph_format.left_indent = Pt(72)
```

#### Bullet Gray

**Purpose:** Secondary information bullets (dates, course lists, details)

**Visual properties:**
- Font: Helvetica 9pt
- Weight: Regular
- Color: Gray (#808080)
- Indent: 72pt left margin

**Usage frequency:** ~100 times per document

**Consolidates:** `ps2532`, `ps40350`, `ps151234` (3 original styles)

**When to use:**
- Degree conferral dates
- Course lists
- Committee details
- Secondary achievements
- Supplementary information

**Visual effect:**
```
EDUCATION

1994-1997 California Institute of the Arts
          Master of Fine Arts, Acting
          • Degree conferred May 1997
          • Thesis: "Stanislavski in Contemporary Practice"
          • Relevant coursework: Voice, Movement, Alexander
```

Gray bullets recede visually, indicating secondary importance.

**Code:**
```python
def _create_bullet_gray_style(self, doc: Document):
    """Create Bullet Gray style (bullets for dates/education)"""
    style = doc.styles.add_style('Bullet Gray', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)
    style.font.color.rgb = self.GRAY_RGB  # RGBColor(128, 128, 128)

    style.paragraph_format.left_indent = Pt(72)
```

#### Bullet Emphasis

**Purpose:** Highlighted achievements, awards, key items

**Visual properties:**
- Font: Helvetica 9pt
- Weight: Bold Italic
- Color: Black
- Indent: 72pt left margin

**Usage frequency:** ~50 times per document

**Consolidates:** `ps40465`, `ps46257`, `ps40394`, `ps40547`, `ps40503`, `ps40592`, `ps45767`, `ps176103` (8 original styles)

**When to use:**
- Major awards
- Published work
- Keynote presentations
- Significant grants
- Career milestones

**Visual effect:**
```
HONORS AND AWARDS

• Recipient of Excellence in Teaching Award (2022)
• Published in peer-reviewed Theatre Journal
• $500K grant from National Endowment for the Arts
```

Bold italic creates visual weight, drawing attention to important items.

**Code:**
```python
def _create_bullet_emphasis_style(self, doc: Document):
    """Create Bullet Emphasis style (bold italic bullets)"""
    style = doc.styles.add_style('Bullet Emphasis', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)
    style.font.bold = True
    style.font.italic = True

    style.paragraph_format.left_indent = Pt(72)
```

### Character Styles (5)

Character styles apply to specific text within paragraphs (inline formatting).

#### Play Title

**Purpose:** Titles of theatrical productions, artistic works

**Visual properties:**
- Weight: Bold Italic
- Inherits size and font from paragraph

**Usage frequency:** ~468 times per document (most used character style!)

**Consolidates:** `ss2578`, `ss40454`, `ss2547` (3 original styles)

**Why most common?**
For a theater professional's CV, play titles appear in:
- Directing credits
- Acting credits
- Design credits
- Playwriting credits
- Every production listed

**Semantic distinction:**
Even though this is bold italic like Job Title, it represents different meaning (artistic work vs employment position).

**Example:**
```
SELECTED DIRECTING CREDITS

Romeo & Juliet - California Shakespeare Theater, 2019
```

"Romeo & Juliet" gets Play Title style.

**Code:**
```python
def _create_play_title_style(self, doc: Document):
    """Create Play Title character style (bold italic for productions)"""
    style = doc.styles.add_style('Play Title', WD_STYLE_TYPE.CHARACTER)
    style.font.bold = True
    style.font.italic = True
```

#### Institution

**Purpose:** Names of schools, universities, companies, organizations

**Visual properties:**
- Weight: Bold
- Inherits size, color, and font from paragraph

**Usage frequency:** ~100 times per document

**Consolidates:** `ss2505`, `ss93858`, `ss2543`, `ss138597` (4 original styles)

**When applied:**
- School names in education
- Employer names in experience
- Theater company names
- Conference names
- Organization names

**Example:**
```
2023 - Present California State University Long Beach
               Interim Associate Dean
```

"California State University Long Beach" gets Institution style (bold).

**Code:**
```python
def _create_institution_style(self, doc: Document):
    """Create Institution character style (bold for institution names)"""
    style = doc.styles.add_style('Institution', WD_STYLE_TYPE.CHARACTER)
    style.font.bold = True
```

#### Job Title

**Purpose:** Position titles, roles, appointments

**Visual properties:**
- Weight: Bold Italic
- Inherits size, color, and font from paragraph

**Usage frequency:** ~50 times per document

**Consolidates:** `ss2592`, `ss2508` (2 original styles)

**Semantic distinction:**
Identical appearance to Play Title (bold italic) but different meaning:
- Job Title: "Interim Associate Dean" (employment position)
- Play Title: "Romeo & Juliet" (artistic work)

**Context matters:**
Claude determines which style based on what comes before/after:
- After institution name → likely Job Title
- In directing credits section → likely Play Title

**Example:**
```
2023 - Present California State University Long Beach
               Interim Associate Dean for Student Success
```

"Interim Associate Dean for Student Success" gets Job Title style.

**Code:**
```python
def _create_job_title_style(self, doc: Document):
    """Create Job Title character style (bold italic for positions)"""
    style = doc.styles.add_style('Job Title', WD_STYLE_TYPE.CHARACTER)
    style.font.bold = True
    style.font.italic = True
```

#### Orange Emphasis

**Purpose:** Highlight specific terms, awards, key information

**Visual properties:**
- Weight: Bold
- Color: Orange (#FF6D49)
- Inherits size and font from paragraph

**Usage frequency:** ~20 times per document (sparingly used for impact)

**Consolidates:** `ss2555`, `ss2561`, `ss40405`, `ss52919` (4 original styles)

**When to use (sparingly):**
- Award names
- Grant amounts
- Special recognitions
- Key terms in context

**Example:**
```
Recipient of Excellence in Teaching Award from CSULB (2022)
```

"Excellence in Teaching Award" could get Orange Emphasis for visual pop.

**Usage principle:**
Less is more - orange draws the eye, so use it only for truly important items. Overuse diminishes impact.

**Code:**
```python
def _create_orange_emphasis_style(self, doc: Document):
    """Create Orange Emphasis character style"""
    style = doc.styles.add_style('Orange Emphasis', WD_STYLE_TYPE.CHARACTER)
    style.font.bold = True
    style.font.color.rgb = self.ORANGE_RGB  # RGBColor(255, 109, 73)
```

#### Gray Text

**Purpose:** Dates, secondary information, de-emphasized content

**Visual properties:**
- Color: Gray (#808080)
- Inherits size, weight, and font from paragraph

**Usage frequency:** ~50 times per document

**Consolidates:** `ss2507`, `ss40419`, `ss8153`, `ss8151` (4 original styles)

**When to use:**
- Year of publication
- Committee membership years
- Dates within text
- Parenthetical details
- Supplementary information

**Example:**
```
Published in Theatre Journal (2018)
Graduate Studies Committee (ex-officio, 2020-present)
```

"(2018)" and "(ex-officio, 2020-present)" get Gray Text style.

**Visual effect:**
Gray recedes visually, keeping information available but not prominent.

**Code:**
```python
def _create_gray_text_style(self, doc: Document):
    """Create Gray Text character style (dates, secondary info)"""
    style = doc.styles.add_style('Gray Text', WD_STYLE_TYPE.CHARACTER)
    style.font.color.rgb = self.GRAY_RGB  # RGBColor(128, 128, 128)
```

## Style Usage Patterns

### Paragraph vs Character Styles

**Paragraph styles** apply to entire paragraphs:
```python
# Entire paragraph is "Section Header"
doc.add_paragraph("EDUCATION", style="Section Header")
```

**Character styles** apply within paragraphs:
```python
# Paragraph is "Timeline Entry", with Institution style inline
para = doc.add_paragraph(style="Timeline Entry")
para.add_run("2023 - Present ")
para.add_run("California State University Long Beach").style = "Institution"
```

### Common Combinations

#### Timeline with Institution
```
[Timeline Entry paragraph style]
2023 - Present [Institution character style]California State University Long Beach
```

#### Timeline with Institution and Job Title
```
[Timeline Entry paragraph style]
2023 - Present [Institution]California State University Long Beach
[Timeline Entry paragraph style]
[Job Title]Interim Associate Dean[/Job Title] for Student Success
```

#### Production Credit with Play Title
```
[Timeline Entry paragraph style]
[Play Title]Romeo & Juliet[/Play Title] - [Institution]California Shakespeare Theater[/Institution], [Gray Text](2019)[/Gray Text]
```

#### Body Text with Emphasis
```
[Body Text paragraph style]
Recipient of [Orange Emphasis]Excellence in Teaching Award[/Orange Emphasis] from CSULB [Gray Text](2022)[/Gray Text]
```

## Template Generation Process

### How the Template is Created

**Step 1: Style Analysis**
```bash
# Original CV had 97 styles with cryptic names
# analyze_cv_styles.py extracted usage patterns:
ss2578: 468 uses (bold italic - play titles)
ps2548: 85 uses (body text)
ps40376: 254 uses (bullets)
...
```

**Step 2: Consolidation Mapping**
```python
# cv_formatting/style_mapping.py
STYLE_CONSOLIDATION = {
    'ss2578': 'Play Title',
    'ss40454': 'Play Title',  # duplicate
    'ss2547': 'Play Title',   # duplicate

    'ps2548': 'Body Text',
    'ps81934': 'Body Text',   # duplicate
    'ps2597': 'Body Text',    # duplicate
    ...
}
```

**Step 3: Template Building**
```python
# cv_formatting/template_builder.py
class TemplateBuilder:
    def create_template(self, output_path):
        doc = Document()

        # Create all 12 styles
        self._create_cv_name_style(doc)
        self._create_section_header_style(doc)
        self._create_body_text_style(doc)
        ...

        doc.save(output_path)
```

**Step 4: Generation Script**
```bash
python generate_cv_template.py
# Creates: ~/.claude/skills/career/format-resume/cv-template.docx
```

**Step 5: Validation**
```bash
python validate_template.py
# Checks:
# ✓ All 12 styles present
# ✓ Properties correct (colors, fonts, indents)
# ✓ Template opens successfully
```

### Regenerating the Template

If you need to regenerate (after modifying style properties):

```bash
cd /path/to/career-lexicon-builder

# Modify template builder if needed
nano cv_formatting/template_builder.py

# Regenerate
python generate_cv_template.py

# Validate
python validate_template.py

# Output:
# ✓ Template exists: ~/.claude/skills/career/format-resume/cv-template.docx
# ✓ Template opens successfully
# ✓ All 12 semantic styles present
# ✓ Section Header: bold orange
# ✓ Timeline Entry: has hanging indent
# ✓ Play Title: bold italic
# ✓ Template validation PASSED (3/3 checks)
```

## Customization Guide

### Changing Colors

**Change section header color from orange to blue:**

Edit `cv_formatting/template_builder.py`:

```python
class TemplateBuilder:
    # Change this:
    ORANGE_RGB = RGBColor(255, 109, 73)  # Orange

    # To this:
    ORANGE_RGB = RGBColor(0, 102, 204)   # Blue
```

Regenerate:
```bash
python generate_cv_template.py
```

### Changing Fonts

**Change from Helvetica to Arial:**

Edit `cv_formatting/template_builder.py`, modify all `style.font.name = 'Helvetica'` to `style.font.name = 'Arial'`.

Or change specific styles:

```python
def _create_section_header_style(self, doc: Document):
    style = doc.styles.add_style('Section Header', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Georgia'  # Serif for headers
    style.font.size = Pt(10)
    style.font.bold = True
    style.font.color.rgb = self.ORANGE_RGB
```

### Changing Sizes

**Make section headers larger:**

```python
def _create_section_header_style(self, doc: Document):
    style = doc.styles.add_style('Section Header', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(12)  # Changed from 10pt to 12pt
    style.font.bold = True
    style.font.color.rgb = self.ORANGE_RGB
```

### Changing Indents

**Change hanging indent from 72pt (1 inch) to 54pt (0.75 inch):**

```python
def _create_timeline_entry_style(self, doc: Document):
    style = doc.styles.add_style('Timeline Entry', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = 'Helvetica'
    style.font.size = Pt(9)

    # Changed from 72pt to 54pt
    style.paragraph_format.left_indent = Pt(54)
    style.paragraph_format.first_line_indent = Pt(-54)
```

### Adding New Styles

**Add a new style (e.g., "Award Title"):**

1. Add creation method:
```python
def _create_award_title_style(self, doc: Document):
    """Create Award Title character style"""
    style = doc.styles.add_style('Award Title', WD_STYLE_TYPE.CHARACTER)
    style.font.bold = True
    style.font.italic = True
    style.font.color.rgb = self.ORANGE_RGB
```

2. Call it in `create_template`:
```python
def create_template(self, output_path: str) -> bool:
    doc = Document()

    # Existing styles
    self._create_cv_name_style(doc)
    ...

    # New style
    self._create_award_title_style(doc)

    doc.save(output_path)
```

3. Regenerate template
4. Update Claude's style-mappings.yaml to use it

## Technical Details

### File Format

The template is a standard Office Open XML (.docx) file.

**Structure:**
```
cv-template.docx
├── [Content_Types].xml
├── _rels/
├── word/
│   ├── document.xml         # Main document
│   ├── styles.xml           # Style definitions (our 12 styles!)
│   ├── settings.xml
│   ├── fontTable.xml
│   └── ...
└── docProps/
```

**Our styles live in:** `word/styles.xml`

### python-docx Integration

We use the `python-docx` library to create and manipulate .docx files programmatically.

**Key classes:**
```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE

# Create document
doc = Document()

# Add paragraph style
style = doc.styles.add_style('My Style', WD_STYLE_TYPE.PARAGRAPH)
style.font.name = 'Helvetica'
style.font.size = Pt(12)

# Add character style
char_style = doc.styles.add_style('My Char Style', WD_STYLE_TYPE.CHARACTER)
char_style.font.bold = True

# Use styles
para = doc.add_paragraph("Text", style='My Style')
run = para.add_run("emphasized")
run.style = 'My Char Style'
```

### Style Inheritance

Word has a style inheritance system. Our template leverages this:

**Body Text:**
Built-in Word style that other styles can inherit from. We modify it rather than creating a new one.

**Custom styles:**
Created fresh without inheritance to ensure consistent behavior across Word versions.

### Validation

Template validation checks:

1. **Existence:** File exists at expected path
2. **Openability:** Can be opened by python-docx
3. **Completeness:** All 12 styles present
4. **Properties:** Key styles have expected formatting

**Validation code:**
```python
def validate_template(template_path):
    doc = Document(str(template_path))

    # Check all styles present
    style_names = {s.name for s in doc.styles}
    expected = get_all_semantic_styles()

    missing = expected - style_names
    if missing:
        raise ValidationError(f"Missing styles: {missing}")

    # Check properties
    section_header = doc.styles['Section Header']
    assert section_header.font.bold == True
    assert section_header.font.color.rgb is not None

    return True
```

## Troubleshooting

### Template not generating

**Error:**
```
Failed to create template: Permission denied
```

**Solution:**
Skill directory doesn't exist. Create it:
```bash
mkdir -p ~/.claude/skills/career/format-resume
```

### Styles missing in generated document

**Error:**
```
KeyError: 'Play Title' style not found
```

**Cause:**
Template is out of date or corrupted.

**Solution:**
Regenerate template:
```bash
python generate_cv_template.py
python validate_template.py
```

### Custom fonts not showing

**Issue:**
Changed font to "Times New Roman" but still seeing Helvetica.

**Cause:**
Font must be installed on system and spelled exactly right.

**Solution:**
1. Check available fonts:
```python
from docx import Document
doc = Document()
# Font names must exactly match system fonts
```

2. Use common fonts: Helvetica, Arial, Times New Roman, Georgia

### Colors not appearing correctly

**Issue:**
Orange color showing as black.

**Cause:**
RGBColor values out of range (0-255).

**Solution:**
```python
# Wrong:
RGBColor(300, 109, 73)  # 300 is invalid

# Right:
RGBColor(255, 109, 73)  # Valid range: 0-255
```

## Style Reference Quick Sheet

| Style Name | Type | Visual | When to Use |
|------------|------|--------|-------------|
| CV Name | Para | 13pt bold black | Your name only |
| Section Header | Para | 10pt bold orange | EDUCATION, EXPERIENCE |
| Body Text | Para | 9pt regular black | Descriptions, details |
| Timeline Entry | Para | 9pt with indent | Date ranges + institutions |
| Bullet Standard | Para | 9pt black bullet | Regular lists |
| Bullet Gray | Para | 9pt gray bullet | Secondary details |
| Bullet Emphasis | Para | 9pt bold italic bullet | Key achievements |
| Play Title | Char | Bold italic | Theatrical works |
| Institution | Char | Bold | School/company names |
| Job Title | Char | Bold italic | Position titles |
| Orange Emphasis | Char | Bold orange | Highlighted terms |
| Gray Text | Char | Gray | Dates, parentheticals |

**Legend:**
- Para = Paragraph style (entire paragraph)
- Char = Character style (inline text)

## Related Documentation

- [format-resume-skill-guide.md](format-resume-skill-guide.md) - How to use the formatting skill
- [../TEMPLATE_GENERATION.md](../TEMPLATE_GENERATION.md) - Technical generation details
- [../plans/2025-11-09-cv-style-extraction-and-formatting-design.md](../plans/2025-11-09-cv-style-extraction-and-formatting-design.md) - System design
