# Append Document References

Script to append "Files Referenced" sections to lexicon files.

## Purpose

Adds a comprehensive list of all source documents to the end of each lexicon file, organized by document type and sorted chronologically.

## Usage

### Dry Run (Recommended First)

```bash
python3 append_document_references.py --dry-run
```

Shows what would happen without making any changes.

### Real Run

```bash
python3 append_document_references.py
```

**Interactive prompts:** You'll be asked to confirm dates extracted from PDF content.

**Safety:** Creates timestamped backup before modifying lexicons.

## What It Does

1. **Scans** `my_documents/converted/` for all documents
2. **Extracts dates** from filenames (e.g., "2024-11-25 - file.pdf")
3. **For files without dates:** Extracts from PDF content and asks for confirmation
4. **Renames files** to standard format: `YYYY-MM-DD - original_name.pdf`
5. **Classifies** documents into categories:
   - CVs
   - Resumes
   - Cover Letters
   - Diversity Statements
   - Other
6. **Formats** as markdown lists sorted newest-first
7. **Appends** to all files in `lexicons_llm/`

## Output Format

```markdown
## Files Referenced

### CVs
- 2024 AJB CV 2024.pdf
- 2015-11 AJB CV 2015 v2.pdf

### Resumes
- 2025-10-13 Byrnes, Anthony Resume - Colburn School submitted.pdf
- 2020-11-23 ajb resume.pdf

### Cover Letters
- 2025-01-15 CSULB AD cover letter.pdf
...
```

## Safety Features

- **Dry-run mode** to preview changes
- **Automatic backups** before modifying lexicons
- **Collision detection** prevents duplicate filenames
- **Idempotent** - skips lexicons that already have "Files Referenced"

## Restoring from Backup

If something goes wrong:

```bash
rm -rf lexicons_llm
mv lexicons_llm_backup_TIMESTAMP lexicons_llm
```

## Integration with Lexicon Pipeline

This is a **one-time update script**. To integrate into the automated pipeline, see:
- Design doc: `docs/plans/2025-11-02-append-document-references-design.md`
- Section: "Future Integration: Approach 3 (LLM-Based)"
