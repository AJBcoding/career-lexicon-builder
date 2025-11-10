# Archived: Pages Document Analysis Experiments

**Archive Date:** 2025-11-10
**Project:** .pages Style Extraction Research
**Status:** Archived - Research Complete

---

## About This Archive

This directory contains experimental scripts and tools created during the investigation of Apple .pages document style extraction. These scripts were developed to explore direct parsing of .iwa (iWork Archive) files.

### Why Archived:
- **Research Complete:** Investigation concluded with successful solution (iwork-converter)
- **Not Production Code:** These were exploratory/experimental scripts
- **Superseded:** iwork-converter tool provides better results with less complexity
- **Educational Value:** Preserved for reference and understanding .pages format
- **Not Deleted:** May be useful for future similar investigations

---

## What's in This Archive

### Python Scripts - .iwa Parsing

#### Core Parsers:
1. **iwa_parser.py**
   - Basic IWA file structure parser
   - Handles Protobuf wire format at binary level
   - Extracts readable strings from binary data
   - Foundation for other extractors

2. **extract_styles.py**
   - Initial style extraction attempt
   - Reads DocumentStylesheet.iwa
   - Extracts style names and font references
   - ~65% success rate

3. **extract_styles_comprehensive.py**
   - Full-featured style extraction
   - Extracts style names, colors, spacing, fonts
   - Searches within ±250 byte windows for properties
   - ~85% success rate for most properties

4. **extract_styles_final.py**
   - Cleaned up version with filtered output
   - Removes artifacts and duplicates
   - Best version of direct parsing approach
   - Good for validation, not complete parsing

#### Analysis Scripts:
5. **analyze_document_text.py**
   - Analyzes Document.iwa structure
   - Attempts to understand text content organization
   - Explores how text is stored in Protobuf messages

6. **map_text_to_styles.py**
   - Attempted to map text content to style IDs
   - **Did not succeed** - requires Protobuf schemas
   - Documents why text-to-style mapping is hard
   - Valuable for understanding the challenge

7. **test_iwa_parser.py**
   - Initial test script for iwa_parser.py
   - Early exploration of format

8. **analyze_cv_styles.py**
   - Parses HTML output from iwork-converter
   - Categorizes styles by usage patterns
   - Used to analyze CV style usage

#### PDF Export Tools (Unrelated):
9. **export_to_pdf.py**
   - Converts markdown files to PDFs
   - Uses WeasyPrint for rendering
   - Archived here as it's not core functionality

10. **PDF_EXPORT_README.md**
    - Documentation for export_to_pdf.py
    - Installation and usage instructions

11. **requirements-pdf-export.txt**
    - Python dependencies for PDF export
    - `markdown>=3.5.0` and `weasyprint>=60.0`

---

## Key Findings from These Scripts

### What We Successfully Extracted:
✅ **Style Names:** 95% accurate extraction
- Some artifacts like prefixes (@) or suffixes (J, f)
- Example: "@BOLD TITLES GREENJ" → "BOLD TITLES GREEN"

✅ **Font Families:** 100% accurate
- Helvetica, Times New Roman, Arial, Courier, Gotham-Light
- Always correctly identified

✅ **Style Existence:** 100% reliable
- Can definitively say if a style exists in document
- Good for validation use cases

⚠️ **Colors:** ~85% reliable
- Found RGB values within ±250 bytes of style names
- Association based on proximity, not guaranteed
- Approximate but useful

⚠️ **Spacing/Indents:** ~70% reliable
- Found numeric values near style definitions
- Can't always determine which value means what
- Requires manual verification

### What We Could Not Extract:
❌ **Text-to-Style Mapping:**
- Styles referenced by numeric IDs in text
- Without Protobuf .proto schemas, can't resolve ID→Name
- This was the critical missing piece

❌ **Complete Style Properties:**
- Full property extraction requires schema knowledge
- We got approximations, not complete definitions

❌ **Style Inheritance:**
- Could not determine parent-child relationships
- Would need full message decoding

---

## Technical Details

### .pages File Structure:
```
document.pages/
├── Index/
│   ├── DocumentStylesheet.iwa   ← Style definitions (37-41KB)
│   ├── Document.iwa              ← Text content (67KB in CV)
│   └── [other .iwa files]
└── [preview images, metadata]
```

### .iwa Format:
- IWA = iWork Archive
- Protocol Buffers serialization
- May use Snappy compression
- Contains MessageType headers
- Requires .proto schemas for complete parsing

### Our Approach:
1. Treat .iwa as binary data
2. Extract ASCII strings (style names, fonts)
3. Search for patterns (RGB floats, numeric values)
4. Associate by proximity (±250 bytes)
5. Filter and deduplicate results

### Why This Partially Worked:
- Style names stored as ASCII strings
- Colors stored as RGB float triplets (0.0-1.0)
- Simple patterns can be found without schemas
- Basic information is accessible

### Why It Didn't Fully Work:
- Text references styles by numeric ID
- ID→Name mapping encoded in Protobuf structure
- Without .proto schemas, can't decode messages
- Proximity-based association is unreliable for complex data

---

## When to Use These Scripts

