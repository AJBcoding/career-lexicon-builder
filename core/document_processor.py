"""
Document classification and processing utilities.

This module provides functions to classify documents as resumes, cover letters,
or job descriptions using filename patterns and content analysis.
"""

import re
from enum import Enum
from typing import Tuple, Optional
from core.confidence_scorer import calculate_confidence


class DocumentType(Enum):
    """Document type classifications."""
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"


def classify_by_filename(filename: str) -> Optional[DocumentType]:
    """
    Classify document type based on filename patterns.

    Args:
        filename: Filename to analyze (can include path)

    Returns:
        DocumentType if pattern matched, None otherwise

    Examples:
        >>> classify_by_filename("resume-2024.pdf")
        <DocumentType.RESUME: 'resume'>
        >>> classify_by_filename("cover_letter.docx")
        <DocumentType.COVER_LETTER: 'cover_letter'>
        >>> classify_by_filename("random_document.pdf")
        None
    """
    filename_lower = filename.lower()

    # Resume patterns (use simple substring matching for reliability)
    resume_patterns = [
        r'resume',
        r'\bcv\b',
        r'curriculum.vitae',
    ]

    # Cover letter patterns
    cover_patterns = [
        r'\bcover.?letter\b',
        r'\bletter\b',
    ]

    # Job description patterns
    job_patterns = [
        r'\bjob.?description\b',
        r'\bjob.?posting\b',
        r'\bposition.?description\b',
    ]

    # Check patterns in order of specificity
    for pattern in resume_patterns:
        if re.search(pattern, filename_lower):
            return DocumentType.RESUME

    for pattern in cover_patterns:
        if re.search(pattern, filename_lower):
            return DocumentType.COVER_LETTER

    for pattern in job_patterns:
        if re.search(pattern, filename_lower):
            return DocumentType.JOB_DESCRIPTION

    return None


