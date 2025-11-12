# Wrapper Application Development Roadmap

**Created:** November 12, 2025
**Status:** MVP Complete - Planning Future Development
**Purpose:** Comprehensive development paths beyond MVP

---

## Overview

This roadmap outlines development paths from MVP (complete) through production-ready application. Each phase builds on previous work and can be pursued in parallel where dependencies allow.

**Current State:** MVP complete (12/12 tasks)
**Next Milestones:** Phase 2 → Phase 3 → Phase 4 → Production

---

## Phase 2: Essential Features (Est. 2-3 weeks)

### 2A: Additional Skill Integration ⭐ HIGH PRIORITY
**Goal:** Add JSON export to all remaining career skills

**Tasks:**
1. **Add JSON export to resume-alignment skill**
   - Output: `resume-alignment-v1.json`
   - Structure: matched achievements, keyword coverage, gap analysis
   - Estimated: 4 hours

2. **Add JSON export to cover-letter-voice skill**
   - Output: `cover-letter-draft-v1.json`
   - Structure: paragraphs, tone analysis, word count
   - Estimated: 4 hours

3. **Add JSON export to format-resume skill**
   - Output: `resume-formatted-v1.json` + PDF
   - Structure: formatting metadata, sections, validation results
   - Estimated: 6 hours

4. **Add JSON export to format-cover-letter skill**
   - Output: `cover-letter-formatted-v1.json` + PDF
   - Structure: formatting metadata, paragraphs, validation
   - Estimated: 6 hours

5. **Add JSON export to job-fit-analysis skill**
   - Output: `job-fit-analysis-v1.json`
   - Structure: gap analysis, competitive assessment, recommendations
   - Estimated: 5 hours

**Success Criteria:**
- All 5 skills export JSON + original output
- Wrapper can invoke all skills via API
- UI has buttons for each skill in appropriate workflow stage

---

### 2B: Live Preview System ⭐ HIGH PRIORITY
**Goal:** See document changes without downloading PDFs

**Phase 2B.1: HTML Preview (Week 1)**
- Add `POST /api/preview/html/{project_id}/{file}` endpoint
- Convert markdown → HTML server-side
- Display in iframe in frontend
- Live update on file change
- Estimated: 8 hours

**Phase 2B.2: PDF Preview (Week 1)**
- Add `GET /api/preview/pdf/{project_id}/{file}` endpoint
- Serve existing PDFs via backend
- Use `react-pdf` or `pdf.js` for display
- Side-by-side HTML (fast) + PDF (accurate) view
- Estimated: 8 hours

**Phase 2B.3: Progressive Preview (Week 2)**
- Show HTML immediately when skill starts
- Update HTML in real-time as skill generates content
- Generate PDF when complete
- Swap to PDF when ready
- Estimated: 12 hours

**Success Criteria:**
- Can preview any markdown/PDF in project
- No need to download files to see results
- Fast feedback loop (<2 seconds for HTML)

---

### 2C: Version History UI ⭐ MEDIUM PRIORITY
**Goal:** Navigate and compare versions of generated files

**Tasks:**
1. **Version Detection Service (Backend)**
   - Scan project for versioned files (`*-v1.json`, `*-v2.json`)
   - Group by base name
   - Sort by version number
   - API: `GET /api/projects/{id}/versions`
   - Estimated: 4 hours

2. **Version History Component (Frontend)**
   - List all versions of a file
   - Show created date, size, version number
   - Click to view specific version
   - Estimated: 6 hours

3. **Version Comparison View**
   - Side-by-side diff view
   - Highlight changes between versions
   - JSON diff for structured data
   - Text diff for markdown
   - Estimated: 10 hours

4. **Version Restore**
   - Copy old version to new version number
   - API: `POST /api/projects/{id}/versions/restore`
   - Confirmation dialog
   - Estimated: 4 hours

**Success Criteria:**
- Can see all versions of job-analysis, resume, cover letter
- Can compare any two versions
- Can restore previous version

