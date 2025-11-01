# Migrating from Socratic Steps to Skills

The Socratic career application process has been implemented as Claude Code skills.

## What Changed

**Before:** Markdown documentation in `Socratic Steps/`
**Now:** Executable skills in `~/.claude/skills/career/`

## Installation

Skills are already installed if you see them in:
```bash
ls ~/.claude/skills/career/
```

Should show:
- job-description-analysis/
- resume-alignment/
- job-fit-analysis/
- cover-letter-voice/
- collaborative-writing/

## Usage

**Invoke by natural language:**

Instead of: "Let's use the Socratic Resume Alignment process"
Now: "Tailor my resume for this job"

Skills activate automatically based on your request.

## Preserved Files

Original documentation preserved in `Socratic Steps/` for reference.

## Benefits of Skills

- ✅ Automatic lexicon loading
- ✅ Built-in verification (no fabrication)
- ✅ Evidence trails in outputs
- ✅ File organization handled automatically
- ✅ Resumable (can pause and continue)
- ✅ Integrated with career lexicons

## Support

See skill-specific README: `~/.claude/skills/career/README.md`
