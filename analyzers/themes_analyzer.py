"""
Themes analyzer - extracts recurring themes/values from cover letters.

This module identifies value statements and philosophical themes from cover letters,
clusters similar themes together, and tracks how themes evolve over time.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import date
import re
from utils.similarity import calculate_semantic_similarity, cluster_similar_items
from core.confidence_scorer import calculate_confidence
from core.document_processor import DocumentType


@dataclass
class ThemeOccurrence:
    """
    A single occurrence of a theme in a document.

    Attributes:
        quote: The actual quote expressing the theme
        context: Surrounding sentences for context
        source_document: Filepath of the source document
        date: Document date (if available)
    """
    quote: str
    context: str
    source_document: str
    date: Optional[date]


@dataclass
class Theme:
    """
    A recurring theme identified across documents.

    Attributes:
        theme_name: Name/label for the theme (e.g., "Leadership")
        occurrences: List of all occurrences of this theme
        confidence: Confidence score (0.0-1.0) that this is a real theme
        first_seen: Earliest date this theme appeared
        last_seen: Most recent date this theme appeared
    """
    theme_name: str
    occurrences: List[ThemeOccurrence]
    confidence: float
    first_seen: Optional[date]
    last_seen: Optional[date]


# Patterns for identifying value statements and themes
THEME_PATTERNS = [
    r'\bI believe\b[^.!?]*[.!?]',
    r'\bI value\b[^.!?]*[.!?]',
    r'\bI(?:\'m| am) passionate about\b[^.!?]*[.!?]',
    r'\bI(?:\'m| am) committed to\b[^.!?]*[.!?]',
    r'\bI(?:\'m| am) driven by\b[^.!?]*[.!?]',
    r'\bmy philosophy (?:is|of)\b[^.!?]*[.!?]',
    r'\bI(?:\'m| am) dedicated to\b[^.!?]*[.!?]',
]

# Compile patterns for efficiency
COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in THEME_PATTERNS]


def extract_themes_from_document(text: str, filepath: str, doc_date: Optional[date]) -> List[ThemeOccurrence]:
    """
    Extract theme occurrences from a single document.

    Identifies value-laden statements and philosophical themes using pattern matching.
    Looks for first-person statements about values, beliefs, and passions.

    Args:
        text: Document text content
        filepath: Path to the source document
        doc_date: Document date (if available)

    Returns:
        List of ThemeOccurrence objects found in the document

    Examples:
        >>> text = "I believe in collaborative leadership. I value teamwork."
        >>> occurrences = extract_themes_from_document(text, "letter.txt", None)
        >>> len(occurrences)
        2
    """
    if not text or not text.strip():
        return []

    occurrences = []

    # Split text into sentences for context extraction
    sentences = _split_into_sentences(text)

    # Find all pattern matches
    for pattern in COMPILED_PATTERNS:
        for match in pattern.finditer(text):
            quote = match.group(0).strip()

            # Skip very short or generic quotes
            if len(quote) < 15 or _is_generic_phrase(quote):
                continue

            # Extract context (surrounding sentences)
            context = _extract_context(sentences, quote)

            occurrence = ThemeOccurrence(
                quote=quote,
                context=context,
                source_document=filepath,
                date=doc_date
            )
            occurrences.append(occurrence)

    return occurrences


def _split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """
    # Simple sentence splitting (can be improved with NLP library)
    # Split on period, exclamation, or question mark followed by space and capital
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if s.strip()]


def _extract_context(sentences: List[str], quote: str) -> str:
    """
    Extract context around a quote.

    Finds the sentence containing the quote and includes surrounding sentences.

    Args:
        sentences: List of sentences from the document
        quote: The quote to find context for

    Returns:
        Context string (quote + surrounding sentences)
    """
    # Find the sentence containing the quote
    for i, sentence in enumerate(sentences):
        if quote in sentence:
            # Include previous and next sentence if available
            start_idx = max(0, i - 1)
            end_idx = min(len(sentences), i + 2)
            context_sentences = sentences[start_idx:end_idx]
            return ' '.join(context_sentences)

    # If not found in sentences, return the quote itself
    return quote


def _is_generic_phrase(quote: str) -> bool:
    """
    Check if a quote is too generic to be meaningful.

    Args:
        quote: Quote to check

    Returns:
        True if the quote is generic, False otherwise
    """
    # Generic phrases to filter out
    generic_patterns = [
        r'I believe (?:that )?this',
        r'I value your',
        r'I(?:\'m| am) passionate about (?:this|the)',
    ]

    for pattern in generic_patterns:
        if re.search(pattern, quote, re.IGNORECASE):
            return True

    return False


