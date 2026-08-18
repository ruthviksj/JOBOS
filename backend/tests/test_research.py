"""Tests for the research agent parser (spec 14)."""

from app.services.research import detect_ats, parse_jd

SAMPLE_JD = """
Senior Product Manager - Fintech

Bengaluru, India (Hybrid)

We are hiring a Product Manager to own our lending platform.
Requirements:
- 4+ years of product management experience
- Experience with lending, risk analytics and payments
- Strong API and platform thinking
- SQL skills preferred
Compensation: Rs. 25,00,000 - 35,00,000 per annum
"""


def test_detect_ats():
    assert detect_ats("https://boards.greenhouse.io/xyz/jobs/1") == "greenhouse"
    assert detect_ats("https://jobs.lever.co/abc") == "lever"
    assert detect_ats("https://company.com/careers") is None


def test_parse_jd_experience():
    parsed = parse_jd(SAMPLE_JD)
    assert parsed["minimum_experience"] == 4
    assert parsed["remote_policy"] == "hybrid"
    assert parsed["location"] == "Bengaluru"
    assert parsed["seniority"] == "senior"
    assert parsed["requirements"], "should extract requirement bullets"


def test_parse_jd_title():
    parsed = parse_jd(SAMPLE_JD)
    assert parsed["title"] and "Product Manager" in parsed["title"]
