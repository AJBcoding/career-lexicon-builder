"""
Tests for Term Categorization Module
Tests Phase 3.3: Term Categorization
"""

import pytest
from src.term_extractor import ExtractedTerm, TermCategory, extract_terms_from_text
from src.context_analyzer import TermContext, ActionVerbStrength, analyze_term_contexts
from src.term_categorizer import (
    TermCategorizer,
    CategorizedTerm,
    SkillDomain,
    RoleCategory,
    categorize_terms
)


class TestCategorizedTerm:
    """Test CategorizedTerm dataclass"""
    
    def test_categorized_term_creation(self):
        """Test creating a categorized term"""
        term = ExtractedTerm(text="Python", category=TermCategory.LANGUAGE)
        cat_term = CategorizedTerm(
            term=term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING, RoleCategory.DATA_SCIENCE},
            skill_level="senior"
        )
        
        assert cat_term.term == term
        assert cat_term.skill_domain == SkillDomain.TECHNICAL
        assert len(cat_term.role_categories) == 2
        assert cat_term.skill_level == "senior"
    
    def test_is_transferable(self):
        """Test transferability detection"""
        # Soft skill should be transferable
        soft_skill = ExtractedTerm(text="leadership", category=TermCategory.SOFT_SKILL)
        cat1 = CategorizedTerm(term=soft_skill)
        assert cat1.is_transferable()
        
        # Methodology should be transferable
        methodology = ExtractedTerm(text="agile", category=TermCategory.METHODOLOGY)
        cat2 = CategorizedTerm(term=methodology)
        assert cat2.is_transferable()
        
        # Technical skill may not be transferable
        tech_skill = ExtractedTerm(text="python", category=TermCategory.LANGUAGE)
        cat3 = CategorizedTerm(term=tech_skill, skill_domain=SkillDomain.TECHNICAL)
        assert not cat3.is_transferable()
    
    def test_get_primary_role(self):
        """Test getting primary role category"""
        term = ExtractedTerm(text="Python")
        cat_term = CategorizedTerm(
            term=term,
            role_categories={RoleCategory.ENGINEERING, RoleCategory.DATA_SCIENCE}
        )
        
        primary = cat_term.get_primary_role()
        assert primary is not None
        assert primary in {RoleCategory.ENGINEERING, RoleCategory.DATA_SCIENCE}
    
    def test_get_primary_role_empty(self):
        """Test getting primary role when none exist"""
        term = ExtractedTerm(text="unknown")
        cat_term = CategorizedTerm(term=term)
        
        assert cat_term.get_primary_role() is None


