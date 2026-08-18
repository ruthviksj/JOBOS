"""Browser Application Agent (spec 31-34, 60).

Field mapping + decision engine for autofilling application forms. A Chrome
extension reads the visible form fields and posts them here; this service:

1. Classifies each field semantically (spec 32).
2. Looks up candidate data from the master profile.
3. Computes a confidence score and an action: AUTOFILL / SUGGEST / GENERATE /
   ASK / BLOCK.
4. Flags high-risk fields (spec 33) so the user decides — never silent autofill.

The agent operates only within an approved application session (spec 54) and
never invents data (spec 31).
"""

from __future__ import annotations

from app.seed_data import USER

# candidate data from the master profile (spec 10)
CANDIDATE = {
    "first_name": "Ruthvik",
    "last_name": "S J",
    "email": USER["email"],
    "phone": USER["phone"],
    "location": "Bengaluru, Karnataka, India",
    "country": "India",
    "linkedin": "linkedin.com/in/sjruthvik",
    "portfolio": "sjruthvik.in",
    "work_authorization": "India (citizen)",
}

# (field-label keywords) -> candidate key
FIELD_MAP = {
    ("first", "firstname", "first name", "given"): "first_name",
    ("last", "lastname", "last name", "surname", "family"): "last_name",
    ("email", "email address"): "email",
    ("phone", "mobile", "contact", "telephone"): "phone",
    ("location", "city", "current city", "address"): "location",
    ("country",): "country",
    ("linkedin", "linkedin url", "linkedin profile"): "linkedin",
    ("portfolio", "website", "personal site", "url"): "portfolio",
}

# High-risk fields (spec 33): never silently autofill.
HIGH_RISK = [
    "salary", "salary expectation", "compensation", "visa", "sponsorship",
    "work authorization", "criminal", "background check", "legal", "disability",
    "medical", "demographic", "ethnicity", "gender", "veteran", "employment eligibility",
]

# Factual/profile-derived keys that can be GENERATE'd from evidence.
GENERATIVE_KEYS = {"portfolio", "linkedin"}


def classify_field(label: str) -> tuple[str | None, bool]:
    """Return (candidate_key, is_high_risk) for a field label."""
    low = (label or "").lower()
    for sig in HIGH_RISK:
        if sig in low:
            return None, True
    for keys, cand in FIELD_MAP.items():
        if any(k in low for k in keys):
            return cand, False
    return None, False


def map_fields(fields: list[str]) -> list[dict]:
    """Map a list of detected form field labels to actions (spec 32)."""
    out = []
    for label in fields:
        key, high_risk = classify_field(label)
        if high_risk:
            out.append({
                "field": label, "action": "BLOCK",
                "reason": "high-risk field - requires review (spec 33)",
            })
            continue
        if key is None:
            out.append({
                "field": label, "action": "ASK",
                "reason": "unknown field - cannot map",
            })
            continue
        if key in GENERATIVE_KEYS:
            out.append({
                "field": label, "action": "GENERATE",
                "value": CANDIDATE[key],
                "confidence": 0.9,
            })
            continue
        out.append({
            "field": label, "action": "AUTOFILL",
            "value": CANDIDATE[key],
            "confidence": 0.98,
        })
    return out


def review_required(fields: list[str]) -> bool:
    """Spec 35: any high-risk or unknown field requires human review."""
    return any(f["action"] in ("BLOCK", "ASK") for f in map_fields(fields))
