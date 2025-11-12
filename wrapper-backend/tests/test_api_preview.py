import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from main import app

@pytest.fixture
def temp_apps_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("APPLICATIONS_DIR", temp_dir)

    # Create test project with files
    project_dir = Path(temp_dir) / "test-project"
    project_dir.mkdir()

    # Create markdown file
    md_file = project_dir / "test.md"
    md_file.write_text("# Test Heading\n\nTest content.")

    # Create PDF file (empty for test)
    pdf_file = project_dir / "test.pdf"
    pdf_file.write_text("%PDF-1.4")  # Minimal PDF header

    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def client():
    return TestClient(app)

def test_preview_html_converts_markdown(client, temp_apps_dir):
    response = client.get("/api/preview/html/test-project/test.md")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert '<h1 id="test-heading">Test Heading</h1>' in response.text
    assert "Test content" in response.text

def test_preview_html_not_found(client, temp_apps_dir):
    response = client.get("/api/preview/html/test-project/nonexistent.md")
    assert response.status_code == 404

def test_preview_pdf_serves_file(client, temp_apps_dir):
    response = client.get("/api/preview/pdf/test-project/test.pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_preview_pdf_not_found(client, temp_apps_dir):
    response = client.get("/api/preview/pdf/test-project/nonexistent.pdf")
    assert response.status_code == 404
