# Append Document References Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create script to append "Files Referenced" sections to lexicon files, listing source documents organized by type and sorted reverse chronologically.

**Architecture:** Python script that scans converted documents, extracts/confirms dates, classifies by document type, and appends formatted markdown lists to existing lexicon files.

**Tech Stack:** Python 3.9+, existing utilities (`utils/text_extraction.py`, `utils/date_parser.py`, `core/document_processor.py`)

---

## Task 1: Create Basic Script Structure

**Files:**
- Create: `append_document_references.py`

**Step 1: Create script with argument parsing**

```python
#!/usr/bin/env python3
"""
Append document references to lexicon files.

Usage:
    python append_document_references.py [--dry-run]
"""

import argparse
import os
from pathlib import Path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Append document references to lexicon files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    args = parser.parse_args()

    print("Appending document references to lexicons...")
    print(f"Dry run mode: {args.dry_run}")

    # TODO: Implement


if __name__ == "__main__":
    main()
```

**Step 2: Test script runs**

Run: `python3 append_document_references.py --dry-run`
Expected output:
```
Appending document references to lexicons...
Dry run mode: True
```

**Step 3: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add script skeleton for document references"
```

---

## Task 2: Document Discovery

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add document discovery function**

Add after imports:
```python
from typing import List, Dict, Optional
from datetime import datetime


def discover_documents(converted_dir: Path) -> List[Path]:
    """
    Discover all documents in converted directory.

    Args:
        converted_dir: Path to my_documents/converted/

    Returns:
        List of document paths
    """
    if not converted_dir.exists():
        raise FileNotFoundError(f"Directory not found: {converted_dir}")

    # Get all files (not directories)
    documents = [
        f for f in converted_dir.iterdir()
        if f.is_file() and not f.name.startswith('.')
    ]

    return sorted(documents)
```

**Step 2: Update main() to use discovery**

Replace `# TODO: Implement` in main() with:
```python
    converted_dir = Path("my_documents/converted")

    try:
        documents = discover_documents(converted_dir)
        print(f"\nFound {len(documents)} documents in {converted_dir}")

        # Show first 3 for verification
        for doc in documents[:3]:
            print(f"  - {doc.name}")
        if len(documents) > 3:
            print(f"  ... and {len(documents) - 3} more")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    return 0
```

**Step 3: Test discovery**

Run: `python3 append_document_references.py --dry-run`
Expected output showing ~37 documents found

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add document discovery from converted folder"
```

---

## Task 3: Date Extraction from Filenames

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add filename date extraction**

Add import at top:
```python
from utils.date_parser import extract_date_from_filename
```

Add function after `discover_documents`:
```python
def extract_date_from_filename_safe(filename: str) -> Optional[datetime]:
    """
    Extract date from filename using existing parser.

    Args:
        filename: Document filename

    Returns:
        datetime object if date found in filename, None otherwise
    """
    try:
        date = extract_date_from_filename(filename)
        return date
    except Exception:
        # Filename doesn't contain parseable date
        return None
```

**Step 2: Add file entry dataclass**

Add after imports:
```python
from dataclasses import dataclass


@dataclass
class FileEntry:
    """Represents a document with metadata."""
    path: Path
    filename: str
    date: Optional[datetime]
    date_source: str  # 'filename', 'content', or 'none'
    needs_confirmation: bool
    new_filename: Optional[str] = None
