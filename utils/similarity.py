"""
Semantic similarity and clustering utilities for career lexicon builder.

This module provides functions for calculating semantic similarity between texts
and clustering similar items together. Uses sentence-transformers for embeddings
and scikit-learn for clustering algorithms.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering


# Load the model once at module level for efficiency
# Using a lightweight model that works well for semantic similarity
_model = None


def _get_model() -> SentenceTransformer:
    """
    Get or initialize the sentence transformer model.

    Returns:
        SentenceTransformer: Pre-trained sentence embedding model
    """
    global _model
    if _model is None:
        # Using 'all-MiniLM-L6-v2' - small, fast, and good quality
        # 384 dimensions, ~80MB
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two text strings.

    Uses sentence embeddings to compute cosine similarity between the semantic
    representations of the two texts. Returns a score between 0.0 (completely
    different) and 1.0 (identical meaning).

    Args:
        text1: First text string
        text2: Second text string

    Returns:
        float: Similarity score between 0.0 and 1.0

    Examples:
        >>> calculate_semantic_similarity("software engineer", "software developer")
        0.85  # High similarity
        >>> calculate_semantic_similarity("coding", "cooking")
        0.15  # Low similarity
    """
    # Handle empty strings
    if not text1 and not text2:
        return 1.0  # Both empty = identical
    if not text1 or not text2:
        return 0.0  # One empty = no similarity

    # Get the model
    model = _get_model()

    # Encode both texts to embeddings
    embeddings = model.encode([text1, text2])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity([embeddings[0]], [embeddings[1]])
    similarity = float(similarity_matrix[0][0])

    # Ensure result is in [0, 1] range (cosine similarity can be slightly negative)
    similarity = max(0.0, min(1.0, similarity))

    return similarity


def cluster_similar_items(items: List[str], threshold: float = 0.7) -> List[List[str]]:
    """
    Cluster similar items together based on semantic similarity.

    Groups items that have semantic similarity above the threshold into clusters.
    Uses agglomerative (hierarchical) clustering with average linkage.

    Args:
        items: List of text strings to cluster
        threshold: Similarity threshold (0.0-1.0). Higher = stricter clustering.
                  Default 0.7 means items must be 70% similar to cluster together.

    Returns:
        List of clusters, where each cluster is a list of similar items.
        Items appear in the same order as input within each cluster.

    Examples:
        >>> items = ["software engineer", "software developer", "data scientist"]
        >>> clusters = cluster_similar_items(items, threshold=0.7)
        >>> len(clusters)
        2  # First two cluster together, third separate
    """
    # Handle edge cases
    if not items:
        return []

    if len(items) == 1:
        return [items]

    # Get the model
    model = _get_model()

    # Encode all items to embeddings
    embeddings = model.encode(items)

    # Calculate pairwise cosine similarities
    similarity_matrix = cosine_similarity(embeddings)

    # Convert similarity to distance for clustering
    # Distance = 1 - similarity
    distance_matrix = 1 - similarity_matrix

    # Convert threshold to distance threshold
    distance_threshold = 1 - threshold

    # Use agglomerative clustering with average linkage
    # distance_threshold determines when to stop merging clusters
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric='precomputed',
        linkage='average'
    )

    # Fit the clustering model
    cluster_labels = clustering.fit_predict(distance_matrix)

    # Group items by cluster label
    clusters_dict = {}
    for idx, label in enumerate(cluster_labels):
        if label not in clusters_dict:
            clusters_dict[label] = []
        clusters_dict[label].append(items[idx])

    # Convert to list of clusters
    clusters = list(clusters_dict.values())

    return clusters
