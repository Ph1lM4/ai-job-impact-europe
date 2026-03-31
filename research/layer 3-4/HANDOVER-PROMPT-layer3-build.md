# Session Handover — Layer 3 Build: disruptions.nexalps.com

## Your task

Build **disruptions.nexalps.com** — a static site presenting 580 years of historic technology disruptions and their impact on labour markets. This is Product 3 of 6 in the Nexalps European AI Labour Market suite.

## Critical files to read first (in this order)

1. **Build plan (read fully before doing anything):**
   `/Users/philippmaul/Documents/projects/european-ai-exposure-map/research/layer 3-4/BUILD-PLAN-disruptions-2026-03-29.md`
   — Contains complete specs: architecture, page structure, design system (CSS variables, typography, components), data architecture (JSON schema), 6 D3 chart specifications, accessibility rules, llms.txt content, hosting/CI, cross-linking, and sprint-by-sprint build sequence.

2. **Template to fork (the primary code reference):**
   `/Users/philippmaul/Documents/projects/european-careers-map/site/index.html`
   — This is the Layer 2 site. Fork its exact patterns: nav bar, stat cards, accordions, D3 chart integration, PostHog setup, responsive breakpoints, burger menu JS, footer. The build plan specifies all CSS values explicitly, but this file is the working implementation.

3. **Secondary code references:**
   - `/Users/philippmaul/Documents/projects/european-ai-exposure-map/site/analysis.html` — for `.highlight` boxes, `.author-note`, `.data-table`, finding sections
   - `/Users/philippmaul/Documents/projects/european-careers-map/site/sources.html` — for tier badges and bibliography layout
   - `/Users/philippmaul/Documents/projects/european-careers-map/site/job-market-data.json` — for JSON data architecture pattern

4. **Content sources (the research to extract data from):**
   All in `/Users/philippmaul/Documents/projects/european-ai-exposure-map/research/layer 3-4/`:
   - `Nine disruptions, one pattern-what GPT history tells us about AI and European labour-claude.md` — 9 macro GPT case studies + GPT adoption timeline table + cross-cutting analysis (acceleration, "this time different", EU vs US)
   - `Ten micro-disruptions reveal how technology reshapes occupations-claude.md` — 10 occupation-level case studies + 5-type disruption taxonomy + diagnostic framework + timescale comparison table
   - `What actually happened to displaced workers- eight cases, one pattern-claude.md` — 8 displaced worker outcomes + retraining evidence (207-study meta-analysis) + age-50 threshold + geographic scarring

## What to build

**4 HTML pages + 1 JSON data file + llms.txt + robots.txt + sitemap.xml**

```
/Users/philippmaul/Documents/projects/european-disruptions-map/site/
├── index.html              → Overview: GPT timeline chart, taxonomy cards, 10 patterns, EU divergence
├── cases.html              → 19 accordion case studies (9 macro + 10 micro) with ISCO links
├── outcomes.html           → 8 displaced worker cases, retraining funnel, age gradient chart
├── sources.html            → ~45 sources with tier badges
├── disruptions-data.json   → All structured data (extracted from the 3 research files)
├── llms.txt                → Content specified in build plan
├── robots.txt
├── sitemap.xml
└── _redirects
```

## Build sequence

Follow the sprints in the build plan:

1. **Sprint 1 (Data):** Create project dir. Extract all structured data from the 3 research files into `disruptions-data.json`. The JSON schema is fully specified in the build plan. Create `llms.txt` (content in build plan).

2. **Sprint 2 (index.html):** Hero + 4 stat cards + GPT Timeline D3 Gantt chart + 5 taxonomy cards + diagnostic framework table + 10 patterns as highlight boxes + European divergence author note + CTA bar + footer. This establishes the CSS base that Sprints 3-4 reuse.

3. **Sprint 3 (cases.html):** 9 macro disruption accordions + 10 micro disruption accordions with Type badges and ISCO deep links to ai-exposure.nexalps.com + timescale comparison table + D3 bar chart + employment sparklines for 5-6 key cases.

4. **Sprint 4 (outcomes.html):** 3 stat cards + D3 retraining funnel chart + 8 displaced worker accordions + D3 age-reemployment gradient chart + geographic scarring section + 10 predictions as highlight boxes + author note.

5. **Sprint 5 (Polish):** sources.html + cross-link verification + PostHog events + SEO check + responsive pass + accessibility pass.

## Key rules

- **Design system:** Every CSS value is specified in the build plan. Use those exact values. Do not invent new colors, font sizes, or spacing.
- **Accessibility:** Lighthouse >90. WCAG 2.1 AA. Accordions use `<button>` with `aria-expanded`. Charts have `aria-label` + hidden data table fallback. Skip link. `prefers-reduced-motion` media query. All specs in the build plan.
- **Data accuracy:** Every number in the JSON must trace to the research files. Do not hallucinate statistics.
- **Progressive disclosure:** Visual first (charts, cards) → content scan (headings, bold data) → deep dive (accordion content). No walls of text before the first visual element.
- **Cross-links:** Each micro-disruption with an ISCO code links to `ai-exposure.nexalps.com`. The nav links to all 3 products. Deep linking via hash anchors on accordions (e.g., `cases.html#atm-tellers`).
- **No backend:** Pure static site. Data loaded via `fetch('disruptions-data.json')`. D3.js loaded from CDN.

## Gate checks (verify at each sprint)

- Sprint 1: `disruptions-data.json` loads, validates, contains all 19 cases + all source references
- Sprint 2: index.html renders at 375px/768px/1280px, GPT timeline chart is interactive, no console errors
- Sprint 3: All 19 accordions open/close, ISCO links resolve, sparklines render
- Sprint 4: Retraining funnel + age gradient charts render, all 8 cases display
- Sprint 5: All cross-links work, Lighthouse >90 accessibility + performance, PostHog events fire
