"""
Lexicon Builder Module
Aggregates terms across multiple documents to build unified skill profiles.

Part of Phase 4: Lexicon Building
"""

import json
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from collections import Counter, defaultdict
from enum import Enum

from src.term_extractor import ExtractedTerm, TermCategory
from src.context_analyzer import TermContext, ActionVerbStrength
from src.term_categorizer import CategorizedTerm, SkillDomain, RoleCategory


@dataclass
class DocumentMetadata:
    """Metadata about a processed document"""
    filename: str
    document_type: str  # 'resume' or 'cover_letter'
    date: Optional[date] = None
    target_position: Optional[str] = None
    target_organization: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        if self.date:
            data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DocumentMetadata':
        """Create from dictionary"""
        if 'date' in data and data['date']:
            data['date'] = date.fromisoformat(data['date'])
        return cls(**data)


@dataclass
class SkillOccurrence:
    """Single occurrence of a skill in a document"""
    document: DocumentMetadata
    frequency: int  # How many times in this document
    prominence_score: float  # 0-1 prominence in this document
    action_verbs: List[Tuple[str, str]]  # (verb, strength)
    quantifiers: List[str]
    skill_level: Optional[str] = None  # junior/mid/senior/expert
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'document': self.document.to_dict(),
            'frequency': self.frequency,
            'prominence_score': self.prominence_score,
            'action_verbs': self.action_verbs,
            'quantifiers': self.quantifiers,
            'skill_level': self.skill_level
        }


@dataclass
class AggregatedSkill:
    """
    Aggregated information about a skill across all documents.
    
    Tracks:
    - Total usage across documents
    - Recency (most recent usage)
    - Prominence trends
    - Context evolution
    """
    skill_name: str
    category: TermCategory
    skill_domain: SkillDomain
    role_categories: Set[RoleCategory]
    
    # Aggregated statistics
    total_documents: int = 0
    total_occurrences: int = 0
    first_used: Optional[date] = None
    last_used: Optional[date] = None
    
    # Per-document occurrences
    occurrences: List[SkillOccurrence] = field(default_factory=list)
    
    # Aggregated context
    all_action_verbs: Counter = field(default_factory=Counter)
    all_quantifiers: Set[str] = field(default_factory=set)
    avg_prominence: float = 0.0
    
    # Metadata
    is_transferable: bool = False
    industry_specific: bool = False
    
    def add_occurrence(self, occurrence: SkillOccurrence):
        """Add a new occurrence from a document"""
        self.occurrences.append(occurrence)
        self.total_documents += 1
        self.total_occurrences += occurrence.frequency
        
        # Update date range
        if occurrence.document.date:
            if not self.first_used or occurrence.document.date < self.first_used:
                self.first_used = occurrence.document.date
            if not self.last_used or occurrence.document.date > self.last_used:
                self.last_used = occurrence.document.date
        
        # Aggregate context
        for verb, strength in occurrence.action_verbs:
            self.all_action_verbs[verb] += 1
        self.all_quantifiers.update(occurrence.quantifiers)
        
        # Recalculate average prominence
        self.avg_prominence = sum(o.prominence_score for o in self.occurrences) / len(self.occurrences)
    
    def get_recency_score(self, reference_date: Optional[date] = None) -> float:
        """
        Calculate recency score (0-1).
        More recent usage = higher score.
        """
        if not self.last_used:
            return 0.0
        
        if not reference_date:
            reference_date = date.today()
        
        days_since = (reference_date - self.last_used).days
        
        # Decay function: score decreases as time increases
        # 0 days = 1.0, 365 days = 0.5, 730 days = 0.25, etc.
        score = 1.0 / (1.0 + (days_since / 365.0))
        return min(1.0, score)
    
    def get_frequency_score(self) -> float:
        """
        Calculate frequency score (0-1) based on how often skill appears.
        """
        # Normalize by documents: appearing in more documents = higher score
        # 1 doc = 0.1, 5 docs = 0.5, 10+ docs = 1.0
        score = min(1.0, self.total_documents / 10.0)
        return score
    
    def get_combined_score(self, reference_date: Optional[date] = None) -> float:
        """
        Calculate combined score considering recency, frequency, and prominence.
        
        Weights:
        - Recency: 35%
        - Frequency: 30%
        - Prominence: 35%
        """
        recency = self.get_recency_score(reference_date)
        frequency = self.get_frequency_score()
        prominence = self.avg_prominence
        
        return (recency * 0.35) + (frequency * 0.30) + (prominence * 0.35)
    
    def get_strongest_verb(self) -> Optional[str]:
        """Get most frequently used action verb"""
        if not self.all_action_verbs:
            return None
        return self.all_action_verbs.most_common(1)[0][0]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'skill_name': self.skill_name,
            'category': self.category.value,
            'skill_domain': self.skill_domain.value,
            'role_categories': [r.value for r in self.role_categories],
            'total_documents': self.total_documents,
            'total_occurrences': self.total_occurrences,
            'first_used': self.first_used.isoformat() if self.first_used else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'occurrences': [o.to_dict() for o in self.occurrences],
            'all_action_verbs': dict(self.all_action_verbs),
            'all_quantifiers': list(self.all_quantifiers),
            'avg_prominence': round(self.avg_prominence, 3),
            'is_transferable': self.is_transferable,
            'industry_specific': self.industry_specific,
            'recency_score': round(self.get_recency_score(), 3),
            'frequency_score': round(self.get_frequency_score(), 3),
            'combined_score': round(self.get_combined_score(), 3),
            'strongest_verb': self.get_strongest_verb()
        }


