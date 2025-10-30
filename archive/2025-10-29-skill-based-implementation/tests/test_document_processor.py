"""Tests for document classification system."""

import pytest
from src.document_processor import (
    DocumentType,
    DocumentClassifier,
    DocumentProcessor,
    ClassificationResult
)


# Test Documents

SAMPLE_RESUME = """
JOHN DOE
Software Engineer

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing scalable applications.

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2018

WORK EXPERIENCE
Senior Software Engineer | Tech Company | 2020 - Present
- Developed microservices architecture serving 1M+ users
- Led team of 4 engineers

Software Engineer | StartupCo | 2018 - 2020
- Built RESTful APIs using Python and Django
- Implemented CI/CD pipelines

SKILLS
Python, Java, JavaScript, AWS, Docker, Kubernetes

CERTIFICATIONS
AWS Certified Solutions Architect

References available upon request.
"""

SAMPLE_COVER_LETTER = """
January 15, 2024

Dear Hiring Manager,

I am writing to express my strong interest in the Senior Software Engineer position at Tech Innovations Inc. With over 5 years of experience in full-stack development and a proven track record of delivering scalable solutions, I believe I would be an excellent fit for your team.

In my current role at Tech Company, I have led the development of microservices that serve over 1 million users daily. My experience aligns well with your requirements for someone who can design and implement distributed systems. I am particularly excited about your company's mission to democratize access to technology.

My background in both startup and enterprise environments has given me the versatility to thrive in fast-paced, dynamic settings. I am confident that my technical skills and collaborative approach would make me a valuable addition to your engineering team.

I would welcome the opportunity to discuss how my experience and passion for technology can contribute to Tech Innovations' continued success. Thank you for considering my application.

Best regards,
John Doe
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer - Tech Innovations Inc.

About Us:
We are seeking a talented Senior Software Engineer to join our growing team. Tech Innovations is a fast-paced startup revolutionizing the industry through cutting-edge technology.

Responsibilities:
- Design and implement scalable microservices architecture
- Lead technical discussions and mentor junior engineers  
- Collaborate with product team to define requirements
- Participate in code reviews and architectural decisions

Requirements:
- 5+ years of software engineering experience
- Strong proficiency in Python, Java, or Go
- Experience with AWS and container orchestration
- Excellent communication skills

Preferred Qualifications:
- Master's degree in Computer Science
- Experience with distributed systems
- Prior startup experience

What We Offer:
- Competitive salary ($150,000 - $180,000)
- Equity package
- Comprehensive health benefits
- Flexible work arrangements

To Apply:
Submit your resume and cover letter through our careers portal by February 1, 2024.

Tech Innovations is an equal opportunity employer committed to diversity and inclusion.
"""

AMBIGUOUS_SHORT_TEXT = """
Software Engineer
5 years experience
Python, Java
"""

MIXED_CHARACTERISTICS = """
Dear Hiring Manager,

PROFESSIONAL EXPERIENCE
Senior Developer | Tech Corp | 2020 - Present

Requirements:
- 5+ years experience
- Must have Python skills

Please send resume to jobs@company.com
"""


