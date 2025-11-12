import pytest
from pathlib import Path
import tempfile
import shutil
from services.project_service import ProjectService

@pytest.fixture
def temp_apps_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_create_project_creates_directory_structure(temp_apps_dir):
    service = ProjectService(temp_apps_dir)
    project_id = service.create_project(
        institution="UCLA",
        position="Assistant Dean",
        date="2024-11-15"
    )

    project_path = temp_apps_dir / project_id
    assert project_path.exists()
    assert (project_path / ".project-state.json").exists()

def test_list_projects_returns_all_projects(temp_apps_dir):
    service = ProjectService(temp_apps_dir)
    service.create_project("UCLA", "Assistant Dean", "2024-11-15")
    service.create_project("USC", "Director", "2024-11-16")

    projects = service.list_projects()
    assert len(projects) == 2
    assert any(p.institution == "UCLA" for p in projects)
    assert any(p.institution == "USC" for p in projects)
