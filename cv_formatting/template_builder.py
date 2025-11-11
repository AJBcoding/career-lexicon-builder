"""Build clean .docx template with semantic style names."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TemplateBuilder:
    """Builds clean .docx templates with semantic style names."""

    # Orange brand color from analysis: rgba(255,109,73,1.000)
    ORANGE_RGB = RGBColor(255, 109, 73)
    GRAY_RGB = RGBColor(128, 128, 128)

    def create_template(self, output_path: str) -> bool:
        """
        Create clean .docx template with 12 semantic styles.

        Args:
            output_path: Where to save the template

        Returns:
            True if successful
        """
        try:
            doc = Document()

            # Create paragraph styles
            self._create_cv_name_style(doc)
            self._create_section_header_style(doc)
            self._create_body_text_style(doc)
            self._create_timeline_entry_style(doc)
            self._create_bullet_standard_style(doc)
            self._create_bullet_gray_style(doc)
            self._create_bullet_emphasis_style(doc)

            # Create character styles
            self._create_play_title_style(doc)
            self._create_institution_style(doc)
            self._create_job_title_style(doc)
            self._create_orange_emphasis_style(doc)
            self._create_gray_text_style(doc)

            doc.save(output_path)
            logger.info(f"Template created: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to create template: {e}")
            return False

    def _create_cv_name_style(self, doc: Document):
        """Create CV Name paragraph style (name at top)"""
        style = doc.styles.add_style('CV Name', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(13)
        style.font.bold = True

    def _create_section_header_style(self, doc: Document):
        """Create Section Header style (EDUCATION, PROFESSIONAL EXPERIENCE)"""
        style = doc.styles.add_style('Section Header', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(10)
        style.font.bold = True
        style.font.color.rgb = self.ORANGE_RGB

    def _create_body_text_style(self, doc: Document):
        """Create Body Text paragraph style (standard paragraphs)"""
        # Body Text is a built-in style, so modify it instead of creating new
        style = doc.styles['Body Text']
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

    def _create_timeline_entry_style(self, doc: Document):
        """Create Timeline Entry style (date + institution with hanging indent)"""
        style = doc.styles.add_style('Timeline Entry', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

        # 72pt hanging indent (from analysis)
        style.paragraph_format.left_indent = Pt(72)
        style.paragraph_format.first_line_indent = Pt(-72)

    def _create_bullet_standard_style(self, doc: Document):
        """Create Bullet Standard style (regular bullets)"""
        style = doc.styles.add_style('Bullet Standard', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)

        # Bullet formatting with hanging indent (matches list numbering)
        # Note: List numbering will be applied separately when formatting documents
        style.paragraph_format.left_indent = Pt(72)
        style.paragraph_format.first_line_indent = Pt(-18)  # 0.25" hanging for bullet (18pt = 360 twentieths)

    def _create_bullet_gray_style(self, doc: Document):
        """Create Bullet Gray style (bullets for dates/education)"""
        style = doc.styles.add_style('Bullet Gray', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)
        style.font.color.rgb = self.GRAY_RGB

        # Bullet formatting with hanging indent
        style.paragraph_format.left_indent = Pt(72)
        style.paragraph_format.first_line_indent = Pt(-18)  # 0.25" hanging for bullet

    def _create_bullet_emphasis_style(self, doc: Document):
        """Create Bullet Emphasis style (bold italic bullets)"""
        style = doc.styles.add_style('Bullet Emphasis', WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = 'Helvetica'
        style.font.size = Pt(9)
        style.font.bold = True
        style.font.italic = True

        # Bullet formatting with hanging indent
        style.paragraph_format.left_indent = Pt(72)
        style.paragraph_format.first_line_indent = Pt(-18)  # 0.25" hanging for bullet

    def _create_play_title_style(self, doc: Document):
        """Create Play Title character style (bold italic for productions)"""
        style = doc.styles.add_style('Play Title', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.italic = True

    def _create_institution_style(self, doc: Document):
        """Create Institution character style (bold for institution names)"""
        style = doc.styles.add_style('Institution', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True

    def _create_job_title_style(self, doc: Document):
        """Create Job Title character style (bold italic for positions)"""
        style = doc.styles.add_style('Job Title', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.italic = True

    def _create_orange_emphasis_style(self, doc: Document):
        """Create Orange Emphasis character style"""
        style = doc.styles.add_style('Orange Emphasis', WD_STYLE_TYPE.CHARACTER)
        style.font.bold = True
        style.font.color.rgb = self.ORANGE_RGB

    def _create_gray_text_style(self, doc: Document):
        """Create Gray Text character style (dates, secondary info)"""
        style = doc.styles.add_style('Gray Text', WD_STYLE_TYPE.CHARACTER)
        style.font.color.rgb = self.GRAY_RGB
