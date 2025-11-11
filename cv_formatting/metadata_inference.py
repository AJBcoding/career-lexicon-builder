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
