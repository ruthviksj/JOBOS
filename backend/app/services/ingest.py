"""Job ingestion service (spec 13, 6-7).

Forward -> Done. Preserves the raw source forever (never discard), extracts URLs,
and creates an Opportunity + JobSource. Research (URL -> canonical Job) is a
separate agent step, stubbed here as `research_opportunity`.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app import models

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)

URL_CLASSIFIERS = [
    (r"linkedin\.com/jobs", "linkedin"),
    (r"greenhouse\.io", "greenhouse"),
    (r"lever\.co", "lever"),
    (r"jobs\.ashbyhq\.com", "ashby"),
    (r"workday\.com", "workday"),
    (r"jobs\.", "ats"),
]


def extract_urls(text: str) -> list[str]:
    return [u.rstrip(".,);]") for u in URL_RE.findall(text or "")]


def classify_url(url: str) -> str:
    low = url.lower()
    for pattern, kind in URL_CLASSIFIERS:
        if re.search(pattern, low):
            return kind
    return "job_or_other"


def opportunity_id(db: Session) -> str:
    n = db.query(models.Opportunity).count() + 1
    return f"OPP-{n:05d}"


def create_opportunity_from_source(db: Session, *, source_type: str,
                                   raw_text: str, sender: str | None = None,
                                   source_name: str | None = None,
                                   source_channel: str | None = None,
                                   message_id: str | None = None,
                                   message_timestamp: datetime | None = None,
                                   attachments: list | None = None,
                                   original_message: str | None = None) -> models.Opportunity:
    """Persist a raw job source and its opportunity. Returns the opportunity."""
    urls = extract_urls(raw_text)
    opp = models.Opportunity(
        opportunity_id=opportunity_id(db),
        discovery_status="NEW",
        research_status="PENDING",
        application_status="DISCOVERED",
    )
    db.add(opp)
    db.flush()

    src = models.JobSource(
        opportunity_id=opp.id,
        source_type=source_type,
        source_name=source_name,
        source_channel=source_channel,
        sender=sender,
        message_id=message_id,
        message_timestamp=message_timestamp,
        raw_text=raw_text,
        urls=urls,
        attachments=attachments or [],
        original_message=original_message or raw_text,
    )
    db.add(src)
    db.commit()
    db.refresh(opp)
    return opp


def research_opportunity(db: Session, opp_id: int) -> dict:
    """Run the Research Agent (spec 14/51): fetch URL -> canonical Job."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        return {"ok": False, "error": "opportunity not found"}
    sources = db.query(models.JobSource).filter_by(opportunity_id=opp.id).all()
    urls = [u for s in sources for u in (s.urls or [])]
    if not urls:
        return {"ok": False, "error": "no URL in source", "opportunity_id": opp.opportunity_id}

    url = urls[0]
    try:
        from app.services.research import research

        data = research(url)
    except Exception as exc:  # surface failure per spec 60, never silently fail
        opp.research_status = "FAILED"
        db.commit()
        return {"ok": False, "error": str(exc), "opportunity_id": opp.opportunity_id}

    job = models.Job(
        job_id=f"JOB-{db.query(models.Job).count() + 1:05d}",
        title=data.get("title") or "Untitled role",
        location=data.get("location"),
        remote_policy=data.get("remote_policy"),
        minimum_experience=data.get("minimum_experience"),
        preferred_experience=data.get("preferred_experience"),
        seniority=data.get("seniority"),
        jd_url=data.get("jd_url"),
        application_url=data.get("application_url"),
        ats=data.get("ats"),
        full_jd=data.get("full_jd"),
        jd_tldr=data.get("jd_tldr"),
        posting_date=None,
    )
    db.add(job)
    db.flush()
    for req in (data.get("requirements") or []):
        db.add(models.JobRequirement(job_id=job.id, kind="requirement", text=req))

    opp.canonical_job_id = job.id
    opp.research_status = "COMPLETE"
    db.commit()

    return {
        "ok": True,
        "opportunity_id": opp.opportunity_id,
        "job_id": job.job_id,
        "title": job.title,
        "ats": job.ats,
        "requirements": len(data.get("requirements") or []),
    }


def opportunity_to_dict(opp: models.Opportunity, db: Session) -> dict[str, Any]:
    sources = db.query(models.JobSource).filter_by(opportunity_id=opp.id).all()
    return {
        "opportunity_id": opp.opportunity_id,
        "discovery_status": opp.discovery_status,
        "research_status": opp.research_status,
        "application_status": opp.application_status,
        "compatibility_score": opp.compatibility_score,
        "priority_score": opp.priority_score,
        "recommended_profile_id": opp.recommended_profile_id,
        "sources": [
            {
                "source_type": s.source_type,
                "sender": s.sender,
                "urls": s.urls,
                "raw_text": s.raw_text,
            }
            for s in sources
        ],
    }
