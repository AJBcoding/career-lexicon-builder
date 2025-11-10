"""Style consolidation mapping from 97 .pages styles to 12 semantic styles."""
from typing import Optional


# Consolidation map: old style class → semantic style name
# Based on usage analysis from analyze_cv_styles.py
STYLE_CONSOLIDATION = {
    # Character styles - Emphasis and formatting
    'ss2578': 'Play Title',       # 468 uses - bold italic (most used!)
    'ss40454': 'Play Title',       # duplicate - bold italic
    'ss2547': 'Play Title',        # duplicate - bold italic small

    'ss2592': 'Job Title',         # 28 uses - bold italic for positions
    'ss2508': 'Job Title',         # 22 uses - bold italic variant

    'ss2505': 'Institution',       # 48 uses - bold for institution names
    'ss93858': 'Institution',      # duplicate - bold
    'ss2543': 'Institution',       # duplicate - bold
    'ss138597': 'Institution',     # duplicate - bold black

    'ss2555': 'Orange Emphasis',   # 18 uses - bold orange
    'ss2561': 'Orange Emphasis',   # 5 uses - bold orange section headers
    'ss40405': 'Orange Emphasis',  # duplicate - bold orange small
    'ss52919': 'Orange Emphasis',  # duplicate - orange color only

    'ss2507': 'Gray Text',         # 5 uses - gray for dates
    'ss40419': 'Gray Text',        # 3 uses - gray duplicate
    'ss8153': 'Gray Text',         # 37 uses - used for secondary text
    'ss8151': 'Gray Text',         # 10 uses - duplicate

    # Paragraph styles - Structure
    'ps2539': 'Section Header',    # 19 uses - bold orange headers
    'ps2557': 'Section Header',    # 1 use - section header with indent
    'ps2551': 'Section Header',    # duplicate - bold orange

    'ps2554': 'CV Name',           # intro/name paragraph
    'ps27686': 'CV Name',          # duplicate

    'ps81934': 'Body Text',        # 25 uses - standard body
    'ps2548': 'Body Text',         # 85 uses - most used body text
    'ps2597': 'Body Text',         # 20 uses - duplicate
    'ps53936': 'Body Text',        # 57 uses - duplicate
    'ps8131': 'Body Text',         # 17 uses - duplicate
    'ps2573': 'Body Text',         # duplicate
    'ps2570': 'Body Text',         # duplicate
    'ps8343': 'Body Text',         # duplicate
    'ps8957': 'Body Text',         # duplicate
    'ps2599': 'Body Text',         # 17 uses - black body text

    'ps2532': 'Timeline Entry',    # 103 uses - gray with 72pt hanging indent
    'ps81930': 'Timeline Entry',   # black variant with hanging indent
    'ps2541': 'Timeline Entry',    # plain variant with hanging indent
    'ps52931': 'Timeline Entry',   # 11 uses - duplicate hanging indent
    'ps176105': 'Timeline Entry',  # 55 uses - indent variant
    'ps49520': 'Timeline Entry',   # 22 uses - indent variant

    # Bullet lists
    'ps40376': 'Bullet Standard',  # 254 uses - most common bullet style
    'ps40524': 'Bullet Standard',  # 79 uses - duplicate
    'ps40420': 'Bullet Standard',  # duplicate
    'ps40357': 'Bullet Standard',  # duplicate
    'ps40270': 'Bullet Standard',  # duplicate
    'ps40470': 'Bullet Standard',  # duplicate
    'ps40339': 'Bullet Standard',  # 17 uses - bullet with indent
    'ps40585': 'Bullet Standard',  # duplicate

    'ps40350': 'Bullet Gray',      # 14 uses - gray bullet duplicate
    'ps151234': 'Bullet Gray',     # 16 uses - gray justified

    'ps40465': 'Bullet Emphasis',  # 16 uses - bold italic bullets
    'ps46257': 'Bullet Emphasis',  # 24 uses - bold italic duplicate
    'ps40394': 'Bullet Emphasis',  # duplicate - bold italic
    'ps40547': 'Bullet Emphasis',  # duplicate
    'ps40503': 'Bullet Emphasis',  # duplicate
    'ps40592': 'Bullet Emphasis',  # 12 uses - duplicate
    'ps45767': 'Bullet Emphasis',  # 28 uses - bold italic variant
    'ps176103': 'Bullet Emphasis', # 55 uses - bold italic with indent
}


def get_semantic_name(old_class: str) -> Optional[str]:
    """
    Get semantic style name for old .pages style class.

    Args:
        old_class: Original style class name (e.g., 'ss2578')

    Returns:
        Semantic style name or None if not mapped
    """
    return STYLE_CONSOLIDATION.get(old_class)


def get_all_semantic_styles() -> set:
    """Get set of all unique semantic style names."""
    return set(STYLE_CONSOLIDATION.values())
