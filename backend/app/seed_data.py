"""Seed data for JOBOS (spec 9, 11, 49).

Mirrors MASTER/EVIDENCE_LIBRARY.md and PROFILES/*/PROFILE.md. Loaded by app.seed.
All claims trace to the evidence library (anti-hallucination layer).
"""

USER = {
    "name": "S J Ruthvik",
    "email": "sjruthvik99@gmail.com",
    "phone": "+91 88928 65788",
}

PROFILES = [
    {
        "profile_id": "FINTECH_PM",
        "name": "Fintech PM",
        "target_roles": ["Product Manager", "Senior Product Manager", "Product Lead", "Product Owner"],
        "target_industries": ["Fintech", "Lending", "Wealthtech", "Payments", "Embedded finance", "B2B SaaS"],
        "target_locations": ["Bengaluru", "Remote"],
        "preferred_company_stage": ["Series A-C", "Growth"],
        "preferred_company_size": ["30-500"],
        "must_haves": [
            "Lending/fintech domain", "Product strategy", "Workflow/operations automation",
            "Product analytics", "Cross-functional leadership",
        ],
        "nice_to_haves": [
            "Payments rails", "Regtech/compliance", "Platform/API/SDK", "AI-assisted delivery",
        ],
        "dealbreakers": ["6+ years PM experience", "Systems-architecture-only", "Hardware field-validation"],
        "positioning_statement": (
            "Fintech product manager who ships lending platforms, repayment rails, and risk "
            "automation - 70% faster approval TAT, 30% lower NPA, 80% less manual ops."
        ),
        "headline": "Product Manager - Fintech (Lending · Risk · Payments Rails)",
        "summary": (
            "APM at Rang De (P2P lending) owning LOS/LMS, repayment rails and risk automation; "
            "Associate PM at Akteena (AI dashcam SDK); freelance PM in fintech product strategy."
        ),
        "skills": [
            "Product strategy", "Roadmapping", "Workflow automation", "Product analytics",
            "SQL", "Risk analytics", "Platform/SDK", "API integration", "Regtech/compliance",
            "Agile/Scrum", "Stakeholder management", "GTM",
        ],
        "domains": [
            "Digital lending", "LMS/LOS", "NPA/Risk", "Payments rails", "P2P",
            "Wealthtech", "Regtech", "Compliance", "Fintech ops",
        ],
        "experience_emphasis": [
            "Rang De: LMS TAT -70%, NPA -30%, manual ops -80%, LOS -40%/-45%",
            "Akteena: SDK/API docs, partner onboarding -40%, AIS compliance",
            "Freelance: EU wealthtech product strategy + compliance tooling",
        ],
        "resume_rules": [
            "Lead with Rang De",
            "Keep freelance wealthtech generic; never name the stealth company",
            "Do NOT claim Rang De platform-scale numbers as personal",
            "Use EVID-001/002/003/005/006/009/010/011",
        ],
    },
    {
        "profile_id": "B2B_SAAS_PM",
        "name": "B2B SaaS PM",
        "target_roles": ["Product Manager", "Senior Product Manager", "Platform/API/SDK PM", "Product Owner"],
        "target_industries": ["B2B SaaS", "Platform", "Developer tools", "Martech", "Fintech SaaS"],
        "target_locations": ["Bengaluru", "Remote"],
        "preferred_company_stage": ["Series A-D", "Growth"],
        "preferred_company_size": ["30-1000"],
        "must_haves": [
            "B2B/platform product management", "API/SDK/developer-docs",
            "Product strategy", "Partner/customer enablement", "Cross-functional leadership",
        ],
        "nice_to_haves": [
            "Enterprise/B2B go-to-market", "Market research + PMF",
            "AI-assisted delivery", "Technical breadth (IoT, embedded, SQL)",
        ],
        "dealbreakers": ["Consumer-only B2C focus", "Systems-architecture-only", "Hardware field-validation"],
        "positioning_statement": (
            "B2B SaaS/platform PM who owns SDK and API products end-to-end - built partner "
            "onboarding from scratch, cut ramp 40%, drove 2 roadmap shifts."
        ),
        "headline": "Product Manager - B2B SaaS / Platform / SDK",
        "summary": (
            "Associate PM at Akteena owning SDK + firmware roadmap, API docs (ReadMe), partner "
            "onboarding, AIS compliance; Product Analyst at Dell (presales, market analysis, PMF)."
        ),
        "skills": [
            "Product strategy", "Roadmapping", "Product lifecycle", "API/SDK",
            "Developer experience", "Partner enablement", "Market research",
            "Competitive analysis", "Product analytics", "SQL", "Agile/Scrum", "GTM",
        ],
        "domains": [
            "B2B SaaS", "Platform", "SDK/API", "Developer tools", "Enterprise storage",
            "Telematics/IoT", "Martech",
        ],
        "experience_emphasis": [
            "Akteena: SDK roadmap, API docs, partner onboarding -40%, compliance-GPT",
            "Dell: presales/sizing, market analysis + ~15% upside (estimate), PMF",
            "Freelance: WBC AI-assisted build, team leadership",
        ],
        "resume_rules": [
            "Lead with Akteena SDK/API/partner work, then Dell presales/market analysis",
            "Frame Dell ~15% strictly as estimated upside",
            "Keep WBC generic (IP agreement)",
            "Use EVID-006/007/008/009/013/015/016",
        ],
    },
    {
        "profile_id": "GENERAL_PM",
        "name": "General PM",
        "target_roles": ["Product Manager", "Senior Product Manager", "Product Lead", "Product Owner"],
        "target_industries": [
            "Healthtech", "Community", "Marketplace", "SaaS", "Fintech", "Any product-led org",
        ],
        "target_locations": ["Bengaluru", "Remote"],
        "preferred_company_stage": ["Series A-D", "Growth"],
        "preferred_company_size": ["30-1000"],
        "must_haves": [
            "End-to-end product management", "Product strategy + roadmapping",
            "User journeys + market research", "Cross-functional leadership",
            "Metrics-driven decisions",
        ],
        "nice_to_haves": [
            "Domain breadth", "AI-assisted delivery", "Analytics (SQL, Mixpanel, GA4)", "Team leadership",
        ],
        "dealbreakers": ["Systems-architecture-only", "Hardware field-validation", "Ultra-early solo-PM seat"],
        "positioning_statement": (
            "Versatile product manager who owns products end-to-end across fintech, healthtech "
            "and community platforms - from strategy to AI-assisted delivery."
        ),
        "headline": "Product Manager - End-to-End Delivery",
        "summary": (
            "Product lead at WBC (AI-assisted build, team of 3); PM at iHealth (patient community); "
            "APM at Rang De (workflow automation, risk); APM at Akteena (SDK + compliance)."
        ),
        "skills": [
            "Product strategy", "Roadmapping", "Product lifecycle", "New product design",
            "User journeys", "Market research", "Product analytics", "Agile/Scrum",
            "Stakeholder management", "AI-assisted delivery", "SQL", "Mixpanel", "GA4",
        ],
        "domains": [
            "Fintech", "Healthtech", "Community/social", "Marketplace", "Telematics",
            "Enterprise storage", "Platform/SDK",
        ],
        "experience_emphasis": [
            "Freelance: WBC end-to-end + team leadership + beta; iHealth journeys/recommendations",
            "Rang De: workflow automation, dashboards, risk",
            "Akteena: SDK roadmap, compliance, onboarding",
        ],
        "resume_rules": [
            "Lead with strongest most-relevant evidence per role",
            "Keep WBC + iHealth prelaunch-framed (no invented metrics)",
            "Never name stealth wealthtech",
            "Use EVID-013/014/001/002/003/006/009/016",
        ],
    },
]

