# Career Lexicon Builder - Complete Quickstart Guide

**Transform your career history into job application materials through AI-powered analysis, document formatting, and an intelligent web interface.**

---

## 🎯 What This System Does

The Career Lexicon Builder is a comprehensive suite of tools for job seekers in academia and creative industries:

### 1. **Lexicon Generation** (Phase 3)
Analyzes your career documents with Claude AI to create four comprehensive reference guides documenting your philosophy, achievements, narratives, and language patterns.

### 2. **Socratic Career Skills** (Phase 4)
Five interactive Claude Code skills that guide you through crafting job-specific materials using the Socratic method, grounded in your authentic experience.

### 3. **Document Formatting** (Weeks 1-2)
Professional CV and cover letter formatting with semantic styling, automatic structure detection, and .docx template generation.

### 4. **Wrapper Application** (Weeks 3-8)
Full-stack web interface with AI-powered chat, smart suggestions, document previews, and project management for job applications.

---

## ⚡ Quick Start (Choose Your Path)

### Path A: Just Generate Lexicons (15 minutes)

Perfect for: Getting started, analyzing your documents, creating reference materials

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# 3. Place career documents in folder
mkdir -p my_documents/converted/
# Copy your PDFs, .docx files here

# 4. Generate lexicons
python3 run_llm_analysis.py
```

**Output:** Four markdown files in `lexicons_llm/` with your career philosophy, achievements, narratives, and language patterns.

**Cost:** ~$1-2 per run (3-4 minutes for 37 PDFs)

---

### Path B: Use Socratic Skills (30 minutes)

Perfect for: Crafting targeted resumes/cover letters for specific jobs

**Prerequisites:** Complete Path A first (generate lexicons)

```bash
# Skills are available in Claude Code conversations
# Example conversation:
You: "I need to apply for this job: [paste job description]"
Claude: [Uses job-description-analysis skill]

You: "Create a targeted resume for this role"
Claude: [Uses resume-alignment skill with your lexicons]

You: "Now help me write a cover letter"
Claude: [Uses cover-letter-voice skill]
```

**See:** [QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md) for detailed skill usage

---

### Path C: Format Documents (10 minutes)

Perfect for: Converting markdown drafts to polished .docx files

```bash
# Format a CV from markdown
python3 format_cv.py path/to/cv.md

# Format a cover letter
# (Use the format-cover-letter skill in Claude Code)
```

**Output:** Professionally formatted .docx file with semantic styling

**See:** [docs/guides/format-cover-letter-skill-guide.md](docs/guides/format-cover-letter-skill-guide.md)

---

### Path D: Run Full Web Application (45 minutes)

Perfect for: Managing multiple job applications with AI assistance

**Prerequisites:**
- Python 3.9+
- Node.js 18+
- PostgreSQL (or use Docker)

#### Option 1: Docker (Recommended)

```bash
# 1. Start all services
docker-compose up -d

# 2. Access application
open http://localhost:5173
```

#### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd wrapper-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python init_db.py

# Start server
python main.py
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd wrapper-frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start dev server
npm run dev
# Runs on http://localhost:5173
```

**See:** [WRAPPER_SETUP.md](WRAPPER_SETUP.md) for detailed setup

---

## 📚 Core Features Deep Dive

### Feature 1: Lexicon Generation

**What it does:** Analyzes your career documents using Claude AI to extract and organize:
- **Philosophy & Values** - Core beliefs, leadership principles, educational philosophy
- **Achievements** - Hierarchical record from high-level themes to specific accomplishments
- **Narrative Patterns** - Storytelling frameworks, opening hooks, thematic connections
- **Language Bank** - Professional terminology, action verbs, quantified impact statements

**How it works:**
```
my_documents/converted/ → run_llm_analysis.py → lexicons_llm/
     (Your PDFs)              (Claude API)        (4 .md files)
```

**Key Features:**
- **Interpretive Analysis** - Understands context and meaning, not just keywords
- **Hierarchical Organization** - From high-level themes to specific examples
- **Source Citations** - Every claim links to original document
- **Incremental Updates** - Only processes new/changed files

**Cost:** ~$1-2 per full run, less for incremental updates

