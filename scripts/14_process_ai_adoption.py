"""
14_process_ai_adoption.py — Process Eurostat AI adoption by enterprise (isoc_eb_ai).

Reads the bulk CSV downloaded from Eurostat, filters for the headline indicator
(E_AI_TANY = enterprises using at least one AI technology) across all size classes
(GE10 = 10+ employees), and produces a clean JSON per-country time series.

Input:  data/eurostat/ai_adoption_enterprise.csv
Output: data/eurostat/ai_adoption_processed.json

Structure:
{
  "source": "Eurostat isoc_eb_ai",
  "indicator": "E_AI_TANY — Enterprises using at least one AI technology (% of enterprises with 10+ employees)",
  "countries": {
    "AT": { "name": "Austria", "series": { "2021": 9.5, "2023": 13.2, "2024": 15.1, "2025": 19.8 } },
    ...
  }
}
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "eurostat" / "ai_adoption_enterprise.csv"
OUTPUT = ROOT / "data" / "eurostat" / "ai_adoption_processed.json"

# Target: headline AI adoption indicator, all enterprises 10+
TARGET_INDICATOR = "E_AI_TANY"
TARGET_SIZE = "GE10"

# Eurostat geo codes → ISO 2-letter (map EL→GR for consistency with site)
GEO_REMAP = {"EL": "GR"}

COUNTRY_NAMES = {
    "AL": "Albania", "AT": "Austria", "BA": "Bosnia and Herzegovina",
    "BE": "Belgium", "BG": "Bulgaria", "CY": "Cyprus", "CZ": "Czechia",
    "DE": "Germany", "DK": "Denmark", "EE": "Estonia", "GR": "Greece",
    "ES": "Spain", "FI": "Finland", "FR": "France", "HR": "Croatia",
    "HU": "Hungary", "IE": "Ireland", "IT": "Italy", "LT": "Lithuania",
    "LU": "Luxembourg", "LV": "Latvia", "ME": "Montenegro",
    "MK": "North Macedonia", "MT": "Malta", "NL": "Netherlands",
    "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia", "SK": "Slovakia",
    "TR": "Turkey",
}

# Skip aggregates
SKIP_GEOS = {"EU27_2020", "EA"}


def main():
    countries = {}

    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        # Column indices (paired code+name columns):
        # 5=size_emp code, 9=indic_is code, 13=geo code, 15=TIME_PERIOD, 17=OBS_VALUE
        for row in reader:
            size_code = row[5]
            indic_code = row[9]
            geo_code = row[13]
            year = row[15]
            obs_value = row[17]

            if indic_code != TARGET_INDICATOR:
                continue
            if size_code != TARGET_SIZE:
                continue
            if geo_code in SKIP_GEOS:
                continue
            if not obs_value or obs_value.strip() == "":
                continue

            geo = GEO_REMAP.get(geo_code, geo_code)
            value = round(float(obs_value), 2)

            if geo not in countries:
                countries[geo] = {"name": COUNTRY_NAMES.get(geo, geo), "series": {}}
            countries[geo]["series"][year] = value

    # Sort countries and years
    result = {
        "source": "Eurostat isoc_eb_ai",
        "indicator": "E_AI_TANY — Enterprises using at least one AI technology (% of enterprises with 10+ employees)",
        "unit": "percentage",
        "countries": {},
    }

    for geo in sorted(countries.keys()):
        entry = countries[geo]
        entry["series"] = dict(sorted(entry["series"].items()))
        # Add latest value as top-level for easy access
        years = sorted(entry["series"].keys())
        if years:
            entry["latest_year"] = years[-1]
            entry["latest_value"] = entry["series"][years[-1]]
        result["countries"][geo] = entry

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✓ Processed {len(result['countries'])} countries")
    # Print a summary table
    print(f"\n{'Country':<25} {'2021':>6} {'2023':>6} {'2024':>6} {'2025':>6}")
    print("-" * 55)
    for geo, data in sorted(result["countries"].items(), key=lambda x: -(x[1].get("latest_value", 0))):
        s = data["series"]
        print(f"{data['name']:<25} {s.get('2021', ''):>6} {s.get('2023', ''):>6} {s.get('2024', ''):>6} {s.get('2025', ''):>6}")


if __name__ == "__main__":
    main()
