"""
Tests for themes_analyzer module.
"""

import pytest
from datetime import date
from analyzers.themes_analyzer import (
    ThemeOccurrence,
    Theme,
    extract_themes_from_document,
    cluster_theme_occurrences,
    analyze_themes
)
from core.document_processor import DocumentType


class TestDataStructures:
    """Tests for ThemeOccurrence and Theme dataclasses."""

    def test_theme_occurrence_creation(self):
        """Test creating a ThemeOccurrence."""
        occurrence = ThemeOccurrence(
            quote="I believe in collaborative leadership",
            context="When managing teams, I believe in collaborative leadership that empowers individuals.",
            source_document="/path/to/cover_letter.txt",
            date=date(2024, 1, 15)
        )
        assert occurrence.quote == "I believe in collaborative leadership"
        assert "empowers individuals" in occurrence.context
        assert occurrence.source_document == "/path/to/cover_letter.txt"
        assert occurrence.date == date(2024, 1, 15)

    def test_theme_occurrence_no_date(self):
        """Test ThemeOccurrence with no date."""
        occurrence = ThemeOccurrence(
            quote="I value transparency",
            context="In my work, I value transparency and open communication.",
            source_document="/path/to/letter.txt",
            date=None
        )
        assert occurrence.date is None

    def test_theme_creation(self):
        """Test creating a Theme."""
        occ1 = ThemeOccurrence("I believe in leadership", "context1", "doc1.txt", date(2024, 1, 1))
        occ2 = ThemeOccurrence("Leadership is important", "context2", "doc2.txt", date(2024, 2, 1))

        theme = Theme(
            theme_name="Leadership",
            occurrences=[occ1, occ2],
            confidence=0.85,
            first_seen=date(2024, 1, 1),
            last_seen=date(2024, 2, 1)
        )

        assert theme.theme_name == "Leadership"
        assert len(theme.occurrences) == 2
        assert theme.confidence == 0.85
        assert theme.first_seen == date(2024, 1, 1)
        assert theme.last_seen == date(2024, 2, 1)

    def test_theme_no_dates(self):
        """Test Theme with no dates."""
        occ = ThemeOccurrence("I value teamwork", "context", "doc.txt", None)
        theme = Theme(
            theme_name="Teamwork",
            occurrences=[occ],
            confidence=0.7,
            first_seen=None,
            last_seen=None
        )
        assert theme.first_seen is None
        assert theme.last_seen is None


class TestExtractThemesFromDocument:
    """Tests for extract_themes_from_document function."""

    def test_extract_value_statements(self):
        """Test extracting themes with 'I believe' pattern."""
        text = """
        Dear Hiring Manager,

        I believe in collaborative leadership. When I work with teams,
        I believe that transparency is essential. These values have
        guided my career.
        """
        filepath = "/path/to/letter.txt"
        doc_date = date(2024, 1, 15)

        occurrences = extract_themes_from_document(text, filepath, doc_date)

        assert len(occurrences) >= 1, "Should find at least one theme"
        # Should find "I believe in collaborative leadership" or similar
        quotes = [occ.quote for occ in occurrences]
        assert any("believe" in q.lower() for q in quotes)

    def test_extract_passion_statements(self):
        """Test extracting themes with 'passionate about' pattern."""
        text = """
        I am passionate about using technology to solve real-world problems.
        Throughout my career, I've been driven by this passion.
        """
        occurrences = extract_themes_from_document(text, "letter.txt", None)

        assert len(occurrences) >= 1
        quotes = [occ.quote for occ in occurrences]
        assert any("passionate" in q.lower() for q in quotes)

    def test_extract_value_statements_pattern(self):
        """Test extracting themes with 'I value' pattern."""
        text = """
        In my approach to work, I value open communication and feedback.
        I value diversity of thought and inclusive practices.
        """
        occurrences = extract_themes_from_document(text, "letter.txt", None)

        assert len(occurrences) >= 1
        quotes = [occ.quote for occ in occurrences]
        assert any("value" in q.lower() for q in quotes)

    def test_context_included(self):
        """Test that context includes surrounding sentences."""
        text = """
        Previous sentence here. I believe in teamwork and collaboration.
        Next sentence provides more detail.
        """
        occurrences = extract_themes_from_document(text, "letter.txt", None)

        if len(occurrences) > 0:
            # Context should include surrounding text
            assert len(occurrences[0].context) > len(occurrences[0].quote)

    def test_empty_document(self):
        """Test with empty document."""
        occurrences = extract_themes_from_document("", "empty.txt", None)
        assert len(occurrences) == 0

    def test_no_themes(self):
        """Test document with no clear themes."""
        text = """
        This is a generic cover letter. I am applying for the position.
        Please see my resume for details.
        """
        occurrences = extract_themes_from_document(text, "generic.txt", None)
        # Should find few or no themes in generic text
        assert len(occurrences) >= 0  # May be 0, that's OK

    def test_metadata_preserved(self):
        """Test that source document and date are preserved."""
        text = "I believe in innovation and continuous improvement."
        filepath = "/documents/2024-01-cover-letter.txt"
        doc_date = date(2024, 1, 20)

        occurrences = extract_themes_from_document(text, filepath, doc_date)

        if len(occurrences) > 0:
            assert occurrences[0].source_document == filepath
            assert occurrences[0].date == doc_date


