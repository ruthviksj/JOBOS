# EVIDENCE_LIBRARY — S J Ruthvik

> **The anti-hallucination layer.** Every significant professional claim maps to an
> evidence record. The matching agent may ONLY assert what an allowed claim here
> supports. If a JD requirement has no supporting evidence, classify it
> `NO EVIDENCE` — never fabricate.

**Strength legend:** Verified · Estimated · Directional (interview-derived) · Case-study (NOT shipped) · Projected (designed, shipped after he left).

---

## EVID-001 — LMS approval TAT −70%
- **Claim:** Reduced loan-workflow approval turnaround time by ~70% via LMS redesign and automation.
- **Company:** Rang De
- **Context:** Redesigned LMS information architecture + automated verification/cross-checks (Aadhaar/PAN, risk score, image liveness). Approval ~10–13 min → ~3–4 min per application.
- **Metric:** −70% (approx 10–13 → 3–4 min)
- **Strength:** Verified (measurement, with before/after basis)
- **Relevant domains:** Fintech, Lending, Workflow automation, Operations
- **Allowed claims:** Reduced TAT · Workflow automation · Product optimization · Loan operations
- **Forbidden inference:** Payments orchestration · Credit underwriting · Fraud detection · Direct lending P&L ownership

## EVID-002 — Manual data ops −80%
- **Claim:** Automated NPA/delinquency reporting via role-based dashboards, cutting manual data ops ~80%.
- **Company:** Rang De
- **Context:** Replaced 4–5 hrs/day of hand-calculated NPA %, rolling NPA, moving averages with automated metrics dashboards.
- **Metric:** −80% (≈4–5 hrs/day manual calc eliminated)
- **Strength:** Verified (estimate, shipped)
- **Relevant domains:** Fintech, Lending, Risk analytics, Product analytics, Ops tooling
- **Allowed claims:** Reporting automation · Risk dashboard · Ops efficiency · Product analytics
- **Forbidden inference:** Building the credit scoring model · Originating risk policy

## EVID-003 — NPA −30%
- **Claim:** Reduced portfolio NPA ~30% (≈12–13% → ≈8.5–9%) via debit-card repayment rails and automated risk escalation.
- **Company:** Rang De
- **Context:** Two owned parts: (A) debit-card e-mandate repayment rails (RBI banned UPI on virtual accounts; ran 3-mandate experiment w/ Razorpay, owned end-to-end) + (B) rule-based daily risk score per org (Safe/Unsafe/Danger) + escalation ladder w/ human-in-the-loop.
- **Metric:** −30% (12–13% → 8.5–9%)
- **Strength:** Verified (realized, defensible as estimate)
- **Relevant domains:** Fintech, Lending, Risk, Payments rails, Operations
- **Allowed claims:** Repayment collections · Risk automation · NPA reduction · Payment rails design · Escalation workflows
- **Forbidden inference:** Credit underwriting · Fraud detection · Owned the risk scoring model (risk team owned weights) · Payments orchestration platform

## EVID-004 — Reviewer man-hours −30%
- **Claim:** Restructured approval flow cut reviewer man-hours ~30%.
- **Company:** Rang De
- **Context:** Same basis as LMS TAT; estimate.
- **Metric:** −30%
- **Strength:** Estimated
- **Relevant domains:** Fintech, Lending, Operations
- **Allowed claims:** Approval flow optimization · Operations efficiency
- **Forbidden inference:** Layoffs / headcount reduction

## EVID-005 — LOS drop-offs −40% / failures −45%
- **Claim:** LOS app revamp reduced drop-offs ~40% and failures ~45%.
- **Company:** Rang De
- **Context:** Offline-first + save-as-draft, split text/photo submission, bulk upload, per-document API triggers, consent overhaul. Derived from interviewing ~50–60 of ~100 field agents (before-vs-after profiles completed, not a system counter).
- **Metric:** −40% / −45%
- **Strength:** Directional (interview-derived estimate)
- **Relevant domains:** Fintech, Lending, Field operations, Mobile UX, Offline-first
- **Allowed claims:** Field-agent app · Origination UX · Drop-off reduction · Offline-first design
- **Forbidden inference:** System-measured funnel analytics · Specific numeric funnel conversion without backup

## EVID-006 — Partner onboarding ramp −40%, 10 partners
- **Claim:** Built partner onboarding + API docs from scratch; cut ramp ~40% (~20 → ~12 hrs); onboarded 10 partners (1 enterprise, rest B2B).
- **Company:** Akteena
- **Context:** No onboarding existed before; built self-serve module + ReadMe API portal + integration playbooks. First customer had multiple business units.
- **Metric:** −40% (20 → 12 hrs), 10 partners
- **Strength:** Verified (estimate for the 40%; 10 partners confirmed)
- **Relevant domains:** SDK/Platform, B2B, API, Partner enablement, Developer docs
- **Allowed claims:** Partner onboarding · API documentation · Developer relations · B2B enablement
- **Forbidden inference:** Claiming the ~40% as reducing an existing process (it was built from nothing)

