# Plan: State of the European Job Market in Early 2026

**Status:** FINAL DRAFT — ready for approval

---

## Context

The AI Exposure Map (ai-exposure.nexalps.com) answers: *"Which jobs does AI hit?"* — 130 ISCO occupation groups × 36 countries × 7 layers (technical exposure, regulated exposure, pay, growth, education, adoption, augmentation).

This companion product answers the other side: *"Where is the job market actually going, and what do you need to get there?"*

**Title:** "State of the European Job Market in Early 2026" — borrowing Lenny Rachitsky's proven framing but for Europe, with depth Lenny doesn't have (regulatory layer, country-level data, 9 role deep dives, connection to AI exposure scores).

Built on the same frontend stack (static site, D3.js, Geist font, shadcn dark theme), same data.json architecture, same nav — but a different lens: **role-level career intelligence** instead of occupation-level exposure scores.

---

## Phase 1: SPECIFY (User Journeys + Success Criteria)

### Who Uses This

**Individual Contributors (all levels):**
- Junior: "How do I break into the market when entry-level roles are disappearing?"
- Mid-level: "I'm a PM in Germany — should I be worried? What should I learn?"
- Senior: "I'm switching from ops to product — what's the demand?"

**Managers & Team Leads:**
- "How do I restructure my team given AI?"
- "What should I screen for when hiring?"
- "How do I develop my junior pipeline when entry-level is collapsing?"
- "How does MY role change? What does 'manager' mean when teams shrink and AI handles execution?"
- "Do I need to become more technical, or more strategic, or both?"

**Leadership (VP/C-level/Founders):**
- "What does our hiring strategy look like for 2026-2027?"
- "Where should we invest in talent vs. AI tooling?"
- "What regulatory roles do we need that we don't have?"
- "How does the C-suite itself change? Do we need a Chief AI Officer? What happens to the COO role?"
- "My own role is being reshaped by AI too — what's the exposure of leadership functions?"

**Content consumers (social media, newsletters):**
- Shareable insights, quotable data points
- Expert credibility for Phil's consulting positioning

### What It Shows

1. **Demand Direction** — 9 role families × growing/flat/shrinking, backed by Ravio ground truth
2. **The Seniority Shift** — junior collapse (-73%) vs senior premium, per role + what this means for younger generations
3. **AI Premium** — 12% salary premium, 88% AI/ML hiring growth
4. **Country Hiring Heat** — European countries, which markets are expanding/contracting
5. **Role Deep Dives** — for each of the 9 roles: what's asked for now, what will be asked for, how to futureproof
6. **Skills That Protect** — cross-role skill matrix at each level (junior → senior → leadership)
7. **IC vs Management Tracks** — how both career paths are changing under AI, what's needed in the future for each
8. **The Junior Playbook** — dedicated section for career starters: how to break in when entry-level is shrinking, including the "start your own company" path (it's never been easier)
9. **Regulatory Demand Creation** — EU-specific jobs with expiration probability (permanent vs window of opportunity)
10. **Leadership Impact** — how manager and C-level roles themselves are being reshaped

### The 8 Role Families

| # | Role Family | Why Included |
|---|---|---|
| 1 | **Product Management** | PM-to-designer ratio flipped, AI PM emerging, junior PM vanishing |
| 2 | **Engineering** | Largest volume, AI/ML bifurcation, entry-level collapse |
| 3 | **Design** | The outlier — flat while everything else recovered. Canary for AI displacement |
| 4 | **Sales (SDR/BDR/AE)** | SDR/BDR most AI-disrupted role. AE growing. Structural restructuring |
| 5 | **Business Development** | Partnerships + strategic alliances growing (+34.9% on TrueUp). Distinct from transactional sales |
| 6 | **Growth & Marketing** | Only growing function (commercial 34.7%). Brand vs performance split |
| 7 | **Operations** | Bifurcating: routine automated, strategic retained. Compliance creates demand |
| 8 | **Data & AI** | Fastest-growing specialization (+88%), highest salary premium, distinct from general SWE |
| 9 | **Cybersecurity** | 424K European gap, NIS2/DORA regulatory demand driver, no juniors available |

### Success Criteria (Phil's)

- ✅ Intuitive, easy, accessible — people can use it without instruction
- ✅ Creates demand for expert counseling / consulting work
- ✅ Provides clear answers = counterpart to the questions raised by the exposure map
- ✅ Foundation for a third tool: frameworks + instructions per role/level

### What This Is NOT (Non-Goals)

- NOT a job board or salary calculator
- NOT a real-time job scraper (we use published reports, not live APIs)
- NOT US-focused — European data only, US as comparison baseline
- NOT a replacement for the exposure map — it's the other side of the coin

### Content Gating Strategy

**Free on the page (draws traffic, builds credibility):**
- All data: hiring rates, salary benchmarks, demand direction, country heat
- The "what" of each role: what's growing, what's shrinking, what's asked for
- The seniority shift story, AI premium story, regulatory demand story
- Enough insight that a hiring leader could restructure their thinking

**Teased but not fully unpacked (creates demand for consulting):**
- Specific futureproofing action plans per role × seniority level
- Role transition playbooks (e.g., "SDR → AE in the AI era", "Designer → AI Product Designer")
- Company-specific workforce restructuring frameworks
- The "how" behind the "what" — personalized to context

**Format:** Each role deep dive ends with a "What this means for you" teaser + CTA to "Get a personalized assessment" or "Book a workforce strategy session." The page sells the problem; consulting sells the solution.

---

## Phase 2: PLAN (Architecture + Data)

### Page Structure

**Option A: Single interactive page (like index.html)**
One page with a role selector + country selector + seniority filter. Roles displayed as cards or a different visualization (not treemap — roles are 6 families, not 130 occupation groups).

**Option B: Article-style page with interactive elements (like analysis.html)**
Narrative-driven findings page with embedded interactive charts/tables. Structured as "findings" like the analysis page but with role-specific deep dives.

**Option C: Hybrid — overview dashboard + deep-dive accordion**
Top section: visual dashboard (6 role cards with demand arrows, country heat, AI premium). Below: accordion deep dives per role (like questions.html pattern). Each accordion section has the role-specific data, skills, and futureproofing advice.

**→ Recommendation: Option C.** It serves both the "quick scan" user (dashboard) and the "deep dive" user (accordions). It matches existing site patterns (uses both the stat-card pattern from analysis.html AND the accordion pattern from questions.html). And it's the most shareable — each role section can be deep-linked.

### Design Philosophy: Visual First, Rams + Maeda

**Core rule: VISUAL → CONTENT → DEEP DIVE** (three layers of progressive disclosure)

1. **Visual layer (instant):** You land on the page, you SEE the story in charts, arrows, color-coded cards. No reading required to get the headline. A hiring manager glancing for 5 seconds gets the signal.
2. **Content layer (scan):** Short text blocks, stat callouts, one-sentence summaries. A professional scanning for 30 seconds gets the key facts per role.
3. **Deep dive layer (read):** Accordion sections, methodology notes, source citations. Someone spending 5 minutes gets the full picture per role.

**Applying Maeda's 10 Laws of Simplicity** (from the brain's John Maeda advisory profile):

