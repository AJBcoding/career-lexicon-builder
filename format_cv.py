#!/usr/bin/env python3
"""
Format CV content using template styles.

Usage:
    python format_cv.py input.json output.docx

Input format: JSON with content mapping
"""
import sys
import json
from pathlib import Path
from cv_formatting.style_applicator import StyleApplicator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Format CV from content mapping."""
    if len(sys.argv) != 3:
        print("Usage: python format_cv.py <input.json> <output.docx>")
        print("\nInput JSON format:")
        print('[')
        print('  {"text": "EDUCATION", "style": "Section Header", "type": "paragraph"},')
        print('  {"text": "Body text", "style": "Body Text", "type": "paragraph"}')
        print(']')
        return 1

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return 1

    # Load content mapping
    try:
        with open(input_file) as f:
            content_mapping = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse input JSON: {e}")
        return 1

    # Get template
    template_path = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"

    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        logger.error("Run generate_cv_template.py first")
        return 1

    # Apply styles
    logger.info(f"Formatting {len(content_mapping)} content items...")
    applicator = StyleApplicator(str(template_path))

    if not applicator.apply_styles(content_mapping, str(output_file)):
        logger.error("Formatting failed")
        return 1

    logger.info(f"✓ Formatted document: {output_file}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