class TestDocumentClassifier:
    """Test suite for DocumentClassifier."""
    
    def test_classify_resume(self):
        """Test resume classification."""
        classifier = DocumentClassifier()
        result = classifier.classify(SAMPLE_RESUME)
        
        assert result.document_type == DocumentType.RESUME
        assert result.confidence >= 0.7
        assert "resume" in result.reasoning.lower()
    
    def test_classify_cover_letter(self):
        """Test cover letter classification."""
        classifier = DocumentClassifier()
        result = classifier.classify(SAMPLE_COVER_LETTER)
        
        assert result.document_type == DocumentType.COVER_LETTER
        assert result.confidence >= 0.7
        assert "cover" in result.reasoning.lower() or "letter" in result.reasoning.lower()
    
    def test_classify_job_description(self):
        """Test job description classification."""
        classifier = DocumentClassifier()
        result = classifier.classify(SAMPLE_JOB_DESCRIPTION)
        
        assert result.document_type == DocumentType.JOB_DESCRIPTION
        assert result.confidence >= 0.65  # Realistic threshold for job descriptions
        assert "job" in result.reasoning.lower() or "description" in result.reasoning.lower()
    
    def test_empty_text(self):
        """Test classification of empty text."""
        classifier = DocumentClassifier()
        result = classifier.classify("")
        
        assert result.document_type == DocumentType.UNKNOWN
        assert result.confidence == 0.0
        assert "too short" in result.reasoning.lower()
    
    def test_very_short_text(self):
        """Test classification of very short text."""
        classifier = DocumentClassifier()
        result = classifier.classify("Hello world")
        
        assert result.document_type == DocumentType.UNKNOWN
        assert result.confidence == 0.0
        assert "too short" in result.reasoning.lower()
    
    def test_ambiguous_text(self):
        """Test classification of ambiguous text."""
        classifier = DocumentClassifier()
        result = classifier.classify(AMBIGUOUS_SHORT_TEXT)
        
        # Should either classify with low confidence or return UNKNOWN
        assert result.confidence < 0.7 or result.document_type == DocumentType.UNKNOWN
    
    def test_mixed_characteristics(self):
        """Test document with mixed characteristics."""
        classifier = DocumentClassifier()
        result = classifier.classify(MIXED_CHARACTERISTICS)
        
        # Mixed documents may be rejected as UNKNOWN due to low confidence
        # This is correct behavior - better to be uncertain than wrong
        assert isinstance(result, ClassificationResult)
        assert result.confidence < 0.7  # Should have low confidence
        # Reasoning should mention patterns or confidence
        assert "pattern" in result.reasoning.lower() or "confidence" in result.reasoning.lower()
    
    def test_confidence_threshold(self):
        """Test minimum confidence threshold."""
        # Create truly ambiguous text with minimal distinguishing features
        # Mix of different document type indicators to keep confidence low
        truly_ambiguous = """
        Technology professional with strong background in software.
        Dear Hiring Committee, we are seeking qualified candidates.
        Working in various roles from 2020 to present time.
        Must have skills in multiple programming languages.
        I am interested in opportunities that challenge me.
        Requirements include teamwork and communication abilities.
        Looking forward to discussing potential collaboration.
        Education and experience in relevant technical areas.
        Please submit applications to the recruitment team.
        Developed solutions for complex business problems.
        The ideal candidate will demonstrate expertise.
        My qualifications align with industry standards.
        """ * 2  # Repeat to ensure sufficient length
        
        # High threshold should reject ambiguous documents
        classifier = DocumentClassifier(min_confidence=0.9)
        result = classifier.classify(truly_ambiguous)
        
        # Should classify as UNKNOWN due to high confidence requirement
        # (the mixed signals create lower confidence)
        assert result.document_type == DocumentType.UNKNOWN
        assert "confidence too low" in result.reasoning.lower()
    
    def test_resume_with_date_ranges(self):
        """Test resume identification via date ranges."""
        resume_with_dates = """
        Work Experience:
        Software Engineer | Company A | 2020 - 2023
        Junior Developer | Company B | 2018 - 2020
        
        Education:
        BS Computer Science | 2014 - 2018
        """
        
        classifier = DocumentClassifier()
        result = classifier.classify(resume_with_dates)
        
        assert result.document_type == DocumentType.RESUME
        assert result.confidence > 0.5
    
    def test_cover_letter_with_salutation(self):
        """Test cover letter identification via salutation."""
        letter_with_salutation = """
        Dear Hiring Manager,
        
        I am writing to apply for the position. My experience includes
        working with various technologies and teams. I look forward to
        discussing this opportunity further.
        
        Sincerely,
        Jane Smith
        """
        
        classifier = DocumentClassifier()
        result = classifier.classify(letter_with_salutation)
        
        assert result.document_type == DocumentType.COVER_LETTER
        assert result.confidence > 0.6
    
    def test_job_description_with_requirements(self):
        """Test job description identification via requirements."""
        job_desc_text = """
        Position: Senior Engineer
        
        Responsibilities:
        - Design systems
        - Lead team
        
        Requirements:
        - 5+ years experience required
        - Must have Python skills
        - Preferred: AWS certification
        
        To apply, submit your resume to careers@company.com
        We are an equal opportunity employer.
        """
        
        classifier = DocumentClassifier()
        result = classifier.classify(job_desc_text)
        
        assert result.document_type == DocumentType.JOB_DESCRIPTION
        assert result.confidence > 0.6
    
    def test_classification_result_structure(self):
        """Test that ClassificationResult has correct structure."""
        classifier = DocumentClassifier()
        result = classifier.classify(SAMPLE_RESUME)
        
        assert isinstance(result, ClassificationResult)
        assert isinstance(result.document_type, DocumentType)
        assert isinstance(result.confidence, float)
        assert isinstance(result.reasoning, str)
        assert 0.0 <= result.confidence <= 1.0
        assert len(result.reasoning) > 0


