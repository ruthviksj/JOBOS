"""Browser agent API (spec 28-35). Receives detected form fields from the Chrome
extension and returns the autofill/action plan. No submission is ever performed
here - the extension only fills after human review (spec 35)."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import browser as browser_svc

router = APIRouter(prefix="/browser", tags=["browser"])


class FieldsIn(BaseModel):
    opportunity_id: str | None = None
    fields: list[str]


@router.post("/map-fields")
def map_fields(body: FieldsIn, db: Session = Depends(get_db)):
    plan = browser_svc.map_fields(body.fields)
    return {
        "opportunity_id": body.opportunity_id,
        "actions": plan,
        "review_required": browser_svc.review_required(body.fields),
    }
