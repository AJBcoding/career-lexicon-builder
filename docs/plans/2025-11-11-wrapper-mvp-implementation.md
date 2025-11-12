# Wrapper Application MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build web-based GUI wrapper for career-lexicon-builder that enables fast job application document creation

**Architecture:** Python/FastAPI backend shells out to Claude Code CLI, React frontend with progressive preview, JSON as canonical format for all documents

**Tech Stack:** FastAPI, React, Vite, Monaco Editor, PDF.js, Watchdog, WebSockets

**Parallelization Strategy:** Tasks marked with `[PARALLEL GROUP N]` can be executed simultaneously by different agents

---

## PARALLEL GROUP 1: Project Infrastructure Setup

### Task 1A: Backend Project Structure [PARALLEL GROUP 1]

**Files:**
- Create: `wrapper-backend/main.py`
- Create: `wrapper-backend/requirements.txt`
- Create: `wrapper-backend/api/__init__.py`
- Create: `wrapper-backend/services/__init__.py`
- Create: `wrapper-backend/models/__init__.py`
- Create: `wrapper-backend/.env.example`

**Step 1: Create backend directory structure**

```bash
mkdir -p wrapper-backend/{api,services,models,tests}
touch wrapper-backend/{main.py,requirements.txt,__init__.py}
touch wrapper-backend/api/__init__.py
touch wrapper-backend/services/__init__.py
touch wrapper-backend/models/__init__.py
```

**Step 2: Write requirements.txt**

Create `wrapper-backend/requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
watchdog==3.0.0
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
websockets==12.0
```

**Step 3: Create basic FastAPI app**

Create `wrapper-backend/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Career Lexicon Wrapper API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Step 4: Create environment example**

Create `wrapper-backend/.env.example`:
```
APPLICATIONS_DIR=/path/to/applications
CLAUDE_CODE_PATH=claude
```

**Step 5: Test backend starts**

Run: `cd wrapper-backend && python main.py`
Expected: Server starts on http://0.0.0.0:8000

Visit: `http://localhost:8000/health`
Expected: `{"status": "healthy"}`

**Step 6: Commit**

```bash
git add wrapper-backend/
git commit -m "feat: create backend project structure with FastAPI"
```

---

### Task 1B: Frontend Project Structure [PARALLEL GROUP 1]

**Files:**
- Create: `wrapper-frontend/` (entire React app via Vite)

**Step 1: Create React app with Vite**

```bash
npm create vite@latest wrapper-frontend -- --template react
cd wrapper-frontend
npm install
```

**Step 2: Install additional dependencies**

```bash
npm install @monaco-editor/react react-pdf axios zustand react-router-dom
```

**Step 3: Configure API base URL**

Create `wrapper-frontend/src/config.js`:
```javascript
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

Create `wrapper-frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

**Step 4: Test frontend starts**

Run: `npm run dev`
Expected: Dev server starts on http://localhost:5173

**Step 5: Create basic health check integration**

Create `wrapper-frontend/src/services/api.js`:
```javascript
import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
```

**Step 6: Test health check from frontend**

Modify `wrapper-frontend/src/App.jsx`:
```javascript
import { useState, useEffect } from 'react';
import { healthCheck } from './services/api';

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    healthCheck().then(setHealth).catch(console.error);
  }, []);

  return (
    <div>
      <h1>Career Lexicon Wrapper</h1>
      <p>Backend Status: {health?.status || 'connecting...'}</p>
    </div>
  );
}

export default App;
```

Run both: backend (`python main.py`) and frontend (`npm run dev`)
Expected: Page shows "Backend Status: healthy"

**Step 7: Commit**

```bash
git add wrapper-frontend/
git commit -m "feat: create frontend project structure with React/Vite"
```

---

## PARALLEL GROUP 2: Core Backend Services

### Task 2A: Project Management Service [PARALLEL GROUP 2]

**Files:**
- Create: `wrapper-backend/models/project.py`
- Create: `wrapper-backend/services/project_service.py`
- Create: `wrapper-backend/tests/test_project_service.py`

**Step 1: Write failing test for project creation**

