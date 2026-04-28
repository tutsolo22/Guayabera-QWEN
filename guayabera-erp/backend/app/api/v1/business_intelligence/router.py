from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.business_intelligence import ReporteBI
from app.schemas.business_intelligence import (
    ReporteBICreate, ReporteBIUpdate, ReporteBIResponse,
    WidgetDashboardCreate, WidgetDashboardUpdate, WidgetDashboardResponse,
    DashboardBICreate, DashboardBIUpdate, DashboardBIResponse,
    AnalisisPredictivoCreate, AnalisisPredictivoUpdate, AnalisisPredictivoResponse,
    KpiCreate, KpiUpdate, KpiResponse,
    HistoricoKpiCreate, HistoricoKpiUpdate, HistoricoKpiResponse
)
from app.crud.business_intelligence import (
    create_bi_report, get_bi_report, get_bi_reports_by_tipo,
    get_bi_reports_by_creator, update_bi_report, delete_bi_report,
    create_widget_dashboard, get_widget_dashboard, get_widgets_by_dashboard,
    update_widget_dashboard, delete_widget_dashboard,
    create_dashboard_bi, get_dashboard_bi, get_dashboards_by_owner,
    get_public_dashboards, update_dashboard_bi, delete_dashboard_bi,
    create_analisis_predictivo, get_analisis_predictivo, get_analisis_predictivo_by_tipo,
    update_analisis_predictivo, delete_analisis_predictivo,
    create_kpi, get_kpi, get_kpis_by_department, get_active_kpis,
    update_kpi, delete_kpi,
    create_historico_kpi, get_historico_kpi, get_historico_kpi_by_kpi
)

router = APIRouter()


# ============================================================================
# ENDPOINTS PARA REPORTES DE BUSINESS INTELLIGENCE
# ============================================================================

