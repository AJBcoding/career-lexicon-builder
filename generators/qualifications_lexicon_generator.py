"""
Qualifications lexicon generator - creates resume bullet variations reference.

This module generates a markdown document that catalogs work positions and their
description variations across resume versions, organized by position with
chronological tracking of phrasing evolution.
"""

from typing import List
from datetime import datetime

from analyzers.qualifications_analyzer import Qualification
from templates.formatting_utils import (
    format_date,
    format_confidence,
    create_markdown_file
)


def generate_qualifications_lexicon(qualifications: List[Qualification], output_path: str) -> None:
    """
    Generate "Resume Bullet Variations" reference document from qualifications analysis.

    Creates a searchable markdown document showing how position descriptions
    evolved across resume versions, with source citations and dates.

    Args:
        qualifications: List of Qualification objects from qualifications analyzer
        output_path: Path to write markdown file

    Examples:
        >>> from analyzers.qualifications_analyzer import analyze_qualifications
        >>> qualifications = analyze_qualifications(documents)
        >>> generate_qualifications_lexicon(qualifications, "output/resume_variations.md")
    """
    if not qualifications:
        content = "# Resume Bullet Variations\n\nNo qualifications found.\n"
        create_markdown_file(output_path, content)
        return

    # Sort qualifications by most recent variation date (most recent first)
    def get_most_recent_date(qual):
        dates = [v.date for v in qual.variations if v.date]
        return max(dates) if dates else datetime.min.date()

    sorted_qualifications = sorted(
        qualifications,
        key=get_most_recent_date,
        reverse=True
    )

    # Build markdown content
    lines = []

    # Header
    lines.append("# Resume Bullet Variations\n\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    lines.append(f"Total qualifications: {len(qualifications)}\n\n")
    lines.append("---\n\n")

    # Each qualification section
    for qual in sorted_qualifications:
        # Position title and organization as H2
        lines.append(f"## {qual.position_title} at {qual.organization}\n\n")

        # Metadata line
        lines.append(f"ID: `{qual.qualification_id}` | Confidence: {format_confidence(qual.confidence)}\n\n")

        # Variations section
        lines.append("### Variations (most recent first)\n\n")

        # Sort variations by date (most recent first)
        sorted_variations = sorted(
            qual.variations,
            key=lambda v: v.date if v.date else datetime.min.date(),
            reverse=True
        )

        for i, variation in enumerate(sorted_variations, 1):
            # Version number with source and date as H4
            date_str = format_date(variation.date) if variation.date else "Unknown"
            lines.append(f"#### Version {i} - {variation.source_document} ({date_str})\n\n")

            # Bullet point text
            lines.append(f"- {variation.text}\n\n")

        # Separator between qualifications
        lines.append("---\n\n")

    # Write to file
    content = ''.join(lines)
    create_markdown_file(output_path, content)
