"""Lookup and identify play titles in text for automatic italic styling."""
import yaml
from pathlib import Path
from typing import List, Tuple, Optional


class PlayTitlesLookup:
    """Finds play/production titles in text using dictionary."""

    def __init__(self, dictionary_path: Optional[str] = None):
        """
        Initialize with play titles dictionary.

        Args:
            dictionary_path: Path to play-titles-dictionary.yaml
                           If None, uses default location
        """
        if dictionary_path is None:
            dictionary_path = (
                Path.home() /
                ".claude/skills/format-cover-letter/play-titles-dictionary.yaml"
            )

        self.dictionary_path = Path(dictionary_path)
        self.plays = self._load_dictionary()

    def _load_dictionary(self) -> List[str]:
        """Load play titles from YAML dictionary."""
        if not self.dictionary_path.exists():
            return []

        with open(self.dictionary_path) as f:
            data = yaml.safe_load(f)

        plays = []

        # Load from different sections
        if data:
            plays.extend(data.get('productions', []))
            plays.extend(data.get('programs', []))

            # Load learned plays
            learned = data.get('learned', [])
            for item in learned:
                if isinstance(item, dict):
                    plays.append(item['text'])
                else:
                    plays.append(item)

        # Sort by length (longest first) to match longer titles first
        # E.g., "Romeo & Juliet" before "Juliet"
        plays.sort(key=len, reverse=True)

        return plays

    def find_plays_in_text(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Find all play titles in text.

        Args:
            text: Text to search

        Returns:
            List of (play_title, start_pos, end_pos) tuples
        """
        matches = []

        for play in self.plays:
            # Find all occurrences of this play
            start = 0
            while True:
                pos = text.find(play, start)
                if pos == -1:
                    break

                matches.append((play, pos, pos + len(play)))
                start = pos + len(play)

        # Sort by position
        matches.sort(key=lambda x: x[1])

        # Remove overlapping matches (keep first/longest)
        non_overlapping = []
        for match in matches:
            _, start, end = match

            # Check if this overlaps with any existing match
            overlaps = False
            for existing in non_overlapping:
                _, ex_start, ex_end = existing
                if start < ex_end and end > ex_start:
                    overlaps = True
                    break

            if not overlaps:
                non_overlapping.append(match)

        return non_overlapping

    def should_exclude(self, play_text: str, inline_styles: List[dict]) -> bool:
        """
        Check if a play title should be excluded from auto-styling.

        Args:
            play_text: The play title text
            inline_styles: List of inline_styles from JSON

        Returns:
            True if this play should NOT be styled
        """
        for style_spec in inline_styles:
            if style_spec.get('text') == play_text and style_spec.get('exclude'):
                return True

        return False