```

**Step 3: Build file inventory in main()**

Replace the document loop in main() with:
```python
    try:
        documents = discover_documents(converted_dir)
        print(f"\nFound {len(documents)} documents in {converted_dir}")

        # Build file inventory
        file_entries: List[FileEntry] = []

        for doc in documents:
            date = extract_date_from_filename_safe(doc.name)

            if date:
                # Date found in filename - no confirmation needed
                entry = FileEntry(
                    path=doc,
                    filename=doc.name,
                    date=date,
                    date_source='filename',
                    needs_confirmation=False
                )
            else:
                # No date in filename - will need content extraction
                entry = FileEntry(
                    path=doc,
                    filename=doc.name,
                    date=None,
                    date_source='none',
                    needs_confirmation=True
                )

            file_entries.append(entry)

        # Summary
        files_with_dates = sum(1 for e in file_entries if e.date is not None)
        files_needing_extraction = sum(1 for e in file_entries if e.needs_confirmation)

        print(f"\nDate extraction summary:")
        print(f"  Files with filename dates: {files_with_dates}")
        print(f"  Files needing date extraction: {files_needing_extraction}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
```

**Step 4: Test date extraction**

Run: `python3 append_document_references.py --dry-run`
Expected output showing split between files with/without dates

**Step 5: Commit**

```bash
git add append_document_references.py
git commit -m "feat: extract dates from filenames"
```

---

## Task 4: Date Extraction from PDF Content

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add PDF date extraction function**

Add import:
```python
from utils.text_extraction import extract_text_from_document
import re
```

Add function:
```python
def extract_date_from_pdf_content(file_path: Path) -> Optional[datetime]:
    """
    Extract date from PDF content.

    Looks for dates in first 2 pages using common patterns.

    Args:
        file_path: Path to PDF file

    Returns:
        datetime object if date found, None otherwise
    """
    try:
        # Extract text from document
        text = extract_text_from_document(str(file_path))

        # Focus on first ~2000 characters (roughly first 2 pages)
        text_sample = text[:2000]

        # Date patterns to search for
        patterns = [
            # YYYY-MM-DD
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
            # Month DD, YYYY
            (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})', None),
            # MM/DD/YYYY
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
        ]

        dates_found = []

        for pattern, date_format in patterns:
            matches = re.findall(pattern, text_sample, re.IGNORECASE)
            for match in matches:
                try:
                    if date_format:
                        date_str = '-'.join(match) if isinstance(match, tuple) else match
                        date_obj = datetime.strptime(date_str, date_format)
                    else:
                        # Month DD, YYYY format
                        month_map = {
                            'january': 1, 'february': 2, 'march': 3, 'april': 4,
                            'may': 5, 'june': 6, 'july': 7, 'august': 8,
                            'september': 9, 'october': 10, 'november': 11, 'december': 12
                        }
                        month = month_map[match[0].lower()]
                        day = int(match[1])
                        year = int(match[2])
                        date_obj = datetime(year, month, day)

                    # Only accept reasonable dates (1990-2030)
                    if 1990 <= date_obj.year <= 2030:
                        dates_found.append(date_obj)
                except (ValueError, KeyError):
                    continue

        # Return most recent date found (likely to be document date)
        if dates_found:
            return max(dates_found)

        return None

    except Exception as e:
        print(f"    Warning: Could not extract date from {file_path.name}: {e}")
        return None
```

**Step 2: Update inventory building to extract from content**

In main(), replace the `else:` block that creates entries with `date_source='none'`:
```python
            else:
                # No date in filename - try extracting from content
                print(f"  Extracting date from: {doc.name}")
                content_date = extract_date_from_pdf_content(doc)

                if content_date:
                    entry = FileEntry(
                        path=doc,
                        filename=doc.name,
                        date=content_date,
                        date_source='content',
                        needs_confirmation=True
                    )
                else:
                    entry = FileEntry(
                        path=doc,
                        filename=doc.name,
                        date=None,
                        date_source='none',
                        needs_confirmation=True
                    )
```

**Step 3: Test content extraction**

Run: `python3 append_document_references.py --dry-run`
Expected: Progress messages showing date extraction from files without filename dates

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: extract dates from PDF content"
```

---

## Task 5: Interactive Date Confirmation

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add confirmation function**

Add function:
```python
def confirm_dates(file_entries: List[FileEntry]) -> List[FileEntry]:
    """
    Interactively confirm dates extracted from content.

    Args:
        file_entries: List of file entries

    Returns:
        Updated file entries with confirmed dates
    """
    entries_needing_confirmation = [
        e for e in file_entries if e.needs_confirmation
    ]

    if not entries_needing_confirmation:
        print("\nNo dates need confirmation.")
        return file_entries

    print(f"\n{'='*60}")
    print(f"DATE CONFIRMATION ({len(entries_needing_confirmation)} files)")
    print(f"{'='*60}\n")

    for entry in entries_needing_confirmation:
        print(f"File: {entry.filename}")

        if entry.date:
            print(f"Found Date: {entry.date.strftime('%Y-%m-%d')} (from PDF content)")
        else:
            print(f"Found Date: None")

        while True:
            response = input("Confirm? [y/n/enter new date (YYYY-MM-DD)]: ").strip()

            if response.lower() in ['y', 'yes', '']:
                # Accept the extracted date
                if entry.date:
                    # Generate new filename with date prefix
                    entry.new_filename = f"{entry.date.strftime('%Y-%m-%d')} - {entry.filename}"
                    print(f"  → Will rename to: {entry.new_filename}\n")
                else:
                    print(f"  → Keeping as-is (no date)\n")
                break

            elif response.lower() in ['n', 'no']:
                # Ask for correct date
                continue

            else:
                # Try to parse as date
                try:
                    new_date = datetime.strptime(response, '%Y-%m-%d')
                    entry.date = new_date
                    entry.date_source = 'user'
                    entry.new_filename = f"{new_date.strftime('%Y-%m-%d')} - {entry.filename}"
                    print(f"  → Will rename to: {entry.new_filename}\n")
                    break
                except ValueError:
                    print("  Invalid date format. Please use YYYY-MM-DD or y/n")
                    continue

    return file_entries
```

