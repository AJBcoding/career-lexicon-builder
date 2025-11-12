from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import os
import shutil

router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile = File(...)):
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    # Save uploaded file
    file_path = project_path / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "path": str(file_path),
        "size": file_path.stat().st_size
    }
