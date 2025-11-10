# Format Resume Skill Guide

A comprehensive guide to using the intelligent CV formatting system.

## What Is This?

The format-resume skill is an intelligent document formatting system that understands the **semantic meaning** of your CV content, not just its visual appearance. It knows the difference between "Romeo & Juliet" (a play title) and "Interim Dean" (a job title), even though both might be bold italic in the final document.

**Key capabilities:**
- Semantic understanding of content context
- Professional styling with 12 clean, purpose-built styles
- Visual preview workflow (PDF + images)
- Learning system that remembers your corrections

## Quick Start

### Basic Usage

In Claude Code, simply say:

```
Format this CV: [paste your CV content]
```

Or if you have a file:

```
Format the CV in my-cv-draft.txt
```

Claude will:
1. Analyze your content semantically
2. Show you the proposed formatting
3. Generate a formatted .docx document
4. Create a visual preview for review
5. Learn from any corrections you make

## How It Works

### Step 1: Semantic Analysis

Claude analyzes your content to understand what each element represents:

**Example input:**
```
Anthony Byrnes

EDUCATION

1994-1997 California Institute of the Arts
Master of Fine Arts, Acting

PROFESSIONAL EXPERIENCE

2023 - Present California State University Long Beach
Interim Associate Dean for Student Success and Outreach
Oversee 12 department-based staff academic advisors.

SELECTED DIRECTING CREDITS

Romeo & Juliet - California Shakespeare Theater
Macbeth - Oregon Shakespeare Festival
```

**Claude's analysis:**
```
Line 1: "Anthony Byrnes"
  → CV Name (first line, short, proper name pattern)

Line 2: "EDUCATION"
  → Section Header (all caps, section divider)

Line 3: "1994-1997 California Institute of the Arts"
  → Timeline Entry (date range pattern)
  → Inline: "California Institute of the Arts" → Institution (school name)

Line 4: "Master of Fine Arts, Acting"
  → Body Text (degree detail under education)

Line 5: "PROFESSIONAL EXPERIENCE"
  → Section Header (all caps, section divider)

Line 6: "2023 - Present California State University Long Beach"
  → Timeline Entry (date range pattern)
  → Inline: "California State University Long Beach" → Institution (employer)

Line 7: "Interim Associate Dean for Student Success and Outreach"
  → Timeline Entry with inline Job Title styling
  → Context: follows employer, indicates position

Line 8: "Oversee 12 department-based staff academic advisors."
  → Body Text (responsibility under job)

Line 9: "SELECTED DIRECTING CREDITS"
  → Section Header (all caps, section divider)

Line 10: "Romeo & Juliet - California Shakespeare Theater"
  → Timeline Entry
  → Inline: "Romeo & Juliet" → Play Title (NOT Job Title!)
  → Context: in artistic works section, follows pattern of theatrical productions
```

**Why this matters:**

Traditional formatting tools would see "Interim Associate Dean" and "Romeo & Juliet" as identical (both bold italic) and format them the same way. Claude understands that one is a job title following an employer, and the other is a play title in a productions section, and styles them appropriately for their semantic meaning.

### Step 2: Confirmation

Claude shows you the analysis and asks: "Does this look right?"

**If yes:** Say "yes" and Claude proceeds to generate the document.

**If corrections needed:** Point out what's wrong:
- "Line 8 should be a bullet point, not body text"
- "Committee roles should be gray text"
- "That's a play title, not a job title"

Claude will update the analysis and remember your preference for next time.

### Step 3: Document Generation

Claude creates your formatted .docx using the clean template with 12 semantic styles.

Behind the scenes, Claude:
1. Converts the analysis to a JSON content mapping
2. Calls the Python style applicator
3. Generates the formatted document