---

## Phase 3: Advanced Features (Est. 3-4 weeks)

### 3A: WebSocket Real-Time Updates ⭐ HIGH PRIORITY
**Goal:** See skill execution progress in real-time

**Phase 3A.1: WebSocket Infrastructure (Week 1)**
- Add WebSocket endpoint to FastAPI
- Connection management (connect, disconnect, reconnect)
- Room-based messaging (one room per project)
- Heartbeat/ping-pong for connection health
- Estimated: 8 hours

**Phase 3A.2: Skill Execution Streaming (Week 1)**
- Stream stdout from subprocess to WebSocket
- Parse partial output and send as events
- Frontend displays in progress indicator
- Show last N lines of output
- Estimated: 10 hours

**Phase 3A.3: File Watcher Integration (Week 2)**
- Start WatcherService when project opened
- Emit WebSocket event when file created/modified
- Frontend auto-refreshes file list
- Show toast notification on new file
- Estimated: 8 hours

**Phase 3A.4: Progress Indicators (Week 2)**
- Skill-specific progress parsing
- Progress bar based on skill stages
- Estimated time remaining
- Cancel button (SIGINT to subprocess)
- Estimated: 10 hours

**Success Criteria:**
- See live output as skill executes
- Get notified when files appear
- Know how long skill will take
- Can cancel long-running skills

---

### 3B: Natural Language Routing ⭐ MEDIUM PRIORITY
**Goal:** "Analyze this job" → automatically routes to correct skill

**Phase 3B.1: Intent Classification (Week 1)**
- Simple keyword matching for MVP
  - "analyze" + "job" → job-description-analysis
  - "resume" + "align" → resume-alignment
  - "cover letter" + "draft" → cover-letter-voice
- API: `POST /api/intent/classify` (body: {text: string})
- Returns: {skill: string, confidence: float, context: object}
- Estimated: 6 hours

**Phase 3B.2: Smart Prompt Builder (Week 1)**
- Extract file references from user input
- Build complete skill prompt from intent + context
- Handle ambiguous requests (ask clarifying questions)
- Estimated: 8 hours

**Phase 3B.3: Conversational UI (Week 2)**
- Chat-style interface option
- Type natural language requests
- System responds with action taken or question
- Execute skills from conversation
- Estimated: 12 hours

**Phase 3B.4: Suggested Next Actions (Week 2)**
- Based on project state, suggest next steps
- "You've analyzed the job. Ready to align your resume?"
- One-click execution of suggestions
- Estimated: 6 hours

**Success Criteria:**
- Can type "analyze this job" and it works
- System suggests logical next steps
- Reduces cognitive load (no need to remember skill names)

---

### 3C: Batch Operations ⭐ MEDIUM PRIORITY
**Goal:** Process multiple projects/files at once

**Tasks:**
1. **Batch Project Creation**
   - Upload CSV with multiple jobs (institution, position, date, URL)
   - Create all projects at once
   - Background task queue
   - Estimated: 8 hours

2. **Batch Skill Invocation**
   - Select multiple projects
   - Run same skill on all (e.g., analyze all job postings)
   - Progress dashboard showing status of each
   - Estimated: 10 hours

3. **Batch Export**
   - Export all projects as ZIP
   - Include all JSON + PDFs
   - Generate summary report
   - Estimated: 6 hours

4. **Bulk Actions**
   - Delete multiple projects
   - Archive completed applications
   - Bulk status updates
   - Estimated: 6 hours

**Success Criteria:**
- Can create 10 projects from CSV in one action
- Can run analysis on all 10 simultaneously
- Can export all results as ZIP

---

### 3D: Template System ⭐ LOW PRIORITY
**Goal:** Reusable project templates and skill configurations

**Tasks:**
1. **Project Templates**
   - Save project as template
   - Templates include: folder structure, initial files, skill sequence
   - Create project from template
   - API: `GET /api/templates`, `POST /api/templates/{id}/instantiate`
   - Estimated: 8 hours

