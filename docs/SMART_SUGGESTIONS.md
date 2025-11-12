# Smart Suggestions System

## Overview
AI-powered recommendations for workflow optimization that guide users through the job application process with intelligent next-step suggestions and document quality analysis.

## Features

### Next Steps Recommendations
- **Rule-Based Engine**: Fast, deterministic suggestions based on project state
- **AI-Powered Analysis**: Context-aware, intelligent recommendations using Claude
- **Priority Ranking**: Suggestions ranked by importance and impact
- **Action Integration**: One-click execution of suggested actions

### Document Quality Analysis
- **Quality Scoring**: 1-10 scale assessment of document quality
- **Strengths Identification**: Highlights what's working well
- **Improvement Areas**: Specific weaknesses to address
- **Actionable Items**: Concrete steps for enhancement

## Suggestion Types

### Critical (Red Border)
Must-do items that block progress. Example:
- Upload Job Description (when starting a new project)

### Recommended (Blue Border)
Should-do items that follow the optimal workflow. Examples:
- Analyze Job Description (after upload)
- Align Resume (after job analysis)
- Draft Cover Letter (after resume alignment)

### Optional (Green Border)
Nice-to-have improvements and enhancements. Examples:
- ATS keyword optimization
- Document formatting improvements
- Strategic positioning opportunities

## How It Works

### Rule-Based Suggestions (Fast)
1. Check project state (uploaded files, completed analyses)
2. Match against workflow patterns
3. Return prioritized suggestions instantly
4. No API calls required

### AI-Powered Suggestions (Intelligent)
1. Analyze completed documents and project context
2. Use Claude to identify improvement opportunities
3. Generate context-aware recommendations
4. Cache results for performance

### Priority Scoring
- **Priority 1**: Critical path items (must complete)
- **Priority 2**: Important workflow steps
- **Priority 3**: Quality improvements
- **Priority 4-5**: Optional enhancements

## API Endpoints

### GET /api/suggestions/{project_id}/next-steps
Returns prioritized list of next-step suggestions.

**Response:**
```json
{
  "suggestions": [
    {
      "type": "critical",
      "title": "Upload Job Description",
      "description": "Start by uploading the job posting to analyze",
      "action": "upload_file",
      "priority": 1
    },
    {
      "type": "recommended",
      "title": "Analyze Job Description",
      "description": "Run job-description-analysis to understand requirements",
      "action": "run_skill:job-description-analysis",
      "priority": 1
    }
  ]
}
```

### POST /api/suggestions/{project_id}/analyze-document
Analyzes document quality and returns improvement suggestions.

**Request:**
```json
{
  "document_type": "resume",
  "filename": "resume-aligned.md"
}
```

**Response:**
```json
{
  "quality_score": 8,
  "strengths": [
    "Clear structure with strong action verbs",
    "Quantified achievements throughout",
    "Tailored to job requirements"
  ],
  "improvements": [
    "Add more industry-specific keywords",
    "Expand on leadership examples",
    "Strengthen summary section"
  ],
  "action_items": [
    "Add keywords: Python, machine learning, data pipeline",
    "Include team size in leadership bullets",
    "Rewrite summary with more impact"
  ]
}
```

## Frontend Integration

### SuggestionsPanel Component
```jsx
<SuggestionsPanel project={project} />
```

**Features:**
- Auto-loads suggestions on project change
- Visual priority indicators (colored borders)
- Click-to-execute actions
- Refresh button for manual reload
- Error handling and retry logic

**Styling:**
- Red left border: Critical items
- Blue left border: Recommended items
- Green left border: Optional items
- Hover effects for interactivity
- Clean, minimal design

### Action Handlers
- `run_skill:SKILL_NAME` - Triggers skill invocation
- `upload_file` - Focuses file upload component
- `review` - Prompts document review

## Workflow Integration

### Typical Workflow
1. **Upload** → Critical: "Upload Job Description"
2. **Analyze** → Recommended: "Analyze Job Description"
3. **Align** → Recommended: "Align Resume"
4. **Draft** → Recommended: "Draft Cover Letter"
5. **Improve** → Optional: AI-generated improvements
6. **Review** → Optional: "Review Documents"

### State Detection
The system detects project state by analyzing:
- Uploaded files count
- Filename patterns (job-analysis, resume, cover-letter)
- File content (for advanced analysis)
- Project metadata

## Performance Considerations

### Caching Strategy
- Rule-based suggestions: Instant (no caching needed)
- AI suggestions: Optional, only when documents exist
- Document analysis: On-demand only

### Token Usage
- Next steps: ~200-500 tokens per AI call
- Document analysis: ~500-1000 tokens per analysis
- Minimize calls by using rule-based logic first

## Future Enhancements

### Planned Features
- Real-time document scoring as you type
- Skill execution from suggestions panel
- Suggestion history and tracking
- A/B testing of suggestion effectiveness
- Machine learning for personalized suggestions

### Potential Integrations
- ATS keyword scanner integration
- Industry-specific suggestion templates
- Collaborative feedback from mentors
- Application deadline reminders
