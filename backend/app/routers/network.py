"""Networking API (spec 40-45)."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.services import networking as net

router = APIRouter(prefix="/network", tags=["network"])


class ContactIn(BaseModel):
    name: str
    company_id: int | None = None
    title: str | None = None
    department: str | None = None
    team: str | None = None
    email: str | None = None
    linkedin: str | None = None
    shared_background: str | None = None
    shared_connections: int | None = None
    referral_probability: float | None = None


@router.post("/contacts")
def create_contact(body: ContactIn, db: Session = Depends(get_db)):
    c = net.add_contact(db, **body.model_dump())
    return {"contact_id": c.contact_id, "name": c.name}


@router.get("/opportunity/{opp_id}")
def opportunity_network(opp_id: int, db: Session = Depends(get_db)):
    """Spec 46: ranked contacts + referral strategy for an opportunity."""
    opp = db.get(models.Opportunity, opp_id)
    if opp is None:
        raise HTTPException(404, "opportunity not found")
    job = db.get(models.Job, opp.canonical_job_id) if opp.canonical_job_id else None
    company_id = job.company_id if job else None
    domain = (job.industry if job else None)

    contacts = net.discover_contacts(db, company_id, domain)
    ranked = []
    for c in contacts:
        ranked.append({**c, "referral_strategy": net.referral_strategy(c)})
    return {"opportunity_id": opp.opportunity_id, "contacts": ranked,
            "count": len(ranked)}


@router.get("/contacts/{contact_id}")
def contact_detail(contact_id: str, db: Session = Depends(get_db)):
    c = db.query(models.Contact).filter_by(contact_id=contact_id).first()
    if c is None:
        raise HTTPException(404, "contact not found")
    return {
        "contact_id": c.contact_id, "name": c.name, "title": c.title,
        "company_id": c.company_id, "department": c.department, "team": c.team,
        "email": c.email, "linkedin": c.linkedin,
        "relevance_score": c.relevance_score, "referral_probability": c.referral_probability,
        "status": c.contact_status,
    }
