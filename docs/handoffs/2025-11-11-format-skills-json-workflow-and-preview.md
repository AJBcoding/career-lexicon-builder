# Format Skills - JSON Workflow & Preview Display Solution

**Date**: 2025-11-11
**Status**: ✅ Complete workflow validated, ready for skill refactoring
**Previous Handoff**: [2025-11-11-format-cover-letter-skill-ready.md](./2025-11-11-format-cover-letter-skill-ready.md)

---

## Executive Summary

Successfully identified and resolved all issues with the formatting skills. The Python formatter (`format_cv.py`) works perfectly when:
1. Content is packaged as JSON (not markdown)
2. Virtual environment (`.venv`) is activated
3. Preview images are opened with `open` command or iTerm2's `imgcat`

**Key Discovery**: The 790-line format-cover-letter skill documentation was incorrect - it said to use `.md` files when the formatter requires `.json` files.

---

## What We Accomplished

### 1. Validated Complete 5-Step Workflow ✅

**Step 1: Analyze Content**
- Claude reads cover letter or CV content
- Identifies structural elements (sections, headers, dates)
- Identifies content mentions (institutions, positions, productions)

**Step 2: Create JSON Mapping**
```json
[
  {
    "text": "November 11, 2025",
    "style": "Date Line",
    "type": "paragraph"
  },
  {
    "text": "At UCLA, I developed programs serving 5,000 students.",
    "style": "Body Text",
    "type": "paragraph",
    "runs": [
      {"text": "At ", "style": null},
      {"text": "UCLA", "style": "Institution"},
      {"text": ", I developed programs serving ", "style": null},
      {"text": "5,000 students", "style": "Orange Emphasis"},
      {"text": ".", "style": null}
    ]
  }
]
```

**Step 3: Save JSON**
```bash
/tmp/content-mapping.json
```

**Step 4: Call Formatter**
```bash
source .venv/bin/activate && python3 format_cv.py \
  /tmp/content-mapping.json \
  output.docx \
  --document-type cover-letter \
  --preview
```

**Step 5: Display Preview**
```bash
# Option A: System viewer (works in any terminal)
open output.pdf

# Option B: Inline in iTerm2 (requires iTerm2)
~/bin/imgcat output_images/page-1.jpg
```

### 2. Resolved LibreOffice & PDF Generation Issues ✅

**Problem**: Initially got "module not found" errors.

**Solution**: Must activate virtual environment before calling Python formatter.

**Verification**:
- ✅ LibreOffice installed: `/opt/homebrew/bin/soffice`
- ✅ Poppler (pdftoppm) installed: `/opt/homebrew/bin/pdftoppm`
- ✅ python-docx installed in `.venv/`
- ✅ All three outputs generated successfully:
  - DOCX file (formatted document)
  - PDF file (via LibreOffice conversion)
  - JPG images (via pdftoppm conversion)

### 3. Solved Preview Display Issue ✅

**Problem**: Claude can see images via Read tool, but they don't display inline for user in Terminal.app.

**Solutions Tested**:

**A. `open` command (works everywhere)** ⭐ RECOMMENDED
```bash
open output.pdf  # Opens in Preview.app
```
- ✅ Works in Terminal.app, iTerm2, any terminal
- ✅ Full quality preview
- ✅ No setup required

**B. iTerm2 with imgcat (inline display)**
```bash
~/bin/imgcat output_images/page-1.jpg
```
- ✅ iTerm2 installed: `/Applications/iTerm.app`
- ✅ imgcat installed: `~/bin/imgcat`
- ⏳ Not yet tested (user needs to switch to iTerm2)
- ✅ Enables full-quality inline image display

### 4. JSON Packaging Approach Confirmed ✅

Both format-resume AND format-cover-letter use the **same JSON format**:

**JSON Structure**:
```json
[
  {
    "text": "Paragraph or inline text",
    "style": "Style Name",
    "type": "paragraph",
    "runs": [  // Optional for inline styling
      {"text": "plain text", "style": null},
      {"text": "styled text", "style": "Institution"}
    ]
  }
]
```

