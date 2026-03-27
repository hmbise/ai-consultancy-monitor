"""
FastAPI application entry point.
Aggregates all routers and configures middleware.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import get_settings
from src.core.database import init_db
from src.core.exceptions import AIConsultancyMonitorException
from src.engagement_generator.routers import engagement
from src.opportunity_engine.routers import opportunities
from src.org_diagnosis_ai.routers import diagnosis
from src.signal_scanner.routers import companies, signals

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting AI Consultancy Monitor...")
    await init_db()
    logger.info("Database initialized (schema: ai_consultancy)")
    yield
    # Shutdown
    logger.info("Shutting down AI Consultancy Monitor...")


app = FastAPI(
    title="AI Consultancy Monitor",
    description="AI-powered signal detection and consulting opportunity engine",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(AIConsultancyMonitorException)
async def handle_app_exception(request: Request, exc: AIConsultancyMonitorException):
    """Handle application-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "status_code": exc.status_code,
        },
    )


# Include routers
app.include_router(signals.router)
app.include_router(companies.router)
app.include_router(diagnosis.router)
app.include_router(opportunities.router)
app.include_router(engagement.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "schema": "ai_consultancy",
        "database": "neon (ai-foundry-products)",
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "AI Consultancy Monitor",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }
