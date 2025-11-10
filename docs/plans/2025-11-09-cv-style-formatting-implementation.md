# CV Style Extraction and Formatting Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extract 97 styles from .pages CV, consolidate to 12 semantic styles, create clean .docx template, and build intelligent formatting skill.

**Architecture:** Two-phase approach - (1) Python script extracts and consolidates styles into clean template, (2) Claude skill uses semantic understanding to format CV content using the template.

**Tech Stack:** python-docx, BeautifulSoup4, iwork-converter, LibreOffice, Poppler

**Design Document:** `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`

---

## Phase 1: Template Creation (Tasks 1-8)

### Task 1: Set Up Project Structure

**Files:**
- Create: `cv_formatting/`
- Create: `cv_formatting/__init__.py`
- Create: `cv_formatting/template_builder.py`
- Create: `tests/test_template_builder.py`

**Step 1: Create directory structure**

```bash
mkdir -p cv_formatting
mkdir -p tests
touch cv_formatting/__init__.py
```

**Step 2: Verify structure**

```bash
ls -la cv_formatting/
```

Expected: `__init__.py` exists

**Step 3: Commit**

```bash
git add cv_formatting/
git commit -m "feat: create cv_formatting module structure"
```

---

### Task 2: Parse iwork-converter HTML Output

**Files:**
- Create: `cv_formatting/style_parser.py`
- Create: `tests/test_style_parser.py`

**Step 1: Write test for CSS parsing**

File: `tests/test_style_parser.py`

```python
import pytest
from cv_formatting.style_parser import StyleParser


def test_parse_css_extracts_style_classes():
    """Test that CSS parsing extracts style class definitions"""
    css = """
    .ps2539 {
        font-weight: bold;
        font-size: calc(var(--slide-scale, 1) * 9.00pt);
        color: rgba(255,109,73,1.000);
    }
    .ss2505 {
        font-weight: bold;
        font-size: calc(var(--slide-scale, 1) * 9.00pt);
    }
    """

    parser = StyleParser()
    styles = parser.parse_css(css)

    assert len(styles) == 2
    assert 'ps2539' in styles
    assert styles['ps2539']['bold'] == True
    assert styles['ps2539']['size'] == 9
    assert styles['ps2539']['color'] == 'rgba(255,109,73,1.000)'


def test_parse_css_handles_empty_input():
    """Test that empty CSS returns empty dict"""
    parser = StyleParser()
    styles = parser.parse_css("")

    assert styles == {}
```

**Step 2: Run test to verify it fails**

```bash
source .venv/bin/activate
pytest tests/test_style_parser.py -v
```

Expected: FAIL - "No module named 'cv_formatting.style_parser'"

**Step 3: Write minimal implementation**

File: `cv_formatting/style_parser.py`

```python
"""Parse iwork-converter HTML/CSS output to extract style definitions."""
import re
from typing import Dict, Any


class StyleParser:
    """Parser for iwork-converter CSS output."""

    def parse_css(self, css_text: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse CSS text and extract style definitions.

        Args:
            css_text: CSS content from iwork-converter HTML

        Returns:
            Dict mapping style class names to property dicts
        """
        if not css_text:
            return {}

        styles = {}

        # Match CSS class definitions: .classname { properties }
        pattern = r'\.([a-z0-9]+)\s*\{([^}]+)\}'

        for match in re.finditer(pattern, css_text, re.IGNORECASE):
            class_name = match.group(1)
            properties_text = match.group(2)

            # Parse properties
            props = self._parse_properties(properties_text)

            if props:
                styles[class_name] = props

        return styles

    def _parse_properties(self, props_text: str) -> Dict[str, Any]:
        """Parse CSS properties into structured dict."""
        props = {}

        # Font weight
        if 'font-weight: bold' in props_text:
            props['bold'] = True

        # Font style
        if 'font-style: italic' in props_text:
            props['italic'] = True

        # Font size
        size_match = re.search(r'font-size.*?(\d+)\.00pt', props_text)
        if size_match:
            props['size'] = int(size_match.group(1))

        # Font family
        font_match = re.search(r"font-family:\s*'([^']+)'", props_text)
        if font_match:
            props['font'] = font_match.group(1)

        # Color
        color_match = re.search(r'color:\s*(rgba\([^)]+\))', props_text)
        if color_match:
            props['color'] = color_match.group(1)

        # Margins/indents
        margin_left = re.search(r'margin-left:\s*(\d+\.\d+)pt', props_text)
        if margin_left:
            props['margin_left'] = float(margin_left.group(1))

        text_indent = re.search(r'text-indent:\s*(-?\d+\.\d+)pt', props_text)
        if text_indent:
            props['text_indent'] = float(text_indent.group(1))

        # List style
        if 'list-style-type: disc' in props_text:
            props['list_style'] = 'disc'

        return props
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_style_parser.py -v
```

Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add cv_formatting/style_parser.py tests/test_style_parser.py
git commit -m "feat: add CSS style parser for iwork-converter output"
```

---

### Task 3: Define Style Consolidation Mapping

**Files:**
- Create: `cv_formatting/style_mapping.py`
- Create: `tests/test_style_mapping.py`

**Step 1: Write test for style mapping**

File: `tests/test_style_mapping.py`

```python
from cv_formatting.style_mapping import STYLE_CONSOLIDATION, get_semantic_name


def test_consolidation_map_contains_key_styles():
    """Test that consolidation map includes heavily used styles"""
    # Most used style from analysis
    assert 'ss2578' in STYLE_CONSOLIDATION
    assert STYLE_CONSOLIDATION['ss2578'] == 'Play Title'

    # Institution names
    assert 'ss2505' in STYLE_CONSOLIDATION
    assert STYLE_CONSOLIDATION['ss2505'] == 'Institution'

    # Body text duplicates should all map to same name
    assert STYLE_CONSOLIDATION['ps81934'] == 'Body Text'
    assert STYLE_CONSOLIDATION['ps2548'] == 'Body Text'


def test_get_semantic_name_returns_mapped_name():
    """Test getting semantic name for old style"""
    assert get_semantic_name('ss2578') == 'Play Title'
    assert get_semantic_name('ss2505') == 'Institution'


def test_get_semantic_name_returns_none_for_unknown():
    """Test that unknown styles return None"""
    assert get_semantic_name('unknown123') is None


