# Socratic Career Application Skills System - Design Document

**Date:** 2025-10-31
**Status:** Design Complete - Ready for Implementation
**Replaces/Enhances:** Socratic Steps markdown documentation
**Integrates With:** LLM-based lexicon generator (already implemented)

---

## Executive Summary

Create a comprehensive system of Claude Code skills that guides job seekers through application development using Socratic methodology and personal career lexicons. The system consists of 5 standalone, modular skills that work independently or in sequence, each leveraging LLM analysis rather than Python semantic matching.

**Key Innovation:** All skills (except initial job analysis) reference pre-generated lexicon files, ensuring application materials are grounded in verified experience and authentic voice.

---

## Problem Statement

**Current State:**
- LLM-based lexicon generator successfully creates 4 hierarchical reference guides from career documents
- Socratic career application process exists only as markdown documentation
- No integration between lexicons and application development process
- No tooling to help apply lexicons to specific job opportunities

**User Need:**
When applying for jobs, users need a systematic, Socratic process that:
1. Analyzes job descriptions structurally (not just literally)
2. Compares job requirements against personal lexicons to identify matches and gaps
3. Develops authentic application materials grounded in verified experience
4. Maintains voice consistency with established patterns
5. Never fabricates or exaggerates experience

---

## Solution Architecture

### Two-Component System

**Component 1: Lexicon Generator (Already Built)**
- Python + Claude API (`run_llm_analysis.py`)
- Analyzes career documents once to create 4 lexicon files
- Run when new career documents are added

**Component 2: Socratic Application Skills (To Build)**
- Pure Claude Code skills (no Python for application process)
- Each skill reads lexicons for context and comparison
- Interactive Socratic dialogue through conversation
- Generates job-specific markdown outputs

### Data Flow

```
Your Career Documents
    ↓
[Python LLM Analyzer - Component 1]
    ↓
Lexicon Files (4 hierarchical markdown files)
    ↓
Job Description → [Socratic Skills - Component 2] → Application Materials
```

---

## Design Principles

### 1. Pure LLM Approach
**Why:** Previous semantic similarity (Python) approach was literal, flat, and not actionable. LLM analysis is interpretive, hierarchical, and provides usage guidance.

**Application:** Use Claude's native analytical capabilities for all job analysis and application development. Python only for initial lexicon generation.

### 2. Modular Independence
**Why:** Users need flexibility to use individual skills, not just orchestrated sequences.

**Application:** Each skill is fully standalone and independently useful. No required execution order (except job analysis before comparison-based skills).

### 3. Lexicon-Grounded Authenticity
**Why:** Prevent fabrication and ensure application materials reflect verified experience.

**Application:** Every skill after job analysis reads lexicons. All content must trace to lexicon sources or user-provided documents.

### 4. Comparison-Ready Structure
**Why:** Enable clear gap analysis between job requirements and personal background.

**Application:** Job description analysis outputs structured to match lexicon categories (4-part structure).

### 5. Evidence-Based Verification
**Why:** Build user confidence and prevent rationalization or exaggeration.

**Application:** Every statement in outputs includes source citation. Show before/after comparisons for user confirmation.

### 6. Socratic Methodology
**Why:** Reflective dialogue produces more authentic, thoughtful application materials than direct generation.

**Application:** Ask one question at a time, use structured choices, present incrementally, confirm before proceeding.

---

## System Components

### Lexicon Files (Input - Already Generated)

Located in: `~/lexicons_llm/`

**1. Career Philosophy & Values** (`01_career_philosophy.md`)
- Leadership approach themes
- Core values with evidence
- Problem-solving philosophy
- Hierarchical structure with usage recommendations

**2. Achievement Library** (`02_achievement_library.md`)
- Categorized achievements with multiple framings
- Quantifiable outcomes
- Usage recommendations by role type
- Cross-references between related achievements

**3. Narrative Patterns & Story Structures** (`03_narrative_patterns.md`)
- Cover letter architecture patterns
- Resume bullet formulas
- Thematic storytelling approaches
- Opening/closing strategies

**4. Language Bank & Phrase Library** (`04_language_bank.md`)
- Action verbs by category
- Impact phrases
- Industry-specific language
- Powerful phrase templates

### Skill Files (Output - To Build)

Located in: `~/.claude/skills/career/`

**5 Standalone Skills:**
1. Job Description Analysis
2. Resume Alignment
3. Job Fit Analysis
4. Cover Letter Voice Development
5. Collaborative Writing

---

## Skill Specifications

### Skill 1: Job Description Analysis

**File:** `~/.claude/skills/career/job-description-analysis/SKILL.md`

**Purpose:** Analyze job postings for requirements, culture, and values - output structured to enable comparison with lexicons.

**Invocation Triggers:**
- "Analyze this job description"
- "Help me understand this job posting"
- "What are the key requirements for this role?"

**Lexicon Dependencies:** NONE (standalone analysis)

**Input:** Job posting (paste, upload PDF/Word, or URL)

**Process:**

```markdown
## Phase 0: Setup
- Create job slug from title
- Initialize output directory: ~/career-applications/[job-slug]/

## Phase 1: Document Intake
- Accept job posting in any format
- Extract full text
- Confirm completeness with user

## Phase 2: Structured Analysis (4 Sections)

Generate output matching lexicon structure:

### I. Values & Philosophy Requirements
- Leadership expectations
- Core values signals (explicit + implicit)
- Problem-solving philosophy
→ Structured for comparison with 01_career_philosophy.md

### II. Experience & Achievement Requirements
- Organized by achievement categories
- Quantifiable expectations (budget, team size, scope)
- Project types and scales
→ Structured for comparison with 02_achievement_library.md

### III. Communication & Narrative Requirements
- Resonant narrative types
- Tone & voice requirements
- Cultural communication style
→ Structured for comparison with 03_narrative_patterns.md

### IV. Language & Terminology Requirements
- ATS keywords ranked by importance
- Action verbs they use (frequency analysis)
- Industry-specific terminology
- Synonym mapping
→ Structured for comparison with 04_language_bank.md

## Phase 3: Sophistication Analysis

Beyond literal requirements:

- **Cultural Decoding:** Stated vs. implied culture
- **Reading Omissions:** What's NOT said (team size, salary, etc.)
- **Competitive Positioning:** Who wins this role and why
- **Priority Decoding:** True importance vs. boilerplate
- **Risk Assessment:** Red flags with severity and context
- **Strategic Timing:** Urgency signals, role type (new vs. backfill)

## Phase 4: Output Generation
```

**Output File:** `~/career-applications/[job-slug]/01-job-analysis.md`