**Documentation:**
- Technical design: [DesignDocuments/2025-10-31-llm-based-analysis-design.md](DesignDocuments/2025-10-31-llm-based-analysis-design.md)
- Latest features: [docs/QUICKSTART_LATEST_FEATURES.md](docs/QUICKSTART_LATEST_FEATURES.md)

---

### Feature 2: Socratic Career Skills

**What it does:** Five interactive Claude Code skills that guide you through job application development:

#### Skill 1: `job-description-analysis`
Analyzes job postings to understand true requirements and cultural fit signals.

**Example:**
```
You: [Paste job description]
Skill: What aspects of this role interest you most?
You: The teaching and administrative balance
Skill: [Identifies key themes, required vs. preferred qualifications]
```

#### Skill 2: `resume-alignment`
Crafts targeted resumes using your lexicon achievements.

**Example:**
```
Skill: Which achievements from your lexicon highlight teaching innovation?
You: Points to specific achievements
Skill: [Generates resume section with citations]
```

#### Skill 3: `job-fit-analysis`
Validates alignment between you and the role.

#### Skill 4: `cover-letter-voice`
Develops authentic cover letter strategies.

#### Skill 5: `collaborative-writing`
Writes materials with citation verification to prevent fabrication.

**Key Features:**
- **Socratic Questioning** - Refines thinking through dialogue
- **Lexicon Grounding** - Every claim cites source documents
- **Anti-Fabrication Safeguards** - Prevents invention of false achievements
- **Iterative Refinement** - Multiple review cycles

**Documentation:**
- User guide: [QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md)
- System overview: [SOCRATIC_SKILLS_SUMMARY.md](SOCRATIC_SKILLS_SUMMARY.md)
- Technical design: [DesignDocuments/2025-10-31-socratic-career-skills-system-design.md](DesignDocuments/2025-10-31-socratic-career-skills-system-design.md)

---

### Feature 3: Document Formatting

**What it does:** Converts markdown drafts to professionally formatted .docx files with semantic styling.

#### CV Formatting

**Features:**
- Page headers (name, page number on pages 2+)
- Section headers (EDUCATION, EXPERIENCE, etc.) - Orange, 11pt, Bold
- Subsection headers (Institution names) - Black, 11pt, Bold
- Inline mentions (productions, positions, venues) - Italics/Bold
- Automatic style learning from corrections

**Usage:**
```bash
python3 format_cv.py path/to/cv.md
# Output: cv.docx with semantic styles applied
```

**Documentation:** [docs/guides/cv-template-guide.md](docs/guides/cv-template-guide.md)

---

#### Cover Letter Formatting

**Features:**
- Automatic structure detection (date, salutation, headers, body, closing)
- Content mention styling (institutions → bold, productions → bold italic)
- Context-aware formatting (thematic headers are black 13pt, not orange like CVs)
- Learning system remembers corrections
- Shared template with CV formatting

**Usage:**
```
# In Claude Code conversation:
You: Format this cover letter: [paste content]
Claude: [Analyzes structure, applies styles, generates .docx + preview]
```

**Example Structure:**
```
November 25, 2024                      [Right-aligned, 11pt]

Dear Members of the Search Committee,  [Body Text]

[Body paragraphs with inline styling]

Why This Institution?                  [Section Header - Black, 13pt, Bold]

[More body paragraphs]

Thank you for your consideration,      [Body Text]

Anthony Byrnes                         [Body Text]
```

**Documentation:**
- Skill guide: [docs/guides/format-cover-letter-skill-guide.md](docs/guides/format-cover-letter-skill-guide.md)
- Design doc: [docs/plans/2025-11-10-cover-letter-formatting-design.md](docs/plans/2025-11-10-cover-letter-formatting-design.md)

---

### Feature 4: Wrapper Application

**What it does:** Full-stack web interface for managing job applications with AI assistance.

#### Architecture

**Frontend (React + Vite):**
- Project dashboard and workspace
- Real-time streaming AI chat
- Document preview panel
- Smart suggestions sidebar
- File upload with drag-and-drop

**Backend (FastAPI + Python):**
- PostgreSQL database with 4 models
- JWT authentication (register/login)
- Project ownership and authorization
- Anthropic API integration with streaming
- Structured JSON logging

