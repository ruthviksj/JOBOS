"""Application Package generator (spec 24, 26).

Creates an application package for an approved opportunity: selected profile,
resume version id, application answers, company research, role positioning,
instructions. Deterministic + evidence-driven (no LLM). Resume *content* generation
is intentionally NOT automated here — spec 25 forbids altering factual details
without approval; we create a version record and reference the base resume.
"""

from __future__ import annotations

import re
from datetime import datetime

from sqlalchemy.orm import Session

from app import models

_RESUME_NONCE_RE = re.compile(r"[^A-Z0-9\-]", re.IGNORECASE)


def resume_version_id(profile_id: str, db: Session) -> str:
    """Spec 26: RUTHVIK-FINTECH-V04 pattern. Deterministic, monotonic."""
    key = _RESUME_NONCE_RE.sub("", profile_id).upper()
    count = (
        db.query(models.Document)
        .filter(models.Document.doc_type == "resume", models.Document.profile_id == profile_id)
        .count()
    )
    return f"RUTHVIK-{key}-V{count + 1:02d}"


def _application_answers(db: Session, job: models.Job, profile_id: str) -> list[dict]:
    """Generate evidence-backed answers for common application questions (spec 27)."""
    ev = (
        db.query(models.Evidence)
        .filter(models.Evidence.evidence_id.in_(["EVID-001", "EVID-003", "EVID-006", "EVID-009"]))
        .all()
    )
    by_id = {e.evidence_id: e for e in ev}

    why_this = (
        f"Your {job.title or 'product'} role aligns with my product-management experience "
        "across fintech lending, platforms/SDKs, and risk automation, with measurable impact "
        "on turnaround time, NPA, and operations efficiency."
    )

    answers = [
        {"question": "Why are you interested in this role?", "classification": "GENERATIVE",
         "answer": why_this},
        {"question": "Tell us about your relevant experience.", "classification": "GENERATIVE",
         "answer": (
             "Associate PM at Rang De (P2P lending) where I drove a ~70% approval TAT reduction "
             "and ~30% NPA drop via repayment rails and risk automation; Associate PM at Akteena "
             "(AI dashcam SDK) owning the SDK roadmap, API docs, and AIS compliance."
         )},
        {"question": "Availability / notice period", "classification": "FACTUAL",
         "answer": "Immediately available (freelance, ready to return to full-time)."},
    ]
    return answers


def generate_package(db: Session, opp: models.Opportunity, profile_id: str) -> dict:
    """Generate an ApplicationPackage for an opportunity + profile."""
    job = db.get(models.Job, opp.canonical_job_id) if opp.canonical_job_id else None
    if job is None:
        raise ValueError("opportunity has no canonical job yet")

    profile = db.query(models.Profile).filter_by(profile_id=profile_id).first()
    if profile is None:
        raise ValueError(f"unknown profile {profile_id}")

    opp.selected_profile_id = profile_id
    opp.application_status = "APPROVED"

    version = resume_version_id(profile_id, db)

    answers = _application_answers(db, job, profile_id)

    pkg = models.ApplicationPackage(
        opportunity_id=opp.id,
        profile_id=profile_id,
        resume_version=version,
        status="GENERATED",
        company_research=f"Company: {job.title and job.industry or ''}. Research pending (Phase D stub).",
        role_positioning=profile.positioning_statement,
        instructions=(
            "Open the application URL, use the selected profile resume, fill factual fields "
            "automatically, and review high-risk answers before submission."
        ),
    )
    db.add(pkg)

    # Persist resume version record (spec 26: exact submitted version preserved).
    db.add(models.Document(
        doc_type="resume",
        version=version,
        profile_id=profile_id,
        job_id=job.id,
        path=f"RESUMES/{version}.md",
        content=f"# {version}\nProfile: {profile.name}\nJob: {job.title}\nCreated: {datetime.now().isoformat()}\n",
    ))

    db.commit()
    return {
        "application_package_id": pkg.id,
        "profile_id": profile_id,
        "resume_version": version,
        "status": pkg.status,
        "application_answers": answers,
        "application_url": job.application_url,
        "ats": job.ats,
    }
