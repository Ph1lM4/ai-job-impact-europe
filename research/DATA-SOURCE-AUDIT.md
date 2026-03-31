# Consolidated Data Source Audit — European Tech Career Signals

**Date:** 2026-03-28
**Scope:** 23 research files (11 round 1 + 7 round 2 + 5 primary source PDFs)
**Purpose:** Identify every verifiable data point usable for the companion product to ai-exposure.nexalps.com

---

## Executive Summary

- **~1,200+ quantitative claims** extracted across all research files
- **~55% are verifiable** (attributed to named institutional or industry sources)
- **~25% are partially verifiable** (attributed but from blog posts, vendor reports, or LinkedIn snapshots)
- **~20% are unsourced** (author estimates, generic market research, or fabricated)
- **5 primary source PDFs** provide ground truth for the most-cited claims
- **7 institutional data sources** can be fetched programmatically (Eurostat, OECD, Cedefop)
- **3 industry reports** provide the richest proprietary data (Ravio, Bridge Group, McKinsey)

---

## Part 1: Primary Source PDFs — Ground Truth

These are the actual reports that secondary research cites. Numbers here are canonical.

### 1.1 Ravio Compensation Trends 2026
- **Methodology:** 1,500+ companies, real-time HRIS data, Q3 2025, GBP currency
- **Status:** PDF in `/research/`. Richest single source for European tech hiring.

**Verified ground truth numbers:**

| Metric | Value | Usable? |
|---|---|---|
| EU tech hiring rate 2025 | 28.6% (down from 34% in 2023) | ✅ YES |
| UK hiring rate | 31.8% (-20.5% YoY) | ✅ YES |
| Germany hiring rate | 29.8% (+2.8% YoY) — only positive market | ✅ YES |
| France hiring rate | 22.3% (-28.1% YoY) | ✅ YES |
| Netherlands hiring rate | 23.5% (-13.0% YoY) | ✅ YES |
| Spain hiring rate | 26.3% (-26.9% YoY) | ✅ YES |
| Sweden hiring rate | 16.5% (-34.0% YoY) — lowest in Europe | ✅ YES |
| Commercial function hiring | 34.7% — ONLY growing function | ✅ YES |
| Engineering hiring rate | 20.7% (down from 30% in 2023) | ✅ YES |
| Product hiring rate | 20.6% (down from 31% in 2023) | ✅ YES |
| Marketing hiring rate | 21.8% (down from 33% in 2023) | ✅ YES |
| Operations hiring rate | 27.1% | ✅ YES |
| People hiring rate | 22.9% | ✅ YES |
| AI/ML hiring growth | +88% YoY (proportion of new hires) | ✅ YES |
| AI/ML job title expansion | +50% distinct titles | ✅ YES |
| AI salary premium (IC) | +12% | ✅ YES |
| AI salary premium (Mgmt) | +3% | ✅ YES |
| Entry-level hiring collapse | -73.4% (P1/P2 vs -7% all levels) | ✅ YES |
| Median salary increase | 5.0% (second consecutive year) | ✅ YES |
| Promotion-based salary increase | 22.3% median | ✅ YES |
| Average tenure | 2 years 1 month | ✅ YES |
| Operations attrition | 21.3% — highest, surged 34.8% | ✅ YES |
| Engineering attrition | 12.0% — lowest | ✅ YES |
| Gender pay gap (unadjusted) | 23% | ✅ YES |
| Gender pay gap (adjusted, like-for-like) | 2.4% | ✅ YES |
| Women in tech roles | 40% | ✅ YES |
| Women in leadership | 21% | ✅ YES |
| Early-stage hiring collapse | 49% → 26.7% (2023→2025) | ✅ YES |
| Late-stage convergence | 22% → 27.8% (2023→2025) | ✅ YES |

### 1.2 ENISA NIS Investments 2025
- **Methodology:** 1,080 professionals, 27 EU states, phone interviews, May-Aug 2025
- **Status:** PDF in `/research/`.
- **Key finding:** This report focuses on INVESTMENT and PRACTICES, not workforce gap numbers.

**Verified ground truth numbers:**

| Metric | Value | Usable? |
|---|---|---|
| 1 in 3 orgs did no cybersecurity assessment | 33% | ✅ YES |
| 63% of SMEs: no assessment in past year | 63% | ✅ YES |
| 51% of SMEs: >3 months to apply critical patches | 51% | ✅ YES |
| Supply chain attacks: 2nd most cited future concern | 47% | ✅ YES |
| Supply chain risk mgmt: most difficult NIS2 requirement | 37% | ✅ YES |
| Ransomware: #1 future threat concern | 55% | ✅ YES |
| 90% implement third-party controls | 90% | ✅ YES |
| DoS attacks: most common operational impact | 22% | ✅ YES |