**Output Template:**
```markdown
---
job_title: Senior Director, Center for the Arts
company: UCLA
date_analyzed: 2025-10-31
posting_url: https://...
analyst: Claude Code
---

# Job Analysis: Senior Director - UCLA

## Executive Summary
[2-3 sentence overview]

## I. Values & Philosophy Requirements
### Leadership Expectations
[Analysis with quotes from posting]

### Core Values Signals
[Explicit and implicit values]

### Problem-Solving Philosophy
[What approach they value]

## II. Experience & Achievement Requirements
### Capital Projects & Infrastructure
[What they need with specifics]

### Organizational Transformation
[Requirements in this category]

[Continue for all relevant categories...]

## III. Communication & Narrative Requirements
### Resonant Narratives
[What stories will work]

### Tone & Voice Requirements
[Formal? Collaborative? Innovative?]

## IV. Language & Terminology Requirements
### Critical ATS Keywords (Use in resume + cover letter)
- **stakeholder management** (appears 5x, explicit requirement)
  - Context: "manage relationships with campus stakeholders"
  - Recommended frequency: 2-3x in application materials

### Important Keywords (Emphasize in resume)
[Ranked list with context]

### Action Verbs They Use
[Strategic: stewarded, led, oversaw...]

## V. Sophistication Analysis
### Cultural Reality
**Stated:** "Collaborative, innovative environment"
**Implied:** Emphasis on "established processes" suggests balanced innovation
**Interpretation:** Not a disruptive startup culture; measured change within structure

### Reading What's NOT Said
- ❌ No team size mentioned → Possible new team or restructuring
- ❌ No salary range → Need to research or negotiate carefully
- ✅ Reporting structure clear → Stable organizational position

### Competitive Positioning
**Who wins:** Candidates with 10+ years higher ed arts administration, proven capital project success, established network in CA arts community

### Priority Decoding
1. **Capital project experience** (mentioned 7x, specific budget minimums)
2. **Stakeholder management** (5x, multiple contexts)
3. **Fundraising/development** (4x, revenue generation emphasis)

### Risk & Red Flag Assessment
⚠️ MODERATE: "Fast-paced environment" + "manage multiple priorities"
- Context: Also mentions "work-life balance" → likely typical higher ed workload
- Severity: Monitor during interview process

✅ POSITIVE: Strong DEI commitment, clear mission alignment opportunities

## VI. Strategic Recommendations
### For Resume
1. Lead with capital project achievement ($10M+ scale)
2. Emphasize stakeholder management throughout
3. Use their action verbs: "stewarded," "cultivated," "advanced"

### For Cover Letter
1. Open with institutional positioning (their unique assets)
2. Connect your arts-as-social-justice philosophy to their DEI mission
3. Middle: capital project example + stakeholder success story
4. Close: vision for arts in higher education

---
Generated: 2025-10-31 via job-description-analysis skill
```

**Reference Materials:**
- `ats-keyword-framework.md` - Detailed ATS optimization guidance
- `tone-analysis-guide.md` - Culture decoding patterns
- `values-alignment-patterns.md` - Mission/values identification

---

### Skill 2: Resume Alignment

**File:** `~/.claude/skills/career/resume-alignment/SKILL.md`

**Purpose:** Tailor resumes to job descriptions using verified achievements from lexicons - never fabricates.

**Invocation Triggers:**
- "Tailor my resume for this job"
- "Align my resume with this position"
- "Update my resume for [job title]"

**Lexicon Dependencies:**
- ✅ `01-job-analysis.md` (what they need)
- ✅ `lexicons_llm/02_achievement_library.md` (what you have)
- ✅ `lexicons_llm/04_language_bank.md` (how to phrase it)

**Input:**
- Job description or job analysis file
- User's existing resume(s)

**Process:**

```markdown
## Phase 0: Lexicon Loading

**Required files:**
1. Read: ~/career-applications/[job-slug]/01-job-analysis.md
   - If missing: "I need a job analysis first. Should I analyze the job description now?"

2. Read: ~/lexicons_llm/02_achievement_library.md → store as context
   - If missing: "I need your career lexicons. Run: python run_llm_analysis.py"

3. Read: ~/lexicons_llm/04_language_bank.md → store as context

**Verification:** Confirm all files loaded successfully before proceeding

## Phase 1: Job + Lexicon Review

**Actions:**
- Display job analysis summary (from Section II: Achievement Requirements)
- Review achievement library structure
- Identify potentially relevant sections

**User Communication:**
"Based on the job requirements, I found these matching sections in your achievement library:
- Section II.A: Capital Projects (Kirk Douglas Theater, Amphitheater)
- Section III.A: Revenue Generation (Gala growth, earned revenue)
- Section IV: Academic Leadership

Ready to select specific achievements?"

## Phase 2: Match & Select

**For each job requirement:**

Use AskUserQuestion tool to present side-by-side comparisons:

**Example:**
```
JD Requirement: "Project management experience with $5M+ budgets"

Your Achievement Library Matches:

Option A: Kirk Douglas Theater - $12.1M Project
  Variation 1 (Project Management Focus):
  "Stewarded $12.1M adaptive reuse project from conceptual sketch through
  on-time, on-budget delivery, managing all phases including budgeting,
  architect selection, regulatory approvals, construction oversight"

  Source: achievement_library.md:338-342
  Best for: PM roles, operations positions

Option B: Outdoor Amphitheater - 600-seat venue
  Variation 1 (Scope Focus):
  "Conceived and delivered 600-seat outdoor amphitheater from design through
  completion, managing vendor relationships and regulatory compliance"

  Source: achievement_library.md:405-408
  Best for: Smaller-scale project emphasis

Which achievement and variation best fits this requirement?
```

**Process:**
- Present 2-3 matching achievements
- Show variations from lexicon
- Include source citations
- User selects preferred option
- Build achievement selection list

**Language Selection:**

Reference language bank for action verbs:

"They use 'stewarded' 3 times in the posting. Your language bank categorizes this under:
- Section I.A.1: Vision & Planning (Strategic Leadership)
- Usage: Opening statements, executive-level positioning

Should we use 'stewarded' for your capital project bullets?"

## Phase 3: Draft Creation

**Generate resume section by section:**

**Present before/after for each change:**

```
Original (from your 2023 resume):
"Led theater renovation project with team of contractors"

Proposed (tailored for this role):
"Stewarded $12.1M adaptive reuse project from conception through on-time,
on-budget delivery, managing cross-functional team of 50 full- and part-time
staff across design, construction, and operational launch phases"

Source: achievement_library.md:338 (Variation A: Project Management Focus)
Keywords matched: "stewarded" (JD priority), "$12.1M" (exceeds $5M requirement),
"cross-functional team" (collaboration emphasis)

Does this accurately represent your experience? [Yes/No/Adjust]
```

**Rules:**
- Only include after user confirms "Yes"
- If "No" → ask why, adjust, re-present
- If "Adjust" → Socratic questioning to refine
- Continue for all sections

**Track evidence:**
- Every bullet → source citation
- Every verb → language bank reference
- Every number → achievement library verification

## Phase 4: Authenticity Validation

**Final review:**
- Present complete draft
- Ask: "Does this resume feel authentic to how you describe your work?"
- Review evidence trail
- Check: Every statement traceable to source (lexicon or user resume)

**Confirmation checklist:**
- ☐ All achievements verified from lexicon
- ☐ All language from language bank or user's existing materials
- ☐ No fabrication or exaggeration
- ☐ User confirms authenticity
- ☐ ATS keywords from job analysis incorporated

**Final confirmation:** "Ready to save this tailored resume?"
```

**Output File:** `~/career-applications/[job-slug]/02-resume-tailored.md`

**Output Template:**
```markdown
---
job_title: Senior Director, Center for the Arts
company: UCLA
date_created: 2025-10-31
lexicons_referenced:
  - achievement_library.md (Section II.A: Capital Projects, Section III.A: Revenue)
  - language_bank.md (Strategic Leadership verbs)
verified: true
authenticity_confirmed: 2025-10-31
---

# [Your Name]
[Contact Information]

## Professional Summary
[Tailored summary incorporating JD keywords and philosophy]

## Professional Experience

### Associate Producer | Center Theatre Group | 1997-2004

• Stewarded $12.1M adaptive reuse project from conception through on-time, on-budget delivery, managing all phases including budgeting, architect selection, regulatory approvals, construction oversight, and operational launch
  → Source: achievement_library.md:338-342 (Kirk Douglas Theater, Variation A)
  → Keywords: stewarded (JD priority), $12.1M (exceeds requirement), cross-functional

• Negotiated multi-party Disposition and Development Agreement between nonprofit, municipality, and redevelopment agency for public-private partnership adaptive reuse project
  → Source: achievement_library.md:358-362 (Kirk Douglas Theater, Variation C)
  → Keywords: stakeholder management, public-private partnership

[Continue for all positions...]

---

## Evidence Trail
**All content verified and sourced:**

Line 5: "Stewarded $12.1M project..."
  ← achievement_library.md:338 (Kirk Douglas Theater, Variation A)
  ← language_bank.md:192 (Strategic Leadership: Vision & Planning)

Line 8: "Negotiated multi-party agreement..."
  ← achievement_library.md:358 (Kirk Douglas Theater, Variation C)
  ← language_bank.md:215 (Stakeholder Engagement: Collaborative)

[Continue for all bullets...]

**Verification Status:**
✅ No fabricated content
✅ All achievements traced to lexicon
✅ User confirmed authenticity: 2025-10-31
✅ ATS keywords from job analysis incorporated

---
Generated: 2025-10-31 via resume-alignment skill
```

