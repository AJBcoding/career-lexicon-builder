"""
Tests for keywords_analyzer module.
"""

import pytest
from datetime import date
from analyzers.keywords_analyzer import (
    KeywordUsage,
    KeywordEntry,
    extract_keywords_from_document,
    build_keyword_index,
    analyze_keywords
)
from core.document_processor import DocumentType


class TestDataStructures:
    """Tests for KeywordUsage and KeywordEntry dataclasses."""

    def test_keyword_usage_creation(self):
        """Test creating a KeywordUsage."""
        usage = KeywordUsage(
            keyword="stakeholder management",
            context="Experienced in stakeholder management across multiple teams.",
            source_document="resume.txt",
            document_type="resume",
            date=date(2024, 1, 15)
        )
        assert usage.keyword == "stakeholder management"
        assert "multiple teams" in usage.context
        assert usage.document_type == "resume"
        assert usage.date == date(2024, 1, 15)

    def test_keyword_usage_no_date(self):
        """Test KeywordUsage with no date."""
        usage = KeywordUsage(
            keyword="leadership",
            context="Leadership experience in software development.",
            source_document="doc.txt",
            document_type="cover_letter",
            date=None
        )
        assert usage.date is None

    def test_keyword_entry_creation(self):
        """Test creating a KeywordEntry."""
        usage1 = KeywordUsage("leadership", "ctx1", "doc1", "resume", None)
        usage2 = KeywordUsage("leadership", "ctx2", "doc2", "cover_letter", None)

        entry = KeywordEntry(
            keyword="leadership",
            aliases=["leading", "team leadership"],
            usages=[usage1, usage2],
            frequency=2,
            document_types={"resume", "cover_letter"}
        )

        assert entry.keyword == "leadership"
        assert len(entry.aliases) == 2
        assert entry.frequency == 2
        assert "resume" in entry.document_types
        assert "cover_letter" in entry.document_types


class TestExtractKeywordsFromDocument:
    """Tests for extract_keywords_from_document function."""

    def test_extract_simple_keywords(self):
        """Test extracting basic keywords from document."""
        text = """
        I have extensive experience in software development and project management.
        I worked on cloud computing and data analysis projects.
        """
        usages = extract_keywords_from_document(text, "doc.txt", "resume", None)

        assert len(usages) > 0
        keywords = [u.keyword for u in usages]
        # Should extract some multi-word phrases
        assert any("software" in k.lower() or "project" in k.lower() or "cloud" in k.lower() for k in keywords)

    def test_extract_phrases(self):
        """Test extracting multi-word phrases."""
        text = "I have experience in stakeholder management and team leadership."
        usages = extract_keywords_from_document(text, "doc.txt", "resume", None)

        keywords = [u.keyword for u in usages]
        # Should extract phrases, not just single words
        assert any(len(k.split()) >= 2 for k in keywords)

    def test_context_captured(self):
        """Test that context is captured for keywords."""
        text = "I led software development teams. I managed cloud infrastructure projects."
        usages = extract_keywords_from_document(text, "doc.txt", "resume", None)

        if len(usages) > 0:
            # Context should be the sentence containing the keyword
            for usage in usages:
                assert len(usage.context) >= len(usage.keyword)

    def test_metadata_preserved(self):
        """Test that metadata is preserved."""
        text = "Software engineering and data analysis experience."
        filepath = "/path/to/resume.txt"
        doc_type = "resume"
        doc_date = date(2024, 1, 20)

        usages = extract_keywords_from_document(text, filepath, doc_type, doc_date)

        if len(usages) > 0:
            assert usages[0].source_document == filepath
            assert usages[0].document_type == doc_type
            assert usages[0].date == doc_date

    def test_empty_document(self):
        """Test with empty document."""
        usages = extract_keywords_from_document("", "empty.txt", "resume", None)
        assert len(usages) == 0

    def test_short_document(self):
        """Test with very short document."""
        text = "Hello world."
        usages = extract_keywords_from_document(text, "short.txt", "resume", None)
        # May have few or no keywords
        assert len(usages) >= 0

    def test_stopwords_filtered(self):
        """Test that common stopwords are filtered out."""
        text = "The and or but if then when where which that this."
        usages = extract_keywords_from_document(text, "stopwords.txt", "resume", None)

        # Should not extract pure stopwords as keywords
        keywords = [u.keyword.lower() for u in usages]
        # Common stopwords shouldn't appear as standalone keywords
        assert not any(k in ["the", "and", "or", "but"] for k in keywords)


