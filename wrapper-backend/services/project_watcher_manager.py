from pathlib import Path
from typing import Dict
from services.watcher_service import WatcherService
from api.websocket import get_connection_manager
import asyncio
import os

class ProjectWatcherManager:
    def __init__(self):
        self.watchers: Dict[str, WatcherService] = {}
        self.applications_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))

    async def start_watching_project(self, project_id: str):
        """Start watching a project directory"""
        if project_id in self.watchers:
            return  # Already watching

        project_path = self.applications_dir / project_id
        if not project_path.exists():
            return

        async def on_file_created(file_path: Path):
            """Callback when file is created"""
            manager = get_connection_manager()
            await manager.broadcast_to_project(
                {
                    "type": "file_created",
                    "project_id": project_id,
                    "filename": file_path.name,
                    "path": str(file_path.relative_to(project_path)),
                    "extension": file_path.suffix
                },
                project_id
            )

        loop = asyncio.get_event_loop()
        watcher = WatcherService(project_path, on_file_created, loop)
        watcher.start()
        self.watchers[project_id] = watcher

    def stop_watching_project(self, project_id: str):
        """Stop watching a project directory"""
        if project_id in self.watchers:
            self.watchers[project_id].stop()
            del self.watchers[project_id]

    def stop_all(self):
        """Stop all watchers"""
        for project_id in list(self.watchers.keys()):
            self.stop_watching_project(project_id)

# Global manager instance
_manager = ProjectWatcherManager()

def get_project_watcher_manager():
    return _manager