---

### Skill 3: Job Fit Analysis

**File:** `~/.claude/skills/career/job-fit-analysis/SKILL.md`

**Purpose:** Analyze fit between job requirements and background using lexicons - identifies gaps, develops reframing strategies, creates cover letter plan.

**Invocation Triggers:**
- "Analyze my fit for this role"
- "What are my gaps for this position?"
- "Help me plan my cover letter"

**Lexicon Dependencies:**
- ✅ `01-job-analysis.md` (requirements)
- ✅ `lexicons_llm/01_career_philosophy.md` (values)
- ✅ `lexicons_llm/02_achievement_library.md` (experience)

**Input:**
- Job description or job analysis file
- User's resume (optional, for additional context)

**Process:**

```markdown
## Phase 0: Lexicon Loading

**Required files:**
1. Read: ~/career-applications/[job-slug]/01-job-analysis.md
2. Read: ~/lexicons_llm/01_career_philosophy.md → store as context
3. Read: ~/lexicons_llm/02_achievement_library.md → store as context

**Important:** Trust the job analysis - don't re-parse requirements

## Phase 1: Load & Review

**Actions:**
- Display job analysis summary
- Review relevant lexicon sections
- Confirm understanding

**User Communication:**
"I've loaded:
- Job analysis for Senior Director role at UCLA
- Your career philosophy (3 leadership approaches, 5 core values)
- Your achievement library (4 major categories, 15 key achievements)

Ready to analyze your fit and identify opportunities for strategic positioning."

## Phase 2: Gap Analysis (Direct Comparison)

**For each requirement category from job analysis:**

**Example Output:**
```
## Fit Analysis: Section II - Experience & Achievement Requirements

### Capital Projects & Infrastructure
JD Requirement: "$10M+ budget experience, adaptive reuse preferred"

Your Achievement Library:
✅ STRONG MATCH: Kirk Douglas Theater
   - $12.1M budget (exceeds requirement)
   - Adaptive reuse project (exact match)
   - 4 variations available for different emphases
   - Source: achievement_library.md:320-430

✅ STRONG MATCH: Outdoor Amphitheater
   - 600-seat venue, ground-up construction
   - Demonstrates range (new build + adaptive reuse)
   - Source: achievement_library.md:405-450

Assessment: COMPETITIVE STRENGTH - exceeds requirement

---

### Team Leadership
JD Requirement: "Experience managing teams of 25+ in complex environments"

Your Achievement Library:
✅ STRONG MATCH: Kirk Douglas Theater
   - Managed 50 full- and part-time staff
   - Cross-functional team complexity
   - Source: achievement_library.md:371

⚠️  PARTIAL MATCH: Academic Advising Crisis
   - Leadership demonstrated, but not direct management
   - Team coordination vs. formal reporting structure
   - Source: achievement_library.md:890-920

Assessment: STRONG - direct evidence available

---

### Change Management Certification
JD Requirement: "Certified change management professional preferred"

Your Achievement Library:
❌ GAP: No certification mentioned

⚠️  REFRAMING OPPORTUNITY:
   - Practical experience: Free-to-Earned Revenue Model transformation
   - Organizational change: 200+ employees affected
   - Evidence: achievement_library.md:520-560

Reframing Strategy Needed: Emphasize practical expertise, frame cert as growth opportunity

Assessment: ADDRESSABLE GAP - strong practical foundation

---

### Values Alignment
JD Requirement: "Commitment to equity, diversity, inclusion, access, and belonging"

Your Career Philosophy:
✅ STRONG MATCH: Core Value - Arts as Social Justice
   - Direct alignment with DEI emphasis
   - Evidence from philosophy lexicon
   - Source: career_philosophy.md:215-240

✅ STRONG MATCH: Leadership Approach - Equity-Centered Practice
   - Structural commitment, not just values statement
   - Source: career_philosophy.md:125-160

Assessment: AUTHENTIC ALIGNMENT - this is a strength to emphasize
```

**Summary Matrix:**
- ✅ Direct matches: [count]
- ⚠️  Partial matches needing reframing: [count]
- ❌ Missing requirements: [count]
- Ranked by job priority (from job analysis)

## Phase 3: Reframing Strategy Development

**For each gap or partial match:**

Use AskUserQuestion tool:

```
Gap Identified: "Change management certification preferred"

Your Background: Extensive practical change management experience
- Free-to-Earned Revenue Model (organizational transformation)
- Data Infrastructure Implementation (systems change)
- Strategic Planning Leadership (cultural change)

Reframing Options:

A) Emphasize Practical Expertise
"While not formally certified in change management, I have led three major
organizational transformations affecting 200+ employees, applying change
management principles including stakeholder analysis, communication planning,
and resistance mitigation"

Best for: When practical experience is extensive and certification is "preferred" not "required"

B) Frame as Growth Opportunity
"My practical change management experience positions me to pursue formal
certification, which would formalize the expertise gained through [specific examples]"

Best for: When showing commitment to professional development

C) Highlight Transferable Framework
"Applied evidence-based change management frameworks in [specific transformation],
including Kotter's 8-step model for the revenue transition and adaptive leadership
principles for the data infrastructure implementation"

Best for: When you've used recognized frameworks even without formal training

Which approach feels most authentic and strategic?
```

**Build Reframing List:**
- User confirms each reframing strategy
- Document chosen approach
- Link to supporting achievements from lexicon
- Prepare for cover letter integration

## Phase 4: Cover Letter Plan Development

**Based on gaps + reframing + strengths:**

**Structure:**
```
## Cover Letter Strategic Plan

### Opening Strategy (Values Alignment)
**Recommendation:** Institutional Positioning pattern
**Why:** Job emphasizes UCLA's unique assets in arts + higher ed

**From your narrative patterns:**
- Pattern: "[Institution] is uniquely positioned by..."
- Source: narrative_patterns.md:130-145

**Application to this role:**
"UCLA's School of the Arts and Architecture is uniquely positioned by its intersection
of artistic excellence, research innovation, and public mission to advance arts as
a tool for social transformation—a vision that aligns precisely with my 15-year
commitment to arts-as-social-justice practice."

**Philosophy connection:**
Links to career_philosophy.md:215 (Arts as Social Justice value)

---

### Middle Development (Achievements + Reframing)

**Paragraph 2: Capital Project Strength**
- Achievement: Kirk Douglas Theater (variation C: stakeholder focus)
- Connects to: Their emphasis on "collaborative leadership"
- Evidence: achievement_library.md:358-370

**Paragraph 3: Transformation Experience + Reframe**
- Achievement: Free-to-Earned Revenue Model
- Addresses gap: Change management (reframing strategy A)
- Evidence: achievement_library.md:520-560

**Paragraph 4: Values-Driven Leadership**
- Philosophy: Equity-Centered Practice
- Connects to: Their DEIAB commitment
- Evidence: career_philosophy.md:125-160

---

### Closing Strategy
**Recommendation:** Values Reaffirmation + Vision
**Pattern:** Forward-looking invitation
**Source:** narrative_patterns.md:155-165

---

### Tone Profile
**Job requirement:** Collaborative-innovative, mission-driven
**Your natural voice:** Warm, reflective, authoritative (from past letters)
**Recommended:** Balanced warmth + vision, emphasize collaboration

**Language guidance:**
- Use "listening-first leadership" phrasing (philosophy.md:85)
- Mirror their verbs: "stewarded," "cultivated," "advanced"
- Avoid: overly academic jargon, maintain accessibility
```
```

**Output File:** `~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md`

