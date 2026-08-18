"""Email response monitor + follow-up engine (spec 38, 39, 56).

Email ingestion here is via an explicit API call (spec 30 says only relevant
verification/application messages are surfaced; external Gmail/IMAP sync is out
of scope for this slice). `classify_email` tags an incoming message, and
`process_email` associates it with the matching application and advances its
tracker state. `follow_up_due` computes the spec 39 follow-up checkpoints.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models
from app.services import tracker as tracker_service

# Spec 38 classifications.
CATEGORIES = [
    "APPLICATION_CONFIRMATION", "REJECTION", "RECRUITER_OUTREACH",
    "INTERVIEW_INVITATION", "ASSESSMENT", "SCHEDULING",
    "REQUEST_FOR_INFORMATION", "OFFER", "OTHER",
]

_SIGNALS = {
    "APPLICATION_CONFIRMATION": ["application received", "we received your", "application submitted", "thank you for applying"],
    "REJECTION": ["not moving forward", "unfortunately", "we will not", "regret to inform", "unable to offer"],
    "RECRUITER_OUTREACH": ["recruiter", "we'd love to", "came across your profile"],
    "INTERVIEW_INVITATION": ["interview", "schedule a call", "meet with"],
    "ASSESSMENT": ["assessment", "test", "take-home", "coding challenge"],
    "SCHEDULING": ["availability", "time slot", "calendar", "book a time"],
    "REQUEST_FOR_INFORMATION": ["more information", "portfolio", "references", "resume attached"],
    "OFFER": ["offer", "we are pleased to offer", "congratulations"],
}


def classify_email(subject: str, body: str) -> str:
    text = f"{subject} {body}".lower()
    for cat, sigs in _SIGNALS.items():
        if any(s in text for s in sigs):
            return cat
    return "OTHER"


# State transitions per spec 38 category (toward spec 37 tracker).
_STATE_BY_CATEGORY = {
    "APPLICATION_CONFIRMATION": "APPLIED",
    "REJECTION": "REJECTED",
    "RECRUITER_OUTREACH": "RECRUITER_RESPONSE",
    "INTERVIEW_INVITATION": "INTERVIEW",
    "ASSESSMENT": "APPLICATION_STARTED",
    "SCHEDULING": "RECRUITER_RESPONSE",
    "OFFER": "OFFER",
}


def process_email(db: Session, *, message_id: str, subject: str, body: str,
                  application_id: int | None = None) -> dict:
    """Classify an email, record it, and (optionally) advance an application."""
    category = classify_email(subject, body)
    ev = models.EmailEvent(
        application_id=application_id, message_id=message_id,
        classification=category, snippet=body[:200],
    )
    db.add(ev)

    result = {"message_id": message_id, "classification": category}
    if application_id is not None:
        app = db.get(models.Application, application_id)
        target = _STATE_BY_CATEGORY.get(category)
        if app is not None and target:
            try:
                tracker_service.transition(db, app, target)
                result["status"] = app.status
            except ValueError:
                result["status"] = app.status
                result["note"] = "transition skipped"
    db.commit()
    return result


def follow_up_due(app: models.Application, now: datetime | None = None) -> dict:
    """Spec 39: return follow-up checkpoints relative to submission date."""
    now = now or datetime.now()
    if not app.submitted_at:
        return {"recommended": False, "reason": "not submitted"}
    elapsed = now - app.submitted_at
    first = app.submitted_at + timedelta(days=4)   # "19 Aug" from "15 Aug" (spec example)
    second = app.submitted_at + timedelta(days=11)  # "26 Aug"
    return {
        "recommended": elapsed.days >= 4,
        "first_checkpoint": first.isoformat(),
        "second_checkpoint": second.isoformat(),
        "days_elapsed": elapsed.days,
    }
