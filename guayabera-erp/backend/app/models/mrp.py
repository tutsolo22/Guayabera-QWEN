from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum, 
                        UniqueConstraint, Index)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class Receta(Base):
    """Receta de producción - Recipe for manufacturing"""
    __tablename__ = "mrp_recetas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    nombre = Column(String(200), nullable=False)  # Nombre de la receta
    producto_final_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Producto resultante
    descripcion = Column(Text)  # Descripción de la receta
    rendimiento = Column(Numeric(10, 4), nullable=False)  # Cantidad de producto final producido
    activa = Column(Boolean, default=True)  # Si la receta está activa
    version = Column(Integer, default=1)  # Versión de la receta
    fecha_revision = Column(Date)  # Fecha de última revisión
    
    producto_final = relationship("Producto")
    ingredientes = relationship("IngredienteReceta", back_populates="receta")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class IngredienteReceta(Base):
    """Ingrediente en una receta - Ingredient in recipe"""
    __tablename__ = "mrp_ingredientes_receta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    receta_id = Column(UUID(as_uuid=True), ForeignKey("mrp_recetas.id"), nullable=False)
    ingrediente_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Producto que es ingrediente
    cantidad_requerida = Column(Numeric(10, 4), nullable=False)  # Cantidad necesaria del ingrediente
    unidad_medida = Column(String(20), nullable=False)  # Unidad de medida
    secuencia = Column(Integer, default=1)  # Orden de utilización en el proceso
    
    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Producto")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OrdenProduccion(Base):
    """Orden de producción - Production Order"""
    __tablename__ = "mrp_ordenes_produccion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    codigo = Column(String(50), unique=True, nullable=False)  # Código único de la orden
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Producto a fabricar
    cantidad_programada = Column(Numeric(10, 4), nullable=False)  # Cantidad a producir
    cantidad_real = Column(Numeric(10, 4), default=0)  # Cantidad realmente producida
    fecha_inicio = Column(Date, nullable=False)  # Fecha programada de inicio
    fecha_fin = Column(Date)  # Fecha programada de finalización
    fecha_inicio_real = Column(DateTime(timezone=True))  # Fecha real de inicio
    fecha_fin_real = Column(DateTime(timezone=True))  # Fecha real de finalización
    estado = Column(SQLEnum('pendiente', 'programada', 'en_progreso', 'completada', 'cancelada', name='orden_estado'), 
                    default='pendiente', nullable=False)  # Estado de la orden
    prioridad = Column(SQLEnum('baja', 'media', 'alta', 'urgente', name='prioridad_orden'), 
                       default='media', nullable=False)  # Prioridad de la orden
    observaciones = Column(Text)  # Observaciones sobre la orden
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsable de la orden
    
    producto = relationship("Producto")
    responsable = relationship("Empleado")
    materiales = relationship("ConsumoMaterial", back_populates="orden_produccion")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ConsumoMaterial(Base):
    """Consumo de material en producción - Material consumption"""
    __tablename__ = "mrp_consumo_material"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    orden_produccion_id = Column(UUID(as_uuid=True), ForeignKey("mrp_ordenes_produccion.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Material consumido
    cantidad_requerida = Column(Numeric(10, 4), nullable=False)  # Cantidad requerida
    cantidad_consumida = Column(Numeric(10, 4), default=0)  # Cantidad realmente consumida
    unidad_medida = Column(String(20), nullable=False)  # Unidad de medida
    fecha_consumo = Column(Date)  # Fecha de consumo
    
    orden_produccion = relationship("OrdenProduccion", back_populates="materiales")
    producto = relationship("Producto")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PrevisionDemanda(Base):
    """Previsión de demanda - Demand forecast"""
    __tablename__ = "mrp_prevision_demanda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Producto previsto
    periodo_inicio = Column(Date, nullable=False)  # Fecha de inicio del período
    periodo_fin = Column(Date, nullable=False)  # Fecha de fin del período
    cantidad_prevista = Column(Numeric(10, 4), nullable=False)  # Cantidad prevista
    tipo_prevision = Column(SQLEnum('venta', 'proyecto', 'evento', 'promocion', 'otros', name='tipo_prevision'), 
                            nullable=False)  # Tipo de previsión
    origen_datos = Column(String(100))  # Origen de la previsión
    confianza = Column(Float)  # Nivel de confianza en la previsión (0-100%)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsable de la previsión
    
    producto = relationship("Producto")
    responsable = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProgramaMaestroProduccion(Base):
    """Programa maestro de producción - Master production schedule"""
    __tablename__ = "mrp_programa_maestro"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)  # Producto programado
    periodo_inicio = Column(Date, nullable=False)  # Fecha de inicio del período
    periodo_fin = Column(Date, nullable=False)  # Fecha de fin del período
    cantidad_programada = Column(Numeric(10, 4), nullable=False)  # Cantidad programada
    tipo_programa = Column(SQLEnum('demanda_cliente', 'prevision', 'inventario_seguridad', 'muestra', 'otros', name='tipo_programa'), 
                           nullable=False)  # Tipo de programa
    origen = Column(String(100))  # Origen del programa
    estado = Column(SQLEnum('borrador', 'aprobado', 'en_ejecucion', 'cerrado', name='estado_programa'), 
                    default='borrador', nullable=False)  # Estado del programa
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsable del programa
    
    producto = relationship("Producto")
    responsable = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())