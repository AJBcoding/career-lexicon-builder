---
name: job-description-analysis
description: Use when analyzing job postings to identify requirements, extract ATS keywords, decode culture, and find values alignment opportunities - creates structured analysis for targeted resume and cover letter development, serves as Phase 0 of career application orchestration
---

# Job Description Analysis

## Overview

Analyze job descriptions to extract strategic information for targeted application materials. This skill serves as Phase 0 (foundational analysis) of the Socratic Career Application Orchestration process and also functions as a standalone analysis tool.

**Core principle:** Transform unstructured job postings into actionable strategic guidance through systematic extraction, prioritization, and interpretation.

**Announce at start:**  
> "I'm using the Job Description Analysis Skill to extract requirements, decode culture, and identify strategic opportunities."

## When to Use

**Standalone activation:**
- User explicitly requests: "analyze this job description"
- User uploads document with job-posting content and asks for analysis
- Quick strategic assessment needed before application

**Orchestration activation:**
- Automatically triggered as mandatory Phase 0 when user starts career application orchestration
- Runs before Initialization and Orientation phase
- Provides structured foundation for all downstream application materials

## Analysis Components

This skill produces a comprehensive analysis covering:

| Component | Purpose | Downstream Use |
|-----------|---------|----------------|
| **Required vs. Preferred Qualifications** | Distinguish must-haves from nice-to-haves | Gap analysis, strategic positioning |
| **ATS Keyword Strategy** | Weighted keywords with placement guidance | Resume optimization, cover letter integration |
| **Tone & Culture Analysis** | Decode organizational culture signals | Voice matching, writing style alignment |
| **Values Alignment Hooks** | Identify mission/values opportunities | Authentic cover letter narratives |
| **Role Clarity** | Seniority, reporting structure, scope | Resume positioning, experience emphasis |
| **Red Flags & Considerations** | Detect potential concerns | Informed decision-making |
| **Application Strategy** | Top priorities for resume and cover letter | Targeted material development |

## Workflow

### Phase 1: Document Extraction and Initial Analysis

**Input handling:**
1. Accept multiple formats (PDF, Word, plain text, web pages, pasted text)
2. Use appropriate tool:
   - PDF → pdfplumber for text extraction
   - Word → python-docx for .docx files
   - Web → web_fetch for URLs
   - Plain text → direct analysis
3. Preserve formatting cues (bold, bullets) that signal importance

**Automated analysis:**
- Parse document into logical sections: responsibilities, qualifications, company info, benefits
- Extract all mentioned skills, qualifications, requirements
- Identify explicit requirements vs. preferred qualifications (by section and language patterns)
- Categorize keywords by type:
  - Hard skills (technical abilities, tools, methodologies)
  - Soft skills (communication, leadership, collaboration)
  - Domain knowledge (industry-specific expertise)
  - Tools and technologies
  - Certifications and credentials
- Track keyword frequency and positioning
- Detect formatting emphasis (bold, bullet hierarchy)

**Preliminary detection:**
- Flag ambiguous language ("some experience," "familiarity")
- Identify contradictory culture signals
- Detect missing standard components
- Note unclear role boundaries (IC vs. management)
- Spot potential red flags

**Output:** Internal structured data for Phase 2 refinement

### Phase 2: Socratic Refinement (Priority-Based Questioning)

**Question prioritization:** Ask strategic questions one at a time; batch low-priority clarifications.

**Triggers for HIGH-PRIORITY strategic questions:**

Ask ONE strategic question when detecting:
- **Role ambiguity**: Language suggests both IC and management (e.g., "lead teams" + "report to Director")
- **Seniority unclear**: Could be interpreted as mid-level OR senior-level
- **Cultural contradiction**: Conflicting signals (e.g., "innovative" + "established processes," "fast-paced" + "work-life balance")
- **Multiple interpretations**: Key requirement could mean different things in context
- **Unclear scope**: Responsibilities span multiple distinct functions

