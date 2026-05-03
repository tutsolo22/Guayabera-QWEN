from fastapi import APIRouter
from app.api.v1.admin.router import router as admin_router
from app.api.v1.hr.router import router as hr_router
from app.api.v1.finance.router import router as finance_router
from app.api.v1.supply_chain.router import router as supply_chain_router
from app.api.v1.production.router import router as production_router
from app.api.v1.inventory.router import router as inventory_router
from app.api.v1.sales.router import router as sales_router
from app.api.v1.invoice.router import router as invoice_router
from app.api.v1.payroll.router import router as payroll_router
from app.api.v1.agents.router import router as agents_router
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
from app.api.v1.reports.router import router as reports_router
from app.api.v1.permissions.router import router as permissions_router
from app.api.v1.email_config.router import router as email_config_router
from app.api.v1.mrp.router import router as mrp_router
from app.api.v1.maintenance.router import router as maintenance_router
from app.api.v1.ai_assistant.router import router as ai_assistant_router

router = APIRouter()

# Incluir todos los routers
router.include_router(admin_router)
router.include_router(hr_router)
router.include_router(finance_router)
router.include_router(supply_chain_router)
router.include_router(production_router)
router.include_router(inventory_router)
router.include_router(sales_router)
router.include_router(invoice_router)
router.include_router(payroll_router)
router.include_router(agents_router)
router.include_router(cad_router)
router.include_router(size_chart_router)
router.include_router(helpdesk_router)
router.include_router(requisitions_router)
router.include_router(notifications_router)
router.include_router(quality_control_router)
router.include_router(advanced_accounting_router)
router.include_router(logistics_router)
router.include_router(crm_router)
router.include_router(project_management_router)
router.include_router(asset_management_router)
router.include_router(business_intelligence_router)
router.include_router(reports_router)
router.include_router(permissions_router)
router.include_router(email_config_router)
router.include_router(mrp_router)
router.include_router(maintenance_router)
router.include_router(ai_assistant_router)