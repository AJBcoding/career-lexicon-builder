"""
Tests for Context Analysis Module
Tests Phase 3.2: Context Analysis
"""

import pytest
from src.term_extractor import ExtractedTerm, TermCategory, extract_terms_from_text
from src.context_analyzer import (
    ContextAnalyzer,
    TermContext,
    ActionVerbStrength,
    analyze_term_contexts
)


class TestTermContext:
    """Test TermContext dataclass"""
    
    def test_context_creation(self):
        """Test creating a term context"""
        term = ExtractedTerm(text="Python", category=TermCategory.LANGUAGE)
        context = TermContext(
            term=term,
            action_verbs=[("developed", ActionVerbStrength.STRONG)],
            quantifiers=["50%", "10k"],
            prominence_score=0.85
        )
        
        assert context.term == term
        assert len(context.action_verbs) == 1
        assert len(context.quantifiers) == 2
        assert context.prominence_score == 0.85
    
    def test_get_strongest_verb(self):
        """Test getting the strongest action verb"""
        term = ExtractedTerm(text="Java")
        context = TermContext(
            term=term,
            action_verbs=[
                ("supported", ActionVerbStrength.WEAK),
                ("developed", ActionVerbStrength.STRONG),
                ("managed", ActionVerbStrength.MODERATE),
            ]
        )
        
        strongest = context.get_strongest_verb()
        assert strongest is not None
        assert strongest[0] == "developed"
        assert strongest[1] == ActionVerbStrength.STRONG
    
    def test_get_strongest_verb_empty(self):
        """Test getting strongest verb when none exist"""
        term = ExtractedTerm(text="Python")
        context = TermContext(term=term)
        
        assert context.get_strongest_verb() is None
    
    def test_has_quantifiable_impact(self):
        """Test checking for quantifiable impact"""
        term = ExtractedTerm(text="AWS")
        
        context_with = TermContext(term=term, quantifiers=["50%", "2x"])
        context_without = TermContext(term=term, quantifiers=[])
        
        assert context_with.has_quantifiable_impact()
        assert not context_without.has_quantifiable_impact()


