"""
04_score.py — Score ~125 ISCO 3-digit occupation groups for AI exposure using Claude Sonnet.

Reads composite descriptions from occupations.csv, sends each to the Anthropic API,
caches results in scores.json to avoid re-scoring on reruns.

Input:  occupations.csv
Output: scores.json
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
OUTPUT = ROOT / "scores.json"
MODEL = "claude-sonnet-4-20250514"

SCORING_PROMPT = """\
You are an expert analyst assessing how much artificial intelligence will reshape \
occupations in the European labor market.

Score the following occupation group on TWO axes, each from 0 to 10:

1. **technical_score** — Pure technical capability. How much CAN AI reshape this job? \
Ignore regulation, labor law, and adoption barriers. Score raw AI capability vs. the tasks.

2. **regulated_score** — Practical European exposure. How much WILL AI reshape this job \
in the EU regulatory environment? Factor in:
   - EU AI Act: Annex III high-risk classifications (recruitment, performance evaluation, \
workforce management, education, law enforcement, access to essential services)
   - Works council co-determination: Germany (BetrVG §87(1) No. 6), Austria (ArbVG §96a) — \
any AI system affecting working conditions requires consultation
   - Employment protection: stronger dismissal protections slow workforce restructuring
   - GDPR constraints: automated decision-making restrictions (Art. 22)
   - The regulated_score should ALWAYS be ≤ technical_score. The delta represents regulatory friction.

Both scores measure AI transformation considering:
- Direct automation: AI systems performing tasks currently done by humans
- Indirect effects: AI making workers so productive that fewer are needed

Key scoring signals:
- If the work product is fundamentally digital (done entirely on a computer/from \
home office), AI exposure is inherently HIGH
- Physical presence, manual dexterity, real-time human interaction, or work in \
unstructured physical environments create natural barriers → LOWER exposure
- Consider both current LLM/AI capabilities and near-term trajectory (2-5 years)

Calibration for technical_score (use these as anchors):
0-1: Roofers, janitors, construction laborers
2-3: Electricians, plumbers, nursing assistants, firefighters
4-5: Registered nurses, retail workers, physicians
6-7: Teachers, managers, accountants, engineers
8-9: Software developers, paralegals, data analysts, editors
10: Medical transcriptionists

For regulated_score, the delta from technical_score should reflect regulatory friction:
- Minimal delta (0-1): Low-regulation occupations, or occupations where AI tools don't \
trigger high-risk classifications (e.g., construction, cleaning — no AI to regulate)
- Moderate delta (1-2): Occupations where GDPR or general employment protection slows adoption
- Large delta (2-4): Occupations where AI Act Annex III + works council rights create \
significant barriers (e.g., HR managers, recruiters, performance evaluators, teachers)

Respond in JSON format ONLY (no markdown, no code fences):
{{
  "technical_score": <float 0-10>,
  "regulated_score": <float 0-10>,
  "rationale": "<2-3 sentence explanation of technical exposure>",
  "regulatory_friction": "<1-2 sentences: which specific EU regulations create friction and why>",
  "key_vulnerable_tasks": ["task1", "task2", "task3"],
  "key_protected_tasks": ["task1", "task2", "task3"]
}}

OCCUPATION GROUP:
Title: {isco3_label}
ISCO-08 Code: {isco3}
Constituent occupations: {esco_occupations}
Description: {composite_description}
Representative skills required: {sample_skills}
"""


def load_cache():
    if OUTPUT.exists():
        with open(OUTPUT, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def score_occupation(client, row):
    """Send one occupation to Claude Sonnet and parse the JSON response."""
    prompt = SCORING_PROMPT.format(
        isco3_label=row["isco3_label"],
        isco3=row["isco3"],
        esco_occupations=row["esco_occupations"],
        composite_description=row["composite_description"][:3000],  # truncate very long descriptions
        sample_skills=row["sample_skills"],
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=768,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Handle potential markdown code fences
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

    cache = load_cache()
    print(f"  {len(cache)} already scored (cached)")

    # Re-score entries that don't have the dual-score format
    to_score = [row for _, row in df.iterrows()
                if row["isco3"] not in cache or "technical_score" not in cache.get(row["isco3"], {})]
    print(f"  {len(to_score)} remaining to score")

    if not to_score:
        print("All groups already scored!")
        return

    errors = 0
    for row in tqdm(to_score, desc="Scoring"):
        isco3 = row["isco3"]
        try:
            result = score_occupation(client, row)
            cache[isco3] = result
            save_cache(cache)  # save after each to preserve progress
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

    print(f"\nDone! {len(cache)} scored, {errors} errors")

    # Summary stats
    tech_scores = [v["technical_score"] for v in cache.values() if "technical_score" in v]
    reg_scores = [v["regulated_score"] for v in cache.values() if "regulated_score" in v]
    if tech_scores:
        avg_tech = sum(tech_scores) / len(tech_scores)
        avg_reg = sum(reg_scores) / len(reg_scores)
        avg_delta = avg_tech - avg_reg
        print(f"Average technical score: {avg_tech:.1f}")
        print(f"Average regulated score: {avg_reg:.1f}")
        print(f"Average regulatory delta: {avg_delta:.1f}")
        deltas = [t - r for t, r in zip(tech_scores, reg_scores)]
        max_delta_idx = deltas.index(max(deltas))
        keys = list(cache.keys())
        print(f"Largest delta: {keys[max_delta_idx]} ({max(deltas):.1f})")


if __name__ == "__main__":
    main()