2. **Skill Presets**
   - Save skill invocation with specific prompts as preset
   - E.g., "Academic Resume" preset with specific instructions
   - One-click execution of preset
   - Estimated: 6 hours

3. **Workflow Templates**
   - Define multi-skill workflows
   - E.g., "Complete Application" = analyze → align → draft → format
   - Execute entire workflow with one click
   - Pause/resume between steps
   - Estimated: 12 hours

**Success Criteria:**
- Can create "Academic Application" template
- One-click creates project with all necessary structure
- Can execute full workflow automatically

---

## Phase 4: Production Readiness (Est. 3-4 weeks)

### 4A: Authentication & Multi-User Support ⭐ HIGH PRIORITY
**Goal:** Multiple users can use application securely

**Phase 4A.1: User Authentication (Week 1)**
- User registration and login
- JWT token-based auth
- Password hashing with bcrypt
- Session management
- API: `POST /api/auth/register`, `POST /api/auth/login`
- Estimated: 12 hours

**Phase 4A.2: Project Ownership (Week 1)**
- Projects belong to specific users
- Filter projects by current user
- Authorization checks on all endpoints
- Cannot access other users' projects
- Estimated: 8 hours

**Phase 4A.3: User Profile (Week 2)**
- View/edit profile
- Store user preferences
- API key management (for Claude API)
- Usage statistics
- Estimated: 8 hours

**Phase 4A.4: Sharing & Collaboration (Week 2)**
- Share project with other users (read-only or edit)
- Collaborative editing with conflict resolution
- Activity log (who did what when)
- Estimated: 16 hours

**Success Criteria:**
- Multiple users can have separate accounts
- Each user sees only their own projects
- Can share specific projects with collaborators

---

### 4B: Database Integration ⭐ HIGH PRIORITY
**Goal:** Replace JSON files with proper database

**Phase 4B.1: Database Setup (Week 1)**
- Choose: PostgreSQL (production) or SQLite (dev)
- Define schema with SQLAlchemy models
- Migration system (Alembic)
- Tables: users, projects, project_files, skill_executions, versions
- Estimated: 10 hours

**Phase 4B.2: Data Migration (Week 1)**
- Script to migrate JSON files → database
- Import existing projects
- Verify data integrity
- Rollback capability
- Estimated: 8 hours

**Phase 4B.3: Update Services (Week 2)**
- Replace file-based storage with DB queries
- Keep file system for actual documents
- DB stores metadata only
- Update all services and tests
- Estimated: 16 hours

**Phase 4B.4: Query Optimization (Week 2)**
- Add indexes for common queries
- Implement pagination
- Caching layer (Redis optional)
- Query performance monitoring
- Estimated: 10 hours

**Success Criteria:**
- All project data in database
- Faster queries than file-based
- Can handle 1000+ projects
- All tests still pass

---

### 4C: Error Handling & Monitoring ⭐ HIGH PRIORITY
**Goal:** Robust error handling and observability

**Phase 4C.1: Structured Logging (Week 1)**
- Replace print statements with proper logging
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Structured logs (JSON format)
- Request/response logging with correlation IDs
- Estimated: 8 hours

**Phase 4C.2: Error Tracking (Week 1)**
- Integrate Sentry or similar
- Automatic error reporting
- User context in error reports
- Source maps for frontend errors
- Estimated: 6 hours

**Phase 4C.3: Health Checks & Metrics (Week 1)**
- Expand `/health` endpoint with dependencies
- Check: database connection, file system, API availability
- Expose Prometheus metrics
- Response time tracking
- Estimated: 8 hours

**Phase 4C.4: User-Facing Error Messages (Week 2)**
- Toast notifications instead of alerts
- Error codes with help links
- Retry logic for transient failures
- Graceful degradation
- Estimated: 10 hours

**Success Criteria:**
- All errors logged with context
- Error tracking dashboard shows issues
- Users see helpful error messages
- Can diagnose issues quickly

