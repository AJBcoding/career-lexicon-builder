"""Apply styles to document content using template."""
from docx import Document
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class StyleApplicator:
    """Applies styles to content using template document."""

    def __init__(self, template_path: str):
        """
        Initialize with template.

        Args:
            template_path: Path to cv-template.docx
        """
        self.template_path = template_path

    def apply_styles(self, content_mapping: List[Dict[str, Any]],
                     output_path: str, document_type: str = 'cv') -> bool:
        """
        Apply styles to content and save document.

        Args:
            content_mapping: List of content elements with styles
            output_path: Where to save formatted document
            document_type: Type of document ('cv' or 'cover-letter')

        Returns:
            True if successful

        Content mapping format:
            [{
                "text": "Content text",
                "style": "Style Name",
                "type": "paragraph" | "inline",
                "runs": [  # optional, for inline styling
                    {"text": "text", "style": "Style Name"}
                ]
            }]
        """
        try:
            # Load template
            doc = Document(self.template_path)

            # Apply each content element
            for item in content_mapping:
                self._add_content_item(doc, item)

            # Save formatted document
            doc.save(output_path)
            logger.info(f"Document saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply styles: {e}")
            return False

    def _add_content_item(self, doc: Document, item: Dict[str, Any]):
        """Add single content item to document."""
        item_type = item.get('type', 'paragraph')

        if item_type == 'paragraph':
            # Add paragraph with style
            style_name = item.get('style', 'Body Text')

            # Check if item has inline runs
            if 'runs' in item:
                para = doc.add_paragraph(style=style_name)
                for run_data in item['runs']:
                    run = para.add_run(run_data['text'])
                    if run_data.get('style'):
                        run.style = run_data['style']
            else:
                # Simple paragraph
                doc.add_paragraph(item['text'], style=style_name)
