"""Tests for CV page headers."""
import pytest
from pathlib import Path
from cv_formatting.metadata_inference import MetadataHelper


@pytest.fixture
def metadata_helper():
    """Create MetadataHelper with CV defaults."""
    defaults_path = Path.home() / ".claude/skills/format-resume/defaults.yaml"
    return MetadataHelper(defaults_path=str(defaults_path))


def test_infer_cv_metadata_basic(metadata_helper):
    """Test basic CV metadata inference."""
    content = """
    ANTHONY BYRNES
    T: 213.305.3132
    E: anthonybyrnes@mac.com

    EDUCATION
    """

    metadata = metadata_helper.infer_cv_metadata(content)

    assert metadata['type'] == 'cv'
    assert metadata['author_name'] == 'ANTHONY BYRNES'
    assert metadata['document_title'] == 'Curriculum Vitae'
    assert 'last_updated' in metadata


def test_cv_page_header_format(metadata_helper):
    """Test CV page header format matches design."""
    content = "Sample CV content"

    metadata = metadata_helper.infer_cv_metadata(content)

    assert 'page_header' in metadata
    page_header = metadata['page_header']

    assert page_header['enabled'] is True
    assert page_header['left'] == 'ANTHONY BYRNES - Curriculum Vitae'
    assert page_header['right'] == 'page'


def test_cv_page_header_disabled_when_configured(tmp_path):
    """Test page headers can be disabled via config."""
    # Create temp defaults with page headers disabled
    defaults_file = tmp_path / "defaults.yaml"
    defaults_file.write_text("""
contact:
  name: "JOHN DOE"
  phone: "555-1234"
  email: "john@example.com"

cv_defaults:
  document_title: "Resume"
  page_header:
    enabled: false
    format: "{name} - {title}"

preferences:
  version: "Industry"
""")

    helper = MetadataHelper(defaults_path=str(defaults_file))
    metadata = helper.infer_cv_metadata("Sample content")

    assert metadata['page_header']['enabled'] is False


def test_cv_version_detection_academic(metadata_helper):
    """Test detection of academic CV version."""
    content = """
    EDUCATION
    PUBLICATIONS
    TEACHING EXPERIENCE
    RESEARCH INTERESTS
    """

    metadata = metadata_helper.infer_cv_metadata(content)

    # Should detect academic version
    assert metadata['version'] in ['Academic', 'General']


def test_cv_version_detection_industry(metadata_helper):
    """Test detection of industry CV version."""
    content = """
    EDUCATION
    PROFESSIONAL EXPERIENCE
    SKILLS
    CERTIFICATIONS
    """

    metadata = metadata_helper.infer_cv_metadata(content)

    # Should detect industry version or use default
    assert metadata['version'] in ['Industry', 'Academic', 'General']


def test_cv_version_detection_arts(metadata_helper):
    """Test detection of arts CV version."""
    content = """
    EDUCATION
    PRODUCTIONS
    PERFORMANCES
    ARTISTIC COLLABORATIONS
    """

    metadata = metadata_helper.infer_cv_metadata(content)

    # Should detect arts version or use default
    assert metadata['version'] in ['Arts', 'Academic', 'General']


def test_cv_metadata_includes_date(metadata_helper):
    """Test CV metadata includes formatted date."""
    metadata = metadata_helper.infer_cv_metadata("Sample content")

    assert 'last_updated' in metadata
    # Should be in format like "November 2025"
    assert len(metadata['last_updated']) > 0


def test_cv_metadata_from_defaults(metadata_helper):
    """Test CV metadata loads from defaults.yaml."""
    metadata = metadata_helper.infer_cv_metadata("Sample content")

    # Should load contact info from defaults
    assert metadata['author_name'] == 'ANTHONY BYRNES'

    # Should load document title from defaults
    assert metadata['document_title'] == 'Curriculum Vitae'


def test_cv_page_header_uses_inferred_title(tmp_path):
    """Test page header uses inferred document title."""
    defaults_file = tmp_path / "defaults.yaml"
    defaults_file.write_text("""
contact:
  name: "JOHN DOE"
  phone: "555-1234"
  email: "john@example.com"

cv_defaults:
  document_title: "Resume"
  page_header:
    enabled: true
    format: "{name} - {title}"

preferences:
  version: "Industry"
""")

    helper = MetadataHelper(defaults_path=str(defaults_file))
    metadata = helper.infer_cv_metadata("Sample content")

    # Page header should use "Resume" not "Curriculum Vitae"
    assert metadata['page_header']['left'] == 'JOHN DOE - Resume'
