import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models.db_models import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
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
def client():
    # Create test database
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Drop test database
    Base.metadata.drop_all(bind=engine)

def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert data["is_active"] is True

def test_register_duplicate_email(client):
    # Register first user
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    # Try to register again
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "different123",
        "full_name": "Another User"
    })

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client):
    # Register user
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    # Login
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    # Register user
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    # Login with wrong password
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401

def test_login_nonexistent_user(client):
    # Login with user that doesn't exist
    response = client.post("/api/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "testpass123"
    })

    assert response.status_code == 401

def test_get_current_user(client):
    # Register and login
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })

    login_response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_get_current_user_invalid_token(client):
    # Try to get current user with invalid token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401

def test_get_current_user_no_token(client):
    # Try to get current user without token
    response = client.get("/api/auth/me")

    assert response.status_code == 401
