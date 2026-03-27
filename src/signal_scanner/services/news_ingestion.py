import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx

from src.core.config import get_settings
from src.core.exceptions import ExternalAPIException
from src.signal_scanner.models.signal import SignalSource
from src.signal_scanner.services.signal_normalizer import (
    extract_company_name,
    normalize_signal,
)

settings = get_settings()

NEWS_API_URL = "https://newsapi.org/v2/everything"


class NewsAPIIngestion:
    """Ingests signals from NewsAPI."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.news_api_key
        if not self.api_key:
            raise ValueError("News API key is required")

    async def search_funding_news(
        self,
        query: str = "startup funding investment series",
        days_back: int = 7,
        language: str = "en",
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Search for funding-related news articles.
        
        Args:
            query: Search query string
            days_back: How many days back to search
            language: Article language code
            page_size: Number of results per page
            
        Returns:
            List of raw article data
        """
        from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        params = {
            "q": query,
            "from": from_date,
            "language": language,
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": self.api_key,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(NEWS_API_URL, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                if data.get("status") != "ok":
                    raise ExternalAPIException(
                        "NewsAPI",
                        f"API error: {data.get('message', 'Unknown error')}"
                    )

                return data.get("articles", [])

            except httpx.HTTPStatusError as e:
                raise ExternalAPIException(
                    "NewsAPI",
                    f"HTTP {e.response.status_code}: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise ExternalAPIException("NewsAPI", str(e))

    async def search_leadership_changes(
        self,
        company_name: Optional[str] = None,
        days_back: int = 30,
    ) -> List[Dict[str, Any]]:
        """Search for leadership change announcements."""
        query = "CEO appointment departure executive leadership"
        if company_name:
            query = f"{company_name} {query}"

        return await self.search_funding_news(
            query=query,
            days_back=days_back,
        )

    async def ingest_signals(
        self,
        signal_types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Ingest and normalize signals from NewsAPI.
        
        Returns:
            List of normalized signal dictionaries
        """
        articles = await self.search_funding_news()
        normalized = []

        for article in articles:
            raw_signal = {
                "source": "news_api",
                "title": article.get("title", ""),
                "content": article.get("description", "") or article.get("content", ""),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "author": article.get("author"),
                "source_name": article.get("source", {}).get("name"),
            }

            # Add extracted company name if possible
            company_name = extract_company_name(raw_signal)
            if company_name:
                raw_signal["company"] = company_name

            normalized_signal = normalize_signal(raw_signal)
            
            # Only include if we detected a signal type
            if normalized_signal.get("signal_type"):
                normalized.append(normalized_signal)

        return normalized
