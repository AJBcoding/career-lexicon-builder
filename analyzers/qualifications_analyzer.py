"""
Qualifications analyzer - tracks position phrasing variations across resume versions.

This module extracts work positions and their descriptions from resumes,
clusters variations of the same position, and tracks how descriptions evolve over time.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import date
import re
from utils.similarity import calculate_semantic_similarity, cluster_similar_items
from core.confidence_scorer import calculate_confidence
from core.document_processor import DocumentType


@dataclass
class QualificationVariation:
    """
    A variation of how a position/qualification was described in a resume.

    Attributes:
        text: The bullet point or description phrase
        source_document: Filepath of the source document
        date: Document date (if available)
        position_context: Job title and company context
    """
    text: str
    source_document: str
    date: Optional[date]
    position_context: str


@dataclass
class Qualification:
    """
    A work position/qualification with all its description variations.

    Attributes:
        qualification_id: Unique identifier for this qualification
        position_title: Job title (e.g., "Senior Software Engineer")
        organization: Organization/company name
        variations: List of all description variations for this position
        confidence: Confidence score (0.0-1.0) that this is well-defined
    """
    qualification_id: str
    position_title: str
    organization: str
    variations: List[QualificationVariation]
    confidence: float


# Patterns for identifying positions and organizations
POSITION_PATTERNS = [
    r'(?:^|\n)([A-Z][A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Designer|Architect|Lead|Director|Scientist|Consultant))',
    r'(?:^|\n)([A-Z][A-Za-z\s]+),\s*([A-Z][A-Za-z\s&]+(?:Inc|LLC|Corp|Company|Co\.|Ltd))',
]

# Date range patterns (to identify experience entries)
DATE_RANGE_PATTERN = r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})\s*[-–—]\s*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}|Present|Current)'

# Bullet point patterns
BULLET_PATTERNS = [r'^\s*[•●▪▸▹◦■□▫◆◇▾▴]\s*(.+)$', r'^\s*[-*]\s*(.+)$']


def extract_qualifications_from_resume(text: str, filepath: str, doc_date: Optional[date]) -> List[QualificationVariation]:
    """
    Extract qualification variations from a resume.

    Parses resume structure to identify positions, organizations, and bullet points.
    Each bullet point becomes a qualification variation associated with its position context.

    Args:
        text: Resume text content
        filepath: Path to the source document
        doc_date: Document date (if available)

    Returns:
        List of QualificationVariation objects found in the resume

    Examples:
        >>> text = "Software Engineer at TechCorp\\n• Built APIs"
        >>> variations = extract_qualifications_from_resume(text, "resume.txt", None)
        >>> len(variations) > 0
        True
    """
    if not text or not text.strip():
        return []

    variations = []

    # Split text into lines for processing
    lines = text.split('\n')

    # Try to identify sections and extract positions
    current_position = None
    current_organization = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Check if this line is a position/title
        position_match = _extract_position_and_org(line, lines, i)
        if position_match:
            current_position = position_match.get('position', '')
            current_organization = position_match.get('organization', '')
            continue

        # Check if this line is a bullet point
        bullet_text = _extract_bullet_point(line)
        if bullet_text:
            # Create a variation for this bullet
            position_context = _format_position_context(current_position, current_organization)

            variation = QualificationVariation(
                text=bullet_text,
                source_document=filepath,
                date=doc_date,
                position_context=position_context
            )
            variations.append(variation)

    return variations


def _extract_position_and_org(line: str, lines: List[str], index: int) -> Optional[Dict[str, str]]:
    """
    Extract position title and organization from a line and surrounding context.

    Args:
        line: Current line to analyze
        lines: All lines in the document
        index: Index of current line

    Returns:
        Dict with 'position' and 'organization' keys, or None if not a position
    """
    # Pattern 1: "Position Title, Organization"
    match = re.match(r'^([A-Z][A-Za-z\s&]+),\s*([A-Z][A-Za-z\s&.,]+(?:Inc|LLC|Corp|Company|Co|Ltd|Corporation)?.*)$', line)
    if match:
        return {
            'position': match.group(1).strip(),
            'organization': match.group(2).strip()
        }

    # Pattern 2: "Position Title at Organization"
    match = re.match(r'^([A-Z][A-Za-z\s&]+)\s+at\s+([A-Z][A-Za-z\s&.,]+.*)$', line, re.IGNORECASE)
    if match:
        return {
            'position': match.group(1).strip(),
            'organization': match.group(2).strip()
        }

    # Pattern 3: Position title on one line, org on next line
    if index + 1 < len(lines):
        next_line = lines[index + 1].strip()
        # Check if current line looks like a position title
        if re.match(r'^[A-Z][A-Za-z\s&]+(Engineer|Developer|Manager|Analyst|Designer|Architect|Lead|Director|Scientist)', line):
            # Check if next line looks like an organization
            if re.match(r'^[A-Z][A-Za-z\s&.,]+', next_line) and not re.match(DATE_RANGE_PATTERN, next_line):
                return {
                    'position': line.strip(),
                    'organization': next_line.strip()
                }

    # Pattern 4: Just a position title with common job words
    if re.search(r'\b(Engineer|Developer|Manager|Analyst|Designer|Architect|Lead|Director|Scientist|Consultant)\b', line):
        return {
            'position': line.strip(),
            'organization': ''
        }

    return None


def _extract_bullet_point(line: str) -> Optional[str]:
    """
    Extract text from a bullet point line.

    Args:
        line: Line to check for bullet point

    Returns:
        Bullet text without the bullet character, or None
    """
    for pattern in BULLET_PATTERNS:
        match = re.match(pattern, line)
        if match:
            return match.group(1).strip()

    return None


def _format_position_context(position: Optional[str], organization: Optional[str]) -> str:
    """
    Format position and organization into a context string.

    Args:
        position: Position title
        organization: Organization name

    Returns:
        Formatted context string
    """
    if position and organization:
        return f"{position} at {organization}"
    elif position:
        return position
    elif organization:
        return organization
    else:
        return "Unknown Position"


def cluster_qualification_variations(variations: List[QualificationVariation]) -> List[Qualification]:
    """
    Cluster qualification variations by position and organization.

    Groups variations that describe the same position/role together using semantic
    similarity of position contexts. Sorts variations chronologically (most recent first).

    Args:
        variations: List of qualification variations to cluster

    Returns:
        List of Qualification objects, each containing clustered variations

    Examples:
        >>> var1 = QualificationVariation("Led team", "doc1", None, "Engineer at Co")
        >>> var2 = QualificationVariation("Managed team", "doc2", None, "Engineer at Co")
        >>> quals = cluster_qualification_variations([var1, var2])
        >>> len(quals)
        1
    """
    if not variations:
        return []

    if len(variations) == 1:
        # Single variation = single qualification
        var = variations[0]
        position, org = _parse_position_context(var.position_context)
        qual_id = _generate_qualification_id(position, org)

        return [Qualification(
            qualification_id=qual_id,
            position_title=position,
            organization=org,
            variations=[var],
            confidence=0.6  # Lower confidence for single occurrence
        )]

    # Cluster by position context similarity
    contexts = [v.position_context for v in variations]
    clusters = cluster_similar_items(contexts, threshold=0.6)

    # Build Qualification objects from clusters
    qualifications = []
    for cluster in clusters:
        # Find variations for this cluster
        cluster_variations = []
        for context in cluster:
            for var in variations:
                if var.position_context == context and var not in cluster_variations:
                    cluster_variations.append(var)
                    break

        # Sort variations chronologically (most recent first)
        cluster_variations.sort(key=lambda x: x.date if x.date else date.min, reverse=True)

        # Determine position and organization from most common/recent variation
        representative_var = cluster_variations[0]
        position, org = _parse_position_context(representative_var.position_context)

        # Generate qualification ID
        qual_id = _generate_qualification_id(position, org)

        # Calculate confidence
        confidence = _calculate_qualification_confidence(cluster_variations, position, org)

        qualification = Qualification(
            qualification_id=qual_id,
            position_title=position,
            organization=org,
            variations=cluster_variations,
            confidence=confidence
        )
        qualifications.append(qualification)

    return qualifications


def _parse_position_context(context: str) -> tuple[str, str]:
    """
    Parse position context into position and organization.

    Args:
        context: Position context string

    Returns:
        Tuple of (position, organization)
    """
    # Try "Position at Organization" format
    match = re.match(r'^(.+?)\s+at\s+(.+)$', context, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Try "Position, Organization" format
    match = re.match(r'^(.+?),\s*(.+)$', context)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Default: treat entire context as position
    return context.strip(), ""


def _generate_qualification_id(position: str, organization: str) -> str:
    """
    Generate a unique identifier for a qualification.

    Args:
        position: Position title
        organization: Organization name

    Returns:
        Qualification ID (e.g., "engineer_techcorp")
    """
    # Convert to lowercase, replace spaces with underscores
    position_slug = re.sub(r'\W+', '_', position.lower()).strip('_')
    org_slug = re.sub(r'\W+', '_', organization.lower()).strip('_')

    if org_slug:
        return f"{position_slug}_{org_slug}"
    else:
        return position_slug


def _calculate_qualification_confidence(variations: List[QualificationVariation],
                                       position: str, organization: str) -> float:
    """
    Calculate confidence score for a qualification.

    Based on:
    - Clarity of position title
    - Presence of organization
    - Number of variations (frequency)

    Args:
        variations: List of variations for this qualification
        position: Position title
        organization: Organization name

    Returns:
        Confidence score (0.0-1.0)
    """
    # Clarity score: well-defined position and org
    has_position = len(position) > 0 and position != "Unknown Position"
    has_org = len(organization) > 0
    clarity_score = 0.5 if has_position else 0.0
    if has_org:
        clarity_score += 0.5

    # Frequency score: more variations = higher confidence
    frequency_score = min(1.0, len(variations) / 5.0)

    # Document diversity: appears in multiple documents
    documents = set(v.source_document for v in variations)
    diversity_score = min(1.0, len(documents) / 3.0)

    # Calculate weighted confidence
    confidence = calculate_confidence(
        {
            'clarity': clarity_score,
            'frequency': frequency_score,
            'diversity': diversity_score
        },
        weights={
            'clarity': 0.5,
            'frequency': 0.3,
            'diversity': 0.2
        }
    )

    return confidence


def analyze_qualifications(documents: List[Dict]) -> List[Qualification]:
    """
    Analyze qualifications across all documents.

    Main API function. Filters to resumes only, extracts qualification variations,
    clusters them by position, and returns sorted by date (most recent first).

    Args:
        documents: List of processed document dictionaries, each containing:
            - filepath: Path to document
            - text: Document text
            - document_type: Type of document (from DocumentType enum)
            - date: Document date (optional)

    Returns:
        List of Qualification objects sorted by date (most recent first)

    Examples:
        >>> docs = [{'filepath': 'resume.txt', 'text': 'Engineer at Co\\n• Built apps',
        ...          'document_type': 'resume', 'date': None}]
        >>> quals = analyze_qualifications(docs)
        >>> len(quals) >= 0
        True
    """
    if not documents:
        return []

    # Filter to resumes only
    resumes = [
        doc for doc in documents
        if doc.get('document_type') == DocumentType.RESUME.value
    ]

    if not resumes:
        return []

    # Extract qualification variations from all resumes
    all_variations = []
    for doc in resumes:
        variations = extract_qualifications_from_resume(
            text=doc.get('text', ''),
            filepath=doc.get('filepath', ''),
            doc_date=doc.get('date')
        )
        all_variations.extend(variations)

    if not all_variations:
        return []

    # Cluster variations into qualifications
    qualifications = cluster_qualification_variations(all_variations)

    # Sort by most recent variation date (most recent first)
    def get_most_recent_date(qual: Qualification) -> date:
        dates = [v.date for v in qual.variations if v.date]
        return max(dates) if dates else date.min

    qualifications.sort(key=get_most_recent_date, reverse=True)

    return qualifications
