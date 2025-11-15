from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import os
import shutil
from utils.auth import get_current_user
from utils.security import validate_file_path

router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/upload/{project_id}")
async def upload_file(
    project_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    # Validate file path to prevent directory traversal attacks
    try:
        file_path = validate_file_path(project_path, file.filename, allow_dirs=False)
    except HTTPException:
        raise HTTPException(status_code=403, detail="Invalid file path")

    # Save uploaded file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "path": str(file_path),
        "size": file_path.stat().st_size
    }
