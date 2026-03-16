"""
01_prepare_esco.py — Parse ESCO v1.2.1 CSVs into processed JSON at ISCO 3-digit level.

Input:  data/esco/occupations_en.csv, ISCOGroups_en.csv, occupationSkillRelations_en.csv, skills_en.csv
Output: data/esco/esco_processed.json
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

ESCO_DIR = Path("data/esco")
OUTPUT = ESCO_DIR / "esco_processed.json"


def load_isco_groups():
    """Load ISCOGroups_en.csv → dict of code → preferredLabel."""
    groups = {}
    with open(ESCO_DIR / "ISCOGroups_en.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            groups[row["code"]] = row["preferredLabel"]
    return groups


def load_occupations():
    """Load occupations_en.csv → list of dicts with parsed ISCO codes."""
    occupations = []
    with open(ESCO_DIR / "occupations_en.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            isco4 = row["iscoGroup"].strip()
            if len(isco4) != 4 or not isco4.isdigit():
                continue
            occupations.append({
                "uri": row["conceptUri"],
                "label": row["preferredLabel"],
                "description": row.get("description", ""),
                "isco4": isco4,
                "isco3": isco4[:3],
                "isco2": isco4[:2],
                "isco1": isco4[:1],
            })
    return occupations


def load_skills():
    """Load skills_en.csv → dict of skillUri → preferredLabel."""
    skills = {}
    with open(ESCO_DIR / "skills_en.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            skills[row["conceptUri"]] = row["preferredLabel"]
    return skills


def load_skill_relations():
    """Load occupationSkillRelations_en.csv → dict of occupationUri → [skillLabel, ...]."""
    # Only load essential skills (not optional) to keep it manageable
    relations = defaultdict(list)
    with open(ESCO_DIR / "occupationSkillRelations_en.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["relationType"] == "essential":
                relations[row["occupationUri"]].append(row["skillLabel"])
    return relations


def build_isco3_groups(occupations, isco_labels, skill_relations):
    """Aggregate ESCO occupations into ISCO 3-digit groups."""
    groups = defaultdict(lambda: {
        "occupations": [],
        "descriptions": [],
        "skills": set(),
    })

    for occ in occupations:
        key = occ["isco3"]
        groups[key]["occupations"].append(occ["label"])
        if occ["description"]:
            groups[key]["descriptions"].append(occ["description"])
        # Collect skills for this occupation
        for skill in skill_relations.get(occ["uri"], []):
            groups[key]["skills"].add(skill)

    result = []
    for isco3, data in sorted(groups.items()):
        isco2 = isco3[:2]
        isco1 = isco3[:1]

        # Pick up to 3 longest descriptions as representative samples
        descs_sorted = sorted(data["descriptions"], key=len, reverse=True)
        representative_descs = descs_sorted[:3]

        # Build composite description for LLM scoring
        occ_list = ", ".join(sorted(set(data["occupations"])))
        desc_block = "\n\n".join(representative_descs)
        composite = f"Occupation group: {isco_labels.get(isco3, isco3)}\n"
        composite += f"Constituent occupations: {occ_list}\n\n"
        composite += f"Representative occupation descriptions:\n{desc_block}"

        # Sample skills — pick up to 15 most common
        sample_skills = sorted(data["skills"])[:15]

        result.append({
            "isco3": isco3,
            "isco3_label": isco_labels.get(isco3, f"ISCO {isco3}"),
            "isco2": isco2,
            "isco2_label": isco_labels.get(isco2, f"ISCO {isco2}"),
            "isco1": isco1,
            "isco1_label": isco_labels.get(isco1, f"ISCO {isco1}"),
            "esco_occupations": sorted(set(data["occupations"])),
            "esco_count": len(data["occupations"]),
            "composite_description": composite,
            "sample_skills": sample_skills,
        })

    return result


def main():
    print("Loading ISCO group labels...")
    isco_labels = load_isco_groups()
    print(f"  {len(isco_labels)} ISCO groups loaded")

    print("Loading ESCO occupations...")
    occupations = load_occupations()
    print(f"  {len(occupations)} occupations loaded")

    print("Loading skills and skill relations...")
    skill_relations = load_skill_relations()
    print(f"  {len(skill_relations)} occupations with skill links")

    print("Building ISCO 3-digit groups...")
    groups = build_isco3_groups(occupations, isco_labels, skill_relations)
    print(f"  {len(groups)} ISCO 3-digit groups built")

    # Summary stats
    total_occ = sum(g["esco_count"] for g in groups)
    avg_per_group = total_occ / len(groups) if groups else 0
    print(f"  {total_occ} total ESCO occupations mapped (avg {avg_per_group:.1f} per group)")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2, ensure_ascii=False)
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
