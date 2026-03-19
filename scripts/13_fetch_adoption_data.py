"""
13_fetch_adoption_data.py — Triangulated Adoption Reality layer.

Downloads and processes three independent AI labor market datasets:
  1. Anthropic Economic Index (HuggingFace, CC-BY) — observed Claude usage by SOC group
  2. Microsoft "Working with AI" (GitHub, MIT) — AI applicability scores per SOC
  3. OpenAI "GPTs are GPTs" (GitHub/Science paper) — theoretical LLM exposure per SOC

All three use US SOC codes. Pipeline:
  SOC 6-digit → aggregate to SOC 2-digit (22 major groups) → crosswalk to ISCO 1-digit (9 groups)

Output: data/adoption/triangulated_adoption.csv
  Columns: isco1, anthropic_observed, microsoft_applicability, openai_theoretical,
           observed_usage (mean of Anthropic + Microsoft), theoretical_ceiling (OpenAI),
           adoption_gap (theoretical - observed)

Note: All datasets are US-based. Applied uniformly across countries (occupation-level).
"""

import io
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "adoption"
OUTPUT = OUT_DIR / "triangulated_adoption.csv"

# ── SOC 2-digit → ISCO 1-digit crosswalk ──
SOC2_TO_ISCO1 = {
    "11": "1",   # Management → Managers
    "13": "2",   # Business and Financial Operations → Professionals
    "15": "2",   # Computer and Mathematical → Professionals
    "17": "2",   # Architecture and Engineering → Professionals
    "19": "2",   # Life, Physical, and Social Science → Professionals
    "21": "2",   # Community and Social Service → Professionals
    "23": "2",   # Legal → Professionals
    "25": "2",   # Educational Instruction and Library → Professionals
    "27": "2",   # Arts, Design, Entertainment, Sports, Media → Professionals
    "29": "2",   # Healthcare Practitioners and Technical → Professionals
    "31": "3",   # Healthcare Support → Technicians and Associate Professionals
    "33": "5",   # Protective Service → Service and Sales Workers
    "35": "5",   # Food Preparation and Serving → Service and Sales Workers
    "37": "9",   # Building and Grounds Cleaning → Elementary Occupations
    "39": "5",   # Personal Care and Service → Service and Sales Workers
    "41": "5",   # Sales and Related → Service and Sales Workers
    "43": "4",   # Office and Administrative Support → Clerical Support Workers
    "45": "6",   # Farming, Fishing, and Forestry → Skilled Agricultural Workers
    "47": "7",   # Construction and Extraction → Craft and Related Trades
    "49": "7",   # Installation, Maintenance, Repair → Craft and Related Trades
    "51": "8",   # Production → Plant and Machine Operators
    "53": "9",   # Transportation and Material Moving → Elementary Occupations
    "55": "0",   # Military Specific → Armed Forces
}


def extract_soc2(code_str: str) -> str | None:
    """Extract SOC 2-digit major group from a SOC code string."""
    if pd.isna(code_str):
        return None
    s = str(code_str).strip().replace("-", "").replace(".", "")
    if len(s) >= 2 and s[:2].isdigit():
        return s[:2]
    return None