class TestTermCategorizer:
    """Test TermCategorizer class"""
    
    def test_initialization(self):
        """Test categorizer initialization"""
        categorizer = TermCategorizer()
        assert isinstance(categorizer.categorized_terms, dict)
        assert len(categorizer.categorized_terms) == 0
    
    def test_classify_technical_domain(self):
        """Test classification of technical domain"""
        term = ExtractedTerm(text="Python", category=TermCategory.LANGUAGE)
        context = None
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, context)
        
        assert categorized.skill_domain == SkillDomain.TECHNICAL
    
    def test_classify_interpersonal_domain(self):
        """Test classification of interpersonal domain"""
        term = ExtractedTerm(text="leadership", category=TermCategory.SOFT_SKILL)
        context = None
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, context)
        
        assert categorized.skill_domain == SkillDomain.INTERPERSONAL
    
    def test_classify_business_domain(self):
        """Test classification of business domain"""
        text = "Strategic business planning and financial analysis"
        term = ExtractedTerm(
            text="business planning",
            category=TermCategory.DOMAIN_KNOWLEDGE,
            context_window=text
        )
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        # Should detect business indicators
        assert categorized.skill_domain in {SkillDomain.BUSINESS, SkillDomain.ANALYTICAL}
    
    def test_classify_engineering_role(self):
        """Test classification for engineering role"""
        term = ExtractedTerm(text="Python")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert RoleCategory.ENGINEERING in categorized.role_categories
    
    def test_classify_data_science_role(self):
        """Test classification for data science role"""
        term = ExtractedTerm(text="machine learning")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert RoleCategory.DATA_SCIENCE in categorized.role_categories
    
    def test_classify_marketing_role(self):
        """Test classification for marketing role"""
        term = ExtractedTerm(text="seo")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert RoleCategory.MARKETING in categorized.role_categories
    
    def test_classify_general_role(self):
        """Test classification for general/transferable skills"""
        term = ExtractedTerm(text="communication", category=TermCategory.SOFT_SKILL)
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert RoleCategory.GENERAL in categorized.role_categories
    
    def test_infer_senior_level(self):
        """Test inferring senior skill level"""
        term = ExtractedTerm(text="Python")
        term_context = TermContext(
            term=term,
            action_verbs=[("led", ActionVerbStrength.STRONG)]
        )
        term_context.term.context_window = "Led Python development teams"
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, term_context)
        
        assert categorized.skill_level == "senior"
    
    def test_infer_mid_level(self):
        """Test inferring mid skill level"""
        term = ExtractedTerm(text="Java")
        term_context = TermContext(
            term=term,
            action_verbs=[("managed", ActionVerbStrength.MODERATE)]
        )
        term_context.term.context_window = "Managed Java projects"
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, term_context)
        
        assert categorized.skill_level == "mid"
    
    def test_infer_junior_level(self):
        """Test inferring junior skill level"""
        term = ExtractedTerm(text="Python")
        term_context = TermContext(
            term=term,
            action_verbs=[("assisted", ActionVerbStrength.WEAK)]
        )
        term_context.term.context_window = "Assisted with Python development"
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, term_context)
        
        assert categorized.skill_level == "junior"
    
    def test_industry_specific_detection(self):
        """Test detection of industry-specific terms"""
        # Domain knowledge should be industry-specific
        term1 = ExtractedTerm(text="clinical protocols", category=TermCategory.DOMAIN_KNOWLEDGE)
        categorizer = TermCategorizer()
        cat1 = categorizer._categorize_single_term(term1, None)
        assert cat1.industry_specific
        
        # HIPAA is healthcare-specific
        term2 = ExtractedTerm(text="hipaa compliance")
        cat2 = categorizer._categorize_single_term(term2, None)
        assert cat2.industry_specific
    
    def test_categorize_multiple_terms(self):
        """Test categorizing multiple terms"""
        text = "Led Python development and SEO optimization campaigns"
        terms = extract_terms_from_text(text)
        
        categorizer = TermCategorizer()
        categorized = categorizer.categorize_terms(terms)
        
        assert len(categorized) > 0
        assert "python" in categorized
        assert "seo" in categorized  # SEO is a known marketing tool
    
    def test_get_by_domain(self):
        """Test filtering by skill domain"""
        text = "Python programming, leadership skills, and data analysis"
        terms = extract_terms_from_text(text)
        
        categorizer = TermCategorizer()
        categorizer.categorize_terms(terms)
        
        technical_terms = categorizer.get_by_domain(SkillDomain.TECHNICAL)
        assert len(technical_terms) > 0
        
        interpersonal_terms = categorizer.get_by_domain(SkillDomain.INTERPERSONAL)
        assert len(interpersonal_terms) > 0
    
    def test_get_by_role(self):
        """Test filtering by role category"""
        text = "Python development, SEO optimization, and financial analysis"
        terms = extract_terms_from_text(text)
        
        categorizer = TermCategorizer()
        categorizer.categorize_terms(terms)
        
        engineering_terms = categorizer.get_by_role(RoleCategory.ENGINEERING)
        assert len(engineering_terms) > 0
        
        marketing_terms = categorizer.get_by_role(RoleCategory.MARKETING)
        assert len(marketing_terms) > 0
    
    def test_get_transferable_skills(self):
        """Test getting transferable skills"""
        text = "Python programming, leadership, agile methodology, communication"
        terms = extract_terms_from_text(text)
        
        categorizer = TermCategorizer()
        categorizer.categorize_terms(terms)
        
        transferable = categorizer.get_transferable_skills()
        
        # Leadership, agile, and communication should be transferable
        assert len(transferable) >= 2
        transferable_texts = {t.term.text.lower() for t in transferable}
        assert any(skill in transferable_texts for skill in ['leadership', 'agile', 'communication'])
    
    def test_get_by_skill_level(self):
        """Test filtering by skill level"""
        text = """
        Led Python development teams.
        Managed Java projects.
        Assisted with AWS deployment.
        """
        terms = extract_terms_from_text(text)
        contexts = analyze_term_contexts(terms, text)
        
        categorizer = TermCategorizer()
        categorizer.categorize_terms(terms, contexts)
        
        senior_terms = categorizer.get_by_skill_level("senior")
        mid_terms = categorizer.get_by_skill_level("mid")
        junior_terms = categorizer.get_by_skill_level("junior")
        
        # Should have terms at different levels
        assert len(senior_terms) > 0 or len(mid_terms) > 0 or len(junior_terms) > 0
    
    def test_taxonomy_report(self):
        """Test generating taxonomy report"""
        text = """
        Led Python development and data analysis.
        Managed marketing campaigns and SEO optimization.
        Strong leadership and communication skills.
        """
        terms = extract_terms_from_text(text)
        contexts = analyze_term_contexts(terms, text)
        
        categorizer = TermCategorizer()
        categorizer.categorize_terms(terms, contexts)
        
        report = categorizer.generate_taxonomy_report()
        
        assert report['total_terms'] > 0
        assert 'by_domain' in report
        assert 'by_role' in report
        assert 'by_level' in report
        assert report['transferable_count'] >= 0
        assert report['industry_specific_count'] >= 0
    
    def test_empty_taxonomy_report(self):
        """Test taxonomy report with no terms"""
        categorizer = TermCategorizer()
        report = categorizer.generate_taxonomy_report()
        
        assert report['total_terms'] == 0
        assert report['transferable_count'] == 0


