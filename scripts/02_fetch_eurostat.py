"""
02_fetch_eurostat.py — Download employment + wage data from Eurostat.

Employment: LFSA_EGAI2D (ISCO-08 2-digit, employed persons in thousands)
Wages: EARN_SES22_28 (mean annual earnings by ISCO 1-digit, 2022 SES)

Pulls ALL available countries (EU-27, EFTA, candidates) — no country filter.

Output:
  data/eurostat/employment_isco2d.csv
  data/eurostat/wages_isco.csv
"""

import eurostat
import pandas as pd
from pathlib import Path

OUT_DIR = Path("data/eurostat")

# Geo codes to exclude: aggregates and non-country entries
EXCLUDE_GEO = {
    "EA19", "EA20", "EA21", "EU15", "EU25", "EU27_2007", "EU28",
    "EEA30_2007", "EEA31", "EFTA",
}


def fetch_employment():
    """Fetch LFSA_EGAI2D — employment by ISCO 2-digit, all countries."""
    print("Fetching LFSA_EGAI2D (employment by ISCO-08 2-digit)...")
    df = eurostat.get_data_df("LFSA_EGAI2D")

    # Filter: total sex, working-age (15-64)
    geo_col = "geo\\TIME_PERIOD"
    mask = (
        (df["sex"] == "T")
        & (df["age"] == "Y15-64")
        & (~df[geo_col].isin(EXCLUDE_GEO))
    )
    df = df[mask].copy()

    # Find latest year column with data
    year_cols = [c for c in df.columns if c.startswith("20")]
    latest_year = None
    for col in reversed(sorted(year_cols)):
        if df[col].notna().any():
            latest_year = col
            break

    print(f"  Using year: {latest_year}")

    # Keep only 2-digit ISCO codes (OC11, OC25, etc. — length 4)
    # and filter out aggregates (OC1, OC2 = 1-digit; TOTAL; NRP)
    df = df[df["isco08"].str.match(r"^OC\d{2}$")].copy()

    # Parse ISCO code: OC25 → 25
    df["isco2"] = df["isco08"].str.replace("OC", "")

    result = df[["isco2", geo_col, latest_year]].rename(
        columns={geo_col: "country", latest_year: "employment_thousands"}
    )
    result["year"] = int(latest_year)

    # Drop rows with no employment data
    result = result.dropna(subset=["employment_thousands"])

    countries = sorted(result["country"].unique())
    print(f"  {len(result)} rows ({result['isco2'].nunique()} ISCO groups × {len(countries)} countries)")
    print(f"  Countries: {', '.join(countries)}")
    return result


def fetch_wages():
    """Fetch EARN_SES22_28 — mean annual earnings by ISCO 1-digit, all countries."""
    print("Fetching EARN_SES22_28 (mean annual earnings by ISCO, 2022 SES)...")
    df = eurostat.get_data_df("EARN_SES22_28")

    geo_col = "geo\\TIME_PERIOD"
    # Filter: total sex, total age, enterprises ≥10 employees, ERN indicator
    mask = (
        (df["sex"] == "T")
        & (df["age"] == "TOTAL")
        & (df["sizeclas"] == "GE10")
        & (df["indic_se"] == "ERN")
        & (~df[geo_col].isin(EXCLUDE_GEO))
    )
    df = df[mask].copy()

    # Keep single-digit ISCO codes (OC1..OC9, OC0)
    df = df[df["isco08"].str.match(r"^OC\d$")].copy()
    df["isco1"] = df["isco08"].str.replace("OC", "")

    result = df[["isco1", geo_col, "2022"]].rename(
        columns={geo_col: "country", "2022": "mean_annual_eur"}
    )
    result = result.drop_duplicates(subset=["isco1", "country"])
    result = result.dropna(subset=["mean_annual_eur"])
    result["year"] = 2022

    countries = sorted(result["country"].unique())
    print(f"  {len(result)} rows ({result['isco1'].nunique()} ISCO groups × {len(countries)} countries)")
    print(f"  Countries: {', '.join(countries)}")
    return result


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    emp = fetch_employment()
    emp_path = OUT_DIR / "employment_isco2d.csv"
    emp.to_csv(emp_path, index=False)
    print(f"  Saved: {emp_path}")

    # Quick summary
    eu = emp[emp["country"] == "EU27_2020"]
    total = eu["employment_thousands"].sum()
    print(f"  EU27 total employment: {total:,.0f} thousand ({total/1000:.1f}M)")

    # Per-country summary
    print("\n  Employment coverage by country:")
    for country in sorted(emp["country"].unique()):
        c_total = emp[emp["country"] == country]["employment_thousands"].sum()
        c_groups = emp[emp["country"] == country]["isco2"].nunique()
        print(f"    {country:15s}: {c_total:8,.0f}k  ({c_groups} ISCO groups)")

    wages = fetch_wages()
    wages_path = OUT_DIR / "wages_isco.csv"
    wages.to_csv(wages_path, index=False)
    print(f"  Saved: {wages_path}")


if __name__ == "__main__":
    main()
