"""
10_fetch_growth.py — Parse Cedefop employment forecast + fetch Eurostat YoY employment change.

Section 1: Parse Cedefop Skills Forecast 2025 (xlsx in data/cedefop/)
  - ISCO 1-digit × country, employment 2024 + 2035 projections
  - Compute CAGR (compound annual growth rate)
  - Output: data/cedefop/growth_forecast.csv

Section 2: Fetch Eurostat LFSA_EGAI2D for 2023 + 2024
  - ISCO 2-digit × country employment
  - Compute YoY % change
  - Aggregate to ISCO 1-digit (employment-weighted)
  - Output: data/eurostat/employment_yoy.csv

Note: Cedefop raw data must NOT be redistributed (per their terms).
      Only derived scores (growth_score in layer_scores.json) are published.
"""

import pandas as pd
import numpy as np
from pathlib import Path

import eurostat

ROOT = Path(__file__).resolve().parent.parent
CEDEFOP_XLS = ROOT / "data" / "cedefop" / "skills-forecast-2025" / "Employment_occupation.xlsx"
OUT_CEDEFOP = ROOT / "data" / "cedefop" / "growth_forecast.csv"
OUT_EUROSTAT = ROOT / "data" / "eurostat" / "employment_yoy.csv"

# Cedefop uses full country names — map to our ISO codes
CEDEFOP_COUNTRY_MAP = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Cyprus": "CY", "Czech Republic": "CZ", "Denmark": "DK", "Estonia": "EE",
    "Finland": "FI", "France": "FR", "Germany": "DE", "Greece": "EL",
    "Hungary": "HU", "Iceland": "IS", "Ireland": "IE", "Italy": "IT",
    "Latvia": "LV", "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT",
    "Netherlands": "NL", "Norway": "NO", "Poland": "PL", "Portugal": "PT",
    "Romania": "RO", "Slovakia": "SK", "Slovenia": "SI", "Spain": "ES",
    "Sweden": "SE", "Switzerland": "CH", "Turkey": "TR",
    "Republic of North Macedonia": "MK", "EU-27": "EU27",
}

# Geo codes to exclude from Eurostat (aggregates)
EXCLUDE_GEO = {
    "EA19", "EA20", "EA21", "EU15", "EU25", "EU27_2007", "EU28",
    "EEA30_2007", "EEA31", "EFTA",
}

# Map Eurostat geo codes to our country codes
EUROSTAT_GEO_MAP = {
    "EU27_2020": "EU27",
}

# ISCO 2-digit → 1-digit mapping
ISCO2_TO_ISCO1 = {str(i).zfill(2): str(i)[0] for i in range(10, 100)}
ISCO2_TO_ISCO1.update({"01": "0", "02": "0", "03": "0"})


def parse_cedefop():
    """Parse Cedefop Skills Forecast 2025 → CAGR per ISCO 1-digit × country."""
    print("=" * 60)
    print("Section 1: Cedefop Skills Forecast 2025")
    print("=" * 60)

    if not CEDEFOP_XLS.exists():
        print(f"  WARNING: {CEDEFOP_XLS} not found, skipping Cedefop")
        return None

    df = pd.read_excel(CEDEFOP_XLS, sheet_name="Data", header=0)
    print(f"  Loaded: {len(df)} rows, {df['country'].nunique()} countries")

    # Filter out "Total" rows
    df = df[df["isco_1d_code"] != "Total"].copy()

    # Map country names to ISO codes
    df["country_code"] = df["country"].map(CEDEFOP_COUNTRY_MAP)
    unmapped = df[df["country_code"].isna()]["country"].unique()
    if len(unmapped) > 0:
        print(f"  WARNING: Unmapped countries: {unmapped}")

    df = df.dropna(subset=["country_code"])

    # Compute CAGR: (emp_2035 / emp_2024) ^ (1/11) - 1
    df["emp_2024"] = df[2024].astype(float)
    df["emp_2035"] = df[2035].astype(float)
    df["cagr_pct"] = ((df["emp_2035"] / df["emp_2024"]) ** (1 / 11) - 1) * 100

    result = df[["isco_1d_code", "country_code", "occupation", "emp_2024", "emp_2035", "cagr_pct"]].rename(
        columns={"isco_1d_code": "isco1", "country_code": "country"}
    )

    # Print stats
    print(f"\n  Coverage: {result['country'].nunique()} countries × {result['isco1'].nunique()} ISCO groups")
    print(f"  CAGR distribution:")
    arr = result["cagr_pct"].values
    print(f"    min={arr.min():.2f}%  p25={np.percentile(arr,25):.2f}%  median={np.median(arr):.2f}%  p75={np.percentile(arr,75):.2f}%  max={arr.max():.2f}%")

    # Show some examples
    print(f"\n  Sample (EU27):")
    eu = result[result["country"] == "EU27"].sort_values("cagr_pct", ascending=False)
    for _, row in eu.iterrows():
        print(f"    ISCO {row['isco1']} {row['occupation']:<50s}  {row['cagr_pct']:+.2f}%  ({row['emp_2024']:,.0f} → {row['emp_2035']:,.0f})")

    # Save
    OUT_CEDEFOP.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT_CEDEFOP, index=False)
    print(f"\n  Saved: {OUT_CEDEFOP}")

    return result


