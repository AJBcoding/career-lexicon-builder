import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api_projects.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client(monkeypatch):
    # Create temp applications directory
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("APPLICATIONS_DIR", temp_dir)

    # Create test database
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    shutil.rmtree(temp_dir)

@pytest.fixture
def auth_token(client):
    """Create and login a test user"""
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

def test_create_project_endpoint(client, auth_token):
    response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["institution"] == "UCLA"

def test_list_projects_endpoint(client, auth_token):
    # Create two projects
    client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/projects",
        json={
            "institution": "USC",
            "position": "Director",
            "date": "2024-11-16"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # List projects
    response = client.get(
        "/api/projects",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 2

def test_start_watching_project(client, auth_token):
    # Create a project
    create_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    project_id = create_response.json()["project_id"]

    # Start watching
    response = client.post(f"/api/projects/{project_id}/watch")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "watching"
    assert data["project_id"] == project_id

def test_stop_watching_project(client, auth_token):
    # Create a project
    create_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    project_id = create_response.json()["project_id"]

    # Start watching
    client.post(f"/api/projects/{project_id}/watch")

    # Stop watching
    response = client.delete(f"/api/projects/{project_id}/watch")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "stopped"
    assert data["project_id"] == project_id