**Step 2: Add confirmation call in main()**

After building file_entries, add:
```python
        # Confirm dates that need it
        if not args.dry_run:
            file_entries = confirm_dates(file_entries)
        else:
            print("\n[DRY RUN] Skipping interactive confirmation")
```

**Step 3: Test confirmation (requires real run)**

Run: `python3 append_document_references.py` (no --dry-run)
Expected: Interactive prompts for files without filename dates

Then test dry-run still works:
Run: `python3 append_document_references.py --dry-run`
Expected: Skips confirmation

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add interactive date confirmation"
```

---

## Task 6: File Renaming

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add rename function**

Add function:
```python
def rename_files(file_entries: List[FileEntry], dry_run: bool = False) -> List[FileEntry]:
    """
    Rename files that have new filenames.

    Args:
        file_entries: List of file entries
        dry_run: If True, only show what would be renamed

    Returns:
        Updated file entries with new paths
    """
    entries_to_rename = [e for e in file_entries if e.new_filename]

    if not entries_to_rename:
        print("\nNo files need renaming.")
        return file_entries

    print(f"\n{'='*60}")
    print(f"FILE RENAMING ({len(entries_to_rename)} files)")
    print(f"{'='*60}\n")

    # Check for collisions
    existing_names = set(e.filename for e in file_entries)
    collisions = []

    for entry in entries_to_rename:
        if entry.new_filename in existing_names:
            collisions.append(entry.new_filename)

    if collisions:
        print("ERROR: Filename collisions detected:")
        for name in collisions:
            print(f"  - {name}")
        print("\nAborting rename operation.")
        return file_entries

    # Perform renames
    for entry in entries_to_rename:
        old_path = entry.path
        new_path = entry.path.parent / entry.new_filename

        print(f"  {entry.filename}")
        print(f"  → {entry.new_filename}")

        if not dry_run:
            try:
                old_path.rename(new_path)
                entry.path = new_path
                entry.filename = entry.new_filename
                print(f"  ✓ Renamed\n")
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
        else:
            print(f"  [DRY RUN]\n")

    return file_entries
```

**Step 2: Add rename call in main()**

After `confirm_dates`, add:
```python
        # Rename files
        file_entries = rename_files(file_entries, dry_run=args.dry_run)
```

**Step 3: Test dry-run rename**

Run: `python3 append_document_references.py --dry-run`
Expected: Shows what would be renamed without actually doing it

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add file renaming with collision detection"
```

---

## Task 7: Document Classification

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add classification function**

Add import:
```python
from enum import Enum
```

Add enum and function:
```python
class DocumentCategory(Enum):
    """Document categories for organization."""
    CV = "CVs"
    RESUME = "Resumes"
    COVER_LETTER = "Cover Letters"
    DIVERSITY_STATEMENT = "Diversity Statements"
    OTHER = "Other"


def classify_document(filename: str) -> DocumentCategory:
    """
    Classify document by filename.

    Args:
        filename: Document filename

    Returns:
        DocumentCategory
    """
    filename_lower = filename.lower()

    # Check patterns in order of specificity

    # Diversity statements (check before generic "letter")
    if 'diversity' in filename_lower and 'statement' in filename_lower:
        return DocumentCategory.DIVERSITY_STATEMENT

    # CVs
    if 'cv' in filename_lower or 'curriculum' in filename_lower:
        return DocumentCategory.CV

    # Resumes
    if 'resume' in filename_lower:
        return DocumentCategory.RESUME

    # Cover letters
    if 'cover' in filename_lower or 'letter' in filename_lower:
        return DocumentCategory.COVER_LETTER

    # Fallback
    return DocumentCategory.OTHER
```

