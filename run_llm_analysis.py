"""
Run LLM-based career lexicon analysis.

This script provides a simple interface to analyze career documents
using Claude API and generate hierarchical reference guides.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import process_documents
from core.state_manager import ProcessingManifest
from analyzers.llm_analyzer import LLMAnalyzer
from generators.hierarchical_generator import HierarchicalMarkdownGenerator


def main():
    """Run the LLM analysis pipeline."""

    # Configuration
    input_dir = "my_documents/converted"  # Use converted PDFs
    output_dir = "lexicons_llm"

    # Try to get API key (may not be needed in Claude Code)
    api_key = os.getenv('ANTHROPIC_API_KEY')

    print("=" * 70)
    print("Career Lexicon Builder - LLM Analysis")
    print("=" * 70)
    print("")
    print(f"Input directory:  {input_dir}")
    print(f"Output directory: {output_dir}")
    print("")

    # Step 1: Process documents
    print("Step 1: Processing documents...")

    # Create empty manifest (we'll process all files)
    from datetime import datetime
    manifest = ProcessingManifest(
        last_updated=datetime.now().isoformat(),
        documents={},
        version="1.0"
    )
    documents = process_documents(input_dir, manifest)

    print(f"  ✓ Processed {len(documents)} documents")
    print("")

    # Step 2: Analyze with LLM
    print("Step 2: Analyzing with Claude API...")
    print("  (This may take 2-3 minutes...)")
    print("")

    analyzer = LLMAnalyzer(api_key=api_key)

    # Analyze each lexicon type
    formatted_docs = analyzer._format_documents(documents)

    results = {}

    print("  Analyzing career philosophy & values...")
    results['philosophy'] = analyzer.analyze_philosophy(formatted_docs, documents)
    print("  ✓ Philosophy complete")

    print("  Analyzing achievements...")
    results['achievements'] = analyzer.analyze_achievements(formatted_docs, documents)
    print("  ✓ Achievements complete")

    print("  Analyzing narrative patterns...")
    results['narratives'] = analyzer.analyze_narratives(formatted_docs, documents)
    print("  ✓ Narratives complete")

    print("  Analyzing language patterns...")
    results['language_bank'] = analyzer.analyze_language(formatted_docs, documents)
    print("  ✓ Language bank complete")

    print("")

    # Step 3: Generate markdown
    print("Step 3: Generating hierarchical markdown...")
    generator = HierarchicalMarkdownGenerator()
    output_files = generator.generate_all(results, output_dir)

    print(f"  ✓ Generated {len(output_files)} lexicon files")
    print("")

    # Show results
    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print("")
    print("Generated files:")
    for name, path in output_files.items():
        print(f"  • {path}")
    print("")
    print("Next steps:")
    print("  1. Review the generated lexicons")
    print("  2. Use them when analyzing job descriptions")
    print("  3. Reference them when writing cover letters/resumes")
    print("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
