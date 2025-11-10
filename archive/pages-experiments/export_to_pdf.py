#!/usr/bin/env python3
"""
Export markdown files from career applications and lexicons to formatted PDFs.
Adds generation date both internally and to filename.
"""

import os
import sys
from datetime import date
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Configuration
PROJECT_ROOT = Path(__file__).parent
CAREER_APPS_DIR = PROJECT_ROOT / "career-applications"
LEXICONS_DIR = PROJECT_ROOT / "lexicons_llm"
EXPORT_DIR = PROJECT_ROOT / "document-exports"
DATE_FORMAT = "%Y-%m-%d"
TODAY = date.today().strftime(DATE_FORMAT)

# CSS for PDF formatting
PDF_STYLE = """
@page {
    size: letter;
    margin: 1in;
    @top-center {
        content: "Generated on """ + TODAY + """";
        font-size: 9pt;
        color: #666;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    font-size: 24pt;
    margin-top: 0;
    margin-bottom: 12pt;
    color: #1a1a1a;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 8pt;
}

h2 {
    font-size: 18pt;
    margin-top: 16pt;
    margin-bottom: 10pt;
    color: #1a1a1a;
}

h3 {
    font-size: 14pt;
    margin-top: 12pt;
    margin-bottom: 8pt;
    color: #333;
}

h4 {
    font-size: 12pt;
    margin-top: 10pt;
    margin-bottom: 6pt;
    color: #555;
}

code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 10pt;
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
}

pre {
    background-color: #f6f8fa;
    padding: 12pt;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #ddd;
    padding-left: 12pt;
    margin-left: 0;
    color: #666;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8pt;
    text-align: left;
}

th {
    background-color: #f6f8fa;
    font-weight: 600;
}

ul, ol {
    margin: 8pt 0;
    padding-left: 24pt;
}

li {
    margin: 4pt 0;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 16pt 0;
}

a {
    color: #0366d6;
    text-decoration: none;
}

.generation-notice {
    font-size: 9pt;
    color: #666;
    text-align: right;
    margin-bottom: 20pt;
    font-style: italic;
}
"""


def create_export_directories():
    """Create the export directory structure."""
    # Main export directory
    EXPORT_DIR.mkdir(exist_ok=True)

    # Subdirectories
    (EXPORT_DIR / "career-applications").mkdir(exist_ok=True)
    (EXPORT_DIR / "lexicons").mkdir(exist_ok=True)

    print(f"✓ Created export directory: {EXPORT_DIR}")


def convert_markdown_to_pdf(md_file: Path, output_dir: Path):
    """
    Convert a markdown file to PDF with generation date.

    Args:
        md_file: Path to markdown file
        output_dir: Directory to save PDF
    """
    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'tables',
            'fenced_code',
            'toc'
        ])
        html_content = md.convert(md_content)

        # Create full HTML document with generation notice
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{md_file.stem}</title>
        </head>
        <body>
            <div class="generation-notice">Generated on {TODAY}</div>
            {html_content}
        </body>
        </html>
        """

        # Generate PDF filename with date prefix
        pdf_filename = f"{TODAY}-{md_file.stem}.pdf"
        pdf_path = output_dir / pdf_filename

        # Convert HTML to PDF
        font_config = FontConfiguration()
        html_obj = HTML(string=full_html)
        css = CSS(string=PDF_STYLE, font_config=font_config)

        html_obj.write_pdf(pdf_path, stylesheets=[css], font_config=font_config)

        print(f"  ✓ {md_file.name} → {pdf_filename}")
        return True

    except Exception as e:
        print(f"  ✗ Error converting {md_file.name}: {e}")
        return False


def export_career_applications():
    """Export all markdown files from career applications."""
    if not CAREER_APPS_DIR.exists():
        print(f"⚠ Career applications directory not found: {CAREER_APPS_DIR}")
        return 0

    print(f"\n📁 Exporting Career Applications from: {CAREER_APPS_DIR}")

    count = 0
    # Process all .md files in all subdirectories
    for md_file in CAREER_APPS_DIR.rglob("*.md"):
        # Create subdirectory structure in exports
        relative_path = md_file.parent.relative_to(CAREER_APPS_DIR)
        output_dir = EXPORT_DIR / "career-applications" / relative_path
        output_dir.mkdir(parents=True, exist_ok=True)

        if convert_markdown_to_pdf(md_file, output_dir):
            count += 1

    print(f"✓ Exported {count} career application documents")
    return count


def export_lexicons():
    """Export all markdown files from lexicons."""
    if not LEXICONS_DIR.exists():
        print(f"⚠ Lexicons directory not found: {LEXICONS_DIR}")
        return 0

    print(f"\n📁 Exporting Lexicons from: {LEXICONS_DIR}")

    output_dir = EXPORT_DIR / "lexicons"
    count = 0

    # Process all .md files
    for md_file in LEXICONS_DIR.glob("*.md"):
        if convert_markdown_to_pdf(md_file, output_dir):
            count += 1

    print(f"✓ Exported {count} lexicon documents")
    return count


def main():
    """Main execution function."""
    print(f"🚀 Starting PDF export process")
    print(f"📅 Generation date: {TODAY}")
    print("=" * 60)

    # Create export directories
    create_export_directories()

    # Export documents
    career_count = export_career_applications()
    lexicon_count = export_lexicons()

    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Export complete!")
    print(f"   Career Applications: {career_count} files")
    print(f"   Lexicons: {lexicon_count} files")
    print(f"   Total: {career_count + lexicon_count} PDFs generated")
    print(f"\n📂 PDFs saved to: {EXPORT_DIR}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠ Export cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)