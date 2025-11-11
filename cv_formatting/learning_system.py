"""Simple learning system for CV formatting preferences.

Intelligence lives in the skill (Claude analyzes text).
This class just loads/saves/applies learned patterns.
"""
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LearningSystem:
    """Load, save, and apply learned CV formatting preferences."""

    def __init__(self, learned_path: Optional[str] = None):
        """
        Initialize learning system.

        Args:
            learned_path: Path to learned-preferences.yaml (uses default if None)
        """
        if learned_path is None:
            learned_path = (
                Path.home() /
                ".claude/skills/format-resume/learned-preferences.yaml"
            )

        self.learned_path = Path(learned_path)
        self.learned = self._load_learned_preferences()

    def _load_learned_preferences(self) -> Dict:
        """Load learned preferences from YAML file."""
        if not self.learned_path.exists():
            logger.warning(f"Learned preferences file not found: {self.learned_path}")
            return self._get_empty_learned()

        try:
            with open(self.learned_path) as f:
                data = yaml.safe_load(f)
                # Ensure all expected keys exist
                if data is None:
                    return self._get_empty_learned()
                return {
                    'style_rules': data.get('style_rules', []),
                    'metadata_defaults': data.get('metadata_defaults', {}),
                    'section_patterns': data.get('section_patterns', {})
                }
        except Exception as e:
            logger.error(f"Failed to load learned preferences: {e}")
            return self._get_empty_learned()

    def _get_empty_learned(self) -> Dict:
        """Return empty learned preferences structure."""
        return {
            'style_rules': [],
            'metadata_defaults': {},
            'section_patterns': {}
        }

    def _save_learned_preferences(self):
        """Save learned preferences to YAML file."""
        try:
            # Ensure directory exists
            self.learned_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.learned_path, 'w') as f:
                yaml.dump(self.learned, f, default_flow_style=False, sort_keys=False)

            logger.info(f"Saved learned preferences to {self.learned_path}")
        except Exception as e:
            logger.error(f"Failed to save learned preferences: {e}")

    def learn_correction(self, text: str, context: str, preferred_style: str):
        """
        Learn a style correction.

        Args:
            text: The text that was corrected
            context: Context where this applies (e.g., "service section", "experience")
            preferred_style: The preferred style for this pattern
        """
        rule = {
            'pattern': text,
            'context': context,
            'preferred_style': preferred_style,
            'learned_date': datetime.now().strftime("%Y-%m-%d"),
            'example': text
        }

        self.learned['style_rules'].append(rule)
        self._save_learned_preferences()

        logger.info(f"Learned: '{text}' in {context} -> {preferred_style}")

    def apply_learned_patterns(self, content: List[Dict]) -> List[Dict]:
        """
        Apply learned style patterns to content.

        Simple pattern matching - just checks if pattern appears in text.
        Claude (the skill) does the semantic analysis.

        Args:
            content: List of content items with 'text' and 'style' keys

        Returns:
            Updated content with learned patterns applied
        """
        if not self.learned.get('style_rules'):
            return content

        current_section = None

        for item in content:
            # Track current section
            if item.get('style') == 'Section Header':
                current_section = item.get('text', '').strip()

            # Apply style rules
            for rule in self.learned['style_rules']:
                if self._matches_pattern(item.get('text', ''), rule['pattern']):
                    if self._context_matches(current_section, rule.get('context', '')):
                        item['style'] = rule['preferred_style']
                        logger.debug(
                            f"Applied learned rule: '{item['text']}' -> {rule['preferred_style']}"
                        )

        return content

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """
        Check if text matches pattern.

        Simple case-insensitive substring match.
        No complex regex - keep it simple.

        Args:
            text: Text to check
            pattern: Pattern to match

        Returns:
            True if pattern found in text
        """
        return pattern.lower() in text.lower()

    def _context_matches(self, current_section: Optional[str], rule_context: str) -> bool:
        """
        Check if current context matches rule context.

        Args:
            current_section: Current section header text (e.g., "EDUCATION")
            rule_context: Context from rule (e.g., "education", "service section")

        Returns:
            True if context matches
        """
        if not rule_context:
            return True  # No context restriction

        if current_section is None:
            return False

        # Simple case-insensitive substring match
        return rule_context.lower() in current_section.lower()

    def get_style_rules(self) -> List[Dict]:
        """Get all learned style rules."""
        return self.learned.get('style_rules', [])

    def clear_style_rule(self, index: int):
        """Remove a specific style rule by index."""
        if 0 <= index < len(self.learned['style_rules']):
            removed = self.learned['style_rules'].pop(index)
            self._save_learned_preferences()
            logger.info(f"Removed learned rule: {removed}")
        else:
            logger.warning(f"Invalid rule index: {index}")
