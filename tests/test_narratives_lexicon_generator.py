"""Tests for narratives_lexicon_generator module."""

import pytest
from datetime import date
from pathlib import Path
import tempfile
import os

from analyzers.narratives_analyzer import NarrativeCategory, NarrativePattern
from generators.narratives_lexicon_generator import generate_narratives_lexicon


@pytest.fixture
def sample_narrative_patterns():
    """Create sample narrative patterns for testing."""
    return [
        NarrativePattern(
            pattern_type="metaphor",
            text="I approach problems like a detective solving a mystery",
            context="Throughout my career at TechCorp, I approach problems like a detective solving a mystery, gathering clues and building understanding.",
            source_document="cover_letter_2024.txt",
            date=date(2024, 1, 15)
        ),
        NarrativePattern(
            pattern_type="metaphor",
            text="My work is like building bridges between teams",
            context="I see my role as like building bridges between technical and business teams, facilitating communication.",
            source_document="cover_letter_2023.txt",
            date=date(2023, 6, 20)
        ),
    ]


@pytest.fixture
def sample_narrative_category(sample_narrative_patterns):
    """Create a sample narrative category for testing."""
    return NarrativeCategory(
        category_name="Metaphors",
        patterns=sample_narrative_patterns,
        confidence=0.78
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


def test_generate_narratives_lexicon_creates_file(sample_narrative_category, temp_output_file):
    """Test that generate_narratives_lexicon creates output file."""
    generate_narratives_lexicon([sample_narrative_category], temp_output_file)

    assert Path(temp_output_file).exists()
    assert Path(temp_output_file).stat().st_size > 0


def test_generate_narratives_lexicon_markdown_structure(sample_narrative_category, temp_output_file):
    """Test that output has correct markdown structure."""
    generate_narratives_lexicon([sample_narrative_category], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check main headers
    assert "# Storytelling Patterns Catalog" in content
    assert "## Metaphors" in content


def test_generate_narratives_lexicon_metadata_inclusion(sample_narrative_category, temp_output_file):
    """Test that metadata (confidence, count) is included."""
    generate_narratives_lexicon([sample_narrative_category], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "Confidence: 78%" in content
    assert "Patterns found: 2" in content
    assert "Generated:" in content


def test_generate_narratives_lexicon_content_accuracy(sample_narrative_category, temp_output_file):
    """Test that narrative content appears correctly."""
    generate_narratives_lexicon([sample_narrative_category], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check patterns appear
    assert "I approach problems like a detective" in content
    assert "My work is like building bridges" in content

    # Check contexts appear
    assert "Throughout my career at TechCorp" in content
    assert "I see my role as" in content

    # Check sources appear
    assert "cover_letter_2024.txt" in content
    assert "cover_letter_2023.txt" in content


def test_generate_narratives_lexicon_chronological_ordering(sample_narrative_category, temp_output_file):
    """Test that patterns are in chronological order (most recent first)."""
    generate_narratives_lexicon([sample_narrative_category], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # More recent date (2024) should appear before older date (2023)
    pos_2024 = content.find("2024-01-15")
    pos_2023 = content.find("2023-06-20")

    assert pos_2024 < pos_2023


def test_generate_narratives_lexicon_empty_input(temp_output_file):
    """Test handling of empty narrative category list."""
    generate_narratives_lexicon([], temp_output_file)

    assert Path(temp_output_file).exists()

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "# Storytelling Patterns Catalog" in content
    assert "No narrative patterns found" in content


def test_generate_narratives_lexicon_creates_directory():
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "subdir", "nested", "output.md")

        category = NarrativeCategory(
            category_name="Test Category",
            patterns=[
                NarrativePattern(
                    pattern_type="test",
                    text="Test pattern text",
                    context="Test context",
                    source_document="test.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.5
        )

        generate_narratives_lexicon([category], output_path)

        assert Path(output_path).exists()
        assert Path(output_path).parent.exists()


def test_generate_narratives_lexicon_multiple_categories(temp_output_file):
    """Test generating lexicon with multiple narrative categories."""
    categories = [
        NarrativeCategory(
            category_name="Metaphors",
            patterns=[
                NarrativePattern(
                    pattern_type="metaphor",
                    text="Building bridges",
                    context="Building bridges context",
                    source_document="doc1.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.8
        ),
        NarrativeCategory(
            category_name="Opening Hooks",
            patterns=[
                NarrativePattern(
                    pattern_type="opening-hook",
                    text="What if we could transform",
                    context="Opening hook context",
                    source_document="doc2.txt",
                    date=date(2024, 2, 1)
                )
            ],
            confidence=0.9
        ),
    ]

    generate_narratives_lexicon(categories, temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Metaphors" in content
    assert "## Opening Hooks" in content
    assert "Building bridges" in content
    assert "What if we could transform" in content


def test_generate_narratives_lexicon_alphabetical_ordering(temp_output_file):
    """Test that categories are ordered alphabetically."""
    categories = [
        NarrativeCategory(
            category_name="Transitions",
            patterns=[
                NarrativePattern(
                    pattern_type="transition",
                    text="Test",
                    context="Test",
                    source_document="doc.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.5
        ),
        NarrativeCategory(
            category_name="Metaphors",
            patterns=[
                NarrativePattern(
                    pattern_type="metaphor",
                    text="Test",
                    context="Test",
                    source_document="doc.txt",
                    date=date(2024, 1, 1)
                )
            ],
            confidence=0.5
        ),
    ]

    generate_narratives_lexicon(categories, temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # "Metaphors" should appear before "Transitions" alphabetically
    pos_metaphors = content.find("## Metaphors")
    pos_transitions = content.find("## Transitions")

    assert pos_metaphors < pos_transitions


def test_generate_narratives_lexicon_no_dates(temp_output_file):
    """Test handling narratives with missing dates."""
    category = NarrativeCategory(
        category_name="Test Category",
        patterns=[
            NarrativePattern(
                pattern_type="test",
                text="Test pattern",
                context="Test context",
                source_document="test.txt",
                date=None
            )
        ],
        confidence=0.6
    )

    generate_narratives_lexicon([category], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## Test Category" in content
    assert "Test pattern" in content
    # Should handle None dates gracefully
    assert "Unknown" in content
