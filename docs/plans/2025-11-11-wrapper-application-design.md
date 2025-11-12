# Claude Code Wrapper Application Design

**Date:** November 11, 2025
**Status:** Design Complete - Ready for Implementation
**Goal:** Create a web-based GUI wrapper for career-lexicon-builder that enables fast, iterative document creation for job applications

## Problem Statement

Current CLI workflow suffers from:
- **Iteration speed bottleneck** - formatting and revision take too long
- **Context loss** - both technical (job data, drafts) and process (which skills to use, in what order)
- **Context switching friction** - terminal ↔ file browser ↔ document viewer
- **Skills are monolithic** - regenerate everything from scratch rather than incremental edits
- **No state persistence** - process feels like it needs to be rediscovered each time

## Architecture Overview

### System Type
Python backend (FastAPI) + Modern web frontend (React)

**Rationale:**
- Reuses all existing Python code (cv_formatting, analyzers, generators)
- Web UI enables rich interactions: live previews, side-by-side views, drag-drop
- Can package as desktop app later (Tauri/Electron) or offer as web service
- Fast development iteration with hot reload

### Integration Strategy
**Shell out to Claude Code CLI**

- Wrapper invokes Claude Code with specific skills
- Skills save structured JSON to standardized locations
- Wrapper reads JSON to display state, drive UI, enable iteration
- Benefits: zero reimplementation, skills auto-improve, proven tool handling

### Core Principle
**JSON as canonical format**

- All documents represented as structured JSON (content + formatting + semantic links)
- Markdown and .docx are rendered outputs, not source of truth
- Enables atomic edits, version tracking, and intelligent iteration
- Skills operate on JSON → wrapper orchestrates → renders to desired format

## Project Structure & State Management

### Job Application Project Folder

```
applications/
  ucla-assistant-dean-2024-11-15/
    # Inputs
    job-posting.pdf

    # Analysis outputs (iterative)
    job-analysis-v1.json
    job-analysis-v2.json
    resume-alignment-v1.json
    resume-alignment-v2.json
    outline-v1.json
    outline-v2.json

    # Content iterations (markdown)
    draft-v1.md
    draft-v2.md
    draft-v3.md

    # Formatting iterations (JSON + renders)
    cover-letter-v1.json
    cover-letter-v1.pdf
    cover-letter-v2.json
    cover-letter-v2.pdf

    # Metadata
    .project-state.json  # tracks workflow stage, current versions, history
```

### Project State Tracking

The `.project-state.json` file maintains:
- Current workflow stage (analyzing, drafting, formatting, complete)
- Pointers to "current" version for each artifact
- Iteration history with timestamps
- User notes/comments on each iteration
- Which skills were invoked when

**Benefits:**
- Wrapper knows exactly where you are in the workflow
- Can "pick up where you left off" across sessions
- Full audit trail of what was done when
- Supports rollback to any previous state

## Workflow Decomposition & Skills

### Stage 1: Analysis (Iterative Structured Data)

**Skill: `analyze-job-posting`**
- Input: job-posting.pdf
- Output: job-analysis-v1.json → v2.json... (requirements, culture, values, key terms)

**Skill: `align-resume`**
- Input: job-analysis-vN.json, user's background data
- Output: resume-alignment-v1.json → v2.json... (gap analysis, reframing strategies, emphasis areas)

**Skill: `generate-outline`**
- Input: job-analysis-vN.json, resume-alignment-vN.json
- Output: outline-v1.json → v2.json... (cover letter structure, talking points per section)

**Iteration pattern:** Refine analysis → regenerate alignment → adjust outline (cascading updates supported)

### Stage 2: Content Iteration (Markdown, Fast Iterations)

**Skill: `create-draft`**
- Input: outline-vN.json
- Output: draft-v1.md

**Skill: `refine-content`**
- Input: draft-vN.md, user feedback (natural language)
- Output: draft-vN+1.md

### Stage 3: Formatting Iteration (JSON with Live Preview)

**Skill: `content-to-structured-json`**
- Input: draft-final.md
- Output: cover-letter-v1.json (content structure + default formatting)

