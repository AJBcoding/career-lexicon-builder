"""
Tests for document_processor module.
"""

import pytest
from core.document_processor import (
    DocumentType,
    classify_by_filename,
    classify_by_content,
    classify_document
)


class TestDocumentType:
    """Tests for DocumentType enum."""

    def test_enum_values(self):
        """Test that all expected document types exist."""
        assert DocumentType.RESUME.value == "resume"
        assert DocumentType.COVER_LETTER.value == "cover_letter"
        assert DocumentType.JOB_DESCRIPTION.value == "job_description"
        assert DocumentType.UNKNOWN.value == "unknown"


class TestClassifyByFilename:
    """Tests for classify_by_filename function."""

    def test_resume_patterns(self):
        """Test resume filename patterns."""
        assert classify_by_filename("resume.pdf") == DocumentType.RESUME
        assert classify_by_filename("Resume-2024.docx") == DocumentType.RESUME
        assert classify_by_filename("john_resume_final.pdf") == DocumentType.RESUME
        assert classify_by_filename("CV.pdf") == DocumentType.RESUME
        assert classify_by_filename("my-cv-2024.docx") == DocumentType.RESUME
        assert classify_by_filename("curriculum.vitae.pdf") == DocumentType.RESUME

    def test_cover_letter_patterns(self):
        """Test cover letter filename patterns."""
        assert classify_by_filename("cover_letter.pdf") == DocumentType.COVER_LETTER
        assert classify_by_filename("CoverLetter.docx") == DocumentType.COVER_LETTER
        assert classify_by_filename("cover-letter-company.pdf") == DocumentType.COVER_LETTER
        assert classify_by_filename("letter.pdf") == DocumentType.COVER_LETTER

    def test_job_description_patterns(self):
        """Test job description filename patterns."""
        assert classify_by_filename("job_description.pdf") == DocumentType.JOB_DESCRIPTION
        assert classify_by_filename("JobDescription.docx") == DocumentType.JOB_DESCRIPTION
        assert classify_by_filename("job-posting.pdf") == DocumentType.JOB_DESCRIPTION
        assert classify_by_filename("position_description.pdf") == DocumentType.JOB_DESCRIPTION

    def test_no_match(self):
        """Test filenames that don't match any pattern."""
        assert classify_by_filename("random_document.pdf") is None
        assert classify_by_filename("notes.txt") is None
        assert classify_by_filename("2024-10-meeting.docx") is None

    def test_with_path(self):
        """Test that classification works with full paths."""
        assert classify_by_filename("/path/to/resume.pdf") == DocumentType.RESUME
        assert classify_by_filename("../docs/cover_letter.docx") == DocumentType.COVER_LETTER

    def test_case_insensitive(self):
        """Test that pattern matching is case-insensitive."""
        assert classify_by_filename("RESUME.PDF") == DocumentType.RESUME
        assert classify_by_filename("CoverLetter.DOCX") == DocumentType.COVER_LETTER


