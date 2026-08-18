"""Tests for the tracker agent (spec 37, 47)."""

import uuid

import pytest

from app import models
from app.db import SessionLocal
from app.services import tracker as tracker_service
from app.services.package import generate_package


def _approved_opportunity(db):
    from app.services.ingest import create_opportunity_from_source
    opp = create_opportunity_from_source(
        db, source_type="telegram",
        raw_text="Hiring PM at XYZ https://greenhouse.io/xyz",
    )
    job = models.Job(job_id=f"JOB-TR-{uuid.uuid4().hex[:8]}",
                     title="Senior Product Manager",
                     industry="Fintech", ats="greenhouse",
                     application_url="https://greenhouse.io/xyz")
    db.add(job)
    db.flush()
    opp.canonical_job_id = job.id
    db.add(models.JobRequirement(job_id=job.id, kind="requirement", text="Fintech lending"))
    db.commit()
    generate_package(db, opp, "FINTECH_PM")
    db.refresh(opp)
    return opp


def test_create_and_transition():
    db = SessionLocal()
    opp = _approved_opportunity(db)
    app = tracker_service.create_application(db, opp.id)
    assert app.status == "APPLICATION_READY"
    assert app.resume_version.startswith("RUTHVIK-FINTECH")

    r = tracker_service.transition(db, app, "APPLICATION_STARTED")
    assert r["status"] == "APPLICATION_STARTED"
    r = tracker_service.transition(db, app, "APPLIED")
    assert r["status"] == "APPLIED"
    assert app.submitted_at is not None

    log = tracker_service.activity_log(db, app)
    assert any(e["event_type"] == "STATUS_CHANGED" for e in log)
    assert any(e["event_type"] == "APPLICATION_CREATED" for e in log)
    db.close()


def test_regression_blocked():
    db = SessionLocal()
    opp = _approved_opportunity(db)
    app = tracker_service.create_application(db, opp.id)
    tracker_service.transition(db, app, "APPLIED")
    with pytest.raises(ValueError):
        tracker_service.transition(db, app, "SHORTLISTED")
    db.close()


def test_terminal_locks():
    db = SessionLocal()
    opp = _approved_opportunity(db)
    app = tracker_service.create_application(db, opp.id)
    tracker_service.transition(db, app, "REJECTED")
    with pytest.raises(ValueError):
        tracker_service.transition(db, app, "INTERVIEW")
    db.close()