---

### 4D: Performance Optimization ⭐ MEDIUM PRIORITY
**Goal:** Fast, responsive application

**Tasks:**
1. **Backend Optimization**
   - API response caching
   - Database query optimization
   - Async file operations
   - Background task queue (Celery)
   - Estimated: 12 hours

2. **Frontend Optimization**
   - Code splitting and lazy loading
   - Image optimization
   - Virtual scrolling for long lists
   - Memoization for expensive renders
   - Estimated: 10 hours

3. **Network Optimization**
   - Compression (gzip)
   - HTTP/2 support
   - CDN for static assets
   - API request batching
   - Estimated: 8 hours

4. **Load Testing**
   - Locust or k6 load tests
   - Identify bottlenecks
   - Stress test with 100 concurrent users
   - Performance regression tests
   - Estimated: 10 hours

**Success Criteria:**
- Page load time <2 seconds
- API response time <200ms (p95)
- Can handle 50 concurrent users
- Smooth UI even with 100+ projects

---

## Phase 5: Advanced Integrations (Est. 2-3 weeks)

### 5A: Anthropic API Direct Integration ⭐ HIGH PRIORITY
**Goal:** Option to use Anthropic API instead of Claude Code CLI

**Why:** Faster, more flexible, better for production, enables streaming

**Phase 5A.1: API Client (Week 1)**
- Add Anthropic SDK to backend
- Implement skill execution via API
- Handle streaming responses
- Map CLI tool use to API tool use
- Estimated: 12 hours

**Phase 5A.2: Hybrid Mode (Week 1)**
- User can choose: CLI or API
- API mode for speed
- CLI mode for local skills
- Configuration per skill
- Estimated: 8 hours

**Phase 5A.3: Streaming UI (Week 2)**
- Token-by-token rendering
- Real-time markdown preview
- Progress indication
- Cost tracking (tokens used)
- Estimated: 14 hours

**Success Criteria:**
- Skills run 3-5x faster via API
- Can see content appear in real-time
- Know cost before and after execution
- Can switch between CLI and API modes

---

### 5B: Git Integration ⭐ MEDIUM PRIORITY
**Goal:** Version control for generated documents

**Tasks:**
1. **Auto-Git Project Folders**
   - Initialize git repo in each project
   - Auto-commit after each skill execution
   - Commit message: skill name + timestamp
   - Estimated: 6 hours

2. **Git History UI**
   - Browse git history in UI
   - See diff between commits
   - Restore from git history
   - Estimated: 10 hours

3. **Branch Support**
   - Create branches for experiments
   - E.g., "try-different-tone" branch for cover letter
   - Merge branches back to main
   - Estimated: 8 hours

4. **Remote Sync (Optional)**
   - Push to GitHub/GitLab automatically
   - Backup in cloud
   - Share via git URL
   - Estimated: 8 hours

**Success Criteria:**
- Every change tracked in git
- Can see full history
- Can revert to any previous state
- (Optional) Projects backed up to GitHub

---

### 5C: PostgreSQL/Python419 Integration ⭐ HIGH PRIORITY
**Goal:** Generate documents from database data

**Context:** User has existing PostgreSQL database (Python419) with academic data

**Phase 5C.1: Database Connection (Week 1)**
- Add PostgreSQL connection to backend
- Read-only access to Python419
- Query builder for common reports
- Estimated: 8 hours

**Phase 5C.2: Data Templates (Week 1)**
- "Teaching Load Report" template
- "Cost Analysis Report" template
- Pull data from database
- Generate markdown/PDF
- Estimated: 12 hours

**Phase 5C.3: Skill Integration (Week 2)**
- Pass database data to skills as context
- E.g., "Include these achievements from database"
- Merge database data with lexicons
- Estimated: 10 hours

**Phase 5C.4: Scheduled Reports (Week 2)**
- Cron-style scheduling
- Generate reports automatically
- Email or save to project
- Estimated: 10 hours

