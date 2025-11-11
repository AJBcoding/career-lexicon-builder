# Format Cover Letter Skill Guide

Comprehensive guide to formatting cover letters with semantic styling using the `format-cover-letter` Claude skill.

## Quick Start

**1. Invoke the skill:**
```
Format this cover letter: [paste your cover letter content]
```

**2. Claude analyzes structure:**
- Detects: date, salutation, section headers, body paragraphs, closing, signature
- Identifies: institutions, positions, productions mentioned

**3. Applies semantic styles:**
- Structural elements → appropriate paragraph styles
- Content mentions → character styles (bold, italic, etc.)

**4. Generates preview:**
- Creates formatted .docx
- Converts to PDF
- Shows images for visual validation

**5. Review and correct:**
- If any styling is wrong, tell Claude
- System learns and remembers your corrections

## Document Structure

### Date Line
```
November 25, 2024
```
- Right-aligned
- 11pt Helvetica
- First element in document

### Salutation
```
Dear Members of the Search Committee,
```
- Body Text style
- Standard paragraph formatting

### Body Paragraphs
```
I am writing to express my interest in the Associate Dean position.
At Center Theatre Group, I built the Kirk Douglas Theatre...
```
- Body Text style
- Inline character styles for mentions (bold institutions, italic titles, etc.)

### Thematic Section Headers
```
Why This Institution?

Enhancing Scholarship and Creative Practice
```
- Section Header style
- Black color, 13pt, Bold
- Different from CV headers (which are orange, 11pt)
- Narrative/essay headers, not categorical (like EDUCATION)

### Closing
```
Thank you for your consideration,
```
- Body Text style
- Precedes signature

### Signature
```
Anthony Byrnes
```
- Body Text style
- Your name only

## Content Mentions (Inline Styling)

### Institutions (Bold)
- **What**: Universities, organizations, companies
- **Examples**:
  - UCLA
  - Center Theatre Group
  - California State University Long Beach (CSULB)
- **How styled**: Bold

### Productions/Venues (Bold Italic)
- **What**: Play titles, theater names, creative works
- **Examples**:
  - Kirk Douglas Theatre
  - Romeo & Juliet
  - Geffen Playhouse
- **How styled**: Bold Italic

### Job Titles (Bold Italic)
- **What**: Positions held or mentioned
- **Examples**:
  - Associate Dean
  - Interim Associate Dean
  - Artistic Director
- **How styled**: Bold Italic

### Key Highlights (Bold Orange)
- **What**: Important achievements, statistics
- **Examples**:
  - $18 million project
  - 100+ new plays
  - 370% growth