**Step 2: Update FileEntry dataclass**

Add field to FileEntry:
```python
@dataclass
class FileEntry:
    """Represents a document with metadata."""
    path: Path
    filename: str
    date: Optional[datetime]
    date_source: str  # 'filename', 'content', or 'none'
    needs_confirmation: bool
    new_filename: Optional[str] = None
    category: Optional[DocumentCategory] = None  # Add this
```

**Step 3: Classify documents in main()**

After `rename_files`, add:
```python
        # Classify documents
        print(f"\n{'='*60}")
        print("CLASSIFYING DOCUMENTS")
        print(f"{'='*60}\n")

        for entry in file_entries:
            entry.category = classify_document(entry.filename)

        # Summary by category
        from collections import Counter
        category_counts = Counter(e.category for e in file_entries)

        for category in DocumentCategory:
            count = category_counts[category]
            if count > 0:
                print(f"  {category.value}: {count}")
```

**Step 4: Test classification**

Run: `python3 append_document_references.py --dry-run`
Expected: Shows count of documents per category

**Step 5: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add document classification by type"
```

---

## Task 8: Format Document Lists

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add formatting function**

Add function:
```python
def format_document_references(file_entries: List[FileEntry]) -> str:
    """
    Format document references as markdown.

    Args:
        file_entries: List of file entries

    Returns:
        Formatted markdown string
    """
    # Group by category
    by_category: Dict[DocumentCategory, List[FileEntry]] = {}

    for entry in file_entries:
        if entry.category not in by_category:
            by_category[entry.category] = []
        by_category[entry.category].append(entry)

    # Sort each category by date (newest first)
    for category in by_category:
        by_category[category].sort(
            key=lambda e: (e.date or datetime.min),
            reverse=True
        )

    # Build markdown
    lines = ["## Files Referenced", ""]

    # Process categories in order
    for category in DocumentCategory:
        if category not in by_category or not by_category[category]:
            continue

        lines.append(f"### {category.value}")

        for entry in by_category[category]:
            # Format with date prefix if available
            if entry.date:
                date_str = entry.date.strftime('%Y-%m-%d')
                # Check if filename already has date
                if entry.filename.startswith(date_str):
                    lines.append(f"- {entry.filename}")
                else:
                    lines.append(f"- {date_str} {entry.filename}")
            else:
                lines.append(f"- {entry.filename}")

        lines.append("")  # Blank line between categories

    return '\n'.join(lines)
```

**Step 2: Test formatting in main()**

After classification summary, add:
```python
        # Format document references
        print(f"\n{'='*60}")
        print("FORMATTED OUTPUT")
        print(f"{'='*60}\n")

        formatted_output = format_document_references(file_entries)
        print(formatted_output)
```

**Step 3: Test formatting**

Run: `python3 append_document_references.py --dry-run`
Expected: Shows formatted markdown output

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: format document references as markdown"
```

---

## Task 9: Append to Lexicon Files

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add append function**

Add function:
```python
def append_to_lexicons(formatted_refs: str, dry_run: bool = False) -> None:
    """
    Append document references to all lexicon files.

    Args:
        formatted_refs: Formatted markdown document references
        dry_run: If True, only show what would be done
    """
    lexicon_dir = Path("lexicons_llm")

    if not lexicon_dir.exists():
        print(f"Error: Lexicon directory not found: {lexicon_dir}")
        return

    lexicon_files = sorted(lexicon_dir.glob("*.md"))

    if not lexicon_files:
        print(f"Error: No lexicon files found in {lexicon_dir}")
        return

    print(f"\n{'='*60}")
    print(f"APPENDING TO LEXICONS ({len(lexicon_files)} files)")
    print(f"{'='*60}\n")

    for lexicon_file in lexicon_files:
        print(f"Processing: {lexicon_file.name}")

        # Read current content
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ✗ Error reading: {e}\n")
            continue

        # Check if "Files Referenced" already exists
        if "## Files Referenced" in content:
            print(f"  ⊗ Already contains 'Files Referenced' section - skipping\n")
            continue

        # Prepare new content
        separator = "\n\n---\n\n"
        new_content = content + separator + formatted_refs

        if not dry_run:
            try:
                with open(lexicon_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✓ Updated\n")
            except Exception as e:
                print(f"  ✗ Error writing: {e}\n")
        else:
            print(f"  [DRY RUN] Would append {len(formatted_refs)} characters\n")
```

