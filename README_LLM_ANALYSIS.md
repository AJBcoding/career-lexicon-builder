# LLM-Based Career Lexicon Analysis

**New approach using Claude API for interpretive analysis**

---

## What Changed?

The original system used semantic similarity to find patterns. While technically sophisticated, it produced outputs that were:
- Too literal (tracked phrases like "I believe" instead of actual values)
- Too granular (individual bullet points without meaningful grouping)
- Not actionable (no guidance on when/how to use the information)

**The new approach** uses Claude API to perform interpretive analysis, producing:
- **Meta-level themes** (e.g., "Listening-First Leadership" not "I believe that")
- **Hierarchical structure** (easy to navigate and find what you need)
- **Actionable guidance** (when to use, how to phrase, what it demonstrates)
- **Multiple variations** (different ways to frame the same achievement)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Claude API Key

1. Go to https://console.anthropic.com/
2. Create an account (or sign in)
3. Generate an API key
4. Set as environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or add to your shell profile (~/.zshrc or ~/.bashrc):

```bash
echo "export ANTHROPIC_API_KEY='your-api-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### 3. Run Analysis

```bash
python run_llm_analysis.py
```

**What happens**:
1. Reads all documents from `my_documents/`
2. Sends to Claude for analysis (~2-3 minutes)
3. Generates 4 hierarchical markdown files in `lexicons_llm/`

**Cost**: ~$1-2 per complete analysis

---

## Output Files

### `01_career_philosophy.md`
**Meta-level values and leadership approaches**

Structure:
```
I. Leadership Approaches
   A. Listening-First Leadership
      - Core principle
      - Evidence (quotes with context)
      - When to use
      - How to phrase
      - Related themes

II. Core Values
   A. Arts as Social Justice
      - Definition
      - Evidence
      - What this shows about you
      - How to apply

III. Problem-Solving Philosophy
   A. Data-Informed Decision Making
   ...
```

**Use this when**: Writing cover letter philosophy paragraphs, describing your leadership approach

---

### `02_achievement_library.md`
**Major achievements with multiple variations**

Structure:
```
A. Capital Projects & Infrastructure
   1. Kirk Douglas Theater
      - Overview (scale, context)
      - Variations by Emphasis:
        • Project Management Focus
          "Stewarded $12.1M adaptive reuse project..."
          Use for: PM roles, operations positions
        • Financial Stewardship Focus
          "Delivered on-time, on-budget completion..."
          Use for: CFO roles, budget positions
      - Quantifiable Outcomes
      - Usage Recommendations
        • Resume: Single bullet or 2-3 bullets?
        • Cover Letter: When to use as example
        • Interview: What questions it answers
```

**Use this when**: Writing resume bullets, selecting examples for cover letters

---

### `03_narrative_patterns.md`
**Story structures and narrative templates**

Structure:
```
I. Cover Letter Architecture
   A. Institutional Positioning Pattern
      - Structure:
        1. Acknowledge institutional strengths
        2. Connect to field challenges
        3. Position as uniquely equipped
      - Template with placeholders
      - Real examples from your letters
      - When to use

II. Evidence Presentation Patterns
   A. Challenge → Action → Result
   ...

III. Resume Bullet Formulas
   A. Action Verb + Scale + Outcome
   ...
```

**Use this when**: Structuring cover letter paragraphs, formatting resume bullets

---

### `04_language_bank.md`
**Action verbs, phrases, and terminology**

Structure:
```
I. Action Verbs by Category
   A. Strategic Leadership
      1. Vision & Planning
         - Stewarded
           • Context: Long-term projects
           • Examples: "Stewarded $12.1M project..."
           • Use for: Executive positions
           • Strength: Implies careful guidance

II. Impact Phrases
   A. Scale & Scope
      - "$X.XM" pattern
      - Variations:
        • "Managed $X.XM budget"
        • "Oversaw fiscal operations for $X.XM"

III. Industry Terminology
   A. Academic / Higher Education
      - Pedagogy, curriculum, student success...
   B. Nonprofit / Arts
      - Mission-driven, stakeholder engagement...

IV. Signature Phrases
   - "Listen first" (appears 12 times)
   - When to use, how it differentiates you
