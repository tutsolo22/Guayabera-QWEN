"""
Task Service: Celery background tasks for heavy operations
Handles long-running operations in the background
"""

from celery import Celery
from app.core.config import settings
from typing import Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Celery instance
celery_app = Celery(
    'task_service',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Mexico_City',  # Adjust to your timezone
    enable_utc=False,
    result_expires=3600,  # Results expire after 1 hour
    worker_prefetch_multiplier=1,  # Process one task at a time per worker
    task_acks_late=True,  # Acknowledge tasks after completion
    worker_max_tasks_per_child=100,  # Restart workers after 100 tasks
)

# Import tasks modules after creating the Celery instance to avoid circular imports
from app.tasks import invoice_tasks, payroll_tasks, email_tasks


def create_task_wrapper(task_func, task_name: str):
    """
    Wrapper to create a task with error handling
    :param task_func: The task function to wrap
    :param task_name: Name of the task
    :return: Wrapped task function
    """
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Starting task: {task_name}")
            result = task_func(*args, **kwargs)
            logger.info(f"Completed task: {task_name}")
            return result
        except Exception as e:
            logger.error(f"Error in task {task_name}: {str(e)}")
            raise e
    
    return wrapper


# Define some common background tasks

@celery_app.task(name="process_heavy_report")
def process_heavy_report(report_type: str, filters: dict) -> dict:
    """
    Process a heavy report in the background
    :param report_type: Type of report to generate
    :param filters: Filters to apply to the report
    :return: Report processing result
    """
    # Simulate report processing
    import time
    time.sleep(5)  # Simulate heavy processing
    
    return {
        "status": "completed",
        "report_type": report_type,
        "filters": filters,
        "processed_at": "2026-04-27T22:30:00Z",
        "file_path": f"/reports/{report_type}_report.pdf"
    }


@celery_app.task(name="generate_monthly_invoices")
def generate_monthly_invoices(empresa_id: str, month: int, year: int) -> dict:
    """
    Generate monthly invoices for all clients
    :param empresa_id: ID of the company
    :param month: Month to generate invoices for
    :param year: Year to generate invoices for
    :return: Generation result
    """
    # Simulate invoice generation
    import time
    time.sleep(10)  # Simulate heavy processing
    
    return {
        "status": "completed",
        "empresa_id": empresa_id,
        "month": month,
        "year": year,
        "generated_count": 150,
        "processed_at": "2026-04-27T22:40:00Z"
    }


@celery_app.task(name="sync_inventory")
def sync_inventory(warehouse_id: str) -> dict:
    """
    Synchronize inventory levels
    :param warehouse_id: ID of the warehouse to sync
    :return: Sync result
    """
    # Simulate inventory sync
    import time
    time.sleep(7)  # Simulate heavy processing
    
    return {
        "status": "completed",
        "warehouse_id": warehouse_id,
        "updated_products": 250,
        "synced_at": "2026-04-27T22:45:00Z"
    }


@celery_app.task(name="backup_database")
def backup_database() -> dict:
    """
    Backup the database
    :return: Backup result
    """
    # Simulate database backup
    import time
    time.sleep(30)  # Simulate heavy processing
    
    return {
        "status": "completed",
        "backup_file": "/backups/db_backup_20260427.sql",
        "backup_size": "1.2GB",
        "completed_at": "2026-04-27T23:00:00Z"
    }


# Additional utility functions

def send_task_to_queue(task_name: str, *args, **kwargs):
    """
    Send a task to the queue
    :param task_name: Name of the task to execute
    :param args: Arguments to pass to the task
    :param kwargs: Keyword arguments to pass to the task
    :return: AsyncResult object
    """
    return celery_app.send_task(task_name, args=args, kwargs=kwargs)


def get_task_status(task_id: str) -> dict:
    """
    Get the status of a task
    :param task_id: ID of the task
    :return: Task status information
    """
    result = celery_app.AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "info": result.info if hasattr(result, 'info') else None
    }