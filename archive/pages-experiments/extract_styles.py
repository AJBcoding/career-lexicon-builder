#!/usr/bin/env python3
"""
Extract style definitions from .pages DocumentStylesheet.iwa
"""

import struct
from pathlib import Path
from collections import defaultdict


def extract_strings_with_context(data, min_length=3):
    """Extract strings and their byte offsets for context analysis."""
    strings_with_offset = []
    current = b''
    start_offset = 0

    for i, byte in enumerate(data):
        if 32 <= byte <= 126:  # Printable ASCII
            if not current:
                start_offset = i
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                try:
                    strings_with_offset.append({
                        'text': current.decode('ascii'),
                        'offset': start_offset,
                        'length': len(current)
                    })
                except:
                    pass
            current = b''

    return strings_with_offset


def find_numeric_properties(data, string_offset, window=20):
    """Look for numeric values near a string (potential font sizes, colors, etc)."""
    properties = {}

    # Look before and after the string
    start = max(0, string_offset - window)
    end = min(len(data), string_offset + window)

    context = data[start:end]

    # Look for small integers (font sizes are typically 9-72)
    for i in range(len(context) - 1):
        byte = context[i]
        if 8 <= byte <= 72 and context[i+1] < 10:  # Likely font size
            properties['possible_size'] = byte

    return properties


def analyze_style_patterns(iwa_path):
    """Analyze DocumentStylesheet.iwa for detailed style patterns."""
    print(f"\n{'='*70}")
    print(f"DETAILED STYLE ANALYSIS: {iwa_path.name}")
    print(f"{'='*70}\n")

    with open(iwa_path, 'rb') as f:
        data = f.read()

    # Extract all strings with their positions
    strings = extract_strings_with_context(data)

    # Group style-related strings
    style_names = []
    font_names = []
    style_keywords = ['Body', 'Title', 'Heading', 'Caption', 'TOC', 'List',
                     'Free Form', 'Footer', 'Header', 'Footnote']

    for s in strings:
        text = s['text'].strip()

        # Look for potential style names (clean strings matching keywords)
        for keyword in style_keywords:
            if keyword.lower() == text.lower() or text.startswith(keyword):
                # Get context
                props = find_numeric_properties(data, s['offset'])
                style_names.append({
                    'name': text,
                    'offset': s['offset'],
                    **props
                })

        # Font names
        if any(font in text for font in ['Helvetica', 'Times', 'Arial', 'Courier',
                                          'Georgia', 'Verdana', 'Palatino', 'Gotham']):
            font_names.append({
                'font': text,
                'offset': s['offset']
            })

    # Print findings
    print(f"{'='*70}")
    print(f"PARAGRAPH & CHARACTER STYLES FOUND:")
    print(f"{'='*70}\n")

    # Deduplicate style names
    seen = set()
    unique_styles = []
    for style in style_names:
        if style['name'] not in seen:
            seen.add(style['name'])
            unique_styles.append(style)

    for style in sorted(unique_styles, key=lambda x: x['name']):
        print(f"Style: {style['name']}")
        if 'possible_size' in style:
            print(f"  └─ Possible font size: {style['possible_size']}pt")
        print()

    if font_names:
        print(f"{'='*70}")
        print(f"FONTS REFERENCED:")
        print(f"{'='*70}\n")
        seen_fonts = set()
        for font in font_names:
            if font['font'] not in seen_fonts:
                seen_fonts.add(font['font'])
                print(f"  • {font['font']}")

    # Look for all unique clean strings that might be style names
    print(f"\n{'='*70}")
    print(f"ALL POTENTIAL STYLE/FORMAT NAMES:")
    print(f"{'='*70}\n")

    potential_names = []
    for s in strings:
        text = s['text'].strip()
        # Filter for likely style names: capitalized, short, no special chars
        if (3 < len(text) < 30 and
            text[0].isupper() and
            not any(c in text for c in ['$', '(', '{', '[', '@', '#']) and
            any(kw.lower() in text.lower() for kw in
                ['body', 'title', 'head', 'caption', 'toc', 'list', 'form',
                 'foot', 'note', 'text', 'bold', 'italic'])):
            potential_names.append(text)

    for name in sorted(set(potential_names)):
        print(f"  • {name}")


def main():
    index_dir = Path("/tmp/pages_test/Index")
    stylesheet = index_dir / "DocumentStylesheet.iwa"

    if stylesheet.exists():
        analyze_style_patterns(stylesheet)
    else:
        print(f"Error: {stylesheet} not found")


if __name__ == "__main__":
    main()
