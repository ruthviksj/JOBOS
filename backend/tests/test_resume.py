"""Tests for the resume agent (spec 25-26, 53)."""

from pathlib import Path

from app.db import SessionLocal
from app.services import resume as resume_service


def test_build_resume_markdown_only_allowed_claims():
    db = SessionLocal()
    profile = db.query(resume_service.models.Profile).filter_by(
        profile_id="FINTECH_PM").first()
    assert profile is not None
    md = resume_service.build_resume_markdown(db, profile, ["EVID-001", "EVID-003"])
    # Only evidence claims should appear, never forbidden inference text.
    assert "loan-workflow" in md or "approval" in md.lower() or "TAT" in md
    assert "fraud" not in md.lower()
    db.close()


def test_generate_resume_creates_files():
    db = SessionLocal()
    result = resume_service.generate_resume(db, "FINTECH_PM", ["EVID-001"])
    assert result["claims"] >= 1
    assert Path(result["markdown"]).exists()
    assert Path(result["docx"]).exists()
    assert result["docx"].endswith(".docx")
    db.close()
