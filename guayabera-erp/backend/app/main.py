from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.middleware.cache_middleware import CacheMiddleware

# Import routers
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.finance import router as finance_router
from app.api.v1.finance.accounting_monitoring import router as monitoring_router
from app.api.v1.agents import router as agents_router
from app.api.v1.supply_chain import router as supply_chain_router
from app.api.v1.production.router import router as production_router
from app.api.v1.hr.router import router as hr_router
from app.api.v1.sales.router import router as sales_router
from app.api.v1.cad.router import router as cad_router
from app.api.v1.size_chart.router import router as size_chart_router
from app.api.v1.helpdesk.router import router as helpdesk_router
from app.api.v1.requisitions.router import router as requisitions_router
from app.api.v1.notifications.router import router as notifications_router
from app.api.v1.quality_control.router import router as quality_control_router
from app.api.v1.advanced_accounting.router import router as advanced_accounting_router
from app.api.v1.logistics.router import router as logistics_router
from app.api.v1.crm.router import router as crm_router
from app.api.v1.project_management.router import router as project_management_router
from app.api.v1.asset_management.router import router as asset_management_router
from app.api.v1.business_intelligence.router import router as business_intelligence_router
from app.api.v1.invoice.router import router as invoice_router
from app.api.v1.email_config.router import router as email_config_router
from app.api.v1.payroll.router import router as payroll_router
from app.api.v1.reports.router import router as reports_router
from app.api.v1.permissions.router import router as permissions_router
from app.api.v1.ai_assistant.router import router as ai_assistant_router

# Context manager for lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown: Cleanup if needed
    print("👋 Shutting down GuayaberaERP")

# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Cache Middleware
app.add_middleware(
    CacheMiddleware,
    cache_ttl=300,  # 5 minutes
    exclude_patterns=["/api/v1/auth", "/api/v1/invoice", "/api/v1/payroll"]  # Don't cache auth and transactional endpoints
)

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "guayabera-erp-backend"}

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "GuayaberaERP API",
        "version": settings.VERSION,
        "status": "running"
    }

# API Routes grouped by module
app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(admin_router, prefix=settings.API_V1_STR, tags=["Administration"])
app.include_router(finance_router, prefix=settings.API_V1_STR, tags=["Finance"])
app.include_router(monitoring_router, prefix=settings.API_V1_STR, tags=["Accounting Monitoring"])
app.include_router(agents_router, prefix=settings.API_V1_STR, tags=["Local Agents"])
app.include_router(supply_chain_router, prefix=settings.API_V1_STR, tags=["Supply Chain"])
app.include_router(production_router, prefix=settings.API_V1_STR, tags=["Production"])
app.include_router(hr_router, prefix=settings.API_V1_STR, tags=["Human Resources"])
app.include_router(sales_router, prefix=settings.API_V1_STR, tags=["Sales"])
app.include_router(cad_router, prefix=settings.API_V1_STR, tags=["CAD Design"])
app.include_router(size_chart_router, prefix=settings.API_V1_STR, tags=["Size Charts"])
app.include_router(helpdesk_router, prefix=settings.API_V1_STR, tags=["Helpdesk"])
app.include_router(requisitions_router, prefix=settings.API_V1_STR, tags=["Requisitions"])
app.include_router(notifications_router, prefix=settings.API_V1_STR, tags=["Notifications"])
app.include_router(quality_control_router, prefix=settings.API_V1_STR, tags=["Quality Control"])
app.include_router(advanced_accounting_router, prefix=settings.API_V1_STR, tags=["Advanced Accounting"])
app.include_router(logistics_router, prefix=settings.API_V1_STR, tags=["Logistics"])
app.include_router(crm_router, prefix=settings.API_V1_STR, tags=["CRM"])
app.include_router(project_management_router, prefix=settings.API_V1_STR, tags=["Project Management"])
app.include_router(asset_management_router, prefix=settings.API_V1_STR, tags=["Asset Management"])
app.include_router(business_intelligence_router, prefix=settings.API_V1_STR, tags=["Business Intelligence"])
app.include_router(invoice_router, prefix=settings.API_V1_STR, tags=["Electronic Invoicing"])
app.include_router(email_config_router, prefix=settings.API_V1_STR, tags=["Email Configuration"])
app.include_router(payroll_router, prefix=settings.API_V1_STR, tags=["Electronic Payroll"])
app.include_router(reports_router, prefix=settings.API_V1_STR, tags=["Reports"])
app.include_router(permissions_router, prefix=settings.API_V1_STR, tags=["Permissions"])
app.include_router(ai_assistant_router, prefix=settings.API_V1_STR, tags=["AI Assistant"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)