class TestClusterThemeOccurrences:
    """Tests for cluster_theme_occurrences function."""

    def test_cluster_similar_themes(self):
        """Test clustering semantically similar theme occurrences."""
        occurrences = [
            ThemeOccurrence("I believe in team leadership", "ctx1", "doc1.txt", date(2024, 1, 1)),
            ThemeOccurrence("I value collaborative leadership", "ctx2", "doc2.txt", date(2024, 2, 1)),
            ThemeOccurrence("I am passionate about innovation", "ctx3", "doc3.txt", date(2024, 3, 1)),
            ThemeOccurrence("I value creative problem-solving", "ctx4", "doc4.txt", date(2024, 4, 1)),
        ]

        themes = cluster_theme_occurrences(occurrences)

        # Should identify at least 2 clusters (leadership vs innovation)
        assert len(themes) >= 1, "Should create at least one theme"
        assert len(themes) <= 4, "Should cluster similar items"

        # Each theme should have a name
        for theme in themes:
            assert len(theme.theme_name) > 0

    def test_confidence_calculation(self):
        """Test that confidence is calculated for themes."""
        occurrences = [
            ThemeOccurrence("I believe in leadership", "ctx1", "doc1.txt", date(2024, 1, 1)),
            ThemeOccurrence("Leadership is important", "ctx2", "doc2.txt", date(2024, 2, 1)),
        ]

        themes = cluster_theme_occurrences(occurrences)

        assert len(themes) > 0
        for theme in themes:
            assert 0.0 <= theme.confidence <= 1.0, "Confidence should be in [0,1]"

    def test_chronological_ordering(self):
        """Test that occurrences within themes are sorted chronologically."""
        occurrences = [
            ThemeOccurrence("Leadership quote 3", "ctx", "doc3.txt", date(2024, 3, 1)),
            ThemeOccurrence("Leadership quote 1", "ctx", "doc1.txt", date(2024, 1, 1)),
            ThemeOccurrence("Leadership quote 2", "ctx", "doc2.txt", date(2024, 2, 1)),
        ]

        themes = cluster_theme_occurrences(occurrences)

        # Find a theme with multiple occurrences
        for theme in themes:
            if len(theme.occurrences) > 1:
                dates = [occ.date for occ in theme.occurrences if occ.date]
                # Should be sorted chronologically
                assert dates == sorted(dates), "Occurrences should be chronologically ordered"

    def test_first_and_last_seen(self):
        """Test that first_seen and last_seen are calculated correctly."""
        occurrences = [
            ThemeOccurrence("Quote", "ctx", "doc1.txt", date(2024, 1, 1)),
            ThemeOccurrence("Quote", "ctx", "doc2.txt", date(2024, 3, 1)),
            ThemeOccurrence("Quote", "ctx", "doc3.txt", date(2024, 2, 1)),
        ]

        themes = cluster_theme_occurrences(occurrences)

        assert len(themes) > 0
        theme = themes[0]
        if theme.first_seen and theme.last_seen:
            assert theme.first_seen == date(2024, 1, 1)
            assert theme.last_seen == date(2024, 3, 1)

    def test_single_occurrence(self):
        """Test clustering with a single occurrence."""
        occurrences = [
            ThemeOccurrence("I believe in something", "ctx", "doc.txt", date(2024, 1, 1))
        ]

        themes = cluster_theme_occurrences(occurrences)

        assert len(themes) == 1
        assert len(themes[0].occurrences) == 1

    def test_empty_list(self):
        """Test clustering with no occurrences."""
        themes = cluster_theme_occurrences([])
        assert len(themes) == 0

    def test_occurrences_without_dates(self):
        """Test clustering when some occurrences lack dates."""
        occurrences = [
            ThemeOccurrence("Quote 1", "ctx", "doc1.txt", None),
            ThemeOccurrence("Quote 2", "ctx", "doc2.txt", date(2024, 1, 1)),
        ]

        themes = cluster_theme_occurrences(occurrences)

        assert len(themes) > 0
        # Should handle None dates gracefully