class TestDomainClassification:
    """Test domain classification logic"""
    
    def test_technical_domain_indicators(self):
        """Test detection of technical domain indicators"""
        technical_terms = [
            "software development",
            "code review",
            "api design",
            "cloud architecture",
        ]
        
        categorizer = TermCategorizer()
        
        for text in technical_terms:
            term = ExtractedTerm(text=text, context_window=text)
            categorized = categorizer._categorize_single_term(term, None)
            assert categorized.skill_domain == SkillDomain.TECHNICAL
    
    def test_business_domain_indicators(self):
        """Test detection of business domain indicators"""
        business_terms = [
            "strategic planning",
            "financial analysis",
            "stakeholder management",
        ]
        
        categorizer = TermCategorizer()
        
        for text in business_terms:
            term = ExtractedTerm(text=text, context_window=text)
            categorized = categorizer._categorize_single_term(term, None)
            assert categorized.skill_domain == SkillDomain.BUSINESS
    
    def test_analytical_domain_indicators(self):
        """Test detection of analytical domain indicators"""
        analytical_terms = [
            "data analysis",
            "statistical modeling",
            "metrics reporting",
        ]
        
        categorizer = TermCategorizer()
        
        for text in analytical_terms:
            term = ExtractedTerm(text=text, context_window=text)
            categorized = categorizer._categorize_single_term(term, None)
            assert categorized.skill_domain == SkillDomain.ANALYTICAL


class TestRoleClassification:
    """Test role classification logic"""
    
    def test_multiple_role_assignment(self):
        """Test that terms can belong to multiple roles"""
        # Python is relevant for both engineering and data science
        term = ExtractedTerm(text="python")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert len(categorized.role_categories) >= 1
        # Could be engineering, data science, or both
        assert any(role in {RoleCategory.ENGINEERING, RoleCategory.DATA_SCIENCE} 
                  for role in categorized.role_categories)
    
    def test_role_specific_skills(self):
        """Test role-specific skill classification"""
        role_skills = {
            "docker": RoleCategory.ENGINEERING,
            "tableau": RoleCategory.DATA_SCIENCE,
            "figma": RoleCategory.DESIGN,
            "google ads": RoleCategory.MARKETING,
            "salesforce": RoleCategory.SALES,
        }
        
        categorizer = TermCategorizer()
        
        for skill_text, expected_role in role_skills.items():
            term = ExtractedTerm(text=skill_text)
            categorized = categorizer._categorize_single_term(term, None)
            assert expected_role in categorized.role_categories