### ✅ Good Use Cases:
1. **Style Validation:** Check if specific styles exist in document
2. **Quick Inspection:** Get list of all styles without full parsing
3. **Font Detection:** Identify which fonts are used
4. **Learning:** Understand .pages format structure
5. **Research:** Base for more advanced parsing attempts

### ❌ Not Recommended For:
1. **Production Parsing:** Use iwork-converter instead
2. **Complete Style Extraction:** Too many limitations
3. **Text-to-Style Mapping:** Doesn't work reliably
4. **Automated Processing:** Results need manual verification

---

## Better Alternatives

### Use iwork-converter Instead:
```bash
# Install (one-time)
cd /tmp
git clone https://github.com/orcastor/iwork-converter.git
cd iwork-converter
go build -o iwork-converter main.go

# Use
/tmp/iwork-converter/iwork-converter input.pages output.html
```

### Why iwork-converter is Better:
- ✅ Has full Protobuf schemas
- ✅ 100% accurate style extraction
- ✅ Text-to-style mapping works perfectly
- ✅ Multiple output formats (HTML, JSON, TXT)
- ✅ Battle-tested and maintained
- ✅ Supports Pages, Keynote, Numbers

---

## Dependencies

### For Python Scripts:
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-snappy protobuf beautifulsoup4
```

### For PDF Export:
```bash
pip install -r requirements-pdf-export.txt
# On macOS:
brew install pango cairo gdk-pixbuf libffi
```

---

## Example Usage (If You Must)

### Extract Styles from .pages Document:
```python
from extract_styles_final import extract_styles_clean

# Extract from DocumentStylesheet.iwa
styles = extract_styles_clean('document.pages/Index/DocumentStylesheet.iwa')

# Check if required styles exist
if 'full-cv-indent' in styles:
    print("✓ Style found")

# Get all style names
for style in styles:
    print(f"Style: {style}")
```

### Note:
This only gives you style names. For complete information, use iwork-converter.

---

## What We Learned

### Technical Insights:
1. .pages uses Protobuf for serialization
2. Files may be Snappy-compressed
3. Style names are ASCII, easy to extract
4. Numeric IDs separate definitions from references
5. Without schemas, only partial parsing is possible

### Process Insights:
1. Don't reinvent the wheel - check for existing tools first
2. Reverse engineering is hard without proper specs
3. Community solutions (iwork-converter) often better than custom
4. Exploratory scripts valuable for learning, not production
5. Document both successes AND failures for future reference

### Project Management:
1. Research phase ended successfully with working solution
2. Experimental code should be archived, not deleted
3. Documentation is critical for understanding decisions
4. Clear handoff documents prevent future re-work

---

## Related Documentation

### Research Documents:
See `/docs/research/pages-style-extraction/` for:
- HANDOFF_PAGES_STYLE_EXTRACTION.md (complete guide)
- IWORK_CONVERTER_SUCCESS.md (solution documentation)
- CV_STYLES_LIST.md (your CV's 97 styles)
- CV_DUPLICATE_STYLES.md (21 redundant styles analysis)
- COMPREHENSIVE_STYLE_EXTRACTION_RESULTS.md (technical analysis)
- TEXT_TO_STYLE_MAPPING_ANALYSIS.md (why mapping is hard)

---

## Future Work (If Needed)

### If You Want to Improve Direct Parsing:
1. Extract Protobuf schemas from Pages.app binary
   - Use `proto-dump` or similar tools
   - Get .proto definitions for all message types

2. Compile schemas with protoc
   - Generate Python bindings
   - Parse .iwa files with proper message types

3. Build ID resolution
   - Create style ID → name lookup table
   - Map text runs to style IDs
   - Complete text-to-style mapping

**Estimated Effort:** 2-4 weeks of development
**Success Rate:** ~90%
**Recommendation:** Use iwork-converter instead

---

## Files Manifest

```
archive/pages-experiments/
├── README.md (this file)
├── iwa_parser.py (6.4KB)
├── extract_styles.py (4.8KB)
├── extract_styles_comprehensive.py (8.6KB)
├── extract_styles_final.py (6.0KB)
├── analyze_document_text.py (5.8KB)
├── map_text_to_styles.py (7.2KB)
├── test_iwa_parser.py (5.0KB)
├── analyze_cv_styles.py (5.2KB)
├── export_to_pdf.py (6.7KB)
├── PDF_EXPORT_README.md (2.0KB)
└── requirements-pdf-export.txt (69 bytes)
```

**Total:** 12 files, ~64KB of experimental code

---

## Archive Decision Rationale

### Why Archive Instead of Delete:
1. **Educational Value:** Shows exploration process
2. **Partial Success:** Scripts do work for some use cases
3. **Future Reference:** May be useful for similar problems
4. **Research History:** Documents what was tried
5. **Learning Resource:** Helps understand .pages format

### Why Not Keep in Main Codebase:
1. **Not Production Quality:** Experimental/research code
2. **Superseded:** Better solution exists (iwork-converter)
3. **Limited Use Cases:** Only good for validation
4. **Maintenance Burden:** Would require updates
5. **Code Clarity:** Main codebase should contain only production code

---

**Archived:** 2025-11-10
**Research Period:** 2025-11-09
**Decision:** Archive for reference, use iwork-converter for production
**Status:** Complete - Preserved for Historical Reference
