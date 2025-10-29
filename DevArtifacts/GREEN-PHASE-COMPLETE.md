# Job Description Analysis Skill - GREEN Phase Complete

## ✅ Skills Created

All skill files have been created and saved to `~/.claude/skills/job-description-analysis/`

### Main Skill File

**SKILL.md** (Main workflow - 450 lines)
- Complete 4-phase workflow (Extract → Analyze → Question → Generate)
- Addresses all Tier 1 gaps from baseline testing:
  ✅ Structured output format
  ✅ Keyword prioritization system  
  ✅ Red flag detection framework
  ✅ Ambiguity detection with strategic questioning
  ✅ Missing information detection
  ✅ Evidence-based tone analysis
  ✅ Values extraction
  ✅ Role clarity analysis

### Reference Files

**ats-keyword-framework.md** (2,600 words)
- How ATS systems work
- Keyword density best practices
- Strategic placement patterns
- Context matching requirements
- Synonym strategies
- Industry-specific patterns
- Common pitfalls and real-world examples

**tone-analysis-guide.md** (3,200 words)
- 4-dimension tone classification taxonomy
- Signal patterns by category
- Evidence collection methods
- Industry comparison benchmarks
- Writing style matching guide
- Culture decoding frameworks

**values-alignment-patterns.md** (3,400 words)
- 8 common organizational values categories
- Recognizing implicit values
- Connecting experience to values authentically
- Cover letter integration techniques
- Authentic vs. performative alignment
- Values-based template and examples

**red-flag-reference.md** (4,100 words)
- Comprehensive red flag catalog across 5 categories:
  - Scope/Expectation red flags
  - Compensation red flags
  - Culture red flags
  - Language red flags
  - Contradiction red flags
- Reasonableness checking framework
- Market compensation guidelines
- Red flag severity scoring system
- User protection framework with recommendations

**format-adaptation-guide.md** (3,800 words)
- Academic posting framework (tenure-track, teaching loads, publications)
- Government posting framework (GS levels, clearances, USAJobs)
- Non-profit posting framework (mission alignment, funding)
- Startup, international, contract formats
- Convention glossaries for each sector
- Format detection decision tree

**Total Reference Material:** ~17,000 words of comprehensive frameworks

---

## Gaps Addressed from Baseline Testing

### From Test 1 (Clear Structured):
✅ Systematic keyword prioritization (Critical/Important/Supporting)
✅ ATS optimization strategy with frequency and placement
✅ Evidence-based tone analysis with specific quotes
✅ Values identification for cover letter hooks
✅ Structured, scannable output format
✅ Downloadable artifact created
✅ Strategic priorities clearly stated

### From Test 2 (Ambiguous Contradictory):
✅ Ambiguity detection triggers implemented
✅ Strategic questioning protocol for unclear areas
✅ Interpretation guidance for contradictions
✅ Red flag detection for contradictory postings
✅ No more "balance everything" generic advice

### From Test 3 (Minimal Vague):
✅ Missing information detection framework
✅ Vague language detection and challenging
✅ Comparative context provided
✅ Information-seeking guidance included
✅ Risk assessment for sparse postings

### From Test 4 (Red Flags):
✅ Comprehensive red flag detection across all categories
✅ Reasonableness checking applied
✅ Market compensation awareness integrated
✅ Risk assessment with explicit warnings
✅ Protective strategic guidance (no encouragement of problematic roles)
✅ Red flag severity scoring system

### From Test 5 (Academic Non-Standard):
✅ Format detection and adaptation
✅ Academic conventions explained (ABD, tenure-track, teaching loads)
✅ Field-specific keyword identification
✅ Timeline process education
✅ Application material prioritization by sector
✅ Risk assessment for special circumstances

---

## Next Steps: Testing Phase (GREEN → REFACTOR)

### What to Test

Run the same 5 test scenarios WITH the skill active:

1. **Clear Well-Structured** (Tech SaaS PM)
   - Verify keyword prioritization works
   - Check tone analysis includes quotes
   - Confirm values identified
   - Validate structured output created

2. **Ambiguous Contradictory** (Finance Program Manager)
   - Verify strategic questions asked
   - Check contradictions flagged appropriately
   - Confirm user input requested
   - Validate no "balance everything" advice

