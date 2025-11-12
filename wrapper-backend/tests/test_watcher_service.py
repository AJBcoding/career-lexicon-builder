import pytest
from pathlib import Path
import tempfile
import shutil
import time
import asyncio
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

@pytest.mark.asyncio
async def test_watcher_with_async_callback(temp_watch_dir):
    detected_files = []

    async def on_file_created(file_path):
        detected_files.append(file_path)

    loop = asyncio.get_event_loop()
    watcher = WatcherService(temp_watch_dir, on_file_created, loop)
    watcher.start()

    # Create a JSON file
    test_file = temp_watch_dir / "async-test.json"
    test_file.write_text('{"test": true}')

    # Give watcher time to detect
    await asyncio.sleep(0.5)

    watcher.stop()

    assert len(detected_files) == 1
    assert detected_files[0].name == "async-test.json"

@pytest.mark.asyncio
async def test_watcher_detects_markdown_files(temp_watch_dir):
    detected_files = []

    async def on_file_created(file_path):
        detected_files.append(file_path)

    loop = asyncio.get_event_loop()
    watcher = WatcherService(temp_watch_dir, on_file_created, loop)
    watcher.start()

    # Create markdown and PDF files
    md_file = temp_watch_dir / "test.md"
    md_file.write_text("# Test")

    pdf_file = temp_watch_dir / "test.pdf"
    pdf_file.write_bytes(b"fake pdf content")

    # Give watcher time to detect
    await asyncio.sleep(0.5)

    watcher.stop()

    assert len(detected_files) == 2
    file_names = [f.name for f in detected_files]
    assert "test.md" in file_names
    assert "test.pdf" in file_names

@pytest.mark.asyncio
async def test_watcher_ignores_other_file_types(temp_watch_dir):
    detected_files = []

    async def on_file_created(file_path):
        detected_files.append(file_path)

    loop = asyncio.get_event_loop()
    watcher = WatcherService(temp_watch_dir, on_file_created, loop)
    watcher.start()

    # Create files that should be ignored
    txt_file = temp_watch_dir / "test.txt"
    txt_file.write_text("ignored")

    py_file = temp_watch_dir / "test.py"
    py_file.write_text("# ignored")

    # Give watcher time to detect (should detect nothing)
    await asyncio.sleep(0.5)

    watcher.stop()

    assert len(detected_files) == 0

def test_watcher_prevents_double_start(temp_watch_dir):
    detected_files = []

    def on_file_created(file_path):
        detected_files.append(file_path)

    watcher = WatcherService(temp_watch_dir, on_file_created)
    watcher.start()
    watcher.start()  # Should not raise error

    test_file = temp_watch_dir / "test.json"
    test_file.write_text('{"test": true}')

    time.sleep(0.5)

    watcher.stop()

    # Should only detect once
    assert len(detected_files) == 1