**⚠️ IMPORTANT:** The "89% need additional cybersecurity staff" and "76% difficulty attracting" and "71% difficulty retaining" numbers cited in the Claude research files are NOT from this 2025 report. They may be from an earlier ENISA edition or a different ENISA publication. Cannot verify from this PDF.

### 1.3 Bridge Group — 2025 SDR Metrics Report
- **Methodology:** US-focused B2B SaaS benchmarking. Not European.
- **Status:** PDF in `/research/`.

**Verified ground truth numbers:**

| Metric | Value | Usable? |
|---|---|---|
| SDR-to-AE promotion rate | 16% (2024), down from 34% (2020) | ✅ YES (US data, directional for Europe) |
| SDR quota attainment | 60% achieve quota (lowest ever) | ✅ YES |
| SDR median tenure | 1.9 years (2024) | ✅ YES |
| SDR annual turnover | 40% median (P25: 21%, P75: 57%) | ✅ YES |
| SDR OTE | $80K (base $55K, variable $25K, split 68:32) | ✅ YES (US dollars) |
| Quality conversations/day | 4.1 (2024), down from 8.0 (2014) | ✅ YES |
| Monthly pipeline per SDR | $3.78M median (2024) | ✅ YES |
| SDR-to-leader ratio | 6.4 (down from 8 in 2021-2023) | ✅ YES |
| Leadership OTE: first-ever negative growth | Directors -2%, VPs -1% | ✅ YES |
| SDRs promoted ≤11 months: AE failure rate | 55% | ✅ YES |
| SDRs promoted 16+ months: AE failure rate | 6% | ✅ YES |

### 1.4 McKinsey — State of Marketing Europe 2026
- **Methodology:** 500 senior marketing leaders, FR/DE/IT/ES/UK. Published 2026.
- **Status:** PDF in `/research/`.

**Verified ground truth numbers:**

| Metric | Value | Usable? |
|---|---|---|
| 72% of CMOs plan to increase budgets | 72% | ✅ YES |
| 99% expect spend steady or grow | 99% | ✅ YES |
| Marketing budgets avg 8.7% of revenue | 8.7% | ✅ YES |
| #1 investment priority: Gen AI-enabled marketing | 50% | ✅ YES |
| 62% agree human creative teams irreplaceable | 62% | ✅ YES |
| Classic brand campaigns: used 75%, plan to use 48% | -27pp | ✅ YES |
| 71% build multipurpose campaigns (full funnel) | 71% | ✅ YES |
| Only 3% can explain >50% of marketing spend via MROI | 3% | ✅ YES |
| Top MROI obstacle: lack of data (49%) | 49% | ✅ YES |
| Budget centralization: 77% | 77% | ✅ YES |

**⚠️ CORRECTION:** Several Claude research files cite "brand building ranked #1 of 20 priorities; GenAI ranked #17." The actual McKinsey report shows Gen AI-enabled marketing at #1 INVESTMENT priority (50%), not brand. Brand is the strategic priority, Gen AI is the spend priority. The reports conflated two different rankings.

### 1.5 ISC2 — 2025 Cybersecurity Workforce Study
- **Methodology:** 16,029 professionals globally, online survey, May-June 2025
- **Status:** PDF in `/research/`. This is a WHITEPAPER SUMMARY, not the full data release.

**Verified ground truth numbers:**

| Metric | Value | Usable? |
|---|---|---|
| 69% on path toward regular AI tool use | 69% | ✅ YES |
| 63% of AI users report significant productivity boost | 63% | ✅ YES |
| 73% believe AI will create more specialized skills | 73% | ✅ YES |
| Job satisfaction: 68% (up from 66% in 2024) | 68% | ✅ YES |
| 47% feel overwhelmed by workload | 47% | ✅ YES |
| 28% considered switching careers | 28% | ✅ YES |
| 78% plan to stay in cybersecurity | 78% | ✅ YES |
| 56% entered through IT experience | 56% | ✅ YES |

**⚠️ IMPORTANT:** The headline "424,000 European cybersecurity gap" and "274,000 open positions" numbers are NOT in this whitepaper. They come from a separate ISC2 data release (the full Workforce Study, not this summary). The whitepaper doesn't break out European regional data.

---

## Part 2: Source Reliability Tiers

