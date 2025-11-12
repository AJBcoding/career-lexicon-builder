from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import os
from services.preview_service import PreviewService

router = APIRouter(prefix="/api/preview", tags=["preview"])

def get_preview_service():
    apps_dir = os.getenv("APPLICATIONS_DIR", "./applications")
    return PreviewService(Path(apps_dir))

@router.get("/html/{project_id}/{filename}", response_class=HTMLResponse)
async def preview_html(
    project_id: str,
    filename: str,
    service: PreviewService = Depends(get_preview_service)
):
    """Convert markdown file to HTML for preview"""
    html_content = service.markdown_to_html(project_id, filename)

    if html_content is None:
        raise HTTPException(status_code=404, detail="File not found or cannot be converted")

    return HTMLResponse(content=html_content)

@router.get("/pdf/{project_id}/{filename}")
async def preview_pdf(
    project_id: str,
    filename: str,
    service: PreviewService = Depends(get_preview_service)
):
    """Serve PDF file for preview"""
    pdf_path = service.get_pdf_path(project_id, filename)

    if pdf_path is None:
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name
    )
