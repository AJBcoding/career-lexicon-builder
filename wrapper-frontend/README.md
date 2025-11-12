# Career Lexicon Wrapper - Frontend

React frontend for managing job application projects with Claude Code integration.

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

Preview production build:
```bash
npm run preview
```

## Features

### Project Dashboard
- Create new job application projects
- View all projects with status and last updated date
- Click to open project workspace

### Project Workspace
- Upload job posting files (drag-and-drop or click-to-select)
- Invoke Claude Code skills (currently: job-description-analysis)
- View skill execution results

### File Upload
- Drag-and-drop support
- Multiple file upload
- Visual feedback for drag state
- Upload progress indication

## Architecture

```
wrapper-frontend/
├── src/
│   ├── components/              # React components
│   │   ├── ProjectDashboard.jsx # Project list and creation
│   │   ├── ProjectWorkspace.jsx # Project detail view
│   │   └── FileUpload.jsx       # File upload widget
│   ├── services/                # API integration
│   │   ├── api.js               # Axios client
│   │   └── projectService.js    # Project API calls
│   ├── config.js                # Environment configuration
│   └── App.jsx                  # Main application component
├── public/                      # Static assets
└── index.html                   # HTML entry point
```

## Development

**Lint:**
```bash
npm run lint
```

**Build for production:**
```bash
npm run build
```
The built files will be in the `dist/` directory.