**Output Template:**
```markdown
---
job_title: Senior Director, Center for the Arts
company: UCLA
date_created: 2025-10-31
lexicons_referenced:
  - 01-job-analysis.md
  - 01_career_philosophy.md (Section I.C, Section II.A)
  - 02_achievement_library.md (Section II.A, Section II.B)
---

# Job Fit Analysis & Cover Letter Plan
## Senior Director, Center for the Arts - UCLA

## I. Overall Fit Assessment

**Competitive Position:** STRONG CANDIDATE
- Direct matches: 8 of 10 key requirements
- Partial matches: 2 (with reframing strategies)
- Missing requirements: 0 critical, 1 preferred (certification)
- Values alignment: EXCEPTIONAL (authentic overlap)

**Recommended Application Strategy:**
Lead with capital project + stakeholder strength, emphasize values alignment,
address certification gap proactively through reframing

---

## II. Detailed Gap Analysis

[Full analysis from Phase 2, organized by requirement category]

---

## III. Reframing Strategies

[Documented strategies from Phase 3 with user-confirmed approaches]

---

## IV. Cover Letter Strategic Plan

[Complete plan from Phase 4 with narrative structure]

---

## V. Evidence & Source Map

**All recommendations linked to lexicon sources:**

Opening strategy ← narrative_patterns.md:130
Capital project emphasis ← achievement_library.md:358
Values alignment ← career_philosophy.md:215
Reframing approach ← achievement_library.md:520 + user confirmation

---
Generated: 2025-10-31 via job-fit-analysis skill
```

---

### Skill 4: Cover Letter Voice Development

**File:** `~/.claude/skills/career/cover-letter-voice/SKILL.md`

**Purpose:** Develop authentic cover letter narrative using philosophy, patterns, and job's cultural requirements.

**Invocation Triggers:**
- "Develop my cover letter narrative"
- "Help me find my voice for this letter"
- "What story should I tell?"

**Lexicon Dependencies:**
- ✅ `01-job-analysis.md` (their values/tone)
- ✅ `lexicons_llm/01_career_philosophy.md` (your values)
- ✅ `lexicons_llm/03_narrative_patterns.md` (your storytelling)
- ✅ `lexicons_llm/04_language_bank.md` (your voice)

**Input:**
- Job description or job analysis file
- Previous cover letters (optional, for tone reference)
- Cover letter plan (optional, from job-fit-analysis skill)

**Process:**

```markdown
## Phase 0: Lexicon Loading

**Required files:**
1. Read: ~/career-applications/[job-slug]/01-job-analysis.md
2. Read: ~/lexicons_llm/01_career_philosophy.md → store as context
3. Read: ~/lexicons_llm/03_narrative_patterns.md → store as context
4. Read: ~/lexicons_llm/04_language_bank.md → store as context

**Optional files:**
5. Read: ~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md (if exists)
6. Accept: User-provided past cover letters for tone analysis

## Phase 1: Context Review

**Load and summarize:**
- Job analysis: Section I (Values) and Section III (Communication requirements)
- Cover letter plan (if available)
- Job's cultural tone requirements

**Communication:**
```
I've loaded:
- Job analysis showing collaborative-innovative culture, mission-driven emphasis
- Your career philosophy (3 leadership approaches, 5 core values)
- Your narrative patterns (5 opening strategies, 4 evidence patterns)
- Your language bank (action verbs, power phrases)

[If plan exists]: I also have your cover letter strategic plan from the gap analysis.
[If past letters provided]: And 3 previous cover letters for tone reference.

Ready to develop your narrative framework.
```

## Phase 2: Content & Pattern Analysis

**Analyze multiple sources:**

**A. Past Cover Letters (if provided)**
```
From your 2023 CSUF letter:
- Opening: Institutional positioning ("CSUF is uniquely positioned...")
- Tone: Warm, collaborative, student-centered
- Evidence pattern: Challenge → Action → Result
- Length: 3 paragraphs, ~450 words

From your 2024 UCLA letter:
- Opening: Personal connection to mission
- Tone: Authoritative, visionary, strategic
- Evidence pattern: Context → Insight → Application
- Length: 4 paragraphs, ~550 words

Pattern observation: You shift tone based on role level
(collaborative for director, authoritative for VP)
```

**B. Narrative Patterns from Lexicon**
```
From narrative_patterns.md, your established patterns:

Opening Strategies:
1. Institutional Positioning (used in 60% of letters)
   - Template: "[Institution] is uniquely positioned by..."
   - When: Academic, mission-driven organizations
   - Source: narrative_patterns.md:130

2. Personal Connection (used in 30% of letters)
   - Template: "My commitment to [value] was shaped by..."
   - When: Values-driven roles, mission emphasis
   - Source: narrative_patterns.md:145

Evidence Patterns:
1. Challenge → Action → Result (primary pattern)
   - Source: narrative_patterns.md:180-195
```

**C. Job Requirements**
```
From job analysis Section III:

Communication & Narrative Requirements:
- Tone: Collaborative-innovative
- Values emphasis: DEI, student-centered, mission-driven
- Cultural fit: Balanced (not startup-disruptive, not traditional-rigid)

Recommendation: Your "institutional positioning" opening + "challenge-action-result"
evidence pattern align well with their culture.
```

## Phase 3: Narrative Thread Exploration

**Socratic questioning to identify core story:**

Use AskUserQuestion:
```
Based on your philosophy and this role, which narrative thread feels most authentic?

A) Arts Leadership as Social Transformation
Your philosophy emphasizes "Arts as Social Justice" (philosophy.md:215)
Job emphasizes: "Advancing arts for social impact"
Story arc: Your journey from believing arts = access to leading institutions that embody this

B) Listening-First Leadership in Complex Environments
Your philosophy: "Listening-First Leadership" (philosophy.md:85)
Job context: Large organization, diverse stakeholders, collaborative culture
Story arc: How your leadership approach builds consensus and drives change

C) Building Infrastructure for Creative Excellence
Your achievements: Capital projects, systems building, resource development
Job requirements: Facility stewardship, program development, financial management
Story arc: How you create conditions for artistic excellence through strategic infrastructure

Which thread resonates most for this opportunity?
```

**User selects narrative thread**

**Explore depth:**
```
You selected: Arts Leadership as Social Transformation

Let's develop this thread:

From your philosophy lexicon (philosophy.md:215-240):
"Arts as a tool for social justice, community transformation, and equitable access"

Which experience best illustrates this philosophy in action?

A) Kirk Douglas Theater - Public-private partnership for community access
B) Free-to-Earned Revenue Model - Making arts sustainable and accessible
C) Academic Leadership - Creating equitable pathways for diverse students

[User selects]

How do you want to position the tension/opportunity this role represents?
- Continuing your social justice work at larger scale?
- Bringing infrastructure expertise to mission-driven context?
- Bridging artistic excellence with community impact?
```

**Build narrative map:**
- Core thread identified
- Key experiences selected from achievement library
- Philosophy connections documented
- Tension/opportunity framed

## Phase 4: Tone & Structure Framing

**Match tone requirements:**

```
## Tone Profile Development

Job Requirement (from analysis):
- Collaborative-innovative
- Mission-driven
- Professional but not overly formal

Your Natural Voice (from past letters + lexicon):
- Warm and reflective (CSUF letter)
- Strategic and visionary (UCLA VP letter)
- Value narrative patterns: Institutional positioning, challenge-action-result

Recommended Synthesis:
- Formality level: Professional-collaborative (not academic, not casual)
- Sentence structure: Mix of longer vision statements with concrete examples
- Vocabulary: Mission-oriented language, avoid jargon
- Emotional register: Committed optimism (not neutral, not effusive)

Example opening sentence (tone demonstration):
"UCLA's School of the Arts and Architecture is uniquely positioned by its
intersection of artistic excellence, research innovation, and public mission
to advance arts as a tool for social transformation—a vision that aligns
precisely with my 15-year commitment to arts-as-social-justice practice."

