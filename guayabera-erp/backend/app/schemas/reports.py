"""
Reports Schemas: Generic reporting system for all ERP modules
Specialized for textile manufacturing companies
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
# REPORTES GENERALES SCHEMAS
# ============================================================================

class ReporteBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del reporte")
    titulo: str = Field(..., max_length=200, description="Título del reporte")
    descripcion: Optional[str] = Field(None, description="Descripción del reporte")
    tipo: str = Field(..., description="Tipo de reporte")
    modulo: str = Field(..., description="Módulo al que pertenece el reporte")
    parametros: Optional[Dict[str, Any]] = Field(None, description="Parámetros utilizados para generar el reporte")
    frecuencia: Optional[str] = Field("unica", description="Frecuencia de generación del reporte")
    formato_salida: Optional[str] = Field("pdf", description="Formato de salida del reporte")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del periodo del reporte")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin del periodo del reporte")
    estado: Optional[str] = Field("pendiente", description="Estado actual del reporte")
    generado_por_id: Optional[UUID4] = Field(None, description="ID del empleado que generó el reporte")
    fecha_generacion: Optional[datetime] = Field(None, description="Fecha de generación del reporte")
    archivo_url: Optional[str] = Field(None, max_length=500, description="URL del archivo generado")
    datos_reporte: Optional[Dict[str, Any]] = Field(None, description="Datos del reporte en formato JSON")
    activo: bool = Field(default=True, description="¿Está activo el reporte?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class ReporteCreate(ReporteBase):
    pass


class ReporteUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    parametros: Optional[Dict[str, Any]] = None
    fecha_generacion: Optional[datetime] = None
    archivo_url: Optional[str] = Field(None, max_length=500)
    comentarios: Optional[str] = None


class ReporteResponse(ReporteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORTES ESPECÍFICOS DE RH
# ============================================================================

class ReporteRHBase(BaseModel):
    reporte_id: UUID4
    empleado_id: Optional[UUID4] = Field(None, description="ID del empleado a filtrar")
    departamento_id: Optional[UUID4] = Field(None, description="ID del departamento a filtrar")
    puesto: Optional[str] = Field(None, max_length=100, description="Puesto a filtrar")
    fecha_contratacion_desde: Optional[date] = Field(None, description="Fecha mínima de contratación")
    fecha_contratacion_hasta: Optional[date] = Field(None, description="Fecha máxima de contratación")
    nomina_id: Optional[UUID4] = Field(None, description="ID de nómina a filtrar")
    periodo_inicio: Optional[date] = Field(None, description="Inicio del periodo de nómina")
    periodo_fin: Optional[date] = Field(None, description="Fin del periodo de nómina")
    tipo_nomina: Optional[str] = Field(None, description="Tipo de nómina")
    tipo_reporte_rh: str = Field(..., description="Tipo específico de reporte de RH")


class ReporteRHCreate(ReporteRHBase):
    pass


class ReporteRHUpdate(BaseModel):
    empleado_id: Optional[UUID4] = None
    departamento_id: Optional[UUID4] = None
    puesto: Optional[str] = None
    fecha_contratacion_desde: Optional[date] = None
    fecha_contratacion_hasta: Optional[date] = None
    nomina_id: Optional[UUID4] = None
    periodo_inicio: Optional[date] = None
    periodo_fin: Optional[date] = None
    tipo_nomina: Optional[str] = None
    tipo_reporte_rh: Optional[str] = None


class ReporteRHResponse(ReporteRHBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORTES ESPECÍFICOS DE PRODUCCIÓN
# ============================================================================

class ReporteProduccionBase(BaseModel):
    reporte_id: UUID4
    orden_produccion_id: Optional[UUID4] = Field(None, description="ID de la orden de producción a filtrar")
    fecha_inicio_desde: Optional[date] = Field(None, description="Fecha inicial mínima")
    fecha_inicio_hasta: Optional[date] = Field(None, description="Fecha inicial máxima")
    fecha_fin_desde: Optional[date] = Field(None, description="Fecha final mínima")
    fecha_fin_hasta: Optional[date] = Field(None, description="Fecha final máxima")
    estado_orden: Optional[str] = Field(None, description="Estado de la orden a filtrar")
    producto_id: Optional[UUID4] = Field(None, description="ID del producto a filtrar")
    categoria_producto_id: Optional[UUID4] = Field(None, description="ID de la categoría de producto a filtrar")
    proceso: Optional[str] = Field(None, description="Proceso a filtrar")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable a filtrar")
    tipo_reporte_prod: str = Field(..., description="Tipo específico de reporte de producción")


class ReporteProduccionCreate(ReporteProduccionBase):
    pass


class ReporteProduccionUpdate(BaseModel):
    orden_produccion_id: Optional[UUID4] = None
    fecha_inicio_desde: Optional[date] = None
    fecha_inicio_hasta: Optional[date] = None
    fecha_fin_desde: Optional[date] = None
    fecha_fin_hasta: Optional[date] = None
    estado_orden: Optional[str] = None
    producto_id: Optional[UUID4] = None
    categoria_producto_id: Optional[UUID4] = None
    proceso: Optional[str] = None
    responsable_id: Optional[UUID4] = None
    tipo_reporte_prod: Optional[str] = None


class ReporteProduccionResponse(ReporteProduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORTES ESPECÍFICOS DE VENTAS
# ============================================================================

class ReporteVentasBase(BaseModel):
    reporte_id: UUID4
    venta_id: Optional[UUID4] = Field(None, description="ID de la venta a filtrar")
    cliente_id: Optional[UUID4] = Field(None, description="ID del cliente a filtrar")
    vendedor_id: Optional[UUID4] = Field(None, description="ID del vendedor a filtrar")
    fecha_venta_desde: Optional[date] = Field(None, description="Fecha de venta mínima")
    fecha_venta_hasta: Optional[date] = Field(None, description="Fecha de venta máxima")
    estado_venta: Optional[str] = Field(None, description="Estado de la venta a filtrar")
    producto_id: Optional[UUID4] = Field(None, description="ID del producto a filtrar")
    categoria_producto_id: Optional[UUID4] = Field(None, description="ID de la categoría de producto a filtrar")
    tipo_reporte_venta: str = Field(..., description="Tipo específico de reporte de ventas")


class ReporteVentasCreate(ReporteVentasBase):
    pass


class ReporteVentasUpdate(BaseModel):
    venta_id: Optional[UUID4] = None
    cliente_id: Optional[UUID4] = None
    vendedor_id: Optional[UUID4] = None
    fecha_venta_desde: Optional[date] = None
    fecha_venta_hasta: Optional[date] = None
    estado_venta: Optional[str] = None
    producto_id: Optional[UUID4] = None
    categoria_producto_id: Optional[UUID4] = None
    tipo_reporte_venta: Optional[str] = None


class ReporteVentasResponse(ReporteVentasBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORTES ESPECÍFICOS DE INVENTARIO
# ============================================================================

class ReporteInventarioBase(BaseModel):
    reporte_id: UUID4
    producto_id: Optional[UUID4] = Field(None, description="ID del producto a filtrar")
    categoria_producto_id: Optional[UUID4] = Field(None, description="ID de la categoría de producto a filtrar")
    almacen_id: Optional[UUID4] = Field(None, description="ID del almacén a filtrar")
    fecha_ultima_revision_desde: Optional[date] = Field(None, description="Fecha de última revisión mínima")
    fecha_ultima_revision_hasta: Optional[date] = Field(None, description="Fecha de última revisión máxima")
    bajo_stock: Optional[bool] = Field(default=False, description="Filtro para productos con bajo stock")
    tipo_reporte_inv: str = Field(..., description="Tipo específico de reporte de inventario")


class ReporteInventarioCreate(ReporteInventarioBase):
    pass


class ReporteInventarioUpdate(BaseModel):
    producto_id: Optional[UUID4] = None
    categoria_producto_id: Optional[UUID4] = None
    almacen_id: Optional[UUID4] = None
    fecha_ultima_revision_desde: Optional[date] = None
    fecha_ultima_revision_hasta: Optional[date] = None
    bajo_stock: Optional[bool] = None
    tipo_reporte_inv: Optional[str] = None


class ReporteInventarioResponse(ReporteInventarioBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REPORTES ESPECÍFICOS DE FINANZAS
# ============================================================================

class ReporteFinanzasBase(BaseModel):
    reporte_id: UUID4
    cuenta_id: Optional[UUID4] = Field(None, description="ID de la cuenta a filtrar")
    poliza_id: Optional[UUID4] = Field(None, description="ID de la póliza a filtrar")
    fecha_contable_desde: Optional[date] = Field(None, description="Fecha contable mínima")
    fecha_contable_hasta: Optional[date] = Field(None, description="Fecha contable máxima")
    tipo_reporte_fin: str = Field(..., description="Tipo específico de reporte de finanzas")


class ReporteFinanzasCreate(ReporteFinanzasBase):
    pass


class ReporteFinanzasUpdate(BaseModel):
    cuenta_id: Optional[UUID4] = None
    poliza_id: Optional[UUID4] = None
    fecha_contable_desde: Optional[date] = None
    fecha_contable_hasta: Optional[date] = None
    tipo_reporte_fin: Optional[str] = None


class ReporteFinanzasResponse(ReporteFinanzasBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS ESPECÍFICOS DE REPORTES Y DASHBOARD
# ============================================================================

class DashboardWidgetBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del widget")
    tipo: str = Field(..., max_length=50, description="Tipo de widget")
    configuracion: Optional[Dict[str, Any]] = Field(None, description="Configuración específica del widget")
    posicion_x: int = Field(default=0, description="Posición X en el grid")
    posicion_y: int = Field(default=0, description="Posición Y en el grid")
    tamano_w: int = Field(default=4, description="Ancho del widget")
    tamano_h: int = Field(default=3, description="Alto del widget")
    modulo_origen: Optional[str] = Field(None, max_length=50, description="Módulo del cual obtiene datos")
    empresa_id: Optional[UUID4] = Field(None, description="ID de la empresa (para multiempresa)")


class DashboardWidgetCreate(DashboardWidgetBase):
    pass


class DashboardWidgetUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    tipo: Optional[str] = Field(None, max_length=50)
    configuracion: Optional[Dict[str, Any]] = None
    posicion_x: Optional[int] = None
    posicion_y: Optional[int] = None
    tamano_w: Optional[int] = None
    tamano_h: Optional[int] = None
    modulo_origen: Optional[str] = Field(None, max_length=50)
    empresa_id: Optional[UUID4] = None
    activo: Optional[bool] = None


class DashboardWidgetResponse(DashboardWidgetBase):
    id: UUID4
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportePersonalizadoBase(BaseModel):
    nombre: str = Field(..., max_length=200, description="Nombre del reporte")
    descripcion: Optional[str] = Field(None, description="Descripción del reporte")
    modulo: str = Field(..., max_length=50, description="Módulo al que pertenece")
    tipo: str = Field(..., max_length=50, description="Tipo de reporte")
    consulta_sql: Optional[str] = Field(None, description="Consulta SQL personalizada")
    parametros: Optional[Dict[str, Any]] = Field(None, description="Parámetros del reporte")
    formato_salida: str = Field(default="pdf", max_length=20, description="Formato de salida del reporte")
    empresa_id: Optional[UUID4] = Field(None, description="ID de la empresa (para multiempresa)")


class ReportePersonalizadoCreate(ReportePersonalizadoBase):
    pass


class ReportePersonalizadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    modulo: Optional[str] = Field(None, max_length=50)
    tipo: Optional[str] = Field(None, max_length=50)
    consulta_sql: Optional[str] = None
    parametros: Optional[Dict[str, Any]] = None
    formato_salida: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None
    empresa_id: Optional[UUID4] = None


class ReportePersonalizadoResponse(ReportePersonalizadoBase):
    id: UUID4
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistoricoReporteBase(BaseModel):
    reporte_id: UUID4
    usuario_ejecutor_id: UUID4
    parametros_utilizados: Optional[Dict[str, Any]] = None
    duracion_segundos: Optional[float] = None
    tamano_bytes: Optional[int] = None
    ruta_archivo: Optional[str] = Field(None, max_length=500)
    estado: str = Field(default="procesando", max_length=20)
    mensaje_error: Optional[str] = None


class HistoricoReporteCreate(HistoricoReporteBase):
    pass


class HistoricoReporteUpdate(BaseModel):
    parametros_utilizados: Optional[Dict[str, Any]] = None
    duracion_segundos: Optional[float] = None
    tamano_bytes: Optional[int] = None
    ruta_archivo: Optional[str] = Field(None, max_length=500)
    estado: Optional[str] = Field(None, max_length=20)
    mensaje_error: Optional[str] = None


class HistoricoReporteResponse(HistoricoReporteBase):
    id: UUID4
    fecha_ejecucion: datetime
    created_at: datetime

    class Config:
        from_attributes = True
