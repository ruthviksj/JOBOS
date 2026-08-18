"""Tests for email monitor + follow-up engine (spec 38, 39)."""

from datetime import datetime, timedelta

from app import models
from app.db import SessionLocal
from app.services import email_monitor as email_svc


def _approved_app(db):
    from app.services.ingest import create_opportunity_from_source
    from app.services.package import generate_package
    from app.services.tracker import create_application

    opp = create_opportunity_from_source(
        db, source_type="telegram",
        raw_text="Hiring PM at XYZ https://greenhouse.io/xyz",
    )
    import uuid
    job = models.Job(job_id=f"JOB-EM-{uuid.uuid4().hex[:8]}",
                     title="Product Manager", ats="greenhouse")
    db.add(job)
    db.flush()
    opp.canonical_job_id = job.id
    db.commit()
    generate_package(db, opp, "FINTECH_PM")
    return create_application(db, opp.id)


def test_classify_email_categories():
    assert email_svc.classify_email("Application received", "Thank you for applying") == "APPLICATION_CONFIRMATION"
    assert email_svc.classify_email("Update", "We regret to inform you that we will not be moving forward") == "REJECTION"
    assert email_svc.classify_email("Interview", "Can we schedule a call to interview you") == "INTERVIEW_INVITATION"
    assert email_svc.classify_email("Hello", "random unrelated note") == "OTHER"


def test_process_email_advances_application():
    db = SessionLocal()
    app = _approved_app(db)
    r = email_svc.process_email(
        db, message_id="m1", subject="Interview",
        body="Can we schedule a call to interview you", application_id=app.id,
    )
    assert r["classification"] == "INTERVIEW_INVITATION"
    db.refresh(app)
    assert app.status == "INTERVIEW"
    db.close()


def test_follow_up_due():
    db = SessionLocal()
    app = _approved_app(db)
    app.submitted_at = datetime.now() - timedelta(days=6)
    db.commit()
    fu = email_svc.follow_up_due(app)
    assert fu["recommended"] is True
    assert fu["days_elapsed"] == 6
    db.close()

