"""
Tests for text extraction from multiple document formats.
"""

import pytest
import zipfile
import tempfile
import os
from pathlib import Path
from utils.text_extraction import (
    extract_text_from_document,
    extract_metadata,
    get_extraction_instructions,
    ExtractionResult,
    FormattingSpan,
    BulletPoint,
    SUPPORTED_EXTENSIONS
)


class TestExtractTextFromDocument:
    """Tests for extract_text_from_document function."""

    def test_file_not_found(self):
        """Test extraction from non-existent file."""
        result = extract_text_from_document("nonexistent.pages")
        assert result['success'] is False
        assert 'File not found' in result['error']
        assert result['extraction_method'] == 'failed'

    def test_unsupported_format(self):
        """Test extraction from unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx') as tmp:
            tmp.write(b'some content')
            tmp.flush()
            result = extract_text_from_document(tmp.name)
            assert result['success'] is False
            assert 'Unsupported file format' in result['error']

    def test_invalid_pages_file(self):
        """Test extraction from file that's not a zip archive."""
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            tmp.write(b'not a zip file')
            tmp.flush()

            try:
                result = extract_text_from_document(tmp.name)
                assert result['success'] is False
                assert 'not a zip archive' in result['error']
            finally:
                os.unlink(tmp.name)

    def test_xml_extraction_no_index_xml(self):
        """Test XML extraction when index.xml is missing."""
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create a valid zip but without index.xml
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('other.xml', '<root></root>')

            try:
                result = extract_text_from_document(tmp.name)
                # Should fail both XML and PDF extraction
                assert result['success'] is False
            finally:
                os.unlink(tmp.name)

    def test_xml_extraction_success(self):
        """Test successful XML extraction from old format .pages file."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<document>
    <body>
        <p>This is a test paragraph.</p>
        <p>This is another paragraph.</p>
    </body>
</document>'''

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('index.xml', xml_content)

            try:
                result = extract_text_from_document(tmp.name)
                assert result['success'] is True
                assert result['extraction_method'] == 'xml'
                assert 'This is a test paragraph' in result['text']
                assert 'This is another paragraph' in result['text']
                assert 'metadata' in result
                assert 'file_hash' in result['metadata']
            finally:
                os.unlink(tmp.name)

    def test_xml_extraction_with_bullets(self):
        """Test XML extraction preserves bullet points."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<document>
    <body>
        <p>Regular paragraph.</p>
        <list>
            <list-item>First bullet point</list-item>
            <list-item>Second bullet point</list-item>
        </list>
    </body>
