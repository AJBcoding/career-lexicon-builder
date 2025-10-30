"""
State management and processing manifest utilities.

This module provides functionality to track processed documents, detect changes,
and enable incremental processing.
"""

import json
import hashlib
import os
from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Dict, List, Optional
from core.document_processor import DocumentType


@dataclass
class DocumentRecord:
    """
    Record of a processed document.

    Attributes:
        filepath: Path to the document file
        file_hash: SHA-256 hash of file contents
        document_type: Classified document type
        date_processed: When the document was processed
        date_from_filename: Date extracted from filename (if any)
        extraction_success: Whether text extraction succeeded
    """
    filepath: str
    file_hash: str
    document_type: str  # Store as string for JSON serialization
    date_processed: str  # Store as ISO format string
    date_from_filename: Optional[str]  # Store as ISO format string or None
    extraction_success: bool

    def to_dict(self) -> dict:
        """Convert record to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentRecord':
        """Create record from dictionary (for JSON deserialization)."""
        return cls(**data)


@dataclass
class ProcessingManifest:
    """
    Manifest tracking all processed documents.

    Attributes:
        last_updated: Timestamp of last manifest update
        documents: Dictionary mapping filepath to DocumentRecord
        version: Manifest format version
    """
    last_updated: str  # ISO format string
    documents: Dict[str, DocumentRecord]
    version: str = "1.0.0"

    def to_dict(self) -> dict:
        """Convert manifest to dictionary for JSON serialization."""
        return {
            'last_updated': self.last_updated,
            'version': self.version,
            'documents': {
                filepath: record.to_dict()
                for filepath, record in self.documents.items()
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ProcessingManifest':
        """Create manifest from dictionary (for JSON deserialization)."""
        documents = {
            filepath: DocumentRecord.from_dict(record_data)
            for filepath, record_data in data.get('documents', {}).items()
        }
        return cls(
            last_updated=data['last_updated'],
            documents=documents,
            version=data.get('version', '1.0.0')
        )


def compute_file_hash(filepath: str) -> str:
    """
    Compute SHA-256 hash of file contents.

    Args:
        filepath: Path to file

    Returns:
        Hexadecimal hash string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read

    Examples:
        >>> hash1 = compute_file_hash("document.pdf")
        >>> hash2 = compute_file_hash("document.pdf")
        >>> hash1 == hash2
        True
    """
    sha256_hash = hashlib.sha256()

    with open(filepath, "rb") as f:
        # Read in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def load_manifest(manifest_path: str) -> ProcessingManifest:
    """
    Load processing manifest from JSON file.

    Creates a new empty manifest if file doesn't exist.

    Args:
        manifest_path: Path to manifest JSON file

    Returns:
        ProcessingManifest instance

    Examples:
        >>> manifest = load_manifest(".lexicon-cache/manifest.json")
        >>> isinstance(manifest, ProcessingManifest)
        True
    """
    if not os.path.exists(manifest_path):
        # Create new empty manifest
        return ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return ProcessingManifest.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        # If manifest is corrupted, return empty manifest
        # In production, you might want to log this error
        return ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )


def save_manifest(manifest: ProcessingManifest, manifest_path: str) -> None:
    """
    Save processing manifest to JSON file.

    Creates directory if it doesn't exist.
    Updates last_updated timestamp.

    Args:
        manifest: ProcessingManifest to save
        manifest_path: Path to manifest JSON file

    Examples:
        >>> manifest = ProcessingManifest(
        ...     last_updated=datetime.now().isoformat(),
        ...     documents={},
        ...     version="1.0.0"
        ... )
        >>> save_manifest(manifest, ".lexicon-cache/manifest.json")
    """
    # Update timestamp
    manifest.last_updated = datetime.now().isoformat()

    # Create directory if it doesn't exist
    manifest_dir = os.path.dirname(manifest_path)
    if manifest_dir and not os.path.exists(manifest_dir):
        os.makedirs(manifest_dir, exist_ok=True)

    # Write JSON with pretty formatting
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)


def needs_processing(filepath: str, manifest: ProcessingManifest) -> bool:
    """
    Check if a file needs processing.

    A file needs processing if:
    1. It's not in the manifest (new file)
    2. Its hash has changed (modified file)
    3. The file doesn't exist anymore (will return False to skip)

    Args:
        filepath: Path to file to check
        manifest: Current processing manifest

    Returns:
        True if file needs processing, False otherwise

    Examples:
        >>> manifest = ProcessingManifest(
        ...     last_updated=datetime.now().isoformat(),
        ...     documents={},
        ...     version="1.0.0"
        ... )
        >>> needs_processing("new_file.pdf", manifest)
        True
    """
    # If file doesn't exist, skip it
    if not os.path.exists(filepath):
        return False

    # If not in manifest, needs processing (new file)
    if filepath not in manifest.documents:
        return True

    # Check if hash has changed (modified file)
    try:
        current_hash = compute_file_hash(filepath)
        stored_record = manifest.documents[filepath]
        return current_hash != stored_record.file_hash
    except (IOError, OSError):
        # If we can't read the file, skip it
        return False


def add_document_record(
    manifest: ProcessingManifest,
    record: DocumentRecord
) -> None:
    """
    Add or update a document record in the manifest.

    Args:
        manifest: ProcessingManifest to update
        record: DocumentRecord to add/update

    Examples:
        >>> from datetime import datetime
        >>> manifest = ProcessingManifest(
        ...     last_updated=datetime.now().isoformat(),
        ...     documents={},
        ...     version="1.0.0"
        ... )
        >>> record = DocumentRecord(
        ...     filepath="resume.pdf",
        ...     file_hash="abc123",
        ...     document_type="resume",
        ...     date_processed=datetime.now().isoformat(),
        ...     date_from_filename=None,
        ...     extraction_success=True
        ... )
        >>> add_document_record(manifest, record)
        >>> "resume.pdf" in manifest.documents
        True
    """
    manifest.documents[record.filepath] = record


def get_documents_by_type(
    manifest: ProcessingManifest,
    doc_type: DocumentType
) -> List[DocumentRecord]:
    """
    Get all documents of a specific type from manifest.

    Args:
        manifest: ProcessingManifest to query
        doc_type: DocumentType to filter by

    Returns:
        List of DocumentRecords matching the type

    Examples:
        >>> manifest = ProcessingManifest(
        ...     last_updated=datetime.now().isoformat(),
        ...     documents={},
        ...     version="1.0.0"
        ... )
        >>> resumes = get_documents_by_type(manifest, DocumentType.RESUME)
        >>> isinstance(resumes, list)
        True
    """
    doc_type_str = doc_type.value
    return [
        record
        for record in manifest.documents.values()
        if record.document_type == doc_type_str
    ]


def get_files_to_process(
    input_dir: str,
    manifest: ProcessingManifest,
    extensions: Optional[List[str]] = None
) -> List[str]:
    """
    Get list of files that need processing from a directory.

    Args:
        input_dir: Directory to scan for files
        manifest: Current processing manifest
        extensions: Optional list of file extensions to include (e.g., ['.pdf', '.docx'])
                   If None, includes all files

    Returns:
        List of filepaths that need processing

    Examples:
        >>> manifest = ProcessingManifest(
        ...     last_updated=datetime.now().isoformat(),
        ...     documents={},
        ...     version="1.0.0"
        ... )
        >>> files = get_files_to_process("docs/", manifest, ['.pdf', '.docx'])
        >>> isinstance(files, list)
        True
    """
    if not os.path.exists(input_dir):
        return []

    files_to_process = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Check extension filter if provided
            if extensions is not None:
                if not any(filepath.lower().endswith(ext.lower()) for ext in extensions):
                    continue

            # Check if file needs processing
            if needs_processing(filepath, manifest):
                files_to_process.append(filepath)

    return files_to_process
