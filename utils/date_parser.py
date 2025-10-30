"""
Date Parser Utility
Extracts dates from filenames for Career Lexicon Builder.

Supports multiple date formats:
- YYYY-MM-DD (e.g., 2024-03-15)
- YYYY-MM (e.g., 2023-11)
- MonthYYYY (e.g., March2022)
- Month-YYYY (e.g., March-2022)
"""

import re
from datetime import date
from typing import Optional


# Month name to number mapping
MONTH_MAP = {
    'january': 1, 'jan': 1,
    'february': 2, 'feb': 2,
    'march': 3, 'mar': 3,
    'april': 4, 'apr': 4,
    'may': 5,
    'june': 6, 'jun': 6,
    'july': 7, 'jul': 7,
    'august': 8, 'aug': 8,
    'september': 9, 'sept': 9, 'sep': 9,
    'october': 10, 'oct': 10,
    'november': 11, 'nov': 11,
    'december': 12, 'dec': 12
}


def extract_date_from_filename(filename: str) -> Optional[date]:
    """
    Extract date from filename.

    Tries multiple date format patterns in order:
    1. YYYY-MM-DD (2024-03-15)
    2. YYYY-MM (2023-11, assumes day 1)
    3. MonthYYYY or Month-YYYY (March2022, March-2022, assumes day 1)

    Args:
        filename: Filename to parse (can include path)

    Returns:
        date object if found, None otherwise

    Examples:
        >>> extract_date_from_filename("2024-03-15-cover-letter.pages")
        date(2024, 3, 15)
        >>> extract_date_from_filename("2023-11-resume-company.pages")
        date(2023, 11, 1)
        >>> extract_date_from_filename("March2022-letter.pages")
        date(2022, 3, 1)
        >>> extract_date_from_filename("cover-letter.pages")
        None
    """
    if not filename:
        return None

    # Try YYYY-MM-DD format
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        try:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return date(year, month, day)
        except (ValueError, OverflowError):
            pass  # Invalid date, continue trying other patterns

    # Try YYYY-MM format (but not if it's part of YYYY-MM-DD)
    # This pattern ensures there's no -DD following
    match = re.search(r'(\d{4})-(\d{2})(?!-\d{2})', filename)
    if match:
        try:
            year = int(match.group(1))
            month = int(match.group(2))
            return date(year, month, 1)
        except (ValueError, OverflowError):
            pass

    # Try MonthYYYY or Month-YYYY format (case insensitive)
    pattern = r'(' + '|'.join(MONTH_MAP.keys()) + r')[-_]?(\d{4})'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        try:
            month_str = match.group(1).lower()
            year = int(match.group(2))
            month = MONTH_MAP[month_str]
            return date(year, month, 1)
        except (ValueError, KeyError, OverflowError):
            pass

    return None


def format_date_citation(doc_date: Optional[date]) -> str:
    """
    Format date for citation in lexicons.

    Args:
        doc_date: Date to format

    Returns:
        Formatted date string (YYYY-MM-DD) or "Unknown date"

    Examples:
        >>> format_date_citation(date(2024, 3, 15))
        '2024-03-15'
        >>> format_date_citation(None)
        'Unknown date'
    """
    if doc_date:
        return doc_date.isoformat()
    return "Unknown date"


def compare_dates(date1: Optional[date], date2: Optional[date]) -> int:
    """
    Compare two dates for chronological sorting.

    Args:
        date1: First date
        date2: Second date

    Returns:
        -1 if date1 < date2
         0 if date1 == date2
         1 if date1 > date2

    None values are treated as oldest (infinitely in the past)
    For descending sort (most recent first), None will sort last.
    """
    if date1 is None and date2 is None:
        return 0
    if date1 is None:
        return -1  # None is infinitely old, so "less than" any real date
    if date2 is None:
        return 1   # Any real date is "greater than" None

    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    else:
        return 0
