"""
Term Extraction Module
Extracts professional terms, skills, and phrases from career documents.

Part of Phase 3.1: Core Term Extraction
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter
from enum import Enum


class TermCategory(Enum):
    """Categories for extracted terms"""
    SKILL = "skill"
    TOOL = "tool"
    METHODOLOGY = "methodology"
    SOFT_SKILL = "soft_skill"
    DOMAIN_KNOWLEDGE = "domain_knowledge"
    CERTIFICATION = "certification"
    LANGUAGE = "language"
    UNKNOWN = "unknown"


@dataclass
class ExtractedTerm:
    """Represents an extracted term with its properties"""
    text: str
    category: TermCategory = TermCategory.UNKNOWN
    frequency: int = 1
    positions: List[int] = field(default_factory=list)  # Character positions in document
    confidence: float = 0.0  # 0-1 confidence score
    context_window: str = ""  # Surrounding text for analysis
    
    def __post_init__(self):
        """Normalize term text"""
        self.text = self.text.strip()
    
    def add_occurrence(self, position: int, context: str = ""):
        """Record another occurrence of this term"""
        self.frequency += 1
        self.positions.append(position)
        if context and not self.context_window:
            self.context_window = context


class TermExtractor:
    """
    Extracts professional terms, skills, and key phrases from career documents.
    
    Uses pattern matching and heuristics to identify:
    - Technical skills and tools
    - Programming languages
    - Methodologies and frameworks
    - Soft skills
    - Domain-specific terminology
    - Certifications
    """
    
    # Common technical skills and tools
    TECH_SKILLS = {
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
        'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
        'flask', 'spring', 'rails', 'asp.net', 'laravel',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle',
        'sqlite', 'cassandra', 'dynamodb',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ansible', 'git', 'ci/cd', 'devops',
        
        # Data & Analytics
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'tableau',
        'power bi', 'spark', 'hadoop', 'kafka',
        
        # Marketing & SEO
        'seo', 'sem', 'google analytics', 'google ads', 'facebook ads',
        'content marketing', 'email marketing', 'social media',
        
        # Tools
        'jira', 'confluence', 'slack', 'github', 'gitlab', 'bitbucket',
    }
    
    # Methodology patterns
    METHODOLOGY_PATTERNS = [
        r'\b(agile|scrum|kanban|waterfall|lean|six sigma|devops)\b',
        r'\b(tdd|bdd|test[\s-]driven|behavior[\s-]driven)\b',
        r'\b(microservices|monolithic|serverless)\b',
        r'\b(object[\s-]oriented|functional programming|oop)\b',
    ]
    
    # Certification patterns
    CERTIFICATION_PATTERNS = [
        r'\b(aws|azure|google cloud|gcp)\s+certified\b',
        r'\b(pmp|prince2|csm|psm|safe)\b',
        r'\b(cpa|cfa|cma|cia)\b',
        r'\b(cissp|cism|security\+|network\+)\b',
        r'\b(ccna|ccnp|ccie)\b',
    ]
    
    # Soft skills (common phrases)
    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'project management', 'stakeholder management',
        'collaboration', 'analytical', 'creative', 'innovative', 'strategic thinking',
        'attention to detail', 'organizational', 'adaptability', 'flexibility',
        'mentoring', 'coaching', 'presentation', 'negotiation', 'conflict resolution',
    }
    
    # Domain-specific term indicators
    DOMAIN_INDICATORS = {
        'finance': ['financial', 'accounting', 'audit', 'tax', 'revenue', 'budget', 'forecasting'],
        'healthcare': ['clinical', 'patient', 'medical', 'diagnosis', 'treatment', 'hipaa'],
        'marketing': ['campaign', 'seo', 'sem', 'brand', 'content marketing', 'social media'],
        'sales': ['revenue', 'quota', 'pipeline', 'crm', 'leads', 'conversion'],
        'education': ['curriculum', 'pedagogical', 'assessment', 'learning outcomes', 'teaching'],
        'legal': ['litigation', 'compliance', 'regulatory', 'contract', 'intellectual property'],
    }
    
    def __init__(self):
        """Initialize the term extractor"""
        self.extracted_terms: Dict[str, ExtractedTerm] = {}
        
    def extract_terms(self, text: str, document_type: str = "") -> Dict[str, ExtractedTerm]:
        """
        Extract professional terms from text.
        
        Args:
            text: Document text to analyze
            document_type: Type of document (resume, cover_letter, job_description)
            
        Returns:
            Dictionary mapping term text to ExtractedTerm objects
        """
        if not text:
            return {}
        
        self.extracted_terms = {}
        text_lower = text.lower()
        
        # Extract different types of terms
        self._extract_technical_skills(text_lower, text)
        self._extract_methodologies(text_lower, text)
        self._extract_certifications(text_lower, text)
        self._extract_soft_skills(text_lower, text)
        self._extract_noun_phrases(text, text_lower)
        
        # Calculate confidence scores
        self._calculate_confidence_scores()
        
        return self.extracted_terms
    
    def _extract_technical_skills(self, text_lower: str, original_text: str):
        """Extract technical skills and tools"""
        for skill in self.TECH_SKILLS:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                position = match.start()
                context = self._get_context_window(original_text, position)
                
                term_key = skill.lower()
                if term_key in self.extracted_terms:
                    self.extracted_terms[term_key].add_occurrence(position, context)
                else:
                    self.extracted_terms[term_key] = ExtractedTerm(
                        text=skill,
                        category=self._categorize_tech_skill(skill),
                        positions=[position],
                        context_window=context
                    )
    
    def _categorize_tech_skill(self, skill: str) -> TermCategory:
        """Categorize a technical skill"""
        skill_lower = skill.lower()
        
        # Programming languages
        languages = {'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 
                    'rust', 'php', 'swift', 'kotlin', 'scala', 'r'}
        if skill_lower in languages:
            return TermCategory.LANGUAGE
        
        # Cloud platforms
        if skill_lower in {'aws', 'azure', 'gcp'}:
            return TermCategory.TOOL
        
        # Default to tool/skill
        return TermCategory.SKILL
    
    def _extract_methodologies(self, text_lower: str, original_text: str):
        """Extract methodologies and frameworks"""
        for pattern in self.METHODOLOGY_PATTERNS:
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                methodology = match.group(0)
                position = match.start()
                context = self._get_context_window(original_text, position)
                
                term_key = methodology.lower()
                if term_key in self.extracted_terms:
                    self.extracted_terms[term_key].add_occurrence(position, context)
                else:
                    self.extracted_terms[term_key] = ExtractedTerm(
                        text=methodology,
                        category=TermCategory.METHODOLOGY,
                        positions=[position],
                        context_window=context
                    )
    
    def _extract_certifications(self, text_lower: str, original_text: str):
        """Extract certifications and credentials"""
        for pattern in self.CERTIFICATION_PATTERNS:
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                cert = match.group(0)
                position = match.start()
                context = self._get_context_window(original_text, position)
                
                term_key = cert.lower()
                if term_key in self.extracted_terms:
                    self.extracted_terms[term_key].add_occurrence(position, context)
                else:
                    self.extracted_terms[term_key] = ExtractedTerm(
                        text=cert,
                        category=TermCategory.CERTIFICATION,
                        positions=[position],
                        context_window=context
                    )
    
    def _extract_soft_skills(self, text_lower: str, original_text: str):
        """Extract soft skills"""
        for skill in self.SOFT_SKILLS:
            # Use word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                position = match.start()
                context = self._get_context_window(original_text, position)
                
                term_key = skill.lower()
                if term_key in self.extracted_terms:
                    self.extracted_terms[term_key].add_occurrence(position, context)
                else:
                    self.extracted_terms[term_key] = ExtractedTerm(
                        text=skill,
                        category=TermCategory.SOFT_SKILL,
                        positions=[position],
                        context_window=context
                    )
    
    def _extract_noun_phrases(self, original_text: str, text_lower: str):
        """
        Extract potential multi-word noun phrases.
        Uses simple heuristics (capitalized phrases, common patterns).
        """
        # Pattern for capitalized multi-word terms (likely proper nouns/technologies)
        # e.g., "Machine Learning", "Natural Language Processing"
        capitalized_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
        
        for match in re.finditer(capitalized_pattern, original_text):
            phrase = match.group(0)
            position = match.start()
            phrase_lower = phrase.lower()
            
            # Skip if it's a common sentence start pattern
            if self._is_common_sentence_start(phrase):
                continue
            
            context = self._get_context_window(original_text, position)
            
            if phrase_lower in self.extracted_terms:
                # Already extracted - just add occurrence
                self.extracted_terms[phrase_lower].add_occurrence(position, context)
            else:
                # Try to categorize based on context or patterns
                category = self._categorize_noun_phrase(phrase, context)
                
                self.extracted_terms[phrase_lower] = ExtractedTerm(
                    text=phrase,
                    category=category,
                    positions=[position],
                    context_window=context
                )
    
    def _is_common_sentence_start(self, phrase: str) -> bool:
        """Check if phrase is a common sentence starter (not a technical term)"""
        common_starts = {
            'I have', 'I am', 'The company', 'The team', 'This position',
            'We are', 'My experience', 'In this', 'During my', 'At the'
        }
        return phrase in common_starts
    
    def _categorize_noun_phrase(self, phrase: str, context: str) -> TermCategory:
        """Attempt to categorize a noun phrase based on context"""
        phrase_lower = phrase.lower()
        context_lower = context.lower()
        
        # Check for domain indicators
        for domain, indicators in self.DOMAIN_INDICATORS.items():
            if any(ind in phrase_lower or ind in context_lower for ind in indicators):
                return TermCategory.DOMAIN_KNOWLEDGE
        
        # Check for tool/technology indicators
        tech_indicators = ['software', 'platform', 'system', 'tool', 'framework']
        if any(ind in context_lower for ind in tech_indicators):
            return TermCategory.TOOL
        
        return TermCategory.UNKNOWN
    
    def _get_context_window(self, text: str, position: int, window_size: int = 100) -> str:
        """Extract context window around a term"""
        start = max(0, position - window_size)
        end = min(len(text), position + window_size)
        return text[start:end].strip()
    
    def _calculate_confidence_scores(self):
        """Calculate confidence scores for extracted terms"""
        if not self.extracted_terms:
            return
        
        # Get frequency stats
        frequencies = [term.frequency for term in self.extracted_terms.values()]
        max_freq = max(frequencies) if frequencies else 1
        
        for term in self.extracted_terms.values():
            # Base confidence on:
            # 1. Category certainty (known categories score higher)
            # 2. Frequency (more occurrences = higher confidence)
            # 3. Context clarity
            
            category_confidence = {
                TermCategory.SKILL: 0.9,
                TermCategory.TOOL: 0.9,
                TermCategory.LANGUAGE: 0.95,
                TermCategory.CERTIFICATION: 0.95,
                TermCategory.METHODOLOGY: 0.85,
                TermCategory.SOFT_SKILL: 0.7,
                TermCategory.DOMAIN_KNOWLEDGE: 0.6,
                TermCategory.UNKNOWN: 0.3,
            }
            
            base_confidence = category_confidence.get(term.category, 0.5)
            frequency_boost = min(0.3, (term.frequency / max_freq) * 0.3)
            
            term.confidence = min(1.0, base_confidence + frequency_boost)
    
    def get_top_terms(self, n: int = 20, min_confidence: float = 0.5) -> List[ExtractedTerm]:
        """
        Get top N terms by confidence score.
        
        Args:
            n: Number of terms to return
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of top ExtractedTerm objects
        """
        filtered = [
            term for term in self.extracted_terms.values()
            if term.confidence >= min_confidence
        ]
        return sorted(filtered, key=lambda t: (t.confidence, t.frequency), reverse=True)[:n]
    
    def get_terms_by_category(self, category: TermCategory) -> List[ExtractedTerm]:
        """Get all terms of a specific category"""
        return [
            term for term in self.extracted_terms.values()
            if term.category == category
        ]
    
    def get_term_statistics(self) -> Dict:
        """Get statistics about extracted terms"""
        if not self.extracted_terms:
            return {
                'total_terms': 0,
                'unique_terms': 0,
                'by_category': {},
                'avg_confidence': 0.0
            }
        
        category_counts = Counter(term.category for term in self.extracted_terms.values())
        avg_confidence = sum(t.confidence for t in self.extracted_terms.values()) / len(self.extracted_terms)
        
        return {
            'total_terms': sum(term.frequency for term in self.extracted_terms.values()),
            'unique_terms': len(self.extracted_terms),
            'by_category': {cat.value: count for cat, count in category_counts.items()},
            'avg_confidence': round(avg_confidence, 3)
        }


def extract_terms_from_text(text: str, document_type: str = "") -> Dict[str, ExtractedTerm]:
    """
    Convenience function to extract terms from text.
    
    Args:
        text: Document text
        document_type: Type of document (optional)
        
    Returns:
        Dictionary of extracted terms
    """
    extractor = TermExtractor()
    return extractor.extract_terms(text, document_type)
