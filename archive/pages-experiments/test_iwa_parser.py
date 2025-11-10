#!/usr/bin/env python3
"""
Test script to parse .iwa files from Apple Pages documents
and look for style information.
"""

import snappy
import struct
from pathlib import Path


def parse_iwa_file(iwa_path):
    """
    Parse an IWA file and extract the protobuf messages.

    IWA format: varint (length) + ArchiveInfo message + Payloads
    The file is Snappy compressed.
    """
    print(f"\n{'='*60}")
    print(f"Parsing: {iwa_path.name}")
    print(f"Size: {iwa_path.stat().st_size} bytes")
    print(f"{'='*60}\n")

    with open(iwa_path, 'rb') as f:
        compressed_data = f.read()

    # IWA files use Snappy framing format but with modifications
    # Try multiple decompression approaches
    decompressed = None

    # Approach 1: Try raw Snappy decompression
    try:
        decompressed = snappy.decompress(compressed_data)
        print(f"✓ Raw decompression: {len(compressed_data)} -> {len(decompressed)} bytes\n")
    except Exception as e:
        print(f"  Raw decompression failed: {e}")

    # Approach 2: Try stream decompression
    if decompressed is None:
        try:
            decompressed = snappy.stream_decompress(compressed_data)
            print(f"✓ Stream decompression: {len(compressed_data)} -> {len(decompressed)} bytes\n")
        except Exception as e:
            print(f"  Stream decompression failed: {e}")

    # Approach 3: Try reading the file as chunks
    if decompressed is None:
        print("  Trying chunk-based decompression...")
        chunks = []
        offset = 0
        while offset < len(compressed_data):
            try:
                # Skip potential framing bytes and try to decompress chunks
                for skip in [0, 4, 8, 16]:
                    try:
                        chunk = snappy.decompress(compressed_data[offset + skip:])
                        chunks.append(chunk)
                        print(f"  ✓ Decompressed chunk at offset {offset + skip}")
                        offset = len(compressed_data)  # Done
                        break
                    except:
                        continue
                break
            except:
                offset += 1
                if offset > 100:  # Don't search forever
                    break

        if chunks:
            decompressed = b''.join(chunks)
            print(f"✓ Chunk decompression: {len(decompressed)} bytes\n")

    if decompressed is None:
        print("✗ All decompression methods failed")
        print("  This might require the full IWA framing parser")
        return

    # Look for potential text strings and patterns
    # We'll search for common style-related keywords
    style_keywords = [
        b'style', b'Style', b'STYLE',
        b'paragraph', b'Paragraph',
        b'character', b'Character',
        b'font', b'Font',
        b'Helvetica', b'Times', b'Arial',
        b'bold', b'italic',
        b'Body', b'Heading', b'Title'
    ]

    found_keywords = {}
    for keyword in style_keywords:
        count = decompressed.count(keyword)
        if count > 0:
            found_keywords[keyword.decode('utf-8', errors='ignore')] = count

    if found_keywords:
        print("Found style-related keywords:")
        for kw, count in sorted(found_keywords.items(), key=lambda x: x[1], reverse=True):
            print(f"  {kw}: {count} occurrences")
    else:
        print("No style-related keywords found")

    # Try to extract readable strings
    print("\n" + "-"*60)
    print("Sample readable strings (3+ chars):")
    print("-"*60)

    current_string = b''
    readable_strings = []

    for byte in decompressed:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += bytes([byte])
        else:
            if len(current_string) >= 3:
                try:
                    readable_strings.append(current_string.decode('ascii'))
                except:
                    pass
            current_string = b''

    # Show unique strings that might be style names
    unique_strings = list(set(readable_strings))
    style_related = [s for s in unique_strings if any(
        kw.lower() in s.lower()
        for kw in ['style', 'heading', 'body', 'title', 'caption', 'paragraph']
    )]

    if style_related:
        print("\nPotential style names found:")
        for s in sorted(style_related)[:20]:  # Show first 20
            print(f"  • {s}")

    # Show some general strings
    general_strings = [s for s in unique_strings if 10 < len(s) < 50][:15]
    if general_strings:
        print("\nOther interesting strings:")
        for s in sorted(general_strings)[:15]:
            print(f"  • {s}")

    return decompressed


def main():
    index_dir = Path("/tmp/pages_test/Index")

    if not index_dir.exists():
        print(f"Error: {index_dir} not found")
        return

    # Focus on the stylesheet file first
    stylesheet = index_dir / "DocumentStylesheet.iwa"
    if stylesheet.exists():
        parse_iwa_file(stylesheet)

    # Also check Document.iwa
    document = index_dir / "Document.iwa"
    if document.exists():
        parse_iwa_file(document)


if __name__ == "__main__":
    main()