**Success Criteria:**
- Can generate teaching load report from database
- Can include database achievements in resume
- Reports generated automatically on schedule

---

### 5D: Email & Calendar Integration ⭐ LOW PRIORITY
**Goal:** Track application deadlines and communications

**Tasks:**
1. **Deadline Tracking**
   - Add deadline field to projects
   - Calendar view of all deadlines
   - Email reminders (1 week, 1 day before)
   - Estimated: 8 hours

2. **Email Integration**
   - Connect to email (IMAP/SMTP)
   - Track sent applications
   - Log responses from employers
   - Link emails to projects
   - Estimated: 14 hours

3. **Status Pipeline**
   - Track application status: draft → submitted → interview → offer
   - Visual kanban board
   - Auto-update status from email keywords
   - Estimated: 10 hours

**Success Criteria:**
- Never miss a deadline
- Know status of all applications
- Email history linked to projects

---

## Phase 6: AI Enhancements (Est. 2-3 weeks)

### 6A: Smart Suggestions ⭐ MEDIUM PRIORITY
**Goal:** AI-powered recommendations

**Tasks:**
1. **Content Improvement Suggestions**
   - Analyze generated documents
   - Suggest improvements: "This achievement could be more specific"
   - Highlight weak areas
   - Estimated: 12 hours

2. **Missing Information Detection**
   - "You haven't mentioned any budget numbers"
   - "No diversity/inclusion language found"
   - Checklist of recommended elements
   - Estimated: 10 hours

3. **Competitive Intelligence**
   - Analyze job posting vs. your profile
   - "Your competitors likely have X, emphasize your Y"
   - Strategic positioning advice
   - Estimated: 12 hours

**Success Criteria:**
- AI points out gaps before you submit
- Suggestions are actionable
- Documents improve with AI guidance

---

### 6B: Learning System ⭐ LOW PRIORITY
**Goal:** Application learns from your preferences

**Tasks:**
1. **Preference Learning**
   - Track which suggestions you accept/reject
   - Learn your writing style preferences
   - Adapt future suggestions
   - Estimated: 14 hours

2. **Success Tracking**
   - Track which applications get interviews
   - Correlate with document characteristics
   - "Applications with X got 40% more responses"
   - Estimated: 12 hours

3. **Personalized Templates**
   - Generate templates based on your successes
   - "Use this structure - it worked before"
   - Estimated: 10 hours

**Success Criteria:**
- System gets smarter over time
- Recommendations improve with use
- Know what works for you

---

### 6C: Multi-Modal Input ⭐ LOW PRIORITY
**Goal:** Extract information from various sources

**Tasks:**
1. **PDF Text Extraction**
   - Extract job postings from PDF automatically
   - Handle multi-column layouts
   - OCR for image-based PDFs
   - Estimated: 10 hours

2. **URL Scraping**
   - Paste job posting URL
   - Automatically extract and analyze
   - Handle common job sites (Indeed, LinkedIn, HigherEdJobs)
   - Estimated: 12 hours

3. **Voice Input (Stretch)**
   - Record voice notes about job
   - Transcribe with Whisper
   - Extract key information
   - Estimated: 14 hours

**Success Criteria:**
- Paste URL, get instant analysis
- Upload PDF, automatic extraction
- No manual copy-paste needed

---

## Phase 7: Mobile & Accessibility (Est. 2-3 weeks)

### 7A: Mobile-Responsive UI ⭐ HIGH PRIORITY
**Goal:** Works great on phone and tablet

**Tasks:**
1. **Responsive Layout**
   - Breakpoints for mobile, tablet, desktop
   - Touch-friendly controls
   - Hamburger menu for navigation
   - Estimated: 14 hours

2. **Mobile-First Components**
   - Bottom sheet for actions
   - Swipe gestures
   - Mobile-optimized file picker
   - Estimated: 12 hours

3. **Progressive Web App**
   - Add service worker
   - Offline support (view cached projects)
   - Add to home screen
   - Estimated: 10 hours

