#!/usr/bin/env python3
"""
Build country_signals section for job-market-data.json.
Merges: Eurostat AI adoption, ICT specialists %, OECD EPL, Stack Overflow survey,
employment YoY, LinkedIn hiring data, Ravio country hiring, Atomico ecosystem data.

Output: Updates ../european-careers-map/site/job-market-data.json in place.
"""

import csv
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")
SITE_JSON = os.path.join(BASE, "..", "..", "european-careers-map", "site", "job-market-data.json")

# Country name mapping for display
COUNTRY_NAMES = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CH": "Switzerland",
    "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany", "DK": "Denmark",
    "EE": "Estonia", "EL": "Greece", "ES": "Spain", "FI": "Finland",
    "FR": "France", "GB": "United Kingdom", "GR": "Greece", "HR": "Croatia",
    "HU": "Hungary", "IE": "Ireland", "IS": "Iceland", "IT": "Italy",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MK": "North Macedonia",
    "MT": "Malta", "NL": "Netherlands", "NO": "Norway", "PL": "Poland",
    "PT": "Portugal", "RO": "Romania", "RS": "Serbia", "SE": "Sweden",
    "SI": "Slovenia", "SK": "Slovakia", "UA": "Ukraine",
}

# ISCO 2-digit codes relevant to our 9 role families
ROLE_ISCO_MAP = {
    "25": "engineering",     # ICT professionals
    "35": "engineering",     # ICT technicians
    "13": "operations",      # Production and specialized services managers
    "12": "operations",      # Administrative and commercial managers
    "24": "data_ai",         # Business and administration professionals (includes data)
    "33": "sales",           # Business and administration associate professionals
    "26": "design",          # Legal, social, cultural professionals (includes design)
}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_ai_adoption():
    """Eurostat AI adoption by country."""
    data = load_json(os.path.join(DATA, "eurostat", "ai_adoption_processed.json"))
    result = {}
    for iso2, info in data["countries"].items():
        result[iso2] = {
            "ai_adoption_pct": info["latest_value"],
            "ai_adoption_year": info["latest_year"],
            "ai_adoption_series": info.get("series", {}),
        }
    return result


def load_ict_specialists():
    """Eurostat ICT specialists % of employment."""
    data = load_json(os.path.join(DATA, "eurostat", "ict_specialists_processed.json"))
    result = {}
    for iso2, info in data["countries"].items():
        result[iso2] = {
            "ict_specialists_pct": info["latest_value"],
            "ict_specialists_year": info["latest_year"],
        }
    return result


def load_epl():
    """OECD Employment Protection Legislation scores."""
    data = load_json(os.path.join(DATA, "oecd", "epl_processed.json"))
    result = {}
    # Map OECD country codes to our ISO2
    code_map = {"UK": "GB"}
    for code, info in data["countries"].items():
        iso2 = code_map.get(code, code)
        if iso2 in COUNTRY_NAMES:
            result[iso2] = {
                "epl_score": info["score"],
                "epl_year": info.get("year", 2019),
            }
    return result


def load_stackoverflow():
    """Stack Overflow developer survey data."""
    path = os.path.join(DATA, "stackoverflow", "so_europe_processed.json")
    if not os.path.exists(path):
        print("WARNING: SO data not found, skipping")
        return {}
    data = load_json(path)
    result = {}
    for iso2, info in data["countries"].items():
        entry = {
            "so_respondents": info["respondents"],
        }
        if "salary_usd" in info:
            entry["so_median_salary_usd"] = info["salary_usd"]["median"]
            entry["so_salary_p25_usd"] = info["salary_usd"]["p25"]
            entry["so_salary_p75_usd"] = info["salary_usd"]["p75"]
        if "remote_work" in info:
            entry["so_remote_work"] = info["remote_work"]
        if "ai_threat" in info:
            entry["so_ai_threat"] = info["ai_threat"]
        if "ai_tool_usage_pct" in info:
            entry["so_ai_tool_usage_pct"] = info["ai_tool_usage_pct"]
        if "ic_vs_pm" in info:
            entry["so_ic_vs_pm"] = info["ic_vs_pm"]
        result[iso2] = entry
    return result


def load_employment_yoy():
    """Eurostat employment YoY by ISCO 2-digit."""
    path = os.path.join(DATA, "eurostat", "employment_yoy.csv")
    result = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = row["country"]
            if country == "EU27":
                continue
            isco = row["isco2"]
            yoy = row.get("yoy_pct", "")

            if country not in result:
                result[country] = {"isco_yoy": {}}

            if yoy and yoy != "":
                try:
                    result[country]["isco_yoy"][isco] = round(float(yoy), 1)
                except ValueError:
                    pass

    # Compute tech-relevant aggregate: ISCO 25 (ICT professionals) + 35 (ICT technicians)
    for country, data in result.items():
        isco_yoy = data["isco_yoy"]
        tech_codes = ["25", "35"]
        tech_vals = [isco_yoy[c] for c in tech_codes if c in isco_yoy]
        if tech_vals:
            data["tech_employment_yoy"] = round(sum(tech_vals) / len(tech_vals), 1)

    return result


