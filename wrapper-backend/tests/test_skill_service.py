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

@pytest.mark.asyncio
async def test_invoke_skill_streaming():
    import asyncio
    from unittest.mock import AsyncMock

    temp_dir = Path(tempfile.mkdtemp())
    service = SkillService(claude_path="claude")

    output_lines = []

    async def capture_output(line: str):
        output_lines.append(line)

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        # Create a mock process
        mock_process = Mock()
        mock_process.returncode = 0

        # Create async mock for stdout
        mock_stdout = Mock()
        readline_calls = [b'Line 1\n', b'Line 2\n', b'']
        call_index = [0]

        async def mock_readline():
            idx = call_index[0]
            call_index[0] += 1
            if idx < len(readline_calls):
                return readline_calls[idx]
            return b''

        mock_stdout.readline = mock_readline
        mock_process.stdout = mock_stdout

        # Create async mock for stderr
        mock_stderr = Mock()
        mock_stderr.readline = AsyncMock(return_value=b'')
        mock_process.stderr = mock_stderr

        # Mock wait
        mock_process.wait = AsyncMock()

        mock_exec.return_value = mock_process

        result = await service.invoke_skill_streaming(
            skill_name="test-skill",
            project_path=temp_dir,
            prompt="test",
            on_output=capture_output
        )

        assert result["success"] is True
        assert len(output_lines) == 2
        assert output_lines[0] == "Line 1\n"
        assert output_lines[1] == "Line 2\n"

    shutil.rmtree(temp_dir)
