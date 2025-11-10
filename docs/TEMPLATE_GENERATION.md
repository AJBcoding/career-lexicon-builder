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
