"""Parse iwork-converter HTML/CSS output to extract style definitions."""
import re
from typing import Dict, Any


class StyleParser:
    """Parser for iwork-converter CSS output."""

    def parse_css(self, css_text: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse CSS text and extract style definitions.

        Args:
            css_text: CSS content from iwork-converter HTML

        Returns:
            Dict mapping style class names to property dicts
        """
        if not css_text:
            return {}

        styles = {}

        # Match CSS class definitions: .classname { properties }
        pattern = r'\.([a-z0-9]+)\s*\{([^}]+)\}'

        for match in re.finditer(pattern, css_text, re.IGNORECASE):
            class_name = match.group(1)
            properties_text = match.group(2)

            # Parse properties
            props = self._parse_properties(properties_text)

            if props:
                styles[class_name] = props

        return styles

    def _parse_properties(self, props_text: str) -> Dict[str, Any]:
        """Parse CSS properties into structured dict."""
        props = {}

        # Font weight
        if 'font-weight: bold' in props_text:
            props['bold'] = True

        # Font style
        if 'font-style: italic' in props_text:
            props['italic'] = True

        # Font size
        size_match = re.search(r'font-size.*?(\d+(?:\.\d+)?)pt', props_text)
        if size_match:
            props['size'] = float(size_match.group(1))

        # Font family
        font_match = re.search(r"font-family:\s*['\"]([^'\"]+)['\"]", props_text)
        if font_match:
            props['font'] = font_match.group(1)

        # Color
        color_match = re.search(r'color:\s*(rgba\([^)]+\))', props_text)
        if color_match:
            props['color'] = color_match.group(1)

        # Margins/indents
        margin_left = re.search(r'margin-left:\s*(\d+\.\d+)pt', props_text)
        if margin_left:
            props['margin_left'] = float(margin_left.group(1))

        text_indent = re.search(r'text-indent:\s*(-?\d+\.\d+)pt', props_text)
        if text_indent:
            props['text_indent'] = float(text_indent.group(1))

        # List style
        if 'list-style-type: disc' in props_text:
            props['list_style'] = 'disc'

        return props
