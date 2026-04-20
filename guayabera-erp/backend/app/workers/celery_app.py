"""
Celery configuration and tasks for automatic accounting entries
"""

from celery import Celery
from celery.schedules import crontab
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Celery application
celery_app = Celery(
    "guayabera-erp",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.workers.tasks.process_pending_accounting_entries": {
            "queue": "accounting"
        },
        "app.workers.tasks.retry_failed_accounting_entries": {
            "queue": "accounting"
        },
    },
    
    # Queue definitions
    task_queues={
        "accounting": {
            "exchange": "accounting",
            "routing_key": "accounting",
        },
    },
    
    # Beat schedule (periodic tasks)
    beat_schedule={
        # Process pending accounting entries every 5 minutes
        "process-pending-entries-every-5-minutes": {
            "task": "app.workers.tasks.process_pending_accounting_entries",
            "schedule": 300.0,  # 5 minutes
            "options": {"queue": "accounting"},
        },
        
        # Retry failed entries every hour
        "retry-failed-entries-every-hour": {
            "task": "app.workers.tasks.retry_failed_accounting_entries",
            "schedule": 3600.0,  # 1 hour
            "options": {"queue": "accounting"},
        },
        
        # Daily summary report at 6 PM
        "daily-accounting-summary": {
            "task": "app.workers.tasks.generate_daily_summary",
            "schedule": crontab(hour=18, minute=0),  # 6:00 PM
            "options": {"queue": "accounting"},
        },
    },
    
    # Retry policy
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # Timezone
    timezone="America/Merida",
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks after Celery configuration"""
    logger.info("✅ Periodic accounting tasks configured")
