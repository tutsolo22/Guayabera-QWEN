from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.reports import Reporte
from app.schemas.reports import (
    ReporteCreate, ReporteUpdate, ReporteResponse,
    ReporteRHCreate, ReporteRHUpdate, ReporteRHResponse,
    ReporteProduccionCreate, ReporteProduccionUpdate, ReporteProduccionResponse,
    ReporteVentasCreate, ReporteVentasUpdate, ReporteVentasResponse,
    ReporteInventarioCreate, ReporteInventarioUpdate, ReporteInventarioResponse,
    ReporteFinanzasCreate, ReporteFinanzasUpdate, ReporteFinanzasResponse,
    DashboardWidgetCreate, DashboardWidgetUpdate, DashboardWidgetResponse,
    ReportePersonalizadoCreate, ReportePersonalizadoUpdate, ReportePersonalizadoResponse,
    HistoricoReporteCreate, HistoricoReporteUpdate, HistoricoReporteResponse
)
from app.crud.reports import (
    create_reporte, get_reporte, get_reportes,
    update_reporte, delete_reporte,
    create_reporte_rh, get_reporte_rh, get_reportes_rh,
    update_reporte_rh, delete_reporte_rh,
    create_reporte_produccion, get_reporte_produccion, get_reportes_produccion,
    update_reporte_produccion, delete_reporte_produccion,
    create_reporte_ventas, get_reporte_ventas, get_reportes_ventas,
    update_reporte_ventas, delete_reporte_ventas,
    create_reporte_inventario, get_reporte_inventario, get_reportes_inventario,
    update_reporte_inventario, delete_reporte_inventario,
    create_reporte_finanzas, get_reporte_finanzas, get_reportes_finanzas,
    update_reporte_finanzas, delete_reporte_finanzas,
    create_dashboard_widget, get_dashboard_widget, get_dashboard_widgets,
    update_dashboard_widget, delete_dashboard_widget,
    create_reporte_personalizado, get_reporte_personalizado, get_reportes_personalizados,
    update_reporte_personalizado, delete_reporte_personalizado,
    create_historico_reporte, get_historico_reporte, get_historicos_by_reporte,
    update_historico_reporte
)

router = APIRouter()


# ============================================================================
# REPORTES GENERALES
# ============================================================================

