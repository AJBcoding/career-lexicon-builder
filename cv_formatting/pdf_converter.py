"""Convert .docx documents to PDF using LibreOffice."""
import subprocess
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFConverter:
    """Converts .docx to PDF using LibreOffice."""

    def is_available(self) -> bool:
        """Check if LibreOffice is available."""
        return shutil.which('soffice') is not None

    def convert_to_pdf(self, docx_path: str, pdf_path: str) -> bool:
        """
        Convert .docx to PDF.

        Args:
            docx_path: Input .docx file
            pdf_path: Output .pdf file

        Returns:
            True if successful
        """
        if not self.is_available():
            logger.warning("LibreOffice not available - skipping PDF conversion")
            return False

        try:
            docx_path = Path(docx_path)
            pdf_path = Path(pdf_path)

            if not docx_path.exists():
                logger.error(f"Input file not found: {docx_path}")
                return False

            # Create output directory if needed
            pdf_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert using LibreOffice
            result = subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(pdf_path.parent),
                str(docx_path)
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error(f"Conversion failed: {result.stderr}")
                return False

            # LibreOffice creates PDF with same basename as input
            generated_pdf = pdf_path.parent / f"{docx_path.stem}.pdf"

            # Rename if needed
            if generated_pdf != pdf_path:
                generated_pdf.rename(pdf_path)

            logger.info(f"PDF created: {pdf_path}")
            return True

        except subprocess.TimeoutExpired:
            logger.error("PDF conversion timed out")
            return False
        except Exception as e:
            logger.error(f"PDF conversion error: {e}")
            return False
