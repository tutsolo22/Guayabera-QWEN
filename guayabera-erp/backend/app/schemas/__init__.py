# Importar todos los esquemas de los diferentes módulos
from . import admin
from . import security
from . import finance
from . import supply_chain
from . import production
from . import hr
from . import sales
from . import inventory
from . import cad
from . import size_chart
from . import helpdesk
from . import requisitions
from . import notifications
from . import quality_control
from . import advanced_accounting
from . import logistics
from . import crm
from . import project_management
from . import asset_management
from . import business_intelligence
from . import invoice
from . import email_config
from . import payroll
from . import agents
from . import permissions
from . import reports
from . import ai_assistant
from . import mrp
from . import maintenance

# Definir __all__ para cada módulo individualmente
try:
    admin_all = admin.__all__ if hasattr(admin, '__all__') else dir(admin)
except AttributeError:
    admin_all = []

try:
    security_all = security.__all__ if hasattr(security, '__all__') else dir(security)
except AttributeError:
    security_all = []

try:
    finance_all = finance.__all__ if hasattr(finance, '__all__') else dir(finance)
except AttributeError:
    finance_all = []

try:
    supply_chain_all = supply_chain.__all__ if hasattr(supply_chain, '__all__') else dir(supply_chain)
except AttributeError:
    supply_chain_all = []

try:
    production_all = production.__all__ if hasattr(production, '__all__') else dir(production)
except AttributeError:
    production_all = []

try:
    hr_all = hr.__all__ if hasattr(hr, '__all__') else dir(hr)
except AttributeError:
    hr_all = []

try:
    sales_all = sales.__all__ if hasattr(sales, '__all__') else dir(sales)
except AttributeError:
    sales_all = []

try:
    inventory_all = inventory.__all__ if hasattr(inventory, '__all__') else dir(inventory)
except AttributeError:
    inventory_all = []

try:
    cad_all = cad.__all__ if hasattr(cad, '__all__') else dir(cad)
except AttributeError:
    cad_all = []

try:
    size_chart_all = size_chart.__all__ if hasattr(size_chart, '__all__') else dir(size_chart)
except AttributeError:
    size_chart_all = []

try:
    helpdesk_all = helpdesk.__all__ if hasattr(helpdesk, '__all__') else dir(helpdesk)
except AttributeError:
    helpdesk_all = []

try:
    requisitions_all = requisitions.__all__ if hasattr(requisitions, '__all__') else dir(requisitions)
except AttributeError:
    requisitions_all = []

try:
    notifications_all = notifications.__all__ if hasattr(notifications, '__all__') else dir(notifications)
except AttributeError:
    notifications_all = []

try:
    quality_control_all = quality_control.__all__ if hasattr(quality_control, '__all__') else dir(quality_control)
except AttributeError:
    quality_control_all = []

try:
    advanced_accounting_all = advanced_accounting.__all__ if hasattr(advanced_accounting, '__all__') else dir(advanced_accounting)
except AttributeError:
    advanced_accounting_all = []

try:
    logistics_all = logistics.__all__ if hasattr(logistics, '__all__') else dir(logistics)
except AttributeError:
    logistics_all = []

try:
    crm_all = crm.__all__ if hasattr(crm, '__all__') else dir(crm)
except AttributeError:
    crm_all = []

try:
    project_management_all = project_management.__all__ if hasattr(project_management, '__all__') else dir(project_management)
except AttributeError:
    project_management_all = []

try:
    asset_management_all = asset_management.__all__ if hasattr(asset_management, '__all__') else dir(asset_management)
except AttributeError:
    asset_management_all = []

try:
    business_intelligence_all = business_intelligence.__all__ if hasattr(business_intelligence, '__all__') else dir(business_intelligence)
except AttributeError:
    business_intelligence_all = []

try:
    invoice_all = invoice.__all__ if hasattr(invoice, '__all__') else dir(invoice)
except AttributeError:
    invoice_all = []

try:
    email_config_all = email_config.__all__ if hasattr(email_config, '__all__') else dir(email_config)
except AttributeError:
    email_config_all = []

try:
    payroll_all = payroll.__all__ if hasattr(payroll, '__all__') else dir(payroll)
except AttributeError:
    payroll_all = []

try:
    agents_all = agents.__all__ if hasattr(agents, '__all__') else dir(agents)
except AttributeError:
    agents_all = []

try:
    permissions_all = permissions.__all__ if hasattr(permissions, '__all__') else dir(permissions)
except AttributeError:
    permissions_all = []

try:
    reports_all = reports.__all__ if hasattr(reports, '__all__') else dir(reports)
except AttributeError:
    reports_all = []

try:
    ai_assistant_all = ai_assistant.__all__ if hasattr(ai_assistant, '__all__') else dir(ai_assistant)
except AttributeError:
    ai_assistant_all = []

try:
    mrp_all = mrp.__all__ if hasattr(mrp, '__all__') else dir(mrp)
except AttributeError:
    mrp_all = []

try:
    maintenance_all = maintenance.__all__ if hasattr(maintenance, '__all__') else dir(maintenance)
except AttributeError:
    maintenance_all = []


# Definir __all__ combinando todos los elementos
__all__ = (
    admin_all +
    security_all +
    finance_all +
    supply_chain_all +
    production_all +
    hr_all +
    sales_all +
    inventory_all +
    cad_all +
    size_chart_all +
    helpdesk_all +
    requisitions_all +
    notifications_all +
    quality_control_all +
    advanced_accounting_all +
    logistics_all +
    crm_all +
    project_management_all +
    asset_management_all +
    business_intelligence_all +
    invoice_all +
    email_config_all +
    payroll_all +
    agents_all +
    permissions_all +
    reports_all +
    ai_assistant_all +
    mrp_all +
    maintenance_all
)