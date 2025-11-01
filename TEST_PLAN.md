# End-to-End Integration Test Plan

**Status:** Ready for User Testing
**Created:** 2025-10-31

## Overview

All 5 Socratic Career Skills have been implemented, code-reviewed, and approved with ratings of 9/10 to 9.5/10. This document outlines the integration testing plan to validate the complete workflow with real user data.

## Implementation Status

### Skills Completed

| # | Skill | Status | Code Review | File Size | Location |
|---|-------|--------|-------------|-----------|----------|
| 1 | job-description-analysis | ✅ Complete | 9/10 | 480 lines (14KB) | ~/.claude/skills/career/job-description-analysis/ |
| 2 | resume-alignment | ✅ Complete | Excellent | 480 lines (13KB) | ~/.claude/skills/career/resume-alignment/ |
| 3 | job-fit-analysis | ✅ Complete | 9.5/10 | 802 lines (25KB) | ~/.claude/skills/career/job-fit-analysis/ |
| 4 | cover-letter-voice | ✅ Complete | A (93/100) | 1,524 lines (47KB) | ~/.claude/skills/career/cover-letter-voice/ |
| 5 | collaborative-writing | ✅ Complete | 9.5/10 | 689 lines (21KB) | ~/.claude/skills/career/collaborative-writing/ |

### Supporting Documentation

- ✅ Installation README (`~/.claude/skills/career/README.md`)
- ✅ Design specification (DesignDocuments/2025-10-31-socratic-career-skills-system-design.md)
- ✅ Implementation plan (docs/plans/2025-10-31-socratic-career-skills-implementation.md)
- ✅ Task completion markers (docs/task-completions/task-01 through task-07)

## Prerequisites for Testing

### Required

1. **Career Lexicons Generated**
   ```bash
   cd /path/to/career-lexicon-builder
   python run_llm_analysis.py
   ```

   Verify lexicons exist:
   ```bash
   ls ~/lexicons_llm/
   # Should show:
   # 01_career_philosophy.md
   # 02_achievement_library.md
   # 03_narrative_patterns.md
   # 04_language_bank.md
   ```

2. **Test Materials**
   - Real job description (copy from online posting)
   - Current resume (your actual resume file)
   - Optional: Past cover letters for tone reference

### Optional

- Multiple job descriptions for comparison testing
- Various resume versions to test different scenarios

## Test Scenarios

### Scenario 1: Complete Job Application Workflow

**Objective:** Validate all 5 skills work together for a real job application

**Steps:**

1. **Job Description Analysis**
   ```
   User: "Analyze this job description"
   [Paste actual job posting]
   ```

   **Verify:**
   - [ ] Skill activates automatically
   - [ ] Generates 4 lexicon-matched sections:
     - Section I: Values & Philosophy Requirements
     - Section II: Experience & Achievement Requirements
     - Section III: Communication & Narrative Requirements
     - Section IV: Language & Terminology Requirements
   - [ ] ATS keywords identified
   - [ ] Cultural tone analyzed
   - [ ] Red flags noted (if any)
   - [ ] Output saved to: `~/career-applications/[job-slug]/01-job-analysis.md`

2. **Resume Alignment**
   ```
   User: "Tailor my resume for this role"
   [Upload current resume]
   ```

   **Verify:**
   - [ ] Loads job analysis automatically
   - [ ] Loads achievement library and language bank
   - [ ] Presents side-by-side comparisons (original vs. proposed)
   - [ ] Every achievement includes source citation
   - [ ] Requires explicit user confirmation for each change
   - [ ] Creates evidence trail with timestamps
   - [ ] No fabricated content
   - [ ] Output saved to: `~/career-applications/[job-slug]/02-resume-tailored.md`

3. **Job Fit Analysis**
   ```
   User: "Analyze my fit for this role"
   ```

   **Verify:**
   - [ ] Loads job analysis and lexicons
   - [ ] Gap analysis uses ✅/⚠️/❌ symbols clearly
   - [ ] Identifies strong matches with evidence
   - [ ] Identifies partial matches with context
   - [ ] Identifies gaps honestly
   - [ ] Reframing strategies grounded in actual achievements
   - [ ] Cover letter plan includes specific narrative direction
   - [ ] All recommendations link to lexicon sources
   - [ ] Output saved to: `~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md`

4. **Cover Letter Voice Development**
   ```
   User: "Develop my cover letter narrative"
   [Optionally: Upload past cover letters]
   ```

   **Verify:**
   - [ ] Loads all required lexicons
   - [ ] Analyzes past letters if provided
   - [ ] Uses AskUserQuestion for narrative thread selection
   - [ ] Presents 3 narrative thread options
   - [ ] Explores chosen thread with follow-up questions
   - [ ] Develops tone profile matching job + user voice
   - [ ] Provides example opening sentence with tone notes
   - [ ] Recommends complete structure (opening, development, closing)
   - [ ] Flags any language not in lexicon
   - [ ] Requires explicit authenticity confirmation
   - [ ] Output saved to: `~/career-applications/[job-slug]/04-cover-letter-framework.md`

5. **Collaborative Writing**
   ```
   User: "Help me draft the cover letter"
   ```

   **Verify:**
   - [ ] Loads lexicons (if available)
   - [ ] References cover letter framework (if exists)
   - [ ] Follows 5-phase Socratic process
   - [ ] Drafts in 50-150 word segments
   - [ ] Voice consistency checks (if lexicons loaded)
   - [ ] Iterative refinement based on feedback
   - [ ] Final draft feels authentic to user
   - [ ] Output saved to: user-specified location

### Scenario 2: Graceful Degradation (No Lexicons)

