"""
Tests for Lexicon Builder Module
Tests Phase 4.1: Lexicon Building
"""

import pytest
from datetime import date, timedelta
from collections import Counter

from src.lexicon_builder import (
    DocumentMetadata,
    SkillOccurrence,
    AggregatedSkill,
    SkillLexicon,
    build_lexicon_from_documents
)
from src.term_extractor import ExtractedTerm, TermCategory
from src.context_analyzer import TermContext, ActionVerbStrength
from src.term_categorizer import CategorizedTerm, SkillDomain, RoleCategory


class TestDocumentMetadata:
    """Test DocumentMetadata dataclass"""
    
    def test_metadata_creation(self):
        """Test creating document metadata"""
        metadata = DocumentMetadata(
            filename="resume_2024.pdf",
            document_type="resume",
            date=date(2024, 1, 15),
            target_position="Software Engineer"
        )
        
        assert metadata.filename == "resume_2024.pdf"
        assert metadata.document_type == "resume"
        assert metadata.date == date(2024, 1, 15)
        assert metadata.target_position == "Software Engineer"
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary"""
        metadata = DocumentMetadata(
            filename="resume.pdf",
            document_type="resume",
            date=date(2024, 1, 1)
        )
        
        data = metadata.to_dict()
        assert data['filename'] == "resume.pdf"
        assert data['date'] == "2024-01-01"
    
    def test_metadata_from_dict(self):
        """Test creating metadata from dictionary"""
        data = {
            'filename': "resume.pdf",
            'document_type': "resume",
            'date': "2024-01-01",
            'target_position': None,
            'target_organization': None
        }
        
        metadata = DocumentMetadata.from_dict(data)
        assert metadata.filename == "resume.pdf"
        assert metadata.date == date(2024, 1, 1)


class TestSkillOccurrence:
    """Test SkillOccurrence dataclass"""
    
    def test_occurrence_creation(self):
        """Test creating a skill occurrence"""
        metadata = DocumentMetadata("resume.pdf", "resume")
        
        occurrence = SkillOccurrence(
            document=metadata,
            frequency=3,
            prominence_score=0.75,
            action_verbs=[("developed", "strong")],
            quantifiers=["30%", "5M+"]
        )
        
        assert occurrence.frequency == 3
        assert occurrence.prominence_score == 0.75
        assert len(occurrence.action_verbs) == 1
        assert len(occurrence.quantifiers) == 2


class TestAggregatedSkill:
    """Test AggregatedSkill dataclass"""
    
    def test_skill_creation(self):
        """Test creating an aggregated skill"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        assert skill.skill_name == "python"
        assert skill.total_documents == 0
        assert skill.total_occurrences == 0
    
    def test_add_occurrence(self):
        """Test adding occurrences to skill"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        metadata = DocumentMetadata("resume.pdf", "resume", date=date(2024, 1, 1))
        occurrence = SkillOccurrence(
            document=metadata,
            frequency=3,
            prominence_score=0.8,
            action_verbs=[("developed", "strong")],
            quantifiers=["50%"]
        )
        
        skill.add_occurrence(occurrence)
        
        assert skill.total_documents == 1
        assert skill.total_occurrences == 3
        assert skill.first_used == date(2024, 1, 1)
        assert skill.last_used == date(2024, 1, 1)
        assert "developed" in skill.all_action_verbs
        assert "50%" in skill.all_quantifiers
    
    def test_recency_score(self):
        """Test recency score calculation"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        # Recent usage (today)
        today = date.today()
        skill.last_used = today
        score_today = skill.get_recency_score(reference_date=today)
        assert score_today == 1.0
        
        # One year ago
        one_year_ago = today - timedelta(days=365)
        skill.last_used = one_year_ago
        score_year = skill.get_recency_score(reference_date=today)
        assert 0.4 < score_year < 0.6  # Should be around 0.5
        
        # Two years ago
        two_years_ago = today - timedelta(days=730)
        skill.last_used = two_years_ago
        score_two_years = skill.get_recency_score(reference_date=today)
        assert score_two_years < score_year  # Should decay
    
    def test_frequency_score(self):
        """Test frequency score calculation"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        # Add occurrences
        metadata = DocumentMetadata("doc.pdf", "resume")
        for i in range(5):
            occurrence = SkillOccurrence(
                document=metadata,
                frequency=1,
                prominence_score=0.5,
                action_verbs=[],
                quantifiers=[]
            )
            skill.add_occurrence(occurrence)
        
        score = skill.get_frequency_score()
        assert score == 0.5  # 5 documents / 10 max = 0.5
    
    def test_combined_score(self):
        """Test combined score calculation"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        today = date.today()
        metadata = DocumentMetadata("doc.pdf", "resume", date=today)
        
        occurrence = SkillOccurrence(
            document=metadata,
            frequency=1,
            prominence_score=0.9,
            action_verbs=[],
            quantifiers=[]
        )
        skill.add_occurrence(occurrence)
        
        score = skill.get_combined_score(reference_date=today)
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high with recent, prominent usage
    
    def test_get_strongest_verb(self):
        """Test getting strongest action verb"""
        skill = AggregatedSkill(
            skill_name="python",
            category=TermCategory.LANGUAGE,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        skill.all_action_verbs = Counter({
            'developed': 5,
            'managed': 2,
            'assisted': 1
        })
        
        strongest = skill.get_strongest_verb()
        assert strongest == 'developed'


class TestSkillLexicon:
    """Test SkillLexicon class"""
    
    def test_lexicon_creation(self):
        """Test creating an empty lexicon"""
        lexicon = SkillLexicon()
        
        assert len(lexicon.skills) == 0
        assert len(lexicon.documents) == 0
        assert lexicon.build_date is not None
    
    def test_add_document_analysis(self):
        """Test adding document analysis to lexicon"""
        lexicon = SkillLexicon()
        
        # Create sample data
        metadata = DocumentMetadata(
            "resume.pdf",
            "resume",
            date=date(2024, 1, 1)
        )
        
        # Sample term
        term = ExtractedTerm(
            text="Python",
            category=TermCategory.LANGUAGE,
            frequency=3,
            positions=[10, 50, 100]
        )
        
        # Sample context
        context = TermContext(term=term)
        context.prominence_score = 0.8
        context.action_verbs = [("developed", ActionVerbStrength.STRONG)]
        context.quantifiers = ["50%"]
        
        # Sample categorized term
        cat_term = CategorizedTerm(
            term=term,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        categorized = {"python": cat_term}
        contexts = {"python": context}
        
        lexicon.add_document_analysis(metadata, categorized, contexts)
        
        assert len(lexicon.documents) == 1
        assert "python" in lexicon.skills
        assert lexicon.skills["python"].total_documents == 1
    
    def test_get_top_skills_by_combined(self):
        """Test getting top skills by combined score"""
        lexicon = self._create_sample_lexicon()
        
        top = lexicon.get_top_skills(n=3, by='combined')
        
        assert len(top) <= 3
        assert all(isinstance(s, AggregatedSkill) for s in top)
    
    def test_get_top_skills_by_recency(self):
        """Test getting top skills by recency"""
        lexicon = self._create_sample_lexicon()
        
        top = lexicon.get_top_skills(n=3, by='recency')
        
        assert len(top) <= 3
        # Should be sorted by recency
        if len(top) > 1:
            assert (top[0].get_recency_score() >= 
                   top[1].get_recency_score())
    
    def test_get_skills_by_domain(self):
        """Test filtering skills by domain"""
        lexicon = self._create_sample_lexicon()
        
        technical = lexicon.get_skills_by_domain(SkillDomain.TECHNICAL)
        
        assert all(s.skill_domain == SkillDomain.TECHNICAL for s in technical)
    
    def test_get_skills_by_role(self):
        """Test filtering skills by role category"""
        lexicon = self._create_sample_lexicon()
        
        engineering = lexicon.get_skills_by_role(RoleCategory.ENGINEERING)
        
        assert all(
            RoleCategory.ENGINEERING in s.role_categories 
            for s in engineering
        )
    
    def test_get_transferable_skills(self):
        """Test getting transferable skills"""
        lexicon = self._create_sample_lexicon()
        
        transferable = lexicon.get_transferable_skills()
        
        assert all(s.is_transferable for s in transferable)
    
    def test_get_recent_skills(self):
        """Test getting recently used skills"""
        lexicon = self._create_sample_lexicon()
        
        recent = lexicon.get_recent_skills(days=365)
        
        today = date.today()
        cutoff = date(today.year - 1, today.month, today.day)
        
        assert all(
            s.last_used and s.last_used >= cutoff
            for s in recent
        )
    
    def test_generate_skill_profile(self):
        """Test generating skill profile summary"""
        lexicon = self._create_sample_lexicon()
        
        profile = lexicon.generate_skill_profile()
        
        assert 'build_date' in profile
        assert 'total_documents_analyzed' in profile
        assert 'total_unique_skills' in profile
        assert 'skills_by_domain' in profile
        assert 'skills_by_role' in profile
        assert 'transferable_skills_count' in profile
        assert 'top_skills_combined' in profile
    
    def test_multiple_documents_same_skill(self):
        """Test aggregating same skill across documents"""
        lexicon = SkillLexicon()
        
        # Add skill from first document
        metadata1 = DocumentMetadata("resume1.pdf", "resume", date=date(2024, 1, 1))
        term1 = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=2)
        context1 = TermContext(term=term1)
        context1.prominence_score = 0.7
        cat_term1 = CategorizedTerm(
            term=term1,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        lexicon.add_document_analysis(
            metadata1,
            {"python": cat_term1},
            {"python": context1}
        )
        
        # Add same skill from second document
        metadata2 = DocumentMetadata("resume2.pdf", "resume", date=date(2024, 6, 1))
        term2 = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=3)
        context2 = TermContext(term=term2)
        context2.prominence_score = 0.9
        cat_term2 = CategorizedTerm(
            term=term2,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        lexicon.add_document_analysis(
            metadata2,
            {"python": cat_term2},
            {"python": context2}
        )
        
        # Check aggregation
        assert "python" in lexicon.skills
        skill = lexicon.skills["python"]
        assert skill.total_documents == 2
        assert skill.total_occurrences == 5  # 2 + 3
        assert skill.first_used == date(2024, 1, 1)
        assert skill.last_used == date(2024, 6, 1)
    
    def _create_sample_lexicon(self) -> SkillLexicon:
        """Helper to create a sample lexicon for testing"""
        lexicon = SkillLexicon()
        
        today = date.today()
        
        # Add Python skill
        metadata1 = DocumentMetadata("resume.pdf", "resume", date=today)
        term1 = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=3)
        context1 = TermContext(term=term1)
        context1.prominence_score = 0.9
        cat_term1 = CategorizedTerm(
            term=term1,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        # Add Leadership skill
        term2 = ExtractedTerm("leadership", TermCategory.SOFT_SKILL, frequency=2)
        context2 = TermContext(term=term2)
        context2.prominence_score = 0.7
        cat_term2 = CategorizedTerm(
            term=term2,
            skill_domain=SkillDomain.INTERPERSONAL,
            role_categories={RoleCategory.GENERAL}
        )
        cat_term2._is_transferable = True
        
        lexicon.add_document_analysis(
            metadata1,
            {"python": cat_term1, "leadership": cat_term2},
            {"python": context1, "leadership": context2}
        )
        
        return lexicon


class TestConvenienceFunction:
    """Test convenience functions"""
    
    def test_build_lexicon_from_documents(self):
        """Test building lexicon from multiple documents"""
        # Prepare documents
        today = date.today()
        
        metadata1 = DocumentMetadata("resume.pdf", "resume", date=today)
        term1 = ExtractedTerm("Python", TermCategory.LANGUAGE, frequency=2)
        context1 = TermContext(term=term1)
        context1.prominence_score = 0.8
        cat_term1 = CategorizedTerm(
            term=term1,
            skill_domain=SkillDomain.TECHNICAL,
            role_categories={RoleCategory.ENGINEERING}
        )
        
        documents = [
            (metadata1, {"python": cat_term1}, {"python": context1})
        ]
        
        lexicon = build_lexicon_from_documents(documents)
        
        assert len(lexicon.documents) == 1
        assert "python" in lexicon.skills


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_lexicon_profile(self):
        """Test generating profile from empty lexicon"""
        lexicon = SkillLexicon()
        profile = lexicon.generate_skill_profile()
        
        assert profile['total_documents_analyzed'] == 0
        assert profile['total_unique_skills'] == 0
    
    def test_skill_with_no_dates(self):
        """Test skill without date information"""
        lexicon = SkillLexicon()
        
        metadata = DocumentMetadata("resume.pdf", "resume")  # No date
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
        
        skill = lexicon.skills["python"]
        assert skill.get_recency_score() == 0.0  # No date = 0 recency
    
    def test_large_lexicon_performance(self):
        """Test performance with many skills"""
        lexicon = SkillLexicon()
        
        today = date.today()
        metadata = DocumentMetadata("resume.pdf", "resume", date=today)
        
        # Add 100 skills
        categorized = {}
        contexts = {}
        
        for i in range(100):
            skill_name = f"skill_{i}"
            term = ExtractedTerm(skill_name, TermCategory.TOOL, frequency=1)
            context = TermContext(term=term)
            context.prominence_score = 0.5
            cat_term = CategorizedTerm(
                term=term,
                skill_domain=SkillDomain.TECHNICAL,
                role_categories={RoleCategory.ENGINEERING}
            )
            
            categorized[skill_name] = cat_term
            contexts[skill_name] = context
        
        lexicon.add_document_analysis(metadata, categorized, contexts)
        
        assert len(lexicon.skills) == 100
        
        # Should still be able to get top skills quickly
        top = lexicon.get_top_skills(20)
        assert len(top) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
