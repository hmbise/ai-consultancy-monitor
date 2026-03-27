"""
Diagnosis models for organizational diagnosis AI module.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DiagnosisType(str, Enum):
    OPERATIONAL_CHAOS = "operational_chaos"
    FINANCE_IMMATURITY = "finance_immaturity"
    GOVERNANCE_GAP = "governance_gap"
    DATA_BLINDNESS = "data_blindness"
    GROWTH_SCALING = "growth_scaling"
    MARKET_EXPANDING = "market_expanding"
    PRODUCT_MATURITY = "product_maturity"
    LEADERSHIP_GAP = "leadership_gap"


class DiagnosisSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Diagnosis(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_id: UUID
    diagnosis_type: DiagnosisType
    severity: DiagnosisSeverity

    # Reasoning
    summary: str
    reasoning: str
    supporting_signals: List[UUID]

    # Confidence
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_factors: List[str]

    # Metadata
    diagnosed_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "company_id": "660e8400-e29b-41d4-a716-446655440001",
                "diagnosis_type": "finance_immaturity",
                "severity": "high",
                "summary": "A empresa não possui estrutura financeira para escalar",
                "reasoning": "A análise dos sinais indica contratação de liderança financeira...",
                "supporting_signals": ["550e8400-...", "551e8400-..."],
                "confidence_score": 0.85,
                "confidence_factors": [
                    "Sinais recentes de hiring financeiro",
                    "Ausência de VP de Finance anterior",
                ],
                "diagnosed_at": "2026-03-27T10:00:00Z",
            }
        }


class DiagnosisFeedback(BaseModel):
    diagnosis_id: UUID
    is_accurate: bool
    feedback: Optional[str] = None
    suggested_diagnosis: Optional[DiagnosisType] = None
    suggested_severity: Optional[DiagnosisSeverity] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
