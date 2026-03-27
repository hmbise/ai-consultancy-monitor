import re
from typing import Any, Dict, Optional

from src.signal_scanner.models.signal import SignalSource, SignalType


# Pattern matching rules for signal detection
SIGNAL_PATTERNS: Dict[SignalType, Dict[str, Any]] = {
    SignalType.HIRING_FINANCE_LEAD: {
        "sources": [SignalSource.JOB_BOARD, SignalSource.LINKEDIN],
        "title_patterns": [
            r"(?i)(?:cfo|chief financial officer|vp finance|head of finance|director of finance|finance lead)",
        ],
    },
    SignalType.HIRING_FP_A: {
        "sources": [SignalSource.JOB_BOARD, SignalSource.LINKEDIN],
        "title_patterns": [
            r"(?i)(?:fp&a|financial planning|financial analyst|planning and analysis)",
        ],
    },
    SignalType.HIRING_CONTROLLER: {
        "sources": [SignalSource.JOB_BOARD, SignalSource.LINKEDIN],
        "title_patterns": [
            r"(?i)(?:controller|comptroller|accounting manager)",
        ],
    },
    SignalType.HIRING_OPS_LEAD: {
        "sources": [SignalSource.JOB_BOARD, SignalSource.LINKEDIN],
        "title_patterns": [
            r"(?i)(?:vp operations|head of ops|director of operations|operations lead|coo|chief operating officer)",
        ],
    },
    SignalType.HIRING_DATA_LEAD: {
        "sources": [SignalSource.JOB_BOARD, SignalSource.LINKEDIN],
        "title_patterns": [
            r"(?i)(?:data|analytics|business intelligence|bi lead|data director)",
        ],
    },
    SignalType.FUNDING_ANNOUNCED: {
        "sources": [SignalSource.NEWS_API, SignalSource.PRESS_RELEASE, SignalSource.CRUNCHBASE],
        "title_patterns": [
            r"(?i)(?:raises?|funding|series [a-f]|investment|backed|seed round)",
        ],
    },
    SignalType.LEADERSHIP_CHANGE: {
        "sources": [SignalSource.NEWS_API, SignalSource.PRESS_RELEASE, SignalSource.CRUNCHBASE],
        "title_patterns": [
            r"(?i)(?:new ceo|appoints?|exits?|depart|steps? down|leadership change|founder leaves?)",
        ],
    },
    SignalType.OFFICE_EXPANSION: {
        "sources": [SignalSource.NEWS_API, SignalSource.PRESS_RELEASE],
        "title_patterns": [
            r"(?i)(?:new office|expands?|opens? office|hiring in|new location|grows? team)",
        ],
    },
    SignalType.NEW_PRODUCT: {
        "sources": [SignalSource.NEWS_API, SignalSource.PRESS_RELEASE],
        "title_patterns": [
            r"(?i)(?:launches?|new product|new service|announces?|releases?|unveils?)",
        ],
    },
}


def normalize_signal(raw_signal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw signal from various sources into a standardized format.
    
    Args:
        raw_signal: Raw signal data from external source
        
    Returns:
        Normalized signal dictionary
    """
    source = _detect_source(raw_signal)
    signal_type = _detect_signal_type(raw_signal, source)
    
    return {
        "source": source.value,
        "signal_type": signal_type.value if signal_type else None,
        "title": raw_signal.get("title", ""),
        "content": raw_signal.get("content", raw_signal.get("description", "")),
        "url": raw_signal.get("url"),
        "raw_data": raw_signal,
    }


def _detect_source(raw_signal: Dict[str, Any]) -> SignalSource:
    """Detect the source of the raw signal."""
    source_str = raw_signal.get("source", "").lower()
    
    source_mapping = {
        "news": SignalSource.NEWS_API,
        "newsapi": SignalSource.NEWS_API,
        "job": SignalSource.JOB_BOARD,
        "job_board": SignalSource.JOB_BOARD,
        "indeed": SignalSource.JOB_BOARD,
        "linkedin": SignalSource.LINKEDIN,
        "glassdoor": SignalSource.GLASSDOOR,
        "crunchbase": SignalSource.CRUNCHBASE,
        "press": SignalSource.PRESS_RELEASE,
    }
    
    return source_mapping.get(source_str, SignalSource.NEWS_API)


def _detect_signal_type(
    raw_signal: Dict[str, Any], source: SignalSource
) -> Optional[SignalType]:
    """Detect the signal type based on patterns in the raw data."""
    title = raw_signal.get("title", "")
    content = raw_signal.get("content", "")
    text_to_search = f"{title} {content}"
    
    for signal_type, config in SIGNAL_PATTERNS.items():
        if source not in config["sources"]:
            continue
            
        for pattern in config["title_patterns"]:
            if re.search(pattern, text_to_search):
                return signal_type
    
    return None


def extract_company_name(raw_signal: Dict[str, Any]) -> Optional[str]:
    """Extract company name from raw signal data."""
    # Try common fields where company name might be stored
    company_fields = ["company", "company_name", "organization", "employer", "organization_name"]
    
    for field in company_fields:
        if field in raw_signal and raw_signal[field]:
            return str(raw_signal[field])
    
    # Try to extract from title using common patterns
    title = raw_signal.get("title", "")
    
    # Pattern: "Company X raises..." or "Company X hiring..."
    patterns = [
        r"^([A-Z][A-Za-z0-9\s]+)\s+(?:raises?|hiring|announces?|launches?)",
        r"(?:at|from|join|for)\s+([A-Z][A-Za-z0-9\s]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1).strip()
    
    return None
