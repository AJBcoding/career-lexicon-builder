"""
Career Lexicon Builder - Source Package

A comprehensive toolkit for analyzing career documents and building
targeted application materials.

Modules:
- document_processor: Document classification
- text_extractor: Multi-format text extraction
- metadata_extractor: Date, position, organization extraction
- cache_manager: Smart caching with change detection
- term_extractor: Skill and qualification extraction
- context_analyzer: Action verb and quantifier analysis
- term_categorizer: Skill categorization by domain/role/level
- lexicon_builder: Skill aggregation across documents
- gap_analyzer: Job requirement gap analysis
"""

__version__ = "1.0.0"
__author__ = "Career Lexicon Builder Contributors"

__all__ = [
    "document_processor",
    "text_extractor",
    "metadata_extractor",
    "cache_manager",
    "term_extractor",
    "context_analyzer",
    "term_categorizer",
    "lexicon_builder",
    "gap_analyzer",
]
