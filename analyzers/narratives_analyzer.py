"""
Narratives analyzer - extracts storytelling patterns and rhetorical devices from cover letters.

This module identifies metaphors, opening hooks, problem-solution structures,
transitions, and calls-to-action to catalog effective narrative patterns.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import date
import re
from core.confidence_scorer import calculate_confidence
from core.document_processor import DocumentType


@dataclass
class NarrativePattern:
    """
    A narrative or rhetorical pattern found in a document.

    Attributes:
        pattern_type: Type of pattern (e.g., "metaphor", "opening-hook")
        text: The actual text of the pattern
        context: Surrounding paragraphs for context
        source_document: Filepath of the source document
        date: Document date (if available)
    """
    pattern_type: str
    text: str
    context: str
    source_document: str
    date: Optional[date]


@dataclass
class NarrativeCategory:
    """
    A category of narrative patterns.

    Attributes:
        category_name: Name of the category (e.g., "Metaphors", "Opening Hooks")
        patterns: List of patterns in this category
        confidence: Confidence score (0.0-1.0) for categorization
    """
    category_name: str
    patterns: List[NarrativePattern]
    confidence: float


# Pattern detection rules
METAPHOR_PATTERNS = [
    r'\blike\s+(?:a|an|the)?\s*\w+',
    r'\bas\s+(?:a|an|the)?\s*\w+',
    r'\bsimilar\s+to\b',
    r'\bremind(?:s|ed)?\s+me\s+of\b',
]

PROBLEM_SOLUTION_PATTERNS = [
    (r'\b(challenge|problem|issue|difficulty)\b', r'\b(solution|approach|addressed|resolved|solved)\b'),
    (r'\bfaced\b', r'\b(implemented|created|developed|solved)\b'),
]

CALL_TO_ACTION_PATTERNS = [
    r'\bI\s+look\s+forward\s+to\b',
    r'\bI\s+would\s+welcome\b',
    r'\bexcited\s+to\s+discuss\b',
    r'\bI\s+would\s+(?:love|appreciate|be\s+happy)\s+to\b',
    r'\bplease\s+(?:contact|reach|call)\b',
]

TRANSITION_PATTERNS = [
    r'\bFurthermore\b',
    r'\bAdditionally\b',
    r'\bIn\s+addition(?:\s+to)?\b',
    r'\bMoreover\b',
    r'\bBuilding\s+on\b',
    r'\bSimilarly\b',
    r'\bIn\s+contrast\b',
    r'\bHowever\b',
]

OPENING_HOOK_PATTERNS = [
    r'^\s*(?:What|How|Why|Where|When|Who)\s+[^.!?]{10,}[?]',  # Question
    r'^\s*Imagine\b',  # Imagination prompt
    r'^\s*(?:In|During)\s+my\s+\w+\s+years?\b',  # Personal anecdote
]


def extract_narrative_patterns(text: str, filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """
    Extract narrative patterns from a document.

    Identifies metaphors, opening hooks, problem-solution structures,
    transitions, and calls-to-action using pattern matching.

    Args:
        text: Document text content
        filepath: Path to the source document
        doc_date: Document date (if available)

    Returns:
        List of NarrativePattern objects found in the document

    Examples:
        >>> text = "I work like a bridge between teams."
        >>> patterns = extract_narrative_patterns(text, "letter.txt", None)
        >>> len(patterns) > 0
        True
    """
    if not text or not text.strip():
        return []

    patterns = []

    # Split into paragraphs for context
    paragraphs = _split_into_paragraphs(text)

    # Extract metaphors
    patterns.extend(_extract_metaphors(text, paragraphs, filepath, doc_date))

    # Extract opening hooks (first paragraph only)
    if paragraphs:
        patterns.extend(_extract_opening_hooks(paragraphs[0], paragraphs, filepath, doc_date))

    # Extract problem-solution patterns
    patterns.extend(_extract_problem_solution(text, paragraphs, filepath, doc_date))

    # Extract calls-to-action (last paragraph especially)
    patterns.extend(_extract_calls_to_action(text, paragraphs, filepath, doc_date))

    # Extract transitions
    patterns.extend(_extract_transitions(text, paragraphs, filepath, doc_date))

    return patterns


def _split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs.

    Args:
        text: Text to split

    Returns:
        List of paragraphs
    """
    # Split on double newlines or multiple spaces
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]


