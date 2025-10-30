"""Tests for themes_lexicon_generator module."""

import pytest
from datetime import date
from pathlib import Path
import tempfile
import os

from analyzers.themes_analyzer import Theme, ThemeOccurrence
from generators.themes_lexicon_generator import generate_themes_lexicon


@pytest.fixture
def sample_theme_occurrences():
    """Create sample theme occurrences for testing."""
    return [
        ThemeOccurrence(
            quote="I believe in collaborative leadership",
            context="When working with teams, I believe in collaborative leadership that empowers individuals.",
            source_document="cover_letter_2024.txt",
            date=date(2024, 1, 15)
        ),
        ThemeOccurrence(
            quote="Leadership through collaboration is essential",
            context="Throughout my career, leadership through collaboration is essential to building strong teams.",
            source_document="cover_letter_2023.txt",
            date=date(2023, 6, 20)
        ),
    ]


@pytest.fixture
def sample_theme(sample_theme_occurrences):
    """Create a sample theme for testing."""
    return Theme(
        theme_name="Leadership",
        occurrences=sample_theme_occurrences,
        confidence=0.85,
        first_seen=date(2023, 6, 20),
        last_seen=date(2024, 1, 15)
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


def test_generate_themes_lexicon_creates_file(sample_theme, temp_output_file):
    """Test that generate_themes_lexicon creates output file."""
    generate_themes_lexicon([sample_theme], temp_output_file)

    assert Path(temp_output_file).exists()
    assert Path(temp_output_file).stat().st_size > 0


def test_generate_themes_lexicon_markdown_structure(sample_theme, temp_output_file):
    """Test that output has correct markdown structure."""
    generate_themes_lexicon([sample_theme], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check main headers
    assert "# My Values and Themes" in content
    assert "## Leadership" in content
    assert "### Occurrences (chronological)" in content


def test_generate_themes_lexicon_metadata_inclusion(sample_theme, temp_output_file):
    """Test that metadata (confidence, dates) is included."""
    generate_themes_lexicon([sample_theme], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "Confidence: 85%" in content
    assert "First seen: 2023-06-20" in content
    assert "Last seen: 2024-01-15" in content
    assert "Generated:" in content


def test_generate_themes_lexicon_content_accuracy(sample_theme, temp_output_file):
    """Test that theme content appears correctly."""
    generate_themes_lexicon([sample_theme], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check quotes appear
    assert "I believe in collaborative leadership" in content
    assert "Leadership through collaboration is essential" in content

    # Check contexts appear
    assert "When working with teams" in content
    assert "Throughout my career" in content

    # Check sources appear
    assert "cover_letter_2024.txt" in content
    assert "cover_letter_2023.txt" in content


def test_generate_themes_lexicon_chronological_ordering(sample_theme, temp_output_file):
    """Test that occurrences are in chronological order."""
    generate_themes_lexicon([sample_theme], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Earlier date should appear first
    pos_2023 = content.find("2023-06-20")
    pos_2024 = content.find("2024-01-15")

    assert pos_2023 < pos_2024


def test_generate_themes_lexicon_empty_input(temp_output_file):
    """Test handling of empty theme list."""
    generate_themes_lexicon([], temp_output_file)

    assert Path(temp_output_file).exists()

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "# My Values and Themes" in content
    assert "No themes found" in content


def test_generate_themes_lexicon_creates_directory():
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "subdir", "nested", "output.md")

        theme = Theme(
            theme_name="Test",
            occurrences=[
                ThemeOccurrence(
                    quote="Test quote",
                    context="Test context",
                    source_document="test.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.5,
            first_seen=date(2024, 1, 1),
            last_seen=date(2024, 1, 1)
        )

        generate_themes_lexicon([theme], output_path)

        assert Path(output_path).exists()
        assert Path(output_path).parent.exists()


def test_generate_themes_lexicon_multiple_themes(temp_output_file):
    """Test generating lexicon with multiple themes."""
    themes = [
        Theme(
            theme_name="Leadership",
            occurrences=[
                ThemeOccurrence(
                    quote="Leadership quote",
                    context="Leadership context",
                    source_document="doc1.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.9,
            first_seen=date(2024, 1, 1),
            last_seen=date(2024, 1, 1)
        ),
        Theme(
            theme_name="Innovation",
            occurrences=[
                ThemeOccurrence(
                    quote="Innovation quote",
                    context="Innovation context",
                    source_document="doc2.txt",
                    date=date(2024, 2, 1)
                )
            ],
            confidence=0.8,
            first_seen=date(2024, 2, 1),
            last_seen=date(2024, 2, 1)
        ),
    ]

    generate_themes_lexicon(themes, temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Leadership" in content
    assert "## Innovation" in content
    assert "Leadership quote" in content
    assert "Innovation quote" in content


def test_generate_themes_lexicon_no_dates(temp_output_file):
    """Test handling themes with missing dates."""
    theme = Theme(
        theme_name="Test Theme",
        occurrences=[
            ThemeOccurrence(
                quote="Test quote",
                context="Test context",
                source_document="test.txt",
                date=None
            )
        ],
        confidence=0.7,
        first_seen=None,
        last_seen=None
    )

    generate_themes_lexicon([theme], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Test Theme" in content
    assert "Test quote" in content
    # Should handle None dates gracefully
    assert "Unknown" in content
