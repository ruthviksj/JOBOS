"""Tests for the application package generator (spec 24, 26)."""

from app import models
from app.db import SessionLocal, init_db
from app.services import package as pkg_service


def _seed_one(db):
    init_db()
    opp = db.query(models.Opportunity).first()
    if opp and opp.canonical_job_id:
        return opp
    from app.services.ingest import create_opportunity_from_source
    opp = create_opportunity_from_source(
        db, source_type="telegram",
        raw_text="Hiring PM at XYZ https://greenhouse.io/xyz",
    )
    job = models.Job(job_id="JOB-T1", title="Senior Product Manager",
                     industry="Fintech", ats="greenhouse",
                     application_url="https://greenhouse.io/xyz")
    db.add(job)
    db.flush()
    opp.canonical_job_id = job.id
    db.add(models.JobRequirement(job_id=job.id, kind="requirement", text="Fintech lending"))
    db.commit()
    return opp


def test_resume_version_id_monotonic():
    db = SessionLocal()
    pid = "FINTECHPMTEST"  # unique to avoid polluting the seed DB
    v1 = pkg_service.resume_version_id(pid, db)
    # inserting a version record bumps the next id (spec 26 monotonic versions)
    db.add(models.Document(doc_type="resume", version=v1, profile_id=pid, path="x", content=""))
    db.commit()
    v2 = pkg_service.resume_version_id(pid, db)
    assert v1 == "RUTHVIK-FINTECHPMTEST-V01"
    assert v2 == "RUTHVIK-FINTECHPMTEST-V02"
    db.close()


def test_generate_package():
    db = SessionLocal()
    opp = _seed_one(db)
    # ensure a profile exists
    if not db.query(models.Profile).filter_by(profile_id="FINTECH_PM").first():
        from app.seed import seed
        seed()
        db.close()
        db = SessionLocal()
    result = pkg_service.generate_package(db, opp, "FINTECH_PM")
    assert result["profile_id"] == "FINTECH_PM"
    assert result["resume_version"].startswith("RUTHVIK-FINTECH")
    assert result["status"] == "GENERATED"
    assert result["application_answers"], "should generate answers"
    db.refresh(opp)
    assert opp.application_status == "APPROVED"
    db.close()