Tone notes:
- "Uniquely positioned" = institutional positioning pattern
- "intersection of" = complexity acknowledgment (collaborative tone)
- "aligns precisely" = confident but not presumptuous
- "15-year commitment" = credibility through specificity

Does this tone feel authentic to how you want to present?
```

**Structure recommendation:**

```
## Narrative Structure

Based on selected thread + job requirements + your patterns:

**Opening (1 paragraph, ~100 words)**
Pattern: Institutional Positioning
Content: UCLA's unique position + your aligned philosophy
Source: narrative_patterns.md:130

**Development (2-3 paragraphs, ~300 words)**

Paragraph 2: Capital project achievement
- Kirk Douglas Theater (stakeholder variation)
- Demonstrates: Leadership, complexity management, public mission
- Pattern: Challenge → Action → Result
- Source: achievement_library.md:358

Paragraph 3: Transformation + values
- Free-to-Earned Revenue Model
- Demonstrates: Change leadership, mission sustainability
- Connects to: Their financial stewardship requirement
- Source: achievement_library.md:520

[Optional Paragraph 4: If gap to address]
- Reframing strategy from gap analysis
- Frames certification gap as growth opportunity

**Closing (1 paragraph, ~80 words)**
Pattern: Values Reaffirmation + Forward-Looking
Content: Enthusiasm for bringing infrastructure expertise to mission-driven context
Source: narrative_patterns.md:160

Total length: 480-580 words (standard for this role level)
```

## Phase 5: Voice Consistency Check

**Review against language bank:**

```
## Language Consistency Review

Checking proposed narrative against your established voice:

Action Verbs (from language_bank.md):
✅ "Stewarded" (Strategic Leadership category) - appears in your lexicon
✅ "Cultivated" (Stakeholder Engagement) - appears in your lexicon
❌ "Spearheaded" - NOT in your lexicon, sounds unlike your voice
   Replacement: "Led" or "Stewarded" instead

Power Phrases (from language_bank.md):
✅ "I believe [role] should be..." (Leadership Philosophy template)
✅ "uniquely positioned by..." (Institutional Positioning template)
✅ "Our moment demands..." (Challenge Framing template)

Industry Language:
✅ "Adaptive reuse" (Architecture/facilities term from your experience)
✅ "Stakeholder management" (Standard in your sector)
✅ "Evidence-based" (Your preferred framing from philosophy.md)

Consistency: STRONG - narrative uses your established language patterns
```

## Phase 6: Authenticity Review

**Final Socratic check:**

Ask open-ended questions:
- "Does this narrative framework sound like your real voice?"
- "Are there any elements that feel performative or unlike you?"
- "Which part of this story excites you most to tell?"
- "Is there anything missing that feels important?"

**Compare to philosophy:**
```
Authenticity Alignment Check:

Your Core Values (philosophy.md):
1. Arts as Social Justice ✅ Central to narrative
2. Student-Centered Education ✅ Implied in access emphasis
3. Institutional Stewardship ✅ Capital project examples

Your Leadership Approach (philosophy.md):
1. Listening-First Leadership ⚠️  Not explicit in current framework
   - Add?: Could strengthen collaborative tone
2. Collaborative Decision-Making ✅ Evident in stakeholder examples
3. Equity-Centered Practice ✅ Central to social justice thread

Recommendation: Consider adding brief mention of listening-first approach
in paragraph about stakeholder management at Kirk Douglas?
```

**User confirms framework feels authentic**
```

**Output File:** `~/career-applications/[job-slug]/04-cover-letter-framework.md`

**Output Template:**
```markdown
---
job_title: Senior Director, Center for the Arts
company: UCLA
date_created: 2025-10-31
lexicons_referenced:
  - 01-job-analysis.md (Sections I & III)
  - 01_career_philosophy.md (Arts as Social Justice, Listening-First Leadership)
  - 03_narrative_patterns.md (Institutional Positioning, Challenge-Action-Result)
  - 04_language_bank.md (Strategic Leadership verbs, Power phrases)
narrative_thread: Arts Leadership as Social Transformation
authenticity_confirmed: 2025-10-31
---

# Cover Letter Narrative Framework
## Senior Director, Center for the Arts - UCLA

## I. Tone Profile

**Recommended Voice:**
- Professional-collaborative (not academic, not casual)
- Committed optimism
- Strategic vision grounded in practical examples
- Warm but authoritative

**Sentence Structure:**
Mix of:
- Vision statements (longer, 25-30 words)
- Concrete examples (medium, 15-20 words)
- Impact summaries (shorter, 10-12 words)

**Vocabulary Guidelines:**
✅ Use: stewarded, cultivated, advanced, listening-first, stakeholder, evidence-based
❌ Avoid: spearheaded, synergy, leverage (not in your lexicon)

## II. Narrative Structure

### Opening Paragraph (~100 words)
**Pattern:** Institutional Positioning
**Source:** narrative_patterns.md:130

**Draft:**
"UCLA's School of the Arts and Architecture is uniquely positioned by its intersection of artistic excellence, research innovation, and public mission to advance arts as a tool for social transformation—a vision that aligns precisely with my 15-year commitment to arts-as-social-justice practice. Throughout my career leading arts organizations and academic programs, I have stewarded capital projects, built sustainable revenue models, and cultivated stakeholder partnerships that advance equitable access to transformative artistic experiences."

**Philosophy Connection:**
Links to career_philosophy.md:215 (Arts as Social Justice core value)

**Evidence:**
- "15-year commitment" = credibility
- "stewarded capital projects" = preview of evidence
- "equitable access" = values alignment with their DEI emphasis

---

### Development Paragraph 2: Capital Project Achievement (~140 words)
**Pattern:** Challenge → Action → Result
**Achievement:** Kirk Douglas Theater (Variation C: Stakeholder focus)
**Source:** achievement_library.md:358-370

**Draft Guidance:**
Begin with context/challenge:
"When the City of Culver City sought a nonprofit partner to transform a historic building into a professional theater..."

Action (your role):
"I negotiated a multi-party Disposition and Development Agreement... cultivated relationships across municipal, artistic, and community stakeholders... applied listening-first leadership approach to build consensus..."

Result:
"...resulting in the on-time, on-budget delivery of a $12.1M, 317-seat venue that has served the community for 20 years..."

**Why This Achievement:**
- Demonstrates: Stakeholder management (job priority)
- Scale: Exceeds their requirements
- Approach: Listening-first leadership (your philosophy + their culture)

**Language Notes:**
- "Negotiated" ← language_bank.md:215 (Stakeholder Engagement)
- "Listening-first" ← philosophy.md:85 (your terminology, shows authenticity)
- "$12.1M" ← achievement_library.md:360 (specific, credible)

---

### Development Paragraph 3: Transformation + Values (~140 words)
**Pattern:** Context → Insight → Application
**Achievement:** Free-to-Earned Revenue Model
**Source:** achievement_library.md:520-560

**Draft Guidance:**
Context:
"Understanding that sustainable mission requires sustainable resources..."

Insight:
"I recognized that our free-admission model, while expanding access, was unsustainable without diversified revenue..."

Application (action):
"I led the strategic transition to an earned-revenue model, growing ticket sales 20% year-over-year while maintaining commitment to accessibility through expanded scholarship programs..."

Result:
"This evidence-based approach demonstrated that financial sustainability and equitable access are not in tension—they are mutually reinforcing when grounded in clear mission and inclusive practice."

**Why This Achievement:**
- Demonstrates: Strategic thinking, change management
- Values alignment: Access + sustainability (their mission)
- Addresses: Financial stewardship requirement

**Philosophy Connection:**
Links to career_philosophy.md:280 (Sustainable Solutions)

---

### Closing Paragraph (~80 words)
**Pattern:** Values Reaffirmation + Forward-Looking Invitation
**Source:** narrative_patterns.md:160

**Draft:**
"The Senior Director role offers an opportunity to bring my infrastructure expertise, stakeholder engagement approach, and commitment to arts-as-social-justice to an institution uniquely positioned to model how artistic excellence and community impact can advance together. I would welcome the opportunity to discuss how my experience aligns with UCLA's vision for the School of the Arts and Architecture."

**Tone Notes:**
- "offers an opportunity" = enthusiastic but not presumptuous
- "uniquely positioned" = callback to opening (structural cohesion)
- "discuss how" = invitation, collaborative tone

---

## III. Evidence & Source Map

**All content linked to lexicon sources:**

Opening: Institutional positioning pattern ← narrative_patterns.md:130
Philosophy: Arts as social justice ← career_philosophy.md:215
Achievement 1: Kirk Douglas Theater ← achievement_library.md:358
Leadership approach: Listening-first ← career_philosophy.md:85
Achievement 2: Revenue model transformation ← achievement_library.md:520
Action verb: "stewarded" ← language_bank.md:192
Action verb: "cultivated" ← language_bank.md:215
Closing pattern: Forward-looking invitation ← narrative_patterns.md:160

---

## IV. Authenticity Confirmation

☐ Narrative thread resonates with your actual motivations
☐ Examples feel accurate (not exaggerated)
☐ Language sounds like your voice (per language bank)
☐ Values alignment is genuine (per philosophy lexicon)
☐ Tone feels comfortable and authentic

**User Confirmation:** ✅ Confirmed authentic - 2025-10-31

---

## V. Next Steps

**Options:**

A) Begin collaborative drafting now
   - Move to collaborative-writing skill for iterative development

B) Draft independently and return for review
   - Use this framework as guide
   - Return for voice/consistency check

C) Adjust framework first
   - Revise narrative thread, tone, or structure
   - Re-confirm before drafting

---
Generated: 2025-10-31 via cover-letter-voice skill
```