**Example strategic questions:**
> "This posting mentions both 'lead cross-functional projects' and 'report to Senior Director.' Do you interpret this as an individual contributor role with project leadership, or a people management position?"

> "The posting emphasizes both 'innovative problem-solving' and 'following established frameworks.' Which culture signal do you think is more authentic based on the company/industry context?"

**Triggers for LOW-PRIORITY clarifications (batch 2-4 together):**
- Preferred vs. required distinctions unclear
- Vague quantifiers ("some," "familiarity," "exposure")
- Industry terminology that might have multiple meanings
- Salary/benefits interpretation
- Standard qualifications that seem to be missing

**Example batched clarifications:**
> "I have 3 quick clarifications:
> 1. Is 'familiarity with SQL' treated as required or preferred?
> 2. Does '5+ years experience' typically include internship time in this field?
> 3. Is 'stakeholder management' here primarily internal teams or external clients?"

**Principle:** Minimize interruption. Only ask when user input genuinely improves analysis quality.

### Phase 3: Comprehensive Analysis and Structuring

**Keyword prioritization framework:**

Apply weighting system (see [ats-keyword-framework.md](ats-keyword-framework.md) for details):

**Critical Keywords** (must appear in BOTH resume and cover letter):
- Explicitly required qualifications
- Keywords repeated 3+ times
- Role-defining terms (e.g., "data analysis" for Data Analyst role)
- Skills emphasized in early paragraphs

**Important Keywords** (emphasize in resume):
- Preferred qualifications
- Keywords mentioned 2 times
- Technical tools/methodologies central to role
- Domain-specific terminology

**Supporting Keywords** (include if applicable):
- Nice-to-have skills
- Tools mentioned once
- Industry buzzwords
- Related methodologies

**Strategic placement guidance:**
- Where in resume each keyword should appear (summary, experience, skills section)
- How often to use without stuffing (density guidelines)
- Context requirements (keywords need proper context, not just presence)
- Synonym mapping for natural variation

**Tone and culture decoding:**

Analyze along four dimensions (see [tone-analysis-guide.md](tone-analysis-guide.md) for framework):

1. **Formality**: Formal / Professional-Casual / Casual
2. **Innovation**: Traditional / Balanced / Cutting-edge
3. **Collaboration**: Independent / Balanced / Highly Collaborative
4. **Autonomy**: Directed / Balanced / Self-Guided

**Evidence collection:**
- Pull direct quotes demonstrating each dimension
- Identify signal patterns (e.g., "fast-paced" + "startup environment" = casualcutting-edge)
- Compare to industry norms
- Flag contradictions between stated and implied culture

**Writing recommendations:**
- Formality level to match in cover letter
- Sentence structure guidance (short/punchy vs. developed paragraphs)
- Vocabulary to mirror (specific words/phrases from posting)
- Tone balance for contradictory signals

**Values alignment identification:**

Detect explicit and implicit values (see [values-alignment-patterns.md](values-alignment-patterns.md)):

Common value categories:
- Innovation and creativity
- Diversity, equity, and inclusion
- Customer/user focus
- Social impact and sustainability
- Collaboration and teamwork
- Excellence and quality
- Integrity and ethics
- Growth and development

**Connection opportunities:**
- Opening hook suggestions based on strongest values
- Mid-letter narrative connections (experience → values)
- Closing reflection angles (shared mission)

**Role clarity analysis:**
- Role type: IC / People Manager / Hybrid
- Seniority level: Entry / Mid / Senior / Executive
- Reporting structure (if stated or inferable)
- Team dynamics indicators
- Cross-functional interaction expectations

**Key responsibilities prioritization:**
- Rank by emphasis in posting (positioning, repetition, formatting)
- Identify what matters MOST to the employer
- Flag responsibilities that need addressing in application materials

**Red flag detection:**

Systematically check for concerns (see [red-flag-reference.md](red-flag-reference.md) for comprehensive catalog):

