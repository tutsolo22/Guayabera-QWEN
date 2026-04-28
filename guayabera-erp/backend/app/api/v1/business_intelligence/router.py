"""
Business Intelligence API Router: Reports, data analysis, and dashboards for decision making
Specialized for textile manufacturing analytics
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.business_intelligence import (
    InformeBICreate, InformeBIUpdate, InformeBIResponse,
    VisualizacionInformeCreate, VisualizacionInformeUpdate, VisualizacionInformeResponse,
    DashboardCreate, DashboardUpdate, DashboardResponse,
    WidgetDashboardCreate, WidgetDashboardUpdate, WidgetDashboardResponse,
    EjecucionInformeCreate, EjecucionInformeUpdate, EjecucionInformeResponse,
    IndicadorKPICreate, IndicadorKPIUpdate, IndicadorKPIResponse,
    ValorKPIHistoricoCreate, ValorKPIHistoricoUpdate, ValorKPIHistoricoResponse
)
from app.crud.business_intelligence import (
    create_informe_bi, get_informe_bi, get_informe_bi_by_codigo,
    get_informes_bi, update_informe_bi, delete_informe_bi,
    create_visualizacion_informe, get_visualizacion_informe, get_visualizaciones_by_informe,
    update_visualizacion_informe, delete_visualizacion_informe,
    create_dashboard, get_dashboard, get_dashboard_by_codigo,
    get_dashboards, update_dashboard, delete_dashboard,
    create_widget_dashboard, get_widget_dashboard, get_widgets_by_dashboard,
    update_widget_dashboard, delete_widget_dashboard,
    create_ejecucion_informe, get_ejecucion_informe, get_ejecuciones_by_informe,
    update_ejecucion_informe, delete_ejecucion_informe,
    create_indicador_kpi, get_indicador_kpi, get_indicador_kpi_by_codigo,
    get_indicadores_kpi, update_indicador_kpi, delete_indicador_kpi,
    create_valor_kpi_historico, get_valor_kpi_historico, get_valores_kpi_historico,
    update_valor_kpi_historico, delete_valor_kpi_historico
)

router = APIRouter(prefix="/business-intelligence", tags=["Business Intelligence"])

# ============================================================================
# REPORT ENDPOINTS
# ============================================================================

@router.post("/reports/", response_model=InformeBIResponse)
def create_report(informe: InformeBICreate, db: Session = Depends(get_db)):
    """Create a new business intelligence report"""
    try:
        return create_informe_bi(db=db, informe_data=informe)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/reports/{informe_id}", response_model=InformeBIResponse)
def get_report(informe_id: str, db: Session = Depends(get_db)):
    """Get a business intelligence report by ID"""
    informe = get_informe_bi(db, informe_id)
    if not informe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return informe


@router.get("/reports/code/{codigo}", response_model=InformeBIResponse)
def get_report_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a business intelligence report by code"""
    informe = get_informe_bi_by_codigo(db, codigo)
    if not informe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return informe


