# AI Consultancy Monitor

AI-powered signal detection and consulting opportunity engine. Part of the AI CTO OS ecosystem.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-00a393.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

AI Consultancy Monitor tracks public signals from companies (hiring patterns, funding announcements, leadership changes) and uses AI to identify consulting opportunities. Follows the [AI CTO OS MANIFEST](link-to-manifest) principles: standalone-first, optional integrations, MVP within 14 days.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Signal Scanner │────▶│ Org Diagnosis AI │────▶│ Opportunity Eng. │
│  (News, Jobs)   │     │    (Groq LLM)    │     │  (Scoring, Fit)  │
└─────────────────┘     └──────────────────┘     └──────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Neon PostgreSQL (ai_consultancy schema)     │
│                    Redis (Cache + Celery)                        │
│                    Elasticsearch (Signal Index)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Stack

| Component | Technology |
|-----------|------------|
| **API** | FastAPI + Uvicorn |
| **Database** | Neon Serverless PostgreSQL (ai-foundry-products project, `ai_consultancy` schema) |
| **Cache/Queue** | Redis |
| **Search** | Elasticsearch 8.x |
| **AI/LLM** | Groq API (configurable model) |
| **Async** | Celery + asyncpg |
| **Frontend** | Next.js (separate repo) |

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for Redis/Elasticsearch)
- Neon PostgreSQL account
- Groq API key

### Setup

```bash
# Clone repository
git clone <repo-url>
cd ai-consultancy-monitor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL (Neon connection string)
# - GROQ_API_KEY
# - NEWS_API_KEY (optional)

# Start supporting services
docker-compose up -d redis elasticsearch

# Run database migrations (auto-creates schema on first run)
python -c "import asyncio; from src.core.database import init_db; asyncio.run(init_db())"

# Start API
uvicorn src.api.main:app --reload

# Start worker (separate terminal)
celery -A src.worker worker -l info
```

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/docs
```

## Environment Variables

```env
# Database (Neon)
DATABASE_URL=postgresql://user:pass@neon-host.neon.tech/db?sslmode=require

# Redis
REDIS_URL=redis://localhost:6379/0

# AI (Groq)
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.1-70b-versatile

# Data Sources (optional)
NEWS_API_KEY=...

# App
APP_ENV=development
APP_DEBUG=true
SECRET_KEY=change-me-in-production
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/signals` | List signals |
| GET | `/api/v1/companies` | List companies |
| POST | `/api/v1/companies/scan` | Scan new company |
| POST | `/api/v1/diagnosis` | Create diagnosis |
| GET | `/api/v1/diagnosis/types` | List diagnosis types |
| GET | `/api/v1/opportunities` | List opportunities |
| GET | `/api/v1/opportunities/ranking` | Ranked opportunities |
| GET | `/api/v1/engagement/angles/{id}` | Generate engagement angles |
| POST | `/api/v1/engagement/emails/{id}` | Generate outreach email |

## Project Structure

```
ai-consultancy-monitor/
├── src/
│   ├── api/main.py              # FastAPI entry point
│   ├── core/                    # Config, database, exceptions, SQLAlchemy models
│   ├── signal_scanner/          # Signal detection (news, jobs, glassdoor)
│   ├── org_diagnosis_ai/        # LLM-based diagnosis (Groq)
│   ├── opportunity_engine/      # Opportunity scoring & matching
│   ├── engagement_generator/    # Outreach angles & email templates
│   └── worker.py                # Celery configuration
├── tests/                       # pytest test suite
├── docker-compose.yml           # Redis + Elasticsearch only
├── Dockerfile
└── pyproject.toml
```

## Background Tasks

Celery handles periodic and async tasks:

```bash
# Run worker
celery -A src.worker worker -l info

# Run scheduler (for periodic tasks)
celery -A src.worker beat -l info
```

**Periodic Tasks:**
- `ingest_news_batch`: Every 6 hours - fetch news signals
- `detect_changes_batch`: Every hour - run change detection
- `refresh_expired_diagnoses`: Daily - re-diagnose expired entries

## Development

```bash
# Run tests
pytest

# Code formatting
black src tests
ruff check src tests

# Type checking
mypy src
```

## Architecture Decisions

### Neon Schema Configuration

- **Project:** `ai-foundry-products`
- **Schema:** `ai_consultancy`
- **Rationale:** Part of products portfolio, standalone schema per MANIFEST section 4.1

### LLM Provider

- **Primary:** Groq (fast, cost-effective)
- **Model:** Configurable (default: `llama-3.1-70b-versatile`)
- **Fallback:** Manual retry logic with tenacity

### Standalone-First Design

- No hard dependencies on other AI CTO OS products
- Optional integration: Can export insights to AI CTO OS via API
- Self-contained database schema

## Signal Types

Detected signal patterns:

| Category | Signals |
|----------|---------|
| **Hiring** | Finance Lead, FP&A, Controller, Ops Lead, Data Lead |
| **Funding** | Announcement, Stage Change |
| **Operational** | Leadership Change, Office Expansion, New Product |
| **Reviews** | Negative Spike, Low Rating |
| **Patterns** | Rapid Hiring, Chaos Hiring |

## Diagnosis Types

AI-generated organizational diagnoses:

| Type | Indicators |
|------|-----------|
| `finance_immaturity` | Hiring finance + reactive processes |
| `operational_chaos` | Manual processes + growth without structure |
| `governance_gap` | Centralized decisions + no board |
| `data_blindness` | No dashboards + feeling-based decisions |
| `growth_scaling` | Fast growth + missing infrastructure |
| `leadership_gap` | Executive departures + hiring gaps |

## License

MIT - See LICENSE file

## Ecosystem

Part of [AI CTO OS](link-to-ecosystem). Follows the [MANIFEST](link-to-manifest) architecture principles:
- Standalone-first
- Optional integrations
- 14-day MVP cycles
- Visual connection graphs (planned)
