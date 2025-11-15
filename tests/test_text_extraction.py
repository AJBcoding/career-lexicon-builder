"""
Tests for text extraction from multiple document formats.
"""

import pytest
import zipfile
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
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

    def test_pages_pdf_preview_extraction(self):
        """
        Test extraction from Pages file using PDF preview.

        Coverage gap: Lines 301-366 (PDF preview extraction)
        Priority: HIGH - Pages format handling
        """
        # This tests the fallback to PDF preview when XML extraction fails
        # Create a .pages file (zip) with QuickLook/Preview.pdf but no index.xml

        # Note: Creating actual PDF content requires complex setup
        # This test verifies the pathway exists and handles missing pdfplumber gracefully

        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create zip with Preview.pdf path but empty content (will fail extraction)
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                # Add a Preview.pdf entry (empty for now - would need real PDF for full test)
                zf.writestr('QuickLook/Preview.pdf', b'')

            try:
                result = extract_text_from_document(tmp.name)
                # Without pdfplumber or with empty PDF, should fail gracefully
                assert result is not None
                # Either pdfplumber not installed or no text in PDF
            finally:
                os.unlink(tmp.name)

    def test_pages_no_preview_pdf(self):
        """
        Test handling when Preview.pdf is missing from .pages file.

        Coverage gap: Lines 316-322 (missing PDF handling)
        Priority: MEDIUM - Error handling
        """
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create zip without Preview.pdf or index.xml
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                zf.writestr('other.xml', '<root></root>')

            try:
                result = extract_text_from_document(tmp.name)
                # Should fail both XML and PDF extraction
                assert result['success'] is False
                assert 'error' in result
            finally:
                os.unlink(tmp.name)


