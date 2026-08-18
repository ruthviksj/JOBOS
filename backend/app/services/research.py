"""Research Agent (spec 14, 51).

Fetches a job URL, extracts the job description, and parses it into a canonical
Job record. Deterministic + heuristic (no LLM dependency for the slice): regex
parsing for title/experience/location/remote/salary, keyword detection for ATS.

Phase A/B (URL analysis, job extraction) and Phase C (application discovery) are
covered here. Phase D (company research) and the LLM-based TLDR are stubbed.
"""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

APP_METHODS = [
    (r"greenhouse\.io", "greenhouse"),
    (r"jobs\.lever\.co|lever\.co", "lever"),
    (r"jobs\.ashbyhq\.com|ashbyhq\.com", "ashby"),
    (r"workday\.com", "workday"),
    (r"applytojob\.com", "jobvite"),
    (r"smartrecruiters\.com", "smartrecruiters"),
]

EXP_RE = re.compile(
    r"(\d+)\+?\s*(?:-|to)?\s*(\d+)?\s*years?(?:\s*of)?(?:\s*experience)?",
    re.IGNORECASE,
)
REMOTE_RE = re.compile(r"\b(remote|hybrid|onsite|on-site|in[- ]office)\b", re.IGNORECASE)
LOCATION_RE = re.compile(
    r"\b(bengaluru|bangalore|mumbai|delhi|hyderabad|pune|chennai|gurgaon|"
    r"gurugram|noida|india)\b",
    re.IGNORECASE,
)
SALARY_RE = re.compile(
    r"(?:₹|INR|Rs\.?)\s?([\d,]+(?:\s?(?:-|to)\s?[\d,]+)?)\s?([lLkK]|lpa|ctc)?",
    re.IGNORECASE,
)
SENIORITY_RE = re.compile(
    r"\b(senior|lead|principal|staff|junior|associate|head of|director)\b",
    re.IGNORECASE,
)


def detect_ats(url: str) -> str | None:
    low = url.lower()
    for pattern, ats in APP_METHODS:
        if re.search(pattern, low):
            return ats
    return None


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_jd(url: str, timeout: float = 15.0) -> str:
    """Fetch a job page and return its visible text."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; JOBOS/0.2)"}
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    return strip_html(text)


def _extract_title(jd_text: str) -> str | None:
    # ATS pages often have the title in an h1.
    # Heuristic: first line that mentions "product"/"manager"/"engineer".
    lines = [ln for ln in re.split(r"[.\n]", jd_text) if ln.strip()]
    for ln in lines:
        if re.search(r"\b(product manager|product owner|product analyst)\b", ln, re.IGNORECASE):
            return strip_html(ln).strip(" .")[:120]
    return None


def parse_jd(jd_text: str) -> dict:
    """Parse JD text into structured fields."""
    title = _extract_title(jd_text)

    exp_match = EXP_RE.search(jd_text)
    min_exp = int(exp_match.group(1)) if exp_match else None
    max_exp = int(exp_match.group(2)) if exp_match and exp_match.group(2) else None

    remote_match = REMOTE_RE.search(jd_text)
    remote = remote_match.group(1).lower() if remote_match else None

    loc_match = LOCATION_RE.search(jd_text)
    location = loc_match.group(1).capitalize() if loc_match else None

    salary_match = SALARY_RE.search(jd_text)
    salary_text = salary_match.group(0) if salary_match else None

    seniority = None
    sn = SENIORITY_RE.search(jd_text)
    if sn:
        seniority = sn.group(1).lower()

    # Requirements: bullet-ish lines under a "requirements/qualifications" heading.
    requirements: list[str] = []
    body = jd_text
    m = re.search(r"(requirements|qualifications|what you'?ll (bring|need)|about you)\s*[:.]?\s*", body, re.IGNORECASE)
    if m:
        tail = body[m.end():]
        head = re.match(r"^(.{0,600})", tail)
        seg = head.group(1) if head else tail
        parts = re.split(r"[•·▪\n]|(?<!\d)\.\s+", seg)
        requirements = [p.strip(" -") for p in parts if len(p.strip(" -")) > 15][:10]

    return {
        "title": title,
        "minimum_experience": min_exp,
        "preferred_experience": max_exp,
        "remote_policy": remote,
        "location": location,
        "salary_raw": salary_text,
        "seniority": seniority,
        "requirements": requirements,
        "jd_tldr": jd_text[:400],
    }


def research(url: str) -> dict:
    """Run the research agent on one URL: fetch + parse + ATS detect."""
    jd_text = fetch_jd(url)
    parsed = parse_jd(jd_text)
    parsed["jd_url"] = url
    parsed["application_url"] = url
    parsed["ats"] = detect_ats(url)
    parsed["full_jd"] = jd_text
    parsed["research_timestamp"] = date.today().isoformat()
    return parsed
