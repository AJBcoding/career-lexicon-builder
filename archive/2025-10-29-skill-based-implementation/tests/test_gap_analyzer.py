"""
Tests for Gap Analysis Module
Tests Phase 4.2: Gap Analysis
"""

import pytest
from datetime import date

from src.gap_analyzer import (
    GapSeverity,
    MatchQuality,
    SkillGap,
    SkillStrength,
    GapAnalysisReport,
    GapAnalyzer,
    analyze_job_fit
)
from src.lexicon_builder import (
    SkillLexicon,
    DocumentMetadata,
    AggregatedSkill
)
from src.term_extractor import ExtractedTerm, TermCategory
from src.context_analyzer import TermContext
from src.term_categorizer import CategorizedTerm, SkillDomain, RoleCategory


class TestSkillGap:
    """Test SkillGap dataclass"""
    
    def test_gap_creation(self):
        """Test creating a skill gap"""
        gap = SkillGap(
            required_skill="Machine Learning",
            severity=GapSeverity.CRITICAL,
            requirement_type='required'
        )
        
        assert gap.required_skill == "Machine Learning"
        assert gap.severity == GapSeverity.CRITICAL
        assert gap.requirement_type == 'required'
    
    def test_has_transferable_match(self):
        """Test checking for transferable matches"""
        # Create aggregated skill
        skill = AggregatedSkill(
            skill_name="data analysis",
            category=TermCategory.SOFT_SKILL,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.DATA_SCIENCE},
            is_transferable=True
        )
        
        gap = SkillGap(
            required_skill="Machine Learning",
            severity=GapSeverity.SIGNIFICANT,
            requirement_type='required',
            closest_matches=[(skill, MatchQuality.MODERATE)]
        )
        
        assert gap.has_transferable_match() is True
    
    def test_get_best_match(self):
        """Test getting best match"""
        skill1 = AggregatedSkill(
            "skill1", TermCategory.TOOL,
            SkillDomain.TECHNICAL, {RoleCategory.ENGINEERING}
        )
        skill2 = AggregatedSkill(
            "skill2", TermCategory.TOOL,
            SkillDomain.TECHNICAL, {RoleCategory.ENGINEERING}
        )
        
        gap = SkillGap(
            required_skill="required_skill",
            severity=GapSeverity.MODERATE,
            requirement_type='required',
            closest_matches=[
                (skill1, MatchQuality.WEAK),
                (skill2, MatchQuality.STRONG)
            ]
        )
        
        best = gap.get_best_match()
        assert best is not None
        assert best[0] == skill2
        assert best[1] == MatchQuality.STRONG


class TestSkillStrength:
    """Test SkillStrength dataclass"""
    
    def test_strength_creation(self):
        """Test creating a skill strength"""
        skill = AggregatedSkill(
            "python", TermCategory.LANGUAGE,
            SkillDomain.TECHNICAL, {RoleCategory.ENGINEERING}
        )
        
        strength = SkillStrength(
            skill=skill,
            match_quality=MatchQuality.EXACT,
            emphasis_score=0.85,
            suggested_verbs=["developed", "built"],
            quantifiable_examples=["50%", "10M+"]
        )
        
        assert strength.skill.skill_name == "python"
        assert strength.match_quality == MatchQuality.EXACT
        assert strength.emphasis_score == 0.85
    
    def test_should_emphasize_heavily(self):
        """Test emphasis threshold check"""
        skill = AggregatedSkill(
            "python", TermCategory.LANGUAGE,
            SkillDomain.TECHNICAL, {RoleCategory.ENGINEERING}
        )
        
        strong_strength = SkillStrength(
            skill=skill,
            match_quality=MatchQuality.EXACT,
            emphasis_score=0.8
        )
        
        weak_strength = SkillStrength(
            skill=skill,
            match_quality=MatchQuality.WEAK,
            emphasis_score=0.4
        )
        
        assert strong_strength.should_emphasize_heavily() is True
        assert weak_strength.should_emphasize_heavily() is False


