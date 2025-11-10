#!/usr/bin/env python3
"""
Comprehensive style extractor for .pages DocumentStylesheet.iwa
Extracts custom styles, colors, spacing, and all formatting details.
"""

import struct
from pathlib import Path
from collections import defaultdict


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


def extract_all_strings(data, min_length=2):
    """Extract ALL strings with their byte positions."""
    strings_with_context = []
    current = b''
    start_offset = 0

    for i, byte in enumerate(data):
        # Accept printable ASCII plus some extended chars
        if 32 <= byte <= 126:  # Printable ASCII
            if not current:
                start_offset = i
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                try:
                    text = current.decode('ascii')
                    # Store the string
                    strings_with_context.append({
                        'text': text,
                        'offset': start_offset,
                        'end': i,
                        'length': len(current)
                    })
                except:
                    pass
            current = b''

    # Don't forget last string
    if len(current) >= min_length:
        try:
            text = current.decode('ascii')
            strings_with_context.append({
                'text': text,
                'offset': start_offset,
                'end': len(data),
                'length': len(current)
            })
        except:
            pass

    return strings_with_context


def find_floats_near(data, offset, window=250):
    """Find floating point values near an offset (for spacing, indents, sizes)."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)

    floats = []

    # Look for 4-byte floats
    for i in range(start, end - 3):
        try:
            val = struct.unpack('<f', data[i:i+4])[0]
            # Filter for reasonable values (0-200 for spacing/indents in points)
            if 0 <= val <= 200 and not (val > 1000 or val < 0.01):
                floats.append({
                    'value': val,
                    'offset': i,
                    'distance': abs(i - offset)
                })
        except:
            pass

    # Sort by distance from the string
    floats.sort(key=lambda x: x['distance'])
    return floats[:5]  # Return closest 5


def find_rgb_colors_near(data, offset, window=250):
    """Find RGB color values near an offset."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)

    colors = []

    # Look for sequences of 3 floats between 0-1 (normalized RGB)
    for i in range(start, end - 11):
        try:
            r = struct.unpack('<f', data[i:i+4])[0]
            g = struct.unpack('<f', data[i+4:i+8])[0]
            b = struct.unpack('<f', data[i+8:i+12])[0]

            if (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1):
                colors.append({
                    'r': int(r * 255),
                    'g': int(g * 255),
                    'b': int(b * 255),
                    'r_float': r,
                    'g_float': g,
                    'b_float': b,
                    'offset': i,
                    'distance': abs(i - offset)
                })
        except:
            pass

    # Also look for 8-bit RGB values (0-255)
    for i in range(start, end - 2):
        r, g, b = data[i], data[i+1], data[i+2]
        # Only accept if values look like real colors
        if not (r == g == b == 0) and not (r == g == b == 255):
            colors.append({
                'r': r,
                'g': g,
                'b': b,
                'offset': i,
                'distance': abs(i - offset)
            })

    # Remove duplicates and sort by distance
    seen = set()
    unique_colors = []
    for c in colors:
        key = (c['r'], c['g'], c['b'])
        if key not in seen:
            seen.add(key)
            unique_colors.append(c)

    unique_colors.sort(key=lambda x: x['distance'])
    return unique_colors[:3]  # Return closest 3


def analyze_comprehensive(iwa_path):
    """Comprehensive analysis of DocumentStylesheet.iwa."""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE STYLE ANALYSIS: {iwa_path.name}")
    print(f"{'='*80}\n")

    with open(iwa_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data):,} bytes\n")

    # Extract ALL strings
    all_strings = extract_all_strings(data, min_length=2)
    print(f"Total strings found: {len(all_strings)}")

    # Find potential style names - be more permissive
    # Look for capitalized strings, hyphenated names, etc.
    potential_styles = []

    for s in all_strings:
        text = s['text'].strip()

        # Skip very short strings
        if len(text) < 3:
            continue

        # Skip strings with lots of punctuation/numbers
        alpha_ratio = sum(c.isalpha() or c in ' -_' for c in text) / len(text)
        if alpha_ratio < 0.6:
            continue

        # Look for likely style names
        is_potential_style = False

        # Pattern 1: Starts with capital or contains style keywords
        if text[0].isupper() or any(kw in text.lower() for kw in
            ['style', 'heading', 'body', 'title', 'caption', 'list',
             'indent', 'bold', 'italic', 'green', 'red', 'blue']):
            is_potential_style = True

        # Pattern 2: Contains hyphens (like "full-cv-indent")
        if '-' in text and text[0].isalpha():
            is_potential_style = True

        # Pattern 3: All caps (like "BOLD TITLES GREEN")
        if text.isupper() and len(text) > 4:
            is_potential_style = True

        if is_potential_style:
            # Find associated properties
            floats = find_floats_near(data, s['offset'], window=150)
            colors = find_rgb_colors_near(data, s['offset'], window=150)

            potential_styles.append({
                'name': text,
                'offset': s['offset'],
                'floats': floats,
                'colors': colors
            })

    # Deduplicate by name
    seen_names = set()
    unique_styles = []
    for style in potential_styles:
        if style['name'] not in seen_names:
            seen_names.add(style['name'])
            unique_styles.append(style)

    # Sort by name
    unique_styles.sort(key=lambda x: x['name'])

    print(f"\n{'='*80}")
    print(f"ALL POTENTIAL STYLES FOUND: {len(unique_styles)}")
    print(f"{'='*80}\n")

    for style in unique_styles:
        print(f"📝 Style: {style['name']}")

        if style['floats']:
            print(f"   Numeric values (spacing/size/indent):")
            for f in style['floats'][:3]:
                print(f"      • {f['value']:.2f} pt (distance: {f['distance']} bytes)")

        if style['colors']:
            print(f"   Colors:")
            for c in style['colors']:
                print(f"      • RGB({c['r']}, {c['g']}, {c['b']}) = #{c['r']:02x}{c['g']:02x}{c['b']:02x}")

        print()

    # Also show ALL unique strings for reference
    print(f"\n{'='*80}")
    print(f"ALL UNIQUE STRINGS (for verification):")
    print(f"{'='*80}\n")

    all_unique = sorted(set(s['text'].strip() for s in all_strings if len(s['text'].strip()) >= 4))

    # Filter for likely style-related
    likely_relevant = [s for s in all_unique if
        any(kw in s.lower() for kw in
            ['style', 'heading', 'body', 'title', 'caption', 'list',
             'indent', 'bold', 'italic', 'form', 'toc', 'cv', 'green',
             'red', 'blue', 'color', 'font', 'paragraph', 'character'])]

    for i, s in enumerate(likely_relevant):
        print(f"  {i+1:3d}. {s}")
        if i >= 100:  # Limit output
            print(f"  ... and {len(likely_relevant) - 100} more")
            break


def main():
    # Analyze CV document
    cv_path = Path("/tmp/pages_cv/Index/DocumentStylesheet.iwa")
    if cv_path.exists():
        print("\n" + "="*80)
        print("ANALYZING: AJB CV 2024.pages")
        print("="*80)
        analyze_comprehensive(cv_path)

    # Analyze UCLA CAO document
    cao_path = Path("/tmp/pages_cao/Index/DocumentStylesheet.iwa")
    if cao_path.exists():
        print("\n\n" + "="*80)
        print("ANALYZING: 2025-11-09 - ucla cao byrnes, Anthony.pages")
        print("="*80)
        analyze_comprehensive(cao_path)


if __name__ == "__main__":
    main()
