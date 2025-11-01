# LLM-Based Career Lexicon Analysis - Design Document

**Date**: 2025-10-31
**Status**: Proposed
**Replaces**: Semantic similarity-based analysis approach

---

## Problem Statement

The current semantic similarity approach produces outputs that are:
- Too literal (tracks phrases like "I believe" instead of actual values)
- Too granular (individual bullet points without meaningful grouping)
- Not actionable (lacks guidance on when/how to use the information)
- Flat structure (no hierarchy, hard to navigate)

**User's Goal**: Create a useful reference when analyzing job descriptions and writing cover letters/resumes.

---

## Solution: LLM-Based Interpretive Analysis

Use Claude API to perform **interpretive analysis** of career documents, producing hierarchical, actionable reference guides.

### Key Differences from Current Approach

| Current (Semantic Similarity) | New (LLM-Based) |
|------------------------------|-----------------|
| Finds similar text chunks | Interprets meaning and themes |
| Groups by text similarity | Groups by conceptual relevance |
| No actionable guidance | Provides usage recommendations |
| Flat markdown output | Hierarchical, navigable structure |
| Pattern matching | Understanding + synthesis |

---

## Hierarchical Output Structure

### 1. **Career Philosophy & Values**

```
# Career Philosophy & Values

## I. Leadership Approach
  ├─ A. Listening-First Leadership
  │   ├─ 1. Core Principle
  │   │   └─ Definition & importance
  │   ├─ 2. Evidence from Documents
  │   │   ├─ Primary quotes
  │   │   └─ Secondary examples
  │   ├─ 3. Application Guidance
  │   │   ├─ When to emphasize
  │   │   └─ How to phrase
  │   └─ 4. Related Themes
  │       └─ Links to other sections
  │
  ├─ B. Collaborative Decision-Making
  │   └─ [same structure]
  │
  └─ C. Equity-Centered Practice
      └─ [same structure]

## II. Core Values
  ├─ A. Arts as Social Justice
  ├─ B. Student-Centered Education
  └─ C. Institutional Stewardship

## III. Problem-Solving Philosophy
  ├─ A. Data-Informed Decisions
  ├─ B. Systems Thinking
  └─ C. Sustainable Solutions
```

### 2. **Achievement Library**

```
# Achievement Library

## I. Capital Projects & Infrastructure
  ├─ A. Kirk Douglas Theater ($12.1M Project)
  │   ├─ 1. Overview
  │   │   └─ Context, scope, impact
  │   ├─ 2. Variations by Emphasis
  │   │   ├─ a. Project Management Focus
  │   │   │   └─ "Stewarded $12.1M adaptive reuse from conception..."
  │   │   ├─ b. Financial Stewardship Focus
  │   │   │   └─ "Delivered on-time, on-budget completion..."
  │   │   ├─ c. Stakeholder Management Focus
  │   │   │   └─ "Negotiated public-private partnership with..."
  │   │   └─ d. Team Leadership Focus
  │   │       └─ "Built and managed team of 50..."
  │   ├─ 3. Quantifiable Outcomes
  │   │   ├─ $12.1M project value
  │   │   ├─ On-time, on-budget delivery
  │   │   └─ 50 staff members managed
  │   ├─ 4. Usage Recommendations
  │   │   ├─ Best for: Executive/leadership roles
  │   │   ├─ Resume bullet: Use variation a or b
  │   │   └─ Cover letter: Use as example of [theme]
  │   └─ 5. Related Achievements
  │       └─ Links to Ivy Substation renovation
  │
  └─ B. Outdoor Amphitheater (600-seat venue)
      └─ [same structure]

## II. Organizational Transformation
  ├─ A. Free-to-Earned Revenue Model
  ├─ B. Data Infrastructure Implementation
  └─ C. Strategic Planning Leadership

## III. Revenue Generation & Growth
  ├─ A. Gala Revenue Growth (50% increase)
  ├─ B. Earned Revenue Transition (20% YOY)
  └─ C. $1.4M Musical Production

## IV. Academic Leadership
  ├─ A. Advisor Crisis Resolution
  ├─ B. Enrollment Growth
  └─ C. Curriculum Database Creation
```

