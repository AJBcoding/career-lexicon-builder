"""
LLM-based career document analyzer using Claude API.

This module uses Claude to perform interpretive analysis of career documents,
extracting themes, patterns, and actionable guidance rather than just
semantic similarity matching.
"""

import os
from typing import Dict, List, Any, Optional
import json
from anthropic import Anthropic


class LLMAnalyzer:
    """Analyzes career documents using Claude API for interpretive analysis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize LLM analyzer.

        Args:
            api_key: Anthropic API key (if None, reads from ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = 16384

    def analyze_all(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform complete analysis of all documents.

        Args:
            documents: List of document dicts from document_processor

        Returns:
            Dict containing all four lexicon analyses
        """
        # Format documents for analysis
        formatted_docs = self._format_documents(documents)

        results = {
            'philosophy': self.analyze_philosophy(formatted_docs, documents),
            'achievements': self.analyze_achievements(formatted_docs, documents),
            'narratives': self.analyze_narratives(formatted_docs, documents),
            'language_bank': self.analyze_language(formatted_docs, documents)
        }

        return results

    def _format_documents(self, documents: List[Dict[str, Any]]) -> str:
        """Format documents for Claude analysis."""
        formatted = []

        for doc in documents:
            # Handle both old and new document format
            doc_type = doc.get('doc_type', 'unknown')
            if hasattr(doc_type, 'value'):
                doc_type = doc_type.value

            date = doc.get('date', 'unknown')
            filepath = doc.get('filepath', 'unknown')
            content = doc.get('text', '')

            # Extract just filename from path
            import os
            filename = os.path.basename(filepath) if filepath != 'unknown' else 'unknown'

            formatted.append(
                f"---\n"
                f"TYPE: {doc_type}\n"
                f"DATE: {date}\n"
                f"FILE: {filename}\n"
                f"---\n"
                f"{content}\n\n"
            )

        return "\n".join(formatted)

    def analyze_philosophy(
        self,
        formatted_docs: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze career philosophy and values.

        Returns structured data for Career Philosophy & Values lexicon.
        """
        from .llm_prompt_templates import PHILOSOPHY_PROMPT

        prompt = PHILOSOPHY_PROMPT.format(documents=formatted_docs)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract JSON from response
        content = response.content[0].text

        # Try to parse as JSON
        try:
            # Claude might wrap in markdown code blocks
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            result = json.loads(content)
        except json.JSONDecodeError:
            # If not valid JSON, return as raw markdown
            result = {'markdown': content}

        return result

    def analyze_achievements(
        self,
        formatted_docs: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze achievements and create variation library.

        Returns structured data for Achievement Library lexicon.
        """
        from .llm_prompt_templates import ACHIEVEMENTS_PROMPT

        prompt = ACHIEVEMENTS_PROMPT.format(documents=formatted_docs)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
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

    def analyze_narratives(
        self,
        formatted_docs: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze narrative patterns and story structures.

        Returns structured data for Narrative Patterns lexicon.
        """
        from .llm_prompt_templates import NARRATIVES_PROMPT

        prompt = NARRATIVES_PROMPT.format(documents=formatted_docs)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
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

    def analyze_language(
        self,
        formatted_docs: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze language patterns and create phrase library.

        Returns structured data for Language Bank lexicon.
        """
        from .llm_prompt_templates import LANGUAGE_PROMPT

        prompt = LANGUAGE_PROMPT.format(documents=formatted_docs)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
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


def analyze_documents_with_llm(
    documents: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to analyze documents with LLM.

    Args:
        documents: List of processed document dicts
        api_key: Optional Anthropic API key

    Returns:
        Dict with all four lexicon analyses
    """
    analyzer = LLMAnalyzer(api_key=api_key)
    return analyzer.analyze_all(documents)