class SkillLexicon:
    """
    Unified lexicon of skills aggregated across all documents.
    
    Main data structure for Phase 4.
    """
    
    def __init__(self):
        """Initialize empty lexicon"""
        self.skills: Dict[str, AggregatedSkill] = {}
        self.documents: List[DocumentMetadata] = []
        self.build_date: datetime = datetime.now()
    
    def add_document_analysis(
        self,
        metadata: DocumentMetadata,
        categorized_terms: Dict[str, CategorizedTerm],
        contexts: Dict[str, TermContext]
    ):
        """
        Add analysis results from a single document to the lexicon.
        
        Args:
            metadata: Document metadata
            categorized_terms: Categorized terms from Phase 3.3
            contexts: Term contexts from Phase 3.2
        """
        self.documents.append(metadata)
        
        for term_key, cat_term in categorized_terms.items():
            context = contexts.get(term_key)
            if not context:
                continue
            
            # Create occurrence
            occurrence = SkillOccurrence(
                document=metadata,
                frequency=cat_term.term.frequency,
                prominence_score=context.prominence_score,
                action_verbs=[(v, s.value) for v, s in context.action_verbs],
                quantifiers=context.quantifiers,
                skill_level=cat_term.skill_level
            )
            
            # Add to lexicon
            skill_name = cat_term.term.text.lower()
            
            if skill_name not in self.skills:
                # Create new aggregated skill
                self.skills[skill_name] = AggregatedSkill(
                    skill_name=skill_name,
                    category=cat_term.term.category,
                    skill_domain=cat_term.skill_domain,
                    role_categories=cat_term.role_categories,
                    is_transferable=cat_term.is_transferable(),
                    industry_specific=cat_term.industry_specific
                )
            
            self.skills[skill_name].add_occurrence(occurrence)
    
    def get_top_skills(
        self,
        n: int = 20,
        by: str = 'combined',
        reference_date: Optional[date] = None
    ) -> List[AggregatedSkill]:
        """
        Get top N skills by various criteria.
        
        Args:
            n: Number of skills to return
            by: Sort criteria ('combined', 'recency', 'frequency', 'prominence')
            reference_date: Reference date for recency calculations
            
        Returns:
            List of top skills
        """
        if by == 'combined':
            key_func = lambda s: s.get_combined_score(reference_date)
        elif by == 'recency':
            key_func = lambda s: s.get_recency_score(reference_date)
        elif by == 'frequency':
            key_func = lambda s: s.get_frequency_score()
        elif by == 'prominence':
            key_func = lambda s: s.avg_prominence
        else:
            raise ValueError(f"Invalid sort criteria: {by}")
        
        return sorted(
            self.skills.values(),
            key=key_func,
            reverse=True
        )[:n]
    
    def get_skills_by_domain(self, domain: SkillDomain) -> List[AggregatedSkill]:
        """Get all skills in a specific domain"""
        return [
            skill for skill in self.skills.values()
            if skill.skill_domain == domain
        ]
    
    def get_skills_by_role(self, role: RoleCategory) -> List[AggregatedSkill]:
        """Get all skills relevant to a specific role"""
        return [
            skill for skill in self.skills.values()
            if role in skill.role_categories
        ]
    
    def get_transferable_skills(self) -> List[AggregatedSkill]:
        """Get all transferable skills"""
        return [
            skill for skill in self.skills.values()
            if skill.is_transferable
        ]
    
    def get_recent_skills(
        self,
        days: int = 365,
        reference_date: Optional[date] = None
    ) -> List[AggregatedSkill]:
        """Get skills used within the last N days"""
        if not reference_date:
            reference_date = date.today()
        
        cutoff_date = date(
            reference_date.year - (days // 365),
            reference_date.month,
            reference_date.day
        )
        
        return [
            skill for skill in self.skills.values()
            if skill.last_used and skill.last_used >= cutoff_date
        ]
    
    def generate_skill_profile(self) -> Dict:
        """
        Generate comprehensive skill profile summary.
        
        Returns:
            Dictionary with skill statistics and breakdowns
        """
        total_skills = len(self.skills)
        total_docs = len(self.documents)
        
        # Skills by domain
        by_domain = defaultdict(int)
        for skill in self.skills.values():
            by_domain[skill.skill_domain.value] += 1
        
        # Skills by role
        by_role = defaultdict(int)
        for skill in self.skills.values():
            for role in skill.role_categories:
                by_role[role.value] += 1
        
        # Transferable vs. specialized
        transferable = sum(1 for s in self.skills.values() if s.is_transferable)
        specialized = total_skills - transferable
        
        # Recent vs. older
        recent = len(self.get_recent_skills(days=365))
        older = total_skills - recent
        
        # Top skills
        top_combined = [s.skill_name for s in self.get_top_skills(10, by='combined')]
        top_recent = [s.skill_name for s in self.get_top_skills(10, by='recency')]
        
        return {
            'build_date': self.build_date.isoformat(),
            'total_documents_analyzed': total_docs,
            'total_unique_skills': total_skills,
            'skills_by_domain': dict(by_domain),
            'skills_by_role': dict(by_role),
            'transferable_skills_count': transferable,
            'specialized_skills_count': specialized,
            'recent_skills_count': recent,
            'older_skills_count': older,
            'top_skills_combined': top_combined,
            'top_skills_recent': top_recent
        }
    
    def export_to_json(self, filepath: str):
        """Export lexicon to JSON file"""
        data = {
            'build_date': self.build_date.isoformat(),
            'documents': [d.to_dict() for d in self.documents],
            'skills': {name: skill.to_dict() for name, skill in self.skills.items()},
            'profile': self.generate_skill_profile()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_json(cls, filepath: str) -> 'SkillLexicon':
        """Load lexicon from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        lexicon = cls()
        lexicon.build_date = datetime.fromisoformat(data['build_date'])
        
        # Load documents
        lexicon.documents = [
            DocumentMetadata.from_dict(d) for d in data['documents']
        ]
        
        # Note: Loading full skills would require recreating objects
        # For now, this is primarily for exporting
        
        return lexicon


def build_lexicon_from_documents(
    documents_analysis: List[Tuple[DocumentMetadata, Dict, Dict]]
) -> SkillLexicon:
    """
    Convenience function to build lexicon from multiple document analyses.
    
    Args:
        documents_analysis: List of (metadata, categorized_terms, contexts) tuples
        
    Returns:
        Built SkillLexicon
    """
    lexicon = SkillLexicon()
    
    for metadata, categorized, contexts in documents_analysis:
        lexicon.add_document_analysis(metadata, categorized, contexts)
    
    return lexicon
