"""
Confidence scoring utilities for analysis outputs.

This module provides functions to calculate confidence scores based on
multiple criteria with optional weighting.
"""

from typing import Dict, Optional


def calculate_confidence(
    criteria: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate a weighted confidence score from multiple criteria.

    Args:
        criteria: Dictionary of criterion names to scores (0.0-1.0)
        weights: Optional dictionary of criterion names to weights.
                If None, all criteria are weighted equally.

    Returns:
        Weighted average confidence score, clamped to [0.0, 1.0]

    Examples:
        >>> # Equal weights
        >>> calculate_confidence({
        ...     'pattern_matches': 0.8,
        ...     'text_length': 1.0,
        ...     'clarity': 0.9
        ... })
        0.9

        >>> # Custom weights
        >>> calculate_confidence({
        ...     'frequency': 0.7,
        ...     'similarity': 0.85,
        ...     'context_match': 0.6
        ... }, weights={
        ...     'frequency': 2.0,
        ...     'similarity': 1.5,
        ...     'context_match': 1.0
        ... })
        0.7277777777777777
    """
    if not criteria:
        return 0.0

    # If no weights provided, use equal weights of 1.0
    if weights is None:
        weights = {key: 1.0 for key in criteria.keys()}

    # Calculate weighted sum
    weighted_sum = 0.0
    total_weight = 0.0

    for key, score in criteria.items():
        # Get weight for this criterion (default to 1.0 if not specified)
        weight = weights.get(key, 1.0)

        # Clamp score to [0.0, 1.0] to handle any out-of-range inputs
        clamped_score = max(0.0, min(1.0, score))

        weighted_sum += clamped_score * weight
        total_weight += weight

    # Avoid division by zero
    if total_weight == 0.0:
        return 0.0

    # Calculate weighted average
    result = weighted_sum / total_weight

    # Clamp result to [0.0, 1.0]
    return max(0.0, min(1.0, result))


def should_flag_for_review(confidence: float, threshold: float = 0.75) -> bool:
    """
    Determine if a confidence score should be flagged for manual review.

    Args:
        confidence: Confidence score (0.0-1.0)
        threshold: Minimum confidence threshold (default 0.75)

    Returns:
        True if confidence is below threshold

    Examples:
        >>> should_flag_for_review(0.5)
        True
        >>> should_flag_for_review(0.8)
        False
        >>> should_flag_for_review(0.7, threshold=0.6)
        False
    """
    return confidence < threshold


def get_confidence_category(confidence: float) -> str:
    """
    Categorize a confidence score as high, medium, or low.

    Args:
        confidence: Confidence score (0.0-1.0)

    Returns:
        Category string: "high", "medium", or "low"

    Examples:
        >>> get_confidence_category(0.9)
        'high'
        >>> get_confidence_category(0.6)
        'medium'
        >>> get_confidence_category(0.3)
        'low'
    """
    if confidence >= 0.75:
        return "high"
    elif confidence >= 0.5:
        return "medium"
    else:
        return "low"
