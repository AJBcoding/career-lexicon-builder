# Career Lexicon Builder

[![Backend CI](https://github.com/AJBcoding/career-lexicon-builder/workflows/Backend%20CI/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)
[![Frontend CI](https://github.com/AJBcoding/career-lexicon-builder/workflows/Frontend%20CI/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)
[![Docker Build](https://github.com/AJBcoding/career-lexicon-builder/workflows/Docker%20Build%20and%20Push/badge.svg)](https://github.com/AJBcoding/career-lexicon-builder/actions)

Transform your career history into actionable resources for job applications through AI-powered analysis and Socratic career skills.

## What This Does

The Career Lexicon Builder is a two-part system:

1. **Lexicon Generation (Phase 3)** - Analyzes your resumes, cover letters, and CVs using Claude AI to create four comprehensive lexicons documenting your career philosophy, achievements, narratives, and language patterns.

2. **Socratic Career Skills (Phase 4)** - Five interactive Claude Code skills that guide you through crafting job-specific materials using the Socratic method, ensuring every statement is grounded in your authentic experience.

## Quick Start

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

## Repository Structure

```
career-lexicon-builder/
├── README.md                           # This file
├── PHASES.md                           # Project evolution documentation
├── QUICKSTART_SOCRATIC_SKILLS.md       # Skills user guide
├── SOCRATIC_SKILLS_SUMMARY.md          # Skills system overview
│
├── analyzers/                          # Phase 3: LLM Analysis
│   ├── llm_analyzer.py                 # Claude API integration
│   └── llm_prompt_templates.py         # Lexicon-specific prompts
│
├── generators/                         # Phase 3: Output Generation
│   └── hierarchical_generator.py       # Markdown lexicon formatting
│
├── core/                               # Document Processing
│   ├── document_processor.py           # Document classification
│   ├── orchestrator.py                 # Document ingestion
│   └── state_manager.py                # Incremental update tracking
│
├── utils/                              # Utilities
│   ├── text_extraction.py              # Extract from PDF, .docx, etc.
│   └── date_parser.py                  # Parse dates from filenames
│
├── my_documents/                       # Input
│   └── converted/                      # Your career documents (PDFs, etc.)
│
├── lexicons_llm/                       # Output
│   ├── philosophy_and_values.md
│   ├── achievements.md
│   ├── narrative_patterns.md
│   └── language_bank.md
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

## Documentation

- **For Users:**
  - [QUICKSTART_SOCRATIC_SKILLS.md](QUICKSTART_SOCRATIC_SKILLS.md) - How to use the skills
  - [README_LLM_ANALYSIS.md](README_LLM_ANALYSIS.md) - Lexicon generation details

- **For Developers:**
  - [HANDOFF.md](HANDOFF.md) - Development handoff guide
  - [PHASES.md](PHASES.md) - Project evolution
  - [DesignDocuments/2025-10-31-llm-based-analysis-design.md](DesignDocuments/2025-10-31-llm-based-analysis-design.md) - LLM system design
  - [DesignDocuments/2025-10-31-socratic-career-skills-system-design.md](DesignDocuments/2025-10-31-socratic-career-skills-system-design.md) - Skills system design

## Testing

```bash
# Run all tests (331 tests, 100% pass rate)
pytest

# Run specific test suite
pytest tests/test_llm_analyzer.py
```

**Note:** Tests were written for the archived Phase 2 semantic system. The LLM-based system (Phase 3) is tested through actual usage and manual validation of generated lexicons.

## Cost & Performance

**Lexicon Generation (Phase 3):**
- 37 PDFs (47MB): ~3-4 minutes, $1-2
- Incremental updates: Only processes changed files
- One-time setup, re-run when adding new documents

**Skills Usage (Phase 4):**
- Free to use (runs in Claude Code)
- Interactive sessions, no batch costs

## License

This is a personal project for career development. Not licensed for redistribution.

## Deprecated Code

The original semantic similarity system (Phase 2) has been archived in the `archive/phase2-semantic-analysis` branch. See [PHASES.md](PHASES.md) for why it was deprecated and how the LLM-based approach differs.
