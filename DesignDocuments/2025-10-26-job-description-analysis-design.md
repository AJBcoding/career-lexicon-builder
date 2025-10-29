# Job Description Analysis Skill - Design Document

**Date:** 2025-10-26  
**Purpose:** Create a skill to analyze job descriptions and extract strategic information for targeted application materials  
**Integration:** Phase 0 of Socratic Career Application Orchestration + Standalone capability

---

## Overview

This skill analyzes job descriptions to identify key qualifications, extract ATS-optimized keywords, decode organizational culture, and surface values alignment opportunities. It serves as the foundation (Phase 0) for the career application orchestration process while also functioning as a standalone analysis tool.

### Core Capabilities

1. **Weighted Keyword Extraction** - Categorize and prioritize keywords by importance with strategic placement guidance
2. **Tone & Culture Analysis** - Decode organizational culture signals with industry comparison
3. **Values Alignment Identification** - Surface mission/values hooks for cover letter narratives
4. **Role Clarity Analysis** - Determine seniority, reporting structure, and role type
5. **Strategic Guidance** - Provide actionable recommendations for resume and cover letter

---

## Architecture

### File Structure

```
job-description-analysis/
├── SKILL.md (main workflow and overview)
├── ats-keyword-framework.md (strategic keyword mapping reference)
├── tone-analysis-guide.md (culture decoding patterns)
└── values-alignment-patterns.md (identifying mission/values hooks)
```

### Progressive Disclosure Pattern

- **SKILL.md** - Lightweight workflow and core patterns (<500 lines)
- **Reference files** - Detailed frameworks loaded only when needed
- Follows existing skill architecture (e.g., pptx, docx patterns)

---

## Workflow Process

### Phase 1: Initial Analysis (Automated)

**Input Handling:**
- Accept job descriptions in multiple formats: PDF, Word, plain text, web pages
- Parse document into logical sections: responsibilities, qualifications, company info, benefits
- Handle various job posting structures (structured vs. unstructured)

**Preliminary Analysis:**
- Extract all mentioned skills, qualifications, and requirements
- Identify explicit requirements vs. preferred qualifications
- Categorize keywords by type (hard skills, soft skills, tools, industry terms)
- Flag ambiguous or contradictory language
- Detect missing standard components

**Output:** Internal structured data ready for refinement

### Phase 2: Socratic Refinement (Priority-based)

**High-Priority Strategic Questions (one at a time):**

Triggers for strategic questions:
- Ambiguous role interpretation (IC vs. management, seniority level unclear)
- Cultural contradictions (innovative + risk-averse language)
- Multiple valid interpretations of key requirements
- Unclear reporting structure or team dynamics
- Requirements gaps (missing expected qualifications for role type)

Example questions:
- "This posting mentions both 'lead projects' and 'report to Senior Director.' Do you interpret this as an individual contributor role with project leadership, or a people management position?"
- "The posting emphasizes 'innovative thinking' but also 'established processes.' Which signal do you think is stronger for your cover letter emphasis?"

**Low-Priority Clarifications (batched):**

Batch 2-4 related questions together:
- Confirmation of preferred vs. required distinctions
- Clarification of vague quantifiers ("some experience," "familiarity")
- Verification of industry terminology interpretation
- Salary/benefits interpretation

Example:
- "I have 3 quick clarifications:
  1. Is 'familiarity with SQL' preferred or required?
  2. Does '5+ years' include internship experience?
  3. Is 'stakeholder management' primarily internal or external?"

### Phase 3: Output Generation

**Create Structured Markdown File:**

Filename: `job-analysis-YYYY-MM-DD-[sanitized-title].md`  
Location: `/mnt/user-data/outputs/`

**File Structure:**

