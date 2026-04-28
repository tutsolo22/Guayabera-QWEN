"""
Business Intelligence CRUD Operations: Reports, data analysis, and dashboards for decision making
Specialized for textile manufacturing analytics
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.business_intelligence import (
    InformeBI, VisualizacionInforme, Dashboard, WidgetDashboard,
    EjecucionInforme, IndicadorKPI, ValorKPIHistorico
)
from app.schemas.business_intelligence import (
    InformeBICreate, InformeBIUpdate,
    VisualizacionInformeCreate, VisualizacionInformeUpdate,
    DashboardCreate, DashboardUpdate,
    WidgetDashboardCreate, WidgetDashboardUpdate,
    EjecucionInformeCreate, EjecucionInformeUpdate,
    IndicadorKPICreate, IndicadorKPIUpdate,
    ValorKPIHistoricoCreate, ValorKPIHistoricoUpdate
)


# ============================================================================
# REPORT CRUD
# ============================================================================

def create_informe_bi(db: Session, informe_data: InformeBICreate) -> InformeBI:
    """Create a new business intelligence report"""
    # Check if report code already exists
    existing_informe = db.query(InformeBI).filter(InformeBI.codigo == informe_data.codigo).first()
    if existing_informe:
        raise ValueError(f"A report with code {informe_data.codigo} already exists")
    
    db_informe = InformeBI(**informe_data.model_dump())
    db.add(db_informe)
    db.commit()
    db.refresh(db_informe)
    return db_informe


def get_informe_bi(db: Session, informe_id: UUID) -> Optional[InformeBI]:
    """Get a business intelligence report by ID"""
    return db.query(InformeBI).filter(InformeBI.id == informe_id).first()


def get_informe_bi_by_codigo(db: Session, codigo: str) -> Optional[InformeBI]:
    """Get a business intelligence report by code"""
    return db.query(InformeBI).filter(InformeBI.codigo == codigo).first()


def get_informes_bi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    tipo_reporte: Optional[str] = None,
    estado: Optional[str] = None,
    creador_id: Optional[UUID] = None,
    departamento_id: Optional[UUID] = None
) -> List[InformeBI]:
    """Get list of reports, optionally filtered"""
    query = db.query(InformeBI)
    
    if tipo_reporte:
        query = query.filter(InformeBI.tipo_reporte == tipo_reporte)
    if estado:
        query = query.filter(InformeBI.estado == estado)
    if creador_id:
        query = query.filter(InformeBI.creador_id == creador_id)
    if departamento_id:
        query = query.filter(InformeBI.departamento_id == departamento_id)
    
    return query.offset(skip).limit(limit).all()


def update_informe_bi(db: Session, informe_id: UUID, informe_data: InformeBIUpdate) -> Optional[InformeBI]:
    """Update a business intelligence report"""
    db_informe = get_informe_bi(db, informe_id)
    if db_informe:
        update_data = informe_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_informe, field, value)
        db.commit()
        db.refresh(db_informe)
    return db_informe


def delete_informe_bi(db: Session, informe_id: UUID) -> bool:
    """Soft delete a business intelligence report"""
    db_informe = get_informe_bi(db, informe_id)
    if db_informe:
        db_informe.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# REPORT VISUALIZATION CRUD
# ============================================================================

def create_visualizacion_informe(db: Session, visualizacion_data: VisualizacionInformeCreate) -> VisualizacionInforme:
    """Create a new report visualization"""
    db_visualizacion = VisualizacionInforme(**visualizacion_data.model_dump())
    db.add(db_visualizacion)
    db.commit()
    db.refresh(db_visualizacion)
    return db_visualizacion


def get_visualizacion_informe(db: Session, visualizacion_id: UUID) -> Optional[VisualizacionInforme]:
    """Get a report visualization by ID"""
    return db.query(VisualizacionInforme).filter(VisualizacionInforme.id == visualizacion_id).first()


def get_visualizaciones_by_informe(db: Session, informe_id: UUID) -> List[VisualizacionInforme]:
    """Get all visualizations for a specific report"""
    return db.query(VisualizacionInforme).filter(
        VisualizacionInforme.informe_id == informe_id
    ).all()


def update_visualizacion_informe(
    db: Session, 
    visualizacion_id: UUID, 
    visualizacion_data: VisualizacionInformeUpdate
) -> Optional[VisualizacionInforme]:
    """Update a report visualization"""
    db_visualizacion = get_visualizacion_informe(db, visualizacion_id)
    if db_visualizacion:
        update_data = visualizacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_visualizacion, field, value)
        db.commit()
        db.refresh(db_visualizacion)
    return db_visualizacion


def delete_visualizacion_informe(db: Session, visualizacion_id: UUID) -> bool:
    """Delete a report visualization"""
    db_visualizacion = get_visualizacion_informe(db, visualizacion_id)
    if db_visualizacion:
        db.delete(db_visualizacion)
        db.commit()
        return True
    return False


# ============================================================================
# DASHBOARD CRUD
# ============================================================================

def create_dashboard(db: Session, dashboard_data: DashboardCreate) -> Dashboard:
    """Create a new dashboard"""
    # Check if dashboard code already exists
    existing_dashboard = db.query(Dashboard).filter(Dashboard.codigo == dashboard_data.codigo).first()
    if existing_dashboard:
        raise ValueError(f"A dashboard with code {dashboard_data.codigo} already exists")
    
    db_dashboard = Dashboard(**dashboard_data.model_dump())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def get_dashboard(db: Session, dashboard_id: UUID) -> Optional[Dashboard]:
    """Get a dashboard by ID"""
    return db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()


def get_dashboard_by_codigo(db: Session, codigo: str) -> Optional[Dashboard]:
    """Get a dashboard by code"""
    return db.query(Dashboard).filter(Dashboard.codigo == codigo).first()


def get_dashboards(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    creador_id: Optional[UUID] = None,
    departamento_id: Optional[UUID] = None,
    activo: Optional[bool] = None
) -> List[Dashboard]:
    """Get list of dashboards, optionally filtered"""
    query = db.query(Dashboard)
    
    if creador_id:
        query = query.filter(Dashboard.creador_id == creador_id)
    if departamento_id:
        query = query.filter(Dashboard.departamento_id == departamento_id)
    if activo is not None:
        query = query.filter(Dashboard.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_dashboard(db: Session, dashboard_id: UUID, dashboard_data: DashboardUpdate) -> Optional[Dashboard]:
    """Update a dashboard"""
    db_dashboard = get_dashboard(db, dashboard_id)
    if db_dashboard:
        update_data = dashboard_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dashboard, field, value)
        db.commit()
        db.refresh(db_dashboard)
    return db_dashboard


def delete_dashboard(db: Session, dashboard_id: UUID) -> bool:
    """Soft delete a dashboard"""
    db_dashboard = get_dashboard(db, dashboard_id)
    if db_dashboard:
        db_dashboard.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# DASHBOARD WIDGET CRUD
# ============================================================================

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


def get_widgets_by_dashboard(db: Session, dashboard_id: UUID) -> List[WidgetDashboard]:
    """Get all widgets for a specific dashboard"""
    return db.query(WidgetDashboard).filter(
        WidgetDashboard.dashboard_id == dashboard_id
    ).all()


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


# ============================================================================
# REPORT EXECUTION CRUD
# ============================================================================

def create_ejecucion_informe(db: Session, ejecucion_data: EjecucionInformeCreate) -> EjecucionInforme:
    """Create a new report execution record"""
    db_ejecucion = EjecucionInforme(**ejecucion_data.model_dump())
    db.add(db_ejecucion)
    db.commit()
    db.refresh(db_ejecucion)
    
    # Update the report with the execution timestamp
    informe = get_informe_bi(db, ejecucion_data.informe_id)
    if informe:
        informe.fecha_ultima_ejecucion = func.now()
        # Calculate next execution based on frequency
        if informe.frecuencia_actualizacion == "diaria":
            informe.fecha_proxima_ejecucion = func.now() + func.interval('1 day')
        elif informe.frecuencia_actualizacion == "semanal":
            informe.fecha_proxima_ejecucion = func.now() + func.interval('1 week')
        elif informe.frecuencia_actualizacion == "mensual":
            informe.fecha_proxima_ejecucion = func.now() + func.interval('1 month')
        elif informe.frecuencia_actualizacion == "trimestral":
            informe.fecha_proxima_ejecucion = func.now() + func.interval('3 months')
        elif informe.frecuencia_actualizacion == "anual":
            informe.fecha_proxima_ejecucion = func.now() + func.interval('1 year')
        db.commit()
    
    return db_ejecucion


def get_ejecucion_informe(db: Session, ejecucion_id: UUID) -> Optional[EjecucionInforme]:
    """Get a report execution record by ID"""
    return db.query(EjecucionInforme).filter(EjecucionInforme.id == ejecucion_id).first()


def get_ejecuciones_by_informe(
    db: Session, 
    informe_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[EjecucionInforme]:
    """Get all executions for a specific report"""
    return db.query(EjecucionInforme).filter(
        EjecucionInforme.informe_id == informe_id
    ).order_by(EjecucionInforme.fecha_ejecucion.desc()).offset(skip).limit(limit).all()


def update_ejecucion_informe(
    db: Session, 
    ejecucion_id: UUID, 
    ejecucion_data: EjecucionInformeUpdate
) -> Optional[EjecucionInforme]:
    """Update a report execution record"""
    db_ejecucion = get_ejecucion_informe(db, ejecucion_id)
    if db_ejecucion:
        update_data = ejecucion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ejecucion, field, value)
        db.commit()
        db.refresh(db_ejecucion)
    return db_ejecucion


def delete_ejecucion_informe(db: Session, ejecucion_id: UUID) -> bool:
    """Delete a report execution record"""
    db_ejecucion = get_ejecucion_informe(db, ejecucion_id)
    if db_ejecucion:
        db.delete(db_ejecucion)
        db.commit()
        return True
    return False


# ============================================================================
# KPI INDICATOR CRUD
# ============================================================================

def create_indicador_kpi(db: Session, indicador_data: IndicadorKPICreate) -> IndicadorKPI:
    """Create a new KPI indicator"""
    # Check if KPI code already exists
    existing_indicador = db.query(IndicadorKPI).filter(IndicadorKPI.codigo == indicador_data.codigo).first()
    if existing_indicador:
        raise ValueError(f"A KPI indicator with code {indicador_data.codigo} already exists")
    
    db_indicador = IndicadorKPI(**indicador_data.model_dump())
    db.add(db_indicador)
    db.commit()
    db.refresh(db_indicador)
    return db_indicador


def get_indicador_kpi(db: Session, indicador_id: UUID) -> Optional[IndicadorKPI]:
    """Get a KPI indicator by ID"""
    return db.query(IndicadorKPI).filter(IndicadorKPI.id == indicador_id).first()


def get_indicador_kpi_by_codigo(db: Session, codigo: str) -> Optional[IndicadorKPI]:
    """Get a KPI indicator by code"""
    return db.query(IndicadorKPI).filter(IndicadorKPI.codigo == codigo).first()


def get_indicadores_kpi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    tipo_indicador: Optional[str] = None,
    activo: Optional[bool] = None,
    departamento_id: Optional[UUID] = None
) -> List[IndicadorKPI]:
    """Get list of KPI indicators, optionally filtered"""
    query = db.query(IndicadorKPI)
    
    if tipo_indicador:
        query = query.filter(IndicadorKPI.tipo_indicador == tipo_indicador)
    if activo is not None:
        query = query.filter(IndicadorKPI.activo == activo)
    if departamento_id:
        query = query.filter(IndicadorKPI.departamento_id == departamento_id)
    
    return query.offset(skip).limit(limit).all()


def update_indicador_kpi(
    db: Session, 
    indicador_id: UUID, 
    indicador_data: IndicadorKPIUpdate
) -> Optional[IndicadorKPI]:
    """Update a KPI indicator"""
    db_indicador = get_indicador_kpi(db, indicador_id)
    if db_indicador:
        update_data = indicador_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_indicador, field, value)
        db.commit()
        db.refresh(db_indicador)
    return db_indicador


def delete_indicador_kpi(db: Session, indicador_id: UUID) -> bool:
    """Soft delete a KPI indicator"""
    db_indicador = get_indicador_kpi(db, indicador_id)
    if db_indicador:
        db_indicador.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# HISTORICAL KPI VALUE CRUD
# ============================================================================

def create_valor_kpi_historico(db: Session, valor_data: ValorKPIHistoricoCreate) -> ValorKPIHistorico:
    """Create a new historical KPI value"""
    db_valor = ValorKPIHistorico(**valor_data.model_dump())
    db.add(db_valor)
    db.commit()
    db.refresh(db_valor)
    return db_valor


def get_valor_kpi_historico(db: Session, valor_id: UUID) -> Optional[ValorKPIHistorico]:
    """Get a historical KPI value by ID"""
    return db.query(ValorKPIHistorico).filter(ValorKPIHistorico.id == valor_id).first()


def get_valores_kpi_historico(
    db: Session, 
    indicador_id: UUID, 
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[ValorKPIHistorico]:
    """Get historical KPI values for a specific indicator, optionally filtered by date range"""
    query = db.query(ValorKPIHistorico).filter(
        ValorKPIHistorico.indicador_id == indicador_id
    ).order_by(ValorKPIHistorico.fecha_registro.desc())
    
    if fecha_inicio:
        query = query.filter(ValorKPIHistorico.fecha_registro >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ValorKPIHistorico.fecha_registro <= fecha_fin)
    
    return query.offset(skip).limit(limit).all()


def update_valor_kpi_historico(
    db: Session, 
    valor_id: UUID, 
    valor_data: ValorKPIHistoricoUpdate
) -> Optional[ValorKPIHistorico]:
    """Update a historical KPI value"""
    db_valor = get_valor_kpi_historico(db, valor_id)
    if db_valor:
        update_data = valor_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_valor, field, value)
        db.commit()
        db.refresh(db_valor)
    return db_valor


def delete_valor_kpi_historico(db: Session, valor_id: UUID) -> bool:
    """Delete a historical KPI value"""
    db_valor = get_valor_kpi_historico(db, valor_id)
    if db_valor:
        db.delete(db_valor)
        db.commit()
        return True
    return False