Create `wrapper-backend/tests/test_project_service.py`:
```python
import pytest
from pathlib import Path
import tempfile
import shutil
from services.project_service import ProjectService

@pytest.fixture
def temp_apps_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_create_project_creates_directory_structure(temp_apps_dir):
    service = ProjectService(temp_apps_dir)
    project_id = service.create_project(
        institution="UCLA",
        position="Assistant Dean",
        date="2024-11-15"
    )

    project_path = temp_apps_dir / project_id
    assert project_path.exists()
    assert (project_path / ".project-state.json").exists()
```

**Step 2: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_project_service.py::test_create_project_creates_directory_structure -v`
Expected: FAIL with "No module named 'services.project_service'"

**Step 3: Write Project model**

Create `wrapper-backend/models/project.py`:
```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectState(BaseModel):
    project_id: str
    institution: str
    position: str
    created_at: datetime
    updated_at: datetime
    current_stage: str = "created"  # created, analyzing, drafting, formatting, complete
    current_versions: dict = {}
    history: List[dict] = []
    notes: str = ""
```

**Step 4: Write minimal ProjectService implementation**

Create `wrapper-backend/services/project_service.py`:
```python
from pathlib import Path
import json
from datetime import datetime
from models.project import ProjectState

class ProjectService:
    def __init__(self, applications_dir: Path):
        self.applications_dir = Path(applications_dir)
        self.applications_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, institution: str, position: str, date: str) -> str:
        # Generate project ID: institution-position-date
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
```

**Step 5: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_project_service.py::test_create_project_creates_directory_structure -v`
Expected: PASS

**Step 6: Add test for listing projects**

Add to `wrapper-backend/tests/test_project_service.py`:
```python
def test_list_projects_returns_all_projects(temp_apps_dir):
    service = ProjectService(temp_apps_dir)
    service.create_project("UCLA", "Assistant Dean", "2024-11-15")
    service.create_project("USC", "Director", "2024-11-16")

    projects = service.list_projects()
    assert len(projects) == 2
    assert any(p.institution == "UCLA" for p in projects)
    assert any(p.institution == "USC" for p in projects)
```

**Step 7: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_project_service.py::test_list_projects_returns_all_projects -v`
Expected: FAIL with "ProjectService has no attribute 'list_projects'"

**Step 8: Implement list_projects**

Add to `wrapper-backend/services/project_service.py`:
```python
    def list_projects(self) -> List[ProjectState]:
        projects = []
        for project_dir in self.applications_dir.iterdir():
            if project_dir.is_dir():
                state_file = project_dir / ".project-state.json"
                if state_file.exists():
                    state_data = json.loads(state_file.read_text())
                    projects.append(ProjectState(**state_data))
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)
```

Add import at top:
```python
from typing import List
```

**Step 9: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_project_service.py -v`
Expected: All tests PASS

**Step 10: Commit**

```bash
git add wrapper-backend/models/project.py wrapper-backend/services/project_service.py wrapper-backend/tests/test_project_service.py
git commit -m "feat: add project management service with create and list"
```

---

### Task 2B: Skill Invocation Service [PARALLEL GROUP 2]

**Files:**
- Create: `wrapper-backend/services/skill_service.py`
- Create: `wrapper-backend/tests/test_skill_service.py`

**Step 1: Write failing test for skill invocation**

Create `wrapper-backend/tests/test_skill_service.py`:
```python
import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch
from services.skill_service import SkillService

@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_invoke_skill_calls_claude_code(temp_project_dir):
    service = SkillService(claude_path="claude")

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")

        result = service.invoke_skill(
            skill_name="analyze-job-posting",
            project_path=temp_project_dir,
            prompt="Analyze the job posting"
        )

        assert result["success"] is True
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "claude" in call_args
        assert "analyze-job-posting" in " ".join(call_args)
```

**Step 2: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_skill_service.py::test_invoke_skill_calls_claude_code -v`
Expected: FAIL with "No module named 'services.skill_service'"

**Step 3: Write minimal SkillService implementation**

Create `wrapper-backend/services/skill_service.py`:
```python
import subprocess
from pathlib import Path
from typing import Dict, Any

class SkillService:
    def __init__(self, claude_path: str = "claude"):
        self.claude_path = claude_path

    def invoke_skill(
        self,
        skill_name: str,
        project_path: Path,
        prompt: str
    ) -> Dict[str, Any]:
        """Invoke a Claude Code skill in the project directory"""
        cmd = [
            self.claude_path,
            "--skill", skill_name,
            prompt
        ]

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
```

**Step 4: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_skill_service.py::test_invoke_skill_calls_claude_code -v`
Expected: PASS

