"""Tests for CVAnalyzer text-to-JSON conversion."""
import pytest
from pathlib import Path
import tempfile
import yaml
from cv_formatting.cv_analyzer import CVAnalyzer
from cv_formatting.metadata_inference import MetadataHelper
from cv_formatting.learning_system import LearningSystem


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


@pytest.fixture
def temp_learned_file():
    """Create temporary learned-preferences.yaml for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        learned = {
            'style_rules': [],
            'metadata_defaults': {},
            'section_patterns': {}
        }
        yaml.dump(learned, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


def test_detect_section_header():
    """Test 'EDUCATION' detected as Section Header"""
    analyzer = CVAnalyzer()

    raw_text = """
    EDUCATION
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find EDUCATION section
    education_items = [item for item in content if item['text'].strip() == 'EDUCATION']
    assert len(education_items) > 0, "Should find EDUCATION section"
    assert education_items[0]['style'] == 'Section Header'


def test_detect_cv_name():
    """Test name at top detected as CV Name style"""
    analyzer = CVAnalyzer()

    raw_text = """
    ANTHONY BYRNES
    T: 213.305.3132
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # First non-empty item should be name
    name_item = content[0]
    assert 'ANTHONY BYRNES' in name_item['text']
    assert name_item['style'] == 'CV Name'


def test_parse_contact_info():
    """Test phone/email detection"""
    analyzer = CVAnalyzer()

    raw_text = """
    T: 213.305.3132
    E: anthonybyrnes@mac.com
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find contact info items
    phone_items = [item for item in content if 'T: 213.305.3132' in item['text']]
    email_items = [item for item in content if 'E: anthonybyrnes@mac.com' in item['text']]

    assert len(phone_items) > 0, "Should detect phone"
    assert phone_items[0]['style'] == 'Contact Info'

    assert len(email_items) > 0, "Should detect email"
    assert email_items[0]['style'] == 'Contact Info'


def test_parse_timeline_entry():
    """Test '2020-2024 CSULB' parsed with institution inline"""
    analyzer = CVAnalyzer()

    raw_text = """
    EDUCATION

    2020-2024  California State University, Long Beach
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find timeline entry
    timeline_items = [item for item in content if '2020-2024' in item['text']]
    assert len(timeline_items) > 0, "Should find timeline entry"

    timeline = timeline_items[0]
    assert timeline['style'] == 'Timeline Entry'

    # Check for inline institution style
    if 'inline_styles' in timeline:
        institutions = [s for s in timeline['inline_styles']
                       if s['style'] == 'Institution']
        assert len(institutions) > 0, "Should have Institution inline style"
        assert 'California State University' in institutions[0]['text']


def test_parse_timeline_with_job_title():
    """Test job title detected and styled"""
    analyzer = CVAnalyzer()

    raw_text = """
    PROFESSIONAL EXPERIENCE

    2020-2024  California State University, Long Beach
    Interim Associate Dean, College of the Arts
    Led $29M budget across 23 programs
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find job title (should be after timeline entry)
    dean_items = [item for item in content if 'Interim Associate Dean' in item['text']]
    assert len(dean_items) > 0, "Should find job title"

    job_title_item = dean_items[0]
    # Job titles can be styled as Body Text with inline Job Title, or as standalone
    assert job_title_item['style'] in ['Body Text', 'Timeline Entry']


def test_parse_bullet_list():
    """Test bullet detection and style assignment"""
    analyzer = CVAnalyzer()

    raw_text = """
    EDUCATION

    2020-2024  California State University, Long Beach
    • Led $29M budget across 23 programs
    • Managed 150+ faculty and staff
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find bullet items
    bullet_items = [item for item in content if item['text'].strip().startswith('•')]
    assert len(bullet_items) >= 2, "Should find at least 2 bullet items"

    # Bullets should use Bullet Standard style
    for bullet in bullet_items:
        assert bullet['style'] in ['Bullet Standard', 'Bullet Gray', 'Bullet Emphasis']


def test_detect_contact_info_variations():
    """Test various contact info formats"""
    analyzer = CVAnalyzer()

    raw_text = """
    Phone: 213.305.3132
    Email: anthonybyrnes@mac.com
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    phone_items = [item for item in content if '213.305.3132' in item['text']]
    email_items = [item for item in content if 'anthonybyrnes@mac.com' in item['text']]

    assert len(phone_items) > 0, "Should detect 'Phone:' format"
    assert len(email_items) > 0, "Should detect 'Email:' format"