</document>'''

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('index.xml', xml_content)

            try:
                result = extract_text_from_document(tmp.name)
                assert result['success'] is True
                assert '•' in result['text']  # Bullet marker
                assert 'First bullet point' in result['text']
                assert 'Second bullet point' in result['text']
                # Check formatting metadata
                assert len(result['formatting']['bullets']) == 2
            finally:
                os.unlink(tmp.name)

    def test_xml_extraction_with_namespaces(self):
        """Test XML extraction handles namespaced elements."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<document xmlns="http://example.com/ns">
    <body>
        <p>Namespaced paragraph.</p>
    </body>
</document>'''

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('index.xml', xml_content)

            try:
                result = extract_text_from_document(tmp.name)
                assert result['success'] is True
                assert 'Namespaced paragraph' in result['text']
            finally:
                os.unlink(tmp.name)

    def test_xml_extraction_empty_content(self):
        """Test XML extraction with no text content."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<document>
    <metadata></metadata>
</document>'''

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('index.xml', xml_content)

            try:
                result = extract_text_from_document(tmp.name)
                # Should fail if no text found (either XML reports no content or falls back to PDF which also fails)
                assert result['success'] is False
                assert result['error'] is not None
            finally:
                os.unlink(tmp.name)

    def test_pdf_preview_extraction_missing_pdfplumber(self, monkeypatch):
        """Test PDF extraction fails gracefully when pdfplumber not installed."""
        # Mock import error for pdfplumber
        import sys
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create zip without index.xml (so XML extraction fails)
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('QuickLook/Preview.pdf', b'fake pdf')

            try:
                # Temporarily remove pdfplumber if it exists
                pdfplumber_backup = sys.modules.get('pdfplumber')
                if 'pdfplumber' in sys.modules:
                    del sys.modules['pdfplumber']

                # Mock the import to raise ImportError
                import builtins
                real_import = builtins.__import__

                def mock_import(name, *args, **kwargs):
                    if name == 'pdfplumber':
                        raise ImportError("No module named 'pdfplumber'")
                    return real_import(name, *args, **kwargs)

                monkeypatch.setattr(builtins, '__import__', mock_import)

                result = extract_text_from_document(tmp.name)
                assert result['success'] is False
                # Either failed on XML or PDF extraction

                # Restore pdfplumber
                if pdfplumber_backup:
                    sys.modules['pdfplumber'] = pdfplumber_backup
            finally:
                os.unlink(tmp.name)


class TestPDFExtraction:
    """Tests for PDF extraction."""

    def test_pdf_extraction_simple(self):
        """Test extraction from a simple text file (as PDF substitute for testing)."""
        # Note: Creating actual PDFs in tests is complex
        # This test verifies the extraction pathway exists
        # Real PDF testing would require sample PDF files
        pass  # Placeholder - requires pdfplumber and test PDF files


class TestDOCXExtraction:
    """Tests for DOCX extraction."""

    def test_docx_extraction_simple(self):
        """Test extraction from DOCX file."""
        # Note: Creating actual DOCX files in tests requires python-docx
        # This test verifies the extraction pathway exists
        pass  # Placeholder - requires python-docx and test files


class TestTextExtraction:
    """Tests for plain text extraction."""

    def test_text_file_utf8(self):
        """Test extraction from UTF-8 text file."""
        content = "This is a test document.\n\nSecond paragraph."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp.flush()
            tmp_path = tmp.name

            try:
                result = extract_text_from_document(tmp_path)
                assert result['success'] is True
                assert result['extraction_method'] == 'text'
                assert content in result['text']
                assert result['metadata']['encoding'] == 'utf-8'
            finally:
                os.unlink(tmp_path)

    def test_markdown_file(self):
        """Test extraction from markdown file."""
        content = "# Heading\n\nThis is **bold** text."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp.flush()
            tmp_path = tmp.name

            try:
                result = extract_text_from_document(tmp_path)
                assert result['success'] is True
                assert result['extraction_method'] == 'text'
                assert 'Heading' in result['text']
                assert 'bold' in result['text']
            finally:
                os.unlink(tmp_path)

    def test_empty_text_file(self):
        """Test extraction from empty text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write("")
            tmp.flush()
            tmp_path = tmp.name

            try:
                result = extract_text_from_document(tmp_path)
                # Empty file should still succeed but with empty text
                assert result['success'] is True
                assert result['text'] == ""
            finally:
                os.unlink(tmp_path)


class TestSupportedExtensions:
    """Tests for supported extensions."""

    def test_supported_extensions_list(self):
        """Test that SUPPORTED_EXTENSIONS contains expected formats."""
        assert '.pages' in SUPPORTED_EXTENSIONS
        assert '.pdf' in SUPPORTED_EXTENSIONS
        assert '.docx' in SUPPORTED_EXTENSIONS
        assert '.txt' in SUPPORTED_EXTENSIONS
        assert '.md' in SUPPORTED_EXTENSIONS

    def test_supported_extensions_types(self):
        """Test that extensions map to correct types."""
        assert SUPPORTED_EXTENSIONS['.pages'] == 'pages'
        assert SUPPORTED_EXTENSIONS['.pdf'] == 'pdf'
        assert SUPPORTED_EXTENSIONS['.docx'] == 'docx'
        assert SUPPORTED_EXTENSIONS['.txt'] == 'text'
        assert SUPPORTED_EXTENSIONS['.md'] == 'text'


class TestExtractMetadata:
    """Tests for extract_metadata function."""

    def test_metadata_from_filename(self):
        """Test metadata extraction from filename."""
        result = extract_metadata(
            "2024-03-15-cover-letter-university-dean.pages",
            ""
        )

        assert result['filename'] == "2024-03-15-cover-letter-university-dean.pages"
        assert result['date'] == "2024-03-15"
        assert 'university' in result['target_organization'].lower()

    def test_metadata_from_text_dear(self):
        """Test metadata extraction from 'Dear' salutation."""
        text = "Dear Hiring Manager at TechCorp,\n\nI am writing to apply..."
        result = extract_metadata("2024-01-15.pages", text)  # Use filename without misleading parts

        assert result['target_organization'] is not None
        assert 'TechCorp' in result['target_organization']

    def test_metadata_position_from_text(self):
        """Test position extraction from text content."""
        text = "I am writing to apply for the Senior Director position at your organization."
        result = extract_metadata("letter.pages", text)

        assert result['target_position'] is not None
        assert 'director' in result['target_position'].lower()

    def test_metadata_no_date(self):
        """Test metadata when no date in filename."""
        result = extract_metadata("cover-letter.pages", "")
        assert result['date'] is None

    def test_metadata_complex_filename(self):
        """Test metadata from complex filename."""
        result = extract_metadata(
            "2023-11-cv-nonprofit-program-director.pages",
            ""
        )

        assert result['date'] == "2023-11-01"
        assert result['target_organization'] is not None

    def test_metadata_position_too_long(self):
        """Test position extraction ignores unreasonably long matches."""
        text = "I am interested in the " + ("very " * 50) + "long position title that goes on forever."
        result = extract_metadata("letter.pages", text)

        # Should not extract extremely long position strings
        if result['target_position']:
            assert len(result['target_position']) < 100