@router.get("/reports/", response_model=List[InformeBIResponse])
def get_reports(
    skip: int = 0, 
    limit: int = 100,
    tipo_reporte: Optional[str] = None,
    estado: Optional[str] = None,
    creador_id: Optional[str] = None,
    departamento_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of reports, optionally filtered"""
    creador_uuid = UUID(creador_id) if creador_id else None
    dept_uuid = UUID(departamento_id) if departamento_id else None
    return get_informes_bi(db, skip, limit, tipo_reporte, estado, creador_uuid, dept_uuid)


@router.put("/reports/{informe_id}", response_model=InformeBIResponse)
def update_report(
    informe_id: str, 
    informe_data: InformeBIUpdate, 
    db: Session = Depends(get_db)
):
    """Update a business intelligence report"""
    updated_informe = update_informe_bi(
        db=db, 
        informe_id=informe_id, 
        informe_data=informe_data
    )
    if not updated_informe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return updated_informe


@router.delete("/reports/{informe_id}")
def delete_report(informe_id: str, db: Session = Depends(get_db)):
    """Soft delete a business intelligence report"""
    success = delete_informe_bi(db=db, informe_id=informe_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return {"message": "Report deactivated successfully"}


# ============================================================================
# REPORT VISUALIZATION ENDPOINTS
# ============================================================================

@router.post("/visualizations/", response_model=VisualizacionInformeResponse)
def create_report_visualization(visualizacion: VisualizacionInformeCreate, db: Session = Depends(get_db)):
    """Create a new report visualization"""
    return create_visualizacion_informe(db=db, visualizacion_data=visualizacion)


@router.get("/visualizations/{visualizacion_id}", response_model=VisualizacionInformeResponse)
def get_report_visualization(visualizacion_id: str, db: Session = Depends(get_db)):
    """Get a report visualization by ID"""
    visualizacion = get_visualizacion_informe(db, visualizacion_id)
    if not visualizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report visualization not found"
        )
    return visualizacion


@router.get("/reports/{informe_id}/visualizations", response_model=List[VisualizacionInformeResponse])
def get_visualizations_by_report(informe_id: str, db: Session = Depends(get_db)):
    """Get all visualizations for a specific report"""
    return get_visualizaciones_by_informe(db, informe_id)


@router.put("/visualizations/{visualizacion_id}", response_model=VisualizacionInformeResponse)
def update_report_visualization(
    visualizacion_id: str, 
    visualizacion_data: VisualizacionInformeUpdate, 
    db: Session = Depends(get_db)
):
    """Update a report visualization"""
    updated_visualizacion = update_visualizacion_informe(
        db=db, 
        visualizacion_id=visualizacion_id, 
        visualizacion_data=visualizacion_data
    )
    if not updated_visualizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report visualization not found"
        )
    return updated_visualizacion


@router.delete("/visualizations/{visualizacion_id}")
def delete_report_visualization(visualizacion_id: str, db: Session = Depends(get_db)):
    """Delete a report visualization"""
    success = delete_visualizacion_informe(db=db, visualizacion_id=visualizacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report visualization not found"
        )
    return {"message": "Report visualization deleted successfully"}


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@router.post("/dashboards/", response_model=DashboardResponse)
def create_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db)):
    """Create a new dashboard"""
    try:
        return create_dashboard(db=db, dashboard_data=dashboard)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
def get_dashboard(dashboard_id: str, db: Session = Depends(get_db)):
    """Get a dashboard by ID"""
    dashboard = get_dashboard(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    return dashboard


@router.get("/dashboards/code/{codigo}", response_model=DashboardResponse)
def get_dashboard_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a dashboard by code"""
    dashboard = get_dashboard_by_codigo(db, codigo)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    return dashboard


@router.get("/dashboards/", response_model=List[DashboardResponse])
def get_dashboards(
    skip: int = 0, 
    limit: int = 100,
    creador_id: Optional[str] = None,
    departamento_id: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of dashboards, optionally filtered"""
    creador_uuid = UUID(creador_id) if creador_id else None
    dept_uuid = UUID(departamento_id) if departamento_id else None
    return get_dashboards(db, skip, limit, creador_uuid, dept_uuid, activo)


@router.put("/dashboards/{dashboard_id}", response_model=DashboardResponse)
def update_dashboard(
    dashboard_id: str, 
    dashboard_data: DashboardUpdate, 
    db: Session = Depends(get_db)
):
    """Update a dashboard"""
    updated_dashboard = update_dashboard(
        db=db, 
        dashboard_id=dashboard_id, 
        dashboard_data=dashboard_data
    )
    if not updated_dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    return updated_dashboard


@router.delete("/dashboards/{dashboard_id}")
def delete_dashboard(dashboard_id: str, db: Session = Depends(get_db)):
    """Soft delete a dashboard"""
    success = delete_dashboard(db=db, dashboard_id=dashboard_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    return {"message": "Dashboard deactivated successfully"}


# ============================================================================
# DASHBOARD WIDGET ENDPOINTS
# ============================================================================

@router.post("/dashboard-widgets/", response_model=WidgetDashboardResponse)
def create_dashboard_widget(widget: WidgetDashboardCreate, db: Session = Depends(get_db)):
    """Create a new dashboard widget"""
    return create_widget_dashboard(db=db, widget_data=widget)


@router.get("/dashboard-widgets/{widget_id}", response_model=WidgetDashboardResponse)
def get_dashboard_widget(widget_id: str, db: Session = Depends(get_db)):
    """Get a dashboard widget by ID"""
    widget = get_widget_dashboard(db, widget_id)
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard widget not found"
        )
    return widget


@router.get("/dashboards/{dashboard_id}/widgets", response_model=List[WidgetDashboardResponse])
def get_widgets_by_dashboard(dashboard_id: str, db: Session = Depends(get_db)):
    """Get all widgets for a specific dashboard"""
    return get_widgets_by_dashboard(db, dashboard_id)


@router.put("/dashboard-widgets/{widget_id}", response_model=WidgetDashboardResponse)
def update_dashboard_widget(
    widget_id: str, 
    widget_data: WidgetDashboardUpdate, 
    db: Session = Depends(get_db)
):
    """Update a dashboard widget"""
    updated_widget = update_widget_dashboard(
        db=db, 
        widget_id=widget_id, 
        widget_data=widget_data
    )
    if not updated_widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard widget not found"
        )
    return updated_widget


@router.delete("/dashboard-widgets/{widget_id}")
def delete_dashboard_widget(widget_id: str, db: Session = Depends(get_db)):
    """Delete a dashboard widget"""
    success = delete_widget_dashboard(db=db, widget_id=widget_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard widget not found"
        )
    return {"message": "Dashboard widget deleted successfully"}


# ============================================================================
# REPORT EXECUTION ENDPOINTS
# ============================================================================

@router.post("/report-executions/", response_model=EjecucionInformeResponse)
def create_report_execution(ejecucion: EjecucionInformeCreate, db: Session = Depends(get_db)):
    """Create a new report execution record"""
    return create_ejecucion_informe(db=db, ejecucion_data=ejecucion)


@router.get("/report-executions/{ejecucion_id}", response_model=EjecucionInformeResponse)
def get_report_execution(ejecucion_id: str, db: Session = Depends(get_db)):
    """Get a report execution record by ID"""
    ejecucion = get_ejecucion_informe(db, ejecucion_id)
    if not ejecucion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report execution not found"
        )
    return ejecucion


@router.get("/reports/{informe_id}/executions", response_model=List[EjecucionInformeResponse])
def get_executions_by_report(
    informe_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all executions for a specific report"""
    return get_ejecuciones_by_informe(db, informe_id, skip, limit)


@router.put("/report-executions/{ejecucion_id}", response_model=EjecucionInformeResponse)
def update_report_execution(
    ejecucion_id: str, 
    ejecucion_data: EjecucionInformeUpdate, 
    db: Session = Depends(get_db)
):
    """Update a report execution record"""
    updated_ejecucion = update_ejecucion_informe(
        db=db, 
        ejecucion_id=ejecucion_id, 
        ejecucion_data=ejecucion_data
    )
    if not updated_ejecucion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report execution not found"
        )
    return updated_ejecucion


@router.delete("/report-executions/{ejecucion_id}")
def delete_report_execution(ejecucion_id: str, db: Session = Depends(get_db)):
    """Delete a report execution record"""
    success = delete_ejecucion_informe(db=db, ejecucion_id=ejecucion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report execution not found"
        )
    return {"message": "Report execution deleted successfully"}


# ============================================================================
# KPI INDICATOR ENDPOINTS
# ============================================================================

@router.post("/kpi-indicators/", response_model=IndicadorKPIResponse)
def create_kpi_indicator(indicador: IndicadorKPICreate, db: Session = Depends(get_db)):
    """Create a new KPI indicator"""
    try:
        return create_indicador_kpi(db=db, indicador_data=indicador)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/kpi-indicators/{indicador_id}", response_model=IndicadorKPIResponse)
def get_kpi_indicator(indicador_id: str, db: Session = Depends(get_db)):
    """Get a KPI indicator by ID"""
    indicador = get_indicador_kpi(db, indicador_id)
    if not indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI indicator not found"
        )
    return indicador


