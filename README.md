# JOBOS — Personal Job Operating System (v0.2)

Convert high-signal job opportunities into prioritized, well-prepared, efficiently
submitted applications while maximizing referral/networking leverage.

## Status

Phase 0 — Candidate OS (foundation): local workspace + master profile + evidence
library + candidate profiles + database schema. Building the vertical slice next:

> Forward job -> Run agent -> Job card -> Fit score -> Choose profile -> Application package.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2.
- **Database:** SQLite by default (file-based, zero-config, cost-free). Set
  `JOBOS_DATABASE_URL` to a Postgres URL for production (spec 49).
- **Deploy:** `uvicorn app.main:app` — runs anywhere Python runs; free-tier friendly.

## Layout

```
MASTER/           MASTER_PROFILE.md, EVIDENCE_LIBRARY.md, PREFERENCES.md
PROFILES/         FINTECH_PM, B2B_SAAS_PM, GENERAL_PM
JOBS/             RAW, RESEARCHED, ARCHIVE
APPLICATIONS/     submitted application records
NETWORK/          contacts & outreach
RESUMES/          generated resume versions
ANALYTICS/        outcome analytics
LOGS/             agent run logs
backend/app/      FastAPI source (config, db, models, main)
```

## Run

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate        # Windows  (source .venv/bin/activate on Unix)
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```
