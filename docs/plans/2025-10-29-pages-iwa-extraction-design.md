# .pages IWA Format Extraction Enhancement

**Date**: 2025-10-29
**Status**: Design Complete - Ready for Implementation
**Objective**: Add robust text extraction support for newer .pages files using .iwa (iWork Archive) format

---

## Problem Statement

### Current Situation
The Career Lexicon Builder pipeline failed to extract text from 23 .pages files during execution. All failures showed the same error:

```
Could not extract text from [file]. This .pages file uses a newer format
that requires manual conversion. Please export to .docx or .pdf from Pages
and re-run extraction.
```

### Root Cause Analysis

Investigation revealed:

1. **Current extraction strategy** (utils/text_extraction.py:143-182) uses a two-tier approach:
   - **Tier 1**: XML extraction (`_try_xml_extraction`) - targets old format .pages files with `index.xml`
   - **Tier 2**: PDF preview extraction (`_try_pdf_preview_extraction`) - targets files with `QuickLook/Preview.pdf`

2. **Why it's failing**: Newer .pages files (Pages 5.0+, circa 2013+) use:
   - `.iwa` (iWork Archive) format instead of `index.xml`
   - Binary protobuf + Snappy compression
   - `preview.jpg` (JPEG) instead of `Preview.pdf`

3. **Evidence from failing files**:
   ```bash
   $ zipinfo "2025-10-13 - Colburn School, Byrnes, Anthony - submitted.pages"
   Archive:  2025-10-13 - Colburn School, Byrnes, Anthony - submitted.pages
   -rw---- 6.2 fat 16792 b- stor 25-Oct-15 13:19 Index/Document.iwa
   -rw---- 6.2 fat 843 b- stor 25-Oct-15 13:23 Index/ViewState.iwa
   -rw---- 6.2 fat 327215 b- stor 25-Oct-15 13:19 preview.jpg
   ...
   ```

   **No `index.xml`, no `Preview.pdf` → both extraction methods fail**

### Requirements

**Must-haves:**
- Extract text from all 23 failing .pages files
- Maintain backward compatibility (existing XML/PDF preview methods still work)
- Preserve existing API contract (returns same Dict structure)
- Pure Python solution (no external binaries, no macOS-only dependencies)
- Graceful degradation when extraction fails

**Nice-to-haves:**
- Preserve formatting metadata where possible
- Performance comparable to existing methods
- Handle edge cases (corrupted files, incomplete archives)

---

## Design Decision

### Approach Selected: **Protobuf + Snappy Decompression (Native .iwa Parsing)**

**Why this approach:**
- ✅ Extracts actual document content (most accurate)
- ✅ Pure Python dependencies (pip-installable)
- ✅ Platform-independent (works on Linux, macOS, Windows)
- ✅ Can preserve formatting if needed later

**Alternatives considered:**
1. **OCR from preview.jpg** - Less accurate, OCR errors, external binary dependency (tesseract)
2. **Multi-strategy cascade** - More complex, unnecessary if protobuf approach works well

---

## Technical Design

### Architecture Overview

**New extraction cascade:**

```
.pages file
    ↓
is_zipfile?
    ↓
[1] Try XML extraction (old format)
    ↓ (if fails)
[2] Try IWA extraction (NEW - newer format)  ← INSERT HERE
    ↓ (if fails)
[3] Try PDF preview extraction (fallback)
    ↓ (if fails)
[4] Return failure with manual conversion instructions
```

The new `_try_iwa_extraction()` function slots between XML and PDF preview, maintaining backward compatibility.

### .IWA Format Technical Details

**What is .iwa?**
- **IWA = iWork Archive format** (used since Pages 5.0/2013)
- Binary format: Snappy-compressed protobuf messages
- Stored in `Index/*.iwa` files within the .pages zip archive

**Key Files:**
- `Index/Document.iwa` - Main document structure and text content
- `Index/DocumentStylesheet.iwa` - Styling information
- `Index/Metadata.iwa` - Document metadata