```markdown
# Job Analysis: [Position Title] - [Company]
Date: YYYY-MM-DD

## Executive Summary
[2-3 sentence overview for quick context]

## Required Qualifications [High Priority]
- Explicit requirements from posting
- Years of experience
- Must-have skills/certifications

## Preferred Qualifications [Medium Priority]
- Nice-to-have skills
- Bonus experience areas
- Optional certifications/tools

## ATS Keyword Strategy

### Critical Keywords (Use in BOTH resume + cover letter)
- **[Keyword]**
  - Resume placement: [specific location guidance]
  - Cover letter placement: [paragraph suggestion]
  - Frequency: [recommendation]

### Important Keywords (Emphasize in resume)
- **[Keyword]**
  - Priority reasoning: [explicit requirement / repeated 3x / role-critical]
  - Resume placement: [guidance]

### Supporting Keywords (Include if applicable)
- Tools: [list]
- Methodologies: [list]
- Industry terms: [list]

### Synonym Mapping
- [Keyword] → Alternative phrasings: [synonyms that match intent]

### Action Verbs from Posting
- [List verbs to mirror in application materials]

## Tone & Culture Analysis

### Tone Classification
- Formality: [Formal / Casual / Mixed]
- Innovation: [Innovative / Traditional / Balanced]
- Collaboration: [Highly collaborative / Independent / Balanced]

### Evidence from Posting
- "[Quote demonstrating tone]"
- "[Quote demonstrating culture]"
- "[Quote showing values]"

### Culture Signals
**Innovation indicators:** [specific findings]
**Collaboration markers:** [specific findings]
**Autonomy signals:** [specific findings]
**Work-life balance:** [signals from posting]

### Industry Comparison
- Compared to [industry/sector] norms: [analysis]
- Distinctive culture elements: [what stands out]

### Writing Recommendations for Cover Letter
- **Formality level:** [guidance]
- **Sentence structure:** [suggestions]
- **Vocabulary alignment:** [specific words/phrases to mirror]
- **Tone matching:** [overall approach]

## Role Clarity

### Role Type
- [Individual Contributor / People Manager / Hybrid]
- [Entry / Mid / Senior / Executive level]

### Reporting Structure
- Reports to: [from posting or inferred]
- Team size: [if mentioned]
- Cross-functional interactions: [analysis]

### Key Responsibilities (Prioritized)
1. [Most emphasized responsibility]
2. [Second priority]
3. [Third priority]

## Values & Mission Alignment Hooks

### Stated Mission/Purpose
- [Direct quotes from posting about company mission]

### Implicit Values
- Diversity & inclusion signals: [findings]
- Innovation focus: [findings]
- Customer/user focus: [findings]
- Social impact: [findings]
- [Other identified values]

### Cover Letter Connection Opportunities
- Opening hook: [suggestion based on values]
- Mid-letter alignment: [opportunity to demonstrate shared values]
- Closing reflection: [values-based closing angle]

## Red Flags & Considerations

### Potential Concerns
- [Any red flag language: "fast-paced" + long hours]
- [Vague or unrealistic expectations]
- [Missing information: no salary, no team info]
- [Contradictory requirements]

### Missing Standard Components
- [What's NOT mentioned that typically would be]
- [Implications of gaps]

## Application Strategy Summary

### Top 3 Priorities for Resume
1. [Most critical alignment point]
2. [Second priority]
3. [Third priority]

### Top 3 Priorities for Cover Letter
1. [Most compelling narrative angle]
2. [Values alignment opportunity]
3. [Unique differentiator to emphasize]
```

**Generate Context Summary:**

Concise 3-5 sentence summary injected into conversation:
- Role type and seniority
- Top 3 critical keywords
- Primary culture signal
- Key values alignment opportunity

### Phase 4: Handoff

**For Standalone Use:**
- Present download link: `[View your job analysis](computer:///mnt/user-data/outputs/job-analysis-...md)`
- Brief summary of key findings
- Offer to explore any section in depth

**For Orchestration Integration:**
- Provide download link
- Inject context summary into conversation
- Announce: "Job analysis complete. Ready to proceed to Phase 1: Initialization and Orientation."
- Pass structured data to downstream skills

---

## Integration Points

### Activation Patterns

**Standalone Activation:**
- User explicitly requests: "analyze this job description"
- User uploads document with job-posting-like content and asks for analysis

**Orchestration Activation:**
- Automatically triggered as mandatory Phase 0 when user starts: "I'd like to begin the Socratic Career Application Orchestration Skill"
- Runs before current Phase 1 (Initialization and Orientation)

### Downstream Skill Handoffs

**To Resume Alignment Skill:**
- ATS keyword list (Critical + Important keywords)
- Action verbs for resume bullet points
- Role clarity information for positioning

