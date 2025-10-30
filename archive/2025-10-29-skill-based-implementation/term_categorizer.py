"""
Term Categorization Module
Categorizes and groups extracted terms by domain, role, and skill type.

Part of Phase 3.3: Term Categorization
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from enum import Enum

from src.term_extractor import ExtractedTerm, TermCategory
from src.context_analyzer import TermContext


class SkillDomain(Enum):
    """High-level skill domains"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    INTERPERSONAL = "interpersonal"
    LEADERSHIP = "leadership"
    UNKNOWN = "unknown"


class RoleCategory(Enum):
    """Role-specific skill categories"""
    ENGINEERING = "engineering"
    DATA_SCIENCE = "data_science"
    PRODUCT = "product"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    FINANCE = "finance"
    OPERATIONS = "operations"
    HUMAN_RESOURCES = "human_resources"
    GENERAL = "general"


@dataclass
class CategorizedTerm:
    """Term with full categorization information"""
    term: ExtractedTerm
    context: Optional[TermContext] = None
    skill_domain: SkillDomain = SkillDomain.UNKNOWN
    role_categories: Set[RoleCategory] = field(default_factory=set)
    skill_level: Optional[str] = None  # junior, mid, senior, expert
    industry_specific: bool = False
    
    def is_transferable(self) -> bool:
        """Check if skill is broadly transferable across roles"""
        transferable_categories = {
            TermCategory.SOFT_SKILL,
            TermCategory.METHODOLOGY,
        }
        return (
            self.term.category in transferable_categories or
            self.skill_domain == SkillDomain.INTERPERSONAL
        )
    
    def get_primary_role(self) -> Optional[RoleCategory]:
        """Get the most likely primary role category"""
        if not self.role_categories:
            return None
        # Return first role (could be improved with more sophisticated logic)
        return next(iter(self.role_categories))


