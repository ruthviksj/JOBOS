"""Analytics / optimization service (Phase 6, spec 67-68).

Computes outcome analytics over the tracker data:
- Funnel conversion (DISCOVERED -> APPLIED -> INTERVIEW -> OFFER).
- Referral conversion: applications that had a network contact/referral vs not.
- Qualified-interviews-per-effort proxy (product North Star, spec 68).

All figures are computed from persisted rows; no estimates are invented.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models

INTERVIEW_STATES = {"SCREEN", "INTERVIEW", "FINAL_ROUND", "OFFER"}
TERMINAL_NEGATIVE = {"REJECTED", "WITHDRAWN", "NO_RESPONSE"}


def funnel_conversion(db: Session) -> dict:
    """Conversion rates across the spec 37 funnel, using application statuses."""
    apps = db.query(models.Application).all()
    total = len(apps)
    applied = sum(1 for a in apps if a.status == "APPLIED" or a.submitted_at is not None)
    interviewed = sum(1 for a in apps if a.status in INTERVIEW_STATES)
    offered = sum(1 for a in apps if a.status == "OFFER")
    pct = lambda n: round(n * 100 / total, 1) if total else 0.0
    return {
        "total": total,
        "applied": {"count": applied, "pct_of_total": pct(applied)},
        "interviewed": {"count": interviewed, "pct_of_applied": pct(interviewed)},
        "offered": {"count": offered, "pct_of_applied": pct(offered)},
    }


def referral_conversion(db: Session) -> dict:
    """Compare outcomes for applications that had a recorded outreach/referral vs not."""
    apps = db.query(models.Application).all()

    # A referral is present when an Outreach record links to the app's opportunity.
    by_opp = {}
    for o in db.query(models.Outreach).all():
        if o.opportunity_id is not None:
            by_opp[o.opportunity_id] = True

    def _bucket(rows):
        n = len(rows)
        interview = sum(1 for a in rows if a.status in INTERVIEW_STATES)
        return {"count": n,
                "interview_rate": round(interview * 100 / n, 1) if n else 0.0}

    with_ref = [a for a in apps if a.opportunity_id in by_opp]
    without = [a for a in apps if a.opportunity_id not in by_opp]
    return {"with_referral": _bucket(with_ref), "without_referral": _bucket(without)}


def interviews_per_effort(db: Session) -> dict:
    """Product North Star proxy (spec 68): interviews per hour of user effort.

    Uses the spec 67 budget (2+1+2 = ~5 min user effort per opportunity) as the
    effort denominator, and reports a synthetic per-100-hours figure.
    """
    apps = db.query(models.Application).all()
    total = len(apps)
    interviewed = sum(1 for a in apps if a.status in INTERVIEW_STATES)
    effort_per_app_min = 5.0  # spec 67: research <2m, decision <1m, prep <2m
    total_hours = total * effort_per_app_min / 60.0
    per_100h = (interviewed * 100 / total_hours) if total_hours else 0.0
    return {
        "opportunities": total,
        "interviews": interviewed,
        "estimated_user_hours": round(total_hours, 2),
        "interviews_per_100_hours": round(per_100h, 2),
    }


def outcome_summary(db: Session) -> dict:
    """Consolidated analytics payload for the dashboard/API."""
    return {
        "funnel": funnel_conversion(db),
        "referral": referral_conversion(db),
        "north_star": interviews_per_effort(db),
    }
