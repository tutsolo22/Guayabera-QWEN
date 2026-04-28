# GuayaberaERP - Backend

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models import Base

# Import routers
from app.api.v1.admin import router as admin_router
from app.api.v1.finance import router as finance_router
from app.api.v1.finance.accounting_monitoring import router as monitoring_router
from app.api.v1.auth import router as auth_router
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
from app.api.v1.reports.router import router as reports_router  # Nuevo router de reportes
from app.api.v1.permissions.router import router as permissions_router  # Nuevo router de permisos

# Import middleware
from app.middleware.cache_middleware import CacheMiddleware

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown: Cleanup if needed
    print("👋 Shutting down GuayaberaERP")


app = FastAPI(
    title="GuayaberaERP API",
    description="ERP Textil especializado en guayaberas yucatecas",
    version="0.1.0",
    lifespan=lifespan
)

# Add Cache Middleware
app.add_middleware(
    CacheMiddleware,
    cache_ttl=300,  # 5 minutes
    exclude_patterns=["/api/v1/auth", "/api/v1/invoice", "/api/v1/payroll"]  # Don't cache auth and transactional endpoints
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "GuayaberaERP API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    from app.monitoring.health_checks import monitor
    from app.core.database import get_db
    
    db = next(get_db())
    try:
        report = monitor.get_detailed_health_report(db)
        return report
    finally:
        db.close()


@app.get("/performance-metrics")
async def performance_metrics():
    """Get performance metrics"""
    from app.monitoring.health_checks import monitor
    from app.core.database import get_db
    
    db = next(get_db())
    try:
        metrics = monitor.get_performance_metrics(db)
        return metrics
    finally:
        db.close()


# API Routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Administration"])
app.include_router(finance_router, prefix="/api/v1/finance", tags=["Finance"])
app.include_router(monitoring_router, prefix="/api/v1/finance", tags=["Accounting Monitoring"])
app.include_router(agents_router, prefix="/api/v1/agents", tags=["Local Agents"])
app.include_router(supply_chain_router, prefix="/api/v1/supply-chain", tags=["Supply Chain"])
app.include_router(production_router, prefix="/api/v1/production", tags=["Production"])
app.include_router(hr_router, prefix="/api/v1/hr", tags=["Human Resources"])
app.include_router(sales_router, prefix="/api/v1/sales", tags=["Sales"])
app.include_router(cad_router, prefix="/api/v1/cad", tags=["CAD Design"])
app.include_router(size_chart_router, prefix="/api/v1/size-chart", tags=["Size Charts"])
app.include_router(helpdesk_router, prefix="/api/v1/helpdesk", tags=["Helpdesk"])
app.include_router(requisitions_router, prefix="/api/v1/requisitions", tags=["Requisitions"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(quality_control_router, prefix="/api/v1/quality-control", tags=["Quality Control"])
app.include_router(advanced_accounting_router, prefix="/api/v1/advanced-accounting", tags=["Advanced Accounting"])
app.include_router(logistics_router, prefix="/api/v1/logistics", tags=["Logistics"])
app.include_router(crm_router, prefix="/api/v1/crm", tags=["CRM"])
app.include_router(project_management_router, prefix="/api/v1/project-management", tags=["Project Management"])
app.include_router(asset_management_router, prefix="/api/v1/asset-management", tags=["Asset Management"])
app.include_router(business_intelligence_router, prefix="/api/v1/business-intelligence", tags=["Business Intelligence"])
app.include_router(invoice_router, prefix="/api/v1/invoice", tags=["Electronic Invoicing"])
app.include_router(email_config_router, prefix="/api/v1/email-config", tags=["Email Configuration"])
app.include_router(payroll_router, prefix="/api/v1/payroll", tags=["Electronic Payroll"])
app.include_router(reports_router, prefix="/api/v1/reports", tags=["Reports"])  # Nuevo router de reportes
app.include_router(permissions_router, prefix="/api/v1/permissions", tags=["Permissions"])  # Nuevo router de permisos


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)