# Pages Document Automation Design

**Date:** 2025-11-09
**Status:** Research Complete - Ready for Implementation
**Goal:** Programmatically format resume and cover letter content into styled templates

---

## Background

The career-lexicon-builder project generates high-quality career content through AI-powered analysis and Socratic career skills. However, the final step—formatting this content into professionally styled documents—remains manual.

**Current Workflow:**
1. Generate content using Socratic skills (markdown output)
2. Manually copy existing .pages resume/cover letter
3. Paste new content and reapply formatting by hand
4. Use "Paste and Match Style" to preserve document formatting

**Desired Workflow:**
1. Generate content using Socratic skills
2. Automatically format into styled template
3. Output professional resume/cover letter ready for submission

---

## Research Findings

### .pages File Format

**Current Structure (Pages 14.4):**
- .pages files are ZIP archives containing:
  - `.iwa` files (iWork Archive - Protocol Buffers format)
  - Binary, proprietary Apple schema
  - NOT human-readable XML (old format)
- Direct manipulation is complex and brittle

**Example:**
```bash
$ file "document.pages"
Zip archive data, at least v2.0 to extract

$ unzip -l "document.pages"
Index/Document.iwa          # Binary Protocol Buffer
Index/DocumentStylesheet.iwa # Style definitions (binary)
```

### AppleScript Capabilities for Pages

**What AppleScript CAN do:**
- ✅ Open/close documents
- ✅ Access `body text` property
- ✅ Set direct formatting: `font`, `size`, `color`
- ✅ Manipulate `paragraphs`, `characters`, `words`
- ✅ Use `placeholder text` with tags
- ✅ Export to PDF, Word, RTF, etc.

**What AppleScript CANNOT do:**
- ❌ List paragraph styles in a document
- ❌ Apply paragraph styles by name (e.g., "Heading 1", "Body Text")
- ❌ Query which style is applied to text
- ❌ Create or modify style definitions

**Critical Limitation:** Pages' AppleScript dictionary does not expose paragraph or character style management. You can only apply direct formatting, not named styles from templates.

### Word .docx Capabilities

**python-docx Library:**
- ✅ Full paragraph style support
- ✅ Character style support
- ✅ Apply styles by name
- ✅ Query existing styles
- ✅ Platform-independent (pure Python)

**Example:**
```python
from docx import Document

doc = Document('template.docx')

# Apply style by name
paragraph = doc.add_paragraph('Anthony Byrnes', style='Header')
paragraph = doc.add_paragraph('Experience...', style='full-cv-indent 2')
```

### .pages → .docx Conversion Test

**Test Results:**
- ✅ Custom styles preserved: `"full-cv-indent 2"`, `"Heading 3 A"`
- ✅ Standard styles preserved: `"Header"`, `"Normal"`
- ✅ One-time conversion via AppleScript works perfectly

**Conversion Code:**
```applescript
tell application "Pages"
    open POSIX file "/path/to/template.pages"
    export front document to POSIX file "/path/to/template.docx" as Microsoft Word
    close front document saving no
end tell
```

---

## Technical Approach Comparison

### Approach A: AppleScript Automation (Pages)

**Pros:**
- Uses official Pages app
- No file format reverse-engineering
- Works with native .pages files

**Cons:**
- ❌ Cannot apply named paragraph styles
- ❌ Limited to direct formatting (font, size, color)
- ❌ Slower (GUI automation)
- ❌ macOS-only
- ❌ Would lose template style benefits

**Verdict:** Not viable due to lack of style support

---

### Approach B: .docx with python-docx (Recommended)

**Pros:**
- ✅ Full paragraph and character style support
- ✅ Apply styles by name programmatically
- ✅ Platform-independent
- ✅ Fast (no GUI)
- ✅ Can leverage existing Office skills/MCP servers
- ✅ Integrates with career-lexicon-builder Python codebase

**Cons:**
- Requires one-time .pages → .docx template conversion
- Output is .docx instead of .pages (but easily convertible)

**Verdict:** Optimal approach

---

## Recommended Architecture

### High-Level Design

```
Content Source → Style Mapper → python-docx → Formatted .docx
    ↓                ↓              ↓              ↓
  .txt/.md      Pattern rules    Template    Resume/Cover Letter
  Claude AI      + Config         styles
```

### Components

