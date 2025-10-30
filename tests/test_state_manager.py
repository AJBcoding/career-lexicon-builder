"""
Tests for state_manager module.
"""

import pytest
import json
import os
import tempfile
import shutil
from datetime import datetime, date
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

    def test_create_record(self):
        """Test creating a document record."""
        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed="2024-01-01T12:00:00",
            date_from_filename="2024-01-01",
            extraction_success=True
        )
        assert record.filepath == "test.pdf"
        assert record.file_hash == "abc123"
        assert record.document_type == "resume"
        assert record.extraction_success is True

    def test_to_dict(self):
        """Test converting record to dictionary."""
        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed="2024-01-01T12:00:00",
            date_from_filename="2024-01-01",
            extraction_success=True
        )
        record_dict = record.to_dict()
        assert record_dict['filepath'] == "test.pdf"
        assert record_dict['file_hash'] == "abc123"
        assert record_dict['document_type'] == "resume"

    def test_from_dict(self):
        """Test creating record from dictionary."""
        data = {
            'filepath': "test.pdf",
            'file_hash': "abc123",
            'document_type': "resume",
            'date_processed': "2024-01-01T12:00:00",
            'date_from_filename': "2024-01-01",
            'extraction_success': True
        }
        record = DocumentRecord.from_dict(data)
        assert record.filepath == "test.pdf"
        assert record.file_hash == "abc123"

    def test_round_trip_serialization(self):
        """Test that to_dict/from_dict round-trip works."""
        original = DocumentRecord(
            filepath="test.pdf",
            file_hash="xyz789",
            document_type="cover_letter",
            date_processed="2024-01-01T12:00:00",
            date_from_filename=None,
            extraction_success=False
        )
        record_dict = original.to_dict()
        restored = DocumentRecord.from_dict(record_dict)
        assert restored.filepath == original.filepath
        assert restored.file_hash == original.file_hash
        assert restored.document_type == original.document_type
        assert restored.extraction_success == original.extraction_success


class TestProcessingManifest:
    """Tests for ProcessingManifest dataclass."""

    def test_create_manifest(self):
        """Test creating a processing manifest."""
        manifest = ProcessingManifest(
            last_updated="2024-01-01T12:00:00",
            documents={},
            version="1.0.0"
        )
        assert manifest.version == "1.0.0"
        assert len(manifest.documents) == 0

    def test_to_dict(self):
        """Test converting manifest to dictionary."""
        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed="2024-01-01T12:00:00",
            date_from_filename=None,
            extraction_success=True
        )
        manifest = ProcessingManifest(
            last_updated="2024-01-01T12:00:00",
            documents={"test.pdf": record},
            version="1.0.0"
        )
        manifest_dict = manifest.to_dict()
        assert manifest_dict['version'] == "1.0.0"
        assert 'test.pdf' in manifest_dict['documents']

    def test_from_dict(self):
        """Test creating manifest from dictionary."""
        data = {
            'last_updated': "2024-01-01T12:00:00",
            'version': "1.0.0",
            'documents': {
                'test.pdf': {
                    'filepath': "test.pdf",
                    'file_hash': "abc123",
                    'document_type': "resume",
                    'date_processed': "2024-01-01T12:00:00",
                    'date_from_filename': None,
                    'extraction_success': True
                }
            }
        }
        manifest = ProcessingManifest.from_dict(data)
        assert manifest.version == "1.0.0"
        assert "test.pdf" in manifest.documents
        assert manifest.documents["test.pdf"].file_hash == "abc123"

    def test_round_trip_serialization(self):
        """Test that to_dict/from_dict round-trip works."""
        record1 = DocumentRecord(
            filepath="test1.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed="2024-01-01T12:00:00",
            date_from_filename=None,
            extraction_success=True
        )
        record2 = DocumentRecord(
            filepath="test2.pdf",
            file_hash="xyz789",
            document_type="cover_letter",
            date_processed="2024-01-02T12:00:00",
            date_from_filename="2024-01-02",
            extraction_success=True
        )
        original = ProcessingManifest(
            last_updated="2024-01-01T12:00:00",
            documents={"test1.pdf": record1, "test2.pdf": record2},
            version="1.0.0"
        )
        manifest_dict = original.to_dict()
        restored = ProcessingManifest.from_dict(manifest_dict)
        assert len(restored.documents) == 2
        assert "test1.pdf" in restored.documents
        assert "test2.pdf" in restored.documents


