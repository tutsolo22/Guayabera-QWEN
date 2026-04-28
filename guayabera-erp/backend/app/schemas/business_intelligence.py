from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


class ReporteBIBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del reporte")
    descripcion: Optional[str] = Field(None, description="Descripción del reporte")
    tipo: str = Field(..., max_length=50, description="Tipo de reporte")
    query_sql: str = Field(..., description="Consulta SQL del reporte")
    parametros: Optional[Dict[str, Any]] = Field(None, description="Parámetros del reporte")
    activo: bool = Field(default=True, description="Si el reporte está activo")
    creador_id: UUID4 = Field(..., description="ID del empleado que creó el reporte")


class ReporteBICreate(ReporteBIBase):
    pass


class ReporteBIUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo: Optional[str] = Field(None, max_length=50)
    query_sql: Optional[str] = None
    parametros: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class ReporteBIResponse(ReporteBIBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WidgetDashboardBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del widget")
    tipo: str = Field(..., max_length=50, description="Tipo de widget")
    posicion_x: int = Field(default=0, description="Posición X en el dashboard")
    posicion_y: int = Field(default=0, description="Posición Y en el dashboard")
    ancho: int = Field(default=4, description="Ancho del widget")
    alto: int = Field(default=3, description="Alto del widget")
    configuracion: Optional[Dict[str, Any]] = Field(None, description="Configuración específica del widget")
    reporte_id: Optional[UUID4] = Field(None, description="Reporte asociado al widget")
    dashboard_id: UUID4 = Field(..., description="Dashboard al que pertenece el widget")


class WidgetDashboardCreate(WidgetDashboardBase):
    pass


class WidgetDashboardUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    tipo: Optional[str] = Field(None, max_length=50)
    posicion_x: Optional[int] = None
    posicion_y: Optional[int] = None
    ancho: Optional[int] = None
    alto: Optional[int] = None
    configuracion: Optional[Dict[str, Any]] = None
    reporte_id: Optional[UUID4] = None
    dashboard_id: Optional[UUID4] = None


class WidgetDashboardResponse(WidgetDashboardBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DashboardBIBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del dashboard")
    descripcion: Optional[str] = Field(None, description="Descripción del dashboard")
    es_publico: bool = Field(default=False, description="Si el dashboard es público")
    propietario_id: UUID4 = Field(..., description="Dueño del dashboard")
    departamento_id: Optional[UUID4] = Field(None, description="Departamento al que pertenece")


class DashboardBICreate(DashboardBIBase):
    pass


class DashboardBIUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    es_publico: Optional[bool] = None
    propietario_id: Optional[UUID4] = None
    departamento_id: Optional[UUID4] = None


class DashboardBIResponse(DashboardBIBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnalisisPredictivoBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del análisis")
    descripcion: Optional[str] = Field(None, description="Descripción del análisis")
    tipo_modelo: str = Field(..., max_length=50, description="Tipo de modelo predictivo")
    formula: str = Field(..., description="Fórmula del modelo")
    activo: bool = Field(default=True, description="Si el análisis está activo")
    ultimo_entrenamiento: Optional[datetime] = Field(None, description="Fecha del último entrenamiento")
    precision_modelo: Optional[float] = Field(None, description="Precisión del modelo")
    creador_id: UUID4 = Field(..., description="Quién creó el análisis")


class AnalisisPredictivoCreate(AnalisisPredictivoBase):
    pass


class AnalisisPredictivoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo_modelo: Optional[str] = Field(None, max_length=50)
    formula: Optional[str] = None
    activo: Optional[bool] = None
    ultimo_entrenamiento: Optional[datetime] = None
    precision_modelo: Optional[float] = None


class AnalisisPredictivoResponse(AnalisisPredictivoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KpiBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del KPI")
    descripcion: Optional[str] = Field(None, description="Descripción del KPI")
    formula: str = Field(..., description="Fórmula de cálculo del KPI")
    unidad_medida: Optional[str] = Field(None, max_length=50, description="Unidad de medida del KPI")
    frecuencia_calculo: str = Field(default='diaria', max_length=20, description="Frecuencia de cálculo")
    meta_valor: Optional[Decimal] = Field(None, description="Valor objetivo del KPI")
    umbral_alerta: Optional[Decimal] = Field(None, description="Umbral para alertas")
    activo: bool = Field(default=True, description="Si el KPI está activo")
    responsable_id: Optional[UUID4] = Field(None, description="Responsable del KPI")
    departamento_id: Optional[UUID4] = Field(None, description="Departamento responsable")


class KpiCreate(KpiBase):
    pass


class KpiUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    formula: Optional[str] = None
    unidad_medida: Optional[str] = None
    frecuencia_calculo: Optional[str] = Field(None, max_length=20)
    meta_valor: Optional[Decimal] = None
    umbral_alerta: Optional[Decimal] = None
    activo: Optional[bool] = None
    responsable_id: Optional[UUID4] = None
    departamento_id: Optional[UUID4] = None


class KpiResponse(KpiBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistoricoKpiBase(BaseModel):
    kpi_id: UUID4 = Field(..., description="KPI relacionado")
    valor: Decimal = Field(..., description="Valor del KPI")
    fecha_registro: date = Field(..., description="Fecha del registro")
    fuente_datos: Optional[str] = Field(None, max_length=100, description="Fuente de los datos")


class HistoricoKpiCreate(HistoricoKpiBase):
    pass


class HistoricoKpiUpdate(BaseModel):
    valor: Optional[Decimal] = None
    fecha_registro: Optional[date] = None
    fuente_datos: Optional[str] = Field(None, max_length=100)


class HistoricoKpiResponse(HistoricoKpiBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True