def cluster_theme_occurrences(occurrences: List[ThemeOccurrence]) -> List[Theme]:
    """
    Cluster similar theme occurrences into themes.

    Uses semantic similarity to group related quotes together. Calculates confidence
    based on frequency, consistency, and temporal stability.

    Args:
        occurrences: List of theme occurrences to cluster

    Returns:
        List of Theme objects, each containing clustered occurrences

    Examples:
        >>> occ1 = ThemeOccurrence("I believe in leadership", "ctx", "doc1", None)
        >>> occ2 = ThemeOccurrence("I value team leadership", "ctx", "doc2", None)
        >>> themes = cluster_theme_occurrences([occ1, occ2])
        >>> len(themes)
        1
    """
    if not occurrences:
        return []

    if len(occurrences) == 1:
        # Single occurrence = single theme
        occurrence = occurrences[0]
        theme_name = _extract_theme_name(occurrence.quote)
        return [Theme(
            theme_name=theme_name,
            occurrences=[occurrence],
            confidence=0.6,  # Lower confidence for single occurrence
            first_seen=occurrence.date,
            last_seen=occurrence.date
        )]

    # Extract quotes for clustering
    quotes = [occ.quote for occ in occurrences]

    # Cluster similar quotes
    clusters = cluster_similar_items(quotes, threshold=0.5)

    # Build Theme objects from clusters
    themes = []
    for cluster in clusters:
        # Find occurrences for this cluster
        cluster_occurrences = []
        for quote in cluster:
            for occ in occurrences:
                if occ.quote == quote and occ not in cluster_occurrences:
                    cluster_occurrences.append(occ)
                    break

        # Sort occurrences chronologically
        cluster_occurrences.sort(key=lambda x: x.date if x.date else date.min)

        # Determine theme name from most representative quote
        theme_name = _determine_theme_name(cluster_occurrences)

        # Calculate confidence
        confidence = _calculate_theme_confidence(cluster_occurrences)

        # Determine first and last seen dates
        dates = [occ.date for occ in cluster_occurrences if occ.date]
        first_seen = min(dates) if dates else None
        last_seen = max(dates) if dates else None

        theme = Theme(
            theme_name=theme_name,
            occurrences=cluster_occurrences,
            confidence=confidence,
            first_seen=first_seen,
            last_seen=last_seen
        )
        themes.append(theme)

    return themes


def _extract_theme_name(quote: str) -> str:
    """
    Extract a theme name from a quote.

    Args:
        quote: Quote to extract theme from

    Returns:
        Theme name
    """
    # Look for key concepts after "I believe in", "I value", etc.
    patterns = [
        (r'I believe in ([^.!?,]+)', 1),
        (r'I value ([^.!?,]+)', 1),
        (r'I(?:\'m| am) passionate about ([^.!?,]+)', 1),
        (r'I(?:\'m| am) committed to ([^.!?,]+)', 1),
        (r'I(?:\'m| am) driven by ([^.!?,]+)', 1),
        (r'I(?:\'m| am) dedicated to ([^.!?,]+)', 1),
    ]

    for pattern, group_idx in patterns:
        match = re.search(pattern, quote, re.IGNORECASE)
        if match:
            concept = match.group(group_idx).strip()
            # Capitalize first letter of each word
            return concept.title()

    # Fallback: use first few significant words
    words = quote.split()[:5]
    return ' '.join(words).title()


def _determine_theme_name(occurrences: List[ThemeOccurrence]) -> str:
    """
    Determine the best name for a theme from its occurrences.

    Uses the shortest, most concise occurrence as the theme name.

    Args:
        occurrences: List of occurrences in this theme

    Returns:
        Theme name
    """
    if not occurrences:
        return "Unknown Theme"

    # Extract theme names from all quotes
    names = [_extract_theme_name(occ.quote) for occ in occurrences]

    # Use the shortest name (usually most concise)
    shortest_name = min(names, key=len)

    return shortest_name


def _calculate_theme_confidence(occurrences: List[ThemeOccurrence]) -> float:
    """
    Calculate confidence score for a theme.

    Based on:
    - Frequency: More occurrences = higher confidence
    - Temporal stability: Appears across multiple dates = higher confidence
    - Number of documents: More documents = higher confidence

    Args:
        occurrences: List of occurrences for this theme

    Returns:
        Confidence score (0.0-1.0)
    """
    # Frequency criterion (more occurrences = higher confidence)
    frequency_score = min(1.0, len(occurrences) / 5.0)

    # Temporal stability (appears across multiple dates)
    dates = [occ.date for occ in occurrences if occ.date]
    unique_dates = len(set(dates)) if dates else 0
    temporal_score = min(1.0, unique_dates / 3.0) if dates else 0.5

    # Document diversity (appears in multiple documents)
    documents = set(occ.source_document for occ in occurrences)
    document_score = min(1.0, len(documents) / 3.0)

    # Calculate weighted confidence
    confidence = calculate_confidence(
        {
            'frequency': frequency_score,
            'temporal_stability': temporal_score,
            'document_diversity': document_score
        },
        weights={
            'frequency': 0.4,
            'temporal_stability': 0.3,
            'document_diversity': 0.3
        }
    )

    return confidence


def analyze_themes(documents: List[Dict]) -> List[Theme]:
    """
    Analyze themes across all documents.

    Main API function. Filters to cover letters only, extracts theme occurrences,
    clusters them into themes, and returns sorted by confidence.

    Args:
        documents: List of processed document dictionaries, each containing:
            - filepath: Path to document
            - text: Document text
            - document_type: Type of document (from DocumentType enum)
            - date: Document date (optional)

    Returns:
        List of Theme objects sorted by confidence (highest first)

    Examples:
        >>> docs = [{'filepath': 'letter.txt', 'text': 'I believe in leadership',
        ...          'document_type': 'cover_letter', 'date': None}]
        >>> themes = analyze_themes(docs)
        >>> len(themes) > 0
        True
    """
    if not documents:
        return []

    # Filter to cover letters only
    cover_letters = [
        doc for doc in documents
        if doc.get('document_type') == DocumentType.COVER_LETTER.value
    ]

    if not cover_letters:
        return []

    # Extract theme occurrences from all cover letters
    all_occurrences = []
    for doc in cover_letters:
        occurrences = extract_themes_from_document(
            text=doc.get('text', ''),
            filepath=doc.get('filepath', ''),
            doc_date=doc.get('date')
        )
        all_occurrences.extend(occurrences)

    if not all_occurrences:
        return []

    # Cluster occurrences into themes
    themes = cluster_theme_occurrences(all_occurrences)

    # Sort by confidence (highest first)
    themes.sort(key=lambda t: t.confidence, reverse=True)

    return themes
