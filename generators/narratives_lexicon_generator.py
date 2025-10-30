"""
Narratives lexicon generator - creates storytelling patterns catalog.

This module generates a markdown document that catalogs narrative and rhetorical
patterns identified across cover letters, organized by category with chronological
tracking and source citations.
"""

from typing import List
from datetime import datetime

from analyzers.narratives_analyzer import NarrativeCategory
from templates.formatting_utils import (
    format_date,
    format_confidence,
    create_markdown_file
)


def generate_narratives_lexicon(narratives: List[NarrativeCategory], output_path: str) -> None:
    """
    Generate "Storytelling Patterns Catalog" from narratives analysis.

    Creates a searchable markdown document showing narrative and rhetorical patterns
    (metaphors, opening hooks, transitions, etc.) with full text and context.

    Args:
        narratives: List of NarrativeCategory objects from narratives analyzer
        output_path: Path to write markdown file

    Examples:
        >>> from analyzers.narratives_analyzer import analyze_narratives
        >>> narratives = analyze_narratives(documents)
        >>> generate_narratives_lexicon(narratives, "output/storytelling_patterns.md")
    """
    if not narratives:
        content = "# Storytelling Patterns Catalog\n\nNo narrative patterns found.\n"
        create_markdown_file(output_path, content)
        return

    # Sort categories alphabetically by name
    sorted_categories = sorted(narratives, key=lambda c: c.category_name)

    # Build markdown content
    lines = []

    # Header
    lines.append("# Storytelling Patterns Catalog\n\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    total_patterns = sum(len(cat.patterns) for cat in narratives)
    lines.append(f"Total categories: {len(narratives)} | Total patterns: {total_patterns}\n\n")
    lines.append("---\n\n")

    # Each category section
    for category in sorted_categories:
        # Category name as H2
        lines.append(f"## {category.category_name}\n\n")

        # Metadata line
        lines.append(
            f"Confidence: {format_confidence(category.confidence)} | "
            f"Patterns found: {len(category.patterns)}\n\n"
        )

        # Sort patterns by date (most recent first)
        sorted_patterns = sorted(
            category.patterns,
            key=lambda p: p.date if p.date else datetime.min.date(),
            reverse=True
        )

        # Each pattern within category
        for pattern in sorted_patterns:
            # Date and source as H3
            date_str = format_date(pattern.date) if pattern.date else "Unknown"
            lines.append(f"### {date_str} - {pattern.source_document}\n\n")

            # Pattern text in bold
            lines.append(f"**Pattern**: \"{pattern.text}\"\n\n")

            # Context
            lines.append(f"**Context**: {pattern.context}\n\n")

            # Separator between patterns
            lines.append("---\n\n")

    # Write to file
    content = ''.join(lines)
    create_markdown_file(output_path, content)
