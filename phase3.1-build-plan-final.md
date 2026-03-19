# Phase 3.1 Build Plan — Final

## Status: Sprints 1-4 COMPLETE. Sprint 5 (3.1 close + 3.1b) IN PROGRESS.

---

## Completed Sprints

### Sprint 1: Pay Layer + Frontend Dropdown ✅
- `scripts/12_compute_layers.py` — Pay normalization (percentile-rank within country, 0-10)
- `scripts/05_build_site_data.py` — Layer merging infrastructure
- `site/index.html` — Dropdown UI, LAYER_CONFIG, color scales, sub-toggle for Technical/Regulated
- 3 layers live: AI Exposure (tech+reg), Median Pay

### Sprint 2: Growth Layer ✅
- `scripts/10_fetch_growth.py` — Cedefop Skills Forecast 2025 (33 countries × 9 ISCO 1-digit, CAGR 2024→2035) + Eurostat YoY (35 countries, ISCO 2-digit → 1-digit)
- Blended z-scores: 40% Eurostat YoY + 60% Cedefop CAGR
- data.json: 959KB → 1206KB
- 4 layers live

### Sprint 2.5: Triangulated Adoption Reality ✅
- `scripts/13_fetch_adoption_data.py` — 3 datasets: Anthropic Economic Index (HuggingFace), Microsoft Working with AI (GitHub), OpenAI GPTs are GPTs (GitHub)
- SOC 6-digit → SOC 2-digit → ISCO 1-digit crosswalk
- `data/adoption/triangulated_adoption.csv` (10 ISCO 1-digit groups)
- Theoretical ceiling (OpenAI) vs observed usage mean(Anthropic, Microsoft)
- 5 layers live

### Sprint 3: Education Layer ✅
- `scripts/11_fetch_education.py` — Eurostat lfsa_egised, ISCED cross-tab
- Education score = pct_high_ed rescaled 0-10
- 6 layers live

### Sprint 4: Augmentation Composite + Narrative Polish ✅
- Augmentation composite: 0.5×exposure_z + 0.3×growth_z + 0.2×education_z
- Per-layer insight text in delta indicator (7 layers)
- Cross-layer insight cards in detail panel (6 conditional rules)
- Collapsible methodology disclosure with nested scoring rubrics
- Dynamic subtitle per layer
- 7 layers live, data.json: 1.44MB

---

## Sprint 5: Phase 3.1 Close + 3.1b Content & Navigation

### 5a. Close Phase 3.1 — Add Missing References to sources.html
Add 3 lab dataset references to the references table in `site/sources.html`:
1. Anthropic Economic Index (Handa et al., 2025 + Massenkoff & McCrory, 2026)
2. Microsoft "Working with AI" (Tomlinson et al., 2025)
3. OpenAI "GPTs are GPTs" (Eloundou et al., 2024)

### 5b. Create methodology.html
New page consolidating all methodology content currently split across:
- Collapsible on index.html (scoring rubrics)
- Author's note in analysis.html
- Augmentation formula in sources.html
Structure: Data Sources → Scoring Approach → Layer Definitions → Normalization → Limitations
Add to nav menu between Questions and Sources.

### 5c. Update analysis.html
- Strengthen "Education Doesn't Protect" finding with education layer data
- Strengthen "Regulatory Buffer" finding with adoption reality evidence
- Add new Finding 8: "The Augmentation Sweet Spot" — high exposure + growing + educated = transformed not eliminated
- Reference new layers where they reinforce existing findings
- Update methodology sections to link to methodology.html

### 5d. Update questions.html
- Add actionable layer references in relevant accordion sections (e.g., "Switch to Employment Growth to see your country's outlook")
- Add questions about augmentation potential and adoption reality where relevant

### 5e. Layer Legend Tooltip
- Add (?) icon next to the layer dropdown
- On hover/click: compact legend showing what each of the 7 layers measures
- 6 rows, one sentence each
- Lightweight — tooltip or small slide-down panel, not a modal

### 5f. Cross-link collapsible on index.html to methodology.html
- Keep the collapsible scoring disclosure on index.html as a summary
- Add "Full methodology →" link at the bottom of the collapsible pointing to methodology.html

---

## NOT in Phase 3.1b (deferred to Phase 3.2+)

- Overlay/triangulation function (filter/highlight mode or side-by-side)
- US vs EU transatlantic comparison
- Language versions
- Additional overlays (works council trigger map, green jobs)
- Temporal tracking

---

## Verification for Sprint 5

- All 3 lab references appear in sources.html with correct titles, authors, dates, URLs, licenses
- methodology.html loads, appears in nav menu, contains all methodology content
- analysis.html has updated findings including new Finding 8
- questions.html has layer references in relevant accordions
- Layer legend tooltip appears on hover/click next to dropdown
- Collapsible on index.html links to methodology.html
- All internal links work (nav, breadcrumbs, cross-references)
- No console errors
- Mobile: methodology page and legend tooltip render correctly

---

## Post-Sprint 5 Actions

1. Deploy to ai-exposure.nexalps.com
2. Email skills-forecast@cedefop.europa.eu with live link
3. Resume LinkedIn content calendar (Posts 2-8)
4. Update project status document for Phase 3.2 planning