```

**Use this when**: Finding the right verb, checking terminology for specific industry

---

## How to Use

### Scenario 1: Writing a Cover Letter for Dean Position

1. **Open** `01_career_philosophy.md`
   - Find "Listening-First Leadership" under Leadership Approaches
   - Copy suggested phrasings

2. **Open** `02_achievement_library.md`
   - Navigate to "Academic Leadership" category
   - Find "Strategic Planning" achievement
   - Use "Leadership Focus" variation

3. **Open** `03_narrative_patterns.md`
   - Use "Institutional Positioning" opening pattern
   - Apply "Challenge → Action → Result" for evidence

4. **Open** `04_language_bank.md`
   - Check "Academic / Higher Education" terminology
   - Use "Strategic Leadership" action verbs

---

### Scenario 2: Tailoring Resume for CFO Role

1. **Open** `02_achievement_library.md`
   - Look for achievements with financial emphasis
   - Use "Financial Stewardship Focus" variations
   - Examples:
     - "Delivered on-time, on-budget completion of $12.1M project"
     - "Achieved 20% year-over-year revenue growth"

2. **Open** `04_language_bank.md`
   - Use "Financial Management" action verbs
   - Check "$X.XM" impact phrase patterns

---

### Scenario 3: Preparing for Interview

1. **Open** `02_achievement_library.md`
   - Each achievement has "Interview" section
   - Shows what questions it answers
   - Provides STAR format breakdown

2. **Open** `01_career_philosophy.md`
   - Review leadership approaches
   - Prepare to articulate your philosophy

---

## Features of Hierarchical Structure

### 1. Navigation
- Table of contents with anchor links
- Clear section numbering (I., A., 1., a.)
- Cross-references between related items

### 2. Multiple Levels
- **Level 1**: Major categories (Leadership Approaches, Core Values)
- **Level 2**: Specific themes (Listening-First Leadership)
- **Level 3**: Supporting details (Evidence, Examples, Usage)

### 3. Searchability
- Keywords tags on every item
- Consistent naming conventions
- Easy to CMD+F / CTRL+F

### 4. Actionable Guidance
Every entry tells you:
- **When to use** (what types of positions)
- **How to phrase** (specific examples)
- **What it shows** (what this demonstrates about you)

---

## Cost & Performance

**API Cost** (Claude 3.5 Sonnet):
- Input: $3 per million tokens
- Output: $15 per million tokens
- Typical analysis: ~$1-2 per full run

**Time**:
- Document processing: 10-30 seconds
- Claude analysis: 2-3 minutes
- Markdown generation: 5-10 seconds
- **Total**: ~3-4 minutes

**When to re-run**:
- When adding new career documents
- When refining prompts for better output
- After major career milestones

---

## Customizing the Analysis

### Modify Prompts

Edit `analyzers/llm_prompt_templates.py` to customize what gets extracted.

**Example**: Add more emphasis on specific skills

```python
ACHIEVEMENTS_PROMPT = """
...
IMPORTANT GUIDELINES:
1. Pay special attention to data analysis skills
2. Highlight Python/technical skills prominently
3. Emphasize quantitative outcomes
...
"""
```

### Adjust Output Format

Edit `generators/hierarchical_generator.py` to change markdown structure.

---

## Comparison: Old vs New

### Old System (Semantic Similarity)

```markdown
## I Believe That It Is

Confidence: 100% | First seen: 2023-01-27

### Occurrences

> "I believe that it is from this highly attuned position..."
```

**Issues**:
- Literal phrase matching
- No actionable guidance
- Flat structure

---

### New System (LLM Analysis)

```markdown
### A. Listening-First Leadership

**Core Principle**: Building constructive relationships requires deep
listening to stakeholders before taking action

#### Evidence
> "Listen closely to one's partners, one's constituents, one's audience..."
> Source: CSUF cover letter, 2023-01-27

#### When to Use
Best for: Academic positions, mission-driven organizations, collaborative
leadership roles

#### How to Phrase
- Cover letter: "My leadership approach begins with listening..."
- Interview: "I believe effective leadership starts with understanding..."
```

**Improvements**:
- Meta-level theme extraction
- Actionable guidance
- Hierarchical organization
- Context-specific recommendations

---

## Troubleshooting

### API Key Not Found

```
ERROR: ANTHROPIC_API_KEY environment variable not set
```

**Solution**: Set the environment variable

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Cost Concerns

**Worried about API costs?**

- Each full analysis costs ~$1-2
- You only need to run it when documents change
- Can test with a few documents first

To analyze fewer documents:
1. Move some documents out of `my_documents/` temporarily
2. Run analysis
3. Move them back

### Output Quality

**If output isn't what you expected:**

1. **Check the prompts** in `analyzers/llm_prompt_templates.py`
2. **Modify guidelines** to emphasize what you want
3. **Re-run** analysis

**Example adjustment**:
```python
# In PHILOSOPHY_PROMPT
IMPORTANT GUIDELINES:
1. Focus heavily on leadership philosophy
2. Extract at least 5 major leadership themes
3. Provide extensive evidence for each
```

---

## Next Steps

1. **Run the analysis** on your documents
2. **Review the output** - are the themes accurate?
3. **Try using it** - write a cover letter using the guides
4. **Refine prompts** if needed
5. **Re-run** analysis with improvements

---

## Files Created by This System

```
lexicons_llm/
├── 01_career_philosophy.md       # Values, leadership, philosophy
├── 02_achievement_library.md     # Achievements with variations
├── 03_narrative_patterns.md      # Story structures and templates
└── 04_language_bank.md           # Verbs, phrases, terminology
```

---

## Questions?

**How is this different from the old system?**
- Old: Pattern matching (finds similar text)
- New: Interpretation (understands meaning and provides guidance)

**Why use Claude instead of local models?**
- Higher quality interpretation
- Better at following complex instructions
- More consistent output format

**Can I use this with job descriptions?**
- Yes! You can add a job description analyzer
- Compare job requirements to your lexicons
- Suggest which achievements to emphasize

**Can I export to other formats?**
- Currently: Markdown
- Future: HTML, PDF, JSON, or structured database

---

**Happy analyzing!**
