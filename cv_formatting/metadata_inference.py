"""Helper utilities for cover letter and CV metadata inference.

The actual intelligence lives in the format-cover-letter and format-resume skills,
which use LLM to extract metadata. This module provides simple file system utilities.
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
        self.learned = self._load_learned_preferences()

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

    def _load_learned_preferences(self) -> Dict:
        """Load learned preferences if available."""
        # Check for format-resume learned preferences (for CVs)
        learned_path = (
            Path.home() /
            ".claude/skills/format-resume/learned-preferences.yaml"
        )

        if not learned_path.exists():
            return {}

        try:
            with open(learned_path) as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.warning(f"Failed to load learned preferences: {e}")
            return {}

    def infer_cv_metadata(self, content: str) -> Dict:
        """
        Infer CV metadata from content and defaults.

        Intelligence lives in the skill (Claude analyzes text).
        This just loads defaults and generates page header config.

        Args:
            content: CV content text (used for version detection)

        Returns:
            Dictionary with CV metadata including page header config
        """
        cv_title = self._detect_cv_title()
        author_name = self.defaults.get('contact', {}).get('name', 'UNKNOWN')
        version = self._detect_version(content)

        # Get page header config from defaults
        cv_defaults = self.defaults.get('cv_defaults', {})
        page_header_config = cv_defaults.get('page_header', {
            'enabled': True,
            'format': '{name} - {title}'
        })

        return {
            'type': 'cv',
            'author_name': author_name,
            'document_title': cv_title,
            'last_updated': self.get_current_date(),
            'version': version,
            'page_header': {
                'enabled': page_header_config.get('enabled', True),
                'left': f"{author_name} - {cv_title}",
                'right': 'page'
            }
        }

    def _detect_cv_title(self) -> str:
        """
        Detect document title preference.

        Checks learned preferences first, then defaults.

        Returns:
            Document title (e.g., 'Curriculum Vitae', 'Resume', 'CV')
        """
        # Check learned preferences first
        learned_title = self.learned.get('metadata_defaults', {}).get('document_title')
        if learned_title:
            return learned_title

        # Use default from cv_defaults
        return self.defaults.get('cv_defaults', {}).get('document_title', 'Curriculum Vitae')

    def _detect_version(self, content: str) -> str:
        """
        Detect CV version based on sections present.

        Simple keyword-based detection. Claude (the skill) does
        the actual semantic analysis.

        Args:
            content: CV content text

        Returns:
            Version type ('Academic', 'Industry', 'Arts', or 'General')
        """
        content_lower = content.lower()

        # Academic indicators
        academic_keywords = ['publications', 'research', 'teaching', 'grants', 'dissertation']
        academic_count = sum(1 for kw in academic_keywords if kw in content_lower)

        # Industry indicators
        industry_keywords = ['skills', 'certifications', 'technical', 'software', 'projects']
        industry_count = sum(1 for kw in industry_keywords if kw in content_lower)

        # Arts indicators
        arts_keywords = ['productions', 'performances', 'exhibitions', 'concerts', 'repertoire']
        arts_count = sum(1 for kw in arts_keywords if kw in content_lower)

        # Return version with most indicators
        max_count = max(academic_count, industry_count, arts_count)

        if max_count == 0:
            # Use default from config
            return self.defaults.get('preferences', {}).get('version', 'General')

        if academic_count == max_count:
            return 'Academic'
        elif arts_count == max_count:
            return 'Arts'
        elif industry_count == max_count:
            return 'Industry'
        else:
            return 'General'
