# Career Lexicon Builder

[![Backend CI](https://github.com/AJBcoding/career-lexicon-builder/workflows/Backend%20CI/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)
[![Frontend CI](https://github.com/AJBcoding/career-lexicon-builder/workflows/Frontend%20CI/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)
[![Docker Build](https://github.com/AJBcoding/career-lexicon-builder/workflows/Docker%20Build%20and%20Push/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)

Transform your career history into actionable resources for job applications through AI-powered analysis, Socratic career skills, document formatting, and an intelligent web interface.

## 🚀 Quick Start

**→ [Complete Quickstart Guide](QUICKSTART.md)** - Comprehensive guide covering all features

**→ [Wrapper Setup](WRAPPER_SETUP.md)** - Set up the web application in 15 minutes

**→ [Socratic Skills Guide](QUICKSTART_SOCRATIC_SKILLS.md)** - Use interactive skills for job applications

## What This Does

The Career Lexicon Builder is a comprehensive suite of four integrated systems:

### 1. **Lexicon Generation** (Phase 3)
Analyzes your resumes, cover letters, and CVs using Claude AI to create four comprehensive lexicons documenting your career philosophy, achievements, narratives, and language patterns.

### 2. **Socratic Career Skills** (Phase 4)
Five interactive Claude Code skills that guide you through crafting job-specific materials using the Socratic method, ensuring every statement is grounded in your authentic experience.

### 3. **Document Formatting** (Weeks 1-2)
Professional CV and cover letter formatting with semantic styling, automatic structure detection, and .docx template generation.

### 4. **Wrapper Application** (Weeks 3-8)
Full-stack web interface with AI-powered chat, smart suggestions, document previews, and project management for job applications.

## ✨ Key Features

- **🤖 AI-Powered Analysis** - Claude analyzes your career documents to understand themes, achievements, and language patterns
- **💬 Socratic Guidance** - Interactive skills that refine your thinking through dialogue, preventing fabrication
- **📝 Professional Formatting** - Semantic .docx styling with automatic structure detection and learning system
- **🌐 Web Application** - Full-stack interface with real-time streaming AI, project management, and smart suggestions
- **🔒 Secure & Private** - JWT authentication, project ownership, user isolation
- **📊 Structured Output** - JSON exports for skills, markdown for readability, .docx for final documents
- **🔄 Incremental Updates** - Only reprocess changed documents, saving time and money
- **📚 Source Citations** - Every claim links to original documents, ensuring authenticity

## Getting Started (Choose Your Path)

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Install dependencies
pip install -r requirements.txt

# Set up Claude API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 1. Generate Your Lexicons (One-Time Setup)

Place your career documents (PDFs, .pages, .docx, etc.) in `my_documents/converted/` and run:

```bash
python3 run_llm_analysis.py
```

This will:
- Analyze all your career documents
- Generate 4 lexicons in `lexicons_llm/`:
  - `philosophy_and_values.md` - Core beliefs and principles
  - `achievements.md` - Hierarchical record of accomplishments
  - `narrative_patterns.md` - Storytelling frameworks and examples
  - `language_bank.md` - Professional terminology and phrasing

**Cost:** ~$1-2 per run (3-4 minutes for 37 PDFs, 47MB)

### 2. Use the Socratic Skills (Per Job Application)

The skills are installed in `~/.claude/skills/career/`:

1. **job-description-analysis** - Analyze job postings to understand true requirements
2. **resume-alignment** - Craft targeted resumes from your lexicons
3. **job-fit-analysis** - Validate alignment between you and the role
4. **cover-letter-voice** - Develop authentic cover letter strategies
5. **collaborative-writing** - Write materials with citation verification

See [QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md) for detailed usage.

## Cover Letter Formatting

Format academic and professional cover letters with semantic styling.

### Quick Start

```
User: Format this cover letter: [paste content]
Claude: [Analyzes, styles, generates formatted .docx + preview]
```

### Features
- Automatic structure detection (date, salutation, headers, body, closing)
- Content mention styling (institutions, positions, productions)
- Context-aware formatting (black thematic headers, not orange)
- Learning system remembers corrections
- Shares template with CV formatting

### Learn More
- [Format Cover Letter Skill Guide](docs/guides/format-cover-letter-skill-guide.md)
- [CV Template Guide](docs/guides/cv-template-guide.md)
- [System Design](docs/plans/2025-11-10-cover-letter-formatting-design.md)

## How It Works

### Phase 3: LLM Lexicon Generation

```
my_documents/converted/ → run_llm_analysis.py → lexicons_llm/
        (PDFs, .docx, etc.)        (Claude API)       (4 markdown files)
```

**Key Features:**
- Interpretive analysis (understands context and meaning)
- Hierarchical organization (from high-level to specific)
- Source citations (every claim links to original document)
- Incremental updates (only processes new/changed files)

**Architecture:**
- `analyzers/llm_analyzer.py` - Claude API integration
- `analyzers/llm_prompt_templates.py` - Specialized prompts for each lexicon
- `generators/hierarchical_generator.py` - Markdown output formatting
- `run_llm_analysis.py` - Main entry point

### Phase 4: Socratic Career Skills

Interactive workflows using the Socratic method:

```
Job Description → job-description-analysis → Understanding
     ↓
Lexicons + Job Understanding → resume-alignment → Targeted Resume
     ↓
Resume + Job → job-fit-analysis → Alignment Validation
     ↓
Fit Analysis + Lexicons → cover-letter-voice → Cover Letter Strategy
     ↓
Strategy + Lexicons → collaborative-writing → Final Materials
```

**Key Features:**
- Socratic questioning (refines thinking through dialogue)
- Lexicon grounding (every achievement cites source)
- Anti-fabrication safeguards (prevents invention of false claims)
- Iterative refinement (multiple review cycles)

**Documentation:**
- [SOCRATIC_SKILLS_SUMMARY.md](SOCRATIC_SKILLS_SUMMARY.md) - System overview
- [QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md) - User guide
- [DesignDocuments/2025-10-31-socratic-career-skills-system-design.md](DesignDocuments/2025-10-31-socratic-career-skills-system-design.md) - Technical design

## 🏗️ Repository Structure

```
career-lexicon-builder/
├── README.md                           # Project overview (you are here)
├── QUICKSTART.md                       # START HERE - Complete quickstart guide
├── WRAPPER_SETUP.md                    # Web application setup
│
├── analyzers/                          # Phase 3: LLM Analysis
│   ├── llm_analyzer.py                 # Claude API integration
│   └── llm_prompt_templates.py         # Lexicon-specific prompts
│
├── cv_formatting/                      # Document Formatting System
│   ├── style_applicator.py            # Apply semantic styles to .docx
│   ├── template_builder.py            # Generate .docx templates
│   ├── metadata_inference.py          # Infer document metadata
│   ├── learning_system.py             # Remember style corrections
│   └── templates/                     # .docx templates
│
├── wrapper-backend/                    # FastAPI Backend
│   ├── api/                           # API endpoints
│   │   ├── projects.py                # Project CRUD
│   │   ├── skills.py                  # Skill invocation
│   │   ├── chat.py                    # AI chat with streaming
│   │   └── auth.py                    # JWT authentication
│   ├── services/                      # Business logic
│   │   ├── anthropic_service.py       # Claude API integration
│   │   ├── chat_service.py            # Chat & intent classification
│   │   └── suggestions_service.py     # Smart suggestions
│   ├── models/                        # Database models
│   ├── tests/                         # 47 tests (all passing)
│   └── main.py                        # FastAPI app
│
├── wrapper-frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProjectDashboard.jsx   # Project list & creation
│   │   │   ├── ProjectWorkspace.jsx   # Project detail view
│   │   │   ├── ChatInterface.jsx      # AI chat with streaming
│   │   │   ├── PreviewPanel.jsx       # Document preview
│   │   │   └── SuggestionsPanel.jsx   # Smart suggestions
│   │   └── services/                  # API clients
│   └── package.json
│
├── my_documents/                       # Input
│   └── converted/                     # Your career documents (PDFs, etc.)
│
├── lexicons_llm/                       # Output
│   ├── 01_career_philosophy.md
│   ├── 02_achievement_library.md
│   ├── 03_narrative_patterns.md
│   └── 04_language_bank.md
│
├── docs/                               # Documentation
│   ├── guides/                        # User guides
│   ├── plans/                         # Design documents
│   └── handoffs/                      # Implementation handoffs
│
└── ~/.claude/skills/career/            # Phase 4: Socratic Skills
    ├── job-description-analysis/
    ├── resume-alignment/
    ├── job-fit-analysis/
    ├── cover-letter-voice/
    └── collaborative-writing/
```

## Project Evolution

See [PHASES.md](PHASES.md) for the complete story of how this project evolved from initial concept through two major pivots to the current production-ready system.

**TL;DR:** Started with conceptual Socratic skills, tried semantic similarity (too literal), pivoted to LLM-based analysis (works!), then implemented executable Socratic skills. The semantic analysis code has been archived in the `archive/phase2-semantic-analysis` branch.

## 📖 Complete Documentation

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - **START HERE** - Comprehensive guide covering all features
- **[WRAPPER_SETUP.md](WRAPPER_SETUP.md)** - Web application setup (15 minutes)
- **[QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md)** - How to use the five interactive skills
- **[docs/QUICKSTART_LATEST_FEATURES.md](docs/QUICKSTART_LATEST_FEATURES.md)** - Document management features

### User Guides
- **[docs/guides/format-cover-letter-skill-guide.md](docs/guides/format-cover-letter-skill-guide.md)** - Cover letter formatting
- **[docs/guides/format-resume-skill-guide.md](docs/guides/format-resume-skill-guide.md)** - Resume formatting (detailed)
- **[docs/guides/cv-template-guide.md](docs/guides/cv-template-guide.md)** - CV template structure

### System Documentation
- **[SOCRATIC_SKILLS_SUMMARY.md](SOCRATIC_SKILLS_SUMMARY.md)** - Skills system overview
- **[MVP_COMPLETE_HANDOFF.md](MVP_COMPLETE_HANDOFF.md)** - Wrapper MVP implementation details
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Future development roadmap
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[SECURITY.md](SECURITY.md)** - Security considerations

### Technical Documentation
- **[docs/TESTING.md](docs/TESTING.md)** - Comprehensive testing guide (81% coverage)
- **[HANDOFF.md](HANDOFF.md)** - Development handoff guide
- **[PHASES.md](PHASES.md)** - Project evolution history
- **[docs/LOGGING.md](docs/LOGGING.md)** - Logging architecture
- **[DOCKER_README.md](DOCKER_README.md)** - Docker containerization

### Code Reviews (2025-11-15)
- **[docs/reviews/REVIEW_INDEX.md](docs/reviews/REVIEW_INDEX.md)** - Review navigation guide
- **[docs/reviews/architecture_review.md](docs/reviews/architecture_review.md)** - Architecture & design patterns (14 issues)
- **[docs/reviews/security_audit_report.md](docs/reviews/security_audit_report.md)** - Security vulnerabilities (18 issues, 4 P0)
- **[docs/reviews/audit_summary.md](docs/reviews/audit_summary.md)** - Quick security reference
- **[docs/reviews/critical_issues_code_examples.md](docs/reviews/critical_issues_code_examples.md)** - Architecture fixes
- **[docs/reviews/remediation_code_examples.md](docs/reviews/remediation_code_examples.md)** - Security fixes

### Design Documents
- **[DesignDocuments/2025-10-31-llm-based-analysis-design.md](DesignDocuments/2025-10-31-llm-based-analysis-design.md)** - Lexicon generation design
- **[DesignDocuments/2025-10-31-socratic-career-skills-system-design.md](DesignDocuments/2025-10-31-socratic-career-skills-system-design.md)** - Socratic skills design
- **[docs/plans/2025-11-10-cover-letter-formatting-design.md](docs/plans/2025-11-10-cover-letter-formatting-design.md)** - Cover letter formatting design
- **[docs/plans/2025-11-11-wrapper-application-design.md](docs/plans/2025-11-11-wrapper-application-design.md)** - Wrapper application design
- **[docs/plans/2025-11-12-wrapper-development-roadmap.md](docs/plans/2025-11-12-wrapper-development-roadmap.md)** - Full development roadmap

## 🧪 Testing

**Current Test Coverage: 81%** (194 passing tests) ✅

See **[docs/TESTING.md](docs/TESTING.md)** for comprehensive testing guide, patterns, and best practices.

### Core System Tests
```bash
# Run all core system tests (194 tests, 81% coverage)
PYTHONPATH=. pytest tests/ -v --ignore=tests/wrapper-backend

# Generate coverage report
PYTHONPATH=. coverage run -m pytest tests/ --ignore=tests/wrapper-backend
coverage report --include="core/*,utils/*,generators/*"

# Run specific test files
PYTHONPATH=. pytest tests/test_core_orchestrator.py -v      # 100% coverage
PYTHONPATH=. pytest tests/test_confidence_scorer.py -v      # 100% coverage
PYTHONPATH=. pytest tests/test_core_state_manager.py -v     # 96% coverage
PYTHONPATH=. pytest tests/test_document_processor.py -v     # 96% coverage
```

**Coverage by Module:**
- **Core Systems** (97% coverage): orchestrator, state_manager, document_processor, confidence_scorer
- **Utilities** (85% coverage): date_parser, text_extraction
- **Generators** (75% coverage): hierarchical_generator

### Lexicon Generation Tests
```bash
# Run all tests (331 tests from Phase 2 semantic system)
pytest

# Run LLM analyzer tests
pytest tests/test_llm_analyzer.py
```

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

### Wrapper Application Tests
```bash
cd wrapper-backend
source venv/bin/activate

# Run all backend tests (47 tests)
pytest -v

# Run specific modules
pytest tests/test_auth.py -v                    # Authentication tests
pytest tests/test_authorization.py -v           # Authorization & ownership
pytest tests/test_anthropic_service.py -v       # Claude API integration
pytest tests/test_api_projects.py -v            # Projects API
pytest tests/test_api_skills.py -v              # Skills API
pytest tests/test_chat_service.py -v            # Chat & intent classification
```

**Frontend:**
```bash
cd wrapper-frontend
npm run build  # Verify no build errors
```

## 💰 Cost & Performance

**Lexicon Generation:**
- 37 PDFs (47MB): ~3-4 minutes, $1-2
- Incremental updates: Only processes changed files, <$0.50
- One-time setup, re-run when adding new documents

**Socratic Skills:**
- Free to use (runs in Claude Code conversations)
- Interactive sessions, no batch costs

**Document Formatting:**
- Free (local processing)
- Instant .docx generation

**Wrapper Application:**
- Development: Free (local PostgreSQL)
- Production: ~$5-20/month
  - Database hosting
  - Anthropic API usage (streaming)
  - Frontend/backend hosting (if deploying)

## 🚀 Production Deployment

**Docker Deployment:**
```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d
```

**CI/CD Pipelines:**
- GitHub Actions for backend, frontend, and Docker builds
- Automated testing on every push
- Container registry integration

**See:** [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide

## License

This is a personal project for career development. Not licensed for redistribution.

## Deprecated Code

The original semantic similarity system (Phase 2) has been archived in the `archive/phase2-semantic-analysis` branch. See [PHASES.md](PHASES.md) for why it was deprecated and how the LLM-based approach differs.
