"""JOBOS API entrypoint. Phase 0 exposes health + workspace info only;
agents/dashboard land in later phases."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db, init_db
from app.routers import analytics, browser, dashboard, email, ingest, jobs, network, tracker, ui

app = FastAPI(title="JOBOS", version="0.2.0")

# Allow the Chrome extension (chrome-extension://) and any dev origin to call the
# API cross-origin. Tighten this to your production origin once public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ui.router)
app.include_router(dashboard.router)
app.include_router(jobs.router)
app.include_router(ingest.router)
app.include_router(tracker.router)
app.include_router(network.router)
app.include_router(email.router)
app.include_router(browser.router)
app.include_router(analytics.router)


@app.on_event("startup")
def _on_startup() -> None:
    init_db()


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "version": app.version}


@app.get("/workspace")
def workspace_info() -> dict:
    settings = get_settings()
    return {"root": str(settings.jobos_root), "db": settings.database_url}
