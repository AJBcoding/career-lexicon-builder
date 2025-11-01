# Career Lexicon Builder - Development Handoff

**Last Updated:** November 1, 2025
**Status:** ✅ Production-Ready
**Version:** Phase 3 (LLM) + Phase 4 (Skills)

---

## Executive Summary

The Career Lexicon Builder is a two-phase system that helps you create authentic, grounded job application materials:

1. **Phase 3: LLM Lexicon Generation** - Analyzes your career documents using Claude API to generate four hierarchical reference guides
2. **Phase 4: Socratic Career Skills** - Five interactive skills that guide you through crafting job-specific materials using the Socratic method

**Key Innovation:** Anti-fabrication architecture - every achievement, value, and phrase in your job applications must trace to a verified source in your career history.

---

## Quick Start for Developers

### Setup

```bash
# Clone and install
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
pip install -r requirements.txt

# Set up Claude API key (for lexicon generation)
export ANTHROPIC_API_KEY="your-api-key-here"

# Generate lexicons (one-time)
python3 run_llm_analysis.py
```

### Skills Location

The Socratic Skills are installed at:
```
~/.claude/skills/career/
├── job-description-analysis/
├── resume-alignment/
├── job-fit-analysis/
├── cover-letter-voice/
└── collaborative-writing/
```

---

## System Architecture

### Two-Component Design

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: LLM Lexicon Generation (Python + Claude API)      │
│                                                              │
│ my_documents/converted/  →  run_llm_analysis.py            │
│   (PDFs, .docx, etc.)         ↓                            │
│                          analyzers/llm_analyzer.py          │
│                               ↓                             │
│                          lexicons_llm/                      │
│                           ├── 01_career_philosophy.md       │
│                           ├── 02_achievement_library.md     │
│                           ├── 03_narrative_patterns.md      │
│                           └── 04_language_bank.md           │
└─────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Socratic Skills (Claude Code)                     │
│                                                              │
│ User + Job Description  →  Skills (load lexicons)          │
│                               ↓                             │
│                        Socratic Dialogue                    │
│                               ↓                             │
│                   Verified Application Materials            │
│                   (every claim cited from lexicons)         │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 3: LLM Lexicon Generation

### Purpose

Convert raw career documents into actionable, hierarchical reference guides using interpretive AI analysis.

### Components

**1. LLM Analyzer** (`analyzers/llm_analyzer.py` - 257 lines)
- Claude API integration
- Four specialized analysis methods (one per lexicon)
- JSON parsing from Claude responses
- Error handling and fallbacks

**2. Prompt Templates** (`analyzers/llm_prompt_templates.py` - 392 lines)
- `PHILOSOPHY_PROMPT` - Extract meta-level themes about leadership and values
- `ACHIEVEMENTS_PROMPT` - Identify achievements with multiple framings
- `NARRATIVES_PROMPT` - Extract storytelling patterns and templates
- `LANGUAGE_PROMPT` - Catalog action verbs and signature phrases

**3. Hierarchical Generator** (`generators/hierarchical_generator.py` - 783 lines)
- Converts JSON analysis to navigable markdown
- Auto-generates tables of contents with anchor links
- Formats evidence quotes with context and sources
- Creates cross-references between sections

**4. Entry Point** (`run_llm_analysis.py` - 112 lines)
- End-to-end pipeline orchestration
- Progress reporting
- Error handling

### Generated Lexicons

#### 1. Career Philosophy & Values (`01_career_philosophy.md`)
- Leadership approaches (e.g., "Listening-First Leadership")
- Core values (e.g., "Arts as Essential Weavers")
- Problem-solving philosophy
- Each theme includes: principle, evidence, when to use, how to phrase

#### 2. Achievement Library (`02_achievement_library.md`)
- Major achievements organized by category
- 3-5 variations per achievement by emphasis:
  - Project Management focus
  - Financial Stewardship focus
  - Strategic Leadership focus
  - Stakeholder Relations focus