| Law | Application to This Product |
|---|---|
| **1. REDUCE** | Thoughtful reduction — every chart, card, paragraph must earn its space. Can you remove this without losing core value? If a stat doesn't answer a user question, cut it. |
| **2. ORGANIZE** | 9 role cards feel manageable because they're organized in a grid. 4 signals feel scannable because they're numbered. Organization makes many appear fewer. |
| **3. TIME** | Fast feels simple. The page loads instantly (static site). The answer to "how is my role doing?" is visible in <5 seconds via the role card. Progressive disclosure: don't show everything upfront. |
| **4. LEARN** | Familiar patterns feel simple. Same color language as the exposure map (green = good, red = bad). Same card/accordion patterns. Learn once on the exposure map, feel at home here. |
| **5. DIFFERENCES** | Simple foreground (role cards, arrows, colors), complex background (Ravio datasets, ISCO mappings, 5 PDFs of ground truth). The complexity enables the simplicity — but the user never sees it. |
| **6. CONTEXT** | This page doesn't exist alone — it's the counterpart to the exposure map. The context (you already know your AI exposure score) makes the career signals meaningful. Cross-links provide that context. |
| **7. EMOTION** | Career decisions are emotional. "Your role is growing" feels different from seeing a dry percentage. Use color, direction arrows, and clear language to create confidence or urgency — not fear. |
| **8. TRUST** | Only Tier 1-2 verified data. Sources cited inline. "We don't know" where we don't know. Trust-based simplicity: you trust the numbers because we show you where they come from. |
| **9. FAILURE** | Some things CAN'T be made simple. Regulatory demand creation is inherently complex (7 regulations × different timelines × different roles). Don't over-simplify — organize the complexity well instead. |
| **10. THE ONE** | *"Simplicity is about subtracting the obvious and adding the meaningful."* The ONE thing this product does: **tells you where the European job market is going and what to do about it.** Everything on the page serves that purpose or gets cut. |

**Applying Rams's Ten Principles** (from the brain's Dieter Rams advisory profile):

| Principle | Application |
|---|---|
| **Innovative** | First European role-level hiring analysis connected to AI exposure scores — no one else has this |
| **Useful** | Every section answers a specific question a real person has about their career or hiring strategy |
| **Aesthetic** | Beauty serves function — charts are beautiful BECAUSE they're clear, not decorated |
| **Understandable** | Self-explanatory without instructions. Color = direction (green ↑, red ↓). Cards = roles. No legend hunting |
| **Unobtrusive** | The tool serves the user, doesn't demand attention. No animations for animation's sake. No popups. |
| **Honest** | Only Tier 1-2 verified data. Confidence levels shown. "We don't know" where we don't know. |
| **Long-lasting** | Data will be dated (Q1 2026), but structure + insights persist. Design for updates. |
| **Thorough** | Every number has a source. Every role has the same depth. No half-finished sections. |
| **Environmental** | Static site, minimal JS, fast load, no tracking beyond PostHog. Respects bandwidth and attention. |
| **Minimal** | *"Could you remove anything?"* — Every chart, card, and paragraph must earn its space. |