**To Job Fit Analysis Skill:**
- Required vs. preferred qualifications (for gap analysis)
- Role clarity (for alignment assessment)
- Red flags and considerations

**To Cover Letter Planning Skill:**
- Tone & culture analysis (for voice matching)
- Values alignment hooks (for narrative development)
- Writing recommendations

**To Voice & Narrative Development Skill:**
- Tone classification and evidence
- Writing style recommendations
- Values-based narrative opportunities

---

## Reference File Contents

### ats-keyword-framework.md

**Purpose:** Detailed guidance on ATS optimization and keyword strategy

**Contents:**
- How ATS systems work (resume screening algorithms)
- Keyword density best practices (frequency without stuffing)
- Strategic placement patterns (where keywords matter most)
- Context matching (keywords need proper context, not just presence)
- Synonym strategies (variations that match intent)
- Industry-specific keyword patterns
- Common ATS pitfalls to avoid

### tone-analysis-guide.md

**Purpose:** Framework for decoding organizational culture from job postings

**Contents:**
- Tone classification taxonomy
  - Formality spectrum (formal → casual)
  - Innovation spectrum (traditional → cutting-edge)
  - Collaboration spectrum (independent → highly collaborative)
  - Autonomy spectrum (directed → self-guided)
- Signal patterns by category
  - Innovation indicators and their meanings
  - Collaboration markers and implications
  - Work-life balance signals
  - Growth/development culture signs
- Industry comparison benchmarks
  - Tech sector norms
  - Finance sector norms
  - Non-profit sector norms
  - Academic sector norms
  - Government sector norms
- Writing style matching guide
  - How to mirror formality level
  - Vocabulary alignment techniques
  - Sentence structure matching

### values-alignment-patterns.md

**Purpose:** Identify mission/values opportunities for authentic cover letter hooks

**Contents:**
- Common organizational values categories
  - Innovation and creativity
  - Diversity, equity, and inclusion
  - Customer/user focus
  - Social impact and sustainability
  - Collaboration and teamwork
  - Excellence and quality
  - Integrity and ethics
