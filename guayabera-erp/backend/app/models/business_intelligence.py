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
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))
    
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
    """Business Intelligence Dashboard - PanelI'll create new models for business intelligence reports based on the reference solution. The changes will include creating new model files and classes for BI reports, dashboards, predictive analysis, KPIs, and KPI history.

backend/app/models/business_intelligence.py
```python
<<<<<<< SEARCH
# All existing content in the file will be replaced with the new BI models
"""
Business Intelligence Models: Reports, data analysis, and dashboards for decision making
Specialized for textile manufacturing analytics
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum, 
                        UniqueConstraint, Index, LargeBinary)
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


class FrecuenciaActualizacion(enum.Enum):
    MANUAL = "manual"
    DIARIA = "diaria"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"


class TipoVisualizacion(enum.Enum):
    TABLA = "tabla"
    GRAFICO_BARRAS = "grafico_barras"
    GRAFICO_LINEAS = "grafico_lineas"
    GRAFICO_CIRCULAR = "grafico_circular"
    GRAFICO_AREA = "grafico_area"
    MAPA = "mapa"
    INDICADOR = "indicador"
    MATRIZ = "matriz"


class EstadoInforme(enum.Enum):
    BORRADOR = "borrador"
    PROGRAMADO = "programado"
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    ARCHIVADO = "archivado"


class NivelAcceso(enum.Enum):
    PUBLICO = "publico"
    PRIVADO = "privado"
    DEPARTAMENTAL = "departamental"
    RESTRINGIDO = "restringido"


# ============================================================================
# BUSINESS INTELLIGENCE MODELS
# ============================================================================

class ReporteBI(Base):
    """Reporte de Business Intelligence - BI Report"""
    __tablename__ = "bi_reportes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)  # Título del reporte
    descripcion = Column(Text)  # Descripción del reporte
    tipo = Column(String(50), nullable=False)  # tipo de reporte: ventas, finanzas, etc.
    query_sql = Column(Text, nullable=False)  # Consulta SQL del reporte
    parametros = Column(JSONB)  # Parámetros del reporte
    activo = Column(Boolean, default=True)  # Si el reporte está activo
    creador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Quién creó el reporte
    
    creador = relationship("Empleado")
    widgets = relationship("WidgetDashboard", back_populates="reporte")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WidgetDashboard(Base):
    """Widget de Dashboard - Dashboard Widget"""
    __tablename__ = "bi_widgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)  # Título del widget
    tipo = Column(String(50), nullable=False)  # tipo de widget: gráfico, métrica, tabla, etc.
    posicion_x = Column(Integer, default=0)  # Posición X en el dashboard
    posicion_y = Column(Integer, default=0)  # Posición Y en el dashboard
    ancho = Column(Integer, default=4)  # Ancho del widget
    alto = Column(Integer, default=3)  # Alto del widget
    configuracion = Column(JSONB)  # Configuración específica del widget
    reporte_id = Column(UUID(as_uuid=True), ForeignKey("bi_reportes.id"))  # Reporte asociado
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("bi_dashboards.id"), nullable=False)  # Dashboard al que pertenece
    
    reporte = relationship("ReporteBI", back_populates="widgets")
    dashboard = relationship("DashboardBI", back_populates="widgets")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DashboardBI(Base):
    """Dashboard de Business Intelligence - BI Dashboard"""
    __tablename__ = "bi_dashboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)  # Título del dashboard
    descripcion = Column(Text)  # Descripción del dashboard
    es_publico = Column(Boolean, default=False)  # Si el dashboard es público
    propietario_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Dueño del dashboard
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # Departamento al que pertenece
    
    propietario = relationship("Empleado")
    departamento = relationship("Departamento")
    widgets = relationship("WidgetDashboard", back_populates="dashboard")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AnalisisPredictivo(Base):
    """Análisis predictivo - Predictive Analysis"""
    __tablename__ = "bi_analisis_predictivo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)  # Título del análisis
    descripcion = Column(Text)  # Descripción del análisis
    tipo_modelo = Column(String(50), nullable=False)  # Tipo de modelo predictivo
    formula = Column(Text, nullable=False)  # Fórmula del modelo
    activo = Column(Boolean, default=True)  # Si el análisis está activo
    ultimo_entrenamiento = Column(DateTime(timezone=True))  # Fecha del último entrenamiento
    precision_modelo = Column(Float)  # Precisión del modelo
    creador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Quién creó el análisis
    
    creador = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Kpi(Base):
    """Indicador clave de desempeño - Key Performance Indicator"""
    __tablename__ = "bi_kpis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)  # Título del KPI
    descripcion = Column(Text)  # Descripción del KPI
    formula = Column(Text, nullable=False)  # Fórmula de cálculo del KPI
    unidad_medida = Column(String(50))  # Unidad de medida del KPI
    frecuencia_calculo = Column(String(20), default='diaria')  # Frecuencia de cálculo
    meta_valor = Column(Numeric(15, 4))  # Valor objetivo del KPI
    umbral_alerta = Column(Numeric(15, 4))  # Umbral para alertas
    activo = Column(Boolean, default=True)  # Si el KPI está activo
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsable del KPI
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # Departamento responsable
    
    responsable = relationship("Empleado")
    departamento = relationship("Departamento")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HistoricoKpi(Base):
    """Histórico de valores de KPI - KPI History"""
    __tablename__ = "bi_historico_kpis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("bi_kpis.id"), nullable=False)  # KPI relacionado
    valor = Column(Numeric(15, 4), nullable=False)  # Valor del KPI
    fecha_registro = Column(Date, nullable=False)  # Fecha del registro
    fuente_datos = Column(String(100))  # Fuente de los datos
    
    kpi = relationship("Kpi")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
