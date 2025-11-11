# CV Formatting Enhancements Design

**Date:** 2025-11-11
**Status:** Design Complete, Ready for Implementation

## Overview

Bring all cover letter formatting capabilities to the format-resume skill: page headers, metadata inference, raw text → JSON conversion, and full learning system. Use "big bang" implementation approach with comprehensive TDD.

## Goals

1. **Page Headers** - Multi-page CVs get professional headers (page 2+)
2. **Metadata Inference** - Auto-detect contact info, dates, document preferences
3. **Hybrid Workflow** - Support raw text OR manual JSON, with user confirmation
4. **Full Learning** - Remember style corrections, metadata patterns, and section structures
5. **JSON as Truth** - Structured format for maintainability and testing

## Architecture

### Component Structure

```
format-resume skill (skill.md)
    ↓
MetadataHelper (metadata_inference.py)
    ↓ infers
defaults.yaml (contact, preferences)
    ↓ combines with
User Input (raw text OR JSON)
    ↓ converts to
CVAnalyzer (cv_analyzer.py) [NEW]
    ↓ produces
Canonical JSON format
    ↓ applies
StyleApplicator (style_applicator.py)
    ↓ generates
.docx with page headers
```

### Key Components

**Existing (from cover letters):**
- `MetadataHelper` - Contact info, dates, document metadata extraction
- `StyleApplicator` - Already supports page headers!
- `career-documents-template.docx` - 19 semantic styles
- `format_cv.py` - Main formatter script

**New:**
- `CVAnalyzer` - Parses raw CV text into JSON structure
- `defaults.yaml` - CV-specific defaults and preferences
- `learned-preferences.yaml` - Three-layer learning system

### Data Flow

```
Raw Text Input
    ↓
CVAnalyzer.analyze()
    ↓
JSON Draft
    ↓
User Confirmation ("show json" or "yes" or corrections)
    ↓
Enhanced JSON (metadata + learning applied)
    ↓
StyleApplicator.apply_styles()
    ↓
Formatted DOCX with page headers
```

## JSON Schema

### CV JSON Format

```json
{
  "document_metadata": {
    "type": "cv",
    "author_name": "Anthony Byrnes",
    "document_title": "Curriculum Vitae",
    "last_updated": "November 2025",
    "version": "Academic",
    "page_header": {
      "enabled": true,
      "left": "ANTHONY BYRNES - Curriculum Vitae",
      "right": "page"
    }
  },
  "content": [
    {"text": "ANTHONY BYRNES", "style": "CV Name", "type": "paragraph"},
    {"text": "T: 213.305.3132", "style": "Contact Info", "type": "paragraph"},
    {"text": "E: anthonybyrnes@mac.com", "style": "Contact Info", "type": "paragraph"},
    {"text": "EDUCATION", "style": "Section Header", "type": "paragraph"},
    {
      "text": "2020-2024  California State University, Long Beach",
      "style": "Timeline Entry",
      "type": "paragraph",
      "inline_styles": [
        {"text": "California State University, Long Beach", "style": "Institution"}
      ]
    },
    {
      "text": "Interim Associate Dean, College of the Arts",
      "style": "Body Text",
      "type": "paragraph",
      "inline_styles": [
        {"text": "Interim Associate Dean", "style": "Job Title"}
      ]
    },
    {"text": "Led $29M budget across 23 programs", "style": "Bullet Standard", "type": "paragraph"}
  ]
}
```

### defaults.yaml Structure

```yaml
contact:
  name: "ANTHONY BYRNES"
  phone: "213.305.3132"
  email: "anthonybyrnes@mac.com"

cv_defaults:
  document_title: "Curriculum Vitae"
  page_header:
    enabled: true
    format: "{name} - {title}"

preferences:
  version: "Academic"  # vs "Industry", "Arts"
```

### learned-preferences.yaml Structure

**Three-layer learning system:**

```yaml
# Layer 1: Style corrections
style_rules:
  - pattern: "committee|advisory|board"
    context: "service section"
    preferred_style: "Gray Text"
    learned_date: "2025-11-11"
    example: "Graduate Studies Advisory Committee"

  - pattern: "Romeo & Juliet|Hamlet"
    context: "productions"
    preferred_style: "Play Title"
    learned_date: "2025-11-11"

# Layer 2: Metadata patterns
metadata_defaults:
  document_title: "Curriculum Vitae"  # learned: not "Resume"
  page_header_enabled: true
  date_format: "MMMM YYYY"  # "November 2025" not "11/2025"

# Layer 3: Section patterns
section_patterns:
  EDUCATION:
    order: ["Timeline Entry", "Body Text", "Bullet Standard"]
    inline_institution: true

  EXPERIENCE:
    order: ["Timeline Entry", "Job Title", "Bullet Standard"]
    detect_job_title_keywords: ["Dean", "Director", "Manager", "Producer"]
```

