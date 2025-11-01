"""
Hierarchical markdown generator for LLM-analyzed career lexicons.

Converts structured JSON from LLM analysis into navigable,
hierarchical markdown reference guides.
"""

from typing import Dict, Any, List
from datetime import datetime


class HierarchicalMarkdownGenerator:
    """Generates hierarchical markdown from LLM analysis results."""

    def __init__(self):
        self.generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def generate_all(self, analysis_results: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """
        Generate all four lexicon files.

        Args:
            analysis_results: Dict from LLMAnalyzer.analyze_all()
            output_dir: Directory to write files to

        Returns:
            Dict mapping lexicon names to file paths
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        files = {}

        # Generate each lexicon
        files['philosophy'] = self.generate_philosophy(
            analysis_results.get('philosophy', {}),
            os.path.join(output_dir, '01_career_philosophy.md')
        )

        files['achievements'] = self.generate_achievements(
            analysis_results.get('achievements', {}),
            os.path.join(output_dir, '02_achievement_library.md')
        )

        files['narratives'] = self.generate_narratives(
            analysis_results.get('narratives', {}),
            os.path.join(output_dir, '03_narrative_patterns.md')
        )

        files['language'] = self.generate_language_bank(
            analysis_results.get('language_bank', {}),
            os.path.join(output_dir, '04_language_bank.md')
        )

        return files

    def generate_philosophy(self, data: Dict[str, Any], output_path: str) -> str:
        """Generate Career Philosophy & Values lexicon."""

        # Handle raw markdown if JSON parsing failed
        if 'markdown' in data:
            content = data['markdown']
            with open(output_path, 'w') as f:
                f.write(content)
            return output_path

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

        lines.append("---")
        lines.append("")

        # Core Values
        lines.append("## II. Core Values")
        lines.append("")

        for i, value in enumerate(data.get('core_values', []), 1):
            lines.extend(self._format_value_item(value, f"### {chr(64+i)}.", 3))

        lines.append("---")
        lines.append("")

        # Problem-Solving Philosophy
        lines.append("## III. Problem-Solving Philosophy")
        lines.append("")

        for i, philosophy in enumerate(data.get('problem_solving_philosophy', []), 1):
            lines.extend(self._format_philosophy_item(philosophy, f"### {chr(64+i)}.", 3))

        # Write to file
        content = "\n".join(lines)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

    def _format_philosophy_item(self, item: Dict[str, Any], heading: str, level: int) -> List[str]:
        """Format a single philosophy/approach item."""
        lines = []

        # Heading
        lines.append(f"{heading} {item.get('name', 'Unnamed')}")
        lines.append("")

        # Core principle / Approach
        if 'core_principle' in item:
            lines.append(f"**Core Principle**: {item['core_principle']}")
            lines.append("")

        if 'approach' in item:
            lines.append(f"**Approach**: {item['approach']}")
            lines.append("")

        # Description
        if 'description' in item:
            lines.append(item['description'])
            lines.append("")

        # Evidence
        if 'evidence' in item and item['evidence']:
            lines.append(f"{'#' * (level + 1)} Evidence")
            lines.append("")
            for evidence in item['evidence']:
                lines.append(f"> \"{evidence.get('quote', '')}\"")
                lines.append(f"> ")
                lines.append(f"> *{evidence.get('context', '')}*")
                if 'source' in evidence:
                    lines.append(f"> ")
                    lines.append(f"> **Source**: {evidence['source']}")
                lines.append("")

        # When to use
        if 'when_to_use' in item:
            lines.append(f"{'#' * (level + 1)} When to Use")
            lines.append("")
            lines.append(f"**Best for**: {item['when_to_use']}")
            lines.append("")

        # How to phrase
        if 'how_to_phrase' in item and item['how_to_phrase']:
            lines.append(f"{'#' * (level + 1)} How to Phrase")
            lines.append("")
            for phrase in item['how_to_phrase']:
                lines.append(f"- {phrase}")
            lines.append("")

        # Example phrases
        if 'example_phrases' in item and item['example_phrases']:
            lines.append(f"{'#' * (level + 1)} Example Phrases")
            lines.append("")
            for phrase in item['example_phrases']:
                lines.append(f"- {phrase}")
            lines.append("")

        # Related themes
        if 'related_themes' in item and item['related_themes']:
            lines.append(f"**Related themes**: {', '.join(item['related_themes'])}")
            lines.append("")

        # Keywords
        if 'keywords' in item and item['keywords']:
            keywords_str = ' '.join([f'`{kw}`' for kw in item['keywords']])
            lines.append(f"**Keywords**: {keywords_str}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_value_item(self, item: Dict[str, Any], heading: str, level: int) -> List[str]:
        """Format a core value item."""
        lines = []

        lines.append(f"{heading} {item.get('name', 'Unnamed')}")
        lines.append("")

        if 'definition' in item:
            lines.append(f"**Definition**: {item['definition']}")
            lines.append("")

        # Evidence
        if 'evidence' in item and item['evidence']:
            lines.append(f"{'#' * (level + 1)} Evidence")
            lines.append("")
            for evidence in item['evidence']:
                lines.append(f"> \"{evidence.get('quote', '')}\"")
                lines.append(f"> ")
                lines.append(f"> *{evidence.get('context', '')}*")
                if 'source' in evidence:
                    lines.append(f"> ")
                    lines.append(f"> **Source**: {evidence['source']}")
                lines.append("")

        # Differentiation
        if 'differentiation' in item:
            lines.append(f"{'#' * (level + 1)} What This Shows")
            lines.append("")
            lines.append(item['differentiation'])
            lines.append("")

        # Application examples
        if 'application_examples' in item and item['application_examples']:
            lines.append(f"{'#' * (level + 1)} How to Apply")
            lines.append("")
            for example in item['application_examples']:
                lines.append(f"- {example}")
            lines.append("")

        # Keywords
        if 'keywords' in item and item['keywords']:
            keywords_str = ' '.join([f'`{kw}`' for kw in item['keywords']])
            lines.append(f"**Keywords**: {keywords_str}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def generate_achievements(self, data: Dict[str, Any], output_path: str) -> str:
        """Generate Achievement Library lexicon."""

        # Handle raw markdown
        if 'markdown' in data:
            content = data['markdown']
            with open(output_path, 'w') as f:
                f.write(content)
            return output_path

        lines = [
            "# Achievement Library",
            "",
            f"**Generated**: {self.generated_date}",
            "",
            "---",
            "",
            "## Table of Contents",
            ""
        ]

        # Build TOC
        for i, category in enumerate(data.get('categories', []), 1):
            cat_name = category.get('name', 'Category')
            lines.append(f"- [{chr(64+i)}. {cat_name}](#{self._to_anchor(cat_name)})")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Generate categories
        for i, category in enumerate(data.get('categories', []), 1):
            lines.extend(self._format_achievement_category(category, chr(64+i)))

        content = "\n".join(lines)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

    def _format_achievement_category(self, category: Dict[str, Any], letter: str) -> List[str]:
        """Format an achievement category."""
        lines = []

        cat_name = category.get('name', 'Category')
        lines.append(f"## {letter}. {cat_name}")
        lines.append("")

        for i, achievement in enumerate(category.get('achievements', []), 1):
            lines.extend(self._format_achievement(achievement, f"{letter}.{i}"))

        return lines

    def _format_achievement(self, achievement: Dict[str, Any], number: str) -> List[str]:
        """Format a single achievement."""
        lines = []

        name = achievement.get('name', 'Achievement')
        lines.append(f"### {number} {name}")
        lines.append("")

        # Overview
        if 'overview' in achievement:
            overview = achievement['overview']
            lines.append("#### Overview")
            lines.append("")
            if 'summary' in overview:
                lines.append(overview['summary'])
                lines.append("")

            if 'scale' in overview:
                lines.append("**Scale**:")
                for key, value in overview['scale'].items():
                    lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
                lines.append("")

            if 'context' in overview:
                lines.append(f"**Context**: {overview['context']}")
                lines.append("")

        # Variations
        if 'variations' in achievement and achievement['variations']:
            lines.append("#### Variations by Emphasis")
            lines.append("")

            for var in achievement['variations']:
                lines.append(f"##### {var.get('emphasis', 'Variation')}")
                lines.append("")
                if 'use_for' in var:
                    use_for_str = ', '.join(var['use_for'])
                    lines.append(f"> **Use for**: {use_for_str}")
                    lines.append("")
                lines.append(var.get('text', ''))
                lines.append("")
                if 'highlights' in var:
                    highlights_str = ', '.join(var['highlights'])
                    lines.append(f"**Highlights**: {highlights_str}")
                    lines.append("")
                lines.append("---")
                lines.append("")

        # Quantifiable outcomes
        if 'quantifiable_outcomes' in achievement and achievement['quantifiable_outcomes']:
            lines.append("#### Quantifiable Outcomes")
            lines.append("")
            for outcome in achievement['quantifiable_outcomes']:
                metric = outcome.get('metric', '')
                desc = outcome.get('description', '')
                tip = outcome.get('emphasis_tip', '')
                lines.append(f"- **{metric}** - {desc}")
                if tip:
                    lines.append(f"  - *{tip}*")
            lines.append("")

        # Usage recommendations
        if 'usage_recommendations' in achievement:
            recs = achievement['usage_recommendations']
            lines.append("#### Usage Recommendations")
            lines.append("")

            if 'resume' in recs:
                lines.append("**Resume**:")
                for key, value in recs['resume'].items():
                    lines.append(f"- {key.replace('_', ' ').title()}: {value}")
                lines.append("")

            if 'cover_letter' in recs:
                lines.append("**Cover Letter**:")
                for key, value in recs['cover_letter'].items():
                    lines.append(f"- {key.replace('_', ' ').title()}: {value}")
                lines.append("")

            if 'interview' in recs:
                lines.append("**Interview**:")
                interview = recs['interview']
                if 'good_for' in interview:
                    lines.append(f"- Good for: {', '.join(interview['good_for'])}")
                if 'star_format' in interview:
                    lines.append("- STAR Format:")
                    for key, value in interview['star_format'].items():
                        lines.append(f"  - {key.title()}: {value}")
                lines.append("")

        # Related achievements
        if 'related_achievements' in achievement and achievement['related_achievements']:
            related_str = ', '.join(achievement['related_achievements'])
            lines.append(f"**Related achievements**: {related_str}")
            lines.append("")

        # Keywords
        if 'keywords' in achievement and achievement['keywords']:
            keywords_str = ' '.join([f'`{kw}`' for kw in achievement['keywords']])
            lines.append(f"**Keywords**: {keywords_str}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def generate_narratives(self, data: Dict[str, Any], output_path: str) -> str:
        """Generate Narrative Patterns lexicon."""

        # Handle raw markdown
        if 'markdown' in data:
            content = data['markdown']
            with open(output_path, 'w') as f:
                f.write(content)
            return output_path

        lines = [
            "# Narrative Patterns & Story Structures",
            "",
            f"**Generated**: {self.generated_date}",
            "",
            "Use these patterns when crafting cover letters, resumes, and interview responses.",
            "",
            "---",
            ""
        ]

        # Cover Letter Architecture
        if 'cover_letter_architecture' in data:
            lines.append("## I. Cover Letter Architecture")
            lines.append("")
            for pattern in data['cover_letter_architecture']:
                lines.extend(self._format_narrative_pattern(pattern))

        # Evidence Presentation
        if 'evidence_presentation_patterns' in data:
            lines.append("## II. Evidence Presentation Patterns")
            lines.append("")
            for pattern in data['evidence_presentation_patterns']:
                lines.extend(self._format_narrative_pattern(pattern))

        # Resume Bullet Formulas
        if 'resume_bullet_formulas' in data:
            lines.append("## III. Resume Bullet Formulas")
            lines.append("")
            for formula in data['resume_bullet_formulas']:
                lines.extend(self._format_bullet_formula(formula))

        # Other sections...
        for section_name in ['transition_strategies', 'closing_strategies']:
            if section_name in data:
                title = section_name.replace('_', ' ').title()
                lines.append(f"## {title}")
                lines.append("")
                for item in data[section_name]:
                    lines.extend(self._format_narrative_pattern(item))

        content = "\n".join(lines)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

    def _format_narrative_pattern(self, pattern: Dict[str, Any]) -> List[str]:
        """Format a narrative pattern."""
        lines = []

        name = pattern.get('pattern_name', 'Pattern') or pattern.get('strategy_name', 'Strategy')
        lines.append(f"### {name}")
        lines.append("")

        if 'description' in pattern:
            lines.append(pattern['description'])
            lines.append("")

        # Structure
        if 'structure' in pattern:
            lines.append("#### Structure")
            lines.append("")
            if isinstance(pattern['structure'], list):
                for step in pattern['structure']:
                    step_num = step.get('step', '')
                    element = step.get('element', '')
                    lines.append(f"{step_num}. **{element}**")
                    if 'example' in step:
                        lines.append(f"   - *Example*: {step['example']}")
            else:
                lines.append(pattern['structure'])
            lines.append("")

        # Template
        if 'template' in pattern:
            lines.append("#### Template")
            lines.append("")
            lines.append(f"```")
            lines.append(pattern['template'])
            lines.append(f"```")
            lines.append("")

        # Examples
        if 'examples' in pattern and pattern['examples']:
            lines.append("#### Examples")
            lines.append("")
            for ex in pattern['examples']:
                if 'source' in ex:
                    lines.append(f"**From**: {ex['source']}")
                    lines.append("")
                lines.append(f"> {ex.get('text', '')}")
                lines.append("")

        # When to use
        if 'when_to_use' in pattern:
            lines.append(f"**When to use**: {pattern['when_to_use']}")
            lines.append("")

        # Effectiveness
        if 'effectiveness' in pattern:
            lines.append(f"**Why it works**: {pattern['effectiveness']}")
            lines.append("")

        # Variations
        if 'variations' in pattern and pattern['variations']:
            lines.append("#### Variations")
            lines.append("")
            for var in pattern['variations']:
                lines.append(f"- **{var.get('variant_name', '')}**: {var.get('adjustment', '')}")
            lines.append("")

        # Keywords
        if 'keywords' in pattern and pattern['keywords']:
            keywords_str = ' '.join([f'`{kw}`' for kw in pattern['keywords']])
            lines.append(f"**Keywords**: {keywords_str}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_bullet_formula(self, formula: Dict[str, Any]) -> List[str]:
        """Format a resume bullet formula."""
        lines = []

        name = formula.get('formula_name', 'Formula')
        lines.append(f"### {name}")
        lines.append("")

        if 'template' in formula:
            lines.append("#### Template")
            lines.append("")
            lines.append(f"```")
            lines.append(formula['template'])
            lines.append(f"```")
            lines.append("")

        # Examples
        if 'examples' in formula and formula['examples']:
            lines.append("#### Examples")
            lines.append("")
            for ex in formula['examples']:
                lines.append(f"**Text**: {ex.get('text', '')}")
                lines.append("")
                if 'breakdown' in ex:
                    lines.append("**Breakdown**:")
                    for key, value in ex['breakdown'].items():
                        lines.append(f"- {key.replace('_', ' ').title()}: {value}")
                    lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def generate_language_bank(self, data: Dict[str, Any], output_path: str) -> str:
        """Generate Language Bank lexicon."""

        # Handle raw markdown
        if 'markdown' in data:
            content = data['markdown']
            with open(output_path, 'w') as f:
                f.write(content)
            return output_path

        lines = [
            "# Language Bank & Phrase Library",
            "",
            f"**Generated**: {self.generated_date}",
            "",
            "Powerful language patterns, action verbs, and industry terminology.",
            "",
            "---",
            ""
        ]

        # Action Verbs
        if 'action_verbs' in data:
            lines.append("## I. Action Verbs by Category")
            lines.append("")
            for category in data['action_verbs']:
                lines.extend(self._format_verb_category(category))

        # Impact Phrases
        if 'impact_phrases' in data:
            lines.append("## II. Impact Phrases")
            lines.append("")
            for category in data['impact_phrases']:
                lines.extend(self._format_phrase_category(category))

        # Industry Terminology
        if 'industry_terminology' in data:
            lines.append("## III. Industry-Specific Terminology")
            lines.append("")
            for industry in data['industry_terminology']:
                lines.extend(self._format_industry_terms(industry))

        # Powerful Phrase Templates
        if 'powerful_phrase_templates' in data:
            lines.append("## IV. Powerful Phrase Templates")
            lines.append("")
            for template in data['powerful_phrase_templates']:
                lines.extend(self._format_phrase_template(template))

        # Signature Phrases
        if 'signature_phrases' in data:
            lines.append("## V. Signature Phrases")
            lines.append("")
            for phrase in data['signature_phrases']:
                lines.extend(self._format_signature_phrase(phrase))

        content = "\n".join(lines)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

    def _format_verb_category(self, category: Dict[str, Any]) -> List[str]:
        """Format action verb category."""
        lines = []

        lines.append(f"### {category.get('category', 'Category')}")
        lines.append("")

        for subcat in category.get('subcategories', []):
            lines.append(f"#### {subcat.get('name', 'Subcategory')}")
            lines.append("")

            for verb_item in subcat.get('verbs', []):
                verb = verb_item.get('verb', '')
                lines.append(f"**{verb}**")
                if 'usage_context' in verb_item:
                    lines.append(f"- *Context*: {verb_item['usage_context']}")
                if 'examples' in verb_item:
                    lines.append("- *Examples*:")
                    for ex in verb_item['examples']:
                        lines.append(f"  - {ex}")
                if 'when_to_use' in verb_item:
                    lines.append(f"- *Use for*: {verb_item['when_to_use']}")
                lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_phrase_category(self, category: Dict[str, Any]) -> List[str]:
        """Format impact phrase category."""
        lines = []

        lines.append(f"### {category.get('category', 'Category')}")
        lines.append("")

        for phrase in category.get('phrases', []):
            lines.append(f"**{phrase.get('pattern', '')}** ({phrase.get('type', '')})")
            lines.append("")
            if 'examples' in phrase:
                lines.append("Examples:")
                for ex in phrase['examples']:
                    lines.append(f"- {ex}")
                lines.append("")
            if 'variations' in phrase:
                lines.append("Variations:")
                for var in phrase['variations']:
                    lines.append(f"- {var}")
                lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_industry_terms(self, industry: Dict[str, Any]) -> List[str]:
        """Format industry terminology."""
        lines = []

        lines.append(f"### {industry.get('industry', 'Industry')}")
        lines.append("")

        for term_cat in industry.get('term_categories', []):
            lines.append(f"#### {term_cat.get('category', 'Category')}")
            lines.append("")

            for term in term_cat.get('terms', []):
                lines.append(f"**{term.get('term', '')}**")
                if 'definition' in term:
                    lines.append(f"- *Definition*: {term['definition']}")
                if 'usage_examples' in term:
                    lines.append("- *Usage*:")
                    for ex in term['usage_examples']:
                        lines.append(f"  - {ex}")
                lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_phrase_template(self, template: Dict[str, Any]) -> List[str]:
        """Format phrase template."""
        lines = []

        lines.append(f"### {template.get('template_name', 'Template')}")
        lines.append("")
        lines.append(f"**Template**: `{template.get('template', '')}`")
        lines.append("")

        if 'examples' in template:
            lines.append("**Examples**:")
            lines.append("")
            for ex in template['examples']:
                lines.append(f"> {ex.get('filled_example', '')}")
                lines.append("")

        if 'when_to_use' in template:
            lines.append(f"**When to use**: {template['when_to_use']}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _format_signature_phrase(self, phrase: Dict[str, Any]) -> List[str]:
        """Format signature phrase."""
        lines = []

        lines.append(f"### \"{phrase.get('phrase', '')}\"")
        lines.append("")
        lines.append(f"**Category**: {phrase.get('category', '')}")
        lines.append(f"**Appears**: {phrase.get('appearances', 0)} times")
        lines.append("")

        if 'full_quotes' in phrase:
            lines.append("**Examples**:")
            for quote in phrase['full_quotes']:
                lines.append(f"> {quote}")
            lines.append("")

        if 'usage_tip' in phrase:
            lines.append(f"**Usage tip**: {phrase['usage_tip']}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return lines

    def _to_anchor(self, text: str) -> str:
        """Convert text to markdown anchor link."""
        return text.lower().replace(' ', '-').replace('&', '').replace(',', '')


def generate_hierarchical_lexicons(
    analysis_results: Dict[str, Any],
    output_dir: str
) -> Dict[str, str]:
    """
    Convenience function to generate all lexicons.

    Args:
        analysis_results: Results from LLMAnalyzer
        output_dir: Output directory

    Returns:
        Dict mapping lexicon names to file paths
    """
    generator = HierarchicalMarkdownGenerator()
    return generator.generate_all(analysis_results, output_dir)
