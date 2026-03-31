# Skill Protection Data Integration Spec — AI Exposure Map

**Created:** 2026-03-30
**Source:** Skill Protection Landscape research synthesis (4 dossiers, 18 papers)
**Target:** BUILD-PLAN Section 5 ("Skills That Protect"), `data/manual/` data files

## Current State

The build plan (BUILD-PLAN-job-market-2026-03-28.md) references Section 5 "Skills That Protect" as planned but not yet built. The project has:
- 125 ISCO3 occupation codes with AI exposure scores (`scores.json`)
- ESCO skill taxonomy data (`data/esco/skills_en.csv`, skill-skill relations, skill groups)
- AI Act high-risk classification (`data/manual/ai_act_high_risk.json`)
- Multi-layer scoring (`data/layer_scores.json` — pay, growth, adoption, education)

## Proposed Data Structure

### New file: `data/manual/skill_protection_matrix.json`

```json
{
  "metadata": {
    "created": "2026-03-30",
    "sources": "18 papers, 4 research dossiers. See second-brain/sources/dossiers/skill-protection-landscape/README.md",
    "methodology": "Cross-validated synthesis of peer-reviewed labor economics + institutional reports"
  },
  "protection_skills": [
    {
      "id": "ai_fluency",
      "label": "AI Fluency",
      "description": "Using, managing, and orchestrating AI tools in domain workflows",
      "trajectory": "exponential_growth",
      "wage_premium_pct": { "peer_reviewed": 21, "industry": 56 },
      "sources": ["Stephany & Teutloff 2024 Research Policy", "PwC AI Jobs Barometer 2025"],
      "automation_bottleneck": false,
      "hub_skill": true,
      "esco_mapping": ["using computers and electronics", "artificial intelligence"]
    },
    {
      "id": "social_intelligence",
      "label": "Social Intelligence",
      "description": "Negotiation, persuasion, leadership, stakeholder management",
      "trajectory": "growing",
      "employment_growth_pp": 12,
      "sources": ["Deming 2017 QJE", "Frey & Osborne 2017 TFSC"],
      "automation_bottleneck": true,
      "hub_skill": false
    },
    {
      "id": "creative_thinking",
      "label": "Creative Thinking",
      "description": "Novel problem framing, originality, aesthetic judgment",
      "trajectory": "growing",
      "growth_by_2030_pct": 12,
      "sources": ["McKinsey 2024", "Frey & Osborne 2017 TFSC", "WEF 2025"],
      "automation_bottleneck": true,
      "hub_skill": false
    },
    {
      "id": "analytical_thinking",
      "label": "Analytical/Systems Thinking",
      "description": "Complex reasoning, strategic analysis, systems design",
      "trajectory": "growing",
      "employer_demand_pct": 70,
      "sources": ["WEF 2025", "Eloundou et al. 2024 Science"],
      "automation_bottleneck": false,
      "hub_skill": false,
      "note": "Negatively correlated with LLM exposure (Eloundou)"
    },
    {
      "id": "cybersecurity",
      "label": "Cybersecurity",
      "trajectory": "exponential_growth",
      "bls_growth_pct": 29,
      "eu_gap": 300000,
      "sources": ["BLS 2024", "ENISA 2025", "ISC2 2024"]
    },
    {
      "id": "regulatory_compliance",
      "label": "Regulatory/Compliance Knowledge",
      "trajectory": "growing",
      "eu_specific": true,
      "drivers": ["EU AI Act", "NIS2", "DORA", "CSRD", "EAA"],
      "sources": ["European Commission impact assessments", "ENISA 2025"]
    },
    {
      "id": "esg_sustainability",
      "label": "ESG/Sustainability Data",
      "trajectory": "exponential_growth",
      "new_jobs_by_2030": 34000000,
      "sources": ["WEF 2025", "OECD 2023"]
    },
    {
      "id": "resilience_adaptability",
      "label": "Resilience/Adaptability",
      "trajectory": "growing",
      "sources": ["WEF 2025", "OECD 2023/2025"],
      "note": "Differentiates growing from declining jobs (WEF)"
    },
    {
      "id": "data_literacy",
      "label": "Data Literacy",
      "trajectory": "growing",
      "bls_growth_pct": 34,
      "wage_premium_pct": 23,
      "sources": ["BLS 2024", "Lightcast 2024"]
    },
    {
      "id": "communication",
      "label": "Communication & Influence",
      "trajectory": "stable_to_growing",
      "sources": ["LinkedIn Skills on the Rise 2025", "Deming 2017"]
    },
    {
      "id": "domain_expertise",
      "label": "Domain Expertise",
      "trajectory": "stable",
      "note": "Protection value INCREASES when combined with AI fluency"
    }
  ],
  "protection_pairs": [
    {
      "pair": ["analytical_thinking", "social_intelligence"],
      "effect": "super_additive",
      "evidence": "Wage returns doubled between cohorts; employment grew 12pp for combined roles",
      "source": "Deming 2017 QJE",
      "confidence": 5
    },
    {
      "pair": ["domain_expertise", "ai_fluency"],
      "effect": "hub_amplification",
      "evidence": "21-56% wage premium; every industry pays it",
      "source": "Stephany & Teutloff 2024; PwC 2025",
      "confidence": 4
    },
    {
      "pair": ["ai_fluency", "regulatory_compliance"],
      "effect": "scarcity_premium",
      "evidence": "EU AI Act creates mandatory roles with no US equivalent; fines up to 35M EUR",
      "source": "EU AI Act Art 4; ENISA 2025",
      "confidence": 3
    },
    {
      "pair": ["cybersecurity", "regulatory_compliance"],
      "effect": "extreme_scarcity",
      "evidence": "300K+ EU gap; NIS2 expands to 18 sectors; board-level accountability",
      "source": "ENISA 2025; ISC2 2024",
      "confidence": 3
    },
    {
      "pair": ["creative_thinking", "ai_fluency"],
      "effect": "automation_bottleneck_plus_amplifier",
      "evidence": "AI commoditizes execution but increases demand for creative direction",
      "source": "Frey & Osborne 2017; McKinsey 2024; WEF 2025",
      "confidence": 3
    },
    {
      "pair": ["data_literacy", "communication"],
      "effect": "bridging_premium",
      "evidence": "Marketing + SQL = ~40% higher pay; data storytelling bridges technical/business",
      "source": "Burning Glass 2019",
      "confidence": 3
    }
  ],
  "role_exposure_mapping": {
    "product": { "theoretical": "moderate", "complementarity": "high", "ai_premium_pct": "10-40" },
    "engineering": { "theoretical": "high", "complementarity": "high", "note": "Shift from writing to orchestrating code" },
    "design": { "theoretical": "moderate-high", "complementarity": "moderate", "note": "Execution declining, thinking protected" },
    "sales": { "theoretical": "moderate", "complementarity": "high", "note": "Consultative selling protected; transactional exposed" },
    "bizdev": { "theoretical": "moderate", "complementarity": "high", "note": "Relationship-dependent, high-context" },
    "marketing": { "theoretical": "moderate-high", "complementarity": "moderate", "note": "Higher replacement risk than other functions (IBM)" },
    "operations": { "theoretical": "high", "complementarity": "moderate", "note": "Hiring -20% in EU tech; admin tasks fully exposed" },
    "data_ai": { "theoretical": "high", "complementarity": "high", "note": "Paradox: both high disruption AND high demand" },
    "cybersecurity": { "theoretical": "low", "complementarity": "high", "note": "Most protected role family; adversarial nature resists automation" }
  }
}
```