#### 1. Template Converter (One-Time Setup)

**Purpose:** Convert .pages templates to .docx format

**Implementation:**
- AppleScript to export .pages → .docx
- Verify style preservation
- Store converted templates in `templates/` directory

**Script:**
```python
def convert_pages_to_docx(pages_path, docx_path):
    """Convert .pages template to .docx using AppleScript"""
    applescript = f'''
    tell application "Pages"
        open POSIX file "{pages_path}"
        export front document to POSIX file "{docx_path}" as Microsoft Word
        close front document saving no
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
```

#### 2. Style Mapper

**Purpose:** Map content patterns to .docx style names

**Configuration File** (`style_mappings.yaml`):
```yaml
resume:
  name_header: "Header"              # First line with name
  section_header: "Heading 3 A"       # Section titles
  body_text: "full-cv-indent 2"       # Experience descriptions
  bullet_list: "List Bullet"          # Achievement bullets

cover_letter:
  date: "full-cv-indent 2"
  recipient: "Header"
  salutation: "full-cv-indent 2"
  body_paragraph: "full-cv-indent 2"
  signature: "Normal"
```

**Pattern Inference Engine:**
```python
class StyleMapper:
    def infer_style(self, text: str, context: dict) -> str:
        """Infer appropriate style based on content pattern"""
        # First paragraph → name header
        if context['is_first'] and len(text.split()) <= 3:
            return self.config['name_header']

        # All caps or title case → section header
        if text.isupper() or text.istitle():
            return self.config['section_header']

        # Starts with bullet/dash → bullet list
        if text.startswith(('•', '-', '*')):
            return self.config['bullet_list']

        # Default body text
        return self.config['body_text']
```

#### 3. Document Generator

**Purpose:** Create formatted documents from templates

```python
from docx import Document

class DocumentGenerator:
    def __init__(self, template_path: str):
        self.template = Document(template_path)

    def generate_from_content(self, content: str, style_config: dict):
        """Generate formatted document from plain text content"""
        doc = Document(self.template)
        mapper = StyleMapper(style_config)

        paragraphs = content.split('\n\n')
        for i, para_text in enumerate(paragraphs):
            context = {
                'is_first': i == 0,
                'is_last': i == len(paragraphs) - 1,
                'position': i
            }

            style = mapper.infer_style(para_text, context)
            doc.add_paragraph(para_text, style=style)

        return doc
```

#### 4. Content Interface

**Dual Input Support:**

**A) File Input:**
```python
def format_from_file(template: str, content_file: str, output: str):
    """Format content from text/markdown file"""
    with open(content_file) as f:
        content = f.read()

    generator = DocumentGenerator(f'templates/{template}.docx')
    doc = generator.generate_from_content(content, load_config(template))
    doc.save(output)
```

**B) Claude-Generated Content:**
```python
def format_from_claude(template: str, content: str, output: str):
    """Format content directly from Claude AI"""
    generator = DocumentGenerator(f'templates/{template}.docx')
    doc = generator.generate_from_content(content, load_config(template))
    doc.save(output)
```

---

## Integration with Existing System

### Career Lexicon Builder Integration

**Current Flow:**
```
Lexicons → Socratic Skills → Markdown Output → Manual Formatting
```

**Enhanced Flow:**
```
Lexicons → Socratic Skills → Markdown Output → Document Generator → Formatted .docx
```

**Implementation in Socratic Skills:**

Modify `collaborative-writing` skill to optionally format output:

```python
# In collaborative-writing skill completion
if format_output:
    from document_formatter import format_from_claude

    format_from_claude(
        template='resume',  # or 'cover_letter'
        content=final_draft,
        output=f'output/{job_title}_resume.docx'
    )
```

---

## Directory Structure

```
career-lexicon-builder/
├── templates/                      # Converted .docx templates
│   ├── resume-template.docx
│   └── cover-letter-template.docx
│
├── formatters/                     # New formatting module
│   ├── __init__.py
│   ├── style_mapper.py             # Pattern → style mapping
│   ├── document_generator.py       # python-docx integration
│   ├── template_converter.py       # .pages → .docx conversion
│   └── style_mappings.yaml         # Style configuration
│
├── my_documents/                   # Original .pages files
│   └── *.pages
│
└── output/                         # Generated documents
    ├── resumes/
    └── cover-letters/
```

