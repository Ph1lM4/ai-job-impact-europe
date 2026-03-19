# AI labs' labor market research: a complete inventory

**Microsoft Research is the only major lab besides Anthropic to publish real AI usage data mapped to occupational classifications.** Its July 2025 "Working with AI" paper analyzed 200,000 Bing Copilot conversations mapped to O*NET work activities — the closest methodological parallel to Anthropic's Economic Index. OpenAI published the foundational theoretical exposure framework ("GPTs are GPTs," 2023) and later released real ChatGPT usage analysis, but never combined the two into an occupation-mapped usage index. Google DeepMind has published zero direct labor market exposure research, though it is actively building capacity by hiring a Chief AGI Economist (January 2026). xAI has published nothing on this topic whatsoever. Meta AI/FAIR has produced no first-party labor market research, outsourcing its only relevant study to the Linux Foundation. For a European AI Exposure Map dashboard mapping to ISCO 3-digit groups, the most interoperable datasets are Anthropic's Economic Index (O*NET → SOC, open on HuggingFace) and Microsoft's "Working with AI" (O*NET → SOC, open on GitHub), both of which require SOC-to-ISCO crosswalking.

---

## OpenAI built the theoretical foundation, then pivoted to usage analysis

OpenAI's contribution to AI labor market research is anchored by two distinct phases: an influential 2023 theoretical framework, and a 2025 pivot toward real-world usage measurement under its first Chief Economist.

**"GPTs are GPTs" (March 2023, published in *Science* June 2024)** remains the single most-cited AI labor exposure paper. Authored by Tyna Eloundou, Sam Manning, Pamela Mishkin, and Daniel Rock (Wharton), it classified all **O*NET tasks and Detailed Work Activities** across U.S. occupations into exposure categories (E0–E3) using both human annotators and GPT-4 as a classifier. The paper found **~80% of the U.S. workforce** could see at least 10% of tasks affected by LLMs, with **47–56% of all tasks** potentially impacted when accounting for LLM-powered software. Higher-income occupations faced greater exposure — a reversal of traditional automation patterns. The dataset of occupation-level exposure scores was released as a CSV file alongside the *Science* publication, using SOC codes linked to BLS employment and wage data. Critically, this was entirely a theoretical/expert assessment: it scored what LLMs *could* do, not what they actually *were* doing.

OpenAI extended this in 2025 with **"Extending GPTs are GPTs to Firms"** (AEA Papers and Proceedings), which merged the task-level exposure scores with Revelio Labs resume data to compute firm-level LLM exposure for publicly traded companies. The mean firm showed E1 exposure of 0.17 and maximum exposure of 0.77.

The second phase began with Aaron "Ronnie" Chatterji's appointment as OpenAI's first Chief Economist in 2024. His team produced **"How People Are Using ChatGPT"** (NBER Working Paper 34255, September 2025), a privacy-preserving analysis of **~1.5 million de-identified ChatGPT conversations** from 130,000 users. This is the largest published study of consumer AI chatbot usage. Key findings: **~30% of usage is work-related**, writing dominates work tasks (~40% of work messages), and two-thirds of writing interactions involve editing rather than generation from scratch. However, the study classified conversations by topic category rather than mapping them to O*NET occupations — a crucial distinction from Anthropic's approach.

OpenAI also released **GDPval** (September 2025), a benchmark of **1,320 real-world tasks across 44 knowledge-work occupations** in 9 GDP-heavy sectors. While not a usage study, it measures frontier model performance against human experts on economically valuable tasks, using O*NET definitions and BLS wage data. The gold set of **220 tasks is open-sourced on HuggingFace** (openai/gdpval). The best models approached human expert quality on ~47.6% of tasks while operating **~100× faster and ~100× cheaper**.

An affiliated paper worth noting: **"Winners and Losers of Generative AI"** (Journal of Economic Behavior & Organization, 2025), co-authored by Pamela Mishkin, found that generative AI cut freelance platform demand for substitutable skill clusters by **up to 50%** in short-term roles, while complementary AI skill demand increased.

