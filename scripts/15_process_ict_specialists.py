"""
15_process_ict_specialists.py — Process Eurostat ICT specialists (isoc_sks_itspt).

Reads the bulk CSV and produces a clean JSON with per-country time series of
ICT specialists as % of total employment.

Input:  data/eurostat/ict_specialists.csv
Output: data/eurostat/ict_specialists_processed.json

Structure:
{
  "source": "Eurostat isoc_sks_itspt",
  "indicator": "ICT specialists as % of total employment",
  "countries": {
    "AT": { "name": "Austria", "series": { "2015": 4.0, ..., "2024": 5.3 } },
    ...
  }
}
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "eurostat" / "ict_specialists.csv"
OUTPUT = ROOT / "data" / "eurostat" / "ict_specialists_processed.json"

GEO_REMAP = {"EL": "GR"}

COUNTRY_NAMES = {
    "AL": "Albania", "AT": "Austria", "BA": "Bosnia and Herzegovina",
    "BE": "Belgium", "BG": "Bulgaria", "CY": "Cyprus", "CZ": "Czechia",
    "DE": "Germany", "DK": "Denmark", "EE": "Estonia", "GR": "Greece",
    "ES": "Spain", "FI": "Finland", "FR": "France", "HR": "Croatia",
    "HU": "Hungary", "IE": "Ireland", "IS": "Iceland", "IT": "Italy",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia",
    "ME": "Montenegro", "MK": "North Macedonia", "MT": "Malta",
    "NL": "Netherlands", "NO": "Norway", "PL": "Poland", "PT": "Portugal",
    "RO": "Romania", "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia",
    "SK": "Slovakia", "TR": "Turkey", "UK": "United Kingdom",
    "CH": "Switzerland",
}

SKIP_GEOS = {"EU27_2020", "EU28", "EA", "EA19", "EA20"}

# We want percentage of employment, not absolute thousands
TARGET_UNIT = "PC_EMP"


def main():
    countries = {}

    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        # Columns: 5=unit code, 7=geo code, 9=TIME_PERIOD, 11=OBS_VALUE
        for row in reader:
            unit_code = row[5]
            geo_code = row[7]
            year = row[9]
            obs_value = row[11]

            if unit_code != TARGET_UNIT:
                continue
            if geo_code in SKIP_GEOS:
                continue
            if not obs_value or obs_value.strip() == "":
                continue

            geo = GEO_REMAP.get(geo_code, geo_code)
            value = round(float(obs_value), 1)

            if geo not in countries:
                countries[geo] = {"name": COUNTRY_NAMES.get(geo, geo), "series": {}}
            countries[geo]["series"][year] = value

    result = {
        "source": "Eurostat isoc_sks_itspt",
        "indicator": "ICT specialists as % of total employment",
        "unit": "percentage",
        "countries": {},
    }

    for geo in sorted(countries.keys()):
        entry = countries[geo]
        entry["series"] = dict(sorted(entry["series"].items()))
        years = sorted(entry["series"].keys())
        if years:
            entry["latest_year"] = years[-1]
            entry["latest_value"] = entry["series"][years[-1]]
            # Compute 5-year change if possible
            five_ago = str(int(years[-1]) - 5)
            if five_ago in entry["series"]:
                entry["change_5y"] = round(entry["series"][years[-1]] - entry["series"][five_ago], 1)
        result["countries"][geo] = entry

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✓ Processed {len(result['countries'])} countries")
    print(f"\n{'Country':<25} {'Latest':>7} {'Year':>5} {'5y Δ':>5}")
    print("-" * 45)
    for geo, data in sorted(result["countries"].items(), key=lambda x: -(x[1].get("latest_value", 0))):
        chg = data.get("change_5y", "")
        if isinstance(chg, (int, float)):
            chg = f"+{chg}" if chg > 0 else str(chg)
        print(f"{data['name']:<25} {data.get('latest_value', ''):>7} {data.get('latest_year', ''):>5} {chg:>5}")


if __name__ == "__main__":
    main()
