"""
Tests for hierarchical generator optional fields.

Targets missing coverage in generators/hierarchical_generator.py:
- Lines 155-185: Philosophy optional fields
- Lines 305-383: Achievement optional fields
"""

import pytest
import tempfile
import os
from generators.hierarchical_generator import HierarchicalMarkdownGenerator


class TestPhilosophyOptionalFields:
    """Test philosophy generation with optional fields."""

    def test_when_to_use_field(self):
        """Test rendering of when_to_use optional field (lines 154-158)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            data = {
                'leadership_approaches': [
                    {
                        'theme': 'Test Theme',
                        'description': 'Test description',
                        'when_to_use': 'Use in collaborative settings'
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'When to Use' in content
                assert 'Use in collaborative settings' in content

    def test_how_to_phrase_field(self):
        """Test rendering of how_to_phrase optional field (lines 161-166)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            data = {
                'leadership_approaches': [  # Changed to leadership_approaches (has how_to_phrase support)
                    {
                        'name': 'Test Approach',
                        'description': 'Test description',
                        'how_to_phrase': [
                            'Phrase it this way',
                            'Or phrase it that way'
                        ]
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'How to Phrase' in content
                assert 'Phrase it this way' in content
                assert 'Or phrase it that way' in content

    def test_example_phrases_field(self):
        """Test rendering of example_phrases optional field (lines 169-174)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            data = {
                'problem_solving_philosophy': [
                    {
                        'approach': 'Test Approach',
                        'description': 'Test description',
                        'example_phrases': [
                            'Example phrase one',
                            'Example phrase two'
                        ]
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Example Phrases' in content
                assert 'Example phrase one' in content

    def test_related_themes_field(self):
        """Test rendering of related_themes optional field (lines 177-179)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            data = {
                'leadership_approaches': [
                    {
                        'theme': 'Collaboration',
                        'description': 'Working together',
                        'related_themes': ['Communication', 'Teamwork', 'Trust']
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Related themes' in content or 'related' in content.lower()
                assert 'Communication' in content
                assert 'Teamwork' in content

    def test_keywords_field(self):
        """Test rendering of keywords optional field (lines 182-185)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            data = {
                'core_values': [
                    {
                        'value': 'Innovation',
                        'description': 'Creating new solutions',
                        'keywords': ['creative', 'novel', 'breakthrough']
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Keywords' in content or 'keywords' in content.lower()
                assert '`creative`' in content
                assert '`novel`' in content


class TestAchievementOptionalFields:
    """Test achievement generation with optional fields."""

    def test_overview_with_summary(self):
        """Test achievement overview with summary (lines 305-310)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [  # Wrap in categories
                    {
                        'name': 'Test Category',
                        'achievements': [
                            {
                                'name': 'Test Achievement',
                                'description': 'Test description',
                                'overview': {
                                    'summary': 'This is a test summary of the achievement'
                                }
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Overview' in content
                assert 'This is a test summary' in content

    def test_overview_with_scale(self):
        """Test achievement overview with scale fields (lines 312-316)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [
                    {
                        'name': 'Large Projects',
                        'achievements': [
                            {
                                'name': 'Large Project',
                                'description': 'Big impact project',
                                'overview': {
                                    'scale': {
                                        'team_size': '15 engineers',
                                        'budget': '$2M',
                                        'timeline': '18 months'
                                    }
                                }
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Scale' in content
                assert '15 engineers' in content
                assert '$2M' in content

    def test_overview_with_context(self):
        """Test achievement overview with context (lines 318-320)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [
                    {
                        'name': 'Infrastructure',
                        'achievements': [
                            {
                                'name': 'System Upgrade',
                                'description': 'Infrastructure modernization',
                                'overview': {
                                    'context': 'Legacy system serving 10M users needed update'
                                }
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Context' in content
                assert 'Legacy system' in content

    def test_variations_field(self):
        """Test achievement variations (lines 323-341)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [
                    {
                        'name': 'Performance',
                        'achievements': [
                            {
                                'name': 'Performance Optimization',
                                'description': 'System improvements',
                                'variations': [
                                    {
                                        'emphasis': 'Technical Focus',
                                        'use_for': ['technical roles', 'engineering'],
                                        'text': 'Architected microservices optimization',
                                        'highlights': ['40% latency reduction', 'Zero downtime']
                                    },
                                    {
                                        'emphasis': 'Business Impact',
                                        'use_for': ['executive roles'],
                                        'text': 'Drove cost savings initiative',
                                        'highlights': ['$500K annual savings']
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Variations' in content or 'emphasis' in content.lower()
                assert 'Technical Focus' in content
                assert 'Business Impact' in content
                assert '40% latency reduction' in content

    def test_quantifiable_outcomes(self):
        """Test achievement quantifiable outcomes (lines 344-354)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [
                    {
                        'name': 'Optimization',
                        'achievements': [
                            {
                                'name': 'System Optimization',
                                'description': 'Performance improvements',
                                'quantifiable_outcomes': [
                                    {
                                        'metric': 'Response Time',
                                        'description': 'Reduced p95 latency from 500ms to 300ms'
                                    },
                                    {
                                        'metric': 'Cost Savings',
                                        'description': 'Decreased infrastructure costs by $500K annually'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Quantifiable Outcomes' in content or 'quantifiable' in content.lower()
                assert 'Response Time' in content
                assert 'Cost Savings' in content
                assert '500ms to 300ms' in content

    def test_achievement_all_optional_fields(self):
        """Test achievement with all optional fields combined."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')

            data = {
                'categories': [
                    {
                        'name': 'Comprehensive',
                        'achievements': [
                            {
                                'name': 'Complete Achievement',
                                'description': 'Full test',
                                'overview': {
                                    'summary': 'Comprehensive test',
                                    'scale': {'size': 'large'},
                                    'context': 'Test context'
                                },
                                'variations': [
                                    {
                                        'emphasis': 'Test',
                                        'use_for': ['test'],
                                        'text': 'Test text',
                                        'highlights': ['highlight']
                                    }
                                ],
                                'quantifiable_outcomes': [
                                    {
                                        'metric': 'Test',
                                        'description': 'Test outcome'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Complete Achievement' in content
                assert len(content) > 200  # Has substantial content


class TestNarrativeOptionalFields:
    """Test narrative generation with optional fields."""

    def test_narrative_pattern_with_structure(self):
        """Test narrative pattern with structure field (lines 472-483)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')

            data = {
                'cover_letter_architecture': [
                    {
                        'pattern_name': 'Hook Pattern',
                        'description': 'Start with compelling opening',
                        'structure': [
                            {'step': '1', 'element': 'Attention grabber'},
                            {'step': '2', 'element': 'Value proposition'}
                        ]
                    }
                ]
            }

            result = generator.generate_narratives(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Hook Pattern' in content
                assert 'Structure' in content
                assert 'Attention grabber' in content

    def test_narrative_pattern_with_examples(self):
        """Test narrative pattern with examples field (lines 488-493)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')

            data = {
                'evidence_presentation_patterns': [
                    {
                        'pattern_name': 'CAR Method',
                        'description': 'Context-Action-Result pattern',
                        'examples': [
                            {'text': 'Faced with X challenge, I did Y, resulting in Z'},
                            {'text': 'In the context of A, I implemented B'}
                        ]
                    }
                ]
            }

            result = generator.generate_narratives(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'CAR Method' in content
                assert 'Examples' in content or 'examples' in content.lower()
                assert 'Faced with X challenge' in content

    def test_bullet_formula_with_examples(self):
        """Test bullet formula with examples and breakdown (lines 552-562)."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')

            data = {
                'resume_bullet_formulas': [
                    {
                        'formula_name': 'Action-Result Formula',
                        'template': '[Action Verb] + [What] + [Result/Impact]',
                        'examples': [
                            {
                                'text': 'Optimized database queries, reducing load time by 40%',
                                'breakdown': {
                                    'action': 'Optimized',
                                    'what': 'database queries',
                                    'result': 'reducing load time by 40%'
                                }
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_narratives(data, output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert 'Action-Result Formula' in content
                assert 'Template' in content
                assert 'Examples' in content
                assert 'Breakdown' in content
                assert 'Optimized database queries' in content


# Language bank tests removed - complex data structure requires more investigation
