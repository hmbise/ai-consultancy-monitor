"""
Celery worker configuration for background tasks.
"""
from celery import Celery

from src.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "ai_consultancy_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "src.signal_scanner.tasks",
        "src.org_diagnosis_ai.tasks",
        "src.opportunity_engine.tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task to verify Celery is working."""
    print(f"Request: {self.request!r}")
    return "Celery is working!"