## EVID-007 — 100% on-time launches, 3 releases
- **Claim:** Delivered 100% on-time launches across 3 major firmware/SDK releases.
- **Company:** Akteena
- **Context:** Owned SDK + firmware roadmap; MVP → v1 → v2 scoping/timing, 3 review/release cycles.
- **Metric:** 100% on-time, 3 releases
- **Strength:** Verified (self-reported) · 💬 3 releases named? 🔲
- **Relevant domains:** SDK/Platform, Hardware, Roadmapping, Release management
- **Allowed claims:** On-time delivery · Roadmap ownership · Release management
- **Forbidden inference:** Engineering headcount/capacity ownership

## EVID-008 — Competitive benchmarking → 2 roadmap shifts
- **Claim:** Competitive benchmarking drove 2 key roadmap shifts, improving positioning & partner adoption.
- **Company:** Akteena
- **Context:** Ran competitive analysis to set MVP feature floor, safety-feature sequencing, packaging calls.
- **Strength:** Verified
- **Relevant domains:** Product strategy, Market research, Roadmapping
- **Allowed claims:** Competitive analysis · Roadmap strategy · Market research
- **Forbidden inference:** Quantified adoption increase

## EVID-009 — AIS compliance + compliance-GPT
- **Claim:** Led AIS regulatory compliance readiness (India) for ADAS/DMS dashcams; built an internal "compliance GPT."
- **Company:** Akteena
- **Context:** Read entire AIS spec (law being written, mandated ~2026); converted to checklists across analytics/AI/SDK/hardware; per-feature success criteria; LLM chatbot for team + client self-check.
- **Strength:** Verified (scope strictly India/AIS)
- **Relevant domains:** Regtech, Compliance, ADAS/DMS, AI-native product
- **Allowed claims:** Compliance-as-product · Regulatory readiness · AI tooling · ADAS/DMS requirements
- **Forbidden inference:** Multi-market/global compliance (India/AIS only) · Engaged regulators/test agencies (did not)

## EVID-010 — Product function built from scratch + ~20 hrs/wk saved (stealth wealthtech)
- **Claim:** Established the product function from scratch for a stealth EU fintech; saved team ~20 hrs/week of back-and-forth.
- **Company:** Stealth European Wealthtech (NDA — never name)
- **Context:** No product team existed; wrote PRDs, goals, timelines, Jira stories, acceptance criteria, release strategy, post-launch metrics/test plans.
- **Metric:** ~20 hrs/week saved
- **Strength:** Verified (self-reported, directional)
- **Relevant domains:** Fintech, Wealthtech, Product strategy, Roadmapping
- **Allowed claims:** Product strategy · Roadmapping · Establishing product function · PRDs
- **Forbidden inference:** Naming the company · Claiming shipped product outcomes (pre-launch)

## EVID-011 — Internal compliance tracking + ~10–15% time saved
- **Claim:** Built an internal compliance-tracking "data room" + AI audit cross-reference; ~10–15% time saved.
- **Company:** Stealth European Wealthtech
- **Context:** Document store capturing data-flow design + architecture diagram, updated with new ministry orders (scraped from regulator portal); one-click AI audit cross-references docs vs current rules.
- **Strength:** Directional
- **Relevant domains:** Regtech, Compliance, Fintech
- **Allowed claims:** Compliance tooling · Documentation system · Regulatory monitoring
- **Forbidden inference:** Company name · Own product compliance sign-off

## EVID-012 — Multi-tenant architecture (~40% partner setup reduction) — PROJECTED
- **Claim:** Designed a dynamic multi-tenant architecture for NGO hierarchies (shipped after he left).
- **Company:** Rang De
- **Context:** Initiated, architected, PRD'd; large-scale build ~2 months; saw only an early run-through before exit. Designed to cut partner setup ~1 week → ~3 days (~40%).
- **Strength:** Projected (designed to; NOT a realized result)
- **Relevant domains:** Fintech, Lending, Multi-tenant SaaS, Operations
- **Allowed claims:** Architecture design · PRDs · Multi-tenant modeling · "Designed/projected to..."
- **Forbidden inference:** Claiming the ~40% / setup reduction as a delivered outcome

