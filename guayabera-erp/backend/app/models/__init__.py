from app.core.database import Base

# Evitar importaciones circulares definiendo explícitamente qué se exporta
# Solo incluimos aquí los modelos esenciales para evitar problemas
# El resto se importan explícitamente donde se necesiten

# Definir explícitamente los elementos que se van a exportar
__all__ = [
    "Base",
    # Modelos administrativos
    "Empresa", "Sucursal", "Configuracion", "Moneda", "Impuesto",
    # Modelos de recursos humanos
    "Departamento", "Puesto", "Empleado",
    # Modelos de finanzas
    "CuentaContable", "CentroCosto", "PolizaContable", "MovimientoPoliza", 
    "Banco", "MovimientoBancario", "AsientoContable", "PeriodoContable",
    "CuentaBancaria", "Transaccion",  # Modelos añadidos recientemente
    # Modelos de inventario
    "Producto", "CategoriaProducto", "UnidadMedida", "Existencia", "MovimientoInventario",
    # Modelos de ventas
    "Cliente", "Cotizacion", "Pedido", "OrdenVenta", "MetodoPago",
    # Modelos de seguridad
    "Usuario", "Rol", "Permiso",
    # Modelos de CRM
    "Customer", "Contact", "Interaction", "SalesOpportunity", "SalesStage", "Task", "Note", "Tag"
]

# Importaciones específicas para evitar problemas circulares
# Estas se pueden usar en otros archivos que necesiten acceso directo a modelos específicos
def _import_models():
    """Función auxiliar para importar modelos sin causar problemas circulares"""
    try:
        from .admin import Empresa, Sucursal, Configuracion, Moneda, Impuesto
        from .hr import Departamento, Puesto, Empleado
        from .finance import (
            CuentaContable, CentroCosto, PolizaContable, MovimientoPoliza, 
            Banco, MovimientoBancario, AsientoContable, PeriodoContable,
            CuentaBancaria, Transaccion
        )
        from .inventory import Producto, CategoriaProducto, UnidadMedida, Existencia, MovimientoInventario
        from .sales import Cliente, Cotizacion, Pedido, OrdenVenta, MetodoPago
        from .security import Usuario, Rol, Permiso
        from .crm import Customer, Contact, Interaction, SalesOpportunity, SalesStage, Task, Note, Tag
        
        # Hacer que estén disponibles en el módulo
        globals().update(locals())
    except ImportError as e:
        # Si hay problemas de importación, no hacer nada
        # Esto permite que el módulo se cargue aunque haya dependencias pendientes
        pass

# Ejecutar la importación
_import_models()