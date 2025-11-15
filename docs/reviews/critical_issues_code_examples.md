# Career Lexicon Builder - Critical Issues with Code Examples

## P0 Issue #1: Circular Dependencies - Dependency Inversion Violation

### Current Problem (WRONG)
```
File: core/state_manager.py (line 14)
─────────────────────────────────────────────────
from core.document_processor import DocumentType

@dataclass
class DocumentRecord:
    filepath: str
    file_hash: str
    document_type: str  # Stored as string
    ...

def get_documents_by_type(manifest: ProcessingManifest, doc_type: DocumentType):
    # State manager depends on classification types
    doc_type_str = doc_type.value
    return [
        record for record in manifest.documents.values()
        if record.document_type == doc_type_str
    ]


File: core/document_processor.py (line 14)
──────────────────────────────────────────
from core.confidence_scorer import calculate_confidence

class DocumentType(Enum):  # DEFINED HERE
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"

def classify_document(filepath: str, text: str) -> Tuple[DocumentType, float, str]:
    # Returns DocumentType
    ...
```

### The Issue
- `state_manager.py` imports `DocumentType` from `document_processor.py`
- `document_processor.py` depends on `confidence_scorer.py`
- This chain creates:
  - Import dependencies: state_manager → document_processor → confidence_scorer
  - Logical dependencies: where enum lives affects who can import it
  - Testing burden: can't test state_manager without loading document_processor

### The Fix (CORRECT)

**Step 1: Create core/types.py**
```python
# File: core/types.py
"""Shared types for Career Lexicon Builder."""

from enum import Enum

class DocumentType(Enum):
    """Document type classifications."""
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"
```

**Step 2: Update core/state_manager.py**
```python
# File: core/state_manager.py
# REMOVE: from core.document_processor import DocumentType
# ADD:
from core.types import DocumentType

@dataclass
class DocumentRecord:
    filepath: str
    file_hash: str
    document_type: str  # Still stored as string for JSON
    date_processed: str
    date_from_filename: Optional[str]
    extraction_success: bool

def get_documents_by_type(
    manifest: ProcessingManifest,
    doc_type: DocumentType
) -> List[DocumentRecord]:
    """Get all documents of a specific type from manifest."""
    doc_type_str = doc_type.value
    return [
        record for record in manifest.documents.values()
        if record.document_type == doc_type_str
    ]
```

**Step 3: Update core/document_processor.py**
```python
# File: core/document_processor.py
# REMOVE: from enum import Enum ... class DocumentType(Enum):
# ADD:
from core.types import DocumentType
from core.confidence_scorer import calculate_confidence

def classify_document(filepath: str, text: str) -> Tuple[DocumentType, float, str]:
    """Classify document using filename and content analysis."""
    # Uses DocumentType from core.types
    ...
```

### Result
```
BEFORE:                          AFTER:
orchestrator                     orchestrator
  ├→ state_manager                ├→ state_manager
  │   └→ document_processor   →    ├→ document_processor
  │       └→ confidence_scorer     ├→ confidence_scorer
  └→ other imports                 └→ other imports
                                   
              core/types.py
                  ↑
        (all depend on types)
```

---

## P0 Issue #2: God Object - HierarchicalMarkdownGenerator

### Current Problem (WRONG - 782 LOC in one class)

