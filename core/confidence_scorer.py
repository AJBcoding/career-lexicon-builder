"""
Confidence scoring utilities for document classification.

This module provides functions to calculate confidence scores from multiple
criteria, flag low-confidence results for review, and categorize confidence levels.
"""

from typing import Dict, Optional


def calculate_confidence(
    criteria: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate weighted confidence score from multiple criteria.

    Args:
        criteria: Dictionary of criterion name to score (0.0-1.0).
                 Values outside this range are clamped.
        weights: Optional dictionary of criterion name to weight.
                Missing criteria default to weight 1.0.
                If None, all criteria weighted equally.

    Returns:
        Weighted average confidence score (0.0-1.0)

    Examples:
        >>> # Equal weights
        >>> criteria = {
        ...     'pattern_matches': 0.8,
        ...     'text_length': 1.0,
        ...     'clarity': 0.9
        ... }
        >>> calculate_confidence(criteria)
        0.9

        >>> # Custom weights
        >>> criteria = {
        ...     'frequency': 0.7,
        ...     'similarity': 0.85,
        ...     'context_match': 0.6
        ... }
        >>> weights = {
        ...     'frequency': 2.0,
        ...     'similarity': 1.5,
        ...     'context_match': 1.0
        ... }
        >>> calculate_confidence(criteria, weights)
        0.7277777777777777
    """
    if not criteria:
        return 0.0

    # Clamp all criteria values to [0.0, 1.0]
    clamped_criteria = {
        k: max(0.0, min(1.0, v))
        for k, v in criteria.items()
    }

    # Default weights to 1.0 for all criteria if not provided
    if weights is None:
        weights = {k: 1.0 for k in criteria.keys()}
    else:
        # Fill in missing weights with 1.0
        weights = {
            k: weights.get(k, 1.0)
            for k in criteria.keys()
        }

    # Calculate weighted sum
    weighted_sum = sum(
        clamped_criteria[k] * weights[k]
        for k in criteria.keys()
    )

    # Calculate total weight
    total_weight = sum(weights.values())

    # Handle division by zero
    if total_weight == 0.0:
        return 0.0

    return weighted_sum / total_weight


def should_flag_for_review(confidence: float, threshold: float = 0.75) -> bool:
    """
    Determine if a confidence score should be flagged for manual review.

    Args:
        confidence: Confidence score (0.0-1.0)
        threshold: Minimum acceptable confidence (default: 0.75)

    Returns:
        True if confidence is below threshold, False otherwise

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
    Categorize confidence score into low/medium/high.

    Args:
        confidence: Confidence score (0.0-1.0)

    Returns:
        "high" (>= 0.75), "medium" (0.5-0.75), or "low" (< 0.5)

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