class TermCategorizer:
    """
    Categorizes extracted terms into skill domains and role-specific groups.
    
    Features:
    - Domain classification (technical, business, creative, etc.)
    - Role-specific grouping (engineering, product, marketing, etc.)
    - Skill level inference
    - Transferability assessment
    """
    
    # Domain mappings
    TECHNICAL_INDICATORS = {
        'programming', 'development', 'software', 'code', 'api', 'database',
        'cloud', 'infrastructure', 'architecture', 'testing', 'deployment',
        'devops', 'security', 'network', 'system', 'algorithm',
    }
    
    BUSINESS_INDICATORS = {
        'business', 'strategy', 'planning', 'analysis', 'financial', 'budget',
        'revenue', 'profit', 'cost', 'roi', 'market', 'competitive',
        'stakeholder', 'vendor', 'contract', 'compliance', 'regulatory',
    }
    
    CREATIVE_INDICATORS = {
        'design', 'creative', 'visual', 'brand', 'content', 'writing',
        'storytelling', 'aesthetic', 'ui', 'ux', 'graphic', 'video',
        'multimedia', 'artistic',
    }
    
    ANALYTICAL_INDICATORS = {
        'data', 'analysis', 'analytics', 'statistical', 'research', 'insights',
        'metrics', 'measurement', 'modeling', 'forecasting', 'reporting',
        'visualization', 'dashboard',
    }
    
    INTERPERSONAL_INDICATORS = {
        'communication', 'collaboration', 'teamwork', 'leadership', 'mentoring',
        'coaching', 'facilitation', 'presentation', 'negotiation', 'conflict',
        'relationship', 'stakeholder', 'customer service',
    }
    
    # Role-specific skill mappings
    ENGINEERING_SKILLS = {
        # Languages
        'python', 'java', 'javascript', 'c++', 'go', 'rust', 'typescript',
        # Tools
        'git', 'docker', 'kubernetes', 'jenkins', 'terraform',
        # Practices
        'ci/cd', 'tdd', 'agile', 'scrum',
        # Platforms
        'aws', 'azure', 'gcp',
    }
    
    DATA_SCIENCE_SKILLS = {
        'python', 'r', 'sql', 'pandas', 'numpy', 'scikit-learn',
        'tensorflow', 'pytorch', 'machine learning', 'deep learning',
        'data mining', 'statistical modeling', 'data visualization',
        'tableau', 'power bi', 'spark', 'hadoop',
    }
    
    PRODUCT_SKILLS = {
        'product management', 'roadmap', 'prioritization', 'user stories',
        'backlog', 'mvp', 'product strategy', 'go-to-market',
        'user research', 'a/b testing', 'analytics', 'jira',
        'agile', 'scrum', 'stakeholder management',
    }
    
    DESIGN_SKILLS = {
        'ui design', 'ux design', 'user experience', 'wireframing',
        'prototyping', 'figma', 'sketch', 'adobe', 'design thinking',
        'user research', 'usability testing', 'information architecture',
    }
    
    MARKETING_SKILLS = {
        'marketing', 'digital marketing', 'seo', 'sem', 'content marketing',
        'social media', 'email marketing', 'campaign', 'brand', 'copywriting',
        'analytics', 'google analytics', 'google ads', 'facebook ads',
        'crm', 'marketing automation', 'hubspot', 'marketo',
    }
    
    SALES_SKILLS = {
        'sales', 'business development', 'account management', 'crm',
        'salesforce', 'pipeline', 'quota', 'cold calling', 'negotiation',
        'closing', 'prospecting', 'lead generation', 'client relations',
    }
    
    FINANCE_SKILLS = {
        'financial analysis', 'accounting', 'budgeting', 'forecasting',
        'financial modeling', 'valuation', 'excel', 'quickbooks',
        'financial reporting', 'audit', 'tax', 'compliance',
        'cpa', 'cfa', 'gaap',
    }
    
    # Skill level indicators
    JUNIOR_INDICATORS = {
        'assisted', 'supported', 'learned', 'shadowed', 'trained',
        'entry-level', 'junior', 'intern', 'associate',
    }
    
    MID_INDICATORS = {
        'developed', 'implemented', 'managed', 'coordinated',
        'mid-level', 'intermediate', 'experienced',
    }
    
    SENIOR_INDICATORS = {
        'led', 'architected', 'designed', 'established', 'pioneered',
        'senior', 'principal', 'staff', 'lead', 'strategic',
    }
    
    EXPERT_INDICATORS = {
        'expert', 'specialist', 'architect', 'distinguished', 'fellow',
        'thought leader', 'authority', 'recognized expert',
    }
    
    def __init__(self):
        """Initialize the categorizer"""
        self.categorized_terms: Dict[str, CategorizedTerm] = {}
    
    def categorize_terms(
        self,
        terms: Dict[str, ExtractedTerm],
        contexts: Optional[Dict[str, TermContext]] = None
    ) -> Dict[str, CategorizedTerm]:
        """
        Categorize all terms with domain and role information.
        
        Args:
            terms: Dictionary of extracted terms
            contexts: Optional dictionary of term contexts
            
        Returns:
            Dictionary of categorized terms
        """
        self.categorized_terms = {}
        
        for term_key, term in terms.items():
            context = contexts.get(term_key) if contexts else None
            categorized = self._categorize_single_term(term, context)
            self.categorized_terms[term_key] = categorized
        
        return self.categorized_terms
    
    def _categorize_single_term(
        self,
        term: ExtractedTerm,
        context: Optional[TermContext]
    ) -> CategorizedTerm:
        """Categorize a single term"""
        categorized = CategorizedTerm(term=term, context=context)
        
        # Determine skill domain
        categorized.skill_domain = self._classify_domain(term, context)
        
        # Determine role categories
        categorized.role_categories = self._classify_roles(term)
        
        # Infer skill level
        categorized.skill_level = self._infer_skill_level(term, context)
        
        # Check if industry-specific
        categorized.industry_specific = self._is_industry_specific(term)
        
        return categorized
    
    def _classify_domain(
        self,
        term: ExtractedTerm,
        context: Optional[TermContext]
    ) -> SkillDomain:
        """Classify term into a skill domain"""
        term_lower = term.text.lower()
        context_text = context.term.context_window.lower() if context else ""
        combined = term_lower + " " + context_text
        
        # Check each domain
        domain_scores = {
            SkillDomain.TECHNICAL: self._count_indicators(combined, self.TECHNICAL_INDICATORS),
            SkillDomain.BUSINESS: self._count_indicators(combined, self.BUSINESS_INDICATORS),
            SkillDomain.CREATIVE: self._count_indicators(combined, self.CREATIVE_INDICATORS),
            SkillDomain.ANALYTICAL: self._count_indicators(combined, self.ANALYTICAL_INDICATORS),
            SkillDomain.INTERPERSONAL: self._count_indicators(combined, self.INTERPERSONAL_INDICATORS),
        }
        
        # Also consider term category
        if term.category == TermCategory.LANGUAGE:
            domain_scores[SkillDomain.TECHNICAL] += 5
        elif term.category == TermCategory.SOFT_SKILL:
            domain_scores[SkillDomain.INTERPERSONAL] += 5
        elif term.category == TermCategory.TOOL:
            domain_scores[SkillDomain.TECHNICAL] += 3
        
        # Get domain with highest score
        max_score = max(domain_scores.values())
        if max_score == 0:
            return SkillDomain.UNKNOWN
        
        for domain, score in domain_scores.items():
            if score == max_score:
                return domain
        
        return SkillDomain.UNKNOWN
    
    def _classify_roles(self, term: ExtractedTerm) -> Set[RoleCategory]:
        """Classify which roles this term is relevant for"""
        roles = set()
        term_lower = term.text.lower()
        
        # Check against role-specific skill sets
        if term_lower in self.ENGINEERING_SKILLS or any(ind in term_lower for ind in ['programming', 'software', 'code']):
            roles.add(RoleCategory.ENGINEERING)
        
        if term_lower in self.DATA_SCIENCE_SKILLS or any(ind in term_lower for ind in ['data', 'analytics', 'machine learning']):
            roles.add(RoleCategory.DATA_SCIENCE)
        
        if term_lower in self.PRODUCT_SKILLS or any(ind in term_lower for ind in ['product', 'roadmap', 'backlog']):
            roles.add(RoleCategory.PRODUCT)
        
        if term_lower in self.DESIGN_SKILLS or any(ind in term_lower for ind in ['design', 'ux', 'ui']):
            roles.add(RoleCategory.DESIGN)
        
        if term_lower in self.MARKETING_SKILLS or any(ind in term_lower for ind in ['marketing', 'seo', 'campaign']):
            roles.add(RoleCategory.MARKETING)
        
        if term_lower in self.SALES_SKILLS or any(ind in term_lower for ind in ['sales', 'account', 'quota']):
            roles.add(RoleCategory.SALES)
        
        if term_lower in self.FINANCE_SKILLS or any(ind in term_lower for ind in ['financial', 'accounting', 'budget']):
            roles.add(RoleCategory.FINANCE)
        
        # Soft skills and methodologies are often general
        if term.category in {TermCategory.SOFT_SKILL, TermCategory.METHODOLOGY}:
            roles.add(RoleCategory.GENERAL)
        
        # If no specific role, mark as general
        if not roles:
            roles.add(RoleCategory.GENERAL)
        
        return roles
    
    def _infer_skill_level(
        self,
        term: ExtractedTerm,
        context: Optional[TermContext]
    ) -> Optional[str]:
        """Infer skill level from context"""
        if not context:
            return None
        
        context_lower = context.term.context_window.lower()
        
        # Check for explicit level indicators
        if any(ind in context_lower for ind in self.EXPERT_INDICATORS):
            return "expert"
        
        if any(ind in context_lower for ind in self.SENIOR_INDICATORS):
            return "senior"
        
        if any(ind in context_lower for ind in self.MID_INDICATORS):
            return "mid"
        
        if any(ind in context_lower for ind in self.JUNIOR_INDICATORS):
            return "junior"
        
        # Infer from action verbs
        if context.action_verbs:
            strongest = context.get_strongest_verb()
            if strongest:
                verb, strength = strongest
                if strength.name == "STRONG":
                    return "senior"
                elif strength.name == "MODERATE":
                    return "mid"
                elif strength.name == "WEAK":
                    return "junior"
        
        return None
    
    def _is_industry_specific(self, term: ExtractedTerm) -> bool:
        """Check if term is industry-specific"""
        # Domain knowledge terms are often industry-specific
        if term.category == TermCategory.DOMAIN_KNOWLEDGE:
            return True
        
        # Certifications can be industry-specific
        if term.category == TermCategory.CERTIFICATION:
            return True
        
        # Check for industry-specific keywords
        industry_keywords = {
            'hipaa', 'gdpr', 'sox', 'pci', 'clinical', 'pharmaceutical',
            'fintech', 'edtech', 'healthtech', 'biotech',
        }
        
        return any(kw in term.text.lower() for kw in industry_keywords)
    
    def _count_indicators(self, text: str, indicators: Set[str]) -> int:
        """Count how many indicators appear in text"""
        count = 0
        for indicator in indicators:
            if indicator in text:
                count += 1
        return count
    
    def get_by_domain(self, domain: SkillDomain) -> List[CategorizedTerm]:
        """Get all terms in a specific skill domain"""
        return [
            term for term in self.categorized_terms.values()
            if term.skill_domain == domain
        ]
    
    def get_by_role(self, role: RoleCategory) -> List[CategorizedTerm]:
        """Get all terms relevant for a specific role"""
        return [
            term for term in self.categorized_terms.values()
            if role in term.role_categories
        ]
    
    def get_transferable_skills(self) -> List[CategorizedTerm]:
        """Get skills that are broadly transferable"""
        return [
            term for term in self.categorized_terms.values()
            if term.is_transferable()
        ]
    
    def get_by_skill_level(self, level: str) -> List[CategorizedTerm]:
        """Get terms at a specific skill level"""
        return [
            term for term in self.categorized_terms.values()
            if term.skill_level == level
        ]
    
    def generate_taxonomy_report(self) -> Dict:
        """Generate a report of the term taxonomy"""
        if not self.categorized_terms:
            return {
                'total_terms': 0,
                'by_domain': {},
                'by_role': {},
                'by_level': {},
                'transferable_count': 0,
                'industry_specific_count': 0,
            }
        
        # Count by domain
        domain_counts = Counter(
            term.skill_domain for term in self.categorized_terms.values()
        )
        
        # Count by role (terms can have multiple roles)
        role_counts = Counter()
        for term in self.categorized_terms.values():
            for role in term.role_categories:
                role_counts[role] += 1
        
        # Count by level
        level_counts = Counter(
            term.skill_level for term in self.categorized_terms.values()
            if term.skill_level
        )
        
        transferable_count = len(self.get_transferable_skills())
        industry_specific_count = sum(
            1 for term in self.categorized_terms.values()
            if term.industry_specific
        )
        
        return {
            'total_terms': len(self.categorized_terms),
            'by_domain': {d.value: count for d, count in domain_counts.items()},
            'by_role': {r.value: count for r, count in role_counts.items()},
            'by_level': dict(level_counts),
            'transferable_count': transferable_count,
            'industry_specific_count': industry_specific_count,
        }


def categorize_terms(
    terms: Dict[str, ExtractedTerm],
    contexts: Optional[Dict[str, TermContext]] = None
) -> Dict[str, CategorizedTerm]:
    """
    Convenience function to categorize terms.
    
    Args:
        terms: Dictionary of extracted terms
        contexts: Optional dictionary of term contexts
        
    Returns:
        Dictionary of categorized terms
    """
    categorizer = TermCategorizer()
    return categorizer.categorize_terms(terms, contexts)