| Category | Examples |
|----------|----------|
| **Scope/Expectations** | Unrealistic job requirements, "wearing many hats," unclear boundaries |
| **Compensation** | Below-market salary, missing benefits info, "competitive pay" without range |
| **Culture** | "Fast-paced" + long hours, high turnover signals, excessive urgency |
| **Language** | Vague descriptions, jargon overload, aggressive tone |
| **Contradictions** | Conflicting requirements, mismatched role level vs. responsibilities |

**Reasonableness checking:**
- Apply market compensation guidelines
- Compare to industry norms for role type
- Flag when expectations don't match seniority level
- Identify gaps in standard posting components

**Missing information detection:**
- What's NOT mentioned that typically would be
- Standard components absent (salary range, team size, reporting structure)
- Implications of gaps for assessment

### Phase 4: Output Generation and Handoff

**Create structured markdown file:**

Filename pattern: `job-analysis-YYYY-MM-DD-[sanitized-title].md`  
Location: `/mnt/user-data/outputs/`

**File structure template:**

```markdown
# Job Analysis: [Position Title] - [Company]
Date: YYYY-MM-DD

## Executive Summary
[2-3 sentence overview: role type, top 3 keywords, culture, key opportunity]

## Required Qualifications [High Priority]
[Must-have skills, experience years, certifications]

## Preferred Qualifications [Medium Priority]
[Nice-to-have skills, bonus areas, optional tools]

## ATS Keyword Strategy

### Critical Keywords (Use in BOTH resume + cover letter)
- **[Keyword]** 
  - Resume placement: [guidance]
  - Cover letter placement: [guidance]
  - Frequency: [recommendation]

### Important Keywords (Emphasize in resume)
[Keywords with priority reasoning and placement]

### Supporting Keywords (Include if applicable)
[Tools, methodologies, industry terms]

### Synonym Mapping
[Keyword variations that match intent]

### Action Verbs from Posting
[Verbs to mirror in materials]

## Tone & Culture Analysis

### Tone Classification
- Formality: [level]
- Innovation: [level]
- Collaboration: [level]
- Autonomy: [level]

### Evidence from Posting
[Direct quotes supporting each classification]

### Culture Signals
[Specific findings on innovation, collaboration, work-life balance, growth]

### Industry Comparison
[How this compares to sector norms, distinctive elements]

### Writing Recommendations for Cover Letter
[Formality, structure, vocabulary, tone guidance]

## Role Clarity

### Role Type
[IC/Manager/Hybrid, seniority level]

### Reporting Structure
[From posting or inferred]

### Key Responsibilities (Prioritized)
[Top 3 most emphasized]

## Values & Mission Alignment Hooks

### Stated Mission/Purpose
[Direct quotes about company mission]

### Implicit Values
[Detected values with evidence]

### Cover Letter Connection Opportunities
[Opening hook, mid-letter alignment, closing reflection suggestions]

## Red Flags & Considerations

### Potential Concerns
[Detected red flags with evidence]

### Missing Standard Components
[What's absent and implications]

## Application Strategy Summary

### Top 3 Priorities for Resume
[Most critical alignment points]

### Top 3 Priorities for Cover Letter
[Narrative angles, values alignment, differentiators]
```

**Generate context summary:**

Create concise 3-5 sentence summary for conversation:
- Role type and seniority
- Top 3 critical keywords  
- Primary culture signal
- Key values alignment opportunity

**Handoff protocol:**

**For standalone use:**
```
Analysis complete. [View your job analysis](computer:///mnt/user-data/outputs/job-analysis-YYYY-MM-DD-title.md)

Key findings: [Context summary]. 

Happy to explore any section in depth or begin developing your application materials.
```

**For orchestration integration:**
```
Job analysis complete. [View your analysis](computer:///mnt/user-data/outputs/job-analysis-YYYY-MM-DD-title.md)

[Context summary]

Ready to proceed to Phase 1: Initialization and Orientation.
```

