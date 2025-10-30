"""
Central orchestrator for Career Lexicon Builder.

Coordinates the full pipeline from document ingestion to lexicon generation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
import os

# Phase 1 imports
from utils.text_extraction import extract_text_from_document
from utils.date_parser import extract_date_from_filename

# Phase 2 imports
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

# Phase 3 imports
from analyzers.themes_analyzer import analyze_themes
from analyzers.qualifications_analyzer import analyze_qualifications
from analyzers.narratives_analyzer import analyze_narratives
from analyzers.keywords_analyzer import analyze_keywords

# Phase 4 imports
from generators.themes_lexicon_generator import generate_themes_lexicon
from generators.qualifications_lexicon_generator import generate_qualifications_lexicon
from generators.narratives_lexicon_generator import generate_narratives_lexicon
from generators.keywords_lexicon_generator import generate_keywords_lexicon

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


def run_all_analyzers(documents: List[Dict]) -> Dict:
    """
    Run all Phase 3 analyzers on documents.

    Args:
        documents: List of document dicts with text, filepath, date, doc_type

    Returns:
        Dict with keys: 'themes', 'qualifications', 'narratives', 'keywords'
    """
    logger.info("Running all analyzers...")

    analysis_results = {}

    try:
        logger.info("Analyzing themes...")
        analysis_results['themes'] = analyze_themes(documents)
        logger.info(f"Found {len(analysis_results['themes'])} themes")
    except Exception as e:
        logger.error(f"Themes analysis failed: {e}")
        analysis_results['themes'] = []

    try:
        logger.info("Analyzing qualifications...")
        analysis_results['qualifications'] = analyze_qualifications(documents)
        logger.info(f"Found {len(analysis_results['qualifications'])} qualifications")
    except Exception as e:
        logger.error(f"Qualifications analysis failed: {e}")
        analysis_results['qualifications'] = []

    try:
        logger.info("Analyzing narratives...")
        analysis_results['narratives'] = analyze_narratives(documents)
        logger.info(f"Found {len(analysis_results['narratives'])} narratives")
    except Exception as e:
        logger.error(f"Narratives analysis failed: {e}")
        analysis_results['narratives'] = []

    try:
        logger.info("Analyzing keywords...")
        analysis_results['keywords'] = analyze_keywords(documents)
        logger.info(f"Found {len(analysis_results['keywords'])} keywords")
    except Exception as e:
        logger.error(f"Keywords analysis failed: {e}")
        analysis_results['keywords'] = []

    logger.info("Analysis complete")

    return analysis_results


def generate_all_lexicons(analysis_results: Dict, output_dir: str) -> None:
    """
    Generate all Phase 4 lexicons from analysis results.

    Creates:
    - output_dir/my_values.md
    - output_dir/resume_variations.md
    - output_dir/storytelling_patterns.md
    - output_dir/usage_index.md

    Args:
        analysis_results: Dict with keys: themes, qualifications, narratives, keywords
        output_dir: Directory to write lexicons
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    logger.info("Generating lexicons...")

    # Generate themes lexicon
    try:
        themes_path = os.path.join(output_dir, "my_values.md")
        generate_themes_lexicon(analysis_results['themes'], themes_path)
        logger.info(f"Themes lexicon written to: {themes_path}")
    except Exception as e:
        logger.error(f"Failed to generate themes lexicon: {e}")

    # Generate qualifications lexicon
    try:
        qualifications_path = os.path.join(output_dir, "resume_variations.md")
        generate_qualifications_lexicon(analysis_results['qualifications'], qualifications_path)
        logger.info(f"Qualifications lexicon written to: {qualifications_path}")
    except Exception as e:
        logger.error(f"Failed to generate qualifications lexicon: {e}")

    # Generate narratives lexicon
    try:
        narratives_path = os.path.join(output_dir, "storytelling_patterns.md")
        generate_narratives_lexicon(analysis_results['narratives'], narratives_path)
        logger.info(f"Narratives lexicon written to: {narratives_path}")
    except Exception as e:
        logger.error(f"Failed to generate narratives lexicon: {e}")

    # Generate keywords lexicon
    try:
        keywords_path = os.path.join(output_dir, "usage_index.md")
        generate_keywords_lexicon(analysis_results['keywords'], keywords_path)
        logger.info(f"Keywords lexicon written to: {keywords_path}")
    except Exception as e:
        logger.error(f"Failed to generate keywords lexicon: {e}")

    logger.info("Lexicon generation complete")


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


