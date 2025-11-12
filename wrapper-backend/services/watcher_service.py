from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import asyncio

class ProjectFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Path], None], loop: Optional[asyncio.AbstractEventLoop] = None):
        self.callback = callback
        self.loop = loop or asyncio.get_event_loop()

    def on_created(self, event: FileCreatedEvent):
        if not event.is_directory:
            file_path = Path(event.src_path)
            # Only notify for JSON, markdown, and PDF files
            if file_path.suffix in ['.json', '.md', '.pdf']:
                # Schedule callback in event loop
                if asyncio.iscoroutinefunction(self.callback):
                    asyncio.run_coroutine_threadsafe(
                        self.callback(file_path),
                        self.loop
                    )
                else:
                    self.callback(file_path)

class WatcherService:
    def __init__(self, watch_path: Path, on_file_created: Callable[[Path], None], loop: Optional[asyncio.AbstractEventLoop] = None):
        self.watch_path = Path(watch_path)
        self.observer = Observer()
        self.handler = ProjectFileHandler(on_file_created, loop)
        self.is_watching = False

    def start(self):
        if not self.is_watching:
            self.observer.schedule(self.handler, str(self.watch_path), recursive=True)
            self.observer.start()
            self.is_watching = True

    def stop(self):
        if self.is_watching:
            self.observer.stop()
            self.observer.join()
            self.is_watching = False

    def __del__(self):
        self.stop()