### Integration with existing data

1. **Link to ISCO3 codes:** Each role family maps to multiple ISCO3 codes in `occupations.csv`. The `role_exposure_mapping` above can be linked to specific ISCO3 groups.

2. **Link to ESCO skills:** The `esco_mapping` field in each protection skill connects to `data/esco/skills_en.csv` via preferredLabel matching.

3. **Enhance `scores.json`:** Add `protective_skills` array to each ISCO3 entry, listing which of the 11 protection skills apply most.

4. **New script:** `scripts/20_build_skill_protection.py` — reads `skill_protection_matrix.json`, cross-references with ESCO mappings, and integrates into `site/data.json` for frontend.

## Build Plan Section 5 — Concrete Implementation

The BUILD-PLAN references "Skills That Protect" as a cross-role skill matrix at each seniority level. With the research now grounded, the implementation should:

1. Use the 11 protection skills above (mapped to ESCO taxonomy)
2. Score each skill per role using the research-backed matrix from the dossiers
3. Add seniority modifiers (junior: AI fluency matters more; senior: leadership + regulatory matters more)
4. Show protection pairs as the "skill connections" the build plan mentions
5. Add EU regulatory moat as a distinct European advantage section

## Key Numbers for Visualization

| Metric | Value | Source |
|---|---|---|
| Skills disrupted by 2030 | 39% | WEF 2025 |
| Technical skill half-life | ~2.5 years | IBM/WEF |
| AI wage premium | 21-56% | Stephany/PwC |
| Hybrid job automation risk | 12% vs 42% overall | Burning Glass |
| EU cybersecurity gap | 300,000+ | ENISA 2025 |
| Skill change rate (2021-2024) | 32% | Lightcast |
| Complementary roles per AI sub | >1.5 in management | Makela & Stephany 2024 |
| Cognitive-social wage growth | 12pp labor force share | Deming 2017 |
