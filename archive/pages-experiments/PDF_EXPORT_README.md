# PDF Export Script

This script converts all markdown files from your career applications and lexicons to professionally formatted PDFs.

## Features

- Adds "Generated on YYYY-MM-DD" to each PDF (both in header and content)
- Filename format: `2025-11-01-filename.pdf`
- Professional formatting with:
  - Page numbers
  - Clean typography
  - Syntax highlighting for code blocks
  - Proper table formatting
  - Preserved markdown structure

## Installation

Install the required dependencies:

```bash
pip install -r requirements-pdf-export.txt
```

**Note:** WeasyPrint requires some system dependencies. On macOS:
```bash
brew install pango cairo gdk-pixbuf libffi
```

## Usage

Simply run the script:

```bash
python3 export_to_pdf.py
```

Or make it executable:

```bash
chmod +x export_to_pdf.py
./export_to_pdf.py
```

## Output

PDFs are saved to `document-exports/` with this structure:

```
document-exports/
├── career-applications/
│   └── 2025-10-22-associate-dean-cao-ucla/
│       ├── 2025-11-01-00-job-description.pdf
│       ├── 2025-11-01-01-job-analysis.pdf
│       └── 2025-11-01-03-gap-analysis-and-cover-letter-plan.pdf
└── lexicons/
    ├── 2025-11-01-01_career_philosophy.pdf
    ├── 2025-11-01-02_achievement_library.pdf
    ├── 2025-11-01-03_narrative_patterns.pdf
    └── 2025-11-01-04_language_bank.pdf
```

## What Gets Exported

- **Career Applications**: All `.md` files in `career-applications/` (preserving folder structure)
- **Lexicons**: All `.md` files in `lexicons_llm/`

## Troubleshooting

**Error: "No module named 'weasyprint'"**
- Run: `pip install -r requirements-pdf-export.txt`

**Error: "Cannot load library: libcairo"**
- On macOS: `brew install cairo pango gdk-pixbuf`
- On Ubuntu: `sudo apt-get install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0`

**PDFs look wrong or have missing fonts**
- Ensure system fonts are available
- WeasyPrint uses system fonts for rendering