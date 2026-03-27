"""
Signal router for /api/v1/signals endpoints.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFoundException
from src.signal_scanner.models.signal import Signal, SignalSource, SignalType

router = APIRouter(prefix="/api/v1/signals", tags=["signals"])


@router.get("")
async def list_signals(
    source: Optional[SignalSource] = Query(None),
    signal_type: Optional[SignalType] = Query(None),
    company_id: Optional[UUID] = Query(None),
    since: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    List signals with optional filters.
    
    Query Parameters:
    - source: Filter by signal source (news_api, job_board, etc.)
    - signal_type: Filter by signal type (hiring_finance_lead, funding_announced, etc.)
    - company_id: Filter by specific company
    - since: Only signals after this datetime
    - page: Page number (1-based)
    - page_size: Items per page (max 100)
    """
    # Placeholder implementation - would query database
    return {
        "data": [],
        "pagination": {
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
        },
    }


@router.get("/{signal_id}")
async def get_signal(
    signal_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Signal:
    """
    Get detailed information about a specific signal.
    
    Path Parameters:
    - signal_id: UUID of the signal to retrieve
    """
    # Placeholder implementation
    raise NotFoundException("Signal")


@router.get("/types")
async def list_signal_types() -> dict:
    """List all available signal types and their descriptions."""
    signal_types = {
        SignalType.HIRING_FINANCE_LEAD: "Company hiring finance leadership (CFO, VP Finance)",
        SignalType.HIRING_FP_A: "Company hiring FP&A roles",
        SignalType.HIRING_CONTROLLER: "Company hiring financial controller",
        SignalType.HIRING_OPS_LEAD: "Company hiring operations leadership",
        SignalType.HIRING_DATA_LEAD: "Company hiring data/analytics leadership",
        SignalType.HIRING_LEGAL_LEAD: "Company hiring legal leadership",
        SignalType.FUNDING_ANNOUNCED: "Funding announcement detected",
        SignalType.FUNDING_STAGE_CHANGE: "Company changed funding stage",
        SignalType.LEADERSHIP_CHANGE: "Leadership change detected",
        SignalType.OFFICE_EXPANSION: "Office expansion or new location",
        SignalType.NEW_PRODUCT: "New product or service launch",
        SignalType.NEGATIVE_REVIEW_SPIKE: "Spike in negative reviews",
        SignalType.LOW_RATING: "Low company rating detected",
        SignalType.RAPID_HIRING: "Rapid hiring across multiple roles",
        SignalType.CHAOS_HIRING: "Chaotic hiring pattern detected",
    }
    
    return {
        "signal_types": [
            {"type": t.value, "description": d}
            for t, d in signal_types.items()
        ]
    }
