#!/usr/bin/env python3
"""
Analyze Document.iwa to find how text is mapped to styles.
"""

import struct
from pathlib import Path
from collections import defaultdict


def extract_strings_with_context(data, min_length=3):
    """Extract strings and surrounding bytes for context."""
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
                    # Get 20 bytes before and after for context
                    context_start = max(0, start_pos - 20)
                    context_end = min(len(data), i + 20)

                    strings.append({
                        'text': current.decode('ascii'),
                        'offset': start_pos,
                        'context_before': data[context_start:start_pos],
                        'context_after': data[i:context_end]
                    })
                except:
                    pass
            current = b''

    return strings


def read_varint(data, offset):
    """Read protobuf varint."""
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


def analyze_document_structure(doc_path):
    """Analyze Document.iwa to understand text and style relationship."""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {doc_path.name}")
    print(f"{'='*80}\n")

    with open(doc_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data):,} bytes\n")

    # Extract all strings
    all_strings = extract_strings_with_context(data, min_length=4)

    print(f"Total strings found: {len(all_strings)}\n")

    # Look for actual document text (longer strings that look like content)
    content_strings = []
    for s in all_strings:
        text = s['text']
        # Filter for likely content (not codes/identifiers)
        if len(text) > 15 and ' ' in text:
            content_strings.append(s)

    print(f"{'='*80}")
    print(f"DOCUMENT CONTENT FOUND ({len(content_strings)} pieces):")
    print(f"{'='*80}\n")

    for i, s in enumerate(content_strings[:20]):  # Show first 20
        text = s['text'][:100]  # Truncate long text
        print(f"{i+1}. \"{text}{'...' if len(s['text']) > 100 else ''}\"")
        print(f"   Offset: {s['offset']}")

        # Look at bytes immediately before the text
        before = s['context_before'][-10:] if len(s['context_before']) >= 10 else s['context_before']
        print(f"   Bytes before: {' '.join(f'{b:02x}' for b in before)}")

        # Look for potential style IDs (varints)
        # Check if there's a varint in the few bytes before
        for check_offset in range(max(0, s['offset'] - 10), s['offset']):
            try:
                val, _ = read_varint(data, check_offset)
                if val is not None and 0 < val < 10000:  # Reasonable style ID range
                    print(f"   Possible style ID at offset {check_offset}: {val}")
            except:
                pass

        print()

    # Look for known style names in the document
    print(f"\n{'='*80}")
    print(f"STYLE REFERENCES IN DOCUMENT:")
    print(f"{'='*80}\n")

    style_keywords = ['Body', 'Title', 'Bold', 'Heading', 'full-cv',
                     'BOLD TITLES GREEN', 'Free Form', 'TOC']

    for keyword in style_keywords:
        if keyword.encode('ascii') in data:
            offset = data.find(keyword.encode('ascii'))
            print(f"✓ Found '{keyword}' at offset {offset}")

            # Show hex context
            context_start = max(0, offset - 30)
            context_end = min(len(data), offset + len(keyword) + 30)
            context = data[context_start:context_end]

            print(f"   Hex context:")
            for i in range(0, len(context), 16):
                hex_str = ' '.join(f'{b:02x}' for b in context[i:i+16])
                ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in context[i:i+16])
                print(f"   {context_start+i:08x}  {hex_str:<48}  {ascii_str}")
            print()

    # Look for patterns that might indicate style application
    print(f"\n{'='*80}")
    print(f"ANALYZING TEXT-STYLE PATTERNS:")
    print(f"{'='*80}\n")

    # Find sequences where we have: [numbers] + "text content" + [numbers]
    # This might indicate: style_id + text + formatting_data

    for s in content_strings[:5]:  # Analyze first 5 content pieces
        print(f"\nText: \"{s['text'][:60]}...\"")
        print(f"Offset: {s['offset']}")

        # Look at the structure around this text
        start = max(0, s['offset'] - 50)
        end = min(len(data), s['offset'] + len(s['text']) + 50)

        # Try to find varints in the region
        print("  Varints in nearby region:")
        for check_pos in range(start, s['offset'], 1):
            try:
                val, next_pos = read_varint(data, check_pos)
                if val is not None and 1 < val < 1000:
                    distance = s['offset'] - check_pos
                    print(f"    Value {val} at distance -{distance} bytes")
            except:
                pass


def main():
    # Analyze UCLA CAO document (smaller, easier to start with)
    cao_path = Path("/tmp/pages_cao/Index/Document.iwa")
    if cao_path.exists():
        analyze_document_structure(cao_path)

    # Then CV document
    print("\n\n" + "="*80)
    print("NOW ANALYZING CV DOCUMENT")
    print("="*80)

    cv_path = Path("/tmp/pages_cv/Index/Document.iwa")
    if cv_path.exists():
        analyze_document_structure(cv_path)


if __name__ == "__main__":
    main()