**Success Criteria:**
- Fully functional on iPhone/Android
- Smooth on tablet
- Can work offline (view mode)

---

### 7B: Accessibility (WCAG 2.1 AA) ⭐ MEDIUM PRIORITY
**Goal:** Usable by everyone

**Tasks:**
1. **Keyboard Navigation**
   - Tab through all controls
   - Escape to close modals
   - Shortcuts for common actions
   - Estimated: 8 hours

2. **Screen Reader Support**
   - ARIA labels on all interactive elements
   - Semantic HTML
   - Focus management
   - Estimated: 10 hours

3. **Visual Accessibility**
   - High contrast mode
   - Resizable text
   - Color-blind friendly
   - Focus indicators
   - Estimated: 8 hours

4. **Accessibility Testing**
   - Automated tests (axe-core)
   - Manual testing with screen reader
   - WCAG compliance report
   - Estimated: 6 hours

**Success Criteria:**
- WCAG 2.1 AA compliant
- Works with screen readers
- Keyboard-only navigation functional

---

## Phase 8: Deployment & DevOps (Est. 2-3 weeks)

### 8A: Production Deployment ⭐ HIGH PRIORITY
**Goal:** Deploy to real server

**Phase 8A.1: Containerization (Week 1)**
- Dockerfile for backend
- Dockerfile for frontend
- Docker Compose for local dev
- Multi-stage builds
- Estimated: 10 hours

**Phase 8A.2: Cloud Deployment (Week 1)**
- Choose: AWS/GCP/Azure/DigitalOcean
- Infrastructure as Code (Terraform or CloudFormation)
- Load balancer
- Auto-scaling
- Estimated: 16 hours

**Phase 8A.3: Database Hosting (Week 2)**
- Managed PostgreSQL (RDS/Cloud SQL)
- Backups and point-in-time recovery
- Connection pooling
- Estimated: 8 hours

**Phase 8A.4: File Storage (Week 2)**
- S3/GCS/Azure Blob for project files
- CDN for fast access
- Signed URLs for security
- Estimated: 10 hours

**Success Criteria:**
- Application accessible at public URL
- Handles production load
- Data is backed up
- Files stored reliably

---

### 8B: CI/CD Pipeline ⭐ HIGH PRIORITY
**Goal:** Automated testing and deployment

**Tasks:**
1. **Continuous Integration**
   - GitHub Actions or GitLab CI
   - Run tests on every commit
   - Lint and format checks
   - Build validation
   - Estimated: 8 hours

2. **Continuous Deployment**
   - Auto-deploy to staging on merge to main
   - Manual approval for production
   - Blue-green deployment
   - Rollback capability
   - Estimated: 12 hours

3. **Automated Testing**
   - Unit tests
   - Integration tests
   - E2E tests (Playwright/Cypress)
   - Coverage reporting
   - Estimated: 14 hours

**Success Criteria:**
- Every commit tested automatically
- Passing commits deploy to staging
- Production deployment is one click
- Can rollback in <5 minutes

---

### 8C: Monitoring & Observability ⭐ MEDIUM PRIORITY
**Goal:** Know what's happening in production

**Tasks:**
1. **Application Monitoring**
   - New Relic, Datadog, or open-source APM
   - Request traces
   - Error tracking
   - Performance metrics
   - Estimated: 8 hours

2. **Infrastructure Monitoring**
   - CPU, memory, disk usage
   - Database performance
   - Network metrics
   - Alerts for anomalies
   - Estimated: 8 hours

3. **User Analytics**
   - Plausible or Google Analytics
   - Feature usage tracking
   - User flows
   - Conversion funnels
   - Estimated: 6 hours

4. **Alerting**
   - Slack/email alerts for errors
   - Threshold-based alerts (response time >1s)
   - On-call rotation (if team)
   - Estimated: 6 hours

