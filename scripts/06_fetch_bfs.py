"""
06_fetch_bfs.py — Parse Swiss BFS employment + wage data.

Expects manually downloaded files in data/bfs/:
  Employment: je-d-03.02.01.21.xlsx — CH-ISCO-19 major groups, yearly, in 1000s
  Wages:      je-d-03.04.01.02.47.xlsx — monthly median gross wage by CH-ISCO-19

BFS uses CH-ISCO-19 which is directly based on ISCO-08 — codes are compatible.

Output:
  data/bfs/employment_ch_bfs.csv   — employment by ISCO 1-digit (BFS only publishes 1-digit)
  data/bfs/wages_ch_bfs.csv        — wages by ISCO 1-digit and 2-digit

Usage:
  1. Download from BFS and place in data/bfs/
  2. Run: python scripts/06_fetch_bfs.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

BFS_DIR = Path("data/bfs")
OUT_EMP = BFS_DIR / "employment_ch_bfs.csv"
OUT_WAGE = BFS_DIR / "wages_ch_bfs.csv"

# German ISCO major group names → ISCO 1-digit code
ISCO1_DE = {
    "Führungskräfte": "1",
    "Intellektuelle und wissenschaftliche Berufe": "2",
    "Techniker/innen und gleichrangige nichttechnische Berufe": "3",
    "Bürokräfte und verwandte Berufe": "4",
    "Dienstleistungsberufe und Verkäufer/innen": "5",
    "Fachkräfte in Land- und Forstwirtschaft und Fischerei": "6",
    "Handwerks- und verwandte Berufe": "7",
    "Bediener/innen von Anlagen und Maschinen und Montageberufe": "8",
    "Hilfsarbeitskräfte": "9",
    "Keine Angabe/Angehörige der regulären Streitkräfte": "0",
}


def parse_employment() -> pd.DataFrame:
    """Parse je-d-03.02.01.21.xlsx — employment by CH-ISCO-19 major group.

    Structure (sheet: Nationalität-Jahreswerte):
      Row 4: header — [label, 2023, 2024, 2025]
      Row 7-17: Swiss nationals by ISCO major group
      Row 18: Ausländer/innen header
      Row 19-28: Foreign nationals by ISCO major group
      Row 29: Total row (full workforce)
      Row 30+: Total breakdown by ISCO major group

    Values are in thousands (Jahresdurchschnittswerte, in 1000).
    """
    emp_file = BFS_DIR / "je-d-03.02.01.21.xlsx"
    if not emp_file.exists():
        print(f"  Employment file not found: {emp_file}")
        print("  Download from: https://www.bfs.admin.ch → Arbeit und Erwerb → Erwerbstätigkeit")
        return pd.DataFrame()

    print(f"--- Parsing employment: {emp_file.name} ---")
    df = pd.read_excel(emp_file, sheet_name="Nationalität-Jahreswerte", header=None)
    print(f"  Shape: {df.shape}")

    # Find the year columns from the header row (row 4)
    header_row = df.iloc[4]
    year_cols = {}
    for i, val in enumerate(header_row):
        if pd.notna(val):
            try:
                year = int(float(val))
                if 2020 <= year <= 2030:
                    year_cols[year] = i
            except (ValueError, TypeError):
                pass

    if not year_cols:
        print("  ERROR: Could not find year columns in header row.")
        return pd.DataFrame()

    latest_year = max(year_cols.keys())
    year_col_idx = year_cols[latest_year]
    print(f"  Years available: {sorted(year_cols.keys())}, using {latest_year}")

    # Find the "Total" section — after both Swiss and Foreign subsections
    # Look for second "Total" which starts the combined data
    total_rows = []
    for i in range(len(df)):
        val = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ""
        if val == "Total" and i > 20:  # Second "Total" is around row 29+
            # The rows after this Total are the combined ISCO breakdowns
            for j in range(i + 1, min(i + 15, len(df))):
                label = str(df.iloc[j, 0]).strip() if pd.notna(df.iloc[j, 0]) else ""
                value = df.iloc[j, year_col_idx]
                # Match against known ISCO labels
                matched_isco = None
                for de_label, code in ISCO1_DE.items():
                    if label.startswith(de_label):
                        matched_isco = code
                        break
                if matched_isco and pd.notna(value):
                    total_rows.append({
                        "isco1": matched_isco,
                        "label_de": label,
                        "employment_thousands": round(float(value), 1),
                    })
            break

    # If we couldn't find the combined Total section, fall back to summing
    # Swiss + Foreign for each ISCO group
    if not total_rows:
        print("  Combined total section not found, summing Swiss + Foreign...")
        swiss_data = {}
        foreign_data = {}
        current_section = None

        for i in range(5, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ""
            value = df.iloc[i, year_col_idx]

            if "Schweizer" in label:
                current_section = "swiss"
                continue
            elif "Ausländer" in label:
                current_section = "foreign"
                continue
            elif label == "Total" and i > 20:
                break

            for de_label, code in ISCO1_DE.items():
                if label.startswith(de_label) and pd.notna(value):
                    target = swiss_data if current_section == "swiss" else foreign_data
                    target[code] = float(value)
                    break

        for code in sorted(set(list(swiss_data.keys()) + list(foreign_data.keys()))):
            total = swiss_data.get(code, 0) + foreign_data.get(code, 0)
            de_label = [k for k, v in ISCO1_DE.items() if v == code]
            total_rows.append({
                "isco1": code,
                "label_de": de_label[0] if de_label else f"ISCO {code}",
                "employment_thousands": round(total, 1),
            })

    if not total_rows:
        print("  ERROR: Could not extract employment data.")
        return pd.DataFrame()

    output = pd.DataFrame(total_rows)
    output["country"] = "CH"
    output["year"] = latest_year
    output["source"] = "BFS"

    print(f"\n  Parsed {len(output)} ISCO 1-digit groups (year: {latest_year})")
    total = output["employment_thousands"].sum()
    print(f"  Total employment: {total:,.1f}k ({total/1000:.1f}M)")
    for _, row in output.iterrows():
        print(f"    ISCO {row['isco1']}: {row['employment_thousands']:>8,.1f}k  {row['label_de'][:50]}")

    return output


def parse_wages() -> pd.DataFrame:
    """Parse je-d-03.04.01.02.47.xlsx — monthly median gross wages by CH-ISCO-19.

    Structure (sheet: 2024):
      Row 0-6: headers/metadata
      Row 7: TOTAL row
      Row 8+: ISCO groups — col 0 has code, col 1 has label, col 3 has Total wage

    Wages are monthly gross median in CHF. We convert to annual.
    """
    wage_file = BFS_DIR / "je-d-03.04.01.02.47.xlsx"
    if not wage_file.exists():
        print(f"  Wage file not found: {wage_file}")
        print("  Download from: https://www.bfs.admin.ch → Arbeit und Erwerb → Löhne")
        return pd.DataFrame()

    # Try latest year sheet first
    print(f"\n--- Parsing wages: {wage_file.name} ---")
    xl = pd.ExcelFile(wage_file)
    year_sheets = [s for s in xl.sheet_names if s.isdigit()]
    target_sheet = max(year_sheets) if year_sheets else xl.sheet_names[1]
    wage_year = int(target_sheet) if target_sheet.isdigit() else 2024

    print(f"  Using sheet: {target_sheet}")
    df = pd.read_excel(wage_file, sheet_name=target_sheet, header=None)
    print(f"  Shape: {df.shape}")

    # Find the wage data rows: col 0 = ISCO code, col 1 = label, col 3 = Total wage
    # The structure has col 4 = "Berufsgruppen nach CH-ISCO-19" header row
    # Data starts after the header rows (around row 7-8)

    rows = []
    for i in range(7, len(df)):
        code_val = df.iloc[i, 0]
        label_val = df.iloc[i, 1]
        wage_val = df.iloc[i, 3]  # "Total" column

        if pd.isna(code_val) and pd.isna(label_val):
            continue

        code_str = str(code_val).strip() if pd.notna(code_val) else ""
        label_str = str(label_val).strip() if pd.notna(label_val) else ""

        # Skip non-ISCO rows
        if not re.match(r"^\d{1,2}$", code_str):
            continue

        # Parse wage — handle '*' (suppressed) and '[x]' (uncertain) markers
        wage_str = str(wage_val).strip() if pd.notna(wage_val) else ""
        wage_str = wage_str.replace("[", "").replace("]", "").strip()
        if wage_str == "*" or wage_str == "" or wage_str == "…":
            continue

        try:
            monthly_chf = float(wage_str)
        except ValueError:
            continue

        rows.append({
            "isco_code": code_str,
            "isco_digits": len(code_str),
            "label_de": label_str[:60],
            "monthly_median_chf": monthly_chf,
        })

    if not rows:
        print("  ERROR: Could not extract wage data.")
        return pd.DataFrame()

    result = pd.DataFrame(rows)

    # Convert monthly → annual (× 12 + 13th month salary common in CH = × 13)
    # BFS data is standardised monthly, use × 12 for comparability with Eurostat
    result["mean_annual_chf"] = (result["monthly_median_chf"] * 12).round(0)

    # Convert CHF → EUR
    CHF_EUR_RATE = 0.96  # ~1 CHF ≈ 0.96 EUR (2022-2024 average)
    result["mean_annual_eur"] = (result["mean_annual_chf"] * CHF_EUR_RATE).round(0)

    result["country"] = "CH"
    result["year"] = wage_year
    result["source"] = "BFS"

    # Separate 1-digit (major group) and 2-digit (sub-major group)
    isco1 = result[result["isco_digits"] == 1].copy()
    isco2 = result[result["isco_digits"] == 2].copy()

    print(f"\n  Parsed {len(isco1)} ISCO 1-digit + {len(isco2)} ISCO 2-digit groups (year: {wage_year})")
    print(f"\n  ISCO 1-digit wages:")
    for _, row in isco1.iterrows():
        print(f"    ISCO {row['isco_code']}: {row['monthly_median_chf']:>7,.0f} CHF/mo → {row['mean_annual_chf']:>9,.0f} CHF/yr ({row['mean_annual_eur']:>9,.0f} EUR)  {row['label_de']}")
    print(f"\n  ISCO 2-digit wages ({len(isco2)} groups):")
    for _, row in isco2.iterrows():
        print(f"    ISCO {row['isco_code']:>2}: {row['monthly_median_chf']:>7,.0f} CHF/mo → {row['mean_annual_chf']:>9,.0f} CHF/yr  {row['label_de']}")

    # Output: include both levels
    output = result[["isco_code", "isco_digits", "monthly_median_chf",
                      "mean_annual_chf", "mean_annual_eur", "country", "year", "source"]].copy()
    return output


def main():
    if not BFS_DIR.exists():
        print(f"Directory {BFS_DIR} does not exist.")
        print("Please create it and place BFS data files there.")
        sys.exit(1)

    emp = parse_employment()
    if not emp.empty:
        emp.to_csv(OUT_EMP, index=False)
        print(f"\n  Saved: {OUT_EMP}")

    wages = parse_wages()
    if not wages.empty:
        wages.to_csv(OUT_WAGE, index=False)
        print(f"\n  Saved: {OUT_WAGE}")

    print("\nDone.")


if __name__ == "__main__":
    main()
