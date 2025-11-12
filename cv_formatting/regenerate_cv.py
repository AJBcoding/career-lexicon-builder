#!/usr/bin/env python3
"""
Regenerate CV from JSON

Quick script to regenerate the CV after editing the JSON content mapping.

Usage:
    python3 cv_formatting/regenerate_cv.py
    python3 cv_formatting/regenerate_cv.py --output custom-name.docx

This script:
1. Loads the JSON content mapping from /tmp/ucla-cv-v3-semantic-mapping.json
2. Infers metadata (name, page headers)
3. Applies styles using the template
4. Outputs to CV Draft folder

Created: November 11, 2025
"""

from cv_formatting.style_applicator import StyleApplicator
from cv_formatting.metadata_inference import MetadataHelper
import json
import shutil
import argparse
from datetime import datetime


def regenerate_cv(json_path='/tmp/ucla-cv-v3-semantic-mapping.json', output_name=None):
    """Regenerate CV from JSON mapping."""

    print("=== REGENERATING CV FROM JSON ===\n")

    # Load JSON
    print(f"1. Loading JSON from {json_path}...")
    with open(json_path) as f:
        content = json.load(f)
    print(f"   ✓ Loaded {len(content)} content items\n")

    # Generate metadata
    print("2. Inferring metadata...")
    helper = MetadataHelper()
    cv_text = ' '.join([item.get('text', '') for item in content])
    metadata = helper.infer_cv_metadata(cv_text)
    print(f"   ✓ Metadata generated\n")

    # Apply styles
    print("3. Applying styles with template...")
    applicator = StyleApplicator('cv_formatting/templates/career-documents-template.docx')

    # Generate output filename
    if not output_name:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        output_name = f"UCLA-CAO-Resume-{timestamp}.docx"

    temp_output = f'/tmp/{output_name}'

    applicator.apply_styles(
        content_mapping=content,
        output_path=temp_output,
        document_type='cv',
        metadata=metadata
    )
    print(f"   ✓ Created: {temp_output}\n")

    # Copy to CV Draft folder
    cv_draft_folder = 'career-applications/2025-10-22-associate-dean-cao-ucla/CV Draft'
    final_output = f'{cv_draft_folder}/{output_name}'
    shutil.copy(temp_output, final_output)
    print(f"   ✓ Copied to: {final_output}\n")

    print("=== COMPLETE ===")
    print(f"\n✓ CV regenerated successfully: {output_name}")
    print(f"\nTo convert to PDF:")
    print(f"soffice --headless --convert-to pdf --outdir '{cv_draft_folder}' '{final_output}'")

    return final_output


def main():
    parser = argparse.ArgumentParser(description='Regenerate CV from JSON mapping')
    parser.add_argument('--json', default='/tmp/ucla-cv-v3-semantic-mapping.json',
                      help='Path to JSON content mapping (default: /tmp/ucla-cv-v3-semantic-mapping.json)')
    parser.add_argument('--output', help='Output filename (default: UCLA-CAO-Resume-TIMESTAMP.docx)')

    args = parser.parse_args()

    regenerate_cv(json_path=args.json, output_name=args.output)


if __name__ == '__main__':
    main()
