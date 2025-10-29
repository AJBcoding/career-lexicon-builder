"""
Gap Analysis Module
Compares skill lexicon against job description requirements.

Part of Phase 4: Lexicon Building
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

from src.lexicon_builder import SkillLexicon, AggregatedSkill
from src.term_extractor import extract_terms_from_text, TermCategory
from src.context_analyzer import analyze_term_contexts
from src.term_categorizer import categorize_terms, SkillDomain, RoleCategory


class MatchLevel(Enum):
    """Level of match between candidate skills and requirements"""
    STRONG = "strong"  # Have skill, used recently, high proficiency
    GOOD = "good"  # Have skill, moderate recency/proficiency
    WEAK = "weak"  # Have skill but outdated or low proficiency
    MISSING = "missing"  # Don't have skill


@dataclass
class SkillMatch:
    """Match information for a single required skill"""
    required_skill: str
    match_level: MatchLevel
    candidate_skill: Optional[AggregatedSkill] = None
    
    # Match quality indicators
    recency_score: float = 0.0
    proficiency_score: float = 0.0
    relevance_score: float = 0.0
    
    # Recommendations
    recommendation: str = ""
    
    def get_overall_score(self) -> float:
        """Calculate overall match score (0-1)"""
        if self.match_level == MatchLevel.MISSING:
            return 0.0
        return (self.recency_score * 0.4 + 
                self.proficiency_score * 0.3 + 
                self.relevance_score * 0.3)


@dataclass
class GapAnalysisResult:
    """
    Results of comparing candidate skills against job requirements.
    """
    job_title: str
    job_company: Optional[str] = None
    
    # Required skills analysis
    strong_matches: List[SkillMatch] = field(default_factory=list)
    good_matches: List[SkillMatch] = field(default_factory=list)
    weak_matches: List[SkillMatch] = field(default_factory=list)
    missing_skills: List[SkillMatch] = field(default_factory=list)
    
    # Additional candidate skills (not required but relevant)
    additional_strengths: List[AggregatedSkill] = field(default_factory=list)
    
    # Summary metrics
    match_percentage: float = 0.0
    confidence_level: str = "unknown"  # high/medium/low
    
    def get_summary(self) -> Dict:
        """Generate summary statistics"""
        total_required = (len(self.strong_matches) + len(self.good_matches) + 
                         len(self.weak_matches) + len(self.missing_skills))
        
        matched = len(self.strong_matches) + len(self.good_matches)
        
        return {
            'job_title': self.job_title,
            'job_company': self.job_company,
            'total_required_skills': total_required,
            'strong_matches': len(self.strong_matches),
            'good_matches': len(self.good_matches),
            'weak_matches': len(self.weak_matches),
            'missing_skills': len(self.missing_skills),
            'match_percentage': self.match_percentage,
            'confidence_level': self.confidence_level,
            'additional_strengths_count': len(self.additional_strengths)
        }
    
    def get_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        # Prioritize missing critical skills
        if self.missing_skills:
            critical_missing = [s.required_skill for s in self.missing_skills[:3]]
            recs.append(f"Critical gaps: {', '.join(critical_missing)}")
            recs.append("Consider addressing these gaps before applying")
        
        # Strengthen weak matches
        if self.weak_matches:
            weak_skills = [s.required_skill for s in self.weak_matches[:2]]
            recs.append(f"Refresh these skills: {', '.join(weak_skills)}")
        
        # Leverage strengths
        if self.strong_matches:
            recs.append(f"Emphasize your strong matches ({len(self.strong_matches)} skills)")
        
        # Highlight transferable skills
        if self.additional_strengths:
            transferable = [s.skill_name for s in self.additional_strengths if s.is_transferable][:3]
            if transferable:
                recs.append(f"Highlight transferable skills: {', '.join(transferable)}")
        
        return recs


class GapAnalyzer:
    """
    Analyzes gaps between candidate skills and job requirements.
    """
    
    def __init__(self, lexicon: SkillLexicon):
        """
        Initialize with candidate's skill lexicon.
        
        Args:
            lexicon: Candidate's aggregated skill lexicon
        """
        self.lexicon = lexicon
    
    def analyze_job_description(
        self,
        job_description: str,
        job_title: str,
        job_company: Optional[str] = None
    ) -> GapAnalysisResult:
        """
        Analyze gaps between candidate skills and job requirements.
        
        Args:
            job_description: Full text of job description
            job_title: Job title
            job_company: Company name (optional)
            
        Returns:
            GapAnalysisResult with detailed analysis
        """
        # Extract required skills from job description
        required_terms = extract_terms_from_text(job_description, document_type="job_description")
        contexts = analyze_term_contexts(required_terms, job_description)
        categorized = categorize_terms(required_terms, contexts)
        
        result = GapAnalysisResult(
            job_title=job_title,
            job_company=job_company
        )
        
        # Analyze each required skill
        for skill_key, cat_term in categorized.items():
            skill_name = cat_term.term.text.lower()
            context = contexts.get(skill_key)
            
            match = self._match_skill(
                skill_name,
                cat_term.term.category,
                cat_term.skill_domain,
                cat_term.role_categories,
                context
            )
            
            # Categorize match
            if match.match_level == MatchLevel.STRONG:
                result.strong_matches.append(match)
            elif match.match_level == MatchLevel.GOOD:
                result.good_matches.append(match)
            elif match.match_level == MatchLevel.WEAK:
                result.weak_matches.append(match)
            else:
                result.missing_skills.append(match)
        
        # Calculate match percentage
        total_required = len(categorized)
        if total_required > 0:
            matched = len(result.strong_matches) + len(result.good_matches)
            result.match_percentage = (matched / total_required) * 100
        
        # Determine confidence level
        result.confidence_level = self._calculate_confidence(result)
        
        # Identify additional strengths
        result.additional_strengths = self._find_additional_strengths(
            categorized,
            result
        )
        
        return result
    
    def _match_skill(
        self,
        required_skill: str,
        category: TermCategory,
        domain: SkillDomain,
        roles: Set[RoleCategory],
        context: Optional[any] = None
    ) -> SkillMatch:
        """
        Match a required skill against candidate's lexicon.
        
        Returns:
            SkillMatch object with match details
        """
        match = SkillMatch(
            required_skill=required_skill,
            match_level=MatchLevel.MISSING
        )
        
        # Check for exact match
        if required_skill in self.lexicon.skills:
            candidate_skill = self.lexicon.skills[required_skill]
            match.candidate_skill = candidate_skill
            
            # Calculate scores
            match.recency_score = candidate_skill.get_recency_score()
            match.proficiency_score = self._calculate_proficiency(candidate_skill)
            match.relevance_score = self._calculate_relevance(candidate_skill, domain, roles)
            
            # Determine match level
            overall_score = match.get_overall_score()
            if overall_score >= 0.7:
                match.match_level = MatchLevel.STRONG
                match.recommendation = f"Strong match - emphasize in application"
            elif overall_score >= 0.4:
                match.match_level = MatchLevel.GOOD
                match.recommendation = f"Good match - highlight relevant experience"
            else:
                match.match_level = MatchLevel.WEAK
                match.recommendation = f"Refresh this skill before applying"
        
        else:
            # Check for related skills
            related = self._find_related_skills(required_skill, category, domain)
            if related:
                match.recommendation = f"No direct match - consider highlighting: {', '.join([s.skill_name for s in related[:2]])}"
            else:
                match.recommendation = f"Missing skill - consider acquiring or emphasizing transferable skills"
        
        return match
    
    def _calculate_proficiency(self, skill: AggregatedSkill) -> float:
        """
        Calculate proficiency score based on usage patterns.
        
        Factors:
        - Frequency of use
        - Prominence in documents
        - Action verb strength
        - Quantifiable impact
        """
        score = 0.0
        
        # Frequency component
        score += skill.get_frequency_score() * 0.4
        
        # Prominence component
        score += skill.avg_prominence * 0.3
        
        # Action verb component
        strong_verbs = sum(1 for v in skill.all_action_verbs 
                          if v in ['led', 'architected', 'developed', 'launched'])
        if strong_verbs > 0:
            score += min(0.2, strong_verbs / 10.0)
        
        # Quantifiable impact component
        if skill.all_quantifiers:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_relevance(
        self,
        skill: AggregatedSkill,
        target_domain: SkillDomain,
        target_roles: Set[RoleCategory]
    ) -> float:
        """
        Calculate relevance to target job.
        
        Factors:
        - Domain match
        - Role match
        - Transferability
        """
        score = 0.0
        
        # Domain match
        if skill.skill_domain == target_domain:
            score += 0.5
        elif skill.is_transferable:
            score += 0.25
        
        # Role match
        role_overlap = len(skill.role_categories & target_roles)
        if role_overlap > 0:
            score += min(0.5, role_overlap / len(target_roles))
        
        return min(1.0, score)
    
    def _find_related_skills(
        self,
        required_skill: str,
        category: TermCategory,
        domain: SkillDomain
    ) -> List[AggregatedSkill]:
        """Find skills in lexicon related to required skill"""
        related = []
        
        for skill in self.lexicon.skills.values():
            # Same category and domain
            if (skill.category == category and 
                skill.skill_domain == domain):
                related.append(skill)
        
        # Sort by combined score
        related.sort(key=lambda s: s.get_combined_score(), reverse=True)
        
        return related[:5]
    
    def _calculate_confidence(self, result: GapAnalysisResult) -> str:
        """
        Calculate confidence level for application.
        
        Returns:
            'high', 'medium', or 'low'
        """
        if result.match_percentage >= 75:
            return 'high'
        elif result.match_percentage >= 50:
            return 'medium'
        else:
            return 'low'
    
    def _find_additional_strengths(
        self,
        required_skills: Dict,
        result: GapAnalysisResult
    ) -> List[AggregatedSkill]:
        """
        Find candidate's additional strengths not explicitly required.
        
        Returns:
            List of additional relevant skills
        """
        required_names = set(cat.term.text.lower() for cat in required_skills.values())
        
        additional = []
        for skill in self.lexicon.get_top_skills(20, by='combined'):
            if skill.skill_name not in required_names:
                # Check if relevant to any of the matched skills' domains/roles
                is_relevant = False
                for match in result.strong_matches + result.good_matches:
                    if match.candidate_skill:
                        if (skill.skill_domain == match.candidate_skill.skill_domain or
                            skill.role_categories & match.candidate_skill.role_categories):
                            is_relevant = True
                            break
                
                if is_relevant or skill.is_transferable:
                    additional.append(skill)
        
        return additional[:10]
    
    def compare_multiple_jobs(
        self,
        job_descriptions: List[Tuple[str, str, Optional[str]]]
    ) -> List[GapAnalysisResult]:
        """
        Compare against multiple job descriptions.
        
        Args:
            job_descriptions: List of (description, title, company) tuples
            
        Returns:
            List of GapAnalysisResult, sorted by match percentage
        """
        results = []
        
        for description, title, company in job_descriptions:
            result = self.analyze_job_description(description, title, company)
            results.append(result)
        
        # Sort by match percentage
        results.sort(key=lambda r: r.match_percentage, reverse=True)
        
        return results
    
    def generate_gap_report(self, result: GapAnalysisResult) -> str:
        """
        Generate human-readable gap analysis report.
        
        Returns:
            Formatted string report
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"GAP ANALYSIS REPORT: {result.job_title}")
        if result.job_company:
            lines.append(f"Company: {result.job_company}")
        lines.append("=" * 80)
        lines.append("")
        
        # Summary
        summary = result.get_summary()
        lines.append("SUMMARY:")
        lines.append(f"  Match Percentage: {result.match_percentage:.1f}%")
        lines.append(f"  Confidence Level: {result.confidence_level.upper()}")
        lines.append(f"  Total Required Skills: {summary['total_required_skills']}")
        lines.append(f"  Strong Matches: {summary['strong_matches']}")
        lines.append(f"  Good Matches: {summary['good_matches']}")
        lines.append(f"  Weak Matches: {summary['weak_matches']}")
        lines.append(f"  Missing Skills: {summary['missing_skills']}")
        lines.append("")
        
        # Strong matches
        if result.strong_matches:
            lines.append("STRONG MATCHES (Emphasize These):")
            for match in result.strong_matches[:10]:
                skill = match.candidate_skill
                lines.append(f"  Ã¢Å“" {match.required_skill:25} | "
                           f"Score: {match.get_overall_score():.2f} | "
                           f"Used in {skill.total_documents} docs")
            lines.append("")
        
        # Good matches
        if result.good_matches:
            lines.append("GOOD MATCHES (Highlight These):")
            for match in result.good_matches[:10]:
                skill = match.candidate_skill
                lines.append(f"  Ã¢Å“" {match.required_skill:25} | "
                           f"Score: {match.get_overall_score():.2f} | "
                           f"Recency: {skill.get_recency_score():.2f}")
            lines.append("")
        
        # Weak matches
        if result.weak_matches:
            lines.append("WEAK MATCHES (Consider Refreshing):")
            for match in result.weak_matches[:5]:
                skill = match.candidate_skill
                days_since = (skill.last_used - skill.first_used).days if skill.last_used and skill.first_used else 0
                lines.append(f"  Ã¢â‚¬" {match.required_skill:25} | "
                           f"Last used: {skill.last_used} ({days_since} days ago)")
            lines.append("")
        
        # Missing skills
        if result.missing_skills:
            lines.append("MISSING SKILLS (Gaps to Address):")
            for match in result.missing_skills[:10]:
                lines.append(f"  Ã¢Å“â€” {match.required_skill:25} | {match.recommendation}")
            lines.append("")
        
        # Additional strengths
        if result.additional_strengths:
            lines.append("ADDITIONAL STRENGTHS (Not Required But Relevant):")
            for skill in result.additional_strengths[:5]:
                lines.append(f"  + {skill.skill_name:25} | "
                           f"Score: {skill.get_combined_score():.2f}")
            lines.append("")
        
        # Recommendations
        recommendations = result.get_recommendations()
        if recommendations:
            lines.append("RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


def analyze_job_fit(
    lexicon: SkillLexicon,
    job_description: str,
    job_title: str,
    job_company: Optional[str] = None
) -> GapAnalysisResult:
    """
    Convenience function for gap analysis.
    
    Args:
        lexicon: Candidate's skill lexicon
        job_description: Job description text
        job_title: Job title
        job_company: Company name (optional)
        
    Returns:
        GapAnalysisResult
    """
    analyzer = GapAnalyzer(lexicon)
    return analyzer.analyze_job_description(job_description, job_title, job_company)