**Where Rams and Maeda reinforce each other:**
- Rams's "Minimal" + Maeda's "Reduce" = the same principle from different traditions
- Rams's "Understandable" + Maeda's "Learn" = use familiar patterns, be self-explanatory
- Rams's "Honest" + Maeda's "Trust" = show your sources, never manipulate
- Rams's "Thorough" + Maeda's "Failure" = some complexity is necessary, handle it well

**Where they add different value:**
- Maeda's "Organize" (Law 2) is more actionable than Rams for data-heavy products — 9 roles feel manageable because they're in a grid
- Maeda's "Emotion" (Law 7) reminds us career decisions are emotional — color and language should create confidence, not fear
- Maeda's "Context" (Law 6) is unique — this product exists in context of the exposure map, and that context makes it meaningful
- Rams's "Environmental" extends to respecting users' bandwidth and attention (not just ecological)
- Rams's "Long-lasting" pushes us to design for update cycles, not just this snapshot

**Anti-patterns to avoid:**
- ❌ Wall of text before the first visual element
- ❌ Data tables that require horizontal scrolling
- ❌ Multiple font sizes competing for attention
- ❌ Decorative elements that don't carry information
- ❌ Cluttered dashboards trying to show everything at once
- ❌ Hiding complexity instead of organizing it (Law 2 > hiding)
- ❌ Making things simplistic (removing too much) instead of simple (removing the right things)

### Hosting: Separate Subdomain

**Decision:** Separate subdomain under nexalps.com, cross-linked with ai-exposure.nexalps.com.

**Subdomain: TBD — placeholder during build, decide before deploy.**

Top two candidates after external review:

| Subdomain | Best For | Pairing with ai-exposure |
|---|---|---|
| **job-market.nexalps.com** | Broad LinkedIn reach — zero ambiguity when shared. "ai-exposure shows which jobs AI hits, job-market shows what's actually happening." | Natural narrative arc for general audience |
| **signals.nexalps.com** | Intelligence positioning — signals analytical capability, ages well (can absorb wage trends, skills demand, migration patterns). "ai-exposure detects the problem, signals reads the market response." | Sharper for consulting/leadership audience |

**The trade-off:** `job-market` optimizes for organic reach (everyone knows what it is). `signals` optimizes for consulting credibility (positions Phil as intelligence provider, not career coach). Phil deciding based on primary GTM strategy.

**Build with:** `{SUBDOMAIN}.nexalps.com` as placeholder variable. Single config change at deploy time.

**Cross-linking architecture:**
- `ai-exposure.nexalps.com` → links to `careers.nexalps.com` for "what to do about it"
- `careers.nexalps.com` → links to `ai-exposure.nexalps.com` for "why this is happening" (ISCO-level exposure scores)
- Both link to `nexalps.com` for consulting CTA
- Shared nav bar with both sites + nexalps.com main
- Same design system (shadcn dark, Geist font, orange accent) for brand consistency
- `llms.txt` on careers.nexalps.com for machine-readable project summary (same pattern as ai-exposure)

### Site Architecture

**Two separate static sites, same design system, cross-linked:**

```
european-ai-exposure-map/site/     → ai-exposure.nexalps.com (EXISTING)
├── index.html                      (treemap)
├── analysis.html                   (8 findings)
├── questions.html                  (accordion)
├── methodology.html                (reference)
├── sources.html                    (bibliography)
├── data.json                       (extended with new Eurostat layers)
└── llms.txt                        (machine-readable)

european-careers-map/site/          → careers.nexalps.com (NEW PROJECT)
├── index.html                      (main page: dashboard + signals + roles + playbooks)
├── methodology.html                (data sources + methodology)
├── sources.html                    (bibliography)
├── job-market-data.json            (role-level verified data)
├── llms.txt                        (machine-readable)
└── [shared CSS/design tokens]      (extracted from ai-exposure for consistency)
```

**Nav on both sites:** Cross-links between ai-exposure and careers + nexalps.com consulting CTA
**Deployment:** Same as ai-exposure (static hosting, no backend, same CI/CD)
**New project folder:** `/Users/philippmaul/Documents/projects/european-careers-map/`

### Data Architecture

**Two data files:**

1. **`data.json` (existing, extended):** Add 2 new layers to existing ISCO occupation groups:
   - `ai_adoption_enterprise` — Eurostat `isoc_eb_ai` enterprise AI adoption % by country (replaces uniform lab-based adoption scores)
   - `ict_specialist_pct` — Eurostat `isoc_sks_itspt` ICT specialists as % of employment by country

2. **`job-market-data.json` (NEW):** Role-level data that can't map cleanly to ISCO:

```json
{
  "meta": {
    "last_updated": "2026-03-28",
    "sources": ["Ravio 2026", "Recruited.tech", "Bridge Group 2025", "McKinsey 2026", "Eurostat"]
  },
  "roles": {
    "product": {
      "label": "Product Management",
      "isco_codes": ["133", "251"],
      "demand": {
        "global_open": 7300,
        "europe_open": 4200,
        "yoy_change_europe": -0.17,
        "direction": "contracting",
        "source": "Recruited.tech / TrueUp"
      },
      "hiring_rate": { "value": 0.206, "source": "Ravio" },
      "seniority": {
        "junior_pct": 0.03,
        "mid_pct": 0.72,
        "senior_pct": 0.16,
        "leadership_pct": 0.09,
        "source": "Recruited.tech"
      },
      "ai_subspecialty": {
        "ai_pm_roles_europe": 50,
        "ai_pm_growth": "exploding but from tiny base",
        "source": "Recruited.tech"
      },
      "salary": {
        "UK_P3": { "value": 67000, "currency": "GBP", "yoy_pct": 1.7 },
        "DE_P3": { "value": 71500, "currency": "EUR", "yoy_pct": 1.1 },
        "SE_P3": { "value": 65600, "currency": "EUR", "yoy_pct": 5.5 },
        "source": "Ravio"
      },
      "remote_split": {
        "remote": 0.28, "hybrid": 0.45, "onsite": 0.27,
        "source": "Recruited.tech"
      },
      "skills_now": ["SQL", "Jira", "LLM experience", "stakeholder management"],
      "skills_future": ["AI product design", "prompt engineering", "agent orchestration"],
      "futureproof": "The PM role is becoming MORE valuable, not less — AI makes execution faster, making 'what to build' the bottleneck. But junior PM roles are vanishing (-73% entry-level). Senior PMs who can leverage AI tools to ship faster are the winners.",
      "connection_to_exposure_map": "ISCO 133/251 technical exposure: 6-7. PM work is high-judgment, low-routine — the augmentation sweet spot."
    },
    "engineering": { /* same structure */ },
    "design": { /* same structure */ },
    "sales": { /* same structure */ },
    "growth_marketing": { /* same structure */ },
    "operations": { /* same structure */ }
  },
  "cross_role": {
    "entry_level_collapse": { "value": -0.734, "source": "Ravio" },
    "ai_ml_hiring_growth": { "value": 0.88, "source": "Ravio" },
    "ai_salary_premium_ic": { "value": 0.12, "source": "Ravio" },
    "ai_salary_premium_mgmt": { "value": 0.03, "source": "Ravio" },
    "median_salary_increase": { "value": 0.05, "source": "Ravio" },
    "overall_hiring_rate": { "value": 0.286, "source": "Ravio" }
  },
  "country_hiring": {
    "UK": { "rate": 0.318, "yoy": -0.205 },
    "DE": { "rate": 0.298, "yoy": 0.028 },
    "FR": { "rate": 0.223, "yoy": -0.281 },
    "NL": { "rate": 0.235, "yoy": -0.130 },
    "ES": { "rate": 0.263, "yoy": -0.269 },
    "SE": { "rate": 0.165, "yoy": -0.340 },
    "source": "Ravio"
  },
  "regulatory_demand": {
    "cybersecurity_gap_eu": { "value": 424000, "source": "ISC2 (separate data release — not verified from our whitepaper)", "confidence": "medium" },
    "nis2_entities_in_scope": { "value": 160000, "source": "ENISA/regulatory" },
    "dora_entities_in_scope": { "value": 22000, "source": "regulatory" },
    "ai_governance_hiring_intent": { "value": 0.78, "note": "78% plan to hire 1-10 AI governance professionals", "source": "IAPP 2025" }
  }
}
```

### New Eurostat Data — Fetch Guide

**For Phil (step-by-step):**

Both tables are available as CSV bulk downloads from Eurostat. No API scripting needed — same approach as existing data:

**Table 1: Enterprise AI Adoption (`isoc_eb_ai`)**
1. Go to: https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table
2. Set filters:
   - Size class: "10 persons employed or more" (covers all enterprises)
   - Information society indicator: select `E_AI_TTML` (enterprises using at least one AI technology — this is the headline number)
   - Unit: "Percentage of enterprises"
   - Time: 2021, 2023, 2024, 2025
3. Click "Download" → CSV
4. Save to `data/eurostat/ai_adoption_enterprise.csv`

**Table 2: ICT Specialists (`isoc_sks_itspt`)**
1. Go to: https://ec.europa.eu/eurostat/databrowser/view/isoc_sks_itspt/default/table
2. Set filters:
   - Unit of measure: "Percentage of total employment"
   - Time: 2020-2024 (all available years)
3. Click "Download" → CSV
4. Save to `data/eurostat/ict_specialists.csv`

**Table 3: OECD Employment Protection (`EPL_OV`)**
1. Go to: https://data-explorer.oecd.org/
2. Search for "Employment Protection Legislation"
3. Select dataset: "Strictness of employment protection – individual and collective dismissals (regular contracts)"
4. Filter: All available countries, latest year
5. Download CSV
6. Save to `data/oecd/epl_scores.csv`

**All three are simple CSV downloads — no coding needed.** I'll write processing scripts that read these CSVs and integrate into `data.json` and `job-market-data.json`.

### Visual Design — job-market.html

**Hero Section:**
- Title: "State of the European Job Market in Early 2026"
- Lede: "The other side of AI exposure — where demand is growing, what employers *should* want, and what you need to get there"
- 4 stat cards — each tells a clear story:
  - **"28.6% hiring rate"** → subtitle: "European tech companies are still hiring — but slower than 2023's 34%"
  - **"-73% entry-level"** → subtitle: "Junior roles collapsed — the pipeline is breaking"
  - **"+88% AI/ML growth"** → subtitle: "AI specialist hiring grew 88% while everything else shrank"
  - **"424K cybersecurity gap"** → subtitle: "Europe can't fill these roles — regulation creates demand faster than talent"
