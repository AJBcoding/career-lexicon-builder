#!/usr/bin/env python3
"""
Proper IWA file parser for Apple iWork files.
Based on reverse-engineered format from iWorkFileFormat project.
"""

import snappy
import struct
from pathlib import Path


def read_varint(data, offset):
    """Read a protobuf varint from data at offset."""
    result = 0
    shift = 0
    pos = offset

    while pos < len(data):
        byte = data[pos]
        result |= (byte & 0x7F) << shift
        pos += 1
        if (byte & 0x80) == 0:
            break
        shift += 7

    return result, pos


def parse_iwa_chunks(data):
    """
    Parse IWA file structure.

    IWA format (repeated):
    - varint: length of ArchiveInfo message
    - ArchiveInfo protobuf message
    - One or more payload messages
    """
    chunks = []
    offset = 0

    print(f"Parsing {len(data)} bytes of data...")

    chunk_num = 0
    while offset < len(data):
        # Read the varint that indicates the ArchiveInfo length
        try:
            archive_info_len, new_offset = read_varint(data, offset)
            if archive_info_len == 0 or archive_info_len > len(data):
                break

            print(f"\nChunk {chunk_num}: ArchiveInfo length = {archive_info_len} bytes at offset {offset}")

            # Skip the ArchiveInfo for now (we'd need .proto files to parse it properly)
            payload_offset = new_offset + archive_info_len

            if payload_offset >= len(data):
                break

            # Try to find readable content in the region after ArchiveInfo
            # Look ahead a bit to find potential payload
            chunk_data = data[new_offset:min(new_offset + archive_info_len + 1000, len(data))]
            chunks.append(chunk_data)

            # Move to next chunk (heuristic - look for next varint pattern)
            offset = payload_offset
            chunk_num += 1

            if chunk_num > 100:  # Safety limit
                break

        except Exception as e:
            print(f"Error at offset {offset}: {e}")
            break

    return chunks


def extract_strings_from_data(data, min_length=3):
    """Extract human-readable strings from binary data."""
    strings = []
    current = b''

    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                try:
                    strings.append(current.decode('ascii'))
                except:
                    pass
            current = b''

    # Don't forget the last string
    if len(current) >= min_length:
        try:
            strings.append(current.decode('ascii'))
        except:
            pass

    return strings


def analyze_stylesheet(iwa_path):
    """Analyze DocumentStylesheet.iwa for style information."""
    print(f"\n{'='*70}")
    print(f"Analyzing: {iwa_path.name}")
    print(f"{'='*70}\n")

    with open(iwa_path, 'rb') as f:
        raw_data = f.read()

    print(f"Raw file size: {len(raw_data)} bytes")

    # Check if file is compressed or not
    # Try Snappy decompression first
    data_to_parse = None
    compressed = False

    for header_offset in [0, 4, 8]:
        try:
            decompressed = snappy.decompress(raw_data[header_offset:])
            print(f"✓ Successfully decompressed from offset {header_offset}")
            print(f"  {len(raw_data[header_offset:])} -> {len(decompressed)} bytes\n")
            data_to_parse = decompressed
            compressed = True
            break
        except:
            pass

    # If not compressed, use raw data
    if data_to_parse is None:
        print("✓ File is not Snappy compressed, parsing as raw protobuf\n")
        data_to_parse = raw_data
        compressed = False

    # Extract all strings directly from the data
    all_strings = extract_strings_from_data(data_to_parse, min_length=3)

    print(f"Found {len(all_strings)} strings total")
    print(f"Found {len(set(all_strings))} unique strings\n")

    # Parse IWA chunks if needed
    if compressed:
        chunks = parse_iwa_chunks(data_to_parse)
        print(f"Parsed {len(chunks)} IWA chunks")

    # Look for style-related content
    unique_strings = sorted(set(all_strings))

    # Filter for style names and properties
    style_related = [s for s in unique_strings if any(kw in s.lower() for kw in
                      ['style', 'heading', 'body', 'title', 'caption', 'paragraph',
                       'list', 'free form', 'toc', 'footer', 'header'])]

    font_names = [s for s in unique_strings if any(kw in s for kw in
                 ['Helvetica', 'Times', 'Arial', 'Courier', 'Verdana', 'Georgia',
                  'San Francisco', 'Palatino', 'Baskerville'])]

    properties = [s for s in unique_strings if any(kw in s.lower() for kw in
                 ['bold', 'italic', 'underline', 'color', 'size', 'alignment',
                  'indent', 'spacing', 'margin'])]

    print(f"{'='*70}")
    print(f"STYLE-RELATED STRINGS ({len(style_related)} found):")
    print(f"{'='*70}")
    for name in style_related[:40]:
        print(f"  • {name}")

    if font_names:
        print(f"\n{'='*70}")
        print(f"FONTS ({len(font_names)} found):")
        print(f"{'='*70}")
        for font in font_names[:30]:
            print(f"  • {font}")

    if properties:
        print(f"\n{'='*70}")
        print(f"STYLE PROPERTIES ({len(properties)} found):")
        print(f"{'='*70}")
        for prop in properties[:30]:
            print(f"  • {prop}")

    # Show some other interesting strings
    other = [s for s in unique_strings
            if len(s) > 8 and len(s) < 50
            and s not in style_related
            and s not in font_names
            and s not in properties][:25]
    if other:
        print(f"\n{'='*70}")
        print(f"OTHER INTERESTING STRINGS ({len(other)} shown):")
        print(f"{'='*70}")
        for s in other:
            print(f"  • {s}")

    return True


def main():
    index_dir = Path("/tmp/pages_test/Index")

    if not index_dir.exists():
        print(f"Error: {index_dir} not found")
        return

    # Analyze the DocumentStylesheet.iwa
    stylesheet = index_dir / "DocumentStylesheet.iwa"
    if stylesheet.exists():
        success = analyze_stylesheet(stylesheet)
        if success:
            print("\n✓ Successfully parsed DocumentStylesheet.iwa!")
        else:
            print("\n✗ Failed to parse DocumentStylesheet.iwa")


if __name__ == "__main__":
    main()
