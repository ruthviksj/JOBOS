"""Email monitor API (spec 38)."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import email_monitor as email_svc

router = APIRouter(prefix="/email", tags=["email"])


class EmailIn(BaseModel):
    message_id: str
    subject: str
    body: str
    application_id: int | None = None


@router.post("/process")
def process(body: EmailIn, db: Session = Depends(get_db)):
    return email_svc.process_email(
        db, message_id=body.message_id, subject=body.subject,
        body=body.body, application_id=body.application_id,
    )


@router.get("/classify")
def classify(subject: str = "", body: str = ""):
    return {"classification": email_svc.classify_email(subject, body)}
