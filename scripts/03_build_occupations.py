"""
03_build_occupations.py — Merge ESCO processed data + Eurostat stats → occupations.csv

Distributes ISCO 2-digit employment to 3-digit groups using ESCO occupation counts as weights.
Attaches wage data at ISCO 1-digit level.

Input:  data/esco/esco_processed.json, data/eurostat/employment_isco2d.csv, data/eurostat/wages_isco.csv
Output: occupations.csv
"""

import json
import pandas as pd
from pathlib import Path

ROOT = Path(".")
ESCO_FILE = ROOT / "data/esco/esco_processed.json"
EMP_FILE = ROOT / "data/eurostat/employment_isco2d.csv"
WAGE_FILE = ROOT / "data/eurostat/wages_isco.csv"
OUTPUT = ROOT / "occupations.csv"

COUNTRY_COLS = {
    "EU27_2020": "employment_eu27",
    "DE": "employment_de",
    "AT": "employment_at",
    "CH": "employment_ch",
}


def load_esco():
    with open(ESCO_FILE, encoding="utf-8") as f:
        return json.load(f)


def distribute_employment(esco_groups, emp_df):
    """Distribute 2-digit employment to 3-digit using ESCO occupation counts."""
    # Build weight: esco_count per 3-digit / total esco_count per 2-digit
    df = pd.DataFrame([
        {"isco3": g["isco3"], "isco2": g["isco2"], "esco_count": g["esco_count"]}
        for g in esco_groups
    ])
    totals = df.groupby("isco2")["esco_count"].sum().rename("esco_total_2d")
    df = df.merge(totals, on="isco2")
    df["weight"] = df["esco_count"] / df["esco_total_2d"]

    results = {}
    for country, col_name in COUNTRY_COLS.items():
        country_emp = emp_df[emp_df["country"] == country].set_index("isco2")["employment_thousands"]
        emp_values = {}
        for _, row in df.iterrows():
            emp_2d = country_emp.get(row["isco2"], None)
            if pd.notna(emp_2d):
                emp_values[row["isco3"]] = round(emp_2d * row["weight"], 1)
            else:
                emp_values[row["isco3"]] = None
        results[col_name] = emp_values

    return results


def main():
    print("Loading ESCO processed data...")
    esco_groups = load_esco()
    print(f"  {len(esco_groups)} ISCO 3-digit groups")

    print("Loading Eurostat employment...")
    emp_df = pd.read_csv(EMP_FILE, dtype={"isco2": str})
    print(f"  {len(emp_df)} rows")

    print("Loading Eurostat wages...")
    wage_df = pd.read_csv(WAGE_FILE, dtype={"isco1": str})
    print(f"  {len(wage_df)} rows")

    print("Distributing employment to 3-digit groups...")
    emp_distributed = distribute_employment(esco_groups, emp_df)

    # Build wage lookup: isco1 → country → mean_annual_eur
    wage_lookup = {}
    for _, row in wage_df.iterrows():
        wage_lookup.setdefault(row["isco1"], {})[row["country"]] = row["mean_annual_eur"]

    print("Building occupations table...")
    rows = []
    for g in esco_groups:
        row = {
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
        }

        # Add distributed employment
        for col_name, values in emp_distributed.items():
            row[col_name] = values.get(g["isco3"])

        # Add wage (EU27 at ISCO 1-digit)
        eu_wage = wage_lookup.get(g["isco1"], {}).get("EU27_2020")
        row["mean_annual_wage_eur"] = eu_wage

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT, index=False)

    # Summary
    eu_total = df["employment_eu27"].sum()
    print(f"\nOutput: {OUTPUT}")
    print(f"  {len(df)} occupation groups")
    print(f"  EU27 total employment: {eu_total:,.0f} thousand ({eu_total/1000:.1f}M)")
    print(f"  Groups with EU27 employment: {df['employment_eu27'].notna().sum()}")
    print(f"  Groups with wage data: {df['mean_annual_wage_eur'].notna().sum()}")

    # Show top 10 by employment
    print("\nTop 10 by EU27 employment:")
    top = df.nlargest(10, "employment_eu27")[["isco3", "isco3_label", "employment_eu27"]]
    for _, r in top.iterrows():
        print(f"  {r['isco3']} {r['isco3_label']}: {r['employment_eu27']:,.0f}k")


if __name__ == "__main__":
    main()