def test_all_twelve_core_styles_present():
    """Test that all 12 core styles are represented"""
    semantic_names = set(STYLE_CONSOLIDATION.values())

    expected_styles = {
        'CV Name',
        'Section Header',
        'Body Text',
        'Timeline Entry',
        'Bullet Standard',
        'Bullet Gray',
        'Bullet Emphasis',
        'Play Title',
        'Institution',
        'Job Title',
        'Orange Emphasis',
        'Gray Text'
    }

    assert semantic_names == expected_styles
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_style_mapping.py -v
```

Expected: FAIL - "No module named 'cv_formatting.style_mapping'"

**Step 3: Write implementation based on usage analysis**

File: `cv_formatting/style_mapping.py`

```python
"""Style consolidation mapping from 97 .pages styles to 12 semantic styles."""
from typing import Optional


# Consolidation map: old style class → semantic style name
# Based on usage analysis from analyze_cv_styles.py
STYLE_CONSOLIDATION = {
    # Character styles - Emphasis and formatting
    'ss2578': 'Play Title',       # 468 uses - bold italic (most used!)
    'ss40454': 'Play Title',       # duplicate - bold italic
    'ss2547': 'Play Title',        # duplicate - bold italic small

    'ss2592': 'Job Title',         # 28 uses - bold italic for positions
    'ss2508': 'Job Title',         # 22 uses - bold italic variant

    'ss2505': 'Institution',       # 48 uses - bold for institution names
    'ss93858': 'Institution',      # duplicate - bold
    'ss2543': 'Institution',       # duplicate - bold
    'ss138597': 'Institution',     # duplicate - bold black

    'ss2555': 'Orange Emphasis',   # 18 uses - bold orange
    'ss2561': 'Orange Emphasis',   # 5 uses - bold orange section headers
    'ss40405': 'Orange Emphasis',  # duplicate - bold orange small
    'ss52919': 'Orange Emphasis',  # duplicate - orange color only

    'ss2507': 'Gray Text',         # 5 uses - gray for dates
    'ss40419': 'Gray Text',        # 3 uses - gray duplicate
    'ss8153': 'Gray Text',         # 37 uses - used for secondary text
    'ss8151': 'Gray Text',         # 10 uses - duplicate

    # Paragraph styles - Structure
    'ps2539': 'Section Header',    # 19 uses - bold orange headers
    'ps2557': 'Section Header',    # 1 use - section header with indent
    'ps2551': 'Section Header',    # duplicate - bold orange

    'ps2554': 'CV Name',           # intro/name paragraph
    'ps27686': 'CV Name',          # duplicate

    'ps81934': 'Body Text',        # 25 uses - standard body
    'ps2548': 'Body Text',         # 85 uses - most used body text
    'ps2597': 'Body Text',         # 20 uses - duplicate
    'ps53936': 'Body Text',        # 57 uses - duplicate
    'ps8131': 'Body Text',         # 17 uses - duplicate
    'ps2573': 'Body Text',         # duplicate
    'ps2570': 'Body Text',         # duplicate
    'ps8343': 'Body Text',         # duplicate
    'ps8957': 'Body Text',         # duplicate
    'ps2599': 'Body Text',         # 17 uses - black body text

    'ps2532': 'Timeline Entry',    # 103 uses - gray with 72pt hanging indent
    'ps81930': 'Timeline Entry',   # black variant with hanging indent
    'ps2541': 'Timeline Entry',    # plain variant with hanging indent
    'ps52931': 'Timeline Entry',   # 11 uses - duplicate hanging indent
    'ps176105': 'Timeline Entry',  # 55 uses - indent variant
    'ps49520': 'Timeline Entry',   # 22 uses - indent variant

    # Bullet lists
    'ps40376': 'Bullet Standard',  # 254 uses - most common bullet style
    'ps40524': 'Bullet Standard',  # 79 uses - duplicate
    'ps40420': 'Bullet Standard',  # duplicate
    'ps40357': 'Bullet Standard',  # duplicate
    'ps40270': 'Bullet Standard',  # duplicate
    'ps40470': 'Bullet Standard',  # duplicate
    'ps40339': 'Bullet Standard',  # 17 uses - bullet with indent
    'ps40585': 'Bullet Standard',  # duplicate

    'ps2532': 'Bullet Gray',       # 103 uses - gray bullets (education/dates)
    'ps40350': 'Bullet Gray',      # 14 uses - gray bullet duplicate
    'ps151234': 'Bullet Gray',     # 16 uses - gray justified

    'ps40465': 'Bullet Emphasis',  # 16 uses - bold italic bullets
    'ps46257': 'Bullet Emphasis',  # 24 uses - bold italic duplicate
    'ps40394': 'Bullet Emphasis',  # duplicate - bold italic
    'ps40547': 'Bullet Emphasis',  # duplicate
    'ps40503': 'Bullet Emphasis',  # duplicate
    'ps40592': 'Bullet Emphasis',  # 12 uses - duplicate
    'ps45767': 'Bullet Emphasis',  # 28 uses - bold italic variant
    'ps176103': 'Bullet Emphasis', # 55 uses - bold italic with indent
}


def get_semantic_name(old_class: str) -> Optional[str]:
    """
    Get semantic style name for old .pages style class.

    Args:
        old_class: Original style class name (e.g., 'ss2578')

    Returns:
        Semantic style name or None if not mapped
    """
    return STYLE_CONSOLIDATION.get(old_class)


def get_all_semantic_styles() -> set:
    """Get set of all unique semantic style names."""
    return set(STYLE_CONSOLIDATION.values())
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_style_mapping.py -v
```

Expected: PASS (4 tests)

**Step 5: Commit**

```bash
git add cv_formatting/style_mapping.py tests/test_style_mapping.py
git commit -m "feat: add style consolidation mapping (97→12 styles)"
```

---

### Task 4: Build Template with python-docx

**Files:**
- Modify: `cv_formatting/template_builder.py`
- Create: `tests/test_template_builder.py`

**Step 1: Write test for template creation**

File: `tests/test_template_builder.py`

```python
import pytest
from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from cv_formatting.template_builder import TemplateBuilder
from cv_formatting.style_mapping import get_all_semantic_styles


def test_create_template_generates_docx(tmp_path):
    """Test that template creation generates .docx file"""
    output_path = tmp_path / "test-template.docx"

    builder = TemplateBuilder()
    result = builder.create_template(str(output_path))

    assert result is True
    assert output_path.exists()


def test_template_contains_all_semantic_styles(tmp_path):
    """Test that template includes all 12 semantic styles"""
    output_path = tmp_path / "test-template.docx"

    builder = TemplateBuilder()
    builder.create_template(str(output_path))

    # Load and verify
    doc = Document(str(output_path))
    style_names = {s.name for s in doc.styles}

    expected_styles = get_all_semantic_styles()

    for expected in expected_styles:
        assert expected in style_names, f"Missing style: {expected}"


