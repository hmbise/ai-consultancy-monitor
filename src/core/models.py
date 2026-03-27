"""
SQLAlchemy models for database persistence.
These models map to tables in the ai_consultancy schema.
"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class CompanyDB(Base):
    """Company database model."""
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Firmographics
    employee_count_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    employee_count_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location_country: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    location_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Funding
    funding_stage: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_funding_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_funding_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_raised: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Signals
    last_signal_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    signals: Mapped[List["SignalDB"]] = relationship(
        back_populates="company",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    diagnoses: Mapped[List["DiagnosisDB"]] = relationship(
        back_populates="company",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    opportunities: Mapped[List["OpportunityDB"]] = relationship(
        back_populates="company",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<CompanyDB(name='{self.name}', slug='{self.slug}')>"


class SignalDB(Base):
    """Signal database model."""
    __tablename__ = "signals"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    raw_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    company: Mapped["CompanyDB"] = relationship(back_populates="signals")
    diagnoses: Mapped[List["DiagnosisDB"]] = relationship(
        secondary="diagnosis_signals",
        back_populates="signals",
    )

    def __repr__(self) -> str:
        return f"<SignalDB(type='{self.signal_type}', company='{self.company_id}')>"


# Association table for Diagnosis <-> Signal many-to-many
diagnosis_signals = Table(
    "diagnosis_signals",
    Base.metadata,
    Column("diagnosis_id", UUID(as_uuid=True), ForeignKey("diagnoses.id"), primary_key=True),
    Column("signal_id", UUID(as_uuid=True), ForeignKey("signals.id"), primary_key=True),
)


class DiagnosisDB(Base):
    """Diagnosis database model."""
    __tablename__ = "diagnoses"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )
    diagnosis_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)

    # Reasoning
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)

    # Confidence
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_factors: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )

    # Metadata
    diagnosed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    company: Mapped["CompanyDB"] = relationship(back_populates="diagnoses")
    signals: Mapped[List["SignalDB"]] = relationship(
        secondary=diagnosis_signals,
        back_populates="diagnoses",
    )
    opportunities: Mapped[List["OpportunityDB"]] = relationship(
        secondary="opportunity_diagnoses",
        back_populates="diagnoses",
    )

    def __repr__(self) -> str:
        return f"<DiagnosisDB(type='{self.diagnosis_type}', company='{self.company_id}')>"


# Association table for Opportunity <-> Diagnosis many-to-many
opportunity_diagnoses = Table(
    "opportunity_diagnoses",
    Base.metadata,
    Column("opportunity_id", UUID(as_uuid=True), ForeignKey("opportunities.id"), primary_key=True),
    Column("diagnosis_id", UUID(as_uuid=True), ForeignKey("diagnoses.id"), primary_key=True),
)


class OpportunityDB(Base):
    """Opportunity database model."""
    __tablename__ = "opportunities"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )

    # Service Recommendation
    recommended_services: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )

    # Scoring
    priority_score: Mapped[float] = mapped_column(Float, nullable=False)
    urgency_score: Mapped[float] = mapped_column(Float, nullable=False)
    revenue_potential: Mapped[str] = mapped_column(String(10), nullable=False)
    fit_score: Mapped[float] = mapped_column(Float, nullable=False)

    # Engagement
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False)
    outreach_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    company: Mapped["CompanyDB"] = relationship(back_populates="opportunities")
    diagnoses: Mapped[List["DiagnosisDB"]] = relationship(
        secondary=opportunity_diagnoses,
        back_populates="opportunities",
    )

    def __repr__(self) -> str:
        return f"<OpportunityDB(score={self.priority_score}, status='{self.status}')>"
