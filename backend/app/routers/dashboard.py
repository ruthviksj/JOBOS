"""Dashboard API (spec 19-20): header counts + priority-sorted job feed."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Opportunity
from app.services.ingest import opportunity_to_dict

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Spec 37 tracker states.
STATUS_GROUPS = [
    ("New", "NEW", "DISCOVERED"),
    ("Shortlisted", None, "SHORTLISTED"),
    ("Approved", None, "APPROVED"),
    ("Applied", None, "APPLIED"),
    ("Interviews", None, "INTERVIEW"),
    ("Offers", None, "OFFER"),
]


@router.get("")
def dashboard(
    status: str | None = Query(None, description="Filter feed by application_status"),
    min_compatibility: float | None = Query(None, ge=0, le=100),
    min_priority: float | None = Query(None, ge=0, le=100),
    sort: str = Query("priority", pattern="^(priority|compatibility|newest)$"),
    db: Session = Depends(get_db),
):
    # Header counts
    counts: dict[str, int] = {}
    total = db.query(func.count(Opportunity.id)).scalar() or 0
    for label, disp, app_status in STATUS_GROUPS:
        if disp is None:
            counts[label] = (
                db.query(func.count(Opportunity.id))
                .filter(Opportunity.application_status == app_status)
                .scalar()
                or 0
            )
        else:
            counts[label] = (
                db.query(func.count(Opportunity.id))
                .filter(Opportunity.discovery_status == disp)
                .scalar()
                or 0
            )
    counts["Total"] = total

    # Feed
    q = db.query(Opportunity)
    if status:
        q = q.filter(Opportunity.application_status == status)
    if min_compatibility is not None:
        q = q.filter(Opportunity.compatibility_score >= min_compatibility)
    if min_priority is not None:
        q = q.filter(Opportunity.priority_score >= min_priority)

    order = {
        "priority": Opportunity.priority_score.desc(),
        "compatibility": Opportunity.compatibility_score.desc(),
        "newest": Opportunity.created_at.desc(),
    }[sort]
    feed = [opportunity_to_dict(o, db) for o in q.order_by(order).all()]

    return {"counts": counts, "feed": feed}
