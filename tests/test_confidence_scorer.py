"""
Tests for confidence_scorer module.
"""

import pytest
from core.confidence_scorer import (
    calculate_confidence,
    should_flag_for_review,
    get_confidence_category
)


class TestCalculateConfidence:
    """Tests for calculate_confidence function."""

    def test_equal_weights_simple(self):
        """Test confidence calculation with equal weights."""
        criteria = {
            'criterion1': 0.8,
            'criterion2': 0.6,
            'criterion3': 0.7
        }
        result = calculate_confidence(criteria)
        expected = (0.8 + 0.6 + 0.7) / 3
        assert abs(result - expected) < 0.0001

    def test_equal_weights_all_ones(self):
        """Test with all criteria at maximum confidence."""
        criteria = {
            'pattern_matches': 1.0,
            'text_length': 1.0,
            'clarity': 1.0
        }
        result = calculate_confidence(criteria)
        assert result == 1.0

    def test_equal_weights_all_zeros(self):
        """Test with all criteria at minimum confidence."""
        criteria = {
            'criterion1': 0.0,
            'criterion2': 0.0,
            'criterion3': 0.0
        }
        result = calculate_confidence(criteria)
        assert result == 0.0

    def test_custom_weights(self):
        """Test confidence calculation with custom weights."""
        criteria = {
            'frequency': 0.7,
            'similarity': 0.85,
            'context_match': 0.6
        }
        weights = {
            'frequency': 2.0,
            'similarity': 1.5,
            'context_match': 1.0
        }
        result = calculate_confidence(criteria, weights)
        # (0.7*2.0 + 0.85*1.5 + 0.6*1.0) / (2.0 + 1.5 + 1.0)
        # = (1.4 + 1.275 + 0.6) / 4.5
        # = 3.275 / 4.5
        # = 0.7277777...
        expected = 3.275 / 4.5
        assert abs(result - expected) < 0.0001

    def test_custom_weights_with_high_weight(self):
        """Test that high-weighted criteria dominate the score."""
        criteria = {
            'important': 0.9,
            'minor': 0.1
        }
        weights = {
            'important': 10.0,
            'minor': 1.0
        }
        result = calculate_confidence(criteria, weights)
        # (0.9*10 + 0.1*1) / (10 + 1) = (9 + 0.1) / 11 = 9.1 / 11 = 0.8272...
        expected = 9.1 / 11
        assert abs(result - expected) < 0.0001
        # Result should be closer to 0.9 than 0.1
        assert result > 0.8

    def test_partial_weights(self):
        """Test when weights are provided only for some criteria."""
        criteria = {
            'criterion1': 0.8,
            'criterion2': 0.6,
            'criterion3': 0.7
        }
        weights = {
            'criterion1': 2.0
            # criterion2 and criterion3 should default to 1.0
        }
        result = calculate_confidence(criteria, weights)
        # (0.8*2.0 + 0.6*1.0 + 0.7*1.0) / (2.0 + 1.0 + 1.0)
        # = (1.6 + 0.6 + 0.7) / 4.0
        # = 2.9 / 4.0
        # = 0.725
        expected = 2.9 / 4.0
        assert abs(result - expected) < 0.0001

    def test_clamping_high_values(self):
        """Test that values above 1.0 are clamped."""
        criteria = {
            'criterion1': 1.5,  # Should be clamped to 1.0
            'criterion2': 0.8
        }
        result = calculate_confidence(criteria)
        # (1.0 + 0.8) / 2 = 0.9
        expected = 0.9
        assert abs(result - expected) < 0.0001

    def test_clamping_low_values(self):
        """Test that values below 0.0 are clamped."""
        criteria = {
            'criterion1': -0.5,  # Should be clamped to 0.0
            'criterion2': 0.6
        }
        result = calculate_confidence(criteria)
        # (0.0 + 0.6) / 2 = 0.3
        expected = 0.3
        assert abs(result - expected) < 0.0001

    def test_empty_criteria(self):
        """Test with empty criteria dictionary."""
        result = calculate_confidence({})
        assert result == 0.0

    def test_single_criterion(self):
        """Test with a single criterion."""
        criteria = {'only_one': 0.75}
        result = calculate_confidence(criteria)
        assert result == 0.75

    def test_zero_weights(self):
        """Test behavior when all weights are zero."""
        criteria = {
            'criterion1': 0.8,
            'criterion2': 0.6
        }
        weights = {
            'criterion1': 0.0,
            'criterion2': 0.0
        }
        result = calculate_confidence(criteria, weights)
        # Division by zero protection should return 0.0
        assert result == 0.0

    def test_weight_normalization_not_required(self):
        """Test that weights don't need to sum to 1.0."""
        criteria = {
            'criterion1': 0.8,
            'criterion2': 0.6
        }
        # Weights sum to 5.0, not 1.0
        weights = {
            'criterion1': 3.0,
            'criterion2': 2.0
        }
        result = calculate_confidence(criteria, weights)
        # (0.8*3 + 0.6*2) / (3 + 2) = (2.4 + 1.2) / 5 = 3.6 / 5 = 0.72
        expected = 0.72
        assert abs(result - expected) < 0.0001

    def test_example_from_docstring_equal_weights(self):
        """Test the equal weights example from the docstring."""
        criteria = {
            'pattern_matches': 0.8,
            'text_length': 1.0,
            'clarity': 0.9
        }
        result = calculate_confidence(criteria)
        expected = (0.8 + 1.0 + 0.9) / 3
        assert abs(result - expected) < 0.0001

    def test_example_from_docstring_custom_weights(self):
        """Test the custom weights example from the docstring."""
        criteria = {
            'frequency': 0.7,
            'similarity': 0.85,
            'context_match': 0.6
        }
        weights = {
            'frequency': 2.0,
            'similarity': 1.5,
            'context_match': 1.0
        }
        result = calculate_confidence(criteria, weights)
        expected = (0.7*2.0 + 0.85*1.5 + 0.6*1.0) / (2.0 + 1.5 + 1.0)
        assert abs(result - expected) < 0.0001


