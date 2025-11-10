import pytest
from cv_formatting.style_parser import StyleParser


def test_parse_css_extracts_style_classes():
    """Test that CSS parsing extracts style class definitions"""
    css = """
    .ps2539 {
        font-weight: bold;
        font-size: calc(var(--slide-scale, 1) * 9.00pt);
        color: rgba(255,109,73,1.000);
    }
    .ss2505 {
        font-weight: bold;
        font-size: calc(var(--slide-scale, 1) * 9.00pt);
    }
    """

    parser = StyleParser()
    styles = parser.parse_css(css)

    assert len(styles) == 2
    assert 'ps2539' in styles
    assert styles['ps2539']['bold'] == True
    assert styles['ps2539']['size'] == 9
    assert styles['ps2539']['color'] == 'rgba(255,109,73,1.000)'


def test_parse_css_handles_empty_input():
    """Test that empty CSS returns empty dict"""
    parser = StyleParser()
    styles = parser.parse_css("")

    assert styles == {}
