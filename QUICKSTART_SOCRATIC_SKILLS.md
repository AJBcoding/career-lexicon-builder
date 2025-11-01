# Socratic Career Skills - Quick Start Guide

**Get started with your personalized career application assistant in 3 steps.**

---

## Step 1: Generate Your Career Lexicons (One-Time Setup)

Your skills need to learn your authentic voice first.

```bash
cd /path/to/career-lexicon-builder
python run_llm_analysis.py
```

**What this does:**
- Analyzes your existing career documents (resumes, cover letters, statements)
- Creates 4 lexicon files in `~/lexicons_llm/`
- Takes 2-3 minutes to complete

**Required files in `my_documents/` folder:**
- At least 2-3 career documents
- Formats supported: PDF, Word, .pages, text, markdown

**Output:**
```
~/lexicons_llm/
├── 01_career_philosophy.md      # Your values and approach
├── 02_achievement_library.md    # Your achievements with variations
├── 03_narrative_patterns.md     # Your storytelling patterns
└── 04_language_bank.md          # Your authentic language
```

**✅ You only need to do this once** (or when you have new career experiences to add)

---

## Step 2: Find a Job Opportunity

Copy a job description you're interested in. You'll need the full text.

**Good sources:**
- Company career pages
- LinkedIn job postings
- Indeed, Glassdoor, etc.

**Tip:** Copy the entire posting including:
- Job title
- Company description
- Responsibilities
- Requirements
- About section
- Application instructions

---

## Step 3: Start Using the Skills

Simply talk to Claude naturally. Skills activate automatically.

### For a Complete Job Application

**Skill 1: Analyze the Job** (2-3 minutes)
```
You: "Analyze this job description"

[Paste the full job posting]
```

**What you get:**
- Structured analysis in 4 sections (values, experience, communication, language)
- ATS keywords identified
- Cultural tone decoded
- Red flags noted
- Saved to: `~/career-applications/[job-slug]/01-job-analysis.md`

---

**Skill 2: Tailor Your Resume** (10-15 minutes)
```
You: "Tailor my resume for this job"

[Upload your current resume]
```

**What happens:**
- Loads job analysis automatically
- Presents side-by-side comparisons for each change
- Every achievement includes source citation from your library
- You confirm each change ("Yes" / "No" / "Adjust")
- Creates evidence trail with timestamps

**What you get:**
- Tailored resume with verified content
- ATS-optimized for the specific job
- Every statement traceable to your actual experience
- Saved to: `~/career-applications/[job-slug]/02-resume-tailored.md`

**Important:** You must confirm authenticity before it saves anything!

---

**Skill 3: Understand Your Fit** (15-20 minutes)
```
You: "Analyze my fit for this role"
```

**What happens:**
- Compares job requirements with your achievements
- Uses symbols: ✅ Strong match, ⚠️ Partial match, ❌ Gap
- Develops reframing strategies for gaps
- Creates cover letter strategic plan

**What you get:**
- Honest gap analysis
- Reframing strategies grounded in your actual achievements
- Cover letter plan with 3-4 key messages
- Saved to: `~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md`

**Example output:**
```markdown
### Capital Projects & Infrastructure
JD Requirement: "$10M+ budget experience"

✅ STRONG MATCH: Kirk Douglas Theater
   - $12.1M budget (exceeds requirement)
   - Source: achievement_library.md:320-430

⚠️ PARTIAL MATCH: Outdoor Amphitheater
   - Smaller scale but demonstrates range

❌ GAP: Change management certification
   - Not in library, need reframing strategy
```

---

**Skill 4: Develop Your Narrative** (20-30 minutes)
```
You: "Develop my cover letter narrative"
```

**What happens:**
- Asks you to choose narrative thread (3 options presented)
- Develops tone profile matching job culture + your voice
- Creates paragraph-by-paragraph framework
- Checks all language against your language bank
- Requires authenticity confirmation

**What you get:**
- Complete cover letter framework (not a draft!)
- Tone profile with examples
- Structure with draft guidance for each paragraph
- Voice consistency notes
- Saved to: `~/career-applications/[job-slug]/04-cover-letter-framework.md`

**Note:** This creates a strategic foundation, not a ready-to-send letter.

---

**Skill 5: Write the Letter Together** (30-45 minutes)
```
You: "Help me draft the cover letter"
```

**What happens:**
- Co-creates the actual letter through dialogue
- Drafts in 50-150 word segments
- You review and adjust each segment
- Voice consistency checks (if lexicons loaded)
- Iterative refinement until you're satisfied

**What you get:**
- Complete cover letter draft in your authentic voice
- Ready to export to Word/PDF
- Saved to: `~/career-applications/[job-slug]/05-cover-letter-draft.md`

---

## Quick Reference Commands

| What You Want | What to Say |
|---------------|-------------|
| Analyze a job posting | "Analyze this job description" |
| Customize your resume | "Tailor my resume for this job" |
| Understand fit | "Analyze my fit for this role" |
| Plan cover letter | "Develop my cover letter narrative" |
| Write cover letter | "Help me draft the cover letter" |
| Any professional writing | "Help me write [type of document]" |

---

## Your File Organization

After a complete workflow, you'll have:

```
~/career-applications/
└── 2025-10-31-ucla-senior-director/
    ├── 01-job-analysis.md                    # From Skill 1
    ├── 02-resume-tailored.md                 # From Skill 2
    ├── 03-gap-analysis-and-cover-letter-plan.md  # From Skill 3
    ├── 04-cover-letter-framework.md          # From Skill 4
    └── 05-cover-letter-draft.md              # From Skill 5
```

Each file includes:
- YAML metadata (job title, company, date)
- Main content
- Evidence & source map
- Verification checklist

---

## Tips for Best Results

### ✅ Do This

1. **Generate lexicons first** - Skills need your authentic voice to work properly
2. **Copy complete job postings** - More context = better analysis
3. **Read and confirm changes** - You're in control, not the AI
4. **Say "No" if something's inaccurate** - Skills will revise, not force content
5. **Use skills in sequence** - Each builds on the previous

### ❌ Avoid This

1. **Skipping lexicon generation** - Skills won't have your authentic voice
2. **Copying partial job descriptions** - Missing context hurts analysis
3. **Auto-confirming without reading** - Defeats the authenticity safeguards
4. **Accepting inaccurate content** - Always speak up if something's wrong
5. **Using generic templates** - The whole point is personalization

---

## Common Scenarios

### "I have multiple job opportunities"

Run the workflow for each job independently:

```
Job 1: "Analyze this [Company A] job description"
       → Creates: ~/career-applications/2025-10-31-companyA-role/

Job 2: "Analyze this [Company B] job description"
       → Creates: ~/career-applications/2025-11-01-companyB-role/
```

Each application is isolated - no cross-contamination.

---

### "I need to update my lexicons"

When you have new career experiences:

```bash
# Add new documents to my_documents/ folder
cd /path/to/career-lexicon-builder
python run_llm_analysis.py
```

Skills automatically use updated lexicons on next invocation.

---

### "I just want to write something, not apply for a job"

Use collaborative-writing skill for any professional writing:

```
You: "Help me write a recommendation letter for my colleague"
You: "Co-write this professional statement with me"
You: "Draft an email to the board about [topic]"
```

This skill works with OR without lexicons (graceful degradation).

---

### "I want to skip a step"

Skills work independently! You can:

- Use only job-description-analysis to evaluate opportunities
- Use only collaborative-writing for any professional document
- Use job-fit-analysis to understand competitive position
- Mix and match as needed

---

## Troubleshooting

### "Skills say lexicons are missing"

```bash
# Check if they exist:
ls ~/lexicons_llm/

# If missing, generate them:
cd /path/to/career-lexicon-builder
python run_llm_analysis.py
```

---

### "Resume skill won't include an achievement"

**This is working correctly!** The skill only includes achievements from your verified library.

**Options:**
1. Add the experience to your documents and regenerate lexicons
2. Document it as a gap in the job-fit-analysis
3. Address it in your cover letter with explanation

**The skill will never fabricate.** This is intentional.

---

### "Cover letter doesn't sound like me"

Tell the skill! It will ask:
- "What feels inauthentic?"
- "Which part doesn't sound like your voice?"
- "What would make this more authentic?"

The skill adjusts based on your feedback. You're in control.

---

### "I need to export to Word/PDF"

Skills produce markdown files. To export:

1. Open the markdown file
2. Copy content
3. Paste into Word/Google Docs
4. Format as needed
5. Export to PDF

**Future enhancement:** Direct export integration planned.

---

## Time Expectations

**First-time complete workflow:** ~2-3 hours
- Job analysis: 2-3 minutes
- Resume tailoring: 10-15 minutes
- Fit analysis: 15-20 minutes
- Cover letter voice: 20-30 minutes
- Collaborative writing: 30-45 minutes

**Repeat applications:** ~1-2 hours (faster with practice)

**Individual skills:** As listed above

---

## What Makes This Different

### Traditional Approach
- Generic AI writes everything
- No source verification
- Fabricated achievements
- Generic voice
- No evidence trail

### Socratic Skills Approach
- ✅ All content verified against YOUR career history
- ✅ Every statement includes source citation
- ✅ No fabrication possible (multiple safeguards)
- ✅ Your authentic voice (from language bank)
- ✅ Complete evidence trail with timestamps

**You maintain control and authenticity throughout.**

---

## Next Steps

1. **Generate lexicons** (if not done): `python run_llm_analysis.py`
2. **Find a job opportunity** you're interested in
3. **Start with Skill 1:** "Analyze this job description"
4. **Follow the workflow** through all 5 skills
5. **Export and submit** your application materials

---

## Need Help?

- **User Guide:** `~/.claude/skills/career/README.md`
- **Migration Guide:** `MIGRATING_TO_SKILLS.md`
- **Test Plan:** `TEST_PLAN.md`
- **Detailed Docs:** Check individual `SKILL.md` files in each skill directory

---

## Key Principles to Remember

1. **Lexicon-Grounded** - All content verified against your history
2. **No Fabrication** - Every statement traceable to source
3. **Socratic Process** - One question at a time, you confirm
4. **Evidence-Based** - Complete source trails in outputs
5. **Modular** - Use skills independently or together

---

**You're ready to start!** 🚀

Begin with: `"Analyze this job description"` and paste a job posting you're interested in.