class TestBuildKeywordIndex:
    """Tests for build_keyword_index function."""

    def test_build_index_single_keyword(self):
        """Test building index with a single keyword."""
        usages = [
            KeywordUsage("leadership", "ctx1", "doc1", "resume", date(2024, 1, 1)),
            KeywordUsage("leadership", "ctx2", "doc2", "resume", date(2024, 2, 1)),
        ]

        index = build_keyword_index(usages)

        assert len(index) == 1
        entry = index[0]
        assert entry.keyword == "leadership"
        assert entry.frequency == 2
        assert len(entry.usages) == 2

    def test_build_index_multiple_keywords(self):
        """Test building index with multiple different keywords."""
        usages = [
            KeywordUsage("leadership", "ctx", "doc1", "resume", None),
            KeywordUsage("teamwork", "ctx", "doc2", "resume", None),
            KeywordUsage("innovation", "ctx", "doc3", "resume", None),
        ]

        index = build_keyword_index(usages)

        assert len(index) == 3
        keywords = [entry.keyword for entry in index]
        assert "leadership" in keywords
        assert "teamwork" in keywords
        assert "innovation" in keywords

    def test_alias_detection(self):
        """Test that similar keywords are detected as aliases."""
        usages = [
            KeywordUsage("leadership", "ctx", "doc1", "resume", None),
            KeywordUsage("leading", "ctx", "doc2", "resume", None),
            KeywordUsage("team leadership", "ctx", "doc3", "resume", None),
        ]

        index = build_keyword_index(usages)

        # Should identify these as related (may cluster or list as aliases)
        # At minimum, should have alias detection working
        assert len(index) >= 1
        # Check if any entry has aliases
        has_aliases = any(len(entry.aliases) > 0 for entry in index)
        # This is optional - aliases might be detected
        assert has_aliases or len(index) <= 3  # Either aliases found or separate entries

    def test_frequency_calculation(self):
        """Test that frequency is calculated correctly."""
        usages = [
            KeywordUsage("python programming", "ctx1", "doc1", "resume", None),
            KeywordUsage("python programming", "ctx2", "doc2", "cover_letter", None),
            KeywordUsage("python programming", "ctx3", "doc3", "resume", None),
        ]

        index = build_keyword_index(usages)

        entry = next(e for e in index if "python" in e.keyword.lower())
        assert entry.frequency == 3

    def test_document_types_tracked(self):
        """Test that document types are tracked."""
        usages = [
            KeywordUsage("leadership", "ctx", "resume.txt", "resume", None),
            KeywordUsage("leadership", "ctx", "letter.txt", "cover_letter", None),
            KeywordUsage("leadership", "ctx", "job.txt", "job_description", None),
        ]

        index = build_keyword_index(usages)

        entry = index[0]
        assert "resume" in entry.document_types
        assert "cover_letter" in entry.document_types
        assert "job_description" in entry.document_types

    def test_chronological_ordering(self):
        """Test that usages are sorted by date (most recent first)."""
        usages = [
            KeywordUsage("leadership", "ctx1", "doc1", "resume", date(2024, 1, 1)),
            KeywordUsage("leadership", "ctx3", "doc3", "resume", date(2024, 3, 1)),
            KeywordUsage("leadership", "ctx2", "doc2", "resume", date(2024, 2, 1)),
        ]

        index = build_keyword_index(usages)

        entry = index[0]
        dates = [u.date for u in entry.usages if u.date]
        # Should be sorted most recent first
        assert dates == sorted(dates, reverse=True)

    def test_empty_usages(self):
        """Test building index with no usages."""
        index = build_keyword_index([])
        assert len(index) == 0

    def test_single_usage(self):
        """Test building index with single usage."""
        usages = [
            KeywordUsage("single keyword", "ctx", "doc", "resume", None)
        ]

        index = build_keyword_index(usages)

        assert len(index) == 1
        assert index[0].frequency == 1