@router.post("/reports", response_model=ReporteBIResponse)
def create_bi_report_endpoint(
    report_data: ReporteBICreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_bi_report(db, report_data)


@router.get("/reports/{report_id}", response_model=ReporteBIResponse)
def get_bi_report_endpoint(
    report_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    report = get_bi_report(db, UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Reporte BI no encontrado")
    return report


@router.get("/reports/type/{tipo}", response_model=List[ReporteBIResponse])
def get_bi_reports_by_tipo_endpoint(
    tipo: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_bi_reports_by_tipo(db, tipo, skip, limit)


@router.get("/reports/creator/{creador_id}", response_model=List[ReporteBIResponse])
def get_bi_reports_by_creator_endpoint(
    creador_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_bi_reports_by_creator(db, UUID(creador_id), skip, limit)


@router.put("/reports/{report_id}", response_model=ReporteBIResponse)
def update_bi_report_endpoint(
    report_id: str,
    report_data: ReporteBIUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_report = update_bi_report(db, UUID(report_id), report_data)
    if not updated_report:
        raise HTTPException(status_code=404, detail="Reporte BI no encontrado")
    return updated_report


@router.delete("/reports/{report_id}")
def delete_bi_report_endpoint(
    report_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_bi_report(db, UUID(report_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte BI no encontrado")
    return {"message": "Reporte BI eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA WIDGETS DE DASHBOARD
# ============================================================================

@router.post("/widgets", response_model=WidgetDashboardResponse)
def create_widget_dashboard_endpoint(
    widget_data: WidgetDashboardCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_widget_dashboard(db, widget_data)


@router.get("/widgets/{widget_id}", response_model=WidgetDashboardResponse)
def get_widget_dashboard_endpoint(
    widget_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    widget = get_widget_dashboard(db, UUID(widget_id))
    if not widget:
        raise HTTPException(status_code=404, detail="Widget de dashboard no encontrado")
    return widget


@router.get("/widgets/dashboard/{dashboard_id}", response_model=List[WidgetDashboardResponse])
def get_widgets_by_dashboard_endpoint(
    dashboard_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_widgets_by_dashboard(db, UUID(dashboard_id), skip, limit)


@router.put("/widgets/{widget_id}", response_model=WidgetDashboardResponse)
def update_widget_dashboard_endpoint(
    widget_id: str,
    widget_data: WidgetDashboardUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_widget = update_widget_dashboard(db, UUID(widget_id), widget_data)
    if not updated_widget:
        raise HTTPException(status_code=404, detail="Widget de dashboard no encontrado")
    return updated_widget


@router.delete("/widgets/{widget_id}")
def delete_widget_dashboard_endpoint(
    widget_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_widget_dashboard(db, UUID(widget_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Widget de dashboard no encontrado")
    return {"message": "Widget de dashboard eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA DASHBOARDS DE BUSINESS INTELLIGENCE
# ============================================================================

@router.post("/dashboards", response_model=DashboardBIResponse)
def create_dashboard_bi_endpoint(
    dashboard_data: DashboardBICreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de administrador o gerente pueden crear dashboards
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear dashboards")
    
    return create_dashboard_bi(db, dashboard_data)


@router.get("/dashboards/{dashboard_id}", response_model=DashboardBIResponse)
def get_dashboard_bi_endpoint(
    dashboard_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    dashboard = get_dashboard_bi(db, UUID(dashboard_id))
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard BI no encontrado")
    return dashboard


@router.get("/dashboards/owner/{owner_id}", response_model=List[DashboardBIResponse])
def get_dashboards_by_owner_endpoint(
    owner_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_dashboards_by_owner(db, UUID(owner_id), skip, limit)


@router.get("/dashboards/public", response_model=List[DashboardBIResponse])
def get_public_dashboards_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_public_dashboards(db, skip, limit)


@router.put("/dashboards/{dashboard_id}", response_model=DashboardBIResponse)
def update_dashboard_bi_endpoint(
    dashboard_id: str,
    dashboard_data: DashboardBIUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador o gerente pueden actualizar dashboards
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar dashboards")
    
    updated_dashboard = update_dashboard_bi(db, UUID(dashboard_id), dashboard_data)
    if not updated_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard BI no encontrado")
    return updated_dashboard


@router.delete("/dashboards/{dashboard_id}")
def delete_dashboard_bi_endpoint(
    dashboard_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador o gerente pueden eliminar dashboards
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar dashboards")
    
    deleted = delete_dashboard_bi(db, UUID(dashboard_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Dashboard BI no encontrado")
    return {"message": "Dashboard BI eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA ANÁLISIS PREDICTIVOS
# ============================================================================

@router.post("/analyses", response_model=AnalisisPredictivoResponse)
def create_analisis_predictivo_endpoint(
    analisis_data: AnalisisPredictivoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de administrador pueden crear análisis predictivos
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear análisis predictivos")
    
    return create_analisis_predictivo(db, analisis_data)


@router.get("/analyses/{analisis_id}", response_model=AnalisisPredictivoResponse)
def get_analisis_predictivo_endpoint(
    analisis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    analisis = get_analisis_predictivo(db, UUID(analisis_id))
    if not analisis:
        raise HTTPException(status_code=404, detail="Análisis predictivo no encontrado")
    return analisis


@router.get("/analyses/type/{tipo_modelo}", response_model=List[AnalisisPredictivoResponse])
def get_analisis_predictivo_by_tipo_endpoint(
    tipo_modelo: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_analisis_predictivo_by_tipo(db, tipo_modelo, skip, limit)


@router.put("/analyses/{analisis_id}", response_model=AnalisisPredictivoResponse)
def update_analisis_predictivo_endpoint(
    analisis_id: str,
    analisis_data: AnalisisPredictivoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador pueden actualizar análisis predictivos
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar análisis predictivos")
    
    updated_analisis = update_analisis_predictivo(db, UUID(analisis_id), analisis_data)
    if not updated_analisis:
        raise HTTPException(status_code=404, detail="Análisis predictivo no encontrado")
    return updated_analisis


@router.delete("/analyses/{analisis_id}")
def delete_analisis_predictivo_endpoint(
    analisis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador pueden eliminar análisis predictivos
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar análisis predictivos")
    
    deleted = delete_analisis_predictivo(db, UUID(analisis_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Análisis predictivo no encontrado")
    return {"message": "Análisis predictivo eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA KPIs
# ============================================================================

@router.post("/kpis", response_model=KpiResponse)
def create_kpi_endpoint(
    kpi_data: KpiCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de administrador o gerente pueden crear KPIs
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear KPIs")
    
    return create_kpi(db, kpi_data)


@router.get("/kpis/{kpi_id}", response_model=KpiResponse)
def get_kpi_endpoint(
    kpi_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    kpi = get_kpi(db, UUID(kpi_id))
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI no encontrado")
    return kpi


@router.get("/kpis/department/{department_id}", response_model=List[KpiResponse])
def get_kpis_by_department_endpoint(
    department_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_kpis_by_department(db, UUID(department_id), skip, limit)


@router.get("/kpis/active", response_model=List[KpiResponse])
def get_active_kpis_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_active_kpis(db, skip, limit)


@router.put("/kpis/{kpi_id}", response_model=KpiResponse)
def update_kpi_endpoint(
    kpi_id: str,
    kpi_data: KpiUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador o gerente pueden actualizar KPIs
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar KPIs")
    
    updated_kpi = update_kpi(db, UUID(kpi_id), kpi_data)
    if not updated_kpi:
        raise HTTPException(status_code=404, detail="KPI no encontrado")
    return updated_kpi


@router.delete("/kpis/{kpi_id}")
def delete_kpi_endpoint(
    kpi_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador o gerente pueden eliminar KPIs
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar KPIs")
    
    deleted = delete_kpi(db, UUID(kpi_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="KPI no encontrado")
    return {"message": "KPI eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA HISTÓRICO DE KPIs
# ============================================================================

@router.post("/kpis/history", response_model=HistoricoKpiResponse)
def create_historico_kpi_endpoint(
    historico_data: HistoricoKpiCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de administrador, gerente o responsable de KPI pueden crear registros
    if not current_user.get("rol") in ["admin", "gerente", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear historial de KPI")
    
    return create_historico_kpi(db, historico_data)


@router.get("/kpis/history/{historico_id}", response_model=HistoricoKpiResponse)
def get_historico_kpi_endpoint(
    historico_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    historico = get_historico_kpi(db, UUID(historico_id))
    if not historico:
        raise HTTPException(status_code=404, detail="Registro de historial de KPI no encontrado")
    return historico


@router.get("/kpis/history/kpi/{kpi_id}/range")
def get_historico_kpi_by_kpi_endpoint(
    kpi_id: str,
    start_date: date,
    end_date: date,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    historicos = get_historico_kpi_by_kpi(db, UUID(kpi_id), start_date, end_date)
    return historicos