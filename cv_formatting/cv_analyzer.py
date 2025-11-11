"""Convert raw CV text to structured JSON format."""
from typing import Dict, List, Any, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class CVAnalyzer:
    """Parse raw CV text into structured JSON."""

    def __init__(self, metadata_helper=None, learning_system=None):
        """
        Initialize CVAnalyzer.

        Args:
            metadata_helper: MetadataHelper instance for metadata inference
            learning_system: LearningSystem instance for applying learned patterns
        """
        self.metadata_helper = metadata_helper
        self.learning_system = learning_system
        self.current_section = None

    def analyze(self, raw_text: str) -> Dict[str, Any]:
        """
        Parse raw CV text into JSON structure.

        Args:
            raw_text: Raw CV text to parse

        Returns:
            Dictionary with 'document_metadata' and 'content' keys
        """
        lines = raw_text.split('\n')
        content = []

        for line in lines:
            if not line.strip():
                continue

            # Detect element type and add to content
            item = self._classify_line(line)
            if item:
                content.append(item)

        # Apply learned patterns if learning system available
        if self.learning_system:
            try:
                content = self.learning_system.apply_learned_patterns(content)
            except NotImplementedError:
                # Learning system not yet fully implemented
                pass

        # Get document metadata
        if self.metadata_helper:
            document_metadata = self.metadata_helper.infer_cv_metadata(raw_text)
        else:
            document_metadata = {
                'type': 'cv',
                'author_name': 'ANTHONY BYRNES',
                'document_title': 'Curriculum Vitae',
                'version': 'General',
                'page_header': {
                    'enabled': True,
                    'left': 'ANTHONY BYRNES - Curriculum Vitae',
                    'right': 'page'
                }
            }

        return {
            'document_metadata': document_metadata,
            'content': content
        }

    def _classify_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Classify a line and return appropriate content item.

        Args:
            line: Line of text to classify

        Returns:
            Content item dictionary or None if line should be skipped
        """
        stripped = line.strip()

        # Empty line
        if not stripped:
            return None

        # Check patterns in order of specificity
        # Check name first (before section header) since names are also all caps
        if self._is_name(stripped):
            return {"text": stripped, "style": "CV Name", "type": "paragraph"}

        elif self._is_section_header(stripped):
            self.current_section = stripped
            return {"text": stripped, "style": "Section Header", "type": "paragraph"}

        elif self._is_contact_info(stripped):
            return self._parse_contact(stripped)

        elif self._is_timeline_entry(stripped):
            return self._parse_timeline(stripped)

        elif self._is_bullet(stripped):
            return self._parse_bullet(stripped)

        else:
            # Default to Body Text
            return {"text": stripped, "style": "Body Text", "type": "paragraph"}

    def _is_section_header(self, line: str) -> bool:
        """Check if line is a section header (ALL CAPS)."""
        # Must be all uppercase (allowing spaces and punctuation)
        # Must not be contact info or timeline
        if not line.isupper():
            return False

        # Not a contact line
        if re.match(r'^[TE]:', line) or 'Phone:' in line or 'Email:' in line:
            return False

        # Not a timeline (starts with date)
        if re.match(r'^\d{4}', line):
            return False

        # Common section keywords (optional check)
        section_keywords = [
            'EDUCATION', 'EXPERIENCE', 'PROFESSIONAL EXPERIENCE',
            'PUBLICATIONS', 'TEACHING', 'RESEARCH', 'SKILLS',
            'CERTIFICATIONS', 'PRODUCTIONS', 'PERFORMANCES',
            'SERVICE', 'AWARDS', 'HONORS'
        ]

        # If it matches common keywords, definitely a section header
        for keyword in section_keywords:
            if keyword in line:
                return True

        # If short (< 50 chars) and all caps, likely a section header
        return len(line) < 50

    def _is_name(self, line: str) -> bool:
        """Check if line is the CV name (usually first line, all caps name)."""
        # All caps, likely a name (2-4 words, capitalized)
        if not line.isupper():
            return False

        # Not contact info
        if ':' in line or '@' in line:
            return False

        # Not a section header (check against common sections)
        common_sections = ['EDUCATION', 'EXPERIENCE', 'SKILLS', 'PUBLICATIONS']
        if any(section in line for section in common_sections):
            return False

        # Likely a name if 2-4 words and reasonable length
        words = line.split()
        return 2 <= len(words) <= 4 and len(line) < 40

    def _is_contact_info(self, line: str) -> bool:
        """Check if line is contact information."""
        # Phone patterns
        if re.match(r'^[TP]:\s*\d', line, re.IGNORECASE):
            return True
        if re.match(r'^Phone:', line, re.IGNORECASE):
            return True

        # Email patterns
        if re.match(r'^E:', line, re.IGNORECASE):
            return True
        if re.match(r'^Email:', line, re.IGNORECASE):
            return True
        if '@' in line and '.' in line and len(line) < 50:
            return True

        return False

    def _is_timeline_entry(self, line: str) -> bool:
        """Check if line is a timeline entry (starts with dates)."""
        # Pattern: YYYY-YYYY or YYYY - YYYY or YYYY-Present
        if re.match(r'^\d{4}[\s\-]+(\d{4}|Present|present)', line):
            return True

        # Pattern: Fall YYYY, Spring YYYY, etc.
        if re.match(r'^(Fall|Spring|Summer|Winter)\s+\d{4}', line, re.IGNORECASE):
            return True

        return False

    def _is_bullet(self, line: str) -> bool:
        """Check if line is a bullet point."""
        # Starts with bullet character
        return line.startswith(('•', '-', '*'))

    def _parse_contact(self, line: str) -> Dict[str, Any]:
        """Parse contact info line."""
        return {
            "text": line,
            "style": "Contact Info",
            "type": "paragraph"
        }

    def _parse_timeline(self, line: str) -> Dict[str, Any]:
        """
        Parse timeline entry and extract institution if present.

        Args:
            line: Timeline line text

        Returns:
            Content item with potential inline_styles for institution
        """
        item = {
            "text": line,
            "style": "Timeline Entry",
            "type": "paragraph"
        }

        # Try to extract institution name for inline styling
        # Pattern: dates followed by institution name
        # e.g., "2020-2024  California State University, Long Beach"

        # Match date pattern and capture rest
        match = re.match(
            r'^(\d{4}[\s\-]+(?:\d{4}|Present|present))\s+(.+)$',
            line,
            re.IGNORECASE
        )

        if match:
            institution_text = match.group(2).strip()

            # Extract institution (everything, or up to first comma/period)
            # Common patterns:
            # - "California State University, Long Beach"
            # - "The Colburn School"
            # - "University of California, Los Angeles"

            if institution_text:
                item['inline_styles'] = [
                    {
                        "text": institution_text,
                        "style": "Institution"
                    }
                ]

        return item

    def _parse_bullet(self, line: str) -> Dict[str, Any]:
        """Parse bullet point line."""
        return {
            "text": line,
            "style": "Bullet Standard",
            "type": "paragraph"
        }