**Step 5: Add test for skill invocation with working directory**

Add to `wrapper-backend/tests/test_skill_service.py`:
```python
def test_invoke_skill_uses_project_working_directory(temp_project_dir):
    service = SkillService(claude_path="claude")

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")

        service.invoke_skill(
            skill_name="test-skill",
            project_path=temp_project_dir,
            prompt="Test prompt"
        )

        call_kwargs = mock_run.call_args[1]
        assert call_kwargs['cwd'] == temp_project_dir
```

**Step 6: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_skill_service.py -v`
Expected: All tests PASS

**Step 7: Commit**

```bash
git add wrapper-backend/services/skill_service.py wrapper-backend/tests/test_skill_service.py
git commit -m "feat: add skill invocation service for Claude Code CLI"
```

---

### Task 2C: File Watcher Service [PARALLEL GROUP 2]

**Files:**
- Create: `wrapper-backend/services/watcher_service.py`
- Create: `wrapper-backend/tests/test_watcher_service.py`

**Step 1: Write failing test for file watching**

Create `wrapper-backend/tests/test_watcher_service.py`:
```python
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
```

**Step 2: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_watcher_service.py::test_watcher_detects_new_json_file -v`
Expected: FAIL with "No module named 'services.watcher_service'"

**Step 3: Write minimal WatcherService implementation**

Create `wrapper-backend/services/watcher_service.py`:
```python
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
```

**Step 4: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_watcher_service.py::test_watcher_detects_new_json_file -v`
Expected: PASS

**Step 5: Commit**

```bash
git add wrapper-backend/services/watcher_service.py wrapper-backend/tests/test_watcher_service.py
git commit -m "feat: add file watcher service for detecting skill outputs"
```

---

## PARALLEL GROUP 3: API Endpoints

### Task 3A: Projects API Endpoints [PARALLEL GROUP 3]

**Files:**
- Create: `wrapper-backend/api/projects.py`
- Modify: `wrapper-backend/main.py`
- Create: `wrapper-backend/tests/test_api_projects.py`

**Step 1: Write failing test for create project endpoint**

Create `wrapper-backend/tests/test_api_projects.py`:
```python
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from main import app

@pytest.fixture
def temp_apps_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("APPLICATIONS_DIR", temp_dir)
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def client():
    return TestClient(app)

def test_create_project_endpoint(client, temp_apps_dir):
    response = client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })

    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["institution"] == "UCLA"
