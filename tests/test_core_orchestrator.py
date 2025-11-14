"""
Tests for orchestrator module.

This module tests document processing orchestration, workflow, and integration.
Currently 0% coverage (143 lines untested).
"""

import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

from core.orchestrator import (
    process_documents,
    get_document_hash,
    is_document_modified
)
from core.state_manager import (
    ProcessingManifest,
    DocumentRecord
)
from core.document_processor import DocumentType


class TestProcessDocuments:
    """Tests for process_documents function."""

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    @patch('core.orchestrator.extract_date_from_filename')
    @patch('core.orchestrator.classify_document')
    @patch('core.orchestrator.compute_file_hash')
    def test_process_documents_basic(
        self,
        mock_hash,
        mock_classify,
        mock_date,
        mock_extract,
        mock_get_files
    ):
        """Test basic document processing workflow."""
        # Setup
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = ['/path/to/resume.pdf']
        mock_extract.return_value = {
            'success': True,
            'text': 'Resume content with experience and skills'
        }
        mock_date.return_value = None
        mock_classify.return_value = (DocumentType.RESUME, 0.95, 'filename')
        mock_hash.return_value = 'abc123'

        # Execute
        result = process_documents('/input/dir', manifest)

        # Verify
        assert len(result) == 1
        assert result[0]['text'] == 'Resume content with experience and skills'
        assert result[0]['filepath'] == '/path/to/resume.pdf'
        assert result[0]['doc_type'] == DocumentType.RESUME
        assert 'date' not in result[0]  # No date extracted

        # Verify manifest updated
        assert '/path/to/resume.pdf' in manifest.documents

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    @patch('core.orchestrator.extract_date_from_filename')
    @patch('core.orchestrator.classify_document')
    @patch('core.orchestrator.compute_file_hash')
    def test_process_documents_with_date(
        self,
        mock_hash,
        mock_classify,
        mock_date,
        mock_extract,
        mock_get_files
    ):
        """Test document processing with date extraction."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        from datetime import date
        test_date = date(2024, 3, 15)

        mock_get_files.return_value = ['/path/to/2024-03-15-resume.pdf']
        mock_extract.return_value = {
            'success': True,
            'text': 'Resume content'
        }
        mock_date.return_value = test_date
        mock_classify.return_value = (DocumentType.RESUME, 0.95, 'filename')
        mock_hash.return_value = 'abc123'

        result = process_documents('/input/dir', manifest)

        assert len(result) == 1
        assert result[0]['date'] == test_date

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    def test_process_documents_extraction_failure(
        self,
        mock_extract,
        mock_get_files
    ):
        """Test handling of text extraction failures."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = ['/path/to/corrupted.pdf']
        mock_extract.return_value = {
            'success': False,
            'error': 'Failed to decode PDF'
        }

        result = process_documents('/input/dir', manifest)

        # Failed extraction should be skipped
        assert len(result) == 0

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    def test_process_documents_empty_text(
        self,
        mock_extract,
        mock_get_files
    ):
        """Test skipping documents with empty text."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = ['/path/to/empty.pdf']
        mock_extract.return_value = {
            'success': True,
            'text': '   \n\n  '  # Only whitespace
        }

        result = process_documents('/input/dir', manifest)

        # Empty documents should be skipped
        assert len(result) == 0

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    @patch('core.orchestrator.extract_date_from_filename')
    @patch('core.orchestrator.classify_document')
    @patch('core.orchestrator.compute_file_hash')
    def test_process_documents_multiple_files(
        self,
        mock_hash,
        mock_classify,
        mock_date,
        mock_extract,
        mock_get_files
    ):
        """Test processing multiple documents."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = [
            '/path/to/resume.pdf',
            '/path/to/cover-letter.pdf',
            '/path/to/job-desc.pdf'
        ]

        # Different responses for each file
        def extract_side_effect(filepath):
            if 'resume' in filepath:
                return {'success': True, 'text': 'Resume text'}
            elif 'cover' in filepath:
                return {'success': True, 'text': 'Cover letter text'}
            else:
                return {'success': True, 'text': 'Job description text'}

        def classify_side_effect(filepath, text):
            if 'resume' in filepath:
                return (DocumentType.RESUME, 0.95, 'filename')
            elif 'cover' in filepath:
                return (DocumentType.COVER_LETTER, 0.90, 'filename')
            else:
                return (DocumentType.JOB_DESCRIPTION, 0.85, 'content')

        mock_extract.side_effect = extract_side_effect
        mock_classify.side_effect = classify_side_effect
        mock_date.return_value = None
        mock_hash.return_value = 'hash'

        result = process_documents('/input/dir', manifest)

        assert len(result) == 3
        assert result[0]['doc_type'] == DocumentType.RESUME
        assert result[1]['doc_type'] == DocumentType.COVER_LETTER
        assert result[2]['doc_type'] == DocumentType.JOB_DESCRIPTION

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    def test_process_documents_exception_handling(
        self,
        mock_extract,
        mock_get_files
    ):
        """Test that exceptions during processing don't crash the workflow."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = ['/path/to/problematic.pdf']
        mock_extract.side_effect = Exception("Unexpected error")

        # Should not raise, just log and continue
        result = process_documents('/input/dir', manifest)

        assert len(result) == 0  # Failed file skipped

    @patch('core.orchestrator.get_files_to_process')
    def test_process_documents_empty_directory(
        self,
        mock_get_files
    ):
        """Test processing empty directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        mock_get_files.return_value = []

        result = process_documents('/empty/dir', manifest)

        assert len(result) == 0

    @patch('core.orchestrator.get_files_to_process')
    @patch('core.orchestrator.extract_text_from_document')
    @patch('core.orchestrator.extract_date_from_filename')
    @patch('core.orchestrator.classify_document')
    @patch('core.orchestrator.compute_file_hash')
    def test_process_documents_manifest_updated(
        self,
        mock_hash,
        mock_classify,
        mock_date,
        mock_extract,
        mock_get_files
    ):
        """Test that manifest is properly updated after processing."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        from datetime import date
        test_date = date(2024, 3, 15)

        mock_get_files.return_value = ['/path/to/resume.pdf']
        mock_extract.return_value = {'success': True, 'text': 'Content'}
        mock_date.return_value = test_date
        mock_classify.return_value = (DocumentType.RESUME, 0.95, 'filename')
        mock_hash.return_value = 'hash123'

        process_documents('/input/dir', manifest)

        # Check manifest updated correctly
        assert '/path/to/resume.pdf' in manifest.documents
        record = manifest.documents['/path/to/resume.pdf']
        assert record.file_hash == 'hash123'
        assert record.document_type == DocumentType.RESUME.value
        assert record.extraction_success is True
        assert record.date_from_filename == test_date.isoformat()


class TestGetDocumentHash:
    """Tests for get_document_hash function."""

    def test_get_document_hash(self):
        """Test getting hash of a document."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Test content for hashing")
            tmp.flush()
            tmp_path = tmp.name

        try:
            hash1 = get_document_hash(tmp_path)
            assert isinstance(hash1, str)
            assert len(hash1) == 64  # SHA-256

            # Hash should be deterministic
            hash2 = get_document_hash(tmp_path)
            assert hash1 == hash2
        finally:
            os.unlink(tmp_path)

    def test_get_document_hash_different_files(self):
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
            hash1 = get_document_hash(path1)
            hash2 = get_document_hash(path2)
            assert hash1 != hash2
        finally:
            os.unlink(path1)
            os.unlink(path2)


class TestIsDocumentModified:
    """Tests for is_document_modified function."""

    def test_is_document_modified_new_file(self):
        """Test that new files are marked as modified."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"New file content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = is_document_modified(tmp_path, manifest)
            assert result is True
        finally:
            os.unlink(tmp_path)

    def test_is_document_modified_unchanged(self):
        """Test that unchanged files are not marked as modified."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Unchanged content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            from core.state_manager import compute_file_hash

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

            result = is_document_modified(tmp_path, manifest)
            assert result is False
        finally:
            os.unlink(tmp_path)

    def test_is_document_modified_changed(self):
        """Test that modified files are detected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Original content")
            tmp.flush()
            tmp_path = tmp.name

        try:
            from core.state_manager import compute_file_hash

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

            result = is_document_modified(tmp_path, manifest)
            assert result is True
        finally:
            os.unlink(tmp_path)