**Micro-skills for iteration:**
- `edit-section` - modify specific section content
- `adjust-formatting` - tweak margins, fonts, spacing
- `reorder-sections` - restructure document
- `refine-section-json` - natural language edits to specific section

**Skill: `render-pdf`**
- Input: cover-letter-vN.json
- Output: cover-letter-vN.pdf

## User Interface Design

### Main UI Layout

**Dashboard View (home screen)**
- List of job application projects
- Each shows: institution name, position, current stage, last updated
- Actions: Create New Project, Open Existing, Archive
- Visual status indicators: "Analyzing", "Drafting", "Formatting", "Complete"

**Project Workspace (when project is open)**

**Left Sidebar: Project Navigator**
- Files tree showing all artifacts (inputs, JSONs, drafts, PDFs)
- Version indicators (v1, v2, v3...) with timestamps
- Current/active version highlighted

**Center Panel: Context-aware workspace**
- **Analysis stage:** JSON viewer/editor
- **Content stage:** Markdown editor with simple preview
- **Formatting stage:** Split view - controls on left, live preview on right

**Right Sidebar: Actions & Chat**
- Stage-specific quick actions (buttons/forms)
- Natural language input for iterations
- Opportunistic prompts ("No job analysis found - analyze first?")
- Progress indicators when skills are running

**Bottom Bar: Stage progression**
- Visual workflow: [Analysis] → [Content] → [Formatting] → [Export]
- Click any stage to jump there (if data exists)
- "Next Step" button with smart suggestions

## Skill Integration Mechanics

### How the Wrapper Invokes Claude Code

**Skill Invocation Flow:**
1. User triggers action (e.g., "Analyze job posting")
2. Wrapper prepares context:
   - Sets working directory to project folder
   - Prepares input files
   - Constructs prompt for skill
3. Wrapper invokes: `claude --skill [skill-name] [prompt]`
4. Claude Code executes skill, saves outputs to project folder
5. Wrapper polls/watches for completion and expected output files
6. Wrapper reads result (JSON/markdown/PDF), updates UI

### Skill Modifications Needed

Your existing skills need JSON export capability:
- Add explicit "save to JSON" instructions at end of skill prompts
- Use standardized filenames (job-analysis.json, resume-alignment.json, etc.)
- Include metadata in JSON (timestamp, version, inputs used)

**Example skill modification:**
```markdown
# Current skill ending:
Present your analysis to the user.

# Modified skill ending:
Present your analysis to the user, then save it to `job-analysis-v[N].json`
where N is the next version number. Include:
- All analysis findings
- Metadata: timestamp, input files used, version number
```

### Communication Protocol
- Wrapper → Skill: via command-line arguments and working directory
- Skill → Wrapper: via saved files in project folder
- Progress tracking: wrapper monitors file creation/modification

## Preview & Rendering System

### Preview Strategy by Stage

**Analysis Stage:** JSON viewers
- Syntax-highlighted JSON display
- Collapsible sections for readability
- No rendering needed - viewing structured data

**Content Stage:** Simple markdown preview
- Split pane: markdown source | HTML preview
- Fast, in-browser rendering
- Focus on content, not appearance

**Formatting Stage:** Progressive preview

1. **Instant HTML preview**
   - JSON → styled HTML/CSS approximation
   - Updates immediately on edit
   - Good enough for "does this look right?"

2. **Background PDF generation**
   - Triggered after changes settle (debounced)
   - Invokes `render-pdf` skill in background
   - Shows loading indicator

3. **PDF display**
   - "PDF ready" notification when complete
   - Toggle between HTML preview (fast) and PDF view (accurate)
   - PDF embedded in browser (no external app during iteration)

### Export/Final Output
- "Export Final PDF" button
- Saves to project folder and optionally to a specified output location
- Opens in system PDF viewer for final review

**Performance Characteristics:**
- HTML preview: <100ms (instant feedback)
- PDF generation: 2-5s (accurate but slower)
- Best of both: iterate fast, verify accurate

## Natural Language Routing & Command Interpretation

### The Three Ways to Trigger Actions

