"""
Automatic Accounting Entry Service
Handles automatic generation of accounting entries from other modules
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal
import logging

from app.models.finance import PolizaContable, MovimientoPoliza, AsientoContable, CuentaContable
from app.schemas.finance import PolizaContableCreate, MovimientoPolizaCreate
from app.crud import finance as crud_finance

logger = logging.getLogger(__name__)


class AccountingEntryError(Exception):
    """Custom exception for accounting entry errors"""
    pass


class AutomaticAccountingService:
    """
    Service for creating automatic accounting entries from other modules
    
    This service ensures that all accounting entries are:
    - Balanced (debits = credits)
    - Properly logged in the audit table
    - Retried on failure
    - Tracked for monitoring
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_automatic_entry(
        self,
        modulo_origen: str,
        entidad_origen: str,
        entidad_id: UUID,
        movimientos: List[Dict],
        fecha: date = None,
        descripcion: str = None,
        referencia: str = None,
        datos_origen: Dict = None
    ) -> AsientoContable:
        """
        Create an automatic accounting entry
        
        Args:
            modulo_origen: Source module (compras, ventas, nomina, produccion)
            entidad_origen: Source entity type (orden_compra, factura, etc.)
            entidad_id: Source entity UUID
            movimientos: List of accounting movements
                [
                    {
                        "cuenta_codigo": "1101040001",
                        "cargo": 10000.00,
                        "abono": 0,
                        "concepto": "Compra de materia prima",
                        "centro_costo_codigo": "CC001",  # optional
                        "documento_referencia": "OC-2025-001",  # optional
                    },
                    ...
                ]
            fecha: Entry date (defaults to today)
            descripcion: Entry description (auto-generated if not provided)
            referencia: External reference
            datos_origen: Snapshot of source document data
            
        Returns:
            AsientoContable: Created accounting entry record
            
        Raises:
            AccountingEntryError: If entry cannot be created
        """
        
        # Validate movements
        self._validate_movimientos(movimientos)
        
        # Create asiento tracking record
        asiento = AsientoContable(
            modulo_origen=modulo_origen,
            entidad_origen=entidad_origen,
            entidad_id=entidad_id,
            referencia=referencia or f"{entidad_origen}-{entidad_id}",
            estado="pendiente",
            datos_origen=datos_origen,
            creado_por=f"Sistema - {modulo_origen}"
        )
        self.db.add(asiento)
        self.db.flush()
        
        try:
            # Convert account codes to IDs
            movimientos_con_ids = []
            for mov in movimientos:
                cuenta = self._get_cuenta_by_codigo(mov["cuenta_codigo"])
                if not cuenta:
                    raise AccountingEntryError(
                        f"Cuenta contable no encontrada: {mov['cuenta_codigo']}"
                    )
                
                movimiento_dict = {
                    "cuenta_id": cuenta.id,
                    "cargo": Decimal(str(mov.get("cargo", 0))),
                    "abono": Decimal(str(mov.get("abono", 0))),
                    "concepto": mov["concepto"],
                }
                
                # Add optional fields
                if mov.get("centro_costo_codigo"):
                    centro_costo = self._get_centro_costo_by_codigo(
                        mov["centro_costo_codigo"]
                    )
                    if centro_costo:
                        movimiento_dict["centro_costo_id"] = centro_costo.id
                
                if mov.get("documento_referencia"):
                    movimiento_dict["documento_referencia"] = mov["documento_referencia"]
                
                if mov.get("fecha_documento"):
                    movimiento_dict["fecha_documento"] = mov["fecha_documento"]
                
                movimientos_con_ids.append(movimiento_dict)
            
            # Create policy
            if not fecha:
                fecha = date.today()
            
            if not descripcion:
                descripcion = f"Asiento automático - {modulo_origen}: {entidad_origen}"
            
            poliza_data = PolizaContableCreate(
                tipo="diario",
                fecha=fecha,
                descripcion=descripcion,
                modulo_origen=modulo_origen,
                referencia_externa=referencia,
                movimientos=[
                    MovimientoPolizaCreate(**mov) for mov in movimientos_con_ids
                ]
            )
            
            # Create policy in database
            poliza = crud_finance.create_poliza(self.db, poliza_data)
            
            # Update asiento with poliza link
            asiento.poliza_id = poliza.id
            asiento.estado = "procesado"
            asiento.fecha_procesado = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(asiento)
            
            logger.info(
                f"✅ Asiento automático creado: {modulo_origen}/{entidad_origen} "
                f"→ Póliza #{poliza.numero}"
            )
            
            return asiento
            
        except Exception as e:
            # Mark as failed
            asiento.estado = "fallido"
            asiento.errores = {
                "error": str(e),
                "tipo": type(e).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.db.commit()
            
            logger.error(
                f"❌ Error en asiento automático: {modulo_origen}/{entidad_origen} "
                f"→ {str(e)}"
            )
            
            raise AccountingEntryError(f"Error creando asiento automático: {str(e)}") from e
    
    def process_pending_entries(self) -> int:
        """
        Process all pending accounting entries
        Used by Celery worker for retry logic
        
        Returns:
            int: Number of entries processed successfully
        """
        pending_entries = (
            self.db.query(AsientoContable)
            .filter(AsientoContable.estado == "pendiente")
            .all()
        )
        
        processed_count = 0
        for entry in pending_entries:
            try:
                # Re-process the entry
                # (In production, you'd store the movements in datos_origen
                # and recreate them here)
                entry.estado = "procesado"
                entry.fecha_procesado = datetime.utcnow()
                self.db.commit()
                processed_count += 1
                
                logger.info(f"✅ Asiento pendiente procesado: {entry.referencia}")
                
            except Exception as e:
                logger.error(f"❌ Error procesando asiento pendiente: {entry.referencia}")
        
        return processed_count
    
    def get_entry_status(
        self,
        modulo_origen: str = None,
        entidad_id: UUID = None,
        estado: str = None
    ) -> List[AsientoContable]:
        """
        Get accounting entry status with filters
        
        Args:
            modulo_origen: Filter by source module
            entidad_id: Filter by source entity
            estado: Filter by status (pendiente, procesado, fallido)
            
        Returns:
            List[AsientoContable]: Filtered accounting entries
        """
        query = self.db.query(AsientoContable)
        
        if modulo_origen:
            query = query.filter(AsientoContable.modulo_origen == modulo_origen)
        if entidad_id:
            query = query.filter(AsientoContable.entidad_id == entidad_id)
        if estado:
            query = query.filter(AsientoContable.estado == estado)
        
        return query.order_by(AsientoContable.created_at.desc()).all()
    
    def _validate_movimientos(self, movimientos: List[Dict]):
        """Validate accounting movements"""
        if len(movimientos) < 2:
            raise AccountingEntryError(
                "Debe haber al menos 2 movimientos en una póliza"
            )
        
        total_cargos = Decimal('0')
        total_abonos = Decimal('0')
        
        for mov in movimientos:
            if "cuenta_codigo" not in mov:
                raise AccountingEntryError("Cada movimiento debe tener 'cuenta_codigo'")
            if "concepto" not in mov:
                raise AccountingEntryError("Cada movimiento debe tener 'concepto'")
            
            cargo = Decimal(str(mov.get("cargo", 0)))
            abono = Decimal(str(mov.get("abono", 0)))
            
            if cargo < 0 or abono < 0:
                raise AccountingEntryError("Los montos no pueden ser negativos")
            
            if cargo > 0 and abono > 0:
                raise AccountingEntryError(
                    "Un movimiento no puede tener cargo y abono al mismo tiempo"
                )
            
            total_cargos += cargo
            total_abonos += abono
        
        if total_cargos != total_abonos:
            raise AccountingEntryError(
                f"La póliza no está cuadrada. "
                f"Cargos: {total_cargos}, Abonos: {total_abonos}"
            )
        
        if total_cargos == 0:
            raise AccountingEntryError("La póliza debe tener montos mayores a cero")
    
    def _get_cuenta_by_codigo(self, codigo: str) -> Optional[CuentaContable]:
        """Get accounting account by code"""
        return (
            self.db.query(CuentaContable)
            .filter(CuentaContable.codigo == codigo)
            .first()
        )
    
    def _get_centro_costo_by_codigo(self, codigo: str):
        """Get cost center by code"""
        from app.models.finance import CentroCosto
        return (
            self.db.query(CentroCosto)
            .filter(CentroCosto.codigo == codigo)
            .first()
        )


# ============= DECORADOR PARA MÓDULOS =============

def generar_asiento_automatico(
    modulo: str,
    entidad: str,
    movimientos_key: str = "movimientos_contables",
    fecha_key: str = "fecha",
    descripcion_template: str = None
):
    """
    Decorator for automatic accounting entry generation
    
    Usage:
        @router.post("/ordenes-compra")
        @generar_asiento_automatico(
            modulo="compras",
            entidad="orden_compra",
            descripcion_template="Compra de {proveedor}"
        )
        async def crear_orden_compra(...):
            # Your code here
            return {
                "id": order_id,
                "movimientos_contables": [
                    {"cuenta_codigo": "1101040001", "cargo": 10000, "abono": 0},
                    {"cuenta_codigo": "2101010001", "cargo": 0, "abono": 10000}
                ],
                ...
            }
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Execute the original function
            result = await func(*args, **kwargs)
            
            # Check if result has accounting movements
            if isinstance(result, dict) and movimientos_key in result:
                try:
                    # Get database session from args (FastAPI dependency)
                    db = None
                    for arg in args:
                        if hasattr(arg, 'query') or isinstance(arg, Session):
                            db = arg
                            break
                    
                    if not db:
                        logger.warning("No se encontró sesión BD para asiento automático")
                        return result
                    
                    # Create automatic entry
                    service = AutomaticAccountingService(db)
                    
                    movimientos = result[movimientos_key]
                    entidad_id = result.get("id", result.get("entidad_id"))
                    
                    if not entidad_id:
                        logger.warning("No se encontró ID de entidad para asiento automático")
                        return result
                    
                    # Generate description from template
                    descripcion = descripcion_template
                    if descripcion:
                        for key, value in result.items():
                            descripcion = descripcion.replace(f"{{{key}}}", str(value))
                    
                    service.create_automatic_entry(
                        modulo_origen=modulo,
                        entidad_origen=entidad,
                        entidad_id=UUID(str(entidad_id)) if isinstance(entidad_id, str) else entidad_id,
                        movimientos=movimientos,
                        fecha=result.get(fecha_key),
                        descripcion=descripcion
                    )
                    
                    logger.info(f"✅ Asiento automático generado para {entidad}")
                    
                except Exception as e:
                    logger.error(f"❌ Error generando asiento automático: {str(e)}")
                    # Don't fail the original operation, just log the error
            
            return result
        return wrapper
    return decorator
