from cv_formatting.style_mapping import STYLE_CONSOLIDATION, get_semantic_name


def test_consolidation_map_contains_key_styles():
    """Test that consolidation map includes heavily used styles"""
    # Most used style from analysis
    assert 'ss2578' in STYLE_CONSOLIDATION
    assert STYLE_CONSOLIDATION['ss2578'] == 'Play Title'

    # Institution names
    assert 'ss2505' in STYLE_CONSOLIDATION
    assert STYLE_CONSOLIDATION['ss2505'] == 'Institution'

    # Body text duplicates should all map to same name
    assert STYLE_CONSOLIDATION['ps81934'] == 'Body Text'
    assert STYLE_CONSOLIDATION['ps2548'] == 'Body Text'


def test_get_semantic_name_returns_mapped_name():
    """Test getting semantic name for old style"""
    assert get_semantic_name('ss2578') == 'Play Title'
    assert get_semantic_name('ss2505') == 'Institution'


def test_get_semantic_name_returns_none_for_unknown():
    """Test that unknown styles return None"""
    assert get_semantic_name('unknown123') is None


def test_all_twelve_core_styles_present():
    """Test that all 12 core styles are represented"""
    semantic_names = set(STYLE_CONSOLIDATION.values())

    expected_styles = {
        'CV Name',
        'Section Header',
        'Body Text',
        'Timeline Entry',
        'Bullet Standard',
        'Bullet Gray',
        'Bullet Emphasis',
        'Play Title',
        'Institution',
        'Job Title',
        'Orange Emphasis',
        'Gray Text'
    }

    assert semantic_names == expected_styles