### 3. **Narrative Patterns & Story Structures**

```
# Narrative Patterns & Story Structures

## I. Cover Letter Architecture
  ├─ A. Opening Strategies
  │   ├─ 1. Institutional Positioning
  │   │   ├─ Pattern Template
  │   │   │   └─ "[Institution] is uniquely positioned..."
  │   │   ├─ Structure
  │   │   │   ├─ a. Acknowledge institutional strengths
  │   │   │   ├─ b. Connect to field challenges
  │   │   │   └─ c. Position as solution
  │   │   ├─ Examples
  │   │   │   ├─ CSUF example
  │   │   │   ├─ CSULB example
  │   │   │   └─ UCLA example
  │   │   └─ When to Use
  │   │       └─ Academic positions, mission-driven orgs
  │   │
  │   ├─ 2. Personal Connection Opening
  │   └─ 3. Challenge-Response Opening
  │
  ├─ B. Evidence Presentation Patterns
  │   ├─ 1. Challenge → Action → Result
  │   ├─ 2. Context → Insight → Application
  │   └─ 3. Problem → Solution → Outcome
  │
  ├─ C. Transition Strategies
  │   ├─ 1. Thematic bridging
  │   ├─ 2. Qualification pivots
  │   └─ 3. Vision connections
  │
  └─ D. Closing Strategies
      ├─ 1. Forward-looking invitation
      ├─ 2. Values reaffirmation
      └─ 3. Gratitude + eagerness

## II. Resume Bullet Formulas
  ├─ A. Action-Verb Patterns
  │   ├─ Strategic oversight: "Stewarded", "Oversaw", "Led"
  │   ├─ Creation/Building: "Conceived", "Designed", "Built"
  │   └─ Financial: "Generated", "Achieved", "Increased"
  │
  ├─ B. Impact Quantification
  │   ├─ Percentage growth: "X% increase in Y"
  │   ├─ Dollar amounts: "$X.XM in..."
  │   └─ Scale indicators: "X students/staff/stakeholders"
  │
  └─ C. Scope Communication
      ├─ Scale: "Across X programs/departments/units"
      ├─ Timeline: "Over X years..."
      └─ Complexity: "X-person team", "$XM budget"

## III. Thematic Storytelling
  ├─ A. Equity & Inclusion Narrative
  ├─ B. Innovation & Transformation Arc
  └─ C. Stewardship & Sustainability Theme
```

### 4. **Language Bank & Phrase Library**

```
# Language Bank & Phrase Library

## I. Action Verbs by Category
  ├─ A. Strategic Leadership
  │   ├─ 1. Vision & Planning
  │   │   ├─ Stewarded, Conceived, Envisioned
  │   │   ├─ Usage: Opening statements
  │   │   └─ Examples: [links to achievements]
  │   ├─ 2. Execution & Delivery
  │   └─ 3. Change Management
  │
  ├─ B. Financial Management
  ├─ C. Stakeholder Engagement
  └─ D. Program Development

## II. Impact Phrases
  ├─ A. Scale & Scope
  │   ├─ 1. Financial Impact
  │   │   └─ "$X.XM", "X% increase", "X% year-over-year"
  │   ├─ 2. People Impact
  │   │   └─ "X students", "X-person team", "X stakeholders"
  │   └─ 3. Reach & Duration
  │       └─ "Over X years", "Across X programs"
  │
  ├─ B. Transformation Language
  └─ C. Collaboration Indicators

## III. Industry-Specific Language
  ├─ A. Academic/Higher Ed
  │   ├─ Curriculum, pedagogy, scholarship
  │   ├─ Student success, retention, recruitment
  │   └─ EDIAB, inclusive excellence, access
  │
  ├─ B. Nonprofit/Arts
  │   ├─ Mission-driven, stakeholder engagement
  │   ├─ Community partnerships, public service
  │   └─ Artistic excellence, creative practice
  │
  └─ C. Management/Operations
      ├─ Strategic planning, fiscal stewardship
      ├─ Data-driven, evidence-based
      └─ Operational efficiency, resource allocation

## IV. Powerful Phrase Templates
  ├─ A. Leadership Philosophy
  │   └─ "I believe [role] should be..."
  ├─ B. Institutional Positioning
  │   └─ "[Institution] is uniquely positioned by..."
  └─ C. Challenge Framing
      └─ "Our moment demands..."
```

