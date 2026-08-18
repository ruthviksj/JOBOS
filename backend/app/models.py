"""JOBOS database schema (spec 49).

Operational tables for the candidate workspace. String-backed status/kind
columns (not DB enums) so the schema stays portable across SQLite and Postgres.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(64), unique=True)  # e.g. FINTECH_PM
    name: Mapped[str] = mapped_column(String(255))
    target_roles: Mapped[list] = mapped_column(JSON, default=list)
    target_industries: Mapped[list] = mapped_column(JSON, default=list)
    target_locations: Mapped[list] = mapped_column(JSON, default=list)
    preferred_company_stage: Mapped[list] = mapped_column(JSON, default=list)
    preferred_company_size: Mapped[list] = mapped_column(JSON, default=list)
    must_haves: Mapped[list] = mapped_column(JSON, default=list)
    nice_to_haves: Mapped[list] = mapped_column(JSON, default=list)
    dealbreakers: Mapped[list] = mapped_column(JSON, default=list)
    positioning_statement: Mapped[str | None] = mapped_column(Text)
    headline: Mapped[str | None] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(Text)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    domains: Mapped[list] = mapped_column(JSON, default=list)
    experience_emphasis: Mapped[list] = mapped_column(JSON, default=list)
    resume_base: Mapped[str | None] = mapped_column(Text)  # path or base content
    resume_rules: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(64), unique=True)  # EVID-001
    claim: Mapped[str] = mapped_column(Text)
    company: Mapped[str] = mapped_column(String(255))
    context: Mapped[str | None] = mapped_column(Text)
    metric: Mapped[str | None] = mapped_column(String(255))
    strength: Mapped[str] = mapped_column(String(32))  # Verified / Estimated / Directional / Case-study / Projected
    relevant_domains: Mapped[list] = mapped_column(JSON, default=list)
    allowed_claims: Mapped[list] = mapped_column(JSON, default=list)
    forbidden_inferences: Mapped[list] = mapped_column(JSON, default=list)
    source_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    legal_name: Mapped[str | None] = mapped_column(String(255))
    website: Mapped[str | None] = mapped_column(String(255))
    linkedin_url: Mapped[str | None] = mapped_column(String(255))
    industry: Mapped[str | None] = mapped_column(String(128))
    subindustry: Mapped[str | None] = mapped_column(String(128))
    company_size: Mapped[str | None] = mapped_column(String(64))
    company_stage: Mapped[str | None] = mapped_column(String(64))
    headquarters: Mapped[str | None] = mapped_column(String(255))
    locations: Mapped[list] = mapped_column(JSON, default=list)
    company_description: Mapped[str | None] = mapped_column(Text)
    company_tldr: Mapped[str | None] = mapped_column(Text)
    known_products: Mapped[list] = mapped_column(JSON, default=list)
    known_competitors: Mapped[list] = mapped_column(JSON, default=list)
    research_timestamp: Mapped[datetime | None] = mapped_column(DateTime)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[str] = mapped_column(String(64), unique=True)
    canonical_job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"))
    discovery_status: Mapped[str] = mapped_column(String(32), default="NEW")
    research_status: Mapped[str] = mapped_column(String(32), default="PENDING")  # pending/running/complete/failed
    application_status: Mapped[str] = mapped_column(String(32), default="DISCOVERED")
    priority_score: Mapped[float | None] = mapped_column(Float)
    compatibility_score: Mapped[float | None] = mapped_column(Float)
    recommended_profile_id: Mapped[str | None] = mapped_column(String(64))
    selected_profile_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    sources: Mapped[list[JobSource]] = relationship(back_populates="opportunity")
    job: Mapped[Job | None] = relationship(back_populates="opportunities")


class JobSource(Base):
    __tablename__ = "job_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
    source_type: Mapped[str] = mapped_column(String(32))  # linkedin/whatsapp/telegram/...
    source_name: Mapped[str | None] = mapped_column(String(255))
    source_channel: Mapped[str | None] = mapped_column(String(255))
    sender: Mapped[str | None] = mapped_column(String(255))
    message_id: Mapped[str | None] = mapped_column(String(255))
    message_timestamp: Mapped[datetime | None] = mapped_column(DateTime)
    raw_text: Mapped[str | None] = mapped_column(Text)  # never discard the raw source
    urls: Mapped[list] = mapped_column(JSON, default=list)
    attachments: Mapped[list] = mapped_column(JSON, default=list)
    original_message: Mapped[str | None] = mapped_column(Text)

    opportunity: Mapped[Opportunity] = relationship(back_populates="sources")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] = mapped_column(String(64), unique=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"))
    title: Mapped[str] = mapped_column(String(255))
    normalized_title: Mapped[str | None] = mapped_column(String(255))
    department: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255))
    remote_policy: Mapped[str | None] = mapped_column(String(64))
    employment_type: Mapped[str | None] = mapped_column(String(64))
    minimum_experience: Mapped[float | None] = mapped_column(Float)
    preferred_experience: Mapped[float | None] = mapped_column(Float)
    salary_min: Mapped[float | None] = mapped_column(Float)
    salary_max: Mapped[float | None] = mapped_column(Float)
    salary_currency: Mapped[str | None] = mapped_column(String(8))
    industry: Mapped[str | None] = mapped_column(String(128))
    function: Mapped[str | None] = mapped_column(String(128))
    seniority: Mapped[str | None] = mapped_column(String(64))
    jd_url: Mapped[str | None] = mapped_column(String(512))
    application_url: Mapped[str | None] = mapped_column(String(512))
    application_method: Mapped[str | None] = mapped_column(String(64))  # greenhouse/lever/ashby/...
    ats: Mapped[str | None] = mapped_column(String(64))
    full_jd: Mapped[str | None] = mapped_column(Text)
    posting_date: Mapped[date | None] = mapped_column(Date)
    deadline: Mapped[date | None] = mapped_column(Date)
    jd_tldr: Mapped[str | None] = mapped_column(Text)
    company_tldr: Mapped[str | None] = mapped_column(Text)
    compatibility_score: Mapped[float | None] = mapped_column(Float)
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    gaps: Mapped[list] = mapped_column(JSON, default=list)
    risks: Mapped[list] = mapped_column(JSON, default=list)
    recommended_profile: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    opportunities: Mapped[list[Opportunity]] = relationship(back_populates="job")
    requirements: Mapped[list[JobRequirement]] = relationship(back_populates="job")


class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    kind: Mapped[str] = mapped_column(String(16))  # requirement / nice_to_have / dealbreaker
    text: Mapped[str] = mapped_column(Text)
    evidence_match: Mapped[str | None] = mapped_column(String(16))  # DIRECT/TRANSFERABLE/WEAKLY/NO EVIDENCE/CONTRADICTED
    evidence_id: Mapped[str | None] = mapped_column(String(64))
    explanation: Mapped[str | None] = mapped_column(Text)

    job: Mapped[Job] = relationship(back_populates="requirements")


class CompatibilityScore(Base):
    __tablename__ = "compatibility_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    profile_id: Mapped[str] = mapped_column(String(64))
    total: Mapped[float] = mapped_column(Float)
    breakdown: Mapped[dict] = mapped_column(JSON, default=dict)  # per-dimension weights/scores
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ApplicationPackage(Base):
    __tablename__ = "application_packages"

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
    profile_id: Mapped[str] = mapped_column(String(64))
    resume_version: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")  # draft/ready/generated
    company_research: Mapped[str | None] = mapped_column(Text)
    role_positioning: Mapped[str | None] = mapped_column(Text)
    instructions: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[str] = mapped_column(String(64), unique=True)  # APP-2026-xxxx
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
    status: Mapped[str] = mapped_column(String(32), default="READY")  # tracker states (37)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime)
    ats: Mapped[str | None] = mapped_column(String(64))
    source: Mapped[str | None] = mapped_column(String(32))
    confirmation_received: Mapped[bool] = mapped_column(default=False)
    resume_version: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)


class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    event_type: Mapped[str] = mapped_column(String(64))  # activity log event (47)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    detail: Mapped[str | None] = mapped_column(Text)


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id: Mapped[str] = mapped_column(String(64), unique=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"))
    name: Mapped[str] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    department: Mapped[str | None] = mapped_column(String(255))
    team: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    linkedin: Mapped[str | None] = mapped_column(String(255))
    current_company_start: Mapped[date | None] = mapped_column(Date)
    previous_companies: Mapped[list] = mapped_column(JSON, default=list)
    education: Mapped[str | None] = mapped_column(Text)
    shared_connections: Mapped[int | None] = mapped_column(Integer)
    shared_background: Mapped[str | None] = mapped_column(Text)
    relevance_score: Mapped[float | None] = mapped_column(Float)
    referral_probability: Mapped[float | None] = mapped_column(Float)
    research_notes: Mapped[str | None] = mapped_column(Text)
    contact_status: Mapped[str] = mapped_column(String(32), default="DISCOVERED")


class ContactEvent(Base):
    __tablename__ = "contact_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    event_type: Mapped[str] = mapped_column(String(64))  # connected/drafted/contacted/responded
    occurred_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    detail: Mapped[str | None] = mapped_column(Text)


class Outreach(Base):
    __tablename__ = "outreach"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    opportunity_id: Mapped[int | None] = mapped_column(ForeignKey("opportunities.id"))
    channel: Mapped[str | None] = mapped_column(String(32))  # linkedin/email/...
    message: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")  # draft/sent/replied
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)


class EmailEvent(Base):
    __tablename__ = "email_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int | None] = mapped_column(ForeignKey("applications.id"))
    message_id: Mapped[str | None] = mapped_column(String(255))
    classification: Mapped[str] = mapped_column(String(32))  # APPLICATION_CONFIRMATION/REJECTION/...
    received_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    snippet: Mapped[str | None] = mapped_column(Text)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_type: Mapped[str] = mapped_column(String(32))  # resume/cover_letter/application_answer
    version: Mapped[str | None] = mapped_column(String(64))
    profile_id: Mapped[str | None] = mapped_column(String(64))
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"))
    path: Mapped[str] = mapped_column(String(512))
    content: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent: Mapped[str] = mapped_column(String(32))  # research/match/resume/apply/network/tracker
    opportunity_id: Mapped[int | None] = mapped_column(ForeignKey("opportunities.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    inputs: Mapped[dict] = mapped_column(JSON, default=dict)
    actions: Mapped[list] = mapped_column(JSON, default=list)
    outputs: Mapped[dict] = mapped_column(JSON, default=dict)
    external_services: Mapped[list] = mapped_column(JSON, default=list)
    human_interventions: Mapped[list] = mapped_column(JSON, default=list)
    errors: Mapped[list] = mapped_column(JSON, default=list)
    result: Mapped[str | None] = mapped_column(String(32))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(255))
    target_type: Mapped[str | None] = mapped_column(String(64))
    target_id: Mapped[str | None] = mapped_column(String(64))
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