## EVID-013 — WBC early traction (beta)
- **Claim:** Led end-to-end build of a members + business directory for a US community network; early traction in beta.
- **Company:** World's Best Connectors (name OK)
- **Context:** Product lead, led team of 3, AI-assisted build, full beta + design docs. Beta: 300+ families/athletes, 25+ businesses/brands, ~30 active users. 🔒 IP agreement — generic description only.
- **Strength:** Directional (beta/early traction, not full-launch adoption)
- **Relevant domains:** Community platforms, Social products, Consumer directory, Team leadership
- **Allowed claims:** End-to-end delivery · Team leadership (3) · AI-assisted development · Early/beta traction
- **Forbidden inference:** Full-launch adoption/engagement metrics · Detailing proprietary features · Revenue/retention

## EVID-014 — iHealth product ownership (scope/ownership)
- **Claim:** Owned search/sort/filter, user journeys, market research, and recommendation logic for an NF patient-care network.
- **Company:** iHealth and Wellness Foundation (name OK)
- **Context:** Social + care-management network for Neurofibromatosis ("LinkedIn for NF"); prelaunch, no adoption metrics. 🔲 metric backup.
- **Strength:** Directional (scope/ownership only)
- **Relevant domains:** Healthtech, Social product, Recommendation systems, Search
- **Allowed claims:** User journeys · Search & filtering · Recommendation/feed logic · Market research
- **Forbidden inference:** Adoption/engagement numbers · Shipped product outcomes (prelaunch)

## EVID-015 — Dell ~15% field-sales upside — ESTIMATE, NOT realized
- **Claim:** Identified an estimated ~15% field-sales upside via market analysis + product-placement strategy.
- **Company:** Dell Technologies
- **Context:** Emerging-market analysis; targeted SaaS in South India on AWS shifting to on-prem. Projected/estimated pipeline improvement.
- **Strength:** Estimated/projected (NOT realized)
- **Relevant domains:** Enterprise storage, Market analysis, PMF, B2B
- **Allowed claims:** Market analysis · Product placement · "Identified an estimated ~15% upside"
- **Forbidden inference:** Claiming ~15% as a realized sales increase

## EVID-016 — Log 9 EV telematics build (Technical PM anchor)
- **Claim:** Built a complete EV telematics system end-to-end (hardware + software) as an intern.
- **Company:** Log 9 Materials
- **Context:** Designed TCU (every component/circuit, manufactured), AWS + CI/CD, IoT battery+GPS streaming, S3/registry + APIs, Power BI dashboard. Didn't ship as-is; Log 9 productized the software + used his hardware in EVs sold to delivery fleets.
- **Strength:** Verified (build done; adoption by company confirmed)
- **Relevant domains:** IoT, Embedded, EV, Telematics, Cloud, Data engineering
- **Allowed claims:** Telematics · IoT · Hardware design · Cloud/API build · Technical breadth
- **Forbidden inference:** Shipped production EV product as his own · Claiming fleet outcomes as personal metrics

## EVID-017 — Upraised smallcase 15% PRD — CASE STUDY
- **Claim:** Authored a PRD to grow smallcase monthly transacting users 15% (approved by a Senior PM at PayPal).
- **Company:** Upraised (fellowship case study)
- **Context:** Fellowship project resolving payment-related churn. NOT a shipped result.
- **Strength:** Case-study
- **Relevant domains:** Fintech, Product management, Churn/payments
- **Allowed claims:** PRD · Case study · Problem framing for payment-related churn
- **Forbidden inference:** Claiming a realized 15% growth at smallcase

## EVID-018 — Rang De platform scale (context only, NOT personal)
- **Claim (context):** Supported a lending platform that disbursed ₹94 Cr+ to 25,000+ borrowers across 29 states (RBI-licensed NBFC-P2P); FY24–25: ₹17.49 Cr, 4,150 borrowers, 97% satisfaction, 64% women.
- **Company:** Rang De
- **Attribution:** These are Rang De platform/program outcomes delivered with impact partners — NOT Ruthvik's personal metrics. His role: rapidly adapted LOS/LMS to support each program. Never claim program headline numbers as his own.
- **Strength:** Context (citable as platform scale, not personal impact)
- **Allowed claims:** "Supported a lending platform that disbursed ₹94 Cr+ / 25,000+ borrowers" · Program-enablement framing
- **Forbidden inference:** Claiming disbursement/borrower/impact numbers as personal achievements

---

## Evidence matching rules

1. For each JD requirement, search the library; classify: `DIRECT`, `TRANSFERABLE`, `WEAKLY RELATED`, `NO EVIDENCE`, `CONTRADICTED`.
2. The compatibility engine weights Evidence strength (Verified > Estimated > Directional > Case-study/Projected).
3. Never assert a claim outside its `allowed_claims`. Never cross a `forbidden_inference`.
4. No evidence for a requirement → score `NO EVIDENCE`, do not invent.
