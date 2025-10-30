# Phase 2 - Start Here

**Quick start guide for new Claude session**

## 1. Verify Current State (30 seconds)

```bash
cd /Users/anthonybyrnes/PycharmProjects/career-lexicon-builder
python -m pytest tests/ -v
```

**Expected**: `55 passed in 0.17s` ✅

If tests fail, something is wrong. Check Python environment.

## 2. Read Handoff Document (5 minutes)

```bash
open DevArtifacts/HANDOFF-PHASE-2.md
```

This 475-line document contains everything you need:
- What Phase 1 built
- What Phase 2 needs to build
- Detailed function signatures
- Test requirements
- Architecture decisions

**TL;DR**: Read sections "Current Project State" and "Phase 2: Document Classification & State Management"

## 3. Start Coding (Phase 2)

### Order of Implementation

**Task 1**: `core/confidence_scorer.py` (30 min)
```bash
# Create file and tests
touch core/confidence_scorer.py
touch tests/test_confidence_scorer.py
```

Write tests first, then implement:
```python
def calculate_confidence(
    criteria: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """Calculate weighted confidence score."""
    # Returns 0.0-1.0
```

**Task 2**: `core/document_processor.py` (2 hours)
```bash
touch core/document_processor.py
touch tests/test_document_processor.py
```

Pattern-based classification:
- Resume: "experience", "education", date ranges
- Cover letter: "Dear", "Sincerely", first person
- Job description: "requirements", "we are seeking"

**Task 3**: `core/state_manager.py` (2 hours)
```bash
touch core/state_manager.py
touch tests/test_state_manager.py
```

JSON manifest in `.lexicon-cache/manifest.json`:
- Track processed documents
- Detect file changes (hash-based)
- Enable incremental processing

## 4. Files to Reference

**Must read**:
- `DevArtifacts/HANDOFF-PHASE-2.md` - Complete context
- `DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md` (lines 115-235)

**Can reference**:
- `utils/date_parser.py` - Example of clean implementation
- `utils/text_extraction.py` - Example of multi-format handling
- `tests/test_*.py` - Example test structure

**Don't reference**:
- `archive/2025-10-29-skill-based-implementation/*` - Wrong approach

## 5. Success Criteria

Phase 2 complete when:
- [ ] All Phase 1 tests still passing (55/55)
- [ ] `core/confidence_scorer.py` with tests
- [ ] `core/document_processor.py` with tests
- [ ] `core/state_manager.py` with tests
- [ ] Integration test showing full Phase 2 pipeline
- [ ] Total tests: 80+ passing

## Quick Commands

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_confidence_scorer.py -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=utils

# Check test count
python -m pytest tests/ --collect-only | grep "test session starts" -A 1
```

## Design Document Links

- **Design**: [2025-01-27-career-lexicon-builder-design.md](../DesignDocuments/2025-01-27-career-lexicon-builder-design.md)
- **Implementation**: [2025-01-27-career-lexicon-builder-implementation.md](../DesignDocuments/2025-01-27-career-lexicon-builder-implementation.md)
- **Handoff**: [HANDOFF-PHASE-2.md](HANDOFF-PHASE-2.md)
- **Phase 1 Summary**: [PHASE-1-COMPLETE-SUMMARY.md](PHASE-1-COMPLETE-SUMMARY.md)

## Key Principle

**Follow the implementation plan exactly.** It specifies:
- Function signatures
- Data structures
- Test requirements

This ensures smooth integration with Phase 3+.

---

**Ready?** Start with `core/confidence_scorer.py` - it's simple and has no dependencies.