class TestComputeFileHash:
    """Tests for compute_file_hash function."""

    def test_hash_consistency(self):
        """Test that same file produces same hash."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            filepath = f.name

        try:
            hash1 = compute_file_hash(filepath)
            hash2 = compute_file_hash(filepath)
            assert hash1 == hash2
        finally:
            os.unlink(filepath)

    def test_different_content_different_hash(self):
        """Test that different content produces different hash."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write("Content A")
            filepath1 = f1.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write("Content B")
            filepath2 = f2.name

        try:
            hash1 = compute_file_hash(filepath1)
            hash2 = compute_file_hash(filepath2)
            assert hash1 != hash2
        finally:
            os.unlink(filepath1)
            os.unlink(filepath2)

    def test_modified_file_different_hash(self):
        """Test that modifying file changes hash."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Original content")
            filepath = f.name

        try:
            hash1 = compute_file_hash(filepath)

            # Modify file
            with open(filepath, 'w') as f:
                f.write("Modified content")

            hash2 = compute_file_hash(filepath)
            assert hash1 != hash2
        finally:
            os.unlink(filepath)

    def test_file_not_found(self):
        """Test that missing file raises error."""
        with pytest.raises(FileNotFoundError):
            compute_file_hash("/nonexistent/file.txt")

    def test_hash_format(self):
        """Test that hash is hexadecimal string."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test")
            filepath = f.name

        try:
            file_hash = compute_file_hash(filepath)
            # SHA-256 hash is 64 hex characters
            assert len(file_hash) == 64
            assert all(c in '0123456789abcdef' for c in file_hash)
        finally:
            os.unlink(filepath)


