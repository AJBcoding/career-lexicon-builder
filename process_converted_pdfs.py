#!/usr/bin/env python3
"""
Process converted .pages PDFs and extract lexicon data.
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.orchestrator import run_full_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run pipeline on converted PDFs."""

    # Input directory with converted PDFs
    input_dir = "my_documents/converted"

    # Output directory for lexicons
    output_dir = "test_output/converted_pdfs"

    logger.info("=" * 80)
    logger.info("Processing Converted .pages PDFs")
    logger.info("=" * 80)
    logger.info(f"Input: {input_dir}")
    logger.info(f"Output: {output_dir}")
    logger.info("")

    # Run the full pipeline
    result = run_full_pipeline(
        input_dir=input_dir,
        output_dir=output_dir
    )

    # Print results
    logger.info("")
    logger.info("=" * 80)
    logger.info("RESULTS")
    logger.info("=" * 80)

    if result['success']:
        logger.info("✅ Pipeline completed successfully!")
    else:
        logger.error("❌ Pipeline completed with errors:")
        for error in result['errors']:
            logger.error(f"  - {error}")

    stats = result['statistics']
    logger.info("")
    logger.info("Statistics:")
    logger.info(f"  Documents processed: {stats['documents_processed']}")
    logger.info(f"  Themes found: {stats['themes_found']}")
    logger.info(f"  Qualifications found: {stats['qualifications_found']}")
    logger.info(f"  Narratives found: {stats['narratives_found']}")
    logger.info(f"  Keywords found: {stats['keywords_found']}")
    logger.info("")
    logger.info(f"Output files created in: {output_dir}/")
    logger.info("  - my_values.md")
    logger.info("  - resume_variations.md")
    logger.info("  - storytelling_patterns.md")
    logger.info("  - usage_index.md")
    logger.info("")

    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
