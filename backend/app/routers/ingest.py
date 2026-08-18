"""Ingest API (spec 13): Forward -> Done."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import ingest as ingest_service

router = APIRouter(prefix="/ingest", tags=["ingest"])


class RawSource(BaseModel):
    source_type: str = Field(..., description="linkedin/whatsapp/telegram/slack/email/...")
    raw_text: str
    sender: Optional[str] = None
    source_name: Optional[str] = None
    source_channel: Optional[str] = None
    message_id: Optional[str] = None
    message_timestamp: Optional[datetime] = None
    attachments: list[str] = Field(default_factory=list)


@router.post("/raw")
def ingest_raw(body: RawSource, db: Session = Depends(get_db)):
    opp = ingest_service.create_opportunity_from_source(
        db,
        source_type=body.source_type,
        raw_text=body.raw_text,
        sender=body.sender,
        source_name=body.source_name,
        source_channel=body.source_channel,
        message_id=body.message_id,
        message_timestamp=body.message_timestamp,
        attachments=body.attachments,
    )
    return {"received": True, "opportunity_id": opp.opportunity_id}


@router.post("/{opp_id}/research")
def run_research(opp_id: int, db: Session = Depends(get_db)):
    return ingest_service.research_opportunity(db, opp_id)