---

## Technical Implementation

### Architecture

```
Input: Career Documents
    ↓
Document Processor (existing)
    ↓
Claude API Analysis (NEW)
    ↓
Structured JSON Output
    ↓
Hierarchical Markdown Generator (NEW)
    ↓
Four Reference Guides
```

### File Structure

```
analyzers/
├── llm_analyzer.py           # NEW: Claude API integration
└── llm_prompt_templates.py   # NEW: Analysis prompts

generators/
├── hierarchical_generator.py # NEW: Creates hierarchical markdown
└── templates/
    ├── philosophy_template.md
    ├── achievements_template.md
    ├── narratives_template.md
    └── language_bank_template.md

outputs/
├── 01_career_philosophy.md   # Hierarchical output
├── 02_achievement_library.md
├── 03_narrative_patterns.md
└── 04_language_bank.md
```

---

## Output Features

### 1. **Navigation**

Each file includes:
- **Table of Contents** with anchor links
- **Cross-references** between sections
- **Search tags** for quick finding

### 2. **Usage Guidance**

Every item includes:
- **When to use** (what types of positions)
- **How to use** (resume vs cover letter vs interview)
- **Emphasis** (what aspect this highlights)

### 3. **Examples**

- Multiple real examples from your documents
- Side-by-side variations showing different framings
- Context showing how it fits into larger narrative

### 4. **Metadata**

