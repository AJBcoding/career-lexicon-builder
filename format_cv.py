#!/usr/bin/env python3
"""
Format CV content using template styles.

Usage:
    python format_cv.py input.json output.docx [--preview] [--document-type {cv,cover-letter}]

Input format: JSON with content mapping
"""
import sys
import json
import argparse
from pathlib import Path
from cv_formatting.style_applicator import StyleApplicator
from cv_formatting.pdf_converter import PDFConverter
from cv_formatting.image_generator import ImageGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Format CV from content mapping."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Format CV or cover letter content using template styles.'
    )
    parser.add_argument('input', help='Input JSON file with content mapping')
    parser.add_argument('output', help='Output DOCX file path')
    parser.add_argument('--preview', action='store_true',
                        help='Generate PDF and page images for visual verification')
    parser.add_argument('--document-type', choices=['cv', 'cover-letter'],
                        default='cv',
                        help='Type of document to format (default: cv)')

    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit on error, catch it and return error code
        return 1

    input_file = Path(args.input)
    output_file = Path(args.output)
    preview = args.preview
    document_type = args.document_type

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return 1

    # Load content mapping
    try:
        with open(input_file) as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse input JSON: {e}")
        return 1

    # Handle both old and new JSON formats
    if isinstance(data, dict) and 'content' in data:
        # New format with metadata
        content_mapping = data['content']
        metadata = data.get('document_metadata', {})
    else:
        # Old format (backward compatible)
        content_mapping = data
        metadata = {}

    # Get template (shared location for both CVs and cover letters)
    template_path = Path("cv_formatting/templates/career-documents-template.docx")

    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        logger.error("Run generate_cv_template.py first")
        return 1

    # Get dictionary and signature paths
    dictionary_path = Path.home() / ".claude/skills/format-cover-letter/play-titles-dictionary.yaml"
    signature_path = Path.home() / ".claude/skills/format-cover-letter/signatures"

    # Apply styles
    logger.info(f"Formatting {len(content_mapping)} content items as {document_type}...")
    applicator = StyleApplicator(
        str(template_path),
        str(dictionary_path) if dictionary_path.exists() else None,
        str(signature_path) if signature_path.exists() else None
    )

    if not applicator.apply_styles(content_mapping, str(output_file),
                                   document_type=document_type,
                                   metadata=metadata):
        logger.error("Formatting failed")
        return 1

    logger.info(f"✓ Formatted document: {output_file}")

    # Generate preview if requested
    if preview:
        logger.info("\nGenerating preview...")

        # Convert to PDF
        pdf_converter = PDFConverter()
        pdf_path = output_file.with_suffix('.pdf')

        if pdf_converter.is_available():
            logger.info("PDF conversion: available")
            if pdf_converter.convert_to_pdf(str(output_file), str(pdf_path)):
                logger.info(f"✓ PDF: {pdf_path}")

                # Convert to images
                image_gen = ImageGenerator()
                image_dir = output_file.parent / f"{output_file.stem}_images"

                if image_gen.is_available():
                    logger.info("Image generation: available")
                    images = image_gen.generate_images(str(pdf_path), str(image_dir))

                    if images:
                        logger.info(f"✓ Preview images: {image_dir}/")
                        logger.info(f"  Generated {len(images)} page images")
                        for img in images:
                            logger.info(f"  - {img.name}")
                    else:
                        logger.warning("Image generation failed")
                else:
                    logger.info("Image generation: skipped (pdftoppm not available)")
            else:
                logger.warning("PDF conversion failed")
        else:
            logger.info("PDF conversion: skipped (LibreOffice not available)")
            logger.info("Image generation: skipped (requires PDF)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
