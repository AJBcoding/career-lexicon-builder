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
