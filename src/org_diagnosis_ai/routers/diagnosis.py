"""
Diagnosis router for /api/v1/diagnosis endpoints.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFoundException
from src.org_diagnosis_ai.models.diagnosis import (
    Diagnosis,
    DiagnosisFeedback,
    DiagnosisSeverity,
    DiagnosisType,
)
from src.org_diagnosis_ai.prompts.diagnosis_prompts import DIAGNOSIS_TYPES_DESCRIPTION
from src.org_diagnosis_ai.services.classifier import DiagnosisClassifier

router = APIRouter(prefix="/api/v1/diagnosis", tags=["diagnosis"])


class CreateDiagnosisRequest(BaseModel):
    company_id: UUID
    force_recalculate: bool = False


class DiagnosisResponse(BaseModel):
    data: Diagnosis


class DiagnosisListResponse(BaseModel):
    data: List[Diagnosis]


class FeedbackRequest(BaseModel):
    is_accurate: bool
    feedback: Optional[str] = None
    suggested_diagnosis: Optional[DiagnosisType] = None
    suggested_severity: Optional[DiagnosisSeverity] = None


@router.post("", response_model=DiagnosisResponse, status_code=status.HTTP_201_CREATED)
async def create_diagnosis(
    request: CreateDiagnosisRequest,
    db: AsyncSession = Depends(get_db),
) -> DiagnosisResponse:
    """
    Create a new diagnosis for a company.
    
    This will:
    1. Fetch the company's signals
    2. Run the LLM-based diagnosis classification
    3. Store and return the diagnosis
    
    Request Body:
    - company_id: UUID of the company to diagnose
    - force_recalculate: If true, ignore cached diagnosis and recalculate
    """
    # Placeholder - would implement actual diagnosis flow
    raise NotImplementedError("Diagnosis creation not yet implemented")


@router.get("/{diagnosis_id}")
async def get_diagnosis(
    diagnosis_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Diagnosis:
    """
    Get a specific diagnosis by ID.
    
    Path Parameters:
    - diagnosis_id: UUID of the diagnosis to retrieve
    """
    raise NotFoundException("Diagnosis")


@router.get("/company/{company_id}")
async def get_company_diagnosis(
    company_id: UUID,
    active_only: bool = Query(True, description="Only return non-expired diagnoses"),
    db: AsyncSession = Depends(get_db),
) -> Diagnosis:
    """
    Get the current diagnosis for a company.
    
    Path Parameters:
    - company_id: UUID of the company
    
    Query Parameters:
    - active_only: If true, only return non-expired diagnoses
    """
    raise NotFoundException("Diagnosis")


@router.post("/{diagnosis_id}/feedback")
async def submit_feedback(
    diagnosis_id: UUID,
    feedback: FeedbackRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Submit feedback on a diagnosis (human-in-the-loop).
    
    Path Parameters:
    - diagnosis_id: UUID of the diagnosis
    
    Request Body:
    - is_accurate: Whether the diagnosis was accurate
    - feedback: Optional text feedback
    - suggested_diagnosis: Alternative diagnosis type if inaccurate
    - suggested_severity: Alternative severity if inaccurate
    """
    # Placeholder - would store feedback for model improvement
    return {
        "status": "received",
        "diagnosis_id": diagnosis_id,
        "message": "Thank you for your feedback. It will help improve our models.",
    }


@router.get("/history/{company_id}")
async def get_diagnosis_history(
    company_id: UUID,
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db),
) -> DiagnosisListResponse:
    """
    Get the history of diagnoses for a company.
    
    Path Parameters:
    - company_id: UUID of the company
    
    Query Parameters:
    - limit: Maximum number of historical diagnoses to return
    """
    return DiagnosisListResponse(data=[])


@router.get("/types")
async def list_diagnosis_types() -> dict:
    """List all available diagnosis types with descriptions."""
    return {
        "diagnosis_types": [
            {
                "type": key,
                "name": value["name"],
                "description": value["description"],
                "indicators": value["indicators"],
            }
            for key, value in DIAGNOSIS_TYPES_DESCRIPTION.items()
        ]
    }


@router.get("/types/{diagnosis_type}")
async def get_diagnosis_type_info(diagnosis_type: DiagnosisType) -> dict:
    """Get detailed information about a specific diagnosis type."""
    info = DIAGNOSIS_TYPES_DESCRIPTION.get(diagnosis_type.value, {})
    return {
        "type": diagnosis_type.value,
        "name": info.get("name", ""),
        "description": info.get("description", ""),
        "indicators": info.get("indicators", []),
    }
