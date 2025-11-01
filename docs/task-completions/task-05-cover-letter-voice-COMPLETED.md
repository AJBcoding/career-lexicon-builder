# Task 5: Cover Letter Voice Development - COMPLETED

**Completion Date:** 2025-10-31

## Implementation Summary

Created `~/.claude/skills/career/cover-letter-voice/SKILL.md` implementing complete narrative framework development process for authentic cover letter creation.

## File Details

- **Location:** `~/.claude/skills/career/cover-letter-voice/SKILL.md`
- **Size:** 1,524 lines, 47KB
- **Format:** Markdown with YAML frontmatter

## Implementation Includes

### Phase Structure (7 Phases: 0-6)

**Phase 0: Lexicon Loading**
- Job analysis file loading
- Career philosophy lexicon
- Narrative patterns lexicon
- Language bank lexicon
- Optional gap analysis plan
- Optional past cover letters

**Phase 1: Context Review**
- Job analysis summary (Sections I & III)
- Cover letter plan review (if available)
- Philosophy & pattern overview

**Phase 2: Content & Pattern Analysis**
- Past cover letter analysis (tone, structure, patterns)
- Narrative pattern extraction from lexicon
- Job requirements alignment
- Pattern-to-job recommendations

**Phase 3: Narrative Thread Exploration**
- AskUserQuestion tool for 3 narrative thread options
- Each option connects philosophy to job requirements
- Socratic deepening questions
- Evidence selection from achievements
- Tension/opportunity framing
- Complete narrative map creation

**Phase 4: Tone & Structure Framing**
- Tone profile development (formality, voice, register)
- Example opening sentence with tone notes
- Complete structure recommendation (opening + development + closing)
- Detailed draft guidance for each paragraph
- Length calculation based on role level

**Phase 5: Voice Consistency Check**
- Action verb verification against language_bank.md
- Power phrase verification
- Industry language verification
- Flag ANY language not in lexicon
- Replacement recommendations for non-lexicon terms

**Phase 6: Authenticity Review**
- Open-ended Socratic questions (4 questions)
- Philosophy alignment check (all core values)
- Authenticity confirmation gate
- User must confirm "feels authentic" before proceeding

### Output File Template

Complete `04-cover-letter-framework.md` template with:

**I. Tone Profile**
- Recommended voice characteristics
- Sentence structure guidance
- Vocabulary guidelines (use/avoid lists)

**II. Narrative Structure**
- Opening paragraph (pattern, draft guidance, example, philosophy connection)
- Development paragraphs (2-3, each with pattern, achievement, structure, draft guidance, language notes, philosophy connection)
- Optional gap-addressing paragraph
- Closing paragraph (pattern, draft guidance, example, tone notes)

**III. Evidence & Source Map**
- Complete traceability of all elements to lexicon sources
- Line-level citations for every element
- Fabrication check confirmation

**IV. Authenticity Confirmation**
- Checklist of authenticity criteria
- User confirmation timestamp
- User notes on what feels most authentic

**V. Next Steps**
- Three options: collaborative drafting, independent drafting, framework adjustment

### Error Handlers

**Error Handler A: Missing Job Analysis**
- Offer to invoke job-description-analysis skill
- Alternative: manual analysis path
- Warning about proceeding without analysis

**Error Handler B: Missing Lexicon Files**
- Detailed explanation of why each lexicon matters
- Instructions for generating lexicons
- Hard stop: cannot proceed without lexicons (anti-fabrication)

**Error Handler C: User Rejects Narrative Thread**
- Exploratory questions to understand concerns
- Generate alternative thread options
- Multiple rounds if needed
- Option to review job analysis or philosophy together

**Error Handler D: Tone Feels Inauthentic**
- Specific diagnostic questions
- Reference past letters if available
- User-drafted example sentence analysis
- Iterative tone adjustment until authentic

### Success Criteria

- ✓ Narrative framework grounded in philosophy lexicon
- ✓ All language choices traceable to language bank or past letters
- ✓ Tone matches job requirements + user's authentic voice
- ✓ Structure uses established narrative patterns
- ✓ User confirms: "This framework feels authentic to my voice"
- ✓ Complete evidence trail linking all content to sources

## Quality Standards Applied

**From Task 2 (job-description-analysis):**
- Clear numbered phase structure
- Comprehensive examples throughout
- Detailed error handling for all failure modes

**From Task 3 (resume-alignment):**
- Anti-fabrication safeguards (every element traces to lexicon)
- User confirmation gates at critical points
- Before/after comparisons for transparency
- Evidence trails with timestamps

**From Task 4 (job-fit-analysis):**
- Visual clarity (checkboxes, symbols)
- Empathetic error messages
- Multiple options presented via AskUserQuestion
- Strategic counseling approach
- Complete output templates with all sections

## Key Features

1. **Authenticity First:** Every narrative element must trace to philosophy/patterns/language lexicons
2. **Socratic Methodology:** One question at a time, structured choices via AskUserQuestion, incremental validation
3. **No Fabrication:** Framework only uses verified narrative patterns and language from lexicons
4. **User Confirmation:** Explicit "Yes" required for authenticity before saving
5. **Evidence Trails:** Complete source map linking all content to lexicon files with line numbers
6. **Example Opening:** Phase 4 provides example opening sentence with detailed tone notes
7. **Voice Consistency:** Phase 5 flags any language NOT in lexicon, offers replacements
8. **Complete Framework:** Not a draft, but complete strategic foundation for writing

## Design Specification Compliance

✓ All 7 phases (0-6) implemented exactly per design
✓ YAML frontmatter with name and description
✓ All required lexicon dependencies documented
✓ AskUserQuestion tool used in Phase 3 for narrative threads
✓ Example opening sentence with tone notes in Phase 4
✓ Voice consistency check flags non-lexicon language in Phase 5
✓ Complete output template with all 5 sections
✓ All 4 error handlers implemented (A-D)
✓ Success criteria clearly listed
✓ Evidence trails with source citations throughout

## Notes

This skill represents the most Socratic and authenticity-focused implementation in the suite. It includes:
- Multiple confirmation gates
- User-driven narrative selection via AskUserQuestion
- Hard stops for missing lexicons (anti-fabrication)
- Explicit authenticity review phase
- Complete traceability of every element

The skill creates a FRAMEWORK (strategic foundation) not a DRAFT (ready-to-send letter), maintaining user ownership and authentic voice throughout the process.

---

**Status:** COMPLETED ✓
**Ready for:** Testing, code review, Task 6 implementation
