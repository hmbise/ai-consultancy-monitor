from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.signal_scanner.models.signal import Signal


class FundingStage(str, Enum):
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D_PLUS = "series_d_plus"
    IPO = "ipo"


class Company(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    slug: str
    domain: Optional[str] = None

    # Firmographics
    employee_count_range: Optional[Tuple[int, int]] = None
    industry: Optional[str] = None
    location_country: Optional[str] = None
    location_city: Optional[str] = None

    # Funding
    funding_stage: Optional[FundingStage] = None
    last_funding_amount: Optional[float] = None
    last_funding_date: Optional[datetime] = None
    total_raised: Optional[float] = None

    # Signals
    signals: List[Signal] = Field(default_factory=list)
    last_signal_at: Optional[datetime] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "name": "TechCorp Brasil",
                "slug": "techcorp-brasil",
                "domain": "techcorp.com.br",
                "employee_count_range": [50, 200],
                "industry": "Software",
                "location_country": "BR",
                "location_city": "São Paulo",
                "funding_stage": "series_a",
                "last_funding_amount": 5000000.0,
                "signals": [],
                "created_at": "2026-03-27T10:00:00Z",
                "is_active": True,
            }
        }