class TestDataClasses:
    """Tests for data classes."""

    def test_formatting_span(self):
        """Test FormattingSpan dataclass."""
        span = FormattingSpan(start=0, end=10, bold=True)
        assert span.start == 0
        assert span.end == 10
        assert span.bold is True
        assert span.italic is False

    def test_bullet_point(self):
        """Test BulletPoint dataclass."""
        bullet = BulletPoint(text="Test bullet", level=1)
        assert bullet.text == "Test bullet"
        assert bullet.level == 1

    def test_extraction_result_defaults(self):
        """Test ExtractionResult with defaults."""
        result = ExtractionResult(
            text="Test text",
            success=True,
            extraction_method='xml'
        )
        assert result.text == "Test text"
        assert result.success is True
        assert result.formatting is not None
        assert 'bold_spans' in result.formatting
        assert 'bullets' in result.formatting
        assert result.metadata is not None

    def test_extraction_result_to_dict(self):
        """Test ExtractionResult conversion to dict."""
        result = ExtractionResult(
            text="Test",
            success=True,
            extraction_method='xml'
        )
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict['text'] == "Test"
        assert result_dict['success'] is True
        assert result_dict['extraction_method'] == 'xml'


class TestGetExtractionInstructions:
    """Tests for get_extraction_instructions function."""

    def test_instructions_returned(self):
        """Test that instructions are returned."""
        instructions = get_extraction_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0

    def test_instructions_mention_manual_conversion(self):
        """Test instructions mention manual conversion."""
        instructions = get_extraction_instructions()
        assert 'manual' in instructions.lower() or 'export' in instructions.lower()

    def test_instructions_mention_formats(self):
        """Test instructions mention supported formats."""
        instructions = get_extraction_instructions()
        assert '.docx' in instructions or 'docx' in instructions.lower()
        assert '.pdf' in instructions or 'pdf' in instructions.lower()


