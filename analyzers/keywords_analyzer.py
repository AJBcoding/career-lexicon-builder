"""
Keywords analyzer - builds cross-referenced keyword index showing usage contexts.

This module extracts significant keywords/phrases from documents and tracks
where and how they're used across resumes, cover letters, and job descriptions.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set
from datetime import date
from collections import Counter, defaultdict
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from core.document_processor import DocumentType


@dataclass
class KeywordUsage:
    """
    A single usage of a keyword in a document.

    Attributes:
        keyword: The keyword or phrase
        context: Sentence containing the keyword
        source_document: Filepath of the source document
        document_type: Type of document (resume, cover_letter, job_description)
        date: Document date (if available)
    """
    keyword: str
    context: str
    source_document: str
    document_type: str
    date: Optional[date]


@dataclass
class KeywordEntry:
    """
    An entry in the keyword index with all usages.

    Attributes:
        keyword: The main keyword
        aliases: List of similar/related terms
        usages: All usages of this keyword across documents
        frequency: Total count of usages
        document_types: Set of document types where it appears
    """
    keyword: str
    aliases: List[str]
    usages: List[KeywordUsage]
    frequency: int
    document_types: Set[str] = field(default_factory=set)


# Common English stopwords to filter out
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'have', 'had', 'been', 'were', 'would',
    'could', 'should', 'may', 'might', 'can', 'this', 'these', 'those',
    'i', 'you', 'we', 'they', 'my', 'your', 'our', 'their', 'his', 'her'
}

# Minimum keyword length
MIN_KEYWORD_LENGTH = 10

# Load the model once at module level for efficiency
_model = None


def _get_model() -> SentenceTransformer:
    """
    Get or initialize the sentence transformer model.

    Returns:
        SentenceTransformer: Pre-trained sentence embedding model
    """
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def extract_keywords_from_document(text: str, filepath: str, doc_type: str,
                                   doc_date: Optional[date]) -> List[KeywordUsage]:
    """
    Extract keywords and phrases from a document.

    Uses n-gram extraction (2-4 words) with stopword filtering to identify
    significant terms. Captures the sentence context for each keyword.

    Args:
        text: Document text content
        filepath: Path to the source document
        doc_type: Document type (resume, cover_letter, job_description)
        doc_date: Document date (if available)

    Returns:
        List of KeywordUsage objects found in the document

    Examples:
        >>> text = "I have experience in project management and software development."
        >>> usages = extract_keywords_from_document(text, "resume.txt", "resume", None)
        >>> len(usages) > 0
        True
    """
    if not text or not text.strip():
        return []

    usages = []

    # Split into sentences for context
    sentences = _split_into_sentences(text)

    # Extract n-grams from each sentence
    for sentence in sentences:
        # Extract 2-gram, 3-gram, and 4-gram phrases
        keywords = _extract_ngrams(sentence, min_n=2, max_n=4)

        # Filter and create usages
        for keyword in keywords:
            # Skip if too short or all stopwords
            if len(keyword) < MIN_KEYWORD_LENGTH:
                continue

            if _is_all_stopwords(keyword):
                continue

            # Avoid duplicates from same sentence
            if any(u.keyword == keyword and u.context == sentence for u in usages):
                continue

            usage = KeywordUsage(
                keyword=keyword,
                context=sentence,
                source_document=filepath,
                document_type=doc_type,
                date=doc_date
            )
            usages.append(usage)

    return usages


def _split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]


def _extract_ngrams(text: str, min_n: int = 2, max_n: int = 4) -> List[str]:
    """
    Extract n-grams (phrases of n words) from text.

    Args:
        text: Text to extract n-grams from
        min_n: Minimum number of words in phrase
        max_n: Maximum number of words in phrase

    Returns:
        List of n-gram phrases
    """
    # Tokenize into words (letters only, lowercase)
    words = re.findall(r'\b[a-z]+\b', text.lower())

    ngrams = []
    for n in range(min_n, max_n + 1):
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)

    return ngrams


def _is_all_stopwords(phrase: str) -> bool:
    """
    Check if a phrase contains only stopwords.

    Args:
        phrase: Phrase to check

    Returns:
        True if all words are stopwords
    """
    words = phrase.lower().split()
    return all(word in STOPWORDS for word in words)


def build_keyword_index(usages: List[KeywordUsage]) -> List[KeywordEntry]:
    """
    Build a keyword index from usages.

    Groups usages by keyword, identifies aliases using semantic similarity,
    and aggregates statistics.

    Args:
        usages: List of keyword usages to index

    Returns:
        List of KeywordEntry objects sorted by frequency (highest first)

    Examples:
        >>> usage1 = KeywordUsage("leadership", "ctx", "doc1", "resume", None)
        >>> usage2 = KeywordUsage("leadership", "ctx", "doc2", "cover_letter", None)
        >>> index = build_keyword_index([usage1, usage2])
        >>> len(index)
        1
        >>> index[0].frequency
        2
    """
    if not usages:
        return []

    # Group usages by normalized keyword
    keyword_groups: Dict[str, List[KeywordUsage]] = defaultdict(list)
    for usage in usages:
        normalized = usage.keyword.lower().strip()
        keyword_groups[normalized].append(usage)

    # Pre-compute embeddings for all keywords once (huge optimization!)
    all_keywords = list(keyword_groups.keys())
    keyword_embeddings = _compute_keyword_embeddings(all_keywords)

    # Compute full similarity matrix ONCE (massive speedup!)
    similarity_matrix = cosine_similarity(keyword_embeddings, keyword_embeddings)

    # Build KeywordEntry objects
    entries = []
    for idx, (keyword, usage_list) in enumerate(keyword_groups.items()):
        # Sort usages by date (most recent first)
        usage_list.sort(key=lambda u: u.date if u.date else date.min, reverse=True)

        # Calculate frequency
        frequency = len(usage_list)

        # Collect document types
        doc_types = set(u.document_type for u in usage_list)

        # Find aliases using pre-computed similarity matrix
        aliases = _find_aliases_from_matrix(
            keyword_idx=idx,
            all_keywords=all_keywords,
            similarity_matrix=similarity_matrix
        )

        entry = KeywordEntry(
            keyword=keyword,
            aliases=aliases,
            usages=usage_list,
            frequency=frequency,
            document_types=doc_types
        )
        entries.append(entry)

    # Sort by frequency (highest first)
    entries.sort(key=lambda e: e.frequency, reverse=True)

    return entries


def _compute_keyword_embeddings(keywords: List[str]) -> np.ndarray:
    """
    Compute embeddings for all keywords in a single batch.

    Args:
        keywords: List of keywords to encode

    Returns:
        numpy array of embeddings with shape (n_keywords, embedding_dim)
    """
    if not keywords:
        return np.array([])

    model = _get_model()
    embeddings = model.encode(keywords, show_progress_bar=True)
    return embeddings


def _find_aliases_from_matrix(keyword_idx: int, all_keywords: List[str],
                              similarity_matrix: np.ndarray, threshold: float = 0.8) -> List[str]:
    """
    Find semantically similar keywords as aliases using pre-computed similarity matrix.

    Args:
        keyword_idx: Index of the target keyword in all_keywords
        all_keywords: List of all keywords
        similarity_matrix: Pre-computed similarity matrix (n_keywords × n_keywords)
        threshold: Similarity threshold (0.8 = very similar)

    Returns:
        List of alias keywords
    """
    if len(all_keywords) == 0 or similarity_matrix.size == 0:
        return []

    # Extract similarities for this keyword (just a row lookup!)
    similarities = similarity_matrix[keyword_idx]

    # Find keywords above threshold (excluding self)
    aliases = []
    for idx, similarity in enumerate(similarities):
        if idx == keyword_idx:
            continue  # Skip self

        if similarity >= threshold:
            aliases.append((all_keywords[idx], similarity))

    # Sort by similarity (highest first) and return top 5
    aliases.sort(key=lambda x: x[1], reverse=True)
    return [keyword for keyword, _ in aliases[:5]]


def analyze_keywords(documents: List[Dict], min_frequency: int = 2) -> List[KeywordEntry]:
    """
    Analyze keywords across all documents.

    Main API function. Extracts keywords from all document types, builds an index,
    and filters by minimum frequency.

    Args:
        documents: List of processed document dictionaries, each containing:
            - filepath: Path to document
            - text: Document text
            - document_type: Type of document (from DocumentType enum)
            - date: Document date (optional)
        min_frequency: Minimum number of occurrences to include (default: 2)

    Returns:
        List of KeywordEntry objects sorted by frequency (highest first)

    Examples:
        >>> docs = [{'filepath': 'resume.txt', 'text': 'Software engineering skills',
        ...          'document_type': 'resume', 'date': None}]
        >>> keywords = analyze_keywords(docs, min_frequency=1)
        >>> len(keywords) >= 0
        True
    """
    if not documents:
        return []

    # Extract keywords from all documents (all types)
    all_usages = []
    for doc in documents:
        usages = extract_keywords_from_document(
            text=doc.get('text', ''),
            filepath=doc.get('filepath', ''),
            doc_type=doc.get('document_type', 'unknown'),
            doc_date=doc.get('date')
        )
        all_usages.extend(usages)

    if not all_usages:
        return []

    # Build keyword index
    index = build_keyword_index(all_usages)

    # Filter by minimum frequency
    filtered_index = [entry for entry in index if entry.frequency >= min_frequency]

    return filtered_index
