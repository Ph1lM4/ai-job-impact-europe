# EU AI Exposure Map — Project Status Summary
## Date: 19 March 2026

---

## What It Is

An interactive treemap visualizing AI exposure across the European job market. 
Inspired by Karpathy's US version (karpathy.ai/jobs), differentiated by:
- 36 countries (vs Karpathy's US-only)
- Dual scores: technical exposure + regulated exposure (EU and UK-specific)
- EU AI Act structured overlay with legal source references
- Full analysis, questions, and sources pages

**Live at:** ai-exposure.nexalps.com
**Repo:** github.com/Ph1lM4/ai-job-impact-europe (note: no 's' in job)
**License:** MIT (code) + CC-BY 4.0 (data/analysis) Philipp Maul | Nexalps

---

## What's Been Built (V2 — shipped and live)

### Data Pipeline (scripts/)
| Script | Purpose |
|--------|---------|
| 01_prepare_esco.py | Parse 3,043 ESCO occupations → 125 ISCO 3-digit groups |
| 02_fetch_eurostat.py | Employment (ISCO 2-digit, 2024) + wages for 35 Eurostat countries |
| 03_build_occupations.py | Merge ESCO + Eurostat + BFS + ONS → occupations.csv + occupations_by_country.csv |
| 04_score.py | Claude Sonnet 4 scores: technical + EU regulated (125 groups, dual scores) |
| 05_build_site_data.py | Generate site/data.json (353KB) with all countries, scores, AI Act overlay |
| 06_fetch_bfs.py | Parse Swiss BFS employment (ISCO 1-digit, 2025) + wages (ISCO 2-digit, 2024) |
| 07_fetch_ons.py | Parse UK ONS employment + wages from ASHE (SOC 2020 → ISCO-08 mapped) |
| 09_score_uk_regulated.py | UK-specific regulated scores (125 groups, avg friction 0.5 vs EU 1.2) |

### Data Sources
| Source | Coverage | Reference Year |
|--------|----------|---------------|
| ESCO v1.2.1 | Occupation descriptions + skills | 2024 (structural, not time-dependent) |
| Eurostat EU-LFS (lfsa_egai2d) | Employment by ISCO 2-digit, 35 countries | 2024 |
| Eurostat SES (earn_ses22_28) | Wages by ISCO 1-digit, 35 countries | 2022 |
| BFS LSE | Swiss wages by ISCO 2-digit (CHF→EUR at 0.96) | 2024 |
| BFS SAKE | Swiss employment by ISCO 1-digit | 2025 |
| ONS ASHE | UK employment + wages by SOC 2-digit (GBP→EUR at 1.16) | 2025 |

### Key Numbers
| Metric | Value |
|--------|-------|
| Total EU-27 jobs | 199.6M |
| Occupation groups | 125 (ISCO 3-digit) |
| Countries | 36 (EU-27 + EFTA + UK + candidates) |
| Avg technical exposure | 5.6 |
| Avg EU regulated exposure | 4.4 |
| Avg UK regulated exposure | 5.3 (friction: 0.5) |
| EU regulatory delta | 1.2 points |
| UK regulatory delta | 0.5 points |
| Exposure-weighted wages (technical) | €4.7T |
| Exposure-weighted wages (EU regulated) | €3.7T |
| AI Act relevant groups | 95 of 125 |
| High-risk deployer groups | 40 of 125 |
| Avg overlapping regulatory frameworks | 3.7 per group |

### Site Pages (site/)
| Page | Content |
|------|---------|
| index.html | Interactive D3.js treemap, country selector (36 grouped), technical/regulated toggle, AI Act overlay toggle, stats bar, slide-in detail panel (desktop), bottom sheet (mobile), mobile hero |
| analysis.html | 7 findings sections + author's note + builder's perspective + methodology. Findings: Screen Test, Education Doesn't Protect, Regulatory Buffer, DACH Angle, Enterprises, Workers, Regulatory Compliance Surface |
| questions.html | 11 accordion sections: Macro Picture, Society, Workers, Founders, Corporations, Regulators, EU-27, Austria, Germany, Switzerland, UK. Bottom CTA: "let's build together" |
| sources.html | Full legal reference table: EU-wide (AI Act, Platform Work Dir, Pay Transparency Dir, Data Act, GDPR, Quality Jobs Act), Germany (BetrVG), Austria (ArbVG), Switzerland (FADP, OR 328/328b, ArGV3 Art 26, Mitwirkungsgesetz), UK (Employment Rights Act, Equality Act, DPA 2018, ICE Regs, DSIT framework). Plus academic references (Draghi, Dalio, Mazzucato, EU-Inc). All timestamped 17 March 2026. |

### Frontend Features
- D3.js treemap: area = employment, color = AI exposure (green→red)
- Country selector: grouped (Western/Northern/Southern/Eastern/UK/Candidates) with search, source badges (Eurostat/BFS/ONS)
- Toggle: Technical Exposure ↔ Regulated Exposure (uses UK scores when UK selected)
- AI Act overlay toggle: shows deployer/subject badges, ⚠️📋 icons, legend
- Slide-in detail panel (desktop, 400px overlay from right, click to lock)
- Bottom sheet (mobile, swipe to dismiss)
- Hover tooltip (lightweight, cursor-following, name + score badge)
- Stats bar: total jobs, avg exposure, exposure-weighted wages, regulatory delta, histogram
- Burger menu navigation (desktop: inline links, mobile: slide-down panel)
- Mobile hero (above fold: title + two buttons, "Explore the data ↓" / "Read the analysis →")
- Consistent CTA boxes on all pages with "let's build together" + Nexalps button
- Breadcrumbs on article pages (kept alongside burger menu on desktop)
- Geist font (Google Fonts), shadcn design language, dark theme
- WCAG 2.0 accessibility (aria labels, keyboard nav, focus indicators, score numbers on cells)
- PostHog tracking (EU host, page views + country_changed + score_toggle + cell_clicked + cta_clicked)
- SEO: meta tags, og:image, JSON-LD Dataset schema, sitemap.xml, robots.txt, llms.txt, canonical

### Legal Data (data/legal/)
Full legal texts downloaded and verified for:
- EU AI Act (Regulation 2024/1689) — full text including Annex III, Art 6, Art 26
- Platform Work Directive (Directive 2024/2831)
- Pay Transparency Directive (Directive 2023/970)
- EU Data Act (Regulation 2023/2854)
- GDPR (referenced by article: Art 22, 35, 88)
- German BetrVG (full Arbeitsrechtsgesetz + Betriebsverfassungsgesetz)
- Austrian ArbVG (full Arbeitsverfassungsgesetz, §96, §96a)
- Swiss FADP/DSG, OR Art 328/328b, ArGV3 Art 26, Mitwirkungsgesetz
- UK Employment Rights Act 1996, Equality Act 2010, DPA 2018, ICE Regs 2004

### AI Act Overlay (data/manual/ai_act_high_risk.json)
125 groups mapped against:
- Annex III categories (as subject + as deployer)
- EU obligations (Art 26(7), Art 14, GDPR Art 22)
- Works council triggers (BetrVG §87 for DE, ArbVG §96a for AT)
- Swiss framework (FADP Art 21, OR 328b, ArGV3 Art 26)
- Platform Work Directive relevance
- Pay Transparency Directive relevance
- Regulatory surface count per group

---

## What's NOT Built Yet

### Phase 2 Remaining
| Item | Status | Priority |
|------|--------|----------|
| 2.5 Task-level scoring (ESCO skills) | Not started | After Phase 3.1 |
| 2.6 Cross-source normalization | Not started | After Phase 3.1 |

### Phase 3 (Future)
| Item | Priority | Notes |
|------|----------|-------|
| 3.1 Multi-layer toggle + positive spin | **NEXT** | Cedefop growth projections, pay/education layers, "AI Augmentation Potential" layer. Second LinkedIn launch moment. Inspired by Karpathy v2 adding BLS outlook/pay/education toggles. |
| 3.2 US vs EU transatlantic comparison | After 3.1 | Side-by-side with Karpathy aggregate data. Four-tier regulatory gradient (US→UK→CH→EU→DACH). Third LinkedIn launch. |
| 3.3 Language versions | Later | ESCO supports 27 languages. German first, then FR/ES/IT. |
| 3.4 Additional overlays | Later | Works council trigger map, green jobs overlay (ESCO green skills), Cedefop Skills OVATE vacancy data |
| 3.5 Platform & distribution | Later | Temporal tracking (quarterly re-scoring), embeddable widget, API endpoint, downloadable PDF reports |

### Phase 3.1 Detail (next to build)
Add multiple coloring layers to the treemap (like Karpathy v2):
- Employment Growth (Cedefop Skills Forecast to 2035 + Eurostat YoY change)
- Median Pay (already in data)
- Education Level (Eurostat lfsa_egaed)
- AI Exposure Technical (existing)
- AI Exposure Regulated (existing)
- AI Augmentation Potential (NEW — composite: high exposure + growing demand = opportunity)

Key insight from Karpathy's v2: "A high score does not predict the job will disappear. It predicts the job will change." The augmentation layer reframes the tool from risk to opportunity.

---

## Infrastructure

- **Hosting:** Netlify (static site, publish directory: site/)
- **Domain:** ai-exposure.nexalps.com (CNAME in GoDaddy → Netlify)
- **DNS:** GoDaddy (nexalps.com)
- **Repo:** github.com/Ph1lM4/ai-job-impact-europe
- **API keys needed:** ANTHROPIC_API_KEY in .env (for scoring scripts)
- **PostHog:** EU host (eu.i.posthog.com), project key in index.html
- **Redirects:** site/_redirects has /implications.html → /analysis.html 301
- **Auto-deploy:** Netlify watches main branch, deploys site/ on push

## Project Structure
```
european-ai-exposure-map/
├── data/
│   ├── esco/          # ESCO v1.2.1 CSVs (downloaded manually, gitignored)
│   ├── eurostat/      # Fetched by script (gitignored)
│   ├── bfs/           # Swiss BFS xlsx files (downloaded manually)
│   ├── ons/           # UK ONS xlsx files (downloaded manually)
│   ├── manual/        # ai_act_high_risk.json
│   ├── legal/         # Legal texts (PDFs + text extracts)
│   └── reference/     # (Phase 3: karpathy_us.json)
├── scripts/           # Python pipeline (01-09)
├── site/
│   ├── index.html     # Interactive treemap
│   ├── analysis.html  # 7 findings + author's notes
│   ├── questions.html # 11 accordion sections
│   ├── sources.html   # Legal references table
│   ├── data.json      # Generated by 05_build_site_data.py
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── llms.txt
│   └── _redirects     # Netlify redirects
├── icons/
├── scores.json        # Technical + EU regulated scores
├── uk_scores.json     # UK-specific regulated scores
├── occupations.csv    # 125 groups metadata
├── occupations_by_country.csv  # Long format, ~4500 rows
├── BUILD_PLAN.md
├── phase2-build-plan.md
├── README.md
├── LICENSE-CODE       # MIT
├── LICENSE-DATA       # CC-BY 4.0
├── pyproject.toml
└── .env               # ANTHROPIC_API_KEY (gitignored)
```

---

## LinkedIn Launch Status

**Post 1 published:** Wednesday 19 March 2026, ~7:45 CET
- Personal profile (Philipp Maul) — updated to Nexalps founder
- Nexalps company page repost (2-3 hours later)
- 4 link comments: map, analysis, questions, GitHub
- ~10 friends seeded for early engagement
- Active comment engagement throughout the day

**Planned future posts:**
- Post 2 (Thu/Fri): Builder's angle — "I built this in a weekend, not because I'm a data scientist..."
- Post 3 (next week): Germany-specific — BetrVG §87 and works council implications
- Post 4: Regulatory gradient (US→UK→CH→EU→DACH)
- Post 5: Builder's perspective — "regulation as substitute vs foundation for building"
- Post 6: Swiss angle for Zurich network
- Post 7 (after Phase 3.1): Second launch — "we added growth projections, here's where AI creates opportunity"
- Post 8: UK natural experiment

**Timing:** Tuesday-Thursday, 7:30-8:30 CET. No external links in post body (link in comments). Reply to every comment within 2 hours.

---

## Key Files to Reference in New Sessions

- `BUILD_PLAN.md` — original architecture and pipeline design
- `phase2-build-plan.md` — Phase 2 specs, Phase 3 roadmap, priority order
- `data/manual/ai_act_high_risk.json` — regulatory overlay mapping
- `scores.json` — all technical + EU regulated scores
- `uk_scores.json` — UK-specific regulated scores
- `site/data.json` — everything the frontend consumes

## Key Decisions Made
- ISCO 3-digit level (~125 groups) for treemap granularity
- Score TECHNICAL capability separately from regulatory friction
- EU regulated score applies to all EU/EFTA countries
- UK gets separate regulated score (lighter framework)
- Switzerland uses Eurostat employment + BFS wages (fresher)
- Wage data noted as SES 2022 without inflation adjustment (Phase 2.6)
- All legal citations verified against primary source texts as of 17 March 2026
- "Let's build together" as unified CTA across all pages
- Nexalps positioned as builder, not advisor
- Author's note + builder's perspective separated from analysis
