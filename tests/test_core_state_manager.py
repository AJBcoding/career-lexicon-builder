"""
Tests for state manager and processing manifest.

This module tests state persistence, change detection, and manifest management.
Currently 0% coverage (341 lines untested).
"""

import pytest
import tempfile
import os
import json
from datetime import datetime
from pathlib import Path

from core.state_manager import (
    DocumentRecord,
    ProcessingManifest,
    compute_file_hash,
    load_manifest,
    save_manifest,
    needs_processing,
    add_document_record,
    get_documents_by_type,
    get_files_to_process
)
from core.document_processor import DocumentType


class TestDocumentRecord:
    """Tests for DocumentRecord dataclass."""

    def test_document_record_creation(self):
        """Test creating a DocumentRecord."""
        record = DocumentRecord(
            filepath="/path/to/doc.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed="2024-01-15T10:00:00",
            date_from_filename="2024-01-15",
            extraction_success=True
        )

        assert record.filepath == "/path/to/doc.pdf"
        assert record.file_hash == "abc123"
        assert record.document_type == "resume"
        assert record.extraction_success is True

    def test_document_record_to_dict(self):
        """Test converting DocumentRecord to dictionary."""
        record = DocumentRecord(
            filepath="doc.pdf",
            file_hash="hash123",
            document_type="cover_letter",
            date_processed="2024-01-01T00:00:00",
            date_from_filename=None,
            extraction_success=True
        )

        result = record.to_dict()
        assert isinstance(result, dict)
        assert result['filepath'] == "doc.pdf"
        assert result['file_hash'] == "hash123"
        assert result['date_from_filename'] is None

    def test_document_record_from_dict(self):
        """Test creating DocumentRecord from dictionary."""
        data = {
            'filepath': 'test.pdf',
            'file_hash': 'xyz789',
            'document_type': 'resume',
            'date_processed': '2024-02-01T12:00:00',
            'date_from_filename': '2024-02-01',
            'extraction_success': True
        }

        record = DocumentRecord.from_dict(data)
        assert record.filepath == 'test.pdf'
        assert record.file_hash == 'xyz789'
        assert record.document_type == 'resume'


class TestProcessingManifest:
    """Tests for ProcessingManifest dataclass."""

    def test_manifest_creation(self):
        """Test creating a ProcessingManifest."""
        manifest = ProcessingManifest(
            last_updated="2024-01-15T10:00:00",
            documents={},
            version="1.0.0"
        )

        assert manifest.version == "1.0.0"
        assert len(manifest.documents) == 0

    def test_manifest_to_dict(self):
        """Test converting manifest to dictionary."""
        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="hash1",
            document_type="resume",
            date_processed="2024-01-01",
            date_from_filename=None,
            extraction_success=True
        )

        manifest = ProcessingManifest(
            last_updated="2024-01-15",
            documents={"test.pdf": record},
            version="1.0.0"
        )

        result = manifest.to_dict()
        assert isinstance(result, dict)
        assert 'documents' in result
        assert 'test.pdf' in result['documents']

    def test_manifest_from_dict(self):
        """Test creating manifest from dictionary."""
        data = {
            'last_updated': '2024-01-15',
            'version': '1.0.0',
            'documents': {
                'doc1.pdf': {
                    'filepath': 'doc1.pdf',
                    'file_hash': 'hash1',
                    'document_type': 'resume',
                    'date_processed': '2024-01-01',
                    'date_from_filename': None,
                    'extraction_success': True
                }
            }
        }

        manifest = ProcessingManifest.from_dict(data)
        assert len(manifest.documents) == 1
        assert 'doc1.pdf' in manifest.documents
        assert isinstance(manifest.documents['doc1.pdf'], DocumentRecord)


class TestFileHashComputation:
    """Tests for file hash computation."""

    def test_compute_file_hash_basic(self):
        """Test computing hash of a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Test content for hashing")
            tmp.flush()
            tmp_path = tmp.name

        try:
            hash1 = compute_file_hash(tmp_path)
            assert isinstance(hash1, str)
            assert len(hash1) == 64  # SHA-256 produces 64 hex characters

            # Hash should be deterministic
            hash2 = compute_file_hash(tmp_path)
            assert hash1 == hash2
        finally:
            os.unlink(tmp_path)

    def test_compute_file_hash_different_content(self):
        """Test that different files have different hashes."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp1:
            tmp1.write("Content A")
            tmp1.flush()
            path1 = tmp1.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp2:
            tmp2.write("Content B")
            tmp2.flush()
            path2 = tmp2.name

        try:
            hash1 = compute_file_hash(path1)
            hash2 = compute_file_hash(path2)
            assert hash1 != hash2
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_compute_file_hash_nonexistent_file(self):
        """Test hash computation with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            compute_file_hash("/path/to/nonexistent/file.pdf")


class TestManifestLoadSave:
    """Tests for loading and saving manifests."""

    def test_load_manifest_nonexistent(self):
        """Test loading manifest when file doesn't exist creates empty manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            manifest = load_manifest(manifest_path)
            assert isinstance(manifest, ProcessingManifest)
            assert len(manifest.documents) == 0
            assert manifest.version == "1.0.0"

    def test_save_and_load_manifest(self):
        """Test saving and then loading a manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            # Create manifest with a document
            record = DocumentRecord(
                filepath="test.pdf",
                file_hash="abc123",
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )

            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={"test.pdf": record},
                version="1.0.0"
            )

            # Save manifest
            save_manifest(manifest, manifest_path)
            assert os.path.exists(manifest_path)

            # Load it back
            loaded = load_manifest(manifest_path)
            assert len(loaded.documents) == 1
            assert "test.pdf" in loaded.documents
            assert loaded.documents["test.pdf"].file_hash == "abc123"

    def test_load_corrupted_manifest(self):
        """Test loading corrupted manifest returns empty manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            # Write invalid JSON
            with open(manifest_path, 'w') as f:
                f.write("{ invalid json }")

            manifest = load_manifest(manifest_path)
            assert isinstance(manifest, ProcessingManifest)
            assert len(manifest.documents) == 0  # Should return empty on error