def load_linkedin_hiring():
    """LinkedIn hiring data (manually extracted from report)."""
    return {
        "DE": {"linkedin_hiring_vs_prepandemic": -0.17, "linkedin_hiring_small": -0.16, "linkedin_hiring_mid": -0.24, "linkedin_hiring_enterprise": -0.40},
        "GB": {"linkedin_hiring_vs_prepandemic": -0.25, "linkedin_hiring_small": -0.22, "linkedin_hiring_mid": -0.32, "linkedin_hiring_enterprise": -0.38},
        "FR": {"linkedin_hiring_vs_prepandemic": -0.30, "linkedin_hiring_small": -0.34, "linkedin_hiring_mid": -0.37, "linkedin_hiring_enterprise": -0.48},
        "NL": {"linkedin_hiring_vs_prepandemic": -0.35, "linkedin_hiring_small": -0.32, "linkedin_hiring_mid": -0.38, "linkedin_hiring_enterprise": -0.49},
    }


def load_linkedin_ai_talent_migration():
    """LinkedIn AI engineering talent net migration per 10K members."""
    return {
        "FR": {"ai_talent_net_migration_per_10k": 0.3},
        "GB": {"ai_talent_net_migration_per_10k": 0.6},
        "DE": {"ai_talent_net_migration_per_10k": 2.1},
        "IE": {"ai_talent_net_migration_per_10k": 2.2},
    }


def load_atomico_ecosystem():
    """Atomico State of European Tech headline data."""
    return {
        "_europe_wide": {
            "tech_workforce_total": 4600000,
            "tech_workforce_cagr_pct": 9.1,
            "technical_engineering_employees": 2700000,
            "founders_starting_2025": 27000,
            "founders_yoy_growth_pct": 59,
            "net_talent_inflow_2024": 26000,
            "vc_invested_2025_9m_usd_bn": 33,
            "vc_invested_2025_full_year_est_usd_bn": 44,
            "deep_tech_share_of_vc_pct": 36,
            "sustainability_share_of_vc_pct": 18,
            "ai_raised_europe_usd_bn": 14,
            "ai_raised_us_usd_bn": 146,
            "new_unicorns_2025": 28,
            "founder_retention_in_europe_pct": 81,
            "source": "Atomico State of European Tech 2025",
        },
        "CH": {"atomico_note": "18% of deep tech engineers have PhD (highest in Europe); Zurich = Google, OpenAI, Anthropic research hubs"},
    }


def build_country_signals():
    """Merge all sources into country_signals dict."""
    print("Loading data sources...")
    ai_adoption = load_ai_adoption()
    ict_specialists = load_ict_specialists()
    epl = load_epl()
    so = load_stackoverflow()
    emp_yoy = load_employment_yoy()
    linkedin = load_linkedin_hiring()
    linkedin_ai = load_linkedin_ai_talent_migration()
    atomico = load_atomico_ecosystem()

    # Collect all country codes
    all_countries = set()
    for source in [ai_adoption, ict_specialists, epl, so, emp_yoy, linkedin, linkedin_ai]:
        all_countries.update(source.keys())
    all_countries.discard("_europe_wide")

    # Map EL -> GR for consistency
    for source in [ai_adoption, ict_specialists, emp_yoy]:
        if "EL" in source and "GR" not in source:
            source["GR"] = source.pop("EL")
        elif "EL" in source:
            source.pop("EL")

    # Build merged signals
    country_signals = {}

    for iso2 in sorted(all_countries):
        if iso2 not in COUNTRY_NAMES:
            continue

        entry = {"name": COUNTRY_NAMES[iso2]}

        # Data depth indicator
        sources = []

        # Eurostat AI adoption
        if iso2 in ai_adoption:
            entry.update(ai_adoption[iso2])
            sources.append("eurostat_ai")

        # ICT specialists
        if iso2 in ict_specialists:
            entry.update(ict_specialists[iso2])
            sources.append("eurostat_ict")

        # EPL
        if iso2 in epl:
            entry.update(epl[iso2])
            sources.append("oecd_epl")

        # Stack Overflow
        if iso2 in so:
            entry.update(so[iso2])
            sources.append("stackoverflow")

        # Employment YoY
        if iso2 in emp_yoy:
            if "tech_employment_yoy" in emp_yoy[iso2]:
                entry["tech_employment_yoy_pct"] = emp_yoy[iso2]["tech_employment_yoy"]
            # Include a few key ISCO codes
            isco_yoy = emp_yoy[iso2].get("isco_yoy", {})
            relevant = {}
            for code in ["25", "35", "13", "24", "33"]:
                if code in isco_yoy:
                    relevant[code] = isco_yoy[code]
            if relevant:
                entry["employment_yoy_by_isco"] = relevant
            sources.append("eurostat_emp")

        # LinkedIn
        if iso2 in linkedin:
            entry.update(linkedin[iso2])
            sources.append("linkedin")

        if iso2 in linkedin_ai:
            entry.update(linkedin_ai[iso2])

        # Atomico
        if iso2 in atomico:
            entry.update(atomico[iso2])

        entry["data_sources"] = sources
        entry["data_depth"] = len(sources)

        # Skip empty entries (e.g. EL after remap to GR)
        if len(sources) == 0:
            continue

        country_signals[iso2] = entry

    return country_signals, atomico.get("_europe_wide", {})


