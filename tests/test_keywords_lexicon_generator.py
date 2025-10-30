"""Tests for keywords_lexicon_generator module."""

import pytest
from datetime import date
from pathlib import Path
import tempfile
import os

from analyzers.keywords_analyzer import KeywordEntry, KeywordUsage
from generators.keywords_lexicon_generator import generate_keywords_lexicon


@pytest.fixture
def sample_keyword_usages():
    """Create sample keyword usages for testing."""
    return [
        KeywordUsage(
            keyword="stakeholder management",
            context="Strong stakeholder management skills across technical and business teams",
            source_document="resume_2024.txt",
            document_type="resume",
            date=date(2024, 2, 1)
        ),
        KeywordUsage(
            keyword="stakeholder management",
            context="I bring extensive experience in stakeholder management to complex projects",
            source_document="cover_letter_2024.txt",
            document_type="cover_letter",
            date=date(2024, 1, 15)
        ),
        KeywordUsage(
            keyword="stakeholder management",
            context="Demonstrated stakeholder management through successful client engagements",
            source_document="resume_2020.txt",
            document_type="resume",
            date=date(2020, 6, 1)
        ),
    ]


@pytest.fixture
def sample_keyword_entry(sample_keyword_usages):
    """Create a sample keyword entry for testing."""
    return KeywordEntry(
        keyword="stakeholder management",
        aliases=["project management", "client relations"],
        usages=sample_keyword_usages,
        frequency=3,
        document_types={"resume", "cover_letter"}
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


def test_generate_keywords_lexicon_creates_file(sample_keyword_entry, temp_output_file):
    """Test that generate_keywords_lexicon creates output file."""
    generate_keywords_lexicon([sample_keyword_entry], temp_output_file)

    assert Path(temp_output_file).exists()
    assert Path(temp_output_file).stat().st_size > 0


def test_generate_keywords_lexicon_markdown_structure(sample_keyword_entry, temp_output_file):
    """Test that output has correct markdown structure."""
    generate_keywords_lexicon([sample_keyword_entry], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check main headers
    assert "# Keyword Usage Index" in content
    assert "## stakeholder management" in content
    assert "### Usage contexts (most recent first)" in content


def test_generate_keywords_lexicon_metadata_inclusion(sample_keyword_entry, temp_output_file):
    """Test that metadata (frequency, aliases, document types) is included."""
    generate_keywords_lexicon([sample_keyword_entry], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "Frequency: 3" in content
    assert "Aliases: project management, client relations" in content
    assert "Document types: " in content
    # Check that both document types are mentioned (order may vary due to set)
    assert "resume" in content
    assert "cover_letter" in content
    assert "Generated:" in content


def test_generate_keywords_lexicon_content_accuracy(sample_keyword_entry, temp_output_file):
    """Test that keyword content appears correctly."""
    generate_keywords_lexicon([sample_keyword_entry], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check contexts appear (keywords will be bolded)
    assert "Strong **stakeholder management** skills" in content
    assert "I bring extensive experience in **stakeholder management**" in content
    assert "Demonstrated **stakeholder management**" in content

    # Check sources appear
    assert "resume_2024.txt" in content
    assert "cover_letter_2024.txt" in content
    assert "resume_2020.txt" in content


def test_generate_keywords_lexicon_chronological_ordering(sample_keyword_entry, temp_output_file):
    """Test that usages are ordered by most recent first."""
    generate_keywords_lexicon([sample_keyword_entry], temp_output_file)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Most recent date (2024-02) should appear before older dates
    pos_2024_feb = content.find("2024-02-01")
    pos_2024_jan = content.find("2024-01-15")
    pos_2020 = content.find("2020-06-01")

    assert pos_2024_feb < pos_2024_jan < pos_2020


def test_generate_keywords_lexicon_empty_input(temp_output_file):
    """Test handling of empty keyword list."""
    generate_keywords_lexicon([], temp_output_file)

    assert Path(temp_output_file).exists()

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "# Keyword Usage Index" in content
    assert "No keywords found" in content


def test_generate_keywords_lexicon_min_frequency_filter(temp_output_file):
    """Test filtering keywords by minimum frequency."""
    keywords = [
        KeywordEntry(
            keyword="high frequency",
            aliases=[],
            usages=[
                KeywordUsage("high frequency", "context", "doc.txt", "resume", date(2024, 1, 1)),
                KeywordUsage("high frequency", "context", "doc.txt", "resume", date(2024, 1, 2)),
                KeywordUsage("high frequency", "context", "doc.txt", "resume", date(2024, 1, 3)),
            ],
            frequency=3,
            document_types={"resume"}
        ),
        KeywordEntry(
            keyword="low frequency",
            aliases=[],
            usages=[
                KeywordUsage("low frequency", "context", "doc.txt", "resume", date(2024, 1, 1)),
            ],
            frequency=1,
            document_types={"resume"}
        ),
    ]

    generate_keywords_lexicon(keywords, temp_output_file, min_frequency=2)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # High frequency should appear
    assert "## high frequency" in content
    # Low frequency should NOT appear
    assert "## low frequency" not in content


def test_generate_keywords_lexicon_creates_directory():
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "subdir", "nested", "output.md")

        keyword = KeywordEntry(
            keyword="test keyword",
            aliases=[],
            usages=[
                KeywordUsage(
                    keyword="test keyword",
                    context="Test context",
                    source_document="test.txt",
                    document_type="resume",
                    date=date(2024, 1, 1)
                )
            ],
            frequency=1,
            document_types={"resume"}
        )

        generate_keywords_lexicon([keyword], output_path, min_frequency=1)

        assert Path(output_path).exists()
        assert Path(output_path).parent.exists()


def test_generate_keywords_lexicon_multiple_keywords(temp_output_file):
    """Test generating lexicon with multiple keywords."""
    keywords = [
        KeywordEntry(
            keyword="software engineering",
            aliases=["software development"],
            usages=[
                KeywordUsage(
                    keyword="software engineering",
                    context="Expert in software engineering",
                    source_document="resume.txt",
                    document_type="resume",
                    date=date(2024, 1, 1)
                )
            ],
            frequency=1,
            document_types={"resume"}
        ),
        KeywordEntry(
            keyword="data analysis",
            aliases=["analytics"],
            usages=[
                KeywordUsage(
                    keyword="data analysis",
                    context="Skilled in data analysis",
                    source_document="resume.txt",
                    document_type="resume",
                    date=date(2024, 1, 1)
                )
            ],
            frequency=1,
            document_types={"resume"}
        ),
    ]

    generate_keywords_lexicon(keywords, temp_output_file, min_frequency=1)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## data analysis" in content
    assert "## software engineering" in content
    assert "Expert in **software engineering**" in content
    assert "Skilled in **data analysis**" in content


def test_generate_keywords_lexicon_alphabetical_ordering(temp_output_file):
    """Test that keywords are ordered alphabetically."""
    keywords = [
        KeywordEntry(
            keyword="zebra keyword",
            aliases=[],
            usages=[
                KeywordUsage("zebra keyword", "context", "doc.txt", "resume", date(2024, 1, 1))
            ],
            frequency=1,
            document_types={"resume"}
        ),
        KeywordEntry(
            keyword="alpha keyword",
            aliases=[],
            usages=[
                KeywordUsage("alpha keyword", "context", "doc.txt", "resume", date(2024, 1, 1))
            ],
            frequency=1,
            document_types={"resume"}
        ),
    ]

    generate_keywords_lexicon(keywords, temp_output_file, min_frequency=1)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # "alpha keyword" should appear before "zebra keyword"
    pos_alpha = content.find("## alpha keyword")
    pos_zebra = content.find("## zebra keyword")

    assert pos_alpha < pos_zebra


def test_generate_keywords_lexicon_no_dates(temp_output_file):
    """Test handling keywords with missing dates."""
    keyword = KeywordEntry(
        keyword="test keyword",
        aliases=[],
        usages=[
            KeywordUsage(
                keyword="test keyword",
                context="Test context",
                source_document="test.txt",
                document_type="resume",
                date=None
            )
        ],
        frequency=1,
        document_types={"resume"}
    )

    generate_keywords_lexicon([keyword], temp_output_file, min_frequency=1)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## test keyword" in content
    assert "Test context" in content
    # Should handle None dates gracefully
    assert "Unknown" in content


def test_generate_keywords_lexicon_no_aliases(temp_output_file):
    """Test handling keywords with no aliases."""
    keyword = KeywordEntry(
        keyword="test keyword",
        aliases=[],
        usages=[
            KeywordUsage(
                keyword="test keyword",
                context="Test context",
                source_document="test.txt",
                document_type="resume",
                date=date(2024, 1, 1)
            )
        ],
        frequency=1,
        document_types={"resume"}
    )

    generate_keywords_lexicon([keyword], temp_output_file, min_frequency=1)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "## test keyword" in content
    # Should handle empty aliases gracefully (either omit or say "None")
    assert "Aliases: None" in content or "Aliases:" not in content
