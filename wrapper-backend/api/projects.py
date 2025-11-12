from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from pathlib import Path
import os
from services.project_service import ProjectService
from models.project import ProjectState

router = APIRouter(prefix="/api/projects", tags=["projects"])

def get_project_service():
    apps_dir = os.getenv("APPLICATIONS_DIR", "./applications")
    return ProjectService(Path(apps_dir))

class CreateProjectRequest(BaseModel):
    institution: str
    position: str
    date: str

@router.post("", response_model=ProjectState)
async def create_project(
    request: CreateProjectRequest,
    service: ProjectService = Depends(get_project_service)
):
    project_id = service.create_project(
        institution=request.institution,
        position=request.position,
        date=request.date
    )

    # Get the created project state
    project_path = service.applications_dir / project_id
    state_file = project_path / ".project-state.json"

    import json
    state_data = json.loads(state_file.read_text())
    return ProjectState(**state_data)

@router.get("", response_model=List[ProjectState])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()
