"""
Script para depurar errores de importación
"""

def test_imports():
    modules_to_test = [
        "app.models.admin",
        "app.models.hr",
        "app.models.finance",
        "app.models.supply_chain",
        "app.models.production",
        "app.models.inventory",
        "app.models.sales",
        "app.models.invoice",
        "app.models.email_config",
        "app.models.payroll",
        "app.models.agents",
        "app.models.cad",
        "app.models.size_chart",
        "app.models.helpdesk",
        "app.models.requisitions",
        "app.models.notifications",
        "app.models.quality_control",
        "app.models.advanced_accounting",
        "app.models.logistics",
        "app.models.crm",
        "app.models.project_management",
        "app.models.asset_management",
        "app.models.business_intelligence",
        "app.models.reports",
        "app.models.permissions",
        "app.models.security",
        "app.models.mrp",
        "app.models.maintenance",
        "app.models.ai_assistant",
        "app.api.v1",
        "app.api.v1.hr.router",
        "app.api.v1.asset_management.router",
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✓ {module} importado correctamente")
        except ImportError as e:
            print(f"✗ Error al importar {module}: {e}")
        except Exception as e:
            print(f"? Error desconocido al importar {module}: {e}")

if __name__ == "__main__":
    test_imports()