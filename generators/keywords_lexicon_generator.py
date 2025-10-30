"""
Keywords lexicon generator - creates keyword usage index.

This module generates a markdown document that catalogs keywords and phrases
with cross-referenced usage contexts across all documents, organized alphabetically
with frequency filtering and chronological tracking.
"""

from typing import List
from datetime import datetime

from analyzers.keywords_analyzer import KeywordEntry
from templates.formatting_utils import (
    format_date,
    create_markdown_file
)


def generate_keywords_lexicon(
    keywords: List[KeywordEntry],
    output_path: str,
    min_frequency: int = 2
) -> None:
    """
    Generate "Keyword Usage Index" from keywords analysis.

    Creates a searchable markdown document showing how keywords are used
    across documents, with usage contexts highlighted and chronologically ordered.

    Args:
        keywords: List of KeywordEntry objects from keywords analyzer
        output_path: Path to write markdown file
        min_frequency: Minimum frequency threshold (default: 2)

    Examples:
        >>> from analyzers.keywords_analyzer import analyze_keywords
        >>> keywords = analyze_keywords(documents)
        >>> generate_keywords_lexicon(keywords, "output/usage_index.md", min_frequency=2)
    """
    # Filter by minimum frequency
    filtered_keywords = [k for k in keywords if k.frequency >= min_frequency]

    if not filtered_keywords:
        content = f"# Keyword Usage Index\n\nNo keywords found with minimum frequency of {min_frequency}.\n"
        create_markdown_file(output_path, content)
        return

    # Sort keywords alphabetically
    sorted_keywords = sorted(filtered_keywords, key=lambda k: k.keyword.lower())

    # Build markdown content
    lines = []

    # Header
    lines.append("# Keyword Usage Index\n\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    lines.append(
        f"Total keywords: {len(sorted_keywords)} | "
        f"Minimum frequency: {min_frequency}\n\n"
    )
    lines.append("---\n\n")

    # Each keyword section
    for keyword_entry in sorted_keywords:
        # Keyword as H2
        lines.append(f"## {keyword_entry.keyword}\n\n")

        # Metadata line
        metadata_parts = [f"Frequency: {keyword_entry.frequency}"]

        # Aliases
        if keyword_entry.aliases:
            aliases_str = ", ".join(keyword_entry.aliases)
            metadata_parts.append(f"Aliases: {aliases_str}")
        else:
            metadata_parts.append("Aliases: None")

        # Document types (sort for consistency)
        if keyword_entry.document_types:
            doc_types_str = ", ".join(sorted(keyword_entry.document_types))
            metadata_parts.append(f"Document types: {doc_types_str}")

        lines.append(" | ".join(metadata_parts) + "\n\n")

        # Usage contexts section
        lines.append("### Usage contexts (most recent first)\n\n")

        # Sort usages by date (most recent first)
        sorted_usages = sorted(
            keyword_entry.usages,
            key=lambda u: u.date if u.date else datetime.min.date(),
            reverse=True
        )

        for usage in sorted_usages:
            # Date, source, and document type as H4
            date_str = format_date(usage.date) if usage.date else "Unknown"
            lines.append(
                f"#### {usage.source_document} ({usage.document_type}) - {date_str}\n\n"
            )

            # Context with keyword bolded (simple approach: bold the keyword)
            context_with_bold = usage.context.replace(
                keyword_entry.keyword,
                f"**{keyword_entry.keyword}**"
            )
            lines.append(f"> {context_with_bold}\n\n")

        # Separator between keywords
        lines.append("---\n\n")

    # Write to file
    content = ''.join(lines)
    create_markdown_file(output_path, content)
