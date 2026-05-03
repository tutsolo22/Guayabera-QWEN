alembic revision --autogenerate -m "Add CuentaBancaria and Transaccion models""""
Test script to verify that all modules import correctly without connecting to database
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

print("Testing imports...")

try:
    # Test main import without initializing DB
    from app.core.config import settings
    print("✓ Core config imported")
    
    from app.core.database import engine, Base, get_db
    print("✓ Database components imported")
    
    from app.core.security import create_access_token, verify_password, get_password_hash, get_current_user
    print("✓ Security components imported")
    
    from app.models.admin import Empresa, Sucursal, Configuracion
    print("✓ Admin models imported")
    
    from app.models.hr import Departamento, Puesto, Empleado
    print("✓ HR models imported")
    
    from app.models.finance import CuentaContable, PolizaContable, CuentaBancaria, Transaccion
    print("✓ Finance models imported")
    
    # Test API routes
    from app.api.v1.admin.router import router as admin_router
    print("✓ Admin router imported")
    
    from app.integration.bank_integration import bank_integration_router
    print("✓ Bank integration router imported")
    
    from app.ai.document_ocr import ocr_router
    print("✓ OCR router imported")
    
    from app.security.compliance import compliance_router
    print("✓ Compliance router imported")
    
    from app.monitoring.health_checks import health_router
    print("✓ Health checks router imported")
    
    # Test services
    from app.services.notification_service import crear_notificacion_pedido_almacen, start_notification_cleanup_scheduler
    print("✓ Notification service imported")
    
    from app.services.cache_service import CacheService
    print("✓ Cache service imported")
    
    print("\n🎉 All imports successful! The application should now start correctly.")
    print("\nTo run the application, make sure:")
    print("1. PostgreSQL database is running on localhost:5432")
    print("2. Redis server is running on localhost:6379")
    print("3. Environment variables are configured in a .env file")
    print("\nYou can start the API with: uvicorn app.main:app --reload")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)