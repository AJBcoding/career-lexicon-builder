#!/usr/bin/env python3
"""
Re-run Narrative Patterns analysis to fix incomplete entries.
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
    print("Re-running Narrative Patterns Analysis")
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
    
    # Step 2: Analyze narratives only
    print("Step 2: Analyzing narrative patterns with Claude Sonnet 4...")
    print("  (This may take 30-60 seconds...)")
    
    analyzer = LLMAnalyzer()
    formatted_docs = analyzer._format_documents(documents)
    
    narratives_result = analyzer.analyze_narratives(formatted_docs, documents)
    print("  ✓ Narrative analysis complete")
    print()
    
    # Step 3: Generate markdown
    print("Step 3: Generating updated markdown...")
    generator = HierarchicalMarkdownGenerator()
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, '03_narrative_patterns.md')
    output_path = generator.generate_narratives(narratives_result, output_file)
    print(f"  ✓ Generated {output_path}")
    print()
    
    # Check for incomplete patterns
    print("Step 4: Checking for incomplete entries...")
    with open(output_file, 'r') as f:
        content = f.read()
        incomplete_count = content.count('### Pattern\n')
        
    print(f"  • Incomplete 'Pattern' entries: {incomplete_count}")
    
    # Count total patterns
    total_patterns = content.count('### ')
    print(f"  • Total pattern entries: {total_patterns}")
    print()
    
    if incomplete_count == 0:
        print("=" * 70)
        print("SUCCESS! All patterns have descriptive names")
        print("=" * 70)
    else:
        print("=" * 70)
        print(f"WARNING: Still {incomplete_count} incomplete patterns")
        print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