```python
# File: generators/hierarchical_generator.py (782 lines)
class HierarchicalMarkdownGenerator:
    """Generates hierarchical markdown from LLM analysis results."""
    
    def __init__(self):
        self.generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def generate_all(self, analysis_results: Dict[str, Any], output_dir: str):
        """Generate all four lexicons."""
        # 26 lines handling all 4 document types
        files = {}
        files['philosophy'] = self.generate_philosophy(...)
        files['achievements'] = self.generate_achievements(...)
        files['narratives'] = self.generate_narratives(...)
        files['language'] = self.generate_language_bank(...)
        return files
    
    def generate_philosophy(self, data: Dict[str, Any], output_path: str):
        """Generate Career Philosophy & Values lexicon."""
        # 60 lines - handles Section I, II, III
        # Lines 67-82: TOC generation
        # Lines 84-110: Multiple section handling
        # Lines 112-114: File writing
        
    def generate_achievements(self, data: Dict[str, Any], output_path: str):
        """Generate Achievement Library lexicon."""
        # 39 lines - completely different structure
        
    def generate_narratives(self, data: Dict[str, Any], output_path: str):
        """Generate Narrative Patterns lexicon."""
        # 56 lines - completely different structure
        
    def generate_language_bank(self, data: Dict[str, Any], output_path: str):
        """Generate Language Bank lexicon."""
        # 61 lines - completely different structure
    
    # Plus 11 helper methods with duplicated logic:
    def _format_philosophy_item(self, item: Dict, heading: str, level: int):
        # 72 lines
    
    def _format_value_item(self, item: Dict, heading: str, level: int):
        # 49 lines - similar to philosophy_item
    
    def _format_achievement(self, achievement: Dict, number: str):
        # 105 lines - large, complex
    
    # ... 6 more format methods with similar code patterns
```

### Why This Is A Problem

1. **Single Responsibility Principle Violated** - One class for 4 document types
2. **Code Duplication** - Same patterns repeated:
   ```python
   # Pattern 1: Lines 496-504 in _format_narrative_pattern()
   if 'examples' in pattern and pattern['examples']:
       lines.append("#### Examples")
       for ex in pattern['examples']:
           if 'source' in ex:
               lines.append(f"**From**: {ex['source']}")
           lines.append(f"> {ex.get('text', '')}")
   
   # Same pattern at lines 551-562
   if 'examples' in formula and formula['examples']:
       lines.append("#### Examples")
       for ex in formula['examples']:
           lines.append(f"**Text**: {ex.get('text', '')}")
   
   # And again at lines 721-726
   if 'examples' in template:
       lines.append("**Examples**:")
       for ex in template['examples']:
           lines.append(f"> {ex.get('filled_example', '')}")
   ```

3. **Hard to Test** - Each test must set up entire class and verify entire generation
4. **Hard to Modify** - Change to philosophy format might break achievements

### The Fix (CORRECT)

**Architecture:**
```
generators/
├── base_generator.py         # Shared formatting utilities
├── markdown_formatter.py      # Base class for all generators
├── philosophy_generator.py    # ~90 lines
├── achievements_generator.py  # ~80 lines
├── narratives_generator.py    # ~85 lines
├── language_generator.py      # ~90 lines
└── orchestrator.py           # ~15 lines
```

**Step 1: Create base_generator.py**
```python
# File: generators/base_generator.py
"""Base generator with shared formatting utilities."""

from typing import Dict, Any, List
from datetime import datetime

class MarkdownFormatter:
    """Shared formatting utilities for all generators."""
    
    def __init__(self):
        self.generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def _format_examples(self, items: List[Dict], level: int) -> List[str]:
        """Format examples section (used by multiple generators)."""
        lines = []
        if not items:
            return lines
        
        lines.append(f"{'#' * (level + 1)} Examples")
        lines.append("")
        
        for item in items:
            if 'source' in item:
                lines.append(f"**From**: {item['source']}")
                lines.append("")
            
            text_key = item.get('text') or item.get('filled_example')
            lines.append(f"> {text_key}")
            lines.append("")
        
        return lines
    
    def _to_anchor(self, text: str) -> str:
        """Convert text to markdown anchor link."""
        return text.lower().replace(' ', '-').replace('&', '').replace(',', '')
    
    def _format_evidence(self, evidence_list: List[Dict], level: int) -> List[str]:
        """Format evidence section (used by philosophy and values)."""
        lines = []
        if not evidence_list:
            return lines
        
        lines.append(f"{'#' * level} Evidence")
        lines.append("")
        
        for evidence in evidence_list:
            lines.append(f"> \"{evidence.get('quote', '')}\"")
            lines.append(f"> ")
            lines.append(f"> *{evidence.get('context', '')}*")
            if 'source' in evidence:
                lines.append(f"> ")
                lines.append(f"> **Source**: {evidence['source']}")
            lines.append("")
        
        return lines
```

