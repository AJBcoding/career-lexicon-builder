"""Tests for CV learning system."""
import pytest
import yaml
from pathlib import Path
from datetime import datetime
from cv_formatting.learning_system import LearningSystem


@pytest.fixture
def temp_learned_file(tmp_path):
    """Create temporary learned preferences file."""
    learned_file = tmp_path / "learned-preferences.yaml"
    initial_data = {
        'style_rules': [],
        'metadata_defaults': {},
        'section_patterns': {}
    }
    with open(learned_file, 'w') as f:
        yaml.dump(initial_data, f)
    return learned_file


@pytest.fixture
def learning_system(temp_learned_file):
    """Create LearningSystem with temporary file."""
    return LearningSystem(str(temp_learned_file))


def test_load_empty_learned_preferences(learning_system):
    """Test loading empty learned preferences file."""
    assert learning_system.learned == {
        'style_rules': [],
        'metadata_defaults': {},
        'section_patterns': {}
    }


def test_learn_style_correction(learning_system):
    """Test learning a style correction."""
    learning_system.learn_correction(
        text="Graduate Studies Advisory Committee",
        context="service section",
        preferred_style="Gray Text"
    )

    assert len(learning_system.learned['style_rules']) == 1
    rule = learning_system.learned['style_rules'][0]
    assert rule['pattern'] == "Graduate Studies Advisory Committee"
    assert rule['preferred_style'] == "Gray Text"
    assert rule['context'] == "service section"
    assert 'learned_date' in rule


def test_apply_learned_style_rules(learning_system):
    """Test applying learned style rules to content."""
    # Learn a rule
    learning_system.learn_correction(
        text="Graduate Studies Advisory Committee",
        context="service",
        preferred_style="Gray Text"
    )

    # Apply to new content
    content = [
        {"text": "SERVICE", "style": "Section Header"},
        {"text": "Graduate Studies Advisory Committee", "style": "Body Text"}
    ]

    result = learning_system.apply_learned_patterns(content)

    # Should update the style based on learned rule
    assert result[1]['style'] == "Gray Text"


def test_apply_learned_patterns_no_match(learning_system):
    """Test applying learned patterns when no match found."""
    learning_system.learn_correction(
        text="committee role",
        context="service",
        preferred_style="Gray Text"
    )

    content = [
        {"text": "EDUCATION", "style": "Section Header"},
        {"text": "Different text", "style": "Body Text"}
    ]

    result = learning_system.apply_learned_patterns(content)

    # Should not change style
    assert result[1]['style'] == "Body Text"


def test_save_and_reload_learned_preferences(temp_learned_file):
    """Test saving and reloading learned preferences."""
    # Create system and learn something
    system1 = LearningSystem(str(temp_learned_file))
    system1.learn_correction(
        text="Romeo & Juliet",
        context="productions",
        preferred_style="Play Title"
    )

    # Create new system with same file
    system2 = LearningSystem(str(temp_learned_file))

    # Should have the learned rule
    assert len(system2.learned['style_rules']) == 1
    assert system2.learned['style_rules'][0]['pattern'] == "Romeo & Juliet"


def test_multiple_style_rules(learning_system):
    """Test learning multiple style rules."""
    learning_system.learn_correction(
        text="committee",
        context="service",
        preferred_style="Gray Text"
    )
    learning_system.learn_correction(
        text="Romeo & Juliet",
        context="productions",
        preferred_style="Play Title"
    )

    assert len(learning_system.learned['style_rules']) == 2


def test_context_matching(learning_system):
    """Test that style rules only apply in matching context."""
    learning_system.learn_correction(
        text="Dean",
        context="experience",
        preferred_style="Job Title"
    )

    # Should match in experience section
    content = [
        {"text": "EXPERIENCE", "style": "Section Header"},
        {"text": "Dean of Arts", "style": "Body Text"}
    ]
    result = learning_system.apply_learned_patterns(content)
    assert result[1]['style'] == "Job Title"

    # Should NOT match in different section
    content = [
        {"text": "EDUCATION", "style": "Section Header"},
        {"text": "Dean of Arts", "style": "Body Text"}
    ]
    result = learning_system.apply_learned_patterns(content)
    assert result[1]['style'] == "Body Text"


def test_pattern_matching_case_insensitive(learning_system):
    """Test pattern matching is case-insensitive."""
    learning_system.learn_correction(
        text="committee",
        context="service",
        preferred_style="Gray Text"
    )

    content = [
        {"text": "SERVICE", "style": "Section Header"},
        {"text": "Advisory Committee Meeting", "style": "Body Text"}
    ]

    result = learning_system.apply_learned_patterns(content)
    assert result[1]['style'] == "Gray Text"


def test_empty_style_rules(learning_system):
    """Test applying patterns when no rules learned."""
    content = [
        {"text": "EDUCATION", "style": "Section Header"},
        {"text": "Some content", "style": "Body Text"}
    ]

    result = learning_system.apply_learned_patterns(content)

    # Should return unchanged
    assert result == content