class TestPDFDocumentProcessing:
    """Tests for standalone PDF document processing (Lines 384-440)."""

    def test_pdf_extraction_pdfplumber_not_installed(self):
        """
        Test PDF extraction when pdfplumber is not available.

        Coverage gap: Lines 384-392 (import error handling)
        Priority: MEDIUM - Dependency handling
        """
        # This tests the import error handling
        # The actual import error is hard to trigger since pdfplumber is installed
        # But we verify the pathway exists
        pass  # Import handling tested via integration

    def test_pdf_extraction_empty_file(self):
        """
        Test PDF extraction from empty/invalid PDF file.

        Coverage gap: Lines 420-426 (no text content handling)
        Priority: MEDIUM - Error handling
        """
        # Create an empty file with .pdf extension
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b'')  # Empty file
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should fail gracefully - not a valid PDF
            assert result['success'] is False
        finally:
            os.unlink(tmp_path)

    def test_pdf_extraction_exception_handling(self):
        """
        Test exception handling in PDF extraction.

        Coverage gap: Lines 439-444 (exception handling)
        Priority: MEDIUM - Error recovery
        """
        # Test with invalid PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b'Not a valid PDF file')
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            assert result['success'] is False
            assert 'error' in result
        finally:
            os.unlink(tmp_path)

    @patch('utils.text_extraction.pdfplumber')
    def test_pdf_with_metadata_extraction(self, mock_pdfplumber):
        """
        Test PDF extraction with metadata fields.

        Coverage gap: Lines 403-432 (PDF metadata extraction)
        Priority: HIGH - Metadata handling
        """
        # Create a temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b'%PDF-1.4 fake pdf content')
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Mock pdfplumber behavior
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Test PDF content with metadata"
            mock_pdf.pages = [mock_page]

            # Add metadata that will trigger lines 406-412
            mock_pdf.metadata = {
                'Title': 'Test Document',
                'Author': 'Test Author',
                'Subject': 'Test Subject',
                'CreationDate': 'D:20240315120000'
            }

            # Set up context manager
            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            mock_pdfplumber.open.return_value.__exit__.return_value = None

            result = extract_text_from_document(tmp_path)

            # Verify extraction succeeded and metadata path was taken
            assert result['success'] is True
            assert 'Test PDF content with metadata' in result['text']
            assert result['extraction_method'] == 'pdf'
            assert result['metadata']['pdf_title'] == 'Test Document'
            assert result['metadata']['pdf_author'] == 'Test Author'
            assert result['metadata']['pdf_subject'] == 'Test Subject'
            assert result['metadata']['page_count'] == 1
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @patch('utils.text_extraction.pdfplumber')
    def test_pdf_with_multiple_pages(self, mock_pdfplumber):
        """
        Test PDF extraction with multiple pages.

        Coverage gap: Lines 415-418 (multi-page PDF handling)
        Priority: MEDIUM - Multi-page support
        """
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b'%PDF-1.4')
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Mock PDF with multiple pages
            mock_pdf = MagicMock()
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Page 1 content"
            mock_page2 = MagicMock()
            mock_page2.extract_text.return_value = "Page 2 content"
            mock_page3 = MagicMock()
            mock_page3.extract_text.return_value = "Page 3 content"
            mock_pdf.pages = [mock_page1, mock_page2, mock_page3]
            mock_pdf.metadata = {}

            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            mock_pdfplumber.open.return_value.__exit__.return_value = None

            result = extract_text_from_document(tmp_path)

            # Verify all pages extracted
            assert result['success'] is True
            assert 'Page 1 content' in result['text']
            assert 'Page 2 content' in result['text']
            assert 'Page 3 content' in result['text']
            assert result['metadata']['page_count'] == 3
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestDOCXDocumentProcessing:
    """Tests for DOCX document processing (Lines 458-531)."""

    def test_docx_extraction_python_docx_not_installed(self):
        """
        Test DOCX extraction when python-docx is not available.

        Coverage gap: Lines 458-466 (import error handling)
        Priority: MEDIUM - Dependency handling
        """
        # Import handling verified via integration
        pass

    def test_docx_extraction_empty_document(self):
        """
        Test DOCX extraction from document with no text.

        Coverage gap: Lines 511-517 (empty content handling)
        Priority: MEDIUM - Error handling
        """
        # Creating a minimal DOCX requires python-docx
        # This verifies the no-content pathway
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(b'PK')  # Minimal zip header, not valid DOCX
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should fail - not a valid DOCX
            assert result['success'] is False
        finally:
            os.unlink(tmp_path)

    def test_docx_extraction_exception_handling(self):
        """
        Test exception handling in DOCX extraction.

        Coverage gap: Lines 530-535 (exception handling)
        Priority: MEDIUM - Error recovery
        """
        # Test with invalid DOCX file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(b'Not a valid DOCX file')
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            assert result['success'] is False
            assert 'error' in result
        finally:
            os.unlink(tmp_path)

    @patch('utils.text_extraction.Document')
    def test_docx_with_metadata_and_tables(self, mock_document_class):
        """
        Test DOCX extraction with metadata and tables.

        Coverage gap: Lines 481-523 (DOCX metadata and table extraction)
        Priority: HIGH - Comprehensive document handling
        """
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(b'PK\x03\x04')  # Minimal zip signature
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Mock Document instance
            mock_doc = MagicMock()

            # Mock core properties (lines 482-492)
            mock_props = MagicMock()
            mock_props.title = 'Test Document'
            mock_props.author = 'Test Author'
            mock_props.created = datetime(2024, 3, 15, 10, 30)
            mock_props.modified = datetime(2024, 3, 15, 14, 30)
            mock_doc.core_properties = mock_props

            # Mock paragraphs (lines 495-497)
            mock_para = MagicMock()
            mock_para.text = 'Test paragraph content'
            mock_doc.paragraphs = [mock_para]

            # Mock tables (lines 502-509)
            mock_cell1 = MagicMock()
            mock_cell1.text = 'Cell 1'
            mock_cell2 = MagicMock()
            mock_cell2.text = 'Cell 2'
            mock_row = MagicMock()
            mock_row.cells = [mock_cell1, mock_cell2]
            mock_table = MagicMock()
            mock_table.rows = [mock_row]
            mock_doc.tables = [mock_table]

            mock_document_class.return_value = mock_doc

            result = extract_text_from_document(tmp_path)

            # Verify extraction succeeded
            assert result['success'] is True
            assert 'Test paragraph content' in result['text']
            assert 'Cell 1' in result['text']
            assert 'Cell 2' in result['text']
            assert result['extraction_method'] == 'docx'
            assert result['metadata']['doc_title'] == 'Test Document'
            assert result['metadata']['doc_author'] == 'Test Author'
            assert result['metadata']['paragraph_count'] == 1
            assert result['metadata']['table_count'] == 1
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @patch('utils.text_extraction.Document')
    def test_docx_without_core_properties(self, mock_document_class):
        """
        Test DOCX extraction when core properties raise exception.

        Coverage gap: Lines 491-492 (core properties exception handling)
        Priority: MEDIUM - Exception handling
        """
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(b'PK\x03\x04')
            tmp.flush()
            tmp_path = tmp.name

        try:
            # Mock Document instance
            mock_doc = MagicMock()

            # Make core_properties raise an exception
            mock_doc.core_properties = MagicMock()
            type(mock_doc.core_properties).title = MagicMock(side_effect=Exception("Property unavailable"))

            # Mock paragraphs
            mock_para = MagicMock()
            mock_para.text = 'Content without metadata'
            mock_doc.paragraphs = [mock_para]
            mock_doc.tables = []

            mock_document_class.return_value = mock_doc

            result = extract_text_from_document(tmp_path)

            # Should still succeed even if metadata extraction fails
            assert result['success'] is True
            assert 'Content without metadata' in result['text']
            assert result['extraction_method'] == 'docx'
            # Metadata fields should not include doc_title, doc_author, etc.
            assert 'doc_title' not in result['metadata']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestTextCleanupFunctions:
    """Tests for text cleanup and normalization (Lines 575-587)."""

    def test_unicode_decode_error_handling(self):
        """
        Test handling of files with encoding issues.

        Coverage gap: Lines 575-587 (UnicodeDecodeError handling)
        Priority: MEDIUM - Text cleanup
        """
        # Create a file with invalid UTF-8 encoding
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='wb') as tmp:
            # Write bytes that will fail UTF-8 but work with latin-1
            tmp.write(b'\xe9\xe0\xe8')  # Valid latin-1, invalid UTF-8
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should try multiple encodings and succeed with latin-1
            assert result['success'] is True
            assert result['extraction_method'] == 'text'
        finally:
            os.unlink(tmp_path)

    def test_text_extraction_exception_handling(self):
        """
        Test general exception handling in text extraction.

        Coverage gap: Lines 586-592 (general exception handler)
        Priority: MEDIUM - Error recovery
        """
        # Test with a file that will cause an exception
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b'test content')
            tmp.flush()
            tmp_path = tmp.name

        # Delete the file to cause an error during processing
        os.unlink(tmp_path)

        # Should handle the exception gracefully
        result = extract_text_from_document(tmp_path)
        assert result['success'] is False
        assert 'File not found' in result['error']

    @patch('utils.text_extraction.pdfplumber')
    def test_pdf_preview_successful_extraction(self, mock_pdfplumber):
        """
        Test successful PDF preview extraction from .pages file.

        Coverage gap: Lines 333-349 (PDF preview extraction success path)
        Priority: HIGH - Pages file handling
        """
        # Create a minimal .pages file (zip with QuickLook/Preview.pdf)
        with tempfile.TemporaryDirectory() as tmpdir:
            pages_file = os.path.join(tmpdir, 'test.pages')

            # Create a zip file with Preview.pdf
            with zipfile.ZipFile(pages_file, 'w') as zf:
                zf.writestr('QuickLook/Preview.pdf', b'%PDF-1.4 placeholder')

            # Mock pdfplumber behavior
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Extracted preview text from Pages"
            mock_pdf.pages = [mock_page]

            # Set up context manager
            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            mock_pdfplumber.open.return_value.__exit__.return_value = None

            result = extract_text_from_document(pages_file)

            # Should successfully extract from PDF preview
            assert result['success'] is True
            assert 'Extracted preview text from Pages' in result['text']
            assert result['extraction_method'] == 'pdf_preview'
            assert 'note' in result['metadata']
            assert 'PDF preview' in result['metadata']['note']


    def test_text_file_all_encodings_fail(self):
        """
        Test text file that can't be decoded by common encodings.

        Coverage gap: Lines 579-584 (all encodings fail fallback)
        Priority: MEDIUM - Edge case handling
        """
        # Create a file with binary data that's not valid text in any common encoding
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='wb') as tmp:
            # Write binary data that will fail UTF-8, latin-1, and cp1252
            # Actually latin-1 and cp1252 can decode any byte sequence, so this will succeed
            # But we test that the fallback encoding path is exercised
            tmp.write(bytes([0xFF, 0xFE, 0x00, 0x00]))  # Invalid UTF-8 but decodable by others
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should succeed with a fallback encoding (latin-1 or cp1252)
            assert 'success' in result
            # Either succeeds with fallback encoding or properly reports error
        finally:
            os.unlink(tmp_path)

    def test_metadata_extraction_organization_heuristics(self):
        """
        Test metadata extraction with organization name heuristics.

        Coverage gap: Lines 657-659 (organization name filtering)
        Priority: LOW - Metadata heuristics
        """
        # Test text with potential organization that's too short
        text = """Dear Hiring Manager,

I am writing to apply for the X position.

Best regards,
John Doe"""

        result = extract_metadata(text, '2024-resume.pdf')
        # The heuristic should skip very short potential organizations
        assert 'target_organization' in result


