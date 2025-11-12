import pytest
from pathlib import Path
import tempfile
import shutil
import time
from services.watcher_service import WatcherService

@pytest.fixture
def temp_watch_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_watcher_detects_new_json_file(temp_watch_dir):
    detected_files = []

    def on_file_created(file_path):
        detected_files.append(file_path)

    watcher = WatcherService(temp_watch_dir, on_file_created)
    watcher.start()

    # Create a JSON file
    test_file = temp_watch_dir / "test.json"
    test_file.write_text('{"test": true}')

    # Give watcher time to detect
    time.sleep(0.5)

    watcher.stop()

    assert len(detected_files) == 1
    assert detected_files[0].name == "test.json"
