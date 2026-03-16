"""
05_build_site_data.py — Merge occupations.csv + scores.json → site/data.json

Builds nested treemap structure for D3.js visualization with dual scores
(technical vs regulated) and regulatory delta.

Input:  occupations.csv, scores.json
Output: site/data.json
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_OCC = ROOT / "occupations.csv"
INPUT_SCORES = ROOT / "scores.json"
OUTPUT = ROOT / "site" / "data.json"


def get_band(score):
    if score < 2: return "0-2"
    if score < 4: return "2-4"
    if score < 6: return "4-6"
    if score < 8: return "6-8"
    return "8-10"


def compute_stats(leaves, score_key):
    """Compute summary stats for a given score field."""
    total_emp = 0
    weighted_exp = 0
    bands = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
    band_emp = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
    high_exp_wages = 0

    for c in leaves:
        s = c[score_key]
        emp = c["employment"]
        total_emp += emp
        weighted_exp += emp * s
        band = get_band(s)
        bands[band] += 1
        band_emp[band] += emp
        if s >= 7 and c["wage_mean"]:
            high_exp_wages += emp * c["wage_mean"]

    avg = weighted_exp / total_emp if total_emp > 0 else 0
    return {
        "total_employment": total_emp,
        "weighted_avg_exposure": round(avg, 2),
        "bands": bands,
        "band_employment": band_emp,
        "high_exposure_annual_wages": round(high_exp_wages),
    }


def main():
    print("Loading occupations...")
    df = pd.read_csv(INPUT_OCC, dtype={"isco3": str, "isco2": str, "isco1": str})
    print(f"  {len(df)} occupation groups")

    print("Loading scores...")
    with open(INPUT_SCORES, encoding="utf-8") as f:
        scores = json.load(f)
    print(f"  {len(scores)} scores")

    # Merge dual scores
    df["technical_score"] = df["isco3"].map(lambda x: scores.get(x, {}).get("technical_score"))
    df["regulated_score"] = df["isco3"].map(lambda x: scores.get(x, {}).get("regulated_score"))
    df["rationale"] = df["isco3"].map(lambda x: scores.get(x, {}).get("rationale", ""))
    df["regulatory_friction"] = df["isco3"].map(lambda x: scores.get(x, {}).get("regulatory_friction", ""))
    df["key_vulnerable_tasks"] = df["isco3"].map(lambda x: scores.get(x, {}).get("key_vulnerable_tasks", []))
    df["key_protected_tasks"] = df["isco3"].map(lambda x: scores.get(x, {}).get("key_protected_tasks", []))

    scored = df[df["technical_score"].notna()]
    print(f"  {len(scored)} groups with scores")

    # Build nested structure
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

        child = {
            "name": row["isco3_label"],
            "isco3": row["isco3"],
            "isco2": row["isco2"],
            "category": row["isco1_label"],
            "employment": round(row["employment_eu27"] * 1000) if pd.notna(row["employment_eu27"]) else 0,
            "employment_de": round(row["employment_de"] * 1000) if pd.notna(row["employment_de"]) else 0,
            "employment_at": round(row["employment_at"] * 1000) if pd.notna(row["employment_at"]) else 0,
            "employment_ch": round(row["employment_ch"] * 1000) if pd.notna(row["employment_ch"]) else 0,
            "wage_mean": round(row["mean_annual_wage_eur"]) if pd.notna(row["mean_annual_wage_eur"]) else None,
            "technical_score": tech,
            "regulated_score": reg,
            "regulatory_delta": round(tech - reg, 1),
            "rationale": row["rationale"],
            "regulatory_friction": row["regulatory_friction"],
            "key_vulnerable_tasks": row["key_vulnerable_tasks"],
            "key_protected_tasks": row["key_protected_tasks"],
        }
        isco1_groups[key]["children"].append(child)

    treemap = {
        "name": "European Labor Market",
        "children": [isco1_groups[k] for k in sorted(isco1_groups.keys())],
    }

    # Collect all leaves for stats
    leaves = [c for g in treemap["children"] for c in g["children"]]

    tech_stats = compute_stats(leaves, "technical_score")
    reg_stats = compute_stats(leaves, "regulated_score")

    # Delta stats
    deltas = sorted(leaves, key=lambda c: c["regulatory_delta"], reverse=True)
    top_delta = [{"name": c["name"], "isco3": c["isco3"], "delta": c["regulatory_delta"],
                  "technical": c["technical_score"], "regulated": c["regulated_score"]}
                 for c in deltas[:10]]

    summary = {
        "occupation_count": len(scored),
        "technical": tech_stats,
        "regulated": reg_stats,
        "top_regulatory_deltas": top_delta,
        "model": "Claude Sonnet 4",
        "data_year": 2024,
        "wage_year": 2022,
    }

    output_data = {
        "summary": summary,
        "treemap": treemap,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=1, ensure_ascii=False)

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"\nOutput: {OUTPUT} ({size_kb:.0f} KB)")
    print(f"  Total employment: {tech_stats['total_employment']:,}")
    print(f"  Technical avg: {tech_stats['weighted_avg_exposure']:.2f}")
    print(f"  Regulated avg: {reg_stats['weighted_avg_exposure']:.2f}")
    print(f"  Top deltas:")
    for d in top_delta[:5]:
        print(f"    {d['isco3']} {d['name']}: {d['technical']} → {d['regulated']} (Δ{d['delta']})")


if __name__ == "__main__":
    main()
