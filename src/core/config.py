from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    secret_key: str = "change-me-in-production"

    # Database - Neon (Serverless PostgreSQL)
    database_url: str = Field(..., description="Neon PostgreSQL connection string")
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Elasticsearch
    elasticsearch_url: str = "http://localhost:9200"

    # AI/LLM - Groq
    groq_api_key: str = Field(..., description="Groq API key")
    groq_model: str = "llama-3.1-70b-versatile"

    # Data Sources
    news_api_key: Optional[str] = None
    crunchbase_api_key: Optional[str] = None
    glassdoor_api_key: Optional[str] = None

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # Feature Flags
    enable_email_enrichment: bool = False
    enable_linkedin_outreach: bool = False

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


@lru_cache
def get_settings() -> Settings:
    return Settings()
