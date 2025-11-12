import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch
from services.skill_service import SkillService

@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_invoke_skill_calls_claude_code(temp_project_dir):
    service = SkillService(claude_path="claude")

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")

        result = service.invoke_skill(
            skill_name="analyze-job-posting",
            project_path=temp_project_dir,
            prompt="Analyze the job posting"
        )

        assert result["success"] is True
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "claude" in call_args
        assert "analyze-job-posting" in " ".join(call_args)

def test_invoke_skill_uses_project_working_directory(temp_project_dir):
    service = SkillService(claude_path="claude")

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")

        service.invoke_skill(
            skill_name="test-skill",
            project_path=temp_project_dir,
            prompt="Test prompt"
        )

        call_kwargs = mock_run.call_args[1]
        assert call_kwargs['cwd'] == temp_project_dir