@router.get("/kpi-indicators/code/{codigo}", response_model=IndicadorKPIResponse)
def get_kpi_indicator_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a KPI indicator by code"""
    indicador = get_indicador_kpi_by_codigo(db, codigo)
    if not indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI indicator not found"
        )
    return indicador


@router.get("/kpi-indicators/", response_model=List[IndicadorKPIResponse])
def get_kpi_indicators(
    skip: int = 0, 
    limit: int = 100,
    tipo_indicador: Optional[str] = None,
    activo: Optional[bool] = None,
    departamento_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of KPI indicators, optionally filtered"""
    dept_uuid = UUID(departamento_id) if departamento_id else None
    return get_indicadores_kpi(db, skip, limit, tipo_indicador, activo, dept_uuid)


@router.put("/kpi-indicators/{indicador_id}", response_model=IndicadorKPIResponse)
def update_kpi_indicator(
    indicador_id: str, 
    indicador_data: IndicadorKPIUpdate, 
    db: Session = Depends(get_db)
):
    """Update a KPI indicator"""
    updated_indicador = update_indicador_kpi(
        db=db, 
        indicador_id=indicador_id, 
        indicador_data=indicador_data
    )
    if not updated_indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI indicator not found"
        )
    return updated_indicador


@router.delete("/kpi-indicators/{indicador_id}")
def delete_kpi_indicator(indicador_id: str, db: Session = Depends(get_db)):
    """Soft delete a KPI indicator"""
    success = delete_indicador_kpi(db=db, indicador_id=indicador_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI indicator not found"
        )
    return {"message": "KPI indicator deactivated successfully"}