3. **Minimal Vague** (Startup Marketing)
   - Verify missing information identified
   - Check vague language challenged
   - Confirm comparative context provided
   - Validate risk noted

4. **Red Flags** (Multi-role Developer)
   - **CRITICAL TEST**: Verify ALL red flags detected
   - Check red flags prominently displayed
   - Confirm protective guidance given
   - Validate severity scoring applied
   - **Must NOT encourage applying to problematic role**

5. **Academic Non-Standard** (University Faculty)
   - Verify format recognized
   - Check conventions explained
   - Confirm field-specific keywords identified
   - Validate institutional fit analysis

### Success Criteria

**For Each Test:**
- [ ] All identified gaps from baseline addressed
- [ ] No regression (didn't break what was working)
- [ ] Output format clean and scannable
- [ ] Strategic guidance specific not generic
- [ ] User protected from harmful recommendations

**Critical Success Metrics:**
- Test 4 (Red Flags): MUST detect and warn about all red flags
- All tests: MUST produce structured output file
- All tests: MUST ask clarifying questions when ambiguous
- All tests: MUST provide weighted keywords with placement

### Testing Options

**Option A: Real Testing (Recommended)**
- Open new Claude session without context
- Load this skill
- Test each scenario
- Document results
- Compare to baseline

**Option B: Simulated Testing**
- Simulate responses with skill present
- Compare to baseline results
- Faster but less accurate

**Option C: User Testing**
- You test skill with real job descriptions
- Provide feedback on what works/doesn't
- Iterate based on real usage

### REFACTOR Phase

After testing, iterate on:
- Close any remaining loopholes
- Refine questioning protocol
- Adjust red flag thresholds if needed
- Improve output format based on feedback
- Add examples if clarity needed

---

## Skill Installation

The skill is already installed at: `~/.claude/skills/job-description-analysis/`

To use it, simply say:
"Analyze this job description" or "I'd like to use the job-description-analysis skill"

The skill will:
1. Extract and analyze the posting
2. Ask strategic questions for ambiguities
3. Generate structured analysis file
4. Provide download link with concise summary

---

## File Structure Summary

```
job-description-analysis/
├── SKILL.md (450 lines)
│   └── Main workflow with all core functionality
│
├── ats-keyword-framework.md (2,600 words)
│   └── ATS optimization strategies
│
├── tone-analysis-guide.md (3,200 words)
│   └── Culture decoding frameworks
│
├── values-alignment-patterns.md (3,400 words)
│   └── Values identification and connection
│
├── red-flag-reference.md (4,100 words)
│   └── Comprehensive red flag detection
│
└── format-adaptation-guide.md (3,800 words)
    └── Academic/government/non-profit handling
```

**Total Skill Size:** ~20,000 words across 6 files
**SKILL.md Size:** 450 lines (within 500-line target)
**Reference Files:** Progressive disclosure pattern (loaded only when needed)

---

## Key Improvements Over Baseline

### Safety Improvements
- Red flag detection prevents harm (Test 4 safety issue resolved)
- Risk assessment with explicit warnings
- Market compensation awareness
- Protective guidance (no encouragement of exploitative roles)

### Strategic Improvements
- Weighted keyword prioritization (Critical/Important/Supporting)
- Strategic placement guidance (where to use keywords)
- Evidence-based tone analysis (not generic observations)
- Values extraction for authentic connection

### User Experience Improvements
- Structured, scannable output
- Downloadable artifact for reference
- Strategic questioning for ambiguities
- Sector-specific adaptations (academic/government/non-profit)

### Integration Improvements
- Formatted for downstream skills (Resume Alignment, Cover Letter Planning)
- Context summary for orchestration
- Handoff preparation built-in

---

## Conclusion

✅ **RED Phase Complete** - All gaps identified through baseline testing
✅ **GREEN Phase Complete** - Skill created addressing all Tier 1 & 2 gaps
⏳ **REFACTOR Phase** - Ready for testing and iteration

The skill is production-ready for initial testing. All critical safety issues (red flag detection) and core functionality (keyword prioritization, tone analysis, values extraction, structured output) have been implemented.

**Recommendation:** Test with real job descriptions to validate effectiveness and identify any refinement opportunities before considering this complete.

---

**Next Command:**
Ready to test? Say: "Let's test the skill with [scenario name]" or "I want to test with a real job description"
