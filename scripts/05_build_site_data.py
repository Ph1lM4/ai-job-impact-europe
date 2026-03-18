"""
05_build_site_data.py — Merge occupations + country data + scores + AI Act overlay → site/data.json

Builds nested treemap structure for D3.js with dict-based employment/wage per country,
country metadata with groupings, dual exposure scores, and EU AI Act regulatory overlay.

Input:  occupations.csv, occupations_by_country.csv, scores.json, data/manual/ai_act_high_risk.json
Output: site/data.json
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_META = ROOT / "occupations.csv"
INPUT_COUNTRY = ROOT / "occupations_by_country.csv"
INPUT_SCORES = ROOT / "scores.json"
INPUT_AI_ACT = ROOT / "data" / "manual" / "ai_act_high_risk.json"
OUTPUT = ROOT / "site" / "data.json"

# ── Country metadata ──

COUNTRY_NAMES = {
    "EU27": "EU-27 Aggregate",
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "HR": "Croatia",
    "CY": "Cyprus", "CZ": "Czechia", "DK": "Denmark", "EE": "Estonia",
    "FI": "Finland", "FR": "France", "DE": "Germany", "EL": "Greece",
    "HU": "Hungary", "IE": "Ireland", "IT": "Italy", "LV": "Latvia",
    "LT": "Lithuania", "LU": "Luxembourg", "MT": "Malta", "NL": "Netherlands",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "SK": "Slovakia",
    "SI": "Slovenia", "ES": "Spain", "SE": "Sweden",
    "CH": "Switzerland", "IS": "Iceland", "NO": "Norway",
    "UK": "United Kingdom",
    "AL": "Albania", "BA": "Bosnia and Herzegovina",
    "MK": "North Macedonia", "RS": "Serbia", "TR": "Turkey",
}

COUNTRY_GROUP_MAP = {
    "EU27": "europe",
    "AT": "western", "BE": "western", "CH": "western", "DE": "western",
    "FR": "western", "IE": "western", "LU": "western", "NL": "western",
    "DK": "northern", "EE": "northern", "FI": "northern", "IS": "northern",
    "LT": "northern", "LV": "northern", "NO": "northern", "SE": "northern",
    "CY": "southern", "EL": "southern", "ES": "southern", "HR": "southern",
    "IT": "southern", "MT": "southern", "PT": "southern", "SI": "southern",
    "BG": "eastern", "CZ": "eastern", "HU": "eastern", "PL": "eastern",
    "RO": "eastern", "SK": "eastern",
    "UK": "uk",
    "AL": "candidate", "BA": "candidate", "MK": "candidate",
    "RS": "candidate", "TR": "candidate",
}

GROUP_ORDER = [
    {"id": "europe", "label": "Europe"},
    {"id": "western", "label": "Western Europe"},
    {"id": "northern", "label": "Northern Europe"},
    {"id": "southern", "label": "Southern Europe"},
    {"id": "eastern", "label": "Eastern Europe"},
    {"id": "uk", "label": "United Kingdom"},
    {"id": "candidate", "label": "Candidate Countries"},
]

COUNTRY_SOURCES = {
    "EU27": "Eurostat",
    "UK": "ONS",
    "CH": "Eurostat+BFS",
}
DEFAULT_SOURCE = "Eurostat"

EMP_NOTES = {
    "UK": "Employee jobs only (excludes self-employed)",
}


def get_band(score):
    if score < 2: return "0-2"
    if score < 4: return "2-4"
    if score < 6: return "4-6"
    if score < 8: return "6-8"
    return "8-10"


def compute_stats(leaves, score_key, country):
    """Compute summary stats for a given score field and country."""
    total_emp = 0
    weighted_exp = 0
    bands = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
    band_emp = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
    high_exp_wages = 0

    for c in leaves:
        s = c[score_key]
        emp = (c["emp"] or {}).get(country, 0)
        wage = (c["wage"] or {}).get(country)
        total_emp += emp
        weighted_exp += emp * s
        band = get_band(s)
        bands[band] += 1
        band_emp[band] += emp
        if s >= 7 and wage:
            high_exp_wages += emp * wage

    avg = weighted_exp / total_emp if total_emp > 0 else 0
    return {
        "total_employment": total_emp,
        "weighted_avg_exposure": round(avg, 2),
        "bands": bands,
        "band_employment": band_emp,
        "high_exposure_annual_wages": round(high_exp_wages),
    }


def main():
    print("Loading occupations metadata...")
    meta = pd.read_csv(INPUT_META, dtype={"isco3": str, "isco2": str, "isco1": str})
    print(f"  {len(meta)} occupation groups")

    print("Loading country data...")
    country_df = pd.read_csv(INPUT_COUNTRY, dtype={"isco3": str})
    all_countries = sorted(country_df["country"].unique())
    print(f"  {len(country_df)} rows, {len(all_countries)} countries")

    print("Loading scores...")
    with open(INPUT_SCORES, encoding="utf-8") as f:
        scores = json.load(f)
    print(f"  {len(scores)} scores")

    print("Loading AI Act classifications...")
    ai_act = {}
    if INPUT_AI_ACT.exists():
        with open(INPUT_AI_ACT, encoding="utf-8") as f:
            ai_act = json.load(f)
        print(f"  {len(ai_act)} AI Act classifications")
    else:
        print("  WARNING: ai_act_high_risk.json not found, skipping AI Act overlay")

    # Build employment and wage lookups: {isco3: {country: value}}
    emp_lookup = {}
    wage_lookup = {}
    for _, row in country_df.iterrows():
        isco3 = row["isco3"]
        country = row["country"]
        if isco3 not in emp_lookup:
            emp_lookup[isco3] = {}
            wage_lookup[isco3] = {}
        if pd.notna(row["employment_thousands"]):
            emp_lookup[isco3][country] = round(row["employment_thousands"] * 1000)
        if pd.notna(row["mean_annual_wage_eur"]):
            wage_lookup[isco3][country] = round(row["mean_annual_wage_eur"])

    # Merge scores
    meta["technical_score"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("technical_score"))
    meta["regulated_score"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("regulated_score"))
    meta["rationale"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("rationale", ""))
    meta["regulatory_friction"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("regulatory_friction", ""))
    meta["key_vulnerable_tasks"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("key_vulnerable_tasks", []))
    meta["key_protected_tasks"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("key_protected_tasks", []))
    meta["uk_regulated_score"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("uk_regulated_score"))
    meta["uk_rationale"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("uk_rationale", ""))
    meta["uk_regulatory_friction"] = meta["isco3"].map(lambda x: scores.get(x, {}).get("uk_regulatory_friction", ""))

    scored = meta[meta["technical_score"].notna()]
    print(f"  {len(scored)} groups with scores")

    # ── Build treemap ──
    isco1_groups = {}
    for _, row in scored.iterrows():
        key = row["isco1"]
        if key not in isco1_groups:
            isco1_groups[key] = {
                "name": row["isco1_label"],
                "isco1": key,
                "children": [],
            }

        tech = round(row["technical_score"], 1)
        reg = round(row["regulated_score"], 1)
        isco3 = row["isco3"]

        child = {
            "name": row["isco3_label"],
            "isco3": isco3,
            "isco2": row["isco2"],
            "category": row["isco1_label"],
            "emp": emp_lookup.get(isco3, {}),
            "wage": wage_lookup.get(isco3, {}),
            "technical_score": tech,
            "regulated_score": reg,
            "regulatory_delta": round(tech - reg, 1),
            "rationale": row["rationale"],
            "regulatory_friction": row["regulatory_friction"],
            "key_vulnerable_tasks": row["key_vulnerable_tasks"],
            "key_protected_tasks": row["key_protected_tasks"],
        }

        # UK-specific regulated score
        if pd.notna(row.get("uk_regulated_score")):
            child["uk_regulated_score"] = round(row["uk_regulated_score"], 1)
            child["uk_rationale"] = row.get("uk_rationale", "")
            child["uk_regulatory_friction"] = row.get("uk_regulatory_friction", "")

        # Merge AI Act overlay data
        if isco3 in ai_act:
            act = ai_act[isco3]
            child["ai_act_categories_as_subject"] = act.get("ai_act_categories_as_subject", [])
            child["ai_act_categories_as_deployer"] = act.get("ai_act_categories_as_deployer", [])
            child["high_risk_as_subject"] = act.get("high_risk_as_subject", True)
            child["high_risk_as_deployer"] = act.get("high_risk_as_deployer", False)
            child["eu_obligations"] = act.get("eu_obligations", [])
            child["works_council_de"] = act.get("works_council_de", {})
            child["works_council_at"] = act.get("works_council_at", {})
            child["switzerland"] = act.get("switzerland", {})
            child["platform_work_directive_relevant"] = act.get("platform_work_directive_relevant", False)
            child["pay_transparency_relevant"] = act.get("pay_transparency_relevant", False)
            child["regulatory_surface_count"] = act.get("regulatory_surface_count", 0)
            child["regulations_applicable"] = act.get("regulations_applicable", [])
            child["subject_explanation"] = act.get("subject_explanation", "")
            child["deployer_explanation"] = act.get("deployer_explanation", "")

        isco1_groups[key]["children"].append(child)

    treemap = {
        "name": "European Labor Market",
        "children": [isco1_groups[k] for k in sorted(isco1_groups.keys())],
    }

    # Collect all leaves
    leaves = [c for g in treemap["children"] for c in g["children"]]

    # ── Country metadata ──
    countries_meta = {}
    for country in all_countries:
        emp_total = sum(leaf["emp"].get(country, 0) for leaf in leaves)
        has_employment = emp_total > 0
        has_wages = any(country in leaf["wage"] for leaf in leaves)

        entry = {
            "name": COUNTRY_NAMES.get(country, country),
            "group": COUNTRY_GROUP_MAP.get(country, "candidate"),
            "source": COUNTRY_SOURCES.get(country, DEFAULT_SOURCE),
            "emp_total": emp_total,
            "has_employment": has_employment,
            "has_wages": has_wages,
        }
        if country in EMP_NOTES:
            entry["emp_note"] = EMP_NOTES[country]

        countries_meta[country] = entry

    # ── Summary stats (EU27 only, pre-computed) ──
    tech_stats = compute_stats(leaves, "technical_score", "EU27")
    reg_stats = compute_stats(leaves, "regulated_score", "EU27")

    deltas = sorted(leaves, key=lambda c: c["regulatory_delta"], reverse=True)
    top_delta = [{
        "name": c["name"], "isco3": c["isco3"], "delta": c["regulatory_delta"],
        "technical": c["technical_score"], "regulated": c["regulated_score"],
    } for c in deltas[:10]]

    # ── AI Act summary stats ──
    ai_act_summary = {}
    if ai_act:
        deployer_groups = [l for l in leaves if l.get("high_risk_as_deployer")]
        wc_de_groups = [l for l in leaves if l.get("works_council_de", {}).get("triggered")]
        wc_at_groups = [l for l in leaves if l.get("works_council_at", {}).get("triggered")]
        platform_groups = [l for l in leaves if l.get("platform_work_directive_relevant")]
        surfaces = [l.get("regulatory_surface_count", 0) for l in leaves if "regulatory_surface_count" in l]

        deployer_emp = sum(l["emp"].get("EU27", 0) for l in deployer_groups)
        total_emp_eu27 = sum(l["emp"].get("EU27", 0) for l in leaves)
        pct_deployer = round(deployer_emp / total_emp_eu27 * 100, 1) if total_emp_eu27 > 0 else 0

        ai_act_summary = {
            "count_deployer_groups": len(deployer_groups),
            "count_works_council_de": len(wc_de_groups),
            "count_works_council_at": len(wc_at_groups),
            "count_platform_work": len(platform_groups),
            "pct_workforce_deployer": pct_deployer,
            "avg_regulatory_surface": round(sum(surfaces) / len(surfaces), 1) if surfaces else 0,
        }

    summary = {
        "occupation_count": len(scored),
        "technical": tech_stats,
        "regulated": reg_stats,
        "top_regulatory_deltas": top_delta,
        "ai_act": ai_act_summary,
        "model": "Claude Sonnet 4",
        "data_year": 2024,
        "wage_year": 2022,
    }

    output_data = {
        "countries": countries_meta,
        "country_groups": GROUP_ORDER,
        "summary": summary,
        "treemap": treemap,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=1, ensure_ascii=False)

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"\nOutput: {OUTPUT} ({size_kb:.0f} KB)")
    print(f"  {len(countries_meta)} countries")
    print(f"  EU27 employment: {tech_stats['total_employment']:,}")
    print(f"  Technical avg: {tech_stats['weighted_avg_exposure']:.2f}")
    print(f"  Regulated avg: {reg_stats['weighted_avg_exposure']:.2f}")

    # Country coverage summary
    print(f"\n  Country coverage:")
    for ginfo in GROUP_ORDER:
        gid, glabel = ginfo["id"], ginfo["label"]
        group_countries = [c for c, m in countries_meta.items() if m["group"] == gid]
        if group_countries:
            print(f"    {glabel}:")
            for c in sorted(group_countries):
                m = countries_meta[c]
                emp_str = f"{m['emp_total']:>12,}" if m["has_employment"] else "      no data"
                wage_str = "wages" if m["has_wages"] else "no wages"
                print(f"      {c:>5} {m['name']:<28} {emp_str}  {wage_str}  [{m['source']}]")


if __name__ == "__main__":
    main()
