"""
Opportunity models for consulting opportunity engine.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OpportunityService(str, Enum):
    FINANCIAL_STRUCTURING = "financial_structuring"
    FP_A_IMPLEMENTATION = "fp_a_implementation"
    OPERATIONS_PROCESSES = "operations_processes"
    DATA_DASHBOARDS = "data_dashboards"
    GOVERNANCE_ADVISORY = "governance_advisory"
    EXECUTIVE_COACHING = "executive_coaching"
    M_AND_A_SUPPORT = "m_and_a_support"
    IPO_PREPARATION = "ipo_preparation"


class OpportunityStatus(str, Enum):
    NEW = "new"
    REACHED_OUT = "reached_out"
    IN_CONVERSATION = "in_conversation"
    PROPOSAL_SENT = "proposal_sent"
    WON = "won"
    LOST = "lost"


class CompanyInfo(BaseModel):
    id: UUID
    name: str
    domain: Optional[str] = None
    employee_count: Optional[int] = None
    funding_stage: Optional[str] = None


class DiagnosisSummary(BaseModel):
    type: str
    severity: str
    confidence: float


class Opportunity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_id: UUID
    diagnosis_ids: List[UUID]

    # Service Recommendation
    recommended_services: List[OpportunityService]

    # Scoring
    priority_score: float = Field(ge=0.0, le=1.0)
    urgency_score: float = Field(ge=0.0, le=1.0)
    revenue_potential: str  # "low", "medium", "high"
    fit_score: float = Field(ge=0.0, le=1.0)

    # Engagement
    status: OpportunityStatus = OpportunityStatus.NEW
    outreach_note: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "company_id": "660e8400-e29b-41d4-a716-446655440001",
                "diagnosis_ids": ["880e8400-e29b-41d4-a716-446655440002"],
                "recommended_services": ["financial_structuring", "fp_a_implementation"],
                "priority_score": 0.82,
                "urgency_score": 0.75,
                "revenue_potential": "high",
                "fit_score": 0.90,
                "status": "new",
                "created_at": "2026-03-27T10:00:00Z",
            }
        }


class OpportunityDetail(Opportunity):
    company: CompanyInfo
    diagnoses: List[DiagnosisSummary]