class TestShouldFlagForReview:
    """Tests for should_flag_for_review function."""

    def test_below_default_threshold(self):
        """Test flagging when below default threshold (0.75)."""
        assert should_flag_for_review(0.5) is True
        assert should_flag_for_review(0.74) is True

    def test_above_default_threshold(self):
        """Test not flagging when above default threshold."""
        assert should_flag_for_review(0.75) is False
        assert should_flag_for_review(0.8) is False
        assert should_flag_for_review(1.0) is False

    def test_custom_threshold(self):
        """Test with custom threshold."""
        assert should_flag_for_review(0.7, threshold=0.6) is False
        assert should_flag_for_review(0.5, threshold=0.6) is True

    def test_edge_cases(self):
        """Test edge cases at threshold boundaries."""
        assert should_flag_for_review(0.75, threshold=0.75) is False
        assert should_flag_for_review(0.7499999, threshold=0.75) is True
        assert should_flag_for_review(0.0, threshold=0.5) is True
        assert should_flag_for_review(1.0, threshold=0.5) is False


class TestGetConfidenceCategory:
    """Tests for get_confidence_category function."""

    def test_high_confidence(self):
        """Test high confidence category (>= 0.75)."""
        assert get_confidence_category(0.75) == "high"
        assert get_confidence_category(0.9) == "high"
        assert get_confidence_category(1.0) == "high"

    def test_medium_confidence(self):
        """Test medium confidence category (0.5 - 0.75)."""
        assert get_confidence_category(0.5) == "medium"
        assert get_confidence_category(0.6) == "medium"
        assert get_confidence_category(0.74) == "medium"

    def test_low_confidence(self):
        """Test low confidence category (< 0.5)."""
        assert get_confidence_category(0.0) == "low"
        assert get_confidence_category(0.3) == "low"
        assert get_confidence_category(0.49) == "low"

    def test_boundary_values(self):
        """Test exact boundary values."""
        assert get_confidence_category(0.75) == "high"
        assert get_confidence_category(0.7499999) == "medium"
        assert get_confidence_category(0.5) == "medium"
        assert get_confidence_category(0.4999999) == "low"