**Key Features:**

**1. Project Management**
- Create job application projects
- Organize by institution, position, deadline
- Track application status
- Isolate projects by user ownership

**2. AI-Powered Chat**
- Conversational interface using Anthropic Claude
- Real-time streaming (token-by-token)
- Intent classification (routes to appropriate skills)
- Natural language skill invocation

**3. Smart Suggestions**
- Rule-based suggestions (e.g., "Upload job posting first")
- AI-powered suggestions based on project state
- Context-aware recommendations

**4. Document Preview**
- View generated markdown and JSON files
- PDF preview support
- Real-time updates as files change

**5. Authentication & Security**
- User registration and login
- JWT token-based auth
- Project ownership enforcement
- Authorization checks on all operations

#### Typical Workflow

```
1. Register/Login → http://localhost:5173

2. Create Project
   Institution: "UCLA"
   Position: "Assistant Dean"
   Deadline: 2025-03-01

3. Upload Job Posting
   [Drag and drop PDF or text file]

4. Chat with AI
   You: "Analyze this job description"
   AI: [Streams analysis, creates job-analysis.json]

5. View Suggestions
   "Based on the job analysis, create a targeted resume"
   [Click to execute]

6. Preview Documents
   Switch to Tools tab → See generated files
   - job-analysis.json
   - resume-draft.md
   - cover-letter-draft.md

7. Download Finals
   [Download formatted .docx files]
```

**Documentation:**
- Setup guide: [WRAPPER_SETUP.md](WRAPPER_SETUP.md)
- MVP handoff: [MVP_COMPLETE_HANDOFF.md](MVP_COMPLETE_HANDOFF.md)
- Next steps: [NEXT_STEPS.md](NEXT_STEPS.md)
- Design doc: [docs/plans/2025-11-11-wrapper-application-design.md](docs/plans/2025-11-11-wrapper-application-design.md)

---

## 🔄 Common Workflows

### Workflow 1: New Job Application from Scratch

**Goal:** Apply for a specific position using all system features

**Steps:**

1. **Generate Lexicons** (one-time setup)
   ```bash
   python3 run_llm_analysis.py
   # Creates lexicons_llm/*.md
   ```

2. **Analyze Job Posting** (via Socratic skills or wrapper)
   ```bash
   # Option A: Claude Code conversation
   You: [Paste job description]
   Claude: [Uses job-description-analysis skill]

   # Option B: Wrapper application
   # Upload job posting → Chat: "analyze this job"
   ```

3. **Create Targeted Resume**
   ```bash
   # Claude Code with resume-alignment skill
   Claude: Which achievements highlight [key requirement]?
   You: [Select from lexicon]
   Claude: [Generates resume section]
   ```

4. **Format Resume**
   ```bash
   python3 format_cv.py resume-draft.md
   # Output: resume-draft.docx
   ```

5. **Write Cover Letter**
   ```bash
   # Use cover-letter-voice skill
   Claude: What story connects your experience to this role?
   You: [Narrative from lexicon]
   Claude: [Suggests opening paragraph]
   ```

6. **Format Cover Letter**
   ```bash
   # In Claude Code:
   You: Format this cover letter: [paste content]
   Claude: [Generates formatted .docx + preview]
   ```

7. **Final Review**
   - Check all styling is correct
   - Verify citations to source documents
   - Confirm no fabricated achievements
   - Export to PDF

---

### Workflow 2: Batch Application Season

**Goal:** Apply for 10-20 positions efficiently

**Steps:**

1. **Setup Wrapper Application**
   ```bash
   docker-compose up -d
   # Access at http://localhost:5173
   ```

2. **Create Projects for Each Application**
   - Institution: "UCLA"
   - Position: "Assistant Dean"
   - Deadline: 2025-03-01
   - Status: "Researching"

3. **Research Phase** (for each project)
   - Upload job posting
   - Chat: "Analyze this job description"
   - Review generated `job-analysis.json`
   - Update status: "Drafting"

4. **Drafting Phase** (for each project)
   - Use resume-alignment skill
   - Use cover-letter-voice skill
   - Generate markdown drafts
   - Update status: "Formatting"

