"""
Engagement router for /api/v1/engagement endpoints.
Handles angle generation and email templates.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFoundException
from src.engagement_generator.services.angle_generator import AngleGenerator, EngagementAngle
from src.engagement_generator.services.template_engine import EmailTemplate, TemplateEngine
from src.opportunity_engine.models.opportunity import Opportunity

router = APIRouter(prefix="/api/v1/engagement", tags=["engagement"])


class AnglesResponse(BaseModel):
    opportunity_id: UUID
    angles: List[EngagementAngle]


class EmailRequest(BaseModel):
    opportunity_id: UUID
    angle_index: int = 0
    recipient_name: str
    sender_name: str


class EmailResponse(BaseModel):
    opportunity_id: UUID
    email: EmailTemplate


class ExportRequest(BaseModel):
    opportunity_ids: List[UUID]
    format: str = "csv"  # csv, json


class ExportResponse(BaseModel):
    download_url: str
    format: str
    record_count: int


@router.get("/angles/{opportunity_id}")
async def generate_angles(
    opportunity_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> AnglesResponse:
    """
    Generate engagement angles for an opportunity.
    
    Path Parameters:
    - opportunity_id: UUID of the opportunity
    
    Returns 3 different angles with varying tones (consultative, urgent, strategic).
    """
    # Placeholder - would fetch opportunity and generate angles
    generator = AngleGenerator()
    
    # Mock response for now
    return AnglesResponse(
        opportunity_id=opportunity_id,
        angles=[
            EngagementAngle(
                title="Abordagem Consultiva",
                approach="Notamos que a empresa está em fase de crescimento...",
                insight="Empresa em fase de crescimento com necessidades de estruturação",
                value_proposition="Insights gratuitos sobre melhores práticas",
                tone="consultative",
            ),
            EngagementAngle(
                title="Abordagem de Urgência",
                approach="Vimos que estão contratando liderança financeira...",
                insight="Contratação de liderança indica momento de transformação",
                value_proposition="Suporte imediato para acelerar estruturação",
                tone="urgent",
            ),
            EngagementAngle(
                title="Abordagem Estratégica",
                approach="Como parceiros de várias empresas em fase similar...",
                insight="Benchmark de empresas em fase similar",
                value_proposition="Acesso a dados e benchmarks exclusivos",
                tone="strategic",
            ),
        ],
    )


@router.post("/emails/{opportunity_id}")
async def generate_email(
    opportunity_id: UUID,
    request: EmailRequest,
    db: AsyncSession = Depends(get_db),
) -> EmailResponse:
    """
    Generate an outreach email for an opportunity.
    
    Path Parameters:
    - opportunity_id: UUID of the opportunity
    
    Request Body:
    - angle_index: Which angle to use (0, 1, or 2)
    - recipient_name: Name of the recipient
    - sender_name: Name of the sender
    """
    # Placeholder - would generate actual email
    engine = TemplateEngine()
    
    mock_opportunity = Opportunity(
        company_id=UUID("00000000-0000-0000-0000-000000000000"),
        diagnosis_ids=[],
        recommended_services=[],
        priority_score=0.8,
        urgency_score=0.7,
        revenue_potential="high",
        fit_score=0.9,
    )
    
    mock_angle = {
        "title": "Abordagem Consultiva",
        "tone": "consultative",
        "insight": "Empresa em fase de crescimento",
        "value_proposition": "Insights de melhores práticas",
    }
    
    mock_company = {
        "name": "TechCorp",
        "industry": "Software",
        "funding_stage": "series_a",
    }
    
    email = engine.generate_email(
        opportunity=mock_opportunity,
        angle=mock_angle,
        recipient_name=request.recipient_name,
        sender_name=request.sender_name,
        company_info=mock_company,
    )
    
    return EmailResponse(
        opportunity_id=opportunity_id,
        email=email,
    )


@router.post("/export")
async def export_opportunities(
    request: ExportRequest,
    db: AsyncSession = Depends(get_db),
) -> ExportResponse:
    """
    Export opportunities to CSV or JSON.
    
    Request Body:
    - opportunity_ids: List of opportunity UUIDs to export
    - format: Export format (csv or json)
    
    Returns a download URL for the exported file.
    """
    # Placeholder - would generate export file
    return ExportResponse(
        download_url=f"/api/v1/exports/download/export_{request.format}.csv",
        format=request.format,
        record_count=len(request.opportunity_ids),
    )
