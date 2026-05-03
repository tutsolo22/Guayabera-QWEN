from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID
from datetime import date

from app.models.business_intelligence import (
    ReporteBI, WidgetDashboard, DashboardBI, 
    AnalisisPredictivo, KPI as Kpi, ValorKPIHistorico as HistoricoKpi
)
from app.schemas.business_intelligence import (
    ReporteBICreate, ReporteBIUpdate, ReporteBIResponse,
    WidgetDashboardCreate, WidgetDashboardUpdate, WidgetDashboardResponse,
    DashboardBICreate, DashboardBIUpdate, DashboardBIResponse,
    AnalisisPredictivoCreate, AnalisisPredictivoUpdate, AnalisisPredictivoResponse,
    KpiCreate, KpiUpdate, KpiResponse,
    HistoricoKpiCreate, HistoricoKpiUpdate, HistoricoKpiResponse
)


def create_bi_report(db: Session, report_data: ReporteBICreate) -> ReporteBI:
    """Create a new BI report"""
    db_report = ReporteBI(**report_data.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_bi_report(db: Session, report_id: UUID) -> Optional[ReporteBI]:
    """Get a BI report by ID"""
    return db.query(ReporteBI).filter(ReporteBI.id == report_id).first()


def get_bi_reports_by_tipo(db: Session, tipo: str, skip: int = 0, limit: int = 100) -> List[ReporteBI]:
    """Get BI reports by type"""
    return db.query(ReporteBI).filter(
        ReporteBI.tipo == tipo,
        ReporteBI.activo == True
    ).order_by(ReporteBI.created_at.desc()).offset(skip).limit(limit).all()


def get_bi_reports_by_creator(db: Session, creador_id: UUID, skip: int = 0, limit: int = 100) -> List[ReporteBI]:
    """Get BI reports by creator"""
    return db.query(ReporteBI).filter(
        ReporteBI.creador_id == creador_id
    ).order_by(ReporteBI.created_at.desc()).offset(skip).limit(limit).all()


def update_bi_report(
    db: Session, 
    report_id: UUID, 
    report_data: ReporteBIUpdate
) -> Optional[ReporteBI]:
    """Update a BI report"""
    db_report = get_bi_report(db, report_id)
    if db_report:
        update_data = report_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_report, field, value)
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_bi_report(db: Session, report_id: UUID) -> bool:
    """Delete a BI report (soft delete by deactivation)"""
    db_report = get_bi_report(db, report_id)
    if db_report:
        db_report.activo = False
        db.commit()
        return True
    return False


def create_widget_dashboard(db: Session, widget_data: WidgetDashboardCreate) -> WidgetDashboard:
    """Create a new dashboard widget"""
    db_widget = WidgetDashboard(**widget_data.model_dump())
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    return db_widget


def get_widget_dashboard(db: Session, widget_id: UUID) -> Optional[WidgetDashboard]:
    """Get a dashboard widget by ID"""
    return db.query(WidgetDashboard).filter(WidgetDashboard.id == widget_id).first()


def get_widgets_by_dashboard(db: Session, dashboard_id: UUID, skip: int = 0, limit: int = 100) -> List[WidgetDashboard]:
    """Get widgets by dashboard ID"""
    return db.query(WidgetDashboard).filter(
        WidgetDashboard.dashboard_id == dashboard_id
    ).order_by(WidgetDashboard.posicion_y, WidgetDashboard.posicion_x).offset(skip).limit(limit).all()


def update_widget_dashboard(
    db: Session, 
    widget_id: UUID, 
    widget_data: WidgetDashboardUpdate
) -> Optional[WidgetDashboard]:
    """Update a dashboard widget"""
    db_widget = get_widget_dashboard(db, widget_id)
    if db_widget:
        update_data = widget_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_widget, field, value)
        db.commit()
        db.refresh(db_widget)
    return db_widget


def delete_widget_dashboard(db: Session, widget_id: UUID) -> bool:
    """Delete a dashboard widget"""
    db_widget = get_widget_dashboard(db, widget_id)
    if db_widget:
        db.delete(db_widget)
        db.commit()
        return True
    return False


def create_dashboard_bi(db: Session, dashboard_data: DashboardBICreate) -> DashboardBI:
    """Create a new BI dashboard"""
    db_dashboard = DashboardBI(**dashboard_data.model_dump())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def get_dashboard_bi(db: Session, dashboard_id: UUID) -> Optional[DashboardBI]:
    """Get a BI dashboard by ID"""
    return db.query(DashboardBI).filter(DashboardBI.id == dashboard_id).first()


def get_dashboards_by_owner(db: Session, owner_id: UUID, skip: int = 0, limit: int = 100) -> List[DashboardBI]:
    """Get dashboards by owner ID"""
    return db.query(DashboardBI).filter(
        DashboardBI.propietario_id == owner_id
    ).order_by(DashboardBI.created_at.desc()).offset(skip).limit(limit).all()


def get_public_dashboards(db: Session, skip: int = 0, limit: int = 100) -> List[DashboardBI]:
    """Get public dashboards"""
    return db.query(DashboardBI).filter(
        DashboardBI.es_publico == True
    ).order_by(DashboardBI.created_at.desc()).offset(skip).limit(limit).all()