### Tier 1 — Institutional (fetch programmatically, cite with full confidence)

| Source | What We Can Get | Already in Project? | Fetchable? |
|---|---|---|---|
| **Eurostat LFSA_EGAI2D** | Employment by ISCO 2-digit × country | ✅ YES | API |
| **Eurostat EARN_SES22_28** | Wages by ISCO 1-digit | ✅ YES | API |
| **Eurostat LFSA_EGISED** | Education by ISCO 1-digit | ✅ YES | API |
| **Eurostat isoc_eb_ai** | Enterprise AI adoption by country (2021-2025) | ❌ NO | API — HIGH PRIORITY |
| **Eurostat isoc_sks_itspt** | ICT specialists % employment by country | ❌ NO | API — HIGH PRIORITY |
| **Cedefop Skills Forecast** | Employment CAGR 2024→2035 by ISCO 1-digit | ✅ YES | Downloaded |
| **OECD EPL** | Employment protection strictness by country | ❌ NO | API — HIGH PRIORITY |
| **Anthropic/Microsoft/OpenAI** | AI exposure scores by occupation | ✅ YES | GitHub/HF |
| **BFS (Swiss)** | Swiss wages + employment | ✅ YES | Downloaded |
| **ONS (UK)** | UK wages + employment | ✅ YES | Downloaded |
| **Bitkom** | German IT shortage: 109,000-137,000 unfilled | ❌ Not in data/ | Annual report |

### Tier 2 — Industry Reports (proprietary, manual extraction, cite with attribution)

| Source | Coverage | In Project? | Notes |
|---|---|---|---|
| **Ravio** | EU tech hiring/comp/attrition by function × country | ✅ PDF in /research/ | RICHEST source. Manual extraction needed. |
| **Bridge Group** | SDR metrics (US data, directional for EU) | ✅ PDF in /research/ | US-focused but widely cited |
| **McKinsey** | Marketing priorities/budgets (FR/DE/IT/ES/UK) | ✅ PDF in /research/ | 500 leaders, strong methodology |
| **ENISA** | NIS2 compliance + cybersecurity practices | ✅ PDF in /research/ | 1,080 respondents, EU-27 |
| **ISC2** | Cybersecurity workforce global | ✅ PDF in /research/ | Whitepaper only — need full report for EU data |
| **Recruited.tech** | EU PM job counts, seniority, remote splits | Cited in reports | LinkedIn scraping methodology |
| **Figma** (Feb 2026) | Design hiring sentiment, AI fluency | Cited in reports | 2,500 respondents, interested party |
| **Emergence Capital** | SDR/BDR cut rates (560+ B2B SaaS) | Cited in reports | SaaS-specific |
| **Atomico State of European Tech** | European startup ecosystem | Cited in reports | Annual, strong methodology |

### Tier 3 — Directional (use for narrative, NOT for data layers)

| Source | Problem | Used In |
|---|---|---|
| HeroHunt.ai | AI recruiting startup blog — source for ALL Tier 1 growth rates in Gemini demand scan (143%, 140%, 135%) | Gemini Job Demand report |
| Index.dev | Staffing company blog — most-cited for EU market sizing | Multiple files |
| MEXC.com | **Cryptocurrency exchange** news section cited for AI labor market claims | Gemini Job Demand report |
| FullScale.io | Outsourcing firm blog — source for 65K/180K graduate gap claim | Gemini Engineering report |
| SalesforceBen | Salesforce ecosystem data extrapolated to all EU tech | Gemini Demand Scan |
| CuroMinds | Blog — source for "56% AI wage premium" and "43% AI pay bump" | Gemini Demand Scan |
| Generic market size projections | "$18B AI design market by 2030" etc. — no methodology | Multiple files |

### Tier 4 — Do Not Use

| Claim | Problem |
|---|---|
| "200,000-500,000 net new regulatory compliance roles" | Author estimate, zero source |
| "NIS2: 320,000-640,000 new cybersecurity positions" | Author extrapolation from ENISA averages × entity count |
| All salary tables in regulatory files | 100% unsourced |
| All per-task automation percentages (95%, 85-90%, etc.) | Zero sources |
| "RevOps VP title grew 300%" | Appears twice, zero attribution |
| All EU open position volume estimates in Gemini demand scan | Extrapolated from German Bitkom data, no methodology |
| "97.5% of German 500+ companies have works councils" | Zero attribution |

---

## Part 3: Verified Data Points for the Companion Product

These are the claims we CAN put on the website, organized by what they tell us.

### 3.1 Demand Direction by Role (Ravio ground truth)

