from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from pathlib import Path
import os
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from services.project_watcher_manager import get_project_watcher_manager
from models.project import ProjectState
from models.db_models import User
from utils.auth import get_current_user
from database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projects", tags=["projects"])

def get_project_service(db: Session = Depends(get_db)):
    apps_dir = os.getenv("APPLICATIONS_DIR", "./applications")
    return ProjectService(Path(apps_dir), db=db)

class CreateProjectRequest(BaseModel):
    institution: str
    position: str
    date: str

@router.post("", response_model=ProjectState)
async def create_project(
    request: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    project_id = service.create_project(
        institution=request.institution,
        position=request.position,
        date=request.date,
        owner_id=current_user.id
    )

    # Get the created project state
    project_path = service.applications_dir / project_id
    state_file = project_path / ".project-state.json"

    import json
    try:
        state_data = json.loads(state_file.read_text())
        return ProjectState(**state_data)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse project state JSON: {e}", extra={
            'project_id': project_id,
            'state_file': str(state_file)
        })
        logger.debug(f"Invalid JSON content: {state_file.read_text()[:200]}")
        raise HTTPException(
            status_code=500,
            detail=f"Invalid project state file: {e}"
        )

@router.get("", response_model=List[ProjectState])
async def list_projects(
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    return service.list_projects(owner_id=current_user.id)

@router.post("/{project_id}/watch")
async def start_watching_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    """Start watching project directory for file changes"""
    # Verify project ownership
    project = service.get_project(project_id, owner_id=current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized")

    manager = get_project_watcher_manager()
    await manager.start_watching_project(project_id)
    return {"status": "watching", "project_id": project_id}

@router.delete("/{project_id}/watch")
async def stop_watching_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    """Stop watching project directory"""
    # Verify project ownership
    project = service.get_project(project_id, owner_id=current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized")

    manager = get_project_watcher_manager()
    manager.stop_watching_project(project_id)
    return {"status": "stopped", "project_id": project_id}
