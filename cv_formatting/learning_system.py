"""Learning system for CV formatting preferences."""
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LearningSystem:
    """Manages learned preferences for CV formatting."""

    def __init__(self, learned_preferences_path: Optional[str] = None):
        """
        Initialize LearningSystem.

        Args:
            learned_preferences_path: Path to learned-preferences.yaml
        """
        if learned_preferences_path is None:
            learned_preferences_path = (
                Path.home() /
                ".claude/skills/format-resume/learned-preferences.yaml"
            )

        self.learned_preferences_path = Path(learned_preferences_path)
        self.learned = self._load_learned_preferences()

    def _load_learned_preferences(self) -> Dict:
        """Load learned preferences from YAML file."""
        if not self.learned_preferences_path.exists():
            logger.info(f"No learned preferences found at {self.learned_preferences_path}")
            return self._get_default_structure()

        try:
            with open(self.learned_preferences_path) as f:
                data = yaml.safe_load(f)
                if data is None:
                    return self._get_default_structure()
                return data
        except Exception as e:
            logger.error(f"Failed to load learned preferences: {e}")
            return self._get_default_structure()

    def _get_default_structure(self) -> Dict:
        """Return default structure for learned preferences."""
        return {
            'style_rules': [],
            'metadata_defaults': {},
            'section_patterns': {}
        }

    def _save_learned_preferences(self):
        """Save learned preferences to YAML file."""
        try:
            # Ensure directory exists
            self.learned_preferences_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.learned_preferences_path, 'w') as f:
                yaml.dump(self.learned, f, default_flow_style=False, sort_keys=False)

            logger.info(f"Saved learned preferences to {self.learned_preferences_path}")
        except Exception as e:
            logger.error(f"Failed to save learned preferences: {e}")

    def apply_learned_patterns(self, content: List[Dict]) -> List[Dict]:
        """
        Apply all learned patterns to parsed content.

        Args:
            content: List of content items from CVAnalyzer

        Returns:
            Modified content with learned patterns applied
        """
        # Make a copy to avoid modifying original
        modified_content = [item.copy() for item in content]

        # Apply style rules
        style_rules = self.learned.get('style_rules', [])
        for rule in style_rules:
            pattern = rule.get('pattern', '')
            preferred_style = rule.get('preferred_style')
            context = rule.get('context', 'any')

            if not pattern or not preferred_style:
                continue

            # Apply rule to matching items
            for item in modified_content:
                text = item.get('text', '')

                # Case-insensitive pattern matching
                if re.search(pattern, text, re.IGNORECASE):
                    # Check context if specified
                    item_context = item.get('context', 'any')

                    if context == 'any' or item_context == 'any' or context == item_context:
                        item['style'] = preferred_style

        # TODO: Apply section patterns (future enhancement)
        # section_patterns = self.learned.get('section_patterns', {})
        # ...

        return modified_content

    def learn_correction(self, item: Dict, old_style: str, new_style: str, context: str = 'any'):
        """
        Save a style correction as a learned rule.

        Args:
            item: Content item that was corrected
            old_style: Original style
            new_style: Corrected style
            context: Context where this correction applies
        """
        text = item.get('text', '')

        rule = {
            'pattern': text,  # Use exact text as pattern
            'context': context,
            'preferred_style': new_style,
            'learned_date': datetime.now().strftime("%Y-%m-%d"),
            'example': text
        }

        # Add to rules
        self.learned.setdefault('style_rules', []).append(rule)

        # Save to file
        self._save_learned_preferences()

        logger.info(f"Learned correction: '{text}' → {new_style} (context: {context})")

    def learn_metadata_default(self, key: str, value: Any):
        """
        Save a metadata preference.

        Args:
            key: Metadata key (e.g., 'document_title')
            value: Metadata value (e.g., 'Resume')
        """
        self.learned.setdefault('metadata_defaults', {})[key] = value
        self._save_learned_preferences()

        logger.info(f"Learned metadata default: {key} = {value}")

    def learn_section_pattern(self, section_name: str, pattern: Dict):
        """
        Save a section structure pattern.

        Args:
            section_name: Name of section (e.g., 'EDUCATION')
            pattern: Pattern dictionary with 'order' and other keys
        """
        self.learned.setdefault('section_patterns', {})[section_name] = pattern
        self._save_learned_preferences()

        logger.info(f"Learned section pattern for {section_name}")

    def get_style_rules(self) -> List[Dict]:
        """
        Get all style rules.

        Returns:
            List of style rules
        """
        return self.learned.get('style_rules', [])

    def clear_rules_matching(self, pattern: str):
        """
        Remove all rules matching a pattern.

        Args:
            pattern: Pattern to match against rule patterns
        """
        style_rules = self.learned.get('style_rules', [])

        # Filter out matching rules
        filtered_rules = [
            rule for rule in style_rules
            if not re.search(pattern, rule.get('pattern', ''), re.IGNORECASE)
        ]

        self.learned['style_rules'] = filtered_rules
        self._save_learned_preferences()

        removed_count = len(style_rules) - len(filtered_rules)
        logger.info(f"Removed {removed_count} rules matching '{pattern}'")

    def get_metadata_defaults(self) -> Dict:
        """
        Get all metadata defaults.

        Returns:
            Dictionary of metadata defaults
        """
        return self.learned.get('metadata_defaults', {})

    def get_section_patterns(self) -> Dict:
        """
        Get all section patterns.

        Returns:
            Dictionary of section patterns
        """
        return self.learned.get('section_patterns', {})
