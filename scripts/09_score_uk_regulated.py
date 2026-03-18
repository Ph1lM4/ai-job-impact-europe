"""
09_score_uk_regulated.py — Score UK-specific regulated exposure for ~130 ISCO 3-digit groups.

Uses Claude Sonnet to assess each occupation under the UK's regulatory environment,
which deliberately has NO EU AI Act equivalent. Outputs uk_scores.json and merges
uk_regulated_score into scores.json.

Input:  occupations.csv, scores.json
Output: uk_scores.json, scores.json (updated with uk_regulated_score)
"""

import json
import os
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)
INPUT = ROOT / "occupations.csv"
SCORES_FILE = ROOT / "scores.json"
UK_OUTPUT = ROOT / "uk_scores.json"
MODEL = "claude-sonnet-4-20250514"

UK_SCORING_PROMPT = """\
You are an expert analyst assessing the PRACTICAL AI exposure of occupations in the \
United Kingdom's labour market, factoring in the UK's specific regulatory environment.

You are given the TECHNICAL exposure score (pure AI capability). Your task is to assess \
the UK REGULATED exposure — what the UK regulatory environment practically allows.

The UK has deliberately chosen NOT to legislate AI-specific regulation. Key context:
- No EU AI Act equivalent (no high-risk classification, no mandatory notification to workers)
- No works council co-determination (ICE Regulations 2004: weak consultation rights only, \
for 50+ employee undertakings)
- UK GDPR + Data Protection Act 2018: Art 22 equivalent on automated decision-making \
(primary AI-relevant provision)
- Equality Act 2010: discrimination claims for AI-assisted hiring/promotion/pay (reactive, \
not preventive)
- Employment Rights Act 1996: unfair dismissal covers algorithmic termination but no \
AI-specific provisions
- DSIT pro-innovation framework: policy, not legislation
- Sector regulators (FCA, CQC, Ofcom) may add requirements in specific industries

UK friction should be LOWER than the EU regulated score's friction. But not zero — \
Equality Act discrimination risk, UK GDPR Art 22, and unfair dismissal law create some friction.

For low-technical-exposure occupations (physical trades), the UK regulated score should be \
very close to technical (regulation is irrelevant where AI isn't deployed).

Respond in JSON format ONLY (no markdown, no code fences):
{{
  "uk_regulated_score": <float 0-10>,
  "uk_regulatory_friction": <float — difference from technical>,
  "uk_rationale": "<2-3 sentence explanation of UK-specific friction>",
  "key_uk_provisions": ["Equality Act 2010", "UK GDPR Art 22", ...]
}}

OCCUPATION: {isco3_label}
ISCO-08: {isco3}
Technical score: {technical_score}
EU regulated score: {regulated_score}
Description: {composite_description}
"""


