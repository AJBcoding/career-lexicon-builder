#!/usr/bin/env python3
"""
Test runner for LLM-based career lexicon analysis - processes small batch
"""

import sys
from pathlib import Path
from analyzers.llm_analyzer import LLMAnalyzer
from generators.hierarchical_generator import HierarchicalGenerator
from core.document_processor import process_directory

def main():
    # Configuration
    input_dir = "my_documents/converted"
    output_dir = "lexicons_llm_test"
    
    print("=" * 70)
    print("Career Lexicon Builder - LLM Analysis (TEST - 5 documents)")
    print("=" * 70)
    print()
    print(f"Input directory:  {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Step 1: Process documents
    print("Step 1: Processing first 5 documents...")
    documents = process_directory(input_dir)
    
    # Limit to 5 documents
    documents = documents[:5]
    print(f"  ✓ Processed {len(documents)} documents")
    print()
    
    # Step 2: Analyze with Claude
    print("Step 2: Analyzing with Claude API...")
    print("  (This may take 1-2 minutes...)")
    print()
    
    analyzer = LLMAnalyzer()
    results = analyzer.analyze_all(documents)
    
    print("  ✓ Analysis complete")
    print()
    
    # Step 3: Generate outputs
    print("Step 3: Generating hierarchical markdown files...")
    
    generator = HierarchicalGenerator(output_dir)
    
    generator.generate_philosophy(results['philosophy'])
    print("  ✓ Generated 01_career_philosophy.md")
    
    generator.generate_achievements(results['achievements'])
    print("  ✓ Generated 02_achievement_library.md")
    
    generator.generate_narratives(results['narratives'])
    print("  ✓ Generated 03_narrative_patterns.md")
    
    generator.generate_language_bank(results['language_bank'])
    print("  ✓ Generated 04_language_bank.md")
    
    print()
    print("=" * 70)
    print("SUCCESS! Lexicons generated in:", output_dir)
    print("=" * 70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