- **Classification systems used:** O*NET tasks/DWAs, SOC codes, BLS OOH (all U.S.-centric)
- **Open datasets:** GPTs are GPTs occupation scores (GitHub CSV), GDPval gold set (HuggingFace)
- **Notable gap:** No Anthropic-style index combining real usage data with occupational mapping

---

## Microsoft Research produced the closest parallel to Anthropic's Economic Index

Microsoft's research output is the richest among all labs surveyed, driven by an established economics research group, real telemetry from Copilot products, and LinkedIn's labor market data. The flagship study is methodologically the most comparable to Anthropic's work.

**"Working with AI: Measuring the Applicability of Generative AI to Occupations"** (Tomlinson, Jaffe, Wang, Counts, Suri; arXiv July 2025) analyzed **200,000 anonymized Bing Copilot conversations** (January–September 2024) using an LLM pipeline to classify each conversation into O*NET Intermediate Work Activities (IWAs). Like Anthropic's index, it distinguishes between what the *user* seeks help with ("user goals") and what *AI itself performs* ("AI actions") — directly paralleling Anthropic's augmentation-versus-automation distinction. Results are aggregated at both the IWA and occupation level (detailed 2018 SOC codes). The most common AI-assisted activities involve **information gathering and writing**; the most common AI-performed activities are **providing information, writing, teaching, and advising**. AI applicability was highest for knowledge-work occupations requiring at least a bachelor's degree, and lowest for healthcare support and physical labor. The **full dataset is open-sourced on GitHub** (microsoft/working-with-ai), with v1.1 adding physical task classification and nonphysical AI applicability scores. The authors explicitly caution against interpreting applicability scores as job displacement predictions.

Microsoft's second major contribution is **"Early Impacts of M365 Copilot"** (Dillon, Jaffe, Peng, Cambon; arXiv April 2025), a **randomized controlled trial with 6,000+ workers at 56 firms**. Workers with Copilot access spent **30 fewer minutes per week reading email** and completed documents **12% faster**, with ~40% of licensed workers becoming regular users. This is the most rigorous causal evidence of enterprise AI productivity impact from any lab, though it measures behavioral changes rather than task-level occupational exposure and is not open-sourced.

Additional Microsoft studies include three **field experiments on GitHub Copilot** with software developers (Cui et al., 2024), a **Copilot for Security RCT** finding novices became 44% more accurate, and a series of **AI and Productivity Reports** synthesizing internal studies. The 2024 report documented that Dynamics 365 Customer Service agents achieved **12% faster case resolution** with Copilot.

Microsoft's **Work Trend Index** reports (annual joint publications with LinkedIn) provide the broadest workforce survey data: **31,000 people across 31 countries** annually. The 2024 edition found **75% of knowledge workers** already using AI, with **78% bringing their own AI tools** to work. The 2025 edition introduced the "Frontier Firm" concept and reported **82% of leaders** planning to deploy AI agents within 18 months.

LinkedIn's **Economic Graph** research contributes international labor market data, including AI talent concentration metrics shared with the OECD.AI platform. LinkedIn data shows AI hiring surged **323% over 8 years**, with AI-related job postings growing 70%+ year-over-year. This data is available through the OECD.AI dashboard and covers OECD member countries.

Microsoft also established the **AI Economy Institute (AIEI)**, which publishes semi-annual **AI Diffusion Reports** using Microsoft telemetry. The H2 2025 report found **16.3% of the world's population** using generative AI, with the Global North at 24.7% versus Global South at 14.1%.

- **Classification systems used:** O*NET IWAs/GWAs, 2018 SOC codes (Working with AI); industry/occupation categories (Copilot RCT); LinkedIn's proprietary skills taxonomy
- **Open datasets:** Working with AI occupation-level scores (GitHub), LinkedIn data to OECD.AI
- **Key strength:** Only lab with both real usage mapping to O*NET AND causal RCT evidence

---

## Google DeepMind has built capability frameworks but no labor market analysis

