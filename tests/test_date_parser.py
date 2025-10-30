"""
Tests for date parser utility.
"""

import pytest
from datetime import date
from utils.date_parser import (
    extract_date_from_filename,
    format_date_citation,
    compare_dates
)


class TestExtractDateFromFilename:
    """Tests for extract_date_from_filename function."""

    def test_yyyy_mm_dd_format(self):
        """Test YYYY-MM-DD format extraction."""
        result = extract_date_from_filename("2024-03-15-cover-letter.pages")
        assert result == date(2024, 3, 15)

    def test_yyyy_mm_dd_with_path(self):
        """Test YYYY-MM-DD format with full path."""
        result = extract_date_from_filename("/path/to/2024-03-15-resume.pages")
        assert result == date(2024, 3, 15)

    def test_yyyy_mm_format(self):
        """Test YYYY-MM format extraction (assumes day 1)."""
        result = extract_date_from_filename("2023-11-resume-company.pages")
        assert result == date(2023, 11, 1)

    def test_yyyy_mm_no_trailing_digits(self):
        """Test YYYY-MM format doesn't match YYYY-MM-DD."""
        # Should match the full YYYY-MM-DD, not YYYY-MM
        result = extract_date_from_filename("2023-11-05-letter.pages")
        assert result == date(2023, 11, 5)

    def test_month_yyyy_format(self):
        """Test MonthYYYY format extraction."""
        result = extract_date_from_filename("March2022-letter.pages")
        assert result == date(2022, 3, 1)

    def test_month_dash_yyyy_format(self):
        """Test Month-YYYY format extraction."""
        result = extract_date_from_filename("March-2022-letter.pages")
        assert result == date(2022, 3, 1)

    def test_month_underscore_yyyy_format(self):
        """Test Month_YYYY format extraction."""
        result = extract_date_from_filename("March_2022_letter.pages")
        assert result == date(2022, 3, 1)

    def test_month_case_insensitive(self):
        """Test month name is case insensitive."""
        assert extract_date_from_filename("MARCH2022-letter.pages") == date(2022, 3, 1)
        assert extract_date_from_filename("march2022-letter.pages") == date(2022, 3, 1)
        assert extract_date_from_filename("March2022-letter.pages") == date(2022, 3, 1)

    def test_abbreviated_month_names(self):
        """Test abbreviated month names."""
        assert extract_date_from_filename("Jan2024-letter.pages") == date(2024, 1, 1)
        assert extract_date_from_filename("Feb2024-letter.pages") == date(2024, 2, 1)
        assert extract_date_from_filename("Sept2024-letter.pages") == date(2024, 9, 1)
        assert extract_date_from_filename("Dec2024-letter.pages") == date(2024, 12, 1)

    def test_no_date_in_filename(self):
        """Test filename with no date returns None."""
        result = extract_date_from_filename("cover-letter.pages")
        assert result is None

    def test_empty_filename(self):
        """Test empty filename returns None."""
        result = extract_date_from_filename("")
        assert result is None

    def test_none_filename(self):
        """Test None filename returns None."""
        result = extract_date_from_filename(None)
        assert result is None

    def test_invalid_date_values(self):
        """Test invalid date values return None."""
        # Invalid month
        result = extract_date_from_filename("2024-13-15-letter.pages")
        assert result is None

        # Invalid day
        result = extract_date_from_filename("2024-02-30-letter.pages")
        assert result is None

    def test_year_out_of_range(self):
        """Test year out of valid range returns None."""
        result = extract_date_from_filename("10000-01-01-letter.pages")
        assert result is None

    def test_priority_yyyy_mm_dd_over_yyyy_mm(self):
        """Test that YYYY-MM-DD is matched before YYYY-MM."""
        # If filename has YYYY-MM-DD, should extract full date
        result = extract_date_from_filename("2024-03-15-cover-letter.pages")
        assert result == date(2024, 3, 15)
        assert result != date(2024, 3, 1)

    def test_various_separators(self):
        """Test different separators and formats."""
        assert extract_date_from_filename("2024_03_15_letter.pages") is None  # Not supported
        assert extract_date_from_filename("2024.03.15.letter.pages") is None  # Not supported
        assert extract_date_from_filename("2024-03-15-letter.pages") == date(2024, 3, 15)


class TestFormatDateCitation:
    """Tests for format_date_citation function."""

    def test_format_valid_date(self):
        """Test formatting a valid date."""
        result = format_date_citation(date(2024, 3, 15))
        assert result == "2024-03-15"

    def test_format_none_date(self):
        """Test formatting None returns 'Unknown date'."""
        result = format_date_citation(None)
        assert result == "Unknown date"


class TestCompareDates:
    """Tests for compare_dates function."""

    def test_compare_equal_dates(self):
        """Test comparing equal dates."""
        d1 = date(2024, 3, 15)
        d2 = date(2024, 3, 15)
        assert compare_dates(d1, d2) == 0

    def test_compare_date1_earlier(self):
        """Test date1 < date2."""
        d1 = date(2024, 3, 14)
        d2 = date(2024, 3, 15)
        assert compare_dates(d1, d2) == -1

    def test_compare_date1_later(self):
        """Test date1 > date2."""
        d1 = date(2024, 3, 16)
        d2 = date(2024, 3, 15)
        assert compare_dates(d1, d2) == 1

    def test_compare_both_none(self):
        """Test comparing two None dates."""
        assert compare_dates(None, None) == 0

    def test_compare_date1_none(self):
        """Test date1 None (treated as infinitely old)."""
        d2 = date(2024, 3, 15)
        assert compare_dates(None, d2) == -1

    def test_compare_date2_none(self):
        """Test date2 None (treated as infinitely old)."""
        d1 = date(2024, 3, 15)
        assert compare_dates(d1, None) == 1

    def test_compare_for_sorting(self):
        """Test compare function works for sorting (descending)."""
        dates = [
            date(2022, 1, 1),
            date(2024, 6, 15),
            None,
            date(2023, 11, 3),
            date(2024, 1, 1)
        ]

        # Sort in descending order (most recent first)
        # Negate the comparison to reverse order
        from functools import cmp_to_key
        sorted_dates = sorted(dates, key=cmp_to_key(lambda x, y: compare_dates(y, x)))

        expected = [
            date(2024, 6, 15),
            date(2024, 1, 1),
            date(2023, 11, 3),
            date(2022, 1, 1),
            None
        ]
        assert sorted_dates == expected
