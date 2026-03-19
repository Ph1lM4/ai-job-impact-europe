"""
11_fetch_education.py — Fetch Eurostat lfsa_egised (employment by ISCO 1-digit × ISCED education level × country).

Cross-tab ISCED 0-2 (low), 3-4 (mid), 5-8 (high/tertiary).
Education score = pct_high_ed rescaled to 0-10.

Output: data/eurostat/education_by_occupation.csv
  Columns: isco1, country, pct_low_ed, pct_mid_ed, pct_high_ed, ed_score
"""

import numpy as np
import pandas as pd
import eurostat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "eurostat" / "education_by_occupation.csv"

# Geo codes to exclude (aggregates)
EXCLUDE_GEO = {
    "EA19", "EA20", "EA21", "EU15", "EU25", "EU27_2007", "EU28",
    "EEA30_2007", "EEA31", "EFTA",
}

# Map Eurostat geo codes to our country codes
EUROSTAT_GEO_MAP = {
    "EU27_2020": "EU27",
}

# ISCED groupings
ISCED_LOW = {"ED0-2"}       # ISCED 0-2: pre-primary to lower secondary
ISCED_MID = {"ED3_4"}       # ISCED 3-4: upper secondary, post-secondary non-tertiary
ISCED_HIGH = {"ED5-8"}      # ISCED 5-8: tertiary (short-cycle, bachelor, master, doctoral)


def main():
    print("=" * 60)
    print("Fetching Eurostat LFSA_EGISED (Education by Occupation)")
    print("=" * 60)

    print("  Fetching dataset (this may take a minute)...")
    df = eurostat.get_data_df("LFSA_EGISED")

    geo_col = "geo\\TIME_PERIOD"
    print(f"  Raw: {len(df)} rows")
    print(f"  Columns: {list(df.columns[:8])}...")

    # Filter: sex=T (total), exclude geo aggregates
    mask = (
        (df["sex"] == "T")
        & (~df[geo_col].isin(EXCLUDE_GEO))
    )
    df = df[mask].copy()
    print(f"  After sex=T filter: {len(df)} rows")

    # Keep only ISCO 1-digit codes (OC1..OC9, OC0)
    df = df[df["isco08"].str.match(r"^OC\d$")].copy()
    df["isco1"] = df["isco08"].str.replace("OC", "")
    print(f"  After ISCO 1-digit filter: {len(df)} rows")

    # Keep only our ISCED groups
    all_isced = ISCED_LOW | ISCED_MID | ISCED_HIGH
    df = df[df["isced11"].isin(all_isced)].copy()
    print(f"  After ISCED filter: {len(df)} rows")

    # Map geo codes
    df["country"] = df[geo_col].map(lambda x: EUROSTAT_GEO_MAP.get(x, x))

    # Find latest year with data
    year_cols = sorted([c for c in df.columns if c.startswith("20")])
    print(f"  Available years: {year_cols[-5:] if len(year_cols) > 5 else year_cols}")

    # Use the latest year with decent data coverage
    latest_year = None
    for y in reversed(year_cols):
        non_null = df[y].notna().sum()
        if non_null > 50:
            latest_year = y
            break
    if latest_year is None:
        latest_year = year_cols[-1]
    print(f"  Using year: {latest_year}")

    df["value"] = pd.to_numeric(df[latest_year], errors="coerce")
    df = df.dropna(subset=["value"])
    df = df[df["value"] > 0]
    print(f"  After dropping NaN/zero: {len(df)} rows")

    # Assign education level group
    def ed_group(isced):
        if isced in ISCED_LOW:
            return "low"
        elif isced in ISCED_MID:
            return "mid"
        elif isced in ISCED_HIGH:
            return "high"
        return None

    df["ed_level"] = df["isced11"].map(ed_group)

    # Pivot: isco1 × country → low/mid/high employment values
    pivot = df.pivot_table(
        index=["isco1", "country"],
        columns="ed_level",
        values="value",
        aggfunc="sum",
    ).reset_index()

    # Fill missing with 0
    for col in ["low", "mid", "high"]:
        if col not in pivot.columns:
            pivot[col] = 0
        pivot[col] = pivot[col].fillna(0)

    # Compute percentages
    pivot["total"] = pivot["low"] + pivot["mid"] + pivot["high"]
    pivot = pivot[pivot["total"] > 0].copy()

    pivot["pct_low_ed"] = round(pivot["low"] / pivot["total"] * 100, 1)
    pivot["pct_mid_ed"] = round(pivot["mid"] / pivot["total"] * 100, 1)
    pivot["pct_high_ed"] = round(pivot["high"] / pivot["total"] * 100, 1)

    # Education score: pct_high_ed rescaled to 0-10 within each country
    result_rows = []
    for country, grp in pivot.groupby("country"):
        pct_vals = grp["pct_high_ed"].values
        pct_min, pct_max = pct_vals.min(), pct_vals.max()
        spread = pct_max - pct_min
        if spread < 0.1:
            spread = 1.0  # avoid div by zero

        for _, row in grp.iterrows():
            score = ((row["pct_high_ed"] - pct_min) / spread) * 10
            score = round(max(0, min(10, score)), 1)
            result_rows.append({
                "isco1": row["isco1"],
                "country": row["country"],
                "pct_low_ed": row["pct_low_ed"],
                "pct_mid_ed": row["pct_mid_ed"],
                "pct_high_ed": row["pct_high_ed"],
                "ed_score": score,
            })

    result = pd.DataFrame(result_rows)

    # Print stats
    print(f"\n  Coverage: {result['country'].nunique()} countries × {result['isco1'].nunique()} ISCO groups")
    print(f"  Total rows: {len(result)}")

    arr = result["ed_score"].values
    print(f"\n  ed_score distribution:")
    print(f"    min={arr.min():.1f}  p25={np.percentile(arr,25):.1f}  median={np.median(arr):.1f}  p75={np.percentile(arr,75):.1f}  max={arr.max():.1f}")

    pct = result["pct_high_ed"].values
    print(f"  pct_high_ed distribution:")
    print(f"    min={pct.min():.1f}%  p25={np.percentile(pct,25):.1f}%  median={np.median(pct):.1f}%  p75={np.percentile(pct,75):.1f}%  max={pct.max():.1f}%")

    # Show EU27 sample
    eu = result[result["country"] == "EU27"].sort_values("ed_score", ascending=False)
    if len(eu) > 0:
        print(f"\n  EU27 Education by ISCO 1-digit:")
        for _, row in eu.iterrows():
            print(f"    ISCO {row['isco1']}: ed_score={row['ed_score']:4.1f}  low={row['pct_low_ed']:5.1f}%  mid={row['pct_mid_ed']:5.1f}%  high={row['pct_high_ed']:5.1f}%")

    # Save
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)
    print(f"\n  Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