**Example output structure:**
```json
[
  {
    "text": "Anthony Byrnes",
    "style": "CV Name",
    "type": "paragraph"
  },
  {
    "text": "EDUCATION",
    "style": "Section Header",
    "type": "paragraph"
  },
  {
    "text": "1994-1997 California Institute of the Arts",
    "style": "Timeline Entry",
    "type": "paragraph",
    "runs": [
      {"text": "1994-1997 ", "style": null},
      {"text": "California Institute of the Arts", "style": "Institution"}
    ]
  }
]
```

### Step 4: Visual Preview

Claude converts your document to PDF and generates page images so you can see exactly how it looks.

**Preview workflow:**
1. .docx → PDF (using LibreOffice)
2. PDF → JPEG images (using Poppler)
3. Claude displays the images for your review

**If LibreOffice or Poppler unavailable:**
Claude will skip the preview and just provide the .docx file. You can still open it manually to review.

### Step 5: Review and Refinement

You review the preview and can request changes:

**Common refinements:**
- "Make committee roles gray text instead of body text"
- "Those should be bullet points"
- "Add more space after section headers"
- "The dates should be lighter gray"

Claude will regenerate the document with your corrections.

### Step 6: Learning

If you made corrections, Claude automatically updates the learning system:

**Example learned preference:**
```yaml
rules:
  - pattern: "committee|advisory board"
    context: "university service section"
    preferred_style: "Gray Text"
    learned_date: "2025-11-10"
    example: "Graduate Studies Advisory Committee"
    reasoning: "User indicated committee roles should be gray text"
```

**Next time you format a CV:**
Claude will automatically apply gray text to committee roles without asking. No manual "save preferences" button needed.

## The 12 Semantic Styles

Understanding what each style means and when to use it:

### Paragraph Styles

These apply to entire paragraphs and control structure:

#### 1. CV Name
**Purpose:** Your name at the top of the CV
**Formatting:** 13pt Helvetica, bold, black
**When used:** First line only, for your name

**Example:**
```
Anthony Byrnes
```

