#!/usr/bin/env python3
"""
Re-run Achievement Library analysis for comprehensive coverage.
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
    print("Re-running Achievement Library Analysis (Comprehensive)")
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
    
    # Step 2: Analyze achievements
    print("Step 2: Extracting ALL achievements with Claude Sonnet 4...")
    print("  (This may take 60-90 seconds for comprehensive extraction...)")
    
    analyzer = LLMAnalyzer()
    formatted_docs = analyzer._format_documents(documents)
    
    achievements_result = analyzer.analyze_achievements(formatted_docs, documents)
    print("  ✓ Achievement analysis complete")
    print()
    
    # Step 3: Generate markdown
    print("Step 3: Generating updated markdown...")
    generator = HierarchicalMarkdownGenerator()
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, '02_achievement_library.md')
    output_path = generator.generate_achievements(achievements_result, output_file)
    print(f"  ✓ Generated {output_path}")
    print()
    
    # Count achievements
    import json
    if isinstance(achievements_result, str):
        try:
            data = json.loads(achievements_result)
        except:
            data = achievements_result
    else:
        data = achievements_result
        
    if isinstance(data, dict):
        category_count = len(data.get('categories', []))
        achievement_count = sum(len(cat.get('achievements', [])) for cat in data.get('categories', []))
        
        print("=" * 70)
        print("Analysis Complete!")
        print("=" * 70)
        print()
        print(f"Achievement counts:")
        print(f"  • Categories: {category_count}")
        print(f"  • Total achievements: {achievement_count}")
        
        # Show breakdown by category
        print()
        print("Breakdown by category:")
        for cat in data.get('categories', []):
            print(f"  • {cat.get('name', 'Unknown')}: {len(cat.get('achievements', []))} achievements")
        print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
