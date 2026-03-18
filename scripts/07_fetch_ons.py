"""
07_fetch_ons.py — Parse UK ONS employment + wage data (ASHE Table 2.7a).

Expects manually downloaded files in data/ons/:
  Wages+Employment: ASHE Table 2 — SOC 2020 (2-digit) annual gross pay
    File: ashetable22025provisional/PROV - Occupation SOC20 (2) Table 2.7a   Annual pay - Gross 2025.xlsx
    Sheet "All" has: Description, Code, Number of jobs (thousands), Median, %, Mean, ...

  Employment (optional cross-check): APS employment by SOC 4-digit
    File: employmentby4digitsoc1digitindustryatosuk20212024final.xlsx

SOC 2020 → ISCO-08 mapping is built in (based on ONS correspondence tables).

Output:
  data/ons/employment_uk.csv   — employment by ISCO 2-digit (from ASHE job counts)
  data/ons/wages_uk.csv        — wages by ISCO 1-digit and 2-digit

Usage:
  1. Download ASHE Table 2 from ONS
  2. Place in data/ons/ashetable22025provisional/
  3. Run: python scripts/07_fetch_ons.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

ONS_DIR = Path("data/ons")
OUT_EMP = ONS_DIR / "employment_uk.csv"
OUT_WAGE = ONS_DIR / "wages_uk.csv"

# ──────────────────────────────────────────────────────────────────────
# SOC 2020 → ISCO-08 mapping (2-digit level)
# Based on ONS correspondence tables and structural analysis.
#
# Key differences:
#   SOC 5 (Skilled trades) → ISCO 6/7 (Agricultural/Craft)
#   SOC 6 (Caring/service) → ISCO 5 (Service and sales)
#   SOC 7 (Sales/customer) → ISCO 5 (Service and sales) / ISCO 4
#   SOC 33 (Protective)    → ISCO 54 (Protective services, under ISCO 5)
# ──────────────────────────────────────────────────────────────────────

SOC_ISCO_MAJOR = {
    "1": "1",   # Managers → Managers
    "2": "2",   # Professional → Professionals
    "3": "3",   # Associate professional → Technicians (mostly)
    "4": "4",   # Administrative/secretarial → Clerical support
    "5": "7",   # Skilled trades → Craft (mostly, except 51→6)
    "6": "5",   # Caring, leisure, service → Service and sales
    "7": "5",   # Sales and customer service → Service and sales (mostly)
    "8": "8",   # Process, plant, machine → Plant/machine operators
    "9": "9",   # Elementary → Elementary
}

SOC_ISCO_2D = {
    # SOC 1: Managers
    "11": "11",  # Corporate managers → Chief executives, senior officials
    "12": "14",  # Other managers/proprietors → Hospitality/retail/services managers
    # SOC 2: Professionals
    "21": "21",  # Science, research, engineering, tech → same
    "22": "22",  # Health professionals → same
    "23": "23",  # Teaching professionals → same
    "24": "24",  # Business, media, public service → Business/admin professionals
    # SOC 3: Associate professional
    "31": "31",  # Science, engineering, tech associates → same
    "32": "32",  # Health/social care associates → same
    "33": "54",  # Protective services → ISCO 54 (Protective services workers)
    "34": "34",  # Culture, media, sports → same
    "35": "33",  # Business/public service associates → Business associates
    # SOC 4: Administrative/secretarial
    "41": "41",  # Administrative occupations → General/keyboard clerks
    "42": "41",  # Secretarial → General/keyboard clerks
    # SOC 5: Skilled trades
    "51": "61",  # Skilled agricultural trades → Skilled agricultural workers
    "52": "72",  # Metal, electrical, electronic → Metal/machinery workers
    "53": "71",  # Construction/building → Building trades
    "54": "75",  # Textiles, printing, other → Food/garment/craft workers
    # SOC 6: Caring, leisure, service
    "61": "53",  # Caring personal services → Personal care workers
    "62": "51",  # Leisure, travel, personal service → Personal service workers
    "63": "54",  # Community/civil enforcement → Protective services (small)
    # SOC 7: Sales and customer service
    "71": "52",  # Sales → Shop salespersons
    "72": "42",  # Customer service → Client information workers
    # SOC 8: Process, plant, machine
    "81": "81",  # Process operatives → Stationary plant operators
    "82": "83",  # Transport/mobile machine → Drivers/mobile plant operators
    # SOC 9: Elementary
    "91": "93",  # Elementary trades → Labourers in mining/construction/manufacturing
    "92": "91",  # Elementary admin/service → Cleaners/helpers
}

# GBP → EUR conversion (2023-2024 average)
GBP_EUR_RATE = 1.16


def find_ashe_file() -> Path | None:
    """Find ASHE Table 2.7a (annual gross pay) in data/ons/."""
    ashe_dir = ONS_DIR / "ashetable22025provisional"
    if ashe_dir.exists():
        for f in ashe_dir.iterdir():
            if "2.7a" in f.name and "Annual pay" in f.name and f.suffix == ".xlsx":
                return f

    # Fallback: search ONS_DIR recursively
    for f in ONS_DIR.rglob("*.xlsx"):
        if "2.7a" in f.name and "annual" in f.name.lower():
            return f

    return None


def parse_ashe_annual(ashe_file: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse ASHE Table 2.7a — annual gross pay by SOC 2020 (2-digit).

    Sheet "All" structure:
      Row 0: Title
      Row 1: blank
      Row 2-3: sub-headers
      Row 4: Column headers — Description, Code, Number of jobs (thousand), Median, %, Mean, ...
      Row 5: "All employees" total
      Row 6+: SOC 1-digit major group headers, then indented 2-digit sub-groups
      Row ~41: "Not Classified"
      Row 42+: footnotes

    Returns (employment_df, wages_df).
    """
    print(f"\n--- Parsing ASHE: {ashe_file.name} ---")
    df = pd.read_excel(ashe_file, sheet_name="All", header=None)
    print(f"  Shape: {df.shape}")

    # Columns: 0=Description, 1=Code, 2=Jobs(k), 3=Median, 4=%chg, 5=Mean, 6=%chg
    rows = []
    for i in range(5, len(df)):
        code_val = df.iloc[i, 1]
        desc_val = df.iloc[i, 0]
        jobs_val = df.iloc[i, 2]   # Number of jobs in thousands
        mean_val = df.iloc[i, 5]   # Mean annual pay GBP

        if pd.isna(code_val):
            continue

        code_str = str(int(code_val)) if isinstance(code_val, (int, float)) else str(code_val).strip()

        # Must be 1 or 2-digit SOC code
        if not re.match(r"^\d{1,2}$", code_str):
            continue

        desc_str = str(desc_val).strip() if pd.notna(desc_val) else ""

        # Parse employment (thousands)
        jobs_k = None
        if pd.notna(jobs_val):
            try:
                jobs_k = float(jobs_val)
            except (ValueError, TypeError):
                pass

        # Parse mean wage (handle 'x' = suppressed)
        mean_gbp = None
        if pd.notna(mean_val):
            mean_str = str(mean_val).strip()
            if mean_str not in ("x", ":", "..", ".."):
                try:
                    mean_gbp = float(mean_str)
                except (ValueError, TypeError):
                    pass

        rows.append({
            "soc_code": code_str,
            "soc_digits": len(code_str),
            "description": desc_str[:60],
            "employment_thousands": jobs_k,
            "mean_annual_gbp": mean_gbp,
        })

    if not rows:
        print("  ERROR: Could not extract ASHE data.")
        return pd.DataFrame(), pd.DataFrame()

    ashe = pd.DataFrame(rows)

    soc1 = ashe[ashe["soc_digits"] == 1].copy()
    soc2 = ashe[ashe["soc_digits"] == 2].copy()
    print(f"  Found {len(soc1)} SOC 1-digit + {len(soc2)} SOC 2-digit groups")

    # ── Employment: map SOC 2-digit → ISCO 2-digit ──
    soc2["isco2"] = soc2["soc_code"].map(SOC_ISCO_2D)
    emp = soc2[soc2["isco2"].notna() & soc2["employment_thousands"].notna()].copy()

    # Aggregate by ISCO 2-digit (some SOC codes merge, e.g. SOC 41+42 → ISCO 41)
    emp_agg = emp.groupby("isco2").agg(
        employment_thousands=("employment_thousands", "sum"),
    ).reset_index()
    emp_agg["country"] = "UK"
    emp_agg["year"] = 2025
    emp_agg["source"] = "ONS_ASHE"

    total_emp = emp_agg["employment_thousands"].sum()
    print(f"\n  Employment: {len(emp_agg)} ISCO 2-digit groups, total {total_emp:,.0f}k ({total_emp/1000:.1f}M)")
    for _, row in emp_agg.iterrows():
        print(f"    ISCO {row['isco2']:>2}: {row['employment_thousands']:>7,.0f}k")

    # ── Wages: map SOC 2-digit → ISCO 2-digit, then also aggregate to 1-digit ──
    wage2 = soc2[soc2["isco2"].notna() & soc2["mean_annual_gbp"].notna()].copy()
    wage2["mean_annual_eur"] = (wage2["mean_annual_gbp"] * GBP_EUR_RATE).round(0)

    # Weight wages by employment when aggregating
    wage2["weighted_wage"] = wage2["mean_annual_gbp"] * wage2["employment_thousands"].fillna(1)
    wage2["weight"] = wage2["employment_thousands"].fillna(1)

    # ISCO 2-digit wages (direct mapping, weighted avg where merged)
    wage_2d = wage2.groupby("isco2").apply(
        lambda g: pd.Series({
            "mean_annual_gbp": round((g["weighted_wage"].sum() / g["weight"].sum()), 0),
        })
    ).reset_index()
    wage_2d["mean_annual_eur"] = (wage_2d["mean_annual_gbp"] * GBP_EUR_RATE).round(0)

    # ISCO 1-digit wages (aggregate from 2-digit, employment-weighted)
    wage2["isco1"] = wage2["isco2"].str[0]
    wage_1d = wage2.groupby("isco1").apply(
        lambda g: pd.Series({
            "mean_annual_gbp": round((g["weighted_wage"].sum() / g["weight"].sum()), 0),
        })
    ).reset_index()
    wage_1d["mean_annual_eur"] = (wage_1d["mean_annual_gbp"] * GBP_EUR_RATE).round(0)

    # Combine 1-digit and 2-digit into single output
    wage_1d["isco_code"] = wage_1d["isco1"]
    wage_1d["isco_digits"] = 1
    wage_2d["isco_code"] = wage_2d["isco2"]
    wage_2d["isco_digits"] = 2

    wages = pd.concat([
        wage_1d[["isco_code", "isco_digits", "mean_annual_gbp", "mean_annual_eur"]],
        wage_2d[["isco_code", "isco_digits", "mean_annual_gbp", "mean_annual_eur"]],
    ], ignore_index=True)
    wages["country"] = "UK"
    wages["year"] = 2025
    wages["source"] = "ONS_ASHE"

    print(f"\n  Wages: {len(wage_1d)} ISCO 1-digit + {len(wage_2d)} ISCO 2-digit groups")
    print(f"\n  ISCO 1-digit wages:")
    for _, row in wage_1d.iterrows():
        print(f"    ISCO {row['isco1']}: {row['mean_annual_gbp']:>8,.0f} GBP → {row['mean_annual_eur']:>8,.0f} EUR")
    print(f"\n  ISCO 2-digit wages ({len(wage_2d)} groups):")
    for _, row in wage_2d.iterrows():
        print(f"    ISCO {row['isco2']:>2}: {row['mean_annual_gbp']:>8,.0f} GBP → {row['mean_annual_eur']:>8,.0f} EUR")

    return emp_agg, wages


