from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectState(BaseModel):
    project_id: str
    institution: str
    position: str
    created_at: datetime
    updated_at: datetime
    current_stage: str = "created"
    current_versions: dict = {}
    history: List[dict] = []
    notes: str = ""
