import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import tempfile
import shutil
from database import Base, get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api_skills.db"
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

def test_invoke_skill_endpoint(client, auth_token):
    # Create a project first
    project_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    project_id = project_response.json()["project_id"]

    with patch('services.skill_service.SkillService.invoke_skill') as mock_invoke, \
         patch('api.skills.Path.exists', return_value=True):
        mock_invoke.return_value = {
            "success": True,
            "stdout": "Analysis complete",
            "stderr": "",
            "returncode": 0
        }

        response = client.post(
            "/api/skills/invoke",
            json={
                "project_id": project_id,
                "skill_name": "analyze-job-posting",
                "prompt": "Analyze this job"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

def test_invoke_skill_with_streaming_flag(client, auth_token):
    # Create a project first
    project_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    project_id = project_response.json()["project_id"]

    with patch('api.skills.Path.exists', return_value=True):
        response = client.post(
            "/api/skills/invoke",
            json={
                "project_id": project_id,
                "skill_name": "analyze-job-posting",
                "prompt": "Analyze this job",
                "stream": True
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        assert data["streaming"] is True
        assert data["project_id"] == project_id