- **Confidence score** (how often this appears)
- **Time range** (when you've used this)
- **Context** (what roles/sectors)

---

## Sample Output: Achievement Entry

```markdown
# Achievement Library

## I. Capital Projects & Infrastructure

### A. Kirk Douglas Theater Adaptive Reuse

#### 1. Overview

**Project**: Led complete adaptive reuse of historic building into 317-seat professional theater

**Scale**:
- Budget: $12.1M
- Timeline: Conception through delivery (1997-2004)
- Team: 50 full- and part-time staff

**Context**: While serving as Associate Producer at Center Theatre Group, stewarded
public-private partnership with City of Culver City

---

#### 2. Variations by Emphasis

##### a. Project Management Focus
> **Use for**: PM roles, operations positions, organizational leadership

"Stewarded $12.1M adaptive reuse project from conceptual sketch through on-time,
on-budget delivery, managing all phases including budgeting, architect selection,
regulatory approvals, construction oversight, and operational launch."

**Highlights**: Process management, timeline adherence, stakeholder coordination

---

##### b. Financial Stewardship Focus
> **Use for**: CFO/finance roles, budget-conscious positions, fiscal leadership

"Delivered on-time, on-budget completion of $12.1M capital project, negotiating
Disposition and Development Agreement with municipality and managing complex
public-private partnership financing."

**Highlights**: Fiscal responsibility, budget management, financial structuring

---

##### c. Stakeholder Management Focus
> **Use for**: Executive director, public sector, community engagement roles

"Negotiated multi-party Disposition and Development Agreement between nonprofit,
municipality, and redevelopment agency for $12.1M public-private partnership
adaptive reuse project."

**Highlights**: Relationship building, public partnership, consensus building

---

##### d. Team Leadership Focus
> **Use for**: People management, organizational development, HR-adjacent roles

"Built and managed cross-functional team of 50 full- and part-time employees for
$12.1M theater development project, designing operational model and launching
inaugural season."

**Highlights**: Team building, organizational design, staff development

---

#### 3. Quantifiable Outcomes

- **$12.1M** project value
- **On-time, on-budget** delivery (emphasize reliability)
- **50 staff** hired and managed
- **317-seat** venue capacity
- **5 world premieres** in inaugural season
- **7-year** project span (1997-2004)

---

#### 4. Usage Recommendations

**Resume**:
- Use variation **a** or **b** for single bullet
- Can split into 2-3 bullets for depth:
  - Bullet 1: Overall stewardship (variation a)
  - Bullet 2: Specific achievement (negotiations, team building)
  - Bullet 3: Outcome (inaugural season success)

**Cover Letter**:
- Use as **major achievement example** when demonstrating:
  - Project management capabilities
  - Long-term commitment and follow-through
  - Public-private partnership experience
  - Building something from nothing
- Pair with **listening-first leadership** theme
- Connect to **institutional stewardship** value

**Interview**:
- **Opening**: "Tell me about a complex project you've led"
- **Follow-up**: Drill into specific challenges (regulatory, stakeholder, budget)
- **STAR format**:
  - Situation: Historic theater, public-private partnership
  - Task: Conception to delivery
  - Action: [pick relevant variation]
  - Result: On-time, on-budget, inaugural season success

---

#### 5. Related Achievements

- **Ivy Substation Renovation** ($450K) - Similar but smaller scale
- **Outdoor Amphitheater** (600-seat) - Venue creation from scratch
- **Inaugural Season Production** - Follow-through to operations

---

#### 6. Keywords & Tags

`capital-projects` `facilities` `adaptive-reuse` `public-private-partnership`
`project-management` `budget-management` `stakeholder-engagement`
`team-building` `theater` `infrastructure`

---
```

---

## Benefits of This Approach

### 1. **Actionable**
Every entry tells you WHEN and HOW to use it

### 2. **Hierarchical**
Easy to navigate, find what you need quickly

### 3. **Flexible**
Multiple ways to frame same achievement based on role

### 4. **Contextual**
Understands meta-level themes, not just literal text

### 5. **Comprehensive**
Cross-references connect related concepts

---

## Implementation Plan

### Phase 1: Core LLM Analyzer
1. Create Claude API client
2. Design prompts for each lexicon type
3. Test with sample documents
4. Refine prompts based on output quality

### Phase 2: Hierarchical Generator
1. Create markdown template system
2. Build TOC auto-generation
3. Add cross-referencing system
4. Implement search tags

### Phase 3: Integration
1. Replace existing analyzers with LLM calls
2. Update orchestrator to use new generators
3. Add configuration for API key management
4. Test full pipeline

### Phase 4: Enhancement
1. Add interactive navigation (HTML export?)
2. Create "quick find" index
3. Add job description matcher
4. Build cover letter template generator

---

## Cost Estimation

**Claude API Pricing** (Sonnet 3.5):
- Input: $3 per million tokens
- Output: $15 per million tokens

**Estimated Cost per Analysis**:
- Assuming ~50 documents × 2,000 words = 100,000 words
- ~133,000 tokens input
- ~50,000 tokens output (4 detailed lexicons)

**Total**: ~$1.15 per complete analysis

**Annual cost** (running monthly): ~$14/year

---

## Next Steps

1. ✅ Design hierarchical structure (this document)
2. Create Claude API analyzer
3. Build hierarchical markdown generator
4. Test with sample documents
5. Refine prompts and structure
6. Deploy full system

---

## Appendix: Example Claude Prompts

### Prompt 1: Career Philosophy Analysis

```
You are analyzing career documents to extract high-level leadership philosophy
and values for a reference guide.

DOCUMENTS:
[document text]

Create a hierarchical analysis with this structure:

# Career Philosophy & Values

## I. Leadership Approach
For each leadership theme:
- Theme name and core principle
- Evidence (2-3 strong quotes)
- When to emphasize this theme
- How to phrase it for different contexts
- Related values/themes

## II. Core Values
For each value:
- Value name and definition
- Evidence from documents
- How this differentiates the candidate
- Application examples

## III. Problem-Solving Philosophy
[similar structure]

IMPORTANT:
- Extract META-LEVEL themes, not literal phrases
- Focus on ACTIONABLE guidance
- Provide SPECIFIC usage recommendations
- Include CROSS-REFERENCES between themes

Output as hierarchical markdown with clear navigation.
```

---

**END OF DESIGN DOCUMENT**