def merge_analysis_results(existing: Dict, new: Dict) -> Dict:
    """
    Merge new analysis results with existing data.

    Args:
        existing: Existing analysis results
        new: New analysis results to merge

    Returns:
        Merged analysis results dict
    """
    merged = {}

    # Merge each analysis type (themes, qualifications, narratives, keywords)
    for key in ['themes', 'qualifications', 'narratives', 'keywords']:
        existing_items = existing.get(key, [])
        new_items = new.get(key, [])

        # Combine lists and remove duplicates
        # For themes/qualifications/narratives, they have 'theme'/'qualification'/'pattern' fields
        # For keywords, they have 'keyword' field

        if key == 'themes':
            # Merge by theme name
            merged_dict = {}
            for item in existing_items:
                merged_dict[item['theme']] = item
            for item in new_items:
                if item['theme'] in merged_dict:
                    # Merge occurrences and documents
                    existing_item = merged_dict[item['theme']]
                    existing_item['occurrences'] = list(set(existing_item.get('occurrences', []) + item.get('occurrences', [])))
                    existing_item['documents'] = list(set(existing_item.get('documents', []) + item.get('documents', [])))
                else:
                    merged_dict[item['theme']] = item
            merged[key] = list(merged_dict.values())

        elif key == 'qualifications':
            # Merge by qualification name
            merged_dict = {}
            for item in existing_items:
                merged_dict[item['qualification']] = item
            for item in new_items:
                if item['qualification'] in merged_dict:
                    # Merge variations
                    existing_item = merged_dict[item['qualification']]
                    existing_variations = existing_item.get('variations', [])
                    new_variations = item.get('variations', [])
                    # Merge variations by text
                    variation_dict = {v['text']: v for v in existing_variations}
                    for v in new_variations:
                        if v['text'] not in variation_dict:
                            variation_dict[v['text']] = v
                        else:
                            # Merge documents for this variation
                            variation_dict[v['text']]['documents'] = list(set(
                                variation_dict[v['text']].get('documents', []) + v.get('documents', [])
                            ))
                    existing_item['variations'] = list(variation_dict.values())
                else:
                    merged_dict[item['qualification']] = item
            merged[key] = list(merged_dict.values())

        elif key == 'narratives':
            # Merge by pattern name
            merged_dict = {}
            for item in existing_items:
                merged_dict[item['pattern']] = item
            for item in new_items:
                if item['pattern'] in merged_dict:
                    # Merge examples
                    existing_item = merged_dict[item['pattern']]
                    existing_examples = existing_item.get('examples', [])
                    new_examples = item.get('examples', [])
                    # Merge examples by text
                    example_dict = {e['text']: e for e in existing_examples}
                    for e in new_examples:
                        if e['text'] not in example_dict:
                            example_dict[e['text']] = e
                    existing_item['examples'] = list(example_dict.values())
                else:
                    merged_dict[item['pattern']] = item
            merged[key] = list(merged_dict.values())

        elif key == 'keywords':
            # Merge by keyword
            merged_dict = {}
            for item in existing_items:
                merged_dict[item['keyword']] = item
            for item in new_items:
                if item['keyword'] in merged_dict:
                    # Merge contexts and documents
                    existing_item = merged_dict[item['keyword']]
                    existing_item['contexts'] = list(set(existing_item.get('contexts', []) + item.get('contexts', [])))
                    existing_item['documents'] = list(set(existing_item.get('documents', []) + item.get('documents', [])))
                    # Update count
                    existing_item['count'] = len(existing_item['contexts'])
                else:
                    merged_dict[item['keyword']] = item
            merged[key] = list(merged_dict.values())

    return merged


def run_full_pipeline(
    input_dir: str,
    output_dir: str,
    state_file: Optional[str] = None
) -> Dict:
    """
    Run complete pipeline from document ingestion to lexicon generation.

    Steps:
    1. Load or initialize state
    2. Scan input directory for documents
    3. Extract text from documents (Phase 1)
    4. Classify documents (Phase 2)
    5. Run all analyzers (Phase 3)
    6. Generate all lexicons (Phase 4)
    7. Save state
    8. Return summary statistics

    Args:
        input_dir: Directory containing source documents
        output_dir: Directory to write lexicons
        state_file: Optional path to state file (default: output_dir/.state.json)

    Returns:
        Dict with statistics (documents processed, themes found, etc.)
    """
    logger.info(f"Starting full pipeline for: {input_dir}")
    logger.info(f"Output directory: {output_dir}")

    errors = []

    # Step 1: Load or initialize manifest (state)
    if state_file is None:
        state_file = os.path.join(output_dir, ".state.json")

    try:
        manifest = load_manifest(state_file)
        logger.info(f"Loaded manifest from: {state_file}")
    except Exception as e:
        logger.error(f"Failed to load manifest: {e}")
        errors.append(f"Failed to load manifest: {e}")
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

    # Step 2-4: Process documents (extract text, classify)
    logger.info("Phase 1-2: Processing documents...")
    documents = process_documents(input_dir, manifest)

    if not documents:
        logger.warning("No documents processed")
        errors.append("No documents processed")

    logger.info(f"Processed {len(documents)} documents")

    # Step 5: Run all analyzers
    logger.info("Phase 3: Running analyzers...")
    analysis_results = run_all_analyzers(documents)

    # Step 6: Generate all lexicons
    logger.info("Phase 4: Generating lexicons...")
    generate_all_lexicons(analysis_results, output_dir)

    # Step 7: Save state
    try:
        save_manifest(manifest, state_file)
        logger.info(f"Manifest saved to: {state_file}")
    except Exception as e:
        logger.error(f"Failed to save manifest: {e}")
        errors.append(f"Failed to save manifest: {e}")

    # Step 8: Return summary statistics
    statistics = {
        'documents_processed': len(documents),
        'themes_found': len(analysis_results.get('themes', [])),
        'qualifications_found': len(analysis_results.get('qualifications', [])),
        'narratives_found': len(analysis_results.get('narratives', [])),
        'keywords_found': len(analysis_results.get('keywords', [])),
    }

    logger.info("Pipeline complete!")
    logger.info(f"Statistics: {statistics}")

    result = {
        'success': len(errors) == 0,
        'errors': errors,
        'statistics': statistics
    }

    return result


