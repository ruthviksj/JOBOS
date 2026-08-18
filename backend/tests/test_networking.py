"""Tests for the networking agent (spec 42-44)."""

import uuid

from app.db import SessionLocal
from app.services import networking as net


def _mk_contact(db, title, department=None, shared=False, connected=True):
    return net.add_contact(
        db, name=f"C-{uuid.uuid4().hex[:6]}", title=title, department=department,
        shared_background="Rang De" if shared else None,
        shared_connections=3 if connected else 0,
    )


def test_relevance_ranks_pm_domain_over_other():
    db = SessionLocal()
    pm = _mk_contact(db, "Senior Product Manager, Payments", department="Product")
    eng = _mk_contact(db, "Backend Engineer", department="Engineering")
    # rank against fintech domain
    res = net.discover_contacts(db, company_id=None, domain="Fintech")
    scores = {r["name"]: r["relevance_score"] for r in res}
    assert scores[pm.name] > scores[eng.name]
    db.close()


def test_referral_strategy_tiers():
    db = SessionLocal()
    c = _mk_contact(db, "Director of Product", department="Product", shared=True)
    c.referral_probability = 0.9
    db.commit()
    rank = next(r for r in net.discover_contacts(db, None, "Fintech")
                if r["contact_id"] == c.contact_id)
    strat = net.referral_strategy(rank)
    assert "referral" in strat.lower()
    db.close()