```

**Step 2: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_api_projects.py::test_create_project_endpoint -v`
Expected: FAIL with 404 (endpoint doesn't exist)

**Step 3: Create projects API router**

Create `wrapper-backend/api/projects.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from pathlib import Path
import os
from services.project_service import ProjectService
from models.project import ProjectState

router = APIRouter(prefix="/api/projects", tags=["projects"])

def get_project_service():
    apps_dir = os.getenv("APPLICATIONS_DIR", "./applications")
    return ProjectService(Path(apps_dir))

class CreateProjectRequest(BaseModel):
    institution: str
    position: str
    date: str

@router.post("", response_model=ProjectState)
async def create_project(
    request: CreateProjectRequest,
    service: ProjectService = Depends(get_project_service)
):
    project_id = service.create_project(
        institution=request.institution,
        position=request.position,
        date=request.date
    )

    # Get the created project state
    project_path = service.applications_dir / project_id
    state_file = project_path / ".project-state.json"

    import json
    state_data = json.loads(state_file.read_text())
    return ProjectState(**state_data)

@router.get("", response_model=List[ProjectState])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()
```

**Step 4: Register router in main.py**

Modify `wrapper-backend/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.projects import router as projects_router

app = FastAPI(title="Career Lexicon Wrapper API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Step 5: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_api_projects.py::test_create_project_endpoint -v`
Expected: PASS

**Step 6: Add test for list projects endpoint**

Add to `wrapper-backend/tests/test_api_projects.py`:
```python
def test_list_projects_endpoint(client, temp_apps_dir):
    # Create two projects
    client.post("/api/projects", json={
        "institution": "UCLA",
        "position": "Assistant Dean",
        "date": "2024-11-15"
    })
    client.post("/api/projects", json={
        "institution": "USC",
        "position": "Director",
        "date": "2024-11-16"
    })

    # List projects
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 2
```

**Step 7: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_api_projects.py -v`
Expected: All tests PASS

**Step 8: Commit**

```bash
git add wrapper-backend/api/projects.py wrapper-backend/main.py wrapper-backend/tests/test_api_projects.py
git commit -m "feat: add projects API endpoints (create, list)"
```

---

### Task 3B: Skills API Endpoints [PARALLEL GROUP 3]

**Files:**
- Create: `wrapper-backend/api/skills.py`
- Modify: `wrapper-backend/main.py`
- Create: `wrapper-backend/tests/test_api_skills.py`

**Step 1: Write failing test for invoke skill endpoint**

Create `wrapper-backend/tests/test_api_skills.py`:
```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_invoke_skill_endpoint(client):
    with patch('services.skill_service.SkillService.invoke_skill') as mock_invoke:
        mock_invoke.return_value = {
            "success": True,
            "stdout": "Analysis complete",
            "stderr": "",
            "returncode": 0
        }

        response = client.post("/api/skills/invoke", json={
            "project_id": "test-project",
            "skill_name": "analyze-job-posting",
            "prompt": "Analyze this job"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
```

**Step 2: Run test to verify it fails**

Run: `cd wrapper-backend && pytest tests/test_api_skills.py::test_invoke_skill_endpoint -v`
Expected: FAIL with 404 (endpoint doesn't exist)

**Step 3: Create skills API router**

Create `wrapper-backend/api/skills.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import os
from services.skill_service import SkillService

router = APIRouter(prefix="/api/skills", tags=["skills"])

def get_skill_service():
    claude_path = os.getenv("CLAUDE_CODE_PATH", "claude")
    return SkillService(claude_path)

class InvokeSkillRequest(BaseModel):
    project_id: str
    skill_name: str
    prompt: str

@router.post("/invoke")
async def invoke_skill(
    request: InvokeSkillRequest,
    service: SkillService = Depends(get_skill_service)
):
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    project_path = apps_dir / request.project_id

    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    result = service.invoke_skill(
        skill_name=request.skill_name,
        project_path=project_path,
        prompt=request.prompt
    )

    return result
```

**Step 4: Register router in main.py**

Modify `wrapper-backend/main.py` to add:
```python
from api.skills import router as skills_router

# After projects router
app.include_router(skills_router)
```

**Step 5: Run test to verify it passes**

Run: `cd wrapper-backend && pytest tests/test_api_skills.py::test_invoke_skill_endpoint -v`
Expected: PASS

**Step 6: Commit**

```bash
git add wrapper-backend/api/skills.py wrapper-backend/main.py wrapper-backend/tests/test_api_skills.py
git commit -m "feat: add skills API endpoint for invoking Claude Code"
```

---

## PARALLEL GROUP 4: Frontend Components

### Task 4A: Project Dashboard Component [PARALLEL GROUP 4]

**Files:**
- Create: `wrapper-frontend/src/components/ProjectDashboard.jsx`
- Create: `wrapper-frontend/src/services/projectService.js`
- Modify: `wrapper-frontend/src/App.jsx`

**Step 1: Create project API service**

Create `wrapper-frontend/src/services/projectService.js`:
```javascript
import api from './api';

export const createProject = async (institution, position, date) => {
  const response = await api.post('/api/projects', {
    institution,
    position,
    date,
  });
  return response.data;
};

export const listProjects = async () => {
  const response = await api.get('/api/projects');
  return response.data;
};
```

**Step 2: Create ProjectDashboard component**

Create `wrapper-frontend/src/components/ProjectDashboard.jsx`:
```javascript
import { useState, useEffect } from 'react';
import { listProjects, createProject } from '../services/projectService';

function ProjectDashboard({ onSelectProject }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    institution: '',
    position: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await listProjects();
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      const newProject = await createProject(
        formData.institution,
        formData.position,
        formData.date
      );
      setProjects([newProject, ...projects]);
      setShowCreateForm(false);
      setFormData({ institution: '', position: '', date: new Date().toISOString().split('T')[0] });
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  if (loading) return <div>Loading projects...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Job Applications</h1>
        <button onClick={() => setShowCreateForm(!showCreateForm)}>
          {showCreateForm ? 'Cancel' : 'New Project'}
        </button>
      </div>

      {showCreateForm && (
        <form onSubmit={handleCreateProject} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc' }}>
          <div style={{ marginBottom: '10px' }}>
            <label>Institution:</label>
            <input
              type="text"
              value={formData.institution}
              onChange={(e) => setFormData({ ...formData, institution: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Position:</label>
            <input
              type="text"
              value={formData.position}
              onChange={(e) => setFormData({ ...formData, position: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Date:</label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <button type="submit">Create Project</button>
        </form>
      )}

      <div>
        {projects.length === 0 ? (
          <p>No projects yet. Create your first job application project!</p>
        ) : (
          <div style={{ display: 'grid', gap: '15px' }}>
            {projects.map((project) => (
              <div
                key={project.project_id}
                onClick={() => onSelectProject(project)}
                style={{
                  padding: '15px',
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  '&:hover': { backgroundColor: '#f5f5f5' }
                }}
              >
                <h3>{project.institution} - {project.position}</h3>
                <p>Status: {project.current_stage}</p>
                <p>Updated: {new Date(project.updated_at).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProjectDashboard;
```

**Step 3: Update App.jsx to use ProjectDashboard**

Modify `wrapper-frontend/src/App.jsx`:
```javascript
import { useState } from 'react';
import ProjectDashboard from './components/ProjectDashboard';

function App() {
  const [selectedProject, setSelectedProject] = useState(null);

  if (selectedProject) {
    return (
      <div>
        <button onClick={() => setSelectedProject(null)}>← Back to Dashboard</button>
        <h2>Project: {selectedProject.institution} - {selectedProject.position}</h2>
        <p>Project workspace coming soon...</p>
      </div>
    );
  }

  return <ProjectDashboard onSelectProject={setSelectedProject} />;
}

export default App;
```

**Step 4: Test manually**

Run backend: `cd wrapper-backend && python main.py`
Run frontend: `cd wrapper-frontend && npm run dev`

Test:
1. Visit http://localhost:5173
2. Click "New Project"
3. Fill in form and create project
4. Verify project appears in list

**Step 5: Commit**

```bash
git add wrapper-frontend/src/components/ProjectDashboard.jsx wrapper-frontend/src/services/projectService.js wrapper-frontend/src/App.jsx
git commit -m "feat: add project dashboard with create and list functionality"
```

---

### Task 4B: File Upload Component [PARALLEL GROUP 4]

**Files:**
- Create: `wrapper-frontend/src/components/FileUpload.jsx`
- Create: `wrapper-backend/api/files.py`
- Modify: `wrapper-backend/main.py`

**Step 1: Create file upload API endpoint**

Create `wrapper-backend/api/files.py`:
```python
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
```

Register in `wrapper-backend/main.py`:
```python
from api.files import router as files_router
app.include_router(files_router)
```

**Step 2: Create FileUpload component**

Create `wrapper-frontend/src/components/FileUpload.jsx`:
```javascript
import { useState } from 'react';
import api from '../services/api';

function FileUpload({ projectId, onUploadComplete }) {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = async (files) => {
    if (!files || files.length === 0) return;

    setUploading(true);
    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        await api.post(`/api/files/upload/${projectId}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      if (onUploadComplete) onUploadComplete();
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      style={{
        border: `2px dashed ${dragOver ? '#007bff' : '#ccc'}`,
        borderRadius: '5px',
        padding: '40px',
        textAlign: 'center',
        backgroundColor: dragOver ? '#f0f8ff' : 'white',
        cursor: 'pointer'
      }}
    >
      {uploading ? (
        <p>Uploading...</p>
      ) : (
        <>
          <p>Drag and drop files here, or click to select</p>
          <input
            type="file"
            multiple
            onChange={(e) => handleFileSelect(e.target.files)}
            style={{ display: 'none' }}
            id="file-input"
          />
          <label htmlFor="file-input" style={{ cursor: 'pointer', color: '#007bff' }}>
            Select Files
          </label>
        </>
      )}
    </div>
  );
}

export default FileUpload;
```

**Step 3: Test manually**

1. Open a project
2. Add FileUpload component to workspace
3. Upload a PDF
4. Verify file appears in project folder

**Step 4: Commit**

```bash
git add wrapper-frontend/src/components/FileUpload.jsx wrapper-backend/api/files.py wrapper-backend/main.py
git commit -m "feat: add file upload component with drag-and-drop"
```

---

## Task 5: Skill Modifications (Sequential - requires existing skills)

### Task 5A: Add JSON Export to job-description-analysis Skill

**Files:**
- Modify: `.claude/skills/job-description-analysis/SKILL.md` (or wherever skill is located)

**Step 1: Locate the skill file**

Run: `find . -name "*job*description*" -type f`
Expected: Find the skill markdown file

**Step 2: Read current skill**

Read the skill file to understand current structure

**Step 3: Add JSON export instructions**

Add to end of skill (before final user presentation):
```markdown
## Save Analysis as JSON

After presenting your analysis to the user, save it in a structured JSON format.

Create a file named `job-analysis-v1.json` (or increment version if file exists).

Structure:
```json
{
  "metadata": {
    "created_at": "ISO timestamp",
    "input_file": "job-posting.pdf",
    "version": 1
  },
  "institution": "Name of institution",
  "position": "Position title",
  "requirements": {
    "required": ["requirement 1", "requirement 2"],
    "preferred": ["preference 1", "preference 2"]
  },
  "culture": {
    "values": ["value 1", "value 2"],
    "keywords": ["keyword 1", "keyword 2"]
  },
  "key_responsibilities": ["responsibility 1", "responsibility 2"]
}
```

Save this file to the current working directory.
```

**Step 4: Test the modified skill**

Create a test project and run the skill:
```bash
mkdir -p applications/test-skill
cd applications/test-skill
echo "Test job posting" > job-posting.txt
claude --skill job-description-analysis "Analyze job-posting.txt"
```

Expected: `job-analysis-v1.json` file created with proper structure

**Step 5: Commit**

```bash
git add .claude/skills/job-description-analysis/
git commit -m "feat: add JSON export to job-description-analysis skill"
```

---

## Task 6: Integration & End-to-End Testing

### Task 6A: Wire Frontend to Backend for Complete Workflow

**Files:**
- Create: `wrapper-frontend/src/components/ProjectWorkspace.jsx`
- Modify: `wrapper-frontend/src/App.jsx`

**Step 1: Create ProjectWorkspace component**

Create `wrapper-frontend/src/components/ProjectWorkspace.jsx`:
```javascript
import { useState } from 'react';
import FileUpload from './FileUpload';
import api from '../services/api';

function ProjectWorkspace({ project, onBack }) {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyzeJob = async () => {
    setProcessing(true);
    try {
      const response = await api.post('/api/skills/invoke', {
        project_id: project.project_id,
        skill_name: 'job-description-analysis',
        prompt: 'Analyze the job posting and save the analysis as JSON'
      });
      setResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Failed to analyze job posting');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={onBack} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      <h2>{project.institution} - {project.position}</h2>
      <p>Status: {project.current_stage}</p>

      <div style={{ marginTop: '30px' }}>
        <h3>Upload Job Posting</h3>
        <FileUpload
          projectId={project.project_id}
          onUploadComplete={() => alert('File uploaded successfully')}
        />
      </div>

      <div style={{ marginTop: '30px' }}>
        <h3>Actions</h3>
        <button
          onClick={handleAnalyzeJob}
          disabled={processing}
          style={{ padding: '10px 20px' }}
        >
          {processing ? 'Analyzing...' : 'Analyze Job Posting'}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#f5f5f5' }}>
          <h3>Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ProjectWorkspace;
```

**Step 2: Update App.jsx to use ProjectWorkspace**

Modify `wrapper-frontend/src/App.jsx`:
```javascript
import { useState } from 'react';
import ProjectDashboard from './components/ProjectDashboard';
import ProjectWorkspace from './components/ProjectWorkspace';

function App() {
  const [selectedProject, setSelectedProject] = useState(null);

  if (selectedProject) {
    return (
      <ProjectWorkspace
        project={selectedProject}
        onBack={() => setSelectedProject(null)}
      />
    );
  }

  return <ProjectDashboard onSelectProject={setSelectedProject} />;
}

export default App;
```

**Step 3: End-to-end test**

1. Start backend and frontend
2. Create new project
3. Upload a job posting PDF
4. Click "Analyze Job Posting"
5. Verify JSON analysis is created in project folder
6. Verify result displayed in UI

**Step 4: Commit**

```bash
git add wrapper-frontend/src/components/ProjectWorkspace.jsx wrapper-frontend/src/App.jsx
git commit -m "feat: integrate project workspace with skill invocation"
```

---

## Task 7: Documentation & Deployment Prep

### Task 7A: Create Development Documentation

**Files:**
- Create: `wrapper-backend/README.md`
- Create: `wrapper-frontend/README.md`
- Create: `WRAPPER_SETUP.md` (root)

**Step 1: Create backend README**

Create `wrapper-backend/README.md`:
```markdown
# Career Lexicon Wrapper - Backend

FastAPI backend that orchestrates Claude Code CLI for job application document generation.

## Setup

```bash
cd wrapper-backend
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure:
```
APPLICATIONS_DIR=/path/to/applications
CLAUDE_CODE_PATH=claude
```

## Run

Development:
```bash
python main.py
```

Production:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing

```bash
pytest
```

## API Documentation

When running, visit: http://localhost:8000/docs
```

**Step 2: Create frontend README**

Create `wrapper-frontend/README.md`:
```markdown
# Career Lexicon Wrapper - Frontend

React frontend for managing job application projects.

## Setup

```bash
cd wrapper-frontend
npm install
```

## Configuration

Create `.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Run

Development:
```bash
npm run dev
```

Build:
```bash
npm run build
```

## Features

- Project dashboard (create, list projects)
- File upload (drag-and-drop)
- Skill invocation (analyze job postings)
- Real-time progress updates
```

**Step 3: Create setup guide**

Create `WRAPPER_SETUP.md`:
```markdown
# Wrapper Application Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Claude Code CLI installed and configured

## Quick Start

1. **Backend Setup**
   ```bash
   cd wrapper-backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your paths
   python main.py
   ```

2. **Frontend Setup** (in new terminal)
   ```bash
   cd wrapper-frontend
   npm install
   npm run dev
   ```

3. **Access Application**

   Open http://localhost:5173

## First Project

1. Click "New Project"
2. Fill in institution, position, date
3. Upload job posting PDF
4. Click "Analyze Job Posting"
5. Check project folder for `job-analysis-v1.json`

## Troubleshooting

**Backend not starting:**
- Check APPLICATIONS_DIR exists
- Verify Claude Code is in PATH

**Skill invocation fails:**
- Ensure Claude Code CLI is configured
- Check project folder exists
- Verify skill name is correct

## Development

Run tests:
```bash
cd wrapper-backend && pytest
```

## Next Steps

See design doc: `docs/plans/2025-11-11-wrapper-application-design.md`
```

**Step 4: Commit**

```bash
git add wrapper-backend/README.md wrapper-frontend/README.md WRAPPER_SETUP.md
git commit -m "docs: add setup and development documentation"
```

---

## Execution Summary

**Total Tasks:** 19
**Parallelizable Tasks:**
- Group 1 (Tasks 1A, 1B): 2 tasks
- Group 2 (Tasks 2A, 2B, 2C): 3 tasks
- Group 3 (Tasks 3A, 3B): 2 tasks
- Group 4 (Tasks 4A, 4B): 2 tasks

**Sequential Tasks:**
- Task 5A: 1 task (requires skills to exist)
- Tasks 6A, 7A: 2 tasks (require previous completion)

**Estimated Time:**
- Parallel execution (4 groups): ~2-3 hours
- Sequential tasks: ~1 hour
- **Total: ~3-4 hours with parallel execution**

**Success Criteria:**
- All tests pass
- Can create project via UI
- Can upload file to project
- Can invoke skill and see JSON output
- Frontend displays results

---

## Post-MVP Enhancements

After MVP is complete, Phase 2 tasks include:
- Additional skills (outline, draft, format)
- Live preview (HTML + progressive PDF)
- Version history UI
- Natural language routing
- Resume alignment workflow

See design doc for full Phase 2/3 roadmap.
