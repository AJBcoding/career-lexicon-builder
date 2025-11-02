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

        # Show first 3 for verification
        for doc in documents[:3]:
            print(f"  - {doc.name}")
        if len(documents) > 3:
            print(f"  ... and {len(documents) - 3} more")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