EVIDENCE = [
    {
        "evidence_id": "EVID-001", "claim": "Reduced loan-workflow approval TAT ~70% via LMS redesign + automation",
        "company": "Rang De", "context": "LMS information architecture + automated verification; ~10-13 min to ~3-4 min per application",
        "metric": "-70% TAT", "strength": "Verified",
        "relevant_domains": ["Fintech", "Lending", "Workflow automation", "Operations"],
        "allowed_claims": ["Reduced TAT", "Workflow automation", "Product optimization", "Loan operations"],
        "forbidden_inferences": ["Payments orchestration", "Credit underwriting", "Fraud detection"],
    },
    {
        "evidence_id": "EVID-002", "claim": "Automated NPA/delinquency reporting via role-based dashboards, cutting manual data ops ~80%",
        "company": "Rang De", "context": "Replaced 4-5 hrs/day manual NPA calcs with automated dashboards",
        "metric": "-80% manual ops", "strength": "Verified",
        "relevant_domains": ["Fintech", "Lending", "Risk analytics", "Product analytics"],
        "allowed_claims": ["Reporting automation", "Risk dashboard", "Ops efficiency", "Product analytics"],
        "forbidden_inferences": ["Building the credit scoring model", "Originating risk policy"],
    },
    {
        "evidence_id": "EVID-003", "claim": "Reduced portfolio NPA ~30% via debit-card repayment rails + automated risk escalation",
        "company": "Rang De", "context": "Debit-card e-mandate rails (Razorpay experiment) + rule-based risk score + escalation ladder",
        "metric": "-30% NPA (12-13% to 8.5-9%)", "strength": "Verified",
        "relevant_domains": ["Fintech", "Lending", "Risk", "Payments rails", "Operations"],
        "allowed_claims": ["Repayment collections", "Risk automation", "NPA reduction", "Payment rails design", "Escalation workflows"],
        "forbidden_inferences": ["Credit underwriting", "Fraud detection", "Owned the risk scoring model", "Payments orchestration platform"],
    },
    {
        "evidence_id": "EVID-004", "claim": "Restructured approval flow cut reviewer man-hours ~30%",
        "company": "Rang De", "context": "Same basis as LMS TAT; estimate",
        "metric": "-30%", "strength": "Estimated",
        "relevant_domains": ["Fintech", "Lending", "Operations"],
        "allowed_claims": ["Approval flow optimization", "Operations efficiency"],
        "forbidden_inferences": ["Layoffs"],
    },
    {
        "evidence_id": "EVID-005", "claim": "LOS app revamp reduced drop-offs ~40% and failures ~45%",
        "company": "Rang De", "context": "Offline-first + save-as-draft + split submission + bulk upload; derived from ~50-60 field-agent interviews",
        "metric": "-40% / -45%", "strength": "Directional",
        "relevant_domains": ["Fintech", "Lending", "Field operations", "Mobile UX"],
        "allowed_claims": ["Field-agent app", "Origination UX", "Drop-off reduction", "Offline-first design"],
        "forbidden_inferences": ["System-measured funnel analytics", "Specific numeric funnel conversion"],
    },
    {
        "evidence_id": "EVID-006", "claim": "Built partner onboarding + API docs from scratch; cut ramp ~40%; onboarded 10 partners",
        "company": "Akteena", "context": "Self-serve module + ReadMe API portal + integration playbooks; ~20 to ~12 hrs ramp",
        "metric": "-40% ramp, 10 partners", "strength": "Verified",
        "relevant_domains": ["SDK/Platform", "B2B", "API", "Partner enablement", "Developer docs"],
        "allowed_claims": ["Partner onboarding", "API documentation", "Developer relations", "B2B enablement"],
        "forbidden_inferences": ["Reducing an existing 40% process (built from nothing)"],
    },
    {
        "evidence_id": "EVID-007", "claim": "Delivered 100% on-time launches across 3 major firmware/SDK releases",
        "company": "Akteena", "context": "Owned SDK + firmware roadmap; MVP to v1 to v2 scoping/timing",
        "metric": "100% on-time, 3 releases", "strength": "Verified",
        "relevant_domains": ["SDK/Platform", "Hardware", "Roadmapping", "Release management"],
        "allowed_claims": ["On-time delivery", "Roadmap ownership", "Release management"],
        "forbidden_inferences": ["Engineering headcount ownership"],
    },
    {
        "evidence_id": "EVID-008", "claim": "Competitive benchmarking drove 2 key roadmap shifts",
        "company": "Akteena", "context": "Competitive analysis set MVP floor, safety-feature sequencing, packaging",
        "metric": "2 roadmap shifts", "strength": "Verified",
        "relevant_domains": ["Product strategy", "Market research", "Roadmapping"],
        "allowed_claims": ["Competitive analysis", "Roadmap strategy", "Market research"],
        "forbidden_inferences": ["Quantified adoption increase"],
    },
    {
        "evidence_id": "EVID-009", "claim": "Led AIS regulatory compliance readiness (India) for ADAS/DMS dashcams; built internal compliance GPT",
        "company": "Akteena", "context": "Read entire AIS spec; checklists across analytics/AI/SDK/hardware; LLM chatbot for self-check",
        "metric": None, "strength": "Verified",
        "relevant_domains": ["Regtech", "Compliance", "ADAS/DMS", "AI-native product"],
        "allowed_claims": ["Compliance-as-product", "Regulatory readiness", "AI tooling", "ADAS/DMS requirements"],
        "forbidden_inferences": ["Multi-market compliance", "Engaged regulators/test agencies"],
    },
    {
        "evidence_id": "EVID-010", "claim": "Established product function from scratch for a stealth EU fintech; saved ~20 hrs/week",
        "company": "Stealth European Wealthtech", "context": "PRDs, goals, timelines, Jira stories, acceptance criteria, release strategy",
        "metric": "~20 hrs/week", "strength": "Verified",
        "relevant_domains": ["Fintech", "Wealthtech", "Product strategy", "Roadmapping"],
        "allowed_claims": ["Product strategy", "Roadmapping", "Establishing product function", "PRDs"],
        "forbidden_inferences": ["Naming the company", "Shipped product outcomes (pre-launch)"],
    },
    {
        "evidence_id": "EVID-011", "claim": "Built internal compliance-tracking data room + AI audit cross-reference; ~10-15% time saved",
        "company": "Stealth European Wealthtech", "context": "Document store + architecture diagram + regulator-portal scrapes; one-click AI audit",
        "metric": "~10-15% time", "strength": "Directional",
        "relevant_domains": ["Regtech", "Compliance", "Fintech"],
        "allowed_claims": ["Compliance tooling", "Documentation system", "Regulatory monitoring"],
        "forbidden_inferences": ["Company name", "Own product compliance sign-off"],
    },
    {
        "evidence_id": "EVID-012", "claim": "Designed a dynamic multi-tenant architecture for NGO hierarchies (shipped after he left)",
        "company": "Rang De", "context": "Initiated, architected, PRD'd; designed to cut partner setup ~1 week to ~3 days (~40%)",
        "metric": "~40% setup reduction (projected)", "strength": "Projected",
        "relevant_domains": ["Fintech", "Lending", "Multi-tenant SaaS", "Operations"],
        "allowed_claims": ["Architecture design", "PRDs", "Multi-tenant modeling", "Designed/projected to"],
        "forbidden_inferences": ["Setup reduction as delivered outcome"],
    },
    {
        "evidence_id": "EVID-013", "claim": "Led end-to-end build of a members + business directory for a US community network; beta traction",
        "company": "World's Best Connectors", "context": "Product lead, team of 3, AI-assisted build; beta: 300+ families, 25+ brands, ~30 users",
        "metric": "Beta traction", "strength": "Directional",
        "relevant_domains": ["Community platforms", "Social products", "Consumer directory", "Team leadership"],
        "allowed_claims": ["End-to-end delivery", "Team leadership", "AI-assisted development", "Early/beta traction"],
        "forbidden_inferences": ["Full-launch adoption", "Detailing proprietary features", "Revenue/retention"],
    },
    {
        "evidence_id": "EVID-014", "claim": "Owned search/sort/filter, user journeys, market research, recommendation logic for an NF patient network",
        "company": "iHealth and Wellness Foundation", "context": "Social + care-management network for Neurofibromatosis; prelaunch",
        "metric": None, "strength": "Directional",
        "relevant_domains": ["Healthtech", "Social product", "Recommendation systems", "Search"],
        "allowed_claims": ["User journeys", "Search & filtering", "Recommendation/feed logic", "Market research"],
        "forbidden_inferences": ["Adoption/engagement numbers", "Shipped outcomes (prelaunch)"],
    },
    {
        "evidence_id": "EVID-015", "claim": "Identified an estimated ~15% field-sales upside via market analysis + product-placement strategy",
        "company": "Dell Technologies", "context": "Emerging-market analysis; targeted SaaS in South India on AWS; estimated pipeline improvement",
        "metric": "~15% (estimate)", "strength": "Estimated",
        "relevant_domains": ["Enterprise storage", "Market analysis", "PMF", "B2B"],
        "allowed_claims": ["Market analysis", "Product placement", "Identified an estimated ~15% upside"],
        "forbidden_inferences": ["Realized sales increase"],
    },
    {
        "evidence_id": "EVID-016", "claim": "Built a complete EV telematics system end-to-end (hardware + software) as an intern",
        "company": "Log 9 Materials", "context": "TCU design + AWS/CI-CD + IoT battery/GPS streaming + Power BI; Log 9 productized the software",
        "metric": None, "strength": "Verified",
        "relevant_domains": ["IoT", "Embedded", "EV", "Telematics", "Cloud", "Data engineering"],
        "allowed_claims": ["Telematics", "IoT", "Hardware design", "Cloud/API build", "Technical breadth"],
        "forbidden_inferences": ["Shipped production EV product as his own", "Fleet outcomes as personal metrics"],
    },
    {
        "evidence_id": "EVID-017", "claim": "Authored a PRD to grow smallcase monthly transacting users 15% (approved by a Senior PM at PayPal)",
        "company": "Upraised", "context": "Fellowship case study resolving payment-related churn; NOT a shipped result",
        "metric": "15% growth target (case study)", "strength": "Case-study",
        "relevant_domains": ["Fintech", "Product management", "Churn"],
        "allowed_claims": ["PRD", "Case study", "Problem framing for payment-related churn"],
        "forbidden_inferences": ["Realized 15% growth at smallcase"],
    },
    {
        "evidence_id": "EVID-018", "claim": "Supported a lending platform that disbursed Rs 94 Cr+ to 25,000+ borrowers across 29 states",
        "company": "Rang De", "context": "Platform/program outcomes, NOT personal metrics; role was adapting LOS/LMS to support programs",
        "metric": "Rs 94 Cr+ / 25,000+ borrowers (platform)", "strength": "Verified",
        "relevant_domains": ["Fintech", "Lending", "P2P"],
        "allowed_claims": ["Supported a lending platform that disbursed Rs 94 Cr+", "Program enablement"],
        "forbidden_inferences": ["Claiming platform numbers as personal achievements"],
    },
]
