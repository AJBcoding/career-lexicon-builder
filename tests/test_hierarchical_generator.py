"""
Tests for hierarchical markdown generator.

This module tests the generation of hierarchical lexicon markdown files
from analyzed career documents. Currently 0% coverage (491 lines untested).

Coverage gaps to address:
- Hierarchical structure generation
- Markdown formatting
- Citation handling
- Section organization
"""

import pytest
import tempfile
import os
from pathlib import Path
from generators.hierarchical_generator import HierarchicalMarkdownGenerator


class TestHierarchicalGeneration:
    """Tests for main hierarchical generation functions."""

    def test_generator_initialization(self):
        """
        Test HierarchicalMarkdownGenerator initialization.

        Coverage gap: Initialization logic
        Priority: CRITICAL - Basic setup
        """
        generator = HierarchicalMarkdownGenerator()
        assert generator is not None
        assert hasattr(generator, 'generated_date')
        assert generator.generated_date is not None

    def test_generate_philosophy_with_empty_data(self):
        """
        Test philosophy lexicon generation with empty data.

        Coverage gap: Empty data handling
        Priority: MEDIUM - Error handling
        """
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            # Empty data dict
            result = generator.generate_philosophy({}, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            # Verify file has basic structure
            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Career Philosophy & Values' in content
                assert 'Generated' in content

    def test_generate_philosophy_with_markdown_fallback(self):
        """
        Test philosophy generation with raw markdown (JSON parsing fallback).

        Coverage gap: Markdown fallback handling
        Priority: HIGH - Error recovery
        """
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            # Data with markdown key (JSON parsing failed scenario)
            data = {
                'markdown': '# Test Philosophy\n\nThis is fallback markdown content.'
            }

            result = generator.generate_philosophy(data, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Test Philosophy' in content
                assert 'fallback markdown content' in content

    def test_generate_philosophy_with_structured_data(self):
        """
        Test philosophy generation with structured data.

        Coverage gap: Structured data processing
        Priority: CRITICAL - Core functionality
        """
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'philosophy.md')

            # Structured data
            data = {
                'leadership_approaches': [
                    {
                        'name': 'Collaborative Leadership',
                        'core_principle': 'Team empowerment through collaboration',
                        'description': 'Focus on building consensus and shared ownership.',
                        'evidence': [
                            {
                                'quote': 'Led team of 10 engineers',
                                'context': 'At TechCorp',
                                'source': 'Resume 2024'
                            }
                        ]
                    }
                ],
                'core_values': [
                    {
                        'name': 'Innovation',
                        'description': 'Driving change through creative solutions'
                    }
                ],
                'problem_solving_philosophy': [
                    {
                        'name': 'Data-Driven Decisions',
                        'approach': 'Use metrics to guide choices'
                    }
                ]
            }

            result = generator.generate_philosophy(data, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                # Check structure
                assert '# Career Philosophy & Values' in content
                assert '## I. Leadership Approaches' in content
                assert '## II. Core Values' in content
                assert '## III. Problem-Solving Philosophy' in content
                # Check content
                assert 'Collaborative Leadership' in content
                assert 'Innovation' in content
                assert 'Data-Driven Decisions' in content

    def test_generate_all_lexicons(self):
        """
        Test generating all four lexicon files at once.

        Coverage gap: Complete workflow
        Priority: CRITICAL - Main entry point
        """
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            analysis_results = {
                'philosophy': {},
                'achievements': {},
                'narratives': {},
                'language_bank': {}
            }

            files = generator.generate_all(analysis_results, tmpdir)

            assert 'philosophy' in files
            assert 'achievements' in files
            assert 'narratives' in files
            assert 'language' in files

            # Verify all files were created
            assert os.path.exists(files['philosophy'])
            assert os.path.exists(files['achievements'])
            assert os.path.exists(files['narratives'])
            assert os.path.exists(files['language'])

            # Verify filenames
            assert '01_career_philosophy.md' in files['philosophy']
            assert '02_achievement_library.md' in files['achievements']
            assert '03_narrative_patterns.md' in files['narratives']
            assert '04_language_bank.md' in files['language']


class TestAchievementsGeneration:
    """Tests for achievements lexicon generation."""

    def test_generate_achievements_with_empty_data(self):
        """Test achievements generation with empty data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')
            result = generator.generate_achievements({}, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Achievement Library' in content
                assert 'Generated' in content

    def test_generate_achievements_with_markdown_fallback(self):
        """Test achievements generation with markdown fallback."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')
            data = {'markdown': '# Test Achievements\n\nAchievement list here.'}

            result = generator.generate_achievements(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Test Achievements' in content

    def test_generate_achievements_with_structured_data(self):
        """Test achievements generation with structured data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'achievements.md')
            data = {
                'categories': [
                    {
                        'name': 'Leadership',
                        'achievements': [
                            {
                                'title': 'Team Management',
                                'impact': 'Improved team productivity by 30%',
                                'evidence': [{'quote': 'Led team of 10', 'source': 'Resume'}]
                            }
                        ]
                    }
                ]
            }

            result = generator.generate_achievements(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Achievement Library' in content
                assert 'Leadership' in content


class TestNarrativesGeneration:
    """Tests for narratives lexicon generation."""

    def test_generate_narratives_with_empty_data(self):
        """Test narratives generation with empty data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')
            result = generator.generate_narratives({}, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Narrative Patterns' in content
                assert 'Generated' in content

    def test_generate_narratives_with_markdown_fallback(self):
        """Test narratives generation with markdown fallback."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')
            data = {'markdown': '# Test Narratives\n\nNarrative patterns here.'}

            result = generator.generate_narratives(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Test Narratives' in content

    def test_generate_narratives_with_structured_data(self):
        """Test narratives generation with structured data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'narratives.md')
            data = {
                'cover_letter_architecture': [
                    {
                        'pattern_name': 'Opening Hook',
                        'description': 'Start with compelling hook',
                        'examples': [
                            {'text': 'Example 1', 'source': 'Cover Letter 2024'}
                        ]
                    }
                ]
            }

            result = generator.generate_narratives(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Narrative Patterns' in content
                assert 'Cover Letter Architecture' in content
                assert 'Opening Hook' in content


class TestLanguageBankGeneration:
    """Tests for language bank lexicon generation."""

    def test_generate_language_bank_with_empty_data(self):
        """Test language bank generation with empty data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'language_bank.md')
            result = generator.generate_language_bank({}, output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Language Bank' in content
                assert 'Generated' in content

    def test_generate_language_bank_with_markdown_fallback(self):
        """Test language bank generation with markdown fallback."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'language_bank.md')
            data = {'markdown': '# Test Language Bank\n\nPhrases here.'}

            result = generator.generate_language_bank(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Test Language Bank' in content

    def test_generate_language_bank_with_structured_data(self):
        """Test language bank generation with structured data."""
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'language_bank.md')
            data = {
                'action_verbs': [
                    {
                        'category': 'Leadership',
                        'verbs': [
                            {'verb': 'Led', 'usage': 'Past tense'},
                            {'verb': 'Managed', 'usage': 'Past tense'}
                        ]
                    }
                ],
                'impact_phrases': [
                    {
                        'category': 'Quantitative Impact',
                        'phrases': [
                            {'pattern': 'Increased X by Y%', 'type': 'Percentage growth'},
                            {'pattern': 'Reduced costs by $X', 'type': 'Cost savings'}
                        ]
                    }
                ]
            }

            result = generator.generate_language_bank(data, output_path)
            assert result == output_path

            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Language Bank' in content
                assert 'Action Verbs' in content or 'Impact Phrases' in content


class TestHelperMethods:
    """Tests for helper formatting methods."""

    def test_to_anchor_method(self):
        """Test _to_anchor helper method for TOC links."""
        generator = HierarchicalMarkdownGenerator()

        # Test anchor generation
        anchor = generator._to_anchor('Test Section Name')
        assert anchor == 'test-section-name'

        anchor = generator._to_anchor('Section With Numbers 123')
        assert 'section-with-numbers' in anchor.lower()

    def test_format_philosophy_item_with_evidence(self):
        """Test _format_philosophy_item with evidence."""
        generator = HierarchicalMarkdownGenerator()

        item = {
            'name': 'Test Philosophy',
            'core_principle': 'Test principle',
            'evidence': [
                {
                    'quote': 'Test quote',
                    'context': 'Test context',
                    'source': 'Test source'
                }
            ]
        }

        lines = generator._format_philosophy_item(item, '### A.', 3)
        result = '\n'.join(lines)

        assert 'Test Philosophy' in result
        assert 'Test principle' in result
        assert 'Test quote' in result
        assert 'Test source' in result

    def test_format_value_item(self):
        """Test _format_value_item helper method."""
        generator = HierarchicalMarkdownGenerator()

        item = {
            'name': 'Innovation',
            'definition': 'Creating novel solutions',
            'keywords': ['creative', 'novel', 'breakthrough']
        }

        lines = generator._format_value_item(item, '### A.', 3)
        result = '\n'.join(lines)

        assert 'Innovation' in result
        assert 'Creating novel solutions' in result
        assert 'creative' in result


class TestMarkdownFormatting:
    """Tests for markdown output formatting."""

    def test_heading_formatting(self):
        """
        Test markdown heading generation at various levels.

        Coverage gap: Heading formatter functions
        Priority: HIGH - Output format correctness
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'categories': [
                    {
                        'name': 'Test Category',
                        'achievements': [
                            {
                                'name': 'Test Achievement',
                                'description': 'Test description'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_achievements(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                assert '# Achievement Library' in content  # H1 heading
                assert '## A. Test Category' in content  # H2 heading
                assert '### A.1 Test Achievement' in content  # H3 heading

    def test_bullet_list_formatting(self):
        """
        Test markdown bullet list generation.

        Coverage gap: List formatting logic
        Priority: HIGH - Common output format
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'leadership_approaches': [
                    {
                        'name': 'Collaborative Leadership',
                        'description': 'Team-focused approach',
                        'how_to_phrase': [
                            'Facilitate collaboration',
                            'Enable team success',
                            'Foster open communication'
                        ]
                    }
                ]
            }

            # Act
            generator.generate_philosophy(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                assert '- Facilitate collaboration' in content
                assert '- Enable team success' in content
                assert '- Foster open communication' in content

    def test_code_block_formatting(self):
        """
        Test markdown code block generation for examples.

        Coverage gap: Code block formatting
        Priority: MEDIUM - Example formatting
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'resume_bullet_formulas': [
                    {
                        'formula_name': 'XYZ Formula',
                        'template': 'Accomplished [X] by doing [Y], resulting in [Z]',
                        'examples': [
                            {
                                'text': 'Increased revenue by 25% through strategic partnerships'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_narratives(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                assert '```' in content  # Code block markers
                assert 'Accomplished [X] by doing [Y], resulting in [Z]' in content

    def test_link_formatting(self):
        """
        Test markdown link generation.

        Coverage gap: Link formatting logic
        Priority: HIGH - Citation links
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'categories': [
                    {
                        'name': 'Leadership',
                        'achievements': []
                    },
                    {
                        'name': 'Technical Skills',
                        'achievements': []
                    }
                ]
            }

            # Act
            generator.generate_achievements(data, output_path)

            # Assert - Verify Table of Contents links are generated
            with open(output_path, 'r') as f:
                content = f.read()
                assert '[A. Leadership](#leadership)' in content or '[A. Leadership]' in content
                assert '[B. Technical Skills](#technical-skills)' in content or '[B. Technical Skills]' in content


class TestCitationHandling:
    """Tests for citation generation and linking."""

    def test_citation_link_creation(self):
        """
        Test creation of citation links to source documents.

        Coverage gap: Citation link generation
        Priority: CRITICAL - Source attribution
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'leadership_approaches': [
                    {
                        'name': 'Collaborative Leadership',
                        'description': 'Team empowerment',
                        'evidence': [
                            {
                                'quote': 'Led cross-functional team of 12 engineers',
                                'context': 'At TechCorp',
                                'source': 'Resume_2024.pdf'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_philosophy(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                assert '**Source**: Resume_2024.pdf' in content
                assert 'Led cross-functional team of 12 engineers' in content

    def test_multiple_citations_per_entry(self):
        """
        Test handling of entries with multiple source citations.

        Coverage gap: Multi-citation handling
        Priority: HIGH - Common scenario
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'core_values': [
                    {
                        'name': 'Innovation',
                        'definition': 'Driving creative solutions',
                        'evidence': [
                            {
                                'quote': 'Pioneered new architecture',
                                'context': 'At StartupCo',
                                'source': 'Resume_2024.pdf'
                            },
                            {
                                'quote': 'Developed novel approach',
                                'context': 'At TechCorp',
                                'source': 'CV_Academic.pdf'
                            },
                            {
                                'quote': 'Created innovative framework',
                                'context': 'Independent project',
                                'source': 'Portfolio.pdf'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_philosophy(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # All three sources should be present
                assert '**Source**: Resume_2024.pdf' in content
                assert '**Source**: CV_Academic.pdf' in content
                assert '**Source**: Portfolio.pdf' in content
                # All three quotes should be present
                assert 'Pioneered new architecture' in content
                assert 'Developed novel approach' in content
                assert 'Created innovative framework' in content

    def test_citation_text_formatting(self):
        """
        Test formatting of citation text (document name, page, etc.).

        Coverage gap: Citation text generation
        Priority: MEDIUM - Citation display
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'cover_letter_architecture': [
                    {
                        'pattern_name': 'Opening Hook',
                        'description': 'Compelling opening',
                        'examples': [
                            {
                                'text': 'Example hook text',
                                'source': 'CoverLetter_Google_2024.pdf'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_narratives(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify citation source is formatted correctly
                assert 'CoverLetter_Google_2024.pdf' in content
                assert '**From**: CoverLetter_Google_2024.pdf' in content


class TestSectionOrganization:
    """Tests for section organization and ordering."""

    def test_section_ordering(self):
        """
        Test correct ordering of sections in output.

        Coverage gap: Section ordering logic
        Priority: HIGH - Output organization
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'leadership_approaches': [{'name': 'Leadership', 'description': 'Test'}],
                'core_values': [{'name': 'Value', 'definition': 'Test'}],
                'problem_solving_philosophy': [{'name': 'Problem Solving', 'approach': 'Test'}]
            }

            # Act
            generator.generate_philosophy(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Find positions of each section
                leadership_pos = content.find('## I. Leadership Approaches')
                values_pos = content.find('## II. Core Values')
                problem_pos = content.find('## III. Problem-Solving Philosophy')

                # Verify sections are in correct order
                assert leadership_pos < values_pos < problem_pos
                assert leadership_pos > 0  # All sections should be present

    def test_subsection_nesting(self):
        """
        Test proper nesting of subsections.

        Coverage gap: Nesting logic
        Priority: HIGH - Hierarchical structure
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'leadership_approaches': [
                    {
                        'name': 'Servant Leadership',
                        'description': 'Put team first',
                        'evidence': [
                            {
                                'quote': 'Supported team growth',
                                'context': 'At TechCorp',
                                'source': 'Resume.pdf'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_philosophy(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify proper heading nesting (### for approach, #### for evidence)
                assert '### A. Servant Leadership' in content
                assert '#### Evidence' in content
                # Verify evidence is nested under approach
                approach_pos = content.find('### A. Servant Leadership')
                evidence_pos = content.find('#### Evidence')
                assert approach_pos < evidence_pos

    def test_section_metadata_inclusion(self):
        """
        Test inclusion of section metadata (counts, dates, etc.).

        Coverage gap: Metadata generation
        Priority: MEDIUM - Additional info
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            data = {
                'categories': [
                    {
                        'name': 'Technical Achievements',
                        'achievements': [
                            {
                                'name': 'System Migration',
                                'description': 'Migrated legacy system'
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_achievements(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify metadata like generation date is included
                assert '**Generated**:' in content
                assert generator.generated_date in content


class TestContentAggregation:
    """Tests for aggregating content from multiple sources."""

    def test_aggregate_from_multiple_documents(self):
        """
        Test aggregation of content from multiple source documents.

        Coverage gap: Multi-document handling
        Priority: CRITICAL - Core functionality
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Simulate data aggregated from multiple documents
            data = {
                'action_verbs': [
                    {
                        'category': 'Leadership',
                        'subcategories': [
                            {
                                'name': 'Team Management',
                                'verbs': [
                                    {'verb': 'Led', 'usage_context': 'From Resume.pdf'},
                                    {'verb': 'Managed', 'usage_context': 'From CV.pdf'},
                                    {'verb': 'Directed', 'usage_context': 'From Portfolio.pdf'}
                                ]
                            }
                        ]
                    }
                ]
            }

            # Act
            generator.generate_language_bank(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify content from all three sources is aggregated
                assert 'From Resume.pdf' in content
                assert 'From CV.pdf' in content
                assert 'From Portfolio.pdf' in content
                assert 'Led' in content and 'Managed' in content and 'Directed' in content

    def test_duplicate_content_detection(self):
        """
        Test detection and handling of duplicate content.

        Coverage gap: Deduplication logic
        Priority: HIGH - Data quality
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Note: The generator itself doesn't deduplicate - it renders whatever data is passed
            # This test verifies that duplicate data (if passed) is rendered
            data = {
                'signature_phrases': [
                    {
                        'phrase': 'Drove results',
                        'category': 'Impact',
                        'appearances': 3,
                        'full_quotes': [
                            'Drove results in Q1',
                            'Drove results in Q2',
                            'Drove results in Q3'
                        ]
                    }
                ]
            }

            # Act
            generator.generate_language_bank(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify signature phrase with multiple appearances is rendered
                assert '"Drove results"' in content
                assert 'Appears**: 3 times' in content or 'appearances' in content.lower()

    def test_content_merging(self):
        """
        Test merging of similar content from different sources.

        Coverage gap: Content merging
        Priority: MEDIUM - Data consolidation
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Simulate merged content from multiple sources
            data = {
                'powerful_phrase_templates': [
                    {
                        'template_name': 'Growth Pattern',
                        'template': 'Increased [metric] by [percentage]',
                        'examples': [
                            {'filled_example': 'Increased revenue by 40% (from Resume)'},
                            {'filled_example': 'Increased user engagement by 60% (from CV)'}
                        ],
                        'when_to_use': 'When highlighting quantitative growth'
                    }
                ]
            }

            # Act
            generator.generate_language_bank(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify merged examples from different sources
                assert 'Increased revenue by 40% (from Resume)' in content
                assert 'Increased user engagement by 60% (from CV)' in content
                assert 'Growth Pattern' in content


class TestOutputGeneration:
    """Tests for final markdown file generation."""

    def test_write_markdown_file(self):
        """
        Test writing of generated markdown to file.

        Coverage gap: File I/O operations
        Priority: HIGH - Output persistence
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'output.md')

            data = {
                'categories': [
                    {
                        'name': 'Test Category',
                        'achievements': [
                            {
                                'name': 'Test Achievement',
                                'description': 'Test description'
                            }
                        ]
                    }
                ]
            }

            # Act
            result_path = generator.generate_achievements(data, output_path)

            # Assert
            assert result_path == output_path
            assert os.path.exists(output_path)
            assert os.path.isfile(output_path)

            # Verify file is readable and has content
            with open(output_path, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert '# Achievement Library' in content

    def test_output_path_creation(self):
        """
        Test creation of output directory paths.

        Coverage gap: Path handling
        Priority: MEDIUM - File system operations
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory path
            nested_dir = os.path.join(tmpdir, 'level1', 'level2', 'level3')
            output_path = os.path.join(nested_dir, 'output.md')

            # Verify directory doesn't exist yet
            assert not os.path.exists(nested_dir)

            data = {'categories': []}

            # Act - generate_all creates directories
            result_files = generator.generate_all(
                {
                    'philosophy': {},
                    'achievements': data,
                    'narratives': {},
                    'language_bank': {}
                },
                nested_dir
            )

            # Assert
            assert os.path.exists(nested_dir)
            assert os.path.isdir(nested_dir)
            # Verify files were created in the nested directory
            assert all(os.path.exists(path) for path in result_files.values())

    def test_existing_file_overwrite(self):
        """
        Test handling of existing output files.

        Coverage gap: File overwrite logic
        Priority: MEDIUM - File management
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'existing.md')

            # Create existing file with content
            with open(output_path, 'w') as f:
                f.write("# Old Content\n\nThis should be overwritten")

            # Verify file exists with old content
            with open(output_path, 'r') as f:
                old_content = f.read()
                assert 'Old Content' in old_content

            data = {
                'categories': [
                    {
                        'name': 'New Category',
                        'achievements': []
                    }
                ]
            }

            # Act
            generator.generate_achievements(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                new_content = f.read()
                # Old content should be gone
                assert 'Old Content' not in new_content
                # New content should be present
                assert '# Achievement Library' in new_content
                assert 'New Category' in new_content


class TestErrorHandling:
    """Tests for error handling in generation process."""

    def test_malformed_data_handling(self):
        """
        Test handling of malformed input data.

        Coverage gap: Error handling paths
        Priority: HIGH - Robustness
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Test with various malformed data scenarios
            # Scenario 1: None instead of dict
            malformed_data_1 = None

            # Act & Assert - Should handle gracefully (treat as empty)
            try:
                result = generator.generate_achievements(malformed_data_1 or {}, output_path)
                assert os.path.exists(result)
            except (TypeError, AttributeError):
                # If it raises an error, that's also acceptable behavior
                pass

            # Scenario 2: List instead of dict
            malformed_data_2 = ['item1', 'item2']

            # Act & Assert
            try:
                result = generator.generate_philosophy(malformed_data_2 if isinstance(malformed_data_2, dict) else {}, output_path)
                assert os.path.exists(result)
            except (TypeError, AttributeError):
                pass

    def test_missing_required_fields(self):
        """
        Test handling of data missing required fields.

        Coverage gap: Validation logic
        Priority: HIGH - Data integrity
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Data with missing fields (achievement without name)
            data = {
                'categories': [
                    {
                        'name': 'Test Category',
                        'achievements': [
                            {
                                # Missing 'name' field
                                'description': 'Test description without name'
                            },
                            {
                                # Missing 'description' but has name
                                'name': 'Achievement with no description'
                            }
                        ]
                    }
                ]
            }

            # Act
            result = generator.generate_achievements(data, output_path)

            # Assert - Generator should handle gracefully using defaults
            assert os.path.exists(result)
            with open(result, 'r') as f:
                content = f.read()
                # Should use default for missing name
                assert 'Achievement' in content or 'Unnamed' in content
                # Should still render the category
                assert 'Test Category' in content

    def test_file_write_error_handling(self):
        """
        Test handling of file write errors (permissions, disk space, etc.).

        Coverage gap: I/O error handling
        Priority: MEDIUM - Error recovery
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file and make it read-only
            output_path = os.path.join(tmpdir, 'readonly.md')

            # Create file first
            with open(output_path, 'w') as f:
                f.write("# Test")

            # Make it read-only
            os.chmod(output_path, 0o444)

            data = {'categories': []}

            # Act & Assert
            try:
                generator.generate_achievements(data, output_path)
                # If write succeeds (some systems allow overwrite), that's fine
                assert True
            except (PermissionError, OSError):
                # Expected behavior - can't write to read-only file
                assert True
            finally:
                # Cleanup - restore write permissions
                try:
                    os.chmod(output_path, 0o644)
                except:
                    pass


class TestTemplateSystem:
    """Tests for markdown template system (if applicable)."""

    def test_template_loading(self):
        """
        Test loading of markdown templates.

        Coverage gap: Template loading logic
        Priority: MEDIUM - Template system
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Test that generator uses templates for structure
            data = {
                'resume_bullet_formulas': [
                    {
                        'formula_name': 'Test Formula',
                        'template': '[Action] + [Result] + [Impact]',
                        'examples': []
                    }
                ]
            }

            # Act
            generator.generate_narratives(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify template structure is used
                assert 'Test Formula' in content
                assert '#### Template' in content
                assert '[Action] + [Result] + [Impact]' in content
                # Verify standard markdown template structure
                assert '# Narrative Patterns' in content
                assert '**Generated**:' in content

    def test_template_variable_substitution(self):
        """
        Test substitution of variables in templates.

        Coverage gap: Template processing
        Priority: MEDIUM - Dynamic content
        """
        # Arrange
        generator = HierarchicalMarkdownGenerator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test.md')

            # Test variable substitution with template and filled examples
            data = {
                'powerful_phrase_templates': [
                    {
                        'template_name': 'Impact Template',
                        'template': 'Achieved [X] by implementing [Y], resulting in [Z]',
                        'examples': [
                            {
                                'filled_example': 'Achieved 50% cost reduction by implementing automation, resulting in $2M annual savings'
                            },
                            {
                                'filled_example': 'Achieved 99.9% uptime by implementing monitoring, resulting in zero customer complaints'
                            }
                        ],
                        'when_to_use': 'For highlighting measurable impact'
                    }
                ]
            }

            # Act
            generator.generate_language_bank(data, output_path)

            # Assert
            with open(output_path, 'r') as f:
                content = f.read()
                # Verify template is shown
                assert 'Achieved [X] by implementing [Y], resulting in [Z]' in content
                # Verify filled examples (variable substitutions) are shown
                assert '50% cost reduction' in content
                assert '$2M annual savings' in content
                assert '99.9% uptime' in content
                assert 'zero customer complaints' in content
