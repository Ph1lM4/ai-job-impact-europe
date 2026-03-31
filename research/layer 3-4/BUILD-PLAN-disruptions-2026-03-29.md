# Build Plan: Layer 3 — Historic Technology Disruptions

**Product:** disruptions.nexalps.com
**Status:** Ready for build
**Answers:** "What happened every other time?"

---

## Context

Product 3 of 6 in the Nexalps European AI Labour Market suite. Layer 1 (ai-exposure.nexalps.com) shows which jobs AI hits. Layer 2 (job-market.nexalps.com) shows where demand is going. Layer 3 shows the historical record: 580 years of technology disruptions, 19 case studies, and what actually happened to the workers.

Three research files (~60K words) are complete and audited.

---

## Design System (exact specs — fork from Layer 2 index.html)

### CSS Custom Properties

```css
:root {
  --background: #09090b;
  --foreground: #fafafa;
  --card: #0a0a0c;
  --card-border: rgba(255,255,255,0.08);
  --muted: #a1a1aa;
  --muted-foreground: #71717a;
  --accent: #27272a;
  --border: rgba(255,255,255,0.12);
  --input-border: rgba(255,255,255,0.15);
  --ring: #f97316;                /* Orange accent — primary action color */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --font: 'Geist', system-ui, -apple-system, sans-serif;
  --transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Typography

- **Font:** Geist (Google Fonts), weights 400/500/600/700
- **Load:** `<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">`
- **h1 (hero):** 36px, weight 700, letter-spacing -0.03em, line-height 1.15
- **h2 (section):** 22px, weight 700, letter-spacing -0.02em, margin 48px 0 8px
- **h2 .num:** color var(--ring), weight 700
- **h2 .subtitle:** display block, 14px, weight 400, color var(--muted)
- **Body text:** 16px, color #d4d4d8, line-height 1.8
- **Lede:** 18px, weight 400, color var(--muted), line-height 1.7
- **Labels:** 11px, uppercase, letter-spacing 0.05em
- **Stat values:** 24px (desktop), 20px (mobile), weight 700

### Color Scales (D3.js charts)

```javascript
// Risk scale (low=green → high=red)
risk: domain [0,2,4,6,8,10] → range ["#22c55e","#84cc16","#eab308","#f97316","#ef4444","#dc2626"]

// Diverging scale (red → green)
diverging: domain [0,2,4,6,8,10] → range ["#dc2626","#ef4444","#eab308","#84cc16","#22c55e","#16a34a"]
```

### Component Patterns

**Stat Card:**
```css
.stat-card {
  background: var(--card);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-lg);    /* 12px */
  padding: 16px 20px;
}
.stat-card .stat-value { font-size: 24px; font-weight: 700; }
.stat-card .stat-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
.stat-card .stat-sublabel { font-size: 10px; opacity: 0.7; }
```

**Accordion:**
```css
.accordion-trigger {
  cursor: pointer; padding: 20px 36px 20px 0;
  font-size: 17px; font-weight: 600; color: var(--muted);
}
.accordion-trigger:hover { color: var(--ring); }
.accordion-trigger .num { color: var(--ring); font-weight: 700; margin-right: 8px; }
.accordion-trigger::after {
  content: "+"; position: absolute; right: 0; top: 50%;
  width: 28px; height: 28px; border-radius: 6px; background: var(--accent);
}
.accordion-trigger[aria-expanded="true"]::after { content: "−"; }
.accordion-content { max-height: 0; overflow: hidden; transition: max-height 300ms ease; }
```

**Highlight Box:**
```css
.highlight {
  margin: 24px 0; padding: 16px 20px;
  background: rgba(249, 115, 22, 0.06);
  border-left: 3px solid var(--ring);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
```

**Author Note:**
```css
.author-note {
  padding: 24px 28px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: var(--radius-lg);
}
.author-note h3 { font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
.author-note .sig { margin-top: 16px; font-size: 14px; font-weight: 500; color: var(--muted-foreground); }
```