- Quantifiable outcomes
- STAR format breakdowns

#### 3. Narrative Patterns (`03_narrative_patterns.md`)
- Cover letter architecture patterns
- Resume bullet formulas
- Transition phrases
- Rhetorical moves
- Templates with placeholders and real examples

#### 4. Language Bank (`04_language_bank.md`)
- Action verbs by category (strategic, financial, project, people)
- Impact phrases (scale, growth, leadership context)
- Industry terminology
- Signature phrases
- Usage notes and alternatives

### Cost & Performance

**Cost:** ~$1-2 per full analysis (37 PDFs, 47MB)
**Time:** ~3-4 minutes
**When to re-run:** When adding new career documents or before major job search

---

## Phase 4: Socratic Career Skills

### Purpose

Guide users through job application development using verified content from lexicons, with anti-fabrication safeguards.

### Skills Overview

| Skill | Purpose | Lines | Files |
|-------|---------|-------|-------|
| **job-description-analysis** | Analyze job postings for requirements, culture, values | 480 | 4 |
| **resume-alignment** | Tailor resume with verified achievements | 480 | 1 |
| **job-fit-analysis** | Gap analysis + cover letter planning | 802 | 1 |
| **cover-letter-voice** | Develop authentic narrative framework | 1,524 | 1 |
| **collaborative-writing** | Co-create any professional writing | 689 | 1 |

**Total:** 3,975 lines of production-quality skill code

### Key Features

**1. Anti-Fabrication Safeguards**
- Source citations required for every achievement
- Before/after comparisons for transparency
- User confirmation gates at critical points
- Evidence trails with timestamps
- Voice consistency checks against language bank
- Hard stops if lexicons missing (for job-specific skills)

**2. Socratic Methodology**
- One question at a time
- Structured choices with context
- Incremental validation
- User-driven decisions at choice points

**3. Comparison-Ready Structure**
Job analysis outputs match lexicon categories exactly for direct alignment checking.

**4. Sequential Workflow**

```
1. Job Description → job-description-analysis → 01-job-analysis.md
2. Job Analysis + Lexicons → resume-alignment → 02-resume-tailored.md
3. Job + Resume → job-fit-analysis → 03-gap-analysis-and-cover-letter-plan.md
4. Gap Analysis + Lexicons → cover-letter-voice → 04-cover-letter-framework.md
5. Framework + Lexicons → collaborative-writing → 05-cover-letter-draft.md
```

---

## Repository Structure

```
career-lexicon-builder/
├── README.md                          # Main README (Phase 3 & 4)
├── HANDOFF.md                         # This file
├── PHASES.md                          # Project evolution history
├── QUICKSTART_SOCRATIC_SKILLS.md      # User guide for skills
├── SOCRATIC_SKILLS_SUMMARY.md         # Skills implementation summary
│
├── analyzers/                         # Phase 3: LLM Analysis
│   ├── llm_analyzer.py                # Claude API integration (257 lines)
│   └── llm_prompt_templates.py        # 4 specialized prompts (392 lines)
│
├── generators/                        # Phase 3: Output Generation
│   └── hierarchical_generator.py      # Markdown formatting (783 lines)
│
├── core/                              # Document Processing
│   ├── document_processor.py          # Document classification
│   ├── orchestrator.py                # Document ingestion (143 lines)
│   └── state_manager.py               # Incremental update tracking
│
├── utils/                             # Utilities
│   ├── text_extraction.py             # Extract from PDF, .docx, etc.
│   └── date_parser.py                 # Parse dates from filenames
│
├── run_llm_analysis.py                # Phase 3 entry point (112 lines)
│
├── my_documents/                      # Input
│   └── converted/                     # Career documents (37 PDFs)
│
├── lexicons_llm/                      # Output (Phase 3)
│   ├── 01_career_philosophy.md
│   ├── 02_achievement_library.md
│   ├── 03_narrative_patterns.md
│   └── 04_language_bank.md
│
├── tests/                             # Test Suite
│   └── (331 tests, 100% pass rate)
│
├── DesignDocuments/                   # Design Documentation
│   ├── 2025-10-31-llm-based-analysis-design.md
│   └── 2025-10-31-socratic-career-skills-system-design.md
│
└── docs/                              # Implementation Documentation
    ├── plans/
    │   └── 2025-10-31-socratic-career-skills-implementation.md
    └── task-completions/
        └── (4 task completion records)
```

