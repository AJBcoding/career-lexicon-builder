"""
Tests for the orchestrator module.
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path

from core.orchestrator import (
    process_documents,
    run_all_analyzers,
    generate_all_lexicons,
    run_full_pipeline,
    get_document_hash,
    is_document_modified,
    merge_analysis_results,
    run_incremental_update,
)
from core.state_manager import (
    ProcessingManifest,
    load_manifest,
)
from datetime import datetime


class TestProcessDocuments:
    """Tests for process_documents function."""

    def test_process_documents_basic(self, tmp_path):
        """Test basic document processing."""
        # Create test directory with sample files
        fixtures_dir = Path(__file__).parent / "fixtures"

        # Initialize empty manifest
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        # Process documents
        documents = process_documents(str(fixtures_dir), manifest)

        # Verify documents were processed
        assert len(documents) > 0

        # Check document structure
        for doc in documents:
            assert 'text' in doc
            assert 'filepath' in doc
            assert 'doc_type' in doc
            assert doc['text']  # Not empty

    def test_process_documents_empty_directory(self, tmp_path):
        """Test processing with empty directory."""
        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        documents = process_documents(str(tmp_path), manifest)

        assert documents == []

    def test_process_documents_updates_manifest(self, tmp_path):
        """Test that processing updates manifest with document records."""
        # Copy sample files to temp directory
        fixtures_dir = Path(__file__).parent / "fixtures"
        sample_file = fixtures_dir / "sample_resume.txt"
        test_file = tmp_path / "sample_resume.txt"
        shutil.copy(sample_file, test_file)

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        documents = process_documents(str(tmp_path), manifest)

        # Verify manifest was updated
        assert len(manifest.documents) > 0
        assert str(test_file) in manifest.documents


class TestRunAllAnalyzers:
    """Tests for run_all_analyzers function."""

    def test_run_all_analyzers_basic(self):
        """Test running all analyzers with sample documents."""
        documents = [
            {
                'text': 'I am passionate about software engineering and building scalable systems.',
                'filepath': 'test.txt',
                'doc_type': 'cover_letter',
            }
        ]

        results = run_all_analyzers(documents)

        # Verify all analyzer results are present
        assert 'themes' in results
        assert 'qualifications' in results
        assert 'narratives' in results
        assert 'keywords' in results

        # Verify results are lists
        assert isinstance(results['themes'], list)
        assert isinstance(results['qualifications'], list)
        assert isinstance(results['narratives'], list)
        assert isinstance(results['keywords'], list)

    def test_run_all_analyzers_empty_documents(self):
        """Test running analyzers with empty document list."""
        documents = []

        results = run_all_analyzers(documents)

        # Should return empty results for each analyzer
        assert results['themes'] == []
        assert results['qualifications'] == []
        assert results['narratives'] == []
        assert results['keywords'] == []


class TestGenerateAllLexicons:
    """Tests for generate_all_lexicons function."""

    def test_generate_all_lexicons_creates_files(self, tmp_path):
        """Test that all lexicon files are created."""
        analysis_results = {
            'themes': [],
            'qualifications': [],
            'narratives': [],
            'keywords': []
        }

        output_dir = str(tmp_path / "output")
        generate_all_lexicons(analysis_results, output_dir)

        # Verify all lexicon files were created
        assert os.path.exists(os.path.join(output_dir, "my_values.md"))
        assert os.path.exists(os.path.join(output_dir, "resume_variations.md"))
        assert os.path.exists(os.path.join(output_dir, "storytelling_patterns.md"))
        assert os.path.exists(os.path.join(output_dir, "usage_index.md"))

    def test_generate_all_lexicons_creates_output_dir(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        analysis_results = {
            'themes': [],
            'qualifications': [],
            'narratives': [],
            'keywords': []
        }

        output_dir = str(tmp_path / "new_output_dir")
        assert not os.path.exists(output_dir)

        generate_all_lexicons(analysis_results, output_dir)

        # Verify directory was created
        assert os.path.exists(output_dir)


class TestGetDocumentHash:
    """Tests for get_document_hash function."""

    def test_get_document_hash_consistent(self, tmp_path):
        """Test that hash is consistent for same file."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        # Get hash twice
        hash1 = get_document_hash(str(test_file))
        hash2 = get_document_hash(str(test_file))

        # Should be identical
        assert hash1 == hash2
        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters

    def test_get_document_hash_different_content(self, tmp_path):
        """Test that different files produce different hashes."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Content 1")
        file2.write_text("Content 2")

        hash1 = get_document_hash(str(file1))
        hash2 = get_document_hash(str(file2))

        assert hash1 != hash2


class TestIsDocumentModified:
    """Tests for is_document_modified function."""

    def test_is_document_modified_new_file(self, tmp_path):
        """Test that new file is marked as modified."""
        test_file = tmp_path / "new_file.txt"
        test_file.write_text("New content")

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        # New file should be marked as modified
        assert is_document_modified(str(test_file), manifest) is True

    def test_is_document_modified_unchanged_file(self, tmp_path):
        """Test that unchanged file is not marked as modified."""
        test_file = tmp_path / "unchanged.txt"
        test_file.write_text("Unchanged content")

        # Create manifest with file already processed
        from core.state_manager import DocumentRecord, add_document_record, compute_file_hash

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        record = DocumentRecord(
            filepath=str(test_file),
            file_hash=compute_file_hash(str(test_file)),
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )
        add_document_record(manifest, record)

        # Unchanged file should not be marked as modified
        assert is_document_modified(str(test_file), manifest) is False

    def test_is_document_modified_changed_file(self, tmp_path):
        """Test that modified file is detected."""
        test_file = tmp_path / "changed.txt"
        test_file.write_text("Original content")

        # Create manifest with original hash
        from core.state_manager import DocumentRecord, add_document_record, compute_file_hash

        manifest = ProcessingManifest(
            last_updated=datetime.now().isoformat(),
            documents={},
            version="1.0.0"
        )

        record = DocumentRecord(
            filepath=str(test_file),
            file_hash=compute_file_hash(str(test_file)),
            document_type="resume",
            date_processed=datetime.now().isoformat(),
            date_from_filename=None,
            extraction_success=True
        )
        add_document_record(manifest, record)

        # Modify the file
        test_file.write_text("Modified content")

        # Modified file should be detected
        assert is_document_modified(str(test_file), manifest) is True


class TestMergeAnalysisResults:
    """Tests for merge_analysis_results function."""

    def test_merge_empty_results(self):
        """Test merging with empty results."""
        existing = {'themes': [], 'qualifications': [], 'narratives': [], 'keywords': []}
        new = {'themes': [], 'qualifications': [], 'narratives': [], 'keywords': []}

        merged = merge_analysis_results(existing, new)

        assert merged['themes'] == []
        assert merged['qualifications'] == []
        assert merged['narratives'] == []
        assert merged['keywords'] == []

    def test_merge_new_items(self):
        """Test merging new items into empty existing."""
        existing = {'themes': [], 'qualifications': [], 'narratives': [], 'keywords': []}
        new = {
            'themes': [{'theme': 'Innovation', 'occurrences': ['text1'], 'documents': ['doc1']}],
            'qualifications': [],
            'narratives': [],
            'keywords': []
        }

        merged = merge_analysis_results(existing, new)

        assert len(merged['themes']) == 1
        assert merged['themes'][0]['theme'] == 'Innovation'

    def test_merge_duplicate_themes(self):
        """Test merging duplicate themes combines occurrences."""
        existing = {
            'themes': [{'theme': 'Innovation', 'occurrences': ['text1'], 'documents': ['doc1']}],
            'qualifications': [],
            'narratives': [],
            'keywords': []
        }
        new = {
            'themes': [{'theme': 'Innovation', 'occurrences': ['text2'], 'documents': ['doc2']}],
            'qualifications': [],
            'narratives': [],
            'keywords': []
        }

        merged = merge_analysis_results(existing, new)

        # Should have only one theme but combined data
        assert len(merged['themes']) == 1
        assert merged['themes'][0]['theme'] == 'Innovation'
        # Occurrences and documents should be combined
        assert len(merged['themes'][0]['occurrences']) == 2
        assert len(merged['themes'][0]['documents']) == 2


class TestRunIncrementalUpdate:
    """Tests for run_incremental_update function."""

    def test_run_incremental_update_no_existing_state(self, tmp_path):
        """Test incremental update falls back to full pipeline when no state exists."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")

        # Run incremental update with no existing state
        result = run_incremental_update(input_dir, output_dir)

        # Should have run successfully (falling back to full pipeline)
        assert 'success' in result
        assert 'statistics' in result

    def test_run_incremental_update_no_changes(self, tmp_path):
        """Test incremental update with no new documents."""
        # First, run full pipeline to create state
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")

        result1 = run_full_pipeline(input_dir, output_dir)
        assert result1['success']

        # Now run incremental update - should find no changes
        result2 = run_incremental_update(input_dir, output_dir)

        assert result2['success']
        assert result2['statistics']['new_documents'] == 0


