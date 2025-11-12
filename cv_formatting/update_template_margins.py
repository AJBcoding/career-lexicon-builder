#!/usr/bin/env python3
"""
Update CV Template Margins and Indents

This script updates the career-documents-template.docx to match the reference
CV structure (AJB CV 2024.docx) with correct margins and paragraph indents.

Reference measurements:
- Document margins: 0.5" left/right, 0.75" top/bottom
- Timeline Entry: 1.0" left indent, -1.0" hanging, 1.0" tab stop
- Body Text: 1.0" left indent
- Bullet Standard: 1.0" left indent (aligns with position titles at 1.5" from page edge)

Usage:
    python3 cv_formatting/update_template_margins.py

Created: November 11, 2025
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT
import shutil
from datetime import datetime


def update_template(template_path, create_backup=True):
    """
    Update template with correct margins and indents.

    Args:
        template_path: Path to template file
        create_backup: Whether to create backup before modifying
    """
    if create_backup:
        backup_path = template_path.replace('.docx', f'-BACKUP-{datetime.now().strftime("%Y-%m-%d")}.docx')
        shutil.copy(template_path, backup_path)
        print(f"✓ Created backup: {backup_path}\n")

    # Load template
    doc = Document(template_path)

    print("=== APPLYING TEMPLATE FIXES ===\n")

    # Fix 1: Document margins
    section = doc.sections[0]
    print("1. Document Margins:")
    print(f"   Before: L={section.left_margin.inches:.2f}\" R={section.right_margin.inches:.2f}\" "
          f"T={section.top_margin.inches:.2f}\" B={section.bottom_margin.inches:.2f}\"")

    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)

    print(f"   After:  L={section.left_margin.inches:.2f}\" R={section.right_margin.inches:.2f}\" "
          f"T={section.top_margin.inches:.2f}\" B={section.bottom_margin.inches:.2f}\"")
    print()

    # Fix 2: Timeline Entry style
    print("2. Timeline Entry:")
    style = doc.styles['Timeline Entry']
    pf = style.paragraph_format
    print(f"   Before: left_indent={pf.left_indent.inches:.2f}\" first_line={pf.first_line_indent.inches:.2f}\"")

    pf.left_indent = Inches(1.0)
    pf.first_line_indent = Inches(-1.0)
    pf.tab_stops.clear_all()
    pf.tab_stops.add_tab_stop(Inches(1.0), alignment=WD_TAB_ALIGNMENT.LEFT)

    print(f"   After:  left_indent={pf.left_indent.inches:.2f}\" first_line={pf.first_line_indent.inches:.2f}\" tab@1.0\"")
    print()

    # Fix 3: Body Text style
    print("3. Body Text:")
    style = doc.styles['Body Text']
    pf = style.paragraph_format
    print(f"   Before: left_indent={pf.left_indent.inches:.2f}\"")

    pf.left_indent = Inches(1.0)

    print(f"   After:  left_indent={pf.left_indent.inches:.2f}\"")
    print()

    # Fix 4: Bullet Standard style
    # NOTE: Achievement lines should align with position titles (after tab)
    # Tab is at 1.0", so bullets need 1.0" left indent to match
    print("4. Bullet Standard:")
    style = doc.styles['Bullet Standard']
    pf = style.paragraph_format
    print(f"   Before: left_indent={pf.left_indent.inches:.2f}\" first_line={pf.first_line_indent.inches:.2f}\"")

    pf.left_indent = Inches(1.0)
    pf.first_line_indent = Inches(0.0)

    print(f"   After:  left_indent={pf.left_indent.inches:.2f}\" first_line={pf.first_line_indent.inches:.2f}\"")
    print()

    # Fix 5: Contact Info - ensure no space before
    print("5. Contact Info:")
    style = doc.styles['Contact Info']
    pf = style.paragraph_format
    space_before_before = pf.space_before.pt if pf.space_before else 0
    print(f"   Before: space_before={space_before_before:.1f}pt")

    pf.space_before = Pt(0)

    print(f"   After:  space_before=0.0pt")
    print()

    # Save updated template
    doc.save(template_path)
    print(f"✓ Saved updated template: {template_path}")
    print()
    print("=== TEMPLATE UPDATE COMPLETE ===")
    print("\nAll styles now match reference CV (AJB CV 2024.docx):")
    print("  • Document margins: 0.5\" L/R, 0.75\" T/B")
    print("  • Timeline Entry: 1.0\" indent, -1.0\" hanging, 1.0\" tab")
    print("  • Body Text: 1.0\" indent")
    print("  • Bullet Standard: 1.0\" indent (aligns with position titles)")


if __name__ == '__main__':
    template_path = 'cv_formatting/templates/career-documents-template.docx'
    update_template(template_path, create_backup=True)
