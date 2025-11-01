"""
Split prompts for narrative pattern analysis to avoid token limits.
"""

COVER_LETTER_ARCHITECTURE_PROMPT = """You are analyzing career documents to identify cover letter architectural patterns.

Your task: Extract comprehensive patterns in how the candidate structures cover letters.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure focusing ONLY on cover letter architecture:

{{
  "cover_letter_patterns": [
    {{
      "pattern_name": "Institutional Positioning Opening",
      "tier": 1,
      "pattern_type": "Opening Strategy",
      "structure": [
        {{
          "step": 1,
          "element": "Acknowledge institutional strengths",
          "example": "Actual example from documents"
        }},
        {{
          "step": 2,
          "element": "Connect to field challenges",
          "example": "..."
        }}
      ],
      "template": "Fillable template showing the pattern structure",
      "full_examples": [
        {{
          "source": "Document name",
          "opening_paragraph": "Full text of opening",
          "context": "What role/institution"
        }}
      ],
      "when_to_use": "Academic positions, mission-driven organizations",
      "effectiveness": "Why this pattern works",
      "variations": [
        {{
          "variant_name": "For public universities",
          "adjustment": "How to modify for this context"
        }}
      ],
      "keywords": ["institutional", "positioning"]
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. BE COMPREHENSIVE - Extract ALL distinct cover letter architectural patterns
   - Opening strategies (how letters begin)
   - Closing strategies (how letters end)
   - Transitional patterns (how sections connect)
   - Thematic organization patterns
   - Aim for 15-25 distinct patterns

2. Provide FULL EXAMPLES from actual documents
   - Include complete paragraph examples, not just fragments
   - Show the pattern in action

3. Create FILLABLE TEMPLATES
   - Make templates practical and reusable
   - Use [brackets] for fill-in sections

4. Show VARIATIONS by context
   - Academic vs corporate
   - Leadership vs individual contributor
   - Different career stages

Output ONLY valid JSON, no other text.
"""

EVIDENCE_PRESENTATION_PROMPT = """You are analyzing career documents to identify evidence presentation patterns.

Your task: Extract comprehensive patterns in how the candidate presents accomplishments and evidence.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure focusing ONLY on evidence presentation:

{{
  "evidence_patterns": [
    {{
      "pattern_name": "Challenge → Systems → Scale → Result",
      "tier": 1,
      "structure": [
        {{
          "element": "Challenge identification",
          "description": "How challenge is framed",
          "example": "..."
        }},
        {{
          "element": "Systems created",
          "description": "Infrastructure built",
          "example": "..."
        }},
        {{
          "element": "Scale demonstrated",
          "description": "Scope/size shown",
          "example": "..."
        }},
        {{
          "element": "Quantified result",
          "description": "Measurable outcome",
          "example": "..."
        }}
      ],
      "full_examples": [
        {{
          "source": "Document name",
          "complete_example": "Full paragraph showing pattern",
          "breakdown": "Analysis of each element"
        }}
      ],
      "when_to_use": "Complex project descriptions, infrastructure work",
      "effectiveness": "Why this sequencing works",
      "quantification_patterns": [
        "$X million budget",
        "X% increase",
        "X-person team"
      ],
      "keywords": ["systems", "scale", "infrastructure"]
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. BE COMPREHENSIVE - Extract ALL distinct evidence presentation patterns
   - STAR patterns (Situation, Task, Action, Result)
   - CAR patterns (Challenge, Action, Result)  
   - Systems-first patterns
   - Impact-first patterns
   - Collaborative patterns
   - Aim for 15-25 distinct patterns

2. Show QUANTIFICATION strategies
   - Dollar amounts
   - Percentages
   - Team sizes
   - Timelines
   - Scope metrics

3. Include COMPLETE EXAMPLES
   - Full paragraphs showing the pattern
   - Annotated breakdowns

Output ONLY valid JSON, no other text.
"""

RESUME_BULLET_PROMPT = """You are analyzing career documents to identify resume bullet formulas and structures.

Your task: Extract comprehensive patterns in how accomplishments are condensed into resume bullets.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure focusing ONLY on resume bullet formulas:

{{
  "resume_formulas": [
    {{
      "formula_name": "Action Verb + Scale + Infrastructure + Outcome",
      "tier": 1,
      "template": "[Action Verb] [scale/scope] [what was built/changed] resulting in/achieving [quantified outcome]",
      "structure": [
        {{
          "component": "Action Verb",
          "options": ["Stewarded", "Orchestrated", "Led"],
          "when_to_use": "Executive/strategic emphasis"
        }},
        {{
          "component": "Scale",
          "options": ["$XM budget", "X-person team", "X-year timeline"],
          "when_to_use": "Show scope and responsibility"
        }},
        {{
          "component": "Infrastructure",
          "options": ["capital project", "organizational system", "program"],
          "when_to_use": "Emphasize building/creating"
        }},
        {{
          "component": "Outcome",
          "options": ["on-time delivery", "X% increase", "award/recognition"],
          "when_to_use": "Measurable results"
        }}
      ],
      "examples": [
        {{
          "bullet_text": "Complete resume bullet from documents",
          "breakdown": {{
            "action_verb": "Which verb used",
            "scale": "What scale shown",
            "infrastructure": "What was built",
            "outcome": "What result achieved"
          }},
          "source": "Document name"
        }}
      ],
      "action_verb_categories": [
        {{
          "category": "Strategic Leadership",
          "verbs": ["Stewarded", "Orchestrated", "Spearheaded"],
          "when_to_use": "Executive/leadership roles",
          "tone": "Authoritative but collaborative"
        }}
      ],
      "length_guidelines": {{
        "ideal_length": "1-2 lines",
        "max_length": "3 lines",
        "conciseness_tips": "How to condense without losing impact"
      }},
      "keywords": ["action-verbs", "quantification"]
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. BE COMPREHENSIVE - Extract ALL distinct resume bullet formulas
   - Different emphasis patterns (financial, leadership, technical, impact)
   - Different role types (executive, manager, individual contributor)
   - Different industries
   - Aim for 15-20 distinct formulas

2. Categorize ACTION VERBS comprehensively
   - Strategic leadership verbs
   - Financial management verbs
   - Team building verbs
   - Innovation verbs
   - Create 6-8 categories with 5-10 verbs each

3. Show QUANTIFICATION patterns
   - Financial metrics
   - Percentage improvements
   - Team/org sizes
   - Timeline achievements
   - Provide specific examples of each type

4. Include LENGTH guidance
   - Optimal length for different contexts
   - How to condense without losing impact

Output ONLY valid JSON, no other text.
"""
