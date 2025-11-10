# Duplicate Styles in AJB CV 2024.pages

**Analysis Date:** 2025-11-09

---

## Summary

**Yes, there are significant duplicates!**

- **30 styles** (out of 97) have identical formatting
- These group into **9 duplicate groups**
- **21 redundant style definitions** (21.6% of total)
- Could consolidate 30 styles → 9 unique styles

### Breakdown:
- **Duplicate Paragraph Styles:** 21
- **Duplicate Character Styles:** 9
- **Truly Unique Styles:** 67

---

## Duplicate Groups

### Group 1: Black Bold Helvetica 9pt (Character Styles)
**2 identical styles:**
- `ss138597`
- `ss2505` ✓ (commonly used for institution names)

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
font-weight: bold
color: rgba(0,0,0,1.000)
```

**Recommendation:** Use `ss2505` (appears to be the primary)

---

### Group 2: Plain Helvetica 8pt (Paragraph Styles)
**2 identical styles:**
- `ps153763`
- `ps2590`

**Properties:**
```css
font-family: 'Helvetica'
font-size: 8pt
```

**Recommendation:** Consolidate to `ps2590`

---

### Group 3: Plain Helvetica 9pt ⚠️ LARGEST GROUP
**8 identical styles:**
- `ps2548`
- `ps2570`
- `ps2573`
- `ps2597`
- `ps81934` ✓ (most commonly used for body text)
- `ps8343`
- `ps8957`
- `ss8151` (character style)

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
```

**Impact:** This is the most basic body text style - having 8 versions is very redundant

**Recommendation:** Use `ps81934` for paragraphs, `ss8151` for character style

---

### Group 4: Bold Italic Helvetica 9pt (Mixed)
**3 identical styles:**
- `ps2544` (paragraph)
- `ps63797` (paragraph)
- `ss2592` ✓ (character - commonly used for job titles)

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
font-weight: bold
font-style: italic
```

**Recommendation:** Use `ss2592` for inline, `ps2544` for paragraphs

---

### Group 5: Bold Italic Bulleted List
**3 identical styles:**
- `ps40394`
- `ps40465`
- `ps40547`

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
font-weight: bold
font-style: italic
list-style-type: disc
margin-bottom: 6pt
margin-left: 72pt (conflicting with 0pt)
```

**Note:** Has conflicting margin-left values (both 0pt and 72pt defined)

**Recommendation:** Choose one and fix the margin conflict

---

### Group 6: Bold Helvetica 9pt (Character Styles)
**2 identical styles:**
- `ss2543`
- `ss93858` ✓ (used for institution names)

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
font-weight: bold
```

**Recommendation:** Use `ss93858`

---

### Group 7: Plain Bulleted List ⚠️ SECOND LARGEST
**5 identical styles:**
- `ps40270`
- `ps40357`
- `ps40376`
- `ps40420`
- `ps40470`

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
list-style-type: disc
margin-bottom: 6pt
margin-left: 72pt (conflicting with 0pt)
```

**Note:** Also has conflicting margin-left values

**Recommendation:** Choose one and fix margins

---

### Group 8: 72pt Hanging Indent
**2 identical styles:**
- `ps2541`
- `ps52931`

**Properties:**
```css
font-family: 'Helvetica'
font-size: 9pt
margin-left: 72pt
text-indent: -72pt
```

**This is your timeline/date style!**

**Recommendation:** Keep `ps2541` (lower number, likely original)

---

### Group 9: Bold Italic (Character Styles)
**3 identical styles:**
- `ss2578`
- `ss40327`
- `ss40454`

**Properties:**
```css
font-weight: bold
font-style: italic
```

**Note:** No font-family or size specified (inherits from parent)

**Recommendation:** Consolidate to `ss2578`

---

## Why Are There Duplicates?

### Possible Reasons:

1. **Copy-Paste Formatting**
   - When you copy/paste text, Pages sometimes creates new style variants
   - Even if formatting looks identical

2. **Style Inheritance Changes**
   - Modifying a paragraph may create a new style variant
   - Instead of updating the existing style

3. **Import from Other Documents**
   - Importing text from other documents brings their styles
   - Even if they match existing styles

4. **Manual Formatting**
   - Applying formatting manually creates new styles
   - Rather than selecting from style menu

5. **Pages Behavior**
   - Pages tends to create new styles liberally
   - Doesn't automatically merge identical styles

---

## Impact Analysis

### Storage/Performance:
- **Minimal impact** - 21 extra style definitions = ~2KB
- Not a performance concern

### Maintenance:
- **Moderate impact** - If you want to change body text formatting:
  - You'd need to update 8 different styles (Group 3)
  - Or risk inconsistent formatting

### Clarity:
- **High impact** - Hard to know which style to use
  - "Should I use ps81934, ps2548, or ps2570 for body text?"
  - All look identical but have different names

---

## Recommendations

### If Using Pages:

**Don't worry about it.**
- Pages creates these duplicates naturally
- They don't hurt anything
- Cleaning them up manually in Pages is tedious

### If Converting/Processing:

**Consolidate in your processing pipeline:**

```python
# Example: Map duplicates to primary styles
style_mapping = {
    # Group 3 - Body text
    'ps2548': 'ps81934',
    'ps2570': 'ps81934',
    'ps2573': 'ps81934',
    'ps2597': 'ps81934',
    'ps8343': 'ps81934',
    'ps8957': 'ps81934',

    # Group 7 - Lists
    'ps40270': 'ps40420',
    'ps40357': 'ps40420',
    'ps40376': 'ps40420',
    'ps40470': 'ps40420',

    # ... etc
}

# Apply mapping when processing
def normalize_style(style_class):
    return style_mapping.get(style_class, style_class)
```

### If Creating Templates:

**Use a consistent style set:**
- Define your core styles explicitly
- Use style menu instead of manual formatting
- Avoid copy-paste from other documents
- Periodically clean up unused styles

---

## Core Style Set Recommendation

Based on your actual usage, you really only need these **core styles**:

### Paragraph Styles (10 needed):
1. `ps81934` - Body text
2. `ps2532` - Gray timeline entries with hanging indent
3. `ps81930` - Black timeline entries with hanging indent
4. `ps2539` - Orange bold headers
5. `ps2557` - Section headers container
6. `ps2554` - Light intro text
7. `ps2544` - Bold italic emphasis
8. `ps2541` - Plain hanging indent
9. `ps40420` - Bulleted lists
10. `ps40394` - Bold italic bulleted lists

### Character Styles (8 needed):
1. `ss8151` - Plain text
2. `ss2505` - Bold black (institutions)
3. `ss93858` - Bold (alternative)
4. `ss2592` - Bold italic (job titles)
5. `ss2555` - Orange bold
6. `ss2561` - Orange bold headers
7. `ss2507` - Gray text
8. `ss2578` - Bold italic inline

**That's 18 styles instead of 97!**

---

## Conclusion

Your CV has **21 redundant style definitions (21.6%)**:
- ✅ Not a problem for Pages usage
- ⚠️ Could cause confusion when editing
- ✅ Easy to normalize in processing pipeline
- 💡 Consider using fewer styles in future documents

The duplicates don't hurt anything, but understanding them helps if you want to:
1. Process the document programmatically
2. Create cleaner templates
3. Maintain consistent formatting

**For your career-lexicon-builder project:**
Map duplicate styles to their primary versions when processing to simplify your code!