def _extract_metaphors(text: str, paragraphs: List[str], filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """Extract metaphor patterns."""
    patterns = []

    for pattern_str in METAPHOR_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        for match in pattern.finditer(text):
            # Get the full sentence containing the metaphor
            sentence = _get_sentence_containing_match(text, match)
            if sentence and len(sentence) > 15:
                context = _get_context_for_text(sentence, paragraphs)

                narrative_pattern = NarrativePattern(
                    pattern_type="metaphor",
                    text=sentence,
                    context=context,
                    source_document=filepath,
                    date=doc_date
                )
                patterns.append(narrative_pattern)
                break  # Only take first match per sentence

    return patterns


def _extract_opening_hooks(first_paragraph: str, paragraphs: List[str], filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """Extract opening hook patterns from the first paragraph."""
    patterns = []

    for pattern_str in OPENING_HOOK_PATTERNS:
        pattern = re.compile(pattern_str, re.MULTILINE | re.IGNORECASE)
        match = pattern.search(first_paragraph)
        if match:
            # Get first sentence or the match
            sentences = re.split(r'[.!?]\s+', first_paragraph)
            if sentences:
                hook_text = sentences[0].strip()
                if len(hook_text) > 10:
                    context = _get_context_for_text(hook_text, paragraphs)

                    narrative_pattern = NarrativePattern(
                        pattern_type="opening-hook",
                        text=hook_text,
                        context=context,
                        source_document=filepath,
                        date=doc_date
                    )
                    patterns.append(narrative_pattern)
                    break  # Only one opening hook

    return patterns


def _extract_problem_solution(text: str, paragraphs: List[str], filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """Extract problem-solution patterns."""
    patterns = []

    for problem_pattern, solution_pattern in PROBLEM_SOLUTION_PATTERNS:
        # Look for problem followed by solution within a reasonable distance
        problem_matches = list(re.finditer(problem_pattern, text, re.IGNORECASE))
        solution_matches = list(re.finditer(solution_pattern, text, re.IGNORECASE))

        for prob_match in problem_matches:
            for sol_match in solution_matches:
                # Check if solution comes after problem within 200 characters
                if 0 < sol_match.start() - prob_match.start() < 200:
                    # Extract the problem-solution segment
                    segment = text[prob_match.start():sol_match.end() + 50]
                    sentence = _get_sentence_containing_match(text, prob_match)
                    if sentence:
                        context = _get_context_for_text(sentence, paragraphs)

                        narrative_pattern = NarrativePattern(
                            pattern_type="problem-solution",
                            text=sentence,
                            context=context,
                            source_document=filepath,
                            date=doc_date
                        )
                        patterns.append(narrative_pattern)
                        break

    return patterns


def _extract_calls_to_action(text: str, paragraphs: List[str], filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """Extract call-to-action patterns."""
    patterns = []

    for pattern_str in CALL_TO_ACTION_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        for match in pattern.finditer(text):
            sentence = _get_sentence_containing_match(text, match)
            if sentence and len(sentence) > 15:
                context = _get_context_for_text(sentence, paragraphs)

                narrative_pattern = NarrativePattern(
                    pattern_type="call-to-action",
                    text=sentence,
                    context=context,
                    source_document=filepath,
                    date=doc_date
                )
                patterns.append(narrative_pattern)
                break  # Only one per pattern type

    return patterns


def _extract_transitions(text: str, paragraphs: List[str], filepath: str, doc_date: Optional[date]) -> List[NarrativePattern]:
    """Extract transition patterns."""
    patterns = []

    for pattern_str in TRANSITION_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        for match in pattern.finditer(text):
            sentence = _get_sentence_containing_match(text, match)
            if sentence and len(sentence) > 15:
                context = _get_context_for_text(sentence, paragraphs)

                narrative_pattern = NarrativePattern(
                    pattern_type="transition",
                    text=sentence,
                    context=context,
                    source_document=filepath,
                    date=doc_date
                )
                patterns.append(narrative_pattern)

    return patterns


def _get_sentence_containing_match(text: str, match: re.Match) -> Optional[str]:
    """
    Get the complete sentence containing a regex match.

    Args:
        text: Full text
        match: Regex match object

    Returns:
        Complete sentence containing the match
    """
    # Find sentence boundaries around the match
    start_pos = match.start()

    # Find start of sentence (previous period or start of text)
    sent_start = text.rfind('.', 0, start_pos)
    if sent_start == -1:
        sent_start = text.rfind('\n', 0, start_pos)
    if sent_start == -1:
        sent_start = 0
    else:
        sent_start += 1

    # Find end of sentence (next period)
    sent_end = text.find('.', start_pos)
    if sent_end == -1:
        sent_end = text.find('\n', start_pos)
    if sent_end == -1:
        sent_end = len(text)
    else:
        sent_end += 1

    sentence = text[sent_start:sent_end].strip()
    return sentence if sentence else None


def _get_context_for_text(text_snippet: str, paragraphs: List[str]) -> str:
    """
    Find the paragraph containing a text snippet.

    Args:
        text_snippet: Text to find
        paragraphs: List of paragraphs

    Returns:
        Paragraph containing the text
    """
    for paragraph in paragraphs:
        if text_snippet in paragraph:
            return paragraph

    return text_snippet


def categorize_narrative_patterns(patterns: List[NarrativePattern]) -> List[NarrativeCategory]:
    """
    Categorize narrative patterns by type.

    Groups patterns by their pattern_type, sorts chronologically within each category,
    and calculates confidence scores.

    Args:
        patterns: List of narrative patterns to categorize

    Returns:
        List of NarrativeCategory objects

    Examples:
        >>> pat1 = NarrativePattern("metaphor", "like water", "ctx", "doc", None)
        >>> pat2 = NarrativePattern("metaphor", "as rock", "ctx", "doc", None)
        >>> categories = categorize_narrative_patterns([pat1, pat2])
        >>> len(categories)
        1
    """
    if not patterns:
        return []

    # Group by pattern type
    type_groups: Dict[str, List[NarrativePattern]] = {}
    for pattern in patterns:
        if pattern.pattern_type not in type_groups:
            type_groups[pattern.pattern_type] = []
        type_groups[pattern.pattern_type].append(pattern)

    # Create categories
    categories = []
    for pattern_type, pattern_list in type_groups.items():
        # Sort patterns chronologically
        pattern_list.sort(key=lambda p: p.date if p.date else date.min)

        # Calculate confidence
        confidence = _calculate_category_confidence(pattern_list)

        # Create category name
        category_name = _format_category_name(pattern_type)

        category = NarrativeCategory(
            category_name=category_name,
            patterns=pattern_list,
            confidence=confidence
        )
        categories.append(category)

    # Sort categories by name for consistency
    categories.sort(key=lambda c: c.category_name)

    return categories


def _format_category_name(pattern_type: str) -> str:
    """
    Format pattern type into a category name.

    Args:
        pattern_type: Pattern type string

    Returns:
        Formatted category name
    """
    # Convert "metaphor" -> "Metaphors", "opening-hook" -> "Opening Hooks"
    words = pattern_type.split('-')
    formatted = ' '.join(word.capitalize() for word in words)

    # Pluralize if not already
    if not formatted.endswith('s'):
        formatted += 's'

    return formatted


def _calculate_category_confidence(patterns: List[NarrativePattern]) -> float:
    """
    Calculate confidence score for a narrative category.

    Based on:
    - Clarity: How well-defined the patterns are
    - Frequency: Number of patterns in category
    - Diversity: Appears in multiple documents

    Args:
        patterns: List of patterns in this category

    Returns:
        Confidence score (0.0-1.0)
    """
    # Clarity: based on pattern text length (longer = more specific)
    avg_length = sum(len(p.text) for p in patterns) / len(patterns)
    clarity_score = min(1.0, avg_length / 50.0)

    # Frequency: more patterns = higher confidence
    frequency_score = min(1.0, len(patterns) / 5.0)

    # Diversity: appears in multiple documents
    documents = set(p.source_document for p in patterns)
    diversity_score = min(1.0, len(documents) / 3.0)

    # Calculate weighted confidence
    confidence = calculate_confidence(
        {
            'clarity': clarity_score,
            'frequency': frequency_score,
            'diversity': diversity_score
        },
        weights={
            'clarity': 0.4,
            'frequency': 0.3,
            'diversity': 0.3
        }
    )

    return confidence


def analyze_narratives(documents: List[Dict]) -> List[NarrativeCategory]:
    """
    Analyze narrative patterns across all documents.

    Main API function. Filters to cover letters only, extracts narrative patterns,
    categorizes them by type, and returns sorted by category name.

    Args:
        documents: List of processed document dictionaries, each containing:
            - filepath: Path to document
            - text: Document text
            - document_type: Type of document (from DocumentType enum)
            - date: Document date (optional)

    Returns:
        List of NarrativeCategory objects sorted by category name

    Examples:
        >>> docs = [{'filepath': 'letter.txt', 'text': 'I work like a bridge.',
        ...          'document_type': 'cover_letter', 'date': None}]
        >>> categories = analyze_narratives(docs)
        >>> len(categories) >= 0
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

    # Extract narrative patterns from all cover letters
    all_patterns = []
    for doc in cover_letters:
        patterns = extract_narrative_patterns(
            text=doc.get('text', ''),
            filepath=doc.get('filepath', ''),
            doc_date=doc.get('date')
        )
        all_patterns.extend(patterns)

    if not all_patterns:
        return []

    # Categorize patterns by type
    categories = categorize_narrative_patterns(all_patterns)

    return categories
