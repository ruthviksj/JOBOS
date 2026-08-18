"""Analytics API (Phase 6, spec 67-68)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import analytics as analytics_svc

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
def summary(db: Session = Depends(get_db)):
    return analytics_svc.outcome_summary(db)


@router.get("/funnel")
def funnel(db: Session = Depends(get_db)):
    return analytics_svc.funnel_conversion(db)


@router.get("/north-star")
def north_star(db: Session = Depends(get_db)):
    return analytics_svc.interviews_per_effort(db)