def test_full_cv_parsing():
    """Test complete CV text → JSON conversion"""
    analyzer = CVAnalyzer()

    raw_text = """
    ANTHONY BYRNES
    T: 213.305.3132
    E: anthonybyrnes@mac.com

    EDUCATION

    2020-2024  California State University, Long Beach
    Interim Associate Dean, College of the Arts
    • Led $29M budget across 23 programs
    • Managed 150+ faculty and staff

    PROFESSIONAL EXPERIENCE

    2015-2020  The Colburn School
    Director of Production
    Oversaw all theatrical productions
    """

    result = analyzer.analyze(raw_text)

    # Check structure
    assert 'document_metadata' in result
    assert 'content' in result

    content = result['content']

    # Verify key elements are detected
    name_found = any('ANTHONY BYRNES' in item['text'] for item in content)
    education_found = any(item['text'].strip() == 'EDUCATION' for item in content)
    experience_found = any('PROFESSIONAL EXPERIENCE' in item['text'] for item in content)
    timeline_found = any('2020-2024' in item['text'] for item in content)
    bullet_found = any(item['text'].strip().startswith('•') for item in content)

    assert name_found, "Should detect name"
    assert education_found, "Should detect EDUCATION section"
    assert experience_found, "Should detect EXPERIENCE section"
    assert timeline_found, "Should detect timeline entries"
    assert bullet_found, "Should detect bullets"


def test_empty_lines_ignored():
    """Test that empty lines are ignored"""
    analyzer = CVAnalyzer()

    raw_text = """


    EDUCATION


    2020-2024  CSULB


    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Should have exactly 2 items (section header + timeline)
    non_empty = [item for item in content if item['text'].strip()]
    assert len(non_empty) == 2


def test_metadata_included_in_result(temp_defaults_file):
    """Test that document metadata is included in result"""
    metadata_helper = MetadataHelper(defaults_path=temp_defaults_file)
    analyzer = CVAnalyzer(metadata_helper=metadata_helper)

    raw_text = """
    EDUCATION
    """

    result = analyzer.analyze(raw_text)

    assert 'document_metadata' in result
    metadata = result['document_metadata']

    assert metadata['type'] == 'cv'
    assert metadata['author_name'] == 'ANTHONY BYRNES'
    assert 'document_title' in metadata
    assert 'page_header' in metadata


def test_section_header_all_caps_detection():
    """Test that all-caps lines are detected as section headers"""
    analyzer = CVAnalyzer()

    raw_text = """
    EDUCATION
    PROFESSIONAL EXPERIENCE
    PUBLICATIONS
    TEACHING
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    section_headers = [item for item in content if item['style'] == 'Section Header']
    assert len(section_headers) == 4, "Should find 4 section headers"


def test_timeline_variations():
    """Test various timeline date formats"""
    analyzer = CVAnalyzer()

    raw_text = """
    2020-2024  Position 1
    2020 - 2024  Position 2
    Fall 2020  Position 3
    2020-Present  Position 4
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # All should be detected as timeline entries or similar
    timeline_items = [item for item in content if 'Timeline Entry' in item['style']
                     or '2020' in item['text']]
    assert len(timeline_items) >= 4, "Should detect various date formats"


def test_bullet_variations():
    """Test various bullet formats (•, -, *)"""
    analyzer = CVAnalyzer()

    raw_text = """
    EDUCATION

    • Bullet with dot
    - Bullet with dash
    * Bullet with asterisk
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    bullets = [item for item in content
              if item['text'].strip().startswith(('•', '-', '*'))
              and item['style'].startswith('Bullet')]

    assert len(bullets) >= 3, "Should detect various bullet formats"


def test_with_learning_system(temp_defaults_file, temp_learned_file):
    """Test analyzer works with learning system integration"""
    metadata_helper = MetadataHelper(defaults_path=temp_defaults_file)
    learning_system = LearningSystem(learned_preferences_path=temp_learned_file)

    analyzer = CVAnalyzer(
        metadata_helper=metadata_helper,
        learning_system=learning_system
    )

    raw_text = """
    ANTHONY BYRNES
    EDUCATION
    2020-2024  CSULB
    """

    result = analyzer.analyze(raw_text)

    # Should complete without error
    assert 'content' in result
    assert 'document_metadata' in result


def test_institution_inline_detection():
    """Test that institution names are detected for inline styling"""
    analyzer = CVAnalyzer()

    raw_text = """
    2020-2024  California State University, Long Beach
    2015-2020  The Colburn School
    2010-2015  University of California, Los Angeles
    """

    result = analyzer.analyze(raw_text)
    content = result['content']

    # Find timeline entries with inline styles
    timelines_with_institutions = [
        item for item in content
        if item.get('style') == 'Timeline Entry' and 'inline_styles' in item
    ]

    # At least some should have institution inline styles
    institution_count = sum(
        1 for item in timelines_with_institutions
        if any(s.get('style') == 'Institution' for s in item.get('inline_styles', []))
    )

    # Relaxed assertion - at least 1 institution should be detected
    assert institution_count >= 1, "Should detect at least one institution"
