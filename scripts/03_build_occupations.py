"""
03_build_occupations.py — Merge ESCO processed data + Eurostat + BFS + ONS → occupations.csv

Distributes ISCO 2-digit employment to 3-digit groups using ESCO occupation counts as weights.
Attaches wage data: Eurostat SES (default), BFS LSE 2024 (CH override), ONS ASHE 2025 (UK).

Input:
  data/esco/esco_processed.json
  data/eurostat/employment_isco2d.csv
  data/eurostat/wages_isco.csv
  data/bfs/wages_ch_bfs.csv         (optional — CH wage override)
  data/ons/employment_uk.csv        (optional — UK employment)
  data/ons/wages_uk.csv             (optional — UK wages)

Output:
  occupations.csv              — metadata (125 rows): isco labels, descriptions, skills
  occupations_by_country.csv   — long format (~4500 rows): isco3, country, employment, wage
"""

import json
import pandas as pd
from pathlib import Path

ROOT = Path(".")
ESCO_FILE = ROOT / "data/esco/esco_processed.json"
EMP_FILE = ROOT / "data/eurostat/employment_isco2d.csv"
WAGE_FILE = ROOT / "data/eurostat/wages_isco.csv"
BFS_WAGE_FILE = ROOT / "data/bfs/wages_ch_bfs.csv"
ONS_EMP_FILE = ROOT / "data/ons/employment_uk.csv"
ONS_WAGE_FILE = ROOT / "data/ons/wages_uk.csv"
OUTPUT_META = ROOT / "occupations.csv"
OUTPUT_COUNTRY = ROOT / "occupations_by_country.csv"

# Remap codes for brevity in output
CODE_REMAP = {"EU27_2020": "EU27"}


