"""
Glassdoor data extraction service.
Note: Glassdoor requires API partnership for production use.
"""
from typing import Any, Dict, List, Optional

import httpx

from src.core.config import get_settings
from src.core.exceptions import ExternalAPIException
from src.signal_scanner.models.signal import SignalType

settings = get_settings()


class GlassdoorExtractor:
    """Extracts company review and rating data from Glassdoor."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.glassdoor_api_key
        self.base_url = "https://api.glassdoor.com/api/api.htm"

    async def get_company_reviews(
        self,
        company_name: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get company reviews from Glassdoor.
        
        Note: In production, this requires Glassdoor API partnership.
        This is a placeholder implementation.
        """
        if not self.api_key:
            raise ExternalAPIException(
                "Glassdoor",
                "Glassdoor API key not configured"
            )

        # Placeholder implementation
        # In production, integrate with actual Glassdoor API
        return []

    async def analyze_company_rating(
        self,
        company_name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze company rating and detect negative trends.
        
        Returns:
            Signal data if low rating detected, None otherwise
        """
        reviews = await self.get_company_reviews(company_name)

        if not reviews:
            return None

        # Calculate average rating
        ratings = [r.get("rating", 0) for r in reviews if r.get("rating")]
        if not ratings:
            return None

        avg_rating = sum(ratings) / len(ratings)

        # Detect low rating signal
        if avg_rating < 3.0 and len(ratings) > 10:
            return {
                "signal_type": SignalType.LOW_RATING,
                "rating": avg_rating,
                "review_count": len(ratings),
                "source": "glassdoor",
                "company": company_name,
            }

        return None

    async def detect_chaos_indicators(
        self,
        company_name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Detect chaos indicators in reviews (e.g., "no process", "chaos", "disorganized").
        
        Returns:
            Signal data if chaos indicators found, None otherwise
        """
        reviews = await self.get_company_reviews(company_name, limit=100)

        chaos_keywords = [
            "no process",
            "chaos",
            "disorganized",
            "mess",
            "no structure",
            "confusion",
            "unorganized",
        ]

        chaos_reviews = []
        for review in reviews:
            content = review.get("content", "").lower()
            if any(keyword in content for keyword in chaos_keywords):
                chaos_reviews.append(review)

        # If more than 20% of reviews mention chaos
        if reviews and len(chaos_reviews) / len(reviews) > 0.2:
            return {
                "signal_type": SignalType.NEGATIVE_REVIEW_SPIKE,
                "indicator": "chaos_hiring",
                "chaos_review_count": len(chaos_reviews),
                "total_reviews": len(reviews),
                "source": "glassdoor",
                "company": company_name,
            }

        return None