- **How styled**: Bold, Orange (#FF6D49)

### Dates/Secondary Info (Gray)
- **What**: Parenthetical dates, supplementary information
- **Examples**:
  - (2010-2015)
  - 2024
- **How styled**: Gray text

## Example Usage

### Input
```
November 25, 2024

Dear Search Committee,

At Center Theatre Group, I stewarded the Kirk Douglas Theatre project.
As Interim Associate Dean at CSULB, I transformed our advising infrastructure.

Why This Institution?

The university's commitment aligns with my values during my tenure as
Associate Dean.

Thank you for your consideration,

Anthony Byrnes
```

### Styled Output
```
[Date Line]November 25, 2024[/Date Line]

[Body Text]Dear Search Committee,[/Body Text]

[Body Text]At [Institution]Center Theatre Group[/Institution], I stewarded the
[Play Title]Kirk Douglas Theatre[/Play Title] project. As [Job Title]Interim
Associate Dean[/Job Title] at [Institution]CSULB[/Institution], I transformed
our advising infrastructure.[/Body Text]

[Section Header]Why This Institution?[/Section Header]

[Body Text]The university's commitment aligns with my values during my tenure as
[Job Title]Associate Dean[/Job Title].[/Body Text]

[Body Text]Thank you for your consideration,[/Body Text]

[Body Text]Anthony Byrnes[/Body Text]
```

## Learning System

The skill learns from your corrections.

### Example Correction Flow

**User**: "Format this cover letter: ...at the Geffen Playhouse..."

**Claude**: Styles "Geffen Playhouse" as Play Title (bold italic)

**User**: "Actually, style 'Geffen Playhouse' as Institution"

**Claude**: Updates styling, saves preference

**Next time**: "Geffen Playhouse" automatically styled as Institution (bold)

### Viewing Learned Preferences

Preferences stored in: `~/.claude/skills/career/format-cover-letter/learned-preferences.yaml`

## Troubleshooting

### Section Header Wrong Color (Orange Instead of Black)

**Problem**: Section headers styled in orange (11pt) instead of black (13pt)

**Cause**: System detected document as CV, not cover letter

**Solution**:
- Ensure invoking `format-cover-letter` skill (not `format-resume`)
- Check that headers are thematic ("Why X?") not categorical ("EDUCATION")

### Date Not Right-Aligned

**Problem**: Date appears left-aligned

**Cause**: Date Line style not applied

**Solution**:
- Verify date is at top of document
- Format: "Month DD, YYYY" (e.g., "November 25, 2024")
- Tell Claude: "Apply Date Line style to the date"

### Institution Name Not Bold

**Problem**: University or organization name not styled

**Cause**: System may not recognize abbreviation or uncommon name

**Solution**:
- Provide correction: "Style 'CSULB' as Institution"
- System will learn and remember

### Production Title Not Italic

**Problem**: Play/venue name not styled correctly

**Cause**: System may not recognize less common titles

**Solution**:
- Provide correction: "Style 'Kirk Douglas Theatre' as Play Title"
- System will remember preference

### Job Title Not Styled

**Problem**: Position mentioned but not italicized

**Cause**: System may not recognize informal position names

**Solution**:
- Provide correction: "Style 'Interim Associate Dean' as Job Title"
- Include in future corrections

## Technical Details

### Shared Template
- Location: `cv_formatting/templates/career-documents-template.docx`
- Contains: 13 semantic styles
- Shared with: `format-resume` skill

### Python Formatter
- Script: `format_cv.py` (despite name, handles both CVs and cover letters)
- Flag: `--document-type=cover-letter`
- Example: `python format_cv.py input.md output.docx --document-type=cover-letter --preview`

### Preview Generation
- PDF: Generated via LibreOffice (if installed)
- Images: Generated via Poppler/pdftoppm (if installed)
- Graceful degradation if tools unavailable

## Comparison: Cover Letter vs CV Formatting

| Aspect | Cover Letter | CV |
|--------|--------------|-----|
| **Section Headers** | Black, 13pt, thematic | Orange, 11pt, domain |
| **Header Examples** | "Why UCLA?", "Transformational Philanthropy" | "EDUCATION", "EXPERIENCE", "SKILLS" |
| **Date Format** | Right-aligned Date Line | Inline with gray text |
| **Structure** | Narrative paragraphs | Categorical sections with bullets |
| **Timeline Entries** | Not used | 72pt hanging indent dates |
| **Overall Flow** | Essay-like, thematic | Structured, categorical |

**Content Mentions**: Same styles (Institution, Play Title, Job Title) in both document types

## FAQ

**Q: Can I use both format-resume and format-cover-letter skills in one session?**
A: Yes. They're independent skills sharing infrastructure. Invoke whichever matches your current document.

**Q: Do corrections in cover letter formatting affect CV formatting?**
A: No. Each skill maintains separate learned preferences. This prevents cross-contamination.

**Q: What if my cover letter doesn't have section headers?**
A: That's fine. The system is flexible. Just use salutation, body paragraphs, and closing. Section headers are optional.

**Q: Can I format multiple cover letters in one session?**
A: Yes. Each is formatted independently. Learned preferences apply to all.

**Q: Why are my cover letter section headers not orange like my CV?**
A: Intentional design. Thematic essay headers (Why UCLA?) use black for readability in longer narrative text. Domain headers (EDUCATION) use orange for visual pop in sectioned CVs.

**Q: Do I need separate templates for different cover letters?**
A: No. The 13-style template works for all cover letters. Consistency across your application materials is valuable.

**Q: Can I export to formats other than .docx?**
A: The primary output is .docx. The system generates PDF previews if LibreOffice is installed. Further export formats would require additional tools.

**Q: What if formatting fails or produces errors?**
A: Report the error to Claude. The system has graceful error handling. Most issues are due to:
  - Missing dependencies (LibreOffice for PDF, Poppler for images)
  - File permissions
  - Invalid input format

## Advanced Usage

### Customizing Style Mappings

Advanced users can edit: `~/.claude/skills/career/format-cover-letter/style-mappings.yaml`

**Warning**: Incorrect YAML can break skill functionality. Back up before editing.

### Viewing Style Application

To see exactly how styles are applied:

```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
source .venv/bin/activate
python format_cv.py --help
```

### Testing Changes

After modifying style mappings:

```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
source .venv/bin/activate
PYTHONPATH=. pytest tests/test_cover_letter_formatting.py -v
```

## Getting Help

**Skill not working?**
- Check that skill files exist: `ls ~/.claude/skills/career/format-cover-letter/`
- Verify template exists: `ls cv_formatting/templates/career-documents-template.docx`

**Styles not applying correctly?**
- Provide specific corrections to Claude
- System will learn and improve

**Need to see technical details?**
- Read: `~/.claude/skills/career/format-cover-letter/skill.md`
- View: `~/.claude/skills/career/format-cover-letter/style-mappings.yaml`

## Summary

The `format-cover-letter` skill provides semantic formatting for academic and professional cover letters:

✓ Detects structural elements automatically
✓ Styles content mentions consistently
✓ Context-aware formatting (black headers for cover letters)
✓ Learns from corrections
✓ Generates visual previews
✓ Shares infrastructure with `format-resume`

**Start using**: "Format this cover letter: [your content]"
