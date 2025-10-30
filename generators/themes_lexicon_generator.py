"""
Themes lexicon generator - creates reference document for personal values.

This module generates a markdown document that catalogs recurring themes and values
identified across cover letters, organized chronologically with confidence scores
and source citations.
"""

from typing import List
from datetime import datetime

from analyzers.themes_analyzer import Theme
from templates.formatting_utils import (
    format_date,
    format_confidence,
    create_markdown_file
)


def generate_themes_lexicon(themes: List[Theme], output_path: str) -> None:
    """
    Generate "My Values" reference document from themes analysis.

    Creates a searchable markdown document showing recurring themes/values
    from cover letters, with chronological occurrences and confidence scores.

    Args:
        themes: List of Theme objects from themes analyzer
        output_path: Path to write markdown file

    Examples:
        >>> from analyzers.themes_analyzer import analyze_themes
        >>> themes = analyze_themes(documents)
        >>> generate_themes_lexicon(themes, "output/my_values.md")
    """
    if not themes:
        content = "# My Values and Themes\n\nNo themes found.\n"
        create_markdown_file(output_path, content)
        return

    # Sort themes by confidence (highest first)
    sorted_themes = sorted(themes, key=lambda t: t.confidence, reverse=True)

    # Build markdown content
    lines = []

    # Header
    lines.append("# My Values and Themes\n\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    lines.append(f"Total themes: {len(themes)}\n\n")
    lines.append("---\n\n")

    # Each theme section
    for theme in sorted_themes:
        lines.append(f"## {theme.theme_name}\n\n")

        # Metadata line
        metadata_parts = [f"Confidence: {format_confidence(theme.confidence)}"]

        if theme.first_seen:
            metadata_parts.append(f"First seen: {format_date(theme.first_seen)}")
        if theme.last_seen:
            metadata_parts.append(f"Last seen: {format_date(theme.last_seen)}")

        lines.append(" | ".join(metadata_parts) + "\n\n")

        # Occurrences section
        lines.append("### Occurrences (chronological)\n\n")

        # Sort occurrences chronologically (earliest first)
        sorted_occurrences = sorted(
            theme.occurrences,
            key=lambda o: o.date if o.date else datetime.min.date()
        )

        for occ in sorted_occurrences:
            # Date and source as H4
            date_str = format_date(occ.date) if occ.date else "Unknown"
            lines.append(f"#### {date_str} - {occ.source_document}\n\n")

            # Quote in blockquote
            lines.append(f'> "{occ.quote}"\n\n')

            # Context with bold label
            lines.append(f"**Context**: {occ.context}\n\n")

            # Separator
            lines.append("---\n\n")

    # Write to file
    content = ''.join(lines)
    create_markdown_file(output_path, content)