5. **Formatting Phase** (batch process)
   ```bash
   # Format all CVs
   for file in */resume-draft.md; do
     python3 format_cv.py "$file"
   done

   # Format cover letters via Claude Code skill
   ```

6. **Review & Submit**
   - Preview documents in wrapper
   - Download final .docx files
   - Export to PDF
   - Update status: "Submitted"

---

### Workflow 3: Update Lexicons with New Documents

**Goal:** Add recent work to your lexicons

**Steps:**

1. **Add New Documents**
   ```bash
   # Place new PDFs in my_documents/converted/
   cp ~/Downloads/2024-Annual-Report.pdf my_documents/converted/
   ```

2. **Standardize Filenames** (optional)
   ```bash
   python3 append_document_references.py --dry-run
   # Review what would happen

   python3 append_document_references.py
   # Renames files with date prefixes
   # Appends "Files Referenced" to lexicons
   ```

3. **Regenerate Lexicons**
   ```bash
   python3 run_llm_analysis.py
   # Only processes new/changed files (incremental)
   ```

4. **Review Updates**
   ```bash
   git diff lexicons_llm/
   # See what new content was added
   ```

**See:** [docs/QUICKSTART_LATEST_FEATURES.md](docs/QUICKSTART_LATEST_FEATURES.md) for document management features

---

## 📖 Documentation Map

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** (this file) - Complete quickstart guide
- **[README.md](README.md)** - Project overview
- **[WRAPPER_SETUP.md](WRAPPER_SETUP.md)** - Web application setup

### User Guides
- **[QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md)** - How to use the five skills
- **[docs/QUICKSTART_LATEST_FEATURES.md](docs/QUICKSTART_LATEST_FEATURES.md)** - Document management features
- **[docs/guides/format-cover-letter-skill-guide.md](docs/guides/format-cover-letter-skill-guide.md)** - Cover letter formatting
- **[docs/guides/format-resume-skill-guide.md](docs/guides/format-resume-skill-guide.md)** - Resume formatting (detailed)
- **[docs/guides/cv-template-guide.md](docs/guides/cv-template-guide.md)** - CV template structure

### Technical Documentation
- **[PHASES.md](PHASES.md)** - Project evolution history
- **[HANDOFF.md](HANDOFF.md)** - Development handoff guide
- **[MVP_COMPLETE_HANDOFF.md](MVP_COMPLETE_HANDOFF.md)** - Wrapper MVP implementation
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Future development roadmap

### Design Documents
- **[DesignDocuments/2025-10-31-llm-based-analysis-design.md](DesignDocuments/2025-10-31-llm-based-analysis-design.md)** - Lexicon generation design
- **[DesignDocuments/2025-10-31-socratic-career-skills-system-design.md](DesignDocuments/2025-10-31-socratic-career-skills-system-design.md)** - Socratic skills design
- **[docs/plans/2025-11-10-cover-letter-formatting-design.md](docs/plans/2025-11-10-cover-letter-formatting-design.md)** - Cover letter formatting design
- **[docs/plans/2025-11-11-wrapper-application-design.md](docs/plans/2025-11-11-wrapper-application-design.md)** - Wrapper application design
- **[docs/plans/2025-11-12-wrapper-development-roadmap.md](docs/plans/2025-11-12-wrapper-development-roadmap.md)** - Full development roadmap

### System-Specific Docs
- **[SOCRATIC_SKILLS_SUMMARY.md](SOCRATIC_SKILLS_SUMMARY.md)** - Skills system overview
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[DOCKER_README.md](DOCKER_README.md)** - Docker containerization
- **[SECURITY.md](SECURITY.md)** - Security considerations
- **[docs/LOGGING.md](docs/LOGGING.md)** - Logging architecture

### Testing & Validation
- **[TEST_PLAN.md](TEST_PLAN.md)** - Testing strategy
- **[docs/VALIDATION_SUMMARY.md](docs/VALIDATION_SUMMARY.md)** - Validation results

---

## 🧪 Testing

### Lexicon Generation Tests
```bash
# Run all tests (331 tests from Phase 2 semantic system)
pytest

# Run LLM analyzer tests
pytest tests/test_llm_analyzer.py
```

