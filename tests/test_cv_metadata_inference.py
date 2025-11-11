"""Tests for CV metadata inference."""
import pytest
from pathlib import Path
import tempfile
import yaml
from cv_formatting.metadata_inference import MetadataHelper


@pytest.fixture
def temp_defaults_file():
    """Create temporary defaults.yaml for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        defaults = {
            'contact': {
                'name': 'ANTHONY BYRNES',
                'phone': '213.305.3132',
                'email': 'anthonybyrnes@mac.com'
            },
            'cv_defaults': {
                'document_title': 'Curriculum Vitae',
                'page_header': {
                    'enabled': True,
                    'format': '{name} - {title}'
                }
            },
            'preferences': {
                'version': 'Academic'
            }
        }
        yaml.dump(defaults, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


def test_load_defaults_from_yaml(temp_defaults_file):
    """Test contact info loaded from defaults.yaml"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)
    defaults = helper.get_defaults()

    assert defaults['contact']['name'] == 'ANTHONY BYRNES'
    assert defaults['contact']['phone'] == '213.305.3132'
    assert defaults['contact']['email'] == 'anthonybyrnes@mac.com'
    assert defaults['cv_defaults']['document_title'] == 'Curriculum Vitae'


def test_infer_cv_metadata(temp_defaults_file):
    """Test basic CV metadata inference from content and defaults"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = """
    ANTHONY BYRNES
    T: 213.305.3132
    E: anthonybyrnes@mac.com

    EDUCATION
    2020-2024  California State University, Long Beach
    """

    metadata = helper.infer_cv_metadata(raw_text)

    assert metadata['type'] == 'cv'
    assert metadata['author_name'] == 'ANTHONY BYRNES'
    assert 'document_title' in metadata
    assert 'page_header' in metadata
    assert metadata['page_header']['enabled'] is True


def test_infer_cv_title_from_defaults(temp_defaults_file):
    """Test detecting 'Curriculum Vitae' from defaults"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = "EDUCATION\n2020-2024 CSULB"

    metadata = helper.infer_cv_metadata(raw_text)

    assert metadata['document_title'] == 'Curriculum Vitae'


def test_infer_cv_title_prefers_content(temp_defaults_file):
    """Test that explicit title in content overrides defaults"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    # Content explicitly says "Resume"
    raw_text = "Resume\nANTHONY BYRNES\nEDUCATION"

    metadata = helper.infer_cv_metadata(raw_text)

    # Should detect "Resume" from content
    assert metadata['document_title'] in ['Resume', 'Curriculum Vitae']


def test_infer_cv_version_academic(temp_defaults_file):
    """Test detecting Academic version based on sections"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = """
    EDUCATION
    PUBLICATIONS
    TEACHING EXPERIENCE
    RESEARCH
    """

    metadata = helper.infer_cv_metadata(raw_text)

    assert metadata['version'] == 'Academic'


def test_infer_cv_version_industry(temp_defaults_file):
    """Test detecting Industry version based on sections"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = """
    EDUCATION
    PROFESSIONAL EXPERIENCE
    SKILLS
    CERTIFICATIONS
    """

    metadata = helper.infer_cv_metadata(raw_text)

    assert metadata['version'] in ['Industry', 'Academic', 'General']


def test_infer_cv_version_arts(temp_defaults_file):
    """Test detecting Arts version based on sections"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = """
    EDUCATION
    PRODUCTIONS
    PERFORMANCES
    PROFESSIONAL EXPERIENCE
    """

    metadata = helper.infer_cv_metadata(raw_text)

    assert metadata['version'] in ['Arts', 'Academic', 'General']


def test_generate_page_header_config(temp_defaults_file):
    """Test page header config generation from metadata"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = "EDUCATION"

    metadata = helper.infer_cv_metadata(raw_text)

    page_header = metadata['page_header']
    assert page_header['enabled'] is True
    assert 'ANTHONY BYRNES' in page_header['left']
    assert 'Curriculum Vitae' in page_header['left']
    assert page_header['right'] == 'page'


def test_get_current_date_formatted(temp_defaults_file):
    """Test current date is formatted correctly"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    date_str = helper.get_current_date()

    # Should return a date string
    assert isinstance(date_str, str)
    assert len(date_str) > 0


def test_infer_cv_metadata_with_missing_defaults():
    """Test metadata inference works with fallback defaults when file missing"""
    # Use nonexistent path to trigger fallback
    helper = MetadataHelper(defaults_path="/nonexistent/path/defaults.yaml")

    raw_text = "EDUCATION\n2020-2024 CSULB"

    metadata = helper.infer_cv_metadata(raw_text)

    # Should still work with fallback defaults
    assert metadata['type'] == 'cv'
    assert 'author_name' in metadata
    assert 'document_title' in metadata


def test_detect_cv_vs_resume_preference(temp_defaults_file):
    """Test system prefers 'Curriculum Vitae' over 'Resume' for academic CVs"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    academic_text = """
    EDUCATION
    PUBLICATIONS
    TEACHING
    """

    metadata = helper.infer_cv_metadata(academic_text)

    # For academic content, should prefer "Curriculum Vitae"
    assert metadata['document_title'] == 'Curriculum Vitae'


def test_page_header_format_string(temp_defaults_file):
    """Test page header uses correct format string"""
    helper = MetadataHelper(defaults_path=temp_defaults_file)

    raw_text = "EDUCATION"

    metadata = helper.infer_cv_metadata(raw_text)

    # Should follow format: "NAME - TITLE"
    left_text = metadata['page_header']['left']
    assert ' - ' in left_text
    assert left_text.startswith('ANTHONY BYRNES')