class TestNeedsProcessing:
    """Tests for change detection."""

    def test_needs_processing_new_file(self):
        """Test that new files need processing."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Test content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = needs_processing(tmp_path, manifest)
            assert result is True  # New file needs processing
        finally:
            os.unlink(tmp_path)

    def test_needs_processing_unchanged_file(self):
        """Test that unchanged files don't need processing."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Test content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Compute hash and add to manifest
            file_hash = compute_file_hash(tmp_path)
            record = DocumentRecord(
                filepath=tmp_path,
                file_hash=file_hash,
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )

            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={tmp_path: record},
                version="1.0.0"
            )

            result = needs_processing(tmp_path, manifest)
            assert result is False  # Unchanged file doesn't need processing
        finally:
            os.unlink(tmp_path)

    def test_needs_processing_modified_file(self):
        """Test that modified files need processing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Original content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Compute hash of original
            original_hash = compute_file_hash(tmp_path)
            record = DocumentRecord(
                filepath=tmp_path,
                file_hash=original_hash,
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )

            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={tmp_path: record},
                version="1.0.0"
            )

            # Modify the file
            with open(tmp_path, 'w') as f:
                f.write("Modified content")

            result = needs_processing(tmp_path, manifest)
            assert result is True  # Modified file needs processing
        finally:
            os.unlink(tmp_path)

    def test_needs_processing_nonexistent_file(self):
        """Test that nonexistent files don't need processing."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        result = needs_processing("/path/to/nonexistent.pdf", manifest)
        assert result is False  # Nonexistent files are skipped


class TestManifestOperations:
    """Tests for manifest manipulation operations."""

    def test_add_document_record(self):
        """Test adding a document record to manifest."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="hash123",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        add_document_record(manifest, record)
        assert "test.pdf" in manifest.documents
        assert manifest.documents["test.pdf"] == record

    def test_get_documents_by_type(self):
        """Test filtering documents by type."""
        record1 = DocumentRecord(
            filepath="resume1.pdf",
            file_hash="hash1",
            document_type=DocumentType.RESUME.value,
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        record2 = DocumentRecord(
            filepath="letter1.pdf",
            file_hash="hash2",
            document_type=DocumentType.COVER_LETTER.value,
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={"resume1.pdf": record1, "letter1.pdf": record2},
            version="1.0.0"
        )

        resumes = get_documents_by_type(manifest, DocumentType.RESUME)
        assert len(resumes) == 1
        assert resumes[0].filepath == "resume1.pdf"

        letters = get_documents_by_type(manifest, DocumentType.COVER_LETTER)
        assert len(letters) == 1
        assert letters[0].filepath == "letter1.pdf"


class TestGetFilesToProcess:
    """Tests for get_files_to_process function."""

    def test_get_files_to_process_empty_dir(self):
        """Test getting files from empty directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            files = get_files_to_process(tmpdir, manifest)
            assert files == []

    def test_get_files_to_process_with_new_files(self):
        """Test getting new files from directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = os.path.join(tmpdir, "doc1.pdf")
            file2 = os.path.join(tmpdir, "doc2.txt")

            with open(file1, 'w') as f:
                f.write("Content 1")
            with open(file2, 'w') as f:
                f.write("Content 2")

            files = get_files_to_process(tmpdir, manifest, ['.pdf', '.txt'])
            assert len(files) == 2
            assert any('doc1.pdf' in f for f in files)
            assert any('doc2.txt' in f for f in files)

    def test_get_files_to_process_with_extension_filter(self):
        """Test filtering files by extension."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files with different extensions
            pdf_file = os.path.join(tmpdir, "doc.pdf")
            txt_file = os.path.join(tmpdir, "doc.txt")
            other_file = os.path.join(tmpdir, "doc.xyz")

            for f in [pdf_file, txt_file, other_file]:
                with open(f, 'w') as file:
                    file.write("Content")

            # Filter for only .pdf files
            files = get_files_to_process(tmpdir, manifest, ['.pdf'])
            assert len(files) == 1
            assert files[0].endswith('.pdf')

    def test_get_files_to_process_nonexistent_dir(self):
        """Test with nonexistent directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        files = get_files_to_process("/nonexistent/directory", manifest)
        assert files == []