**Success Criteria:**
- Know when something breaks
- Dashboards show key metrics
- Understand how users use the app
- Alerted before users report issues

---

## Phase 9: Enterprise Features (Est. 4-6 weeks)

### 9A: Team & Organization Support ⭐ MEDIUM PRIORITY
**Goal:** Support teams and organizations

**Tasks:**
1. **Organizations**
   - Create organization accounts
   - Multiple users per org
   - Shared project templates
   - Centralized billing
   - Estimated: 16 hours

2. **Role-Based Access Control (RBAC)**
   - Roles: admin, editor, viewer
   - Permissions per resource
   - Audit log of actions
   - Estimated: 14 hours

3. **Team Collaboration**
   - Comments on projects
   - @mentions and notifications
   - Activity feed
   - Real-time presence (who's viewing)
   - Estimated: 18 hours

**Success Criteria:**
- Career services office can use for all students
- Admins can manage users and permissions
- Team can collaborate on applications

---

### 9B: White Label & Multi-Tenancy ⭐ LOW PRIORITY
**Goal:** Universities can brand as their own

**Tasks:**
1. **Theme Customization**
   - Custom colors, logo, fonts
   - Per-organization branding
   - CSS override system
   - Estimated: 12 hours

2. **Custom Domain**
   - careers.university.edu → wrapper instance
   - SSL certificates
   - Email from custom domain
   - Estimated: 10 hours

3. **Data Isolation**
   - Complete data separation between orgs
   - Cannot query across tenants
   - Compliance (FERPA for students)
   - Estimated: 14 hours

**Success Criteria:**
- UCLA Career Center has UCLA-branded instance
- USC Career Services has separate instance
- Data never leaks between tenants

---

### 9C: API for Third-Party Integration ⭐ MEDIUM PRIORITY
**Goal:** Others can build on the platform

**Tasks:**
1. **REST API Documentation**
   - OpenAPI spec
   - Interactive docs (Swagger)
   - Authentication (API keys)
   - Rate limiting
   - Estimated: 10 hours

2. **Webhooks**
   - Trigger on events (project created, skill completed)
   - Configurable endpoints
   - Retry logic
   - Event log
   - Estimated: 12 hours

3. **SDK/Client Libraries**
   - Python SDK
   - JavaScript SDK
   - Example integrations
   - Estimated: 16 hours

**Success Criteria:**
- External apps can integrate
- Webhooks notify other systems
- Partners can build on platform

---

## Phase 10: Business Features (Est. 3-4 weeks)

### 10A: Billing & Subscriptions ⭐ HIGH PRIORITY (if monetizing)
**Goal:** Accept payments for premium features

**Tasks:**
1. **Stripe Integration**
   - Subscription plans
   - Payment processing
   - Invoice generation
   - Estimated: 14 hours

2. **Usage-Based Billing**
   - Track skill invocations
   - Tiered pricing
   - Overage charges
   - Estimated: 12 hours

3. **Subscription Management**
   - Upgrade/downgrade plans
   - Cancel/pause subscription
   - Payment history
   - Estimated: 10 hours

**Success Criteria:**
- Can charge for service
- Automated billing
- Clear pricing tiers

---

### 10B: Admin Dashboard ⭐ MEDIUM PRIORITY
**Goal:** Manage users and system

**Tasks:**
1. **User Management**
   - View all users
   - Suspend/delete accounts
   - Password resets
   - Impersonate user (for support)
   - Estimated: 10 hours

2. **System Settings**
   - Feature flags
   - Rate limits
   - Maintenance mode
   - Global announcements
   - Estimated: 8 hours

3. **Analytics Dashboard**
   - Total users, projects, skills run
   - Growth metrics
   - Revenue (if applicable)
   - Health metrics
   - Estimated: 12 hours

**Success Criteria:**
- Can manage all aspects of system
- Visibility into usage and health
- Quick response to support requests

---

## Recommended Path Forward

### Option D: Focused Feature Path (2 weeks)
**For getting to next usable milestone quickly**

1. **Week 1:**
   - 2A.1: Add JSON to resume-alignment (4h)
   - 2A.2: Add JSON to cover-letter-voice (4h)
   - 2B.1: HTML Preview (8h)
   - 2B.2: PDF Preview (8h)

2. **Week 2:**
   - 3A.1: WebSocket Infrastructure (8h)
   - 3A.2: Skill Execution Streaming (10h)
   - 2C.1: Version Detection Service (4h)

**Result:** All key skills work, live preview, real-time updates

---

### Option E: Production-Ready Path (4 weeks)
**For deploying to real users**

1. **Week 1-2: Phase 4A & 4B**
   - Authentication
   - Database integration
   - Multi-user support

2. **Week 3: Phase 4C**
   - Error handling
   - Monitoring
   - Logging

3. **Week 4: Phase 8A & 8B**
   - Containerization
   - Cloud deployment
   - CI/CD

**Result:** Production-ready application with users

---

### Option F: AI-Enhanced Path (3 weeks)
**For maximum intelligence**

1. **Week 1:**
   - 5A: Anthropic API Direct Integration (streaming!)
   - 3B.1-3B.2: Intent Classification + Smart Prompts

2. **Week 2:**
   - 6A: Smart Suggestions
   - 3B.3: Conversational UI

3. **Week 3:**
   - 6B: Learning System
   - 6C.1-6C.2: PDF/URL extraction

**Result:** Intelligent assistant that learns and helps

---

### Option G: Enterprise Path (6 weeks)
**For selling to universities**

1. **Week 1-2: Phase 4A & 4B** (Auth + Database)
2. **Week 3-4: Phase 9A** (Teams & Orgs)
3. **Week 5: Phase 10A** (Billing)
4. **Week 6: Phase 9B** (White Label)

**Result:** Multi-tenant SaaS product

---

### Option H: Full Stack Excellence (8 weeks)
**For comprehensive application**

Combines D + E + F:
- Weeks 1-2: All remaining skills + live preview + WebSocket
- Weeks 3-4: Auth, database, error handling
- Weeks 5-6: Anthropic API, smart suggestions, conversational UI
- Weeks 7-8: Deployment, monitoring, CI/CD

**Result:** Feature-rich, production-ready, intelligent application

---

## Decision Matrix

| Path | Time | Complexity | User Value | Business Value | Technical Debt |
|------|------|------------|------------|----------------|----------------|
| D: Focused Feature | 2 wks | Low | High | Medium | Low |
| E: Production-Ready | 4 wks | Medium | Medium | High | Very Low |
| F: AI-Enhanced | 3 wks | Medium | Very High | Medium | Medium |
| G: Enterprise | 6 wks | High | Medium | Very High | Low |
| H: Full Stack | 8 wks | Very High | Very High | Very High | Very Low |

---

## Maintenance & Operations

### Ongoing Tasks (Post-Launch)
- **Weekly:** Review error logs, update dependencies
- **Monthly:** Security patches, performance review
- **Quarterly:** User feedback review, roadmap adjustment
- **Annually:** Major version upgrade, architecture review

### Technical Debt Management
- **Refactoring Budget:** 20% of development time
- **Test Coverage Goal:** 80%+ for backend, 60%+ for frontend
- **Documentation:** Update with every feature
- **Code Reviews:** Required for all changes

---

## Success Metrics by Phase

**Phase 2:** Feature adoption
- % of users using live preview
- Time saved vs. CLI workflow
- Version comparison usage

**Phase 4:** Production readiness
- Uptime (target: 99.9%)
- Error rate (target: <0.1%)
- Response time (target: <200ms p95)

**Phase 6:** AI effectiveness
- Suggestion acceptance rate
- Documents improved per session
- User satisfaction scores

**Phase 9:** Enterprise adoption
- Organizations using platform
- Users per organization
- Feature utilization rate

---

**This roadmap is a living document. Prioritize based on user feedback and business goals.**
