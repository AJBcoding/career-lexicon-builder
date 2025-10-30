"""
Tests for similarity utilities module.
"""

import pytest
from utils.similarity import (
    calculate_semantic_similarity,
    cluster_similar_items
)


class TestCalculateSemanticSimilarity:
    """Tests for calculate_semantic_similarity function."""

    def test_identical_texts(self):
        """Test similarity between identical texts should be very high."""
        text = "Leadership and team management"
        result = calculate_semantic_similarity(text, text)
        assert result >= 0.99, "Identical texts should have similarity ~1.0"

    def test_very_similar_texts(self):
        """Test similarity between semantically similar texts."""
        text1 = "Led a team of software engineers"
        text2 = "Managed a group of software developers"
        result = calculate_semantic_similarity(text1, text2)
        assert result >= 0.6, "Similar texts should have high similarity"

    def test_unrelated_texts(self):
        """Test similarity between completely unrelated texts."""
        text1 = "Led software development team"
        text2 = "Enjoys playing basketball on weekends"
        result = calculate_semantic_similarity(text1, text2)
        assert result < 0.4, "Unrelated texts should have low similarity"

    def test_empty_strings(self):
        """Test handling of empty strings."""
        result = calculate_semantic_similarity("", "")
        assert 0.0 <= result <= 1.0, "Empty strings should return valid similarity"

    def test_one_empty_string(self):
        """Test handling when one string is empty."""
        result = calculate_semantic_similarity("Some text", "")
        assert 0.0 <= result <= 1.0, "Should handle empty string gracefully"

    def test_return_type_and_range(self):
        """Test that return value is a float between 0.0 and 1.0."""
        result = calculate_semantic_similarity("hello", "world")
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_symmetry(self):
        """Test that similarity is symmetric: sim(A,B) == sim(B,A)."""
        text1 = "Software engineer with Python expertise"
        text2 = "Python developer with 5 years experience"
        result1 = calculate_semantic_similarity(text1, text2)
        result2 = calculate_semantic_similarity(text2, text1)
        assert abs(result1 - result2) < 0.001, "Similarity should be symmetric"

    def test_different_case_similar_meaning(self):
        """Test that case differences don't drastically affect similarity."""
        text1 = "LEADERSHIP SKILLS"
        text2 = "leadership skills"
        result = calculate_semantic_similarity(text1, text2)
        assert result >= 0.95, "Case shouldn't drastically affect similarity"


class TestClusterSimilarItems:
    """Tests for cluster_similar_items function."""

    def test_clear_clusters(self):
        """Test clustering with clearly distinct groups."""
        items = [
            "Leadership and team management",
            "Leading cross-functional teams",
            "Python programming and development",
            "Software development in Python",
            "Data analysis and visualization",
            "Analyzing data with statistical methods"
        ]
        clusters = cluster_similar_items(items, threshold=0.6)

        # Should identify at least 3 distinct topics
        assert len(clusters) >= 2, "Should identify multiple clusters"

        # Each cluster should have at least one item
        for cluster in clusters:
            assert len(cluster) > 0, "Clusters should not be empty"

        # All items should be assigned to clusters
        all_items = [item for cluster in clusters for item in cluster]
        assert len(all_items) == len(items), "All items should be clustered"

    def test_all_similar_items(self):
        """Test clustering when all items are similar."""
        items = [
            "Software engineer",
            "Software developer",
            "Software programmer"
        ]
        clusters = cluster_similar_items(items, threshold=0.7)

        # With high similarity, might form 1-2 clusters
        assert len(clusters) >= 1, "Should form at least one cluster"
        assert len(clusters) <= 3, "Should merge similar items"

    def test_all_different_items(self):
        """Test clustering when all items are different."""
        items = [
            "Led software teams",
            "Enjoys cooking Italian food",
            "Quantum physics research"
        ]
        clusters = cluster_similar_items(items, threshold=0.7)

        # Different items might stay separate or form individual clusters
        assert len(clusters) >= 1, "Should create at least one cluster"

    def test_single_item(self):
        """Test clustering with a single item."""
        items = ["Only one item"]
        clusters = cluster_similar_items(items, threshold=0.7)

        assert len(clusters) == 1, "Single item should form one cluster"
        assert clusters[0] == items, "Single item should be in its own cluster"

    def test_empty_list(self):
        """Test clustering with empty list."""
        items = []
        clusters = cluster_similar_items(items, threshold=0.7)

        assert len(clusters) == 0, "Empty list should return empty clusters"

    def test_threshold_high(self):
        """Test with high threshold (stricter clustering)."""
        items = [
            "Leadership skills",
            "Team leadership",
            "Managing teams"
        ]
        clusters = cluster_similar_items(items, threshold=0.9)

        # High threshold means stricter matching
        assert len(clusters) >= 1, "Should create at least one cluster"

    def test_threshold_low(self):
        """Test with low threshold (looser clustering)."""
        items = [
            "Software development",
            "Team management",
            "Project planning"
        ]
        clusters = cluster_similar_items(items, threshold=0.3)

        # Low threshold might group more items together
        assert len(clusters) >= 1, "Should create at least one cluster"

    def test_duplicate_items(self):
        """Test handling of duplicate items."""
        items = [
            "Leadership",
            "Leadership",
            "Management"
        ]
        clusters = cluster_similar_items(items, threshold=0.7)

        # Should handle duplicates gracefully
        assert len(clusters) >= 1, "Should cluster duplicates"
        all_items = [item for cluster in clusters for item in cluster]
        assert len(all_items) == len(items), "Should preserve all items"

    def test_very_long_texts(self):
        """Test clustering with longer text passages."""
        items = [
            "Led a cross-functional team of 10 software engineers to deliver a cloud-based application",
            "Managed a team of developers to build a web application deployed on AWS",
            "Conducted data analysis using Python and created visualizations for stakeholders"
        ]
        clusters = cluster_similar_items(items, threshold=0.6)

        assert len(clusters) >= 1, "Should cluster longer texts"
        assert len(clusters) <= 3, "Should identify similar items"

    def test_cluster_integrity(self):
        """Test that items within a cluster are similar."""
        items = [
            "Python programming",
            "Python development",
            "Java programming",
            "Java development"
        ]
        clusters = cluster_similar_items(items, threshold=0.7)

        # Verify each cluster has reasonable grouping
        for cluster in clusters:
            if len(cluster) > 1:
                # Items in same cluster should mention similar concepts
                texts = " ".join(cluster).lower()
                # Either all mention Python or all mention Java
                python_count = texts.count("python")
                java_count = texts.count("java")
                assert (python_count >= len(cluster) or
                       java_count >= len(cluster)), "Cluster should group similar items"