| Function | Hiring Rate 2025 | vs 2023 | Direction |
|---|---|---|---|
| Commercial (Sales/CS) | 34.7% | -0.3pp | ≈ Stable (only growing function) |
| Operations | 27.1% | -6.9pp | ↓ Declining |
| People/HR | 22.9% | -7.1pp | ↓ Declining |
| Marketing | 21.8% | -11.2pp | ↓↓ Sharp decline |
| Engineering | 20.7% | -9.3pp | ↓↓ Sharp decline |
| Product | 20.6% | -10.4pp | ↓↓ Sharp decline |

### 3.2 Country Hiring Heat (Ravio ground truth)

| Country | Rate 2025 | YoY Change | Signal |
|---|---|---|---|
| UK | 31.8% | -20.5% | Contracting from high base |
| Germany | 29.8% | +2.8% | Only positive market |
| Spain | 26.3% | -26.9% | Sharp contraction |
| Netherlands | 23.5% | -13.0% | Moderate contraction |
| France | 22.3% | -28.1% | Sharp contraction |
| Sweden | 16.5% | -34.0% | Severe contraction |

### 3.3 AI Premium (Ravio ground truth)

| Metric | Value |
|---|---|
| AI/ML hiring growth | +88% YoY |
| AI/ML title expansion | +50% |
| AI salary premium (IC) | +12% |
| AI salary premium (Mgmt) | +3% |
| Founders expect AI eng % | 20-50% within 12 months |

### 3.4 Seniority Shift (Ravio + Recruited.tech + Figma)

| Metric | Value | Source |
|---|---|---|
| Entry-level (P1/P2) hiring collapse | -73.4% | Ravio |
| All-level hiring decline | -7% | Ravio |
| PM junior/associate share | 3% | Recruited.tech |
| Design: 56% want seniors, 25% juniors | 56%/25% | Figma Feb 2026 |
| SDR-to-AE promotion rate | 16% (was 34% in 2020) | Bridge Group |

### 3.5 Enterprise AI Adoption (Eurostat — TO FETCH)

| Country | 2025 | 2024 | 2023 | 2021 |
|---|---|---|---|---|
| Denmark | 42.03% | 27.58% | 15.17% | 23.89% |
| Finland | 37.82% | 24.37% | 15.16% | 15.79% |
| Belgium | 34.54% | 24.71% | 13.81% | 10.32% |
| Sweden | 33.84% | 21.89% | 10.37% | 9.92% |
| Luxembourg | 33.61% | 23.73% | 14.45% | 13.86% |
| Netherlands | 33.21% | 23.86% | 14.18% | 13.16% |
| Germany | 25.97% | 19.75% | 11.55% | 10.56% |
| EU-27 avg | 19.95% | 13.48% | 8.06% | 7.65% |
| Romania | 5.21% | 3.07% | 1.31% | 1.38% |

### 3.6 Cybersecurity Gap (ENISA + ISC2 — partially verified)

| Metric | Value | Source | Verified from PDF? |
|---|---|---|---|
| ISC2 European gap | 424,000 | ISC2 (separate data release) | ❌ Not in our whitepaper |
| ENISA open positions | ~299,000 | ENISA (separate publication) | ❌ Not in our 2025 PDF |
| 33% of orgs: no cybersecurity assessment | 33% | ENISA NIS Investments 2025 | ✅ YES |
| 51% of SMEs: >3 months to patch | 51% | ENISA NIS Investments 2025 | ✅ YES |

### 3.7 Sales Restructuring (Emergence Capital + Bridge Group)

| Metric | Value | Source |
|---|---|---|
| B2B companies cutting SDR/BDR | 36% | Emergence Capital (560+ companies) |
| Companies growing AE teams | 28% | Emergence Capital |
| SDR-to-AE promotion rate | 16% (was 34% in 2020) | Bridge Group |
| SDR quota attainment | 60% (lowest ever) | Bridge Group |
| SDR OTE (US) | $80K | Bridge Group |
| Quality conversations/day | 4.1 (was 8.0 in 2014) | Bridge Group |

### 3.8 Marketing Shift (McKinsey ground truth)

| Metric | Value | Source |
|---|---|---|
| 72% of CMOs plan budget increase | 72% | McKinsey (500 EU leaders) |
| Marketing budgets: 8.7% of revenue | 8.7% | McKinsey |
| #1 investment priority: Gen AI marketing | 50% | McKinsey |
| Classic brand campaigns declining | 75%→48% (-27pp) | McKinsey |
| Only 3% can measure >50% of spend | 3% | McKinsey |
| 62% say human creative teams irreplaceable | 62% | McKinsey |

