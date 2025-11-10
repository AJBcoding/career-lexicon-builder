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
    assert styles['ps2539']['size'] == 9.0
    assert styles['ps2539']['color'] == 'rgba(255,109,73,1.000)'


def test_parse_css_handles_empty_input():
    """Test that empty CSS returns empty dict"""
    parser = StyleParser()
    styles = parser.parse_css("")

    assert styles == {}


def test_parse_css_handles_decimal_font_sizes():
    """Test that font-size parsing handles non-.00 decimals"""
    css = """
    .ps2540 {
        font-size: calc(var(--slide-scale, 1) * 10.5pt);
    }
    .ps2541 {
        font-size: calc(var(--slide-scale, 1) * 12pt);
    }
    .ps2542 {
        font-size: 14.25pt;
    }
    """

    parser = StyleParser()
    styles = parser.parse_css(css)

    assert styles['ps2540']['size'] == 10.5
    assert styles['ps2541']['size'] == 12.0
    assert styles['ps2542']['size'] == 14.25


def test_parse_css_handles_double_quoted_font_family():
    """Test that font-family parsing supports both single and double quotes"""
    css = """
    .ps2543 {
        font-family: 'Helvetica Neue';
    }
    .ps2544 {
        font-family: "Times New Roman";
    }
    """

    parser = StyleParser()
    styles = parser.parse_css(css)

    assert styles['ps2543']['font'] == 'Helvetica Neue'
    assert styles['ps2544']['font'] == 'Times New Roman'