- Byline: "Based on data from Ravio (1,500+ EU tech companies), Eurostat (36 countries), OECD (38 countries), and 5 primary research reports"

**Section 1: The Dashboard (visual overview)**
- 9 role cards in a 4×2 grid (mobile: stacked, 2×4)
- Each card: Role name, demand arrow (↑↓→), hiring rate, one killer metric
- Color-coded: green (growing) / amber (stable) / red (contracting)
- Click a card → smooth scroll to that role's deep dive below
- Inspired by Lenny's role-by-role format but with European data and interactive cards

**Section 2: Country Hiring Heat**
- **Full DACH + key European markets:** DE, AT, CH are mandatory. Plus NL, FR, PL, Baltics (EE, LV, LT), Nordics (SE, DK, FI, NO), UK
- **Ideally all 36-37 countries** — depends on data availability per metric:
  - Eurostat AI adoption (`isoc_eb_ai`): 36 countries ✅
  - Eurostat ICT specialists (`isoc_sks_itspt`): 37 countries ✅
  - Ravio hiring rates: 6 countries (UK, DE, FR, NL, ES, SE) — detailed function-level breakdown
  - OECD EPL: 38 OECD members (covers most European countries)
  - Eurostat employment YoY: 35+ countries ✅
- **Strategy:** Show ALL countries where Eurostat data exists (broadest coverage). For countries with Ravio detail (6), show richer function-level breakdown. Flag data depth per country.
- Table: country × hiring rate/trend + YoY change + AI adoption % + ICT specialist % + EPL score + link to exposure map
- Germany highlighted as only positive market in Ravio data (+2.8%)
- Sortable columns so users can rank countries by any metric

**Section 3: The Four Signals (narrative findings, like analysis.html)**

- **Signal 1: The Seniority Shift** — junior collapse (-73%), senior premium, player-coach era
  - Extended focus: **"What this means for Gen Z and career starters"**
  - The pipeline is breaking: if companies don't hire juniors, where do future seniors come from?
  - Mitigation strategies: apprenticeship models, AI-augmented junior roles, "junior + AI tools = mid-level output"
  - Data: Stanford (22-25 age group -13% in AI-exposed occupations), Harvard (7.7% junior decline in AI-adopting firms), Korn Ferry (37% planning to replace entry-level with AI)
  - **European university data to find/add:**
    - Eurostat: EU universities produce ~65K CS graduates/year vs 180K AI-capable demand (115K gap) — need to find the per-country breakdown
    - DAAD: Germany has 35.5% STEM students (highest in EU)
    - UK GOV.UK: ~54K CS enrollments, ~7K cybersecurity graduates annually
    - ECSA: projected 65K specialized engineering shortfall across EU-27
    - Search for: ETH Zurich, TU Munich, Polytechnique, TU Delft, KTH data on AI/ML graduate output
    - Goal: European institutions as primary reference, US studies as supporting evidence — not the other way around
  - Connection to Section 7 (Junior Playbook)

