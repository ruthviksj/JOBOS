"""Tracker API (spec 37, 47)."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.services import tracker as tracker_service

router = APIRouter(prefix="/applications", tags=["applications"])


class TransitionBody(BaseModel):
    to: str


@router.post("/create")
def create(opp_id: int, db: Session = Depends(get_db)):
    """Create an application from an approved opportunity's package."""
    try:
        app = tracker_service.create_application(db, opp_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {"application_id": app.application_id, "status": app.status,
            "resume_version": app.resume_version}


@router.post("/{app_id}/transition")
def transition(app_id: int, body: TransitionBody, db: Session = Depends(get_db)):
    app = db.get(models.Application, app_id)
    if app is None:
        raise HTTPException(404, "application not found")
    try:
        return tracker_service.transition(db, app, body.to)
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.get("/{app_id}/followup")
def followup(app_id: int, db: Session = Depends(get_db)):
    """Spec 39: follow-up checkpoints for an application."""
    from app.services import email_monitor as email_svc

    app = db.get(models.Application, app_id)
    if app is None:
        raise HTTPException(404, "application not found")
    return email_svc.follow_up_due(app)


@router.get("/{app_id}")
def get(app_id: int, db: Session = Depends(get_db)):
    app = db.get(models.Application, app_id)
    if app is None:
        raise HTTPException(404, "application not found")
    return {
        "application_id": app.application_id,
        "status": app.status,
        "submitted_at": app.submitted_at.isoformat() if app.submitted_at else None,
        "ats": app.ats,
        "resume_version": app.resume_version,
        "activity": tracker_service.activity_log(db, app),
    }
