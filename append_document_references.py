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

from utils.date_parser import extract_date_from_filename
from utils.text_extraction import extract_text_from_document
import re


@dataclass
class FileEntry:
    """Represents a document with metadata."""
    path: Path
    filename: str
    date: Optional[datetime]
    date_source: str  # 'filename', 'content', or 'none'
    needs_confirmation: bool
    new_filename: Optional[str] = None


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

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