- **Signal 2: The AI Premium** — 88% hiring growth, 12% salary premium, where AI fluency pays
  - Cross-role: Figma (73% of design hiring managers require AI fluency), Ravio (AI/ML 45% of AI titles), McKinsey (Gen AI = #1 marketing investment)
  - **European company examples to feature:**
    - Klarna: headcount 5,527 → 3,422 (-38%), ~700 CS roles replaced by AI chatbots — the poster child
    - Spotify: ~2,300 job cuts in 2023
    - Ericsson: 15,600+ global cuts, 1,600 in Sweden specifically
    - SAP: investing heavily in AI while restructuring (German bellwether)
    - Wise, Revolut: fintech scaling in Europe with AI-first teams
    - Atomico data: 27,000+ founders started companies in Europe in 2025 (+60%)
    - ECB survey (March 2026, 5,300 firms): firms with AI-using employees 4% MORE likely to hire
    - Note: verify all company-specific numbers from primary sources before publishing

- **Signal 3: The Regulatory Demand Engine** — NIS2 + DORA + AI Act + EAA creating roles that don't exist in the US
  - **NEW: Expiration probability per regulation**
  - NIS2 cybersecurity roles: **Permanent** — ongoing compliance, not one-time implementation. The gap (424K) is structural.
  - DORA financial resilience: **Semi-permanent** — implementation spike 2025-2027, then steady-state at ~40% of peak (ongoing testing + reporting required)
  - EU AI Act governance: **Growing** — enforcement phases through Aug 2027, but AI governance is a permanent function once established. No sunset.
  - EAA accessibility: **Spike then decline** — implementation surge 2025-2026, then maintenance. Estimate: peak demand drops 50-60% within 3 years as compliance becomes routine.
  - CSRD sustainability: **Contracting** — Omnibus I cut 80% of companies from scope. Roles persist for in-scope companies but volume declining.
  - Platform Work Directive: **Slow build** — transposition deadline 2026, enforcement 2027+. Small but persistent.
  - **Framing:** "These windows have different shelf lives. Some are careers, some are 2-year contracts."

- **Signal 4: The Geographic Divergence** — Europe is not one market
  - Germany: only positive market, Kurzarbeit buffer, but 137K IT positions unfilled
  - Sweden: sharpest contraction (-34%) despite highest AI adoption — the flexibility paradox
  - UK: contracting from high base but still highest absolute rate
  - France: sharp decline but McKinsey shows marketing leaders most bullish on budget increases
  - Connect to exposure map's regulatory friction delta: countries with higher EPL move slower on restructuring

**Section 4: Role Deep Dives (accordion, 8 sections)**
- 9 accordion sections: Product, Engineering, Design, Sales, Business Development, Growth/Marketing, Operations, Data & AI, Cybersecurity
- Each contains:
  - **Demand snapshot:** hiring rate, open roles, YoY change, direction arrow
  - **Seniority breakdown:** pie/bar showing junior/mid/senior/leadership split
  - **Salary benchmarks:** table by country (only Tier 1-2 sourced numbers)
  - **What's asked for now:** current top skills from job postings
  - **What will be asked for:** emerging skill signals
  - **The AI angle:** how AI is reshaping this specific role
  - **Connection to exposure map:** deep link to the ISCO code on the map with the relevant layer
  - **What this means for you:** 2-3 sentence teaser → CTA
  - **📊 GRAPHS (Lenny-style):** Each role gets at least 1 chart:
    - Line chart: hiring rate over time (2022→2025/2026 where data exists — Ravio gives us 2023/2024/2025)
    - Bar chart: country comparison (hiring rate or salary by country)
    - Stacked bar: seniority distribution (junior/mid/senior/leadership)
    - These are static charts (D3.js or simple SVG) — not live-updating, snapshot of current data
    - Even if the line ends at "now" without forecast, the trend is the story
- Deep-linkable: `index.html#product`, `index.html#engineering`, etc.

**Section 5: Skills That Protect (cross-role synthesis)**
- Matrix: skills × 9 roles showing which skills matter where
- **Preliminary skill categories (to be expanded during build based on ESCO skills data + research):**
  - AI fluency (tool use, prompt engineering, agent orchestration)
  - Systems thinking (architecture, cross-functional, second-order effects)
  - Strategic judgment (prioritization, trade-offs, ambiguity navigation)
  - Regulatory/compliance knowledge (EU AI Act, NIS2, GDPR, EAA)
  - Cross-functional collaboration (PM×Eng, Sales×Product, etc.)
  - Domain expertise (vertical depth in industry)
  - Data literacy (analytics, metrics, experimentation)
  - Communication & influence (stakeholder management, exec comms)
  - Leadership & coaching (team building, talent development)
  - Technical depth (architecture, code, infrastructure)
- "If you learn one thing" takeaway per seniority level (junior, mid, senior, leadership)
- **Skill Connections / Multiplier Effects:** Where two skills compound (like concept bridges in the brain):
  - "AI fluency + domain expertise = 3× harder to replace than either alone"
  - "Regulatory knowledge + technical depth = the EU AI Act compliance role that commands 25% premium"
  - "Systems thinking + AI fluency = the architect role every company needs but can't fill"
  - Format: connection lines or "bridge" markers between skills in the matrix, with multiplier labels
  - Inspired by the brain's concept bridges — show that skills aren't independent, they compound
- **Prioritization:** Rank skills by impact × demand (not just frequency). A skill that appears in 9/9 roles but weakly matters less than one that appears in 4/9 roles but is the decisive hiring factor.
- Note: this is the preliminary list. During build, we cross-reference against ESCO digital skills collection + Figma/McKinsey/Ravio survey data to produce the definitive matrix.

**Section 6: Career Tracks — IC vs Management in the AI Era**
- **The IC Track:** What changes for senior ICs when AI handles more execution?
  - Staff/Principal roles become "AI-augmented architects" — fewer of them, paid more, expected to leverage AI tools
  - IC salary ceiling rising (Pave: 90th percentile senior IC PMs at ~$1M total comp)
  - The "player-coach" model: ICs who manage AI agents, not people
  - Skills that matter: technical depth, system design, quality judgment, AI tool mastery
- **The Management Track:** What changes for managers when teams get smaller?
  - Span of control increases (fewer, more senior reports)
  - Manager-as-coach: developing talent matters more when juniors are scarce
  - AI governance becomes a management responsibility (EU AI Act Art 26: deployer obligations)
  - Skills that matter: talent development, cross-functional orchestration, regulatory navigation, strategic vision
- **The Divergence:** Where IC and management tracks are pulling apart vs converging
  - Converging: AI fluency required in both tracks
  - Diverging: IC → deeper technical mastery; Management → broader organizational + regulatory scope
  - Ravio data: AI premium 12% for IC, only 3% for management — the market values AI-fluent ICs more (for now)

**Section 7: The Junior Playbook — Breaking Into a Market That's Closing**
- **The problem:** -73% entry-level hiring. 37% of companies planning to replace entry-level with AI. SDR-to-AE promotion dropped from 34% to 16%.
- **The counterargument:** This is NOT the end of junior careers — it's a restructuring. The path in has changed.
- **5 paths that still work:**
  1. **AI-augmented junior:** Position yourself as "junior + AI tools = mid-level output." Demonstrate AI tool proficiency as the differentiator.
  2. **Apprenticeship/embedded learning:** Companies that still hire juniors are doing it through structured programs, not open applications. Find the programs.
  3. **Domain-first, then tech:** Enter through industry expertise (healthcare, fintech, sustainability), not generic "junior PM" roles. Domain knowledge is the moat.
  4. **Freelance/project-based:** Build a portfolio through freelance work, open source, or side projects. The "prove it first" market.
  5. **Start something:** It has never been simpler or cheaper to start a company. AI tools collapse the team size needed for an MVP from 5 to 1-2. The venture path is more accessible than ever for technical founders.
- **Connection:** Links to Founder OS venture data when available. The exposure map shows which occupations are being automated; this section shows how to build instead of compete for shrinking slots.
- **Data backing:** Atomico (27,000+ founders started companies in Europe in 2025, +60% from 2023), early-stage startup OTE for founding roles ($100K-$200K), European VC $44B projected.

**Section 8: What's Next (CTA — built but may be hidden initially)**
- Teaser for two future tools:
  - **Tool 3: AI Readiness Score** — input your role, seniority, country → get your exposure score + demand signal + skill gaps + action plan (combines both existing tools)
  - **Tool 4: Lessons from History** — what happened to workers during previous technological disruptions (loom, steam engine, electricity, computing, internet) and what it tells us about the AI transition. Ray Dalio "Principles for a Changing World Order" format but for labor market disruption. Patterns: displacement timeline, reabsorption rate, skill premium evolution, regulatory response lag, geographic divergence, new role creation velocity.
- CTA to Nexalps consulting / "Get a personalized workforce strategy"
- Note: Section 7's "Start something" path connects to future Founder OS integration
- **Display decision:** Keep in codebase but `display: none` or behind a feature flag until Phil decides to reveal. The structure is there for when we're ready.

**Footer:** Sources + methodology note + CTA bar (same pattern as existing pages)

### Connection to Exposure Map

| Exposure Map (existing) | Career Signals (new) | Link |
|---|---|---|
| ISCO occupation: technical exposure score | Role: demand direction | Deep link from career role → map filtered to that ISCO code |
| Country: regulatory friction delta | Country: hiring rate | Same country selector, shared data |
| Augmentation sweet spot layer | "Skills That Protect" section | Narrative reference |
| Questions page: "What should workers do?" | Career deep dives: specific answers per role | Cross-link from questions → career signals |

### Third Tool (Future)

Both products together enable a **Role-specific AI Readiness Framework** tool:
- Input: your role, seniority, country
- Output: your exposure score + demand signal + skill gaps + action plan
- Built from: exposure map (what AI does to your job) + career signals (what employers want) + ESCO skills data (what skills you need)

This is the consulting product / premium offering. Not built now — but the data architecture supports it.

### Fourth Tool (Future): Lessons from History

**Concept:** What happened to workers during every major technological disruption in history — and what patterns emerge that predict the AI transition.

**Disruptions to analyze:**
- Spinning Jenny / Power Loom (1760s-1830s) — destroyed cottage industry, created factory system
- Steam Engine / Railways (1830s-1860s) — destroyed horse-related jobs, created engineering class
- Electricity / Assembly Line (1880s-1920s) — eliminated craft labor, created middle management
- Computing / Mainframes (1950s-1970s) — eliminated human computers, created IT profession
- Internet / E-commerce (1990s-2010s) — destroyed retail/media jobs, created digital economy
- Mobile / Cloud (2007-2020) — destroyed local services, created app economy
- AI / Agents (2023-present) — the current disruption

**Patterns to extract per disruption:**
- Displacement timeline: how long from invention to peak job displacement?
- Reabsorption rate: how long until new jobs exceeded lost jobs?
- Skill premium evolution: which skills became more/less valuable?
- Regulatory response lag: how long did governments take to respond?
- Geographic divergence: which regions adapted first/last?
- New role creation: what entirely new jobs were invented?
- Who won vs. lost: what profiles thrived vs. were displaced?

**Format:** Dalio-style principles with historical evidence → applied to AI transition → connected to exposure map + career signals data.

**Why it matters:** The exposure map shows what AI CAN do. The career signals show what employers ARE doing. The historical tool shows what WILL LIKELY happen — because every major disruption follows recognizable patterns. The strongest consulting pitch isn't "here's the data" — it's "history tells us what comes next, and here's what to do about it."

**Status:** Concept only. Would be a separate subdomain (e.g., `history.nexalps.com` or integrated into careers as a section). Research phase would involve ingesting economic history sources into the brain. Parks this for now — flagged for future.

---

## Phase 3: TASKS (Build Sequence)

Following Osmani Factory Model: Plan → Spawn → Monitor → Verify → Integrate → Retro

### Sprint 1: Data Pipeline (Phil downloads CSVs + Claude writes processing scripts)

| Task | Owner | Output |
|---|---|---|
| Download 3 CSVs (Eurostat AI adoption, Eurostat ICT specialists, OECD EPL) | Phil | 3 CSV files in `data/` |
| Write `14_fetch_ai_adoption.py` — process Eurostat AI adoption CSV | Claude | `data/eurostat/ai_adoption_enterprise.csv` (processed) |
| Write `15_fetch_ict_specialists.py` — process Eurostat ICT CSV | Claude | `data/eurostat/ict_specialists.csv` (processed) |
| Write `16_process_oecd_epl.py` — process OECD EPL CSV | Claude | `data/oecd/epl_scores.csv` (processed) |
| Manually extract Ravio hiring rate tables from PDF → JSON | Claude (from PDF) | `data/ravio/hiring_rates.json` |
| Build `job-market-data.json` from verified audit data | Claude | `site/job-market-data.json` |

**Gate 1:** Phil reviews data files before any frontend work.

### Sprint 2: New Project Setup + Page Build

| Task | Owner | Output |
|---|---|---|
| Create new project `/european-careers-map/` with same structure as ai-exposure | Claude | Project scaffold |
| Extract shared CSS/design tokens from ai-exposure for reuse | Claude | Shared stylesheet |
| Build `index.html` — full page: hero, 9-role dashboard, country heat, 4 signals (incl. seniority deep dive + junior mitigation), 9 role accordions, skills matrix, IC/mgmt tracks, junior playbook (incl. start a company), leadership impact section, CTA | Claude | `site/index.html` |
| Build `methodology.html` + `sources.html` | Claude | Supporting pages |
| Build `llms.txt` | Claude | Machine-readable summary |
| Update `05_build_site_data.py` in ai-exposure to merge new Eurostat layers into existing `data.json` | Claude | Updated script + data.json |

**Gate 2:** Phil reviews page in browser, checks data accuracy against audit doc.

### Sprint 3: Cross-Links + Polish

| Task | Owner | Output |
|---|---|---|
| Add cross-links from ai-exposure → careers.nexalps.com (nav, analysis findings, questions) | Claude | Updated ai-exposure HTML files |
| Add deep links from careers → ai-exposure (ISCO codes, exposure layers) | Claude | URL parameter links |
| Mobile responsive pass | Claude | CSS adjustments |
| PostHog analytics integration | Claude | Event tracking |
| Deploy careers.nexalps.com (same hosting as ai-exposure) | Phil + Claude | Live site |

**Gate 3:** Full review before deploy.

---

## Verification

1. **Data accuracy:** Every number on job-market.html must trace to a Tier 1 or Tier 2 source in `DATA-SOURCE-AUDIT.md`
2. **Cross-reference:** Check 5 random data points against PDF ground truth
3. **Deep links:** Test all cross-links between exposure map ↔ career signals ↔ questions
4. **Mobile:** Test on mobile viewport (375px)
5. **Accessibility:** Tab navigation, screen reader labels, color contrast
6. **Performance:** Page load < 2s (static site, should be trivial)

---

## Critical Files

### New Project: european-careers-map/
| File | Action |
|---|---|
| `site/index.html` | NEW — "State of the European Job Market in Early 2026" (main page) |
| `site/methodology.html` | NEW — data sources + methodology |
| `site/sources.html` | NEW — bibliography |
| `site/job-market-data.json` | NEW — 9 role families, verified data only |
| `site/llms.txt` | NEW — machine-readable project summary |

### Existing Project: european-ai-exposure-map/
| File | Action |
|---|---|
| `site/data.json` | EXTEND — add 2 new Eurostat layers (AI adoption, ICT specialists) |
| `site/index.html` | UPDATE — cross-link nav to careers.nexalps.com |
| `site/analysis.html` | UPDATE — cross-link nav + references |
| `site/questions.html` | UPDATE — cross-link nav + deep links |
| `site/sources.html` | UPDATE — nav |
| `site/methodology.html` | UPDATE — nav |
| `scripts/14_fetch_ai_adoption.py` | NEW — Eurostat AI adoption processing |
| `scripts/15_fetch_ict_specialists.py` | NEW — Eurostat ICT specialist processing |
| `scripts/16_process_oecd_epl.py` | NEW — OECD EPL processing |
| `scripts/05_build_site_data.py` | UPDATE — merge new layers |

### Data Files (both projects reference)
| File | Action |
|---|---|
| `data/eurostat/ai_adoption_enterprise.csv` | NEW — downloaded by Phil |
| `data/eurostat/ict_specialists.csv` | NEW — downloaded by Phil |
| `data/oecd/epl_scores.csv` | NEW — downloaded by Phil |
| `data/ravio/hiring_rates.json` | NEW — extracted from PDF |
| `research/DATA-SOURCE-AUDIT.md` | REFERENCE — source of truth for all numbers |

---

## Decisions Made

1. ✅ **Page name:** "State of the European Job Market in Early 2026" — Lenny-inspired framing
2. ✅ **Role families:** 9 (original 6 + Business Development + Data & AI + Cybersecurity)
3. ✅ **Gating:** Data free, frameworks teased, action plans behind consulting CTA
4. ✅ **Data fetch:** Phil downloads 3 CSVs manually (step-by-step guide in plan)
5. ✅ **Page structure:** Option C hybrid (dashboard + accordion deep dives)