---

### Skill 5: Collaborative Writing

**File:** `~/.claude/skills/career/collaborative-writing/SKILL.md`

**Purpose:** Co-create any professional writing through Socratic dialogue using established voice patterns.

**Invocation Triggers:**
- "Help me write [message/statement/letter]"
- "Co-write this with me"
- "Draft [communication type]"

**Lexicon Dependencies (Optional):**
- ✅ `lexicons_llm/03_narrative_patterns.md` (for structure)
- ✅ `lexicons_llm/04_language_bank.md` (for voice consistency)
- ⚠️ `01-job-analysis.md` (if job-related writing)

**Input:**
- Writing purpose and audience
- Any existing drafts or relevant materials
- Context (why this communication, what outcome desired)

**Process:**

*(This skill uses the existing Socratic-Collaborative-Writing process with lexicon enhancement)*

```markdown
## Phase 0: Lexicon Loading (Conditional)

**If job-related writing:**
- Read: ~/lexicons_llm/03_narrative_patterns.md
- Read: ~/lexicons_llm/04_language_bank.md
- Optional: ~/career-applications/[job-slug]/01-job-analysis.md

**If general professional writing:**
- Read: ~/lexicons_llm/03_narrative_patterns.md (for your patterns)
- Read: ~/lexicons_llm/04_language_bank.md (for voice consistency)

## Phase 1: Discovery Dialogue
[Existing process from Socratic-Collaborative-Writing-Skill.md]

Ask one question at a time to uncover:
- Strategic intent and timing
- Target audience and desired response
- Emotional and tonal objectives
- Constraints

**Output:** Intent Statement

## Phase 2: Message Architecture
[Existing process]

Identify core ideas and relationships:
- Essential ideas or calls to action
- Supporting details
- Narrative/emotional arc

**Output:** Message Map

## Phase 3: Framing and Voice Calibration
[Existing process + Lexicon Enhancement]

**Enhanced with lexicon reference:**
```
From your narrative patterns (narrative_patterns.md):
- You typically use [pattern type] for [context]
- Your natural rhythm: [sentence structure observation]

From your language bank:
- Preferred action verbs for this context: [list]
- Power phrases you've used successfully: [list]

Recommended voice for this piece:
[Synthesis of audience needs + your authentic patterns]
```

**Output:** Voice Profile

## Phase 4: Collaborative Drafting
[Existing process + Voice Consistency Checks]

Draft 50-150 word segments
After each segment, check against language bank:
- Are you using verbs from your lexicon?
- Does phrasing match your established patterns?

**Output:** Refined Draft

## Phase 5: Alignment and Adaptation
[Existing process]

Validate resonance and adaptability

**Output:** Finalized Message
```

**Output:** Generated collaboratively, saved to user-specified location

---

## File Organization & Structure

### Installation Structure

```
~/.claude/skills/career/
├── job-description-analysis/
│   ├── SKILL.md (main skill)
│   ├── ats-keyword-framework.md (reference)
│   ├── tone-analysis-guide.md (reference)
│   └── values-alignment-patterns.md (reference)
│
├── resume-alignment/
│   └── SKILL.md
│
├── job-fit-analysis/
│   └── SKILL.md
│
├── cover-letter-voice/
│   └── SKILL.md
│
└── collaborative-writing/
    └── SKILL.md
```

### Working Directory Structure

```
~/career-applications/
└── [date]-[job-slug]/
    ├── 01-job-analysis.md
    ├── 02-resume-tailored.md
    ├── 03-gap-analysis-and-cover-letter-plan.md
    ├── 04-cover-letter-framework.md
    ├── 05-cover-letter-draft.md (optional, from collaborative-writing)
    └── source-materials/
        ├── original-job-posting.pdf
        ├── original-resume-2024.pdf
        └── notes.md
```

### Lexicon Files (Input)

```
~/lexicons_llm/ (or user-configured path)
├── 01_career_philosophy.md
├── 02_achievement_library.md
├── 03_narrative_patterns.md
└── 04_language_bank.md
```

---

## Technical Implementation Details

### Configuration Management

**Each skill includes configuration section:**

```markdown
## Configuration

**Default paths (user can override):**
- LEXICONS_DIR: ~/lexicons_llm/
- APPLICATIONS_DIR: ~/career-applications/
- ARCHIVE_DIR: ~/career-applications/archive/

**Skill-specific settings:**
- MAX_OUTPUT_LENGTH: 5000 words
- REQUIRE_USER_CONFIRMATION: true
- AUTO_SAVE_INTERVAL: per-phase
```

### Error Handling Patterns

**Missing Files:**
```markdown
## Startup Checks

1. Check for required lexicon files
   - If missing: "Lexicon files not found at ~/lexicons_llm/.
                  Run: python run_llm_analysis.py to generate them first."

2. Check for job analysis (skills 2-4 only)
   - If missing: "No job analysis found. Should I analyze the job description first?"
   - If user says yes: Invoke job-description-analysis skill
   - If user says no: "I need a job analysis to proceed. Please run job-description-analysis first."

3. Check write permissions for output directory
   - If no permission: "Cannot write to ~/career-applications/. Check permissions or specify different output directory."
```

**Invalid Input:**
```markdown
## Input Validation

- Job posting too short (<100 words): "This seems incomplete. Is this the full posting?"
- Multiple job postings provided: "I see multiple job descriptions. Which one should I analyze?"
- Ambiguous user responses: Use Socratic clarification questions, never assume
```

**Partial Processing:**
```markdown
## Resumption Support

Each skill saves progress after each phase:
- Save to: ~/career-applications/[job-slug]/.skill-state.json
- Contents: {skill_name, phase_completed, user_selections, timestamp}

On skill re-invocation:
- Check for .skill-state.json
- Ask: "I see you started this analysis on [date] and completed Phase 2. Continue from Phase 3?"
```

### Socratic Process Mechanics

**Question Timing:**
```markdown
## When to Use AskUserQuestion Tool

**Use structured questions for:**
- Selecting between 2-4 concrete options (achievements, variations, approaches)
- Confirming interpretations with preset choices
- Priority ranking when multiple valid options exist

**Example:**
```
Which achievement best demonstrates stakeholder management?