**Skills Location (outside repo):**
```
~/.claude/skills/career/
├── README.md
├── job-description-analysis/
│   ├── SKILL.md (480 lines)
│   ├── ats-keyword-framework.md (242 lines)
│   ├── tone-analysis-guide.md (383 lines)
│   └── values-alignment-patterns.md (452 lines)
├── resume-alignment/
│   └── SKILL.md (480 lines)
├── job-fit-analysis/
│   └── SKILL.md (802 lines)
├── cover-letter-voice/
│   └── SKILL.md (1,524 lines)
└── collaborative-writing/
    └── SKILL.md (689 lines)
```

---

## Development Workflow

### Phase 3: Lexicon Generation

**Adding New Documents:**
1. Place PDFs in `my_documents/converted/`
2. Run `python3 run_llm_analysis.py`
3. Review generated lexicons in `lexicons_llm/`
4. Verify accuracy of extracted themes/achievements

**Customizing Output:**
1. Edit prompts in `analyzers/llm_prompt_templates.py`
2. Modify `IMPORTANT GUIDELINES` sections
3. Re-run analysis
4. Iterate until output matches needs

### Phase 4: Skills Modification

**Updating Skills:**
1. Edit files in `~/.claude/skills/career/`
2. Skills are read-only post-installation
3. Changes take effect immediately (no compilation)
4. Test with real job applications

**Adding New Skills:**
1. Create new directory in `~/.claude/skills/career/`
2. Follow existing skill structure
3. Add SKILL.md with frontmatter
4. Test thoroughly

---

## Testing

### Phase 3 Testing

```bash
# Run existing test suite (Phase 2 semantic tests)
pytest

# Manual validation
python3 run_llm_analysis.py
# Review output quality in lexicons_llm/
```

### Phase 4 Testing

See `TEST_PLAN.md` for comprehensive integration testing guide.

**Quick smoke test:**
1. Start Claude Code
2. Say "Analyze this job description" and paste a job posting
3. Verify skill loads, analyzes, produces 01-job-analysis.md
4. Check for source citations and structured output

---

## Dependencies

```bash
# Testing
pytest==8.4.2

# Document processing
pdfplumber==0.11.7
python-docx==1.2.0

# LLM-based analysis (Phase 3)
anthropic>=0.40.0
```

**Removed in deprecation:**
- `sentence-transformers` (Phase 2 semantic similarity)
- `scikit-learn` (Phase 2 clustering)

---

## Configuration

### Environment Variables

```bash
# Required for Phase 3 lexicon generation
export ANTHROPIC_API_KEY="your-api-key-here"
```

### File Paths (in `run_llm_analysis.py`)

```python
input_dir = "my_documents/converted"  # Source documents
output_dir = "lexicons_llm"           # Generated lexicons
```

### API Settings (in `analyzers/llm_analyzer.py`)

```python
model = "claude-3-5-sonnet-20241022"  # Claude model
max_tokens = 16000                     # Max response length
```

---

## Known Issues & Limitations

### Phase 3 (Lexicon Generation)

1. **API Key Required**
   - Claude Code subscription doesn't provide programmatic API key
   - Solution: Get separate API key from Anthropic (free $5 credits)

2. **Sequential Processing**
   - Four API calls run one at a time (not parallelized)
   - Total time: 3-4 minutes for 37 documents