# ============================================================================
# HISTORICAL KPI VALUE ENDPOINTS
# ============================================================================

@router.post("/kpi-historical-values/", response_model=ValorKPIHistoricoResponse)
def create_kpi_historical_value(valor: ValorKPIHistoricoCreate, db: Session = Depends(get_db)):
    """Create a new historical KPI value"""
    return create_valor_kpi_historico(db=db, valor_data=valor)


@router.get("/kpi-historical-values/{valor_id}", response_model=ValorKPIHistoricoResponse)
def get_kpi_historical_value(valor_id: str, db: Session = Depends(get_db)):
    """Get a historical KPI value by ID"""
    valor = get_valor_kpi_historico(db, valor_id)
    if not valor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historical KPI value not found"
        )
    return valor


@router.get("/kpi-indicators/{indicador_id}/historical-values", response_model=List[ValorKPIHistoricoResponse])
def get_historical_values_by_kpi(
    indicador_id: str, 
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get historical KPI values for a specific indicator, optionally filtered by date range"""
    return get_valores_kpi_historico(db, indicador_id, fecha_inicio, fecha_fin, skip, limit)


@router.put("/kpi-historical-values/{valor_id}", response_model=ValorKPIHistoricoResponse)
def update_kpi_historical_value(
    valor_id: str, 
    valor_data: ValorKPIHistoricoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a historical KPI value"""
    updated_valor = update_valor_kpi_historico(
        db=db, 
        valor_id=valor_id, 
        valor_data=valor_data
    )
    if not updated_valor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historical KPI value not found"
        )
    return updated_valor


@router.delete("/kpi-historical-values/{valor_id}")
def delete_kpi_historical_value(valor_id: str, db: Session = Depends(get_db)):
    """Delete a historical KPI value"""
    success = delete_valor_kpi_historico(db=db, valor_id=valor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historical KPI value not found"
        )
    return {"message": "Historical KPI value deleted successfully"}