**Objective:** Verify skills work without lexicons

**Steps:**

1. **Test with missing lexicons:**
   ```bash
   # Temporarily rename lexicons directory
   mv ~/lexicons_llm ~/lexicons_llm.backup
   ```

2. **Run Collaborative Writing:**
   ```
   User: "Help me write a recommendation letter"
   ```

   **Verify:**
   - [ ] Skill reports lexicons not found with positive message
   - [ ] Proceeds confidently without lexicons
   - [ ] Voice profile developed through dialogue
   - [ ] Quality output achieved
   - [ ] No errors or failures

3. **Restore lexicons:**
   ```bash
   mv ~/lexicons_llm.backup ~/lexicons_llm
   ```

### Scenario 3: Skill Independence

**Objective:** Verify skills work standalone

**Steps:**

1. **Skip job analysis, go directly to collaborative writing:**
   ```
   User: "Help me write a professional statement"
   ```

   **Verify:**
   - [ ] Works without job analysis
   - [ ] Discovers context through dialogue
   - [ ] Produces quality output

2. **Use job fit analysis without resume alignment:**
   ```
   User: "Analyze my fit for [job]"
   ```

   **Verify:**
   - [ ] Works independently
   - [ ] Gracefully handles missing resume tailoring

### Scenario 4: Error Handling

**Objective:** Verify robust error handling

**Test Cases:**

1. **Missing job analysis when expected:**
   - Resume alignment invoked without job analysis
   - **Verify:** Offers to analyze job first

2. **No matching achievements:**
   - Job requires experience not in library
   - **Verify:** Identifies as gap, offers reframing strategies

3. **User rejects proposed content:**
   - User says "No, that's not accurate"
   - **Verify:** Asks clarifying questions, revises, doesn't force inaccurate content

4. **Weak competitive position:**
   - User significantly under-qualified
   - **Verify:** Honest assessment, strategic counseling, empowers user decision

## Integration Points to Validate

### File Passing

- [ ] Job analysis → Resume alignment
- [ ] Job analysis → Job fit analysis
- [ ] Job analysis → Cover letter voice
- [ ] Cover letter plan → Cover letter voice
- [ ] Cover letter framework → Collaborative writing

### Lexicon Access

- [ ] All skills can read from `~/lexicons_llm/`
- [ ] Lexicon content properly loaded into context
- [ ] Source citations include correct line numbers

### File Organization

- [ ] Files saved to `~/career-applications/[job-slug]/`
- [ ] Naming convention followed (01, 02, 03, 04, 05)
- [ ] No cross-contamination between different jobs
- [ ] Archive structure (if used)

### Evidence Trails

- [ ] All resume bullets cite sources
- [ ] All cover letter content cites sources
- [ ] Evidence trails include timestamps
- [ ] User confirmations documented

### Authenticity Safeguards

- [ ] No fabricated achievements in resume
- [ ] No hallucinated language in cover letter
- [ ] Before/after comparisons for all changes
- [ ] User confirmation required at critical points
- [ ] Hard stops when fabrication detected

## Success Criteria

**Individual Skills:**
- ✅ Each skill produces expected output
- ✅ All phases execute correctly
- ✅ Error handlers work as designed
- ✅ User confirmations function properly

**Integration:**
- ✅ Skills read each other's outputs correctly
- ✅ Lexicon references work across all skills
- ✅ File organization consistent
- ✅ Evidence trails complete
- ✅ No fabrication detected
- ✅ Socratic process maintained throughout

**User Experience:**
- ✅ Natural language invocation works
- ✅ Skills feel cohesive (not disconnected)
- ✅ Workflow is intuitive
- ✅ User feels supported (not interrogated)
- ✅ Outputs are immediately useful
- ✅ User confident in authenticity of materials

## Known Limitations

1. **Skills Cannot Edit Themselves**
   - Skills are read-only once installed
   - Updates require manual file editing or reinstallation

2. **Lexicons Are Point-in-Time**
   - Skills use lexicons as they existed when generated
   - Updates require re-running `run_llm_analysis.py`

3. **No Cross-Job Learning**
   - Each job application is independent
   - Skills don't learn from previous applications

4. **Manual Resume Export**
   - Skills produce markdown output
   - User must export to Word/PDF for submission

## Test Results Documentation

After testing, document results in: `TEST_RESULTS.md`

**Include:**
- Date of testing
- Which scenarios were tested
- Successes (what worked well)
- Issues found (bugs, usability problems)
- User feedback (surprising, delightful, frustrating)
- Recommendations for improvements

## Next Steps After Testing

1. **If tests pass:**
   - Proceed to Task 9: Documentation & Deployment
   - Update main README with usage instructions
   - Create migration guide
   - Merge to main branch

2. **If issues found:**
   - Document issues in GitHub issues or similar
   - Prioritize fixes (critical, important, nice-to-have)
   - Fix critical issues before deployment
   - Plan important issues for future iterations

3. **Ongoing:**
   - Collect user feedback during real usage
   - Iterate on skills based on real-world experience
   - Update lexicons as career progresses
   - Refine prompts based on what works

## Testing Resources

**Documentation:**
- Skill-specific workflows: Each `SKILL.md` file
- Design document: `DesignDocuments/2025-10-31-socratic-career-skills-system-design.md`
- Installation guide: `~/.claude/skills/career/README.md`

**Support:**
- Code reviews available in: `docs/task-completions/`
- Implementation plan: `docs/plans/2025-10-31-socratic-career-skills-implementation.md`

---

**Note:** This test plan assumes user has actual job opportunities to apply for and real career materials to work with. Skills are designed for real-world use, not synthetic test data.