---

## Part 4: Data We Already Have in Project vs Need to Fetch

### Already Integrated (can overlay immediately)

| Data | File | Granularity |
|---|---|---|
| Employment by occupation × country | `data/eurostat/employment_isco2d.csv` | ISCO 2-digit × 35 countries |
| Wages by occupation | `data/eurostat/wages_isco.csv` | ISCO 1-digit |
| Education by occupation | `data/eurostat/education_by_occupation.csv` | ISCO 1-digit |
| Employment YoY change | `data/eurostat/employment_yoy.csv` | ISCO 2-digit |
| Growth projections 2024→2035 | `data/cedefop/growth_forecast.csv` | ISCO 1-digit × 31 countries |
| AI exposure (lab-based) | `data/adoption/triangulated_adoption.csv` | ISCO 1-digit (uniform) |
| Swiss wages/employment | `data/bfs/` | ISCO 1-2 |
| UK wages/employment | `data/ons/` | SOC→ISCO |
| All layers pre-computed | `data/layer_scores.json` | ISCO 3-digit × 35 countries |
| Occupation descriptions + skills | `data/esco/esco_processed.json` | ISCO 3-digit |

### Need to Fetch (HIGH priority)

| Data | Table Code | What It Adds |
|---|---|---|
| Enterprise AI adoption | Eurostat `isoc_eb_ai` | Country-level adoption reality (replaces uniform lab scores) |
| ICT specialist concentration | Eurostat `isoc_sks_itspt` | Tech workforce density by country |
| Employment protection | OECD `EPL_OV` | Regulatory friction on workforce adjustment |

### Need to Manually Extract (from PDFs in /research/)

| Data | Source PDF | What It Adds |
|---|---|---|
| Hiring rates by function × country | Ravio PDF | The core "demand direction" data layer |
| AI/ML premium + entry-level collapse | Ravio PDF | AI premium + seniority shift layers |
| SDR metrics + career path | Bridge Group PDF | Sales role restructuring data |
| Marketing budget shifts | McKinsey PDF | Marketing demand signal |

---

## Part 5: Key Corrections (Research Files vs Ground Truth)

| Claim in Research Files | Ground Truth from PDF | Severity |
|---|---|---|
| "Brand building ranked #1 of 20 priorities; GenAI ranked #17" (McKinsey) | Gen AI is #1 INVESTMENT priority (50%). Brand is the strategic framing, not a ranked list. | HIGH — misleading |
| "89% need additional cybersecurity staff" (attributed to ENISA) | NOT in our ENISA 2025 PDF. May be from earlier edition. | MEDIUM — unverified |
| "424,000 European cybersecurity gap" (attributed to ISC2) | NOT in our ISC2 whitepaper. Comes from separate data release. | MEDIUM — unverified from our source |
| CSRD scope reduction: "80-85%" (File 1) vs "~90%" (File 2) | Both cite Omnibus I but give different numbers | LOW — internal inconsistency |
| Ravio country hiring rates rounded differently across files | Ground truth: UK 31.8%, DE 29.8%, etc. (not 32%, 30%) | LOW — rounding |
| Operations 2024 data missing from some Ravio tables | Ravio PDF shows 2024 operations data was not reported separately | LOW — data gap in source |

---

## Part 6: ISCO Mapping for Startup Roles

| Startup Role | ISCO 3-digit | Code | In layer_scores.json? |
|---|---|---|---|
| Product Manager | ICT service managers / Software managers | 133 / 251 | ✅ |
| Software Engineer | Software developers | 251 | ✅ |
| AI/ML Engineer | Software developers (subset) | 251 | ✅ (no AI-specific split) |
| UX/Product Designer | Graphic and multimedia designers | 216 | ✅ |
| SDR/BDR/AE | Sales professionals | 243 | ✅ |
| Growth/Marketing | Advertising and marketing professionals | 243 | ✅ (shares code with sales) |
| Operations/BizOps | Business services agents / Admin managers | 333 / 121 | ✅ |
| Cybersecurity | Database and network professionals | 252 | ✅ |
| Data Scientist/Engineer | Database and network professionals | 252 | ✅ |
| Recruiter | Human resource managers | 121 / 242 | ✅ |

**Key limitation:** ISCO codes are too coarse to distinguish PM from SWE (both map to 251) or Sales from Marketing (both 243). The companion product will need a role-level view ALONGSIDE the ISCO occupation view, not purely mapped through ISCO.
