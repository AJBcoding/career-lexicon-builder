#!/usr/bin/env python3
"""
Deployment validation script for Career Lexicon Builder.

Validates that:
1. All required modules can be imported
2. Basic orchestrator functions work
3. Directory structure is correct
4. Dependencies are installed
"""

import sys
import os
from pathlib import Path


def check_directory_structure():
    """Verify all required directories exist."""
    print("1. Checking directory structure...")

    required_dirs = [
        "core",
        "analyzers",
        "generators",
        "utils",
        "templates",
        "tests"
    ]

    missing_dirs = []
    for dirname in required_dirs:
        if not os.path.exists(dirname):
            missing_dirs.append(dirname)

    if missing_dirs:
        print(f"   ❌ Missing directories: {', '.join(missing_dirs)}")
        return False

    print(f"   ✅ All required directories present")
    return True


def check_imports():
    """Verify all required modules can be imported."""
    print("\n2. Checking module imports...")

    modules_to_check = [
        ("core.orchestrator", ["run_full_pipeline", "run_incremental_update"]),
        ("core.document_processor", ["classify_document", "DocumentType"]),
        ("core.state_manager", ["load_manifest", "save_manifest"]),
        ("analyzers.themes_analyzer", ["analyze_themes"]),
        ("analyzers.qualifications_analyzer", ["analyze_qualifications"]),
        ("analyzers.narratives_analyzer", ["analyze_narratives"]),
        ("analyzers.keywords_analyzer", ["analyze_keywords"]),
        ("generators.themes_lexicon_generator", ["generate_themes_lexicon"]),
        ("utils.text_extraction", ["extract_text_from_document"]),
        ("utils.similarity", ["calculate_semantic_similarity"]),
        ("utils.date_parser", ["extract_date_from_filename"])
    ]

    failed_imports = []

    for module_name, functions in modules_to_check:
        try:
            module = __import__(module_name, fromlist=functions)
            for func_name in functions:
                if not hasattr(module, func_name):
                    failed_imports.append(f"{module_name}.{func_name}")
        except ImportError as e:
            failed_imports.append(f"{module_name}: {e}")

    if failed_imports:
        print(f"   ❌ Failed imports:")
        for failure in failed_imports:
            print(f"      - {failure}")
        return False

    print(f"   ✅ All modules import successfully")
    return True


def check_dependencies():
    """Verify required dependencies are installed."""
    print("\n3. Checking dependencies...")

    required_packages = [
        "pytest",
        "sentence_transformers",
        "sklearn",
        "docx",
        "pdfplumber"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"   ❌ Missing packages: {', '.join(missing_packages)}")
        print(f"      Run: pip install -r requirements.txt")
        return False

    print(f"   ✅ All required packages installed")
    return True


def check_test_fixtures():
    """Verify test fixtures exist."""
    print("\n4. Checking test fixtures...")

    fixtures_dir = Path("tests/fixtures")
    if not fixtures_dir.exists():
        print(f"   ❌ Test fixtures directory missing: {fixtures_dir}")
        return False

    # Count fixture files
    fixture_files = list(fixtures_dir.glob("*"))
    if len(fixture_files) == 0:
        print(f"   ⚠️  No test fixture files found (optional)")
        return True

    print(f"   ✅ Test fixtures present ({len(fixture_files)} files)")
    return True


def check_templates():
    """Verify template utilities exist."""
    print("\n5. Checking template utilities...")

    templates_dir = Path("templates")
    if not templates_dir.exists():
        print(f"   ❌ Templates directory missing")
        return False

    # Check for formatting utilities (templates are embedded in generators)
    formatting_utils = templates_dir / "formatting_utils.py"
    if not formatting_utils.exists():
        print(f"   ❌ Missing formatting_utils.py")
        return False

    print(f"   ✅ Template utilities present (templates embedded in generators)")
    return True


def run_basic_validation():
    """Run basic functional validation."""
    print("\n6. Running basic functional validation...")

    try:
        # Import orchestrator functions
        from core.orchestrator import run_full_pipeline

        # This is a smoke test - we don't actually run the pipeline
        # Just verify the function is callable
        if not callable(run_full_pipeline):
            print(f"   ❌ run_full_pipeline is not callable")
            return False

        print(f"   ✅ Orchestrator functions are callable")
        return True
    except Exception as e:
        print(f"   ❌ Validation failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 70)
    print("Career Lexicon Builder - Deployment Validation")
    print("=" * 70)

    checks = [
        check_directory_structure,
        check_imports,
        check_dependencies,
        check_test_fixtures,
        check_templates,
        run_basic_validation
    ]

    results = []
    for check in checks:
        result = check()
        results.append(result)

    print("\n" + "=" * 70)
    print("Validation Summary")
    print("=" * 70)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"\n✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\nThe Career Lexicon Builder is ready for production use!")
        print("\nNext steps:")
        print("  1. Run tests: pytest tests/ -v")
        print("  2. Process documents: python -c \"from core.orchestrator import run_full_pipeline; run_full_pipeline('input/', 'output/')\"")
        print("  3. Review generated lexicons in output directory")
        return 0
    else:
        print(f"\n❌ VALIDATION FAILED ({passed}/{total} checks passed)")
        print("\nPlease fix the issues above before deploying to production.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
