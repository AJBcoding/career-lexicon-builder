"""
Formatting utilities for lexicon generators.

Provides helper functions for formatting dates, confidence scores, citations,
and creating markdown files.
"""

from datetime import date
from pathlib import Path
from typing import Optional


def format_date(d: Optional[date]) -> str:
    """
    Format date as YYYY-MM-DD or 'Unknown'.

    Args:
        d: Date to format, or None

    Returns:
        Formatted date string or 'Unknown' if None

    Examples:
        >>> from datetime import date
        >>> format_date(date(2024, 1, 15))
        '2024-01-15'
        >>> format_date(None)
        'Unknown'
    """
    return d.strftime('%Y-%m-%d') if d else 'Unknown'


def format_confidence(conf: float) -> str:
    """
    Format confidence as percentage.

    Args:
        conf: Confidence score between 0.0 and 1.0

    Returns:
        Formatted percentage string

    Examples:
        >>> format_confidence(0.85)
        '85%'
        >>> format_confidence(0.9)
        '90%'
    """
    return f"{conf*100:.0f}%"


def format_citation(source: str, doc_date: Optional[date] = None) -> str:
    """
    Format source citation.

    Args:
        source: Source document filename
        doc_date: Optional document date

    Returns:
        Formatted citation string

    Examples:
        >>> from datetime import date
        >>> format_citation("resume.txt", date(2024, 1, 15))
        'resume.txt (2024-01-15)'
        >>> format_citation("cover_letter.txt")
        'cover_letter.txt'
    """
    if doc_date:
        return f"{source} ({format_date(doc_date)})"
    return source


def create_markdown_file(path: str, content: str) -> None:
    """
    Create markdown file, creating directories if needed.

    Args:
        path: Path to the markdown file to create
        content: Markdown content to write

    Examples:
        >>> create_markdown_file("output/test.md", "# Test\\n")
        # Creates output directory if it doesn't exist and writes file
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
