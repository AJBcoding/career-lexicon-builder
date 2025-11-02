#!/usr/bin/env python3
"""
Append document references to lexicon files.

Usage:
    python append_document_references.py [--dry-run]
"""

import argparse
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from utils.date_parser import extract_date_from_filename
from utils.text_extraction import extract_text_from_document
import re


class DocumentCategory(Enum):
    """Document categories for organization."""
    CV = "CVs"
    RESUME = "Resumes"
    COVER_LETTER = "Cover Letters"
    DIVERSITY_STATEMENT = "Diversity Statements"
    OTHER = "Other"


@dataclass
class FileEntry:
    """Represents a document with metadata."""
    path: Path
    filename: str
    date: Optional[datetime]
    date_source: str  # 'filename', 'content', or 'none'
    needs_confirmation: bool
    new_filename: Optional[str] = None
    category: Optional[DocumentCategory] = None


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
        if date:
            # Convert date object to datetime object
            return datetime(date.year, date.month, date.day)
        return None
    except Exception:
        # Filename doesn't contain parseable date
        return None


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
        result = extract_text_from_document(str(file_path))

        # Check if extraction was successful
        if not result.get('success', False):
            return None

        text = result.get('text', '')
        if not text:
            return None

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
                    if date_format is not None:
                        # Format string patterns (YYYY-MM-DD, MM/DD/YYYY)
                        # Reconstruct date string with correct separator
                        if isinstance(match, tuple):
                            # Determine separator from format string
                            if '/' in date_format:
                                date_str = '/'.join(match)
                            elif '-' in date_format:
                                date_str = '-'.join(match)
                            else:
                                date_str = ''.join(match)
                        else:
                            date_str = match
                        date_obj = datetime.strptime(date_str, date_format)
                    else:
                        # Month name pattern (Month DD, YYYY)
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
        print(f"  -> {entry.new_filename}")

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

    converted_dir = Path("my_documents/converted")

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

            file_entries.append(entry)

        # Summary
        files_with_dates = sum(1 for e in file_entries if e.date is not None)
        files_needing_extraction = sum(1 for e in file_entries if e.needs_confirmation)

        print(f"\nDate extraction summary:")
        print(f"  Files with filename dates: {files_with_dates}")
        print(f"  Files needing date extraction: {files_needing_extraction}")

        # Confirm dates that need it
        if not args.dry_run:
            file_entries = confirm_dates(file_entries)
        else:
            print("\n[DRY RUN] Skipping interactive confirmation")

        # Rename files
        file_entries = rename_files(file_entries, dry_run=args.dry_run)

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

        # Format document references
        print(f"\n{'='*60}")
        print("FORMATTED OUTPUT")
        print(f"{'='*60}\n")

        formatted_output = format_document_references(file_entries)
        print(formatted_output)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
