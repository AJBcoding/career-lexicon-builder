from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import os
from services.skill_service import SkillService

router = APIRouter(prefix="/api/skills", tags=["skills"])

def get_skill_service():
    claude_path = os.getenv("CLAUDE_CODE_PATH", "claude")
    return SkillService(claude_path)

class InvokeSkillRequest(BaseModel):
    project_id: str
    skill_name: str
    prompt: str

@router.post("/invoke")
async def invoke_skill(
    request: InvokeSkillRequest,
    service: SkillService = Depends(get_skill_service)
):
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / request.project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    result = service.invoke_skill(
        skill_name=request.skill_name,
        project_path=project_path,
        prompt=request.prompt
    )

    return result