@router.post("/", response_model=ReporteResponse)
def create_reporte_endpoint(
    reporte_data: ReporteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte(db, reporte_data)


@router.get("/{reporte_id}", response_model=ReporteResponse)
def get_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte = get_reporte(db, UUID(reporte_id))
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte


@router.get("/", response_model=List[ReporteResponse])
def get_reportes_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_reportes(db, skip, limit)


@router.put("/{reporte_id}", response_model=ReporteResponse)
def update_reporte_endpoint(
    reporte_id: str,
    reporte_data: ReporteUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte = update_reporte(db, UUID(reporte_id), reporte_data)
    if not updated_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return updated_reporte


@router.delete("/{reporte_id}")
def delete_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte(db, UUID(reporte_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": "Reporte eliminado exitosamente"}


# ============================================================================
# REPORTES ESPECÍFICOS DE RH
# ============================================================================

@router.post("/rh/", response_model=ReporteRHResponse)
def create_reporte_rh_endpoint(
    reporte_rh_data: ReporteRHCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_rh(db, reporte_rh_data)


@router.get("/rh/{reporte_rh_id}", response_model=ReporteRHResponse)
def get_reporte_rh_endpoint(
    reporte_rh_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte_rh = get_reporte_rh(db, UUID(reporte_rh_id))
    if not reporte_rh:
        raise HTTPException(status_code=404, detail="Reporte de RH no encontrado")
    return reporte_rh


@router.get("/rh/reporte/{reporte_id}", response_model=List[ReporteRHResponse])
def get_reportes_rh_by_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_reportes_rh_by_reporte(db, UUID(reporte_id))


@router.put("/rh/{reporte_rh_id}", response_model=ReporteRHResponse)
def update_reporte_rh_endpoint(
    reporte_rh_id: str,
    reporte_rh_data: ReporteRHUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte_rh = update_reporte_rh(db, UUID(reporte_rh_id), reporte_rh_data)
    if not updated_reporte_rh:
        raise HTTPException(status_code=404, detail="Reporte de RH no encontrado")
    return updated_reporte_rh


@router.delete("/rh/{reporte_rh_id}")
def delete_reporte_rh_endpoint(
    reporte_rh_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_rh(db, UUID(reporte_rh_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de RH no encontrado")
    return {"message": "Reporte de RH eliminado exitosamente"}


# ============================================================================
# REPORTES ESPECÍFICOS DE PRODUCCIÓN
# ============================================================================

@router.post("/produccion/", response_model=ReporteProduccionResponse)
def create_reporte_produccion_endpoint(
    reporte_prod_data: ReporteProduccionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_produccion(db, reporte_prod_data)


@router.get("/produccion/{reporte_prod_id}", response_model=ReporteProduccionResponse)
def get_reporte_produccion_endpoint(
    reporte_prod_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte_prod = get_reporte_produccion(db, UUID(reporte_prod_id))
    if not reporte_prod:
        raise HTTPException(status_code=404, detail="Reporte de Producción no encontrado")
    return reporte_prod


@router.get("/produccion/reporte/{reporte_id}", response_model=List[ReporteProduccionResponse])
def get_reportes_produccion_by_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_reportes_produccion_by_reporte(db, UUID(reporte_id))


@router.put("/produccion/{reporte_prod_id}", response_model=ReporteProduccionResponse)
def update_reporte_produccion_endpoint(
    reporte_prod_id: str,
    reporte_prod_data: ReporteProduccionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte_prod = update_reporte_produccion(db, UUID(reporte_prod_id), reporte_prod_data)
    if not updated_reporte_prod:
        raise HTTPException(status_code=404, detail="Reporte de Producción no encontrado")
    return updated_reporte_prod


@router.delete("/produccion/{reporte_prod_id}")
def delete_reporte_produccion_endpoint(
    reporte_prod_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_produccion(db, UUID(reporte_prod_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de Producción no encontrado")
    return {"message": "Reporte de Producción eliminado exitosamente"}


# ============================================================================
# REPORTES ESPECÍFICOS DE VENTAS
# ============================================================================

@router.post("/ventas/", response_model=ReporteVentasResponse)
def create_reporte_ventas_endpoint(
    reporte_venta_data: ReporteVentasCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_ventas(db, reporte_venta_data)


@router.get("/ventas/{reporte_venta_id}", response_model=ReporteVentasResponse)
def get_reporte_ventas_endpoint(
    reporte_venta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte_venta = get_reporte_ventas(db, UUID(reporte_venta_id))
    if not reporte_venta:
        raise HTTPException(status_code=404, detail="Reporte de Ventas no encontrado")
    return reporte_venta


@router.get("/ventas/reporte/{reporte_id}", response_model=List[ReporteVentasResponse])
def get_reportes_ventas_by_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_reportes_ventas_by_reporte(db, UUID(reporte_id))


@router.put("/ventas/{reporte_venta_id}", response_model=ReporteVentasResponse)
def update_reporte_ventas_endpoint(
    reporte_venta_id: str,
    reporte_venta_data: ReporteVentasUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte_venta = update_reporte_ventas(db, UUID(reporte_venta_id), reporte_venta_data)
    if not updated_reporte_venta:
        raise HTTPException(status_code=404, detail="Reporte de Ventas no encontrado")
    return updated_reporte_venta


@router.delete("/ventas/{reporte_venta_id}")
def delete_reporte_ventas_endpoint(
    reporte_venta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_ventas(db, UUID(reporte_venta_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de Ventas no encontrado")
    return {"message": "Reporte de Ventas eliminado exitosamente"}


# ============================================================================
# REPORTES ESPECÍFICOS DE INVENTARIO
# ============================================================================

@router.post("/inventario/", response_model=ReporteInventarioResponse)
def create_reporte_inventario_endpoint(
    reporte_inv_data: ReporteInventarioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_inventario(db, reporte_inv_data)


@router.get("/inventario/{reporte_inv_id}", response_model=ReporteInventarioResponse)
def get_reporte_inventario_endpoint(
    reporte_inv_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte_inv = get_reporte_inventario(db, UUID(reporte_inv_id))
    if not reporte_inv:
        raise HTTPException(status_code=404, detail="Reporte de Inventario no encontrado")
    return reporte_inv


@router.get("/inventario/reporte/{reporte_id}", response_model=List[ReporteInventarioResponse])
def get_reportes_inventario_by_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_reportes_inventario_by_reporte(db, UUID(reporte_id))


@router.put("/inventario/{reporte_inv_id}", response_model=ReporteInventarioResponse)
def update_reporte_inventario_endpoint(
    reporte_inv_id: str,
    reporte_inv_data: ReporteInventarioUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte_inv = update_reporte_inventario(db, UUID(reporte_inv_id), reporte_inv_data)
    if not updated_reporte_inv:
        raise HTTPException(status_code=404, detail="Reporte de Inventario no encontrado")
    return updated_reporte_inv


@router.delete("/inventario/{reporte_inv_id}")
def delete_reporte_inventario_endpoint(
    reporte_inv_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_inventario(db, UUID(reporte_inv_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de Inventario no encontrado")
    return {"message": "Reporte de Inventario eliminado exitosamente"}


# ============================================================================
# REPORTES ESPECÍFICOS DE FINANZAS
# ============================================================================

@router.post("/finanzas/", response_model=ReporteFinanzasResponse)
def create_reporte_finanzas_endpoint(
    reporte_fin_data: ReporteFinanzasCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_finanzas(db, reporte_fin_data)


@router.get("/finanzas/{reporte_fin_id}", response_model=ReporteFinanzasResponse)
def get_reporte_finanzas_endpoint(
    reporte_fin_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte_fin = get_reporte_finanzas(db, UUID(reporte_fin_id))
    if not reporte_fin:
        raise HTTPException(status_code=404, detail="Reporte de Finanzas no encontrado")
    return reporte_fin


@router.get("/finanzas/reporte/{reporte_id}", response_model=List[ReporteFinanzasResponse])
def get_reportes_finanzas_by_reporte_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_reportes_finanzas_by_reporte(db, UUID(reporte_id))


@router.put("/finanzas/{reporte_fin_id}", response_model=ReporteFinanzasResponse)
def update_reporte_finanzas_endpoint(
    reporte_fin_id: str,
    reporte_fin_data: ReporteFinanzasUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte_fin = update_reporte_finanzas(db, UUID(reporte_fin_id), reporte_fin_data)
    if not updated_reporte_fin:
        raise HTTPException(status_code=404, detail="Reporte de Finanzas no encontrado")
    return updated_reporte_fin


@router.delete("/finanzas/{reporte_fin_id}")
def delete_reporte_finanzas_endpoint(
    reporte_fin_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_finanzas(db, UUID(reporte_fin_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de Finanzas no encontrado")
    return {"message": "Reporte de Finanzas eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA WIDGETS DEL DASHBOARD EJECUTIVO
# ============================================================================

@router.post("/dashboard-widgets", response_model=DashboardWidgetResponse)
def create_dashboard_widget_endpoint(
    widget_data: DashboardWidgetCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_dashboard_widget(db, widget_data)


@router.get("/dashboard-widgets/{widget_id}", response_model=DashboardWidgetResponse)
def get_dashboard_widget_endpoint(
    widget_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    widget = get_dashboard_widget(db, UUID(widget_id))
    if not widget:
        raise HTTPException(status_code=404, detail="Widget no encontrado")
    return widget


@router.get("/dashboard-widgets", response_model=List[DashboardWidgetResponse])
def get_dashboard_widgets_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_dashboard_widgets(db, skip, limit)


@router.put("/dashboard-widgets/{widget_id}", response_model=DashboardWidgetResponse)
def update_dashboard_widget_endpoint(
    widget_id: str,
    widget_data: DashboardWidgetUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_widget = update_dashboard_widget(db, UUID(widget_id), widget_data)
    if not updated_widget:
        raise HTTPException(status_code=404, detail="Widget no encontrado")
    return updated_widget


@router.delete("/dashboard-widgets/{widget_id}")
def delete_dashboard_widget_endpoint(
    widget_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_dashboard_widget(db, UUID(widget_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Widget no encontrado")
    return {"message": "Widget eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA REPORTES PERSONALIZADOS
# ============================================================================

@router.post("/reportes-personalizados", response_model=ReportePersonalizadoResponse)
def create_reporte_personalizado_endpoint(
    reporte_data: ReportePersonalizadoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_reporte_personalizado(db, reporte_data)


@router.get("/reportes-personalizados/{reporte_id}", response_model=ReportePersonalizadoResponse)
def get_reporte_personalizado_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    reporte = get_reporte_personalizado(db, UUID(reporte_id))
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte personalizado no encontrado")
    return reporte


@router.get("/reportes-personalizados", response_model=List[ReportePersonalizadoResponse])
def get_reportes_personalizados_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_reportes_personalizados(db, skip, limit)


@router.put("/reportes-personalizados/{reporte_id}", response_model=ReportePersonalizadoResponse)
def update_reporte_personalizado_endpoint(
    reporte_id: str,
    reporte_data: ReportePersonalizadoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_reporte = update_reporte_personalizado(db, UUID(reporte_id), reporte_data)
    if not updated_reporte:
        raise HTTPException(status_code=404, detail="Reporte personalizado no encontrado")
    return updated_reporte


@router.delete("/reportes-personalizados/{reporte_id}")
def delete_reporte_personalizado_endpoint(
    reporte_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_reporte_personalizado(db, UUID(reporte_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte personalizado no encontrado")
    return {"message": "Reporte personalizado eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA HISTÓRICO DE REPORTES
# ============================================================================

@router.post("/historico-reportes", response_model=HistoricoReporteResponse)
def create_historico_reporte_endpoint(
    historico_data: HistoricoReporteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_historico_reporte(db, historico_data)


@router.get("/historico-reportes/{historico_id}", response_model=HistoricoReporteResponse)
def get_historico_reporte_endpoint(
    historico_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    historico = get_historico_reporte(db, UUID(historico_id))
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico de reporte no encontrado")
    return historico


@router.get("/historico-reportes/reporte/{reporte_id}", response_model=List[HistoricoReporteResponse])
def get_historicos_by_reporte_endpoint(
    reporte_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_historicos_by_reporte(db, UUID(reporte_id), skip, limit)


@router.put("/historico-reportes/{historico_id}", response_model=HistoricoReporteResponse)
def update_historico_reporte_endpoint(
    historico_id: str,
    historico_data: HistoricoReporteUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_historico = update_historico_reporte(db, UUID(historico_id), historico_data)
    if not updated_historico:
        raise HTTPException(status_code=404, detail="Histórico de reporte no encontrado")
    return updated_historico