def load_cache(path):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def score_occupation(client, row, scores):
    """Send one occupation to Claude Sonnet for UK-specific scoring."""
    isco3 = row["isco3"]
    existing = scores.get(isco3, {})

    prompt = UK_SCORING_PROMPT.format(
        isco3_label=row["isco3_label"],
        isco3=isco3,
        technical_score=existing.get("technical_score", "N/A"),
        regulated_score=existing.get("regulated_score", "N/A"),
        composite_description=row["composite_description"][:3000],
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    return json.loads(text)


def main():
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env")
        return

    client = anthropic.Anthropic(api_key=api_key)

    print("Loading occupations...")
    df = pd.read_csv(INPUT, dtype={"isco3": str, "isco2": str, "isco1": str})
    print(f"  {len(df)} occupation groups")

    print("Loading existing scores...")
    scores = load_cache(SCORES_FILE)
    print(f"  {len(scores)} existing scores")

    uk_cache = load_cache(UK_OUTPUT)
    print(f"  {len(uk_cache)} UK scores already cached")

    to_score = [row for _, row in df.iterrows() if row["isco3"] not in uk_cache]
    print(f"  {len(to_score)} remaining to score")

    if not to_score:
        print("All groups already scored!")
    else:
        errors = 0
        for row in tqdm(to_score, desc="UK Scoring"):
            isco3 = row["isco3"]
            try:
                result = score_occupation(client, row, scores)
                uk_cache[isco3] = result
                save_cache(uk_cache, UK_OUTPUT)
            except json.JSONDecodeError as e:
                print(f"\n  JSON parse error for {isco3}: {e}")
                errors += 1
            except Exception as e:
                print(f"\n  Error for {isco3}: {e}")
                errors += 1
                if "rate_limit" in str(e).lower() or "overloaded" in str(e).lower():
                    print("  Backing off 30s...")
                    time.sleep(30)
                else:
                    time.sleep(1)

        print(f"\nScoring done! {len(uk_cache)} scored, {errors} errors")

    # ── Merge into scores.json ──
    print("\nMerging uk_regulated_score into scores.json...")
    merged = 0
    for isco3, uk_data in uk_cache.items():
        if isco3 in scores:
            scores[isco3]["uk_regulated_score"] = uk_data["uk_regulated_score"]
            scores[isco3]["uk_regulatory_friction"] = uk_data["uk_regulatory_friction"]
            scores[isco3]["uk_rationale"] = uk_data["uk_rationale"]
            scores[isco3]["key_uk_provisions"] = uk_data["key_uk_provisions"]
            merged += 1
    save_cache(scores, SCORES_FILE)
    print(f"  Merged {merged} UK scores into scores.json")

    # ── Summary stats ──
    print("\n" + "=" * 60)
    print("UK SCORING RESULTS SUMMARY")
    print("=" * 60)

    uk_scores = []
    for isco3, data in uk_cache.items():
        tech = scores.get(isco3, {}).get("technical_score", 0)
        eu_reg = scores.get(isco3, {}).get("regulated_score", 0)
        uk_reg = data["uk_regulated_score"]
        uk_friction = data["uk_regulatory_friction"]
        label = scores.get(isco3, {}).get("rationale", isco3)  # fallback
        # Get label from occupations
        uk_scores.append({
            "isco3": isco3,
            "technical": tech,
            "eu_regulated": eu_reg,
            "uk_regulated": uk_reg,
            "uk_friction": uk_friction,
            "eu_friction": tech - eu_reg,
        })

    # Load occupation labels
    labels = dict(zip(df["isco3"], df["isco3_label"]))

    if uk_scores:
        avg_uk_reg = sum(d["uk_regulated"] for d in uk_scores) / len(uk_scores)
        avg_uk_friction = sum(d["uk_friction"] for d in uk_scores) / len(uk_scores)
        avg_eu_friction = sum(d["eu_friction"] for d in uk_scores) / len(uk_scores)
        avg_tech = sum(d["technical"] for d in uk_scores) / len(uk_scores)

        print(f"\nCount:                {len(uk_scores)} occupation groups")
        print(f"Avg technical score:  {avg_tech:.2f}")
        print(f"Avg UK regulated:     {avg_uk_reg:.2f}")
        print(f"Avg UK friction:      {avg_uk_friction:.2f} pts")
        print(f"Avg EU friction:      {avg_eu_friction:.2f} pts (for comparison)")
        print(f"UK/EU friction ratio: {avg_uk_friction/avg_eu_friction:.1%}" if avg_eu_friction > 0 else "")

        # Top 5 by UK friction
        by_friction = sorted(uk_scores, key=lambda d: d["uk_friction"], reverse=True)
        print(f"\nTOP 5 by UK regulatory friction (highest):")
        for d in by_friction[:5]:
            print(f"  {d['isco3']} {labels.get(d['isco3'], '?'):<45} "
                  f"tech={d['technical']:.1f}  uk_reg={d['uk_regulated']:.1f}  "
                  f"uk_friction={d['uk_friction']:.1f}  eu_friction={d['eu_friction']:.1f}")

        print(f"\nBOTTOM 5 by UK regulatory friction (lowest):")
        for d in by_friction[-5:]:
            print(f"  {d['isco3']} {labels.get(d['isco3'], '?'):<45} "
                  f"tech={d['technical']:.1f}  uk_reg={d['uk_regulated']:.1f}  "
                  f"uk_friction={d['uk_friction']:.1f}  eu_friction={d['eu_friction']:.1f}")

        # Distribution of UK friction
        print(f"\nUK friction distribution:")
        brackets = [(0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 10.0)]
        for lo, hi in brackets:
            count = sum(1 for d in uk_scores if lo <= d["uk_friction"] < hi)
            print(f"  {lo:.1f}-{hi:.1f}: {count} groups")


if __name__ == "__main__":
    main()
