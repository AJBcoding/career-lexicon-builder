# Career Lexicon Builder

**A comprehensive Python toolkit for analyzing career documents and building targeted application materials**

Transform your career documents (resumes, cover letters) into an intelligent lexicon that identifies your strongest skills, tracks their evolution over time, and analyzes gaps against job requirements.

## 🎯 What It Does

The Career Lexicon Builder helps you:
1. **Analyze Documents**: Extract skills, experience, and qualifications from your resumes and cover letters
2. **Build Your Lexicon**: Aggregate skills across all documents with frequency and recency tracking
3. **Analyze Job Fit**: Compare your skills against job requirements and identify gaps
4. **Strategic Guidance**: Get actionable recommendations for resume and cover letter development

## ✨ Features

### Phase 2: Document Processing (✅ Complete)
- **Automatic Classification**: Identifies document types (resume, cover letter, job description)
- **Multi-Format Support**: PDF, Word (.docx), plain text (.txt, .md)
- **Metadata Extraction**: Dates, positions, organizations from filenames and content
- **Smart Caching**: SHA-256 hash-based change detection for incremental processing
- **84 tests passing** (100%)

### Phase 3: Term Extraction (✅ Complete)
- **Skill Detection**: Extracts 100+ common technical and soft skills
- **Context Analysis**: Identifies action verbs, quantifiers, and prominence scores
- **Multi-Level Categorization**: Domain (Technical, Business, Creative), Role, and Skill Level
- **102 tests passing** (100%)

### Phase 4: Lexicon Building & Gap Analysis (✅ Complete)
- **Aggregated Skills**: Unified skill inventory across all your documents
- **Recency & Frequency Scoring**: Prioritizes recent and frequently-used skills
- **Gap Analysis**: Compares your skills against job requirements
- **Strategic Recommendations**: Identifies transferable skills and bridging strategies
- **49 tests passing** for Phase 4, **151 total tests passing** (100%)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/AJBcoding/career-lexicon-builder.git
cd career-lexicon-builder

# Install dependencies
pip install -r requirements.txt

# Run tests to verify installation
python -m pytest tests/ -v
# Expected: 151 passed in ~0.8s
```

## 📦 Project Structure

```
career-lexicon-builder/
├── src/                          # 9 source modules
│   ├── document_processor.py     # Document classification
│   ├── text_extractor.py         # Multi-format text extraction
│   ├── metadata_extractor.py     # Date, position, org extraction
│   ├── cache_manager.py          # Smart caching
│   ├── term_extractor.py         # Skill extraction
│   ├── context_analyzer.py       # Context analysis
│   ├── term_categorizer.py       # Skill categorization
│   ├── lexicon_builder.py        # Skill aggregation
│   └── gap_analyzer.py           # Job fit analysis
├── tests/                        # 151 tests (100% passing)
├── skills/                       # Socratic Career Application Skills
├── docs/                         # Comprehensive documentation
└── data/                         # Data directories
```

## 📊 Test Coverage

**Total: 151/151 tests passing (100%)**

- Phase 2: 84 tests (Document Processing)
- Phase 3: 102 tests (Term Extraction)
- Phase 4: 49 tests (Lexicon Building)

## 📚 Documentation

See the `docs/` directory for:
- Complete phase reports
- Design documents
- Implementation guides
- Quick start guides

## 🛠️ Development

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific phase tests
python -m pytest tests/test_document_processor.py -v
python -m pytest tests/test_lexicon_builder.py -v
```

## 📄 License

MIT License - See LICENSE file for details

## 🎉 Status

✅ All phases complete (2-4)  
✅ All 151 tests passing  
✅ Ready for production use

---

**Last Updated**: October 28, 2025  
**Version**: 1.0.0