3. **JSON Parsing Fallback**
   - If Claude returns non-JSON, system falls back to raw markdown
   - Rarely occurs with current prompts

### Phase 4 (Skills)

1. **Skills Are Read-Only Post-Installation**
   - Updates require manual file editing
   - Skills are in `~/.claude/skills/` for easy access

2. **Lexicons Are Point-in-Time**
   - Reflect career state when generated
   - Re-run `run_llm_analysis.py` to update

3. **No Cross-Job Learning**
   - Each application is independent
   - By design to prevent contamination

4. **Manual Export Required**
   - Skills produce markdown output
   - User exports to Word/PDF for submission

---

## Deprecated Code

### Phase 2: Semantic Similarity System

The original semantic similarity approach (using sentence-transformers and scikit-learn) was deprecated on November 1, 2025.

**Why deprecated:**
- Too literal (tracked "I believe..." phrases instead of meta-level themes)
- Too granular (flat bullet points instead of hierarchical structure)
- Not actionable (no guidance on when/how to use content)

**Where archived:**
- Branch: `archive/phase2-semantic-analysis`
- View at: https://github.com/AJBcoding/career-lexicon-builder/tree/archive/phase2-semantic-analysis

**Deleted files:**
- `analyzers/themes_analyzer.py`
- `analyzers/qualifications_analyzer.py`
- `analyzers/narratives_analyzer.py`
- `analyzers/keywords_analyzer.py`
- `generators/themes_lexicon_generator.py`
- `generators/qualifications_lexicon_generator.py`
- `generators/narratives_lexicon_generator.py`
- `generators/keywords_lexicon_generator.py`
- `core/confidence_scorer.py`
- `utils/similarity.py`

See `PHASES.md` for complete evolution history.

---

## Quality Metrics

### Phase 3 (LLM Lexicons)

**Output Quality:**
- Meta-level understanding (vs. literal phrase matching)
- Hierarchical structure (vs. flat lists)
- Actionable guidance (when to use, how to phrase)
- Source citations (document + date)

**Manual Validation Checklist:**
- [ ] Themes are meta-level, not literal
- [ ] Evidence accurately represents beliefs
- [ ] Major achievements captured with variations
- [ ] Narrative patterns reflect actual writing style
- [ ] Action verbs match authentic voice

### Phase 4 (Skills)

**Code Review Ratings:**
- Task 2 (job-description-analysis): 9/10
- Task 3 (resume-alignment): Excellent
- Task 4 (job-fit-analysis): 9.5/10
- Task 5 (cover-letter-voice): A (93/100)
- Task 6 (collaborative-writing): 9.5/10

**Anti-Fabrication Testing:**
- [ ] Source citations required
- [ ] User confirmation gates work
- [ ] Before/after comparisons shown
- [ ] Evidence trails generated
- [ ] Voice consistency checks active
- [ ] Hard stops for missing lexicons

---

## Support & Troubleshooting

### Common Issues

**"ValueError: API key required" (Phase 3)**
```bash
# Solution
export ANTHROPIC_API_KEY="your-api-key-here"

# Verify
echo $ANTHROPIC_API_KEY
```

**"JSON parsing failed" (Phase 3)**
- System falls back to raw markdown
- Check prompt templates for JSON format requirements
- Usually resolves itself on retry

**"Lexicons not found" (Phase 4)**
- Skills look for lexicons in `~/lexicons_llm/`
- Run `python3 run_llm_analysis.py` first
- Verify files exist with correct names

**Skills not loading (Phase 4)**
- Check skills are in `~/.claude/skills/career/`
- Verify SKILL.md files have correct frontmatter
- Restart Claude Code

### Getting Help

**Documentation:**
- README.md - Main overview
- QUICKSTART_SOCRATIC_SKILLS.md - User guide
- PHASES.md - Project evolution
- This file (HANDOFF.md) - Developer guide

