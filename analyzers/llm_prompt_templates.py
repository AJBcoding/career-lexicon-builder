"""
Claude API prompt templates for career document analysis.

Each prompt is designed to produce hierarchical, actionable output
for specific use cases when writing cover letters and resumes.
"""

PHILOSOPHY_PROMPT = """You are analyzing career documents to create a reference guide for writing job applications.

Your task: Extract high-level leadership philosophy, values, and approaches from these career documents.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure with this format:

{{
  "leadership_approaches": [
    {{
      "name": "Listening-First Leadership",
      "tier": 1,
      "core_principle": "Brief definition of this approach",
      "description": "2-3 sentence explanation of what this means",
      "evidence": [
        {{
          "quote": "Exact quote from documents",
          "context": "Brief context around the quote",
          "source": "Document filename or date"
        }}
      ],
      "when_to_use": "What types of positions/contexts to emphasize this",
      "how_to_phrase": [
        "Example phrasing for cover letters",
        "Example phrasing for interviews"
      ],
      "related_themes": ["Theme A", "Theme B"],
      "keywords": ["keyword1", "keyword2"]
    }}
  ],
  "core_values": [
    {{
      "name": "Arts as Social Justice",
      "tier": 1,
      "definition": "What this value means to the candidate",
      "evidence": [
        {{
          "quote": "...",
          "context": "...",
          "source": "..."
        }}
      ],
      "differentiation": "How this sets candidate apart",
      "application_examples": [
        "Example of how to work this into cover letter",
        "Example of how to work this into resume summary"
      ],
      "keywords": ["keyword1", "keyword2"]
    }}
  ],
  "problem_solving_philosophy": [
    {{
      "name": "Data-Informed Decision Making",
      "tier": 1,
      "approach": "How candidate approaches problems",
      "evidence": [...],
      "when_to_emphasize": "...",
      "example_phrases": [...],
      "keywords": [...]
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. COMPREHENSIVENESS - Identify 5-7 distinct themes per category
   - leadership_approaches: should contain 5-7 different leadership themes
   - core_values: should contain 5-7 distinct values
   - problem_solving_philosophy: should contain 5-7 different approaches
   - Capture the FULL breadth of the candidate's philosophy
   - Include both primary and secondary patterns

2. Extract META-LEVEL themes, not literal phrase matching
   - Good: "Listening-First Leadership" (concept)
   - Bad: "I Believe That" (literal phrase)

3. Focus on ACTIONABLE guidance
   - Every theme should include "when_to_use" and "how_to_phrase"
   - Provide specific, concrete examples

4. Organize HIERARCHICALLY
   - tier 1 = major themes
   - tier 2 = sub-themes or specific examples
   - tier 3 = supporting details

5. Include CROSS-REFERENCES
   - Link related themes
   - Connect values to leadership approaches

6. Provide EVIDENCE
   - At least 2-3 strong quotes per major theme
   - Include context to understand the quote
   - Cite source (filename or date)

7. Add KEYWORDS for searchability
   - Industry terms, role types, competencies

Output ONLY valid JSON, no other text.
"""