def fetch_eurostat_yoy():
    """Fetch Eurostat LFSA_EGAI2D for 2023+2024, compute YoY % change."""
    print("\n" + "=" * 60)
    print("Section 2: Eurostat YoY Employment Change (2023→2024)")
    print("=" * 60)

    print("  Fetching LFSA_EGAI2D...")
    df = eurostat.get_data_df("LFSA_EGAI2D")

    geo_col = "geo\\TIME_PERIOD"

    # Filter: total sex, working-age (15-64), exclude aggregates
    mask = (
        (df["sex"] == "T")
        & (df["age"] == "Y15-64")
        & (~df[geo_col].isin(EXCLUDE_GEO))
    )
    df = df[mask].copy()

    # Keep only 2-digit ISCO codes (OC11, OC25, etc.)
    df = df[df["isco08"].str.match(r"^OC\d{2}$")].copy()
    df["isco2"] = df["isco08"].str.replace("OC", "")
    df["isco1"] = df["isco2"].map(ISCO2_TO_ISCO1)

    # Map geo codes
    df["country"] = df[geo_col].map(lambda x: EUROSTAT_GEO_MAP.get(x, x))

    # Find available years
    year_cols = sorted([c for c in df.columns if c.startswith("20")])
    print(f"  Available years: {year_cols}")

    # Use 2023 and 2024 (or latest two years available)
    if "2024" in year_cols and "2023" in year_cols:
        y1, y2 = "2023", "2024"
    else:
        # Fallback to latest two years with data
        usable = [y for y in reversed(year_cols) if df[y].notna().any()]
        y2, y1 = usable[0], usable[1]
    print(f"  Using years: {y1} → {y2}")

    result = df[["isco2", "isco1", "country", y1, y2]].rename(
        columns={y1: "emp_y1", y2: "emp_y2"}
    ).copy()
    result["year_1"] = int(y1)
    result["year_2"] = int(y2)

    # Drop rows missing either year
    result = result.dropna(subset=["emp_y1", "emp_y2"])

    # Compute YoY % change at ISCO 2-digit level
    result["yoy_pct"] = ((result["emp_y2"] / result["emp_y1"]) - 1) * 100

    print(f"  {len(result)} rows ({result['isco2'].nunique()} ISCO-2d × {result['country'].nunique()} countries)")

    # Aggregate to ISCO 1-digit (employment-weighted)
    agg_rows = []
    for (isco1, country), grp in result.groupby(["isco1", "country"]):
        total_emp = grp["emp_y2"].sum()
        if total_emp > 0:
            weighted_yoy = (grp["yoy_pct"] * grp["emp_y2"]).sum() / total_emp
        else:
            weighted_yoy = 0
        agg_rows.append({
            "isco1": isco1,
            "country": country,
            "emp_y1_total": grp["emp_y1"].sum(),
            "emp_y2_total": grp["emp_y2"].sum(),
            "yoy_pct_weighted": round(weighted_yoy, 2),
        })
    agg = pd.DataFrame(agg_rows)

    # Print stats
    print(f"\n  Aggregated: {len(agg)} rows ({agg['isco1'].nunique()} ISCO-1d × {agg['country'].nunique()} countries)")
    arr = agg["yoy_pct_weighted"].values
    print(f"  YoY distribution:")
    print(f"    min={arr.min():.2f}%  p25={np.percentile(arr,25):.2f}%  median={np.median(arr):.2f}%  p75={np.percentile(arr,75):.2f}%  max={arr.max():.2f}%")

    # Show EU27 breakdown
    eu = agg[agg["country"] == "EU27"].sort_values("yoy_pct_weighted", ascending=False)
    if len(eu) > 0:
        print(f"\n  EU27 YoY by ISCO 1-digit:")
        for _, row in eu.iterrows():
            print(f"    ISCO {row['isco1']}:  {row['yoy_pct_weighted']:+.2f}%  ({row['emp_y1_total']:,.0f}k → {row['emp_y2_total']:,.0f}k)")

    # Save detailed (ISCO 2-digit) and aggregated
    OUT_EUROSTAT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT_EUROSTAT, index=False)
    print(f"\n  Saved: {OUT_EUROSTAT}")

    return agg


def main():
    cedefop = parse_cedefop()
    eurostat_yoy = fetch_eurostat_yoy()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    if cedefop is not None:
        cedefop_countries = set(cedefop["country"].unique())
        print(f"  Cedefop: {len(cedefop_countries)} countries (2024→2035 CAGR)")
    else:
        cedefop_countries = set()
        print("  Cedefop: NOT AVAILABLE")

    eurostat_countries = set(eurostat_yoy["country"].unique())
    print(f"  Eurostat: {len(eurostat_countries)} countries (YoY)")

    both = cedefop_countries & eurostat_countries
    cedefop_only = cedefop_countries - eurostat_countries
    eurostat_only = eurostat_countries - cedefop_countries
    print(f"  Both: {len(both)} | Cedefop only: {cedefop_only or 'none'} | Eurostat only: {eurostat_only or 'none'}")


if __name__ == "__main__":
    main()
