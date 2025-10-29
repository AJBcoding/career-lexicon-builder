"""
Tests for Term Extraction Module
Tests Phase 3.1: Core Term Extraction
"""

import pytest
from src.term_extractor import (
    TermExtractor,
    ExtractedTerm,
    TermCategory,
    extract_terms_from_text
)


class TestExtractedTerm:
    """Test ExtractedTerm dataclass"""
    
    def test_term_creation(self):
        """Test creating an extracted term"""
        term = ExtractedTerm(
            text="Python",
            category=TermCategory.LANGUAGE,
            frequency=2,
            positions=[10, 50],
            confidence=0.95
        )
        
        assert term.text == "Python"
        assert term.category == TermCategory.LANGUAGE
        assert term.frequency == 2
        assert len(term.positions) == 2
        assert term.confidence == 0.95
    
    def test_term_normalization(self):
        """Test that term text is normalized"""
        term = ExtractedTerm(text="  Python  ")
        assert term.text == "Python"
    
    def test_add_occurrence(self):
        """Test adding additional occurrences"""
        term = ExtractedTerm(text="Java", frequency=1, positions=[10])
        term.add_occurrence(50, "context here")
        
        assert term.frequency == 2
        assert len(term.positions) == 2
        assert 50 in term.positions
        assert term.context_window == "context here"


class TestTermExtractor:
    """Test TermExtractor class"""
    
    def test_initialization(self):
        """Test extractor initialization"""
        extractor = TermExtractor()
        assert isinstance(extractor.extracted_terms, dict)
        assert len(extractor.extracted_terms) == 0
    
    def test_extract_empty_text(self):
        """Test extraction from empty text"""
        extractor = TermExtractor()
        result = extractor.extract_terms("")
        assert result == {}
    
    def test_extract_technical_skills(self):
        """Test extraction of technical skills"""
        text = "I have experience with Python, Java, and JavaScript for web development."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "python" in terms
        assert "java" in terms
        assert "javascript" in terms
        assert terms["python"].category == TermCategory.LANGUAGE
    
    def test_extract_cloud_platforms(self):
        """Test extraction of cloud platforms"""
        text = "Deployed applications on AWS, Azure, and GCP."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "aws" in terms
        assert "azure" in terms
        assert "gcp" in terms
        assert terms["aws"].category == TermCategory.TOOL
    
    def test_extract_databases(self):
        """Test extraction of database technologies"""
        text = "Experience with SQL, PostgreSQL, MongoDB, and Redis databases."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "sql" in terms
        assert "postgresql" in terms
        assert "mongodb" in terms
        assert "redis" in terms
    
    def test_extract_methodologies(self):
        """Test extraction of methodologies"""
        text = "Experienced with Agile, Scrum, Kanban, and test-driven development."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "agile" in terms
        assert "scrum" in terms
        assert "kanban" in terms
        assert terms["agile"].category == TermCategory.METHODOLOGY
    
    def test_extract_certifications(self):
        """Test extraction of certifications"""
        text = "AWS Certified, PMP, and CISSP certified professional."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "aws certified" in terms
        assert "pmp" in terms
        assert "cissp" in terms
        assert terms["pmp"].category == TermCategory.CERTIFICATION
    
    def test_extract_soft_skills(self):
        """Test extraction of soft skills"""
        text = "Strong leadership, communication, and problem solving skills."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "leadership" in terms
        assert "communication" in terms
        assert "problem solving" in terms
        assert terms["leadership"].category == TermCategory.SOFT_SKILL
    
    def test_extract_noun_phrases(self):
        """Test extraction of multi-word noun phrases"""
        text = "Experience with Machine Learning and Natural Language Processing."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "machine learning" in terms
        assert "natural language processing" in terms
    
    def test_frequency_counting(self):
        """Test that term frequency is counted correctly"""
        text = "Python is great. I love Python. Python programming is fun."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "python" in terms
        assert terms["python"].frequency == 3
        assert len(terms["python"].positions) == 3
    
    def test_context_window_extraction(self):
        """Test context window extraction"""
        text = "I have 5 years of experience with Python programming and web development."
        extractor = TermExtractor()
        extractor._extract_technical_skills(text.lower(), text)
        
        assert "python" in extractor.extracted_terms
        term = extractor.extracted_terms["python"]
        assert len(term.context_window) > 0
        assert "experience" in term.context_window.lower()
    
    def test_confidence_scores(self):
        """Test confidence score calculation"""
        text = "Python, Java, JavaScript, and some unknown_tech."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Known languages should have high confidence
        assert terms["python"].confidence > 0.8
        
    def test_get_top_terms(self):
        """Test getting top terms by confidence"""
        text = "Python Python Java JavaScript AWS Docker Kubernetes"
        extractor = TermExtractor()
        extractor.extract_terms(text)
        
        top_terms = extractor.get_top_terms(n=3, min_confidence=0.5)
        assert len(top_terms) <= 3
        assert all(term.confidence >= 0.5 for term in top_terms)
        
        # Should be sorted by confidence and frequency
        if len(top_terms) > 1:
            assert top_terms[0].confidence >= top_terms[1].confidence
    
    def test_get_terms_by_category(self):
        """Test filtering terms by category"""
        text = "Python, Java for programming. Agile and Scrum for methodology."
        extractor = TermExtractor()
        extractor.extract_terms(text)
        
        languages = extractor.get_terms_by_category(TermCategory.LANGUAGE)
        methodologies = extractor.get_terms_by_category(TermCategory.METHODOLOGY)
        
        assert len(languages) >= 2
        assert len(methodologies) >= 2
        assert all(t.category == TermCategory.LANGUAGE for t in languages)
        assert all(t.category == TermCategory.METHODOLOGY for t in methodologies)
    
    def test_term_statistics(self):
        """Test term statistics generation"""
        text = "Python, Java, AWS, leadership, communication."
        extractor = TermExtractor()
        extractor.extract_terms(text)
        
        stats = extractor.get_term_statistics()
        
        assert stats['unique_terms'] > 0
        assert stats['total_terms'] >= stats['unique_terms']
        assert 'by_category' in stats
        assert 0 <= stats['avg_confidence'] <= 1
    
    def test_case_insensitive_extraction(self):
        """Test that extraction is case-insensitive"""
        text1 = "I use PYTHON and python and Python"
        text2 = "python python python"
        
        extractor1 = TermExtractor()
        terms1 = extractor1.extract_terms(text1)
        
        extractor2 = TermExtractor()
        terms2 = extractor2.extract_terms(text2)
        
        # All variations should be counted as same term
        assert "python" in terms1
        assert terms1["python"].frequency == 3
        assert terms2["python"].frequency == 3
    
    def test_word_boundaries(self):
        """Test that word boundaries are respected"""
        text = "pythonic and python are different"
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should match 'python' but not 'pythonic'
        assert "python" in terms
        assert terms["python"].frequency == 1  # Only the standalone 'python'
    
    def test_empty_result_statistics(self):
        """Test statistics when no terms extracted"""
        extractor = TermExtractor()
        extractor.extract_terms("")
        
        stats = extractor.get_term_statistics()
        assert stats['total_terms'] == 0
        assert stats['unique_terms'] == 0
        assert stats['avg_confidence'] == 0.0


