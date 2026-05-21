## v2.5.0 — 2026-05-21

Versions the Gostev capability-floor work (see the two [Unreleased] notes below) and ships a suite-wide editorial pass.

- **Methodology: Reasoning-Sensitive Occupations subsection** added after the Data Sources table. Plain-language explanation of why reasoning-tuned models can reduce output value in some expert occupations, plus the 12 ISCO-08 3-digit groups (medicine, law, finance, audit, regulation) that carry the flag. Cross-checked against the `GOSTEV_BY_ISCO3` map in `index.html` that drives the per-occupation warning.
- **Methodology: Gostev / Arena primary-source row** added to the Data Sources table. Figures verified word-for-word against `contemporary-claims-registry.md` Source 8: ~6M Arena votes, ~40k expert prompts, Q2 2023–Q1 2026 span, ~9% Q1 2026 dissatisfaction rate.
- **Suite-wide prose pass:** em-dashes removed from all user-facing prose across the six pages and `data.json`, fixed by restructuring rather than character substitution. Minor plain-language clarity edits.
- Closes two of the three open Gostev-backlog items (methodology row, Reasoning-Sensitive watchlist). Layer 6 synthesis copy remains open.

## [Unreleased] — Gostev Capability Floor panel deployed (2026-04-29)

Implements the panel planned in the 2026-04-28 Gostev empirical-floor ingestion. Plus CSS regression fix introduced by panel container styling.

- **Capability Floor (Gostev Q1 2026) panel** added to occupation detail UI (desktop sidebar + mobile sheet, all 36 countries)
- Surfaces the ~9% sensitivity bound + Gostev category mapping (quantitative / general / slow / slow_rs) keyed by ISCO 3-digit
- Reasoning-Sensitive flag for legal, audit, regulatory, and medical occupations (ISCO 221, 222, 225, 226, 241, 261, 321, 322, 325, 331, 335, 341)
- Client-side ISCO mapping; data-pipeline embedding deferred to v2 if Gostev categorisation becomes load-bearing for treemap colouring/sorting
- **CSS fix:** resolved navbar/header overlay regression on sidebar occupation details + page headers (analysis, methodology, sources)

**Three Gostev-backlog items remain open:** methodology page Gostev/Arena primary-source row, Reasoning-Sensitive Occupations Watchlist advisory deliverable, Layer 6 synthesis copy.

## [Unreleased] — Gostev empirical-floor ingestion (2026-04-28)

### Cross-pollination from AI Engineer Europe 2026 (Brain ingestion 2026-04-28)

**Source:** Peter Gostev (AI Capability Lead, Arena.ai), AIE Europe keynote *"What Do Models Still Suck At?"* (London, April 10 2026). Public Arena.ai dataset spanning Q2 2023 → Q1 2026 (~6M votes, ~40,000 expert-classified prompts, top-25-models battles).

**Three findings load-bearing for this project:**

1. **Frontier dissatisfaction floor at ~9% in Q1 2026.** Drop from ~17% (pre-reasoning) → ~12% (post-o1) → 9% (now). This is the empirical sensitivity bound on every "AI will reliably do X%" forecast the Map publishes.
2. **Category gradients are large and persistent.** Quantitative tasks improve dramatically; gaming, magical, finance, law improve weakly. Maps directly to the Map's occupational families — financial-services and legal occupations face *slower* Phase progression than headline benchmarks suggest.
3. **Reasoning often makes pushback worse, not better.** On the "BS benchmark" (155 nonsense questions), GPT-5.x and Gemini score ~50/50 on rejecting bad-premise questions; cranking up reasoning *increases* nonsense-acceptance. For occupations where *refusing the wrong question* is the work (legal triage, audit, regulatory advisory, medical), reasoning models actively degrade deployment quality.

**Implementation backlog (planned, not yet shipped):**

- **Layer 1 occupation pages:** add a "Capability Floor" panel per occupation, derived from Gostev's category mapping.
- **Layer 6 synthesis copy:** lead with the three-friction-layer model (capability floor × physical-compute realisability × regulatory deployability). Map's regulatory-overlay differentiator now sits inside a tighter compound model.
- **New advisory deliverable:** *"Reasoning-Sensitive Occupations Watchlist"* — list of occupations where deploying reasoning models *reduces* deployment value. Direct sales hook for legal-tech, insurance, audit, medical-AI buyers.
- **Methodology page:** add Gostev/Arena as an empirical-floor primary source alongside Karpathy / Frey-Osborne / Anthropic Economic Index / Coface-OEM.

**Cross-references (in second-brain repo):**
- `skills/disruption-analysis/SKILL.md` v0.5.2 Takeaway 30
- `knowledge/practitioner/contemporary-claims-registry.md` Source 8
- `knowledge/practitioner/klinger-three-layer-exposure.md` Gostev calibration section
- `knowledge/lecture-kits/ai-labour-reskilling.md` empirical-floor row
- `venture-data/european-ai-exposure-map/VENTURE-SCOPE.md` Gostev cross-pollination section

---

## v2.3.0 — 2026-04-01

### UX Simplification: Risk / Opportunity / Context Mode Toggle

**Problem:** First-time visitors faced a "pick one of seven" dropdown without understanding what each metric meant.

**Solution:** Three-mode toggle replaces the dropdown:
- **Risk** — Technical Exposure, Regulated Exposure (orange/red palette)
- **Opportunity** — Employment Growth, Augmentation, Median Pay (new green/teal palette)
- **Context** — Adoption Reality, Education Level (neutral blue-gray palette)

**Also ships:**
- Layer narrative cards visible above treemap before any interaction
- Cross-layer insight links in occupation detail panel ("See growth pattern →")
- Full backward compatibility for existing deep links (?layer= auto-infers mode)
- All PostHog capture calls now safely guarded against ad blockers
