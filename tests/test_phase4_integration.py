"""
Integration tests for Phase 4 - Full pipeline from text extraction to lexicon generation.

Tests the complete workflow: extraction -> classification -> analysis -> generation
"""

import pytest
from pathlib import Path
import tempfile
import os

from utils.text_extraction import extract_text_from_document
from utils.date_parser import extract_date_from_filename
from core.document_processor import classify_document, DocumentType
from analyzers.themes_analyzer import analyze_themes
from analyzers.qualifications_analyzer import analyze_qualifications
from analyzers.narratives_analyzer import analyze_narratives
from analyzers.keywords_analyzer import analyze_keywords
from generators.themes_lexicon_generator import generate_themes_lexicon
from generators.qualifications_lexicon_generator import generate_qualifications_lexicon
from generators.narratives_lexicon_generator import generate_narratives_lexicon
from generators.keywords_lexicon_generator import generate_keywords_lexicon


@pytest.fixture
def fixtures_dir():
    """Get path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_full_pipeline_phases_1_to_4(fixtures_dir, temp_output_dir):
    """
    Test complete pipeline from extraction to lexicon generation.

    This integration test exercises:
    - Phase 1: Text extraction and date parsing
    - Phase 2: Document classification
    - Phase 3: All 4 analyzers (themes, qualifications, narratives, keywords)
    - Phase 4: All 4 generators (lexicon outputs)
    """
    # Phase 1: Load sample documents
    resume_path = fixtures_dir / "sample_resume.txt"
    cover_letter_path = fixtures_dir / "sample_cover_letter.txt"
    resume_v2_path = fixtures_dir / "sample_resume_v2.txt"

    # Extract text
    resume_result = extract_text_from_document(str(resume_path))
    cover_letter_result = extract_text_from_document(str(cover_letter_path))
    resume_v2_result = extract_text_from_document(str(resume_v2_path))

    resume_text = resume_result['text']
    cover_letter_text = cover_letter_result['text']
    resume_v2_text = resume_v2_result['text']

    assert resume_text
    assert cover_letter_text
    assert resume_v2_text

    # Parse dates (these files don't have dates in names, so will be None)
    resume_date = extract_date_from_filename(str(resume_path))
    cover_letter_date = extract_date_from_filename(str(cover_letter_path))
    resume_v2_date = extract_date_from_filename(str(resume_v2_path))

    # Phase 2: Classify documents
    resume_type = classify_document(resume_text, str(resume_path))
    cover_letter_type = classify_document(cover_letter_text, str(cover_letter_path))
    resume_v2_type = classify_document(resume_v2_text, str(resume_v2_path))

    assert resume_type == DocumentType.RESUME
    assert cover_letter_type == DocumentType.COVER_LETTER
    assert resume_v2_type == DocumentType.RESUME

    # Prepare document list for analyzers
    documents = [
        {
            "text": resume_text,
            "filepath": str(resume_path),
            "date": resume_date,
            "doc_type": resume_type
        },
        {
            "text": cover_letter_text,
            "filepath": str(cover_letter_path),
            "date": cover_letter_date,
            "doc_type": cover_letter_type
        },
        {
            "text": resume_v2_text,
            "filepath": str(resume_v2_path),
            "date": resume_v2_date,
            "doc_type": resume_v2_type
        },
    ]

    # Phase 3: Run all analyzers
    themes = analyze_themes(documents)
    qualifications = analyze_qualifications(documents)
    narratives = analyze_narratives(documents)
    keywords = analyze_keywords(documents)

    # Verify analyzer outputs
    assert len(themes) > 0, "Should find themes in cover letter"
    assert len(qualifications) > 0, "Should find qualifications in resumes"
    assert len(narratives) > 0, "Should find narratives in cover letter"
    assert len(keywords) > 0, "Should find keywords across documents"

    # Phase 4: Generate all lexicons
    themes_output = os.path.join(temp_output_dir, "my_values.md")
    qualifications_output = os.path.join(temp_output_dir, "resume_variations.md")
    narratives_output = os.path.join(temp_output_dir, "storytelling_patterns.md")
    keywords_output = os.path.join(temp_output_dir, "usage_index.md")

    generate_themes_lexicon(themes, themes_output)
    generate_qualifications_lexicon(qualifications, qualifications_output)
    generate_narratives_lexicon(narratives, narratives_output)
    generate_keywords_lexicon(keywords, keywords_output, min_frequency=1)

    # Verify all output files exist
    assert Path(themes_output).exists()
    assert Path(qualifications_output).exists()
    assert Path(narratives_output).exists()
    assert Path(keywords_output).exists()

    # Verify themes lexicon content
    with open(themes_output, 'r', encoding='utf-8') as f:
        themes_content = f.read()
    assert "# My Values and Themes" in themes_content
    assert "collaborative leadership" in themes_content.lower() or "leadership" in themes_content.lower()

    # Verify qualifications lexicon content
    with open(qualifications_output, 'r', encoding='utf-8') as f:
        quals_content = f.read()
    assert "# Resume Bullet Variations" in quals_content
    assert "TechCorp" in quals_content
    # Should show variations between resume versions
    assert "Version" in quals_content

    # Verify narratives lexicon content
    with open(narratives_output, 'r', encoding='utf-8') as f:
        narratives_content = f.read()
    assert "# Storytelling Patterns Catalog" in narratives_content
    assert "detective" in narratives_content.lower() or "metaphor" in narratives_content.lower()

    # Verify keywords lexicon content
    with open(keywords_output, 'r', encoding='utf-8') as f:
        keywords_content = f.read()
    assert "# Keyword Usage Index" in keywords_content
    assert "stakeholder management" in keywords_content.lower()


def test_themes_generator_with_real_fixtures(fixtures_dir, temp_output_dir):
    """Test themes generator with real fixture data."""
    cover_letter_path = fixtures_dir / "sample_cover_letter.txt"
    cover_letter_result = extract_text_from_document(str(cover_letter_path))
    cover_letter_text = cover_letter_result['text']

    documents = [{
        "text": cover_letter_text,
        "filepath": str(cover_letter_path),
        "date": None,
        "doc_type": DocumentType.COVER_LETTER
    }]

    themes = analyze_themes(documents)
    output_path = os.path.join(temp_output_dir, "themes.md")
    generate_themes_lexicon(themes, output_path)

    assert Path(output_path).exists()
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "# My Values and Themes" in content


def test_qualifications_generator_with_real_fixtures(fixtures_dir, temp_output_dir):
    """Test qualifications generator with real fixture data."""
    resume_path = fixtures_dir / "sample_resume.txt"
    resume_v2_path = fixtures_dir / "sample_resume_v2.txt"

    resume_result = extract_text_from_document(str(resume_path))
    resume_v2_result = extract_text_from_document(str(resume_v2_path))
    resume_text = resume_result['text']
    resume_v2_text = resume_v2_result['text']

    documents = [
        {
            "text": resume_text,
            "filepath": str(resume_path),
            "date": None,
            "doc_type": DocumentType.RESUME
        },
        {
            "text": resume_v2_text,
            "filepath": str(resume_v2_path),
            "date": None,
            "doc_type": DocumentType.RESUME
        }
    ]

    qualifications = analyze_qualifications(documents)
    output_path = os.path.join(temp_output_dir, "qualifications.md")
    generate_qualifications_lexicon(qualifications, output_path)

    assert Path(output_path).exists()
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "# Resume Bullet Variations" in content
    assert "TechCorp" in content


def test_narratives_generator_with_real_fixtures(fixtures_dir, temp_output_dir):
    """Test narratives generator with real fixture data."""
    cover_letter_path = fixtures_dir / "sample_cover_letter.txt"
    cover_letter_result = extract_text_from_document(str(cover_letter_path))
    cover_letter_text = cover_letter_result['text']

    documents = [{
        "text": cover_letter_text,
        "filepath": str(cover_letter_path),
        "date": None,
        "doc_type": DocumentType.COVER_LETTER
    }]

    narratives = analyze_narratives(documents)
    output_path = os.path.join(temp_output_dir, "narratives.md")
    generate_narratives_lexicon(narratives, output_path)

    assert Path(output_path).exists()
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "# Storytelling Patterns Catalog" in content


def test_keywords_generator_with_real_fixtures(fixtures_dir, temp_output_dir):
    """Test keywords generator with real fixture data."""
    resume_path = fixtures_dir / "sample_resume.txt"
    cover_letter_path = fixtures_dir / "sample_cover_letter.txt"

    resume_result = extract_text_from_document(str(resume_path))
    cover_letter_result = extract_text_from_document(str(cover_letter_path))
    resume_text = resume_result['text']
    cover_letter_text = cover_letter_result['text']

    documents = [
        {
            "text": resume_text,
            "filepath": str(resume_path),
            "date": None,
            "doc_type": DocumentType.RESUME
        },
        {
            "text": cover_letter_text,
            "filepath": str(cover_letter_path),
            "date": None,
            "doc_type": DocumentType.COVER_LETTER
        }
    ]

    keywords = analyze_keywords(documents)
    output_path = os.path.join(temp_output_dir, "keywords.md")
    generate_keywords_lexicon(keywords, output_path, min_frequency=1)

    assert Path(output_path).exists()
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "# Keyword Usage Index" in content
    assert "stakeholder management" in content.lower()
