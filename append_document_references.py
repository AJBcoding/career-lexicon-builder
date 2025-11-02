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

    return 0


if __name__ == "__main__":
    main()
