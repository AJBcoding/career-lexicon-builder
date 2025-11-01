"""
Central orchestrator for Career Lexicon Builder.

Coordinates document ingestion for LLM-based lexicon generation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
import os

# Document processing imports
from utils.text_extraction import extract_text_from_document
from utils.date_parser import extract_date_from_filename

# State management imports
from core.document_processor import classify_document, DocumentType
from core.state_manager import (
    load_manifest,
    save_manifest,
    compute_file_hash,
    needs_processing,
    add_document_record,
    get_files_to_process,
    ProcessingManifest,
    DocumentRecord
)

from datetime import datetime

logger = logging.getLogger(__name__)


def process_documents(input_dir: str, manifest: ProcessingManifest) -> List[Dict]:
    """
    Process all documents in input directory.

    For each document:
    - Extract text
    - Parse date from filename
    - Classify document type
    - Check if already processed (using manifest)

    Args:
        input_dir: Directory containing documents to process
        manifest: Current processing manifest

    Returns:
        List of document dicts with keys: text, filepath, date, doc_type
    """
    documents = []

    # Supported extensions
    extensions = ['.pages', '.pdf', '.docx', '.txt', '.md']

    # Get all files to process
    files_to_process = get_files_to_process(input_dir, manifest, extensions)

    logger.info(f"Found {len(files_to_process)} documents to process")

    for filepath in files_to_process:
        try:
            # Extract text
            extraction_result = extract_text_from_document(filepath)

            if not extraction_result['success']:
                logger.warning(f"Failed to extract text from {filepath}: {extraction_result.get('error', 'Unknown error')}")
                continue

            text = extraction_result['text']

            # Skip empty documents
            if not text or not text.strip():
                logger.warning(f"Skipping empty document: {filepath}")
                continue

            # Parse date from filename
            date = extract_date_from_filename(filepath)

            # Classify document
            doc_type, confidence, method = classify_document(filepath, text)

            logger.debug(f"Classified {filepath} as {doc_type.value} (confidence: {confidence:.2f}, method: {method})")

            # Create document dict
            doc_dict = {
                'text': text,
                'filepath': filepath,
                'doc_type': doc_type,
            }

            # Add date if found
            if date is not None:
                doc_dict['date'] = date

            documents.append(doc_dict)

            # Add to manifest
            file_hash = compute_file_hash(filepath)
            record = DocumentRecord(
                filepath=filepath,
                file_hash=file_hash,
                document_type=doc_type.value,
                date_processed=datetime.now().isoformat(),
                date_from_filename=date.isoformat() if date else None,
                extraction_success=True
            )
            add_document_record(manifest, record)

        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            continue

    logger.info(f"Successfully processed {len(documents)} documents")

    return documents


def get_document_hash(filepath: str) -> str:
    """
    Calculate hash of document for change detection.

    Args:
        filepath: Path to document

    Returns:
        SHA-256 hash string
    """
    return compute_file_hash(filepath)


def is_document_modified(filepath: str, manifest: ProcessingManifest) -> bool:
    """
    Check if document has been modified since last processing.

    Args:
        filepath: Path to document
        manifest: Current processing manifest

    Returns:
        True if document is new or modified, False otherwise
    """
    return needs_processing(filepath, manifest)