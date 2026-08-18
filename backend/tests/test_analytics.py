"""Tests for the analytics service (Phase 6, spec 67-68)."""

from app.db import SessionLocal
from app.services import analytics as analytics_svc


def test_funnel_conversion_empty():
    db = SessionLocal()
    res = analytics_svc.funnel_conversion(db)
    assert res["total"] == 0
    assert res["applied"]["pct_of_total"] == 0.0
    db.close()


def test_north_star_zero_safe():
    db = SessionLocal()
    res = analytics_svc.interviews_per_effort(db)
    assert res["opportunities"] == 0
    assert res["interviews_per_100_hours"] == 0.0
    db.close()


def test_referral_conversion_buckets():
    db = SessionLocal()
    res = analytics_svc.referral_conversion(db)
    assert set(res) == {"with_referral", "without_referral"}
    db.close()