class TestIntegration:
    """Integration tests for text extraction workflow."""

    def test_full_extraction_workflow(self):
        """Test complete extraction and metadata workflow."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<document>
    <body>
        <p>Dear Hiring Manager at TestCorp,</p>
        <p>I am applying for the Director of Engineering position.</p>
        <p>Here are my qualifications:</p>
        <list>
            <list-item>10 years of experience</list-item>
            <list-item>Strong leadership skills</list-item>
        </list>
    </body>
</document>'''

        filename = "2024-06-15-cover-letter-testcorp.pages"

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            tmp_path = tmp.name
            # Rename to match our test filename pattern
            test_path = str(Path(tmp.name).parent / filename)

            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('index.xml', xml_content)

            try:
                # Move to correct filename
                os.rename(tmp_path, test_path)

                # Extract text
                result = extract_text_from_document(test_path)
                assert result['success'] is True

                text = result['text']

                # Extract metadata
                metadata = extract_metadata(test_path, text)

                # Verify date extraction
                assert metadata['date'] == "2024-06-15"

                # Verify organization extraction
                assert metadata['target_organization'] is not None

                # Verify content extraction
                assert 'TestCorp' in text or 'testcorp' in text.lower()
                assert 'Director of Engineering' in text
                assert '10 years' in text

            finally:
                if os.path.exists(test_path):
                    os.unlink(test_path)
                elif os.path.exists(tmp_path):
                    os.unlink(tmp_path)


# ============================================================================
# COVERAGE GAP STUBS - To be implemented
# ============================================================================

class TestPagesDocumentProcessing:
    """Tests for .pages document-specific processing (Lines 301-366)."""

    @pytest.mark.skip("TODO: Implement - test Pages XML structure parsing")
    def test_pages_xml_structure_parsing(self):
        """
        Test parsing of Pages-specific XML structure.

        Coverage gap: Lines 301-366 (66 lines)
        Priority: HIGH - Pages format handling
        """
        pass

    @pytest.mark.skip("TODO: Implement - test Pages formatting preservation")
    def test_pages_formatting_preservation(self):
        """
        Test preservation of formatting from Pages documents.

        Coverage gap: Pages-specific formatting extraction
        Priority: MEDIUM - Formatting details
        """
        pass

    @pytest.mark.skip("TODO: Implement - test Pages nested elements")
    def test_pages_nested_elements_handling(self):
        """
        Test handling of nested elements in Pages XML.

        Coverage gap: Complex XML structure handling
        Priority: MEDIUM - Nested content
        """
        pass


class TestKeynoteDocumentProcessing:
    """Tests for .keynote document processing (Lines 384-440)."""

    @pytest.mark.skip("TODO: Implement - test Keynote extraction basic")
    def test_keynote_extraction_basic(self):
        """
        Test basic text extraction from Keynote files.

        Coverage gap: Lines 384-440 (57 lines)
        Priority: MEDIUM - Keynote support
        """
        pass

    @pytest.mark.skip("TODO: Implement - test Keynote slide separation")
    def test_keynote_slide_separation(self):
        """
        Test that Keynote slides are properly separated in output.

        Coverage gap: Keynote slide handling
        Priority: MEDIUM - Presentation structure
        """
        pass

    @pytest.mark.skip("TODO: Implement - test Keynote notes extraction")
    def test_keynote_notes_extraction(self):
        """
        Test extraction of speaker notes from Keynote.

        Coverage gap: Keynote notes handling
        Priority: LOW - Additional content
        """
        pass


class TestPowerPointProcessing:
    """Tests for PowerPoint document processing (Lines 458-531)."""

    @pytest.mark.skip("TODO: Implement - test PowerPoint extraction basic")
    def test_powerpoint_extraction_basic(self):
        """
        Test basic text extraction from PowerPoint files.

        Coverage gap: Lines 458-531 (74 lines)
        Priority: MEDIUM - PowerPoint support
        """
        pass

    @pytest.mark.skip("TODO: Implement - test PowerPoint slide order")
    def test_powerpoint_slide_order_preservation(self):
        """
        Test that PowerPoint slides maintain correct order.

        Coverage gap: PowerPoint slide ordering
        Priority: MEDIUM - Content organization
        """
        pass

    @pytest.mark.skip("TODO: Implement - test PowerPoint tables")
    def test_powerpoint_table_extraction(self):
        """
        Test extraction of tables from PowerPoint slides.

        Coverage gap: PowerPoint table handling
        Priority: LOW - Structured content
        """
        pass


class TestTextCleanupFunctions:
    """Tests for text cleanup and normalization (Lines 575-587)."""

    @pytest.mark.skip("TODO: Implement - test whitespace normalization")
    def test_whitespace_normalization(self):
        """
        Test normalization of excessive whitespace.

        Coverage gap: Lines 575-587 (13 lines)
        Priority: MEDIUM - Text cleanup
        """
        pass

    @pytest.mark.skip("TODO: Implement - test special character handling")
    def test_special_character_handling(self):
        """
        Test handling of special characters and encoding.

        Coverage gap: Character cleanup logic
        Priority: MEDIUM - Text quality
        """
        pass

    @pytest.mark.skip("TODO: Implement - test line break normalization")
    def test_line_break_normalization(self):
        """
        Test normalization of various line break styles.

        Coverage gap: Line break handling
        Priority: LOW - Formatting consistency
        """
        pass


class TestHelperFunctions:
    """Tests for helper/utility functions (Lines 653-659)."""

    @pytest.mark.skip("TODO: Implement - test file hash calculation")
    def test_file_hash_calculation(self):
        """
        Test file hash calculation for change detection.

        Coverage gap: Lines 653-659 (7 lines)
        Priority: MEDIUM - File tracking
        """
        pass

    @pytest.mark.skip("TODO: Implement - test path normalization")
    def test_path_normalization_helper(self):
        """
        Test path normalization helper functions.

        Coverage gap: Path handling utilities
        Priority: LOW - File path utilities
        """
        pass


class TestDocumentTypeDetection:
    """Tests for document type detection logic (Lines 269-270)."""

    @pytest.mark.skip("TODO: Implement - test type detection from content")
    def test_document_type_detection_from_content(self):
        """
        Test automatic detection of document type from content.

        Coverage gap: Lines 269-270
        Priority: MEDIUM - Type classification
        """
        pass

    @pytest.mark.skip("TODO: Implement - test type detection edge cases")
    def test_document_type_detection_edge_cases(self):
        """
        Test type detection with ambiguous content.

        Coverage gap: Type detection edge cases
        Priority: LOW - Edge case handling
        """
        pass


class TestErrorHandlingPaths:
    """Tests for error handling code paths (Line 170)."""

    @pytest.mark.skip("TODO: Implement - test extraction error recovery")
    def test_extraction_error_recovery(self):
        """
        Test recovery from extraction errors.

        Coverage gap: Line 170
        Priority: HIGH - Error handling
        """
        pass

    @pytest.mark.skip("TODO: Implement - test partial extraction success")
    def test_partial_extraction_success(self):
        """
        Test handling of partially successful extractions.

        Coverage gap: Partial success scenarios
        Priority: MEDIUM - Error recovery
        """
        pass