**Available Styles**:

*Paragraph styles:*
- `CV Name` - Name at document top
- `Section Header` - Context-aware (CV: orange 11pt, Cover letter: black 13pt)
- `Date Line` - Right-aligned date (cover letters)
- `Body Text` - Standard paragraphs
- `Timeline Entry` - Date + content with hanging indent
- `Bullet Standard`, `Bullet Gray`, `Bullet Emphasis` - List styles

*Character styles (inline):*
- `Institution` - Bold (UCLA, Center Theatre Group)
- `Job Title` - Bold italic (Interim Associate Dean)
- `Play Title` - Bold italic (Kirk Douglas Theatre, Romeo & Juliet)
- `Orange Emphasis` - Bold orange ($29 million, 5,000 students)
- `Gray Text` - Dates, secondary info

---

## Test Results

### Test 1: Simple Cover Letter ✅
**File**: `/tmp/demo-cover-letter-mapping.json`
**Result**: Perfect formatting
- ✅ Date line right-aligned
- ✅ Job titles bold italic
- ✅ Institutions bold
- ✅ Orange emphasis on statistics
- ✅ PDF generated
- ✅ Images generated

### Test 2: Sample CV ✅
**File**: `tests/fixtures/sample_cv_mapping.json`
**Result**: All tests passing (24/24)
- ✅ Section headers orange 11pt (CV mode)
- ✅ Timeline entries with hanging indent
- ✅ All inline styles correct

### Test 3: UCLA CAO Cover Letter ✅
**File**: `/tmp/ucla-cao-cover-letter-mapping.json`
**Result**: Complex document formatted correctly
- ✅ Multiple institutions styled
- ✅ Multiple job titles styled
- ✅ Theater venues (Kirk Douglas, Ivy Substation) styled as Play Title
- ✅ Multiple dollar amounts in orange
- ✅ All context discrimination working

---

## Current State of Skills

### format-resume
**Location**: `~/.claude/skills/format-resume/`
**Size**: 170 lines (skill.md)
**Status**: ✅ Works, concise and clear
**Structure**:
```
format-resume/
├── skill.md (170 lines)
├── style-mappings.yaml
├── learned-preferences.yaml
├── cv-template.docx
└── apply_styles.py
```

**Quality**: Good - clear 6-step workflow, focused examples

### format-cover-letter
**Location**: `~/.claude/skills/format-cover-letter/`
**Size**: 790 lines (skill.md) - **4.6x larger than format-resume!**
**Status**: ⚠️ Works but bloated, contains incorrect documentation
**Structure**:
```
format-cover-letter/
├── skill.md (790 lines - TOO LONG)
├── style-mappings.yaml
└── learned-preferences.yaml
```

**Issues**:
- ❌ Line 607 says `input.md` - should be `input.json`
- ❌ 790 lines vs 170 for resume (4.6x longer)
- ❌ Excessive FAQs and troubleshooting
- ❌ Redundant examples
- ❌ Verbose explanations

---

## Key Files & Locations

### Python Formatter
```
format_cv.py                          # Main CLI formatter
cv_formatting/
├── style_applicator.py              # Applies styles to document
├── pdf_converter.py                 # DOCX → PDF (LibreOffice)
├── image_generator.py               # PDF → JPEG (pdftoppm)
└── templates/
    └── career-documents-template.docx  # Shared template (13 styles)
```

### Skills
```
~/.claude/skills/
├── format-resume/                   # 170 lines, works well
└── format-cover-letter/             # 790 lines, needs refactoring
```

### Virtual Environment
```
.venv/                               # Must be activated!
├── bin/python3                      # Python with python-docx
└── lib/python3.x/site-packages/
    └── docx/                        # python-docx module
```