## LLM-Based Analysis (Like Cover Letters)

### Core Principle: Intelligence in the Skill

**The format-resume skill (Claude) analyzes raw CV text**, just like format-cover-letter does. No Python regex patterns.

### Why LLM Analysis?

**Advantages:**
- ✅ Understands semantic context (not just patterns)
- ✅ Handles variations naturally ("PhD" vs "Ph.D." vs "Doctor of Philosophy")
- ✅ Consistent with cover letter approach
- ✅ Can explain reasoning to user
- ✅ Learns from corrections through conversation

**Python helpers only:**
- Load defaults from YAML
- Find files
- Generate dates
- No semantic analysis

### Analysis Workflow

**1. User provides raw text:**
```
User: "Format this CV: [pastes raw text]"
```

**2. Skill (Claude) analyzes and creates JSON:**
```
I'll analyze your CV and create a structured format.

I see:
- Name: ANTHONY BYRNES (CV Name style)
- Contact: Phone and email (Contact Info style)
- Section: EDUCATION (Section Header - orange, 11pt)
- Timeline: 2020-2024 California State University... (Timeline Entry with Institution inline)
- Position: Interim Associate Dean... (Body Text with Job Title inline)
- Bullets: Led $29M budget... (Bullet Standard)

Here's my JSON interpretation:
[shows JSON structure]

Looks correct? (yes/show more/line X should be Y)
```

**3. User confirms or corrects:**
- `"yes"` → Proceed to formatting
- `"Line 5 should be Body Text not Timeline Entry"` → Update JSON
- `"show json"` → Display full JSON for manual editing

**4. Format and generate DOCX:**
Uses existing StyleApplicator with confirmed JSON

### No CVAnalyzer Class

Unlike the initial (incorrect) implementation, we **don't need a CVAnalyzer class**. The skill (Claude) does the analysis.

**Helper classes we DO need:**
- `MetadataHelper` - Load defaults, find files (already exists)
- `LearningSystem` - Apply learned preferences (new, simple)

### Learning System Integration

When user makes corrections:
```
User: "That committee role should be Gray Text"

Skill: [Updates JSON, saves to learned-preferences.yaml]
       "I've learned: committee roles → Gray Text"

Next time: Automatically applies Gray Text to committee roles
```

### Simplified Implementation

**What we actually need to build:**

1. **LearningSystem class** (`learning_system.py`)
   - Load/save learned-preferences.yaml
   - Apply learned style rules
   - Simple pattern matching (no complex regex)

2. **Extended MetadataHelper** (already mostly exists)
   - Add `infer_cv_metadata()` method
   - Load CV-specific defaults

3. **Updated format-resume skill** (skill.md)
   - LLM analyzes raw text → creates JSON
   - Shows interpretation to user
   - Applies learned patterns
   - Calls StyleApplicator with JSON

4. **Configuration files:**
   - `defaults.yaml` - Contact info and CV preferences
   - `learned-preferences.yaml` - Learning storage

**That's it!** Much simpler than regex-based CVAnalyzer.

## Page Headers for CVs

### Format

**Page 1:** No header (clean first page)
**Page 2+:** `ANTHONY BYRNES - Curriculum Vitae        page 2`

### Styling

- Font: Helvetica 10pt, bold, gray (RGB 128, 128, 128)
- Left text: Aligned with body text (no indent)
- Right text: Right-aligned via tab stop at 6.5 inches
- Same implementation as cover letters (already working!)

### Implementation

```python
# In StyleApplicator._add_page_headers()
# Already implemented for cover letters!
# Just needs CV metadata support:

if document_type == 'cv':
    left_text = f"{metadata['author_name']} - {metadata['document_title']}"
    right_text = "page"
```

## CV-Specific Features

### Section Header Size

- **CV:** Orange, 11pt
- **Cover Letter:** Orange, 13pt

### Timeline Entry

CV-specific style with hanging indent:
```
2020-2024  California State University, Long Beach
           Interim Associate Dean, College of the Arts
           • Led $29M budget
```

### Inline Styles Usage

| Style | CV Context | Cover Letter Context |
|-------|------------|---------------------|
| Institution | After dates in timeline | Company names in body text |
| Job Title | Position descriptions | Not typically used |
| Play Title | Productions list | Productions mentioned in narrative |
| Gray Text | Dates, committee roles | Dates only |

## Metadata Inference for CVs

### MetadataHelper Extension