class TestLoadManifest:
    """Tests for load_manifest function."""

    def test_load_nonexistent_manifest(self):
        """Test loading manifest when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = load_manifest(manifest_path)
            assert isinstance(manifest, ProcessingManifest)
            assert len(manifest.documents) == 0
            assert manifest.version == "1.0.0"

    def test_load_existing_manifest(self):
        """Test loading existing manifest file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            # Create manifest file
            data = {
                'last_updated': "2024-01-01T12:00:00",
                'version': "1.0.0",
                'documents': {
                    'test.pdf': {
                        'filepath': "test.pdf",
                        'file_hash': "abc123",
                        'document_type': "resume",
                        'date_processed': "2024-01-01T12:00:00",
                        'date_from_filename': None,
                        'extraction_success': True
                    }
                }
            }
            with open(manifest_path, 'w') as f:
                json.dump(data, f)

            # Load manifest
            manifest = load_manifest(manifest_path)
            assert len(manifest.documents) == 1
            assert "test.pdf" in manifest.documents

    def test_load_corrupted_manifest(self):
        """Test loading corrupted manifest returns empty manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            # Create invalid JSON
            with open(manifest_path, 'w') as f:
                f.write("{ invalid json")

            # Should return empty manifest instead of crashing
            manifest = load_manifest(manifest_path)
            assert isinstance(manifest, ProcessingManifest)
            assert len(manifest.documents) == 0


class TestSaveManifest:
    """Tests for save_manifest function."""

    def test_save_manifest(self):
        """Test saving manifest to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            record = DocumentRecord(
                filepath="test.pdf",
                file_hash="abc123",
                document_type="resume",
                date_processed="2024-01-01T12:00:00",
                date_from_filename=None,
                extraction_success=True
            )
            manifest = ProcessingManifest(
                last_updated="2024-01-01T12:00:00",
                documents={"test.pdf": record},
                version="1.0.0"
            )

            save_manifest(manifest, manifest_path)

            # Verify file exists
            assert os.path.exists(manifest_path)

            # Verify content
            with open(manifest_path, 'r') as f:
                data = json.load(f)
            assert 'documents' in data
            assert 'test.pdf' in data['documents']

    def test_save_creates_directory(self):
        """Test that save creates directory if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "subdir", "manifest.json")

            manifest = ProcessingManifest(
                last_updated="2024-01-01T12:00:00",
                documents={},
                version="1.0.0"
            )

            save_manifest(manifest, manifest_path)

            # Verify directory and file created
            assert os.path.exists(os.path.dirname(manifest_path))
            assert os.path.exists(manifest_path)

    def test_save_updates_timestamp(self):
        """Test that save updates last_updated timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            manifest = ProcessingManifest(
                last_updated="2024-01-01T12:00:00",
                documents={},
                version="1.0.0"
            )

            original_timestamp = manifest.last_updated
            save_manifest(manifest, manifest_path)

            # Timestamp should be updated
            assert manifest.last_updated != original_timestamp

    def test_save_load_round_trip(self):
        """Test that save/load round-trip preserves data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")

            record = DocumentRecord(
                filepath="test.pdf",
                file_hash="abc123",
                document_type="resume",
                date_processed="2024-01-01T12:00:00",
                date_from_filename="2024-01-01",
                extraction_success=True
            )
            original = ProcessingManifest(
                last_updated="2024-01-01T12:00:00",
                documents={"test.pdf": record},
                version="1.0.0"
            )

            save_manifest(original, manifest_path)
            loaded = load_manifest(manifest_path)

            assert len(loaded.documents) == 1
            assert "test.pdf" in loaded.documents
            assert loaded.documents["test.pdf"].file_hash == "abc123"


class TestNeedsProcessing:
    """Tests for needs_processing function."""

    def test_new_file_needs_processing(self):
        """Test that new files need processing."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.NamedTemporaryFile(delete=False) as f:
            filepath = f.name

        try:
            assert needs_processing(filepath, manifest) is True
        finally:
            os.unlink(filepath)

    def test_unchanged_file_no_processing(self):
        """Test that unchanged files don't need processing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            filepath = f.name

        try:
            file_hash = compute_file_hash(filepath)
            record = DocumentRecord(
                filepath=filepath,
                file_hash=file_hash,
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )
            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={filepath: record},
                version="1.0.0"
            )

            assert needs_processing(filepath, manifest) is False
        finally:
            os.unlink(filepath)

    def test_modified_file_needs_processing(self):
        """Test that modified files need processing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Original content")
            filepath = f.name

        try:
            # Create record with old hash
            record = DocumentRecord(
                filepath=filepath,
                file_hash="old_hash_123",
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )
            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={filepath: record},
                version="1.0.0"
            )

            # Modify file
            with open(filepath, 'w') as f:
                f.write("Modified content")

            assert needs_processing(filepath, manifest) is True
        finally:
            os.unlink(filepath)

    def test_nonexistent_file_no_processing(self):
        """Test that non-existent files don't need processing."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )
        assert needs_processing("/nonexistent/file.pdf", manifest) is False


class TestAddDocumentRecord:
    """Tests for add_document_record function."""

    def test_add_new_record(self):
        """Test adding a new document record."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        record = DocumentRecord(
            filepath="test.pdf",
            file_hash="abc123",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        add_document_record(manifest, record)

        assert "test.pdf" in manifest.documents
        assert manifest.documents["test.pdf"].file_hash == "abc123"

    def test_update_existing_record(self):
        """Test updating an existing document record."""
        old_record = DocumentRecord(
            filepath="test.pdf",
            file_hash="old_hash",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={"test.pdf": old_record},
            version="1.0.0"
        )

        new_record = DocumentRecord(
            filepath="test.pdf",
            file_hash="new_hash",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        add_document_record(manifest, new_record)

        assert manifest.documents["test.pdf"].file_hash == "new_hash"

    def test_add_multiple_records(self):
        """Test adding multiple document records."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        for i in range(3):
            record = DocumentRecord(
                filepath=f"test{i}.pdf",
                file_hash=f"hash{i}",
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )
            add_document_record(manifest, record)

        assert len(manifest.documents) == 3


class TestGetDocumentsByType:
    """Tests for get_documents_by_type function."""

    def test_filter_by_type(self):
        """Test filtering documents by type."""
        record1 = DocumentRecord(
            filepath="resume.pdf",
            file_hash="hash1",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )
        record2 = DocumentRecord(
            filepath="cover.pdf",
            file_hash="hash2",
            document_type="cover_letter",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )
        record3 = DocumentRecord(
            filepath="resume2.pdf",
            file_hash="hash3",
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={
                "resume.pdf": record1,
                "cover.pdf": record2,
                "resume2.pdf": record3
            },
            version="1.0.0"
        )

        resumes = get_documents_by_type(manifest, DocumentType.RESUME)
        assert len(resumes) == 2

        covers = get_documents_by_type(manifest, DocumentType.COVER_LETTER)
        assert len(covers) == 1

    def test_empty_results(self):
        """Test filtering with no matches."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        results = get_documents_by_type(manifest, DocumentType.RESUME)
        assert len(results) == 0


class TestGetFilesToProcess:
    """Tests for get_files_to_process function."""

    def test_scan_directory(self):
        """Test scanning directory for files."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = os.path.join(tmpdir, "test1.pdf")
            file2 = os.path.join(tmpdir, "test2.docx")

            with open(file1, 'w') as f:
                f.write("test")
            with open(file2, 'w') as f:
                f.write("test")

            files = get_files_to_process(tmpdir, manifest)
            assert len(files) == 2

    def test_filter_by_extension(self):
        """Test filtering files by extension."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            pdf_file = os.path.join(tmpdir, "test.pdf")
            txt_file = os.path.join(tmpdir, "test.txt")
            docx_file = os.path.join(tmpdir, "test.docx")

            for filepath in [pdf_file, txt_file, docx_file]:
                with open(filepath, 'w') as f:
                    f.write("test")

            # Only get PDF files
            files = get_files_to_process(tmpdir, manifest, ['.pdf'])
            assert len(files) == 1
            assert files[0].endswith('.pdf')

            # Get PDF and DOCX files
            files = get_files_to_process(tmpdir, manifest, ['.pdf', '.docx'])
            assert len(files) == 2

    def test_skip_processed_files(self):
        """Test that already-processed unchanged files are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            filepath = os.path.join(tmpdir, "test.pdf")
            with open(filepath, 'w') as f:
                f.write("test content")

            # Add to manifest
            file_hash = compute_file_hash(filepath)
            record = DocumentRecord(
                filepath=filepath,
                file_hash=file_hash,
                document_type="resume",
                date_processed=datetime.now().isoformat(),
                date_from_filename=None,
                extraction_success=True
            )
            manifest = ProcessingManifest(
                last_updated=datetime.now().isoformat(),
                documents={filepath: record},
                version="1.0.0"
            )

            files = get_files_to_process(tmpdir, manifest)
            assert len(files) == 0

    def test_nonexistent_directory(self):
        """Test scanning non-existent directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        files = get_files_to_process("/nonexistent/dir", manifest)
        assert len(files) == 0