**Step 2: Call append in main()**

After formatting, replace the print statement with:
```python
        # Append to lexicons
        append_to_lexicons(formatted_output, dry_run=args.dry_run)

        print(f"\n{'='*60}")
        print("COMPLETE")
        print(f"{'='*60}")
```

**Step 3: Test dry-run**

Run: `python3 append_document_references.py --dry-run`
Expected: Shows it would append to each lexicon file

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: append document references to lexicon files"
```

---

## Task 10: Backup and Safety

**Files:**
- Modify: `append_document_references.py`

**Step 1: Add backup function**

Add import:
```python
import shutil
```

Add function at beginning of file:
```python
def backup_lexicons() -> Path:
    """
    Create backup of lexicon files before modification.

    Returns:
        Path to backup directory
    """
    from datetime import datetime

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(f"lexicons_llm_backup_{timestamp}")

    lexicon_dir = Path("lexicons_llm")

    if not lexicon_dir.exists():
        raise FileNotFoundError(f"Lexicon directory not found: {lexicon_dir}")

    print(f"Creating backup: {backup_dir}")
    shutil.copytree(lexicon_dir, backup_dir)
    print(f"  ✓ Backup created\n")

    return backup_dir
```

**Step 2: Add backup call in main()**

Right after parsing args and before any processing, add:
```python
    print("Appending document references to lexicons...")
    print(f"Dry run mode: {args.dry_run}\n")

    # Create backup (unless dry-run)
    if not args.dry_run:
        try:
            backup_dir = backup_lexicons()
            print(f"Note: Backup saved to {backup_dir}")
            print("You can restore with: rm -rf lexicons_llm && mv {backup_dir} lexicons_llm\n")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
            response = input("Continue anyway? [y/N]: ").strip().lower()
            if response != 'y':
                print("Aborted.")
                return 1
```

**Step 3: Test backup**

Run: `python3 append_document_references.py --dry-run`
Expected: Skips backup

Run: `python3 append_document_references.py` (real run, but cancel when prompted)
Expected: Creates backup directory

**Step 4: Commit**

```bash
git add append_document_references.py
git commit -m "feat: add lexicon backup before modification"
```

---

## Task 11: Final Testing and Documentation

**Files:**
- Create: `docs/APPEND_DOCUMENT_REFERENCES.md`
- Modify: `append_document_references.py`

**Step 1: Add docstring header to script**

Add at top of file after the triple-quote docstring:
```python
"""
Append document references to lexicon files.

This script:
1. Discovers documents in my_documents/converted/
2. Extracts dates from filenames (using date_parser)
3. For files without filename dates: extracts from PDF content
4. Interactively confirms extracted dates
5. Renames files to format: YYYY-MM-DD - filename.pdf
6. Classifies documents by type (CV, Resume, Cover Letter, etc.)
7. Formats as markdown lists sorted by date (newest first)
8. Appends to all lexicon files in lexicons_llm/

Usage:
    # Dry run (no changes)
    python3 append_document_references.py --dry-run

    # Real run (interactive)
    python3 append_document_references.py

The script creates backups before modifying lexicons.
"""
```

**Step 2: Create usage documentation**

Create `docs/APPEND_DOCUMENT_REFERENCES.md`:
```markdown
# Append Document References

Script to append "Files Referenced" sections to lexicon files.

## Purpose

Adds a comprehensive list of all source documents to the end of each lexicon file, organized by document type and sorted chronologically.

## Usage

### Dry Run (Recommended First)

```bash
python3 append_document_references.py --dry-run
```

Shows what would happen without making any changes.

### Real Run

```bash
python3 append_document_references.py
```

**Interactive prompts:** You'll be asked to confirm dates extracted from PDF content.

**Safety:** Creates timestamped backup before modifying lexicons.

## What It Does

1. **Scans** `my_documents/converted/` for all documents
2. **Extracts dates** from filenames (e.g., "2024-11-25 - file.pdf")
3. **For files without dates:** Extracts from PDF content and asks for confirmation
4. **Renames files** to standard format: `YYYY-MM-DD - original_name.pdf`
5. **Classifies** documents into categories:
   - CVs
   - Resumes
   - Cover Letters
   - Diversity Statements
   - Other
