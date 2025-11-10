import pytest
from pathlib import Path
from cv_formatting.pdf_converter import PDFConverter


@pytest.mark.skipif(not Path('/usr/local/bin/soffice').exists() and
                    not Path('/Applications/LibreOffice.app').exists(),
                    reason="LibreOffice not installed")
def test_convert_docx_to_pdf(tmp_path):
    """Test converting .docx to PDF"""
    # Create test .docx (or use existing)
    template = Path.home() / ".claude/skills/career/format-resume/cv-template.docx"

    if not template.exists():
        pytest.skip("Template not available")

    output_pdf = tmp_path / "test.pdf"

    converter = PDFConverter()
    result = converter.convert_to_pdf(str(template), str(output_pdf))

    if converter.is_available():
        assert result is True
        assert output_pdf.exists()
    else:
        assert result is False


def test_pdf_converter_checks_availability():
    """Test that converter checks for LibreOffice"""
    converter = PDFConverter()
    available = converter.is_available()

    assert isinstance(available, bool)
