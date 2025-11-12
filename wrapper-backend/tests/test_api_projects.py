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
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def client():
    return TestClient(app)

def test_create_project_endpoint(client, temp_apps_dir):
    response = client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })

    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["institution"] == "UCLA"

def test_list_projects_endpoint(client, temp_apps_dir):
    # Create two projects
    client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })
    client.post("/api/projects", json={
        "institution": "USC",
        "position": "Director",
        "date": "2024-11-16"
    })

    # List projects
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 2

def test_start_watching_project(client, temp_apps_dir):
    # Create a project
    create_response = client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })
    project_id = create_response.json()["project_id"]

    # Start watching
    response = client.post(f"/api/projects/{project_id}/watch")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "watching"
    assert data["project_id"] == project_id

def test_stop_watching_project(client, temp_apps_dir):
    # Create a project
    create_response = client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })
    project_id = create_response.json()["project_id"]

    # Start watching
    client.post(f"/api/projects/{project_id}/watch")

    # Stop watching
    response = client.delete(f"/api/projects/{project_id}/watch")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "stopped"
    assert data["project_id"] == project_id