**Format Structure:**
```
.pages (ZIP archive)
├── Index/
│   ├── Document.iwa          ← Main content (Snappy + Protobuf)
│   ├── DocumentStylesheet.iwa
│   ├── ViewState.iwa
│   └── ...
├── Data/                      ← Embedded images
├── Metadata/
└── preview.jpg                ← Preview image
```

**Document.iwa Structure:**
- Snappy-compressed outer layer
- Protobuf message inner layer (Apple's proprietary TSP schema)
- Text content stored in protobuf string fields
- Schema is proprietary, requires heuristic parsing

### Implementation Approach

#### 1. Dependencies

**Add to requirements.txt:**
```python
python-snappy>=0.6.1  # Snappy compression/decompression
protobuf>=4.21.0      # Protocol buffer parsing
```

**Why these versions:**
- `python-snappy>=0.6.1` - Stable, widely used, pure Python bindings to snappy
- `protobuf>=4.21.0` - Modern protobuf library with good Python 3 support

#### 2. New Function: `_try_iwa_extraction()`

**Location**: utils/text_extraction.py (insert after `_try_xml_extraction()`)

**Signature:**
```python
def _try_iwa_extraction(filepath: str) -> ExtractionResult:
    """
    Try to extract text from .iwa format .pages file (newer format).

    Args:
        filepath: Path to .pages file

    Returns:
        ExtractionResult with text content or failure details
    """
```

**Algorithm:**

```python
1. Check dependencies (snappy, protobuf)
   ├─ If missing → Return ExtractionResult(success=False, error="...")
   └─ Continue

2. Open .pages as zipfile
   └─ Extract file list

3. Check for 'Index/Document.iwa'
   ├─ If missing → Return ExtractionResult(success=False, error="Not IWA format")
   └─ Extract Document.iwa bytes

4. Decompress with Snappy
   ├─ snappy.decompress(iwa_bytes)
   ├─ If fails → Return ExtractionResult(success=False, error="Snappy decompression failed")
   └─ Continue with decompressed bytes

5. Parse protobuf using heuristics
   ├─ Iterate through protobuf message fields
   ├─ Identify text fields using heuristics (see below)
   ├─ Collect text chunks
   └─ If no text found → Return ExtractionResult(success=False, error="No text found")

6. Assemble final text
   ├─ Join chunks with '\n\n' (preserve paragraphs)
   ├─ Strip excessive whitespace
   └─ Validate minimum length (>50 chars)

7. Return success
   └─ ExtractionResult(text=full_text, success=True, extraction_method='iwa', ...)
```

#### 3. Text Extraction Heuristics

**Challenge**: Apple's protobuf schema is proprietary and undocumented.

**Solution**: Use heuristics to identify text content fields.

**Heuristics for identifying document text:**

| Check | Criteria | Purpose |
|-------|----------|---------|
| **Type** | Must be string/bytes field | Filter out numbers, bools |
| **Length** | `len(field) > 10` characters | Filter out metadata, IDs |
| **Content** | Contains whitespace (spaces) | Real text vs identifiers |
| **Encoding** | Valid UTF-8 | Ensure decodable |
| **Noise filter** | No XML tags, URLs, UUIDs | Exclude embedded metadata |

**Implementation pattern:**
```python
def _extract_text_from_protobuf(data: bytes) -> List[str]:
    """Extract text chunks from protobuf data using heuristics."""
    text_chunks = []

    # Since we don't have the schema, we'll use protobuf reflection
    # to iterate through all fields and identify text content

    # Pseudocode approach:
    # 1. Parse data as generic protobuf message
    # 2. Recursively traverse all fields
    # 3. For each string field:
    #    - Apply heuristics
    #    - If passes, add to text_chunks
    # 4. Return deduplicated, ordered chunks

    return text_chunks
```

**Text assembly rules:**
- Join chunks with `'\n\n'` to preserve paragraph structure
- Deduplicate repeated chunks (sometimes protobuf stores same text multiple times)
- Maintain document order where possible
- Strip leading/trailing whitespace per chunk

#### 4. Error Handling

**Failure modes and responses:**

| Failure Type | Detection | Response | Cascade Behavior |
|--------------|-----------|----------|------------------|
| **Missing dependencies** | `ImportError` on snappy/protobuf | Return failure with install instructions | Continue to PDF preview |
| **Not a .iwa file** | No `Index/Document.iwa` | Return failure silently | Continue to PDF preview |
| **Snappy error** | `snappy.UncompressError` | Return failure with error details | Continue to PDF preview |
| **Protobuf parse error** | Parsing exception | Return failure with error details | Continue to PDF preview |
| **No text found** | Empty text_chunks or len < 50 | Return failure | Continue to PDF preview |
| **Corrupted file** | Any unexpected exception | Return failure with exception message | Continue to PDF preview |

**All failures are non-fatal** - the extraction cascade continues to the next method.

#### 5. Integration Points

**Modified function: `_extract_pages()`**

```python
def _extract_pages(filepath: str) -> Dict:
    """
    Extract text and formatting from a .pages file.

    Tries multiple extraction methods in order:
    1. XML extraction (old format)
    2. IWA extraction (newer format) ← NEW
    3. PDF preview extraction (fallback)
    """
    # Validate is zipfile
    if not zipfile.is_zipfile(filepath):
        return ExtractionResult(...).to_dict()

    # Try XML-based extraction (old format)
    result = _try_xml_extraction(filepath)
    if result.success:
        return result.to_dict()

    # NEW: Try IWA extraction (newer format)
    result = _try_iwa_extraction(filepath)
    if result.success:
        return result.to_dict()

    # Try PDF preview extraction (fallback)
    result = _try_pdf_preview_extraction(filepath)
    if result.success:
        return result.to_dict()

    # All methods failed
    return ExtractionResult(
        text="",
        success=False,
        extraction_method='failed',
        error="Could not extract text. Please export to .docx or .pdf."
    ).to_dict()
```

**Return format** - ExtractionResult for IWA extraction:
```python
ExtractionResult(
    text=str,                    # Extracted text content
    success=True,
    extraction_method='iwa',
    formatting={
        'bold_spans': [],        # Future: could extract formatting
        'bullets': []            # Future: could extract bullet points
    },
    metadata={
        'filename': str,
        'file_hash': str,
        'extraction_date': str,
        'note': 'Extracted from IWA format'
    }
)
```

---

## Testing Strategy

### Unit Tests

**Location**: tests/test_text_extraction.py

**New test cases to add:**

1. **`test_iwa_extraction_success()`**
   - Use one of the 23 failing .pages files as a fixture
   - Call `_try_iwa_extraction(filepath)`
   - Assert `result['success'] == True`
   - Assert `result['extraction_method'] == 'iwa'`
   - Assert `len(result['text']) > 100`
   - Spot-check for expected content (e.g., known words from the document)

2. **`test_iwa_extraction_missing_dependencies()`**
   - Mock `import snappy` to raise `ImportError`
   - Call `_try_iwa_extraction(filepath)`
   - Assert `result['success'] == False`
   - Assert error message mentions missing dependency

3. **`test_iwa_extraction_no_document_iwa()`**
   - Create a test .pages file without `Index/Document.iwa`
   - Call `_try_iwa_extraction(filepath)`
   - Assert `result['success'] == False`

4. **`test_iwa_extraction_corrupt_data()`**
   - Create a .pages file with corrupted Document.iwa
   - Call `_try_iwa_extraction(filepath)`
   - Assert `result['success'] == False`
   - Assert does not raise exception (graceful failure)

5. **`test_extraction_cascade_with_iwa()`**
   - Use a .pages file that only has IWA format (no XML, no PDF)
   - Call `extract_text_from_document(filepath)`
   - Assert extraction succeeds via IWA method
   - Assert `result['extraction_method'] == 'iwa'`

6. **`test_extraction_cascade_fallback_from_iwa()`**
   - Mock `_try_iwa_extraction` to fail
   - Ensure file has PDF preview
   - Call `extract_text_from_document(filepath)`
   - Assert falls back to PDF preview method
   - Assert `result['extraction_method'] == 'pdf_preview'`

### Integration Tests

**Location**: tests/test_phase3_integration.py or new file

**Test case: `test_pipeline_with_iwa_pages_files()`**
- Run full pipeline on `my_documents/` folder
- Check that all 23 previously failing files now extract successfully
- Verify pipeline statistics show 0 extraction failures for .pages files
- Spot-check 2-3 extracted texts for quality

### Manual Validation

**Before merging:**

1. **Install dependencies**: `pip install python-snappy protobuf`
2. **Test single file manually**:
   ```python
   from utils.text_extraction import extract_text_from_document

   result = extract_text_from_document(
       "my_documents/2025-10-13 - Colburn School, Byrnes, Anthony - submitted.pages"
   )

   print(f"Success: {result['success']}")
   print(f"Method: {result['extraction_method']}")
   print(f"Text length: {len(result['text'])}")
   print(f"First 500 chars:\n{result['text'][:500]}")
   ```

3. **Compare with manual open**: Open the same file in Apple Pages, verify extracted text matches

4. **Run full pipeline**:
   ```python
   from core.orchestrator import run_full_pipeline

   result = run_full_pipeline(
       input_dir="my_documents/",
       output_dir="test_output/"
   )

   print(f"Processed: {result['statistics']['documents_processed']}")
   print(f"Errors: {len(result['errors'])}")
   ```

5. **Check for failures**: Verify all 23 files extracted successfully

---

## Implementation Plan

### Phase 1: Dependencies & Setup
**Tasks:**
1. Add `python-snappy>=0.6.1` to requirements.txt
2. Add `protobuf>=4.21.0` to requirements.txt
3. Install dependencies: `pip install -r requirements.txt`
4. Verify imports work: `python -c "import snappy; from google.protobuf import message"`

**Validation:** Dependencies installed successfully

---

### Phase 2: Core IWA Extraction Function
**Tasks:**
1. Create `_try_iwa_extraction(filepath: str) -> ExtractionResult` in utils/text_extraction.py
2. Implement steps:
   - Dependency checks (snappy, protobuf)
   - Zipfile opening and Document.iwa extraction
   - Snappy decompression
   - Basic protobuf parsing skeleton (can be refined later)
   - Text extraction heuristics
   - Result assembly
3. Add comprehensive docstring with examples

**Validation:** Function exists, handles basic cases

---

### Phase 3: Protobuf Text Extraction Heuristics
**Tasks:**
1. Implement `_extract_text_from_protobuf(data: bytes) -> List[str]` helper function
2. Use protobuf reflection to traverse message fields
3. Apply heuristics to identify text fields:
   - Type check (string/bytes)
   - Length check (>10 chars)
   - Content check (contains spaces)
   - Encoding validation (UTF-8)
   - Noise filtering (no XML, URLs, UUIDs)
4. Test on one real .pages file, iterate until text extraction works

**Validation:** Can extract meaningful text from at least one .iwa file

---

### Phase 4: Integration with Extraction Cascade
**Tasks:**
1. Modify `_extract_pages()` to call `_try_iwa_extraction()` between XML and PDF attempts
2. Ensure error handling works (failures cascade gracefully)
3. Test extraction cascade with different .pages file types:
   - Old format (XML) → should still use XML method
   - New format with PDF preview → should try IWA first
   - New format without PDF → should use IWA method

**Validation:** Integration works, no regressions on existing files

---

### Phase 5: Unit Testing
**Tasks:**
1. Add test fixture: Copy one failing .pages file to tests/fixtures/
2. Implement 6 unit tests listed in Testing Strategy section
3. Run tests: `python -m pytest tests/test_text_extraction.py -v -k iwa`
4. Fix any failures
5. Ensure all existing tests still pass: `python -m pytest tests/test_text_extraction.py -v`

**Validation:** All unit tests pass

---

### Phase 6: Integration Testing
**Tasks:**
1. Run full pipeline on my_documents/ folder:
   ```python
   from core.orchestrator import run_full_pipeline
   result = run_full_pipeline("my_documents/", "test_lexicons/")
   ```
2. Verify 0 extraction failures for .pages files
3. Spot-check 3 extracted texts for quality (compare with manual open)
4. Run full test suite: `python -m pytest tests/ -v`
5. Check performance (should not be significantly slower)

**Validation:** Pipeline succeeds, all 23 files extract successfully

---

### Phase 7: Error Handling & Edge Cases
**Tasks:**
1. Test with corrupted .pages file (intentionally corrupt Document.iwa)
2. Test with .pages file missing Document.iwa
3. Test graceful failure when dependencies missing (uninstall snappy temporarily)
4. Verify error messages are helpful to users
5. Add logging for debugging (optional)

**Validation:** All edge cases handled gracefully

---

### Phase 8: Documentation & Cleanup
**Tasks:**
1. Update docstring in `extract_text_from_document()` to mention IWA support
2. Update module docstring in text_extraction.py (lines 1-15)
3. Update README.md to mention IWA format support if needed
4. Add code comments explaining heuristics
5. Clean up any debug print statements

**Validation:** Code is clean, well-documented

---

### Phase 9: Final Validation
**Tasks:**
1. Run complete test suite: `python -m pytest tests/ -v`
2. Run full pipeline on my_documents/: `python -c "from core.orchestrator import run_full_pipeline; run_full_pipeline('my_documents/', 'my_lexicons/')"`
3. Verify all 23 files that previously failed now succeed
4. Commit changes with descriptive message

**Validation:** All tests pass, pipeline runs successfully on real data

---

## Implementation Code Skeleton

### 1. New Function Skeleton

```python
def _try_iwa_extraction(filepath: str) -> ExtractionResult:
    """
    Try to extract text from .iwa format .pages file (newer format).

    .iwa (iWork Archive) format is used by Pages 5.0+ (2013+).
    Files are stored as Snappy-compressed protobuf messages in Index/*.iwa.

    Args:
        filepath: Path to .pages file

    Returns:
        ExtractionResult with text content or failure details

    Examples:
        >>> result = _try_iwa_extraction("document.pages")
        >>> if result.success:
        ...     print(result.text)
    """
    # Check dependencies
    try:
        import snappy
        from google.protobuf import message
    except ImportError as e:
        return ExtractionResult(
            text="",
            success=False,
            extraction_method='iwa',
            error=f"Missing dependency for IWA extraction: {e}. Install with: pip install python-snappy protobuf"
        )

    try:
        # Extract Document.iwa from .pages archive
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            # Check for Document.iwa
            if 'Index/Document.iwa' not in zip_ref.namelist():
                return ExtractionResult(
                    text="",
                    success=False,
                    extraction_method='iwa',
                    error="No Index/Document.iwa found (not IWA format)"
                )

            # Read IWA file
            iwa_data = zip_ref.read('Index/Document.iwa')

        # Decompress with Snappy
        try:
            decompressed = snappy.decompress(iwa_data)
        except Exception as e:
            return ExtractionResult(
                text="",
                success=False,
                extraction_method='iwa',
                error=f"Snappy decompression failed: {str(e)}"
            )

        # Extract text from protobuf
        text_chunks = _extract_text_from_protobuf(decompressed)

        # Validate we found meaningful text
        if not text_chunks:
            return ExtractionResult(
                text="",
                success=False,
                extraction_method='iwa',
                error="No text content found in IWA file"
            )

        # Assemble final text
        full_text = '\n\n'.join(text_chunks)

        # Validate minimum length
        if len(full_text) < 50:
            return ExtractionResult(
                text="",
                success=False,
                extraction_method='iwa',
                error=f"Extracted text too short ({len(full_text)} chars)"
            )

        # Success!
        file_hash = _calculate_hash(filepath)

        return ExtractionResult(
            text=full_text,
            success=True,
            extraction_method='iwa',
            formatting={
                'bold_spans': [],  # Future enhancement
                'bullets': []
            },
            metadata={
                'filename': Path(filepath).name,
                'file_hash': file_hash,
                'extraction_date': str(__import__('datetime').datetime.now()),
                'note': 'Extracted from IWA format (Pages 5.0+)'
            }
        )

    except Exception as e:
        return ExtractionResult(
            text="",
            success=False,
            extraction_method='iwa',
            error=f"IWA extraction failed: {str(e)}"
        )


def _extract_text_from_protobuf(data: bytes) -> List[str]:
    """
    Extract text chunks from protobuf data using heuristics.

    Since Apple's protobuf schema is proprietary, we use heuristics
    to identify fields containing document text.

    Args:
        data: Decompressed protobuf data from Document.iwa

    Returns:
        List of text chunks (paragraphs) in document order
    """
    from google.protobuf import message
    from google.protobuf.message import DecodeError
    import re

    text_chunks = []
    seen_chunks = set()  # Deduplicate

    # TODO: Implement protobuf field traversal
    # Strategy:
    # 1. Try to parse as generic protobuf message
    # 2. Recursively traverse all fields
    # 3. For each string field, apply heuristics
    # 4. Collect qualifying text chunks

    # Heuristic helper function
    def is_likely_document_text(text: str) -> bool:
        """Apply heuristics to identify document text."""
        if not isinstance(text, str):
            try:
                text = text.decode('utf-8')
            except:
                return False

        # Must be reasonable length
        if len(text) < 10:
            return False

        # Must contain whitespace (real text vs identifiers)
        if ' ' not in text:
            return False

        # Filter out metadata patterns
        # URLs
        if re.match(r'https?://', text):
            return False
        # UUIDs
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-', text, re.IGNORECASE):
            return False
        # XML-like tags
        if '<' in text and '>' in text:
            return False

        return True

    # Parse protobuf and extract text
    # (Implementation note: this part will require experimentation
    #  with actual .iwa files to determine the best parsing approach)

    # Placeholder approach:
    # Try to find text by looking for valid UTF-8 strings in the data
    # This is a fallback heuristic if proper protobuf parsing fails

    try:
        # Attempt to find text strings in the binary data
        # Look for sequences that decode as UTF-8 and match our heuristics
        # This is a simplified approach - may need refinement

        potential_strings = []
        i = 0
        while i < len(data):
            # Look for length-prefixed strings (common in protobuf)
            if i + 2 < len(data):
                # Try reading a varint length
                length = data[i]
                if length > 10 and length < 10000:  # Reasonable text length
                    try:
                        text = data[i+1:i+1+length].decode('utf-8', errors='strict')
                        if is_likely_document_text(text):
                            if text not in seen_chunks:
                                potential_strings.append(text)
                                seen_chunks.add(text)
                    except UnicodeDecodeError:
                        pass
            i += 1

        text_chunks = potential_strings

    except Exception as e:
        # If parsing fails, return empty list
        # The calling function will handle this as a failure
        pass

    return text_chunks
```

### 2. Modified _extract_pages() Function

```python
def _extract_pages(filepath: str) -> Dict:
    """
    Extract text and formatting from a .pages file.

    Tries multiple extraction methods in order:
    1. XML extraction (old format, pre-2013)
    2. IWA extraction (newer format, Pages 5.0+)
    3. PDF preview extraction (fallback for files with embedded preview)

    Args:
        filepath: Path to .pages file

    Returns:
        Dictionary with extraction results
    """
    # .pages files are zip archives
    if not zipfile.is_zipfile(filepath):
        return ExtractionResult(
            text="",
            success=False,
            extraction_method='failed',
            error=f"Invalid .pages file (not a zip archive): {filepath}"
        ).to_dict()

    # Try XML-based extraction (old format)
    result = _try_xml_extraction(filepath)
    if result.success:
        return result.to_dict()

    # Try IWA extraction (newer format)  ← NEW
    result = _try_iwa_extraction(filepath)
    if result.success:
        return result.to_dict()

    # Try PDF preview extraction (fallback)
    result = _try_pdf_preview_extraction(filepath)
    if result.success:
        return result.to_dict()

    # Both methods failed
    return ExtractionResult(
        text="",
        success=False,
        extraction_method='failed',
        error=(
            f"Could not extract text from {filepath}. "
            "All extraction methods failed (XML, IWA, PDF preview). "
            "Please export to .docx or .pdf from Pages and re-run extraction."
        )
    ).to_dict()
```

---

## Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Protobuf heuristics don't work** | Medium | High | Build OCR fallback as backup plan |
| **Performance degradation** | Low | Medium | Profile and optimize; IWA parsing should be fast |
| **Apple changes format** | Low | Medium | Maintain XML/PDF fallbacks; document format version support |
| **Dependency installation issues** | Low | Low | Both dependencies are mature, widely used |
| **Text extraction incomplete** | Medium | Medium | Test extensively; refine heuristics based on results |
| **Breaking existing functionality** | Low | High | Comprehensive test suite prevents regressions |

---

## Success Criteria

**Implementation is complete when:**
- ✅ All 23 failing .pages files extract successfully
- ✅ Full test suite passes (331+ tests)
- ✅ New unit tests added and passing (6+ tests)
- ✅ Pipeline runs successfully on my_documents/ folder
- ✅ Spot-check: Extracted text matches manual inspection (3+ files)
- ✅ No performance degradation (pipeline runtime similar to before)
- ✅ Dependencies documented in requirements.txt
- ✅ Code documented with docstrings and comments

---

## References

### .IWA Format Resources
- Apple Pages file format: ZIP archive containing IWA files
- IWA files: Snappy-compressed protobuf messages
- Protobuf schema: Proprietary (TSP - TableStore Protocol)
- Format introduced: Pages 5.0 (2013)

### Dependencies
- **python-snappy**: https://pypi.org/project/python-snappy/
- **protobuf**: https://pypi.org/project/protobuf/

### Related Code Files
- `utils/text_extraction.py` - Main extraction logic (MODIFY)
- `tests/test_text_extraction.py` - Unit tests (ADD TESTS)
- `requirements.txt` - Dependencies (ADD)
- `core/orchestrator.py` - Pipeline coordinator (NO CHANGE)

---

## Notes for Implementation

1. **Start with exploration**: Before full implementation, experiment with one .pages file to understand the protobuf structure better. Use a Python REPL to inspect the decompressed data.

2. **Iterate on heuristics**: The text extraction heuristics may need refinement based on actual file content. Start simple, add filters as needed.

3. **Preserve backward compatibility**: Test with old-format .pages files to ensure XML extraction still works.

4. **Log for debugging**: Consider adding debug logging to track which extraction method succeeds for each file.

5. **Performance note**: Protobuf parsing is typically fast (< 100ms per file). If performance is an issue, consider caching or parallel processing.

6. **Future enhancements**: Once text extraction works, consider extracting:
   - Bold/italic formatting
   - Bullet points
   - Headings hierarchy
   - Tables

---

## Questions for Follow-up

- Should we add verbose logging to track extraction method usage?
- Should we cache IWA extraction results to speed up repeated processing?
- Do we need to handle password-protected .pages files?

---

**End of Design Document**

Ready for implementation in a new session.
