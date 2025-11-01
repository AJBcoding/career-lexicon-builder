# Career Lexicon Builder

**A comprehensive Python toolkit for analyzing career documents and building reusable lexicon files**

Transform your career documents (resumes, cover letters, biographical statements) into intelligent, searchable lexicons that capture your themes, qualifications, storytelling patterns, and keyword usage.

## What It Does

The Career Lexicon Builder analyzes your existing career documents to create four reusable lexicon files:

1. **My Values** (`my_values.md`) - Recurring themes and values from your career narrative
2. **Resume Variations** (`resume_variations.md`) - Qualification phrasing variations and examples
3. **Storytelling Patterns** (`storytelling_patterns.md`) - Narrative patterns catalog for cover letters
4. **Usage Index** (`usage_index.md`) - Keyword usage index with context and confidence scores

## Features

- **Automatic Document Classification**: Identifies resumes, cover letters, and biographical statements
- **Multi-Format Support**: PDF, Word (.docx), plain text (.txt, .md), Apple Pages (.pages)
- **Semantic Analysis**: Uses sentence transformers for intelligent similarity detection
- **Incremental Processing**: Only processes new or modified documents
- **State Management**: Tracks document hashes for efficient updates
- **Comprehensive Testing**: 331+ tests with 100% pass rate

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/career-lexicon-builder.git
cd career-lexicon-builder

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from core.orchestrator import run_full_pipeline

# Process all documents and generate lexicons
result = run_full_pipeline(
    input_dir="my_documents/",
    output_dir="lexicons/"
)

print(f"Processed {result['statistics']['documents_processed']} documents")
print(f"Found {result['statistics']['themes_found']} themes")
```

### Incremental Updates

```python
from core.orchestrator import run_incremental_update

# Only process new or modified documents
result = run_incremental_update(
    input_dir="my_documents/",
    output_dir="lexicons/"
)

print(f"New documents: {result['statistics']['new_documents']}")
print(f"Modified documents: {result['statistics']['modified_documents']}")
```

### Output Files

After processing, you'll find these files in your output directory:

```
lexicons/
├── my_values.md                 # Themes and values from your career
├── resume_variations.md         # Qualification phrasing variations
├── storytelling_patterns.md     # Narrative patterns catalog
├── usage_index.md               # Keyword usage with context
└── .state.json                  # Processing state (for incremental updates)
```

## Socratic Career Application Skills

After generating your lexicons, use the Socratic career skills for job applications:

**Skills installed in:** `~/.claude/skills/career/`

### Quick Workflow

1. **Analyze job description**
   ```
   "Analyze this job description" [paste/upload JD]
   ```

2. **Tailor resume**
   ```
   "Tailor my resume for this role" [upload resume]
   ```

3. **Plan cover letter**
   ```
   "Analyze my fit and plan my cover letter"
   ```

4. **Draft materials**
   ```
   "Develop my cover letter narrative"
   "Help me draft the cover letter"
   ```

**See:** `~/.claude/skills/career/README.md` for detailed skill documentation

**Principles:**
- All content verified against your lexicons
- No fabrication - every statement traceable
- Socratic dialogue guides process
- Evidence trails in all outputs

## Project Structure

```
career-lexicon-builder/
├── core/                        # Core coordination and processing
│   ├── orchestrator.py          # Central pipeline coordinator
│   ├── document_processor.py    # Document classification and extraction
│   ├── state_manager.py         # State and manifest management
│   └── confidence_scorer.py     # Confidence calculation
├── analyzers/                   # Analysis modules (Phase 3)
│   ├── themes_analyzer.py       # Theme detection and clustering
│   ├── qualifications_analyzer.py  # Qualification extraction
│   ├── narratives_analyzer.py   # Narrative pattern detection
│   └── keywords_analyzer.py     # Keyword indexing
├── generators/                  # Lexicon generators (Phase 4)
│   ├── themes_lexicon_generator.py
│   ├── qualifications_lexicon_generator.py
│   ├── narratives_lexicon_generator.py
│   └── keywords_lexicon_generator.py
├── utils/                       # Utilities
│   ├── text_extraction.py       # Multi-format text extraction (.pages, etc)
│   ├── similarity.py            # Semantic similarity utilities
│   └── date_parser.py           # Date extraction from filenames
├── templates/                   # Markdown templates for lexicon output
├── tests/                       # 331+ comprehensive tests
├── README.md                    # This file
└── README_ORCHESTRATOR.md       # Detailed orchestrator documentation
```

## Implementation Status

### Phase 1: Foundation (✅ Complete)
- Date parsing from filenames
- Text extraction from multiple formats
- Apple Pages (.pages) file support
- **55 tests passing**

### Phase 2: Document Processing (✅ Complete)
- Document classification (resume/cover letter/bio)
- Confidence scoring system
- State management with manifest persistence
- Multi-format text extraction
- **82 tests passing**

### Phase 3: Analysis Modules (✅ Complete)
- Themes analyzer with semantic clustering
- Qualifications analyzer with variations
- Narratives analyzer for storytelling patterns
- Keywords analyzer with context tracking
- **119 tests passing**

### Phase 4: Lexicon Generators (✅ Complete)
- Themes → my_values.md
- Qualifications → resume_variations.md
- Narratives → storytelling_patterns.md
- Keywords → usage_index.md
- **40 tests passing**

### Phase 5: Central Orchestrator (✅ Complete)
- Full pipeline coordination
- Incremental update support
- Error handling and logging
- Statistics tracking
- **22 tests passing**

### Phase 6: Testing & Polish (🔄 In Progress)
- Integration test validation
- Manual end-to-end testing
- Documentation (README_ORCHESTRATOR.md)
- Performance profiling

### Phase 7: Documentation & Deployment (🔜 Next)
- Final user guide
- Code polish and cleanup
- Production deployment

**Total: 331+ tests, 100% passing**

## Test Coverage

Run the comprehensive test suite:

```bash
# All tests (331+ tests)
python -m pytest tests/ -v

