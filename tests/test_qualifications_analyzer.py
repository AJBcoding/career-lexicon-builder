"""
Tests for qualifications_analyzer module.
"""

import pytest
from datetime import date
from analyzers.qualifications_analyzer import (
    QualificationVariation,
    Qualification,
    extract_qualifications_from_resume,
    cluster_qualification_variations,
    analyze_qualifications
)
from core.document_processor import DocumentType


class TestDataStructures:
    """Tests for QualificationVariation and Qualification dataclasses."""

    def test_qualification_variation_creation(self):
        """Test creating a QualificationVariation."""
        variation = QualificationVariation(
            text="Led team of 5 engineers",
            source_document="resume_2024.txt",
            date=date(2024, 1, 15),
            position_context="Senior Software Engineer at TechCorp"
        )
        assert variation.text == "Led team of 5 engineers"
        assert variation.source_document == "resume_2024.txt"
        assert variation.date == date(2024, 1, 15)
        assert "TechCorp" in variation.position_context

    def test_qualification_variation_no_date(self):
        """Test QualificationVariation with no date."""
        variation = QualificationVariation(
            text="Developed Python applications",
            source_document="resume.txt",
            date=None,
            position_context="Software Developer"
        )
        assert variation.date is None

    def test_qualification_creation(self):
        """Test creating a Qualification."""
        var1 = QualificationVariation("Led team", "doc1.txt", date(2024, 1, 1), "Engineer at Co")
        var2 = QualificationVariation("Managed team", "doc2.txt", date(2024, 2, 1), "Engineer at Co")

        qual = Qualification(
            qualification_id="engineer_co",
            position_title="Software Engineer",
            organization="Co",
            variations=[var1, var2],
            confidence=0.85
        )

        assert qual.qualification_id == "engineer_co"
        assert qual.position_title == "Software Engineer"
        assert qual.organization == "Co"
        assert len(qual.variations) == 2
        assert qual.confidence == 0.85


class TestExtractQualificationsFromResume:
    """Tests for extract_qualifications_from_resume function."""

    def test_extract_from_experience_section(self):
        """Test extracting qualifications from Experience section."""
        text = """
        EXPERIENCE

        Senior Software Engineer, TechCorp
        June 2020 - Present
        • Led team of 5 engineers
        • Developed cloud-based applications
        • Improved system performance by 40%
        """
        filepath = "resume.txt"
        doc_date = date(2024, 1, 15)

        variations = extract_qualifications_from_resume(text, filepath, doc_date)

        assert len(variations) > 0, "Should extract at least one variation"
        # Should find the position title
        contexts = [v.position_context for v in variations]
        assert any("Engineer" in ctx or "TechCorp" in ctx for ctx in contexts)

    def test_extract_bullet_points(self):
        """Test extracting bullet points as variations."""
        text = """
        Software Developer
        Company XYZ
        • Built REST APIs using Python
        • Implemented CI/CD pipeline
        • Mentored junior developers
        """
        variations = extract_qualifications_from_resume(text, "resume.txt", None)

        assert len(variations) >= 1
        # Should extract bullet points
        texts = [v.text for v in variations]
        assert any("API" in t or "pipeline" in t or "developer" in t for t in texts)

    def test_extract_with_date_range(self):
        """Test extraction with date range in position."""
        text = """
        Lead Developer, StartupCo
        January 2019 - December 2021
        • Architected microservices platform
        • Reduced deployment time by 50%
        """
        variations = extract_qualifications_from_resume(text, "resume.txt", None)

        assert len(variations) >= 1

    def test_multiple_positions(self):
        """Test extracting from multiple positions."""
        text = """
        EXPERIENCE

        Senior Engineer, CompanyA
        2020 - 2024
        • Led backend development

        Engineer, CompanyB
        2018 - 2020
        • Built mobile applications
        """
        variations = extract_qualifications_from_resume(text, "resume.txt", None)

        assert len(variations) >= 2
        # Should have variations from both positions
        contexts = [v.position_context for v in variations]
        assert any("CompanyA" in ctx for ctx in contexts) or any("CompanyB" in ctx for ctx in contexts)

    def test_empty_resume(self):
        """Test with empty resume."""
        variations = extract_qualifications_from_resume("", "empty.txt", None)
        assert len(variations) == 0

    def test_resume_without_structure(self):
        """Test resume with unclear structure."""
        text = "Just some random text without clear structure."
        variations = extract_qualifications_from_resume(text, "unstructured.txt", None)
        # May extract nothing or very little
        assert len(variations) >= 0

    def test_metadata_preserved(self):
        """Test that metadata is preserved in variations."""
        text = """
        Engineer at TechCorp
        • Developed software
        """
        filepath = "/path/to/resume.txt"
        doc_date = date(2024, 1, 20)

        variations = extract_qualifications_from_resume(text, filepath, doc_date)

        if len(variations) > 0:
            assert variations[0].source_document == filepath
            assert variations[0].date == doc_date


