#!/usr/bin/env python3
"""
Analyze CV HTML to understand style usage patterns
"""
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def analyze_cv_styles(html_path):
    """Parse CV HTML and categorize styles by usage"""

    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract CSS definitions
    style_tag = soup.find('style')
    style_definitions = {}

    if style_tag:
        css_text = style_tag.string
        # Parse each style class
        for match in re.finditer(r'\.([a-z0-9]+)\s*\{([^}]+)\}', css_text, re.IGNORECASE):
            class_name = match.group(1)
            properties = match.group(2)
            style_definitions[class_name] = properties.strip()

    # Collect usage examples
    style_usage = defaultdict(list)

    # Find all elements with class
    for elem in soup.find_all(class_=True):
        classes = elem.get('class', [])
        text = elem.get_text(strip=True)

        if text and len(text) < 200:  # Keep examples short
            for cls in classes:
                if cls in style_definitions:
                    style_usage[cls].append(text[:100])

    return style_definitions, style_usage

def categorize_styles(style_definitions, style_usage, top_n=30):
    """Categorize styles by visual properties and semantic usage"""

    categories = {
        'headers': [],
        'body_text': [],
        'timeline_entries': [],
        'bullets': [],
        'emphasis': [],
        'colors': [],
        'small_text': []
    }

    for cls, props in style_definitions.items():
        examples = style_usage.get(cls, [])[:3]

        # Skip if never used
        if not examples:
            continue

        # Categorize by properties
        is_bold = 'font-weight: bold' in props
        is_italic = 'font-style: italic' in props
        has_orange = 'rgba(255,109' in props or 'rgba(255,134' in props
        has_gray = 'rgba(128,128,128' in props
        has_indent = 'margin-left: 72' in props or 'text-indent: -72' in props
        has_list = 'list-style-type: disc' in props

        size_match = re.search(r'font-size.*?(\d+)\.00pt', props)
        size = int(size_match.group(1)) if size_match else 9

        # Categorize
        if 'EDUCATION' in ''.join(examples) or 'PROFESSIONAL EXPERIENCE' in ''.join(examples):
            categories['headers'].append((cls, props, examples, len(style_usage.get(cls, []))))
        elif has_list:
            categories['bullets'].append((cls, props, examples, len(style_usage.get(cls, []))))
        elif has_indent:
            categories['timeline_entries'].append((cls, props, examples, len(style_usage.get(cls, []))))
        elif is_bold or is_italic:
            categories['emphasis'].append((cls, props, examples, len(style_usage.get(cls, []))))
        elif has_orange or has_gray:
            categories['colors'].append((cls, props, examples, len(style_usage.get(cls, []))))
        elif size < 8:
            categories['small_text'].append((cls, props, examples, len(style_usage.get(cls, []))))
        else:
            categories['body_text'].append((cls, props, examples, len(style_usage.get(cls, []))))

    return categories

def main():
    html_path = '/tmp/cv_fresh_analysis.html'

    print("Analyzing CV styles...\n")
    style_definitions, style_usage = analyze_cv_styles(html_path)

    print(f"Total styles defined: {len(style_definitions)}")
    print(f"Styles actually used: {len(style_usage)}\n")

    # Get top used styles
    top_styles = sorted(style_usage.items(), key=lambda x: len(x[1]), reverse=True)[:30]

    print("=" * 80)
    print("TOP 30 MOST USED STYLES (by element count)")
    print("=" * 80)

    for cls, examples in top_styles:
        count = len(examples)
        props = style_definitions.get(cls, 'Unknown')

        # Extract key properties
        size = re.search(r'font-size.*?(\d+)\.00pt', props)
        size_str = f"{size.group(1)}pt" if size else "?"

        bold = "bold" if 'font-weight: bold' in props else ""
        italic = "italic" if 'font-style: italic' in props else ""
        color = ""
        if 'rgba(255,109' in props:
            color = "orange"
        elif 'rgba(128,128,128' in props:
            color = "gray"
        elif 'rgba(0,0,0' in props:
            color = "black"

        list_type = "• list" if 'list-style-type: disc' in props else ""
        indent = "→indent" if 'margin-left: 72' in props or 'text-indent' in props else ""

        tags = ' '.join(filter(None, [size_str, bold, italic, color, list_type, indent]))

        print(f"\n{cls:<15} ({count:>3} uses) - {tags}")
        print(f"  Example: {examples[0][:80]}")

    # Categorize
    categories = categorize_styles(style_definitions, style_usage)

    print("\n" + "=" * 80)
    print("STYLE CATEGORIES")
    print("=" * 80)

    for cat_name, items in categories.items():
        if items:
            print(f"\n{cat_name.upper().replace('_', ' ')}:")
            # Sort by usage count
            items.sort(key=lambda x: x[3], reverse=True)
            for cls, props, examples, count in items[:5]:  # Top 5 per category
                print(f"  {cls:<15} ({count:>3} uses) - {examples[0][:60] if examples else ''}")

if __name__ == '__main__':
    main()
