"""Seed the operational DB with profiles + evidence + user.

Run:  python -m app.seed
Idempotent: skips rows whose unique key already exists.
"""

from app import models
from app.db import SessionLocal, init_db
from app.seed_data import EVIDENCE, PROFILES, USER


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if not db.query(models.User).first():
            db.add(models.User(**USER))
            db.commit()
            print(f"Seeded user {USER['email']}")

        for p in PROFILES:
            if db.query(models.Profile).filter_by(profile_id=p["profile_id"]).first():
                continue
            db.add(models.Profile(**p))
            db.commit()
            print(f"Seeded profile {p['profile_id']}")

        for e in EVIDENCE:
            if db.query(models.Evidence).filter_by(evidence_id=e["evidence_id"]).first():
                continue
            db.add(models.Evidence(**e))
            db.commit()
            print(f"Seeded evidence {e['evidence_id']}")
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