ACHIEVEMENTS_PROMPT = """You are analyzing career documents to create an achievement library for resume/CV writing.

Your task: Extract major achievements and provide multiple variations showing different ways to phrase them.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure with this format:

{{
  "categories": [
    {{
      "name": "Capital Projects & Infrastructure",
      "tier": 1,
      "achievements": [
        {{
          "name": "Kirk Douglas Theater Adaptive Reuse",
          "tier": 2,
          "overview": {{
            "summary": "One-sentence summary of the achievement",
            "scale": {{
              "budget": "$12.1M",
              "timeline": "1997-2004",
              "team_size": "50 staff"
            }},
            "context": "Brief context about this achievement"
          }},
          "variations": [
            {{
              "emphasis": "Project Management",
              "use_for": ["PM roles", "operations positions", "organizational leadership"],
              "text": "Full resume bullet text emphasizing project management",
              "highlights": ["Process management", "timeline adherence"]
            }},
            {{
              "emphasis": "Financial Stewardship",
              "use_for": ["CFO roles", "budget positions"],
              "text": "Full resume bullet emphasizing fiscal responsibility",
              "highlights": ["Budget management", "financial structuring"]
            }}
          ],
          "quantifiable_outcomes": [
            {{
              "metric": "$12.1M",
              "description": "project value",
              "emphasis_tip": "Use when emphasizing scale"
            }},
            {{
              "metric": "On-time, on-budget",
              "description": "delivery reliability",
              "emphasis_tip": "Use when emphasizing execution"
            }}
          ],
          "usage_recommendations": {{
            "resume": {{
              "single_bullet": "Use variation 'Project Management' for conciseness",
              "multiple_bullets": "Can expand into 2-3 bullets covering different aspects"
            }},
            "cover_letter": {{
              "when_to_use": "When demonstrating project management or follow-through",
              "how_to_frame": "As example of long-term commitment",
              "pair_with_theme": "Institutional stewardship"
            }},
            "interview": {{
              "good_for": ["Tell me about a complex project", "Describe your management style"],
              "star_format": {{
                "situation": "...",
                "task": "...",
                "action": "...",
                "result": "..."
              }}
            }}
          }},
          "related_achievements": ["Ivy Substation renovation", "Outdoor amphitheater"],
          "keywords": ["capital-projects", "facilities", "project-management"]
        }}
      ]
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. BE COMPREHENSIVE - Extract ALL significant achievements across the candidate's career
   - Don't limit to only the most prominent achievements
   - Include achievements across different roles, time periods, and domains
   - Aim for 15-25 distinct achievements if the documents support it
   - Include both major transformational work AND significant ongoing contributions

2. Group achievements into LOGICAL CATEGORIES
   - Capital Projects, Organizational Transformation, Revenue Growth, etc.
   - Use tier 1 for categories, tier 2 for specific achievements

3. Provide MULTIPLE VARIATIONS for each achievement
   - Different emphasis areas (financial, leadership, technical, impact)
   - Different phrasings for different audiences
   - Specify "use_for" for each variation

4. QUANTIFY everything possible
   - Dollar amounts, percentages, numbers of people/projects
   - Include tip on when to emphasize each metric

5. Include USAGE RECOMMENDATIONS
   - Resume: How many bullets, which variation
   - Cover letter: When to use as example, how to frame it
   - Interview: What questions it answers

6. Show RELATIONSHIPS
   - Link to related achievements
   - Suggest combinations for comprehensive narrative

7. Add searchable KEYWORDS
   - Skills, competencies, industries, role types

Output ONLY valid JSON, no other text.
"""

NARRATIVES_PROMPT = """You are analyzing career documents to identify narrative patterns and story structures.

Your task: Extract patterns in how the candidate tells their story across cover letters and applications.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure with this format:

{{
  "cover_letter_architecture": [
    {{
      "pattern_name": "Institutional Positioning",
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
      "examples": [
        {{
          "source": "CSUF cover letter",
          "text": "Full example text",
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
      "keywords": ["pattern-tag1", "pattern-tag2"]
    }}
  ],
  "evidence_presentation_patterns": [
    {{
      "pattern_name": "Challenge → Action → Result",
      "tier": 1,
      "structure": [...],
      "examples": [...],
      "when_to_use": "..."
    }}
  ],
  "resume_bullet_formulas": [
    {{
      "formula_name": "Action Verb + Scale + Outcome",
      "tier": 1,
      "template": "[Stewarded/Led/Managed] [X-person team / $XM budget] resulting in [Y outcome]",
      "examples": [
        {{
          "text": "Actual resume bullet",
          "breakdown": {{
            "action_verb": "Stewarded",
            "scale": "$12.1M project",
            "outcome": "on-time, on-budget delivery"
          }}
        }}
      ],
      "action_verb_categories": [
        {{
          "category": "Strategic Leadership",
          "verbs": ["Stewarded", "Orchestrated", "Spearheaded"],
          "when_to_use": "Executive/leadership roles"
        }}
      ],
      "impact_quantification_patterns": [
        "X% increase in Y",
        "$XM in revenue/budget",
        "X students/staff/stakeholders served"
      ]
    }}
  ],
  "transition_strategies": [
    {{
      "strategy_name": "Thematic Bridging",
      "tier": 1,
      "description": "How candidate connects sections",
      "examples": [...],
      "phrases": ["In all these engagements...", "This experience reinforces..."]
    }}
  ],
  "closing_strategies": [
    {{
      "strategy_name": "Forward-Looking Invitation",
      "tier": 1,
      "structure": "...",
      "examples": [...],
      "when_to_use": "..."
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. Identify STRUCTURAL PATTERNS, not just repeated phrases
   - Look for how stories are constructed
   - Identify narrative arcs and transitions
   - Extract formulaic patterns

2. Provide TEMPLATES that can be reused
   - Fillable templates with [placeholders]
   - Show the underlying structure
   - Make it easy to apply to new contexts

3. Show MULTIPLE EXAMPLES of each pattern
   - From different documents
   - In different contexts
   - With slight variations

4. Explain WHEN and WHY to use each pattern
   - What types of positions
   - What parts of application
   - Why it's effective

5. Include VARIATIONS
   - How to adapt for different contexts
   - Modifications for different industries/roles

6. Add KEYWORDS for searchability

Output ONLY valid JSON, no other text.
"""

