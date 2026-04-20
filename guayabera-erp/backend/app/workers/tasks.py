"""
Celery tasks for automatic accounting
"""

from celery import Task
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta
from uuid import UUID

from app.workers.celery_app import celery_app
from app.core.database import SessionLocal
from app.services.automatic_accounting import AutomaticAccountingService
from app.models.finance import AsientoContable, PolizaContable

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task with database session management"""
    _db = None
    
    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db
    
    def after_return(self, *args, **kwargs):
        """Close database session after task completes"""
        if self._db is not None:
            self._db.close()
            self._db = None


@celery_app.task(
    bind=True,
    base=DatabaseTask,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
    acks_late=True
)
def process_pending_accounting_entries(self):
    """
    Process all pending accounting entries
    
    This task runs every 5 minutes to process entries that failed initially
    or are waiting for external dependencies
    """
    logger.info("🔄 Processing pending accounting entries...")
    
    try:
        service = AutomaticAccountingService(self.db)
        
        # Get pending entries (created in last 24 hours)
        pending_entries = (
            self.db.query(AsientoContable)
            .filter(
                AsientoContable.estado == "pendiente",
                AsientoContable.created_at >= datetime.utcnow() - timedelta(hours=24)
            )
            .all()
        )
        
        if not pending_entries:
            logger.info("✅ No pending entries to process")
            return {"processed": 0, "message": "No pending entries"}
        
        processed_count = 0
        failed_count = 0
        
        for entry in pending_entries:
            try:
                # In production, you would reconstruct the movements from
                # datos_origen and call create_automatic_entry
                # For now, we'll just mark them as processed
                
                entry.estado = "procesado"
                entry.fecha_procesado = datetime.utcnow()
                self.db.commit()
                
                processed_count += 1
                logger.info(f"✅ Processed entry: {entry.referencia}")
                
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Failed processing entry {entry.referencia}: {str(e)}")
        
        result = {
            "processed": processed_count,
            "failed": failed_count,
            "total": len(pending_entries)
        }
        
        logger.info(f"📊 Entries processing complete: {result}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in process_pending_accounting_entries: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@celery_app.task(
    bind=True,
    base=DatabaseTask,
    max_retries=2,
    default_retry_delay=300  # 5 minutes
)
def retry_failed_accounting_entries(self):
    """
    Retry failed accounting entries
    
    This task runs every hour to retry entries that failed processing
    Maximum 3 retries before manual intervention is required
    """
    logger.info("🔄 Retrying failed accounting entries...")
    
    try:
        # Get failed entries with less than 3 retries
        failed_entries = (
            self.db.query(AsientoContable)
            .filter(
                AsientoContable.estado == "fallido",
                AsientoContable.created_at >= datetime.utcnow() - timedelta(days=7)
            )
            .all()
        )
        
        if not failed_entries:
            logger.info("✅ No failed entries to retry")
            return {"retried": 0, "message": "No failed entries to retry"}
        
        retried_count = 0
        
        for entry in failed_entries:
            try:
                # Check error count in errores JSONB
                errores = entry.errores or {}
                retry_count = errores.get("retry_count", 0)
                
                if retry_count >= 3:
                    logger.warning(
                        f"⚠️ Entry {entry.referencia} exceeded max retries, "
                        f"requires manual intervention"
                    )
                    entry.estado = "requiere_intervencion"
                    self.db.commit()
                    continue
                
                # Mark for retry
                entry.estado = "pendiente"
                entry.errores = {
                    **errores,
                    "retry_count": retry_count + 1,
                    "last_retry": datetime.utcnow().isoformat()
                }
                self.db.commit()
                
                retried_count += 1
                logger.info(f"🔄 Retried entry: {entry.referencia} (attempt {retry_count + 1})")
                
            except Exception as e:
                logger.error(f"❌ Error retrying entry {entry.referencia}: {str(e)}")
        
        result = {
            "retried": retried_count,
            "total": len(failed_entries)
        }
        
        logger.info(f"📊 Retry complete: {result}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in retry_failed_accounting_entries: {str(e)}")
        raise self.retry(exc=e, countdown=300)


@celery_app.task(
    bind=True,
    base=DatabaseTask
)
def generate_daily_summary(self):
    """
    Generate daily summary of automatic accounting entries
    
    This task runs daily at 6 PM to provide a summary report
    """
    logger.info("📊 Generating daily accounting summary...")
    
    try:
        # Count entries by status for today
        today = datetime.utcnow().date()
        
        total_entries = (
            self.db.query(AsientoContable)
            .filter(
                AsientoContable.created_at >= datetime.combine(today, datetime.min.time()),
                AsientoContable.created_at < datetime.combine(today, datetime.max.time())
            )
            .count()
        )
        
        processed_entries = (
            self.db.query(AsientoContable)
            .filter(
                AsientoContable.estado == "procesado",
                AsientoContable.created_at >= datetime.combine(today, datetime.min.time())
            )
            .count()
        )
        
        failed_entries = (
            self.db.query(AsientoContable)
            .filter(
                AsientoContable.estado == "fallido",
                AsientoContable.created_at >= datetime.combine(today, datetime.min.time())
            )
            .count()
        )
        
        # Count entries by module
        entries_by_module = {}
        modules = ["compras", "ventas", "nomina", "produccion"]
        
        for module in modules:
            count = (
                self.db.query(AsientoContable)
                .filter(
                    AsientoContable.modulo_origen == module,
                    AsientoContable.created_at >= datetime.combine(today, datetime.min.time())
                )
                .count()
            )
            entries_by_module[module] = count
        
        summary = {
            "date": today.isoformat(),
            "total_entries": total_entries,
            "processed_entries": processed_entries,
            "failed_entries": failed_entries,
            "success_rate": f"{(processed_entries / total_entries * 100) if total_entries > 0 else 0:.1f}%",
            "entries_by_module": entries_by_module
        }
        
        logger.info(f"📊 Daily summary: {summary}")
        
        # In production, you would send this to:
        # - Email notification
        # - Slack/Discord webhook
        # - Dashboard API
        # - PDF report
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Error generating daily summary: {str(e)}")
        raise


@celery_app.task(
    bind=True,
    base=DatabaseTask,
    max_retries=1,
    default_retry_delay=30
)
def create_automatic_entry_async(
    self,
    modulo_origen: str,
    entidad_origen: str,
    entidad_id: str,
    movimientos: list,
    fecha: str = None,
    descripcion: str = None,
    referencia: str = None,
    datos_origen: dict = None
):
    """
    Create automatic accounting entry asynchronously
    
    Use this task when you want to create entries without blocking the main flow
    """
    logger.info(f"🔄 Creating automatic entry async: {modulo_origen}/{entidad_origen}")
    
    try:
        from app.services.automatic_accounting import AutomaticAccountingService
        from datetime import date
        
        service = AutomaticAccountingService(self.db)
        
        # Parse date if provided
        fecha_obj = None
        if fecha:
            fecha_obj = date.fromisoformat(fecha)
        
        # Parse UUID
        from uuid import UUID
        entidad_id_obj = UUID(entidad_id) if isinstance(entidad_id, str) else entidad_id
        
        # Create entry
        asiento = service.create_automatic_entry(
            modulo_origen=modulo_origen,
            entidad_origen=entidad_origen,
            entidad_id=entidad_id_obj,
            movimientos=movimientos,
            fecha=fecha_obj,
            descripcion=descripcion,
            referencia=referencia,
            datos_origen=datos_origen
        )
        
        logger.info(f"✅ Automatic entry created: {asiento.id}")
        return {"asiento_id": str(asiento.id), "status": "success"}
        
    except Exception as e:
        logger.error(f"❌ Error in create_automatic_entry_async: {str(e)}")
        raise self.retry(exc=e, countdown=30)