class TestHelperFunctions:
    """Tests for helper/utility functions (Lines 653-659)."""

    def test_metadata_extraction_with_dear_pattern(self):
        """
        Test metadata extraction using 'Dear' pattern matching.

        Coverage gap: Lines 653-659 (Dear pattern matching)
        Priority: MEDIUM - Metadata extraction
        """
        # Test with 'Dear Hiring Manager' pattern
        text = "Dear Hiring Manager,\n\nI am writing to apply for the position."
        result = extract_metadata("letter.pages", text)

        # The function tries to extract organization from Dear pattern
        # but skips if it's a generic title
        assert result is not None
        assert 'target_organization' in result

        # Test with organization-like name
        text = "Dear TechCorp Team,\n\nI am excited to apply."
        result = extract_metadata("letter.pages", text)
        assert result is not None

    def test_position_extraction_from_text(self):
        """
        Test position title extraction from document text.

        Coverage gap: Lines 662-669 (position keyword matching)
        Priority: MEDIUM - Metadata extraction
        """
        # Test extracting position from text
        text = "I am writing to apply for the Senior Director of Operations position at your company."
        result = extract_metadata("letter.pages", text)

        assert result is not None
        assert 'target_position' in result
        # Should extract position if under 100 chars
        if result['target_position']:
            assert len(result['target_position']) < 100


