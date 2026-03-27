"""
Job board scraping service for signal detection.
Currently supports Indeed and generic job board patterns.
"""
from typing import Any, Dict, List, Optional

import httpx
from bs4 import BeautifulSoup

from src.core.config import get_settings
from src.core.exceptions import ExternalAPIException
from src.signal_scanner.services.signal_normalizer import normalize_signal

settings = get_settings()


class JobBoardScraper:
    """Scrapes job postings from various job boards."""

    def __init__(self):
        self.session = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
        )

    async def search_indeed_jobs(
        self,
        query: str,
        location: str = "",
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search Indeed for job postings.
        
        Note: This is a simplified implementation. Production use
        would require proper Indeed API integration or more robust scraping.
        """
        # Indeed job search URL parameters
        params = {
            "q": query,
            "l": location,
            "limit": limit,
            "sort": "date",
        }

        try:
            # Note: In production, use official API or proper scraping infrastructure
            response = await self.session.get(
                "https://www.indeed.com/jobs",
                params=params,
            )
            response.raise_for_status()
            
            return self._parse_indeed_results(response.text)

        except httpx.HTTPStatusError as e:
            raise ExternalAPIException(
                "Indeed",
                f"HTTP {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise ExternalAPIException("Indeed", str(e))

    def _parse_indeed_results(self, html: str) -> List[Dict[str, Any]]:
        """Parse Indeed job listings from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        # Indeed job cards typically have this class structure
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards:
            title_elem = card.find("h2", class_="jobTitle")
            company_elem = card.find("span", class_="companyName")
            summary_elem = card.find("div", class_="job-snippet")

            if title_elem:
                jobs.append({
                    "source": "job_board",
                    "title": title_elem.get_text(strip=True),
                    "company": company_elem.get_text(strip=True) if company_elem else None,
                    "content": summary_elem.get_text(strip=True) if summary_elem else "",
                })

        return jobs

    async def search_finance_roles(
        self,
        location: str = "",
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Search for finance leadership roles."""
        queries = [
            "VP Finance CFO",
            "Financial Controller",
            "FP&A Director",
            "Head of Finance",
        ]

        all_jobs = []
        for query in queries:
            jobs = await self.search_indeed_jobs(query, location, limit)
            all_jobs.extend(jobs)

        return all_jobs

    async def search_operations_roles(
        self,
        location: str = "",
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Search for operations leadership roles."""
        queries = [
            "VP Operations COO",
            "Head of Operations",
            "Operations Director",
        ]

        all_jobs = []
        for query in queries:
            jobs = await self.search_indeed_jobs(query, location, limit)
            all_jobs.extend(jobs)

        return all_jobs

    async def ingest_signals(self) -> List[Dict[str, Any]]:
        """
        Ingest signals from job boards.
        
        Returns:
            List of normalized job signals
        """
        all_jobs = []

        # Search for finance and operations roles
        finance_jobs = await self.search_finance_roles()
        operations_jobs = await self.search_operations_roles()

        all_jobs.extend(finance_jobs)
        all_jobs.extend(operations_jobs)

        # Normalize all jobs
        normalized = []
        for job in all_jobs:
            normalized_signal = normalize_signal(job)
            if normalized_signal.get("signal_type"):
                normalized.append(normalized_signal)

        return normalized

    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()