class TestContextAnalyzer:
    """Test ContextAnalyzer class"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = ContextAnalyzer()
        assert isinstance(analyzer.analyzed_contexts, dict)
        assert len(analyzer.analyzed_contexts) == 0
    
    def test_extract_strong_verbs(self):
        """Test extraction of strong action verbs"""
        text = "Led the development of Python applications."
        analyzer = ContextAnalyzer()
        
        verbs = analyzer._extract_action_verbs(text)
        
        assert len(verbs) > 0
        assert any(verb == "led" and strength == ActionVerbStrength.STRONG 
                  for verb, strength in verbs)
    
    def test_extract_moderate_verbs(self):
        """Test extraction of moderate action verbs"""
        text = "Managed Python projects and implemented solutions."
        analyzer = ContextAnalyzer()
        
        verbs = analyzer._extract_action_verbs(text)
        
        assert len(verbs) > 0
        assert any(strength == ActionVerbStrength.MODERATE for _, strength in verbs)
    
    def test_extract_weak_verbs(self):
        """Test extraction of weak action verbs"""
        text = "Assisted with Python development and supported the team."
        analyzer = ContextAnalyzer()
        
        verbs = analyzer._extract_action_verbs(text)
        
        assert len(verbs) > 0
        assert any(strength == ActionVerbStrength.WEAK for _, strength in verbs)
    
    def test_extract_passive_patterns(self):
        """Test extraction of passive voice patterns"""
        text = "Was responsible for Python development."
        analyzer = ContextAnalyzer()
        
        verbs = analyzer._extract_action_verbs(text)
        
        assert len(verbs) > 0
        assert any(strength == ActionVerbStrength.PASSIVE for _, strength in verbs)
    
    def test_extract_quantifiers(self):
        """Test extraction of quantifiers"""
        text = "Improved performance by 50% and reduced costs by $10k, serving 100+ users."
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        assert len(quants) >= 3
        assert "50%" in quants
        assert any('10' in q for q in quants)  # $10k
        assert any('100' in q for q in quants)  # 100+
    
    def test_extract_multipliers(self):
        """Test extraction of multiplier quantifiers"""
        text = "Increased efficiency 10x and scaled traffic 5x."
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        assert "10x" in quants
        assert "5x" in quants
    
    def test_analyze_single_term(self):
        """Test analyzing context for a single term"""
        text = "Led the development of Python applications, improving performance by 50%."
        term = ExtractedTerm(
            text="Python",
            category=TermCategory.LANGUAGE,
            positions=[text.lower().index("python")]
        )
        
        analyzer = ContextAnalyzer()
        context = analyzer._analyze_single_term(term, text)
        
        assert context.term == term
        assert len(context.action_verbs) > 0
        assert len(context.quantifiers) > 0
        assert context.prominence_score > 0
    
    def test_analyze_term_contexts(self):
        """Test analyzing contexts for multiple terms"""
        text = "Developed Python and Java applications using AWS, improving performance by 50%."
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        contexts = analyzer.analyze_term_contexts(terms, text)
        
        assert len(contexts) > 0
        assert "python" in contexts
        assert "java" in contexts
        assert contexts["python"].prominence_score > 0
    
    def test_prominence_calculation(self):
        """Test prominence score calculation"""
        text = "Python is great. I use Python daily. Python development is fun. " * 10
        term = ExtractedTerm(
            text="Python",
            category=TermCategory.LANGUAGE,
            frequency=30,
            positions=[0, 20, 40],  # Early positions
            confidence=0.95
        )
        
        analyzer = ContextAnalyzer()
        prominence = analyzer._calculate_prominence(term, text)
        
        # Should be high due to:
        # - Early positions
        # - High frequency
        # - High confidence
        assert prominence > 0.5
    
    def test_get_terms_with_strong_verbs(self):
        """Test filtering terms with strong verbs"""
        text = """
        Led Python development and architected AWS infrastructure.
        Assisted with Java projects.
        """
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        analyzer.analyze_term_contexts(terms, text)
        
        strong_verb_terms = analyzer.get_terms_with_strong_verbs()
        
        # Python and AWS should have strong verbs (led, architected)
        assert len(strong_verb_terms) > 0
        assert any(ctx.term.text.lower() == "python" for ctx in strong_verb_terms)
    
    def test_get_terms_with_quantifiable_impact(self):
        """Test filtering terms with quantifiable impact"""
        text = """
        Python development improved performance by 50%.
        Java programming reduced bugs by 30%.
        AWS deployment saved $100k annually.
        """
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        analyzer.analyze_term_contexts(terms, text)
        
        quantified_terms = analyzer.get_terms_with_quantifiable_impact()
        
        # All three should have quantifiers
        assert len(quantified_terms) >= 3
    
    def test_get_top_prominent_terms(self):
        """Test getting top prominent terms"""
        text = """
        Python Python Python at the beginning.
        Later comes Java.
        And finally AWS at the end.
        """
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        analyzer.analyze_term_contexts(terms, text)
        
        top_terms = analyzer.get_top_prominent_terms(n=2)
        
        assert len(top_terms) <= 2
        # Python should be most prominent (early + frequent)
        assert top_terms[0].term.text.lower() == "python"
    
    def test_context_report(self):
        """Test generating context analysis report"""
        text = """
        Led Python development, improving performance by 50%.
        Managed Java projects, reducing costs by $20k.
        Assisted with AWS deployment.
        """
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        analyzer.analyze_term_contexts(terms, text)
        
        report = analyzer.generate_context_report()
        
        assert report['total_terms'] > 0
        assert report['with_strong_verbs'] > 0
        assert report['with_quantifiers'] > 0
        assert 0 <= report['avg_prominence'] <= 1
        assert 'verb_distribution' in report
    
    def test_empty_report(self):
        """Test report generation with no terms"""
        analyzer = ContextAnalyzer()
        report = analyzer.generate_context_report()
        
        assert report['total_terms'] == 0
        assert report['with_strong_verbs'] == 0
        assert report['with_quantifiers'] == 0
        assert report['avg_prominence'] == 0.0


class TestVerbCategorization:
    """Test verb strength categorization"""
    
    def test_strong_verbs_recognized(self):
        """Test that strong verbs are properly categorized"""
        strong_examples = [
            "Led the team",
            "Developed the platform",
            "Architected the system",
            "Launched the product",
            "Pioneered the approach",
        ]
        
        analyzer = ContextAnalyzer()
        
        for text in strong_examples:
            verbs = analyzer._extract_action_verbs(text)
            assert any(s == ActionVerbStrength.STRONG for _, s in verbs)
    
    def test_moderate_verbs_recognized(self):
        """Test that moderate verbs are properly categorized"""
        moderate_examples = [
            "Managed the project",
            "Implemented the solution",
            "Coordinated the effort",
            "Improved the process",
        ]
        
        analyzer = ContextAnalyzer()
        
        for text in moderate_examples:
            verbs = analyzer._extract_action_verbs(text)
            assert any(s == ActionVerbStrength.MODERATE for _, s in verbs)
    
    def test_weak_verbs_recognized(self):
        """Test that weak verbs are properly categorized"""
        weak_examples = [
            "Assisted with development",
            "Supported the team",
            "Helped with testing",
            "Participated in planning",
        ]
        
        analyzer = ContextAnalyzer()
        
        for text in weak_examples:
            verbs = analyzer._extract_action_verbs(text)
            assert any(s == ActionVerbStrength.WEAK for _, s in verbs)
    
    def test_verb_strength_ordering(self):
        """Test that verb strengths are properly ordered"""
        text = "Assisted with development, managed projects, and led the team."
        term = ExtractedTerm(text="Python", positions=[0])
        
        analyzer = ContextAnalyzer()
        context = analyzer._analyze_single_term(term, text)
        
        strongest = context.get_strongest_verb()
        assert strongest is not None
        assert strongest[1] == ActionVerbStrength.STRONG  # "led" should be strongest


class TestQuantifierExtraction:
    """Test quantifier extraction patterns"""
    
    def test_percentage_extraction(self):
        """Test extraction of percentages"""
        text = "Improved by 50%, reduced by 25%, increased by 100%"
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        assert "50%" in quants
        assert "25%" in quants
        assert "100%" in quants
    
    def test_large_number_extraction(self):
        """Test extraction of large numbers with suffixes"""
        text = "Served 10k users, processed 5M records, managed $2B budget"
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        assert any('10k' in q.lower() or '10' in q for q in quants)
        assert any('5m' in q.lower() or '5' in q for q in quants)
        assert any('2b' in q.lower() or '$2' in q for q in quants)
    
    def test_plus_suffix(self):
        """Test extraction of numbers with + suffix"""
        text = "100+ users, 50+ projects, 1000+ lines of code"
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        # Should extract numbers (may or may not include + depending on regex)
        assert any('100' in q for q in quants)
        assert any('50' in q for q in quants)
        assert any('1000' in q for q in quants)
    
    def test_multiplier_extraction(self):
        """Test extraction of multipliers"""
        text = "10x faster, 5x improvement, 2x growth"
        analyzer = ContextAnalyzer()
        
        quants = analyzer._extract_quantifiers(text)
        
        assert "10x" in quants
        assert "5x" in quants
        assert "2x" in quants


class TestProminenceScoring:
    """Test prominence score calculation"""
    
    def test_early_position_bonus(self):
        """Test that early positions score higher"""
        text = "Python " * 100  # Long text
        
        early_term = ExtractedTerm(
            text="Python",
            frequency=1,
            positions=[10],  # Early position
            confidence=0.9
        )
        
        late_term = ExtractedTerm(
            text="Java",
            frequency=1,
            positions=[500],  # Late position
            confidence=0.9
        )
        
        analyzer = ContextAnalyzer()
        early_score = analyzer._calculate_prominence(early_term, text)
        late_score = analyzer._calculate_prominence(late_term, text)
        
        assert early_score > late_score
    
    def test_frequency_bonus(self):
        """Test that higher frequency increases prominence"""
        text = "Python " * 100
        
        frequent_term = ExtractedTerm(
            text="Python",
            frequency=10,
            positions=[10] * 10,
            confidence=0.9
        )
        
        rare_term = ExtractedTerm(
            text="Java",
            frequency=1,
            positions=[10],
            confidence=0.9
        )
        
        analyzer = ContextAnalyzer()
        frequent_score = analyzer._calculate_prominence(frequent_term, text)
        rare_score = analyzer._calculate_prominence(rare_term, text)
        
        assert frequent_score > rare_score
    
    def test_confidence_bonus(self):
        """Test that confidence affects prominence"""
        text = "Python " * 100
        
        high_conf_term = ExtractedTerm(
            text="Python",
            frequency=5,
            positions=[100],
            confidence=0.95
        )
        
        low_conf_term = ExtractedTerm(
            text="Java",
            frequency=5,
            positions=[100],
            confidence=0.3
        )
        
        analyzer = ContextAnalyzer()
        high_score = analyzer._calculate_prominence(high_conf_term, text)
        low_score = analyzer._calculate_prominence(low_conf_term, text)
        
        assert high_score > low_score


class TestConvenienceFunction:
    """Test convenience function"""
    
    def test_analyze_term_contexts_function(self):
        """Test the convenience function"""
        text = "Led Python development, improving performance by 50%."
        terms = extract_terms_from_text(text)
        
        contexts = analyze_term_contexts(terms, text)
        
        assert isinstance(contexts, dict)
        assert len(contexts) > 0
        assert "python" in contexts
        assert contexts["python"].prominence_score > 0


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_text_analysis(self):
        """Test analysis with empty text"""
        analyzer = ContextAnalyzer()
        contexts = analyzer.analyze_term_contexts({}, "")
        
        assert contexts == {}
    
    def test_term_without_positions(self):
        """Test term with no position information"""
        term = ExtractedTerm(text="Python", positions=[])
        text = "Some text"
        
        analyzer = ContextAnalyzer()
        prominence = analyzer._calculate_prominence(term, text)
        
        assert prominence == 0.0
    
    def test_very_long_context(self):
        """Test analysis with very long text"""
        text = ("Python development " * 1000) + "Led projects " * 1000
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        contexts = analyzer.analyze_term_contexts(terms, text)
        
        assert len(contexts) > 0
        assert "python" in contexts
    
    def test_unicode_context(self):
        """Test analysis with unicode characters"""
        text = "Developed Python applications with expertise"
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        contexts = analyzer.analyze_term_contexts(terms, text)
        
        assert "python" in contexts
    
    def test_mixed_verb_strengths(self):
        """Test term with multiple verb strengths"""
        text = """
        Led Python development.
        Managed Python projects.
        Assisted with Python deployment.
        """
        terms = extract_terms_from_text(text)
        
        analyzer = ContextAnalyzer()
        contexts = analyzer.analyze_term_contexts(terms, text)
        
        python_ctx = contexts["python"]
        # Should capture all verb strengths
        strengths = {s for _, s in python_ctx.action_verbs}
        assert ActionVerbStrength.STRONG in strengths
        assert ActionVerbStrength.MODERATE in strengths
        assert ActionVerbStrength.WEAK in strengths


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
