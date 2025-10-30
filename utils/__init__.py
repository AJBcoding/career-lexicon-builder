"""
Utility modules for career lexicon builder.
"""

from utils.date_parser import (
    extract_date_from_filename,
    format_date_citation,
    compare_dates
)

from utils.text_extraction import (
    extract_text_from_document,
    extract_metadata,
    get_extraction_instructions,
    SUPPORTED_EXTENSIONS,
    ExtractionResult,
    BulletPoint,
    FormattingSpan
)

from utils.similarity import (
    calculate_semantic_similarity,
    cluster_similar_items
)

__all__ = [
    # Date parsing
    'extract_date_from_filename',
    'format_date_citation',
    'compare_dates',
    # Text extraction
    'extract_text_from_document',
    'extract_metadata',
    'get_extraction_instructions',
    'SUPPORTED_EXTENSIONS',
    'ExtractionResult',
    'BulletPoint',
    'FormattingSpan',
    # Similarity
    'calculate_semantic_similarity',
    'cluster_similar_items',
]
