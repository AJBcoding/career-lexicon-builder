"""Convert PDF to images using Poppler."""
import subprocess
import shutil
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Converts PDF to images using pdftoppm."""

    def is_available(self) -> bool:
        """Check if pdftoppm is available."""
        return shutil.which('pdftoppm') is not None

    def generate_images(self, pdf_path: str, output_dir: str,
                       dpi: int = 150) -> List[Path]:
        """
        Convert PDF pages to JPEG images.

        Args:
            pdf_path: Input PDF file
            output_dir: Directory for output images
            dpi: Resolution (default 150)

        Returns:
            List of generated image paths
        """
        if not self.is_available():
            logger.warning("pdftoppm not available - skipping image generation")
            return []

        try:
            pdf_path = Path(pdf_path)
            output_dir = Path(output_dir)

            if not pdf_path.exists():
                logger.error(f"PDF not found: {pdf_path}")
                return []

            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)

            # Base name for images
            base_name = output_dir / "page"

            # Convert
            result = subprocess.run([
                'pdftoppm',
                '-jpeg',
                '-r', str(dpi),
                str(pdf_path),
                str(base_name)
            ], capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                logger.error(f"Image generation failed: {result.stderr}")
                return []

            # Find generated images
            images = sorted(output_dir.glob('page-*.jpg'))

            logger.info(f"Generated {len(images)} images")
            return images

        except subprocess.TimeoutExpired:
            logger.error("Image generation timed out")
            return []
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return []
