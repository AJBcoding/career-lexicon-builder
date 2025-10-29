"""
Phase 3 Demonstration
Shows the complete term extraction, context analysis, and categorization pipeline
"""

from src.term_extractor import extract_terms_from_text, TermCategory
from src.context_analyzer import analyze_term_contexts, ActionVerbStrength
from src.term_categorizer import categorize_terms, SkillDomain, RoleCategory, TermCategorizer


def demo_phase_3():
    """Demonstrate the complete Phase 3 pipeline"""
    
    # Sample professional text (like from a resume)
    text = """
    Senior Software Engineer
    
    Led development of Python-based microservices architecture on AWS, 
    serving 10M+ users with 99.9% uptime. Architected data pipeline 
    processing 5TB daily using Apache Spark and Kafka.
    
    Managed cross-functional team of 8 engineers using Agile methodology.
    Implemented machine learning models improving recommendation accuracy by 35%.
    
    Strong leadership, communication, and problem-solving skills.
    Expert in Docker, Kubernetes, and CI/CD pipelines.
    
    AWS Certified Solutions Architect and PMP certified.
    """
    
    print("=" * 80)
    print("PHASE 3 DEMONSTRATION: Term Extraction and Analysis")
    print("=" * 80)
    print()
    
    # PHASE 3.1: TERM EXTRACTION
    print("PHASE 3.1: TERM EXTRACTION")
    print("-" * 80)
    
    terms = extract_terms_from_text(text)
    
    print(f"Extracted {len(terms)} unique terms\n")
    
    # Show top terms by confidence
    from src.term_extractor import TermExtractor
    extractor = TermExtractor()
    extractor.extracted_terms = terms
    top_terms = extractor.get_top_terms(n=10)
    
    print("Top 10 Terms by Confidence:")
    for i, term in enumerate(top_terms, 1):
        print(f"{i:2}. {term.text:25} | Category: {term.category.value:15} | "
              f"Confidence: {term.confidence:.2f} | Frequency: {term.frequency}")
    
    print()
    
    # Show terms by category
    print("Terms by Category:")
    categories = {}
    for term in terms.values():
        cat = term.category.value
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(term.text)
    
    for cat, cat_terms in sorted(categories.items()):
        print(f"  {cat:20}: {', '.join(sorted(cat_terms)[:5])}")
        if len(cat_terms) > 5:
            print(f"                         ...and {len(cat_terms) - 5} more")
    
    print()
    print()
    
    # PHASE 3.2: CONTEXT ANALYSIS
    print("PHASE 3.2: CONTEXT ANALYSIS")
    print("-" * 80)
    
    contexts = analyze_term_contexts(terms, text)
    
    print(f"Analyzed context for {len(contexts)} terms\n")
    
    # Show terms with strong action verbs
    from src.context_analyzer import ContextAnalyzer
    analyzer = ContextAnalyzer()
    analyzer.analyzed_contexts = contexts
    
    strong_verb_terms = analyzer.get_terms_with_strong_verbs()
    print(f"Terms with Strong Action Verbs ({len(strong_verb_terms)} found):")
    for ctx in strong_verb_terms[:5]:
        strongest = ctx.get_strongest_verb()
        if strongest:
            verb, strength = strongest
            print(f"  {ctx.term.text:20} â†’ {verb} ({strength.value})")
    
    print()
    
    # Show terms with quantifiable impact
    quantified_terms = analyzer.get_terms_with_quantifiable_impact()
    print(f"Terms with Quantifiable Impact ({len(quantified_terms)} found):")
    for ctx in quantified_terms[:5]:
        quants = ', '.join(ctx.quantifiers)
        print(f"  {ctx.term.text:20} â†’ {quants}")
    
    print()
    
    # Show top prominent terms
    top_prominent = analyzer.get_top_prominent_terms(n=5)
    print("Top 5 Most Prominent Terms:")
    for ctx in top_prominent:
        print(f"  {ctx.term.text:20} | Prominence: {ctx.prominence_score:.2f}")
    
    print()
    
    # Context report
    report = analyzer.generate_context_report()
    print("Context Analysis Summary:")
    print(f"  Total terms analyzed: {report['total_terms']}")
    print(f"  Terms with strong verbs: {report['with_strong_verbs']}")
    print(f"  Terms with quantifiers: {report['with_quantifiers']}")
    print(f"  Average prominence: {report['avg_prominence']:.2f}")
    
    print()
    print()
    
    # PHASE 3.3: TERM CATEGORIZATION
    print("PHASE 3.3: TERM CATEGORIZATION")
    print("-" * 80)
    
    categorized = categorize_terms(terms, contexts)
    
    print(f"Categorized {len(categorized)} terms\n")
    
    # Set up categorizer for filtering
    categorizer = TermCategorizer()
    categorizer.categorized_terms = categorized
    
    # Show terms by skill domain
    print("Terms by Skill Domain:")
    for domain in SkillDomain:
        if domain == SkillDomain.UNKNOWN:
            continue
        domain_terms = categorizer.get_by_domain(domain)
        if domain_terms:
            term_names = [t.term.text for t in domain_terms]
            print(f"  {domain.value:15}: {', '.join(term_names[:5])}")
            if len(term_names) > 5:
                print(f"                    ...and {len(term_names) - 5} more")
    
    print()
    
    # Show terms by role category
    print("Terms by Role Category:")
    for role in [RoleCategory.ENGINEERING, RoleCategory.DATA_SCIENCE, 
                 RoleCategory.PRODUCT, RoleCategory.GENERAL]:
        role_terms = categorizer.get_by_role(role)
        if role_terms:
            term_names = [t.term.text for t in role_terms]
            print(f"  {role.value:15}: {', '.join(term_names[:5])}")
            if len(term_names) > 5:
                print(f"                    ...and {len(term_names) - 5} more")
    
    print()
    
    # Show terms by skill level
    print("Terms by Skill Level:")
    for level in ['expert', 'senior', 'mid', 'junior']:
        level_terms = categorizer.get_by_skill_level(level)
        if level_terms:
            term_names = [t.term.text for t in level_terms]
            print(f"  {level:10}: {', '.join(term_names)}")
    
    print()
    
    # Show transferable skills
    transferable = categorizer.get_transferable_skills()
    print(f"Transferable Skills ({len(transferable)} found):")
    transfer_names = [t.term.text for t in transferable]
    print(f"  {', '.join(transfer_names)}")
    
    print()
    
    # Taxonomy report
    tax_report = categorizer.generate_taxonomy_report()
    print("Categorization Summary:")
    print(f"  Total terms: {tax_report['total_terms']}")
    print(f"  By domain: {tax_report['by_domain']}")
    print(f"  By role: {tax_report['by_role']}")
    print(f"  Transferable: {tax_report['transferable_count']}")
    print(f"  Industry-specific: {tax_report['industry_specific_count']}")
    
    print()
    print()
    
    # DETAILED EXAMPLE: Single Term Through Pipeline
    print("DETAILED EXAMPLE: 'Python' Through Complete Pipeline")
    print("-" * 80)
    
    if 'python' in terms:
        python_term = terms['python']
        python_context = contexts.get('python')
        python_cat = categorized.get('python')
        
        print("1. EXTRACTED TERM:")
        print(f"   Text: {python_term.text}")
        print(f"   Category: {python_term.category.value}")
        print(f"   Frequency: {python_term.frequency}")
        print(f"   Confidence: {python_term.confidence:.2f}")
        print(f"   Positions: {python_term.positions}")
        print()
        
        print("2. CONTEXT ANALYSIS:")
        if python_context:
            print(f"   Prominence Score: {python_context.prominence_score:.2f}")
            if python_context.action_verbs:
                print(f"   Action Verbs: {python_context.action_verbs}")
                strongest = python_context.get_strongest_verb()
                if strongest:
                    print(f"   Strongest Verb: {strongest[0]} ({strongest[1].value})")
            if python_context.quantifiers:
                print(f"   Quantifiers: {python_context.quantifiers}")
        print()
        
        print("3. CATEGORIZATION:")
        if python_cat:
            print(f"   Skill Domain: {python_cat.skill_domain.value}")
            print(f"   Role Categories: {[r.value for r in python_cat.role_categories]}")
            print(f"   Skill Level: {python_cat.skill_level or 'Not inferred'}")
            print(f"   Transferable: {python_cat.is_transferable()}")
            print(f"   Industry Specific: {python_cat.industry_specific}")
    
    print()
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    demo_phase_3()