6. **Formats** as markdown lists sorted newest-first
7. **Appends** to all files in `lexicons_llm/`

## Output Format

```markdown
## Files Referenced

### CVs
- 2024 AJB CV 2024.pdf
- 2015-11 AJB CV 2015 v2.pdf

### Resumes
- 2025-10-13 Byrnes, Anthony Resume - Colburn School submitted.pdf
- 2020-11-23 ajb resume.pdf

### Cover Letters
- 2025-01-15 CSULB AD cover letter.pdf
...
```

## Safety Features

- **Dry-run mode** to preview changes
- **Automatic backups** before modifying lexicons
- **Collision detection** prevents duplicate filenames
- **Idempotent** - skips lexicons that already have "Files Referenced"

## Restoring from Backup

If something goes wrong:

```bash
rm -rf lexicons_llm
mv lexicons_llm_backup_TIMESTAMP lexicons_llm
```

## Integration with Lexicon Pipeline

This is a **one-time update script**. To integrate into the automated pipeline, see:
- Design doc: `docs/plans/2025-11-02-append-document-references-design.md`
- Section: "Future Integration: Approach 3 (LLM-Based)"
```

**Step 3: Commit documentation**

```bash
git add docs/APPEND_DOCUMENT_REFERENCES.md append_document_references.py
git commit -m "docs: add usage documentation for document references"
```

---

## Task 12: End-to-End Test

**Files:**
- Test: `append_document_references.py`

**Step 1: Run complete dry-run test**

Run: `python3 append_document_references.py --dry-run`

Verify:
- [ ] Discovers all documents
- [ ] Extracts dates from filenames correctly
- [ ] Shows content extraction for files without dates
- [ ] Shows classification summary
- [ ] Shows formatted markdown output
- [ ] Shows which lexicons would be updated

**Step 2: Run real execution (with backup)**

Run: `python3 append_document_references.py`

During execution:
- [ ] Backup is created
- [ ] Interactive prompts appear for date confirmation
- [ ] File renames happen (if applicable)
- [ ] Lexicons are updated

**Step 3: Verify lexicon updates**

```bash
tail -50 lexicons_llm/01_career_philosophy.md
tail -50 lexicons_llm/02_achievement_library.md
tail -50 lexicons_llm/03_narrative_patterns.md
tail -50 lexicons_llm/04_language_bank.md
```

Verify each has:
- [ ] `---` separator
- [ ] `## Files Referenced` heading
- [ ] Organized by category
- [ ] Sorted newest-first within categories

**Step 4: Verify idempotency**

Run again: `python3 append_document_references.py`

Expected: All lexicons show "Already contains 'Files Referenced' section - skipping"

**Step 5: Final commit**

```bash
git add lexicons_llm/*.md
git commit -m "feat: append document references to all lexicons"
```

---

## Task 13: Merge to Main

**Files:**
- N/A (git operations)

**Step 1: Return to main directory and review changes**

```bash
cd ../..
git worktree list
git log feature/append-document-references --oneline
```

**Step 2: Merge feature branch**

```bash
git checkout main
git merge feature/append-document-references --no-ff
```

**Step 3: Verify merge**

```bash
ls -la append_document_references.py
tail -30 lexicons_llm/01_career_philosophy.md
```

**Step 4: Clean up worktree**

```bash
git worktree remove .worktrees/append-document-references
git branch -d feature/append-document-references
```

**Step 5: Final verification**

```bash
python3 append_document_references.py --dry-run
```

Expected: Shows "Already contains" messages (idempotent)

---

## Success Criteria

- [x] Script discovers all 37 documents
- [x] Dates extracted from filenames and content
- [x] Interactive confirmation for content-extracted dates
- [x] Files renamed to standard format
- [x] Documents classified correctly
- [x] All 4 lexicons updated with "Files Referenced" section
- [x] Documents sorted by category and date (newest first)
- [x] Backups created before modification
- [x] Script is idempotent (safe to run multiple times)
- [x] Documentation complete

## Notes

- **YAGNI**: No CLI options beyond --dry-run
- **DRY**: Reuses existing utilities (date_parser, text_extraction)
- **TDD**: Verify each step before proceeding
- **Frequent commits**: Each task is one commit

## Future Work

See design doc section "Future Integration: Approach 3 (LLM-Based)" for integrating into `run_llm_analysis.py` pipeline using Claude API for more robust date extraction.