# Fast tests only (skip slow integration tests)
python -m pytest tests/ -v -k "not Pipeline and not Incremental"

# Orchestrator tests only (22 tests)
python -m pytest tests/test_orchestrator.py -v

# Specific module tests
python -m pytest tests/test_themes_analyzer.py -v
python -m pytest tests/test_qualifications_analyzer.py -v
```

## Performance Notes

### First Run
- Downloads semantic similarity models (~500MB)
- Takes 20-30 minutes for first run
- Models cached locally at `~/.cache/sentence-transformers/`

### Subsequent Runs
- Much faster (models already cached)
- 10 documents: 2-5 minutes
- 50 documents: 10-20 minutes
- 100+ documents: 30-60 minutes

### Incremental Updates
- Only processes new/modified documents
- Significantly faster than full pipeline
- State tracked in `.state.json`

## API Reference

### Core Functions

#### `run_full_pipeline(input_dir, output_dir)`

Process all documents and generate complete lexicons.

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

#### `run_incremental_update(input_dir, output_dir)`

Process only new or modified documents.

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

For detailed API documentation, see [README_ORCHESTRATOR.md](README_ORCHESTRATOR.md).

## Documentation

- **[README_ORCHESTRATOR.md](README_ORCHESTRATOR.md)** - Detailed orchestrator usage guide
- **[DesignDocuments/](DesignDocuments/)** - Architecture and design documents
- **[DevArtifacts/](DevArtifacts/)** - Phase handoff documents and implementation notes

## Supported File Formats

- `.pages` (Apple Pages)
- `.pdf` (PDF documents)
- `.docx` (Microsoft Word)
- `.txt` (Plain text)
- `.md` (Markdown)

Documents are automatically classified based on content analysis.

## Error Handling

The system handles errors gracefully:

```python
result = run_full_pipeline("docs/", "output/")

if not result['success']:
    print("Errors occurred:")
    for error in result['errors']:
        print(f"  - {error}")
else:
    print("Success! Lexicons generated.")
```

Common error scenarios:
- Invalid or missing input directory
- Unsupported file formats (skipped automatically)
- Corrupted files (logged and skipped)
- Permission errors

## Troubleshooting

### Issue: Models downloading slowly

**Solution:** This is normal on first run. The semantic similarity models (~500MB) are downloaded and cached. Subsequent runs will be much faster.

### Issue: No output files generated

**Solution:** Check that your input directory contains supported file formats and that the output directory is writable.

### Issue: "No module named 'core.orchestrator'"

**Solution:** Ensure you're running from the project root directory and have activated the virtual environment.

### Issue: Tests failing

**Solution:** Ensure all dependencies are installed (`pip install -r requirements.txt`) and you're using Python 3.9+.

## Example Workflows

### Workflow 1: Initial Processing

```python
from core.orchestrator import run_full_pipeline

# Process all your career documents
result = run_full_pipeline(
    input_dir="~/Documents/Career/",
    output_dir="~/Lexicons/"
)

print(f"Processed {result['statistics']['documents_processed']} documents")
print(f"Generated 4 lexicon files in ~/Lexicons/")
```

### Workflow 2: Adding New Documents

```python
from core.orchestrator import run_incremental_update

# Add new resume or cover letter to ~/Documents/Career/
# Then run incremental update

result = run_incremental_update(
    input_dir="~/Documents/Career/",
    output_dir="~/Lexicons/"
)

print(f"New: {result['statistics']['new_documents']}")
print(f"Lexicons updated!")
```

### Workflow 3: Batch Processing

```python
from core.orchestrator import run_full_pipeline

directories = [
    "resumes/",
    "cover_letters/",
    "bios/"
]

for dir_path in directories:
    result = run_full_pipeline(
        input_dir=dir_path,
        output_dir=f"lexicons/{dir_path.strip('/')}"
    )
    print(f"{dir_path}: {result['statistics']['documents_processed']} docs")
```

## Development

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=analyzers --cov=generators

# Run specific test file
python -m pytest tests/test_orchestrator.py -v
```

### Code Style

This project follows:
- PEP 8 style guide
- Type hints for all functions
- Comprehensive docstrings
- 80-character line length (where reasonable)

## Requirements

- Python 3.9+
- Dependencies (see `requirements.txt`):
  - `sentence-transformers` - Semantic similarity analysis
  - `scikit-learn` - Clustering and similarity metrics
  - `python-docx` - Word document processing
  - `PyPDF2` - PDF text extraction
  - `pytest` - Testing framework

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with:
- [sentence-transformers](https://www.sbert.net/) for semantic analysis
- [scikit-learn](https://scikit-learn.org/) for clustering
- [pytest](https://pytest.org/) for testing

## Contact

For issues or questions:
- File an issue in the project repository
- Check existing tests for usage examples
- Review documentation in `README_ORCHESTRATOR.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Production Ready (Phases 1-5 Complete)
