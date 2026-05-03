from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router
from app.core.config import settings
from app.core.database import engine, Base
from app.middleware.cache_middleware import CacheMiddleware
from app.services.notification_service import start_notification_cleanup_scheduler
from app.monitoring.health_checks import health_router
from app.security.compliance import compliance_router
from app.ai.document_ocr import ocr_router
from app.integration.bank_integration import bank_integration_router
from app.services.permission_initializer import initialize_all_permissions
from sqlalchemy.orm import sessionmaker
import asyncio

# Importar modelos para que SQLAlchemy los registre
from app.models.admin import *
from app.models.hr import *
from app.models.finance import *
from app.models.supply_chain import *
from app.models.production import *
from app.models.inventory import *
from app.models.sales import *
from app.models.invoice import *
from app.models.email_config import *
from app.models.payroll import *
from app.models.agents import *
from app.models.cad import *
from app.models.size_chart import *
from app.models.helpdesk import *
from app.models.requisitions import *
from app.models.notifications import *
from app.models.quality_control import *
from app.models.advanced_accounting import *
from app.models.logistics import *
from app.models.crm import *
from app.models.project_management import *
from app.models.asset_management import *
from app.models.business_intelligence import *
from app.models.reports import *
from app.models.permissions import *
from app.models.security import *
from app.models.mrp import *
from app.models.maintenance import *
from app.models.ai_assistant import *

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Iniciar el planificador de limpieza de notificaciones
start_notification_cleanup_scheduler()

app = FastAPI(
    title=settings.APP_NAME,
    description="ERP para la industria de la confección, con módulos de administración, contabilidad, recursos humanos, ventas, inventario, producción, cadena de suministro, calidad, logística, CRM, inteligencia de negocios, agentes de IA, diseño asistido y más.",
    version=settings.API_V1_STR
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de caché
app.add_middleware(CacheMiddleware)

# Incluir routers
app.include_router(router, prefix=settings.API_V1_STR)
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(compliance_router, prefix="/compliance", tags=["compliance"])
app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])
app.include_router(bank_integration_router, prefix="/bank-integration", tags=["bank-integration"])

@app.on_event("startup")
async def startup_event():
    # Inicializar permisos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        initialize_all_permissions(db)
    finally:
        db.close()
    
    print("Aplicación iniciada correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicación cerrada correctamente")

@app.get("/")
def read_root():
    return {"message": f"Bienvenido a {settings.APP_NAME}", "version": settings.API_V1_STR}