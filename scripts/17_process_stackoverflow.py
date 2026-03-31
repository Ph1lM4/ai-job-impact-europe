#!/usr/bin/env python3
"""
Process Stack Overflow Developer Survey 2025 for European job market data.
Extracts per-country: median salary (USD), remote %, AI threat sentiment,
IC vs PM split, developer type distribution. European countries only.

Source: Stack Overflow Developer Survey 2025 (49,191 respondents, 15,752 European)
Output: data/stackoverflow/so_europe_processed.json
"""

import csv
import json
import sys
import os
from collections import defaultdict
from statistics import median

csv.field_size_limit(sys.maxsize)

# European country mapping (SO country name -> ISO2)
EUROPEAN_COUNTRIES = {
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Czech Republic": "CZ",
    "Czechia": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Iceland": "IS",
    "Ireland": "IE",
    "Italy": "IT",
    "Latvia": "LV",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Netherlands": "NL",
    "Norway": "NO",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Serbia": "RS",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Ukraine": "UA",
    "United Kingdom of Great Britain and Northern Ireland": "GB",
}

INPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "research", "stack-overflow-developer-survey-2025", "survey_results_public.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "stackoverflow")
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "so_europe_processed.json")


def parse_salary(val):
    """Parse ConvertedCompYearly (USD) - filter outliers."""
    if not val or val.strip() == "":
        return None
    try:
        s = float(val)
        # Filter: $1K-$500K range (removes noise/joke entries)
        if 1000 <= s <= 500000:
            return s
    except ValueError:
        pass
    return None


def parse_ai_threat(val):
    """Parse AIThreat column."""
    if not val:
        return None
    val = val.strip()
    threat_map = {
        "No, I don't think AI is a threat to my job": "no_threat",
        "I'm not sure": "unsure",
        "Yes, I think AI is a threat to my job": "threat",
    }
    # Partial matching for varying text
    val_lower = val.lower()
    if "not" in val_lower and "threat" in val_lower:
        return "no_threat"
    if "not sure" in val_lower or "unsure" in val_lower:
        return "unsure"
    if "yes" in val_lower or ("threat" in val_lower and "not" not in val_lower):
        return "threat"
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Accumulators per country
    countries = defaultdict(lambda: {
        "respondents": 0,
        "salaries_usd": [],
        "remote": defaultdict(int),
        "ai_threat": defaultdict(int),
        "ic_pm": defaultdict(int),
        "dev_types": defaultdict(int),
        "ai_tool_users": 0,
        "job_sat": defaultdict(int),
    })

    total = 0
    european = 0

    with open(INPUT_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            country_name = row.get("Country", "").strip()
            if country_name not in EUROPEAN_COUNTRIES:
                continue

            iso2 = EUROPEAN_COUNTRIES[country_name]
            c = countries[iso2]
            c["respondents"] += 1
            c["country_name"] = country_name
            european += 1

            # Salary
            salary = parse_salary(row.get("ConvertedCompYearly", ""))
            if salary:
                c["salaries_usd"].append(salary)

            # Remote work
            remote_val = row.get("RemoteWork", "").strip()
            if remote_val:
                c["remote"][remote_val] += 1

            # AI Threat
            threat = parse_ai_threat(row.get("AIThreat", ""))
            if threat:
                c["ai_threat"][threat] += 1

            # IC vs PM
            ic_pm = row.get("ICorPM", "").strip()
            if ic_pm:
                c["ic_pm"][ic_pm] += 1

            # Dev Type (can be semicolon-separated)
            dev_type = row.get("DevType", "").strip()
            if dev_type:
                for dt in dev_type.split(";"):
                    dt = dt.strip()
                    if dt:
                        c["dev_types"][dt] += 1

            # AI tool usage (check AISelect)
            ai_select = row.get("AISelect", "").strip()
            if ai_select and "yes" in ai_select.lower():
                c["ai_tool_users"] += 1

            # Job satisfaction
            job_sat = row.get("JobSat", "").strip()
            if job_sat:
                c["job_sat"][job_sat] += 1

    # Build output
    result = {
        "source": "Stack Overflow Developer Survey 2025",
        "methodology": "Annual survey, 49,191 respondents globally, self-selected sample",
        "total_respondents": total,
        "european_respondents": european,
        "salary_unit": "USD (converted by SO using purchasing power parity)",
        "countries": {}
    }

    for iso2, data in sorted(countries.items(), key=lambda x: x[1]["respondents"], reverse=True):
        n = data["respondents"]
        if n < 50:  # Skip countries with tiny samples
            continue

        entry = {
            "name": data["country_name"],
            "respondents": n,
        }

        # Salary
        if data["salaries_usd"]:
            salaries = sorted(data["salaries_usd"])
            entry["salary_usd"] = {
                "median": round(median(salaries)),
                "p25": round(salaries[len(salaries) // 4]),
                "p75": round(salaries[3 * len(salaries) // 4]),
                "n": len(salaries),
            }

        # Remote work
        if data["remote"]:
            total_remote = sum(data["remote"].values())
            remote_pcts = {}
            for k, v in sorted(data["remote"].items(), key=lambda x: -x[1]):
                remote_pcts[k] = round(v / total_remote, 3)
            entry["remote_work"] = remote_pcts

        # AI Threat
        if data["ai_threat"]:
            total_threat = sum(data["ai_threat"].values())
            entry["ai_threat"] = {
                k: round(v / total_threat, 3)
                for k, v in data["ai_threat"].items()
            }
            entry["ai_threat"]["n"] = total_threat

        # IC vs PM
        if data["ic_pm"]:
            total_icpm = sum(data["ic_pm"].values())
            entry["ic_vs_pm"] = {
                k: round(v / total_icpm, 3)
                for k, v in data["ic_pm"].items()
            }

        # Top 10 dev types
        if data["dev_types"]:
            top_types = sorted(data["dev_types"].items(), key=lambda x: -x[1])[:10]
            total_devtype_responses = sum(data["dev_types"].values())
            entry["top_dev_types"] = [
                {"type": t, "count": c, "pct": round(c / n, 3)}
                for t, c in top_types
            ]

        # AI tool usage rate
        entry["ai_tool_usage_pct"] = round(data["ai_tool_users"] / n, 3)

        # Job satisfaction
        if data["job_sat"]:
            total_sat = sum(data["job_sat"].values())
            entry["job_satisfaction"] = {
                k: round(v / total_sat, 3)
                for k, v in sorted(data["job_sat"].items(), key=lambda x: -x[1])
            }

        result["countries"][iso2] = entry

    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Processed {european} European respondents from {total} total")
    print(f"Countries with 50+ respondents: {len(result['countries'])}")
    for iso2, data in sorted(result["countries"].items(), key=lambda x: -x[1]["respondents"]):
        sal = data.get("salary_usd", {}).get("median", "N/A")
        print(f"  {iso2} ({data['name']}): n={data['respondents']}, median_salary=${sal}")


if __name__ == "__main__":
    main()
