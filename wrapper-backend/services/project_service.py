from pathlib import Path
import json
from datetime import datetime
from typing import List
from models.project import ProjectState

class ProjectService:
    def __init__(self, applications_dir: Path):
        self.applications_dir = Path(applications_dir)
        self.applications_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, institution: str, position: str, date: str) -> str:
        # Generate project ID
        project_id = f"{institution.lower().replace(' ', '-')}-{position.lower().replace(' ', '-')}-{date}"
        project_path = self.applications_dir / project_id
        project_path.mkdir(parents=True, exist_ok=True)

        # Create initial project state
        state = ProjectState(
            project_id=project_id,
            institution=institution,
            position=position,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Save project state
        state_file = project_path / ".project-state.json"
        state_file.write_text(state.model_dump_json(indent=2))

        return project_id

    def list_projects(self) -> List[ProjectState]:
        projects = []
        for project_dir in self.applications_dir.iterdir():
            if project_dir.is_dir():
                state_file = project_dir / ".project-state.json"
                if state_file.exists():
                    state_data = json.loads(state_file.read_text())
                    projects.append(ProjectState(**state_data))
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)
