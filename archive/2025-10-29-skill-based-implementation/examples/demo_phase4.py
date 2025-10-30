"""
Phase 4 Demonstration
Shows the complete lexicon building and gap analysis pipeline
"""

from datetime import date, timedelta

from src.term_extractor import extract_terms_from_text, TermCategory
from src.context_analyzer import analyze_term_contexts
from src.term_categorizer import categorize_terms
from src.lexicon_builder import (
    SkillLexicon,
    DocumentMetadata,
    build_lexicon_from_documents
)
from src.gap_analyzer import analyze_job_fit, GapAnalyzer


def demo_phase_4():
    """Demonstrate Phase 4: Lexicon Building and Gap Analysis"""
    
    print("=" * 80)
    print("PHASE 4 DEMONSTRATION: Lexicon Building and Gap Analysis")
    print("=" * 80)
    print()
    
    # ========================================================================
    # PART 1: BUILD LEXICON FROM MULTIPLE DOCUMENTS
    # ========================================================================
    
    print("PART 1: BUILDING SKILL LEXICON FROM MULTIPLE DOCUMENTS")
    print("-" * 80)
    print()
    
    # Document 1: 2024 Resume (recent)
    resume_2024 = """
    Senior Software Engineer (2022-2024)
    
    Led development of Python microservices on AWS, serving 10M+ users.
    Architected data pipeline using Apache Spark, processing 5TB daily.
    Managed cross-functional team of 8 engineers using Agile methodology.
    Implemented machine learning models, improving accuracy by 35%.
    
    Expert in Docker, Kubernetes, CI/CD, and PostgreSQL.
    Strong leadership and communication skills.
    AWS Certified Solutions Architect.
    """
    
    # Document 2: 2023 Resume (older)
    resume_2023 = """
    Software Engineer (2020-2022)
    
    Developed Python applications for data processing.
    Built RESTful APIs using Django and Flask frameworks.
    Collaborated with team members on Agile projects.
    Used Git for version control and GitHub for collaboration.
    
    Proficient in Python, JavaScript, SQL, and AWS services.
    """
    
    # Document 3: Cover Letter
    cover_letter_2024 = """
    I am excited to apply for the Senior Engineering position.
    
    With 5+ years of Python development experience, I have led teams
    building scalable cloud infrastructure on AWS. My background in 
    machine learning and data engineering uniquely positions me to 
    contribute to your data platform initiatives.
    
    I am passionate about mentoring junior engineers and fostering
    collaborative team environments. My communication skills enable me
    to bridge technical and business stakeholders effectively.
    """
    
    # Process all documents
    documents_analysis = []
    
    # Process Resume 2024
    print("Processing: 2024 Resume")
    terms_2024 = extract_terms_from_text(resume_2024)
    contexts_2024 = analyze_term_contexts(terms_2024, resume_2024)
    categorized_2024 = categorize_terms(terms_2024, contexts_2024)
    
    metadata_2024 = DocumentMetadata(
        filename="resume_2024.pdf",
        document_type="resume",
        date=date.today(),
        target_position="Senior Software Engineer"
    )
    documents_analysis.append((metadata_2024, categorized_2024, contexts_2024))
    print(f"  Ã¢Å“" Extracted {len(terms_2024)} terms")
    print()
    
    # Process Resume 2023
    print("Processing: 2023 Resume")
    terms_2023 = extract_terms_from_text(resume_2023)
    contexts_2023 = analyze_term_contexts(terms_2023, resume_2023)
    categorized_2023 = categorize_terms(terms_2023, contexts_2023)
    
    metadata_2023 = DocumentMetadata(
        filename="resume_2023.pdf",
        document_type="resume",
        date=date.today() - timedelta(days=365),
        target_position="Software Engineer"
    )
    documents_analysis.append((metadata_2023, categorized_2023, contexts_2023))
    print(f"  Ã¢Å“" Extracted {len(terms_2023)} terms")
    print()
    
    # Process Cover Letter
    print("Processing: 2024 Cover Letter")
    terms_cl = extract_terms_from_text(cover_letter_2024)
    contexts_cl = analyze_term_contexts(terms_cl, cover_letter_2024)
    categorized_cl = categorize_terms(terms_cl, contexts_cl)
    
    metadata_cl = DocumentMetadata(
        filename="cover_letter_2024.pdf",
        document_type="cover_letter",
        date=date.today(),
        target_position="Senior Engineering Position"
    )
    documents_analysis.append((metadata_cl, categorized_cl, contexts_cl))
    print(f"  Ã¢Å“" Extracted {len(terms_cl)} terms")
    print()
    
    # Build unified lexicon
    print("Building Unified Skill Lexicon...")
    lexicon = build_lexicon_from_documents(documents_analysis)
    print(f"Ã¢Å“" Lexicon built with {len(lexicon.skills)} unique skills")
    print()
    print()
    
    # ========================================================================
    # LEXICON ANALYSIS
    # ========================================================================
    
    print("LEXICON ANALYSIS")
    print("-" * 80)
    print()
    
    # Generate skill profile
    profile = lexicon.generate_skill_profile()
    
    print("Skill Profile Summary:")
    print(f"  Total documents analyzed: {profile['total_documents_analyzed']}")
    print(f"  Total unique skills: {profile['total_unique_skills']}")
    print(f"  Transferable skills: {profile['transferable_skills_count']}")
    print(f"  Recent skills (last year): {profile['recent_skills_count']}")
    print()
    
    print("Skills by Domain:")
    for domain, count in sorted(profile['skills_by_domain'].items()):
        print(f"  {domain:20}: {count}")
    print()
    
    print("Skills by Role:")
    for role, count in sorted(profile['skills_by_role'].items())[:5]:
        print(f"  {role:20}: {count}")
    print()
    
    # Top skills by combined score
    top_combined = lexicon.get_top_skills(n=10, by='combined')
    print("Top 10 Skills (Combined Score):")
    for i, skill in enumerate(top_combined, 1):
        print(f"{i:2}. {skill.skill_name:20} | "
              f"Score: {skill.get_combined_score():.2f} | "
              f"Recency: {skill.get_recency_score():.2f} | "
              f"Docs: {skill.total_documents}")
    print()
    
    # Top recent skills
    top_recent = lexicon.get_top_skills(n=5, by='recency')
    print("Top 5 Most Recent Skills:")
    for i, skill in enumerate(top_recent, 1):
        last_used = skill.last_used.strftime("%Y-%m-%d") if skill.last_used else "Unknown"
        print(f"{i}. {skill.skill_name:20} | Last used: {last_used}")
    print()
    print()
    
    # ========================================================================
    # PART 2: JOB FIT ANALYSIS
    # ========================================================================
    
    print("PART 2: JOB FIT ANALYSIS")
    print("-" * 80)
    print()
    
    # Target job description
    job_description = """
    Principal Engineer - Data Platform
    
    Required:
    - 7+ years experience with Python and distributed systems
    - Expert knowledge of AWS services (EC2, S3, Lambda, EMR)
    - Experience with Apache Spark and large-scale data processing
    - Strong leadership and team management skills
    - Machine Learning experience required
    - CI/CD pipeline development
    
    Preferred:
    - Kubernetes and container orchestration
    - Terraform for infrastructure as code
    - Experience with real-time streaming (Kafka, Kinesis)
    - Background in data engineering or ML engineering
    """
    
    print("Target Position: Principal Engineer - Data Platform")
    print()
    
    # Extract requirements from job description
    print("Extracting job requirements...")
    job_terms = extract_terms_from_text(job_description)
    job_contexts = analyze_term_contexts(job_terms, job_description)
    job_categorized = categorize_terms(job_terms, job_contexts)
    
    # Separate required vs preferred (simplified - in real use would parse sections)
    required_skills = {
        "python": job_categorized.get("python"),
        "aws": job_categorized.get("aws"),
        "apache spark": job_categorized.get("apache spark"),
        "leadership": job_categorized.get("leadership"),
        "machine learning": job_categorized.get("machine learning"),
        "ci/cd": job_categorized.get("ci/cd"),
    }
    # Remove None values
    required_skills = {k: v for k, v in required_skills.items() if v is not None}
    
    preferred_skills = {
        "kubernetes": job_categorized.get("kubernetes"),
        "terraform": job_categorized.get("terraform"),
        "kafka": job_categorized.get("kafka"),
    }
    preferred_skills = {k: v for k, v in preferred_skills.items() if v is not None}
    
    print(f"  Required skills identified: {len(required_skills)}")
    print(f"  Preferred skills identified: {len(preferred_skills)}")
    print()
    
    # Run gap analysis
    print("Analyzing skill gaps...")
    report = analyze_job_fit(
        lexicon,
        "Principal Engineer - Data Platform",
        required_skills,
        preferred_skills,
        organization="TechCorp"
    )
    
    print(f"Ã¢Å“" Analysis complete")
    print()
    print()
    
    # ========================================================================
    # GAP ANALYSIS RESULTS
    # ========================================================================
    
    print("GAP ANALYSIS RESULTS")
    print("-" * 80)
    print()
    
    # Summary metrics
    summary = report.generate_summary()
    
    print("Overall Match Assessment:")
    print(f"  Match Percentage: {summary['match_percentage']:.1f}%")
    print(f"  Requirements Met: {summary['requirements_met']}/{summary['total_requirements']}")
    print(f"  Addressable Gaps: {summary['requirements_addressable']}")
    print()
    
    # Strengths
    print(f"Your Strengths ({len(report.exact_matches)} exact matches):")
    if report.exact_matches:
        for strength in report.exact_matches[:5]:
            print(f"  Ã¢Å“" {strength.skill.skill_name:20} | "
                  f"Emphasis: {strength.emphasis_score:.2f} | "
                  f"Used in {strength.skill.total_documents} docs")
    else:
        print("  (See strong and transferable matches below)")
    print()
    
    if report.strong_matches:
        print(f"Strong Matches ({len(report.strong_matches)}):")
        for strength in report.strong_matches[:5]:
            print(f"  Ã¢Å“" {strength.skill.skill_name:20} | "
                  f"Match: {strength.match_quality.value}")
        print()
    
    if report.transferable_matches:
        print(f"Transferable Skills ({len(report.transferable_matches)}):")
        for strength in report.transferable_matches[:5]:
            print(f"  Ã¢â€ ' {strength.skill.skill_name:20} | "
                  f"Relevance: {strength.emphasis_score:.2f}")
        print()
    
    # Gaps
    all_gaps = report.get_all_gaps()
    if all_gaps:
        print(f"Skill Gaps ({len(all_gaps)} identified):")
        
        if report.critical_gaps:
            print(f"  CRITICAL ({len(report.critical_gaps)}):")
            for gap in report.critical_gaps:
                print(f"    Ã¢â€”  {gap.required_skill}")
                if gap.bridging_strategy:
                    print(f"       Strategy: {gap.bridging_strategy}")
        
        if report.significant_gaps:
            print(f"  SIGNIFICANT ({len(report.significant_gaps)}):")
            for gap in report.significant_gaps:
                print(f"    Ã¢â€”â€  {gap.required_skill}")
        
        if report.moderate_gaps:
            print(f"  MODERATE ({len(report.moderate_gaps)}):")
            for gap in report.moderate_gaps[:3]:
                print(f"    Ã¢â€”â€¹ {gap.required_skill}")
        
        print()
    
    # ========================================================================
    # APPLICATION GUIDANCE
    # ========================================================================
    
    print("APPLICATION GUIDANCE")
    print("-" * 80)
    print()
    
    guidance = GapAnalyzer(lexicon).generate_application_guidance() if report else None
    
    if guidance:
        print("Resume Priorities:")
        print("  Must Include:")
        for skill in guidance['resume_priorities']['must_include'][:5]:
            print(f"    * {skill}")
        print()
        
        if guidance['resume_priorities']['use_these_verbs']:
            print("  Recommended Action Verbs:")
            for skill, verbs in list(guidance['resume_priorities']['use_these_verbs'].items())[:3]:
                print(f"    {skill}: {', '.join(verbs)}")
            print()
        
        print("Cover Letter Priorities:")
        print("  Lead With:")
        for skill in guidance['cover_letter_priorities']['lead_with_strengths'][:3]:
            print(f"    1. {skill}")
        print()
        
        if guidance['cover_letter_priorities']['address_gaps']:
            print("  Address These Gaps:")
            for item in guidance['cover_letter_priorities']['address_gaps'][:2]:
                print(f"    * {item['gap']}")
                print(f"      Ã¢â€ ' {item['strategy']}")
            print()
        
        print("Overall Strategy:")
        print(f"  {guidance['overall_strategy']}")
        print()
    
    print()
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("Phase 4 Features Demonstrated:")
    print("  Ã¢Å“" Lexicon building from multiple documents")
    print("  Ã¢Å“" Skill aggregation across time")
    print("  Ã¢Å“" Recency and frequency scoring")
    print("  Ã¢Å“" Job requirement extraction")
    print("  Ã¢Å“" Gap analysis and match detection")
    print("  Ã¢Å“" Application guidance generation")
    print()


if __name__ == "__main__":
    demo_phase_4()