def fetch_anthropic_data() -> pd.DataFrame | None:
    """Fetch Anthropic Economic Index — pre-aggregated SOC-level observed exposure.

    Uses labor_market_impacts/job_exposure.csv which has observed_exposure per SOC code.
    """
    print("=" * 60)
    print("Dataset 1: Anthropic Economic Index")
    print("=" * 60)

    base_url = "https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main"
    url = f"{base_url}/labor_market_impacts/job_exposure.csv"

    try:
        print(f"  Fetching job_exposure.csv...")
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            return None

        df = pd.read_csv(io.StringIO(r.text))
        print(f"  Got {len(df)} rows, columns: {list(df.columns)}")

        # Save raw file
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT_DIR / "anthropic_job_exposure.csv", index=False)

        # Extract SOC 2-digit and aggregate
        df["soc2"] = df["occ_code"].apply(extract_soc2)
        df = df.dropna(subset=["soc2", "observed_exposure"])

        # Aggregate to SOC 2-digit: mean of detailed occupations
        agg = df.groupby("soc2").agg(
            anthropic_observed=("observed_exposure", "mean"),
        ).reset_index()

        # Normalize to 0-1 (relative within dataset)
        max_val = agg["anthropic_observed"].max()
        if max_val > 0:
            agg["anthropic_observed"] = (agg["anthropic_observed"] / max_val).round(3)

        print(f"  Aggregated to {len(agg)} SOC 2-digit groups")
        print(f"  Top 5 by observed exposure:")
        for _, row in agg.nlargest(5, "anthropic_observed").iterrows():
            print(f"    SOC {row['soc2']}: {row['anthropic_observed']:.3f}")

        return agg[["soc2", "anthropic_observed"]]

    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_microsoft_data() -> pd.DataFrame | None:
    """Fetch Microsoft 'Working with AI' — AI applicability scores per SOC."""
    print("\n" + "=" * 60)
    print("Dataset 2: Microsoft Working with AI")
    print("=" * 60)

    url = "https://raw.githubusercontent.com/microsoft/working-with-ai/main/ai_applicability_scores.csv"
    try:
        print(f"  Fetching ai_applicability_scores.csv...")
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            return None

        df = pd.read_csv(io.StringIO(r.text))
        print(f"  Got {len(df)} rows, columns: {list(df.columns)}")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT_DIR / "microsoft_ai_applicability.csv", index=False)

        # Extract SOC 2-digit
        df["soc2"] = df["SOC Code"].apply(extract_soc2)
        df = df.dropna(subset=["soc2", "ai_applicability_score"])

        # Aggregate to SOC 2-digit: mean of detailed occupations
        agg = df.groupby("soc2").agg(
            microsoft_applicability=("ai_applicability_score", "mean"),
        ).reset_index()

        # Normalize to 0-1
        max_val = agg["microsoft_applicability"].max()
        if max_val > 0:
            agg["microsoft_applicability"] = (agg["microsoft_applicability"] / max_val).round(3)

        print(f"  Aggregated to {len(agg)} SOC 2-digit groups")
        print(f"  Top 5 by AI applicability:")
        for _, row in agg.nlargest(5, "microsoft_applicability").iterrows():
            print(f"    SOC {row['soc2']}: {row['microsoft_applicability']:.3f}")

        return agg[["soc2", "microsoft_applicability"]]

    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_openai_data() -> pd.DataFrame | None:
    """Fetch OpenAI 'GPTs are GPTs' — theoretical LLM exposure per SOC.

    Uses dv_rating_beta (GPT-4 rated E1+E2 exposure) as the theoretical ceiling.
    """
    print("\n" + "=" * 60)
    print("Dataset 3: OpenAI GPTs are GPTs")
    print("=" * 60)

    url = "https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/occ_level.csv"
    try:
        print(f"  Fetching occ_level.csv...")
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            return None

        df = pd.read_csv(io.StringIO(r.text))
        print(f"  Got {len(df)} rows, columns: {list(df.columns)}")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT_DIR / "openai_gpts_exposure.csv", index=False)

        # Use dv_rating_beta = GPT-4 rated E1+E2 (LLM + LLM-powered tools)
        score_col = "dv_rating_beta"
        soc_col = "O*NET-SOC Code"

        # Extract SOC 2-digit
        df["soc2"] = df[soc_col].apply(extract_soc2)
        df = df.dropna(subset=["soc2", score_col])

        # Aggregate to SOC 2-digit: mean of detailed occupations
        agg = df.groupby("soc2").agg(
            openai_theoretical=(score_col, "mean"),
        ).reset_index()

        # Normalize to 0-1
        max_val = agg["openai_theoretical"].max()
        if max_val > 0:
            agg["openai_theoretical"] = (agg["openai_theoretical"] / max_val).round(3)

        print(f"  Aggregated to {len(agg)} SOC 2-digit groups")
        print(f"  Top 5 by theoretical exposure:")
        for _, row in agg.nlargest(5, "openai_theoretical").iterrows():
            print(f"    SOC {row['soc2']}: {row['openai_theoretical']:.3f}")

        return agg[["soc2", "openai_theoretical"]]

    except Exception as e:
        print(f"  Error: {e}")
        return None


