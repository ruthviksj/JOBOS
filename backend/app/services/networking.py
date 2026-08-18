"""Networking Agent (spec 40-45, 55).

Researches potential contacts for a company/opportunity and ranks referral
relevance. Deterministic: relevance scoring uses the spec 42 weighting; contact
discovery is a lookup from an in-DB contact pool (external LinkedIn/email
enrichment is out of scope for this slice). The agent never sends outreach
without authorization (spec 55).

Spec 42 contact relevance weights:
Same role/function 25% | Same team/domain 25% | Seniority/influence 15% |
Referral capability 15% | Shared background 10% | Relationship proximity 10%.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app import models

RELEVANCE_WEIGHTS = {
    "role": 0.25,
    "domain": 0.25,
    "seniority": 0.15,
    "referral_capability": 0.15,
    "shared_background": 0.10,
    "relationship_proximity": 0.10,
}

ROLE_SCORE = {"pm": 1.0, "recruiter": 0.8, "director": 0.75, "head": 0.7,
              "engineer": 0.5, "other": 0.3}
SENIORITY_SCORE = {"director": 1.0, "head": 0.9, "senior": 0.8, "manager": 0.7,
                   "pm": 0.6, "recruiter": 0.5, "other": 0.3}


def _score_role(title: str | None) -> float:
    t = (title or "").lower()
    if "product manager" in t or "pm" in t:
        return ROLE_SCORE["pm"]
    if "recruit" in t:
        return ROLE_SCORE["recruiter"]
    if "director" in t:
        return ROLE_SCORE["director"]
    if "head of" in t:
        return ROLE_SCORE["head"]
    if "engineer" in t:
        return ROLE_SCORE["engineer"]
    return ROLE_SCORE["other"]


def _score_seniority(title: str | None) -> float:
    t = (title or "").lower()
    if "director" in t:
        return SENIORITY_SCORE["director"]
    if "head of" in t:
        return SENIORITY_SCORE["head"]
    if "senior" in t:
        return SENIORITY_SCORE["senior"]
    if "manager" in t or "lead" in t:
        return SENIORITY_SCORE["manager"]
    if "product manager" in t or "pm" in t:
        return SENIORITY_SCORE["pm"]
    if "recruit" in t:
        return SENIORITY_SCORE["recruiter"]
    return SENIORITY_SCORE["other"]


def relevance_score(contact: dict) -> float:
    """Compute spec 42 relevance for a contact dict."""
    role = _score_role(contact.get("title"))
    domain = 1.0 if contact.get("domain_match") else 0.4
    seniority = _score_seniority(contact.get("title"))
    referral = 0.8 if role >= 0.8 else 0.5  # PMs/directors can refer
    shared = 1.0 if contact.get("shared_background") else 0.3
    proximity = 1.0 if contact.get("connected") else 0.4  # 1st connection proxies proximity
    raw = (
        role * RELEVANCE_WEIGHTS["role"]
        + domain * RELEVANCE_WEIGHTS["domain"]
        + seniority * RELEVANCE_WEIGHTS["seniority"]
        + referral * RELEVANCE_WEIGHTS["referral_capability"]
        + shared * RELEVANCE_WEIGHTS["shared_background"]
        + proximity * RELEVANCE_WEIGHTS["relationship_proximity"]
    )
    return round(raw * 100, 1)


def contact_id(db: Session) -> str:
    n = db.query(models.Contact).count() + 1
    return f"CONT-{n:04d}"


def discover_contacts(db: Session, company_id: int | None,
                      domain: str | None) -> list[dict]:
    """Return candidate contacts for a company, ranked by relevance (spec 43)."""
    q = db.query(models.Contact)
    if company_id is not None:
        q = q.filter(models.Contact.company_id == company_id)
    contacts = q.all()

    results = []
    for c in contacts:
        cdict = {
            "title": c.title,
            "domain_match": (domain or "").lower() in (c.department or "").lower()
            if c.department else False,
            "shared_background": bool(c.shared_background),
            "connected": c.shared_connections and c.shared_connections > 0,
        }
        results.append({
            "contact_id": c.contact_id,
            "name": c.name,
            "title": c.title,
            "department": c.department,
            "linkedin": c.linkedin,
            "email": c.email,
            "relevance_score": relevance_score(cdict),
            "referral_probability": c.referral_probability,
            "status": c.contact_status,
        })
    results.sort(key=lambda r: r["relevance_score"], reverse=True)
    return results


def add_contact(db: Session, *, name: str, company_id: int | None = None,
                title: str | None = None, department: str | None = None,
                team: str | None = None, email: str | None = None,
                linkedin: str | None = None, shared_background: str | None = None,
                shared_connections: int | None = None,
                referral_probability: float | None = None) -> models.Contact:
    c = models.Contact(
        contact_id=contact_id(db), company_id=company_id, name=name, title=title,
        department=department, team=team, email=email, linkedin=linkedin,
        shared_background=shared_background, shared_connections=shared_connections,
        referral_probability=referral_probability, contact_status="DISCOVERED",
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def referral_strategy(contact: dict) -> str:
    """Spec 44: recommend whether to ask for a referral or talk first."""
    if contact["relevance_score"] >= 70 and contact["referral_probability"]:
        return "Consider a referral request after a brief conversation."
    if contact["relevance_score"] >= 50:
        return "Talk first; don't ask for referral yet."
    return "Low relevance; contact only if there is a specific reason."