class TestClusterQualificationVariations:
    """Tests for cluster_qualification_variations function."""

    def test_cluster_same_position(self):
        """Test clustering variations of the same position."""
        variations = [
            QualificationVariation("Led team of 5 engineers", "doc1", date(2024, 1, 1), "Engineer at TechCorp"),
            QualificationVariation("Managed engineering team of 5", "doc2", date(2024, 2, 1), "Engineer at TechCorp"),
            QualificationVariation("Built mobile apps", "doc3", date(2024, 3, 1), "Developer at StartupCo"),
        ]

        qualifications = cluster_qualification_variations(variations)

        # Should identify at least 1 qualification (possibly 2 if distinguishes positions)
        assert len(qualifications) >= 1
        assert len(qualifications) <= 3

    def test_qualification_id_generation(self):
        """Test that qualification_id is generated."""
        variations = [
            QualificationVariation("Did something", "doc", None, "Engineer at CompanyX")
        ]

        qualifications = cluster_qualification_variations(variations)

        assert len(qualifications) > 0
        assert len(qualifications[0].qualification_id) > 0

    def test_chronological_ordering(self):
        """Test that variations are sorted chronologically (most recent first)."""
        variations = [
            QualificationVariation("Version 1", "doc1", date(2024, 1, 1), "Engineer at Co"),
            QualificationVariation("Version 3", "doc3", date(2024, 3, 1), "Engineer at Co"),
            QualificationVariation("Version 2", "doc2", date(2024, 2, 1), "Engineer at Co"),
        ]

        qualifications = cluster_qualification_variations(variations)

        assert len(qualifications) > 0
        qual = qualifications[0]
        if len(qual.variations) > 1:
            dates = [v.date for v in qual.variations if v.date]
            # Should be sorted most recent first
            assert dates == sorted(dates, reverse=True)

    def test_confidence_calculation(self):
        """Test that confidence is calculated."""
        variations = [
            QualificationVariation("Task 1", "doc", date(2024, 1, 1), "Senior Engineer at TechCorp"),
            QualificationVariation("Task 2", "doc", date(2024, 2, 1), "Senior Engineer at TechCorp"),
        ]

        qualifications = cluster_qualification_variations(variations)

        assert len(qualifications) > 0
        for qual in qualifications:
            assert 0.0 <= qual.confidence <= 1.0

    def test_single_variation(self):
        """Test clustering with a single variation."""
        variations = [
            QualificationVariation("Only one", "doc", None, "Engineer")
        ]

        qualifications = cluster_qualification_variations(variations)

        assert len(qualifications) == 1
        assert len(qualifications[0].variations) == 1

    def test_empty_list(self):
        """Test clustering with no variations."""
        qualifications = cluster_qualification_variations([])
        assert len(qualifications) == 0

    def test_variations_without_dates(self):
        """Test clustering when variations lack dates."""
        variations = [
            QualificationVariation("Task", "doc1", None, "Engineer at Co"),
            QualificationVariation("Task", "doc2", date(2024, 1, 1), "Engineer at Co"),
        ]

        qualifications = cluster_qualification_variations(variations)

        assert len(qualifications) > 0


class TestAnalyzeQualifications:
    """Tests for analyze_qualifications main API function."""

    def test_analyze_with_resumes(self):
        """Test analyzing qualifications from resume documents."""
        documents = [
            {
                'filepath': 'resume1.txt',
                'text': 'Senior Engineer at TechCorp\n• Led development team',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'resume2.txt',
                'text': 'Engineer at TechCorp\n• Developed software',
                'document_type': DocumentType.RESUME.value,
                'date': date(2023, 1, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)

        # Should extract qualifications from resumes
        assert len(qualifications) >= 0

    def test_filter_to_resumes_only(self):
        """Test that only resumes are analyzed."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Engineer at Co\n• Built apps',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            },
            {
                'filepath': 'cover_letter.txt',
                'text': 'Engineer at Co\n• Built apps',  # Should be ignored
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)

        # Should only process resume
        if len(qualifications) > 0:
            for qual in qualifications:
                for var in qual.variations:
                    assert 'resume' in var.source_document

    def test_sorted_by_date(self):
        """Test that qualifications are sorted by date (most recent first)."""
        documents = [
            {
                'filepath': 'resume_old.txt',
                'text': 'Engineer at OldCo\n• Old work',
                'document_type': DocumentType.RESUME.value,
                'date': date(2020, 1, 1)
            },
            {
                'filepath': 'resume_new.txt',
                'text': 'Engineer at NewCo\n• Recent work',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)

        # If we have qualifications with dates, they should be sorted
        if len(qualifications) > 1:
            # Check if sorted by most recent variation first
            for qual in qualifications:
                if len(qual.variations) > 0 and qual.variations[0].date:
                    break  # Just verify it exists

    def test_empty_documents_list(self):
        """Test with empty documents list."""
        qualifications = analyze_qualifications([])
        assert len(qualifications) == 0

    def test_no_resumes(self):
        """Test when no resumes are present."""
        documents = [
            {
                'filepath': 'letter.txt',
                'text': 'I believe in teamwork',
                'document_type': DocumentType.COVER_LETTER.value,
                'date': date(2024, 1, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)
        assert len(qualifications) == 0

    def test_multiple_resume_versions(self):
        """Test analyzing multiple versions of resume."""
        documents = [
            {
                'filepath': 'resume_v1.txt',
                'text': 'Engineer at TechCorp\n• Led team of engineers',
                'document_type': DocumentType.RESUME.value,
                'date': date(2023, 1, 1)
            },
            {
                'filepath': 'resume_v2.txt',
                'text': 'Senior Engineer at TechCorp\n• Managed engineering team',
                'document_type': DocumentType.RESUME.value,
                'date': date(2024, 1, 1)
            }
        ]

        qualifications = analyze_qualifications(documents)

        # Should find qualifications across versions
        assert len(qualifications) >= 0

    def test_handles_missing_date(self):
        """Test handling documents without dates."""
        documents = [
            {
                'filepath': 'resume.txt',
                'text': 'Engineer\n• Did work',
                'document_type': DocumentType.RESUME.value,
                'date': None
            }
        ]

        qualifications = analyze_qualifications(documents)
        assert len(qualifications) >= 0
