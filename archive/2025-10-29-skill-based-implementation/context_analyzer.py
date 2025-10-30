"""
Context Analysis Module
Analyzes the context around extracted terms to understand usage patterns.

Part of Phase 3.2: Context Analysis
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter
from enum import Enum

from src.term_extractor import ExtractedTerm, TermCategory


class ActionVerbStrength(Enum):
    """Strength level of action verbs"""
    STRONG = "strong"  # Led, Developed, Architected, Launched
    MODERATE = "moderate"  # Managed, Implemented, Created
    WEAK = "weak"  # Assisted, Supported, Helped
    PASSIVE = "passive"  # Was responsible for, Involved in


@dataclass
class TermContext:
    """Detailed context analysis for a term"""
    term: ExtractedTerm
    action_verbs: List[Tuple[str, ActionVerbStrength]] = field(default_factory=list)
    quantifiers: List[str] = field(default_factory=list)  # Numbers, percentages
    descriptors: List[str] = field(default_factory=list)  # Adjectives, adverbs
    prominence_score: float = 0.0  # 0-1 score based on position and context
    usage_contexts: List[str] = field(default_factory=list)  # Different usage contexts
    
    def get_strongest_verb(self) -> Optional[Tuple[str, ActionVerbStrength]]:
        """Get the strongest action verb associated with this term"""
        if not self.action_verbs:
            return None
        
        # Sort by strength: STRONG > MODERATE > WEAK > PASSIVE
        strength_order = {
            ActionVerbStrength.STRONG: 3,
            ActionVerbStrength.MODERATE: 2,
            ActionVerbStrength.WEAK: 1,
            ActionVerbStrength.PASSIVE: 0,
        }
        return max(self.action_verbs, key=lambda x: strength_order[x[1]])
    
    def has_quantifiable_impact(self) -> bool:
        """Check if term usage includes quantifiable impact"""
        return len(self.quantifiers) > 0


class ContextAnalyzer:
    """
    Analyzes the context around extracted terms to understand their usage.
    
    Features:
    - Identifies action verbs paired with terms
    - Extracts quantifiers (numbers, percentages, metrics)
    - Calculates prominence based on position and frequency
    - Identifies different usage contexts
    """
    
    # Action verb categories (past tense and present tense)
    STRONG_VERBS = {
        'led', 'lead', 'developed', 'develop', 'architected', 'architect',
        'launched', 'launch', 'designed', 'design', 'built', 'build',
        'created', 'create', 'established', 'establish', 'founded', 'found',
        'pioneered', 'pioneer', 'drove', 'drive', 'spearheaded', 'spearhead',
        'delivered', 'deliver', 'achieved', 'achieve', 'transformed', 'transform',
    }
    
    MODERATE_VERBS = {
        'managed', 'manage', 'implemented', 'implement', 'coordinated', 'coordinate',
        'organized', 'organize', 'planned', 'plan', 'executed', 'execute',
        'improved', 'improve', 'optimized', 'optimize', 'enhanced', 'enhance',
        'streamlined', 'streamline', 'maintained', 'maintain', 'performed', 'perform',
        'conducted', 'conduct', 'facilitated', 'facilitate', 'oversaw', 'oversee',
    }
    
    WEAK_VERBS = {
        'assisted', 'assist', 'supported', 'support', 'helped', 'help',
        'participated', 'participate', 'contributed', 'contribute',
        'collaborated', 'collaborate', 'worked', 'work',
    }
    
    PASSIVE_PATTERNS = [
        r'was responsible for',
        r'were responsible for',
        r'involved in',
        r'engaged in',
        r'tasked with',
    ]
    
    # Quantifier patterns
    QUANTIFIER_PATTERNS = [
        r'\b\d+[%]',  # Percentages: 50%, 100%
        r'\b\d+[kKmMbB]?\+?\b',  # Numbers: 5, 10k, 2M, 50+
        r'\$\d+[kKmMbB]?',  # Monetary: $50k, $2M
        r'\d+x',  # Multipliers: 2x, 10x
    ]
    
    def __init__(self):
        """Initialize the context analyzer"""
        self.analyzed_contexts: Dict[str, TermContext] = {}
    
    def analyze_term_contexts(
        self, 
        terms: Dict[str, ExtractedTerm], 
        full_text: str
    ) -> Dict[str, TermContext]:
        """
        Analyze contexts for all extracted terms.
        
        Args:
            terms: Dictionary of extracted terms
            full_text: Full document text
            
        Returns:
            Dictionary mapping term text to TermContext objects
        """
        self.analyzed_contexts = {}
        
        for term_key, term in terms.items():
            context = self._analyze_single_term(term, full_text)
            self.analyzed_contexts[term_key] = context
        
        return self.analyzed_contexts
    
    def _analyze_single_term(self, term: ExtractedTerm, full_text: str) -> TermContext:
        """Analyze context for a single term"""
        context = TermContext(term=term)
        
        # Analyze each occurrence
        for position in term.positions:
            window = self._get_analysis_window(full_text, position, size=150)
            
            # Extract action verbs
            verbs = self._extract_action_verbs(window)
            context.action_verbs.extend(verbs)
            
            # Extract quantifiers
            quants = self._extract_quantifiers(window)
            context.quantifiers.extend(quants)
            
            # Extract descriptive words
            descriptors = self._extract_descriptors(window, term.text)
            context.descriptors.extend(descriptors)
            
            # Store usage context
            context.usage_contexts.append(window.strip())
        
        # Remove duplicates
        context.action_verbs = list(set(context.action_verbs))
        context.quantifiers = list(set(context.quantifiers))
        context.descriptors = list(set(context.descriptors))
        
        # Calculate prominence score
        context.prominence_score = self._calculate_prominence(term, full_text)
        
        return context
    
    def _get_analysis_window(self, text: str, position: int, size: int = 150) -> str:
        """Get text window for context analysis"""
        start = max(0, position - size)
        end = min(len(text), position + size)
        return text[start:end]
    
    def _extract_action_verbs(self, window: str) -> List[Tuple[str, ActionVerbStrength]]:
        """Extract action verbs from context window"""
        verbs = []
        window_lower = window.lower()
        
        # Check for passive patterns first
        for pattern in self.PASSIVE_PATTERNS:
            if re.search(pattern, window_lower):
                match = re.search(pattern, window_lower)
                verbs.append((match.group(0), ActionVerbStrength.PASSIVE))
        
        # Check for strong verbs
        for verb in self.STRONG_VERBS:
            if re.search(r'\b' + verb + r'\b', window_lower):
                verbs.append((verb, ActionVerbStrength.STRONG))
        
        # Check for moderate verbs
        for verb in self.MODERATE_VERBS:
            if re.search(r'\b' + verb + r'\b', window_lower):
                verbs.append((verb, ActionVerbStrength.MODERATE))
        
        # Check for weak verbs
        for verb in self.WEAK_VERBS:
            if re.search(r'\b' + verb + r'\b', window_lower):
                verbs.append((verb, ActionVerbStrength.WEAK))
        
        return verbs
    
    def _extract_quantifiers(self, window: str) -> List[str]:
        """Extract quantifiable metrics from context"""
        quantifiers = []
        
        for pattern in self.QUANTIFIER_PATTERNS:
            matches = re.findall(pattern, window)
            quantifiers.extend(matches)
        
        return quantifiers
    
    def _extract_descriptors(self, window: str, term: str) -> List[str]:
        """Extract descriptive words near the term"""
        descriptors = []
        
        # Simple adjective patterns (words ending in common adjective suffixes)
        adjective_suffixes = ['ent', 'ive', 'ous', 'ful', 'less', 'al', 'ic']
        
        words = re.findall(r'\b\w+\b', window.lower())
        
        # Get words near the term
        term_lower = term.lower()
        if term_lower in ' '.join(words):
            term_words = term_lower.split()
            # Find position of term
            for i, word in enumerate(words):
                if word in term_words:
                    # Get surrounding words
                    context_words = words[max(0, i-3):min(len(words), i+len(term_words)+3)]
                    
                    # Filter for adjectives
                    for w in context_words:
                        if any(w.endswith(suffix) for suffix in adjective_suffixes):
                            descriptors.append(w)
                        # Also capture common descriptive words
                        elif w in {'advanced', 'expert', 'senior', 'junior', 'key', 
                                  'primary', 'main', 'critical', 'essential', 'core'}:
                            descriptors.append(w)
        
        return descriptors
    
    def _calculate_prominence(self, term: ExtractedTerm, full_text: str) -> float:
        """
        Calculate prominence score based on position and frequency.
        
        Factors:
        - Position in document (earlier = more prominent)
        - Frequency (more occurrences = more prominent)
        - Section context (headlines, bullet points)
        - Confidence score of term itself
        """
        if not term.positions:
            return 0.0
        
        score = 0.0
        text_length = len(full_text)
        
        # Position score: earlier positions get higher score
        avg_position = sum(term.positions) / len(term.positions)
        position_score = 1.0 - (avg_position / text_length)
        score += position_score * 0.3
        
        # Frequency score: normalized by document length
        # More frequent terms are more prominent
        frequency_score = min(1.0, term.frequency / 10)  # Cap at 10 occurrences
        score += frequency_score * 0.3
        
        # Term confidence score
        score += term.confidence * 0.2
        
        # Context bonus: check if term appears in structured context
        structure_bonus = 0.0
        for pos in term.positions[:3]:  # Check first 3 occurrences
            window = self._get_analysis_window(full_text, pos, size=100)
            
            # Bullet point context
            if '•' in window or '*' in window or re.search(r'^\s*-\s', window):
                structure_bonus += 0.05
            
            # Header context (all caps nearby)
            if re.search(r'[A-Z]{3,}', window):
                structure_bonus += 0.05
        
        score += min(0.2, structure_bonus)
        
        return min(1.0, score)
    
    def get_terms_with_strong_verbs(self) -> List[TermContext]:
        """Get terms paired with strong action verbs"""
        return [
            ctx for ctx in self.analyzed_contexts.values()
            if any(strength == ActionVerbStrength.STRONG for _, strength in ctx.action_verbs)
        ]
    
    def get_terms_with_quantifiable_impact(self) -> List[TermContext]:
        """Get terms with quantifiable impact metrics"""
        return [
            ctx for ctx in self.analyzed_contexts.values()
            if ctx.has_quantifiable_impact()
        ]
    
    def get_top_prominent_terms(self, n: int = 10) -> List[TermContext]:
        """Get most prominent terms by prominence score"""
        return sorted(
            self.analyzed_contexts.values(),
            key=lambda ctx: ctx.prominence_score,
            reverse=True
        )[:n]
    
    def generate_context_report(self) -> Dict:
        """Generate a summary report of context analysis"""
        if not self.analyzed_contexts:
            return {
                'total_terms': 0,
                'with_strong_verbs': 0,
                'with_quantifiers': 0,
                'avg_prominence': 0.0,
                'verb_distribution': {}
            }
        
        # Count verb strengths
        verb_counts = Counter()
        for ctx in self.analyzed_contexts.values():
            for _, strength in ctx.action_verbs:
                verb_counts[strength.value] += 1
        
        strong_verb_terms = len(self.get_terms_with_strong_verbs())
        quantified_terms = len(self.get_terms_with_quantifiable_impact())
        avg_prominence = sum(ctx.prominence_score for ctx in self.analyzed_contexts.values()) / len(self.analyzed_contexts)
        
        return {
            'total_terms': len(self.analyzed_contexts),
            'with_strong_verbs': strong_verb_terms,
            'with_quantifiers': quantified_terms,
            'avg_prominence': round(avg_prominence, 3),
            'verb_distribution': dict(verb_counts)
        }


def analyze_term_contexts(
    terms: Dict[str, ExtractedTerm],
    full_text: str
) -> Dict[str, TermContext]:
    """
    Convenience function to analyze term contexts.
    
    Args:
        terms: Dictionary of extracted terms
        full_text: Full document text
        
    Returns:
        Dictionary of term contexts
    """
    analyzer = ContextAnalyzer()
    return analyzer.analyze_term_contexts(terms, full_text)