Despite being one of the world's leading AI research organizations, **Google DeepMind has published zero papers directly mapping AI capabilities to occupations or measuring labor market exposure.** This is the most significant gap among the labs surveyed. Their relevant work is entirely in adjacent territory: AGI capability taxonomies and governance frameworks.

**"Levels of AGI"** (Morris, Sohl-Dickstein, Fiedel et al.; November 2023, ICML 2024) proposed a taxonomy of AI performance with five levels from "Emerging" to "Superhuman," classifying current LLMs as "Emerging AGI." The paper explicitly discusses the concept of "economically valuable work" as one definition of AGI (referencing OpenAI's charter) but **does not perform any occupational analysis or use any labor classification system**. It calls for "ecologically valid task benchmarks" — a gap the lab has not yet filled for labor applications.

**"Measuring Progress Toward AGI: A Cognitive Taxonomy"** (Burnell, Yamamori et al.; March 2026) developed 10 cognitive faculties (Perception, Generation, Reasoning, etc.) for comparing AI to human capabilities, launched alongside a **$200,000 Kaggle hackathon**. While potentially foundational for future labor analysis, it uses a cognitive science taxonomy rather than occupational classifications.

The **"Intelligent AI Delegation Framework"** (Tomašev, Franklin, Osindero; February 2026) is DeepMind's most workforce-relevant paper. It proposes "cognitive maintenance delegation" — deliberately assigning tasks to humans that AI could handle, to prevent skill atrophy. The concept of the "automation paradox" and curriculum-aware routing directly addresses human-AI work division, but remains theoretical with no empirical data.

Two institutional signals suggest DeepMind is building capacity in this area. In **January 2026, Shane Legg announced hiring for a "Chief AGI Economist"** to study post-AGI economic transformations — scarcity, wealth distribution, and labor market restructuring. The job posting stated AGI is "on the horizon." Additionally, a **partnership with the UK AI Security Institute (AISI)** explicitly plans to "explore the potential impact of AI on economic systems by simulating real-world tasks across different environments" and "predict factors like long-term labour market impact." No outputs have been published from either initiative as of March 2026.

Allan Dafoe, DeepMind's Director of Frontier Safety, founded the **Centre for the Governance of AI (GovAI)**, which has published labor-adjacent work including "How Adaptable Are American Workers to AI-Induced Job Displacement?" (Manning & Aguirre, NBER 2026) using O*NET data. This was published through GovAI/Brookings, not as a DeepMind paper.

- **Classification systems used:** None (no O*NET, SOC, or ISCO)
- **Open datasets:** None related to labor markets
- **Status:** Capability-building phase; no empirical labor market research yet

---

## xAI and Meta represent a research void on workforce impact

**xAI has produced zero published research on AI labor market impact.** A thorough search of xAI's publications page, academic databases, and researcher profiles yielded no papers, reports, datasets, or blog posts on employment, workforce automation, job exposure, or economic effects. xAI's entire publication record consists of model release announcements (Grok 1 through 4.1), API documentation, and infrastructure updates. The company employs no identified labor economists or policy researchers. Elon Musk has made informal statements on X claiming "AI and robots will replace all jobs" (October 2025) and that "work will be optional," but xAI itself has not produced any research supporting or examining these claims.

**Meta AI/FAIR has likewise produced no first-party labor market research.** FAIR's publication portfolio is focused entirely on foundational AI capabilities (SAM, DINO, V-JEPA, Llama). Meta's only engagement with this topic comes through two indirect channels. First, it commissioned the **Linux Foundation report "The Economic and Workforce Impacts of Open Source AI"** (May 2025), a literature review finding that 89% of organizations using AI leverage open-source models and projecting AI-related wage increases of up to 20%. The framing is notably favorable to open-source AI, aligning with Meta's Llama strategy. Second, Meta hosted a **"Generative AI, Labor, and Upskilling Workshop"** acknowledged in academic papers, though no published outputs from Meta researchers emerged from it. Internally, Meta has aggressive AI adoption programs (AI performance reviews, gamification), but these are workforce management policies, not published research.

The Foundation for American Innovation has explicitly named both xAI and Meta as companies that should share anonymized AI usage data for labor market research — underscoring that policymakers recognize these data gaps.

---

## How these datasets map to ISCO for a European exposure dashboard

For a dashboard covering **125 ISCO 3-digit groups × 36 countries**, the practical question is which datasets can be crosswalked to ISCO. Here is a direct assessment:

| Dataset | Classification | Open? | Path to ISCO-08 |
|---|---|---|---|
| **Anthropic Economic Index** | O*NET tasks → SOC codes | Yes (HuggingFace) | SOC → ISCO-08 via BLS/ILO crosswalk tables |
| **Microsoft "Working with AI"** | O*NET IWAs → 2018 SOC | Yes (GitHub) | SOC → ISCO-08 via same crosswalk |
| **OpenAI "GPTs are GPTs"** | O*NET tasks → SOC | Yes (CSV) | SOC → ISCO-08 via same crosswalk |
| **OpenAI GDPval** | O*NET occupation definitions | Yes (HuggingFace) | SOC → ISCO-08 (limited to 44 occupations) |
| **LinkedIn Economic Graph** | Proprietary skills taxonomy | Partial (OECD.AI) | Already mapped to ISCO by OECD |
| **Microsoft Work Trend Index** | Not occupation-coded | No | Not directly mappable |
| **Google DeepMind** | None | N/A | N/A |
| **xAI / Meta** | None | N/A | N/A |

The **SOC-to-ISCO crosswalk** is the critical bridge. The BLS and ILO both publish concordance tables mapping 6-digit SOC codes to 4-digit ISCO-08 codes, which aggregate cleanly to ISCO 3-digit groups. The three open O*NET-based datasets (Anthropic, Microsoft, OpenAI) can all be crosswalked through this pipeline. However, two caveats apply. First, the crosswalk is many-to-many at fine granularity — some SOC codes split across ISCO groups — requiring weighted averaging based on employment shares. Second, all three datasets reflect **U.S.-specific task structures and AI adoption patterns**; European occupational task content may differ, particularly for regulated professions.

The **most valuable combination** for a European dashboard would be: Anthropic's Economic Index for observed-versus-theoretical exposure scores, Microsoft's "Working with AI" for a second real-usage validation point, and OpenAI's "GPTs are GPTs" for the theoretical exposure ceiling. LinkedIn's OECD.AI data could add country-level AI talent density by ISCO group. Layering these provides both the "what AI could do" and "what AI is actually doing" dimensions the user's dashboard concept requires.

---

## Conclusion

The AI lab landscape for labor market research is strikingly uneven. **Only Anthropic and Microsoft have published occupation-level analyses using real AI usage data** — the gold standard for measuring what AI is *actually* doing in the workforce rather than what it could theoretically do. OpenAI's foundational "GPTs are GPTs" framework set the theoretical baseline that almost every subsequent study references, but the lab itself has not closed the loop by mapping its massive ChatGPT usage data to occupational classifications. Google DeepMind's complete absence from empirical labor market research — despite its resources and influence — represents the single largest gap, though the Chief AGI Economist hire and AISI partnership signal this will change. xAI's total absence is consistent with its singular focus on model development. Meta's outsourcing of its only relevant study reveals a strategic choice to treat workforce research as a policy communication exercise rather than a scientific priority.

For the European AI Exposure Map, three open datasets offer actionable starting points: **Anthropic's Economic Index on HuggingFace, Microsoft's "Working with AI" on GitHub, and OpenAI's GPTs are GPTs exposure scores** — all crosswalkable from SOC to ISCO-08. The key insight across all studies is convergent: AI's observed real-world usage is concentrated in **information work — writing, information gathering, and communication** — and remains far narrower than theoretical capability scores would predict. Anthropic's finding that only 35.8% of Computer & Math tasks show observed exposure despite 94% theoretical exposure is echoed by Microsoft's finding that information-gathering and writing dominate actual Copilot usage, even for occupations with broad theoretical applicability. This observed-versus-theoretical gap should be a central design feature of any exposure dashboard.