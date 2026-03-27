from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SignalSource(str, Enum):
    NEWS_API = "news_api"
    JOB_BOARD = "job_board"
    GLASSDOOR = "glassdoor"
    CRUNCHBASE = "crunchbase"
    LINKEDIN = "linkedin"
    PRESS_RELEASE = "press_release"


class SignalType(str, Enum):
    # Hiring Signals
    HIRING_FINANCE_LEAD = "hiring_finance_lead"
    HIRING_FP_A = "hiring_fp_a"
    HIRING_CONTROLLER = "hiring_controller"
    HIRING_OPS_LEAD = "hiring_ops_lead"
    HIRING_DATA_LEAD = "hiring_data_lead"
    HIRING_LEGAL_LEAD = "hiring_legal_lead"

    # Funding Signals
    FUNDING_ANNOUNCED = "funding_announced"
    FUNDING_STAGE_CHANGE = "funding_stage_change"

    # Operational Signals
    LEADERSHIP_CHANGE = "leadership_change"
    OFFICE_EXPANSION = "office_expansion"
    NEW_PRODUCT = "new_product"

    # Review Signals
    NEGATIVE_REVIEW_SPIKE = "negative_review_spike"
    LOW_RATING = "low_rating"

    # Job Quality Signals
    RAPID_HIRING = "rapid_hiring"
    CHAOS_HIRING = "chaos_hiring"


class Signal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_id: UUID
    source: SignalSource
    signal_type: SignalType
    title: str
    content: str
    url: Optional[str] = None
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    raw_data: dict = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "company_id": "660e8400-e29b-41d4-a716-446655440001",
                "source": "job_board",
                "signal_type": "hiring_finance_lead",
                "title": "Hiring VP of Finance",
                "content": "Company X is hiring VP of Finance to lead financial planning...",
                "url": "https://indeed.com/job/123",
                "discovered_at": "2026-03-27T10:00:00Z",
                "raw_data": {},
            }
        }
