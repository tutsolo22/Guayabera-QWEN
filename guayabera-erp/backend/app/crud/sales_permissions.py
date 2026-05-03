"""
Sales Module Permissions: Permissions and roles management for sales configuration module
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
import enum

from app.models.permissions import Permiso, Rol, PermisoRol
from app.crud.permissions import (
    create_permiso, 
    get_permiso_by_nombre, 
    create_permiso_rol,
    get_permisos_by_rol
)


class SalesPermissionsEnum(str, enum.Enum):
    """Sales module specific permissions"""
    # Sales configuration permissions
    VER_CONFIGURACION_VENTAS = "ver_configuracion_ventas"
    EDITAR_CONFIGURACION_VENTAS = "editar_configuracion_ventas"
    
    # Discount rules permissions
    VER_REGLAS_DESCUENTO = "ver_reglas_descuento"
    CREAR_REGLAS_DESCUENTO = "crear_reglas_descuento"
    EDITAR_REGLAS_DESCUENTO = "editar_reglas_descuento"
    ELIMINAR_REGLAS_DESCUENTO = "eliminar_reglas_descuento"
    
    # Loyalty programs permissions
    VER_PROGRAMAS_LEALTAD = "ver_programas_lealtad"
    CREAR_PROGRAMAS_LEALTAD = "crear_programas_lealtad"
    EDITAR_PROGRAMAS_LEALTAD = "editar_programas_lealtad"
    ELIMINAR_PROGRAMAS_LEALTAD = "eliminar_programas_lealtad"
    
    # Price lists permissions
    VER_LISTAS_PRECIOS = "ver_listas_precios"
    CREAR_LISTAS_PRECIOS = "crear_listas_precios"
    EDITAR_LISTAS_PRECIOS = "editar_listas_precios"
    ELIMINAR_LISTAS_PRECIOS = "eliminar_listas_precios"


def initialize_sales_permissions(db: Session):
    """Initialize sales module permissions in the database"""
    
    # Sales configuration permissions
    sales_config_perms = [
        {
            "nombre": "ver_configuracion_ventas",
            "descripcion": "Ver configuración general del módulo de ventas",
            "modulo": "ventas",
            "tipo": "consulta"
        },
        {
            "nombre": "editar_configuracion_ventas",
            "descripcion": "Editar configuración general del módulo de ventas",
            "modulo": "ventas",
            "tipo": "editar"
        }
    ]
    
    # Discount rules permissions
    discount_perms = [
        {
            "nombre": "ver_reglas_descuento",
            "descripcion": "Ver reglas de descuento",
            "modulo": "ventas",
            "tipo": "consulta"
        },
        {
            "nombre": "crear_reglas_descuento",
            "descripcion": "Crear nuevas reglas de descuento",
            "modulo": "ventas",
            "tipo": "crear"
        },
        {
            "nombre": "editar_reglas_descuento",
            "descripcion": "Editar reglas de descuento existentes",
            "modulo": "ventas",
            "tipo": "editar"
        },
        {
            "nombre": "eliminar_reglas_descuento",
            "descripcion": "Eliminar reglas de descuento",
            "modulo": "ventas",
            "tipo": "eliminar"
        }
    ]
    
    # Loyalty programs permissions
    loyalty_perms = [
        {
            "nombre": "ver_programas_lealtad",
            "descripcion": "Ver programas de lealtad",
            "modulo": "ventas",
            "tipo": "consulta"
        },
        {
            "nombre": "crear_programas_lealtad",
            "descripcion": "Crear nuevos programas de lealtad",
            "modulo": "ventas",
            "tipo": "crear"
        },
        {
            "nombre": "editar_programas_lealtad",
            "descripcion": "Editar programas de lealtad existentes",
            "modulo": "ventas",
            "tipo": "editar"
        },
        {
            "nombre": "eliminar_programas_lealtad",
            "descripcion": "Eliminar programas de lealtad",
            "modulo": "ventas",
            "tipo": "eliminar"
        }
    ]
    
    # Price lists permissions
    price_list_perms = [
        {
            "nombre": "ver_listas_precios",
            "descripcion": "Ver listas de precios",
            "modulo": "ventas",
            "tipo": "consulta"
        },
        {
            "nombre": "crear_listas_precios",
            "descripcion": "Crear nuevas listas de precios",
            "modulo": "ventas",
            "tipo": "crear"
        },
        {
            "nombre": "editar_listas_precios",
            "descripcion": "Editar listas de precios existentes",
            "modulo": "ventas",
            "tipo": "editar"
        },
        {
            "nombre": "eliminar_listas_precios",
            "descripcion": "Eliminar listas de precios",
            "modulo": "ventas",
            "tipo": "eliminar"
        }
    ]
    
    # Combine all permissions
    all_perms = sales_config_perms + discount_perms + loyalty_perms + price_list_perms
    
    # Create permissions if they don't exist
    for perm_data in all_perms:
        existing_perm = get_permiso_by_nombre(db, perm_data["nombre"])
        if not existing_perm:
            create_permiso(db, Permiso(**perm_data))


def assign_sales_permissions_to_role(db: Session, rol_id: UUID):
    """Assign all sales configuration permissions to a specific role"""
    
    # Get all sales permissions
    sales_permissions = [
        "ver_configuracion_ventas",
        "editar_configuracion_ventas",
        "ver_reglas_descuento",
        "crear_reglas_descuento",
        "editar_reglas_descuento",
        "eliminar_reglas_descuento",
        "ver_programas_lealtad",
        "crear_programas_lealtad",
        "editar_programas_lealtad",
        "eliminar_programas_lealtad",
        "ver_listas_precios",
        "crear_listas_precios",
        "editar_listas_precios",
        "eliminar_listas_precios",
    ]
    
    # Assign each permission to the role
    for perm_name in sales_permissions:
        perm = get_permiso_by_nombre(db, perm_name)
        if perm:
            # Check if association already exists
            existing_assoc = db.query(PermisoRol).filter(
                PermisoRol.rol_id == rol_id,
                PermisoRol.permiso_id == perm.id
            ).first()
            
            if not existing_assoc:
                assoc_data = PermisoRol(rol_id=rol_id, permiso_id=perm.id)
                db.add(assoc_data)
    
    db.commit()


def get_sales_permissions_for_role(db: Session, rol_id: UUID) -> List[Permiso]:
    """Get all sales configuration permissions for a specific role"""
    permisos_rol = get_permisos_by_rol(db, rol_id)
    sales_perms = []
    
    for perm_rol in permisos_rol:
        perm = db.query(Permiso).filter(Permiso.id == perm_rol.permiso_id).first()
        if perm and perm.modulo == "ventas":
            sales_perms.append(perm)
    
    return sales_perms