def update_dashboard_bi(
    db: Session, 
    dashboard_id: UUID, 
    dashboard_data: DashboardBIUpdate
) -> Optional[DashboardBI]:
    """Update a BI dashboard"""
    db_dashboard = get_dashboard_bi(db, dashboard_id)
    if db_dashboard:
        update_data = dashboard_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dashboard, field, value)
        db.commit()
        db.refresh(db_dashboard)
    return db_dashboard


def delete_dashboard_bi(db: Session, dashboard_id: UUID) -> bool:
    """Delete a BI dashboard"""
    db_dashboard = get_dashboard_bi(db, dashboard_id)
    if db_dashboard:
        db.delete(db_dashboard)
        db.commit()
        return True
    return False


def create_analisis_predictivo(db: Session, analisis_data: AnalisisPredictivoCreate) -> AnalisisPredictivo:
    """Create a new predictive analysis"""
    db_analisis = AnalisisPredictivo(**analisis_data.model_dump())
    db.add(db_analisis)
    db.commit()
    db.refresh(db_analisis)
    return db_analisis


def get_analisis_predictivo(db: Session, analisis_id: UUID) -> Optional[AnalisisPredictivo]:
    """Get a predictive analysis by ID"""
    return db.query(AnalisisPredictivo).filter(AnalisisPredictivo.id == analisis_id).first()


def get_analisis_predictivo_by_tipo(db: Session, tipo_modelo: str, skip: int = 0, limit: int = 100) -> List[AnalisisPredictivo]:
    """Get predictive analyses by model type"""
    return db.query(AnalisisPredictivo).filter(
        AnalisisPredictivo.tipo_modelo == tipo_modelo,
        AnalisisPredictivo.activo == True
    ).order_by(AnalisisPredictivo.created_at.desc()).offset(skip).limit(limit).all()


def update_analisis_predictivo(
    db: Session, 
    analisis_id: UUID, 
    analisis_data: AnalisisPredictivoUpdate
) -> Optional[AnalisisPredictivo]:
    """Update a predictive analysis"""
    db_analisis = get_analisis_predictivo(db, analisis_id)
    if db_analisis:
        update_data = analisis_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_analisis, field, value)
        db.commit()
        db.refresh(db_analisis)
    return db_analisis


def delete_analisis_predictivo(db: Session, analisis_id: UUID) -> bool:
    """Delete a predictive analysis (soft delete by deactivation)"""
    db_analisis = get_analisis_predictivo(db, analisis_id)
    if db_analisis:
        db_analisis.activo = False
        db.commit()
        return True
    return False


def create_kpi(db: Session, kpi_data: KpiCreate) -> Kpi:
    """Create a new KPI"""
    db_kpi = Kpi(**kpi_data.model_dump())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi


def get_kpi(db: Session, kpi_id: UUID) -> Optional[Kpi]:
    """Get a KPI by ID"""
    return db.query(Kpi).filter(Kpi.id == kpi_id).first()


def get_kpis_by_department(db: Session, department_id: UUID, skip: int = 0, limit: int = 100) -> List[Kpi]:
    """Get KPIs by department ID"""
    return db.query(Kpi).filter(
        Kpi.departamento_id == department_id,
        Kpi.activo == True
    ).order_by(Kpi.created_at.desc()).offset(skip).limit(limit).all()


def get_active_kpis(db: Session, skip: int = 0, limit: int = 100) -> List[Kpi]:
    """Get all active KPIs"""
    return db.query(Kpi).filter(
        Kpi.activo == True
    ).order_by(Kpi.created_at.desc()).offset(skip).limit(limit).all()


def update_kpi(
    db: Session, 
    kpi_id: UUID, 
    kpi_data: KpiUpdate
) -> Optional[Kpi]:
    """Update a KPI"""
    db_kpi = get_kpi(db, kpi_id)
    if db_kpi:
        update_data = kpi_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_kpi, field, value)
        db.commit()
        db.refresh(db_kpi)
    return db_kpi


def delete_kpi(db: Session, kpi_id: UUID) -> bool:
    """Delete a KPI (soft delete by deactivation)"""
    db_kpi = get_kpi(db, kpi_id)
    if db_kpi:
        db_kpi.activo = False
        db.commit()
        return True
    return False


def create_historico_kpi(db: Session, historico_data: HistoricoKpiCreate) -> HistoricoKpi:
    """Create a new KPI history record"""
    db_historico = HistoricoKpi(**historico_data.model_dump())
    db.add(db_historico)
    db.commit()
    db.refresh(db_historico)
    return db_historico


def get_historico_kpi(db: Session, historico_id: UUID) -> Optional[HistoricoKpi]:
    """Get a KPI history record by ID"""
    return db.query(HistoricoKpi).filter(HistoricoKpi.id == historico_id).first()


def get_historico_kpi_by_kpi(db: Session, kpi_id: UUID, start_date: date, end_date: date) -> List[HistoricoKpi]:
    """Get KPI history records by KPI ID and date range"""
    return db.query(HistoricoKpi).filter(
        HistoricoKpi.kpi_id == kpi_id,
        HistoricoKpi.fecha_registro >= start_date,
        HistoricoKpi.fecha_registro <= end_date
    ).order_by(HistoricoKpi.fecha_registro.asc()).all()


def update_historico_kpi(
    db: Session, 
    historico_id: UUID, 
    historico_data: HistoricoKpiUpdate
) -> Optional[HistoricoKpi]:
    """Update a KPI history record"""
    db_historico = get_historico_kpi(db, historico_id)
    if db_historico:
        update_data = historico_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_historico, field, value)
        db.commit()
        db.refresh(db_historico)
    return db_historico