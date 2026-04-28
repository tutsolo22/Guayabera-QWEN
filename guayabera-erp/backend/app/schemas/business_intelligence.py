"""
Business Intelligence Schemas: Reports, data analysis, and dashboards for decision making
Specialized for textile manufacturing analytics
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORT SCHEMAS
# ============================================================================

class InformeBIBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del informe")
    nombre: str = Field(..., max_length=150, description="Nombre del informe")
    descripcion: Optional[str] = Field(None, description="Descripción del informe")
    tipo_reporte: str = Field(..., description="Tipo de reporte")
    nivel_acceso: Optional[str] = Field(default="privado", description="Nivel de acceso del informe")
    frecuencia_actualizacion: Optional[str] = Field(default="mensual", description="Frecuencia de actualización")
    creador_id: UUID4 = Field(..., description="ID del usuario creador")
    departamento_id: Optional[UUID4] = Field(None, description="ID del departamento")
    parametros_configuracion: Optional[Dict[str, Any]] = Field(None, description="Parámetros de configuración del informe")
    consulta_sql: Optional[str] = Field(None, description="Consulta SQL del informe")
    fuente_datos: Optional[str] = Field(None, max_length=100, description="Fuente de datos del informe")
    estado: Optional[str] = Field(default="borrador", description="Estado del informe")
    etiquetas: Optional[str] = Field(None, max_length=255, description="Etiquetas del informe")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class InformeBICreate(InformeBIBase):
    pass


class InformeBIUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_reporte: Optional[str] = None
    nivel_acceso: Optional[str] = None
    frecuencia_actualizacion: Optional[str] = None
    departamento_id: Optional[UUID4] = None
    parametros_configuracion: Optional[Dict[str, Any]] = None
    consulta_sql: Optional[str] = None
    fuente_datos: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = None
    etiquetas: Optional[str] = Field(None, max_length=255)
    comentarios: Optional[str] = None


class InformeBIResponse(InformeBIBase):
    id: UUID4
    fecha_ultima_ejecucion: Optional[datetime] = None
    fecha_proxima_ejecucion: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORT VISUALIZATION SCHEMAS
# ============================================================================

class VisualizacionInformeBase(BaseModel):
    informe_id: UUID4
    titulo: str = Field(..., max_length=150, description="Título de la visualización")
    tipo_visualizacion: str = Field(..., description="Tipo de visualización")
    configuracion_visualizacion: Optional[Dict[str, Any]] = Field(None, description="Configuración de la visualización")
    posicion_x: Optional[int] = Field(default=0, description="Posición X en el dashboard")
    posicion_y: Optional[int] = Field(default=0, description="Posición Y en el dashboard")
    ancho: Optional[int] = Field(default=4, ge=1, le=12, description="Ancho en la cuadrícula del dashboard")
    alto: Optional[int] = Field(default=3, ge=1, le=12, description="Alto en la cuadrícula del dashboard")
    dimensiones: Optional[Dict[str, Any]] = Field(None, description="Dimensiones para la visualización")
    filtros: Optional[Dict[str, Any]] = Field(None, description="Filtros para la visualización")
    metricas: Optional[Dict[str, Any]] = Field(None, description="Métricas para la visualización")
    activo: bool = Field(default=True, description="¿Está activa la visualización?")


class VisualizacionInformeCreate(VisualizacionInformeBase):
    pass


class VisualizacionInformeUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=150)
    tipo_visualizacion: Optional[str] = None
    configuracion_visualizacion: Optional[Dict[str, Any]] = None
    posicion_x: Optional[int] = Field(None, ge=0)
    posicion_y: Optional[int] = Field(None, ge=0)
    ancho: Optional[int] = Field(None, ge=1, le=12)
    alto: Optional[int] = Field(None, ge=1, le=12)
    dimensiones: Optional[Dict[str, Any]] = None
    filtros: Optional[Dict[str, Any]] = None
    metricas: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class VisualizacionInformeResponse(VisualizacionInformeBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DASHBOARD SCHEMAS
# ============================================================================

class DashboardBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del dashboard")
    nombre: str = Field(..., max_length=150, description="Nombre del dashboard")
    descripcion: Optional[str] = Field(None, description="Descripción del dashboard")
    creador_id: UUID4 = Field(..., description="ID del usuario creador")
    departamento_id: Optional[UUID4] = Field(None, description="ID del departamento")
    configuracion_layout: Optional[Dict[str, Any]] = Field(None, description="Configuración del layout")
    nivel_acceso: Optional[str] = Field(default="privado", description="Nivel de acceso del dashboard")
    activo: bool = Field(default=True, description="¿Está activo el dashboard?")
    etiquetas: Optional[str] = Field(None, max_length=255, description="Etiquetas del dashboard")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class DashboardCreate(DashboardBase):
    pass


class DashboardUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    departamento_id: Optional[UUID4] = None
    configuracion_layout: Optional[Dict[str, Any]] = None
    nivel_acceso: Optional[str] = None
    activo: Optional[bool] = None
    etiquetas: Optional[str] = Field(None, max_length=255)
    comentarios: Optional[str] = None


class DashboardResponse(DashboardBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DASHBOARD WIDGET SCHEMAS
# ============================================================================

class WidgetDashboardBase(BaseModel):
    dashboard_id: UUID4
    informe_id: UUID4
    titulo: str = Field(..., max_length=150, description="Título del widget")
    posicion_x: Optional[int] = Field(default=0, description="Posición X en el dashboard")
    posicion_y: Optional[int] = Field(default=0, description="Posición Y en el dashboard")
    ancho: Optional[int] = Field(default=4, ge=1, le=12, description="Ancho en la cuadrícula del dashboard")
    alto: Optional[int] = Field(default=3, ge=1, le=12, description="Alto en la cuadrícula del dashboard")
    configuracion: Optional[Dict[str, Any]] = Field(None, description="Configuración específica del widget")
    activo: bool = Field(default=True, description="¿Está activo el widget?")


class WidgetDashboardCreate(WidgetDashboardBase):
    pass


class WidgetDashboardUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=150)
    posicion_x: Optional[int] = Field(None, ge=0)
    posicion_y: Optional[int] = Field(None, ge=0)
    ancho: Optional[int] = Field(None, ge=1, le=12)
    alto: Optional[int] = Field(None, ge=1, le=12)
    configuracion: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class WidgetDashboardResponse(WidgetDashboardBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORT EXECUTION SCHEMAS
# ============================================================================

class EjecucionInformeBase(BaseModel):
    informe_id: UUID4
    ejecutado_por_id: Optional[UUID4] = Field(None, description="ID del usuario que ejecutó")
    duracion_ejecucion_ms: Optional[int] = Field(None, ge=0, description="Duración de la ejecución en ms")
    estado_ejecucion: Optional[str] = Field(None, max_length=50, description="Estado de la ejecución")
    mensaje_error: Optional[str] = Field(None, description="Mensaje de error si falló")
    filas_resultado: Optional[int] = Field(None, ge=0, description="Número de filas del resultado")
    columnas_resultado: Optional[int] = Field(None, ge=0, description="Número de columnas del resultado")


class EjecucionInformeCreate(EjecucionInformeBase):
    pass


class EjecucionInformeUpdate(BaseModel):
    duracion_ejecucion_ms: Optional[int] = Field(None, ge=0)
    estado_ejecucion: Optional[str] = Field(None, max_length=50)
    mensaje_error: Optional[str] = None
    filas_resultado: Optional[int] = Field(None, ge=0)
    columnas_resultado: Optional[int] = Field(None, ge=0)


class EjecucionInformeResponse(EjecucionInformeBase):
    id: UUID4
    fecha_ejecucion: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# KPI INDICATOR SCHEMAS
# ============================================================================

class IndicadorKPIBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del KPI")
    nombre: str = Field(..., max_length=150, description="Nombre del KPI")
    descripcion: Optional[str] = Field(None, description="Descripción del KPI")
    tipo_indicador: str = Field(..., description="Tipo de indicador KPI")
    formula_calculo: Optional[str] = Field(None, description="Fórmula de cálculo del KPI")
    fuente_datos: Optional[str] = Field(None, max_length=100, description="Fuente de datos del KPI")
    frecuencia_actualizacion: Optional[str] = Field(default="diaria", description="Frecuencia de actualización del KPI")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable del KPI")
    departamento_id: Optional[UUID4] = Field(None, description="ID del departamento del KPI")
    valor_objetivo: Optional[Decimal] = Field(None, description="Valor objetivo del KPI")
    umbral_minimo: Optional[Decimal] = Field(None, description="Umbral mínimo del KPI")
    umbral_maximo: Optional[Decimal] = Field(None, description="Umbral máximo del KPI")
    activo: bool = Field(default=True, description="¿Está activo el KPI?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class IndicadorKPICreate(IndicadorKPIBase):
    pass


class IndicadorKPIUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_indicador: Optional[str] = None
    formula_calculo: Optional[str] = None
    fuente_datos: Optional[str] = Field(None, max_length=100)
    frecuencia_actualizacion: Optional[str] = None
    responsable_id: Optional[UUID4] = None
    departamento_id: Optional[UUID4] = None
    valor_objetivo: Optional[Decimal] = None
    umbral_minimo: Optional[Decimal] = None
    umbral_maximo: Optional[Decimal] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None


class IndicadorKPIResponse(IndicadorKPIBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# HISTORICAL KPI VALUE SCHEMAS
# ============================================================================

class ValorKPIHistoricoBase(BaseModel):
    indicador_id: UUID4
    valor: Decimal = Field(..., description="Valor del KPI")
    fecha_registro: date = Field(..., description="Fecha de registro del valor")
    periodo_referencia: Optional[str] = Field(None, max_length=20, description="Período de referencia")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class ValorKPIHistoricoCreate(ValorKPIHistoricoBase):
    pass


class ValorKPIHistoricoUpdate(BaseModel):
    valor: Optional[Decimal] = None
    fecha_registro: Optional[date] = None
    periodo_referencia: Optional[str] = Field(None, max_length=20)
    comentarios: Optional[str] = None


class ValorKPIHistoricoResponse(ValorKPIHistoricoBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True