```python
class MetadataHelper:
    # Already exists from cover letters

    def infer_cv_metadata(self, content: str) -> dict:
        """Infer CV metadata from content and defaults"""
        return {
            "type": "cv",
            "author_name": self.defaults['contact']['name'],
            "document_title": self._detect_cv_title(content),
            "last_updated": self.get_current_date(),
            "version": self._detect_version(content),
            "page_header": {
                "enabled": self.defaults['cv_defaults']['page_header']['enabled'],
                "left": f"{self.defaults['contact']['name']} - {self._detect_cv_title(content)}",
                "right": "page"
            }
        }

    def _detect_cv_title(self, content: str) -> str:
        """Detect whether user prefers 'CV', 'Resume', or 'Curriculum Vitae'"""
        # Check learned preferences first
        if 'document_title' in self.learned.get('metadata_defaults', {}):
            return self.learned['metadata_defaults']['document_title']

        # Check defaults
        return self.defaults['cv_defaults']['document_title']

    def _detect_version(self, content: str) -> str:
        """Detect CV version based on sections present"""
        # Academic: Has PUBLICATIONS, TEACHING, RESEARCH
        # Industry: Has SKILLS, CERTIFICATIONS
        # Arts: Has PRODUCTIONS, PERFORMANCES
        # Return best guess or "General"
```

## Learning System

### Three-Layer Learning

**Layer 1: Style Rules**

When user corrects a style:
```python
User: "That committee role should be Gray Text"

System saves:
{
  "pattern": "Graduate Studies Advisory Committee",
  "context": "service section",
  "preferred_style": "Gray Text",
  "learned_date": "2025-11-11",
  "example": "Graduate Studies Advisory Committee"
}
```

**Layer 2: Metadata Patterns**

When user changes metadata:
```python
User changes: "Resume" → "Curriculum Vitae"

System saves:
{
  "document_title": "Curriculum Vitae"
}
```

**Layer 3: Section Patterns**

When user restructures a section:
```python
User moves bullets before body text in EDUCATION

System saves:
{
  "EDUCATION": {
    "order": ["Timeline Entry", "Bullet Standard", "Body Text"],
    "inline_institution": true
  }
}
```

### Learning Application

```python
class LearningSystem:
    def __init__(self):
        self.learned = self._load_learned_preferences()

    def apply_learned_patterns(self, content: list) -> list:
        """Apply all learned patterns to parsed content"""

        # Apply style rules
        for item in content:
            for rule in self.learned.get('style_rules', []):
                if self._matches(item['text'], rule['pattern']):
                    if self._context_matches(item, rule['context']):
                        item['style'] = rule['preferred_style']

        # Apply section patterns
        current_section = None
        for item in content:
            if item['style'] == 'Section Header':
                current_section = item['text']
            elif current_section in self.learned.get('section_patterns', {}):
                pattern = self.learned['section_patterns'][current_section]
                # Adjust item based on learned pattern

        return content

    def learn_correction(self, item: dict, old_style: str, new_style: str):
        """Save a style correction"""
        rule = {
            "pattern": item['text'],
            "context": self._get_context(item),
            "preferred_style": new_style,
            "learned_date": datetime.now().strftime("%Y-%m-%d"),
            "example": item['text']
        }

        self.learned.setdefault('style_rules', []).append(rule)
        self._save_learned_preferences()
```

### User Control

- **View learned rules:** "Show me what you've learned"
- **Clear specific rule:** "Forget that committee rule"
- **Edit directly:** Open `~/.claude/skills/format-resume/learned-preferences.yaml`

## Testing Strategy

### TDD Approach

Write tests first for every feature, watch them fail, then implement.

### Test Files

**1. tests/test_cv_page_headers.py**

```python
def test_cv_page_headers_format():
    """Test CV headers show 'NAME - Curriculum Vitae' with page number"""

def test_cv_page_headers_match_colburn_style():
    """Test headers match Colburn formatting (Helvetica, gray, etc.)"""

def test_cv_page_headers_align_with_body():
    """Test header left-aligned with body text (no indent)"""
```

**2. tests/test_cv_metadata_inference.py**

```python
def test_load_defaults_from_yaml():
    """Test contact info loaded from defaults.yaml"""

def test_infer_cv_title():
    """Test detecting 'Curriculum Vitae' vs 'Resume' vs 'CV'"""

def test_infer_cv_version():
    """Test detecting Academic vs Industry vs Arts version"""

def test_generate_page_header_config():
    """Test page header config generation from metadata"""
```

**3. tests/test_cv_analyzer.py**

