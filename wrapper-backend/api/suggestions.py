from fastapi import APIRouter, Depends, HTTPException
from services.suggestions_service import SuggestionsService
from services.project_service import ProjectService
from utils.auth import get_current_user
from utils.security import validate_file_path
from models.db_models import User
from database import SessionLocal
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/suggestions", tags=["suggestions"])

def get_suggestions_service():
    return SuggestionsService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_project_service(db = Depends(get_db)):
    applications_dir = os.getenv("APPLICATIONS_DIR", "applications")
    return ProjectService(applications_dir=applications_dir, db=db)

@router.get("/{project_id}/next-steps")
async def get_next_steps(
    project_id: str,
    current_user: User = Depends(get_current_user),
    service: SuggestionsService = Depends(get_suggestions_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """Get smart suggestions for next steps"""
    # Verify ownership
    project = project_service.get_project(project_id, owner_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build project context by checking files in directory
    applications_dir = Path(os.getenv("APPLICATIONS_DIR", "applications"))
    project_path = applications_dir / project_id

    files = []
    if project_path.exists():
        files = [f.name for f in project_path.iterdir() if f.is_file() and not f.name.startswith('.')]

    project_context = {
        'project_id': project_id,
        'institution': project.institution,
        'position': project.position,
        'current_stage': project.current_stage,
        'job_posting_uploaded': len(files) > 0,
        'job_analysis_complete': any('job-analysis' in f.lower() or '01-' in f for f in files),
        'resume_aligned': any('resume' in f.lower() or 'alignment' in f.lower() for f in files),
        'cover_letter_drafted': any('cover-letter' in f.lower() or 'cover_letter' in f.lower() for f in files),
        'completed_files': files
    }

    suggestions = service.get_next_steps(project_context)

    logger.info("Generated suggestions", extra={
        'project_id': project_id,
        'suggestion_count': len(suggestions)
    })

    return {'suggestions': suggestions}

@router.post("/{project_id}/analyze-document")
async def analyze_document(
    project_id: str,
    document_type: str,
    filename: str,
    current_user: User = Depends(get_current_user),
    service: SuggestionsService = Depends(get_suggestions_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """Analyze document quality and get improvement suggestions"""
    # Verify ownership
    project = project_service.get_project(project_id, owner_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Read document content
    applications_dir = Path(os.getenv("APPLICATIONS_DIR", "applications"))
    project_path = applications_dir / project_id

    # Validate file path to prevent path traversal attacks
    try:
        file_path = validate_file_path(project_path, filename, allow_dirs=False)
    except HTTPException:
        raise HTTPException(status_code=403, detail="Access to this file is not allowed")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    content = file_path.read_text()
    analysis = service.analyze_document_quality(document_type, content)

    logger.info("Document analyzed", extra={
        'project_id': project_id,
        'document_type': document_type,
        'filename': filename,
        'quality_score': analysis.get('quality_score', 0)
    })

    return analysis