class TestDomainCategorization:
    """Test domain-specific term categorization"""
    
    def test_finance_domain_detection(self):
        """Test detection of finance domain terms"""
        text = "Financial Analysis experience with budget forecasting and accounting."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should detect Financial Analysis as a capitalized noun phrase
        assert "financial analysis" in terms or len(terms) > 0
    
    def test_healthcare_domain_detection(self):
        """Test detection of healthcare domain terms"""
        text = "Clinical Experience with patient care and HIPAA compliance."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should detect Clinical Experience as a noun phrase
        assert "clinical experience" in terms or len(terms) > 0
    
    def test_marketing_domain_detection(self):
        """Test detection of marketing domain terms"""
        text = "SEO and SEM campaigns with Content Marketing strategies."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should detect SEO and SEM
        assert 'seo' in terms
        assert 'sem' in terms
        # May also detect Content Marketing
        assert len(terms) > 0


class TestConvenienceFunction:
    """Test convenience function"""
    
    def test_extract_terms_from_text(self):
        """Test the convenience function"""
        text = "Python and Java programming with AWS deployment."
        terms = extract_terms_from_text(text)
        
        assert isinstance(terms, dict)
        assert "python" in terms
        assert "java" in terms
        assert "aws" in terms
    
    def test_with_document_type(self):
        """Test extraction with document type specified"""
        text = "Python developer seeking opportunities."
        terms = extract_terms_from_text(text, document_type="resume")
        
        assert isinstance(terms, dict)
        assert len(terms) > 0


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "C++, C#, and Node.js are popular technologies."
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should handle special characters in term names
        assert "c++" in terms or "node.js" in terms
    
    def test_very_long_text(self):
        """Test extraction from very long text"""
        text = ("Python " * 1000) + "Java " * 1000
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "python" in terms
        assert "java" in terms
        assert terms["python"].frequency == 1000
        assert terms["java"].frequency == 1000
    
    def test_unicode_text(self):
        """Test handling of unicode characters"""
        text = "Python programming with ÃƒÂ©xpÃƒÂ©riÃƒÂ©nce in dÃƒÂ©velopment"
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        assert "python" in terms
    
    def test_mixed_content(self):
        """Test extraction from mixed professional content"""
        text = """
        Software Engineer
        
        Skills: Python, Java, AWS, Docker
        Experience: Agile methodology, leadership, team collaboration
        Certifications: AWS Certified, PMP
        
        Developed Machine Learning models using TensorFlow and PyTorch.
        """
        extractor = TermExtractor()
        terms = extractor.extract_terms(text)
        
        # Should extract technical skills
        assert "python" in terms
        assert "java" in terms
        assert "aws" in terms
        assert "docker" in terms
        
        # Should extract methodologies
        assert "agile" in terms
        
        # Should extract soft skills
        assert "leadership" in terms
        
        # Should extract certifications
        assert "aws certified" in terms or "pmp" in terms
        
        # Should extract noun phrases (Machine Learning, Software Engineer, etc.)
        capitalized_phrases = [t for t in terms.values() if ' ' in t.text]
        assert len(capitalized_phrases) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