def enrich_roles_with_linkedin(data):
    """Add LinkedIn hiring-by-function data to roles."""
    # LinkedIn global hiring vs pre-pandemic by function (p.20)
    linkedin_function_hiring = {
        "product": -0.36,
        "engineering": -0.32,
        "design": -0.34,  # Media and Communication as proxy
        "sales": -0.22,
        "operations": -0.05,
        "growth_marketing": -0.32,
        "data_ai": -0.19,  # Research as proxy
        "cybersecurity": -0.29,  # IT as proxy
    }

    # LinkedIn entry-level share change (p.21)
    linkedin_entry_level_change = {
        "product": -1.5,  # Product Management: -1.5 ppt
        "engineering": 0.4,
        "sales": 0.5,
        "operations": 0.1,
        "growth_marketing": -0.3,
        "data_ai": 0.4,  # Research proxy
    }

    for role_key, role_data in data.get("roles", {}).items():
        if role_key in linkedin_function_hiring:
            if "linkedin" not in role_data:
                role_data["linkedin"] = {}
            role_data["linkedin"]["hiring_vs_prepandemic"] = linkedin_function_hiring[role_key]
            role_data["linkedin"]["source"] = "LinkedIn Labor Market Report Jan 2026 (global)"

        if role_key in linkedin_entry_level_change:
            if "linkedin" not in role_data:
                role_data["linkedin"] = {}
            role_data["linkedin"]["entry_level_share_change_ppt"] = linkedin_entry_level_change[role_key]

    return data


def enrich_roles_with_github(data):
    """Add GitHub Copilot working paper data to engineering role."""
    eng = data.get("roles", {}).get("engineering", {})
    if eng:
        eng["ai_productivity"] = {
            "copilot_entry_level_hiring_increase_pct": 6.6,
            "copilot_senior_hiring_increase_pct": 4.9,
            "copilot_non_programming_skills_increase_pct": 13.3,
            "copilot_task_speed_increase_pct": 56,
            "copilot_adoption_rate_gh_firms_pct": 35.6,
            "copilot_retention_month_over_month_pct": 95.6,
            "source": "GitHub Copilot Working Paper (Baird et al., Sept 2024, n=24,517 firms)"
        }
    return data


def enrich_roles_with_ai_jobs(data):
    """Add LinkedIn AI jobs created data."""
    eng = data.get("roles", {}).get("engineering", {})
    if eng:
        if "ai_jobs" not in eng:
            eng["ai_jobs"] = {}
        eng["ai_jobs"]["ai_engineer_created_2023_2025"] = 177000
        eng["ai_jobs"]["ai_engineer_growth_since_2023"] = "13x"
        eng["ai_jobs"]["forward_deployed_eng_created"] = 9000
        eng["ai_jobs"]["forward_deployed_eng_growth"] = "42x"
        eng["ai_jobs"]["source"] = "LinkedIn Labor Market Report Jan 2026"

    dai = data.get("roles", {}).get("data_ai", {})
    if dai:
        if "ai_jobs" not in dai:
            dai["ai_jobs"] = {}
        dai["ai_jobs"]["head_of_ai_created_2023_2025"] = 298000
        dai["ai_jobs"]["data_annotator_created_2023_2025"] = 774000
        dai["ai_jobs"]["total_ai_jobs_created_globally"] = 1300000
        dai["ai_jobs"]["source"] = "LinkedIn Labor Market Report Jan 2026"

    return data