```python
def test_detect_section_header():
    """Test 'EDUCATION' detected as Section Header"""

def test_parse_timeline_entry():
    """Test '2020-2024 CSULB' parsed with institution inline"""

def test_parse_timeline_with_job_title():
    """Test job title detected and styled"""

def test_parse_bullet_list():
    """Test bullet detection and style assignment"""

def test_detect_contact_info():
    """Test phone/email detection"""

def test_full_cv_parsing():
    """Test complete CV text → JSON conversion"""
```

**4. tests/test_cv_learning.py**

```python
def test_learn_style_correction():
    """Test style correction saved to learned-preferences.yaml"""

def test_apply_learned_style_rules():
    """Test learned style rules applied to new CV"""

def test_learn_metadata_pattern():
    """Test metadata preference saved"""

def test_learn_section_pattern():
    """Test section structure pattern saved"""

def test_clear_learned_rule():
    """Test removing specific learned rule"""
```

**5. Integration Tests**

```python
def test_end_to_end_cv_formatting():
    """Test: raw text → JSON → confirmation → formatted DOCX with headers"""

def test_manual_json_workflow():
    """Test: user provides JSON → formatted DOCX"""

def test_learning_workflow():
    """Test: correction → saved → applied to next CV"""
```

### Validation

- All tests pass before commit
- Visual verification with real CV
- Compare output to existing formatted CV examples
- Verify page headers match cover letter quality

## Implementation Plan

### Big Bang Approach

Build all features together with TDD, single comprehensive commit.

### Order of Implementation

1. **Setup & Infrastructure**
   - Create test files (empty, with test stubs)
   - Create `cv_analyzer.py` skeleton
   - Create `defaults.yaml` template
   - Create `learned-preferences.yaml` template

2. **Page Headers (Test First)**
   - Write `test_cv_page_headers.py` tests
   - Watch them fail
   - Implement CV page header support in StyleApplicator
   - All page header tests pass

3. **Metadata Inference (Test First)**
   - Write `test_cv_metadata_inference.py` tests
   - Watch them fail
   - Extend MetadataHelper with CV methods
   - All metadata tests pass

4. **CVAnalyzer (Test First)**
   - Write `test_cv_analyzer.py` tests
   - Watch them fail
   - Implement CVAnalyzer class
   - All parsing tests pass

5. **Learning System (Test First)**
   - Write `test_cv_learning.py` tests
   - Watch them fail
   - Implement LearningSystem class
   - All learning tests pass

6. **Integration & Skill Update**
   - Write integration tests
   - Update format-resume skill.md documentation
   - Wire everything together
   - End-to-end tests pass

7. **Validation & Commit**
   - Run all tests
   - Format real CV with new system
   - Visual verification
   - Single comprehensive commit

## Files to Create/Modify (LLM-Based Approach)

### New Files

```
tests/test_cv_page_headers.py                    - Page header tests for CVs
tests/test_cv_learning.py                        - Learning system tests
cv_formatting/learning_system.py                 - Simple learning system (pattern matching)
~/.claude/skills/format-resume/defaults.yaml     - CV defaults config
~/.claude/skills/format-resume/learned-preferences.yaml  - Learning storage
```

### Modified Files

```
cv_formatting/metadata_inference.py              - Add infer_cv_metadata() method
~/.claude/skills/format-resume/skill.md          - Update with LLM workflow
```

### Already Working (No Changes Needed)

```
cv_formatting/style_applicator.py                - Page headers already implemented!
cv_formatting/templates/career-documents-template.docx  - 19 styles template
format_cv.py                                     - Main formatter script
```

**Note:** No CVAnalyzer needed! Claude (the skill) does the semantic analysis.

## Success Criteria

✅ All tests pass (page headers, metadata, parsing, learning)
✅ Can format CV from raw text with user confirmation
✅ Can format CV from manual JSON
✅ Page headers match cover letter quality (Helvetica, gray, proper alignment)
✅ Learning system captures and applies all three layers
✅ Metadata inference works from defaults.yaml
✅ Documentation updated
✅ Visual output matches professional CV standards

## Future Enhancements

(Not in this implementation)

1. **Smart section detection** - Learn common section names beyond EDUCATION/EXPERIENCE
2. **Multi-version support** - Generate Academic, Industry, and Arts versions from same content
3. **Citation formatting** - Special handling for publications section
4. **Table support** - For skills matrices or course listings
5. **Image support** - Headshots or logos (beyond signatures)

## Notes

- This design mirrors the successful cover letter implementation
- JSON as truth principle ensures maintainability
- Big bang approach acceptable because we have proven patterns from cover letters
- TDD throughout ensures quality and prevents regressions
- Learning system makes the tool smarter over time