**Data Table:**
```css
.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th { text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; padding: 8px 12px; border-bottom: 1px solid var(--border); }
.data-table td { padding: 10px 12px; color: #d4d4d8; border-bottom: 1px solid var(--card-border); }
.data-table td:last-child { font-weight: 600; color: var(--ring); }
```

**CTA Bar:**
```css
.cta-bar {
  max-width: 760px; padding: 32px 24px;
  background: var(--card); border: 1px solid var(--card-border);
  border-radius: var(--radius-lg); text-align: center;
}
.btn { padding: 10px 24px; background: var(--ring); color: #000; font-weight: 600; border-radius: var(--radius-md); }
.btn-outline { background: transparent; color: var(--muted); border: 1px solid var(--border); }
```

**Source Tier Badges:**
```css
.source-badge { font-size: 10px; padding: 1px 6px; border-radius: 9999px; font-weight: 600; }
.tier-1 { background: rgba(34,197,94,0.12); color: #86efac; border: 1px solid rgba(34,197,94,0.2); }
.tier-2 { background: rgba(234,179,8,0.12); color: #fde047; border: 1px solid rgba(234,179,8,0.2); }
.tier-3 { background: rgba(239,68,68,0.12); color: #fca5a5; border: 1px solid rgba(239,68,68,0.2); }
```

**Disruption Type Badges (NEW for Layer 3):**
```css
.type-badge { display: inline-block; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 500; }
.type-1 { background: rgba(34,197,94,0.12); color: #86efac; border: 1px solid rgba(34,197,94,0.2); }   /* green — expansion */
.type-2 { background: rgba(239,68,68,0.12); color: #fca5a5; border: 1px solid rgba(239,68,68,0.2); }   /* red — elimination */
.type-3 { background: rgba(234,179,8,0.12); color: #fde047; border: 1px solid rgba(234,179,8,0.2); }   /* amber — absorption */
.type-4 { background: rgba(249,115,22,0.12); color: #fdba74; border: 1px solid rgba(249,115,22,0.2); } /* orange — restructuring */
.type-5 { background: rgba(59,130,246,0.12); color: #93c5fd; border: 1px solid rgba(59,130,246,0.2); } /* blue — demand creation */
```

### Navigation (fixed top, same as Layer 2)

```html
<nav class="site-nav" role="navigation" aria-label="Main navigation">
  <div class="site-nav-links">
    <a href="index.html">Overview</a>
    <a href="cases.html">Case Studies</a>
    <a href="outcomes.html">Worker Outcomes</a>
    <a href="sources.html">Sources</a>
    <span class="nav-sep"></span>
    <a href="https://ai-exposure.nexalps.com/" target="_blank" rel="noopener">AI Exposure Map ↗</a>
    <a href="https://job-market.nexalps.com/" target="_blank" rel="noopener">Job Market ↗</a>
  </div>
  <!-- Mobile: .burger button with 3 spans, .burger-panel overlay -->
</nav>
```

```css
.site-nav { position: fixed; top: 0; z-index: 9999; pointer-events: none; }
.site-nav-links { display: flex; gap: 20px; backdrop-filter: blur(12px); pointer-events: auto; }
.site-nav-links a { font-size: 13px; font-weight: 500; color: var(--muted); text-decoration: none; }
.site-nav-links a:hover { color: var(--foreground); }
.site-nav-links a[aria-current="page"] { color: var(--ring); }
```

### Responsive Breakpoints

- **Desktop (>768px):** Full layout, multi-column grids, inline charts
- **Tablet/Mobile (≤768px):** Hamburger menu, stat cards 2-col grid, single-col content, container padding 16px
- **Small Mobile (≤480px):** h1 20px, stat values 18px, cards stack fully

### Footer

