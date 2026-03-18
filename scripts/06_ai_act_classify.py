"""
06_ai_act_classify.py — Classify ISCO 3-digit groups against EU AI Act Annex III,
Platform Work Directive, Pay Transparency Directive, and national frameworks (DE/AT/CH).

All legal references verified against source texts in data/legal/ as of 17 March 2026.

Sources:
  - EU AI Act: Regulation (EU) 2024/1689, Annex III (OJ L 2024/1689, pp. 127-129)
  - Platform Work Directive: Directive (EU) 2024/2831
  - Pay Transparency Directive: Directive (EU) 2023/970
  - GDPR: Regulation (EU) 2016/679 (Art 22, 35, 88)
  - BetrVG: §87(1) Nr. 6, Nr. 7
  - ArbVG: §96(1) Nr. 3, §96a(1) Nr. 1
  - Swiss FADP: Art. 21
  - Swiss OR: Art. 328, 328b
  - Swiss ArGV3: Art. 26
  - Swiss Mitwirkungsgesetz: SR 822.14

Input:  occupations.csv (ISCO 3-digit groups)
Output: data/manual/ai_act_high_risk.json
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "occupations.csv"
OUTPUT = ROOT / "data" / "manual" / "ai_act_high_risk.json"

# =============================================================================
# ANNEX III CATEGORIES (verified from OJ L 2024/1689, pp. 127-129)
# =============================================================================
ANNEX_III = {
    "biometrics": "1. Biometrics: remote biometric identification, categorisation, emotion recognition",
    "critical_infrastructure": "2. Critical infrastructure: safety components in management/operation of critical digital infrastructure, road traffic, water/gas/heating/electricity",
    "education": "3. Education & vocational training: access/admission, evaluate learning outcomes, assess education level, monitor tests",
    "employment": "4. Employment, workers' management, access to self-employment: recruitment/selection, decisions on terms/promotion/termination, task allocation, monitor/evaluate performance",
    "essential_services": "5. Essential services: public assistance eligibility, creditworthiness, insurance risk, emergency dispatch/triage",
    "law_enforcement": "6. Law enforcement: risk assessment, polygraphs, evidence reliability, profiling, crime detection",
    "migration": "7. Migration, asylum, border control: polygraphs, risk assessment, application examination, detecting persons",
    "justice": "8. Administration of justice & democratic processes: legal research, applying law, dispute resolution, influencing elections",
}

# =============================================================================
# DEPLOYER MAPPINGS — which occupations DEPLOY high-risk AI on others
# Based on Annex III category definitions cross-referenced with ISCO duties
# =============================================================================

# Category 1: Biometrics deployers — security, law enforcement, border
BIOMETRICS_DEPLOYERS = {"541"}  # Protective services workers

# Category 2: Critical infrastructure deployers
CRITICAL_INFRA_DEPLOYERS = {
    "133",  # ICT service managers
    "214",  # Engineering professionals
    "215",  # Electrotechnology engineers
    "251",  # Software developers (when building critical systems)
    "252",  # Database and network professionals
    "311",  # Physical/engineering science technicians
    "313",  # Process control technicians
    "315",  # Ship and aircraft controllers
    "351",  # ICT operations technicians
    "831",  # Locomotive engine drivers
    "833",  # Heavy truck and bus drivers
    "835",  # Ships' deck crews
}

# Category 3: Education deployers
EDUCATION_DEPLOYERS = {
    "231",  # University teachers
    "232",  # Vocational education teachers
    "233",  # Secondary education teachers
    "234",  # Primary/early childhood teachers
    "235",  # Other teaching professionals
}

# Category 4: Employment deployers — HR, management roles that use AI for
# recruitment, evaluation, task allocation, performance monitoring
EMPLOYMENT_DEPLOYERS = {
    "111",  # Legislators and senior officials
    "112",  # Managing directors and chief executives
    "121",  # Business services and administration managers
    "122",  # Sales, marketing and development managers
    "131",  # Production managers agriculture
    "132",  # Manufacturing/mining/construction managers
    "133",  # ICT service managers
    "134",  # Professional services managers
    "141",  # Hotel and restaurant managers
    "142",  # Retail and wholesale trade managers
    "143",  # Other services managers
    "242",  # Administration professionals (HR)
    "334",  # Administrative and specialised secretaries
    "335",  # Regulatory government associate professionals
}

# Category 5: Essential services deployers
ESSENTIAL_SERVICES_DEPLOYERS = {
    "221",  # Medical doctors (triage, diagnostics)
    "222",  # Nursing and midwifery professionals
    "226",  # Other health professionals
    "241",  # Finance professionals (credit scoring, insurance)
    "331",  # Financial/mathematical associate professionals
    "332",  # Sales and purchasing agents (insurance)
    "335",  # Regulatory government professionals
    "421",  # Tellers, money collectors
}

# Category 6: Law enforcement deployers
LAW_ENFORCEMENT_DEPLOYERS = {
    "335",  # Regulatory government associate professionals
    "541",  # Protective services workers
}

# Category 7: Migration deployers
MIGRATION_DEPLOYERS = {
    "335",  # Regulatory government associate professionals
}

# Category 8: Justice deployers
JUSTICE_DEPLOYERS = {
    "261",  # Legal professionals
    "341",  # Legal, social and religious associate professionals
    "111",  # Legislators and senior officials
}

# =============================================================================
# PLATFORM WORK DIRECTIVE — Directive (EU) 2024/2831
# Flag occupations where platform/gig work is common
# =============================================================================
PLATFORM_WORK_RELEVANT = {
    "511",  # Travel attendants, conductors, guides
    "512",  # Cooks (ghost kitchens, delivery platforms)
    "513",  # Waiters and bartenders
    "514",  # Hairdressers, beauticians
    "515",  # Building and housekeeping supervisors
    "516",  # Other personal services workers
    "521",  # Street and market salespersons
    "522",  # Shop salespersons (marketplace platforms)
    "524",  # Other sales workers
    "531",  # Child care workers
    "532",  # Personal care workers
    "611",  # Market gardeners
    "711",  # Building frame workers
    "712",  # Building finishers
    "713",  # Painters, cleaners
    "723",  # Machinery mechanics
    "741",  # Electrical equipment installers
    "742",  # Electronics installers
    "832",  # Car, van and motorcycle drivers (ride-hailing)
    "833",  # Heavy truck and bus drivers (freight platforms)
    "911",  # Domestic, hotel, office cleaners (cleaning platforms)
    "912",  # Vehicle/window/laundry cleaners
    "933",  # Transport and storage labourers (delivery)
    "941",  # Food preparation assistants (dark kitchens)
    "951",  # Street and related service workers
    "952",  # Street vendors
    "251",  # Software developers (freelance platforms)
    "264",  # Authors, journalists, linguists (freelance platforms)
    "265",  # Creative and performing artists (freelance platforms)
    "216",  # Architects, designers (freelance platforms)
    "243",  # Sales, marketing, PR professionals (freelance)
}

# =============================================================================
# PAY TRANSPARENCY DIRECTIVE — Directive (EU) 2023/970
# Flag occupations where AI-assisted compensation/promotion decisions are likely
# =============================================================================
PAY_TRANSPARENCY_RELEVANT = {
    "112",  # Managing directors
    "121",  # Business services managers
    "122",  # Sales, marketing managers
    "131",  # Production managers
    "132",  # Manufacturing managers
    "133",  # ICT service managers
    "134",  # Professional services managers
    "141",  # Hotel/restaurant managers
    "142",  # Retail/wholesale managers
    "143",  # Other services managers
    "241",  # Finance professionals
    "242",  # Administration professionals (HR/compensation)
    "243",  # Sales/marketing professionals (commission structures)
    "251",  # Software developers (tech compensation AI)
    "252",  # Database/network professionals
    "331",  # Financial associates
    "334",  # Administrative secretaries
    "335",  # Regulatory government professionals
    "411",  # General office clerks
    "431",  # Numerical clerks
}


def get_deployer_categories(isco3):
    """Determine which Annex III categories this occupation deploys."""
    cats = []
    if isco3 in BIOMETRICS_DEPLOYERS:
        cats.append("biometrics")
    if isco3 in CRITICAL_INFRA_DEPLOYERS:
        cats.append("critical_infrastructure")
    if isco3 in EDUCATION_DEPLOYERS:
        cats.append("education")
    if isco3 in EMPLOYMENT_DEPLOYERS:
        cats.append("employment")
    if isco3 in ESSENTIAL_SERVICES_DEPLOYERS:
        cats.append("essential_services")
    if isco3 in LAW_ENFORCEMENT_DEPLOYERS:
        cats.append("law_enforcement")
    if isco3 in MIGRATION_DEPLOYERS:
        cats.append("migration")
    if isco3 in JUSTICE_DEPLOYERS:
        cats.append("justice")
    return cats


def get_subject_explanation(isco3, label):
    """Generate explanation of why this group is high-risk as subject."""
    return (
        f"Workers in '{label}' are subject to AI-assisted recruitment screening, "
        f"performance evaluation, task allocation, and workforce management under "
        f"Annex III category 4 (employment). Employers deploying AI systems for "
        f"these purposes must comply with high-risk requirements."
    )


def get_deployer_explanation(isco3, label, deployer_cats):
    """Generate explanation of deployer status."""
    if not deployer_cats:
        return (
            f"'{label}' does not inherently involve deploying high-risk AI systems "
            f"on others, though individual employers in this sector may use such systems."
        )

    cat_descriptions = {
        "biometrics": "biometric identification/categorisation systems (Annex III cat. 1)",
        "critical_infrastructure": "AI safety components in critical infrastructure (Annex III cat. 2)",
        "education": "AI systems for educational access, assessment, or monitoring (Annex III cat. 3)",
        "employment": "AI for recruitment, evaluation, task allocation, or performance monitoring (Annex III cat. 4)",
        "essential_services": "AI for creditworthiness, insurance risk, healthcare triage, or public benefits eligibility (Annex III cat. 5)",
        "law_enforcement": "AI for risk assessment, evidence evaluation, or criminal profiling (Annex III cat. 6)",
        "migration": "AI for migration risk assessment or application examination (Annex III cat. 7)",
        "justice": "AI for legal research, applying law, or dispute resolution (Annex III cat. 8)",
    }
    descs = [cat_descriptions[c] for c in deployer_cats]
    return f"'{label}' may deploy {'; '.join(descs)}."


def get_eu_obligations(isco3, deployer_cats):
    """List applicable EU obligations."""
    obligations = [
        "AI Act Art 26(7): Employer must inform worker representatives before deploying high-risk AI",
        "AI Act Art 14: Human oversight required for AI-assisted employment decisions",
        "GDPR Art 22: Right against solely automated decisions with legal/significant effects",
    ]

    if deployer_cats:
        obligations.append(
            "AI Act Art 13: Deployers must ensure transparency and provide information"
        )
        obligations.append(
            "AI Act Art 9: Deployers of high-risk AI must implement risk management"
        )

    if "education" in deployer_cats:
        obligations.append(
            "AI Act Annex III(3): High-risk classification for AI in educational assessment"
        )

    if "essential_services" in deployer_cats:
        obligations.append(
            "AI Act Annex III(5): High-risk classification for AI in essential services access"
        )
        obligations.append(
            "GDPR Art 35: Data Protection Impact Assessment required"
        )

    if "law_enforcement" in deployer_cats or "migration" in deployer_cats:
        obligations.append(
            "AI Act Art 99: Penalties up to €35M or 7% global turnover for non-compliance"
        )

    return obligations


def get_works_council_de(isco3):
    """German works council (BetrVG) obligations."""
    # BetrVG §87(1) Nr. 6 applies universally to ANY technical device
    # that monitors employee behaviour or performance
    return {
        "triggered": True,
        "provision": "BetrVG §87(1) Nr. 6",
        "description": (
            "Co-determination required for introduction and use of technical devices "
            "designed to monitor employee behaviour or performance. Works council must "
            "agree before any AI monitoring system is deployed. §87(1) Nr. 7 additionally "
            "covers health and safety aspects of AI workplace tools."
        ),
    }


def get_works_council_at(isco3):
    """Austrian works council (ArbVG) obligations."""
    # ArbVG §96(1) Nr. 3 and §96a(1) Nr. 1 apply to systems that
    # assess employee behaviour or automate personal data processing
    return {
        "triggered": True,
        "provision": "ArbVG §96a(1) Nr. 1, §96(1) Nr. 3",
        "description": (
            "Works council consent required for introduction of systems that automate "
            "collection, processing and transmission of personal employee data (§96a(1) Nr. 1). "
            "Separate consent required for systems assessing employee behaviour (§96(1) Nr. 3). "
            "§91 provides additional information and consultation rights."
        ),
    }


def get_switzerland(isco3, deployer_cats):
    """Swiss regulatory framework assessment."""
    fadp_relevant = True  # FADP Art 21 applies to all automated decisions
    or_relevant = True  # OR 328b applies to all employment data processing
    argv3_relevant = True  # ArGV3 Art 26 applies to behaviour monitoring
    mitwirkung_relevant = False  # Mitwirkungsgesetz = consultation only, no co-determination

    desc_parts = [
        "FADP Art 21: Duty to inform data subjects about automated individual decisions "
        "with legal consequence or considerable adverse effect.",
        "OR Art 328b: Employer data processing limited to job-suitability and "
        "contract-performance purposes (stricter scope than GDPR, civil law enforcement).",
        "ArGV3 Art 26: Monitoring systems whose sole/main purpose is monitoring "
        "employee behaviour are prohibited; permitted only for legitimate purposes "
        "(safety, work organisation) if proportionate and employees informed.",
        "Mitwirkungsgesetz (SR 822.14): Information and consultation rights only — "
        "no co-determination. Employers must inform and consult but NOT obtain consent.",
    ]

    if deployer_cats:
        desc_parts.append(
            "Note: Swiss firms serving EU clients face extraterritorial AI Act compliance "
            "under Art 2(1)(c), but domestic-only employers face lighter obligations."
        )

    return {
        "fadp_art21_relevant": fadp_relevant,
        "or_328b_relevant": or_relevant,
        "argv3_art26_relevant": argv3_relevant,
        "mitwirkung_relevant": mitwirkung_relevant,
        "description": " ".join(desc_parts),
    }


def count_regulatory_surface(deployer_cats, platform_work, pay_transparency):
    """Count number of distinct regulatory frameworks applicable."""
    count = 2  # AI Act (as subject) + GDPR always apply
    if deployer_cats:
        count += 1  # AI Act deployer obligations
    if platform_work:
        count += 1  # Platform Work Directive
    if pay_transparency:
        count += 1  # Pay Transparency Directive
    # National frameworks: BetrVG/ArbVG always triggered, so +1 for DACH context
    count += 1
    return count


def get_regulations_applicable(deployer_cats, platform_work, pay_transparency):
    """List all applicable regulation names."""
    regs = ["AI Act", "GDPR"]
    if deployer_cats:
        regs[0] = "AI Act (subject + deployer)"
    else:
        regs[0] = "AI Act (subject)"
    if platform_work:
        regs.append("Platform Work Directive")
    if pay_transparency:
        regs.append("Pay Transparency Directive")
    regs.append("BetrVG (DE) / ArbVG (AT)")
    regs.append("FADP/OR/ArGV3 (CH)")
    return regs


def classify_occupation(isco3, label):
    """Classify a single ISCO 3-digit occupation group."""
    deployer_cats = get_deployer_categories(isco3)
    is_deployer = len(deployer_cats) > 0
    platform_work = isco3 in PLATFORM_WORK_RELEVANT
    pay_transparency = isco3 in PAY_TRANSPARENCY_RELEVANT

    # All occupations are high_risk_as_subject (Annex III cat 4 = employment)
    subject_cats = ["employment"]

    # Add additional subject categories for specific occupations
    # Workers in education are also subject to education AI
    if isco3 in EDUCATION_DEPLOYERS or isco3 in {"531"}:
        if "education" not in subject_cats:
            subject_cats.append("education")

    # Workers in law enforcement subject to law enforcement AI
    if isco3 in {"541"}:
        if "law_enforcement" not in subject_cats:
            subject_cats.append("law_enforcement")

    # Workers in critical infrastructure subject to critical infra AI
    if isco3 in CRITICAL_INFRA_DEPLOYERS:
        if "critical_infrastructure" not in subject_cats:
            subject_cats.append("critical_infrastructure")

    entry = {
        "isco3": isco3,
        "label": label,
        "ai_act_categories_as_subject": subject_cats,
        "ai_act_categories_as_deployer": deployer_cats,
        "high_risk_as_subject": True,
        "high_risk_as_deployer": is_deployer,
        "subject_explanation": get_subject_explanation(isco3, label),
        "deployer_explanation": get_deployer_explanation(isco3, label, deployer_cats),
        "eu_obligations": get_eu_obligations(isco3, deployer_cats),
        "platform_work_directive_relevant": platform_work,
        "pay_transparency_relevant": pay_transparency,
        "works_council_de": get_works_council_de(isco3),
        "works_council_at": get_works_council_at(isco3),
        "switzerland": get_switzerland(isco3, deployer_cats),
        "regulatory_surface_count": count_regulatory_surface(
            deployer_cats, platform_work, pay_transparency
        ),
        "regulations_applicable": get_regulations_applicable(
            deployer_cats, platform_work, pay_transparency
        ),
    }
    return entry


def main():
    print("Loading occupations...")
    df = pd.read_csv(INPUT, dtype={"isco3": str, "isco2": str, "isco1": str})
    print(f"  {len(df)} occupation groups")

    results = {}
    deployer_count = 0
    platform_count = 0
    pay_trans_count = 0
    total_surface = 0

    for _, row in df.iterrows():
        isco3 = row["isco3"]
        label = row["isco3_label"]
        entry = classify_occupation(isco3, label)
        results[isco3] = entry

        if entry["high_risk_as_deployer"]:
            deployer_count += 1
        if entry["platform_work_directive_relevant"]:
            platform_count += 1
        if entry["pay_transparency_relevant"]:
            pay_trans_count += 1
        total_surface += entry["regulatory_surface_count"]

    # Save output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nOutput: {OUTPUT}")
    print(f"  Total groups classified: {len(results)}")
    print(f"  High-risk as deployer: {deployer_count}")
    print(f"  Platform Work Directive relevant: {platform_count}")
    print(f"  Pay Transparency Directive relevant: {pay_trans_count}")
    print(f"  Average regulatory surface: {total_surface / len(results):.1f}")

    # Print spot-check groups
    spot_check = ["251", "261", "112", "226", "516", "833", "411"]
    print(f"\n{'='*60}")
    print("SPOT-CHECK RESULTS")
    print(f"{'='*60}")
    for isco3 in spot_check:
        entry = results[isco3]
        print(f"\n--- {isco3}: {entry['label']} ---")
        print(f"  Subject categories: {entry['ai_act_categories_as_subject']}")
        print(f"  Deployer categories: {entry['ai_act_categories_as_deployer']}")
        print(f"  High-risk as subject: {entry['high_risk_as_subject']}")
        print(f"  High-risk as deployer: {entry['high_risk_as_deployer']}")
        print(f"  Platform Work Dir: {entry['platform_work_directive_relevant']}")
        print(f"  Pay Transparency Dir: {entry['pay_transparency_relevant']}")
        print(f"  Regulatory surface: {entry['regulatory_surface_count']}")
        print(f"  Regulations: {entry['regulations_applicable']}")
        print(f"  Subject: {entry['subject_explanation'][:100]}...")
        print(f"  Deployer: {entry['deployer_explanation'][:100]}...")


if __name__ == "__main__":
    main()
