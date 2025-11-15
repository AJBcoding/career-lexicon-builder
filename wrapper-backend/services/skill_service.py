import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, Optional
import asyncio
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Define whitelist of allowed skills to prevent command injection
ALLOWED_SKILLS = {
    'job-description-analysis',
    'resume-alignment',
    'job-fit-analysis',
    'cover-letter-voice',
    'collaborative-writing'
}

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
        # VALIDATE SKILL NAME BEFORE USE - prevents command injection
        if skill_name not in ALLOWED_SKILLS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid skill name. Allowed: {', '.join(sorted(ALLOWED_SKILLS))}"
            )

        logger.info("Executing skill", extra={
            'skill_name': skill_name,
            'project_path': str(project_path),
            'prompt_length': len(prompt)
        })

        cmd = [
            self.claude_path,
            "--skill", skill_name,
            prompt
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info("Skill execution completed", extra={
                    'skill_name': skill_name,
                    'stdout_length': len(result.stdout)
                })
            else:
                logger.error("Skill execution failed", extra={
                    'skill_name': skill_name,
                    'returncode': result.returncode,
                    'stderr': result.stderr[:500]  # Truncate for logging
                })

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired as e:
            logger.error("Skill execution timed out", extra={
                'skill_name': skill_name,
                'timeout_seconds': 300
            }, exc_info=True)
            raise
        except Exception as e:
            logger.error("Skill execution error", extra={
                'skill_name': skill_name,
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)
            raise

    async def invoke_skill_streaming(
        self,
        skill_name: str,
        project_path: Path,
        prompt: str,
        on_output: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """Invoke skill with streaming output"""
        # VALIDATE SKILL NAME BEFORE USE - prevents command injection
        if skill_name not in ALLOWED_SKILLS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid skill name. Allowed: {', '.join(sorted(ALLOWED_SKILLS))}"
            )

        logger.info("Executing skill (streaming)", extra={
            'skill_name': skill_name,
            'project_path': str(project_path),
            'prompt_length': len(prompt)
        })

        cmd = [
            self.claude_path,
            "--skill", skill_name,
            prompt
        ]

        try:
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

            if process.returncode == 0:
                logger.info("Skill execution completed (streaming)", extra={
                    'skill_name': skill_name,
                    'stdout_lines': len(stdout_lines)
                })
            else:
                logger.error("Skill execution failed (streaming)", extra={
                    'skill_name': skill_name,
                    'returncode': process.returncode,
                    'stderr_lines': len(stderr_lines)
                })

            return {
                "success": process.returncode == 0,
                "stdout": ''.join(stdout_lines),
                "stderr": ''.join(stderr_lines),
                "returncode": process.returncode
            }
        except Exception as e:
            logger.error("Skill execution error (streaming)", extra={
                'skill_name': skill_name,
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)
            raise
