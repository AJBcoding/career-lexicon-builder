# Quick Start Guide - Career Lexicon Builder

## Running the Code

### Prerequisites
```bash
pip install pytest pdfplumber python-docx --break-system-packages
```

### Test the Implementation

```bash
cd /home/claude/career-lexicon-builder
python -m pytest tests/ -v
```

Expected output:
```
======================== 43 passed in 0.40s ========================
```

## Example Usage

### 1. Classify a Document

```python
from src.document_processor import DocumentClassifier

# Sample document text
document_text = """
JOHN DOE
Software Engineer

EDUCATION
BS Computer Science, University, 2020

EXPERIENCE
Senior Engineer | Company | 2020-Present
- Developed scalable systems
- Led engineering teams
"""

# Classify
classifier = DocumentClassifier()
result = classifier.classify(document_text)

print(f"Document Type: {result.document_type.value}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Reasoning: {result.reasoning}")
```

Output:
```
Document Type: resume
Confidence: 0.85
Reasoning: Classified as resume with strong confidence (0.85). Found 8 characteristic patterns.
```

### 2. Extract Text from PDF

```python
from src.text_extractor import TextExtractor

extractor = TextExtractor()
result = extractor.extract("path/to/resume.pdf")

if result.success:
    print(f"Extracted {len(result.text)} characters")
    print(f"Pages: {result.metadata['page_count']}")
    print(f"Hash: {result.metadata['file_hash'][:16]}...")
else:
    print(f"Error: {result.error}")
```

### 3. Complete Pipeline

```python
from src.text_extractor import TextExtractor
from src.document_processor import DocumentProcessor

# Extract text
extractor = TextExtractor()
extraction = extractor.extract("resume.pdf")

if extraction.success:
    # Classify document
    processor = DocumentProcessor()
    classification = processor.process_document(
        extraction.text,
        filename=extraction.metadata['filename']
    )
    
    print(f"File: {classification['filename']}")
    print(f"Type: {classification['document_type']}")
    print(f"Confidence: {classification['confidence']:.2f}")
    print(f"Text Length: {classification['text_length']} characters")
```

## Testing Individual Components

### Test Document Classifier
```bash
python -m pytest tests/test_document_processor.py -v
```

### Test Text Extractor
```bash
python -m pytest tests/test_text_extractor.py -v
```

### Test Specific Test
```bash
python -m pytest tests/test_document_processor.py::TestDocumentClassifier::test_classify_resume -v
```

## Interactive Python Session

```python
# Start Python
python

# Import modules
from src.document_processor import DocumentClassifier, DocumentType
from src.text_extractor import TextExtractor

# Create instances
classifier = DocumentClassifier()
extractor = TextExtractor()

# Test classification
test_text = "Dear Hiring Manager, I am writing to apply..."
result = classifier.classify(test_text)
print(result)

# Check supported formats
print(extractor.get_supported_extensions())
```

## Common Operations

### Check if File is Supported
```python
from pathlib import Path
from src.text_extractor import TextExtractor

extractor = TextExtractor()
file_ext = Path("document.pdf").suffix.lower()

if file_ext in extractor.get_supported_extensions():
    print("Supported!")
else:
    print(f"Unsupported format: {file_ext}")
```

### Batch Process Multiple Files
```python
from pathlib import Path
from src.text_extractor import TextExtractor
from src.document_processor import DocumentProcessor

extractor = TextExtractor()
processor = DocumentProcessor()

# Process all PDFs in a directory
for pdf_file in Path("data/resumes").glob("*.pdf"):
    extraction = extractor.extract(str(pdf_file))
    
    if extraction.success:
        classification = processor.process_document(
            extraction.text,
            filename=pdf_file.name
        )
        
        print(f"{pdf_file.name}: {classification['document_type']} "
              f"({classification['confidence']:.2f})")
```

### Adjust Confidence Threshold
```python
from src.document_processor import DocumentClassifier

# Stricter classification (fewer false positives)
strict_classifier = DocumentClassifier(min_confidence=0.8)

# More lenient classification (fewer false negatives)
lenient_classifier = DocumentClassifier(min_confidence=0.5)

result = strict_classifier.classify(document_text)
```

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Run from project root:
```bash
cd /home/claude/career-lexicon-builder
python -m pytest tests/
```

### Encoding Error
```
UnicodeDecodeError: ...
```

**Solution**: Text extractor tries multiple encodings automatically. If all fail, the file may be binary or corrupted.

### Low Confidence Classification
```
Document classified as UNKNOWN with confidence 0.45
```

**Solution**: Document may be ambiguous or have mixed characteristics. Review the reasoning field for details. Consider manual classification or providing more context in the document.

## Next Steps

After Phase 2.3 is complete, you'll be able to:
1. Extract metadata (dates, positions, organizations)
2. Cache processed documents
3. Run incremental analysis on document collections
4. Generate lexicon outputs

Stay tuned for updates!

---

**Quick Reference Card**

```python
# Classification
from src.document_processor import DocumentClassifier
classifier = DocumentClassifier()
result = classifier.classify(text)

# Extraction
from src.text_extractor import extract_text
text, metadata = extract_text("file.pdf")

# Combined
from src.document_processor import DocumentProcessor
processor = DocumentProcessor()
result = processor.process_document(text, filename="file.pdf")

# Supported formats
extractor.get_supported_extensions()
# => ['.pdf', '.docx', '.txt', '.md']
```
