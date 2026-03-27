"""
Company router for /api/v1/companies endpoints.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFoundException
from src.signal_scanner.models.company import Company, FundingStage
from src.signal_scanner.models.signal import Signal

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])


class CompanyListResponse(BaseModel):
    data: List[Company]
    pagination: dict


class ScanResponse(BaseModel):
    company_id: UUID
    scan_id: str
    status: str
    message: str


@router.get("")
async def list_companies(
    industry: Optional[str] = Query(None),
    min_employees: Optional[int] = Query(None),
    funding_stage: Optional[FundingStage] = Query(None),
    location_country: Optional[str] = Query(None),
    is_active: bool = Query(True),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
) -> CompanyListResponse:
    """
    List companies with optional filters.
    
    Query Parameters:
    - industry: Filter by industry (e.g., "Software", "Fintech")
    - min_employees: Minimum employee count
    - funding_stage: Filter by funding stage (pre_seed, seed, series_a, etc.)
    - location_country: Filter by country code (e.g., "BR", "US")
    - is_active: Only active companies (default: true)
    - page: Page number (1-based)
    - page_size: Items per page (max 100)
    """
    # Placeholder implementation
    return CompanyListResponse(
        data=[],
        pagination={
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
        },
    )


@router.get("/{company_id}")
async def get_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Company:
    """
    Get detailed information about a specific company.
    
    Path Parameters:
    - company_id: UUID of the company to retrieve
    """
    # Placeholder implementation
    raise NotFoundException("Company")


@router.post("/scan", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def scan_company(
    company_name: str,
    domain: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> ScanResponse:
    """
    Initiate a scan for a new company.
    
    This will:
    1. Create a company record if it doesn't exist
    2. Queue signal scanning jobs across all sources
    3. Return a scan ID to track progress
    
    Query Parameters:
    - company_name: Name of the company to scan
    - domain: Optional domain for better matching
    """
    # Placeholder implementation - would:
    # 1. Create/find company
    # 2. Queue scan tasks
    # 3. Return scan tracking info
    return ScanResponse(
        company_id=UUID("00000000-0000-0000-0000-000000000000"),
        scan_id="scan_12345",
        status="queued",
        message=f"Scan queued for {company_name}. This may take a few minutes.",
    )


@router.get("/{company_id}/signals")
async def get_company_signals(
    company_id: UUID,
    since: Optional[datetime] = Query(None),
    signal_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> List[Signal]:
    """
    Get all signals for a specific company.
    
    Path Parameters:
    - company_id: UUID of the company
    
    Query Parameters:
    - since: Only signals after this datetime
    - signal_type: Filter by signal type
    """
    # Placeholder implementation
    return []


@router.post("/{company_id}/refresh")
async def refresh_company_scan(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ScanResponse:
    """
    Refresh signals for an existing company.
    
    Path Parameters:
    - company_id: UUID of the company to refresh
    """
    # Placeholder implementation
    return ScanResponse(
        company_id=company_id,
        scan_id="scan_refresh_12345",
        status="queued",
        message="Refresh queued. This may take a few minutes.",
    )
