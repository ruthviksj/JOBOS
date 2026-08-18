"""Compatibility + priority scoring engine (spec 16-18, 52).

Heuristic, deterministic, evidence-based. Produces a 0-100 compatibility score
with a per-dimension breakdown and a narrative (strong/partial/gaps/risk), plus a
priority score (spec 18). Weights are configurable via DEFAULT_WEIGHTS (spec 16).

The engine operates on plain dicts so it is DB-agnostic and unit-testable; routers
convert ORM rows into these shapes.
"""

from __future__ import annotations

import re

# Candidate facts (from MASTER_PROFILE). PM-focused experience.
CANDIDATE = {
    "pm_years": 3.0,
    "locations": ["Bengaluru", "Remote"],
    "remote_ok": True,
}

# Evidence strength weights (spec 11/52).
EVIDENCE_STRENGTH = {
    "Verified": 1.0,
    "Estimated": 0.85,
    "Directional": 0.7,
    "Case-study": 0.55,
    "Projected": 0.4,
}

# Spec 16 weighting table.
DEFAULT_WEIGHTS = {
    "pm_competency": 20,
    "domain_relevance": 20,
    "functional_skill": 15,
    "experience_seniority": 15,
    "technical_complexity": 10,
    "evidence_strength": 10,
    "location": 5,
    "compensation": 5,
}

PM_KEYWORDS = [
    "product manager", "product", "strategy", "roadmap", "roadmapping",
    "lifecycle", "prd", "user story", "user journey", "prioritization",
    "go-to-market", "gtm", "stakeholder", "cross-functional", "analytics",
    "requirements", "backlog", "release", "launch", "product owner",
]

TECHNICAL_KEYWORDS = [
    "api", "sdk", "platform", "sql", "python", "integration", "developer",
    "cloud", "saas", "b2b", "multi-tenant", "multitenant", "iot", "embedded",
    "dashcam", "telematics", "adas", "dms", "algorithm", "data",
]