**Step 2: Create philosophy_generator.py**
```python
# File: generators/philosophy_generator.py
"""Generate Career Philosophy & Values lexicon."""

from typing import Dict, Any
from .base_generator import MarkdownFormatter

class PhilosophyLexiconGenerator(MarkdownFormatter):
    """Generates Career Philosophy & Values lexicon."""
    
    def generate(self, data: Dict[str, Any]) -> str:
        """Generate markdown content (no file I/O)."""
        # Handle raw markdown if JSON parsing failed
        if 'markdown' in data:
            return data['markdown']
        
        lines = [
            "# Career Philosophy & Values",
            "",
            f"**Generated**: {self.generated_date}",
            "",
            "---",
            "",
            "## Table of Contents",
            "",
            "- [I. Leadership Approaches](#i-leadership-approaches)",
            "- [II. Core Values](#ii-core-values)",
            "- [III. Problem-Solving Philosophy](#iii-problem-solving-philosophy)",
            "",
            "---",
            ""
        ]
        
        # Leadership Approaches
        lines.append("## I. Leadership Approaches")
        lines.append("")
        for i, approach in enumerate(data.get('leadership_approaches', []), 1):
            lines.extend(self._format_philosophy_item(approach, f"### {chr(64+i)}.", 3))
        
        # Core Values
        lines.append("## II. Core Values")
        lines.append("")
        for i, value in enumerate(data.get('core_values', []), 1):
            lines.extend(self._format_value_item(value, f"### {chr(64+i)}.", 3))
        
        # Problem-Solving Philosophy
        lines.append("## III. Problem-Solving Philosophy")
        lines.append("")
        for i, philosophy in enumerate(data.get('problem_solving_philosophy', []), 1):
            lines.extend(self._format_philosophy_item(philosophy, f"### {chr(64+i)}.", 3))
        
        return "\n".join(lines)
    
    def _format_philosophy_item(self, item: Dict[str, Any], heading: str, level: int) -> List[str]:
        """Format a single philosophy/approach item."""
        lines = []
        lines.append(f"{heading} {item.get('name', 'Unnamed')}")
        lines.append("")
        
        if 'core_principle' in item:
            lines.append(f"**Core Principle**: {item['core_principle']}")
            lines.append("")
        
        if 'description' in item:
            lines.append(item['description'])
            lines.append("")
        
        # Use shared evidence formatter
        lines.extend(self._format_evidence(item.get('evidence', []), level + 1))
        
        # ... rest of formatting
        
        return lines
```

**Step 3: Create orchestrator.py (new)**
```python
# File: generators/orchestrator.py
"""Orchestrate generation of all lexicons."""

from typing import Dict, Any
import os
from .philosophy_generator import PhilosophyLexiconGenerator
from .achievements_generator import AchievementsLexiconGenerator
from .narratives_generator import NarrativesLexiconGenerator
from .language_generator import LanguageGenerator

def generate_all_lexicons(
    analysis_results: Dict[str, Any],
    output_dir: str
) -> Dict[str, str]:
    """Generate all four lexicons."""
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    # Generate each lexicon
    results['philosophy'] = _generate_and_save(
        PhilosophyLexiconGenerator(),
        analysis_results.get('philosophy', {}),
        os.path.join(output_dir, '01_career_philosophy.md')
    )
    
    results['achievements'] = _generate_and_save(
        AchievementsLexiconGenerator(),
        analysis_results.get('achievements', {}),
        os.path.join(output_dir, '02_achievement_library.md')
    )
    
    # ... etc for other lexicons
    
    return results

def _generate_and_save(generator, data: Dict, output_path: str) -> str:
    """Generate content and save to file."""
    content = generator.generate(data)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    
    return output_path
```

### Benefits of This Approach
✓ Each generator: ~85-90 LOC (vs 782 for monolithic)  
✓ Easy to test: test each generator in isolation  
✓ Easy to modify: change philosophy format without affecting achievements  
✓ Easy to extend: add new generator type by creating new class  
✓ DRY: shared formatting in base_generator  
✓ Clear separation of concerns  

---

## P0 Issue #3: Duplicate JSON Parsing (40 lines of duplication)

### Current Problem (WRONG)