def enrich_cross_role(data):
    """Add cross-role enrichments from new sources."""
    cross = data.get("cross_role", {})

    # LinkedIn AI skills by function
    cross["ai_skills_by_function"] = {
        "engineering": 0.10,
        "product_management": 0.10,
        "research": 0.08,
        "entrepreneurship": 0.07,
        "information_technology": 0.05,
        "consulting": 0.04,
        "design": 0.02,
        "marketing": 0.02,
        "sales": 0.01,
        "operations": 0.01,
        "note": "% of US LinkedIn members with 2+ AI engineering skills or in AI engineering occupation",
        "source": "LinkedIn Labor Market Report Jan 2026 (US data, indicative for Europe)"
    }

    # Atomico foundation model hiring
    cross["ai_company_hiring"] = {
        "foundation_models_yoy_employment_change": 0.92,
        "foundation_models_ai_talent_pct": 0.28,
        "big_tech_yoy_employment_change": 0.08,
        "big_tech_ai_talent_pct": 0.15,
        "ai_hardware_yoy_employment_change": 0.25,
        "vertical_applications_yoy_employment_change": 0.06,
        "source": "LinkedIn Labor Market Report Jan 2026"
    }

    # Skills signals
    cross["skills_signal"] = {
        "additional_10_skills_reduces_gap_months": 1.17,
        "median_employment_gap_months": 7.09,
        "source": "Baird, Ko, Gahlawat (LinkedIn EG WP No.1, Jan 2023, US data)"
    }

    data["cross_role"] = cross
    return data


def main():
    # Build country signals
    country_signals, europe_wide = build_country_signals()

    # Load existing job-market-data.json
    with open(SITE_JSON) as f:
        data = json.load(f)

    # Add country_signals
    data["country_signals"] = country_signals
    data["europe_ecosystem"] = europe_wide

    # Update meta
    data["meta"]["sources"].extend([
        "Stack Overflow Developer Survey 2025 (49,191 respondents, 15,752 European)",
        "Atomico State of European Tech 2025 (annual ecosystem report)",
        "LinkedIn Labor Market Report Jan 2026 (1.3B members)",
        "EMEA Labour Market Outlook Mar 2026 (LinkedIn Economic Graph)",
        "Indeed Hiring Lab (DE, FR, UK/IE, March 2026)",
        "Bitkom Startup Report 2025 (152 German startups)",
        "GitHub Copilot Working Paper (Baird et al., n=24,517 firms)",
        "Eurostat employment by ISCO 2-digit (2023-2024 YoY)",
    ])
    # Deduplicate
    data["meta"]["sources"] = list(dict.fromkeys(data["meta"]["sources"]))
    data["meta"]["last_updated"] = "2026-03-28"
    data["meta"]["data_period"] += "; SO Developer Survey June 2025; LinkedIn Jan 2026; Atomico Nov 2025"

    # Enrich roles
    data = enrich_roles_with_linkedin(data)
    data = enrich_roles_with_github(data)
    data = enrich_roles_with_ai_jobs(data)
    data = enrich_cross_role(data)

    # Add Indeed signals
    data["indeed_signals"] = {
        "DE": {
            "headline": "More applications, fewer openings",
            "job_postings_vs_peak": "Declining since late 2022",
            "key_signal": "One-sided market dynamics: employer's market",
            "date": "2026-01-31",
            "source": "Indeed Hiring Lab Germany, Feb 2026"
        },
        "FR": {
            "headline": "Dynamic start to 2026",
            "job_postings_vs_dec2022_peak": -0.42,
            "seasonal_rebound": "Most dynamic in 3 years",
            "candidate_activity_vs_dec": 0.29,
            "application_growth_vs_pre_christmas": 0.16,
            "date": "2026-01-31",
            "source": "Indeed Hiring Lab France, Feb 2026"
        },
        "GB": {
            "headline": "Stabilisation but outlook has darkened",
            "unemployment_rate": 0.052,
            "regular_pay_growth_yoy": 0.038,
            "pay_growth_note": "Lowest in 5+ years",
            "bdo_employment_index": "Lowest in 15 years",
            "london_youth_unemployment": 0.246,
            "date": "2026-01-31",
            "source": "Indeed Hiring Lab UK/Ireland, Mar 2026"
        }
    }

    # Add Bitkom signals
    data["bitkom_signals"] = {
        "DE": {
            "startup_avg_headcount_2025": 13.1,
            "startup_avg_headcount_2024": 14.8,
            "startups_planning_hiring_pct": 0.75,
            "avg_planned_new_hires": 5.7,
            "avg_open_positions": 2.0,
            "ai_adoption_startups_pct": 0.82,
            "brain_drain_would_found_abroad_pct": 0.22,
            "brain_drain_us_destination_pct": 0.38,
            "source": "Bitkom Startup Report 2025 (n=152 German tech startups)"
        }
    }

    # Write back
    with open(SITE_JSON, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nUpdated {SITE_JSON}")
    print(f"Country signals: {len(country_signals)} countries")
    print(f"\nData depth distribution:")
    depths = {}
    for iso2, info in country_signals.items():
        d = info.get("data_depth", 0)
        if d not in depths:
            depths[d] = []
        depths[d].append(iso2)
    for d in sorted(depths.keys(), reverse=True):
        print(f"  {d} sources: {', '.join(depths[d])}")


if __name__ == "__main__":
    main()