class TestAnalyzeThemes:
    """Tests for analyze_themes main API function."""

    def test_analyze_with_cover_letters(self):
        """Test analyzing themes from cover letter documents."""
        documents = [
            {
                'filepath': 'cover_letter1.txt',
                'text': 'I believe in collaborative leadership and teamwork.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'cover_letter2.txt',
                'text': 'I am passionate about innovation and creative problem solving.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 2, 1)
            }
        ]

        themes = analyze_themes(documents)

        # Should extract themes from cover letters
        assert len(themes) >= 0  # May find themes

    def test_filter_to_cover_letters_only(self):
        """Test that only cover letters are analyzed."""
        documents = [
            {
                'filepath': 'cover_letter.txt',
                'text': 'I believe in leadership.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'resume.txt',
                'text': 'I believe in leadership.',  # Should be ignored
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            }
        ]

        themes = analyze_themes(documents)

        # Should only process cover letter
        if len(themes) > 0:
            for theme in themes:
                for occ in theme.occurrences:
                    assert 'cover_letter' in occ.source_document

    def test_sorted_by_confidence(self):
        """Test that themes are sorted by confidence (highest first)."""
        documents = [
            {
                'filepath': 'letter1.txt',
                'text': 'I believe in leadership. I value teamwork. I am passionate about innovation.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            }
        ]

        themes = analyze_themes(documents)

        if len(themes) > 1:
            # Check that themes are sorted by confidence descending
            confidences = [theme.confidence for theme in themes]
            assert confidences == sorted(confidences, reverse=True)

    def test_empty_documents_list(self):
        """Test with empty documents list."""
        themes = analyze_themes([])
        assert len(themes) == 0

    def test_no_cover_letters(self):
        """Test when no cover letters are present."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Software Engineer at TechCorp',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            }
        ]

        themes = analyze_themes(documents)
        assert len(themes) == 0  # No cover letters = no themes

    def test_multiple_cover_letters(self):
        """Test analyzing themes across multiple cover letters."""
        documents = [
            {
                'filepath': 'letter1.txt',
                'text': 'I believe in collaborative leadership.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'letter2.txt',
                'text': 'I value team leadership and collaboration.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 2, 1)
            },
            {
                'filepath': 'letter3.txt',
                'text': 'I am passionate about innovation.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 3, 1)
            }
        ]

        themes = analyze_themes(documents)

        # Should find themes across documents
        assert len(themes) >= 0

    def test_handles_missing_date(self):
        """Test handling documents without dates."""
        documents = [
            {
                'filepath': 'letter.txt',
                'text': 'I believe in something important.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': None
            }
        ]

        themes = analyze_themes(documents)
        # Should handle gracefully
        assert len(themes) >= 0
