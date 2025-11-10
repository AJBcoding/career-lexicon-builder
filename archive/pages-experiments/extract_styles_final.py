#!/usr/bin/env python3
"""
Final clean style extractor for .pages documents
Shows only meaningful paragraph and character styles with their properties.
"""

import struct
from pathlib import Path
from collections import defaultdict


def extract_strings(data, min_length=3):
    """Extract readable strings with positions."""
    strings = []
    current = b''
    start_pos = 0

    for i, byte in enumerate(data):
        if 32 <= byte <= 126:
            if not current:
                start_pos = i
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                try:
                    strings.append({
                        'text': current.decode('ascii'),
                        'offset': start_pos
                    })
                except:
                    pass
            current = b''

    return strings


def find_colors_near(data, offset, window=250):
    """Find RGB colors near offset."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)

    colors = []

    # Look for normalized RGB floats (0.0-1.0)
    for i in range(start, end - 11):
        try:
            r = struct.unpack('<f', data[i:i+4])[0]
            g = struct.unpack('<f', data[i+4:i+8])[0]
            b = struct.unpack('<f', data[i+8:i+12])[0]

            if 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1:
                # Filter out grays unless they're pure black/white
                is_gray = abs(r - g) < 0.05 and abs(g - b) < 0.05
                if not is_gray or r < 0.1 or r > 0.9:
                    colors.append({
                        'r': int(r * 255),
                        'g': int(g * 255),
                        'b': int(b * 255),
                        'hex': f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}",
                        'distance': abs(i - offset)
                    })
        except:
            pass

    # Remove duplicates
    seen = set()
    unique = []
    for c in colors:
        key = (c['r'], c['g'], c['b'])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    unique.sort(key=lambda x: x['distance'])
    return unique[:2]  # Top 2


def find_floats_near(data, offset, window=250):
    """Find float values near offset (spacing, indents, sizes)."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)

    floats = []

    for i in range(start, end - 3):
        try:
            val = struct.unpack('<f', data[i:i+4])[0]
            # Reasonable range for typography values
            if 0.5 <= val <= 150:
                floats.append({
                    'value': val,
                    'distance': abs(i - offset)
                })
        except:
            pass

    # Deduplicate similar values
    unique = []
    for f in floats:
        if not any(abs(f['value'] - u['value']) < 0.1 for u in unique):
            unique.append(f)

    unique.sort(key=lambda x: x['distance'])
    return unique[:4]  # Top 4


def extract_styles_clean(iwa_path):
    """Extract clean style list with properties."""
    with open(iwa_path, 'rb') as f:
        data = f.read()

    all_strings = extract_strings(data)

    # Find meaningful style names
    styles = {}

    for s in all_strings:
        text = s['text'].strip()

        # Skip too short or too long
        if len(text) < 3 or len(text) > 40:
            continue

        # Check if it's likely a style name
        is_style = False

        # Pattern 1: Known style keywords
        if any(kw in text.lower() for kw in
               ['body', 'title', 'heading', 'caption', 'bold', 'italic',
                'list', 'toc', 'footer', 'header', 'footnote']):
            is_style = True

        # Pattern 2: Hyphenated custom styles (like "full-cv-indent")
        if '-' in text and text.replace('-', '').replace(' ', '').isalnum():
            is_style = True

        # Pattern 3: All caps with spaces (like "BOLD TITLES GREEN")
        if text.isupper() and ' ' in text and len(text.split()) <= 4:
            is_style = True

        # Pattern 4: Title case multi-word (like "Free Form", "Numbered List")
        words = text.split()
        if len(words) >= 2 and all(w[0].isupper() for w in words if w):
            is_style = True

        if is_style:
            # Skip if contains weird characters
            if any(c in text for c in ['$', '(', '{', '@', '#', '!', '?', '*']):
                continue

            # Get properties
            colors = find_colors_near(data, s['offset'])
            floats = find_floats_near(data, s['offset'])

            styles[text] = {
                'colors': colors,
                'values': floats
            }

    return styles


def print_styles(title, styles):
    """Print styles in a clean format."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}\n")

    if not styles:
        print("  No styles found")
        return

    for name in sorted(styles.keys()):
        props = styles[name]
        print(f"📐 {name}")

        if props['colors']:
            print(f"   Colors:")
            for c in props['colors']:
                print(f"      • {c['hex'].upper()} - RGB({c['r']}, {c['g']}, {c['b']})")

        if props['values']:
            print(f"   Numeric Values (size/spacing/indent):")
            for v in props['values']:
                print(f"      • {v['value']:.1f} pt")

        print()


def main():
    cv_path = Path("/tmp/pages_cv/Index/DocumentStylesheet.iwa")
    cao_path = Path("/tmp/pages_cao/Index/DocumentStylesheet.iwa")

    if cv_path.exists():
        print("\n" + "█"*80)
        print("DOCUMENT: AJB CV 2024.pages")
        print("█"*80)
        styles = extract_styles_clean(cv_path)
        print_styles("Paragraph & Character Styles", styles)

    if cao_path.exists():
        print("\n\n" + "█"*80)
        print("DOCUMENT: 2025-11-09 - ucla cao byrnes, Anthony.pages")
        print("█"*80)
        styles = extract_styles_clean(cao_path)
        print_styles("Paragraph & Character Styles", styles)


if __name__ == "__main__":
    main()
