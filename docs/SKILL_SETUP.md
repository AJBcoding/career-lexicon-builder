# Format Resume Skill Setup

## Overview

The format-resume skill provides intelligent CV/resume formatting with semantic understanding and visual verification. This document tracks the skill directory structure and configuration.

## Skill Directory Location

`~/.claude/skills/career/format-resume/`

## Files Created

### 1. cv-template.docx
Clean .docx template with 12 semantic styles (created in Phase 1).
- Size: ~36KB
- Contains: All paragraph and character styles for CV formatting

### 2. apply_styles.py
Python helper script for applying styles to content.
- Copied from: `format_cv.py`
- Usage: `python apply_styles.py <input.json> <output.docx> [--preview]`

### 3. style-mappings.yaml
Semantic inference rules for CV formatting.
- Version: 1.0
- Contains: 8 pattern definitions for content type detection
- Patterns include: cv_name, section_header, timeline_entry, job_title, play_production_title, bullet variants, body_paragraph

### 4. learned-preferences.yaml
Empty template for accumulated formatting preferences.
- Version: 1.0
- Structure: Rules array for learned patterns
- Will be populated as user makes corrections

### 5. skill.md (Task 16)
Skill definition and documentation (to be created in next task).

## Verification

Check that all files exist:

```bash
ls -la ~/.claude/skills/career/format-resume/
```

Expected output:
- apply_styles.py (3.6KB, executable)
- cv-template.docx (36KB)
- learned-preferences.yaml (75 bytes)
- style-mappings.yaml (1.4KB)
- skill.md (to be created)

## Usage

The skill will be invoked via Claude Code:

```
Format this CV: [content]
```

The skill will:
1. Analyze content semantically
2. Apply appropriate styles using mappings
3. Generate formatted .docx
4. Provide visual preview (PDF + images)
5. Learn from corrections

## Integration

- **Template Builder**: `cv_formatting/template_builder.py`
- **Style Applicator**: `cv_formatting/style_applicator.py`
- **PDF Converter**: `cv_formatting/pdf_converter.py`
- **Image Generator**: `cv_formatting/image_generator.py`

## Next Steps

- Task 16: Create skill.md with full skill definition
- Task 17-20: Interactive testing and refinement

## Design Document

See: `docs/plans/2025-11-09-cv-style-extraction-and-formatting-design.md`
