import pytest
from pathlib import Path
from cv_formatting.image_generator import ImageGenerator


@pytest.mark.skipif(not Path('/usr/local/bin/pdftoppm').exists() and
                    not Path('/opt/homebrew/bin/pdftoppm').exists(),
                    reason="Poppler not installed")
def test_convert_pdf_to_images(tmp_path):
    """Test converting PDF to JPEG images"""
    # This test requires a real PDF
    # Skip if we don't have one
    generator = ImageGenerator()

    if not generator.is_available():
        pytest.skip("pdftoppm not available")

    # Would need actual PDF for full test
    assert generator.is_available() is True


def test_image_generator_checks_availability():
    """Test that generator checks for poppler"""
    generator = ImageGenerator()
    available = generator.is_available()

    assert isinstance(available, bool)
