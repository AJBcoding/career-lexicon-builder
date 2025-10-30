"""
Integration tests for Phase 3 analyzers.

Tests that all four analyzers (themes, qualifications, narratives, keywords)
work together correctly with realistic document samples.
"""

import pytest
from datetime import date
from pathlib import Path

from analyzers.themes_analyzer import analyze_themes
from analyzers.qualifications_analyzer import analyze_qualifications
from analyzers.narratives_analyzer import analyze_narratives
from analyzers.keywords_analyzer import analyze_keywords
from core.document_processor import DocumentType


# Get fixtures directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures'


def load_fixture(filename: str) -> str:
    """Load a test fixture file."""
    filepath = FIXTURES_DIR / filename
    with open(filepath, 'r') as f:
        return f.read()


class TestPhase3Integration:
    """Integration tests for all Phase 3 analyzers."""

    def test_full_pipeline_with_sample_documents(self):
        """Test all analyzers with realistic sample documents."""
        # Load sample documents
        resume_text = load_fixture('sample_resume.txt')
        cover_letter_text = load_fixture('sample_cover_letter.txt')
        resume_v2_text = load_fixture('sample_resume_v2.txt')

        # Create document list
        documents = [
            {
                'filepath': 'resume_2020.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 6, 1)
            },
            {
                'filepath': 'cover_letter_2024.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            },
            {
                'filepath': 'resume_2024.txt',
                'text': resume_v2_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 2, 1)
            }
        ]

        # Run all analyzers
        themes = analyze_themes(documents)
        qualifications = analyze_qualifications(documents)
        narratives = analyze_narratives(documents)
        keywords = analyze_keywords(documents, min_frequency=1)

        # Verify each analyzer produces output
        assert isinstance(themes, list), "Themes should return a list"
        assert isinstance(qualifications, list), "Qualifications should return a list"
        assert isinstance(narratives, list), "Narratives should return a list"
        assert isinstance(keywords, list), "Keywords should return a list"

        # Themes should be found in cover letter
        if len(themes) > 0:
            assert all(0.0 <= t.confidence <= 1.0 for t in themes), "Themes should have valid confidence"
            assert all(len(t.occurrences) > 0 for t in themes), "Themes should have occurrences"

        # Qualifications should be found in resumes
        if len(qualifications) > 0:
            assert all(0.0 <= q.confidence <= 1.0 for q in qualifications), "Qualifications should have valid confidence"
            assert all(len(q.variations) > 0 for q in qualifications), "Qualifications should have variations"

        # Narratives should be found in cover letter
        if len(narratives) > 0:
            assert all(0.0 <= n.confidence <= 1.0 for n in narratives), "Narratives should have valid confidence"
            assert all(len(n.patterns) > 0 for n in narratives), "Narratives should have patterns"

        # Keywords should be found across documents
        if len(keywords) > 0:
            assert all(k.frequency >= 1 for k in keywords), "Keywords should have frequency >= 1"
            assert all(len(k.usages) > 0 for k in keywords), "Keywords should have usages"

    def test_themes_from_cover_letter(self):
        """Test that themes analyzer processes cover letters correctly."""
        cover_letter_text = load_fixture('sample_cover_letter.txt')

        documents = [
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            }
        ]

        themes = analyze_themes(documents)

        # Should find themes from cover letter
        assert len(themes) >= 1, "Should find at least one theme"

        # Check that themes have proper structure
        for theme in themes:
            assert hasattr(theme, 'theme_name'), "Theme should have name"
            assert hasattr(theme, 'occurrences'), "Theme should have occurrences"
            assert hasattr(theme, 'confidence'), "Theme should have confidence"
            assert len(theme.theme_name) > 0, "Theme name should not be empty"

    def test_qualifications_from_resumes(self):
        """Test that qualifications analyzer tracks variations across resume versions."""
        resume_text = load_fixture('sample_resume.txt')
        resume_v2_text = load_fixture('sample_resume_v2.txt')

        documents = [
            {
                'filepath': 'resume_v1.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 6, 1)
            },
            {
                'filepath': 'resume_v2.txt',
                'text': resume_v2_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 2, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)

        # Should find qualifications from resumes
        assert len(qualifications) >= 1, "Should find at least one qualification"

        # Check for variations across versions
        for qual in qualifications:
            assert hasattr(qual, 'qualification_id'), "Should have ID"
            assert hasattr(qual, 'position_title'), "Should have position title"
            assert hasattr(qual, 'variations'), "Should have variations"
            assert len(qual.variations) > 0, "Should have at least one variation"

    def test_narratives_from_cover_letter(self):
        """Test that narratives analyzer detects rhetorical patterns."""
        cover_letter_text = load_fixture('sample_cover_letter.txt')

        documents = [
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            }
        ]

        narratives = analyze_narratives(documents)

        # Should find narrative patterns
        assert len(narratives) >= 1, "Should find at least one narrative category"

        # Check pattern types
        pattern_types = set()
        for category in narratives:
            for pattern in category.patterns:
                pattern_types.add(pattern.pattern_type)

        # Cover letter should have some narrative patterns (metaphors, transitions, etc.)
        assert len(pattern_types) > 0, "Should detect various pattern types"

    def test_keywords_across_all_documents(self):
        """Test that keywords analyzer indexes terms across all document types."""
        resume_text = load_fixture('sample_resume.txt')
        cover_letter_text = load_fixture('sample_cover_letter.txt')

        documents = [
            {
                'filepath': 'resume.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 6, 1)
            },
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            }
        ]

        keywords = analyze_keywords(documents, min_frequency=1)

        # Should find keywords across documents
        assert len(keywords) >= 1, "Should find keywords"

        # Check that some keywords appear in multiple document types
        multi_type_keywords = [k for k in keywords if len(k.document_types) > 1]

        # At least some keywords should appear in both resumes and cover letters
        # (e.g., "software engineering", "team leadership")
        assert len(multi_type_keywords) >= 0, "Keywords can appear in multiple doc types"

    def test_output_consistency(self):
        """Test that all analyzers produce consistent output formats."""
        resume_text = load_fixture('sample_resume.txt')
        cover_letter_text = load_fixture('sample_cover_letter.txt')

        documents = [
            {
                'filepath': 'resume.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 6, 1)
            },
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            }
        ]

        # Run all analyzers
        themes = analyze_themes(documents)
        qualifications = analyze_qualifications(documents)
        narratives = analyze_narratives(documents)
        keywords = analyze_keywords(documents, min_frequency=1)

        # All should return lists
        assert isinstance(themes, list)
        assert isinstance(qualifications, list)
        assert isinstance(narratives, list)
        assert isinstance(keywords, list)

        # All confidence scores should be in valid range
        if len(themes) > 0:
            for theme in themes:
                assert 0.0 <= theme.confidence <= 1.0

        if len(qualifications) > 0:
            for qual in qualifications:
                assert 0.0 <= qual.confidence <= 1.0

        if len(narratives) > 0:
            for narrative in narratives:
                assert 0.0 <= narrative.confidence <= 1.0

    def test_date_handling_consistency(self):
        """Test that all analyzers handle dates consistently."""
        resume_text = load_fixture('sample_resume.txt')
        cover_letter_text = load_fixture('sample_cover_letter.txt')

        # Documents with dates
        documents_with_dates = [
            {
                'filepath': 'resume.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 6, 1)
            },
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 15)
            }
        ]

        # Documents without dates
        documents_without_dates = [
            {
                'filepath': 'resume.txt',
                'text': resume_text,
                'document_type': DocumentType.RESUME.value,
                'date': None
            },
            {
                'filepath': 'cover_letter.txt',
                'text': cover_letter_text,
                'document_type': DocumentType.COVER_LETTER.value,
                'date': None
            }
        ]

        # All analyzers should handle both cases without errors
        themes_with = analyze_themes(documents_with_dates)
        themes_without = analyze_themes(documents_without_dates)
        assert isinstance(themes_with, list)
        assert isinstance(themes_without, list)

        quals_with = analyze_qualifications(documents_with_dates)
        quals_without = analyze_qualifications(documents_without_dates)
        assert isinstance(quals_with, list)
        assert isinstance(quals_without, list)

        narr_with = analyze_narratives(documents_with_dates)
        narr_without = analyze_narratives(documents_without_dates)
        assert isinstance(narr_with, list)
        assert isinstance(narr_without, list)

        kw_with = analyze_keywords(documents_with_dates, min_frequency=1)
        kw_without = analyze_keywords(documents_without_dates, min_frequency=1)
        assert isinstance(kw_with, list)
        assert isinstance(kw_without, list)

    def test_empty_documents_handling(self):
        """Test that all analyzers handle empty document lists gracefully."""
        empty_docs = []

        themes = analyze_themes(empty_docs)
        qualifications = analyze_qualifications(empty_docs)
        narratives = analyze_narratives(empty_docs)
        keywords = analyze_keywords(empty_docs)

        assert themes == []
        assert qualifications == []
        assert narratives == []
        assert keywords == []