- Recognizing implicit values (what's emphasized but not stated)
- Connecting personal experience to organizational values
- Authentic vs. performative alignment (avoiding hollow statements)
- Cover letter integration techniques
  - Opening hooks using values
  - Mid-letter narrative connections
  - Closing reflections on shared mission
- Examples of effective values-based cover letter excerpts

---

## Socratic Questioning Framework

### Ambiguity Detection Triggers

**Automatic detection for:**
- Vague quantifiers ("some experience," "familiarity with," "exposure to")
- Contradictory language pairs
  - "innovative" + "risk-averse"
  - "fast-paced" + "work-life balance"
  - "autonomous" + "highly structured"
- Requirements gaps (missing expected components for role type)
  - Senior role without leadership mention
  - Technical role without specific technologies
  - Strategic role without outcome metrics
- Red flag language patterns
  - "Wear many hats" + extensive job duties
  - "Fast-paced environment" + long hours
  - "We're like a family" (boundary concerns)
  - Excessive exclamation points or hype language
- Structural oddities
  - No salary range mentioned
  - No team size or reporting structure
  - Unrealistic combination of requirements

### Question Prioritization Logic

**High-Priority (ask individually):**
1. Questions affecting application strategy
   - Role interpretation (IC vs. management)
   - Seniority level ambiguity
   - Primary culture emphasis choice
2. Questions with multiple valid interpretations
   - Responsibilities that could be scope-creep vs. growth
   - Requirements that could be must-have vs. aspirational
3. Red flags requiring user judgment
   - Potentially problematic work expectations
   - Cultural misalignment risks

**Low-Priority (batch together):**
1. Factual clarifications
   - Preferred vs. required distinctions
   - Experience counting rules (internships, part-time)
   - Tool/terminology familiarity
2. Nice-to-know details
   - Benefits interpretation
   - Location flexibility
   - Minor ambiguities that don't affect strategy

---

## Success Criteria

### Skill Effectiveness Measures

**For Standalone Use:**
- User has clear understanding of job requirements
- User has actionable keyword strategy
- User has cultural insight for cover letter tone
- User has values hooks for authentic storytelling

**For Orchestration Use:**
- Downstream skills receive properly structured data
- Resume alignment skill has keyword priorities
- Cover letter planning skill has tone guidance
- User doesn't need to re-analyze posting during later phases

### Quality Indicators

**Analysis Quality:**
- All explicit requirements captured
- Keywords properly weighted by importance
- Tone classification supported by evidence
- Values identification goes beyond obvious statements
- Strategic guidance is actionable, not generic

**Socratic Refinement Quality:**
- High-priority questions focus on genuine ambiguities
- Questions lead to strategic clarity, not just information gathering
- User feels collaborative process, not interrogation
- Clarifications batch efficiently without losing important nuance

---

## Example Use Cases

### Use Case 1: Standalone Analysis

**Scenario:** User has a job description for "Senior Product Manager, B2B SaaS" and wants to understand requirements before starting application

**Workflow:**
1. User: "Can you analyze this job description?" [uploads PDF]
2. Skill: [Extracts content, performs initial analysis]
3. Skill: "I have one strategic question: This posting mentions both 'lead cross-functional teams' and 'report to Director of Product.' Do you interpret this as a people management role or IC with project leadership?"
4. User: "IC with project leadership"
5. Skill: [Completes analysis, generates file]
6. Skill: "Analysis complete. [Link to file]. Key findings: This is a senior IC role emphasizing stakeholder management (critical keyword), B2B SaaS expertise (use 3x), and data-driven decision making. Culture is collaborative-innovative (mirror this tone in your cover letter)."

### Use Case 2: Orchestration Phase 0

**Scenario:** User starting full application process using orchestration skill

**Workflow:**
1. User: "I'd like to begin the Socratic Career Application Orchestration Skill"
2. Orchestration: "Starting with Phase 0: Job Description Analysis. Please provide the job description."
3. User: [Uploads job posting]
4. Analysis Skill: [Performs analysis, asks strategic questions, generates file]
5. Analysis Skill: "Job analysis complete. [Link]. Ready to proceed to Phase 1: Initialization and Orientation."
6. Orchestration: [Receives structured data, continues to Phase 1]

### Use Case 3: Complex Posting with Ambiguities

**Scenario:** Job posting for "Program Manager" with unclear scope and contradictory culture signals

**Workflow:**
1. User: "Analyze this job description" [uploads document]
2. Skill: [Initial analysis flags multiple ambiguities]
3. Skill: "I have one strategic question: This role emphasizes both 'innovative problem-solving' and 'following established frameworks.' Which culture signal do you think is more authentic based on the company/industry?"
4. User: "Probably established frameworks - it's a regulated industry"
5. Skill: "I have 2 clarifications: (1) Is 'manage projects' here about people management or project coordination? (2) The posting lists both 'preferred' and 'nice-to-have' - should I treat these differently?"
6. User: "Project coordination, not people. Treat preferred and nice-to-have as the same."
7. Skill: [Completes analysis with user's interpretations]
8. Skill: "Analysis complete. [Link]. Note: Red flag detected - posting mentions 'fast-paced' with 50+ hour weeks expected. Consider whether this aligns with your preferences."

---

## Implementation Notes

### Technical Considerations

**Document Processing:**
- Use appropriate libraries for different formats (pdfplumber for PDF, python-docx for Word)
- Handle both structured (LinkedIn/Indeed) and unstructured postings
- Preserve formatting cues (bold, bullets) that signal importance
- Extract from web pages if URL provided

**Text Analysis:**
- Identify section boundaries (responsibilities vs. qualifications)
- Distinguish explicit requirements from descriptive language
- Track keyword frequency and positioning
- Detect required vs. preferred qualifications by section and language patterns

**File Generation:**
- Use consistent markdown formatting for scannability
- Include both detailed sections and quick-reference summaries
- Ensure download links work correctly
- Save to /mnt/user-data/outputs/ for user access

### Edge Cases

**Minimal/Vague Postings:**
- Flag insufficient information explicitly
- Ask targeted questions to fill gaps based on role type norms
- Provide analysis of what's missing and why it matters

**Non-Standard Postings:**
- Internal job descriptions (less marketing language)
- Academic positions (different structure/emphasis)
- Contract/freelance roles (different expectations)
- Adapt analysis framework to posting type while maintaining core components

**Multiple Role Variations:**
- When posting describes multiple levels (Junior/Senior)
- When hybrid roles combine distinct functions
- Guide user to clarify which version they're targeting

---

## Future Enhancements

Potential additions for future iterations:

1. **Comparison Mode:** Analyze multiple job descriptions and compare requirements, culture, keywords
2. **Historical Tracking:** Save analyses over time, identify patterns in roles user targets
3. **Company Research Integration:** Supplement job description with broader company culture data
4. **Salary Analysis:** Integrate market data to assess compensation competitiveness
5. **Application Timeline:** Suggest application urgency based on posting language and job market trends

---

## Validation & Testing Plan

### Testing Approach

Follow TDD methodology from writing-skills:

**RED Phase - Baseline Testing:**
- Run scenarios WITHOUT the skill
- Test with different job posting types (tech, non-profit, academic, corporate)
- Document what information gets missed or misinterpreted
- Identify common failure patterns

**GREEN Phase - Skill Creation:**
- Write skill addressing specific baseline failures
- Test with same scenarios - verify correct analysis
- Ensure Socratic questions surface ambiguities effectively

**REFACTOR Phase - Refinement:**
- Test with edge cases (vague postings, contradictory language)
- Verify reference files load correctly when needed
- Ensure downstream skills receive properly formatted data
- Close any loopholes in analysis or questioning logic

### Test Scenarios

**Scenario 1: Clear, Well-Structured Posting**
- Standard corporate job description
- Explicit requirements vs. preferred
- Should complete with minimal Socratic questioning

**Scenario 2: Ambiguous Posting**
- Unclear seniority level
- Mixed culture signals
- Should trigger strategic questions

**Scenario 3: Red Flag Posting**
- Unrealistic expectations
- Boundary concerns
- Should flag issues for user consideration

**Scenario 4: Minimal Information**
- Brief posting with gaps
- Should identify missing components
- Should ask questions to supplement

**Scenario 5: Non-Standard Format**
- Academic position
- Internal job description
- Should adapt analysis appropriately

---

## Documentation Requirements

### SKILL.md Structure

```markdown
---
name: job-description-analysis
description: Use when analyzing job postings to identify requirements, extract ATS keywords, decode culture, and find values alignment opportunities - creates structured analysis for targeted resume and cover letter development, serves as Phase 0 of career application orchestration
---

# Job Description Analysis

## Overview
[Core principle, integration points]

## When to Use
[Standalone vs. orchestration triggers]

## Analysis Components
[Quick reference to what gets analyzed]

## Workflow
[Phase 1-4 summary]

## Output Structure
[What user receives]

## Integration with Other Skills
[How downstream skills use the analysis]

## Socratic Refinement
[When/how questions are asked]

## Reference Materials
[Links to supporting files]
```

### Metadata Requirements

**Name:** `job-description-analysis` (lowercase, hyphens only)

**Description:** Under 1024 characters, includes:
- Triggering conditions ("Use when analyzing job postings...")
- Core capabilities (requirements, keywords, culture, values)
- Integration point (Phase 0 of orchestration)
- Written in third person

---

## Success Metrics

**Immediate Success:**
- User has actionable analysis within 5-10 minutes
- All critical requirements identified and prioritized
- ATS keywords properly weighted and placement-mapped
- Culture/tone analysis supported by evidence
- Strategic questions resolve genuine ambiguities

**Downstream Success:**
- Resume alignment skill has clear keyword priorities
- Cover letter planning skill has tone guidance and values hooks
- Job fit analysis skill has structured requirements data
- User doesn't need to re-reference original posting during later phases

**Quality Indicators:**
- Analysis is comprehensive without being overwhelming
- Strategic guidance is specific, not generic
- Socratic questions focus attention on what matters
- Output file is scannable and well-organized
- User feels confident about job requirements and strategic approach

---

## Conclusion

This skill provides the strategic foundation for the entire career application process. By extracting, analyzing, and organizing job description information comprehensively, it enables targeted, authentic application materials that pass ATS screening while genuinely aligning with organizational culture and values.

The combination of automated analysis and strategic Socratic refinement ensures both efficiency and thoughtfulness - users get quick, actionable results while maintaining the reflective, authentic approach that characterizes the Socratic career application framework.
