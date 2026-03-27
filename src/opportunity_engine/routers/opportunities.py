"""
Opportunities router for /api/v1/opportunities endpoints.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFoundException
from src.opportunity_engine.models.opportunity import (
    Opportunity,
    OpportunityDetail,
    OpportunityService,
    OpportunityStatus,
)

router = APIRouter(prefix="/api/v1/opportunities", tags=["opportunities"])


class OpportunityListResponse(BaseModel):
    data: List[OpportunityDetail]
    pagination: dict


class RankingResponse(BaseModel):
    data: List[OpportunityDetail]
    total: int


class StatusUpdateRequest(BaseModel):
    status: OpportunityStatus
    note: Optional[str] = None


class StatusUpdateResponse(BaseModel):
    opportunity_id: UUID
    previous_status: OpportunityStatus
    new_status: OpportunityStatus
    updated_at: str


@router.get("")
async def list_opportunities(
    status: Optional[OpportunityStatus] = Query(None),
    min_score: float = Query(0.0, ge=0, le=1),
    service: Optional[OpportunityService] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> OpportunityListResponse:
    """
    List opportunities with optional filters.
    
    Query Parameters:
    - status: Filter by opportunity status
    - min_score: Minimum priority score (0.0 - 1.0)
    - service: Filter by recommended service
    - limit: Maximum number of results
    - offset: Pagination offset
    """
    return OpportunityListResponse(
        data=[],
        pagination={
            "total": 0,
            "limit": limit,
            "offset": offset,
        },
    )


@router.get("/ranking")
async def get_opportunity_ranking(
    min_score: float = Query(0.5, ge=0, le=1),
    services: List[OpportunityService] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
) -> RankingResponse:
    """
    Get ranked list of opportunities sorted by priority score.
    
    Query Parameters:
    - min_score: Minimum priority score to include (default: 0.5)
    - services: Filter by specific services
    - limit: Maximum number of results (default: 20)
    """
    return RankingResponse(data=[], total=0)


@router.get("/{opportunity_id}")
async def get_opportunity(
    opportunity_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> OpportunityDetail:
    """
    Get detailed information about a specific opportunity.
    
    Path Parameters:
    - opportunity_id: UUID of the opportunity
    """
    raise NotFoundException("Opportunity")


@router.post("/{opportunity_id}/status", response_model=StatusUpdateResponse)
async def update_opportunity_status(
    opportunity_id: UUID,
    request: StatusUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> StatusUpdateResponse:
    """
    Update the status of an opportunity.
    
    Path Parameters:
    - opportunity_id: UUID of the opportunity
    
    Request Body:
    - status: New status (new, reached_out, in_conversation, proposal_sent, won, lost)
    - note: Optional note about the status change
    """
    return StatusUpdateResponse(
        opportunity_id=opportunity_id,
        previous_status=OpportunityStatus.NEW,
        new_status=request.status,
        updated_at="2026-03-27T10:00:00Z",
    )


@router.get("/services")
async def list_services() -> dict:
    """List all available consulting services."""
    services = {
        OpportunityService.FINANCIAL_STRUCTURING: {
            "name": "Financial Structuring",
            "description": "Estruturação financeira: controles, processos, e governança",
        },
        OpportunityService.FP_A_IMPLEMENTATION: {
            "name": "FP&A Implementation",
            "description": "Implementação de FP&A: planejamento, orçamento, e análise",
        },
        OpportunityService.OPERATIONS_PROCESSES: {
            "name": "Operations Processes",
            "description": "Otimização de operações: processos e eficiência",
        },
        OpportunityService.DATA_DASHBOARDS: {
            "name": "Data Dashboards",
            "description": "Dashboards e BI: visualização de dados e KPIs",
        },
        OpportunityService.GOVERNANCE_ADVISORY: {
            "name": "Governance Advisory",
            "description": "Consultoria de governança: board e estrutura de decisão",
        },
        OpportunityService.EXECUTIVE_COACHING: {
            "name": "Executive Coaching",
            "description": "Coaching executivo: desenvolvimento de liderança",
        },
        OpportunityService.M_AND_A_SUPPORT: {
            "name": "M&A Support",
            "description": "Suporte a M&A: due diligence e integração",
        },
        OpportunityService.IPO_PREPARATION: {
            "name": "IPO Preparation",
            "description": "Preparação para IPO: compliance e governança",
        },
    }

    return {
        "services": [
            {"id": k.value, "name": v["name"], "description": v["description"]}
            for k, v in services.items()
        ]
    }
