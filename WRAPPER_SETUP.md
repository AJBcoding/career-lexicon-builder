# Wrapper Application Setup Guide

Complete setup instructions for the Claude Code Wrapper MVP.

## Prerequisites

- Python 3.9+ (check: `python --version`)
- Node.js 18+ (check: `node --version`)
- Claude Code CLI installed and configured (check: `claude --version`)

## Quick Start

### 1. Backend Setup

```bash
cd wrapper-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your paths:
```
APPLICATIONS_DIR=/Users/yourname/career-applications
CLAUDE_CODE_PATH=claude
```

Start backend:
```bash
python main.py
```

Backend runs on: http://localhost:8000

### 2. Frontend Setup (in new terminal)

```bash
cd wrapper-frontend
npm install
```

Create `.env` file:
```bash
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

Start frontend:
```bash
npm run dev
```

Frontend runs on: http://localhost:5173

### 3. Access Application

Open browser to: http://localhost:5173

## First Project

1. Click "New Project"
2. Fill in:
   - Institution: "UCLA"
   - Position: "Assistant Dean"
   - Date: (today's date)
3. Click "Create Project"
4. Click on the project to open workspace
5. Upload a job posting file (drag-and-drop or click "Select Files")
6. Click "Analyze Job Posting"
7. View results in the UI
8. Check project folder for generated files:
   - `01-job-analysis.md` - Full markdown analysis
   - `job-analysis-v1.json` - Structured JSON data

## Troubleshooting

### Backend won't start

**Error: "No such file or directory: applications"**
- Create applications directory: `mkdir -p ~/career-applications`
- Or update `APPLICATIONS_DIR` in `.env` to existing directory

**Error: "ModuleNotFoundError"**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend won't start

**Error: "Cannot find module"**
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Error: "EADDRINUSE: port 5173"**
- Port already in use, kill process: `lsof -ti:5173 | xargs kill -9`
- Or use different port: `npm run dev -- --port 5174`

### Skill invocation fails

**Error: "Project not found"**
- Verify project was created in dashboard
- Check applications directory contains project folder

**Error: "claude: command not found"**
- Ensure Claude Code CLI is installed and in PATH
- Update `CLAUDE_CODE_PATH` in backend `.env` if installed elsewhere

### File upload fails

**Error: "Failed to upload file"**
- Check project exists
- Verify backend is running
- Check network tab in browser dev tools for details

## Development

### Run backend tests

```bash
cd wrapper-backend
source venv/bin/activate
pytest -v
```

### Build frontend for production

```bash
cd wrapper-frontend
npm run build
```

Production files will be in `wrapper-frontend/dist/`

### View API documentation

With backend running, visit: http://localhost:8000/docs

## Architecture

**Backend:** FastAPI + Python
**Frontend:** React + Vite
**Integration:** Shell out to Claude Code CLI
**Data Flow:** React → FastAPI → Claude CLI → File System → React

## Next Steps

After MVP is working:
- Add more skills (resume-alignment, cover-letter-voice, format-resume)
- Implement live preview (HTML + PDF)
- Add version history UI
- Implement WebSocket for real-time updates
- Add skill output file watcher integration

## Getting Help

- Backend API docs: http://localhost:8000/docs
- Claude Code docs: https://docs.claude.com/en/docs/claude-code
- Design doc: `docs/plans/2025-11-11-wrapper-application-design.md`
- Implementation plan: `docs/plans/2025-11-11-wrapper-mvp-implementation.md`