```html
<footer class="footer container" role="contentinfo">
  Historic Technology Disruptions &middot; 2026 &middot;
  <a href="cases.html">Case Studies</a> &middot;
  <a href="outcomes.html">Worker Outcomes</a> &middot;
  <a href="sources.html">Sources</a><br>
  Built by <a href="https://www.linkedin.com/in/pmaul/">Philipp Maul</a> &middot;
  <a href="https://nexalps.com">Nexalps</a> &mdash; Turning complexity into competitive advantage.
</footer>
```

```css
.footer { padding: 20px 0 36px; font-size: 12px; color: var(--muted-foreground); line-height: 1.7; }
.footer a { color: var(--muted); text-decoration: underline; text-underline-offset: 2px; }
```

### Analytics (PostHog)

```javascript
posthog.init('phc_bjax6jdRxYJAaExodvALjRru8AQzUSbYFNlWlXiJM8A', {
  api_host: 'https://eu.i.posthog.com',
  person_profiles: 'identified_only'
});
// Track: accordion_opened, cta_clicked, chart_interacted, case_viewed
```

### SEO (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "What Happened Every Other Time: Historic Technology Disruptions and European Labour",
  "description": "19 technology disruption case studies spanning 580 years, analysed for patterns that predict AI's impact on European labour markets.",
  "url": "https://disruptions.nexalps.com/",
  "datePublished": "2026-04-XX",
  "author": { "@type": "Person", "name": "Philipp Maul", "url": "https://www.linkedin.com/in/pmaul/", "affiliation": { "@type": "Organization", "name": "Nexalps", "url": "https://nexalps.com" } },
  "publisher": { "@type": "Organization", "name": "Nexalps", "url": "https://nexalps.com" },
  "keywords": ["technology disruption", "labour market", "AI impact", "GPT history", "displaced workers", "European labour", "automation", "retraining"]
}
```

Meta tags: og:type, og:title, og:description, og:url, og:site_name, twitter:card (summary_large_image), canonical URL per page.

### Accessibility

**Target:** Lighthouse accessibility score >90. Follow WCAG 2.1 AA.

**Structural:**
- Skip link as first focusable element: `<a href="#main" class="skip-link">Skip to content</a>`
- All pages wrapped in `<main id="main">` with `role="main"`
- Nav: `role="navigation"`, `aria-label="Main navigation"`
- Footer: `role="contentinfo"`
- Stat cards section: `role="region"`, `aria-label="Summary statistics"`

**Accordions:**
- Trigger: `<button>` element (not `<div>` or `<a>`)
- `aria-expanded="true|false"` toggled on click
- `aria-controls="section-{id}"` pointing to content panel
- Content panel: `role="region"`, `id` matching `aria-controls`
- Keyboard: Enter/Space toggles, Tab navigates between triggers

**Charts (D3):**
- Every chart wrapped in `role="img"` container with `aria-label` describing the data story (e.g., "Timeline showing 9 technology disruptions from 1440 to 2022, with adoption arcs compressing from 160 years to 15 years")
- Hidden `<table>` or `<dl>` fallback inside a `<details>` element below each chart: "View data as table"
- No information conveyed by color alone — use shape/pattern/label as secondary channel
- Chart tooltips accessible via keyboard focus (not hover-only)

**Tables:**
- `<caption>` on every `<table>` describing content
- `<th scope="col">` for column headers, `<th scope="row">` for row headers
- Sortable tables: `aria-sort="ascending|descending|none"` on active column header

**Images/Icons:**
- Decorative icons: `aria-hidden="true"`
- Direction arrows in badges: include screen-reader text (e.g., `<span class="sr-only">growing</span>`)

**Color contrast:**
- All text meets 4.5:1 ratio against `--background` (#09090b)
- `--foreground` (#fafafa) on `--background`: 19.4:1 ✓
- `--muted` (#a1a1aa) on `--background`: 7.2:1 ✓
- `--ring` (#f97316) on `--background`: 5.7:1 ✓
- `--muted-foreground` (#71717a) on `--background`: 4.6:1 ✓ (barely — avoid for small text)

**Focus states:**
- `:focus-visible` outline: `2px solid var(--ring)`, `outline-offset: 2px`
- No `:focus` suppression without `:focus-visible` replacement

**Reduced motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

### llms.txt

```markdown
# What Happened Every Other Time: Historic Technology Disruptions and European Labour
> https://disruptions.nexalps.com/