"""
Business Intelligence Models: Reports, data analysis, and dashboards for decision making
Specialized for textile manufacturing analytics
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


class FrecuenciaActualizacion(enum.Enum):
    MANUAL = "manual"
    DIARIA = "diaria"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"


class TipoVisualizacion(enum.Enum):
    TABLA = "tabla"
    GRAFICO_BARRAS = "grafico_barras"
    GRAFICO_LINEAS = "grafico_lineas"
    GRAFICO_CIRCULAR = "grafico_circular"
    GRAFICO_AREA = "grafico_area"
    MAPA = "mapa"
    INDICADOR = "indicador"
    MATRIZ = "matriz"


class EstadoInforme(enum.Enum):
    BORRADOR = "borrador"
    PROGRAMADO = "programado"
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    ARCHIVADO = "archivado"


class NivelAcceso(enum.Enum):
    PUBLICO = "publico"
    PRIVADO = "privado"
    DEPARTAMENTAL = "departamental"
    RESTRINGIDO = "restringido"


# ============================================================================
# BUSINESS INTELLIGENCE MODELS
# ============================================================================

class InformeBI(Base):
    """Business intelligence report - Informe de inteligencia de negocio"""
    __tablename__ = "bi_informe"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Report identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # BI-VENTAS-001
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Report configuration
    tipo_reporte = Column(SQLEnum(TipoReporte), nullable=False)
    nivel_acceso = Column(SQLEnum(NivelAcceso), default=NivelAcceso.PRIVADO)
    frecuencia_actualizacion = Column(SQLEnum(FrecuenciaActualizacion), default=FrecuenciaActualizacion.MENSUAL)
    
    # Ownership
    creador_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"), nullable=False)
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))
    
    # Configuration
    parametros_configuracion = Column(JSONB)  # Parameters for the report
    consulta_sql = Column(Text)  # SQL query for the report
    fuente_datos = Column(String(100))  # Source of the data
    
    # Status and scheduling
    estado = Column(SQLEnum(EstadoInforme), default=EstadoInforme.BORRADOR)
    fecha_ultima_ejecucion = Column(DateTime(timezone=True))
    fecha_proxima_ejecucion = Column(DateTime(timezone=True))
    
    # Metadata
    etiquetas = Column(String(255))  # Tags for the report
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    creador = relationship("Usuario")
    departamento = relationship("Departamento")
    visualizaciones = relationship("VisualizacionInforme", back_populates="informe")
    ejecuciones = relationship("EjecucionInforme", back_populates="informe")


class VisualizacionInforme(Base):
    """Report visualization - Visualización del informe"""
    __tablename__ = "bi_visualizacion_informe"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    informe_id = Column(UUID(as_uuid=True), ForeignKey("bi_informe.id"), nullable=False)
    
    # Visualization configuration
    titulo = Column(String(150), nullable=False)
    tipo_visualizacion = Column(SQLEnum(TipoVisualizacion), nullable=False)
    configuracion_visualizacion = Column(JSONB)  # Configuration for the visualization
    posicion_x = Column(Integer, default=0)  # Position in dashboard
    posicion_y = Column(Integer, default=0)
    ancho = Column(Integer, default=4)  # Width in dashboard grid
    alto = Column(Integer, default=3)  # Height in dashboard grid
    
    # Filters and dimensions
    dimensiones = Column(JSONB)  # Dimensions for the visualization
    filtros = Column(JSONB)  # Filters for the visualization
    metricas = Column(JSONB)  # Metrics for the visualization
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    informe = relationship("InformeBI", back_populates="visualizaciones")


class Dashboard(Base):
    """Business intelligence dashboard - Panel de control de inteligencia de negocio"""
    __tablename__ = "bi_dashboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dashboard identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # DASH-VENTAS-001
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Ownership
    creador_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"), nullable=False)
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))
    
    # Configuration
    configuracion_layout = Column(JSONB)  # Layout configuration
    nivel_acceso = Column(SQLEnum(NivelAcceso), default=NivelAcceso.PRIVADO)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    etiquetas = Column(String(255))  # Tags for the dashboard
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    creador = relationship("Usuario")
    departamento = relationship("Departamento")
    widgets = relationship("WidgetDashboard", back_populates="dashboard")


class WidgetDashboard(Base):
    """Dashboard widget - Widget del panel de control"""
    __tablename__ = "bi_widget_dashboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("bi_dashboard.id"), nullable=False)
    informe_id = Column(UUID(as_uuid=True), ForeignKey("bi_informe.id"), nullable=False)
    
    # Widget configuration
    titulo = Column(String(150), nullable=False)
    posicion_x = Column(Integer, default=0)  # Position in dashboard
    posicion_y = Column(Integer, default=0)
    ancho = Column(Integer, default=4)  # Width in dashboard grid
    alto = Column(Integer, default=3)  # Height in dashboard grid
    configuracion = Column(JSONB)  # Specific configuration for this widget
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")
    informe = relationship("InformeBI")


class EjecucionInforme(Base):
    """Report execution - Ejecución del informe"""
    __tablename__ = "bi_ejecucion_informe"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    informe_id = Column(UUID(as_uuid=True), ForeignKey("bi_informe.id"), nullable=False)
    ejecutado_por_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))
    
    # Execution details
    fecha_ejecucion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    duracion_ejecucion_ms = Column(Integer)  # Duration in milliseconds
    estado_ejecucion = Column(String(50))  # Success, error, timeout
    mensaje_error = Column(Text)  # Error message if failed
    
    # Results metadata
    filas_resultado = Column(Integer)  # Number of rows returned
    columnas_resultado = Column(Integer)  # Number of columns returned
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    informe = relationship("InformeBI", back_populates="ejecuciones")
    ejecutado_por = relationship("Usuario")


class IndicadorKPI(Base):
    """Key Performance Indicator - Indicador de desempeño clave"""
    __tablename__ = "bi_indicador_kpi"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # KPI identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # KPI-VENTAS-001
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # KPI configuration
    tipo_indicador = Column(SQLEnum(TipoReporte), nullable=False)  # Associated report type
    formula_calculo = Column(Text)  # Formula to calculate the KPI
    fuente_datos = Column(String(100))  # Data source for the KPI
    frecuencia_actualizacion = Column(SQLEnum(FrecuenciaActualizacion), default=FrecuenciaActualizacion.DIARIA)
    
    # Ownership
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))
    
    # Thresholds and targets
    valor_objetivo = Column(Numeric(12, 4))  # Target value
    umbral_minimo = Column(Numeric(12, 4))  # Minimum threshold
    umbral_maximo = Column(Numeric(12, 4))  # Maximum threshold
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    responsable = relationship("Empleado")
    departamento = relationship("Departamento")
    valores_historicos = relationship("ValorKPIHistorico", back_populates="indicador")


class ValorKPIHistorico(Base):
    """Historical KPI value - Valor histórico del indicador KPI"""
    __tablename__ = "bi_valor_kpi_historico"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicador_id = Column(UUID(as_uuid=True), ForeignKey("bi_indicador_kpi.id"), nullable=False)
    
    # Value details
    valor = Column(Numeric(12, 4), nullable=False)
    fecha_registro = Column(Date, nullable=False, server_default=func.current_date())
    periodo_referencia = Column(String(20))  # Daily, weekly, monthly, etc.
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    indicador = relationship("IndicadorKPI", back_populates="valores_historicos")