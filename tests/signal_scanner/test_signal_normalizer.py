"""
Test examples for signal normalizer.
"""
import pytest
from src.signal_scanner.models.signal import SignalSource, SignalType
from src.signal_scanner.services.signal_normalizer import (
    extract_company_name,
    normalize_signal,
)


def test_normalize_news_signal_funding():
    """Test normalization of funding announcement from news."""
    raw_signal = {
        "source": "news",
        "title": "TechCorp raises $50M Series B to expand operations",
        "content": "TechCorp announced today that it has raised $50 million in Series B funding...",
        "url": "https://example.com/news/123",
    }
    
    result = normalize_signal(raw_signal)
    
    assert result["source"] == "news_api"
    assert result["signal_type"] == SignalType.FUNDING_ANNOUNCED


def test_normalize_job_signal_finance():
    """Test normalization of finance leadership job posting."""
    raw_signal = {
        "source": "job_board",
        "title": "We are hiring: VP of Finance",
        "company": "TechCorp",
        "content": "Looking for an experienced VP of Finance to lead our financial planning...",
    }
    
    result = normalize_signal(raw_signal)
    
    assert result["source"] == "job_board"
    assert result["signal_type"] == SignalType.HIRING_FINANCE_LEAD
    assert result["title"] == "We are hiring: VP of Finance"


def test_normalize_job_signal_operations():
    """Test normalization of operations leadership job posting."""
    raw_signal = {
        "source": "indeed",
        "title": "Head of Operations - SaaS Startup",
        "company": "GrowthCo",
    }
    
    result = normalize_signal(raw_signal)
    
    assert result["signal_type"] == SignalType.HIRING_OPS_LEAD


def test_extract_company_name_from_title():
    """Test extracting company name from signal title."""
    raw_signal = {
        "title": "StartupX raises $10M to revolutionize fintech",
    }
    
    company = extract_company_name(raw_signal)
    
    assert company == "StartupX"


def test_extract_company_name_explicit():
    """Test extracting company name from explicit field."""
    raw_signal = {
        "title": "Some generic job posting",
        "company": "SpecificCorp",
    }
    
    company = extract_company_name(raw_signal)
    
    assert company == "SpecificCorp"
