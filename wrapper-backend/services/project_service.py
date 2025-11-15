from pathlib import Path
import json
from datetime import datetime
from typing import List, Optional
from models.project import ProjectState
from models.db_models import Project
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class ProjectService:
    def __init__(self, applications_dir: Path, db: Optional[Session] = None):
        self.applications_dir = Path(applications_dir)
        self.applications_dir.mkdir(parents=True, exist_ok=True)
        self.db = db

    def create_project(self, institution: str, position: str, date: str, owner_id: Optional[int] = None) -> str:
        # Generate project ID
        project_id = f"{institution.lower().replace(' ', '-')}-{position.lower().replace(' ', '-')}-{date}"
        project_path = self.applications_dir / project_id

        logger.info("Creating project", extra={
            'project_id': project_id,
            'institution': institution,
            'position': position,
            'owner_id': owner_id
        })

        try:
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

            # Store in database if db session provided
            if self.db and owner_id is not None:
                db_project = Project(
                    project_id=project_id,
                    institution=institution,
                    position=position,
                    current_stage="created",
                    owner_id=owner_id
                )
                self.db.add(db_project)
                self.db.commit()
                self.db.refresh(db_project)

            logger.info("Project created successfully", extra={
                'project_id': project_id,
                'project_path': str(project_path)
            })

            return project_id
        except Exception as e:
            logger.error("Project creation failed", extra={
                'project_id': project_id,
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)
            raise

    def list_projects(self, owner_id: Optional[int] = None) -> List[ProjectState]:
        logger.debug("Listing projects", extra={'owner_id': owner_id})

        projects = []

        try:
            # If owner_id provided and db available, filter by ownership
            if owner_id is not None and self.db:
                db_projects = self.db.query(Project).filter(Project.owner_id == owner_id).all()
                project_ids = {p.project_id for p in db_projects}

                for project_dir in self.applications_dir.iterdir():
                    if project_dir.is_dir() and project_dir.name in project_ids:
                        state_file = project_dir / ".project-state.json"
                        if state_file.exists():
                            try:
                                state_data = json.loads(state_file.read_text())
                                projects.append(ProjectState(**state_data))
                            except json.JSONDecodeError as e:
                                logger.error(f"Failed to parse project state JSON: {e}", extra={
                                    'project_id': project_dir.name,
                                    'state_file': str(state_file)
                                })
                                logger.debug(f"Invalid JSON content: {state_file.read_text()[:200]}")
                                # Skip this project and continue with others
                                continue
            else:
                # No filtering - list all projects
                for project_dir in self.applications_dir.iterdir():
                    if project_dir.is_dir():
                        state_file = project_dir / ".project-state.json"
                        if state_file.exists():
                            try:
                                state_data = json.loads(state_file.read_text())
                                projects.append(ProjectState(**state_data))
                            except json.JSONDecodeError as e:
                                logger.error(f"Failed to parse project state JSON: {e}", extra={
                                    'project_id': project_dir.name,
                                    'state_file': str(state_file)
                                })
                                logger.debug(f"Invalid JSON content: {state_file.read_text()[:200]}")
                                # Skip this project and continue with others
                                continue

            logger.info("Projects listed", extra={
                'count': len(projects),
                'owner_id': owner_id
            })

            return sorted(projects, key=lambda p: p.updated_at, reverse=True)
        except Exception as e:
            logger.error("Failed to list projects", extra={
                'owner_id': owner_id,
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)
            raise

    def get_project(self, project_id: str, owner_id: Optional[int] = None) -> Optional[Project]:
        """Get project from database with optional ownership verification"""
        if not self.db:
            return None

        query = self.db.query(Project).filter(Project.project_id == project_id)

        if owner_id is not None:
            query = query.filter(Project.owner_id == owner_id)

        return query.first()
