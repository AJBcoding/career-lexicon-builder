"""Tests for qualifications_lexicon_generator module."""

import pytest
from datetime import date
from pathlib import Path
import tempfile
import os

from analyzers.qualifications_analyzer import Qualification, QualificationVariation
from generators.qualifications_lexicon_generator import generate_qualifications_lexicon


@pytest.fixture
def sample_qualification_variations():
    """Create sample qualification variations for testing."""
    return [
        QualificationVariation(
            text="Managed engineering team of 5 developers building cloud infrastructure",
            source_document="resume_2024.txt",
            date=date(2024, 2, 1),
            position_context="Senior Software Engineer at TechCorp"
        ),
        QualificationVariation(
            text="Led cross-functional team of 5 engineers in developing cloud-based applications",
            source_document="resume_2020.txt",
            date=date(2020, 6, 1),
            position_context="Senior Software Engineer at TechCorp"
        ),
    ]


@pytest.fixture
def sample_qualification(sample_qualification_variations):
    """Create a sample qualification for testing."""
    return Qualification(
        qualification_id="senior_engineer_techcorp",
        position_title="Senior Software Engineer",
        organization="TechCorp",
        variations=sample_qualification_variations,
        confidence=0.90
    )


@pytest.fixture
def temp_output_file():
    """Create a temporary file for output testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        output_path = f.name
    yield output_path
    # Cleanup
    if Path(output_path).exists():
        Path(output_path).unlink()


def test_generate_qualifications_lexicon_creates_file(sample_qualification, temp_output_file):
    """Test that generate_qualifications_lexicon creates output file."""
    generate_qualifications_lexicon([sample_qualification], temp_output_file)

    assert Path(temp_output_file).exists()
    assert Path(temp_output_file).stat().st_size > 0


def test_generate_qualifications_lexicon_markdown_structure(sample_qualification, temp_output_file):
    """Test that output has correct markdown structure."""
    generate_qualifications_lexicon([sample_qualification], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check main headers
    assert "# Resume Bullet Variations" in content
    assert "## Senior Software Engineer at TechCorp" in content
    assert "### Variations (most recent first)" in content


def test_generate_qualifications_lexicon_metadata_inclusion(sample_qualification, temp_output_file):
    """Test that metadata (ID, confidence) is included."""
    generate_qualifications_lexicon([sample_qualification], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "ID: `senior_engineer_techcorp`" in content
    assert "Confidence: 90%" in content
    assert "Generated:" in content


def test_generate_qualifications_lexicon_content_accuracy(sample_qualification, temp_output_file):
    """Test that qualification content appears correctly."""
    generate_qualifications_lexicon([sample_qualification], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check variations appear
    assert "Managed engineering team of 5 developers" in content
    assert "Led cross-functional team of 5 engineers" in content

    # Check sources appear
    assert "resume_2024.txt" in content
    assert "resume_2020.txt" in content


def test_generate_qualifications_lexicon_chronological_ordering(sample_qualification, temp_output_file):
    """Test that variations are ordered by most recent first."""
    generate_qualifications_lexicon([sample_qualification], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # More recent date (2024) should appear before older date (2020)
    pos_2024 = content.find("2024-02-01")
    pos_2020 = content.find("2020-06-01")

    assert pos_2024 < pos_2020


def test_generate_qualifications_lexicon_empty_input(temp_output_file):
    """Test handling of empty qualification list."""
    generate_qualifications_lexicon([], temp_output_file)

    assert Path(temp_output_file).exists()

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "# Resume Bullet Variations" in content
    assert "No qualifications found" in content


def test_generate_qualifications_lexicon_creates_directory():
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "subdir", "nested", "output.md")

        qualification = Qualification(
            qualification_id="test_id",
            position_title="Test Position",
            organization="Test Org",
            variations=[
                QualificationVariation(
                    text="Test bullet point",
                    source_document="test.txt",
                    date=date(2024, 1, 1),
                    position_context="Test Position at Test Org"
                )
            ],
            confidence=0.5
        )

        generate_qualifications_lexicon([qualification], output_path)

        assert Path(output_path).exists()
        assert Path(output_path).parent.exists()


def test_generate_qualifications_lexicon_multiple_qualifications(temp_output_file):
    """Test generating lexicon with multiple qualifications."""
    qualifications = [
        Qualification(
            qualification_id="position1",
            position_title="Senior Engineer",
            organization="Company A",
            variations=[
                QualificationVariation(
                    text="Built scalable systems",
                    source_document="resume1.txt",
                    date=date(2024, 1, 1),
                    position_context="Senior Engineer at Company A"
                )
            ],
            confidence=0.9
        ),
        Qualification(
            qualification_id="position2",
            position_title="Developer",
            organization="Company B",
            variations=[
                QualificationVariation(
                    text="Developed web applications",
                    source_document="resume2.txt",
                    date=date(2023, 1, 1),
                    position_context="Developer at Company B"
                )
            ],
            confidence=0.8
        ),
    ]

    generate_qualifications_lexicon(qualifications, temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Senior Engineer at Company A" in content
    assert "## Developer at Company B" in content
    assert "Built scalable systems" in content
    assert "Developed web applications" in content


def test_generate_qualifications_lexicon_no_dates(temp_output_file):
    """Test handling qualifications with missing dates."""
    qualification = Qualification(
        qualification_id="test_id",
        position_title="Test Position",
        organization="Test Org",
        variations=[
            QualificationVariation(
                text="Test variation",
                source_document="test.txt",
                date=None,
                position_context="Test Position at Test Org"
            )
        ],
        confidence=0.7
    )

    generate_qualifications_lexicon([qualification], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Test Position at Test Org" in content
    assert "Test variation" in content
    # Should handle None dates gracefully
    assert "Unknown" in content
