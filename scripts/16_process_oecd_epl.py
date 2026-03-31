"""
16_process_oecd_epl.py — Process OECD Employment Protection Legislation scores.

Reads the OECD EPL CSV (EPL_OV indicator, Version 4, 0-6 scale).
Produces clean JSON with per-country latest EPL score.

Input:  data/oecd/epl_score.csv
Output: data/oecd/epl_processed.json

Structure:
{
  "source": "OECD EPL",
  "indicator": "Strictness of employment protection — individual and collective dismissals (regular contracts)",
  "scale": "0-6 (higher = stricter)",
  "countries": {
    "AT": { "name": "Austria", "score": 1.80, "year": 2017 },
    ...
  }
}
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "oecd" / "epl_score.csv"
OUTPUT = ROOT / "data" / "oecd" / "epl_processed.json"

# OECD uses ISO 3-letter → map to 2-letter
ISO3_TO_ISO2 = {
    "AUS": "AU", "AUT": "AT", "BEL": "BE", "CAN": "CA", "CHL": "CL",
    "COL": "CO", "CRI": "CR", "CZE": "CZ", "DEU": "DE", "DNK": "DK",
    "ESP": "ES", "EST": "EE", "FIN": "FI", "FRA": "FR", "GBR": "UK",
    "GRC": "GR", "HUN": "HU", "IRL": "IE", "ISL": "IS", "ISR": "IL",
    "ITA": "IT", "JPN": "JP", "KOR": "KR", "LTU": "LT", "LUX": "LU",
    "LVA": "LV", "MEX": "MX", "NLD": "NL", "NOR": "NO", "NZL": "NZ",
    "POL": "PL", "PRT": "PT", "SVK": "SK", "SVN": "SI", "SWE": "SE",
    "TUR": "TR", "USA": "US",
}

COUNTRY_NAMES = {
    "AU": "Australia", "AT": "Austria", "BE": "Belgium", "CA": "Canada",
    "CL": "Chile", "CO": "Colombia", "CR": "Costa Rica", "CZ": "Czechia",
    "DE": "Germany", "DK": "Denmark", "EE": "Estonia", "ES": "Spain",
    "FI": "Finland", "FR": "France", "UK": "United Kingdom", "GR": "Greece",
    "HU": "Hungary", "IE": "Ireland", "IS": "Iceland", "IL": "Israel",
    "IT": "Italy", "JP": "Japan", "KR": "South Korea", "LT": "Lithuania",
    "LU": "Luxembourg", "LV": "Latvia", "MX": "Mexico", "NL": "Netherlands",
    "NO": "Norway", "NZ": "New Zealand", "PL": "Poland", "PT": "Portugal",
    "SK": "Slovakia", "SI": "Slovenia", "SE": "Sweden", "TR": "Turkey",
    "US": "United States",
}

# European countries we care about
EUROPEAN_GEOS = {
    "AT", "BE", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR",
    "HU", "IE", "IS", "IT", "LT", "LU", "LV", "NL", "NO", "PL",
    "PT", "SE", "SI", "SK", "TR", "UK",
}


def main():
    # Collect all entries, keep latest year per country
    raw = {}

    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        # Columns: 6=REF_AREA (ISO3), 14=TIME_PERIOD, 16=OBS_VALUE
        for row in reader:
            iso3 = row[6]
            year = int(row[14])
            obs_value = row[16]

            if not obs_value or obs_value.strip() == "":
                continue

            iso2 = ISO3_TO_ISO2.get(iso3)
            if not iso2:
                continue

            score = round(float(obs_value), 2)

            if iso2 not in raw or year > raw[iso2]["year"]:
                raw[iso2] = {"score": score, "year": year}

    result = {
        "source": "OECD EPL",
        "indicator": "Strictness of employment protection — individual and collective dismissals (regular contracts)",
        "scale": "0-6 (higher = stricter)",
        "version": "Version 4 (2013-2019)",
        "countries": {},
    }

    for geo in sorted(raw.keys()):
        entry = raw[geo]
        result["countries"][geo] = {
            "name": COUNTRY_NAMES.get(geo, geo),
            "score": entry["score"],
            "year": entry["year"],
        }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    # Print European countries sorted by strictness
    print(f"✓ Processed {len(result['countries'])} countries ({sum(1 for g in result['countries'] if g in EUROPEAN_GEOS)} European)")
    print(f"\n{'Country':<25} {'EPL Score':>10} {'Year':>5}")
    print("-" * 45)
    for geo, data in sorted(result["countries"].items(), key=lambda x: -x[1]["score"]):
        marker = " *" if geo in EUROPEAN_GEOS else ""
        print(f"{data['name']:<25} {data['score']:>10.2f} {data['year']:>5}{marker}")


if __name__ == "__main__":
    main()
