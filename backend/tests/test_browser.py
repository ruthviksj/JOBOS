"""Tests for the browser application agent (spec 32-35)."""

from app.services import browser as browser_svc


def test_autofill_factual_fields():
    plan = browser_svc.map_fields(["First name", "Email", "Phone"])
    actions = {a["action"] for a in plan}
    assert actions == {"AUTOFILL"}
    first = next(a for a in plan if a["field"] == "First name")
    assert first["value"] == "Ruthvik"
    assert first["confidence"] > 0.9


def test_high_risk_blocked():
    plan = browser_svc.map_fields(["Do you require visa sponsorship?"])
    a = plan[0]
    assert a["action"] == "BLOCK"
    assert "high-risk" in a["reason"]


def test_unknown_asks():
    plan = browser_svc.map_fields(["weird custom field"])
    assert plan[0]["action"] == "ASK"


def test_review_required():
    assert browser_svc.review_required(["First name", "Do you currently require sponsorship?"]) is True
    assert browser_svc.review_required(["First name", "Email"]) is False