**1. UI Shortcuts (explicit, no ambiguity)**
- Click on section in preview → menu appears: "Edit", "Make more concise", "Emphasize more", "Delete"
- Form controls: dropdowns for common formatting (margins, fonts, spacing)
- Stage navigation: "Analyze Job", "Generate Draft", "Format Document" buttons
- Direct to specific micro-skill with pre-filled parameters

**2. Natural Language via Routing Skill (flexible, intelligent)**
- User types: "make paragraph 2 more concise"
- Wrapper invokes meta-skill: `route-command`
  - Input: user request + current project state (what JSONs exist, current stage)
  - Output: routing-decision.json
    ```json
    {
      "skill": "edit-section",
      "parameters": {
        "target": "cover-letter-v3.json",
        "section_index": 2,
        "instruction": "make more concise"
      },
      "reasoning": "User wants to edit specific section content"
    }
    ```
- Wrapper executes the routed skill with parameters
- Result saved, UI updates

**3. Power User Direct Invocation (expert mode)**
- Command palette (keyboard shortcut): type skill name directly
- Dropdown shows available skills + recent history
- Can pass custom parameters
- For users who know exactly what they want

### Routing Skill Intelligence

The `route-command` skill has context awareness:
- Knows current stage (won't suggest formatting if still drafting)
- Knows what files exist (can reference "the current draft" or "latest analysis")
- Can suggest alternatives if request is ambiguous
- Can chain multiple micro-skills if needed

## Error Handling & Recovery

### Common Failure Scenarios

**1. Skill Execution Failures**
- Claude Code returns error (API limit, timeout, invalid input)
- UI shows error message with context
- Options: "Retry", "Edit input", "Skip this step"
- State preserved - can resume without losing work

**2. Missing Dependencies**
- User tries to generate cover letter without job analysis
- Opportunistic prompt: "Job analysis not found. Would you like to analyze the job posting first?"
- Options: "Yes, analyze now" | "Continue anyway" | "Cancel"

**3. File/State Corruption**
- JSON parse error, unexpected file format
- UI shows validation error with details
- Options: "View raw file" | "Revert to previous version" | "Delete and regenerate"
- All versions kept - can always roll back

**4. Slow/Hung Skills**
- Progress indicator with estimated time
- After timeout threshold: "This is taking longer than usual"
- Options: "Keep waiting" | "Cancel" | "View logs"
- Background execution - UI stays responsive

### Recovery Mechanisms

**Version History as Safety Net**
- Every iteration saves new version (never overwrites)
- `.project-state.json` tracks full history
- "Revert" feature: roll back to any previous state
- "Branch" feature: try alternative approach without losing current work

**Graceful Degradation**
- If live preview fails → show last successful preview + error message
- If PDF generation fails → HTML preview still works
- If routing skill fails → show available skills for manual selection

## MVP Scope & Implementation Phases

### Phase 1: Minimum Viable Product (2-3 weeks)

**Scope:**
- Single complete workflow: Job posting → Analysis → Draft → Formatted cover letter
- Basic web UI: project creation, file upload, stage navigation
- Core skills implemented with JSON export:
  - `analyze-job-posting`
  - `generate-outline`
  - `create-draft`
  - `content-to-structured-json`
  - `render-pdf`
- Simple preview: markdown for content, PDF view for formatting
- Manual skill invocation (buttons, no natural language routing yet)

**Success Criteria:**
- Can create a job application project
- Upload job posting, generate complete formatted cover letter
- Faster than current CLI workflow
- All artifacts saved to project folder

### Phase 2: Iteration & Intelligence (2-3 weeks)

**Adds:**
- Content refinement: `refine-content` skill
- Formatting micro-skills: `edit-section`, `adjust-formatting`
- Natural language routing: `route-command` skill
- Live HTML preview with progressive PDF generation
- Version history UI (view/revert previous versions)
- Resume alignment workflow

### Phase 3: Polish & Distribution Prep (2-4 weeks)

**Adds:**
- Full three-task workflow (analysis, alignment, cover letter)
- UI shortcuts (click-to-edit, formatting controls)
- Power user features (command palette, direct skill invocation)
- Batch operations (apply same analysis to multiple positions)
- Desktop packaging (Tauri or Electron)
- Documentation for other users

## Technical Stack & Implementation Details

### Backend (Python/FastAPI)
- **FastAPI** - REST API for frontend communication
- **SQLite or JSON files** - project metadata, history tracking (start with JSON, migrate if needed)
- **Subprocess management** - invoke Claude Code CLI, capture output
- **File watchers** - monitor project folders for skill outputs (watchdog library)
- **Existing modules** - reuse cv_formatting, analyzers, generators as-is

### Frontend (React)
- **React** - mature ecosystem, rich component libraries
- **State management** - Redux Toolkit or Zustand for project state
- **Monaco Editor** - for markdown/JSON editing (VSCode editor in browser)
- **PDF.js** - for embedded PDF viewing
- **WebSocket** - real-time updates when skills complete

### Key Technical Patterns

**Skill Invocation:**
```python
# Backend service
import subprocess

def invoke_skill(skill_name, project_path, prompt):
    cmd = [
        'claude',
        '--skill', skill_name,
        '--working-dir', project_path,
        prompt
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result
```

**File Watching:**
```python
# Watch for skill outputs
from watchdog.observers import Observer

def watch_project_folder(project_path, on_file_created):
    observer = Observer()
    observer.schedule(FileHandler(on_file_created), project_path)
    observer.start()
```

**Progressive PDF Generation:**
- HTML preview: Jinja2 templates + CSS (immediate)
- PDF generation: skill invoked in background worker
- WebSocket pushes "PDF ready" event to frontend

## Security & Sandboxing

### Security Concerns

**1. Bash Execution via Claude Code**
- Claude Code skills may execute bash commands
- Risk: malicious or accidental destructive commands
- Mitigation: Claude Code already sandboxes by default
- Additional: wrapper restricts working directory to project folder only

**2. API Key Management**
- Anthropic API key needed for Claude Code
- Storage: macOS Keychain (secure system storage)
- Never stored in project files or git
- First-run setup: prompt for API key, save to keychain

**3. File System Access**
- Wrapper restricts operations to:
  - User-specified applications folder
  - Project-specific subfolders
- No access to system directories
- Path validation to prevent directory traversal attacks

**4. Input Validation**
- All file uploads: validate type and size
- JSON parsing: handle malformed data gracefully
- Skill outputs: validate expected structure before processing

**5. Future Distribution Considerations (Phase 3)**
- Code signing for macOS distribution
- Sandboxed app bundle if targeting App Store
- Clear privacy policy (data stays local, API calls to Anthropic only)

**Acceptable Risk for Personal Use (MVP):**
- Claude Code CLI already provides sandboxing
- Working directory restrictions add extra layer
- For Phase 1-2 (personal use), this is sufficient
- Phase 3 (distribution) requires hardening review

## Open Questions & Decisions Needed

### Remaining Questions

**1. Frontend Framework Choice**
- React (most popular, rich ecosystem) vs. Vue (simpler, faster to learn)
- Recommendation: React for better long-term component availability

**2. Database for Metadata**
- SQLite (simple, file-based) vs. JSON files (no DB dependency)
- Recommendation: Start with JSON files (.project-state.json), migrate to SQLite if needed

**3. Background Data Integration**
- Your career lexicon data (background, achievements, etc.) - how should it be accessed?
- Option A: Import/configure once in wrapper settings
- Option B: Point to existing files from career-lexicon-builder
- Option C: Manual input per project

**4. Testing Strategy**
- Unit tests for backend services (pytest)
- E2E tests for critical workflows (Playwright)
- How much test coverage for MVP?

## Next Steps

### Immediate Actions

**1. Create project structure**
- Set up FastAPI backend skeleton
- Set up React frontend with Vite
- Create initial project folder structure

**2. Implement first skill with JSON export**
- Modify existing `job-description-analysis` skill
- Test JSON output format
- Validate wrapper can read it

**3. Build basic project creation flow**
- API endpoint: create project
- Frontend: project creation form
- File system: create project folder structure

**4. Prototype skill invocation**
- Backend: invoke Claude Code CLI
- File watcher: detect completion
- Frontend: show progress/results

### Implementation Approach

Use git worktree for isolated development, then create detailed implementation plan with specific tasks and acceptance criteria.

---

**Design Status:** Complete and validated
**Ready for:** Implementation planning and execution
