"""
12_compute_layers.py — Compute normalized layer scores for multi-layer treemap.

Layers:
  - Pay: percentile-ranked within each country, 0-10 scale (Sprint 1)
  - Growth: weighted blend of Eurostat YoY + Cedefop CAGR, normalized 0-10 (Sprint 2)
  - Adoption: triangulated from Anthropic + Microsoft + OpenAI, 0-10 (Sprint 2.5)
  Future: education, augmentation

Input:  occupations_by_country.csv, occupations.csv,
        data/cedefop/growth_forecast.csv, data/eurostat/employment_yoy.csv,
        data/adoption/triangulated_adoption.csv,
        data/eurostat/education_by_occupation.csv
Output: data/layer_scores.json
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_COUNTRY = ROOT / "occupations_by_country.csv"
INPUT_META = ROOT / "occupations.csv"
INPUT_CEDEFOP = ROOT / "data" / "cedefop" / "growth_forecast.csv"
INPUT_EUROSTAT_YOY = ROOT / "data" / "eurostat" / "employment_yoy.csv"
INPUT_ADOPTION = ROOT / "data" / "adoption" / "triangulated_adoption.csv"
INPUT_EDUCATION = ROOT / "data" / "eurostat" / "education_by_occupation.csv"
INPUT_SCORES = ROOT / "scores.json"
OUTPUT = ROOT / "data" / "layer_scores.json"

# EU-27 member states for computing EU27 aggregate
EU27_MEMBERS = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL",
    "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK",
    "SI", "ES", "SE",
}

# Growth blend weights
WEIGHT_EUROSTAT_YOY = 0.4
WEIGHT_CEDEFOP_CAGR = 0.6

# Augmentation composite weights
AUG_W_EXPOSURE = 0.5
AUG_W_GROWTH = 0.3
AUG_W_EDUCATION = 0.2


def compute_pay_scores(df: pd.DataFrame) -> dict:
    """Compute pay_score (0-10) per isco3 × country using within-country percentile ranking."""
    layer = {}  # {isco3: {"pay_score": {country: score}, "pay_eur": {country: amount}}}

    # Initialize all isco3 entries
    all_isco3 = sorted(df["isco3"].unique())
    for isco3 in all_isco3:
        layer[isco3] = {"pay_score": {}, "pay_eur": {}}

    # Compute per-country percentile ranks
    countries = sorted(df["country"].unique())
    for country in countries:
        cdf = df[df["country"] == country].dropna(subset=["mean_annual_wage_eur"])
        if len(cdf) < 2:
            continue

        # Percentile rank: 0 = lowest wage, 1 = highest wage
        cdf = cdf.copy()
        cdf["pct_rank"] = cdf["mean_annual_wage_eur"].rank(pct=True)
        cdf["pay_score"] = (cdf["pct_rank"] * 10).round(1).clip(0, 10)

        for _, row in cdf.iterrows():
            isco3 = row["isco3"]
            if isco3 in layer:
                layer[isco3]["pay_score"][country] = float(row["pay_score"])
                layer[isco3]["pay_eur"][country] = round(float(row["mean_annual_wage_eur"]))

    # Compute EU27 aggregate: employment-weighted average of member states' pay scores
    for isco3 in all_isco3:
        eu_scores = []
        eu_weights = []
        idf = df[(df["isco3"] == isco3) & (df["country"].isin(EU27_MEMBERS))]
        for _, row in idf.iterrows():
            country = row["country"]
            score = layer[isco3]["pay_score"].get(country)
            emp = row["employment_thousands"] if pd.notna(row["employment_thousands"]) else 0
            if score is not None and emp > 0:
                eu_scores.append(score)
                eu_weights.append(emp)
        if eu_scores:
            weighted_avg = np.average(eu_scores, weights=eu_weights)
            layer[isco3]["pay_score"]["EU27"] = round(float(weighted_avg), 1)
        # EU27 wage: employment-weighted average
        eu_wages = []
        eu_wage_weights = []
        for _, row in idf.iterrows():
            country = row["country"]
            wage = layer[isco3]["pay_eur"].get(country)
            emp = row["employment_thousands"] if pd.notna(row["employment_thousands"]) else 0
            if wage is not None and emp > 0:
                eu_wages.append(wage)
                eu_wage_weights.append(emp)
        if eu_wages:
            layer[isco3]["pay_eur"]["EU27"] = round(float(np.average(eu_wages, weights=eu_wage_weights)))

    return layer


def compute_growth_scores(meta: pd.DataFrame) -> dict:
    """Compute growth_score (0-10) per isco3 × country.

    Blends Eurostat YoY (short-term, 0.4 weight) with Cedefop CAGR (long-term, 0.6 weight).
    Growth data is at ISCO 1-digit — all child 3-digit groups inherit their parent's score.
    Normalization: within-country z-scores mapped to 0-10 via min-max.
    """
    # Build ISCO 3-digit → 1-digit mapping
    isco3_to_isco1 = dict(zip(meta["isco3"], meta["isco1"]))
    all_isco3 = sorted(meta["isco3"].unique())

    # Load data sources
    cedefop = None
    if INPUT_CEDEFOP.exists():
        cedefop = pd.read_csv(INPUT_CEDEFOP, dtype={"isco1": str})
        print(f"  Cedefop: {len(cedefop)} rows")
    else:
        print("  Cedefop: not available, using Eurostat YoY only")

    eurostat_yoy = None
    if INPUT_EUROSTAT_YOY.exists():
        eurostat_yoy = pd.read_csv(INPUT_EUROSTAT_YOY, dtype={"isco2": str, "isco1": str})
        # Aggregate to ISCO 1-digit × country (employment-weighted)
        agg_rows = []
        for (isco1, country), grp in eurostat_yoy.groupby(["isco1", "country"]):
            total_emp = grp["emp_y2"].sum()
            if total_emp > 0:
                weighted_yoy = (grp["yoy_pct"] * grp["emp_y2"]).sum() / total_emp
            else:
                weighted_yoy = 0
            agg_rows.append({"isco1": isco1, "country": country, "yoy_pct": round(weighted_yoy, 2)})
        eurostat_agg = pd.DataFrame(agg_rows)
        print(f"  Eurostat YoY: {len(eurostat_agg)} rows (aggregated to ISCO 1-digit)")
    else:
        eurostat_agg = None
        print("  Eurostat YoY: not available")

    if cedefop is None and eurostat_agg is None:
        print("  WARNING: No growth data available")
        return {}

    # Build raw growth values at ISCO 1-digit × country level
    # Key: (isco1, country) → {"yoy": float|None, "cagr": float|None}
    raw_growth = {}

    if eurostat_agg is not None:
        for _, row in eurostat_agg.iterrows():
            key = (row["isco1"], row["country"])
            if key not in raw_growth:
                raw_growth[key] = {"yoy": None, "cagr": None}
            raw_growth[key]["yoy"] = row["yoy_pct"]

    if cedefop is not None:
        for _, row in cedefop.iterrows():
            key = (row["isco1"], row["country"])
            if key not in raw_growth:
                raw_growth[key] = {"yoy": None, "cagr": None}
            raw_growth[key]["cagr"] = row["cagr_pct"]

    # Compute blended z-score per country
    # Group by country, compute z-scores within country, then blend
    country_data = {}  # {country: [(isco1, yoy, cagr), ...]}
    for (isco1, country), vals in raw_growth.items():
        if country not in country_data:
            country_data[country] = []
        country_data[country].append((isco1, vals["yoy"], vals["cagr"]))

    # Result: {isco1: {"growth_score": {country: score}, "growth_yoy_pct": {country: pct}, "cedefop_cagr_pct": {country: pct}}}
    isco1_scores = {}

    for country, entries in country_data.items():
        yoys = [(e[0], e[1]) for e in entries if e[1] is not None]
        cagrs = [(e[0], e[2]) for e in entries if e[2] is not None]

        # Compute z-scores within country
        yoy_z = {}
        if len(yoys) >= 2:
            vals = np.array([v for _, v in yoys])
            z = (vals - vals.mean()) / (vals.std() if vals.std() > 0 else 1)
            for (isco1, _), zs in zip(yoys, z):
                yoy_z[isco1] = float(zs)

        cagr_z = {}
        if len(cagrs) >= 2:
            vals = np.array([v for _, v in cagrs])
            z = (vals - vals.mean()) / (vals.std() if vals.std() > 0 else 1)
            for (isco1, _), zs in zip(cagrs, z):
                cagr_z[isco1] = float(zs)

        # Blend z-scores
        all_isco1_in_country = set(e[0] for e in entries)
        blended = {}
        for isco1 in all_isco1_in_country:
            has_yoy = isco1 in yoy_z
            has_cagr = isco1 in cagr_z
            if has_yoy and has_cagr:
                blended[isco1] = WEIGHT_EUROSTAT_YOY * yoy_z[isco1] + WEIGHT_CEDEFOP_CAGR * cagr_z[isco1]
            elif has_yoy:
                blended[isco1] = yoy_z[isco1]
            elif has_cagr:
                blended[isco1] = cagr_z[isco1]

        if not blended:
            continue

        # Min-max normalize blended z-scores to 0-10 within country
        z_vals = np.array(list(blended.values()))
        z_min, z_max = z_vals.min(), z_vals.max()
        spread = z_max - z_min
        if spread < 1e-6:
            spread = 1.0  # all same → map to 5.0

        for isco1, z in blended.items():
            score = ((z - z_min) / spread) * 10
            score = round(max(0, min(10, score)), 1)

            if isco1 not in isco1_scores:
                isco1_scores[isco1] = {"growth_score": {}, "growth_yoy_pct": {}, "cedefop_cagr_pct": {}}

            isco1_scores[isco1]["growth_score"][country] = score

            # Store raw values for tooltip display
            raw = raw_growth.get((isco1, country), {})
            if raw.get("yoy") is not None:
                isco1_scores[isco1]["growth_yoy_pct"][country] = round(raw["yoy"], 2)
            if raw.get("cagr") is not None:
                isco1_scores[isco1]["cedefop_cagr_pct"][country] = round(raw["cagr"], 2)

    # Propagate ISCO 1-digit scores to all child 3-digit groups
    layer = {}
    for isco3 in all_isco3:
        isco1 = isco3_to_isco1.get(isco3)
        if isco1 and isco1 in isco1_scores:
            layer[isco3] = {
                "growth_score": dict(isco1_scores[isco1]["growth_score"]),
                "growth_yoy_pct": dict(isco1_scores[isco1]["growth_yoy_pct"]),
                "cedefop_cagr_pct": dict(isco1_scores[isco1]["cedefop_cagr_pct"]),
            }
        else:
            layer[isco3] = {"growth_score": {}, "growth_yoy_pct": {}, "cedefop_cagr_pct": {}}

    return layer


def compute_adoption_scores(meta: pd.DataFrame) -> dict:
    """Compute adoption_score (0-10) per isco3.

    Adoption data is US-based (occupation-level, not country-level).
    All countries get the same score per occupation group.
    Scores are derived from triangulated observed usage (Anthropic + Microsoft)
    normalized to 0-10.
    """
    isco3_to_isco1 = dict(zip(meta["isco3"], meta["isco1"]))
    all_isco3 = sorted(meta["isco3"].unique())

    if not INPUT_ADOPTION.exists():
        print("  WARNING: Adoption data not found, run 13_fetch_adoption_data.py first")
        return {}

    adoption = pd.read_csv(INPUT_ADOPTION, dtype={"isco1": str})
    print(f"  Loaded: {len(adoption)} ISCO 1-digit groups")

    # Build ISCO 1-digit score lookup
    isco1_data = {}
    for _, row in adoption.iterrows():
        isco1 = row["isco1"]
        # Scale observed_usage (0-1) to 0-10
        obs = row.get("observed_usage")
        theo = row.get("theoretical_ceiling")
        gap = row.get("adoption_gap")
        anth = row.get("anthropic_observed")
        ms = row.get("microsoft_applicability")
        oai = row.get("openai_theoretical")

        adoption_score = round(float(obs) * 10, 1) if pd.notna(obs) else None

        isco1_data[isco1] = {
            "adoption_score": adoption_score,
            "observed_usage": round(float(obs), 3) if pd.notna(obs) else None,
            "theoretical_ceiling": round(float(theo), 3) if pd.notna(theo) else None,
            "adoption_gap": round(float(gap), 3) if pd.notna(gap) else None,
            "anthropic_observed": round(float(anth), 3) if pd.notna(anth) else None,
            "microsoft_applicability": round(float(ms), 3) if pd.notna(ms) else None,
            "openai_theoretical": round(float(oai), 3) if pd.notna(oai) else None,
        }

    # Propagate ISCO 1-digit → 3-digit (same score for all children)
    # Adoption is NOT per-country — it's a global (US-based) estimate
    layer = {}
    for isco3 in all_isco3:
        isco1 = isco3_to_isco1.get(isco3)
        if isco1 and isco1 in isco1_data:
            data = isco1_data[isco1]
            layer[isco3] = {
                "adoption_score": data["adoption_score"],
                "observed_usage": data["observed_usage"],
                "theoretical_ceiling": data["theoretical_ceiling"],
                "adoption_gap": data["adoption_gap"],
            }
        else:
            layer[isco3] = {
                "adoption_score": None,
                "observed_usage": None,
                "theoretical_ceiling": None,
                "adoption_gap": None,
            }

    return layer


def compute_education_scores(meta: pd.DataFrame) -> dict:
    """Compute education_score (0-10) per isco3 × country.

    Education data is at ISCO 1-digit × country — all child 3-digit groups
    inherit their parent's score. Score = pct_high_ed rescaled 0-10 within country.
    """
    isco3_to_isco1 = dict(zip(meta["isco3"], meta["isco1"]))
    all_isco3 = sorted(meta["isco3"].unique())

    if not INPUT_EDUCATION.exists():
        print("  WARNING: Education data not found, run 11_fetch_education.py first")
        return {}

    edu = pd.read_csv(INPUT_EDUCATION, dtype={"isco1": str})
    print(f"  Loaded: {len(edu)} rows ({edu['country'].nunique()} countries × {edu['isco1'].nunique()} ISCO groups)")

    # Build ISCO 1-digit lookup: {isco1: {"education_score": {country: score}, "pct_tertiary": {country: pct}}}
    isco1_scores = {}
    for _, row in edu.iterrows():
        isco1 = row["isco1"]
        country = row["country"]
        if isco1 not in isco1_scores:
            isco1_scores[isco1] = {"education_score": {}, "pct_tertiary": {}}
        isco1_scores[isco1]["education_score"][country] = float(row["ed_score"])
        isco1_scores[isco1]["pct_tertiary"][country] = float(row["pct_high_ed"])

    # Propagate ISCO 1-digit → 3-digit
    layer = {}
    for isco3 in all_isco3:
        isco1 = isco3_to_isco1.get(isco3)
        if isco1 and isco1 in isco1_scores:
            layer[isco3] = {
                "education_score": dict(isco1_scores[isco1]["education_score"]),
                "pct_tertiary": dict(isco1_scores[isco1]["pct_tertiary"]),
            }
        else:
            layer[isco3] = {"education_score": {}, "pct_tertiary": {}}

    return layer


def compute_augmentation_scores(
    meta: pd.DataFrame,
    layer: dict,
) -> dict:
    """Compute augmentation_score (0-10) per isco3 × country.

    Additive composite: augmentation = AUG_W_EXPOSURE × exposure_z
                                     + AUG_W_GROWTH  × growth_z
                                     + AUG_W_EDUCATION × education_z

    Where _z = z-score normalized within country, then mapped to 0-10.
    Uses technical_score as the exposure input (from scores.json).
    Falls back to EU27 average for missing growth/education values.
    "AI augmentation sweet spot" = high exposure + positive growth + higher education workforce.
    """
    all_isco3 = sorted(meta["isco3"].unique())

    # Load technical_score from scores.json (not in layer_scores.json)
    tech_scores = {}  # {isco3: float}
    if INPUT_SCORES.exists():
        with open(INPUT_SCORES, encoding="utf-8") as f:
            scores = json.load(f)
        for isco3 in all_isco3:
            ts = scores.get(isco3, {}).get("technical_score")
            if ts is not None:
                tech_scores[isco3] = float(ts)
        print(f"  Technical scores loaded: {len(tech_scores)} groups")
    else:
        print("  WARNING: scores.json not found, cannot compute augmentation")
        return {}

    # Gather all countries from growth or education data
    all_countries = set()
    for isco3 in all_isco3:
        if isco3 not in layer:
            continue
        gs = layer[isco3].get("growth_score", {})
        es = layer[isco3].get("education_score", {})
        if isinstance(gs, dict):
            all_countries.update(gs.keys())
        if isinstance(es, dict):
            all_countries.update(es.keys())

    if not all_countries:
        print("  WARNING: No country data for augmentation composite")
        return {}

    # Compute EU27 averages for fallback
    eu27_growth = {}  # {isco3: score}
    eu27_education = {}  # {isco3: score}
    for isco3 in all_isco3:
        if isco3 not in layer:
            continue
        gs = layer[isco3].get("growth_score", {})
        es = layer[isco3].get("education_score", {})
        if isinstance(gs, dict) and "EU27" in gs:
            eu27_growth[isco3] = gs["EU27"]
        if isinstance(es, dict) and "EU27" in es:
            eu27_education[isco3] = es["EU27"]

    result = {}
    for isco3 in all_isco3:
        result[isco3] = {"augmentation_score": {}}

    for country in sorted(all_countries):
        raw_data = []  # [(isco3, exposure, growth, education)]
        for isco3 in all_isco3:
            exposure = tech_scores.get(isco3)
            if exposure is None:
                continue

            ld = layer.get(isco3, {})

            # Growth: per-country, fallback to EU27
            gs = ld.get("growth_score", {})
            growth = gs.get(country) if isinstance(gs, dict) else None
            if growth is None:
                growth = eu27_growth.get(isco3)

            # Education: per-country, fallback to EU27
            es = ld.get("education_score", {})
            education = es.get(country) if isinstance(es, dict) else None
            if education is None:
                education = eu27_education.get(isco3)

            if growth is not None and education is not None:
                raw_data.append((isco3, exposure, growth, education))

        if len(raw_data) < 2:
            continue

        # Z-score normalize each dimension within country
        exposures = np.array([r[1] for r in raw_data])
        growths = np.array([r[2] for r in raw_data])
        educations = np.array([r[3] for r in raw_data])

        def zscore(arr):
            std = arr.std()
            if std < 1e-6:
                return np.zeros_like(arr)
            return (arr - arr.mean()) / std

        exp_z = zscore(exposures)
        grw_z = zscore(growths)
        edu_z = zscore(educations)

        # Weighted composite
        composite = AUG_W_EXPOSURE * exp_z + AUG_W_GROWTH * grw_z + AUG_W_EDUCATION * edu_z

        # Map to 0-10 via min-max within country
        c_min, c_max = composite.min(), composite.max()
        spread = c_max - c_min
        if spread < 1e-6:
            spread = 1.0

        for i, (isco3, _, _, _) in enumerate(raw_data):
            score = ((composite[i] - c_min) / spread) * 10
            score = round(max(0, min(10, score)), 1)
            result[isco3]["augmentation_score"][country] = score

    return result


def print_stats(layer: dict, score_key: str):
    """Print distribution stats for a layer score across countries."""
    all_scores = []
    country_avgs = {}
    for isco3, data in layer.items():
        scores = data.get(score_key, {})
        for country, score in scores.items():
            all_scores.append(score)
            if country not in country_avgs:
                country_avgs[country] = []
            country_avgs[country].append(score)

    if not all_scores:
        print(f"  No data for {score_key}")
        return

    arr = np.array(all_scores)
    print(f"\n  {score_key} distribution (n={len(arr)}):")
    print(f"    min={arr.min():.1f}  p25={np.percentile(arr,25):.1f}  median={np.median(arr):.1f}  p75={np.percentile(arr,75):.1f}  max={arr.max():.1f}  mean={arr.mean():.1f}")

    # Show a few country averages
    sample_countries = ["EU27", "DE", "FR", "UK", "CH", "PL", "RO"]
    print(f"    Country avgs: ", end="")
    for c in sample_countries:
        if c in country_avgs:
            avg = np.mean(country_avgs[c])
            print(f"{c}={avg:.1f} ", end="")
    print()


def main():
    print("Loading occupations by country...")
    df = pd.read_csv(INPUT_COUNTRY, dtype={"isco3": str})
    print(f"  {len(df)} rows, {df['isco3'].nunique()} groups, {df['country'].nunique()} countries")

    print("Loading occupations metadata...")
    meta = pd.read_csv(INPUT_META, dtype={"isco3": str, "isco1": str, "isco2": str})
    print(f"  {len(meta)} occupation groups")

    # ── Pay layer ──
    print("\nComputing pay scores...")
    layer = compute_pay_scores(df)
    print_stats(layer, "pay_score")
    pay_count = sum(1 for v in layer.values() if v["pay_score"])
    print(f"\n  {pay_count}/{len(layer)} groups have pay scores")

    # ── Growth layer ──
    print("\nComputing growth scores...")
    growth_layer = compute_growth_scores(meta)
    if growth_layer:
        print_stats(growth_layer, "growth_score")
        growth_count = sum(1 for v in growth_layer.values() if v["growth_score"])
        print(f"\n  {growth_count}/{len(growth_layer)} groups have growth scores")

        # Merge growth into main layer dict
        for isco3, gdata in growth_layer.items():
            if isco3 in layer:
                layer[isco3].update(gdata)
            else:
                layer[isco3] = gdata

    # ── Adoption layer ──
    print("\nComputing adoption scores...")
    adoption_layer = compute_adoption_scores(meta)
    if adoption_layer:
        # Print adoption stats (not per-country, so custom print)
        scores = [v["adoption_score"] for v in adoption_layer.values() if v.get("adoption_score") is not None]
        if scores:
            arr = np.array(scores)
            print(f"\n  adoption_score distribution (n={len(arr)}):")
            print(f"    min={arr.min():.1f}  p25={np.percentile(arr,25):.1f}  median={np.median(arr):.1f}  p75={np.percentile(arr,75):.1f}  max={arr.max():.1f}  mean={arr.mean():.1f}")
        adoption_count = sum(1 for v in adoption_layer.values() if v.get("adoption_score") is not None)
        print(f"\n  {adoption_count}/{len(adoption_layer)} groups have adoption scores")

        # Merge adoption into main layer dict
        for isco3, adata in adoption_layer.items():
            if isco3 in layer:
                layer[isco3].update(adata)
            else:
                layer[isco3] = adata

    # ── Education layer ──
    print("\nComputing education scores...")
    education_layer = compute_education_scores(meta)
    if education_layer:
        print_stats(education_layer, "education_score")
        education_count = sum(1 for v in education_layer.values() if v["education_score"])
        print(f"\n  {education_count}/{len(education_layer)} groups have education scores")

        # Merge education into main layer dict
        for isco3, edata in education_layer.items():
            if isco3 in layer:
                layer[isco3].update(edata)
            else:
                layer[isco3] = edata

    # ── Augmentation layer ──
    print("\nComputing augmentation scores...")
    augmentation_layer = compute_augmentation_scores(meta, layer)
    if augmentation_layer:
        print_stats(augmentation_layer, "augmentation_score")
        aug_count = sum(1 for v in augmentation_layer.values() if v["augmentation_score"])
        print(f"\n  {aug_count}/{len(augmentation_layer)} groups have augmentation scores")

        # Merge augmentation into main layer dict
        for isco3, adata in augmentation_layer.items():
            if isco3 in layer:
                layer[isco3].update(adata)
            else:
                layer[isco3] = adata

    # Save
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(layer, f, indent=1, ensure_ascii=False)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"\nOutput: {OUTPUT} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