### Test Files
```
tests/fixtures/
├── sample_cv_mapping.json           # Example CV JSON
└── ucla-cao-cover-letter-v3.md      # Real cover letter content

/tmp/
├── demo-cover-letter-mapping.json   # Test JSON we created
├── demo-cover-letter.docx           # Generated output
├── demo-cover-letter.pdf            # PDF preview
└── demo-cover-letter_images/        # Page images
    └── page-1.jpg
```

### Preview Tools
```
/opt/homebrew/bin/soffice            # LibreOffice (DOCX → PDF)
/opt/homebrew/bin/pdftoppm           # Poppler (PDF → JPEG)
/Applications/iTerm.app              # iTerm2 (inline images)
~/bin/imgcat                         # iTerm2 image utility
```

---

## Next Steps

### Immediate: Refactor format-cover-letter Skill

**Goal**: Reduce from 790 lines to ~200-250 lines (matching format-resume)

**What to keep**:
- Clear 5-step workflow
- JSON structure examples
- Key styling distinctions (section headers: CV orange vs cover letter black)
- Concrete code examples

**What to remove/consolidate**:
- Extensive FAQ section → move to docs/guides/
- Redundant examples
- Verbose explanations of obvious concepts
- Duplicate information

**What to fix**:
- Line 607: Change `input.md` to `input.json`
- Add concrete subprocess example showing .venv activation
- Document both preview options (open and imgcat)

**Target structure** (like format-resume):
```markdown
# Format Cover Letter Skill

## Purpose
[2-3 sentences]

## Usage
[Simple examples]

## How It Works
1. Semantic Analysis
2. JSON Mapping
3. Generate Document
4. Visual Preview
5. Learn from Corrections

## The 13 Styles
[Brief list with examples]

## Workflow
[Concrete steps with code]

## Context Discrimination
[Key examples showing semantic understanding]

## Learning System
[How corrections are saved]

## Error Handling
[Common issues]

## Files
[What each file does]
```

### Then: Refactor format-resume Skill

**Goal**: Ensure it matches the same structure and uses identical workflow

**Changes needed**:
- Verify JSON workflow documentation
- Add explicit .venv activation example
- Document preview options (open/imgcat)
- Ensure style list matches cover-letter skill

### Testing: Validate Refactored Skills