def run_incremental_update(
    input_dir: str,
    output_dir: str,
    state_file: Optional[str] = None
) -> Dict:
    """
    Process only new/modified documents and update lexicons.

    Steps:
    1. Load existing state
    2. Identify new/modified documents (by hash/modification time)
    3. Process only changed documents
    4. Load existing analysis data
    5. Merge new analysis with existing
    6. Regenerate lexicons with merged data
    7. Update state
    8. Return summary statistics

    Args:
        input_dir: Directory containing source documents
        output_dir: Directory containing existing lexicons
        state_file: Optional path to state file

    Returns:
        Dict with statistics (new documents, updated themes, etc.)
    """
    logger.info(f"Starting incremental update for: {input_dir}")
    logger.info(f"Output directory: {output_dir}")

    errors = []

    # Step 1: Load existing state
    if state_file is None:
        state_file = os.path.join(output_dir, ".state.json")

    try:
        manifest = load_manifest(state_file)
        logger.info(f"Loaded manifest from: {state_file}")
    except Exception as e:
        logger.error(f"Failed to load manifest: {e}")
        errors.append(f"Failed to load manifest: {e}")
        # If no manifest exists, fall back to full pipeline
        logger.warning("No existing manifest found, running full pipeline instead")
        return run_full_pipeline(input_dir, output_dir, state_file)

    # Step 2-3: Process only new/modified documents
    logger.info("Identifying new/modified documents...")
    new_documents = process_documents(input_dir, manifest)

    if not new_documents:
        logger.info("No new or modified documents found")
        result = {
            'success': True,
            'errors': [],
            'statistics': {
                'new_documents': 0,
                'themes_found': 0,
                'qualifications_found': 0,
                'narratives_found': 0,
                'keywords_found': 0,
            }
        }
        return result

    logger.info(f"Found {len(new_documents)} new/modified documents")

    # Step 4: For MVP, we'll run full analysis on all documents
    # In a full implementation, we would:
    # - Load cached analysis results from .analysis_cache.json
    # - Run analysis only on new documents
    # - Merge with cached results
    # For now, we process ALL documents in the manifest
    logger.info("Running analysis on all documents...")

    # Get all documents from manifest and re-extract them
    # (In a more optimized version, we'd cache extracted text)
    all_filepaths = list(manifest.documents.keys())
    all_documents = []

    for filepath in all_filepaths:
        if not os.path.exists(filepath):
            logger.warning(f"Skipping missing file: {filepath}")
            continue

        try:
            extraction_result = extract_text_from_document(filepath)
            if extraction_result['success']:
                text = extraction_result['text']
                if text and text.strip():
                    doc_type, _, _ = classify_document(filepath, text)
                    date = extract_date_from_filename(filepath)

                    doc_dict = {
                        'text': text,
                        'filepath': filepath,
                        'doc_type': doc_type,
                    }
                    if date is not None:
                        doc_dict['date'] = date

                    all_documents.append(doc_dict)
        except Exception as e:
            logger.error(f"Error re-processing {filepath}: {e}")
            continue

    # Step 5: Run all analyzers on combined document set
    logger.info("Phase 3: Running analyzers on full document set...")
    analysis_results = run_all_analyzers(all_documents)

    # Step 6: Generate all lexicons
    logger.info("Phase 4: Regenerating lexicons...")
    generate_all_lexicons(analysis_results, output_dir)

    # Step 7: Save state
    try:
        save_manifest(manifest, state_file)
        logger.info(f"Manifest saved to: {state_file}")
    except Exception as e:
        logger.error(f"Failed to save manifest: {e}")
        errors.append(f"Failed to save manifest: {e}")

    # Step 8: Return summary statistics
    statistics = {
        'new_documents': len(new_documents),
        'total_documents': len(all_documents),
        'themes_found': len(analysis_results.get('themes', [])),
        'qualifications_found': len(analysis_results.get('qualifications', [])),
        'narratives_found': len(analysis_results.get('narratives', [])),
        'keywords_found': len(analysis_results.get('keywords', [])),
    }

    logger.info("Incremental update complete!")
    logger.info(f"Statistics: {statistics}")

    result = {
        'success': len(errors) == 0,
        'errors': errors,
        'statistics': statistics
    }

    return result