---

## Implementation Phases

### Phase 1: Template Setup (1-2 hours)

**Tasks:**
1. Select 2-3 best .pages templates (resume + cover letter)
2. Convert to .docx using AppleScript
3. Analyze styles in converted .docx files
4. Document style names and their purposes
5. Store templates in `templates/` directory

**Deliverable:** Converted templates with style documentation

---

### Phase 2: Core Formatting Engine (4-6 hours)

**Tasks:**
1. Install/verify python-docx in project venv
2. Implement `DocumentGenerator` class
3. Implement `StyleMapper` with pattern inference
4. Create `style_mappings.yaml` configuration
5. Write unit tests for style application

**Deliverable:** Working formatter that can apply styles to plain text

---

### Phase 3: Content Interface (2-3 hours)

**Tasks:**
1. Implement file input interface
2. Implement Claude AI direct content interface
3. Add CLI wrapper for manual usage
4. Create usage examples and documentation

**Deliverable:** Command-line tool for formatting documents

---

### Phase 4: Integration (3-4 hours)

**Tasks:**
1. Modify `collaborative-writing` skill to use formatter
2. Add optional formatting step to other career skills
3. Test end-to-end workflow
4. Update QUICKSTART_SOCRATIC_SKILLS.md

**Deliverable:** Integrated system with automated formatting

---

## Alternative Approaches Considered

### A) Keyboard Maestro / UI Automation
- **Rejected:** Too brittle, hard to debug, platform-specific
- Would simulate menu clicks to apply styles

### B) RTF with Style Definitions
- **Rejected:** Complex to maintain, limited format support
- Would extract/apply styles via RTF intermediate format

### C) Pages Placeholder Text
- **Partially viable:** Could work for simple templates
- Limited flexibility for dynamic content structures
- Would require fixed template structure

### D) Direct .iwa Manipulation
- **Rejected:** Too complex, proprietary format, brittle
- Would require reverse-engineering Protocol Buffer schemas

---

## Existing Tools and Skills

### Claude Office Skills
- Repository: `tfriedel/claude-office-skills`
- Provides: Document manipulation workflows
- Integration: Could adopt patterns from this project

### MCP Servers
- `Office-Word-MCP-Server`: Word document manipulation
- `document-edit-mcp`: Multi-format document support
- Consideration: May want to integrate with these in future

### python-docx
- Version: 1.2.0 (already installed in project)
- Documentation: https://python-docx.readthedocs.io/
- Status: Mature, well-maintained library

---

## Success Criteria

**Must Have:**
- ✅ Apply paragraph styles by name from templates
- ✅ Support both file and Claude-generated content input
- ✅ Preserve all formatting from original .pages templates
- ✅ Work with existing career lexicon builder workflows

**Should Have:**
- ✅ Pattern-based style inference (minimize manual markup)
- ✅ Configurable style mappings per template
- ✅ CLI tool for manual formatting
- ✅ Integration with Socratic career skills

**Nice to Have:**
- Support for markdown → .docx with style mapping
- Batch processing multiple documents
- Template style inheritance/variants
- Round-trip: .docx → .pages if needed

---

## Cost and Performance

**One-Time Costs:**
- Template conversion: ~5 minutes per template
- Style analysis and mapping: ~30 minutes per template

**Per-Document Costs:**
- Format generation: <1 second
- No API costs (pure Python, local processing)
- No GUI required (scriptable)

**Scalability:**
- Can format hundreds of documents per minute
- Memory: Minimal (~10MB per document)
- CPU: Negligible (< 100ms per document)

---

## Risks and Mitigations

### Risk 1: Style Name Changes
**Problem:** .pages → .docx conversion might alter style names
**Mitigation:**
- Test conversion with multiple templates
- Document all style name mappings
- Add validation to check style existence

### Risk 2: Format Compatibility
**Problem:** Some .pages features might not convert to .docx
**Mitigation:**
- Keep original .pages templates as source of truth
- Test conversion with complex formatting
- Document any limitations

### Risk 3: Pattern Inference Accuracy
**Problem:** Automatic style mapping might mis-identify content
**Mitigation:**
- Start with explicit style configuration
- Add override mechanisms
- Collect feedback and refine patterns