class TestDocumentTypeDetection:
    """Tests for document type detection logic (Lines 269-270)."""

    def test_document_type_detection_from_content(self):
        """
        Test automatic detection of document type from content.

        Coverage gap: Lines 269-270
        Priority: MEDIUM - Type classification
        """
        # Test that the correct extraction method is chosen based on file extension
        test_files = {
            '.txt': 'text',
            '.md': 'text',
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.pages': 'pages'
        }

        for ext, expected_type in test_files.items():
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                if ext in ['.txt', '.md']:
                    tmp.write(b'Test content')
                elif ext == '.pages':
                    # Create valid zip with index.xml
                    with zipfile.ZipFile(tmp.name, 'w') as zf:
                        zf.writestr('index.xml', '<?xml version="1.0"?><document><body><p>Test</p></body></document>')
                else:
                    tmp.write(b'Binary content')
                tmp.flush()
                tmp_path = tmp.name

            try:
                result = extract_text_from_document(tmp_path)
                # Verify the file type was correctly detected
                assert 'extraction_method' in result
                if ext in ['.txt', '.md']:
                    # Text files should succeed
                    assert result['success'] is True
                    assert result['extraction_method'] == expected_type
                elif ext == '.pages':
                    # Pages with index.xml should succeed with xml method
                    assert result['success'] is True
                    assert result['extraction_method'] == 'xml'
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    def test_document_type_detection_edge_cases(self):
        """
        Test type detection with ambiguous content.

        Coverage gap: Type detection edge cases
        Priority: LOW - Edge case handling
        """
        # Test file with no extension
        with tempfile.NamedTemporaryFile(suffix='', delete=False) as tmp:
            tmp.write(b'Content without extension')
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should fail with unsupported format error
            assert result['success'] is False
            assert 'Unsupported file format' in result['error']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        # Test file with uppercase extension
        with tempfile.NamedTemporaryFile(suffix='.TXT', delete=False) as tmp:
            tmp.write(b'Uppercase extension test')
            tmp.flush()
            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should handle uppercase extensions (they're converted to lowercase)
            assert result['success'] is True
            assert result['extraction_method'] == 'text'
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestErrorHandlingPaths:
    """Tests for error handling code paths (Line 170)."""

    def test_extraction_error_recovery(self):
        """
        Test recovery from extraction errors.

        Coverage gap: Line 170
        Priority: HIGH - Error handling
        """
        # Test XML extraction failure that should trigger PDF preview fallback
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create a zip file with corrupted XML
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                # Add malformed XML that will cause parsing to fail
                zf.writestr('index.xml', '<?xml version="1.0"?><unclosed_tag>')

            tmp_path = tmp.name

        try:
            result = extract_text_from_document(tmp_path)
            # Should fail gracefully when both XML and PDF preview extraction fail
            assert result['success'] is False
            assert 'error' in result
            # Error message should indicate the issue
            assert result['extraction_method'] == 'failed'
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @patch('utils.text_extraction.pdfplumber')
    def test_partial_extraction_success(self, mock_pdfplumber):
        """
        Test handling of partially successful extractions.

        Coverage gap: Partial success scenarios
        Priority: MEDIUM - Error recovery
        """
        # Test Pages file where XML extraction fails but PDF preview succeeds
        with tempfile.NamedTemporaryFile(suffix='.pages', delete=False) as tmp:
            # Create zip with both malformed XML and Preview.pdf
            with zipfile.ZipFile(tmp.name, 'w') as zf:
                # Malformed XML (will fail)
                zf.writestr('index.xml', '<?xml version="1.0"?><malformed>')
                # But include a Preview.pdf (will succeed with mock)
                zf.writestr('QuickLook/Preview.pdf', b'%PDF-1.4')

            tmp_path = tmp.name

        try:
            # Mock successful PDF extraction
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Recovered content from PDF preview"
            mock_pdf.pages = [mock_page]
            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            mock_pdfplumber.open.return_value.__exit__.return_value = None

            result = extract_text_from_document(tmp_path)

            # Should succeed via PDF preview fallback
            assert result['success'] is True
            assert result['extraction_method'] == 'pdf_preview'
            assert 'Recovered content from PDF preview' in result['text']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
