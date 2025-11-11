import pytest
from pathlib import Path
from docx import Document
from cv_formatting.style_applicator import StyleApplicator


def test_apply_paragraph_style(tmp_path):
    """Test applying paragraph style to content"""
    template = Path("cv_formatting/templates/career-documents-template.docx")
    output = tmp_path / "test-output.docx"

    content_mapping = [
        {
            "text": "EDUCATION",
            "style": "Section Header",
            "type": "paragraph"
        },
        {
            "text": "Standard body paragraph text.",
            "style": "Body Text",
            "type": "paragraph"
        }
    ]

    applicator = StyleApplicator(str(template))
    result = applicator.apply_styles(content_mapping, str(output))

    assert result is True
    assert output.exists()

    # Verify styles applied
    doc = Document(str(output))
    assert len(doc.paragraphs) == 2
    assert doc.paragraphs[0].style.name == "Section Header"
    assert doc.paragraphs[1].style.name == "Body Text"


def test_apply_character_style_inline(tmp_path):
    """Test applying character style within paragraph"""
    template = Path("cv_formatting/templates/career-documents-template.docx")
    output = tmp_path / "test-output.docx"

    content_mapping = [
        {
            "text": "2023 - Present ",
            "style": "Timeline Entry",
            "type": "paragraph",
            "runs": [
                {"text": "2023 - Present ", "style": None},
                {"text": "California State University", "style": "Institution"}
            ]
        }
    ]

    applicator = StyleApplicator(str(template))
    result = applicator.apply_styles(content_mapping, str(output))

    assert result is True

    # Verify inline style applied
    doc = Document(str(output))
    para = doc.paragraphs[0]
    assert para.style.name == "Timeline Entry"
    assert len(para.runs) == 2
    assert para.runs[1].style.name == "Institution"
