#!/usr/bin/env python3
"""
Run split narrative pattern analysis to avoid token limits.
Generates 3 separate comprehensive lexicons.
"""

import sys
import os
from pathlib import Path
from anthropic import Anthropic

sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import process_documents
from core.state_manager import ProcessingManifest
from datetime import datetime
import json

# Import the split prompts
from analyzers.narrative_split_prompts import (
    COVER_LETTER_ARCHITECTURE_PROMPT,
    EVIDENCE_PRESENTATION_PROMPT,
    RESUME_BULLET_PROMPT
)

def format_documents(documents):
    """Format documents for analysis."""
    formatted = []
    for doc in documents:
        doc_type = doc.get('doc_type', 'unknown')
        if hasattr(doc_type, 'value'):
            doc_type = doc_type.value
        date = doc.get('date', 'unknown')
        content = doc.get('content', '')
        formatted.append(f"=== {doc_type} | {date} ===\n{content}\n")
    return "\n".join(formatted)

def run_analysis(client, prompt_template, documents_text, analysis_name):
    """Run a single narrative analysis."""
    print(f"\n  Analyzing {analysis_name}...")
    
    prompt = prompt_template.format(documents=documents_text)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16384,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result_text = response.content[0].text
    
    # Parse JSON
    try:
        result_json = json.loads(result_text)
        print(f"  ✓ {analysis_name} complete")
        return result_json
    except json.JSONDecodeError as e:
        print(f"  ! Warning: JSON parsing issue for {analysis_name}")
        print(f"    Error: {e}")
        return {"raw_text": result_text}

def generate_markdown(data, output_path, title, data_key):
    """Generate markdown from analysis results."""
    
    lines = [
        f"# {title}",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        ""
    ]
    
    patterns = data.get(data_key, [])
    
    for i, pattern in enumerate(patterns, 1):
        # Pattern heading
        name = pattern.get('pattern_name', pattern.get('formula_name', f'Pattern {i}'))
        lines.append(f"## {i}. {name}")
        lines.append("")
        
        # Pattern type or tier
        if 'pattern_type' in pattern:
            lines.append(f"**Type**: {pattern['pattern_type']}")
            lines.append("")
        
        # Template (for formulas)
        if 'template' in pattern:
            lines.append(f"**Template**: `{pattern['template']}`")
            lines.append("")
        
        # Structure
        if 'structure' in pattern:
            lines.append("### Structure")
            lines.append("")
            for step in pattern['structure']:
                if 'step' in step:
                    lines.append(f"{step['step']}. **{step.get('element', 'Step')}**")
                elif 'component' in step:
                    lines.append(f"- **{step['component']}**: {step.get('when_to_use', '')}")
                elif 'element' in step:
                    lines.append(f"- **{step['element']}**: {step.get('description', '')}")
                    if 'example' in step:
                        lines.append(f"  - Example: *{step['example']}*")
            lines.append("")
        
        # When to use
        if 'when_to_use' in pattern:
            lines.append(f"**When to use**: {pattern['when_to_use']}")
            lines.append("")
        
        # Effectiveness
        if 'effectiveness' in pattern:
            lines.append(f"**Why it works**: {pattern['effectiveness']}")
            lines.append("")
        
        # Examples
        if 'full_examples' in pattern or 'examples' in pattern:
            lines.append("### Examples")
            lines.append("")
            examples = pattern.get('full_examples', pattern.get('examples', []))
            for ex in examples[:3]:  # Limit to 3 examples per pattern
                if 'source' in ex:
                    lines.append(f"**From**: {ex['source']}")
                if 'bullet_text' in ex:
                    lines.append(f"> {ex['bullet_text']}")
                elif 'complete_example' in ex:
                    lines.append(f"> {ex['complete_example']}")
                elif 'opening_paragraph' in ex:
                    lines.append(f"> {ex['opening_paragraph']}")
                lines.append("")
        
        # Variations
        if 'variations' in pattern:
            lines.append("### Variations")
            lines.append("")
            for var in pattern['variations']:
                variant_name = var.get('variant_name', 'Variation')
                lines.append(f"**{variant_name}**: {var.get('adjustment', '')}")
                lines.append("")
        
        # Keywords
        if 'keywords' in pattern:
            keywords_str = ", ".join(pattern['keywords'])
            lines.append(f"**Keywords**: {keywords_str}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Write file
    content = "\n".join(lines)
    with open(output_path, 'w') as f:
        f.write(content)
    
    return output_path

def main():
    input_dir = "my_documents/converted"
    output_dir = "lexicons_llm"
    
    print("=" * 70)
    print("Split Narrative Pattern Analysis (3 Comprehensive Lexicons)")
    print("=" * 70)
    print()
    
    # Step 1: Process documents
    print("Step 1: Processing documents...")
    manifest = ProcessingManifest(
        last_updated=datetime.now().isoformat(),
        documents={},
        version="1.0"
    )
    documents = process_documents(input_dir, manifest)
    print(f"  ✓ Processed {len(documents)} documents")
    
    documents_text = format_documents(documents)
    
    # Step 2: Run 3 separate analyses
    print("\nStep 2: Running 3 comprehensive analyses...")
    print("  (This will take 2-3 minutes total...)")
    
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    cover_letter_result = run_analysis(
        client, 
        COVER_LETTER_ARCHITECTURE_PROMPT,
        documents_text,
        "Cover Letter Architecture"
    )
    
    evidence_result = run_analysis(
        client,
        EVIDENCE_PRESENTATION_PROMPT,
        documents_text,
        "Evidence Presentation Patterns"
    )
    
    resume_result = run_analysis(
        client,
        RESUME_BULLET_PROMPT,
        documents_text,
        "Resume Bullet Formulas"
    )
    
    # Step 3: Generate markdown files
    print("\nStep 3: Generating markdown files...")
    os.makedirs(output_dir, exist_ok=True)
    
    path1 = generate_markdown(
        cover_letter_result,
        os.path.join(output_dir, '03a_cover_letter_patterns.md'),
        "Cover Letter Architecture Patterns",
        "cover_letter_patterns"
    )
    print(f"  ✓ Generated {path1}")
    
    path2 = generate_markdown(
        evidence_result,
        os.path.join(output_dir, '03b_evidence_patterns.md'),
        "Evidence Presentation Patterns",
        "evidence_patterns"
    )
    print(f"  ✓ Generated {path2}")
    
    path3 = generate_markdown(
        resume_result,
        os.path.join(output_dir, '03c_resume_formulas.md'),
        "Resume Bullet Formulas",
        "resume_formulas"
    )
    print(f"  ✓ Generated {path3}")
    
    # Step 4: Count patterns
    print()
    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print()
    print("Pattern counts:")
    print(f"  • Cover Letter Patterns: {len(cover_letter_result.get('cover_letter_patterns', []))}")
    print(f"  • Evidence Patterns: {len(evidence_result.get('evidence_patterns', []))}")
    print(f"  • Resume Formulas: {len(resume_result.get('resume_formulas', []))}")
    print(f"  • TOTAL: {len(cover_letter_result.get('cover_letter_patterns', [])) + len(evidence_result.get('evidence_patterns', [])) + len(resume_result.get('resume_formulas', []))}")
    print()
    print("Generated files:")
    print(f"  • {path1}")
    print(f"  • {path2}")
    print(f"  • {path3}")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