## What this is
Product 3 of 6 in the Nexalps European AI Labour Market suite. Analyses 580 years of technology disruptions to extract patterns that predict how AI will reshape European labour markets.

## Key findings
- Every general purpose technology follows a 20-50 year arc from invention to productivity gains
- Disruptions follow 5 distinct patterns: Transformation+Expansion, Elimination, Absorption, Restructuring, Demand Creation
- 6 diagnostic variables predict which pattern an occupation will follow
- Retraining programmes show "modest positive effects at best" (207-study meta-analysis)
- Worker recovery collapses after age 50: reemployment probability halved, earnings loss doubled
- Geographic scarring lasts 30-50 years (UK coalfields, US Rust Belt — still no convergence)
- European institutional frameworks (works councils, Kurzarbeit, co-determination) produce measurably different outcomes than US flexibility
- Children of displaced workers earn 9% less — displacement transmits across generations
- AI is currently a net hiring driver in Europe (ECB SAFE survey, 5,300 firms, March 2026)
- 25% of German firms expect AI job cuts within 5 years (ifo 2025) — displacement is delayed, not cancelled

## 19 case studies analysed
### 9 Macro (General Purpose Technologies)
1. Printing Press (1440s-1600s) — 160-year arc
2. Mechanised Loom (1760s-1850s) — 90-year arc
3. Steam/Railways (1800s-1870s) — 70-year arc
4. Electricity (1880s-1930s) — 50-year arc, 40-year productivity lag
5. Assembly Line (1910s-1950s) — 40-year arc
6. Computer/Mainframe (1950s-1980s) — 40-year arc, Solow paradox
7. PC/Office Automation (1980s-2000s) — 25-year arc
8. Internet/E-commerce (1995-2015) — 20-year arc
9. Mobile/Platform Economy (2007-2020) — 13-year arc

### 10 Micro (Occupation-Level)
1. ATMs → Bank Tellers — Type 1 (employment doubled before mobile banking reversed it)
2. Spreadsheets → Accountants — Type 1 (market expansion, accountants grew)
3. Containerisation → Dockworkers — Type 2 (90%+ reduction, 40-year geographic scarring)
4. CAD → Technical Drafters — Type 3 (role absorbed into engineering)
5. Telephone Operators — Type 2 (full elimination over 60 years)
6. Elevator Operators — Type 2 (50-year adoption despite mature technology)
7. DTP → Typesetters — Type 2 (high-skill role eliminated in 15 years)
8. Industrial Robots → Manufacturing — Type 1/2 hybrid (Germany vs US divergence)
9. GPS/Ride-hailing → Taxi — Type 3 + Type 4 (absorption + restructuring)
10. E-commerce → Retail — Type 1 transitioning to Type 4

## 5 disruption pattern types
- Type 1: Transformation + Market Expansion (ATM pattern)
- Type 2: Full Task Automation → Elimination (containerisation pattern)
- Type 3: Role Absorption (CAD/drafting pattern)
- Type 4: Market Restructuring (Uber/taxi pattern)
- Type 5: Demand Creation (new occupations)

## Pages
- index.html — Overview: GPT timeline, disruption taxonomy, 10 key patterns
- cases.html — 19 case study deep dives with ISCO codes
- outcomes.html — 8 displaced worker outcomes, retraining evidence, age gradient
- sources.html — ~45 academic and institutional sources with tier ratings
- disruptions-data.json — Machine-readable structured data

## Data sources (~45 primary)
Tier 1: Dittmar (QJE 2011), Paul David (AER 1990), Acemoglu & Restrepo (JPE 2020), Feigenbaum & Gross (QJE 2024), Card/Kluve/Weber meta-analysis, Autor/Dorn/Hanson, Dauth et al. (CEPR 2017), BLS OEWS, Eurostat
Tier 2: IFR World Robotics, McKinsey, BLS Beyond the Numbers, Burning Glass Institute
Tier 3: Levinson (The Box), Thompson (Making of the English Working Class)

