"""Compatibility + job endpoints (spec 16-17, 23)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.compatibility import priority_score, recommend_profile
from app.db import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _profile_rows(db: Session) -> list[dict]:
    return [
        {
            "profile_id": p.profile_id,
            "name": p.name,
            "skills": p.skills or [],
            "domains": p.domains or [],
            "must_haves": p.must_haves or [],
            "nice_to_haves": p.nice_to_haves or [],
            "target_locations": p.target_locations or [],
            "target_industries": p.target_industries or [],
        }
        for p in db.query(models.Profile).all()
    ]


def _evidence_rows(db: Session) -> list[dict]:
    return [
        {
            "evidence_id": e.evidence_id,
            "claim": e.claim,
            "strength": e.strength,
            "relevant_domains": e.relevant_domains or [],
            "allowed_claims": e.allowed_claims or [],
        }
        for e in db.query(models.Evidence).all()
    ]


@router.get("/{opp_id}")
def get_job(opp_id: int, db: Session = Depends(get_db)):
    """Spec 21: job detail — overview, fit, recommendation, application."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise HTTPException(404, "opportunity not found")
    job = db.get(models.Job, opp.canonical_job_id) if opp.canonical_job_id else None
    if job is None:
        return {"opportunity_id": opp.opportunity_id, "job": None,
                "message": "not researched yet"}
    requirements = [
        {"text": r.text, "kind": r.kind}
        for r in db.query(models.JobRequirement).filter_by(job_id=job.id).all()
    ]
    scores = [
        {"profile_id": s.profile_id, "score": s.total}
        for s in db.query(models.CompatibilityScore).filter_by(job_id=job.id).all()
    ]
    pkg = (
        db.query(models.ApplicationPackage)
        .filter_by(opportunity_id=opp.id).first()
    )
    return {
        "opportunity_id": opp.opportunity_id,
        "application_status": opp.application_status,
        "selected_profile_id": opp.selected_profile_id,
        "recommended_profile_id": opp.recommended_profile_id,
        "compatibility_score": opp.compatibility_score,
        "priority_score": opp.priority_score,
        "job": {
            "job_id": job.job_id, "title": job.title, "company_tldr": job.company_tldr,
            "jd_tldr": job.jd_tldr, "location": job.location,
            "remote_policy": job.remote_policy, "seniority": job.seniority,
            "minimum_experience": job.minimum_experience, "ats": job.ats,
            "application_url": job.application_url, "jd_url": job.jd_url,
        },
        "requirements": requirements,
        "profile_scores": sorted(scores, key=lambda s: s["score"], reverse=True),
        "application_package": (
            {"resume_version": pkg.resume_version, "status": pkg.status} if pkg else None
        ),
    }


@router.post("/{opp_id}/package")
def generate_package(opp_id: int, profile_id: str, db: Session = Depends(get_db)):
    """Spec 24: create the application package for an approved opportunity."""
    from app.services.package import generate_package as _gen

    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise HTTPException(404, "opportunity not found")
    try:
        result = _gen(db, opp, profile_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return result


@router.post("/{opp_id}/resume")
def generate_resume(opp_id: int, profile_id: str, db: Session = Depends(get_db)):
    """Spec 25-26: generate a tailored resume (MD + DOCX) for a profile."""
    from app.services.resume import generate_resume as _gen

    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise HTTPException(404, "opportunity not found")
    try:
        result = _gen(db, profile_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    # Version the resume against this opportunity (spec 26).
    from app.services.package import resume_version_id
    version = resume_version_id(profile_id, db)
    if opp.canonical_job_id:
        db.add(models.Document(
            doc_type="resume", version=version, profile_id=profile_id,
            job_id=opp.canonical_job_id, path=result["markdown"],
            content=result["markdown"],
        ))
        db.commit()
        result["resume_version"] = version
    return result


@router.post("/{opp_id}/compatibility")
def compute_compatibility(opp_id: int, db: Session = Depends(get_db)):
    """Score an opportunity against all profiles; store result + recommendation."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None or opp.canonical_job_id is None:
        raise HTTPException(404, "opportunity has no canonical job yet")
    job = db.get(models.Job, opp.canonical_job_id)

    requirements = [
        {"text": r.text, "kind": r.kind}
        for r in db.query(models.JobRequirement).filter_by(job_id=job.id).all()
    ]
    job_dict = {
        "title": job.title,
        "industry": job.industry,
        "location": job.location,
        "remote_policy": job.remote_policy,
        "minimum_experience": job.minimum_experience,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
    }
    profiles = _profile_rows(db)
    evidence = _evidence_rows(db)

    rec = recommend_profile(job_dict, requirements, profiles, evidence)
    top = rec["recommended"]

    # Persist per-profile scores
    for r in rec["results"]:
        existing = (
            db.query(models.CompatibilityScore)
            .filter_by(job_id=job.id, profile_id=r["profile_id"])
            .first()
        )
        if existing:
            existing.total = r["score"]
        else:
            db.add(models.CompatibilityScore(
                job_id=job.id, profile_id=r["profile_id"], total=r["score"],
            ))

    opp.compatibility_score = top["score"]
    opp.recommended_profile_id = top["profile_id"]
    db.commit()

    return {"opportunity_id": opp.opportunity_id, **rec}


@router.post("/{opp_id}/priority")
def compute_priority(opp_id: int, db: Session = Depends(get_db)):
    """Spec 18: Priority = Fit + Referral + Preference - Effort."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise HTTPException(404, "opportunity not found")
    fit = opp.compatibility_score or 0.0
    referral = 0.0  # populated by Networking agent (later phase)
    preference = 0.0
    effort = 0.0
    opp.priority_score = priority_score(fit, referral, preference, effort)
    db.commit()
    return {"opportunity_id": opp.opportunity_id, "priority_score": opp.priority_score}
