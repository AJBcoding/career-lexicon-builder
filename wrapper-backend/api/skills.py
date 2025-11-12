from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from pydantic import BaseModel
from pathlib import Path
import os
from sqlalchemy.orm import Session
from services.skill_service import SkillService
from services.anthropic_service import AnthropicService
from services.project_service import ProjectService
from api.websocket import get_connection_manager
from models.db_models import User
from utils.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/skills", tags=["skills"])

def get_skill_service():
    claude_path = os.getenv("CLAUDE_CODE_PATH", "claude")
    return SkillService(claude_path)

def get_project_service(db: Session = Depends(get_db)):
    apps_dir = os.getenv("APPLICATIONS_DIR", "./applications")
    return ProjectService(Path(apps_dir), db=db)

class InvokeSkillRequest(BaseModel):
    project_id: str
    skill_name: str
    prompt: str
    stream: bool = False
    use_api: bool = False  # New field: use Anthropic API instead of CLI

@router.post("/invoke")
async def invoke_skill(
    request: InvokeSkillRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
    project_service: ProjectService = Depends(get_project_service)
):
    # Verify project exists and user owns it
    project = project_service.get_project(request.project_id, owner_id=current_user.id)
    if not project:
        # Check if project exists at all
        project_exists = project_service.get_project(request.project_id)
        if project_exists:
            # Project exists but user doesn't own it
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this project"
            )
        else:
            # Project doesn't exist
            raise HTTPException(status_code=404, detail="Project not found")

    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / request.project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    if request.use_api:
        # Use Anthropic API instead of CLI
        anthropic_service = AnthropicService()

        if request.stream:
            background_tasks.add_task(
                execute_skill_with_api_streaming,
                anthropic_service,
                request.skill_name,
                request.prompt,
                request.project_id
            )
            return {"status": "started", "streaming": True, "mode": "api", "project_id": request.project_id}
        else:
            result = anthropic_service.invoke_skill(
                skill_name=request.skill_name,
                prompt=request.prompt
            )
            return result

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

async def execute_skill_with_api_streaming(
    service: AnthropicService,
    skill_name: str,
    prompt: str,
    project_id: str
):
    """Execute skill via Anthropic API with streaming"""
    manager = get_connection_manager()

    await manager.broadcast_to_project(
        {"type": "skill_start", "skill": skill_name, "mode": "api"},
        project_id
    )

    async def on_token(token: str):
        await manager.broadcast_to_project(
            {"type": "skill_token", "skill": skill_name, "token": token},
            project_id
        )

    try:
        result = await service.invoke_skill_streaming(
            skill_name=skill_name,
            prompt=prompt,
            on_token=on_token
        )

        await manager.broadcast_to_project(
            {
                "type": "skill_complete",
                "skill": skill_name,
                "success": result["success"],
                "usage": result["usage"]
            },
            project_id
        )
    except Exception as e:
        await manager.broadcast_to_project(
            {"type": "skill_error", "skill": skill_name, "error": str(e)},
            project_id
        )