def cross_check_aps(ashe_emp: pd.DataFrame) -> None:
    """Optional: cross-check ASHE employment with APS 4-digit data."""
    aps_file = ONS_DIR / "employmentby4digitsoc1digitindustryatosuk20212024final.xlsx"
    if not aps_file.exists():
        return

    print(f"\n--- Cross-check: APS employment ({aps_file.name}) ---")
    df = pd.read_excel(aps_file, sheet_name="2024", header=None)

    # Sum across industry columns (cols 2-20) for each SOC 4-digit row
    soc_totals = {}
    for i in range(8, len(df)):
        soc_raw = df.iloc[i, 1]
        if pd.isna(soc_raw):
            continue
        soc_str = str(soc_raw).strip()
        m = re.match(r"^(\d{4})\s", soc_str)
        if not m:
            continue
        soc4 = m.group(1)
        soc2 = soc4[:2]

        # Sum across industry columns
        total = 0
        for j in range(2, min(21, df.shape[1])):
            val = df.iloc[i, j]
            if pd.notna(val):
                v_str = str(val).strip()
                if v_str not in ("*", "-", ""):
                    try:
                        total += float(v_str)
                    except ValueError:
                        pass

        if soc2 not in soc_totals:
            soc_totals[soc2] = 0
        soc_totals[soc2] += total

    if soc_totals:
        print(f"  APS SOC 2-digit totals (from {len(soc_totals)} groups):")
        aps_total = sum(soc_totals.values())
        print(f"  APS total: {aps_total:,.0f} persons ({aps_total/1e6:.1f}M)")
        ashe_total = ashe_emp["employment_thousands"].sum() * 1000
        print(f"  ASHE total: {ashe_total:,.0f} persons ({ashe_total/1e6:.1f}M)")
        ratio = ashe_total / aps_total if aps_total > 0 else 0
        print(f"  Ratio ASHE/APS: {ratio:.2f}")


def main():
    if not ONS_DIR.exists():
        print(f"Directory {ONS_DIR} does not exist.")
        sys.exit(1)

    ashe_file = find_ashe_file()
    if ashe_file is None:
        print("  ASHE Table 2.7a not found in data/ons/")
        print("  Expected: ashetable22025provisional/PROV - Occupation SOC20 (2) Table 2.7a   Annual pay - Gross 2025.xlsx")
        sys.exit(1)

    emp, wages = parse_ashe_annual(ashe_file)

    if not emp.empty:
        emp.to_csv(OUT_EMP, index=False)
        print(f"\n  Saved: {OUT_EMP}")

    if not wages.empty:
        wages.to_csv(OUT_WAGE, index=False)
        print(f"\n  Saved: {OUT_WAGE}")

    # Optional cross-check
    if not emp.empty:
        cross_check_aps(emp)

    print("\nDone.")


if __name__ == "__main__":
    main()