## Connection to other products
- ai-exposure.nexalps.com = which jobs AI hits (130 ISCO groups × 36 countries)
- job-market.nexalps.com = where demand is going (9 roles × 34 countries)
- disruptions.nexalps.com = what happened every other time (19 case studies × 580 years)
- ISCO-08 codes bridge all three products
- Same design system (shadcn dark, Geist font, #f97316 orange accent)

## Author
Philipp Maul, Nexalps (https://nexalps.com)
Licensed under CC-BY 4.0
```

### Hosting & CI

- **Hosting:** Static site (same as Layer 1 and 2 — likely Netlify or similar)
- **`_redirects`:** Same pattern as Layer 1 (`/* /index.html 200` if SPA, or none for pure static)
- **Deploy:** Manual push to hosting platform (same workflow as existing sites)
- **Domain:** `disruptions.nexalps.com` — DNS CNAME to hosting provider
- **SSL:** Automatic via hosting provider (same as existing subdomains)

---

## Architecture: 4 pages + data JSON

```
european-disruptions-map/site/
├── index.html              → Overview: timeline + taxonomy + patterns
├── cases.html              → 19 case study accordions (9 macro + 10 micro)
├── outcomes.html           → 8 displaced worker cases + retraining evidence
├── sources.html            → Bibliography with tier badges
├── disruptions-data.json   → All structured data
├── llms.txt                → Machine-readable summary
├── robots.txt
├── sitemap.xml
└── _redirects
```

**Why 3 content pages:** 60K words on one page is unusable. The three research files map cleanly to three questions: (1) What's the macro pattern? (index), (2) What happens to specific occupations? (cases), (3) What happens to the workers? (outcomes).

---

## Page Specifications

### index.html — "What Happened Every Other Time"

**Hero:** Title + lede + byline + 4 stat cards:
- "580 years" / Of disruption data / Printing press (1440) to AI (2022)
- "20–50 yrs" / Median adoption lag / Invention to measurable productivity
- "5 types" / Disruption patterns / Transform, Eliminate, Absorb, Restructure, Create
- "90%" / Worst-case job loss / Containerisation of dock work

**Section 1 — GPT Timeline:** Interactive D3 horizontal Gantt chart. 10 rows (9 GPTs + AI). Each row = 4 color-coded segments (invention → adoption → productivity → restructuring). AI row has "?" markers. Hover tooltips with dates and notes.

**Section 2 — Disruption Taxonomy:** 5 cards in a 3-col grid (Type 1–5), each with name, definition, example case badges, color-coded left border (green/red/amber/orange/blue). Below: diagnostic framework as responsive data table (6 variables × 5 types).

**Section 3 — Ten Patterns:** 10 numbered highlight boxes (orange left border, `.highlight` component). One pattern per box with bold name + 2-3 sentence summary + inline source badge.

**Section 4 — European Divergence:** `.author-note` component. C.3 content: same technology, different outcomes based on institutional framework.

**CTA bar** → cases.html + outcomes.html + ai-exposure.nexalps.com

### cases.html — "19 Disruptions, 19 Lessons"

**Hero:** Title + lede (no stat cards).

**Section 1 — Macro Disruptions:** 9 accordions. Trigger: "[#]. [Technology] ([date range])" + arc duration badge. Expanded: "The world before" → "What happened" → "The J-curve" → "European variation" → "Relevance to AI". Inline source badges.

**Section 2 — Micro Disruptions:** 10 accordions. Trigger: "[#]. [Technology] → [Occupation] ([dates])" + disruption Type badge (colored pill). Expanded: Prediction → Actual outcome → Mechanism → Timescale → Winners/losers → ISCO code with deep link to ai-exposure.nexalps.com. Employment mini-charts (sparklines) for 5-6 key cases.

**Section 3 — Timescale Comparison:** Sortable data table (10 rows × 4 cols: Case, Tech ready, Employment peak, Near-complete, Total span). Plus D3 horizontal bar chart showing stacked durations.

**CTA bar** → outcomes.html

### outcomes.html — "What Actually Happened to Displaced Workers"

**Hero:** Title + lede + 3 stat cards:
- "$3,300 less" / TAA retraining outcome / Participants earned less than non-participants after 4 years
- "Age 50" / Recovery threshold / Reemployment probability collapses; earnings halved
- "30–50 yrs" / Geographic scarring / UK coalfields, Rust Belt — still no recovery

**Section 1 — Retraining Pipeline:** D3 funnel chart (100 eligible → 60 train → 48 complete → 18 get jobs). Prose on 207-study meta-analysis. Kurzarbeit contrast as highlight box.

**Section 2 — Eight Cases:** 8 accordions. Each with case summary, key data in bold, community impact, institutional response.

**Section 3 — Age Gradient:** D3 dual-axis bar chart. X = age bands (25-34 through 65+). Left Y = reemployment rate (green bars). Right Y = earnings loss (red bars). The cliff at 50 is the story.

**Section 4 — Geographic Scarring:** Prose with key examples (UK coalfields 40 yrs, Detroit 60% pop loss, Pittsburgh as exception). Intergenerational data (9% earnings penalty for children).

**Section 5 — Ten Predictions for AI:** Highlight boxes framing the 10 patterns as forward-looking predictions. Cross-links to Layer 1 and Layer 2.

**Author's note** → synthesis on generational replacement vs worker transition.

**CTA bar** → ai-exposure.nexalps.com + job-market.nexalps.com

### sources.html — Bibliography

Same structure as Layer 2 sources.html. ~45 sources grouped by tier with badges. Tier 1 (peer-reviewed/government): Dittmar, David, Acemoglu, Feigenbaum & Gross, Card/Kluve/Weber, etc. Tier 2 (institutional): BLS, IFR, McKinsey. Tier 3 (secondary): Levinson, Thompson.

---

## Data Architecture: disruptions-data.json

```json
{
  "meta": { "title": "...", "last_updated": "2026-04-XX", "source_count": 45, "case_count": 19 },
  "gpt_timeline": [ { "id": "printing_press", "label": "...", "invention_year": 1440, "mass_adoption_year": 1480, "productivity_visible_year": 1510, "full_restructuring_year": 1580, "total_arc_years": 160, notes per phase } × 10 ],
  "micro_disruptions": [ { "id": "atm_tellers", "technology": "ATMs", "occupation": "Bank Tellers", "disruption_type": 1, "isco_codes": ["4211"], "peak_employment": 608000, timeline years, mechanism, winners/losers } × 10 ],
  "displaced_worker_cases": [ { "id": "handloom_weavers", employment/wage data, recovery type, scarring data } × 8 ],
  "disruption_taxonomy": { 5 types with color, description, cases, 6-variable diagnostic },
  "retraining_evidence": { taa_evaluation with pipeline funnel, meta_analysis (207 studies), kurzarbeit stats },
  "age_gradient": [ { age_band, reemployment_rate, earnings_loss_pct } × 5 ],
  "timescale_comparison": [ { case, tech_ready, employment_peak, near_complete, total_span } × 10 ],
  "cross_cutting": { acceleration, this_time_different, european_divergence summaries },
  "sources": [ { id, tier, title, author, year, type, url } × ~45 ]
}
```

---

## Visualizations (6 D3 charts)

| # | Chart | Page | Type | Key data |
|---|---|---|---|---|
| 1 | GPT Adoption Timeline | index.html | Horizontal Gantt | 10 GPTs × 4 phases, color-coded segments |
| 2 | Timescale Comparison | cases.html | Horizontal stacked bar | 10 disruptions sorted by total span |
| 3 | Retraining Funnel | outcomes.html | Funnel/waterfall | 100 → 60 → 48 → 18 pipeline |
| 4 | Age-Reemployment Gradient | outcomes.html | Dual-axis bar | 5 age bands × reemployment + earnings loss |
| 5 | Employment Sparklines | cases.html | Inline sparklines | 5-6 key cases (tellers, weavers, dockworkers) |
| 6 | Diagnostic Framework | index.html | Styled HTML table | 6 variables × 5 types (not D3) |

---

## Cross-Linking

**Layer 3 → Layer 1:** Each micro-disruption with ISCO code links to `ai-exposure.nexalps.com/?occ=XXXX`. 9 of 10 cases have ISCO codes.

**Layer 3 → Layer 2:** Predictions section cross-links to job-market.nexalps.com (seniority shift = generational replacement pattern; junior collapse = historical precedent).

**Layers 1 & 2 → Layer 3:** Add "Historic Disruptions" to nav bars on both existing sites. Contextual cross-links in analysis.html content where institutional friction and historical patterns are discussed.

**Deep linking:** `disruptions.nexalps.com/cases.html#atm-tellers` auto-opens accordion (same JS pattern as Layer 2).

---

## Build Sequence

| Sprint | Days | Tasks | Gate |
|---|---|---|---|
| **1: Data** | 1-2 | Create project dir, extract all data from 3 research files into disruptions-data.json, create llms.txt | JSON loads and validates |
| **2: index.html** | 2-4 | Full page: nav, hero, GPT timeline chart, taxonomy cards, diagnostic table, 10 patterns, author note, CTA, footer, responsive, a11y | Page renders at all breakpoints, chart interactive |
| **3: cases.html** | 4-6 | 19 accordions (9 macro + 10 micro), type badges, ISCO links, timescale table + chart, employment sparklines | All accordions work, links valid |
| **4: outcomes.html** | 5-7 | Hero, retraining funnel, 8 case accordions, age gradient chart, geographic scarring, 10 predictions, author note | All sections render, charts work |
| **5: Polish** | 7-8 | sources.html, cross-link verification, update Layer 1 + 2 navs, PostHog events, SEO check, performance, final responsive pass | Lighthouse >90, all cross-links work |
| **6: Deploy** | 8-9 | Deploy to disruptions.nexalps.com, update existing site navs in production, verify | Live and cross-linked |

Sprints 3 and 4 are parallelizable after Sprint 2 establishes the CSS base.

---

## Critical Reference Files

| File | Purpose |
|---|---|
| `/projects/european-careers-map/site/index.html` | Fork for: nav, stat cards, accordions, D3 integration, PostHog, responsive, burger menu |
| `/projects/european-careers-map/site/sources.html` | Fork for: tier badges, bibliography layout |
| `/projects/european-ai-exposure-map/site/analysis.html` | Reference for: `.highlight` boxes, `.author-note`, `.data-table`, finding sections |
| `research/layer 3-4/Nine disruptions*.md` | Content source: 9 macro disruptions + GPT timeline table + cross-cutting analysis |
| `research/layer 3-4/Ten micro-disruptions*.md` | Content source: 10 micro disruptions + taxonomy + diagnostic framework + timescale table |
| `research/layer 3-4/What actually happened*.md` | Content source: 8 worker outcomes + retraining evidence + age/geographic data |

---

## Verification

1. **Data accuracy:** Every number in disruptions-data.json traces to a cited source in the research files
2. **Cross-links:** Test all links between disruptions ↔ ai-exposure ↔ job-market
3. **ISCO deep links:** Verify 9 ISCO codes resolve correctly on ai-exposure.nexalps.com
4. **Mobile:** Test at 375px, 768px, 1280px
5. **Accessibility:** Tab navigation through all accordions, ARIA expanded states, chart alt text
6. **Performance:** Page load < 2s, D3 charts don't block initial render (defer chart rendering)
7. **PostHog:** Verify events fire for accordion opens, CTA clicks, chart interactions
