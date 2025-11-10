#!/usr/bin/env python3
"""
Map document text to applied styles by parsing Document.iwa.
"""

import struct
from pathlib import Path
from collections import defaultdict
import re


def read_varint(data, offset):
    """Read a protobuf varint."""
    result = 0
    shift = 0
    pos = offset

    while pos < len(data):
        if pos >= len(data):
            return None, pos
        byte = data[pos]
        result |= (byte & 0x7F) << shift
        pos += 1
        if (byte & 0x80) == 0:
            break
        shift += 7

    return result, pos


def extract_all_strings(data):
    """Extract all ASCII strings with positions."""
    strings = []
    current = b''
    start_pos = 0

    for i, byte in enumerate(data):
        if 32 <= byte <= 126:
            if not current:
                start_pos = i
            current += bytes([byte])
        else:
            if len(current) >= 3:
                try:
                    strings.append({
                        'text': current.decode('ascii'),
                        'offset': start_pos,
                        'length': len(current)
                    })
                except:
                    pass
            current = b''

    return strings


def find_style_references(data):
    """Find all style name references in document."""
    style_refs = []

    # Known style names to search for
    style_names = [
        'Body', 'Title', 'Bold', 'Boldf', 'Heading', 'Free Form',
        'TOC', 'Footnote Text', 'Numbered List', 'full-cv-in',
        'BOLD TITLES GREEN', 'Green Paper', 'Gray Paper'
    ]

    for style_name in style_names:
        search_bytes = style_name.encode('ascii')
        offset = 0

        while True:
            offset = data.find(search_bytes, offset)
            if offset == -1:
                break

            # Look at bytes before to understand context
            context_start = max(0, offset - 30)
            context = data[context_start:offset + len(search_bytes) + 10]

            style_refs.append({
                'style': style_name,
                'offset': offset,
                'context': context
            })

            offset += 1

    return sorted(style_refs, key=lambda x: x['offset'])


def find_text_runs(data):
    """Find text content that looks like document body text."""
    all_strings = extract_all_strings(data)

    text_runs = []

    for s in all_strings:
        text = s['text']

        # Filter for likely body text:
        # - Longer than 15 chars
        # - Contains spaces
        # - Not all caps (unless reasonably long)
        # - Not mostly punctuation
        if len(text) < 15:
            continue

        if ' ' not in text:
            continue

        # Count alphanumeric
        alnum_count = sum(c.isalnum() or c.isspace() for c in text)
        if alnum_count / len(text) < 0.7:
            continue

        text_runs.append(s)

    return text_runs


def map_text_to_styles(doc_path):
    """Map text content to styles based on proximity."""
    print(f"\n{'='*80}")
    print(f"MAPPING TEXT TO STYLES: {doc_path.name}")
    print(f"{'='*80}\n")

    with open(doc_path, 'rb') as f:
        data = f.read()

    # Find all style references
    style_refs = find_style_references(data)
    print(f"Found {len(style_refs)} style references\n")

    # Find all text runs
    text_runs = find_text_runs(data)
    print(f"Found {len(text_runs)} text runs\n")

    # Map text to nearest preceding style
    print(f"{'='*80}")
    print(f"TEXT → STYLE MAPPING:")
    print(f"{'='*80}\n")

    for i, text_run in enumerate(text_runs[:30], 1):  # Show first 30
        text = text_run['text']
        offset = text_run['offset']

        # Find the nearest style reference BEFORE this text
        nearest_style = None
        min_distance = float('inf')

        for style_ref in style_refs:
            if style_ref['offset'] < offset:
                distance = offset - style_ref['offset']
                if distance < min_distance:
                    min_distance = distance
                    nearest_style = style_ref['style']

        # Also check for style references AFTER (sometimes style comes after)
        following_style = None
        min_forward_distance = float('inf')

        for style_ref in style_refs:
            if style_ref['offset'] > offset:
                distance = style_ref['offset'] - offset
                if distance < min_forward_distance and distance < 200:
                    min_forward_distance = distance
                    following_style = style_ref['style']

        # Truncate long text
        display_text = text[:70] + '...' if len(text) > 70 else text

        print(f"{i}. \"{display_text}\"")
        if nearest_style:
            print(f"   → Style (before, -{min_distance:,} bytes): {nearest_style}")
        if following_style and following_style != nearest_style:
            print(f"   → Style (after, +{min_forward_distance:,} bytes): {following_style}")
        if not nearest_style and not following_style:
            print(f"   → No style found nearby")
        print()

    # Show style usage summary
    print(f"\n{'='*80}")
    print(f"STYLE USAGE SUMMARY:")
    print(f"{'='*80}\n")

    for style_ref in style_refs:
        # Count how many text runs come after this style (within 5000 bytes)
        text_count = sum(1 for t in text_runs
                        if style_ref['offset'] < t['offset'] < style_ref['offset'] + 5000)

        print(f"• {style_ref['style']:<20} at offset {style_ref['offset']:>6,} → {text_count} text runs nearby")


def analyze_style_markers(doc_path):
    """Look for pattern markers that indicate style changes."""
    print(f"\n\n{'='*80}")
    print(f"ANALYZING STYLE CHANGE MARKERS:")
    print(f"{'='*80}\n")

    with open(doc_path, 'rb') as f:
        data = f.read()

    # Find transitions between different styles
    style_refs = find_style_references(data)

    for i in range(len(style_refs) - 1):
        current = style_refs[i]
        next_style = style_refs[i + 1]

        # Look at the bytes between style references
        gap = next_style['offset'] - current['offset']
        if gap < 1000:  # Only look at close transitions
            between = data[current['offset']:next_style['offset']]

            # Look for text content between styles
            text_matches = re.findall(rb'[ -~]{15,}', between)

            if text_matches:
                print(f"\nTransition: {current['style']} → {next_style['style']}")
                print(f"Gap: {gap} bytes")
                for match in text_matches[:2]:  # Show first 2
                    try:
                        decoded = match.decode('ascii')
                        print(f"  Text: \"{decoded[:60]}...\"")
                    except:
                        pass


def main():
    # Analyze smaller document first
    cao_path = Path("/tmp/pages_cao/Index/Document.iwa")
    if cao_path.exists():
        map_text_to_styles(cao_path)
        analyze_style_markers(cao_path)

    # Then CV
    print("\n\n" + "█"*80)
    print("CV DOCUMENT")
    print("█"*80)

    cv_path = Path("/tmp/pages_cv/Index/Document.iwa")
    if cv_path.exists():
        map_text_to_styles(cv_path)
        analyze_style_markers(cv_path)


if __name__ == "__main__":
    main()
