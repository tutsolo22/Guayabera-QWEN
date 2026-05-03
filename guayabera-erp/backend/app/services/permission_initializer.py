"""
Service to initialize permissions for all modules
"""

from sqlalchemy.orm import Session
from app.crud.sales_permissions import initialize_sales_permissions, assign_sales_permissions_to_role
from app.models.permissions import Rol


def initialize_all_permissions(db: Session):
    """
    Initialize all permissions for all modules
    """
    print("Initializing all module permissions...")
    
    # Initialize sales permissions
    initialize_sales_permissions(db)
    print("Sales permissions initialized")
    
    # Find admin role and assign all permissions
    admin_role = db.query(Rol).filter(Rol.tipo_rol == "ADMINISTRADOR").first()
    if admin_role:
        assign_sales_permissions_to_role(db, admin_role.id)
        print("Sales permissions assigned to admin role")
    
    print("All permissions initialized successfully")


def assign_permissions_to_role(db: Session, rol_id: str):
    """
    Assign all permissions to a specific role
    """
    assign_sales_permissions_to_role(db, rol_id)