A) Kirk Douglas Theater - Multi-party negotiation ($12.1M)
B) Outdoor Amphitheater - Community partnership (600-seat)
C) Gala Revenue Growth - Donor cultivation (50% increase)
```

**Use open-ended questions for:**
- Exploring motivations and values
- Gathering context not available in files
- Authenticity checks ("Does this feel like your voice?")
- Creative/narrative development

**Never ask when:**
- Information is available in lexicons or provided files
- Priority is clear from job analysis
- Standard practice applies
```

**Confirmation Patterns:**
```markdown
## User Confirmation Requirements

**Require explicit "yes" before:**
- Including any content in final outputs
- Moving to next major phase
- Saving files to disk
- Making claims about user's experience

**Present before/after for:**
- Every resume bullet (original vs. proposed)
- Every reframing strategy (gap vs. reframe)
- Every major tone shift from past writing

**Format:**
```
Original: [user's existing content or "none"]
Proposed: [new content]
Source: [lexicon citation or user document]
Reasoning: [why this change]

Accurate? [Yes/No/Adjust]
```
```

### Output File Metadata

**Standard header for all generated files:**

```markdown
---
# Job Information
job_title: [from analysis or user input]
company: [from analysis or user input]
job_url: [if available]
posting_date: [if available]

# Generation Metadata
skill_used: [skill name]
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD (if updated)

# Lexicon References
lexicons_referenced:
  - file: 01_career_philosophy.md
    sections: [I.A, II.C]
  - file: 02_achievement_library.md
    sections: [II.A, III.B]

# Verification
verified: true/false
authenticity_confirmed: YYYY-MM-DD (user confirmed authentic)
fabrication_check: passed (all content traced to source)

# Optional
based_on_prior_analysis: [file reference if building on previous skill output]
user_notes: [any user-added context]
---
```

### Evidence Trail Format

**At end of each generated file:**

```markdown
---

## Evidence & Source Trail

**All content verified and sourced:**

### Resume Line 5
**Content:** "Stewarded $12.1M adaptive reuse project..."
**Sources:**
- Achievement: achievement_library.md:338-342 (Kirk Douglas Theater, Variation A)
- Language: language_bank.md:192 (Strategic Leadership: Vision & Planning)
- Keywords matched: "stewarded" (JD priority), "$12.1M" (exceeds requirement)
**User confirmation:** 2025-10-31

### Cover Letter Paragraph 2
**Content:** Opening with institutional positioning
**Sources:**
- Pattern: narrative_patterns.md:130 (Institutional Positioning)
- Philosophy: career_philosophy.md:215 (Arts as Social Justice)
- Job alignment: 01-job-analysis.md Section I.A (Values Requirements)
**User confirmation:** 2025-10-31

[Continue for all major content elements...]

---

## Verification Checklist

☑ No fabricated content (all achievements from lexicon or user docs)
☑ No exaggerated claims (all numbers/scales verified)
☑ Voice consistency maintained (language bank references)
☑ User confirmed authenticity (date: 2025-10-31)
☑ All sources cited and traceable
☑ ATS keywords from job analysis incorporated
☑ Tone matches both job culture and user's natural voice

---
Generated: 2025-10-31 via [skill-name] skill
Version: 1.0
```

---

## Success Criteria

### Job Description Analysis Skill
✅ All 4 lexicon-aligned sections populated with specific content
✅ Requirements ranked by true importance (not just listed order)
✅ Cultural decoding goes beyond literal reading (interprets implications)
✅ Red flags identified with severity assessment and context
✅ Output structure enables direct comparison with lexicons
✅ User understands job deeply enough to make informed application decision

### Resume Alignment Skill
✅ Every achievement traces to lexicon (source citations included)
✅ Every language choice references language bank or user's existing materials
✅ ATS keywords from job analysis incorporated appropriately
✅ User confirms: "This resume is authentic to my experience"
✅ No fabricated content (verified through evidence trail)
✅ Resume demonstrates competitive fit for the role

### Job Fit Analysis Skill
✅ Gaps identified and ranked by job priority (not random order)
✅ Reframing strategies grounded in actual lexicon achievements
✅ Cover letter plan has clear narrative direction and structure
✅ User feels confident about positioning (not anxious about gaps)
✅ All recommendations linked to specific lexicon sources
✅ Authentic alignment opportunities identified (not manufactured)

### Cover Letter Voice Development Skill
✅ Narrative framework matches job culture AND user's authentic voice
✅ Examples drawn from achievement library with proper variation selection
✅ Tone profile aligns with job analysis recommendations
✅ User confirms: "This sounds like me"
✅ Language consistency with language bank maintained
✅ Framework provides clear structure for drafting

### Collaborative Writing Skill
✅ Voice consistency with lexicon patterns throughout
✅ Socratic process deepens user's thinking about message
✅ Final draft feels authentic to user's voice
✅ Strategic intent clearly achieved in output
✅ User would feel confident sending/publishing the writing

---

## Refactoring Improvements Applied

### 1. Streamlined Phases
**Resume Alignment:** 7 phases → 4 phases
- Merged redundant intake/analysis phases
- Removed optional adaptation phase (out of scope for standalone use)

**Job Fit Analysis:** Removed duplication
- Eliminated re-parsing of job requirements (trusts job analysis output)
- Direct comparison instead of re-extraction

### 2. Explicit Lexicon Integration
**All skills now include:**
- Phase 0: Lexicon Loading with specific file paths
- Clear instructions for what to do if files missing
- Explicit context storage and reference patterns

### 3. Tool Usage Specification
**Before:** Generic "ask questions"
**Now:** Specific tool call patterns:
- Read tool: Exact file paths and when to use
- AskUserQuestion tool: Formatted examples with options
- Write tool: Output templates and file locations

### 4. Verification & Evidence Strengthening
**Added to all skills:**
- Source citation requirements (quote line numbers)
- Before/after comparison presentation
- User confirmation checkpoints
- Evidence trail in all outputs
- "Never fabricate" explicit rules

### 5. Standalone Independence
**Removed:**
- References to orchestration skill
- Assumptions about execution order
- Coupled dependencies

**Added:**
- Graceful handling of missing prior analyses
- Option to invoke prerequisite skills when needed
- Each skill works independently

### 6. Output Standardization
**All skills now output:**
- Consistent file naming: `[sequence]-[purpose].md`
- Standard metadata headers
- Evidence & source trail sections
- Verification checklists
- Version tracking

---

## Implementation Scope

### In Scope - To Build

1. **5 SKILL.md files** with complete Socratic processes
   - job-description-analysis/SKILL.md
   - resume-alignment/SKILL.md
   - job-fit-analysis/SKILL.md
   - cover-letter-voice/SKILL.md
   - collaborative-writing/SKILL.md

2. **3 Reference documents** for job description analysis
   - ats-keyword-framework.md
   - tone-analysis-guide.md
   - values-alignment-patterns.md

3. **This design document**
   - Complete system architecture
   - Detailed skill specifications
   - Implementation guidance

4. **Implementation plan** (next phase)
   - Detailed task breakdown
   - File-by-file creation guide
   - Testing approach

### Out of Scope - Not Building

1. ~~Orchestration skill~~ (optional convenience, not needed for modular approach)
2. ~~Python rewrites~~ (keeping pure LLM approach as validated)
3. ~~Automated testing~~ (manual validation instead)
4. ~~Web interface~~ (Claude Code CLI is the interface)
5. ~~Integration with job boards~~ (manual input is fine)

### Already Complete - Leveraging

1. ✅ LLM-based lexicon generator (`run_llm_analysis.py`)
2. ✅ Lexicon prompt templates (`llm_prompt_templates.py`)
3. ✅ Hierarchical markdown generator (`hierarchical_generator.py`)
4. ✅ Document processor (for career documents)
5. ✅ Socratic process documentation (templates in `Socratic Steps/`)

---

## User Workflows

### Workflow 1: First-Time Job Application

**Prerequisites:** User has run `python run_llm_analysis.py` and has lexicons generated

**Steps:**
1. User: "Analyze this job description" [pastes or uploads posting]
   - Invokes: job-description-analysis skill
   - Output: `~/career-applications/2025-10-31-senior-director-ucla/01-job-analysis.md`

2. User: "Tailor my resume for this role" [uploads current resume]
   - Invokes: resume-alignment skill
   - Reads: job-analysis.md + achievement_library.md + language_bank.md
   - Output: `02-resume-tailored.md`

3. User: "Analyze my fit and plan my cover letter"
   - Invokes: job-fit-analysis skill
   - Reads: job-analysis.md + philosophy.md + achievement_library.md
   - Output: `03-gap-analysis-and-cover-letter-plan.md`

4. User: "Develop my cover letter voice"
   - Invokes: cover-letter-voice skill
   - Reads: job-analysis.md + all lexicons
   - Output: `04-cover-letter-framework.md`

5. User: "Let's draft the cover letter"
   - Invokes: collaborative-writing skill
   - Reads: cover-letter-framework.md + narrative_patterns.md
   - Output: `05-cover-letter-draft.md`

**Result:** Complete application package with verified authenticity

---

### Workflow 2: Quick Resume Update Only

**User has job description and just needs resume tailored**

**Steps:**
1. User: "Analyze this job posting and tailor my resume"
   - First invocation: job-description-analysis skill
   - Automatically offers: "Would you like me to tailor your resume next?"
   - Second invocation: resume-alignment skill
   - Output: Job analysis + tailored resume

**Result:** Focused output without full application development

---

### Workflow 3: Cover Letter Only (Resume Already Submitted)

**User already applied but wants to send a follow-up letter or different position at same org**

**Steps:**
1. User: "I need to write a cover letter for this role. I already have the job analysis."
   - Invokes: cover-letter-voice skill
   - Skill finds existing job-analysis.md
   - Asks: "Should I use your analysis of [job title] from [date]?"
   - Proceeds with voice development

**Result:** Can use skills modularly, not just sequentially

---

### Workflow 4: Updating Lexicons Mid-Application-Season

**User adds new achievements or documents during active job search**

**Steps:**
1. User runs: `python run_llm_analysis.py` (regenerates lexicons with new content)
2. User: "Re-tailor my resume for the UCLA role with my updated achievements"
   - resume-alignment skill reads updated lexicons
   - Finds new achievements available
   - Presents: "Your updated lexicon includes [new achievement]. Want to incorporate this?"

**Result:** Skills always reference current lexicon state

---

## Migration Path from Existing Socratic Steps

### Existing Markdown Documentation
The `Socratic Steps/` directory contains:
- Socratic-Resume-Alignment-and-Tailoring-Skill.md
- Socratic-Job-Fit-Analysis-and-Cover-Letter-Planning-Skill.md
- Socratic-Cover-Letter-Voice-and-Narrative-Development-Skill.md
- Socratic-Collaborative-Writing-Skill.md
- Socratic-Career-Application-Orchestration-Skill.md
- Socratic-Career-Application-Activation-Prompt.md

### Conversion Process
1. Use existing process descriptions as templates
2. Add Phase 0 (Lexicon Loading) to each
3. Add explicit tool usage patterns (Read, AskUserQuestion, Write)
4. Add output templates with metadata
5. Add verification/evidence requirements
6. Remove orchestration dependencies
7. Test with real job descriptions

### Preservation
- Keep original files in `Socratic Steps/` for reference
- New skills in `~/.claude/skills/career/` become active versions
- Update README to point to new skill location

---

## Testing & Validation Approach

### Manual Testing Protocol

**For each skill:**

1. **Test with real job description**
   - Use actual job posting from target sector (higher ed arts admin)
   - Verify output structure matches design
   - Check that all required sections populated

2. **Test lexicon integration**
   - Verify skill reads correct files
   - Check that citations/sources are accurate
   - Confirm matches are legitimate (not hallucinated)

3. **Test Socratic process**
   - Ensure one question at a time
   - Verify AskUserQuestion tool used appropriately
   - Check that skill doesn't skip ahead without confirmation

4. **Test authenticity verification**
   - Confirm no fabricated content
   - Check evidence trail completeness
   - Verify user confirmation points work

5. **Test error handling**
   - Missing lexicons → appropriate error message
   - Missing job analysis → offers to create
   - Invalid input → clarifying questions, not assumptions

### Validation Criteria

**Each skill must:**
- [ ] Read correct lexicon files on startup
- [ ] Generate output matching specified template
- [ ] Include complete evidence trail
- [ ] Use Socratic methodology (one question at a time)
- [ ] Never fabricate content
- [ ] Cite all sources accurately
- [ ] Work independently (no orchestration required)
- [ ] Handle missing files gracefully
- [ ] Save output to correct location
- [ ] Feel authentic and useful to user

### User Acceptance Testing

**Recruit test user (the primary user):**
1. Apply to real job using skills
2. Gather feedback on:
   - Was the process too long/too short?
   - Did outputs feel authentic?
   - Were recommendations useful?
   - Any frustrating moments?
3. Iterate based on feedback

---

## Future Enhancements (Post-MVP)

### Potential Phase 2 Features

1. **Interview Preparation Skill**
   - Reads job analysis + lexicons
   - Predicts likely interview questions
   - Prepares STAR-format responses using achievement library
   - Practice dialogue mode

2. **Application Tracking**
   - Maintain database of applications
   - Track which achievements used where
   - Prevent resume inconsistencies across applications

3. **Networking Message Generator**
   - Craft LinkedIn outreach
   - Informational interview requests
   - Thank-you notes
   - Uses collaborative-writing + language bank

4. **Salary Negotiation Prep**
   - Research compensation ranges
   - Build value case using achievements
   - Practice negotiation dialogue

5. **Multiple Lexicon Profiles**
   - Academic profile (teaching/research emphasis)
   - Administrative profile (operations/management emphasis)
   - Creative profile (artistic/curatorial emphasis)
   - Switch between based on role type

6. **Annual Review Support**
   - Use achievement library for self-evaluations
   - Track accomplishments throughout year
   - Generate promotion materials

### Technical Enhancements

1. **Web interface** for non-Claude Code users
2. **Export to Word/PDF** with formatting
3. **Version control** for application iterations
4. **Comparison view** for multiple job analyses
5. **Analytics** on keyword usage, achievement selection patterns

---

## Maintenance & Updates

### Lexicon Refresh Cadence

**When to regenerate lexicons:**
- After completing major projects (update achievement library)
- After writing strong cover letters (update narrative patterns)
- Annual review (comprehensive update with year's accomplishments)
- Career transition (shift in focus/values)

**Process:**
1. Add new documents to career documents directory
2. Run: `python run_llm_analysis.py`
3. Skills automatically use updated lexicons on next invocation

### Skill Updates

**When to update skills:**
- User feedback reveals friction points
- New best practices emerge (ATS changes, hiring trends)
- Claude capabilities expand (new tools available)

**Update process:**
1. Edit SKILL.md file in `~/.claude/skills/career/[skill-name]/`
2. Test with real job description
3. Validate with user
4. Deploy (skills refresh automatically)

---

## Conclusion

This comprehensive system transforms the Socratic career application process from documentation into actionable, usable skills. By grounding all recommendations in verified lexicons and maintaining strict authenticity requirements, the system helps users create compelling, truthful application materials efficiently.

**Key Innovations:**
1. Pure LLM approach (no Python semantic matching)
2. Lexicon-grounded authenticity (all content verified)
3. Modular independence (use skills standalone or in sequence)
4. Comparison-ready structure (job requirements → lexicon matches)
5. Evidence-based verification (every claim cited)
6. Socratic methodology (reflective, authentic development)

**Next Steps:**
1. Write implementation plan (detailed task breakdown)
2. Create skill files
3. Test with real job applications
4. Iterate based on user feedback
5. Deploy to production

---

**Document Version:** 1.0
**Date:** 2025-10-31
**Author:** Claude Code + User
**Status:** Design Complete - Ready for Implementation Planning