class TestClassifyByContent:
    """Tests for classify_by_content function."""

    def test_clear_resume(self):
        """Test classification of clear resume content."""
        text = """
        John Doe
        john@email.com | 555-123-4567

        Experience
        Senior Software Engineer | Tech Corp | 2020-2024
        • Developed microservices architecture
        • Led team of 5 engineers
        • Improved system performance by 40%

        Software Engineer | StartupCo | 2018-2020
        • Built REST APIs
        • Implemented CI/CD pipelines

        Education
        BS Computer Science | University | 2018

        Skills
        Python, JavaScript, AWS, Docker
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.RESUME
        assert confidence >= 0.5
        assert "resume" in reasoning.lower()

    def test_clear_cover_letter(self):
        """Test classification of clear cover letter content."""
        text = """
        Dear Hiring Manager,

        I am writing to express my strong interest in the Senior Software Engineer
        position at Tech Corp. With over 6 years of experience in software development,
        I am excited about the opportunity to contribute to your team.

        My experience at StartupCo has prepared me well for this role. I have
        consistently delivered high-quality software solutions and am passionate
        about creating elegant, maintainable code.

        I would welcome the opportunity to discuss how my background and skills
        would benefit your organization. Thank you for your consideration.

        Sincerely,
        John Doe
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.COVER_LETTER
        assert confidence >= 0.5
        assert "cover" in reasoning.lower()

    def test_clear_job_description(self):
        """Test classification of clear job description content."""
        text = """
        Senior Software Engineer

        We are seeking a talented Senior Software Engineer to join our growing team.
        The ideal candidate will have 5+ years of experience in software development.

        Responsibilities include:
        • Design and implement scalable microservices
        • Mentor junior developers
        • Participate in architecture decisions
        • Lead technical projects

        Required qualifications:
        • BS in Computer Science or related field
        • 5+ years of professional software development
        • Strong knowledge of Python and JavaScript
        • Experience with cloud platforms (AWS, GCP)

        We offer competitive compensation, health benefits, and a collaborative
        work environment. Join us in building the future of technology!
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.JOB_DESCRIPTION
        assert confidence >= 0.5
        assert "job" in reasoning.lower() or "description" in reasoning.lower()

    def test_resume_with_bullets(self):
        """Test that bullet-heavy content suggests resume."""
        text = """
        Experience
        Software Engineer 2020-2024
        • First bullet point about work
        • Second bullet point about work
        • Third bullet point about work
        • Fourth bullet point about work
        • Fifth bullet point about work

        Education
        BS Computer Science 2020
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.RESUME

    def test_cover_letter_no_bullets(self):
        """Test that paragraph-heavy content suggests cover letter."""
        text = """
        Dear Hiring Manager,

        I am writing to apply for the position. I have extensive experience in the field
        and believe I would be a great fit for your team. My background includes working
        on various projects where I demonstrated strong technical skills.

        I am excited to apply and look forward to discussing this opportunity.

        Sincerely,
        Jane Smith
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.COVER_LETTER

    def test_ambiguous_content(self):
        """Test classification of ambiguous content."""
        text = """
        This is some generic text that doesn't really indicate what type of
        document it is. It's just a bunch of words without clear patterns.
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        # Should return UNKNOWN with low confidence
        assert doc_type == DocumentType.UNKNOWN
        assert confidence < 0.5

    def test_empty_text(self):
        """Test classification of empty text."""
        doc_type, confidence, reasoning = classify_by_content("")
        assert doc_type == DocumentType.UNKNOWN
        assert confidence == 0.0
        assert "too short" in reasoning.lower()

    def test_very_short_text(self):
        """Test classification of very short text."""
        doc_type, confidence, reasoning = classify_by_content("Hello world")
        assert doc_type == DocumentType.UNKNOWN
        assert confidence == 0.0
        assert "too short" in reasoning.lower()

    def test_resume_with_date_ranges(self):
        """Test that date ranges increase resume confidence."""
        text = """
        Experience

        Software Engineer
        Tech Corp | 2020-2024
        Worked on various projects

        Junior Developer
        StartupCo | 2018-2020
        Built web applications

        Education
        BS Computer Science 2018
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.RESUME
        assert "date range" in reasoning.lower()

    def test_resume_with_present(self):
        """Test date ranges with 'present'."""
        text = """
        Experience
        Senior Engineer | 2020-present
        Currently working on projects

        Skills
        Python, JavaScript
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.RESUME

    def test_cover_letter_with_salutation_only(self):
        """Test cover letter detection with just salutation."""
        text = """
        Dear Sir or Madam,

        This is a letter with a salutation but not much else that clearly
        indicates it's a cover letter. Let's see how it classifies. I am
        interested in working with your company and bringing my skills to
        help your team succeed.

        Thank you for your time and consideration.
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.COVER_LETTER
        assert confidence >= 0.3

    def test_job_description_with_company_voice(self):
        """Test job description with company-centric language."""
        text = """
        About the Role

        We are looking for a talented engineer to join our team. Our company
        is building innovative solutions and we offer competitive benefits.

        You will be responsible for designing and implementing new features,
        collaborating with product teams, and ensuring high code quality.

        Required qualifications include 3+ years of experience and strong
        problem-solving skills. Join us in making an impact!
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.JOB_DESCRIPTION

    def test_multiple_resume_sections(self):
        """Test that multiple resume sections increase confidence."""
        text = """
        Professional Summary
        Experienced software engineer with proven track record

        Experience
        Various roles over the years

        Education
        Degrees and certifications

        Skills
        Technical proficiencies

        Certifications
        Industry certifications
        """
        doc_type, confidence, reasoning = classify_by_content(text)
        assert doc_type == DocumentType.RESUME
        assert confidence >= 0.5


class TestClassifyDocument:
    """Tests for classify_document function."""

    def test_filename_match_resume(self):
        """Test that filename match takes priority."""
        text = "Some generic text"
        doc_type, confidence, reasoning = classify_document("resume.pdf", text)
        assert doc_type == DocumentType.RESUME
        assert confidence == 0.95
        assert "filename match" in reasoning.lower()

    def test_filename_match_cover_letter(self):
        """Test filename match for cover letter."""
        text = "Some generic text"
        doc_type, confidence, reasoning = classify_document("cover_letter.docx", text)
        assert doc_type == DocumentType.COVER_LETTER
        assert confidence == 0.95
        assert "filename match" in reasoning.lower()

    def test_content_fallback(self):
        """Test that content analysis is used when filename doesn't match."""
        text = """
        Dear Hiring Manager,

        I am writing to express my interest in the position. I have extensive
        experience and would love to contribute to your team.

        Sincerely,
        Jane Doe
        """
        doc_type, confidence, reasoning = classify_document("document.pdf", text)
        assert doc_type == DocumentType.COVER_LETTER
        assert "content analysis" in reasoning.lower()

    def test_filename_with_path(self):
        """Test that paths are handled correctly."""
        text = "Some text"
        doc_type, confidence, reasoning = classify_document("/path/to/resume.pdf", text)
        assert doc_type == DocumentType.RESUME
        assert confidence == 0.95

    def test_ambiguous_filename_and_content(self):
        """Test ambiguous document with generic filename."""
        text = "Just some random text without clear indicators."
        doc_type, confidence, reasoning = classify_document("notes.txt", text)
        assert doc_type == DocumentType.UNKNOWN
        assert confidence < 0.5

    def test_conflicting_filename_content(self):
        """Test when filename suggests one type but content another."""
        # Filename says resume, but content is clearly a cover letter
        text = """
        Dear Hiring Manager,

        I am writing to apply for the Software Engineer position. I am excited
        about this opportunity and believe my skills align well with your needs.

        Sincerely,
        John Doe
        """
        # Filename should take priority
        doc_type, confidence, reasoning = classify_document("resume.pdf", text)
        assert doc_type == DocumentType.RESUME
        assert confidence == 0.95
        assert "filename match" in reasoning.lower()

    def test_content_analysis_with_high_confidence(self):
        """Test content analysis with clear indicators."""
        text = """
        Experience

        Senior Engineer | Tech Corp | 2020-2024
        • Led engineering team
        • Designed systems

        Education
        BS Computer Science 2018

        Skills
        Python, AWS, Docker
        """
        doc_type, confidence, reasoning = classify_document("document.txt", text)
        assert doc_type == DocumentType.RESUME
        assert confidence >= 0.5
