#!/usr/bin/env python3
"""
Re-run just the Career Philosophy analysis with updated prompt.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import process_documents
from core.state_manager import ProcessingManifest
from analyzers.llm_analyzer import LLMAnalyzer
from generators.hierarchical_generator import HierarchicalMarkdownGenerator
from datetime import datetime

def main():
    input_dir = "my_documents/converted"
    output_dir = "lexicons_llm"
    
    print("=" * 70)
    print("Re-running Career Philosophy Analysis (5-7 themes per category)")
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
    print()
    
    # Step 2: Analyze philosophy only
    print("Step 2: Analyzing career philosophy with Claude Sonnet 4...")
    print("  (This may take 30-60 seconds...)")
    
    analyzer = LLMAnalyzer()
    formatted_docs = analyzer._format_documents(documents)
    
    philosophy_result = analyzer.analyze_philosophy(formatted_docs, documents)
    print("  ✓ Philosophy analysis complete")
    print()
    
    # Step 3: Generate markdown
    print("Step 3: Generating updated markdown...")
    generator = HierarchicalMarkdownGenerator()
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, '01_career_philosophy.md')
    output_path = generator.generate_philosophy(philosophy_result, output_file)
    print(f"  ✓ Generated {output_path}")
    print()
    
    # Count themes
    import json
    if isinstance(philosophy_result, str):
        try:
            data = json.loads(philosophy_result)
        except:
            data = philosophy_result
    else:
        data = philosophy_result
        
    if isinstance(data, dict):
        leadership_count = len(data.get('leadership_approaches', []))
        values_count = len(data.get('core_values', []))
        problem_solving_count = len(data.get('problem_solving_philosophy', []))
        
        print("=" * 70)
        print("Analysis Complete!")
        print("=" * 70)
        print()
        print(f"Theme counts:")
        print(f"  • Leadership Approaches: {leadership_count}")
        print(f"  • Core Values: {values_count}")
        print(f"  • Problem-Solving Philosophy: {problem_solving_count}")
        print(f"  • TOTAL: {leadership_count + values_count + problem_solving_count}")
        print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
