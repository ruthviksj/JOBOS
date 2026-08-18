"""Tests for the compatibility engine (spec 16-17, 23)."""

from app.compatibility import classify_requirement, recommend_profile, score_job

FIN_REQ = [
    {"text": "Product management experience", "kind": "requirement"},
    {"text": "Fintech lending domain", "kind": "requirement"},
    {"text": "Risk analytics", "kind": "requirement"},
    {"text": "Payments rails", "kind": "requirement"},
]

PLATFORM_REQ = [
    {"text": "SDK and API product management", "kind": "requirement"},
    {"text": "Partner onboarding", "kind": "requirement"},
    {"text": "Developer documentation", "kind": "requirement"},
]

FIN_JOB = {
    "title": "Senior Product Manager", "industry": "Fintech",
    "location": "Bengaluru", "remote_policy": "Hybrid",
    "minimum_experience": 4.0, "salary_min": None, "salary_max": None,
}

PLATFORM_JOB = {
    "title": "Platform Product Manager", "industry": "Developer Tools",
    "location": "Bengaluru", "remote_policy": "Remote",
    "minimum_experience": 3.0, "salary_min": None, "salary_max": None,
}

PROFILES = [
    {"profile_id": "FINTECH_PM", "name": "Fintech PM",
     "skills": ["Product strategy", "Product analytics", "SQL", "Risk analytics",
                "Platform/SDK", "API integration"],
     "domains": ["Digital lending", "LMS/LOS", "NPA/Risk", "Payments rails", "P2P",
                 "Wealthtech", "Regtech", "Compliance", "Fintech ops"],
     "must_haves": [], "nice_to_haves": [], "target_locations": [], "target_industries": []},
    {"profile_id": "B2B_SAAS_PM", "name": "B2B SaaS PM",
     "skills": ["Product strategy", "API/SDK", "Developer experience", "Partner enablement",
                "Market research", "Product analytics", "SQL"],
     "domains": ["B2B SaaS", "Platform", "SDK/API", "Developer tools", "Enterprise storage"],
     "must_haves": [], "nice_to_haves": [], "target_locations": [], "target_industries": []},
    {"profile_id": "GENERAL_PM", "name": "General PM",
     "skills": ["Product strategy", "User journeys", "Product analytics", "SQL", "Mixpanel"],
     "domains": ["Fintech", "Healthtech", "Community/social", "Marketplace", "Telematics"],
     "must_haves": [], "nice_to_haves": [], "target_locations": [], "target_industries": []},
]

EVIDENCE = [
    {"evidence_id": "EVID-001", "claim": "Reduced loan-workflow approval TAT ~70%",
     "strength": "Verified", "relevant_domains": ["Fintech", "Lending", "Workflow automation"],
     "allowed_claims": ["Reduced TAT", "Workflow automation", "Loan operations"]},
    {"evidence_id": "EVID-003", "claim": "Reduced portfolio NPA ~30% via repayment rails + risk escalation",
     "strength": "Verified", "relevant_domains": ["Fintech", "Lending", "Risk", "Payments rails"],
     "allowed_claims": ["Risk automation", "NPA reduction", "Payment rails design"]},
    {"evidence_id": "EVID-006", "claim": "Built partner onboarding + API docs from scratch; cut ramp ~40%",
     "strength": "Verified", "relevant_domains": ["SDK/Platform", "B2B", "API", "Partner enablement"],
     "allowed_claims": ["Partner onboarding", "API documentation", "B2B enablement"]},
]


def test_fintech_job_recommends_fintech():
    rec = recommend_profile(FIN_JOB, FIN_REQ, PROFILES, EVIDENCE)
    assert rec["recommended"]["profile_id"] == "FINTECH_PM"
    assert rec["results"][0]["score"] >= rec["results"][1]["score"]


def test_platform_job_recommends_b2b():
    rec = recommend_profile(PLATFORM_JOB, PLATFORM_REQ, PROFILES, EVIDENCE)
    assert rec["recommended"]["profile_id"] == "B2B_SAAS_PM"


def test_score_in_range_and_breakdown():
    res = score_job(FIN_JOB, FIN_REQ, PROFILES[0], EVIDENCE)
    assert 0 <= res["total"] <= 100
    assert set(res["breakdown"]) == set(res["weights"])
    assert res["explanation"]["risks"], "4+ yrs should surface as a risk"


def test_experience_risk_flag():
    res = score_job(FIN_JOB, FIN_REQ, PROFILES[0], EVIDENCE)
    assert any("4+ years" in r for r in res["explanation"]["risks"])


def test_classify_direct():
    cls, ev = classify_requirement("Risk analytics for lending", PROFILES[0], EVIDENCE)
    assert cls in ("DIRECT", "TRANSFERABLE")