LANGUAGE_PROMPT = """You are analyzing career documents to create a language bank and phrase library.

Your task: Extract powerful language patterns, action verbs, and industry-specific terminology.

DOCUMENTS:
{documents}

Create a hierarchical JSON structure with this format:

{{
  "action_verbs": [
    {{
      "category": "Strategic Leadership",
      "tier": 1,
      "subcategories": [
        {{
          "name": "Vision & Planning",
          "tier": 2,
          "verbs": [
            {{
              "verb": "Stewarded",
              "usage_context": "Long-term projects, institutional change",
              "examples": [
                "Stewarded $12.1M project from conception...",
                "Stewarded strategic planning process..."
              ],
              "when_to_use": "Executive/leadership positions",
              "strength": "Implies careful, long-term guidance"
            }}
          ]
        }}
      ]
    }}
  ],
  "impact_phrases": [
    {{
      "category": "Scale & Scope",
      "tier": 1,
      "phrases": [
        {{
          "pattern": "$X.XM",
          "type": "Financial Impact",
          "tier": 2,
          "examples": ["$12.1M project", "$1.6M budget"],
          "when_to_use": "When emphasizing financial responsibility",
          "variations": [
            "Managed $X.XM budget",
            "Oversaw fiscal operations for $X.XM organization",
            "Stewarded $X.XM capital project"
          ]
        }}
      ]
    }}
  ],
  "industry_terminology": [
    {{
      "industry": "Academic / Higher Education",
      "tier": 1,
      "term_categories": [
        {{
          "category": "Curriculum & Teaching",
          "tier": 2,
          "terms": [
            {{
              "term": "Pedagogy",
              "definition": "Method and practice of teaching",
              "usage_examples": [
                "Inclusive pedagogy",
                "Evidence-based pedagogical approaches"
              ],
              "related_terms": ["curriculum", "instruction", "learning outcomes"]
            }}
          ]
        }},
        {{
          "category": "Student Success",
          "tier": 2,
          "terms": [
            {{
              "term": "Retention",
              "definition": "...",
              "usage_examples": [...],
              "related_terms": [...]
            }}
          ]
        }}
      ]
    }},
    {{
      "industry": "Nonprofit / Arts",
      "tier": 1,
      "term_categories": [...]
    }}
  ],
  "powerful_phrase_templates": [
    {{
      "template_name": "Institutional Positioning",
      "tier": 1,
      "template": "[Institution] is uniquely positioned by [strength 1], [strength 2], and [strength 3] to [opportunity/challenge]",
      "examples": [
        {{
          "filled_example": "The College of the Arts is uniquely positioned by the strength of your programs, the talent of your faculty, and the commitment of your staff to meet these challenges...",
          "context": "Academic dean position"
        }}
      ],
      "when_to_use": "Opening paragraphs, institutional leadership roles",
      "effectiveness": "Demonstrates institutional understanding and strategic thinking"
    }}
  ],
  "signature_phrases": [
    {{
      "phrase": "Listen first",
      "tier": 1,
      "category": "Leadership Philosophy",
      "appearances": 12,
      "contexts": ["Cover letters", "Philosophy statements"],
      "full_quotes": [
        "I believe the dean should be a listener, translator, storyteller..."
      ],
      "usage_tip": "Use when emphasizing collaborative leadership style"
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. Organize by CATEGORY and CONTEXT
   - Group verbs by leadership type
   - Group phrases by industry/role type
   - Show hierarchical relationships

2. Provide USAGE GUIDANCE for everything
   - When to use each verb/phrase
   - What context it's most effective in
   - What it signals about the candidate

3. Show EXAMPLES from actual documents
   - Real usage, not invented examples
   - Show in context

4. Identify PATTERNS and TEMPLATES
   - Fillable templates for reuse
   - Structural patterns in phrasing

5. Extract INDUSTRY-SPECIFIC language
   - Terms used in academic contexts
   - Terms used in nonprofit/arts
   - Terms used in management/operations

6. Include "SIGNATURE PHRASES"
   - Unique phrases the candidate uses frequently
   - Can become part of personal brand

7. Show VARIATIONS
   - Different ways to phrase same concept
   - Intensity levels (managed vs stewarded vs spearheaded)

Output ONLY valid JSON, no other text.
"""