**Test both skills with**:
1. Simple documents (verify basic workflow)
2. Complex documents (UCLA CAO letter, multi-page CV)
3. Preview display (both open and imgcat if using iTerm2)
4. Learning system (make corrections, verify they're saved)

---

## iTerm2 Setup for Next Session

**If you want inline image preview:**

1. **Launch iTerm2**:
   ```bash
   open -a iTerm
   ```

2. **Start Claude Code in iTerm2**

3. **Test inline images**:
   ```bash
   ~/bin/imgcat /tmp/demo-cover-letter_images/page-1.jpg
   ```

4. **Update skills to use imgcat**:
   ```bash
   # Check if iTerm2
   if [ "$TERM_PROGRAM" = "iTerm.app" ]; then
     ~/bin/imgcat output_images/*.jpg
   else
     open output.pdf
   fi
   ```

---

## Code Examples for Refactored Skills

### Example: Complete Workflow in Skill

```markdown
## Workflow

**Step 1: Analyze Content**
Claude reads your cover letter and identifies:
- Structural elements (date, salutation, headers, body, closing)
- Content mentions (institutions, positions, achievements)

**Step 2: Create JSON Mapping**
```json
[
  {
    "text": "November 11, 2025",
    "style": "Date Line",
    "type": "paragraph"
  },
  {
    "text": "At UCLA, I led programs serving 5,000 students.",
    "style": "Body Text",
    "type": "paragraph",
    "runs": [
      {"text": "At ", "style": null},
      {"text": "UCLA", "style": "Institution"},
      {"text": ", I led programs serving ", "style": null},
      {"text": "5,000 students", "style": "Orange Emphasis"},
      {"text": ".", "style": null}
    ]
  }
]
```

**Step 3: Format Document**
```bash
# Save JSON mapping
cat > /tmp/cover-letter-mapping.json << 'EOF'
[JSON content here]
EOF

# Format with preview
source .venv/bin/activate && python3 format_cv.py \
  /tmp/cover-letter-mapping.json \
  output.docx \
  --document-type cover-letter \
  --preview
```

**Step 4: Preview**
```bash
# Opens in Preview.app
open output.pdf
```

**Step 5: Review & Learn**
If styling needs correction, tell Claude and it will:
- Update the document
- Save preference to learned-preferences.yaml
- Apply automatically next time
```

---

## Technical Specifications

### Python Dependencies (in .venv)
```
python-docx==1.2.0    # Document creation
pytest==8.4.2         # Testing
pdfplumber==0.11.7    # PDF parsing
anthropic>=0.40.0     # LLM analysis
```

### System Dependencies (via Homebrew)
```
libreoffice           # DOCX → PDF conversion
poppler               # PDF → JPEG conversion
iterm2 (optional)     # Inline image display
```

### Template Specifications
**File**: `cv_formatting/templates/career-documents-template.docx`
**Size**: 36KB
**Styles**: 13 total
- 8 paragraph styles (CV Name, Section Header, Date Line, Body Text, Timeline Entry, 3 bullet styles)
- 5 character styles (Play Title, Institution, Job Title, Orange Emphasis, Gray Text)

**Context-Aware Style**: Section Header
- CV mode: RGB(255, 109, 73) orange, 11pt, bold
- Cover letter mode: RGB(0, 0, 0) black, 13pt, bold

---

## Success Criteria

✅ **Workflow validated**: All 5 steps work end-to-end
✅ **LibreOffice working**: PDF generation successful
✅ **Image generation working**: JPEG previews created
✅ **Preview display working**: `open` command displays documents
✅ **JSON format confirmed**: Both skills use same structure
✅ **Context awareness verified**: Section headers change by document type
✅ **Complex documents tested**: UCLA CAO letter formatted correctly

---

## Questions for Next Session

1. **Should we use iTerm2 inline display?**
   - Requires user to switch terminals
   - Provides better inline experience
   - Or stick with `open` (works everywhere)

2. **Should both skills be identical in structure?**
   - Same workflow documentation
   - Same code examples
   - Only difference: document-specific patterns

3. **Where should extensive docs go?**
   - Keep skills at ~200 lines
   - Move FAQs/troubleshooting to docs/guides/
   - Link from skill to guide

---

## Files Modified This Session

**Created**:
- `/tmp/test-cover-letter-mapping.json` - Test JSON
- `/tmp/demo-cover-letter-mapping.json` - Demo JSON
- `/tmp/ucla-cao-cover-letter-mapping.json` - Real document JSON
- `~/bin/imgcat` - iTerm2 image utility

**Installed**:
- iTerm2 app at `/Applications/iTerm.app`

**No modifications to skills yet** - ready for refactoring in next session.

---

## Commands Reference

### Format a Cover Letter
```bash
# 1. Activate venv
source .venv/bin/activate

# 2. Format with preview
python3 format_cv.py \
  input.json \
  output.docx \
  --document-type cover-letter \
  --preview

# 3. View result
open output.pdf
# OR (in iTerm2)
~/bin/imgcat output_images/*.jpg
```

### Format a CV
```bash
# Same as above but:
--document-type cv
```

### Test Preview Display
```bash
# In any terminal
open /tmp/demo-cover-letter.pdf

# In iTerm2 only
~/bin/imgcat /tmp/demo-cover-letter_images/page-1.jpg
```

### Verify Installation
```bash
# Check LibreOffice
which soffice

# Check Poppler
which pdftoppm

# Check python-docx
source .venv/bin/activate && python -c "import docx; print('OK')"

# Check iTerm2
ls -la /Applications/iTerm.app

# Check imgcat
ls -la ~/bin/imgcat
```

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-11 | 1.0 | Initial handoff documenting complete workflow validation and preview display solutions |

---

**Ready for refactoring!** Both skills can now be streamlined to ~200 lines with proven, working JSON workflow.