**Design Documents:**
- `DesignDocuments/2025-10-31-llm-based-analysis-design.md`
- `DesignDocuments/2025-10-31-socratic-career-skills-system-design.md`

**Implementation Details:**
- `docs/plans/2025-10-31-socratic-career-skills-implementation.md`
- Code comments and docstrings throughout

---

## Next Steps

### For New Developers

1. **Understand the system:**
   - Read PHASES.md to understand evolution
   - Read README.md for user perspective
   - Review this HANDOFF.md for architecture

2. **Set up environment:**
   - Install dependencies: `pip install -r requirements.txt`
   - Get API key from console.anthropic.com
   - Run lexicon generation: `python3 run_llm_analysis.py`

3. **Test the skills:**
   - Find a real job posting
   - Use skills sequentially
   - Verify anti-fabrication safeguards
   - Review generated outputs

4. **Make improvements:**
   - Check GitHub issues for enhancements
   - Update prompts for better lexicon quality
   - Add time estimates to skills
   - Implement progress indicators

### For Users

1. **Generate lexicons:**
   - Place career documents in `my_documents/converted/`
   - Get API key from Anthropic (free $5 credits)
   - Run `python3 run_llm_analysis.py`
   - Review generated lexicons

2. **Use the skills:**
   - Read QUICKSTART_SOCRATIC_SKILLS.md
   - Start with job-description-analysis
   - Follow sequential workflow
   - Export final materials to Word/PDF

3. **Maintain system:**
   - Re-run lexicon generation when adding new documents
   - Update lexicons before major job search pushes
   - Provide feedback on skill quality

---

## Maintenance

### Regular Tasks

**Monthly:**
- Review and update lexicons if new career documents added
- Check for skill improvements based on usage

**Before Major Job Search:**
- Re-run lexicon generation
- Verify all achievements up to date
- Test skills with sample job posting

**After Career Changes:**
- Add new resumes/cover letters to `my_documents/converted/`
- Re-generate lexicons
- Review for accuracy

### Code Maintenance

**Dependencies:**
- Update `requirements.txt` when dependencies change
- Test after updates

**Skills:**
- Track user feedback
- Implement improvements
- Update documentation

**Tests:**
- Keep test suite passing
- Add integration tests for skills (see TEST_PLAN.md)

---

## Version History

**November 1, 2025** - Deprecation & Consolidation
- Deprecated Phase 2 semantic similarity system
- Archived Phase 2 code to `archive/phase2-semantic-analysis` branch
- Created comprehensive HANDOFF.md replacing 6 old handoff documents
- Updated README.md to focus on Phase 3 & 4

**October 31, 2025** - Phase 4 Complete
- Implemented 5 Socratic Career Skills
- 3,975 lines of production-ready skill code
- All code reviews 9/10 to 9.5/10
- Merged to main branch

**October 31, 2025** - Phase 3 Complete
- LLM-based lexicon generation system
- Four hierarchical markdown lexicons
- $1-2 cost, 3-4 minutes runtime

**October 2024** - Phase 1 & 2
- Initial Socratic Steps (conceptual framework)
- Phase 2 semantic similarity system (later deprecated)

See PHASES.md for complete evolution history.

---

## Summary

This system provides a production-ready, anti-fabrication architecture for creating authentic job application materials. Phase 3 generates verified career lexicons from your documents. Phase 4 uses those lexicons to guide you through crafting job-specific materials with complete evidence trails.

**Key Innovation:** Every achievement, value, and phrase in your job applications is traceable to a verified source in your career history, preventing fabrication while maintaining authenticity.

**Production Status:** ✅ Ready for real-world use

For questions or support, refer to skill-specific documentation in `~/.claude/skills/career/` or the comprehensive design documents in `DesignDocuments/`.

---

*Last Updated: November 1, 2025*
*Maintainer: Anthony Byrnes*