## Format Adaptation

**Non-standard posting types** require adaptation (see [format-adaptation-guide.md](format-adaptation-guide.md)):

- **Academic positions**: Emphasize teaching philosophy, publication expectations, tenure requirements
- **Government roles**: Focus on GS levels, clearance requirements, USAJobs conventions
- **Non-profit positions**: Highlight mission alignment, funding context, community engagement
- **Startup roles**: Note equity details, stage-specific expectations, ambiguity tolerance
- **International postings**: Consider visa requirements, cultural context, location specifics
- **Contract/freelance**: Emphasize project scope, deliverables, client relationship dynamics

**Detection:** Identify posting type early in Phase 1 and load appropriate framework.

## Integration with Other Skills

**Data provided to downstream skills:**

**Resume Alignment Skill receives:**
- Critical + Important ATS keywords
- Action verbs for resume bullets
- Role clarity for positioning
- Priority skills for emphasis

**Job Fit Analysis Skill receives:**
- Required vs. preferred qualifications structure
- Role clarity and expectations
- Red flags and considerations
- Gap areas to address

**Cover Letter Planning Skill receives:**
- Tone & culture classification with evidence
- Values alignment hooks
- Writing recommendations
- Strategic narrative opportunities

**Voice & Narrative Development Skill receives:**
- Detailed tone analysis
- Writing style specifications
- Values-based story angles
- Company mission language

## Socratic Refinement Principles

**When to ask questions:**
- Genuine ambiguity exists with multiple valid interpretations
- User's domain knowledge would improve analysis accuracy
- Cultural signals conflict and context is needed
- Role boundaries are unclear from posting alone

**When NOT to ask questions:**
- Information is clearly stated in posting
- Industry standards provide clear interpretation
- Clarification would not materially improve analysis
- Question is truly low-priority and doesn't affect strategy

**Question quality:**
- Frame as multiple choice when possible to reduce friction
- Provide context for WHY the question matters
- Batch related low-priority questions together
- Keep strategic questions focused and singular

## Reference Materials

For detailed frameworks and comprehensive guidance:

- **[ats-keyword-framework.md](ats-keyword-framework.md)** - ATS system mechanics, keyword density, placement strategies, common pitfalls
- **[tone-analysis-guide.md](tone-analysis-guide.md)** - Culture decoding taxonomy, signal patterns, industry benchmarks, writing style matching
- **[values-alignment-patterns.md](values-alignment-patterns.md)** - Organizational values categories, authentic connection techniques, cover letter integration
- **[red-flag-reference.md](red-flag-reference.md)** - Comprehensive red flag catalog, reasonableness framework, severity scoring, market guidelines
- **[format-adaptation-guide.md](format-adaptation-guide.md)** - Academic, government, non-profit, startup, international, contract posting conventions

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Treating all keywords equally | Use 3-tier prioritization (Critical/Important/Supporting) |
| Generic culture analysis | Pull direct quotes as evidence, compare to industry norms |
| Missing implicit values | Look beyond stated mission to emphasized behaviors and priorities |
| Ignoring red flags | Systematically check all categories, apply reasonableness tests |
| Over-asking questions | Only ask when user input materially improves analysis |
| Skipping format adaptation | Detect posting type and apply appropriate conventions |
| Creating overwhelming output | Use clear hierarchy, make file scannable, prioritize strategically |

## Success Criteria

**Quality indicators:**
- Analysis completed within 5-10 minutes
- All critical requirements identified and properly prioritized
- ATS keywords weighted with strategic placement guidance
- Culture analysis supported by specific evidence from posting
- Strategic questions resolved genuine ambiguities (not make-work)
- Output file is scannable and actionable
- User feels confident about requirements and strategic approach

**Downstream validation:**
- Resume alignment skill has clear keyword priorities
- Cover letter planning skill has tone guidance and values hooks
- Job fit analysis skill has structured requirements
- User doesn't need to re-reference original posting during later phases
