#!/usr/bin/env python3
"""Add cover letter specific styles to the career documents template."""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
import sys


def add_cover_letter_styles(template_path):
    """Add cover letter specific styles to template."""

    doc = Document(template_path)
    styles = doc.styles

    print("Adding cover letter styles to template...")

    # 1. Contact Name (paragraph style)
    try:
        style = styles.add_style('Contact Name', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(10)
        style.font.bold = True
        style.paragraph_format.space_after = Pt(0)
        print("✓ Added 'Contact Name' style")
    except:
        print("  'Contact Name' style already exists")

    # 2. Contact Info (paragraph style)
    try:
        style = styles.add_style('Contact Info', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(10)
        style.paragraph_format.space_after = Pt(0)
        print("✓ Added 'Contact Info' style")
    except:
        print("  'Contact Info' style already exists")

    # 3. Recipient Address (paragraph style)
    try:
        style = styles.add_style('Recipient Address', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(11)
        style.paragraph_format.space_after = Pt(0)
        style.paragraph_format.space_before = Pt(12)  # Space before first address line
        print("✓ Added 'Recipient Address' style")
    except:
        print("  'Recipient Address' style already exists")

    # 4. RE Line (paragraph style) - Bold, 13pt, Orange
    try:
        style = styles.add_style('RE Line', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(13)
        style.font.bold = True
        style.font.color.rgb = RGBColor(255, 109, 73)  # Orange
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(12)
        print("✓ Added 'RE Line' style")
    except:
        print("  'RE Line' style already exists")

    # 5. Page Header (paragraph style)
    try:
        style = styles.add_style('Page Header', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(10)
        style.font.bold = True  # Left side is bold
        style.paragraph_format.space_after = Pt(12)
        print("✓ Added 'Page Header' style")
    except:
        print("  'Page Header' style already exists")

    # 6. Play Title (character style for inline italic)
    try:
        style = styles.add_style('Play Title', WD_STYLE_TYPE.CHARACTER)
        style.font.name = 'Helvetica'
        style.font.italic = True
        print("✓ Added 'Play Title' character style")
    except:
        print("  'Play Title' style already exists")

    # 7. Signature Name (same as Body Text, but documenting explicitly)
    # Actually just use Body Text for this

    # Save updated template
    doc.save(template_path)
    print(f"\n✓ Template updated: {template_path}")
    print("\nNew styles added:")
    print("  - Contact Name (paragraph)")
    print("  - Contact Info (paragraph)")
    print("  - Recipient Address (paragraph)")
    print("  - RE Line (paragraph, orange)")
    print("  - Page Header (paragraph)")
    print("  - Play Title (character, italic)")


if __name__ == '__main__':
    template_path = 'cv_formatting/templates/career-documents-template.docx'

    add_cover_letter_styles(template_path)
    print("\nDone! Template ready for cover letters.")
