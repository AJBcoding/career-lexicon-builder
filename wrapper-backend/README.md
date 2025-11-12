# Career Lexicon Wrapper - Backend

FastAPI backend that orchestrates Claude Code CLI for job application document generation.

## Setup

```bash
cd wrapper-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
pytest -v  # verbose
pytest tests/test_project_service.py  # specific test file
```

## API Documentation

When running, visit: http://localhost:8000/docs

### Endpoints

**Projects:**
- `POST /api/projects` - Create new project
- `GET /api/projects` - List all projects

**Skills:**
- `POST /api/skills/invoke` - Invoke Claude Code skill

**Files:**
- `POST /api/files/upload/{project_id}` - Upload file to project

**Health:**
- `GET /health` - Health check

## Architecture

```
wrapper-backend/
├── api/               # API route handlers
│   ├── projects.py    # Project management endpoints
│   ├── skills.py      # Skill invocation endpoints
│   └── files.py       # File upload endpoints
├── services/          # Business logic services
│   ├── project_service.py    # Project CRUD operations
│   ├── skill_service.py      # Claude Code CLI wrapper
│   └── watcher_service.py    # File system monitoring
├── models/            # Pydantic data models
│   └── project.py     # ProjectState model
├── tests/             # Test suite
└── main.py            # FastAPI application entry point
```

## Development

**Run tests with coverage:**
```bash
pytest --cov=. --cov-report=html
```

**Format code:**
```bash
black .
```

**Lint:**
```bash
flake8 .
```
