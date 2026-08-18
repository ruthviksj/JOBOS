"""Tracker Agent (spec 37, 47, 56).

Creates application records from approved packages, drives state transitions
along the spec 37 tracker, and logs an activity timeline (spec 47).

State machine (forward states):
DISCOVERED -> RESEARCHED -> SHORTLISTED -> APPROVED -> APPLICATION_READY ->
APPLICATION_STARTED -> APPLIED -> RECRUITER_RESPONSE -> SCREEN -> INTERVIEW ->
FINAL_ROUND -> OFFER

Terminal / side states: REJECTED, WITHDRAWN, NO_RESPONSE, CLOSED.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app import models

FORWARD_STATES = [
    "DISCOVERED", "RESEARCHED", "SHORTLISTED", "APPROVED", "APPLICATION_READY",
    "APPLICATION_STARTED", "APPLIED", "RECRUITER_RESPONSE", "SCREEN",
    "INTERVIEW", "FINAL_ROUND", "OFFER",
]
TERMINAL_STATES = ["REJECTED", "WITHDRAWN", "NO_RESPONSE", "CLOSED"]
ALL_STATES = FORWARD_STATES + TERMINAL_STATES

_IDX = {s: i for i, s in enumerate(FORWARD_STATES)}


def application_id(db: Session) -> str:
    n = db.query(models.Application).count() + 1
    return f"APP-2026-{n:04d}"


def log_event(db: Session, application_id: int, event_type: str, detail: str | None = None) -> None:
    db.add(models.ApplicationEvent(
        application_id=application_id, event_type=event_type, detail=detail,
    ))
    db.commit()


def create_application(db: Session, opp_id: int) -> models.Application:
    """Create an Application for an approved opportunity with a package."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise ValueError("opportunity not found")
    pkg = db.query(models.ApplicationPackage).filter_by(opportunity_id=opp.id).first()
    if pkg is None:
        raise ValueError("no application package; generate one first")

    job = db.get(models.Job, opp.canonical_job_id) if opp.canonical_job_id else None
    app = models.Application(
        application_id=application_id(db),
        opportunity_id=opp.id,
        status="APPLICATION_READY",
        ats=job.ats if job else None,
        source=pkg.profile_id,
        resume_version=pkg.resume_version,
    )
    db.add(app)
    db.flush()
    log_event(db, app.id, "APPLICATION_CREATED", f"Package {pkg.resume_version}")
    db.refresh(app)
    return app


def transition(db: Session, app: models.Application, new_state: str) -> dict:
    """Transition an application to new_state, enforcing the spec 37 machine."""
    if new_state not in ALL_STATES:
        raise ValueError(f"unknown state {new_state}")
    if app.status in TERMINAL_STATES and new_state != app.status:
        raise ValueError(f"terminal state {app.status} cannot change")

    old = app.status
    if old in FORWARD_STATES and new_state in FORWARD_STATES:
        if _IDX[new_state] < _IDX[old]:
            raise ValueError(f"cannot regress {old} -> {new_state}")

    if new_state == "APPLIED" and app.submitted_at is None:
        app.submitted_at = datetime.now()
    app.status = new_state
    db.commit()
    log_event(db, app.id, "STATUS_CHANGED", f"{old} -> {new_state}")
    db.refresh(app)
    return {"application_id": app.application_id, "status": app.status}


def activity_log(db: Session, app: models.Application) -> list[dict]:
    """Spec 47: the application's activity timeline."""
    events = (
        db.query(models.ApplicationEvent)
        .filter_by(application_id=app.id)
        .order_by(models.ApplicationEvent.occurred_at)
        .all()
    )
    return [
        {"event_type": e.event_type, "occurred_at": e.occurred_at.isoformat(), "detail": e.detail}
        for e in events
    ]
