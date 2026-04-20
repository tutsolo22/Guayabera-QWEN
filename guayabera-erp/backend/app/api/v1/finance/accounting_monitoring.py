"""
API routes for monitoring automatic accounting entries
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.services.automatic_accounting import AutomaticAccountingService
from app.schemas.finance import AsientoContableResponse

router = APIRouter()


@router.get("/automaticos/monitoreo")
async def monitorear_asientos_automaticos(
    modulo_origen: str = None,
    entidad_id: UUID = None,
    estado: str = None,
    db: Session = Depends(get_db)
):
    """
    Monitor automatic accounting entries
    
    Returns list of accounting entries with filters:
    - modulo_origen: compras, ventas, nomina, produccion
    - entidad_id: Source entity UUID
    - estado: pendiente, procesado, fallido, requiere_intervencion
    """
    service = AutomaticAccountingService(db)
    entries = service.get_entry_status(
        modulo_origen=modulo_origen,
        entidad_id=entidad_id,
        estado=estado
    )
    
    return {
        "total": len(entries),
        "entries": [
            {
                "id": str(entry.id),
                "modulo_origen": entry.modulo_origen,
                "entidad_origen": entry.entidad_origen,
                "entidad_id": str(entry.entidad_id),
                "referencia": entry.referencia,
                "estado": entry.estado,
                "fecha_procesado": entry.fecha_procesado,
                "errores": entry.errores,
                "created_at": entry.created_at
            }
            for entry in entries
        ]
    }


@router.get("/automaticos/estadisticas")
async def estadisticas_asientos_automaticos(
    db: Session = Depends(get_db)
):
    """
    Get statistics of automatic accounting entries
    
    Returns summary statistics for monitoring dashboard
    """
    from app.models.finance import AsientoContable
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Total entries by status
    status_counts = (
        db.query(AsientoContable.estado, func.count(AsientoContable.id))
        .group_by(AsientoContable.estado)
        .all()
    )
    
    # Total entries by module
    module_counts = (
        db.query(AsientoContable.modulo_origen, func.count(AsientoContable.id))
        .group_by(AsientoContable.modulo_origen)
        .all()
    )
    
    # Entries in last 24 hours
    last_24h = (
        db.query(func.count(AsientoContable.id))
        .filter(AsientoContable.created_at >= datetime.utcnow() - timedelta(hours=24))
        .scalar()
    )
    
    # Failed entries requiring intervention
    intervention_count = (
        db.query(func.count(AsientoContable.id))
        .filter(AsientoContable.estado == "requiere_intervencion")
        .scalar()
    )
    
    return {
        "by_status": {status: count for status, count in status_counts},
        "by_module": {module: count for module, count in module_counts},
        "last_24h": last_24h,
        "requires_intervention": intervention_count,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/automaticos/procesar-pendientes")
async def procesar_pendientes_manualmente(
    db: Session = Depends(get_db)
):
    """
    Manually trigger processing of pending accounting entries
    
    Use this for testing or manual intervention
    """
    service = AutomaticAccountingService(db)
    processed = service.process_pending_entries()
    
    return {
        "message": f"Se procesaron {processed} entradas pendientes",
        "processed": processed
    }


@router.get("/automaticos/{asiento_id}")
async def obtener_asiento_automatico(
    asiento_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific automatic accounting entry
    """
    from app.models.finance import AsientoContable
    
    entry = (
        db.query(AsientoContable)
        .filter(AsientoContable.id == asiento_id)
        .first()
    )
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asiento automático no encontrado"
        )
    
    # Get related policy if exists
    poliza = None
    if entry.poliza_id:
        from app.models.finance import PolizaContable
        poliza = (
            db.query(PolizaContable)
            .filter(PolizaContable.id == entry.poliza_id)
            .first()
        )
    
    return {
        "id": str(entry.id),
        "modulo_origen": entry.modulo_origen,
        "entidad_origen": entry.entidad_origen,
        "entidad_id": str(entry.entidad_id),
        "referencia": entry.referencia,
        "estado": entry.estado,
        "datos_origen": entry.datos_origen,
        "errores": entry.errores,
        "poliza_id": str(entry.poliza_id) if entry.poliza_id else None,
        "poliza_numero": poliza.numero if poliza else None,
        "fecha_procesado": entry.fecha_procesado,
        "creado_por": entry.creado_por,
        "created_at": entry.created_at,
        "updated_at": entry.updated_at
    }
