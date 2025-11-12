import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_invoke_skill_endpoint(client):
    with patch('services.skill_service.SkillService.invoke_skill') as mock_invoke, \
         patch('api.skills.Path.exists', return_value=True):
        mock_invoke.return_value = {
            "success": True,
            "stdout": "Analysis complete",
            "stderr": "",
            "returncode": 0
        }

        response = client.post("/api/skills/invoke", json={
            "project_id": "test-project",
            "skill_name": "analyze-job-posting",
            "prompt": "Analyze this job"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