def test_template_styles_have_correct_properties(tmp_path):
    """Test that styles have expected formatting properties"""
    output_path = tmp_path / "test-template.docx"

    builder = TemplateBuilder()
    builder.create_template(str(output_path))

    doc = Document(str(output_path))

    # Check Section Header style
    section_header = doc.styles['Section Header']
    assert section_header.font.bold == True
    assert section_header.font.size.pt == 10
    assert section_header.font.color.rgb is not None  # Has orange color

    # Check Body Text style
    body_text = doc.styles['Body Text']
    assert body_text.font.size.pt == 9
    assert body_text.font.name == 'Helvetica'
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_template_builder.py -v
```

Expected: FAIL - TemplateBuilder not implemented

**Step 3: Write implementation**

File: `cv_formatting/template_builder.py`

```python
"""Build clean .docx template with semantic style names."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TemplateBuilder:
    """Builds clean .docx templates with semantic style names."""

    # Orange brand color from analysis: rgba(255,109,73,1.000)
    ORANGE_RGB = RGBColor(255, 109, 73)
    GRAY_RGB = RGBColor(128, 128, 128)

    def create_template(self, output_path: str) -> bool:
        """
        Create clean .docx template with 12 semantic styles.

        Args:
            output_path: Where to save the template

        Returns:
            True if successful
        """
        try:
            doc = Document()

            # Create paragraph styles
            self._create_cv_name_style(doc)
            self._create_section_header_style(doc)
            self._create_body_text_style(doc)
            self._create_timeline_entry_style(doc)
            self._create_bullet_standard_style(doc)
            self._create_bullet_gray_style(doc)
            self._create_bullet_emphasis_style(doc)

            # Create character styles
            self._create_play_title_style(doc)
            self._create_institution_style(doc)
            self._create_job_title_style(doc)
            self._create_orange_emphasis_style(doc)
            self._create_gray_text_style(doc)

            doc.save(output_path)
            logger.info(f"Template created: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to create template: {e}")
            return False

    def _create_cv_name_style(self, doc: Document):
        """Create CV Name paragraph style (name at top)"""
        style = doc.styles.add_style('CV Name', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(13)
        style.font.bold = True

    def _create_section_header_style(self, doc: Document):
        """Create Section Header style (EDUCATION, PROFESSIONAL EXPERIENCE)"""
        style = doc.styles.add_style('Section Header', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(10)
        style.font.bold = True
        style.font.color.rgb = self.ORANGE_RGB

    def _create_body_text_style(self, doc: Document):
        """Create Body Text paragraph style (standard paragraphs)"""
        style = doc.styles.add_style('Body Text', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

    def _create_timeline_entry_style(self, doc: Document):
        """Create Timeline Entry style (date + institution with hanging indent)"""
        style = doc.styles.add_style('Timeline Entry', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

        # 72pt hanging indent (from analysis)
        style.paragraph_format.left_indent = Pt(72)
        style.paragraph_format.first_line_indent = Pt(-72)

    def _create_bullet_standard_style(self, doc: Document):
        """Create Bullet Standard style (regular bullets)"""
        style = doc.styles.add_style('Bullet Standard', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

        # Bullet formatting
        style.paragraph_format.left_indent = Pt(72)

    def _create_bullet_gray_style(self, doc: Document):
        """Create Bullet Gray style (bullets for dates/education)"""
        style = doc.styles.add_style('Bullet Gray', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)
        style.font.color.rgb = self.GRAY_RGB

        style.paragraph_format.left_indent = Pt(72)

    def _create_bullet_emphasis_style(self, doc: Document):
        """Create Bullet Emphasis style (bold italic bullets)"""
        style = doc.styles.add_style('Bullet Emphasis', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)
        style.font.bold = True
        style.font.italic = True

        style.paragraph_format.left_indent = Pt(72)

    def _create_play_title_style(self, doc: Document):
        """Create Play Title character style (bold italic for productions)"""
        style = doc.styles.add_style('Play Title', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.italic = True

    def _create_institution_style(self, doc: Document):
        """Create Institution character style (bold for institution names)"""
        style = doc.styles.add_style('Institution', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True

    def _create_job_title_style(self, doc: Document):
        """Create Job Title character style (bold italic for positions)"""
        style = doc.styles.add_style('Job Title', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.italic = True

    def _create_orange_emphasis_style(self, doc: Document):
        """Create Orange Emphasis character style"""
        style = doc.styles.add_style('Orange Emphasis', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.color.rgb = self.ORANGE_RGB

    def _create_gray_text_style(self, doc: Document):
        """Create Gray Text character style (dates, secondary info)"""
        style = doc.styles.add_style('Gray Text', WD_STYLE_TYPE.CHARACTER)
        style.font.color.rgb = self.GRAY_RGB
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_template_builder.py -v
```

Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add cv_formatting/template_builder.py tests/test_template_builder.py
git commit -m "feat: implement template builder with 12 semantic styles"
```

---

### Task 5: Create Template Generation Script

**Files:**
- Create: `generate_cv_template.py`

**Step 1: Write script to generate template from source CV**

File: `generate_cv_template.py`

```python
#!/usr/bin/env python3
"""
Generate clean CV template from .pages source document.

Usage:
    python generate_cv_template.py