def _tokens(text: str) -> set[str]:
    if not text:
        return set()
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _overlap(a: set, b: set) -> float:
    """Fraction of `a` covered by `b` (directional coverage)."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a)


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def classify_requirement(req_text: str, profile: dict, evidence_list: list[dict]) -> tuple[str, dict | None]:
    """Classify a JD requirement against profile + evidence library.

    Returns (classification, best_evidence) where classification is one of
    DIRECT / TRANSFERABLE / WEAKLY RELATED / NO EVIDENCE.
    """
    rt = _tokens(req_text)
    if not rt:
        return "NO EVIDENCE", None

    best = None
    best_rank = 0
    for ev in evidence_list:
        allowed = _tokens(" ".join(ev.get("allowed_claims", [])))
        domains = _tokens(" ".join(ev.get("relevant_domains", [])))
        claim = _tokens(ev.get("claim", ""))
        if allowed:
            ratio = _overlap(rt, allowed)
            if ratio >= 0.4:
                return "DIRECT", ev
            if ratio > best_rank:
                best_rank, best = ratio, ev
        if domains and _overlap(rt, domains) >= 0.3:
            return "TRANSFERABLE", ev
        if claim and _overlap(rt, claim) >= 0.3:
            return "TRANSFERABLE", ev

    # fall back to profile domain/skill match
    doms = _tokens(" ".join(profile.get("domains", [])))
    skills = _tokens(" ".join(profile.get("skills", [])))
    if doms and _overlap(rt, doms) >= 0.3:
        return "TRANSFERABLE", best
    if skills and _overlap(rt, skills) >= 0.3:
        return "WEAKLY RELATED", best
    if best is not None and best_rank >= 0.2:
        return "WEAKLY RELATED", best
    return "NO EVIDENCE", None


def score_job(job: dict, requirements: list[dict], profile: dict,
              evidence_list: list[dict], weights: dict | None = None) -> dict:
    """Compute a compatibility score + explanation for one (job, profile).

    job: {title, industry, location, remote_policy, minimum_experience, salary_min, salary_max}
    requirements: [{text, kind}]  kind in requirement/nice_to_have/dealbreaker
    profile: {domains, skills, must_haves, nice_to_haves, target_locations, target_industries}
    evidence_list: [{claim, strength, relevant_domains, allowed_claims}]
    """
    weights = weights or DEFAULT_WEIGHTS
    jt = _tokens(job.get("title", "")) | _tokens(job.get("industry", ""))
    pt_dom = _tokens(" ".join(profile.get("domains", [])))
    pt_skill = _tokens(" ".join(profile.get("skills", [])))

    classified = [classify_requirement(r["text"], profile, evidence_list) for r in requirements]
    direct = [c for c, _ in classified if c == "DIRECT"]
    transferable = [c for c, _ in classified if c == "TRANSFERABLE"]
    no_evidence = [c for c, _ in classified if c == "NO EVIDENCE"]

    # evidence strength
    matched_strengths = [
        EVIDENCE_STRENGTH.get(ev.get("strength", "Estimated"), 0.7)
        for c, ev in classified if c != "NO EVIDENCE" and ev
    ]
    evidence_score = (sum(matched_strengths) / len(matched_strengths)) * 100 if matched_strengths else 35.0

    # PM competency
    pm_ratio = _overlap(_tokens(" ".join(PM_KEYWORDS)), jt)
    pm_score = min(100.0, 50 + pm_ratio * 100)

    req_tokens = set()
    for r in requirements:
        req_tokens |= _tokens(r["text"])

    # Domain relevance (Jaccard vs profile domains using job + requirement tokens)
    job_tokens = jt | req_tokens
    dom_score = _jaccard(pt_dom, job_tokens) * 100 if job_tokens else 50.0

    # Functional skill match
    func_score = _overlap(pt_skill, req_tokens) * 100 if req_tokens else 50.0

    # Experience / seniority
    min_exp = job.get("minimum_experience")
    if min_exp is None:
        exp_score = 70.0
    elif min_exp <= CANDIDATE["pm_years"]:
        exp_score = 90.0
    else:
        exp_score = max(0.0, 100 - (min_exp - CANDIDATE["pm_years"]) * 20)

    # Technical / product complexity
    tech_ratio = _overlap(_tokens(" ".join(TECHNICAL_KEYWORDS)), req_tokens)
    tech_score = min(80.0, 40 + tech_ratio * 100)

    # Location / constraints
    loc = (job.get("location") or "").lower()
    if job.get("remote_policy") and job["remote_policy"].lower() in ("remote", "hybrid") and CANDIDATE["remote_ok"]:
        loc_score = 100.0
    elif any(k in loc for k in ("bengaluru", "bangalore", "remote")):
        loc_score = 90.0
    else:
        loc_score = 40.0

    # Compensation (no preference set -> neutral)
    comp_score = 50.0

    dims = {
        "pm_competency": pm_score,
        "domain_relevance": dom_score,
        "functional_skill": func_score,
        "experience_seniority": exp_score,
        "technical_complexity": tech_score,
        "evidence_strength": evidence_score,
        "location": loc_score,
        "compensation": comp_score,
    }
    total = sum(dims[d] * weights[d] for d in dims) / sum(weights.values())

    # Narrative (spec 17)
    strong, partial, gaps, risks = [], [], [], []
    if dom_score >= 60 and (job.get("industry") or ""):
        strong.append(job["industry"].capitalize())
    if direct:
        strong.append("Direct evidence match")
    if transferable:
        partial.append("Transferable evidence")
    if no_evidence:
        gaps.append(f"{len(no_evidence)} requirement(s) with no evidence")
    if min_exp is not None and min_exp > CANDIDATE["pm_years"]:
        risks.append(f"Role requests {int(min_exp)}+ years PM experience")
    if tech_score < 40:
        gaps.append("Low technical-product signal")

    return {
        "total": round(total, 1),
        "breakdown": {d: round(dims[d], 1) for d in dims},
        "weights": weights,
        "explanation": {
            "strong": strong,
            "partial": partial,
            "gaps": gaps,
            "risks": risks,
        },
        "classification": {
            "direct": len(direct),
            "transferable": len(transferable),
            "no_evidence": len(no_evidence),
            "total_requirements": len(requirements),
        },
    }


def recommend_profile(job: dict, requirements: list[dict], profiles: list[dict],
                      evidence_list: list[dict], weights: dict | None = None) -> dict:
    """Score every profile and return the best recommendation (spec 23)."""
    results = []
    for p in profiles:
        res = score_job(job, requirements, p, evidence_list, weights)
        results.append({"profile_id": p["profile_id"], "name": p["name"],
                        "score": res["total"], "explanation": res["explanation"]})
    results.sort(key=lambda r: r["score"], reverse=True)
    return {"results": results, "recommended": results[0] if results else None}


def priority_score(compatibility: float, referral_bonus: float = 0.0,
                   preference: float = 0.0, effort: float = 0.0) -> float:
    """Spec 18: Priority = Fit + Referral + Preference - Effort, normalized 0-100."""
    raw = compatibility + referral_bonus + preference - effort
    return round(max(0.0, min(100.0, raw)), 1)