def crosswalk_to_isco(merged: pd.DataFrame) -> pd.DataFrame:
    """Map SOC 2-digit major groups to ISCO 1-digit using concordance table."""
    print("\n  Crosswalking SOC 2-digit → ISCO 1-digit...")

    merged["isco1"] = merged["soc2"].map(SOC2_TO_ISCO1)
    unmapped = merged[merged["isco1"].isna()]
    if len(unmapped) > 0:
        print(f"  WARNING: {len(unmapped)} unmapped SOC codes: {unmapped['soc2'].tolist()}")
    merged = merged.dropna(subset=["isco1"])

    # Multiple SOC 2-digit groups map to the same ISCO 1-digit.
    # Average the scores within each ISCO group.
    score_cols = [c for c in merged.columns if c not in ("soc2", "isco1")]
    agg = merged.groupby("isco1")[score_cols].mean().reset_index()

    for col in score_cols:
        agg[col] = agg[col].round(3)

    print(f"  Result: {len(agg)} ISCO 1-digit groups")
    return agg


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch all three datasets
    anthropic = fetch_anthropic_data()
    microsoft = fetch_microsoft_data()
    openai_data = fetch_openai_data()

    # Merge on SOC 2-digit
    all_soc2 = sorted(SOC2_TO_ISCO1.keys())
    merged = pd.DataFrame({"soc2": all_soc2})

    if anthropic is not None:
        merged = merged.merge(anthropic, on="soc2", how="left")
    else:
        merged["anthropic_observed"] = np.nan

    if microsoft is not None:
        merged = merged.merge(microsoft, on="soc2", how="left")
    else:
        merged["microsoft_applicability"] = np.nan

    if openai_data is not None:
        merged = merged.merge(openai_data, on="soc2", how="left")
    else:
        merged["openai_theoretical"] = np.nan

    # Crosswalk to ISCO 1-digit
    isco = crosswalk_to_isco(merged)

    # Compute composite scores
    obs_cols = []
    if "anthropic_observed" in isco.columns and isco["anthropic_observed"].notna().any():
        obs_cols.append("anthropic_observed")
    if "microsoft_applicability" in isco.columns and isco["microsoft_applicability"].notna().any():
        obs_cols.append("microsoft_applicability")

    if obs_cols:
        isco["observed_usage"] = isco[obs_cols].mean(axis=1).round(3)
    else:
        isco["observed_usage"] = np.nan

    if "openai_theoretical" in isco.columns and isco["openai_theoretical"].notna().any():
        isco["theoretical_ceiling"] = isco["openai_theoretical"]
    else:
        isco["theoretical_ceiling"] = np.nan

    isco["adoption_gap"] = (isco["theoretical_ceiling"] - isco["observed_usage"]).round(3)

    # Print summary
    print("\n" + "=" * 60)
    print("Triangulated Adoption Reality — ISCO 1-digit")
    print("=" * 60)
    print(f"{'ISCO':>6}  {'Observed':>10}  {'Theoretical':>12}  {'Gap':>8}  {'Anthropic':>10}  {'Microsoft':>10}  {'OpenAI':>8}")
    print("-" * 76)
    for _, row in isco.sort_values("isco1").iterrows():
        obs = f"{row['observed_usage']:.3f}" if pd.notna(row["observed_usage"]) else "N/A"
        theo = f"{row['theoretical_ceiling']:.3f}" if pd.notna(row["theoretical_ceiling"]) else "N/A"
        gap = f"{row['adoption_gap']:.3f}" if pd.notna(row["adoption_gap"]) else "N/A"
        anth = f"{row.get('anthropic_observed', np.nan):.3f}" if pd.notna(row.get("anthropic_observed")) else "N/A"
        ms = f"{row.get('microsoft_applicability', np.nan):.3f}" if pd.notna(row.get("microsoft_applicability")) else "N/A"
        oai = f"{row.get('openai_theoretical', np.nan):.3f}" if pd.notna(row.get("openai_theoretical")) else "N/A"
        print(f"  {row['isco1']:>4}  {obs:>10}  {theo:>12}  {gap:>8}  {anth:>10}  {ms:>10}  {oai:>8}")

    # Save
    isco.to_csv(OUTPUT, index=False)
    print(f"\nSaved: {OUTPUT}")

    merged.to_csv(OUT_DIR / "soc2_merged.csv", index=False)
    print(f"Saved: {OUT_DIR / 'soc2_merged.csv'}")

    return isco


if __name__ == "__main__":
    main()