class TestGapAnalysisReport:
    """Test GapAnalysisReport dataclass"""
    
    def test_report_creation(self):
        """Test creating a gap analysis report"""
        report = GapAnalysisReport(
            job_title="Software Engineer",
            organization="Tech Corp"
        )
        
        assert report.job_title == "Software Engineer"
        assert report.organization == "Tech Corp"
        assert len(report.critical_gaps) == 0
        assert len(report.exact_matches) == 0
    
    def test_calculate_match_percentage(self):
        """Test match percentage calculation"""
        report = GapAnalysisReport(job_title="Engineer")
        
        report.total_requirements = 10
        report.requirements_met = 7
        report.requirements_addressable = 2
        
        report.calculate_match_percentage()
        
        # 7 met + (2 addressable * 0.5) = 8 / 10 = 80%
        assert report.match_percentage == 80.0
    
    def test_get_all_gaps(self):
        """Test getting all gaps"""
        report = GapAnalysisReport(job_title="Engineer")
        
        gap1 = SkillGap("skill1", GapSeverity.CRITICAL, 'required')
        gap2 = SkillGap("skill2", GapSeverity.MODERATE, 'preferred')
        
        report.critical_gaps.append(gap1)
        report.moderate_gaps.append(gap2)
        
        all_gaps = report.get_all_gaps()
        assert len(all_gaps) == 2
        assert gap1 in all_gaps
        assert gap2 in all_gaps
    
    def test_get_top_strengths(self):
        """Test getting top strengths"""
        report = GapAnalysisReport(job_title="Engineer")
        
        skill1 = AggregatedSkill("s1", TermCategory.TOOL, SkillDomain.TECHNICAL, set())
        skill2 = AggregatedSkill("s2", TermCategory.TOOL, SkillDomain.TECHNICAL, set())
        
        strength1 = SkillStrength(skill1, MatchQuality.EXACT, 0.9)
        strength2 = SkillStrength(skill2, MatchQuality.STRONG, 0.7)
        
        report.exact_matches = [strength1, strength2]
        
        top = report.get_top_strengths(n=1)
        assert len(top) == 1
        assert top[0].emphasis_score == 0.9
    
    def test_generate_summary(self):
        """Test generating summary"""
        report = GapAnalysisReport(job_title="Engineer")
        report.total_requirements = 10
        report.requirements_met = 8
        report.match_percentage = 80.0
        
        summary = report.generate_summary()
        
        assert summary['job_title'] == "Engineer"
        assert summary['total_requirements'] == 10
        assert summary['match_percentage'] == 80.0
        assert 'gaps_by_severity' in summary
        assert 'strengths_by_quality' in summary


