"""Helper utilities for cover letter metadata inference.

The actual intelligence lives in the format-cover-letter skill,
which uses LLM to extract metadata. This module provides simple
file system utilities.
"""
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MetadataHelper:
    """Helper for loading defaults and finding job descriptions."""

    def __init__(self, defaults_path: Optional[str] = None):
        """
        Initialize with defaults configuration.

        Args:
            defaults_path: Path to defaults.yaml (uses default location if None)
        """
        if defaults_path is None:
            defaults_path = (
                Path.home() /
                ".claude/skills/format-cover-letter/defaults.yaml"
            )

        self.defaults_path = Path(defaults_path)
        self.defaults = self._load_defaults()

    def _load_defaults(self) -> Dict:
        """Load defaults from YAML file."""
        if not self.defaults_path.exists():
            logger.warning(f"Defaults file not found: {self.defaults_path}")
            return self._get_fallback_defaults()

        with open(self.defaults_path) as f:
            return yaml.safe_load(f)

    def _get_fallback_defaults(self) -> Dict:
        """Return fallback defaults if config file missing."""
        return {
            'contact': {
                'name': 'ANTHONY BYRNES',
                'phone': 'T: 213.305.3132',
                'email': 'E: anthonybyrnes@mac.com'
            },
            'date': {'auto_populate': True, 'format': '%B %d, %Y'},
            'recipient': {'default_salutation': 'Dear Search Committee,'},
            're_line': {'auto_generate': True, 'require': False},
            'job_descriptions': {
                'primary_path': '/Users/anthonybyrnes/PycharmProjects/career-lexicon-builder/career-applications',
                'filename_pattern': '00-job-description.md'
            }
        }

    def get_defaults(self) -> Dict:
        """Get the loaded defaults configuration."""
        return self.defaults

    def get_current_date(self) -> str:
        """Get current date formatted according to defaults."""
        date_config = self.defaults.get('date', {})
        date_format = date_config.get('format', '%B %d, %Y')
        return datetime.now().strftime(date_format)

    def find_all_job_descriptions(self) -> List[Dict]:
        """
        Find all job description files.

        Returns:
            List of dicts with 'file_path', 'job_title', 'company', etc.
        """
        job_desc_config = self.defaults.get('job_descriptions', {})
        primary_path = Path(job_desc_config.get(
            'primary_path',
            '/Users/anthonybyrnes/PycharmProjects/career-lexicon-builder/career-applications'
        ))
        filename_pattern = job_desc_config.get('filename_pattern', '00-job-description.md')

        if not primary_path.exists():
            logger.warning(f"Job descriptions path not found: {primary_path}")
            return []

        # Find all job description files
        job_desc_files = list(primary_path.glob(f'**/{filename_pattern}'))

        results = []
        for job_file in job_desc_files:
            job_data = self._parse_job_description(job_file)
            if job_data:
                job_data['file_path'] = str(job_file)
                results.append(job_data)

        return results

    def _parse_job_description(self, file_path: Path) -> Optional[Dict]:
        """Parse job description file and extract YAML front matter."""
        try:
            with open(file_path) as f:
                content = f.read()

            # Extract YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    metadata = yaml.safe_load(yaml_content)
                    return metadata

            return None
        except Exception as e:
            logger.error(f"Failed to parse job description {file_path}: {e}")
            return None

    def read_job_description_full(self, file_path: str) -> str:
        """Read full content of a job description file."""
        try:
            with open(file_path) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read job description {file_path}: {e}")
            return ""

    def infer_cv_metadata(self, content: str) -> Dict:
        """
        Infer CV metadata from content and defaults.

        Args:
            content: Raw CV text content

        Returns:
            Dictionary with CV metadata including type, author_name, document_title,
            version, and page_header configuration
        """
        # Get contact info from defaults
        contact = self.defaults.get('contact', {})
        author_name = contact.get('name', 'ANTHONY BYRNES')

        # Detect or use default document title
        document_title = self._detect_cv_title(content)

        # Detect CV version (Academic, Industry, Arts, or General)
        version = self._detect_version(content)

        # Get CV defaults for page header
        cv_defaults = self.defaults.get('cv_defaults', {})
        page_header_config = cv_defaults.get('page_header', {})

        # Build page header configuration
        page_header = {
            'enabled': page_header_config.get('enabled', True),
            'left': f"{author_name} - {document_title}",
            'right': 'page'
        }

        return {
            'type': 'cv',
            'author_name': author_name,
            'document_title': document_title,
            'last_updated': self.get_current_date(),
            'version': version,
            'page_header': page_header
        }

    def _detect_cv_title(self, content: str) -> str:
        """
        Detect whether user prefers 'CV', 'Resume', or 'Curriculum Vitae'.

        Args:
            content: CV text content

        Returns:
            Document title string
        """
        # Check for explicit title in content
        content_lower = content.lower()

        # Look for explicit mentions at the beginning of the document
        lines = content.strip().split('\n')
        if lines:
            first_line = lines[0].strip().lower()
            if 'resume' in first_line and 'curriculum' not in first_line:
                return 'Resume'
            elif 'curriculum vitae' in first_line:
                return 'Curriculum Vitae'
            elif first_line == 'cv':
                return 'CV'

        # Fall back to defaults
        cv_defaults = self.defaults.get('cv_defaults', {})
        return cv_defaults.get('document_title', 'Curriculum Vitae')

    def _detect_version(self, content: str) -> str:
        """
        Detect CV version based on sections present.

        Args:
            content: CV text content

        Returns:
            Version string: 'Academic', 'Industry', 'Arts', or 'General'
        """
        content_upper = content.upper()

        # Academic indicators
        academic_keywords = ['PUBLICATIONS', 'RESEARCH', 'TEACHING EXPERIENCE', 'TEACHING', 'GRANTS']
        academic_score = sum(1 for keyword in academic_keywords if keyword in content_upper)

        # Industry indicators
        industry_keywords = ['SKILLS', 'CERTIFICATIONS', 'TECHNICAL SKILLS', 'SOFTWARE']
        industry_score = sum(1 for keyword in industry_keywords if keyword in content_upper)

        # Arts indicators
        arts_keywords = ['PRODUCTIONS', 'PERFORMANCES', 'DIRECTING', 'ACTING']
        arts_score = sum(1 for keyword in arts_keywords if keyword in content_upper)

        # Determine version based on highest score
        scores = {
            'Academic': academic_score,
            'Industry': industry_score,
            'Arts': arts_score
        }

        # If academic score is highest and > 0, return Academic
        if scores['Academic'] > 0 and scores['Academic'] >= max(scores['Industry'], scores['Arts']):
            return 'Academic'

        # If industry score is highest
        if scores['Industry'] > scores['Arts']:
            return 'Industry'

        # If arts score is highest
        if scores['Arts'] > 0:
            return 'Arts'

        # Fall back to preferences or General
        preferences = self.defaults.get('preferences', {})
        return preferences.get('version', 'General')
