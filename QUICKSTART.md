# Quick Start Guide

Get started with Career Lexicon Builder in 5 minutes.

## What You'll Get

Transform your career documents into four searchable lexicons:
- **my_values.md** - Your recurring themes and values
- **resume_variations.md** - How you phrase qualifications
- **storytelling_patterns.md** - Your narrative patterns
- **usage_index.md** - Keyword usage with context

## Prerequisites

- Python 3.9 or higher
- Your career documents (resumes, cover letters, bios) in PDF, Word, text, or Apple Pages format

## Installation (2 minutes)

```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/career-lexicon-builder.git
cd career-lexicon-builder

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## First Run (5-30 minutes)

### Step 1: Prepare Your Documents

Create an input folder with your career documents:

```bash
mkdir my_documents
# Copy your resumes, cover letters, and bios into my_documents/
```

### Step 2: Run the Pipeline

Create a simple Python script or run this in a Python shell:

```python
from core.orchestrator import run_full_pipeline

# Process all documents
result = run_full_pipeline(
    input_dir="my_documents/",
    output_dir="my_lexicons/"
)

# Check results
if result['success']:
    print(f"✅ Success! Processed {result['statistics']['documents_processed']} documents")
    print(f"📊 Found:")
    print(f"   - {result['statistics']['themes_found']} themes")
    print(f"   - {result['statistics']['qualifications_found']} qualifications")
    print(f"   - {result['statistics']['narratives_found']} narratives")
    print(f"   - {result['statistics']['keywords_found']} keywords")
    print(f"\n📁 Lexicons generated in: my_lexicons/")
else:
    print(f"❌ Errors: {result['errors']}")
```

**Or save as `run_pipeline.py` and execute:**

```bash
python run_pipeline.py
```

### Step 3: First Run Notes

⏰ **First run takes 20-30 minutes** because it:
- Downloads semantic similarity models (~500MB)
- Processes all your documents
- Generates lexicons

The models are cached, so **subsequent runs take only 2-5 minutes**.

### Step 4: Review Your Lexicons

```bash
ls -lh my_lexicons/
```

You should see:
```
my_values.md                  # Your career themes
resume_variations.md          # Qualification phrasing examples
storytelling_patterns.md      # Narrative patterns
usage_index.md                # Keyword index
.state.json                   # Processing state (for updates)
```

Open and explore each file in your favorite markdown viewer or text editor!

## Adding New Documents (30 seconds)

When you create a new resume or cover letter:

```python
from core.orchestrator import run_incremental_update

# Only processes new/modified files
result = run_incremental_update(
    input_dir="my_documents/",
    output_dir="my_lexicons/"
)

print(f"New: {result['statistics']['new_documents']}")
print(f"Modified: {result['statistics']['modified_documents']}")
print(f"Unchanged: {result['statistics']['unchanged_documents']}")
```

This is **much faster** (1-2 minutes) because it only processes changes!

## Quick Examples

### Example 1: Save as a Script

Create `generate_lexicons.py`:

```python
#!/usr/bin/env python3
from core.orchestrator import run_full_pipeline
import sys

result = run_full_pipeline("my_documents/", "my_lexicons/")

if result['success']:
    print("✅ Lexicons generated successfully!")
    sys.exit(0)
else:
    print("❌ Failed:", result['errors'])
    sys.exit(1)
```

Run it:
```bash
chmod +x generate_lexicons.py
python generate_lexicons.py
```

### Example 2: Update Existing Lexicons

Create `update_lexicons.py`:

```python
#!/usr/bin/env python3
from core.orchestrator import run_incremental_update

result = run_incremental_update("my_documents/", "my_lexicons/")

print(f"Updated! {result['statistics']['new_documents']} new documents added")
```

### Example 3: Process Multiple Folders

```python
from core.orchestrator import run_full_pipeline

folders = ["resumes/", "cover_letters/", "bios/"]

for folder in folders:
    print(f"\nProcessing {folder}...")
    result = run_full_pipeline(
        input_dir=folder,
        output_dir=f"lexicons/{folder.strip('/')}"
    )
    print(f"  Done: {result['statistics']['documents_processed']} docs")
```

## Troubleshooting

### ❌ "No module named 'core.orchestrator'"

**Fix:** Make sure you're in the project directory and virtual environment is activated:
```bash
cd career-lexicon-builder
source .venv/bin/activate
python
>>> from core.orchestrator import run_full_pipeline  # Should work
```

### ❌ Models downloading slowly

**This is normal!** First run downloads ~500MB. Be patient. Models are cached locally.

### ❌ No lexicons generated

**Check:**
1. Input directory has supported files (.pdf, .docx, .txt, .md, .pages)
2. Output directory is writable
3. Check for errors in result['errors']

### ❌ ImportError for dependencies

**Fix:** Reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Understanding the Output

### my_values.md
Your core themes like "leadership," "innovation," "collaboration" with examples from your documents.

### resume_variations.md
Different ways you've described the same qualifications:
- "Led team of 5 engineers" vs "Managed engineering team"
- "Python, Java, Go" vs "Full-stack development"

### storytelling_patterns.md
Narrative structures you use:
- Opening hooks
- Challenge-solution patterns
- Achievement highlights

### usage_index.md
Every important keyword with:
- Where it appears
- How often you use it
- Context examples

## Next Steps

1. **Review lexicons** - Understand your career narrative patterns
2. **Use for applications** - Reference when writing new materials
3. **Keep updating** - Run incremental updates as you create new documents
4. **Customize** - Check README_ORCHESTRATOR.md for advanced options

## Testing the Installation

Verify everything works:

```bash
# Run validation
python validate_deployment.py

# Should show: ✅ ALL CHECKS PASSED (6/6)
```

## Common Use Cases

### Use Case 1: Job Application
```
1. Review my_values.md to align with company culture
2. Check resume_variations.md for relevant phrasing
3. Reference storytelling_patterns.md for cover letter
4. Use usage_index.md to find specific examples
```

### Use Case 2: Resume Update
```
1. Update your resume
2. Run: run_incremental_update()
3. Review new variations in resume_variations.md
4. Check consistency across documents
```

### Use Case 3: Career Reflection
```
1. Process all career documents from the past 5 years
2. Review my_values.md to see theme evolution
3. Identify strongest patterns in storytelling_patterns.md
4. Use insights for career planning
```

## Performance Expectations

| Task | First Run | Subsequent Runs |
|------|-----------|-----------------|
| 10 documents | 25 min | 2-3 min |
| 50 documents | 35 min | 8-12 min |
| 100+ documents | 45+ min | 15-25 min |

Incremental updates: **1-2 minutes** regardless of total documents!

## Getting Help

- **Full documentation**: See [README.md](README.md)
- **API reference**: See [README_ORCHESTRATOR.md](README_ORCHESTRATOR.md)
- **Run tests**: `python -m pytest tests/ -v`
- **File issues**: Check the repository issue tracker

## Tips for Best Results

1. ✅ **Use meaningful filenames** - Include dates when possible (e.g., `2024-03-resume.pdf`)
2. ✅ **Organize by type** - Keep resumes, cover letters, bios in separate folders
3. ✅ **Update regularly** - Use incremental updates to keep lexicons current
4. ✅ **Review outputs** - The lexicons help you understand your career narrative
5. ✅ **Keep originals** - The tool doesn't modify your source documents

---

**Ready to start?** Run the installation steps above and process your first documents!

**Questions?** Check [README.md](README.md) for comprehensive documentation.
