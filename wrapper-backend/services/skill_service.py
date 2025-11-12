import subprocess
from pathlib import Path
from typing import Dict, Any

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