#### 2. Section Header
**Purpose:** Major section dividers
**Formatting:** 10pt Helvetica, bold, orange (#FF6D49)
**When used:** All-caps section titles

**Examples:**
```
EDUCATION
PROFESSIONAL EXPERIENCE
SELECTED DIRECTING CREDITS
PUBLICATIONS
```

#### 3. Body Text
**Purpose:** Standard paragraph content
**Formatting:** 9pt Helvetica, regular, black
**When used:** Descriptions, responsibilities, details under jobs/education

**Examples:**
```
Master of Fine Arts, Acting
Oversee 12 department-based staff academic advisors.
Developed curriculum for new theater program.
```

#### 4. Timeline Entry
**Purpose:** Date ranges with institutions
**Formatting:** 9pt Helvetica, 72pt hanging indent
**When used:** Entries with date ranges and institution/employer names

**Examples:**
```
2023 - Present California State University Long Beach
1994-1997 California Institute of the Arts
2015-2020 Oregon Shakespeare Festival
```

**Note:** Often combined with inline character styles (Institution, Job Title, Play Title)

#### 5. Bullet Standard
**Purpose:** Regular bullet lists
**Formatting:** 9pt Helvetica, 72pt left indent, black
**When used:** Standard lists of items, achievements, responsibilities

**Examples:**
```
• Developed strategic plan for student success initiatives
• Led team of 12 academic advisors across departments
• Increased student retention by 15% over two years
```

#### 6. Bullet Gray
**Purpose:** Secondary information bullets
**Formatting:** 9pt Helvetica, gray color, 72pt left indent
**When used:** Dates in education, secondary details, course lists

**Examples:**
```
• Degree conferred May 1997
• Thesis: "Stanislavski in Contemporary Practice"
• Relevant coursework: Voice, Movement, Alexander Technique
```

#### 7. Bullet Emphasis
**Purpose:** Highlighted bullet items
**Formatting:** 9pt Helvetica, bold italic, 72pt left indent
**When used:** Key achievements, awards, important highlights

**Examples:**
```
• Recipient of Outstanding Faculty Award 2022
• Published in Theatre Journal (peer-reviewed)
• Keynote speaker at National Theatre Conference
```

### Character Styles (Inline)

These apply to specific text within paragraphs:

#### 8. Play Title
**Purpose:** Titles of theatrical productions, artistic works
**Formatting:** Bold italic
**When used:** Names of plays, operas, productions in directing/performance credits

**Examples:**
- "Romeo & Juliet" - California Shakespeare Theater
- "The Tempest" - Oregon Shakespeare Festival
- "West Side Story" - Broadway National Tour

**Key distinction:** Even though it's bold italic like Job Title, it's used in artistic works context.

#### 9. Institution
**Purpose:** Names of schools, universities, companies
**Formatting:** Bold only
**When used:** Organization names in timeline entries

**Examples:**
- California Institute of the **Arts**
- **California State University** Long Beach
- **Oregon Shakespeare Festival**

#### 10. Job Title
**Purpose:** Position titles and roles
**Formatting:** Bold italic
**When used:** Your title/position at an organization

**Examples:**
- **Interim Associate Dean** for Student Success
- **Assistant Professor** of Theatre
- **Director of Education**

**Key distinction:** Even though it's bold italic like Play Title, it's used for employment positions.

#### 11. Orange Emphasis
**Purpose:** Highlight specific text for attention
**Formatting:** Bold, orange (#FF6D49)
**When used:** Awards, special recognitions, key terms

**Examples:**
- Recipient of **Excellence in Teaching Award**
- **$500K grant** from National Endowment for the Arts
- **First-generation college student** advocate

#### 12. Gray Text
**Purpose:** Dates, secondary information, de-emphasized content
**Formatting:** Gray color
**When used:** Year ranges, committee roles, supplementary details

**Examples:**
- Published in Theatre Journal (**2018**)
- Graduate Studies Advisory Committee (**ex-officio member**)
- (**ongoing since 2015**)

## Common Use Cases

### Use Case 1: Academic CV (Theater/Arts Focus)

**Input:**
```
Anthony Byrnes

PROFESSIONAL EXPERIENCE

2023 - Present California State University Long Beach
Interim Associate Dean for Student Success and Outreach
Oversee 12 department-based staff academic advisors.

SELECTED DIRECTING CREDITS

Romeo & Juliet - California Shakespeare Theater, 2019
```

**Claude's understanding:**
- "Romeo & Juliet" is in SELECTED DIRECTING CREDITS section
- Context indicates this is an artistic work, not a job
- Apply Play Title style (bold italic) for semantic correctness
- Even though "Interim Associate Dean" is also bold italic, they're different contexts

**Result:**
Both are bold italic visually, but semantically tagged correctly for context.

### Use Case 2: Traditional Academic CV

**Input:**
```
EDUCATION

2019-2023 Stanford University
Ph.D., Computer Science
Dissertation: "Machine Learning for Natural Language Understanding"
Advisor: Dr. Jane Smith

PUBLICATIONS

"Attention Mechanisms in Neural Networks" - Journal of AI Research, 2022
```

**Claude's understanding:**
- "Stanford University" → Institution style (bold)
- "Ph.D., Computer Science" → Body Text (degree details)
- Dissertation and Advisor → Body Text (not special formatting)
- Publication title → could be Play Title style if emphasized, or leave in Body Text
- Journal name → could be Institution style or Orange Emphasis

**Interactive refinement:**
You might say: "Make journal names orange" and Claude learns this preference.

### Use Case 3: Hybrid Professional/Academic CV

**Input:**
```
PROFESSIONAL EXPERIENCE

2020 - Present Tech Startup Inc
Chief Technology Officer
Lead engineering team of 50+ developers.

BOARD MEMBERSHIPS

Graduate Studies Advisory Committee, Stanford University (ex-officio)
Technology Advisory Board, MIT (appointed 2022)
```

**Claude's understanding:**
- Job title → Job Title style
- Company name → Institution style
- Board memberships → Could be Body Text or Gray Text
- You might correct: "Committee roles should be gray text"
- Claude learns: committee/board roles → Gray Text for future CVs

### Use Case 4: Correcting Ambiguous Content

**Scenario:** Claude isn't sure if something is a play title or job title.

**Claude says:**
"I'm analyzing line 15: 'Hamlet'. This appears after 'Director of' but could be either:
- A job title: Director of Hamlet (bold italic as Job Title)
- A play title: Director of [production] Hamlet (bold italic as Play Title)

Which is correct?"

**You respond:**
"It's a play title - I was the director of the production."

**Claude:**
- Updates the formatting
- Saves this as a learned pattern
- Next time: "Director of [Title]" → recognizes as play title

## Troubleshooting

### Problem: Template not found

**Error message:**
```
Template not found: ~/.claude/skills/career/format-resume/cv-template.docx
Run generate_cv_template.py first
```

**Solution:**
The template hasn't been generated yet. Run:
```bash
cd /path/to/career-lexicon-builder
python generate_cv_template.py
```

This creates the clean template with 12 semantic styles.

### Problem: PDF preview not available

**Message:**
```
PDF conversion: skipped (LibreOffice not available)
```

**Solution:**
Install LibreOffice for PDF conversion:
```bash
brew install libreoffice
```

**Alternative:**
You can still use the system without previews. Just open the .docx file manually in Word or Pages to review.

### Problem: Image generation skipped

**Message:**
```
Image generation: skipped (pdftoppm not available)
```

**Solution:**
Install Poppler for PDF-to-image conversion:
```bash
brew install poppler
```

**Alternative:**
You can review the PDF directly without page images.

### Problem: Formatting doesn't match my style preferences

**Issue:** Claude is applying styles you don't like.

**Solution:**
Just tell Claude what you prefer:
- "Committee roles should be gray text"
- "Make all dates lighter gray"
- "Section headers should be black, not orange"

Claude will:
1. Regenerate with your corrections
2. Save your preferences
3. Apply them automatically next time

### Problem: Content is being misclassified

**Example:** Claude thinks "Hamlet" is a job title, not a play title.

**Solution:**
Provide context in your correction:
"'Hamlet' is a play title, not a job title. I was directing the production."

Claude will:
- Fix the current document
- Learn the pattern for future use
- Ask clarifying questions if uncertain next time

### Problem: Want to start fresh (clear learned preferences)

**Solution:**
Delete or rename the learned preferences file:
```bash
mv ~/.claude/skills/career/format-resume/learned-preferences.yaml \
   ~/.claude/skills/career/format-resume/learned-preferences.yaml.backup
```

Create new empty file:
```bash
cat > ~/.claude/skills/career/format-resume/learned-preferences.yaml << EOF
version: 1.0
last_updated: null
rules: []
EOF
```

## Advanced Usage

### Customizing the Template

If you want to modify the base styles (colors, fonts, sizes):

1. Edit the template builder:
```bash
nano /path/to/career-lexicon-builder/cv_formatting/template_builder.py
```

2. Modify style properties (example - change orange to blue):
```python
# Change this:
ORANGE_RGB = RGBColor(255, 109, 73)

# To this:
ORANGE_RGB = RGBColor(0, 102, 204)  # Blue
```

3. Regenerate the template:
```bash
python generate_cv_template.py
```

4. Validate it works:
```bash
python validate_template.py
```

### Understanding the Learning System

Learned preferences are stored in YAML format:

**File location:**
```
~/.claude/skills/career/format-resume/learned-preferences.yaml
```

**Example contents:**
```yaml
version: 1.0
last_updated: "2025-11-10"
rules:
  - pattern: "committee|advisory"
    context: "service section"
    preferred_style: "Gray Text"
    learned_date: "2025-11-10"
    example: "Graduate Studies Advisory Committee"

  - pattern: "director of [title]"
    context: "after production context"
    preferred_style: "Play Title"
    learned_date: "2025-11-10"
    example: "Director of Hamlet"
```

**How it works:**
1. When you correct a formatting decision, Claude extracts the pattern
2. Pattern includes the text, context, and your preferred style
3. Saved with example and date for reference
4. Next time similar content appears, Claude applies your preference automatically

### Direct CLI Usage (Advanced)

You can use the formatting tools directly without the Claude skill:

**Step 1: Create content mapping JSON:**
```json
[
  {
    "text": "Anthony Byrnes",
    "style": "CV Name",
    "type": "paragraph"
  },
  {
    "text": "EDUCATION",
    "style": "Section Header",
    "type": "paragraph"
  }
]
```

**Step 2: Format document:**
```bash
python format_cv.py input.json output.docx --preview
```

**Step 3: Review output:**
```bash
open output.docx
open output_images/page-1.jpg
```

This is useful for:
- Batch processing multiple CVs
- Integration with other tools
- Automation scripts

## Tips and Best Practices

### 1. Start with Complete Content

Format your complete CV content at once rather than section by section. This gives Claude full context for semantic understanding.

**Good:**
```
Format this complete CV: [entire CV content]
```

**Less ideal:**
```
Format this education section: [just education]
[then later] Format this experience section: [just experience]
```

### 2. Use Clear Section Headers

Claude relies on section headers to understand context.

**Good:**
```
SELECTED DIRECTING CREDITS
Romeo & Juliet - California Shakespeare Theater
```

**Ambiguous:**
```
Theater Work:
Romeo & Juliet - California Shakespeare Theater
```

### 3. Provide Context When Correcting

Help Claude learn by explaining your corrections.

**Good correction:**
"Committee roles should be gray text because they're secondary activities, not primary positions."

**Less helpful:**
"Make this gray."

### 4. Review the Preview Carefully

The visual preview is your chance to catch formatting issues before finalizing.

**Check:**
- Are section headers the right color and weight?
- Are institution names bold?
- Are play titles vs job titles styled correctly?
- Is spacing consistent?
- Are bullets aligned properly?

### 5. Build Your Preference Library

The more you use the system, the smarter it becomes.

**First CV:** Might require several corrections
**Second CV:** Fewer corrections needed
**Third CV:** Mostly automatic, just minor tweaks

### 6. Keep Source Content Clean

Claude works best with clean, structured input.

**Good input:**
```
2023 - Present California State University Long Beach
Interim Associate Dean for Student Success
```

**Harder to parse:**
```
2023-present: CSULB - interim associate dean (student success)
```

### 7. Use Consistent Date Formats

Pick a date format and stick with it.

**Consistent:**
```
2020 - 2023 Stanford University
2015 - 2020 Harvard University
2010 - 2015 MIT
```

**Inconsistent:**
```
2020-2023 Stanford University
2015 to 2020 Harvard University
2010-15 MIT
```

## Examples from Real Usage

### Example 1: Theater Professional CV

**Input snippet:**
```
SELECTED DIRECTING CREDITS

Romeo & Juliet - California Shakespeare Theater, 2019
The Tempest - Oregon Shakespeare Festival, 2018
West Side Story - Broadway National Tour, 2017

PROFESSIONAL EXPERIENCE

2020 - Present Oregon Shakespeare Festival
Director of Education and Community Programs
Oversee educational programming for 50,000 students annually.
```

**Claude's analysis:**
- Section: "SELECTED DIRECTING CREDITS" → Section Header (orange, bold)
- "Romeo & Juliet" → Play Title (bold italic, in productions context)
- "The Tempest" → Play Title (bold italic, in productions context)
- "West Side Story" → Play Title (bold italic, in productions context)
- Section: "PROFESSIONAL EXPERIENCE" → Section Header (orange, bold)
- "Oregon Shakespeare Festival" → Institution (bold)
- "Director of Education and Community Programs" → Job Title (bold italic, follows employer)
- "Oversee educational..." → Body Text (responsibility)

**Key insight:** Even though both play titles and the job title are bold italic, Claude correctly distinguishes them by context.

### Example 2: Academic CV with Publications

**Input snippet:**
```
PUBLICATIONS

"Machine Learning Approaches to Natural Language" - Journal of AI Research, 2022
"Neural Networks in Practice" - Conference on ML, 2021

SERVICE

Graduate Studies Committee, Computer Science Department (2020-present)
Diversity and Inclusion Task Force (chair, 2021-2023)
```

**User correction:**
"Committee roles should be gray text"

**Claude's response:**
- Updates current formatting
- Saves learned preference:
  ```yaml
  - pattern: "committee|task force"
    context: "service section"
    preferred_style: "Gray Text"
  ```

**Next CV:** Automatically applies gray to committee roles without asking.

## Frequently Asked Questions

### Q: Can I use this for cover letters too?

**A:** The current system is optimized for CV/resume formatting. Cover letters have different structural patterns (paragraphs vs timeline entries, no section headers). You could use it, but you'd likely need to correct more assumptions.

**Better approach:** Use the collaborative-writing skill for cover letters, which is designed for narrative prose.

### Q: What if I want more than 12 styles?

**A:** The 12 styles were carefully chosen to cover 97% of actual CV formatting needs, consolidating from 97 original .pages styles. Adding more styles increases complexity without much benefit.

**If you really need more:**
1. Edit `cv_formatting/template_builder.py`
2. Add new style methods
3. Regenerate template with `python generate_cv_template.py`

### Q: Can I share my learned preferences with colleagues?

**A:** Yes! The learned preferences file is just YAML:

```bash
# Export your preferences
cp ~/.claude/skills/career/format-resume/learned-preferences.yaml \
   ~/my-cv-preferences.yaml

# Share with colleague
# They copy to their skill directory
cp ~/my-cv-preferences.yaml \
   ~/.claude/skills/career/format-resume/learned-preferences.yaml
```

### Q: Does this work with .pages or .pdf input?

**A:** Currently the skill works with plain text or markdown input. If you have a .pages or .pdf CV:

1. Extract the text (copy-paste or use text extraction tool)
2. Clean up the formatting
3. Paste into Claude for formatting

**Future enhancement:** Could add .pages/.pdf parsing to extract and reformat.

### Q: How accurate is the semantic analysis?

**A:** Very accurate for structured CVs with clear section headers. Claude uses:
- Pattern matching (date ranges, all-caps headers)
- Context understanding (what section we're in)
- Semantic reasoning (is this a job or a play?)
- Your learned preferences

**Accuracy improves with:**
- Clear section headers
- Consistent formatting in input
- Your corrections (builds preference library)

### Q: Can I use this without Claude Code?

**A:** Yes, but you'll need to do the semantic analysis manually:

1. Create the content mapping JSON yourself
2. Run `python format_cv.py mapping.json output.docx --preview`

The Claude skill just automates the semantic analysis step.

### Q: What about multi-page CVs?

**A:** Works perfectly! The template doesn't have page limits. Claude formats the content, and it flows across multiple pages naturally. The preview will show all pages.

### Q: Can I export to formats other than .docx?

**A:** The primary output is .docx because it preserves all style information. However:

**PDF:** Automatically generated with `--preview` flag
**HTML:** Could export from .docx using LibreOffice
**Pages:** Import .docx into Pages
**LaTeX:** Would need custom exporter (not currently supported)

## Getting Help

If you encounter issues or have questions:

1. **Check this guide** - Most common issues are covered in Troubleshooting
2. **Review the design doc** - `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`
3. **Check template generation** - `docs/TEMPLATE_GENERATION.md`
4. **Inspect learned preferences** - `~/.claude/skills/career/format-resume/learned-preferences.yaml`

## Related Documentation

- [cv-template-guide.md](cv-template-guide.md) - Deep dive into the 12 styles
- [../TEMPLATE_GENERATION.md](../TEMPLATE_GENERATION.md) - Technical details
- [../plans/2025-11-09-cv-style-extraction-and-formatting-design.md](../plans/2025-11-09-cv-style-extraction-and-formatting-design.md) - System design
