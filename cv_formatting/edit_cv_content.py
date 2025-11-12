#!/usr/bin/env python3
"""
Edit CV Content JSON Helper

This script helps you find and update specific content in the CV JSON mapping
without breaking the formatting or semantic structure.

Usage:
    # Search for content
    python3 cv_formatting/edit_cv_content.py search "Strategic Planning"

    # Update specific entry by index
    python3 cv_formatting/edit_cv_content.py update 15 "New text here"

    # Show entry at index
    python3 cv_formatting/edit_cv_content.py show 15

Created: November 11, 2025
"""

import json
import sys


def load_json(path='/tmp/ucla-cv-v3-semantic-mapping.json'):
    """Load the CV content JSON."""
    with open(path) as f:
        return json.load(f)


def save_json(content, path='/tmp/ucla-cv-v3-semantic-mapping.json'):
    """Save the CV content JSON."""
    with open(path, 'w') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved to {path}")


def search_content(content, search_term):
    """Search for entries containing the search term."""
    print(f"=== SEARCHING FOR: '{search_term}' ===\n")

    matches = []
    for i, item in enumerate(content):
        text = item.get('text', '')
        if search_term.lower() in text.lower():
            matches.append((i, item))

    if not matches:
        print("No matches found.")
        return

    print(f"Found {len(matches)} match(es):\n")
    for i, (index, item) in enumerate(matches, 1):
        text = item.get('text', '')
        style = item.get('style', 'Unknown')

        # Truncate long text
        display_text = text[:100] + '...' if len(text) > 100 else text

        print(f"{i}. Index {index} [{style}]")
        print(f"   Text: {display_text}")
        print()


def show_entry(content, index):
    """Show full details of an entry."""
    try:
        index = int(index)
        if index < 0 or index >= len(content):
            print(f"Error: Index {index} out of range (0-{len(content)-1})")
            return

        item = content[index]
        print(f"=== ENTRY {index} ===\n")
        print(json.dumps(item, indent=2, ensure_ascii=False))

    except ValueError:
        print("Error: Index must be a number")


def update_entry(content, index, new_text):
    """Update the text of an entry."""
    try:
        index = int(index)
        if index < 0 or index >= len(content):
            print(f"Error: Index {index} out of range (0-{len(content)-1})")
            return None

        old_text = content[index].get('text', '')
        style = content[index].get('style', 'Unknown')

        print(f"=== UPDATING ENTRY {index} [{style}] ===\n")
        print(f"Old text: {old_text[:100]}...")
        print(f"\nNew text: {new_text[:100]}...")
        print()

        # Update the text
        content[index]['text'] = new_text

        return content

    except ValueError:
        print("Error: Index must be a number")
        return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    content = load_json()

    if command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python3 edit_cv_content.py search 'search term'")
            sys.exit(1)
        search_term = sys.argv[2]
        search_content(content, search_term)

    elif command == 'show':
        if len(sys.argv) < 3:
            print("Usage: python3 edit_cv_content.py show INDEX")
            sys.exit(1)
        index = sys.argv[2]
        show_entry(content, index)

    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: python3 edit_cv_content.py update INDEX 'new text'")
            sys.exit(1)
        index = sys.argv[2]
        new_text = sys.argv[3]
        updated_content = update_entry(content, index, new_text)

        if updated_content:
            save_json(updated_content)
            print("\n✓ Entry updated successfully")
            print("\nTo regenerate the CV with this change:")
            print("python3 -c \"")
            print("from cv_formatting.style_applicator import StyleApplicator")
            print("from cv_formatting.metadata_inference import MetadataHelper")
            print("import json")
            print()
            print("with open('/tmp/ucla-cv-v3-semantic-mapping.json') as f:")
            print("    content = json.load(f)")
            print()
            print("helper = MetadataHelper()")
            print("metadata = helper.infer_cv_metadata(' '.join([i.get('text', '') for i in content]))")
            print()
            print("applicator = StyleApplicator('cv_formatting/templates/career-documents-template.docx')")
            print("applicator.apply_styles(content, 'output.docx', 'cv', metadata)")
            print("\"")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