### Risk 4: Template Versioning
**Problem:** Templates evolve, styles change over time
**Mitigation:**
- Version control templates in git
- Tag template versions in config
- Support multiple template variants

---

## Next Steps

### Immediate (Next Session):
1. Select best resume and cover letter .pages templates
2. Convert to .docx and analyze styles
3. Create `style_mappings.yaml` for first template
4. Implement basic `DocumentGenerator`

### Short-Term (This Week):
1. Complete Phase 1 (Template Setup)
2. Complete Phase 2 (Core Formatting Engine)
3. Create demo with sample content

### Medium-Term (Next 2 Weeks):
1. Complete Phase 3 (Content Interface)
2. Complete Phase 4 (Integration)
3. Document and test full workflow

### Long-Term (Future):
1. Consider .docx → .pages conversion for final output
2. Explore integration with MCP servers
3. Add batch processing capabilities
4. Create template gallery with multiple styles

---

## References

**Documentation:**
- python-docx: https://python-docx.readthedocs.io/
- Pages AppleScript Dictionary: `/Applications/Pages.app` (sdef)
- Office Skills: https://github.com/tfriedel/claude-office-skills

**Research Files:**
- Test conversion: `/tmp/test-conversion.docx`
- Pages dictionary: `/tmp/pages_dictionary.xml`

**Related Project Files:**
- `README.md`: Project overview
- `QUICKSTART_SOCRATIC_SKILLS.md`: Skills usage guide
- `docs/plans/2025-10-31-socratic-career-skills-implementation.md`: Skills design

---

## Appendix: Example Code

### Full Working Example

```python
#!/usr/bin/env python3
"""
Document Formatter - Example Usage

Generate formatted resume from plain text content.
"""

from docx import Document
from pathlib import Path

def format_resume(content: str, template_path: str, output_path: str):
    """
    Format resume content with styles from template.

    Args:
        content: Plain text resume content
        template_path: Path to .docx template with styles
        output_path: Where to save formatted document
    """
    # Load template (copies all styles)
    doc = Document(template_path)

    # Simple style mapping
    style_map = {
        'first_line': 'Header',           # Name
        'section': 'Heading 3 A',         # Section headers
        'bullet': 'List Bullet',          # Achievements
        'default': 'full-cv-indent 2'     # Body text
    }

    # Process content
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue

        # Infer style
        if i == 0:
            style = style_map['first_line']
        elif line.isupper():
            style = style_map['section']
        elif line.startswith(('•', '-', '*')):
            style = style_map['bullet']
            line = line.lstrip('•-* ')
        else:
            style = style_map['default']

        # Add paragraph with style
        doc.add_paragraph(line, style=style)

    # Save
    doc.save(output_path)
    print(f"✓ Formatted resume saved to: {output_path}")


if __name__ == '__main__':
    # Example content
    resume_content = """Anthony Byrnes
PROFESSIONAL EXPERIENCE
UCLA CAO
• Led strategic initiatives for arts programming
• Managed $2M budget with 15% efficiency gains
EDUCATION
Master of Arts, Arts Administration"""

    # Format
    format_resume(
        content=resume_content,
        template_path='templates/resume-template.docx',
        output_path='output/anthony-byrnes-resume.docx'
    )
```

### Template Conversion Script

```python
#!/usr/bin/env python3
"""Convert .pages templates to .docx"""

import subprocess
from pathlib import Path

def convert_template(pages_path: Path, docx_path: Path):
    """Convert .pages to .docx via AppleScript"""
    script = f'''
    tell application "Pages"
        open POSIX file "{pages_path.absolute()}"
        set theDoc to front document
        export theDoc to POSIX file "{docx_path.absolute()}" as Microsoft Word
        close theDoc saving no
    end tell
    '''

    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✓ Converted: {pages_path.name} → {docx_path.name}")
    else:
        print(f"✗ Error: {result.stderr}")


if __name__ == '__main__':
    templates_dir = Path('my_documents')
    output_dir = Path('templates')
    output_dir.mkdir(exist_ok=True)

    # Convert specific templates
    templates = [
        '2025-11-09 - ucla cao byrnes, Anthony.pages',
        # Add more templates here
    ]

    for template in templates:
        pages_path = templates_dir / template
        docx_path = output_dir / template.replace('.pages', '.docx')
        convert_template(pages_path, docx_path)
```

---

**End of Design Document**