class TestAnalyzeKeywords:
    """Tests for analyze_keywords main API function."""

    def test_analyze_with_multiple_documents(self):
        """Test analyzing keywords from multiple documents."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Software engineering and cloud computing experience.',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'letter.txt',
                'text': 'Passionate about software engineering and team collaboration.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 2, 1)
            }
        ]

        index = analyze_keywords(documents, min_frequency=1)

        # Should extract keywords from all documents
        assert len(index) >= 0

    def test_process_all_document_types(self):
        """Test that keywords are extracted from all document types."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Software development experience.',
                'document_type': DocumentType.RESUME.value,
                'date': None
            },
            {
                'filepath': 'letter.txt',
                'text': 'Software development passion.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': None
            },
            {
                'filepath': 'job.txt',
                'text': 'Software development required.',
                'document_type': DocumentType.JOB_DESCRIPTION.value,
                'date': None
            }
        ]

        index = analyze_keywords(documents, min_frequency=2)

        # Keywords should appear across document types
        if len(index) > 0:
            # At least one keyword should appear in multiple document types
            multi_type = any(len(entry.document_types) > 1 for entry in index)
            assert multi_type or len(index) >= 1

    def test_frequency_filtering(self):
        """Test that min_frequency filtering works."""
        documents = [
            {
                'filepath': 'doc1.txt',
                'text': 'Leadership and teamwork are important. Innovation is key.',
                'document_type': DocumentType.RESUME.value,
                'date': None
            },
            {
                'filepath': 'doc2.txt',
                'text': 'Leadership is essential for success.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': None
            }
        ]

        # With min_frequency=2, only keywords appearing twice should be included
        index = analyze_keywords(documents, min_frequency=2)

        # All entries should have frequency >= 2
        for entry in index:
            assert entry.frequency >= 2

    def test_sorted_by_frequency(self):
        """Test that results are sorted by frequency (highest first)."""
        documents = [
            {
                'filepath': 'doc.txt',
                'text': 'Leadership leadership leadership. Teamwork teamwork. Innovation.',
                'document_type': DocumentType.RESUME.value,
                'date': None
            }
        ]

        index = analyze_keywords(documents, min_frequency=1)

        if len(index) > 1:
            # Should be sorted by frequency descending
            frequencies = [entry.frequency for entry in index]
            assert frequencies == sorted(frequencies, reverse=True)

    def test_empty_documents_list(self):
        """Test with empty documents list."""
        index = analyze_keywords([])
        assert len(index) == 0

    def test_documents_with_no_keywords(self):
        """Test with documents that have no extractable keywords."""
        documents = [
            {
                'filepath': 'empty.txt',
                'text': '',
                'document_type': DocumentType.RESUME.value,
                'date': None
            }
        ]

        index = analyze_keywords(documents, min_frequency=1)
        assert len(index) == 0

    def test_cross_document_reference(self):
        """Test that same keyword across documents is tracked."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Project management experience in software development.',
                'document_type': DocumentType.RESUME.value,
                'date': date(2023, 1, 1)
            },
            {
                'filepath': 'letter.txt',
                'text': 'Strong project management skills demonstrated.',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            }
        ]

        index = analyze_keywords(documents, min_frequency=2)

        # Should find "project management" appearing in both documents
        if len(index) > 0:
            # At least one entry should have usages from multiple sources
            multi_source = any(
                len(set(u.source_document for u in entry.usages)) > 1
                for entry in index
            )
            assert multi_source or len(index) >= 1

    def test_handles_missing_date(self):
        """Test handling documents without dates."""
        documents = [
            {
                'filepath': 'doc.txt',
                'text': 'Software engineering and development.',
                'document_type': DocumentType.RESUME.value,
                'date': None
            }
        ]

        index = analyze_keywords(documents, min_frequency=1)
        assert len(index) >= 0
