import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import tempfile
import shutil
from database import Base, get_db
from main import app
from models.db_models import User, Project

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_authorization.db"
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
def temp_apps_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("APPLICATIONS_DIR", temp_dir)
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def client(temp_apps_dir):
    # Create test database
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Drop test database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user1_token(client):
    """Create and login user1"""
    client.post("/api/auth/register", json={
        "email": "user1@example.com",
        "password": "password123",
        "full_name": "User One"
    })

    response = client.post("/api/auth/login", data={
        "username": "user1@example.com",
        "password": "password123"
    })
    return response.json()["access_token"]

@pytest.fixture
def user2_token(client):
    """Create and login user2"""
    client.post("/api/auth/register", json={
        "email": "user2@example.com",
        "password": "password456",
        "full_name": "User Two"
    })

    response = client.post("/api/auth/login", data={
        "username": "user2@example.com",
        "password": "password456"
    })
    return response.json()["access_token"]

def test_create_project_requires_authentication(client):
    """Test that creating a project requires authentication"""
    response = client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })

    assert response.status_code == 401

def test_create_project_assigns_owner(client, user1_token):
    """Test that project creation assigns the correct owner"""
    response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["institution"] == "UCLA"

    # Verify in database that owner_id is set
    db = next(override_get_db())
    project = db.query(Project).filter(Project.project_id == data["project_id"]).first()
    assert project is not None
    assert project.owner_id is not None
    user = db.query(User).filter(User.email == "user1@example.com").first()
    assert project.owner_id == user.id

def test_list_projects_shows_only_user_projects(client, user1_token, user2_token):
    """Test that users can only see their own projects"""
    # User1 creates two projects
    user1_response1 = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    user1_project1_id = user1_response1.json()["project_id"]

    user1_response2 = client.post(
        "/api/projects",
        json={
            "institution": "USC",
            "position": "Director",
            "date": "2024-11-16"
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    user1_project2_id = user1_response2.json()["project_id"]

    # User2 creates one project
    user2_response = client.post(
        "/api/projects",
        json={
            "institution": "Stanford",
            "position": "Professor",
            "date": "2024-11-17"
        },
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    user2_project_id = user2_response.json()["project_id"]

    # User1 lists projects - should only see their 2 projects
    user1_list = client.get(
        "/api/projects",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert user1_list.status_code == 200
    user1_projects = user1_list.json()
    assert len(user1_projects) == 2
    user1_project_ids = [p["project_id"] for p in user1_projects]
    assert user1_project1_id in user1_project_ids
    assert user1_project2_id in user1_project_ids
    assert user2_project_id not in user1_project_ids

    # User2 lists projects - should only see their 1 project
    user2_list = client.get(
        "/api/projects",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert user2_list.status_code == 200
    user2_projects = user2_list.json()
    assert len(user2_projects) == 1
    assert user2_projects[0]["project_id"] == user2_project_id

def test_list_projects_requires_authentication(client):
    """Test that listing projects requires authentication"""
    response = client.get("/api/projects")
    assert response.status_code == 401

def test_invoke_skill_requires_authentication(client, temp_apps_dir):
    """Test that invoking a skill requires authentication"""
    # Create project directory manually
    project_id = "test-project"
    project_path = temp_apps_dir / project_id
    project_path.mkdir(parents=True, exist_ok=True)

    response = client.post("/api/skills/invoke", json={
        "project_id": project_id,
        "skill_name": "test-skill",
        "prompt": "test prompt",
        "stream": False
    })

    assert response.status_code == 401

def test_invoke_skill_only_on_owned_projects(client, user1_token, user2_token, temp_apps_dir):
    """Test that users can only invoke skills on their own projects"""
    # User1 creates a project
    user1_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    user1_project_id = user1_response.json()["project_id"]

    # User2 tries to invoke skill on User1's project - should fail with 403
    response = client.post(
        "/api/skills/invoke",
        json={
            "project_id": user1_project_id,
            "skill_name": "test-skill",
            "prompt": "test prompt",
            "stream": False
        },
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 403
    assert "not authorized" in response.json()["detail"].lower() or "forbidden" in response.json()["detail"].lower()

def test_invoke_skill_on_nonexistent_project(client, user1_token):
    """Test that invoking skill on nonexistent project returns 404"""
    response = client.post(
        "/api/skills/invoke",
        json={
            "project_id": "nonexistent-project-id",
            "skill_name": "test-skill",
            "prompt": "test prompt",
            "stream": False
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 404

def test_user_can_invoke_skill_on_own_project(client, user1_token, temp_apps_dir):
    """Test that users can invoke skills on their own projects"""
    # User1 creates a project
    user1_response = client.post(
        "/api/projects",
        json={
            "institution": "UCLA",
            "position": "Assistant Dean",
            "date": "2024-11-15"
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    user1_project_id = user1_response.json()["project_id"]

    # User1 invokes skill on their own project - should succeed (or fail for other reasons, but not 403)
    response = client.post(
        "/api/skills/invoke",
        json={
            "project_id": user1_project_id,
            "skill_name": "test-skill",
            "prompt": "test prompt",
            "stream": False
        },
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Should not be 403 (forbidden) or 401 (unauthorized)
    # May fail with other errors (skill not found, etc.) but authorization should pass
    assert response.status_code != 401
    assert response.status_code != 403