```python
# File: analyzers/llm_analyzer.py

class LLMAnalyzer:
    # Lines 102-127: analyze_philosophy()
    def analyze_philosophy(self, formatted_docs, documents):
        from .llm_prompt_templates import PHILOSOPHY_PROMPT
        prompt = PHILOSOPHY_PROMPT.format(documents=formatted_docs)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {'markdown': content}
        
        return result
    
    # Lines 152-162: analyze_achievements() - IDENTICAL EXCEPT PROMPT
    def analyze_achievements(self, formatted_docs, documents):
        from .llm_prompt_templates import ACHIEVEMENTS_PROMPT
        prompt = ACHIEVEMENTS_PROMPT.format(documents=formatted_docs)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {'markdown': content}
        
        return result
    
    # Lines 189-199: analyze_narratives() - IDENTICAL
    # Lines 226-237: analyze_language() - IDENTICAL
```

### Why This Is A Problem
- 40 lines of identical code across 4 methods
- Bug in JSON parsing requires 4 fixes
- Testing JSON parsing requires testing 4 methods
- Hard to maintain consistency

### The Fix (CORRECT)

```python
# File: analyzers/llm_analyzer.py

class LLMAnalyzer:
    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse JSON from LLM response, fallback to markdown.
        
        Handles:
        - JSON wrapped in ```json ... ```
        - JSON wrapped in ``` ... ```
        - Raw JSON
        - Falls back to returning response as markdown if parsing fails
        
        Args:
            response: Response from Anthropic client
        
        Returns:
            Dict with parsed JSON or {'markdown': raw_text}
        """
        content = response.content[0].text
        
        try:
            # Try to extract JSON from code blocks
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            # Parse as JSON
            return json.loads(content)
        
        except json.JSONDecodeError:
            # Fall back to returning as markdown
            logger.debug(f"Failed to parse as JSON, returning as markdown")
            return {'markdown': content}
    
    def analyze_philosophy(self, formatted_docs, documents):
        """Analyze career philosophy and values."""
        from .llm_prompt_templates import PHILOSOPHY_PROMPT
        
        prompt = PHILOSOPHY_PROMPT.format(documents=formatted_docs)
        logger.info("Analyzing philosophy")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response)
    
    def analyze_achievements(self, formatted_docs, documents):
        """Analyze achievements and create variation library."""
        from .llm_prompt_templates import ACHIEVEMENTS_PROMPT
        
        prompt = ACHIEVEMENTS_PROMPT.format(documents=formatted_docs)
        logger.info("Analyzing achievements")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response)
    
    def analyze_narratives(self, formatted_docs, documents):
        """Analyze narrative patterns and story structures."""
        from .llm_prompt_templates import NARRATIVES_PROMPT
        
        prompt = NARRATIVES_PROMPT.format(documents=formatted_docs)
        logger.info("Analyzing narratives")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response)
    
    def analyze_language(self, formatted_docs, documents):
        """Analyze language patterns and create phrase library."""
        from .llm_prompt_templates import LANGUAGE_PROMPT
        
        prompt = LANGUAGE_PROMPT.format(documents=formatted_docs)
        logger.info("Analyzing language patterns")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response)
```

### Benefits
✓ Single source of truth for JSON parsing  
✓ One place to fix bugs  
✓ Can test JSON parsing separately  
✓ All 4 methods now have consistent error handling  
✓ Each analyze_* method now 8 lines (vs 26 before)  

---

## Summary of P0 Fixes

| Issue | Lines Changed | Time | Impact |
|-------|---------------|------|--------|
| #1: Types extraction | 20 | 1-2h | Foundation for all refactoring |
| #2: Generator refactor | ~400 | 8-12h | Testability + maintainability |
| #3: JSON parsing | 35 | 1-2h | DRY + bug risk reduction |
| **TOTAL** | **~450** | **10-16h** | **Solid foundation** |

---

## Key Principles Demonstrated

1. **DRY (Don't Repeat Yourself)** - Extract duplicate code
2. **SRP (Single Responsibility)** - One class = one reason to change
3. **DIP (Dependency Inversion)** - Depend on abstractions, not concrete types
4. **Separation of Concerns** - Content generation ≠ File I/O
5. **Testability** - Extract, isolate, mock

Apply these to remaining issues (P1 and P2) for consistent improvement.