This will:
1. Convert AJB CV 2024.pages to HTML using iwork-converter
2. Parse style definitions
3. Create clean cv-template.docx with 12 semantic styles
4. Save to ~/.claude/skills/career/format-resume/
"""
import subprocess
import sys
from pathlib import Path
from cv_formatting.template_builder import TemplateBuilder
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Generate CV template."""

    # Paths
    source_pages = Path("my_documents/AJB CV 2024.pages")
    temp_html = Path("/tmp/cv_for_template.html")
    skill_dir = Path.home() / ".claude/skills/career/format-resume"
    output_template = skill_dir / "cv-template.docx"

    # Validate source exists
    if not source_pages.exists():
        logger.error(f"Source file not found: {source_pages}")
        logger.error("Make sure you're running from project root")
        return 1

    # Convert .pages to HTML using iwork-converter
    logger.info(f"Converting {source_pages} to HTML...")
    result = subprocess.run([
        '/tmp/iwork-converter/iwork-converter',
        str(source_pages),
        str(temp_html)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"iwork-converter failed: {result.stderr}")
        return 1

    logger.info(f"Converted to {temp_html}")

    # Create skill directory if needed
    skill_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Skill directory: {skill_dir}")

    # Build template
    logger.info("Creating template with 12 semantic styles...")
    builder = TemplateBuilder()

    if not builder.create_template(str(output_template)):
        logger.error("Template creation failed")
        return 1

    logger.info(f"✓ Template created: {output_template}")
    logger.info("\nTemplate includes 12 styles:")
    logger.info("  Paragraph: CV Name, Section Header, Body Text, Timeline Entry")
    logger.info("             Bullet Standard, Bullet Gray, Bullet Emphasis")
    logger.info("  Character: Play Title, Institution, Job Title, Orange Emphasis, Gray Text")
    logger.info("\nReady for use with format-resume skill!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Step 2: Make script executable**

```bash
chmod +x generate_cv_template.py
```

**Step 3: Run script to generate template**

```bash
python generate_cv_template.py
```

Expected output:
```
INFO: Converting my_documents/AJB CV 2024.pages to HTML...
INFO: Converted to /tmp/cv_for_template.html
INFO: Skill directory: ~/.claude/skills/career/format-resume
INFO: Creating template with 12 semantic styles...
INFO: ✓ Template created: ~/.claude/skills/career/format-resume/cv-template.docx
```

**Step 4: Verify template exists and has styles**

```bash
ls -lh ~/.claude/skills/career/format-resume/cv-template.docx
```

Expected: File exists with reasonable size (10-20KB)

**Step 5: Commit**

```bash
git add generate_cv_template.py
git commit -m "feat: add template generation script"
```

---

### Task 6: Visual Template Validation

**Files:**
- Create: `validate_template.py`

**Step 1: Write validation script**

File: `validate_template.py`

```python
#!/usr/bin/env python3
"""
Validate generated CV template.

Checks:
- All 12 styles present
- Styles have correct properties
- Template can be opened and used
"""
from pathlib import Path
from docx import Document
from cv_formatting.style_mapping import get_all_semantic_styles
import sys


def validate_template(template_path: Path) -> bool:
    """Validate template structure and styles."""

    if not template_path.exists():
        print(f"✗ Template not found: {template_path}")
        return False

    print(f"✓ Template exists: {template_path}")

    # Load template
    try:
        doc = Document(str(template_path))
    except Exception as e:
        print(f"✗ Failed to open template: {e}")
        return False

    print(f"✓ Template opens successfully")

    # Check all styles present
    style_names = {s.name for s in doc.styles}
    expected_styles = get_all_semantic_styles()

    missing = expected_styles - style_names
    if missing:
        print(f"✗ Missing styles: {missing}")
        return False

    print(f"✓ All 12 semantic styles present")

    # Check key properties
    checks_passed = 0
    checks_total = 0

    # Section Header should be bold orange
    checks_total += 1
    section = doc.styles['Section Header']
    if section.font.bold and section.font.color.rgb:
        print("✓ Section Header: bold orange")
        checks_passed += 1
    else:
        print("✗ Section Header: missing properties")

    # Timeline Entry should have hanging indent
    checks_total += 1
    timeline = doc.styles['Timeline Entry']
    if timeline.paragraph_format.left_indent:
        print("✓ Timeline Entry: has hanging indent")
        checks_passed += 1
    else:
        print("✗ Timeline Entry: missing hanging indent")

    # Play Title should be bold italic
    checks_total += 1
    play = doc.styles['Play Title']
    if play.font.bold and play.font.italic:
        print("✓ Play Title: bold italic")
        checks_passed += 1
    else:
        print("✗ Play Title: missing bold italic")

    if checks_passed == checks_total:
        print(f"\n✓ Template validation PASSED ({checks_passed}/{checks_total} checks)")
        return True
    else:
        print(f"\n✗ Template validation FAILED ({checks_passed}/{checks_total} checks)")
        return False


def main():
    """Run validation."""
    skill_dir = Path.home() / ".claude/skills/career/format-resume"
    template_path = skill_dir / "cv-template.docx"

    print("Validating CV template...\n")

    if validate_template(template_path):
        print("\nTemplate ready for use!")
        return 0
    else:
        print("\nTemplate has issues - review and fix")
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

**Step 2: Run validation**

```bash
python validate_template.py
```

Expected: All checks pass

**Step 3: Commit**

```bash
git add validate_template.py
git commit -m "feat: add template validation script"
```

---

### Task 7: Document Phase 1 Completion

**Files:**
- Create: `docs/TEMPLATE_GENERATION.md`

**Step 1: Write documentation**

File: `docs/TEMPLATE_GENERATION.md`

```markdown
# CV Template Generation

## Overview

This module extracts styles from a .pages CV document and creates a clean .docx template with semantic style names.

## Quick Start

```bash
# Generate template from source CV
python generate_cv_template.py

# Validate generated template
python validate_template.py
```

## Components

### 1. Style Parser (`cv_formatting/style_parser.py`)
Parses iwork-converter HTML/CSS output to extract style definitions.

### 2. Style Mapping (`cv_formatting/style_mapping.py`)
Consolidation map: 97 .pages styles → 12 semantic styles.

Based on usage analysis of actual CV content.

### 3. Template Builder (`cv_formatting/template_builder.py`)
Creates clean .docx template using python-docx.

## The 12 Semantic Styles

**Paragraph Styles:**
1. CV Name - Name at top
2. Section Header - "EDUCATION", "PROFESSIONAL EXPERIENCE" (bold orange)
3. Body Text - Standard paragraphs
4. Timeline Entry - Date + institution with 72pt hanging indent
5. Bullet Standard - Regular bullets
6. Bullet Gray - Gray bullets for dates/education
7. Bullet Emphasis - Bold italic bullets

**Character Styles:**
8. Play Title - Bold italic for productions (most used: 468 instances!)
9. Institution - Bold for institution names
10. Job Title - Bold italic for positions
11. Orange Emphasis - Bold orange (#FF6D49)
12. Gray Text - For dates and secondary info

## Output

Template saved to: `~/.claude/skills/career/format-resume/cv-template.docx`

Ready for use with format-resume skill (Phase 2).

## Design Document

See: `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`
```

**Step 2: Commit**

```bash
git add docs/TEMPLATE_GENERATION.md
git commit -m "docs: add template generation documentation"
```

---

### Task 8: Phase 1 Summary Commit

**Step 1: Run full test suite**

```bash
pytest cv_formatting/ tests/ -v
```

Expected: All tests pass

**Step 2: Verify template generation works end-to-end**

```bash
python generate_cv_template.py && python validate_template.py
```

Expected: Template created and validated

**Step 3: Create summary commit**

```bash
git add -A
git commit -m "feat(phase1): complete CV template extraction and generation

Phase 1 deliverables:
- Style parser for iwork-converter output
- Style consolidation mapping (97→12)
- Template builder with semantic names
- Template generation script
- Validation tooling
- Documentation

Template ready at ~/.claude/skills/career/format-resume/cv-template.docx

Next: Phase 2 - Document formatting skill
"
```

---

## Phase 2: Basic Formatting (Tasks 9-14)

### Task 9: Create Style Application Helper

**Files:**
- Create: `cv_formatting/style_applicator.py`
- Create: `tests/test_style_applicator.py`

**Step 1: Write test for style application**

File: `tests/test_style_applicator.py`

```python
import pytest
from pathlib import Path
from docx import Document
from cv_formatting.style_applicator import StyleApplicator


def test_apply_paragraph_style(tmp_path):
    """Test applying paragraph style to content"""
    template = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"
    output = tmp_path / "test-output.docx"

    content_mapping = [
        {
            "text": "EDUCATION",
            "style": "Section Header",
            "type": "paragraph"
        },
        {
            "text": "Standard body paragraph text.",
            "style": "Body Text",
            "type": "paragraph"
        }
    ]

    applicator = StyleApplicator(str(template))
    result = applicator.apply_styles(content_mapping, str(output))

    assert result is True
    assert output.exists()

    # Verify styles applied
    doc = Document(str(output))
    assert len(doc.paragraphs) == 2
    assert doc.paragraphs[0].style.name == "Section Header"
    assert doc.paragraphs[1].style.name == "Body Text"


def test_apply_character_style_inline(tmp_path):
    """Test applying character style within paragraph"""
    template = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"
    output = tmp_path / "test-output.docx"

    content_mapping = [
        {
            "text": "2023 - Present ",
            "style": "Timeline Entry",
            "type": "paragraph",
            "runs": [
                {"text": "2023 - Present ", "style": None},
                {"text": "California State University", "style": "Institution"}
            ]
        }
    ]

    applicator = StyleApplicator(str(template))
    result = applicator.apply_styles(content_mapping, str(output))

    assert result is True

    # Verify inline style applied
    doc = Document(str(output))
    para = doc.paragraphs[0]
    assert para.style.name == "Timeline Entry"
    assert len(para.runs) == 2
    assert para.runs[1].style.name == "Institution"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_style_applicator.py -v
```

Expected: FAIL - StyleApplicator not implemented

**Step 3: Write implementation**

File: `cv_formatting/style_applicator.py`

```python
"""Apply styles to document content using template."""
from docx import Document
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class StyleApplicator:
    """Applies styles to content using template document."""

    def __init__(self, template_path: str):
        """
        Initialize with template.

        Args:
            template_path: Path to cv-template.docx
        """
        self.template_path = template_path

    def apply_styles(self, content_mapping: List[Dict[str, Any]],
                     output_path: str) -> bool:
        """
        Apply styles to content and save document.

        Args:
            content_mapping: List of content elements with styles
            output_path: Where to save formatted document

        Returns:
            True if successful

        Content mapping format:
            [{
                "text": "Content text",
                "style": "Style Name",
                "type": "paragraph" | "inline",
                "runs": [  # optional, for inline styling
                    {"text": "text", "style": "Style Name"}
                ]
            }]
        """
        try:
            # Load template
            doc = Document(self.template_path)

            # Apply each content element
            for item in content_mapping:
                self._add_content_item(doc, item)

            # Save formatted document
            doc.save(output_path)
            logger.info(f"Document saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply styles: {e}")
            return False

    def _add_content_item(self, doc: Document, item: Dict[str, Any]):
        """Add single content item to document."""
        item_type = item.get('type', 'paragraph')

        if item_type == 'paragraph':
            # Add paragraph with style
            style_name = item.get('style', 'Body Text')

            # Check if item has inline runs
            if 'runs' in item:
                para = doc.add_paragraph(style=style_name)
                for run_data in item['runs']:
                    run = para.add_run(run_data['text'])
                    if run_data.get('style'):
                        run.style = run_data['style']
            else:
                # Simple paragraph
                doc.add_paragraph(item['text'], style=style_name)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_style_applicator.py -v
```

Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add cv_formatting/style_applicator.py tests/test_style_applicator.py
git commit -m "feat: implement style applicator for content formatting"
```

---

### Task 10: Create Command-Line Formatter

**Files:**
- Create: `format_cv.py`

**Step 1: Write basic CLI formatter**

File: `format_cv.py`

```python
#!/usr/bin/env python3
"""
Format CV content using template styles.

Usage:
    python format_cv.py input.txt output.docx

Input format: JSON with content mapping
"""
import sys
import json
from pathlib import Path
from cv_formatting.style_applicator import StyleApplicator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Format CV from content mapping."""
    if len(sys.argv) != 3:
        print("Usage: python format_cv.py <input.json> <output.docx>")
        print("\nInput JSON format:")
        print('[')
        print('  {"text": "EDUCATION", "style": "Section Header", "type": "paragraph"},')
        print('  {"text": "Body text", "style": "Body Text", "type": "paragraph"}')
        print(']')
        return 1

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return 1

    # Load content mapping
    try:
        with open(input_file) as f:
            content_mapping = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse input JSON: {e}")
        return 1

    # Get template
    template_path = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"

    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        logger.error("Run generate_cv_template.py first")
        return 1

    # Apply styles
    logger.info(f"Formatting {len(content_mapping)} content items...")
    applicator = StyleApplicator(str(template_path))

    if not applicator.apply_styles(content_mapping, str(output_file)):
        logger.error("Formatting failed")
        return 1

    logger.info(f"✓ Formatted document: {output_file}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Step 2: Create test input file**

File: `tests/fixtures/sample_cv_mapping.json`

```bash
mkdir -p tests/fixtures
```

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
    "text": "1994 - 1997 California Institute of the Arts",
    "style": "Timeline Entry",
    "type": "paragraph",
    "runs": [
      {"text": "1994 - 1997 ", "style": null},
      {"text": "California Institute of the Arts", "style": "Institution"}
    ]
  },
  {
    "text": "Master of Fine Arts, Acting",
    "style": "Body Text",
    "type": "paragraph"
  },
  {
    "text": "PROFESSIONAL EXPERIENCE",
    "style": "Section Header",
    "type": "paragraph"
  },
  {
    "text": "2023 - Present California State University Long Beach",
    "style": "Timeline Entry",
    "type": "paragraph",
    "runs": [
      {"text": "2023 - Present ", "style": null},
      {"text": "California State University Long Beach", "style": "Institution"}
    ]
  },
  {
    "text": "Interim Associate Dean for Student Success and Outreach",
    "style": "Timeline Entry",
    "type": "paragraph",
    "runs": [
      {"text": "Interim Associate Dean for Student Success and Outreach", "style": "Job Title"}
    ]
  },
  {
    "text": "Oversee 12 department-based staff academic advisors.",
    "style": "Body Text",
    "type": "paragraph"
  }
]
```

**Step 3: Test formatter**

```bash
python format_cv.py tests/fixtures/sample_cv_mapping.json /tmp/test-formatted-cv.docx
```

Expected: Document created successfully

**Step 4: Verify output manually**

```bash
open /tmp/test-formatted-cv.docx
```

Expected: Document opens with proper formatting

**Step 5: Commit**

```bash
git add format_cv.py tests/fixtures/sample_cv_mapping.json
git commit -m "feat: add CLI formatter for CV content"
```

---

### Task 11: Add Visual Verification - PDF Conversion

**Files:**
- Create: `cv_formatting/pdf_converter.py`
- Create: `tests/test_pdf_converter.py`

**Step 1: Write test for PDF conversion**

File: `tests/test_pdf_converter.py`

```python
import pytest
from pathlib import Path
from cv_formatting.pdf_converter import PDFConverter


@pytest.mark.skipif(not Path('/usr/local/bin/soffice').exists() and
                    not Path('/Applications/LibreOffice.app').exists(),
                    reason="LibreOffice not installed")
def test_convert_docx_to_pdf(tmp_path):
    """Test converting .docx to PDF"""
    # Create test .docx (or use existing)
    template = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"

    if not template.exists():
        pytest.skip("Template not available")

    output_pdf = tmp_path / "test.pdf"

    converter = PDFConverter()
    result = converter.convert_to_pdf(str(template), str(output_pdf))

    if converter.is_available():
        assert result is True
        assert output_pdf.exists()
    else:
        assert result is False


def test_pdf_converter_checks_availability():
    """Test that converter checks for LibreOffice"""
    converter = PDFConverter()
    available = converter.is_available()

    assert isinstance(available, bool)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_pdf_converter.py -v
```

Expected: FAIL - PDFConverter not implemented

**Step 3: Write implementation**

File: `cv_formatting/pdf_converter.py`

```python
"""Convert .docx documents to PDF using LibreOffice."""
import subprocess
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFConverter:
    """Converts .docx to PDF using LibreOffice."""

    def is_available(self) -> bool:
        """Check if LibreOffice is available."""
        return shutil.which('soffice') is not None

    def convert_to_pdf(self, docx_path: str, pdf_path: str) -> bool:
        """
        Convert .docx to PDF.

        Args:
            docx_path: Input .docx file
            pdf_path: Output .pdf file

        Returns:
            True if successful
        """
        if not self.is_available():
            logger.warning("LibreOffice not available - skipping PDF conversion")
            return False

        try:
            docx_path = Path(docx_path)
            pdf_path = Path(pdf_path)

            if not docx_path.exists():
                logger.error(f"Input file not found: {docx_path}")
                return False

            # Create output directory if needed
            pdf_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert using LibreOffice
            result = subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(pdf_path.parent),
                str(docx_path)
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error(f"Conversion failed: {result.stderr}")
                return False

            # LibreOffice creates PDF with same basename as input
            generated_pdf = pdf_path.parent / f"{docx_path.stem}.pdf"

            # Rename if needed
            if generated_pdf != pdf_path:
                generated_pdf.rename(pdf_path)

            logger.info(f"PDF created: {pdf_path}")
            return True

        except subprocess.TimeoutExpired:
            logger.error("PDF conversion timed out")
            return False
        except Exception as e:
            logger.error(f"PDF conversion error: {e}")
            return False
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_pdf_converter.py -v
```

Expected: PASS or SKIP (if LibreOffice not installed)

**Step 5: Commit**

```bash
git add cv_formatting/pdf_converter.py tests/test_pdf_converter.py
git commit -m "feat: add PDF conversion using LibreOffice"
```

---

### Task 12: Add Visual Verification - PDF to Images

**Files:**
- Create: `cv_formatting/image_generator.py`
- Create: `tests/test_image_generator.py`

**Step 1: Write test for image generation**

File: `tests/test_image_generator.py`

```python
import pytest
from pathlib import Path
from cv_formatting.image_generator import ImageGenerator


@pytest.mark.skipif(not Path('/usr/local/bin/pdftoppm').exists() and
                    not Path('/opt/homebrew/bin/pdftoppm').exists(),
                    reason="Poppler not installed")
def test_convert_pdf_to_images(tmp_path):
    """Test converting PDF to JPEG images"""
    # This test requires a real PDF
    # Skip if we don't have one
    generator = ImageGenerator()

    if not generator.is_available():
        pytest.skip("pdftoppm not available")

    # Would need actual PDF for full test
    assert generator.is_available() is True


def test_image_generator_checks_availability():
    """Test that generator checks for poppler"""
    generator = ImageGenerator()
    available = generator.is_available()

    assert isinstance(available, bool)
```

**Step 2: Run test**

```bash
pytest tests/test_image_generator.py -v
```

Expected: SKIP or minimal pass

**Step 3: Write implementation**

File: `cv_formatting/image_generator.py`

```python
"""Convert PDF to images using Poppler."""
import subprocess
import shutil
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Converts PDF to images using pdftoppm."""

    def is_available(self) -> bool:
        """Check if pdftoppm is available."""
        return shutil.which('pdftoppm') is not None

    def generate_images(self, pdf_path: str, output_dir: str,
                       dpi: int = 150) -> List[Path]:
        """
        Convert PDF pages to JPEG images.

        Args:
            pdf_path: Input PDF file
            output_dir: Directory for output images
            dpi: Resolution (default 150)

        Returns:
            List of generated image paths
        """
        if not self.is_available():
            logger.warning("pdftoppm not available - skipping image generation")
            return []

        try:
            pdf_path = Path(pdf_path)
            output_dir = Path(output_dir)

            if not pdf_path.exists():
                logger.error(f"PDF not found: {pdf_path}")
                return []

            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)

            # Base name for images
            base_name = output_dir / "page"

            # Convert
            result = subprocess.run([
                'pdftoppm',
                '-jpeg',
                '-r', str(dpi),
                str(pdf_path),
                str(base_name)
            ], capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                logger.error(f"Image generation failed: {result.stderr}")
                return []

            # Find generated images
            images = sorted(output_dir.glob('page-*.jpg'))

            logger.info(f"Generated {len(images)} images")
            return images

        except subprocess.TimeoutExpired:
            logger.error("Image generation timed out")
            return []
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return []
```

**Step 4: Run test**

```bash
pytest tests/test_image_generator.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add cv_formatting/image_generator.py tests/test_image_generator.py
git commit -m "feat: add PDF to image conversion using Poppler"
```

---

### Task 13: Integrate Visual Preview Workflow

**Files:**
- Modify: `format_cv.py`

**Step 1: Add preview option to CLI**

File: `format_cv.py`

```python
#!/usr/bin/env python3
"""
Format CV content using template styles.

Usage:
    python format_cv.py input.txt output.docx [--preview]
"""
import sys
import json
from pathlib import Path
from cv_formatting.style_applicator import StyleApplicator
from cv_formatting.pdf_converter import PDFConverter
from cv_formatting.image_generator import ImageGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Format CV from content mapping."""
    if len(sys.argv) < 3:
        print("Usage: python format_cv.py <input.json> <output.docx> [--preview]")
        return 1

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    preview = '--preview' in sys.argv

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return 1

    # Load content mapping
    try:
        with open(input_file) as f:
            content_mapping = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse input JSON: {e}")
        return 1

    # Get template
    template_path = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"

    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        return 1

    # Apply styles
    logger.info(f"Formatting {len(content_mapping)} content items...")
    applicator = StyleApplicator(str(template_path))

    if not applicator.apply_styles(content_mapping, str(output_file)):
        logger.error("Formatting failed")
        return 1

    logger.info(f"✓ Formatted document: {output_file}")

    # Generate preview if requested
    if preview:
        logger.info("Generating preview...")

        # Convert to PDF
        pdf_converter = PDFConverter()
        pdf_path = output_file.with_suffix('.pdf')

        if pdf_converter.convert_to_pdf(str(output_file), str(pdf_path)):
            logger.info(f"✓ PDF: {pdf_path}")

            # Convert to images
            image_gen = ImageGenerator()
            image_dir = output_file.parent / f"{output_file.stem}_images"
            images = image_gen.generate_images(str(pdf_path), str(image_dir))

            if images:
                logger.info(f"✓ Preview images: {image_dir}/")
                logger.info(f"  Generated {len(images)} page images")
                for img in images:
                    logger.info(f"  - {img.name}")
            else:
                logger.warning("Image generation skipped (pdftoppm not available)")
        else:
            logger.warning("PDF conversion skipped (LibreOffice not available)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Step 2: Test with preview**

```bash
python format_cv.py tests/fixtures/sample_cv_mapping.json /tmp/test-cv.docx --preview
```

Expected: Creates .docx, PDF, and images (if tools available)

**Step 3: Commit**

```bash
git add format_cv.py
git commit -m "feat: add preview option to CLI formatter"
```

---

### Task 14: Phase 2 Summary

**Step 1: Run full test suite**

```bash
pytest -v
```

Expected: All tests pass

**Step 2: Test end-to-end formatting**

```bash
python format_cv.py tests/fixtures/sample_cv_mapping.json /tmp/final-test.docx --preview
open /tmp/final-test.docx
```

Expected: Properly formatted document

**Step 3: Create summary commit**

```bash
git add -A
git commit -m "feat(phase2): complete basic CV formatting

Phase 2 deliverables:
- Style applicator for content → formatted doc
- CLI formatter with JSON input
- PDF conversion (LibreOffice)
- Image generation (Poppler)
- Visual preview workflow

Next: Phase 3 - Claude skill with semantic understanding
"
```

---

## Phase 3: Claude Skill (Tasks 15-20)

### Task 15: Create Skill Directory Structure

**Files:**
- Create: `~/.claude/skills/career/format-resume/skill.md`
- Create: `~/.claude/skills/career/format-resume/apply_styles.py`
- Create: `~/.claude/skills/career/format-resume/style-mappings.yaml`
- Create: `~/.claude/skills/career/format-resume/learned-preferences.yaml`

**Step 1: Create skill directory**

```bash
mkdir -p ~/.claude/skills/career/format-resume
```

**Step 2: Copy cv-template.docx (should already exist from Phase 1)**

```bash
ls -lh ~/.claude/skills/career/format-resume/cv-template.docx
```

Expected: Template exists from Phase 1

**Step 3: Copy helper script to skill directory**

```bash
cp format_cv.py ~/.claude/skills/career/format-resume/apply_styles.py
```

**Step 4: Create base style mappings file**

File: `~/.claude/skills/career/format-resume/style-mappings.yaml`

```yaml
# Semantic inference rules for CV formatting
version: 1.0

patterns:
  - name: cv_name
    description: "Name at top of CV"
    condition: "First line, ≤5 words, proper case"
    style: "CV Name"

  - name: section_header
    description: "Section headers like EDUCATION"
    condition: "ALL CAPS, short line, section divider"
    style: "Section Header"

  - name: timeline_entry
    description: "Date range + institution"
    condition: "Starts with date range pattern (YYYY - YYYY or YYYY - Present)"
    style: "Timeline Entry"
    inline_styles:
      institution: "Institution"

  - name: job_title
    description: "Job position title"
    condition: "Follows institution, italic context or bold italic text"
    style: "Timeline Entry"
    inline_style: "Job Title"

  - name: play_production_title
    description: "Play or production titles"
    condition: "Italic text in production/work context, often in lists"
    inline_style: "Play Title"

  - name: bullet_standard
    description: "Standard bullet points"
    condition: "Starts with •, -, *, or list marker"
    style: "Bullet Standard"

  - name: bullet_gray
    description: "Secondary bullets (dates, education details)"
    condition: "Bullet in education section or date context"
    style: "Bullet Gray"

  - name: body_paragraph
    description: "Standard body text"
    condition: "Regular paragraph under job/role"
    style: "Body Text"
```

**Step 5: Create empty learned preferences file**

File: `~/.claude/skills/career/format-resume/learned-preferences.yaml`

```yaml
# Learned formatting preferences
version: 1.0
last_updated: null
rules: []
```

**Step 6: Verify structure**

```bash
ls -la ~/.claude/skills/career/format-resume/
```

Expected: skill.md (next task), cv-template.docx, apply_styles.py, style-mappings.yaml, learned-preferences.yaml

**Step 7: Commit**

```bash
git add -A
git commit -m "feat: create format-resume skill directory structure"
```

---

### Task 16: Write Format Resume Skill

**Files:**
- Create: `~/.claude/skills/career/format-resume/skill.md`

**Step 1: Write skill definition**

File: `~/.claude/skills/career/format-resume/skill.md`

```markdown
---
name: format-resume
description: Intelligently format CV/resume content using semantic understanding and visual verification
---

# Format Resume Skill

## Purpose

Format CV/resume content with intelligent style application based on semantic context. Uses a clean template with 12 semantic styles and learns from your corrections over time.

## Usage

**Format new content:**
```
Format this CV: [paste content]
```

**Format from file:**
```
Format my-cv-draft.txt as a resume
```

## How It Works

1. **Semantic Analysis**: I analyze content to understand what each element represents (name, section header, institution, job title, etc.)

2. **Style Mapping**: Based on context, I assign appropriate styles:
   - "Anthony Byrnes" at top → CV Name
   - "EDUCATION" in caps → Section Header
   - "2023 - Present California State University" → Timeline Entry + Institution
   - "Romeo & Juliet" in productions → Play Title (not Job Title, even though both are bold italic!)

3. **Generate Document**: Create formatted .docx using template

4. **Visual Preview**: Show PDF preview images for review

5. **Learn from Corrections**: If you correct a style choice, I remember for next time

## The 12 Styles

**Paragraph:**
- CV Name - Your name at top
- Section Header - "EDUCATION", "PROFESSIONAL EXPERIENCE" (bold orange)
- Body Text - Standard paragraphs
- Timeline Entry - Date + institution with hanging indent
- Bullet Standard, Bullet Gray, Bullet Emphasis - List variations

**Character (inline):**
- Play Title - Bold italic for productions (most common!)
- Institution - Bold for school/company names
- Job Title - Bold italic for positions
- Orange Emphasis - Highlight text
- Gray Text - Dates, secondary info

## Workflow

**Step 1: Analyze Content**

I'll parse your content and create a structured understanding:

```
Line 1: "Anthony Byrnes" → CV Name (first line, short, proper name)
Line 2: "EDUCATION" → Section Header (all caps, section divider)
Line 3: "1994-1997 California Institute of the Arts" → Timeline Entry
        inline: "California Institute of the Arts" → Institution
```

I'll show you my analysis and ask: "Does this look right?"

**Step 2: Confirm Structure**

If my analysis is correct, say "yes" and I'll proceed.

If something's wrong: "No, line 3 should be Body Text, not Timeline Entry"

**Step 3: Generate Document**

I'll call the style applicator to create your formatted .docx:

```python
import json
import subprocess
from pathlib import Path

# Save content mapping
mapping_file = "/tmp/cv_mapping.json"
with open(mapping_file, 'w') as f:
    json.dump(content_mapping, f, indent=2)

# Format document
result = subprocess.run([
    "python",
    str(Path.home() / ".claude/skills/career/format-resume/apply_styles.py"),
    mapping_file,
    output_path,
    "--preview"
], capture_output=True, text=True)
```

**Step 4: Visual Preview**

I'll convert to PDF and generate page images to show you what it looks like.

You can review and request changes: "That committee role should be gray text, not body text"

**Step 5: Learn (if corrections made)**

If you made corrections, I'll update `learned-preferences.yaml`:

```yaml
rules:
  - pattern: "committee|advisory"
    context: "university service section"
    preferred_style: "Gray Text"
    learned_date: "2025-11-09"
    example: "Graduate Studies Advisory Committee"
```

Next time I format a CV with committee roles, I'll automatically apply gray text.

**Step 6: Finalize**

Once you're happy with the preview, I'll save the final document with a name based on context (e.g., "anthony-byrnes-cv.docx").

## Context Discrimination

The key advantage: I understand **semantic context**, not just patterns.

**Example: Bold Italic**

Traditional regex would apply the same style to all bold italic text. I distinguish:

- "***Interim Associate Dean***" after "2023 - Present CSULB" → Job Title (follows employer)
- "***Romeo & Juliet***" in productions list → Play Title (in artistic works context)

## Learning System

Corrections are automatically saved. No "save preferences" button needed.

**You:** "That should be gray text, it's a committee role"

**Me:** "✓ Updated formatting rules: committee roles → Gray Text"

**Next CV:** Automatically applies gray to committee roles without asking.

## Error Handling

**If template missing:**
- "Template not found. Run generate_cv_template.py first"

**If LibreOffice/Poppler unavailable:**
- "PDF preview not available (LibreOffice not installed)"
- "Continuing with .docx only..."

**If style mapping unclear:**
- "I'm not sure if this is a Job Title or Play Title - can you clarify?"

## Files

- `cv-template.docx` - Clean template with 12 semantic styles
- `apply_styles.py` - Python helper for style application
- `style-mappings.yaml` - Base semantic inference rules
- `learned-preferences.yaml` - Your accumulated corrections

## Related

- Design: `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`
- Template generation: `python generate_cv_template.py`
- Validation: `python validate_template.py`
```

**Step 2: Test skill is discoverable**

```bash
ls ~/.claude/skills/career/format-resume/skill.md
```

Expected: File exists

**Step 3: Commit to main project**

```bash
git add -A
git commit -m "feat: write format-resume skill definition"
```

---

### Task 17-20: Placeholder for Skill Testing and Refinement

*(These tasks would involve interactive testing with the Claude skill, which requires running in Claude Code environment. The implementation steps would be:)*

**Task 17:** Test skill with sample CV content
**Task 18:** Refine semantic analysis based on test results
**Task 19:** Test learning system with corrections
**Task 20:** Document skill usage examples

**For now, commit Phase 3 progress:**

```bash
git add -A
git commit -m "feat(phase3): complete format-resume skill foundation

Phase 3 deliverables:
- Skill directory structure
- Skill definition with semantic understanding
- Style mappings and learning system files
- Integration with Phase 2 tools

Ready for interactive testing in Claude Code

Next: Phase 4 & 5 - Visual verification and learning refinement
"
```

---

## Implementation Notes

### Dependencies

Install before starting:

```bash
# Python packages (in .venv)
pip install python-docx beautifulsoup4

# System tools
brew install libreoffice poppler

# Verify installations
soffice --version
pdftoppm -v
```

### Testing Strategy

- **Unit tests**: Each component independently
- **Integration tests**: End-to-end workflows
- **Manual validation**: Visual inspection of formatted documents

### Skill Testing

The skill (Phase 3+) requires testing in Claude Code environment with real user interaction. Cannot be fully automated.

**Test approach:**
1. Format sample CV content
2. Verify semantic analysis accuracy
3. Test correction learning
4. Verify visual preview workflow

---

## Success Criteria

**Phase 1 Complete:**
- ✅ Template generated with 12 semantic styles
- ✅ Validation confirms all styles present and correct
- ✅ Template usable by python-docx

**Phase 2 Complete:**
- ✅ Can format CV from JSON mapping
- ✅ Visual preview generates PDF and images (if tools available)
- ✅ End-to-end CLI workflow functional

**Phase 3 Complete:**
- ✅ Skill directory structure created
- ✅ Skill definition written
- ✅ Integration with Phase 2 tools working

**Remaining (Phases 4-5):**
- Interactive skill testing
- Learning system validation
- User documentation

---

**Total Tasks: 20**
**Estimated Time: 12-17 hours**
**Current Focus: Phases 1-3 (foundational tooling)**
