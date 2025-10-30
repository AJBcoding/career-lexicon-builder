#!/usr/bin/env python3
"""Manual end-to-end testing for Career Lexicon Builder Orchestrator.

Tests 4 key scenarios:
1. Fresh Pipeline Run
2. Incremental Update (No Changes)
3. Incremental Update (With Changes)
4. Error Handling
"""

from core.orchestrator import run_full_pipeline, run_incremental_update
import os
import shutil
import sys


def cleanup_output():
    """Remove test output directory if it exists."""
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
        print("  Cleaned up previous test_output/")


def check_output_files():
    """Verify all expected output files were created."""
    files = ["my_values.md", "resume_variations.md",
             "storytelling_patterns.md", "usage_index.md", ".state.json"]

    print("\n  Checking output files:")
    all_exist = True
    for f in files:
        path = os.path.join("test_output", f)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"    {f}: {'✓' if exists else '✗'} ({size:,} bytes)")
        if not exists:
            all_exist = False

    return all_exist


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70 + "\n")


# Scenario 1: Fresh Pipeline Run
print_separator()
print("SCENARIO 1: Fresh Pipeline Run")
print_separator()

cleanup_output()

print("Running full pipeline on tests/fixtures...")
result = run_full_pipeline("tests/fixtures", "test_output")

print(f"\nResults:")
print(f"  Success: {result['success']}")
print(f"  Documents processed: {result['statistics']['documents_processed']}")
print(f"  Themes found: {result['statistics']['themes_found']}")
print(f"  Qualifications found: {result['statistics']['qualifications_found']}")
print(f"  Narratives found: {result['statistics']['narratives_found']}")
print(f"  Keywords found: {result['statistics']['keywords_found']}")
print(f"  Errors: {len(result['errors'])}")

if result['errors']:
    print("\n  Error details:")
    for error in result['errors']:
        print(f"    - {error}")

files_ok = check_output_files()

print(f"\n  SCENARIO 1: {'✅ PASS' if result['success'] and files_ok else '❌ FAIL'}")


# Scenario 2: Incremental Update (No Changes)
print_separator()
print("SCENARIO 2: Incremental Update (No Changes)")
print_separator()

print("Running incremental update with no file changes...")
result = run_incremental_update("tests/fixtures", "test_output")

print(f"\nResults:")
print(f"  Success: {result['success']}")
print(f"  New documents: {result['statistics']['new_documents']}")
print(f"  Modified documents: {result['statistics']['modified_documents']}")
print(f"  Unchanged documents: {result['statistics']['unchanged_documents']}")
print(f"  Documents processed: {result['statistics']['documents_processed']}")

expected_new = 0
expected_modified = 0
scenario2_pass = (result['success'] and
                  result['statistics']['new_documents'] == expected_new and
                  result['statistics']['modified_documents'] == expected_modified)

print(f"\n  SCENARIO 2: {'✅ PASS' if scenario2_pass else '❌ FAIL'}")
if not scenario2_pass:
    print(f"    Expected: new={expected_new}, modified={expected_modified}")
    print(f"    Got: new={result['statistics']['new_documents']}, modified={result['statistics']['modified_documents']}")


# Scenario 3: Incremental Update (With Changes)
print_separator()
print("SCENARIO 3: Incremental Update (With Changes)")
print_separator()

# Create a new test file
test_file = "tests/fixtures/test_new_document.txt"
if os.path.exists(test_file):
    os.remove(test_file)

print("Creating new test document...")
with open(test_file, "w") as f:
    f.write("""Sample Resume

John Doe
Software Engineer

Experience:
- Led team of 5 engineers
- Developed scalable microservices
- Implemented CI/CD pipelines

Skills:
- Python, Java, Go
- AWS, Docker, Kubernetes
- Agile methodologies

Education:
BS Computer Science, 2015
""")

print(f"  Created: {test_file}")

print("\nRunning incremental update with new file...")
result = run_incremental_update("tests/fixtures", "test_output")

print(f"\nResults:")
print(f"  Success: {result['success']}")
print(f"  New documents: {result['statistics']['new_documents']}")
print(f"  Modified documents: {result['statistics']['modified_documents']}")
print(f"  Unchanged documents: {result['statistics']['unchanged_documents']}")
print(f"  Documents processed: {result['statistics']['documents_processed']}")

expected_new = 1
scenario3_pass = (result['success'] and
                  result['statistics']['new_documents'] == expected_new)

print(f"\n  SCENARIO 3: {'✅ PASS' if scenario3_pass else '❌ FAIL'}")
if not scenario3_pass:
    print(f"    Expected: new={expected_new}")
    print(f"    Got: new={result['statistics']['new_documents']}")

# Cleanup test file
os.remove(test_file)
print(f"\n  Cleaned up: {test_file}")


# Scenario 4: Error Handling
print_separator()
print("SCENARIO 4: Error Handling")
print_separator()

print("Testing with nonexistent input directory...")
result = run_full_pipeline("nonexistent_directory", "test_output")

print(f"\nResults:")
print(f"  Success: {result['success']}")
print(f"  Errors: {len(result['errors'])}")

if result['errors']:
    print("\n  Error messages:")
    for error in result['errors']:
        print(f"    - {error}")

scenario4_pass = (not result['success'] and len(result['errors']) > 0)

print(f"\n  SCENARIO 4: {'✅ PASS' if scenario4_pass else '❌ FAIL'}")
if not scenario4_pass:
    print(f"    Expected: success=False, errors > 0")
    print(f"    Got: success={result['success']}, errors={len(result['errors'])}")


# Final Summary
print_separator()
print("FINAL SUMMARY")
print_separator()

all_scenarios_pass = all([
    result['success'] and files_ok,  # Scenario 1 from last result
    scenario2_pass,
    scenario3_pass,
    scenario4_pass
])

print(f"  Scenario 1 (Fresh Pipeline): {'✅ PASS' if files_ok else '❌ FAIL'}")
print(f"  Scenario 2 (No Changes): {'✅ PASS' if scenario2_pass else '❌ FAIL'}")
print(f"  Scenario 3 (With Changes): {'✅ PASS' if scenario3_pass else '❌ FAIL'}")
print(f"  Scenario 4 (Error Handling): {'✅ PASS' if scenario4_pass else '❌ FAIL'}")

print(f"\n  OVERALL: {'✅ ALL TESTS PASSED' if all_scenarios_pass else '❌ SOME TESTS FAILED'}")
print_separator()

# Exit with appropriate code
sys.exit(0 if all_scenarios_pass else 1)
