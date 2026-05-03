"""
Business Intelligence Report Models
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class ReportType(enum.Enum):
    VENTAS = "ventas"
    FINANZAS = "finanzas"
    INVENTARIO = "inventario"
    PRODUCCION = "produccion"
    COMPRAS = "compras"
    CLIENTES = "clientes"
    PROVEEDORES = "proveedores"
    RRHH = "rrhh"
    CALIDAD = "calidad"
    ACTIVOS = "activos"
    GENERAL = "general"


class WidgetType(enum.Enum):
    TABLA = "tabla"
    GRAFICO_BARRAS = "grafico_barras"
    GRAFICO_LINEAS = "grafico_lineas"
    GRAFICO_CIRCULAR = "grafico_circular"
    GRAFICO_AREA = "grafico_area"
    MAPA = "mapa"
    INDICADOR = "indicador"
    MATRIZ = "matriz"


# ============================================================================
# BI REPORT MODELS
# ============================================================================

class ReporteBI(Base):
    """Business Intelligence Report - Informe de inteligencia de negocio"""
    __tablename__ = "bi_reportes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Report identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # REP-VENTAS-001
    titulo = Column(String(200), nullable=False)  # Título del reporte
    descripcion = Column(Text)  # Descripción del reporte
    
    # Report configuration
    tipo_reporte = Column(SQLEnum(ReportType), nullable=False)
    query_sql = Column(Text, nullable=False)  # Consulta SQL del reporte
    parametros = Column(JSONB)  # Parámetros del reporte
    fuente_datos = Column(String(100))  # Origen de los datos
    
    # Ownership
    creador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Quién creó el reporte
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))  # Changed from UUID to Integer to match departamentos
    
    # Status
    activo = Column(Boolean, default=True)  # Si el reporte está activo
    fecha_ultima_ejecucion = Column(DateTime(timezone=True))
    
    # Metadata
    etiquetas = Column(String(255))  # Etiquetas para categorizar
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    creador = relationship("Empleado")
    departamento = relationship("Departamento")
    widgets = relationship("WidgetDashboard", back_populates="reporte")
    ejecuciones = relationship("EjecucionReporte", back_populates="reporte")


class WidgetDashboard(Base):
    """Dashboard Widget - Widget para paneles de control"""
    __tablename__ = "bi_widgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Widget configuration
    titulo = Column(String(200), nullable=False)  # Título del widget
    tipo_widget = Column(SQLEnum(WidgetType), nullable=False)  # Tipo de widget
    posicion_x = Column(Integer, default=0)  # Posición X en el dashboard
    posicion_y = Column(Integer, default=0)  # Posición Y en el dashboard
    ancho = Column(Integer, default=4)  # Ancho del widget
    alto = Column(Integer, default=3)  # Alto del widget
    configuracion = Column(JSONB)  # Configuración específica del widget
    
    # Relationships
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("bi_reportes.id"))  # Reporte asociado
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("bi_dashboards.id"), nullable=False)  # Dashboard al que pertenece
    
    reporte = relationship("ReporteBI", back_populates="widgets")
    dashboard = relationship("DashboardBI", back_populates="widgets")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DashboardBI(Base):
    """Business Intelligence Dashboard - Panel de control de inteligencia de negocio"""
    __tablename__ = "bi_dashboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dashboard identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # DASH-VENTAS-001
    titulo = Column(String(200), nullable=False)  # Título del dashboard
    descripcion = Column(Text)  # Descripción del dashboard
    
    # Ownership
    creador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Quién creó el dashboard
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))  # Changed from UUID to Integer to match departamentos - Departamento al que pertenece
    
    # Configuration
    configuracion_layout = Column(JSONB)  # Configuración del layout del dashboard
    es_publico = Column(Boolean, default=False)  # Si el dashboard es público
    
    # Status
    activo = Column(Boolean, default=True)  # Si el dashboard está activo
    
    # Metadata
    etiquetas = Column(String(255))  # Etiquetas para categorizar
    comentarios = Column(Text)  # Comentarios sobre el dashboard
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    creador = relationship("Empleado")
    departamento = relationship("Departamento")
    widgets = relationship("WidgetDashboard", back_populates="dashboard")


class EjecucionReporte(Base):
    """Report execution - Ejecución del reporte"""
    __tablename__ = "bi_ejecuciones_reporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("bi_reportes.id"), nullable=False)
    ejecutado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Quién ejecutó el reporte
    
    # Execution details
    fecha_ejecucion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    duracion_ejecucion_ms = Column(Integer)  # Duración en milisegundos
    estado_ejecucion = Column(String(50))  # éxito, error, timeout
    mensaje_error = Column(Text)  # Mensaje de error si falló
    
    # Results metadata
    filas_resultado = Column(Integer)  # Número de filas devueltas
    columnas_resultado = Column(Integer)  # Número de columnas devueltas
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reporte = relationship("ReporteBI", back_populates="ejecuciones")
    ejecutado_por = relationship("Empleado")


class KPI(Base):
    """Key Performance Indicator - Indicador clave de desempeño"""
    __tablename__ = "bi_kpi"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    unidad_medida = Column(String(50))  # Porcentaje, unidades, pesos, etc.
    meta = Column(Numeric(12, 4))  # Valor objetivo del KPI
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Changed from Integer to UUID to match rh_empleado
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))  # Already correct - Departamento al que pertenece
    tipo_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi_tipos.id"))  # Changed from Integer to UUID to match bi_kpi_tipos
    formula_calculo = Column(Text)  # Fórmula utilizada para calcular el KPI
    frecuencia_calculo = Column(String(20), default="diaria")  # diaria, semanal, mensual
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    responsable = relationship("Empleado")
    departamento = relationship("Departamento")
    valores_historicos = relationship("ValorKPIHistorico", back_populates="kpi")
    alertas = relationship("AlertaKPI", back_populates="kpi")
    tipo_relacionado = relationship("KPITipo", back_populates="kpis")
    analisis_tendencias = relationship("AnalisisTrend", back_populates="kpi")
    valores_por_tipo = relationship("ValorKPITipo", back_populates="kpi")
    analisis_predictivos = relationship("AnalisisPredictivo", back_populates="kpi")


class ValorKPIHistorico(Base):
    """Historical KPI value - Valor histórico del indicador KPI"""
    __tablename__ = "bi_valor_kpi_historico"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi.id"), nullable=False)
    
    # Value details
    valor = Column(Numeric(12, 4), nullable=False)
    fecha_registro = Column(Date, nullable=False, server_default=func.current_date())
    periodo_referencia = Column(String(20))  # Diario, semanal, mensual, etc.
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    kpi = relationship("KPI", back_populates="valores_historicos")


class KPITipo(Base):
    """KPI types for classification - Tipos de KPI para clasificación"""
    __tablename__ = "bi_kpi_tipos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    nombre = Column(String(100), nullable=False)  # e.g., "Financiero", "Operativo", "Comercial"
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relaciones
    kpis = relationship("KPI", back_populates="tipo_relacionado")


class AlertaKPI(Base):
    """KPI alerts for threshold breaches - Alertas de KPI para incumplimientos de umbrales"""
    __tablename__ = "bi_alertas_kpi"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi.id"), nullable=False)
    tipo_alerta = Column(String(50), nullable=False)  # "umbral_superior", "umbral_inferior", "tendencia_negativa"
    valor_referencia = Column(Numeric(10, 4), nullable=False)
    valor_actual = Column(Numeric(10, 4))
    mensaje = Column(Text)
    leido = Column(Boolean, default=False)
    fecha_deteccion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    kpi = relationship("KPI", back_populates="alertas")


class DashboardPersonalizado(Base):
    """Custom dashboards for users - Dashboards personalizados para usuarios"""
    __tablename__ = "bi_dashboards_personalizados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from users to seg_usuario
    configuracion = Column(JSONB)  # Almacena la configuración del dashboard en formato JSON
    publico = Column(Boolean, default=False)  # Si es accesible por otros usuarios
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    usuario = relationship("Usuario")  # Changed from User to Usuario


class ReporteAutomatizado(Base):
    """Scheduled automated reports - Reportes automatizados programados"""
    __tablename__ = "bi_reportes_automaticos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    tipo_reporte = Column(String(100), nullable=False)  # "pdf", "excel", "dashboard"
    configuracion = Column(JSONB)  # Parámetros del reporte
    programacion = Column(String(100))  # "diaria", "semanal", "mensual"
    ultimo_envio = Column(DateTime(timezone=True))
    proximo_envio = Column(DateTime(timezone=True))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    destinatarios = relationship("ReporteDestinatario", back_populates="reporte")


class ReporteDestinatario(Base):
    """Recipients for automated reports - Destinatarios para reportes automatizados"""
    __tablename__ = "bi_reporte_destinatarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("bi_reportes_automaticos.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from users to seg_usuario
    metodo_envio = Column(String(50), default="email")  # "email", "notificacion"
    
    # Relaciones
    reporte = relationship("ReporteAutomatizado", back_populates="destinatarios")
    usuario = relationship("Usuario")  # Changed from User to Usuario


class AnalisisTrend(Base):
    """Trend analysis for business metrics - Análisis de tendencias para métricas de negocio"""
    __tablename__ = "bi_analisis_tendencias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi.id"), nullable=False)
    periodo_inicio = Column(Date, nullable=False)
    periodo_fin = Column(Date, nullable=False)
    tipo_tendencia = Column(String(50), nullable=False)  # "ascendente", "descendente", "estable", "volatil"
    descripcion = Column(Text)
    confianza = Column(Numeric(5, 4))  # Nivel de confianza del análisis (0.0000 a 1.0000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    kpi = relationship("KPI", back_populates="analisis_tendencias")


class ValorKPITipo(Base):
    """Values for KPI by type - Valores del KPI por tipo"""
    __tablename__ = "bi_valor_kpi_tipo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi.id"), nullable=False)
    tipo_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi_tipos.id"), nullable=False)  # Changed from Integer to UUID
    valor = Column(Numeric(10, 4), nullable=False)
    fecha_registro = Column(Date, nullable=False)
    
    # Relaciones
    kpi = relationship("KPI", back_populates="valores_por_tipo")
    tipo = relationship("KPITipo")


class AnalisisPredictivo(Base):
    """Predictive analysis for business metrics - Análisis predictivo para métricas de negocio"""
    __tablename__ = "bi_analisis_predictivo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed from Integer to UUID
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpi.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    tipo_modelo = Column(String(100), nullable=False)  # "regresion", "arima", "red_neuronal", etc.
    descripcion = Column(Text)
    prediccion_valor = Column(Numeric(12, 4))  # Valor predicho
    intervalo_confianza = Column(Numeric(5, 4))  # Intervalo de confianza (0.0000 a 1.0000)
    precision_modelo = Column(Numeric(5, 4))  # Precisión del modelo (0.0000 a 1.0000)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    kpi = relationship("KPI", back_populates="analisis_predictivos")
