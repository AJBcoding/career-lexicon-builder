from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
import os
from services.skill_service import SkillService
from api.websocket import get_connection_manager

router = APIRouter(prefix="/api/skills", tags=["skills"])

def get_skill_service():
    claude_path = os.getenv("CLAUDE_CODE_PATH", "claude")
    return SkillService(claude_path)

class InvokeSkillRequest(BaseModel):
    project_id: str
    skill_name: str
    prompt: str
    stream: bool = False  # New field

@router.post("/invoke")
async def invoke_skill(
    request: InvokeSkillRequest,
    background_tasks: BackgroundTasks,
    service: SkillService = Depends(get_skill_service)
):
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / request.project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    if request.stream:
        # Execute in background with WebSocket streaming
        background_tasks.add_task(
            execute_skill_with_streaming,
            service,
            request.skill_name,
            project_path,
            request.prompt,
            request.project_id
        )
        return {"status": "started", "streaming": True, "project_id": request.project_id}
    else:
        # Original non-streaming execution
        result = service.invoke_skill(
            skill_name=request.skill_name,
            project_path=project_path,
            prompt=request.prompt
        )
        return result

async def execute_skill_with_streaming(
    service: SkillService,
    skill_name: str,
    project_path: Path,
    prompt: str,
    project_id: str
):
    """Execute skill with WebSocket streaming"""
    manager = get_connection_manager()

    # Send start message
    await manager.broadcast_to_project(
        {
            "type": "skill_start",
            "skill": skill_name,
            "project_id": project_id
        },
        project_id
    )

    async def on_output(line: str):
        """Callback for each line of output"""
        await manager.broadcast_to_project(
            {
                "type": "skill_output",
                "skill": skill_name,
                "output": line
            },
            project_id
        )

    try:
        result = await service.invoke_skill_streaming(
            skill_name=skill_name,
            project_path=project_path,
            prompt=prompt,
            on_output=on_output
        )

        # Send completion message
        await manager.broadcast_to_project(
            {
                "type": "skill_complete",
                "skill": skill_name,
                "success": result["success"],
                "returncode": result["returncode"]
            },
            project_id
        )
    except Exception as e:
        # Send error message
        await manager.broadcast_to_project(
            {
                "type": "skill_error",
                "skill": skill_name,
                "error": str(e)
            },
            project_id
        )