class TestRunFullPipeline:
    """Tests for run_full_pipeline function."""

    def test_run_full_pipeline_basic(self, tmp_path):
        """Test full pipeline execution."""
        # Setup input directory with sample files
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")

        # Run pipeline
        result = run_full_pipeline(input_dir, output_dir)

        # Verify result structure
        assert 'success' in result
        assert 'errors' in result
        assert 'statistics' in result

        # Verify statistics
        stats = result['statistics']
        assert 'documents_processed' in stats
        assert 'themes_found' in stats
        assert 'qualifications_found' in stats
        assert 'narratives_found' in stats
        assert 'keywords_found' in stats

        # Verify documents were processed
        assert stats['documents_processed'] > 0

    def test_run_full_pipeline_creates_lexicons(self, tmp_path):
        """Test that pipeline creates all lexicon files."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")

        result = run_full_pipeline(input_dir, output_dir)

        # Verify all lexicons were created
        assert os.path.exists(os.path.join(output_dir, "my_values.md"))
        assert os.path.exists(os.path.join(output_dir, "resume_variations.md"))
        assert os.path.exists(os.path.join(output_dir, "storytelling_patterns.md"))
        assert os.path.exists(os.path.join(output_dir, "usage_index.md"))

    def test_run_full_pipeline_creates_state_file(self, tmp_path):
        """Test that pipeline creates state file."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")

        result = run_full_pipeline(input_dir, output_dir)

        # Verify state file was created
        state_file = os.path.join(output_dir, ".state.json")
        assert os.path.exists(state_file)

        # Verify state file can be loaded
        manifest = load_manifest(state_file)
        assert manifest is not None
        assert len(manifest.documents) > 0

    def test_run_full_pipeline_empty_directory(self, tmp_path):
        """Test pipeline with empty input directory."""
        input_dir = str(tmp_path / "empty_input")
        os.makedirs(input_dir)
        output_dir = str(tmp_path / "output")

        result = run_full_pipeline(input_dir, output_dir)

        # Should still succeed but with no documents processed
        assert result['success'] is False  # Because no documents processed
        assert result['statistics']['documents_processed'] == 0
        assert "No documents processed" in result['errors']

    def test_run_full_pipeline_with_custom_state_file(self, tmp_path):
        """Test pipeline with custom state file path."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        input_dir = str(fixtures_dir)
        output_dir = str(tmp_path / "output")
        state_file = str(tmp_path / "custom_state.json")

        result = run_full_pipeline(input_dir, output_dir, state_file=state_file)

        # Verify custom state file was created
        assert os.path.exists(state_file)
