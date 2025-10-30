# Orchestrator Usage Guide

## Overview

The orchestrator coordinates the full Career Lexicon Builder pipeline from document ingestion to lexicon generation. It provides a streamlined interface for processing career documents (resumes, cover letters, bios) and generating reusable lexicon files.

## Quick Start

### Full Pipeline

Process all documents and generate complete lexicons:

```python
from core.orchestrator import run_full_pipeline

result = run_full_pipeline(
    input_dir="my_documents/",
    output_dir="lexicons/"
)

print(f"Processed {result['statistics']['documents_processed']} documents")
print(f"Generated 4 lexicons in: lexicons/")
```

### Incremental Update

Process only new or modified documents:

```python
from core.orchestrator import run_incremental_update

result = run_incremental_update(
    input_dir="my_documents/",
    output_dir="lexicons/"
)

print(f"New/modified: {result['statistics']['new_documents']}")
print(f"Unchanged: {result['statistics']['unchanged_documents']}")
```

## Output Files

The orchestrator generates 4 lexicon files:

- **`my_values.md`** - Recurring themes and values from your career documents
- **`resume_variations.md`** - Qualification phrasing variations and examples
- **`storytelling_patterns.md`** - Narrative patterns catalog for cover letters and bios
- **`usage_index.md`** - Keyword usage index with context and confidence scores

Plus state management:

- **`.state.json`** - Processing manifest for incremental updates (tracks document hashes and timestamps)

## Supported File Formats

The orchestrator automatically handles:

- `.pages` (Apple Pages)
- `.pdf` (PDF documents)
- `.docx` (Microsoft Word)
- `.txt` (Plain text)
- `.md` (Markdown)

Files are automatically classified as resumes, cover letters, or biographical statements based on content analysis.

## API Reference

### `run_full_pipeline(input_dir, output_dir)`

Runs the complete pipeline: document processing, analysis, and lexicon generation.

**Parameters:**
- `input_dir` (str): Directory containing input documents
- `output_dir` (str): Directory for generated lexicons

**Returns:**
```python
{
    "success": bool,
    "statistics": {
        "documents_processed": int,
        "themes_found": int,
        "qualifications_found": int,
        "narratives_found": int,
        "keywords_found": int
    },
    "errors": list[str]
}
```

**Example:**
```python
result = run_full_pipeline("docs/", "output/")

if result['success']:
    print(f"Success! Found {result['statistics']['themes_found']} themes")
else:
    print("Errors occurred:", result['errors'])
```

### `run_incremental_update(input_dir, output_dir)`

Efficiently updates lexicons by processing only new or modified documents.

**Parameters:**
- `input_dir` (str): Directory containing input documents
- `output_dir` (str): Directory for generated lexicons

**Returns:**
```python
{
    "success": bool,
    "statistics": {
        "documents_processed": int,
        "new_documents": int,
        "modified_documents": int,
        "unchanged_documents": int,
        "themes_found": int,
        "qualifications_found": int,
        "narratives_found": int,
        "keywords_found": int
    },
    "errors": list[str]
}
```

**Example:**
```python
result = run_incremental_update("docs/", "output/")

print(f"New: {result['statistics']['new_documents']}")
print(f"Modified: {result['statistics']['modified_documents']}")
print(f"Unchanged: {result['statistics']['unchanged_documents']}")
```

## Error Handling

The orchestrator handles errors gracefully and continues processing when possible:

```python
result = run_full_pipeline("my_documents/", "lexicons/")

if not result['success']:
    print("Errors occurred:")
    for error in result['errors']:
        print(f"  - {error}")
else:
    print("All processing completed successfully!")
```

**Common error scenarios:**
- Invalid or missing input directory
- Unsupported file formats (non-text files are skipped)
- Corrupted document files (logged and skipped)
- Permission errors on output directory

All errors are logged to the console with detailed context for troubleshooting.

## State Management

The orchestrator automatically manages processing state via a manifest file (`.state.json`) that tracks:

- **Document hashes**: MD5 checksums for change detection
- **Processing timestamps**: When each document was last processed
- **Document classifications**: Whether each file is a resume, cover letter, or bio

This enables efficient incremental updates:

1. **First run**: All documents are processed, state file is created
2. **Subsequent runs**: Only new/modified documents are processed
3. **Lexicons**: Regenerated from combined results of all documents

**State file location:**
```
output_dir/.state.json
```

**State file format:**
```json
{
    "manifest": {
        "file1.pdf": {
            "hash": "abc123...",
            "processed_at": "2025-10-29T12:00:00",
            "classification": "resume"
        }
    },
    "last_updated": "2025-10-29T12:00:00"
}
```

## Workflow Details

### Full Pipeline Workflow

1. **Document Processing**
   - Scan input directory for supported files
   - Extract text from each document
   - Classify documents (resume, cover letter, bio)
   - Update state manifest with hashes

2. **Analysis Phase**
   - **Themes Analyzer**: Identify recurring values and themes
   - **Qualifications Analyzer**: Extract qualification variations
   - **Narratives Analyzer**: Catalog storytelling patterns
   - **Keywords Analyzer**: Build keyword usage index

3. **Lexicon Generation**
   - **my_values.md**: Format themes into markdown
   - **resume_variations.md**: Organize qualifications by category
   - **storytelling_patterns.md**: Present narrative patterns
   - **usage_index.md**: Create searchable keyword index

4. **State Persistence**
   - Save processing manifest to `.state.json`
   - Enable future incremental updates

### Incremental Update Workflow

1. **Change Detection**
   - Load existing state manifest
   - Compare document hashes
   - Identify new, modified, and unchanged files

