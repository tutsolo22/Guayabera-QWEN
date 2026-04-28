"""
Reports Models: Generic reporting system for all ERP modules
Specialized for textile manufacturing companies
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoReporte(enum.Enum):
    ESTADISTICO = "estadistico"
    ANALITICO = "analitico"
    OPERATIVO = "operativo"
    FINANCIERO = "financiero"
    COMERCIAL = "comercial"
    CONTROL = "control"


class FrecuenciaGeneracion(enum.Enum):
    UNICA = "unica"
    DIARIA = "diaria"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    BIMESTRAL = "bimestral"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"


class FormatoReporte(enum.Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"
    JSON = "json"


class EstadoReporte(enum.Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADO = "completado"
    ERROR = "error"
    CANCELADO = "cancelado"


# ============================================================================
# REPORTES GENERALES
# ============================================================================

class Reporte(Base):
    """Generic report model for all ERP modules - Modelo de reporte genérico para todos los módulos del ERP"""
    __tablename__ = "rep_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # REP-2023-001
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Type and module
    tipo = Column(SQLEnum(TipoReporte), nullable=False)
    modulo = Column(String(50), nullable=False)  # rh, finance, production, sales, etc.
    
    # Filters and parameters
    parametros = Column(JSONB)  # Filters and parameters used to generate the report
    
    # Generation info
    frecuencia = Column(SQLEnum(FrecuenciaGeneracion), default=FrecuenciaGeneracion.UNICA)
    formato_salida = Column(SQLEnum(FormatoReporte), default=FormatoReporte.PDF)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    
    # Status and processing
    estado = Column(SQLEnum(EstadoReporte), default=EstadoReporte.PENDIENTE)
    generado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    fecha_generacion = Column(DateTime(timezone=True))
    
    # Output
    archivo_url = Column(String(500))  # URL to the generated report file
    datos_reporte = Column(JSONB)  # Report data in JSON format
    
    # Metadata
    activo = Column(Boolean, default=True)
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    generado_por = relationship("Empleado")


# ============================================================================
# REPORTES ESPECÍFICOS POR MÓDULO
# ============================================================================

class ReporteRH(Base):
    """Human Resources specific reports - Reportes específicos de Recursos Humanos"""
    __tablename__ = "rep_rh_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte.id"), nullable=False)
    
    # Employee search filters
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))
    puesto = Column(String(100))
    fecha_contratacion_desde = Column(Date)
    fecha_contratacion_hasta = Column(Date)
    
    # Payroll filters
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("nom_nomina.id"))
    periodo_inicio = Column(Date)
    periodo_fin = Column(Date)
    tipo_nomina = Column(String(50))
    
    # Report type
    tipo_reporte_rh = Column(String(100), nullable=False)  # empleado_detalle, nomina_detalle, asistencia, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reporte = relationship("Reporte")
    empleado = relationship("Empleado")
    departamento = relationship("Departamento")
    nomina = relationship("Nomina")


class ReporteProduccion(Base):
    """Production specific reports - Reportes específicos de Producción"""
    __tablename__ = "rep_prod_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte.id"), nullable=False)
    
    # Production order filters
    orden_produccion_id = Column(UUID(as_uuid=True), ForeignKey("prod_orden_produccion.id"))
    fecha_inicio_desde = Column(Date)
    fecha_inicio_hasta = Column(Date)
    fecha_fin_desde = Column(Date)
    fecha_fin_hasta = Column(Date)
    estado_orden = Column(String(50))
    
    # Product filters
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))
    categoria_producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_categoria.id"))
    
    # Process filters
    proceso = Column(String(100))
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Report type
    tipo_reporte_prod = Column(String(100), nullable=False)  # orden_detalle, proceso_detalle, eficiencia, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reporte = relationship("Reporte")
    orden_produccion = relationship("OrdenProduccion")
    producto = relationship("Producto")
    categoria_producto = relationship("Categoria")
    responsable = relationship("Empleado")


class ReporteVentas(Base):
    """Sales specific reports - Reportes específicos de Ventas"""
    __tablename__ = "rep_ventas_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte.id"), nullable=False)
    
    # Sale filters
    venta_id = Column(UUID(as_uuid=True), ForeignKey("ventas_venta.id"))
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"))
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    fecha_venta_desde = Column(Date)
    fecha_venta_hasta = Column(Date)
    estado_venta = Column(String(50))
    
    # Product filters
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))
    categoria_producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_categoria.id"))
    
    # Report type
    tipo_reporte_venta = Column(String(100), nullable=False)  # venta_detalle, cliente_detalle, producto_detalle, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reporte = relationship("Reporte")
    venta = relationship("Venta")
    cliente = relationship("Cliente")
    vendedor = relationship("Empleado")
    producto = relationship("Producto")
    categoria_producto = relationship("Categoria")


class ReporteInventario(Base):
    """Inventory specific reports - Reportes específicos de Inventario"""
    __tablename__ = "rep_inv_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte.id"), nullable=False)
    
    # Product filters
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))
    categoria_producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_categoria.id"))
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"))
    
    # Inventory filters
    fecha_ultima_revision_desde = Column(Date)
    fecha_ultima_revision_hasta = Column(Date)
    bajo_stock = Column(Boolean, default=False)
    
    # Report type
    tipo_reporte_inv = Column(String(100), nullable=False)  # existencias, movimientos, valorizacion, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reporte = relationship("Reporte")
    producto = relationship("Producto")
    categoria_producto = relationship("Categoria")
    almacen = relationship("Almacen")


class ReporteFinanzas(Base):
    """Financial specific reports - Reportes específicos de Finanzas"""
    __tablename__ = "rep_fin_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte.id"), nullable=False)
    
    # Financial filters
    cuenta_id = Column(UUID(as_uuid=True), ForeignKey("cont_cuenta.id"))
    poliza_id = Column(UUID(as_uuid=True), ForeignKey("cont_poliza.id"))
    fecha_contable_desde = Column(Date)
    fecha_contable_hasta = Column(Date)
    
    # Report type
    tipo_reporte_fin = Column(String(100), nullable=False)  # balance, estado_result, polizas_detalle, etc.
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reporte = relationship("Reporte")
    cuenta = relationship("Cuenta")
    poliza = relationship("Poliza")


# ============================================================================
# MODELOS ESPECÍFICOS DE REPORTES Y DASHBOARD
# ============================================================================

class DashboardWidget(Base):
    """Widgets del dashboard ejecutivo - Executive dashboard widgets"""
    __tablename__ = "rep_dashboard_widget"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # grafica_barras, grafica_lineas, grafica_pie, metrica, tabla, etc.
    configuracion = Column(JSONB)  # Configuración específica del widget
    posicion_x = Column(Integer, default=0)
    posicion_y = Column(Integer, default=0)
    tamano_w = Column(Integer, default=4)  # Ancho en unidades de grid
    tamano_h = Column(Integer, default=3)  # Alto en unidades de grid
    modulo_origen = Column(String(50))  # Módulo del cual obtiene datos
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("emp_empresa.id"))  # Para multiempresa
    
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ReportePersonalizado(Base):
    """Definición de reportes personalizados - Custom report definitions"""
    __tablename__ = "rep_reporte_personalizado"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    modulo = Column(String(50), nullable=False)  # rh, ventas, produccion, etc.
    tipo = Column(String(50), nullable=False)  # analisis, operacional, financiero, fiscal
    consulta_sql = Column(Text)  # Consulta SQL personalizada
    parametros = Column(JSONB)  # Parámetros del reporte
    formato_salida = Column(String(20), default="pdf")  # pdf, excel, csv, html
    activo = Column(Boolean, default=True)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("emp_empresa.id"))  # Para multiempresa
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HistoricoReporte(Base):
    """Historial de ejecución de reportes - Report execution history"""
    __tablename__ = "rep_historico_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("rep_reporte_personalizado.id"), nullable=False)
    usuario_ejecutor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    parametros_utilizados = Column(JSONB)  # Parámetros usados en la ejecución
    fecha_ejecucion = Column(DateTime(timezone=True), server_default=func.now())
    duracion_segundos = Column(Float)  # Tiempo que tomó generar el reporte
    tamano_bytes = Column(Integer)  # Tamaño del archivo generado
    ruta_archivo = Column(String(500))  # Ruta donde se guardó el archivo
    estado = Column(String(20), default="procesando")  # procesando, completado, fallido
    mensaje_error = Column(Text)  # En caso de error
    
    reporte = relationship("ReportePersonalizado")
    usuario = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