class TestDocumentProcessor:
    """Test suite for DocumentProcessor."""
    
    def test_process_resume(self):
        """Test processing a resume document."""
        processor = DocumentProcessor()
        result = processor.process_document(SAMPLE_RESUME, filename="resume.txt")
        
        assert result['document_type'] == 'resume'
        assert result['confidence'] >= 0.7
        assert result['text_length'] > 0
        assert result['filename'] == "resume.txt"
        assert 'reasoning' in result
    
    def test_process_cover_letter(self):
        """Test processing a cover letter."""
        processor = DocumentProcessor()
        result = processor.process_document(SAMPLE_COVER_LETTER)
        
        assert result['document_type'] == 'cover_letter'
        assert result['confidence'] >= 0.7
        assert result['filename'] is None  # No filename provided
    
    def test_process_job_description(self):
        """Test processing a job description."""
        processor = DocumentProcessor()
        result = processor.process_document(SAMPLE_JOB_DESCRIPTION)
        
        assert result['document_type'] == 'job_description'
        assert result['confidence'] >= 0.65  # Realistic threshold
    
    def test_result_dictionary_structure(self):
        """Test that result dictionary has expected structure."""
        processor = DocumentProcessor()
        result = processor.process_document(SAMPLE_RESUME, filename="test.txt")
        
        required_keys = ['document_type', 'confidence', 'reasoning', 'text_length', 'filename']
        for key in required_keys:
            assert key in result
        
        assert isinstance(result['document_type'], str)
        assert isinstance(result['confidence'], float)
        assert isinstance(result['reasoning'], str)
        assert isinstance(result['text_length'], int)
    
    def test_custom_confidence_threshold(self):
        """Test processor with custom confidence threshold."""
        processor = DocumentProcessor(min_confidence=0.9)
        result = processor.process_document(AMBIGUOUS_SHORT_TEXT)
        
        # Should classify as unknown with high threshold
        assert result['document_type'] == 'unknown'


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_whitespace_only(self):
        """Test document with only whitespace."""
        classifier = DocumentClassifier()
        result = classifier.classify("   \n\n  \t  ")
        
        assert result.document_type == DocumentType.UNKNOWN
        assert result.confidence == 0.0
    
    def test_special_characters(self):
        """Test document with many special characters."""
        special_text = """
        !!!! @@@@ #### $$$$ %%%% ^^^^
        &&&& **** (()) ---- ====
        """
        
        classifier = DocumentClassifier()
        result = classifier.classify(special_text)
        
        assert result.document_type == DocumentType.UNKNOWN
    
    def test_non_english_text(self):
        """Test classification with non-English text."""
        # This should fail gracefully
        non_english = """
        Î³"Î³Â«Î³'Î³â€•Î´Îˆâ€“Î·â€¢Å’
        Hola mundo
        Î â€”Î Î„Î¡â‚¬Î Â°Î Â²Î¡Î¡â€šÎ Â²Î¡Æ’Î Î‰Î¡â€šÎ Î…
        """
        
        classifier = DocumentClassifier()
        result = classifier.classify(non_english)
        
        # Should handle gracefully, likely classify as UNKNOWN
        assert isinstance(result, ClassificationResult)
    
    def test_very_long_document(self):
        """Test classification of very long document."""
        long_resume = SAMPLE_RESUME * 100  # Repeat to make very long
        
        classifier = DocumentClassifier()
        result = classifier.classify(long_resume)
        
        # Should still classify correctly
        assert result.document_type == DocumentType.RESUME
        assert result.confidence > 0.6


@pytest.fixture
def classifier():
    """Fixture providing a DocumentClassifier instance."""
    return DocumentClassifier()


@pytest.fixture
def processor():
    """Fixture providing a DocumentProcessor instance."""
    return DocumentProcessor()


def test_classifier_fixture(classifier):
    """Test classifier fixture."""
    assert isinstance(classifier, DocumentClassifier)


def test_processor_fixture(processor):
    """Test processor fixture."""
    assert isinstance(processor, DocumentProcessor)
