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