class TestSkillLevelInference:
    """Test skill level inference"""
    
    def test_level_from_explicit_indicators(self):
        """Test inferring level from explicit context indicators"""
        levels = {
            "Expert Python developer": "expert",
            "Senior software engineer": "senior",
            "Mid-level analyst": "mid",
            "Junior developer": "junior",
        }
        
        categorizer = TermCategorizer()
        
        for context_text, expected_level in levels.items():
            term = ExtractedTerm(text="developer")
            term_context = TermContext(term=term)
            term_context.term.context_window = context_text
            
            categorized = categorizer._categorize_single_term(term, term_context)
            assert categorized.skill_level == expected_level
    
    def test_level_from_action_verbs(self):
        """Test inferring level from action verb strength"""
        verb_levels = {
            ActionVerbStrength.STRONG: "senior",
            ActionVerbStrength.MODERATE: "mid",
            ActionVerbStrength.WEAK: "junior",
        }
        
        categorizer = TermCategorizer()
        
        for verb_strength, expected_level in verb_levels.items():
            term = ExtractedTerm(text="python")
            term_context = TermContext(
                term=term,
                action_verbs=[("test", verb_strength)]
            )
            term_context.term.context_window = "test context"
            
            categorized = categorizer._categorize_single_term(term, term_context)
            assert categorized.skill_level == expected_level


class TestConvenienceFunction:
    """Test convenience function"""
    
    def test_categorize_terms_function(self):
        """Test the convenience function"""
        text = "Led Python development and managed marketing campaigns"
        terms = extract_terms_from_text(text)
        contexts = analyze_term_contexts(terms, text)
        
        categorized = categorize_terms(terms, contexts)
        
        assert isinstance(categorized, dict)
        assert len(categorized) > 0
        assert "python" in categorized
        assert categorized["python"].skill_domain == SkillDomain.TECHNICAL
    
    def test_categorize_without_contexts(self):
        """Test categorization without context information"""
        text = "Python, Java, leadership, communication"
        terms = extract_terms_from_text(text)
        
        categorized = categorize_terms(terms, None)
        
        assert len(categorized) > 0
        assert all(term.context is None for term in categorized.values())


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_terms(self):
        """Test categorization with no terms"""
        categorizer = TermCategorizer()
        result = categorizer.categorize_terms({})
        
        assert result == {}
    
    def test_unknown_domain(self):
        """Test term with no clear domain"""
        term = ExtractedTerm(text="xyz123")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        # Should default to unknown
        assert categorized.skill_domain == SkillDomain.UNKNOWN
    
    def test_term_without_context(self):
        """Test categorization without context"""
        term = ExtractedTerm(text="python")
        
        categorizer = TermCategorizer()
        categorized = categorizer._categorize_single_term(term, None)
        
        assert categorized.skill_level is None  # Can't infer without context
    
    def test_comprehensive_categorization(self):
        """Test end-to-end categorization with real document"""
        text = """
        Senior Software Engineer
        
        Led development of Python applications using AWS.
        Managed data analysis projects with machine learning.
        Strong leadership and communication skills.
        Expert in agile methodologies and test-driven development.
        
        Marketing campaigns with SEO optimization.
        Financial analysis and budgeting experience.
        """
        
        # Extract terms
        terms = extract_terms_from_text(text)
        
        # Analyze contexts
        contexts = analyze_term_contexts(terms, text)
        
        # Categorize
        categorized = categorize_terms(terms, contexts)
        
        # Should have various domains
        categorizer = TermCategorizer()
        categorizer.categorized_terms = categorized
        
        assert len(categorizer.get_by_domain(SkillDomain.TECHNICAL)) > 0
        assert len(categorizer.get_by_domain(SkillDomain.INTERPERSONAL)) > 0
        
        # Should have various roles
        assert len(categorizer.get_by_role(RoleCategory.ENGINEERING)) > 0
        assert len(categorizer.get_by_role(RoleCategory.DATA_SCIENCE)) > 0
        
        # Should have skill levels
        assert len(categorizer.get_by_skill_level("senior")) > 0
        
        # Should identify transferable skills
        assert len(categorizer.get_transferable_skills()) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
