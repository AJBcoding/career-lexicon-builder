from pathlib import Path
from typing import Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class ProjectFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Path], None]):
        self.callback = callback

    def on_created(self, event: FileCreatedEvent):
        if not event.is_directory:
            file_path = Path(event.src_path)
            # Only notify for JSON and markdown files
            if file_path.suffix in ['.json', '.md', '.pdf']:
                self.callback(file_path)

class WatcherService:
    def __init__(self, watch_path: Path, on_file_created: Callable[[Path], None]):
        self.watch_path = Path(watch_path)
        self.observer = Observer()
        self.handler = ProjectFileHandler(on_file_created)

    def start(self):
        self.observer.schedule(self.handler, str(self.watch_path), recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