class TestGapAnalyzer:
    """Test GapAnalyzer class"""
    
    def test_analyzer_creation(self):
        """Test creating gap analyzer"""
        lexicon = SkillLexicon()
        analyzer = GapAnalyzer(lexicon)
        
        assert analyzer.lexicon == lexicon
        assert analyzer.report is None
    
    def test_exact_match_detection(self):
        """Test detection of exact skill matches"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        # Required skills that match lexicon
        required = self._create_required_skills(["python", "aws"])
        
        report = analyzer.analyze_job_requirements(
            "Software Engineer",
            required
        )
        
        assert len(report.exact_matches) == 2
        assert report.requirements_met >= 2
    
    def test_gap_identification(self):
        """Test identification of skill gaps"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        # Required skills not in lexicon but in same domain
        # These should be found as transferable matches, not gaps
        required = self._create_required_skills(["rust", "golang"])
        
        report = analyzer.analyze_job_requirements(
            "Software Engineer",
            required
        )
        
        # Should find transferable matches since they're same domain/role
        assert len(report.transferable_matches) >= 2 or len(report.strong_matches) >= 2
    
    def test_true_gap_identification(self):
        """Test identification of true gaps with completely unrelated skills"""
        # Create lexicon with only technical engineering skills
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        # Require skills from completely different domain/role
        finance_term = ExtractedTerm("financial modeling", TermCategory.SOFT_SKILL, frequency=1)
        finance_cat = CategorizedTerm(
            term=finance_term,
            skill_domain=SkillDomain.BUSINESS,  # Different domain
            role_categories={RoleCategory.FINANCE}  # Different role
        )
        
        required = {"financial modeling": finance_cat}
        
        report = analyzer.analyze_job_requirements(
            "Financial Analyst",
            required
        )
        
        # Should identify as a gap since completely different domain/role
        all_gaps = report.get_all_gaps()
        assert len(all_gaps) >= 1
    
    def test_transferable_match_detection(self):
        """Test detection of transferable skills"""
        lexicon = self._create_test_lexicon()
        
        # Add transferable skill
        metadata = DocumentMetadata("resume.pdf", "resume", date=date.today())
        term = ExtractedTerm("problem solving", TermCategory.SOFT_SKILL, frequency=1)
        context = TermContext(term=term)
        context.prominence_score = 0.7
        cat_term = CategorizedTerm(
            term=term,
            skill_domain=SkillDomain.INTERPERSONAL,
            role_categories={RoleCategory.GENERAL}
        )
        cat_term._is_transferable = True
        
        lexicon.add_document_analysis(
            metadata,
            {"problem solving": cat_term},
            {"problem solving": context}
        )
        
        analyzer = GapAnalyzer(lexicon)
        
        # Required skill in same domain
        required = self._create_required_skills(["leadership"])
        
        report = analyzer.analyze_job_requirements(
            "Manager",
            required
        )
        
        # Should find transferable match or gap with match
        assert (len(report.transferable_matches) > 0 or
                any(gap.has_transferable_match() for gap in report.get_all_gaps()))
    
    def test_severity_classification(self):
        """Test gap severity classification"""
        lexicon = SkillLexicon()  # Empty lexicon
        analyzer = GapAnalyzer(lexicon)
        
        # Required vs preferred skills
        required = self._create_required_skills(["python"])
        preferred = self._create_required_skills(["golang"])
        
        report = analyzer.analyze_job_requirements(
            "Engineer",
            required,
            preferred
        )
        
        all_gaps = report.get_all_gaps()
        
        # Required missing skills should be critical/significant
        required_gaps = [g for g in all_gaps if g.requirement_type == 'required']
        if required_gaps:
            assert any(
                g.severity in [GapSeverity.CRITICAL, GapSeverity.SIGNIFICANT]
                for g in required_gaps
            )
    
    def test_emphasis_score_calculation(self):
        """Test emphasis score calculation for matches"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        required = self._create_required_skills(["python"])
        
        report = analyzer.analyze_job_requirements(
            "Software Engineer",
            required
        )
        
        if report.exact_matches:
            match = report.exact_matches[0]
            assert 0.0 <= match.emphasis_score <= 1.0
    
    def test_preferred_vs_required(self):
        """Test handling of preferred vs required skills"""
        lexicon = SkillLexicon()  # Empty
        analyzer = GapAnalyzer(lexicon)
        
        required = self._create_required_skills(["python"])
        preferred = self._create_required_skills(["golang"])
        
        report = analyzer.analyze_job_requirements(
            "Engineer",
            required,
            preferred
        )
        
        assert report.total_requirements == 2
        
        # Should have gaps for both
        all_gaps = report.get_all_gaps()
        assert len(all_gaps) == 2
        
        # Required gap should be more severe
        required_gap = next(g for g in all_gaps if g.required_skill == "python")
        preferred_gap = next(g for g in all_gaps if g.required_skill == "golang")
        
        severity_order = {
            GapSeverity.CRITICAL: 4,
            GapSeverity.SIGNIFICANT: 3,
            GapSeverity.MODERATE: 2,
            GapSeverity.MINOR: 1
        }
        
        assert (severity_order[required_gap.severity] >= 
                severity_order[preferred_gap.severity])
    
    def test_generate_application_guidance(self):
        """Test generation of application guidance"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        required = self._create_required_skills(["python", "aws"])
        
        report = analyzer.analyze_job_requirements(
            "Software Engineer",
            required
        )
        
        guidance = analyzer.generate_application_guidance()
        
        assert 'resume_priorities' in guidance
        assert 'cover_letter_priorities' in guidance
        assert 'overall_strategy' in guidance
        
        assert 'must_include' in guidance['resume_priorities']
        assert 'lead_with_strengths' in guidance['cover_letter_priorities']
    
    def test_overall_strategy_recommendation(self):
        """Test overall strategy recommendations"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        # High match percentage scenario
        required = self._create_required_skills(["python", "aws"])
        report = analyzer.analyze_job_requirements("Engineer", required)
        guidance = analyzer.generate_application_guidance()
        
        # Should have a strategy
        assert len(guidance['overall_strategy']) > 0
    
    def test_empty_lexicon_analysis(self):
        """Test analysis with empty lexicon"""
        lexicon = SkillLexicon()
        analyzer = GapAnalyzer(lexicon)
        
        required = self._create_required_skills(["python"])
        
        report = analyzer.analyze_job_requirements("Engineer", required)
        
        assert report.total_requirements == 1
        assert report.requirements_met == 0
        assert len(report.get_all_gaps()) == 1
    
    def test_full_match_scenario(self):
        """Test scenario with all requirements met"""
        lexicon = self._create_test_lexicon()
        analyzer = GapAnalyzer(lexicon)
        
        # Only require skills we have
        required = self._create_required_skills(["python", "aws"])
        
        report = analyzer.analyze_job_requirements("Engineer", required)
        
        assert report.requirements_met == 2
        assert report.match_percentage >= 80.0  # Should be high
    
    def _create_test_lexicon(self) -> SkillLexicon:
        """Helper to create test lexicon"""
        lexicon = SkillLexicon()
        
        today = date.today()
        metadata = DocumentMetadata("resume.pdf", "resume", date=today)
        
        # Add Python
        python_term = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=3)
        python_context = TermContext(term=python_term)
        python_context.prominence_score = 0.9
        python_cat = CategorizedTerm(
            term=python_term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        # Add AWS
        aws_term = ExtractedTerm("AWS", TermCategory.TOOL, frequency=2)
        aws_context = TermContext(term=aws_term)
        aws_context.prominence_score = 0.8
        aws_cat = CategorizedTerm(
            term=aws_term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        lexicon.add_document_analysis(
            metadata,
            {"python": python_cat, "aws": aws_cat},
            {"python": python_context, "aws": aws_context}
        )
        
        return lexicon
    
    def _create_required_skills(self, skill_names: list) -> dict:
        """Helper to create required skills dict"""
        required = {}
        
        for name in skill_names:
            term = ExtractedTerm(name, TermCategory.TOOL, frequency=1)
            cat_term = CategorizedTerm(
                term=term,
                skill_domain=SkillDomain.TECHNICAL,
                role_categories={RoleCategory.ENGINEERING}
            )
            required[name.lower()] = cat_term
        
        return required


class TestConvenienceFunction:
    """Test convenience function"""
    
    def test_analyze_job_fit(self):
        """Test convenience function for job fit analysis"""
        lexicon = SkillLexicon()
        
        today = date.today()
        metadata = DocumentMetadata("resume.pdf", "resume", date=today)
        
        term = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=1)
        context = TermContext(term=term)
        cat_term = CategorizedTerm(
            term=term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        lexicon.add_document_analysis(
            metadata,
            {"python": cat_term},
            {"python": context}
        )
        
        required = {
            "python": CategorizedTerm(
                term=ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=1),
                skill_domain=SkillDomain.TECHNICAL,
                role_categories={RoleCategory.ENGINEERING}
            )
        }
        
        report = analyze_job_fit(
            lexicon,
            "Software Engineer",
            required,
            organization="Tech Corp"
        )
        
        assert report.job_title == "Software Engineer"
        assert report.organization == "Tech Corp"
        assert report.total_requirements == 1


class TestEdgeCases:
    """Test edge cases"""
    
    def test_no_required_skills(self):
        """Test analysis with no required skills"""
        lexicon = SkillLexicon()
        analyzer = GapAnalyzer(lexicon)
        
        report = analyzer.analyze_job_requirements("Engineer", {})
        
        assert report.total_requirements == 0
        assert report.match_percentage == 0.0
    
    def test_case_insensitive_matching(self):
        """Test that matching is case-insensitive"""
        lexicon = SkillLexicon()
        
        today = date.today()
        metadata = DocumentMetadata("resume.pdf", "resume", date=today)
        
        # Add skill in lowercase
        term = ExtractedTerm("python", TermCategory.LANGUAGE, frequency=1)
        context = TermContext(term=term)
        cat_term = CategorizedTerm(
            term=term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        lexicon.add_document_analysis(
            metadata,
            {"python": cat_term},
            {"python": context}
        )
        
        analyzer = GapAnalyzer(lexicon)
        
        # Require skill in uppercase
        required = {
            "python": CategorizedTerm(
                term=ExtractedTerm("PYTHON", TermCategory.LANGUAGE, frequency=1),
                skill_domain=SkillDomain.TECHNICAL,
                role_categories={RoleCategory.ENGINEERING}
            )
        }
        
        report = analyzer.analyze_job_requirements("Engineer", required)
        
        # Should find exact match
        assert len(report.exact_matches) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
