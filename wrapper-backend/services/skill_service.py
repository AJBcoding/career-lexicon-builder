import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, Optional
import asyncio

class SkillService:
    def __init__(self, claude_path: str = "claude"):
        self.claude_path = claude_path

    def invoke_skill(
        self,
        skill_name: str,
        project_path: Path,
        prompt: str
    ) -> Dict[str, Any]:
        """Invoke a Claude Code skill in the project directory"""
        cmd = [
            self.claude_path,
            "--skill", skill_name,
            prompt
        ]

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    async def invoke_skill_streaming(
        self,
        skill_name: str,
        project_path: Path,
        prompt: str,
        on_output: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """Invoke skill with streaming output"""
        cmd = [
            self.claude_path,
            "--skill", skill_name,
            prompt
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=project_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout_lines = []
        stderr_lines = []

        async def read_stream(stream, lines_list, is_stderr=False):
            while True:
                line = await stream.readline()
                if not line:
                    break
                line_text = line.decode('utf-8')
                lines_list.append(line_text)

                if on_output and not is_stderr:
                    await on_output(line_text)

        # Read stdout and stderr concurrently
        await asyncio.gather(
            read_stream(process.stdout, stdout_lines),
            read_stream(process.stderr, stderr_lines, is_stderr=True)
        )

        await process.wait()

        return {
            "success": process.returncode == 0,
            "stdout": ''.join(stdout_lines),
            "stderr": ''.join(stderr_lines),
            "returncode": process.returncode
        }