def load_esco():
    with open(ESCO_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_weights(esco_groups):
    """Build ESCO-based weights for distributing 2-digit employment to 3-digit."""
    df = pd.DataFrame([
        {"isco3": g["isco3"], "isco2": g["isco2"], "esco_count": g["esco_count"]}
        for g in esco_groups
    ])
    totals = df.groupby("isco2")["esco_count"].sum().rename("esco_total_2d")
    df = df.merge(totals, on="isco2")
    df["weight"] = df["esco_count"] / df["esco_total_2d"]
    return df[["isco3", "isco2", "weight"]]


def load_all_employment():
    """Load employment from Eurostat + ONS, return unified DataFrame."""
    print("Loading Eurostat employment...")
    emp = pd.read_csv(EMP_FILE, dtype={"isco2": str})
    # Remap country codes
    emp["country"] = emp["country"].replace(CODE_REMAP)
    print(f"  {len(emp)} rows, {emp['country'].nunique()} countries")

    # Add UK from ONS
    if ONS_EMP_FILE.exists():
        print("Loading ONS employment (UK)...")
        uk_emp = pd.read_csv(ONS_EMP_FILE, dtype={"isco2": str})
        uk_emp = uk_emp[["isco2", "country", "employment_thousands"]].copy()
        uk_emp["year"] = uk_emp.get("year", 2025)
        emp = pd.concat([emp, uk_emp[["isco2", "country", "employment_thousands", "year"]]], ignore_index=True)
        print(f"  Added UK: {len(uk_emp)} rows")
    else:
        print("  ONS employment file not found, skipping UK")

    countries = sorted(emp["country"].unique())
    print(f"  Total: {len(emp)} rows, {len(countries)} countries")
    print(f"  Countries: {', '.join(countries)}")
    return emp


def load_all_wages():
    """Load wages from Eurostat + BFS + ONS.

    Returns dict: {country: {isco_code: wage_eur}}
    BFS provides ISCO 2-digit for CH (preferred over Eurostat ISCO 1-digit).
    ONS provides ISCO 2-digit for UK.
    Eurostat provides ISCO 1-digit for all others.
    """
    wages = {}  # {country: {isco_code: {"wage": float, "source": str, "level": int}}}

    # 1. Eurostat SES (baseline, ISCO 1-digit)
    print("Loading Eurostat wages...")
    wage_df = pd.read_csv(WAGE_FILE, dtype={"isco1": str})
    wage_df["country"] = wage_df["country"].replace(CODE_REMAP)
    for _, row in wage_df.iterrows():
        country = row["country"]
        if country not in wages:
            wages[country] = {}
        wages[country][row["isco1"]] = {
            "wage": row["mean_annual_eur"],
            "source": "eurostat",
            "level": 1,
        }
    eurostat_countries = sorted(wages.keys())
    print(f"  {len(wage_df)} rows, {len(eurostat_countries)} countries (ISCO 1-digit)")

    # 2. BFS LSE 2024 — override CH with ISCO 2-digit + 1-digit
    if BFS_WAGE_FILE.exists():
        print("Loading BFS wages (CH override)...")
        bfs = pd.read_csv(BFS_WAGE_FILE, dtype={"isco_code": str})
        if "CH" not in wages:
            wages["CH"] = {}
        # Load both 1-digit and 2-digit; 2-digit takes priority for matching
        for _, row in bfs.iterrows():
            code = row["isco_code"]
            level = int(row["isco_digits"])
            wages["CH"][code] = {
                "wage": row["mean_annual_eur"],
                "source": "bfs",
                "level": level,
            }
        bfs_1d = len(bfs[bfs["isco_digits"] == 1])
        bfs_2d = len(bfs[bfs["isco_digits"] == 2])
        print(f"  BFS CH: {bfs_1d} ISCO 1-digit + {bfs_2d} ISCO 2-digit groups")
    else:
        print("  BFS wage file not found, using Eurostat for CH")

    # 3. ONS ASHE 2025 — add UK with ISCO 2-digit + 1-digit
    if ONS_WAGE_FILE.exists():
        print("Loading ONS wages (UK)...")
        ons = pd.read_csv(ONS_WAGE_FILE, dtype={"isco_code": str})
        wages["UK"] = {}
        for _, row in ons.iterrows():
            code = row["isco_code"]
            level = int(row["isco_digits"])
            wages["UK"][code] = {
                "wage": row["mean_annual_eur"],
                "source": "ons",
                "level": level,
            }
        ons_1d = len(ons[ons["isco_digits"] == 1])
        ons_2d = len(ons[ons["isco_digits"] == 2])
        print(f"  ONS UK: {ons_1d} ISCO 1-digit + {ons_2d} ISCO 2-digit groups")
    else:
        print("  ONS wage file not found, skipping UK wages")

    return wages


def resolve_wage(wages_country: dict, isco3: str) -> tuple[float | None, str, str]:
    """Resolve wage for an ISCO 3-digit code from a country's wage data.

    Priority: ISCO 2-digit match → ISCO 1-digit fallback.
    Returns (wage_eur, source, level_used).
    """
    if not wages_country:
        return None, "", ""

    isco2 = isco3[:2]
    isco1 = isco3[0]

    # Try ISCO 2-digit first
    if isco2 in wages_country:
        entry = wages_country[isco2]
        return entry["wage"], entry["source"], "isco2"

    # Fall back to ISCO 1-digit
    if isco1 in wages_country:
        entry = wages_country[isco1]
        return entry["wage"], entry["source"], "isco1"

    return None, "", ""


def main():
    print("=" * 60)
    print("Building occupations for all countries")
    print("=" * 60)

    esco_groups = load_esco()
    print(f"\n{len(esco_groups)} ISCO 3-digit groups from ESCO\n")

    weights = build_weights(esco_groups)
    emp_df = load_all_employment()
    wages = load_all_wages()

    all_countries = sorted(emp_df["country"].unique())
    print(f"\n{len(all_countries)} countries with employment data")

    # ── Build metadata CSV (occupations.csv) ──
    print("\nBuilding metadata CSV...")
    meta_rows = []
    for g in esco_groups:
        meta_rows.append({
            "isco3": g["isco3"],
            "isco3_label": g["isco3_label"],
            "isco2": g["isco2"],
            "isco2_label": g["isco2_label"],
            "isco1": g["isco1"],
            "isco1_label": g["isco1_label"],
            "esco_occupation_count": g["esco_count"],
            "composite_description": g["composite_description"],
            "sample_skills": "; ".join(g["sample_skills"]),
            "esco_occupations": "; ".join(g["esco_occupations"]),
        })
    meta_df = pd.DataFrame(meta_rows)

    # ── Build country data CSV (long format) ──
    print("Distributing employment and resolving wages...")
    country_rows = []

    for country in all_countries:
        country_emp = emp_df[emp_df["country"] == country].set_index("isco2")["employment_thousands"]
        country_wages = wages.get(country, {})

        for _, w in weights.iterrows():
            isco3 = w["isco3"]
            isco2 = w["isco2"]

            # Distribute 2-digit employment to 3-digit
            emp_2d = country_emp.get(isco2, None)
            emp_3d = round(emp_2d * w["weight"], 1) if pd.notna(emp_2d) else None

            # Resolve wage
            wage_eur, wage_source, wage_level = resolve_wage(country_wages, isco3)

            if emp_3d is not None or wage_eur is not None:
                country_rows.append({
                    "isco3": isco3,
                    "country": country,
                    "employment_thousands": emp_3d,
                    "mean_annual_wage_eur": round(wage_eur) if wage_eur is not None else None,
                    "wage_source": wage_source,
                    "wage_level": wage_level,
                })

    country_df = pd.DataFrame(country_rows)

    # ── Save outputs ──
    meta_df.to_csv(OUTPUT_META, index=False)
    country_df.to_csv(OUTPUT_COUNTRY, index=False)

    # ── Summary ──
    print(f"\nOutput: {OUTPUT_META} ({len(meta_df)} rows)")
    print(f"Output: {OUTPUT_COUNTRY} ({len(country_df)} rows)")

    n_countries = country_df["country"].nunique()
    print(f"\n{n_countries} countries in country data")

    # Per-country summary
    print("\nEmployment coverage by country:")
    for country in sorted(country_df["country"].unique()):
        c_data = country_df[country_df["country"] == country]
        c_emp = c_data["employment_thousands"].sum()
        c_groups = c_data["employment_thousands"].notna().sum()
        c_wage_source = c_data["wage_source"].mode().iloc[0] if len(c_data["wage_source"].dropna()) > 0 else "none"
        c_wage_groups = c_data["mean_annual_wage_eur"].notna().sum()
        print(f"  {country:>5}: {c_emp:>10,.1f}k emp ({c_groups:>3} groups)  |  wages: {c_wage_source:>10} ({c_wage_groups:>3} groups)")

    # EU27 summary
    eu = country_df[country_df["country"] == "EU27"]
    eu_total = eu["employment_thousands"].sum()
    print(f"\nEU27 total: {eu_total:,.0f}k ({eu_total/1000:.1f}M)")


if __name__ == "__main__":
    main()