**Note:** Phase 3 LLM system tested through actual usage and manual validation.

---

### Document Formatting Tests
```bash
# CV formatting tests
pytest tests/test_format_cv_cli.py
pytest tests/test_cv_learning.py
pytest tests/test_cv_page_headers.py

# Cover letter formatting tests
pytest tests/test_cover_letter_formatting.py
pytest tests/test_ucla_cao_cover_letter.py

# Template tests
pytest tests/test_template_builder.py
pytest tests/test_style_applicator.py
```

---

### Wrapper Application Tests

**Backend (47 tests):**
```bash
cd wrapper-backend
source venv/bin/activate

# Run all tests
pytest -v

# Run specific modules
pytest tests/test_auth.py -v
pytest tests/test_authorization.py -v
pytest tests/test_anthropic_service.py -v
pytest tests/test_api_projects.py -v
pytest tests/test_api_skills.py -v
```

**Frontend:**
```bash
cd wrapper-frontend
npm run build  # Verify no build errors
```

---

## 💰 Cost & Performance

### Lexicon Generation
- **37 PDFs (47MB):** ~3-4 minutes, $1-2 total
- **Incremental updates:** Only processes changed files, <$0.50
- **One-time setup:** Re-run only when adding new documents

### Socratic Skills
- **Free to use** - Runs in Claude Code conversations
- **No batch costs** - Pay-as-you-go through your Anthropic account

### Wrapper Application
- **Development:** Free (local PostgreSQL)
- **Production:** ~$5-20/month depending on usage
  - Database hosting
  - Anthropic API usage (streaming)
  - Frontend/backend hosting (if deploying)

---

## 🚀 Production Deployment

### Docker Deployment (Recommended)

```bash
# 1. Build production images
docker-compose -f docker-compose.prod.yml build

# 2. Start services
docker-compose -f docker-compose.prod.yml up -d

# 3. Access application
open http://your-domain.com
```

**See:** [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide

---

### CI/CD Pipelines

The project includes GitHub Actions workflows:

- **Backend CI** - Run tests on every push
- **Frontend CI** - Build validation
- **Docker Build** - Build and push images to registry

**See:** `.github/workflows/` for pipeline configurations

---

## 🔧 Troubleshooting

### Lexicon Generation Issues

**Problem:** "No API key found"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Problem:** "No documents found"
```bash
# Ensure documents are in correct directory
ls my_documents/converted/
```

---

### Document Formatting Issues

**Problem:** "Style not found in template"
```bash
# Regenerate template
python3 generate_cv_template.py
```

**Problem:** "Learning system not persisting"
```bash
# Check cv_style_mapping.json exists
ls -la cv_formatting/
```

---

### Wrapper Application Issues

**Problem:** Backend won't start
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Or start with Docker Compose
docker-compose up -d
```

**Problem:** Frontend shows "Backend Status: error"
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS configuration in wrapper-backend/main.py
```

**Problem:** Authentication fails
```bash
# Reinitialize database
cd wrapper-backend
python init_db.py
```

**See:** [WRAPPER_SETUP.md](WRAPPER_SETUP.md) for detailed troubleshooting

---

## 📄 License

This is a personal project for career development. Not licensed for redistribution.

---

## 🎯 What's Next?

After completing this quickstart:

1. **Generate your lexicons** - Run `run_llm_analysis.py` to create your career reference guides
2. **Try the Socratic skills** - Practice with a real job description
3. **Explore document formatting** - Format a CV or cover letter
4. **Set up the wrapper** - If managing multiple applications

For more advanced usage, see:
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Future development roadmap
- **[docs/plans/2025-11-12-wrapper-development-roadmap.md](docs/plans/2025-11-12-wrapper-development-roadmap.md)** - Extended features

---

## 📞 Need Help?

- **Documentation Issues:** Check [Documentation Map](#-documentation-map) above
- **Technical Questions:** Review design documents in `docs/plans/`
- **Bug Reports:** Check [TEST_PLAN.md](TEST_PLAN.md) and [VALIDATION_SUMMARY.md](docs/VALIDATION_SUMMARY.md)

---

**Last Updated:** November 14, 2025
**System Version:** 4.0 (Wrapper Application Complete)
