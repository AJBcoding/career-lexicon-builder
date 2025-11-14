# Quickstart: Latest Features

This guide covers the newest features added to Career Lexicon Builder for enhanced document management and lexicon transparency.

## Table of Contents

- [Overview](#overview)
- [Feature 1: Document Reference Tracking](#feature-1-document-reference-tracking)
- [Feature 2: Automatic Date Standardization](#feature-2-automatic-date-standardization)
- [Feature 3: Non-Interactive Mode](#feature-3-non-interactive-mode)
- [Complete Workflow Example](#complete-workflow-example)
- [Troubleshooting](#troubleshooting)

---

## Overview

The latest updates focus on **document traceability** and **workflow automation**:

- **See what documents were analyzed** - Every lexicon now lists its source files
- **Organized by date** - Files automatically get standardized date prefixes
- **Automated processing** - Skip manual confirmations for batch operations

All features work with your existing lexicons and documents with **automatic backups** before any modifications.

---

## Feature 1: Document Reference Tracking

### What It Does

Appends a comprehensive "Files Referenced" section to all your lexicons, showing exactly which career documents were analyzed. This provides full transparency into the sources behind your career philosophy, achievements, and language patterns.

### Quick Start

**Step 1: Preview Changes (Recommended)**

```bash
python3 append_document_references.py --dry-run
```

This shows what would happen without making any changes.

**Step 2: Run for Real**

```bash
python3 append_document_references.py
```

The script will:
1. Scan `my_documents/converted/` for all documents
2. Extract dates from filenames or PDF content
3. Ask you to confirm dates extracted from PDFs
4. Classify documents (CVs, Resumes, Cover Letters, etc.)
5. Create a timestamped backup of `lexicons_llm/`
6. Append organized file lists to all lexicons

### What Gets Added

Each lexicon file gets a new section at the end:

```markdown
---

## Files Referenced

### CVs
- 2024 AJB CV 2024.pdf
- 2015-11 AJB CV 2015 v2.pdf

### Resumes
- 2025-10-13 Byrnes, Anthony Resume - Colburn School submitted.pdf
- 2020-11-23 ajb resume.pdf

### Cover Letters
- 2025-01-15 CSULB AD cover letter.pdf
- 2024-03-20 Cover Letter - University Position.pdf

### Diversity Statements
- 2024-06-15 Diversity Statement.pdf

### Other Documents
- 2023-08-10 Professional References.pdf
```

Documents are:
- **Organized by type** - Clear categories for easy reference
- **Sorted chronologically** - Newest first within each category
- **Consistently formatted** - Standard date prefixes (see Feature 2)

### Safety Features

- **Automatic backups** - Creates `lexicons_llm_backup_TIMESTAMP/` before any changes
- **Idempotent** - Skips lexicons that already have "Files Referenced"
- **Collision detection** - Prevents duplicate filenames during standardization
- **Dry-run mode** - Preview all changes before committing

### Restoring from Backup

If something goes wrong:

```bash
# Remove modified lexicons
rm -rf lexicons_llm

# Restore from backup
mv lexicons_llm_backup_20241114_153022 lexicons_llm
```

Backups are kept indefinitely - delete them manually when you're confident in the results.

---

## Feature 2: Automatic Date Standardization

### What It Does

Automatically renames your career documents to a standard format with date prefixes, making them easier to organize and sort chronologically.

### How It Works

The script processes filenames in two ways:

**1. Files with dates in the filename:**
```
"2024-11-25 - Resume.pdf"      → Already standardized ✓
"Resume 2024-11-25.pdf"        → "2024-11-25 - Resume.pdf"
"Nov 25 2024 Resume.pdf"       → "2024-11-25 - Resume.pdf"
```

**2. Files without dates:**
```
"Resume.pdf"  → Extracts date from PDF content → "2024-03-15 - Resume.pdf"
                (You'll be asked to confirm)
```

### Date Extraction

When dates aren't in filenames, the script:
1. Opens the PDF
2. Searches for dates in the content (headers, footers, metadata)
3. Shows you the extracted date
4. Asks for confirmation before renaming

**Example interaction:**
```
Processing: Resume.pdf
  Extracted date: 2024-03-15
  Confirm this date? [y/n]: y
  ✓ Renamed to: 2024-03-15 - Resume.pdf
```

### Standard Format

All files end up as:
```
YYYY-MM-DD - original_filename.ext
```

Benefits:
- **Chronological sorting** - Files sort correctly in file browsers
- **Clear timeline** - See your career document history at a glance
- **Consistent references** - Lexicons show uniform date formats

---

## Feature 3: Non-Interactive Mode

### What It Does

Allows the append script to run without manual confirmations, perfect for automation or when you trust the extracted dates.

### Usage

```bash
python3 append_document_references.py --skip-confirmation
```

**What gets automated:**
- Accepts all date extractions from PDFs without asking
- Proceeds with all file renaming operations
- Completes the full append process unattended

**What's still safe:**
- Automatic backups still created
- Dry-run mode still available
- Collision detection still active
- Idempotency still applies

### When to Use

**Use `--skip-confirmation` when:**
- You've already reviewed dates in a dry-run
- You're processing documents with reliable metadata
- You're running in a CI/CD pipeline or script
- You trust the PDF date extraction

**Don't use it when:**
- First time running the script
- Documents might have incorrect dates in PDFs
- You want manual control over each rename

### Combining Flags

```bash
# Preview non-interactive run
python3 append_document_references.py --dry-run --skip-confirmation

# Full automated execution
python3 append_document_references.py --skip-confirmation
```

---

## Complete Workflow Example

Here's how to use all three features together when adding new career documents:

### Scenario: You've Added 5 New Documents

**Step 1: Place documents in the right folder**

```bash
# Your new files
my_documents/converted/
├── New Resume Jan 2025.pdf
├── Cover Letter - Tech Company.pdf
├── Updated CV.pdf
├── 2025-01-20 - Already Formatted Resume.pdf
└── References List.pdf
```

**Step 2: Preview the standardization**

```bash
python3 append_document_references.py --dry-run
```

Output shows:
```
DOCUMENT RENAMING (4 files need dates)
=====================================

New Resume Jan 2025.pdf
  → Would extract date from PDF content

Cover Letter - Tech Company.pdf
  → Would extract date from PDF content

Updated CV.pdf
  → Would extract date from PDF content

References List.pdf
  → Would extract date from PDF content

2025-01-20 - Already Formatted Resume.pdf
  ✓ Already has date prefix
```

**Step 3: Run interactively first time**

```bash
python3 append_document_references.py
```

The script asks you to confirm each extracted date:
```
Processing: New Resume Jan 2025.pdf
  Extracted date: 2025-01-15
  Confirm this date? [y/n]: y
  ✓ Renamed to: 2025-01-15 - New Resume Jan 2025.pdf
```

**Step 4: Verify the results**

```bash
ls -1 my_documents/converted/
```

All files now standardized:
```
2025-01-15 - New Resume Jan 2025.pdf
2025-01-18 - Cover Letter - Tech Company.pdf
2025-01-20 - Already Formatted Resume.pdf
2025-01-22 - Updated CV.pdf
2025-01-25 - References List.pdf
```

**Step 5: Check your lexicons**

Each lexicon file now shows:
```markdown
## Files Referenced

### CVs
- 2025-01-22 - Updated CV.pdf
- 2024 AJB CV 2024.pdf
...

### Resumes
- 2025-01-20 - Already Formatted Resume.pdf
- 2025-01-15 - New Resume Jan 2025.pdf
...

### Cover Letters
- 2025-01-18 - Cover Letter - Tech Company.pdf
...

### Other Documents
- 2025-01-25 - References List.pdf
...
```

**Step 6: Regenerate lexicons if needed**

If you want the lexicons to analyze the new documents:

```bash
# This will pick up the new files automatically
python3 run_llm_analysis.py
```

Then re-run the append script to update references:

```bash
# Files already have dates, so this runs quickly
python3 append_document_references.py --skip-confirmation
```

---

## Troubleshooting

### "Files Referenced" Already Exists

**Problem:**
```
Processing: 01_career_philosophy.md
  ⊗ Already contains 'Files Referenced' section - skipping
```

**Solution:**

The script is idempotent - it won't duplicate the section. If you want to refresh it:

1. Manually remove the old "Files Referenced" section from lexicons
2. Re-run the script

Or just leave it - the script handles this gracefully.

### Date Extraction Failed

**Problem:**
```
Processing: Mystery Document.pdf
  ✗ Could not extract date from PDF content
```

**Solution:**

Manually rename the file with a date prefix:
```bash
mv "Mystery Document.pdf" "2024-06-15 - Mystery Document.pdf"
```

Then re-run the script.

### Filename Collision

**Problem:**
```
Processing: Resume.pdf
  ✗ Target filename already exists: 2024-03-15 - Resume.pdf
```

**Solution:**

You have two files that would get the same name. Manually rename one:
```bash
mv "Resume.pdf" "2024-03-15 - Resume Version 2.pdf"
```

### Backup Directory Full

**Problem:**

Multiple backup directories taking up space:
```
lexicons_llm_backup_20241110_120000/
lexicons_llm_backup_20241112_143000/
lexicons_llm_backup_20241114_153022/
```

**Solution:**

Delete old backups once you've verified the current lexicons are correct:
```bash
# Keep only the most recent backup
rm -rf lexicons_llm_backup_20241110_120000
rm -rf lexicons_llm_backup_20241112_143000
```

### Script Won't Find PDFs

**Problem:**
```
Error: Directory not found: my_documents/converted/
```

**Solution:**

Ensure you're running from the project root:
```bash
cd /path/to/career-lexicon-builder
python3 append_document_references.py
```

---

## Additional Resources

- **Full documentation:** [docs/APPEND_DOCUMENT_REFERENCES.md](APPEND_DOCUMENT_REFERENCES.md)
- **Design details:** [docs/plans/2025-11-02-append-document-references-design.md](plans/2025-11-02-append-document-references-design.md)
- **Main README:** [README.md](../README.md)
- **Socratic Skills Guide:** [QUICKSTART_SOCRATIC_SKILLS.md](../QUICKSTART_SOCRATIC_SKILLS.md)

---

## Quick Reference

### Common Commands

```bash
# Preview changes
python3 append_document_references.py --dry-run

# Interactive run (first time)
python3 append_document_references.py

# Automated run (subsequent times)
python3 append_document_references.py --skip-confirmation

# Combined preview of automated run
python3 append_document_references.py --dry-run --skip-confirmation

# Restore from backup
mv lexicons_llm_backup_TIMESTAMP lexicons_llm
```

### File Organization

```
my_documents/converted/          ← Your source documents (standardized with dates)
lexicons_llm/                    ← Generated lexicons (with file references)
lexicons_llm_backup_TIMESTAMP/   ← Automatic safety backups
```

### Document Categories

- **CVs** - Curriculum Vitae
- **Resumes** - Job-specific resumes
- **Cover Letters** - Application cover letters
- **Diversity Statements** - DEI statements
- **Other Documents** - Everything else (references, teaching statements, etc.)