2. **Selective Processing**
   - Process only new and modified documents
   - Load previous analysis results for unchanged docs
   - Merge all results for complete context

3. **Lexicon Regeneration**
   - Generate fresh lexicons from merged results
   - Update state manifest

4. **Statistics Reporting**
   - Report counts of new, modified, and unchanged documents
   - Provide total analysis counts

## Performance Considerations

### Model Loading

The first run downloads and caches semantic similarity models (~500MB):

- **First run**: 20-30 minutes (one-time download)
- **Subsequent runs**: 5-10 minutes (models cached locally)

Models are cached in: `~/.cache/sentence-transformers/`

### Processing Time

Approximate processing times:

- **10 documents**: 2-5 minutes
- **50 documents**: 10-20 minutes
- **100+ documents**: 30-60 minutes

Incremental updates are significantly faster (only processes changed files).

### Optimization Tips

1. **Use incremental updates**: After initial run, use `run_incremental_update()`
2. **Batch processing**: Process documents in batches rather than one at a time
3. **Clean input**: Remove non-text files from input directory
4. **SSD storage**: Use SSD for model cache directory

## Troubleshooting

### Issue: "No module named 'core.orchestrator'"

**Solution**: Ensure you're running from the project root directory:
```bash
cd /path/to/career-lexicon-builder
python -c "from core.orchestrator import run_full_pipeline; ..."
```

### Issue: "Input directory does not exist"

**Solution**: Verify the input directory path is correct:
```python
import os
print(os.path.exists("my_documents/"))  # Should be True
```

### Issue: "Models downloading for long time"

**Solution**: This is normal for first run. Models (~500MB) are cached locally and subsequent runs will be much faster.

### Issue: "No documents processed"

**Solution**: Check that input directory contains supported file formats (.pdf, .docx, .txt, .md, .pages)

### Issue: "Lexicons are empty"

**Solution**: Verify documents contain sufficient text content. Very short documents may not produce enough analysis results.

## Example Workflows

### Workflow 1: Process New Resume Collection

```python
from core.orchestrator import run_full_pipeline

# Initial processing
result = run_full_pipeline(
    input_dir="resumes/2024/",
    output_dir="lexicons/2024/"
)

print(f"Processed {result['statistics']['documents_processed']} resumes")
print(f"Output: lexicons/2024/my_values.md")
```

### Workflow 2: Add New Document and Update

```python
from core.orchestrator import run_incremental_update

# Add new resume to resumes/2024/ directory
# Then run incremental update

result = run_incremental_update(
    input_dir="resumes/2024/",
    output_dir="lexicons/2024/"
)

if result['statistics']['new_documents'] > 0:
    print(f"Added {result['statistics']['new_documents']} new document(s)")
    print("Lexicons updated!")
else:
    print("No changes detected")
```

### Workflow 3: Batch Process Multiple Directories

```python
from core.orchestrator import run_full_pipeline

directories = ["resumes/", "cover_letters/", "bios/"]

for dir_path in directories:
    result = run_full_pipeline(
        input_dir=dir_path,
        output_dir=f"lexicons/{dir_path.strip('/')}"
    )
    print(f"{dir_path}: {result['statistics']['documents_processed']} docs")
```

### Workflow 4: Error Recovery

```python
from core.orchestrator import run_full_pipeline
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

result = run_full_pipeline("documents/", "output/")

if not result['success']:
    print("Processing completed with errors:")
    for error in result['errors']:
        print(f"  ERROR: {error}")

    # Partial results are still available
    print(f"\nPartial results:")
    print(f"  Documents processed: {result['statistics']['documents_processed']}")
    print(f"  Themes found: {result['statistics']['themes_found']}")
```

## Testing

Run the test suite to verify orchestrator functionality:

```bash
# All orchestrator tests (22 tests)
pytest tests/test_orchestrator.py -v

# Fast unit tests only (15 tests, ~17 seconds)
pytest tests/test_orchestrator.py -v -k "not Pipeline and not Incremental"

# Integration tests only (7 tests, ~20-30 minutes first run)
pytest tests/test_orchestrator.py::TestRunFullPipeline -v
pytest tests/test_orchestrator.py::TestRunIncrementalUpdate -v
```

## Architecture

The orchestrator coordinates these components:

1. **Document Processor** (`core.document_processor`)
   - Text extraction
   - Document classification
   - Format handling

2. **Analyzers** (`analyzers/`)
   - `themes_analyzer.py`: Theme extraction
   - `qualifications_analyzer.py`: Qualification analysis
   - `narratives_analyzer.py`: Narrative pattern detection
   - `keywords_analyzer.py`: Keyword indexing

3. **Generators** (`generators/`)
   - `themes_lexicon_generator.py`: Themes → `my_values.md`
   - `qualifications_lexicon_generator.py`: Qualifications → `resume_variations.md`
   - `narratives_lexicon_generator.py`: Narratives → `storytelling_patterns.md`
   - `keywords_lexicon_generator.py`: Keywords → `usage_index.md`

4. **State Manager** (`core.state_manager`)
   - Manifest persistence
   - Change detection
   - Incremental processing

## Next Steps

After generating lexicons:

1. **Review lexicons**: Examine generated markdown files
2. **Refine inputs**: Add more documents for richer lexicons
3. **Use lexicons**: Reference when writing new career documents
4. **Iterate**: Run incremental updates as you add new documents

## Support

For issues or questions:

- File an issue in the project repository
- Check test suite for usage examples: `tests/test_orchestrator.py`
- Review source code: `core/orchestrator.py`

---

**Version**: 1.0
**Last Updated**: 2025-10-29
**Compatible with**: Career Lexicon Builder v1.0+