def classify_by_content(text: str) -> Tuple[DocumentType, float, str]:
    """
    Classify document type based on content analysis.

    Analyzes text structure, keywords, and patterns to determine document type.

    Args:
        text: Document text to analyze

    Returns:
        Tuple of (DocumentType, confidence, reasoning)

    Examples:
        >>> text = "Dear Hiring Manager,\\n\\nI am writing to express..."
        >>> doc_type, conf, reason = classify_by_content(text)
        >>> doc_type == DocumentType.COVER_LETTER
        True
    """
    if not text or len(text.strip()) < 50:
        return (DocumentType.UNKNOWN, 0.0, "Text too short for classification")

    text_lower = text.lower()
    lines = text.split('\n')

    # Initialize scoring
    resume_score = 0.0
    cover_score = 0.0
    job_score = 0.0
    indicators = []

    # === COVER LETTER INDICATORS ===

    # Salutations (strong indicator)
    salutations = [r'\bdear\s+\w+', r'\bhello\s+\w+', r'\bto whom it may concern\b']
    if any(re.search(pattern, text_lower) for pattern in salutations):
        cover_score += 0.4
        indicators.append("salutation found")

    # Closings (strong indicator)
    closings = [r'\bsincerely\b', r'\bbest regards\b', r'\byours truly\b',
                r'\brespectfully\b', r'\bthank you for your consideration\b']
    if any(re.search(pattern, text_lower) for pattern in closings):
        cover_score += 0.4
        indicators.append("closing found")

    # Cover letter phrases
    cover_phrases = [
        r'i am writing to',
        r'i am interested in',
        r'i would like to apply',
        r'i am excited to',
        r'my experience makes me',
    ]
    cover_phrase_matches = sum(1 for phrase in cover_phrases if phrase in text_lower)
    if cover_phrase_matches > 0:
        cover_score += min(0.3, cover_phrase_matches * 0.1)
        indicators.append(f"{cover_phrase_matches} cover letter phrases")

    # Paragraph-heavy structure (more prose, fewer bullets)
    bullet_chars = text.count('•') + text.count('*') + text.count('-')
    if len(text) > 200:
        bullet_density = bullet_chars / len(text)
        if bullet_density < 0.01:  # Very few bullets
            cover_score += 0.2
            indicators.append("paragraph-heavy structure")

    # === RESUME INDICATORS ===

    # Section headers (strong indicator)
    resume_sections = [
        r'\bexperience\b',
        r'\beducation\b',
        r'\bskills\b',
        r'\bcertifications?\b',
        r'\bqualifications?\b',
        r'\bprofessional summary\b',
        r'\bwork history\b',
    ]
    section_matches = sum(1 for section in resume_sections if re.search(section, text_lower))
    if section_matches >= 2:
        resume_score += 0.5
        indicators.append(f"{section_matches} resume sections")
    elif section_matches == 1:
        resume_score += 0.2
        indicators.append("1 resume section")

    # Date ranges (job history indicator)
    date_range_patterns = [
        r'\d{4}\s*[-–—]\s*\d{4}',  # 2020-2024
        r'\d{4}\s*[-–—]\s*present',  # 2020-present
        r'\w+\s+\d{4}\s*[-–—]\s*\w+\s+\d{4}',  # Jan 2020 - Dec 2024
    ]
    date_range_matches = sum(len(re.findall(pattern, text_lower))
                            for pattern in date_range_patterns)
    if date_range_matches >= 2:
        resume_score += 0.3
        indicators.append(f"{date_range_matches} date ranges")

    # Bullet-heavy structure
    if len(text) > 200:
        bullet_density = bullet_chars / len(text)
        if bullet_density > 0.02:  # Many bullets
            resume_score += 0.3
            indicators.append("bullet-heavy structure")

    # Email/phone patterns
    contact_patterns = [
        r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b',
        r'\b\d{3}[-.)]\s*\d{3}[-.)]\s*\d{4}\b',
    ]
    if any(re.search(pattern, text_lower) for pattern in contact_patterns):
        resume_score += 0.1
        indicators.append("contact info")

    # === JOB DESCRIPTION INDICATORS ===

    # Job posting phrases
    job_phrases = [
        r'we are seeking',
        r'we are looking for',
        r'responsibilities include',
        r'required qualifications',
        r'preferred qualifications',
        r'job requirements',
        r'position requires',
        r'you will be responsible',
        r'the ideal candidate',
    ]
    job_phrase_matches = sum(1 for phrase in job_phrases if phrase in text_lower)
    if job_phrase_matches >= 2:
        job_score += 0.5
        indicators.append(f"{job_phrase_matches} job posting phrases")
    elif job_phrase_matches == 1:
        job_score += 0.2
        indicators.append("1 job posting phrase")

    # Company voice (3rd person)
    company_patterns = [
        r'\bour company\b',
        r'\bour team\b',
        r'\bwe offer\b',
        r'\bjoin us\b',
    ]
    company_matches = sum(1 for pattern in company_patterns if re.search(pattern, text_lower))
    if company_matches > 0:
        job_score += min(0.3, company_matches * 0.15)
        indicators.append(f"{company_matches} company phrases")

    # === DETERMINE CLASSIFICATION ===

    scores = {
        DocumentType.RESUME: resume_score,
        DocumentType.COVER_LETTER: cover_score,
        DocumentType.JOB_DESCRIPTION: job_score,
    }

    max_score = max(scores.values())

    # Need minimum confidence threshold
    if max_score < 0.3:
        reasoning = f"Ambiguous document (max score: {max_score:.2f}). " + "; ".join(indicators)
        return (DocumentType.UNKNOWN, max_score, reasoning)

    # Determine winner
    doc_type = max(scores, key=scores.get)

    # Normalize confidence to 0-1 scale (scores can exceed 1.0)
    confidence = min(1.0, max_score)

    reasoning = f"{doc_type.value} (score: {max_score:.2f}). " + "; ".join(indicators)

    return (doc_type, confidence, reasoning)


def classify_document(filepath: str, text: str) -> Tuple[DocumentType, float, str]:
    """
    Classify document using filename and content analysis.

    Tries filename classification first, then falls back to content analysis.
    Uses confidence scoring to determine reliability.

    Args:
        filepath: Path to document file
        text: Extracted document text

    Returns:
        Tuple of (DocumentType, confidence, reasoning)

    Examples:
        >>> classify_document("resume.pdf", "Experience\\n2020-2024...")
        (<DocumentType.RESUME: 'resume'>, 0.95, 'Filename match: resume')
    """
    # Extract filename from path
    import os
    filename = os.path.basename(filepath)

    # Try filename classification first
    filename_type = classify_by_filename(filename)

    if filename_type is not None:
        # High confidence from filename match
        reasoning = f"Filename match: {filename_type.value}"
        return (filename_type, 0.95, reasoning)

    # Fall back to content classification
    doc_type, confidence, reasoning = classify_by_content(text)

    reasoning = f"Content analysis: {reasoning}"

    return (doc_type, confidence, reasoning)
